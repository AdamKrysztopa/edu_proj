"""The seven analytical lenses (spec §2, §2.8 RESULT). Each lens FIRES on `assertion` (unchanged
by the semantic-judge revision) and returns one `Candidate` per fired seed/anchor/rival-group,
always -- closure is no longer decided here. `Candidate.lexical_state` records what the old
lexical closure test over `T` (searched over the whole A/S pool, F1) would have found, kept only
for comparison (spec S1/S2); the state that actually decides `HYP`/`RG-*` categorisation comes
from `semantic.judge_candidate` downstream. Nothing here writes a claim."""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from residual.ledger import Ledger
from residual.vocab import CRITERION_LABELS, EpistemicLabel, KnowledgeType, SourceKind, Tacitness

from gapmap import config, link, text

PERCEPTUAL_TYPES = {KnowledgeType.FAILURE_MODE, KnowledgeType.CUE, KnowledgeType.CHECK,
                    KnowledgeType.PROCEDURE_STEP, KnowledgeType.INTERPRETATION}
_DIAG_TYPES = {KnowledgeType.FAILURE_MODE, KnowledgeType.CUE, KnowledgeType.INTERPRETATION,
              KnowledgeType.MISCONCEPTION, KnowledgeType.EXPERT_NOVICE_CONTRAST}
_HEDGE_FIRING_TYPES = {KnowledgeType.DECISION, KnowledgeType.NORM, KnowledgeType.STRATEGY,
                       KnowledgeType.PROCEDURE_STEP, KnowledgeType.CHECK}
_WHY_TYPES = {KnowledgeType.PROCEDURE_STEP, KnowledgeType.STRATEGY, KnowledgeType.CHECK,
             KnowledgeType.DECISION, KnowledgeType.NORM}
_RESULT_FIRING_TYPES = {KnowledgeType.PROCEDURE_STEP, KnowledgeType.CHECK, KnowledgeType.STRATEGY,
                        KnowledgeType.DECISION}


@dataclass(frozen=True)
class Alternative:
    text: str
    live: bool
    why: str


@dataclass(frozen=True)
class Candidate:
    lens: str
    anchor: str
    seeds: frozenset[str]
    x_a: frozenset[str]
    rivals: frozenset[str]
    lexical_state: str                       # open | partial | closed | synthetic-closed (comparison only, S1)
    lexical_partial_hits: tuple[str, ...]
    lexical_synthetic_hits: tuple[str, ...]
    s_scope_n: int                           # S claims examined by the lexical test (denominator, kept for display)
    test_id: str
    missing: str
    hypothesis_text: str
    predicted_knowledge_type: tuple[KnowledgeType, ...]
    predicted_tacitness: tuple[Tacitness, ...]
    channel: str
    weak_channel: bool
    question_text: str
    question_targets: tuple[str, ...]
    alternatives: tuple[Alternative, ...]
    excluded: bool = False                   # WHY's logged-not-emitted `authority` exclusion
    promo_penalty: bool = False              # F6: PROMO lexicon live on the span -> -1 to score
    closure_seed_stems: frozenset[str] = frozenset()   # retrieval/null scoring stems: () for DISC/DIAG
    closure_pattern_names: tuple[str, ...] = ()
    closure_exclude: frozenset[str] = frozenset()
    extra: dict = field(default_factory=dict)


def _pool(ledger: Ledger, cid: str) -> str | None:
    lab = ledger.label(cid)
    if lab in CRITERION_LABELS:
        return "A"
    if lab is EpistemicLabel.SYNTHETIC_EXTRAPOLATION:
        return "S"
    return None


# ------------------------------------------------------------------------------- S3 defect 1: PROMO

def promo_blocked(ledger: Ledger, index: link.Index, cid: str) -> bool:
    """S3 defect 1: PROMO is an exclusion for every lens -- a seed sourced from a domain in
    `config.PROMO_DOMAINS`, or whose `T` matches the (expanded) PROMO lexicon, does not fire."""
    if config.PATTERNS["PROMO"].search(index.T[cid]):
        return True
    c = ledger.by_id[cid]
    for e in c.supporting:
        if text.domain(e.source.identifier) in config.PROMO_DOMAINS:
            return True
    return False


def promo_excluded_count(ledger: Ledger, index: link.Index) -> int:
    """The count S3 defect 1 asks to be "logged": how many A claims PROMO excludes from firing."""
    return sum(1 for cid in index.a_ids if promo_blocked(ledger, index, cid))


_BARE_REFERENT = re.compile(r"^\s*(this|these|it|they|such)\b", re.IGNORECASE)


def _flat_sentences(ledger: Ledger, cid: str) -> list[tuple[int, str]]:
    """Every sentence of every evidence span of `cid`, in evidence order, flattened so a
    bare-referent fix (S3 defect 6) can look past its own span's boundary."""
    c = ledger.by_id[cid]
    spans = [e.selector.exact for e in c.supporting if e.selector.exact]
    out = []
    for span in spans:
        out.extend(text.sentences(span))
    return list(enumerate(out))


def _best_sentence(ledger: Ledger, cid: str, relevance_stems: frozenset[str]) -> str:
    """S3 defect 6: prefer the sentence (of any of the seed's own evidence spans, in order)
    containing `relevance_stems`; if it opens with a bare referent, prepend the previous sentence
    even across span boundaries, falling back to the assertion when there is no previous sentence
    at all."""
    c = ledger.by_id[cid]
    sents = _flat_sentences(ledger, cid)
    if not sents:
        return c.assertion
    best_i = 0
    if relevance_stems:
        best_i = max(range(len(sents)), key=lambda i: (len(text.cw(sents[i][1]) & relevance_stems), -i))
        if not (text.cw(sents[best_i][1]) & relevance_stems):
            best_i = 0
    sent = sents[best_i][1]
    if _BARE_REFERENT.match(sent):
        if best_i > 0:
            sent = sents[best_i - 1][1].rstrip() + " " + sent.lstrip()
        else:
            sent = c.assertion
    sent = sent.strip()
    # Fix 5: a quote shorter than 5 words (e.g. "retention periods;") reads as a fragment in a
    # question -- fall back to the claim's own assertion, which is always a full sentence.
    if len(_WORD.findall(sent)) < 5:
        return c.assertion
    return sent


def _pick_quotes(ledger: Ledger, claim_ids, relevance_stems: frozenset[str] = frozenset(),
                 n: int = 2) -> list[tuple[str, str, str]]:
    """Up to `n` verbatim spans from different independence keys (question rule, §2), each
    narrowed to its most relevant sentence (S3 defect 6). Never a testimonial or other PROMO
    source (S3 defect 6)."""
    seen: set[str] = set()
    picked: list[tuple[str, str, str]] = []
    for cid in sorted(claim_ids):
        c = ledger.by_id[cid]
        sup = c.supporting
        if not sup:
            continue
        if text.domain(sup[0].source.identifier) in config.PROMO_DOMAINS:
            continue
        key = sup[0].source.independence_key
        if key in seen:
            continue
        picked.append((cid, key, _best_sentence(ledger, cid, relevance_stems)))
        seen.add(key)
        if len(picked) >= n:
            break
    return picked


def _tacitness_from_x(ledger: Ledger, x_a: frozenset[str]) -> Tacitness:
    if not x_a:
        return Tacitness.COLLECTIVE
    n = sum(1 for cid in x_a if ledger.by_id[cid].knowledge_type in PERCEPTUAL_TYPES)
    return Tacitness.PERCEPTUAL if n / len(x_a) >= 0.5 else Tacitness.COLLECTIVE


def _alt(text_: str, live: bool, why: str) -> Alternative:
    return Alternative(text=text_, live=live, why=why)


def _promo_alt(t: str, text_: str) -> tuple[Alternative, bool]:
    """F6: the PROMO lexicon makes the 'promotional source' alternative live (kept alongside the
    S3 defect 1 hard exclusion above, which runs first and usually leaves nothing here to flag)."""
    promo = bool(config.PATTERNS["PROMO"].search(t))
    why = ("a PROMO lexicon hit on the span." if promo
          else "no PROMO lexicon hit on the span; no ledger field marks promotional voice (§10).")
    return _alt(text_, promo, why), promo


# ------------------------------------------------------------------------ shared lexical closure --

_NAMED_PATTERNS = {"COND": config.PATTERNS["COND"], "EXC": config.PATTERNS["EXC"],
                   "DETECT": config.PATTERNS["DETECT"], "RAT": config.PATTERNS["RAT"],
                   "DISCR": config.PATTERNS["DISCR"], "INTERP": config.PATTERNS["INTERP"],
                   "QUANT": config.PATTERNS["QUANT"]}


def _sentence_matches(sent: str, pattern_names: tuple[str, ...]) -> bool:
    return any(_NAMED_PATTERNS[name].search(sent) for name in pattern_names)


def _closure_hits(index: link.Index, seed_stems: frozenset[str], pattern_names: tuple[str, ...],
                  ids, exclude: frozenset[str] = frozenset()) -> tuple[str, ...]:
    """F1: a claim in `ids` closes iff ONE sentence of its `T` matches one of `pattern_names` AND
    contains >= min(2, |seed_stems|) of `seed_stems` -- the lexical test, kept for comparison
    (S1/S2) and no longer decisive."""
    if not seed_stems:
        return ()
    required = min(2, len(seed_stems))
    hits = []
    for cid in ids:
        if cid in exclude:
            continue
        for sent in text.sentences(index.T[cid]):
            if _sentence_matches(sent, pattern_names) and len(seed_stems & text.cw(sent)) >= required:
                hits.append(cid)
                break
    return tuple(sorted(hits))


def _lexical_state(index: link.Index, seed_stems: frozenset[str], pattern_names: tuple[str, ...],
                   exclude: frozenset[str] = frozenset()) -> tuple[str, tuple[str, ...], tuple[str, ...]]:
    """F1: closed over the A pool, else synthetic-closed over the S pool, else open."""
    a_hits = _closure_hits(index, seed_stems, pattern_names, index.a_ids, exclude)
    if a_hits:
        return "closed", a_hits, ()
    s_hits = _closure_hits(index, seed_stems, pattern_names, index.s_ids)
    if s_hits:
        return "synthetic-closed", (), s_hits
    return "open", (), ()


# ---------------------------------------------------------------------------------- DISC ------

_WORD = re.compile(r"[A-Za-z][A-Za-z0-9']*")


def _judge_anchors(assertion: str) -> list[str]:
    words = [(m.start(), m.end(), m.group(0)) for m in _WORD.finditer(assertion)]
    anchors = []
    for jm in config.PATTERNS["JUDGE"].finditer(assertion):
        term = re.sub(r"[- ]", " ", jm.group(0).lower())
        if term in config.FIXED_ANCHORS:
            anchors.append(term)
            continue
        nxt = next((w for (s, _e, w) in words if s >= jm.end() and w.lower() not in config.STOP), None)
        if nxt:
            anchors.append(f"{term} {text.stem(nxt.lower())}")
    return anchors


_DEFN_BARE = (r"\b{term}\b[^.;]{{0,60}}\b(means|defined as|refers? to|is when|occurs when|covers)\b"
             r"|\bis {term} (when|if)\b")


def _disc_lexical(ledger: Ledger, index: link.Index, anchor: str, seeds: frozenset[str]):
    """§2.1, revised by F4: CASE now closes (not partial), and the bare-term definer is searched
    over the whole A/S pool, not only claims whose `T` contains the anchor bigram. Kept for
    comparison (S1) -- no longer decides state."""
    term, head = anchor.split(" ", 1)
    pat = re.compile(rf"\b{re.escape(term)}[- ]{re.escape(head)}\w*", re.IGNORECASE)
    definer = re.compile(_DEFN_BARE.format(term=re.escape(term)), re.IGNORECASE)
    partial_hits: set[str] = set()
    synth_hits: set[str] = set()
    s_scope: set[str] = set()
    for cid in ledger.by_id:
        pool = _pool(ledger, cid)
        if pool is None:
            continue
        t = index.T[cid]
        matches_anchor = pat.search(t) is not None
        if pool == "S" and matches_anchor:
            s_scope.add(cid)
        if pool == "A" and matches_anchor:
            for sent in text.sentences(t):
                if pat.search(sent) and (config.PATTERNS["QUANT"].search(sent)
                                         or config.PATTERNS["CASE"].search(sent)):
                    return "closed", (), (), len(s_scope)
            if cid in seeds and config.PATTERNS["DEFN"].search(t):
                partial_hits.add(cid)
        elif pool == "S" and matches_anchor:
            for sent in text.sentences(t):
                if pat.search(sent) and config.PATTERNS["QUANT"].search(sent):
                    synth_hits.add(cid)
        if pool == "A" and definer.search(t):
            partial_hits.add(cid)
        elif pool == "S" and definer.search(t):
            synth_hits.add(cid)
    if synth_hits:
        return "synthetic-closed", tuple(sorted(partial_hits)), tuple(sorted(synth_hits)), len(s_scope)
    if partial_hits:
        return "partial", tuple(sorted(partial_hits)), (), len(s_scope)
    return "open", (), (), len(s_scope)


def disc(ledger: Ledger, index: link.Index, params: link.LinkParams) -> list[Candidate]:
    common = link.common_stems(index, params.common_cut)
    anchor_claims: dict[str, set[str]] = {}
    for cid in index.a_ids:
        if promo_blocked(ledger, index, cid):
            continue
        for anchor in set(_judge_anchors(ledger.by_id[cid].assertion)):
            anchor_claims.setdefault(anchor, set()).add(cid)
    out = []
    for anchor in sorted(anchor_claims):
        if anchor in config.DISC_STOP_ANCHORS:
            continue
        claim_ids = anchor_claims[anchor]
        if len(claim_ids) < config.TERMHOOD_MIN_CLAIMS:
            continue
        seeds = frozenset(claim_ids)
        state, partial_hits, synth_hits, s_scope_n = _disc_lexical(ledger, index, anchor, seeds)
        x_a = link.explicit_part(index, seeds, common, params.shared_threshold)
        norm_share = sum(1 for cid in seeds
                         if ledger.by_id[cid].knowledge_type in (KnowledgeType.NORM, KnowledgeType.CONCEPT))
        live_indeterminacy = norm_share / len(seeds) >= config.INSTITUTIONAL_INDETERMINACY_SHARE
        term = anchor.split(" ", 1)[0]
        kt = ((KnowledgeType.EXPECTANCY,) if term in ("normal", "expected", "baseline")
              else (KnowledgeType.CUE,))
        tacitness = (_tacitness_from_x(ledger, x_a),)
        quotes = _pick_quotes(ledger, seeds, relevance_stems=text.cw(anchor))
        texts = [q[2] for q in quotes if q[2]]
        if len(texts) >= 2:
            lead = f'Two sources write: "{texts[0]}" and "{texts[1]}".'
        elif texts:
            lead = f'One source writes: "{texts[0]}".'
        else:
            lead = "Sources discuss this."
        test_id = f"DISC:{anchor}"
        alts = (
            _alt("The boundary is stated in paraphrase without the anchor string.", True,
                "the anchor-string regex cannot see a paraphrase (the main limitation of DISC, §9)."),
            _alt(f"The term '{anchor}' is institutionally indeterminate, so experts disagree and there "
                f"is nothing to recover.", live_indeterminacy,
                f"{norm_share}/{len(seeds)} anchor claims are typed norm or concept."),
            _alt("The boundary is in unfetched sources.", True, "the ledger is a bounded retrieval."),
        )
        out.append(Candidate(
            lens="DISC", anchor=anchor, seeds=seeds, x_a=x_a, rivals=frozenset(),
            lexical_state=state, lexical_partial_hits=partial_hits, lexical_synthetic_hits=synth_hits,
            s_scope_n=s_scope_n, test_id=test_id, missing=f"a boundary for '{anchor}'",
            hypothesis_text=(f"Hypothesis (inferred): practitioners are predicted to discriminate "
                            f"'{anchor}' from its neighbours by features that no verified claim in "
                            f"this ledger matched test {test_id} for."),
            predicted_knowledge_type=kt, predicted_tacitness=tacitness,
            channel="contrasting-case classification, or expert-rated written vignettes",
            weak_channel=False,
            question_text=(f'{lead} Think of a recent case where you had to judge whether something '
                          f"was {anchor}. Describe one case that clearly was, one that clearly was "
                          f"not, and one that was hard to call. What differed between them, and what "
                          f"did you check first?"),
            question_targets=tuple(cid for cid, _k, _q in quotes),
            alternatives=alts))
    return out


# ---------------------------------------------------------------------------------- DIAG ------

_CAUSE_AFTER = re.compile(r"caused|due|result(?:s|ing)?\s+from|stem|traceable|relate", re.IGNORECASE)
"""§2.2: passive-shaped markers ("Y is caused by X", "Y stems from X") put the cause after the
marker; the active forms ("X causes Y", "X leads to Y") fall to the "otherwise" branch below,
where the cause is what precedes the marker. Broadening "caused" to match "causes"/"cause" would
wrongly flip the common active-voice case, so the literal spec lexicon is kept as given."""


def _split_cause_effect(assertion: str) -> tuple[str, str] | None:
    """Returns (cause, effect)."""
    m = config.PATTERNS["CAUSE"].search(assertion)
    if not m:
        return None
    before, after = assertion[: m.start()], assertion[m.end():]
    return (after, before) if _CAUSE_AFTER.search(m.group(0)) else (before, after)


def _diag_anchor(assertion: str, effect: str) -> str:
    """Fix 4: the effect side from `_split_cause_effect` can start mid-sentence (e.g. "...a common
    cause of X and should be checked during Y" splits right after the marker "cause", giving "of X
    and should be checked during Y" -- a fragment with no leading subject). Anchor on the FULL
    sentence containing the CAUSE marker instead, from its own start, trimmed at a word boundary
    to <= 80 characters. If the effect side itself is too thin (< 3 content words) to describe a
    real effect at all, fall back to the whole (trimmed) seed assertion."""
    if len(text.cw(effect)) < 3:
        return text.trim(assertion, 80)
    m = config.PATTERNS["CAUSE"].search(assertion)
    sent = text.sentence_containing(assertion, m.start()) if m else assertion
    return text.trim(sent, 80)


def _direct_rivals(seed: str, claim_ids: list[str], edge) -> frozenset[str]:
    """§2.2, literal: "a seed plus its rivals is a group" -- the rivals of `seed` are exactly the
    claims `edge`-adjacent to it, not the transitive closure."""
    return frozenset(cid for cid in claim_ids if cid != seed and edge(seed, cid))


def _dedupe_rivals(rivals: frozenset[str], cause_cw: dict[str, frozenset[str]],
                   common: frozenset[str]) -> tuple[str, ...]:
    """S3 defect 3: drop a rival whose cause-stem Jaccard with any already-kept rival is >=
    `DIAG_CAUSE_JACCARD_MAX`, or which shares a non-common cause stem with one -- the same test
    `rival_edge` uses between seed and candidate, applied pairwise among a seed's own direct
    rivals so two near-duplicate rivals (e.g. differing only by a plural the stemmer already folds
    together) do not both surface."""
    kept: list[str] = []
    for r in sorted(rivals):
        r_nc = cause_cw[r] - common
        if any(link.jaccard(cause_cw[r], cause_cw[k]) >= config.DIAG_CAUSE_JACCARD_MAX
              or (r_nc & (cause_cw[k] - common)) for k in kept):
            continue
        kept.append(r)
    return tuple(kept)


def diag(ledger: Ledger, index: link.Index, params: link.LinkParams) -> list[Candidate]:
    common = link.common_stems(index, params.common_cut)
    eligible = [cid for cid in index.a_ids if ledger.by_id[cid].knowledge_type in _DIAG_TYPES
               and _split_cause_effect(ledger.by_id[cid].assertion) and not promo_blocked(ledger, index, cid)]
    split = {cid: _split_cause_effect(ledger.by_id[cid].assertion) for cid in eligible}
    cause_cw = {cid: text.cw(split[cid][0]) for cid in eligible}
    effect_cw = {cid: text.cw(split[cid][1]) for cid in eligible}

    def rival_edge(a: str, b: str) -> bool:
        """F6: rivals need >= 2 shared effect stems, 0 shared non-common cause stems, AND a full
        cause-stem Jaccard below `DIAG_CAUSE_JACCARD_MAX`."""
        eff = len(effect_cw[a] & effect_cw[b])
        shared_nc = (cause_cw[a] - common) & (cause_cw[b] - common)
        jac = link.jaccard(cause_cw[a], cause_cw[b])
        return eff >= 2 and not shared_nc and jac < config.DIAG_CAUSE_JACCARD_MAX

    out = []
    for seed in sorted(eligible):
        direct = _direct_rivals(seed, eligible, rival_edge)
        rivals = _dedupe_rivals(direct, cause_cw, common)  # S3 defect 3 (already sorted)
        if len(rivals) < 2:
            continue
        # F8: build the stems/split dicts from the sorted tuple, not the frozenset below -- a
        # dict comprehension over a frozenset inserts in hash-randomised (per-process) order.
        rival_stems = {r: (cause_cw[r] - common, effect_cw[r] - common) for r in rivals}
        diag_split = {r: split[r] for r in (seed, *rivals)}
        rivals = frozenset(rivals)
        seeds = frozenset({seed})
        x_a = link.explicit_part(index, seeds | rivals, common, params.shared_threshold)
        anchor = _diag_anchor(ledger.by_id[seed].assertion, split[seed][1])  # fix 4
        test_id = f"DIAG:{seed}"
        alts = (
            _alt("The sign exists but is phrased without the cause's stems.", True,
                "lexical linking is the binding constraint (§9, §10)."),
            _alt("The causes co-occur, and experts test rather than discriminate.", True,
                "rival causes need not be mutually exclusive."),
            _alt("The sign is instrument output, not tacit knowledge.", True,
                "DISCR also matches instrument-reported signs."),
        )
        out.append(Candidate(
            lens="DIAG", anchor=anchor, seeds=seeds, x_a=x_a, rivals=rivals,
            lexical_state="open", lexical_partial_hits=(), lexical_synthetic_hits=(), s_scope_n=0,
            test_id=test_id, missing="",  # finalised post-judge, see semantic._judge_diag
            hypothesis_text="",
            predicted_knowledge_type=(KnowledgeType.INTERPRETATION, KnowledgeType.CUE),
            predicted_tacitness=((Tacitness.RELATIONAL, Tacitness.PERCEPTUAL)
                                 if ledger.by_id[seed].knowledge_type is KnowledgeType.CUE
                                 else (Tacitness.RELATIONAL,)),
            channel="CDM probes on a recalled case, then contrasting cases", weak_channel=False,
            question_text="", question_targets=(), alternatives=alts,
            closure_seed_stems=frozenset(), closure_pattern_names=("DISCR",), closure_exclude=frozenset(),
            extra={"diag_rival_stems": rival_stems, "diag_split": diag_split}))
    return out


# ---------------------------------------------------------------------------------- SEL -------

def sel(ledger: Ledger, index: link.Index, params: link.LinkParams) -> list[Candidate]:
    common = link.common_stems(index, params.common_cut)
    out = []
    for cid in index.a_ids:
        c = ledger.by_id[cid]
        if promo_blocked(ledger, index, cid):
            continue
        if not config.PATTERNS["SEL"].search(c.assertion):
            continue
        if not (config.PATTERNS["MODAL"].search(c.assertion) or c.knowledge_type is KnowledgeType.DECISION):
            continue
        seed_stems = index.assertion_cw[cid] - common
        state, partial_hits, s_hits = _lexical_state(index, seed_stems, ("COND",))
        seeds = frozenset({cid})
        x_a = link.explicit_part(index, seeds, common, params.shared_threshold)
        quotes = _pick_quotes(ledger, seeds, relevance_stems=seed_stems)
        s1 = (quotes + [(None, None, c.assertion)])[0]
        test_id = f"SEL:{cid}"
        alts = (
            _alt("The mapping is stated as an example or a comparative that COND does not match.", True,
                "COND is a regex over if/when/comparatives, not every conditional phrasing."),
            _alt("The choice is not a real decision point in practice.", True,
                "a prescriptive assertion need not reflect a live decision."),
        )
        out.append(Candidate(
            lens="SEL", anchor=c.assertion, seeds=seeds, x_a=x_a, rivals=frozenset(),
            lexical_state=state, lexical_partial_hits=partial_hits, lexical_synthetic_hits=s_hits,
            s_scope_n=len(index.s_ids),
            test_id=test_id, missing="a mapping from situation to option",
            hypothesis_text=(f"Hypothesis (inferred): practitioners are predicted to map situations "
                            f"to the choice '{c.assertion}' by conditions that no verified claim in "
                            f"this ledger matched test {test_id} for."),
            predicted_knowledge_type=(KnowledgeType.DECISION,), predicted_tacitness=(Tacitness.RELATIONAL,),
            channel="CDM probes for options considered and the basis of choice", weak_channel=False,
            question_text=(f'"{s1[2]}". Think of the last time you made this choice. Which options did '
                          f"you consider, which did you take, and what about that situation decided it? "
                          f"When did you last choose differently?"),
            question_targets=(cid,), alternatives=alts,
            closure_seed_stems=seed_stems, closure_pattern_names=("COND",), closure_exclude=frozenset()))
    return out


# --------------------------------------------------------------------------------- HEDGE ------

def hedge(ledger: Ledger, index: link.Index, params: link.LinkParams) -> list[Candidate]:
    common = link.common_stems(index, params.common_cut)
    out = []
    for cid in index.a_ids:
        c = ledger.by_id[cid]
        if promo_blocked(ledger, index, cid):
            continue
        if not (config.PATTERNS["MODAL"].search(c.assertion) or c.knowledge_type in _HEDGE_FIRING_TYPES):
            continue
        hm = config.PATTERNS["HEDGE"].search(c.assertion)
        if not hm:
            continue
        rm = config.PATTERNS["RAT"].search(c.assertion)
        if rm and rm.start() < hm.start():
            continue
        seed_stems = index.assertion_cw[cid] - common
        state, partial_hits, s_hits = _lexical_state(index, seed_stems, ("EXC",), exclude=frozenset({cid}))
        seeds = frozenset({cid})
        x_a = link.explicit_part(index, seeds, common, params.shared_threshold)
        quotes = _pick_quotes(ledger, seeds, relevance_stems=seed_stems)
        s1 = (quotes + [(None, None, c.assertion)])[0]
        test_id = f"HEDGE:{cid}"
        alts = (
            _alt("The exception is circular: it restates the judgement.", True,
                "a hedge whose exception re-states the criterion gives no new information."),
            _alt("The hedge is statutory boilerplate with no practice behind it.", True,
                "a hedge in a legal or standard source may carry no field practice."),
            _alt("A trigger is stated inside the seed itself in a form EXC does not match.", True,
                "EXC is a fixed lexicon and misses e.g. 'at least when'."),
        )
        out.append(Candidate(
            lens="HEDGE", anchor=c.assertion, seeds=seeds, x_a=x_a, rivals=frozenset(),
            lexical_state=state, lexical_partial_hits=partial_hits, lexical_synthetic_hits=s_hits,
            s_scope_n=len(index.s_ids),
            test_id=test_id, missing="an exception condition",
            hypothesis_text=(f"Hypothesis (inferred): practitioners are predicted to know the cases "
                            f"in which '{c.assertion}' does not hold; no verified claim in this "
                            f"ledger matched test {test_id}."),
            predicted_knowledge_type=(KnowledgeType.DECISION,),
            predicted_tacitness=((Tacitness.COLLECTIVE,) if c.knowledge_type is KnowledgeType.NORM
                                 else (Tacitness.RELATIONAL,)),
            channel="CDM hypotheticals and boundary-case vignettes", weak_channel=False,
            question_text=(f'"{s1[2]}". Describe a case where this did not hold, or where you decided '
                          f"against it. What about that case told you it was an exception?"),
            question_targets=(cid,), alternatives=alts,
            closure_seed_stems=seed_stems, closure_pattern_names=("EXC",),
            closure_exclude=frozenset({cid})))
    return out


# --------------------------------------------------------------------------------- GUARD ------

def guard(ledger: Ledger, index: link.Index, params: link.LinkParams) -> list[Candidate]:
    common = link.common_stems(index, params.common_cut)
    out = []
    for cid in index.a_ids:
        c = ledger.by_id[cid]
        if promo_blocked(ledger, index, cid):
            continue
        # F6: misconception type alone no longer fires; ERR AND a human agent/action are required.
        if not config.PATTERNS["ERR"].search(c.assertion):
            continue
        if not config.PATTERNS["GUARD_AGENT"].search(c.assertion):
            continue
        seed_stems = index.assertion_cw[cid] - common
        state, partial_hits, s_hits = _lexical_state(index, seed_stems, ("DETECT",))
        seeds = frozenset({cid})
        x_a = link.explicit_part(index, seeds, common, params.shared_threshold)
        t = index.T[cid]
        promo_alt, promo = _promo_alt(t, "The error is a vendor framing, not a practitioner error.")
        quotes = _pick_quotes(ledger, seeds, relevance_stems=seed_stems)
        s1 = (quotes + [(None, None, c.assertion)])[0]
        test_id = f"GUARD:{cid}"
        alts = (
            _alt("The cue is stated in paraphrase.", True, "DETECT is a fixed lexicon."),
            promo_alt,
            _alt("The guard is organisational (a checklist or procedure), not cognitive.", True,
                "a procedural guard need not be an internalised cue."),
        )
        out.append(Candidate(
            lens="GUARD", anchor=c.assertion, seeds=seeds, x_a=x_a, rivals=frozenset(),
            lexical_state=state, lexical_partial_hits=partial_hits, lexical_synthetic_hits=s_hits,
            s_scope_n=len(index.s_ids),
            test_id=test_id, missing="a detection cue",
            hypothesis_text=(f"Hypothesis (inferred): practitioners are predicted to notice "
                            f"{c.assertion} before or as it happens by a check that no verified "
                            f"claim in this ledger matched test {test_id} for. This is an "
                            f"expert-reported error, not an observed learner difficulty."),
            predicted_knowledge_type=(KnowledgeType.CHECK, KnowledgeType.METACOGNITION),
            predicted_tacitness=(Tacitness.AUTOMATED,),
            channel="observation or process tracing first, a retrospective probe over a recorded trace second",
            weak_channel=True,
            question_text=(f'"{s1[2]}". Think of the last time you or a colleague nearly did this or just '
                          f"had. What made you notice? What did you look at?"),
            question_targets=(cid,), alternatives=alts, promo_penalty=promo,
            closure_seed_stems=seed_stems, closure_pattern_names=("DETECT",), closure_exclude=frozenset()))
    return out


# ----------------------------------------------------------------------------------- WHY ------

def why(ledger: Ledger, index: link.Index, params: link.LinkParams) -> list[Candidate]:
    common = link.common_stems(index, params.common_cut)
    out = []
    for cid in index.a_ids:
        c = ledger.by_id[cid]
        if promo_blocked(ledger, index, cid):
            continue
        # F6: seed must be typed procedure_step, strategy, check, decision or norm.
        if c.knowledge_type not in _WHY_TYPES:
            continue
        if any(e.source.kind is SourceKind.STANDARD for e in c.supporting):
            continue
        if not (config.PATTERNS["MODAL"].search(c.assertion) and config.PATTERNS["CONTRA"].search(c.assertion)):
            continue
        if config.PATTERNS["WHY_DISJUNCTION"].search(c.assertion):
            continue  # F6: descriptive "require(s) or (do/does) not require" is not a prescription
        t = index.T[cid]
        if config.PATTERNS["AUTH"].search(t):
            continue  # excluded as authority: logged, not emitted (§2.6) -- never a candidate at all
        seed_stems = index.assertion_cw[cid] - common
        state, partial_hits, s_hits = _lexical_state(index, seed_stems, ("RAT",))
        seeds = frozenset({cid})
        x_a = link.explicit_part(index, seeds, common, params.shared_threshold)
        promo_alt, promo = _promo_alt(t, "The source is promotional.")
        quotes = _pick_quotes(ledger, seeds, relevance_stems=seed_stems)
        s1 = (quotes + [(None, None, c.assertion)])[0]
        test_id = f"WHY:{cid}"
        alts = (
            _alt("The rationale is a purpose clause that RAT does not match.", True,
                "RAT does not match every 'to identify...' purpose clause."),
            promo_alt,
            _alt("The reason is trivial safety knowledge.", True,
                "an omitted rationale may simply be too obvious to state."),
        )
        out.append(Candidate(
            lens="WHY", anchor=c.assertion, seeds=seeds, x_a=x_a, rivals=frozenset(),
            lexical_state=state, lexical_partial_hits=partial_hits, lexical_synthetic_hits=s_hits,
            s_scope_n=len(index.s_ids),
            test_id=test_id, missing="a reason",
            hypothesis_text=(f"Hypothesis (inferred): practitioners are predicted to know why "
                            f"'{c.assertion}'; no verified claim in this ledger matched test "
                            f"{test_id}."),
            predicted_knowledge_type=(KnowledgeType.RATIONALE,), predicted_tacitness=(Tacitness.RELATIONAL,),
            channel="a targeted confirmation question", weak_channel=False,
            question_text=(f'Sources say: "{s1[2]}". What would happen if someone did it differently, '
                          f"and in what situations, if any, is doing it differently acceptable?"),
            question_targets=(cid,), alternatives=alts, promo_penalty=promo,
            closure_seed_stems=seed_stems, closure_pattern_names=("RAT",), closure_exclude=frozenset()))
    return out


# --------------------------------------------------------------------------------- RESULT -----

_RESULT_WINDOW = 6
_RESULT_PRECONDITION = re.compile(r"only (?:be )?performed when|before using", re.IGNORECASE)
"""S3 defect 2: precondition phrasing ("should only be performed when a circuit is de-energized")
is not a prescription that a result feeds an interpretation from -- it is a safety precondition,
excluded regardless of MODAL."""


def _result_prescriptive(assertion: str) -> bool:
    """S3 defect 2: RESULT fires only on a prescriptive test -- MODAL, or an imperative sentence
    that opens with the TEST verb -- never descriptive or precondition text."""
    if _RESULT_PRECONDITION.search(assertion):
        return False
    if config.PATTERNS["MODAL"].search(assertion):
        return True
    m = config.PATTERNS["TEST"].match(assertion.strip())
    return m is not None and m.start() == 0


def _result_anchor(assertion: str, common: frozenset[str]) -> str | None:
    """§2.8: TEST followed within 6 tokens by >= 1 non-common content stem (the object)."""
    m = config.PATTERNS["TEST"].search(assertion)
    if not m:
        return None
    tail = assertion[m.end():]
    window_words = _WORD.findall(tail)[:_RESULT_WINDOW]
    if not (text.cw(" ".join(window_words)) - common):
        return None
    return text.trim(assertion[m.start():], 60)


def result(ledger: Ledger, index: link.Index, params: link.LinkParams) -> list[Candidate]:
    common = link.common_stems(index, params.common_cut)
    out = []
    for cid in index.a_ids:
        c = ledger.by_id[cid]
        if promo_blocked(ledger, index, cid):
            continue
        if c.knowledge_type not in _RESULT_FIRING_TYPES:
            continue
        if not _result_prescriptive(c.assertion):
            continue
        anchor = _result_anchor(c.assertion, common)
        if anchor is None:
            continue
        seed_stems = index.assertion_cw[cid] - common
        state, partial_hits, s_hits = _lexical_state(index, seed_stems, ("INTERP", "QUANT"))
        seeds = frozenset({cid})
        x_a = link.explicit_part(index, seeds, common, params.shared_threshold)
        verb = config.PATTERNS["TEST"].search(c.assertion).group(0).lower()
        tacitness = ((Tacitness.RELATIONAL, Tacitness.PERCEPTUAL) if re.match(r"inspect|observ", verb)
                    else (Tacitness.RELATIONAL,))
        quotes = _pick_quotes(ledger, seeds, relevance_stems=seed_stems)
        s1 = (quotes + [(None, None, c.assertion)])[0]
        test_id = f"RESULT:{cid}"
        alts = (
            _alt("The interpretation is stated in paraphrase without the seed's stems.", True,
                "the stem-overlap test cannot see a paraphrase (the same limitation as DISC, §9)."),
            _alt("The test is a formality with a binary outcome.", True,
                "not every prescribed test feeds a real branching decision."),
            _alt("The interpretation is instrument-given.", True,
                "a displayed pass/fail reading needs no practitioner interpretation."),
        )
        out.append(Candidate(
            lens="RESULT", anchor=anchor, seeds=seeds, x_a=x_a, rivals=frozenset(),
            lexical_state=state, lexical_partial_hits=partial_hits, lexical_synthetic_hits=s_hits,
            s_scope_n=len(index.s_ids),
            test_id=test_id, missing=f"a result-to-interpretation mapping for '{anchor}'",
            hypothesis_text=(f"Hypothesis (inferred): practitioners are predicted to read the result "
                            f"of '{anchor}' against expected values and map it to the next action; "
                            f"no verified claim in this ledger matched test {test_id}."),
            predicted_knowledge_type=(KnowledgeType.INTERPRETATION, KnowledgeType.EXPECTANCY),
            predicted_tacitness=tacitness,
            channel="CDM probes on a recalled case; process tracing", weak_channel=False,
            question_text=(f'Sources prescribe: "{s1[2]}". Think of the last time you did this. What '
                          f"result did you get, what had you expected, what did that result make you "
                          f"do next -- and what result would have sent you down a different path?"),
            question_targets=(cid,), alternatives=alts,
            closure_seed_stems=seed_stems, closure_pattern_names=("INTERP", "QUANT"),
            closure_exclude=frozenset()))
    return out


LENSES = {"DISC": disc, "DIAG": diag, "SEL": sel, "HEDGE": hedge, "GUARD": guard, "WHY": why,
         "RESULT": result}


def run_all(ledger: Ledger, index: link.Index, params: link.LinkParams) -> list[Candidate]:
    out = []
    for name in sorted(LENSES):
        out.extend(LENSES[name](ledger, index, params))
    return out
