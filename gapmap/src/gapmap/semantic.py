"""S1: turns a lens `Candidate`'s lexical firing into a JUDGED closure decision. Lens FIRING
(which seeds/anchors/rival-groups exist at all) stays exactly as `lenses.py` computes it; only the
open/partial/closed/synthetic-closed *state* now comes from here, via the local judge, not from
`Candidate.lexical_state` (kept on the candidate for comparison only, spec's "Why"). Retrieval is
independent of the four robustness `LinkParams` settings, so a robustness rerun's prompts -- and
therefore its cache hits -- are identical to the primary run's."""
from __future__ import annotations

import dataclasses
import hashlib
from dataclasses import dataclass, field

from residual.ledger import Ledger

from gapmap import config, lenses, link, text
from gapmap.judge import Judge, JudgeCacheMiss

_QUESTIONS = {
    "DISC": ("Does any sentence state how to tell whether something counts as '{anchor}': a "
             "threshold, a defining feature, or a contrast between a case that is and one that "
             "is not?"),
    "SEL": "Does any sentence state a condition that says which option to choose in which situation?",
    "HEDGE": ("Does any sentence state the specific cases in which the rule does NOT hold (an "
              "exception condition that is not merely a restatement of the rule or a "
              "cross-reference)?"),
    "GUARD": "Does any sentence state how a practitioner notices this error before or as it happens?",
    "WHY": ("Does any sentence state why this is done (the reason or the failure it prevents), "
            "other than 'the law/regulation requires it'?"),
    "RESULT": ("Does any sentence state what result of this test to expect and what a given "
               "result means or which next action it leads to?"),
    "DIAG": "Does any sentence state an observable sign that distinguishes '{rival}' from the other listed causes?",
}


@dataclass(frozen=True)
class Retrieval:
    a_items: tuple[tuple[str, str, str], ...]   # (id, claim_id, sentence)
    s_items: tuple[tuple[str, str, str], ...]


@dataclass(frozen=True)
class JudgeOutcome:
    state: str                          # open | partial | closed | synthetic-closed
    a_hits: tuple[str, ...]
    partial_hits: tuple[str, ...]
    synthetic_hits: tuple[str, ...]
    reason: str
    model_id: str
    prompt_sha256: str
    retrieved_n_a: int
    retrieved_n_s: int
    dropped_ids: int
    retrieval: Retrieval | None = None
    per_rival: dict = field(default_factory=dict)   # DIAG only: rival claim_id -> JudgeOutcome


def _assign_ids(rows: list[tuple[str, int, str]], start: int) -> tuple[tuple[str, str, str], ...]:
    """Fix 1: a single unique integer scheme across BOTH pools, `start`..`start + len(rows) - 1`
    -- the model is shown only bare numbers (never an "A3"/"S1" prefix); the A/S pool and the
    claim id are kept internally in the returned `(id, claim_id, sentence)` rows, never shown."""
    return tuple((str(start + i), cid, sent) for i, (cid, _si, sent) in enumerate(rows))


def build_retrieval(a_rows: list[tuple[str, int, str]],
                    s_rows: list[tuple[str, int, str]] = ()) -> Retrieval:
    """Assemble a `Retrieval` from arbitrary `(claim_id, order, sentence)` rows, capped and
    numbered with the same single integer scheme `retrieve()` uses -- used by the S2 fair
    mismatched-evidence control to splice one candidate's seed sentences with another's non-seed
    retrieved sentences into one retrieval-shaped prompt."""
    a_rows = list(a_rows)[: config.JUDGE_A_CAP]
    s_rows = list(s_rows)[: config.JUDGE_S_CAP]
    a_items = _assign_ids(a_rows, 1)
    s_items = _assign_ids(s_rows, len(a_items) + 1)
    return Retrieval(a_items=a_items, s_items=s_items)


def retrieve(index: link.Index, seed_ids: frozenset[str], scoring_stems: frozenset[str]) -> Retrieval:
    """All sentences of `T(c)` over A and S, scored by overlap with `scoring_stems`, top 8 A / top
    4 S at score >= 1, ties by claim_id then sentence index; the seed's own span sentences are
    always included, unconditional on score."""
    seed_sents: list[tuple[str, int, str]] = []
    seen: set[tuple[str, int]] = set()
    for cid in sorted(seed_ids):
        for i, sent in enumerate(text.sentences(index.T[cid])):
            seed_sents.append((cid, i, sent))
            seen.add((cid, i))

    def scored(ids) -> list[tuple[str, int, str, int]]:
        rows = []
        for cid in ids:
            for i, sent in enumerate(text.sentences(index.T[cid])):
                if (cid, i) in seen:
                    continue
                score = len(scoring_stems & text.cw(sent))
                if score >= 1:
                    rows.append((cid, i, sent, score))
        rows.sort(key=lambda r: (-r[3], r[0], r[1]))
        return rows

    a_rest = [(cid, i, sent) for cid, i, sent, _s in scored(index.a_ids)]
    s_rest = [(cid, i, sent) for cid, i, sent, _s in scored(index.s_ids)]
    return build_retrieval(seed_sents + a_rest, s_rest)


def build_prompt(seed_text: str, question: str, retrieval: Retrieval) -> str:
    lines = [f'Seed assertion: "{seed_text}"', f"Question: {question}", "", "Sentences:"]
    for id_, _cid, sent in (*retrieval.a_items, *retrieval.s_items):
        lines.append(f"{id_}: {sent}")
    lines += ["", 'Respond as JSON only: {"states": [numbers], "partially": [numbers], "reason": "<=25 words"}.',
             "Cite only sentence numbers that explicitly state the element; topical relevance alone "
             "is not enough.",
             "Use only the numbers shown above (e.g. 3, not \"A3\"); never invent a number."]
    return "\n".join(lines)


def _resolve_id(x, valid: frozenset[str]) -> str | None:
    """Fix 1: the judge often cites a bare int (`3`) or a numeric string (`"3"`) -- both resolve
    to the same offered id. Anything else (a non-numeric string, a float, `None`, a bool, an id
    outside the offered set) cannot be resolved at all."""
    if isinstance(x, bool):
        return None
    if isinstance(x, int):
        s = str(x)
    elif isinstance(x, str) and x.strip().lstrip("-").isdigit():
        s = x.strip()
    else:
        return None
    return s if s in valid else None


def judge_retrieval(judge: Judge, retrieval: Retrieval, seed_text: str, question: str) -> JudgeOutcome:
    """The judge/parse/state half of `judge_sentences`, taking an already-built `Retrieval` --
    used directly by the S2 fair mismatched-evidence control, which asks a candidate's own
    question against a spliced-together retrieval. Fix 1 (the silent id-drop bug): a cited id is
    parsed as an int or a numeric string; if the JSON is malformed (the judge returned nothing
    parseable) or ANY cited id cannot be resolved to one of the offered numbers, the state is
    `undecided` -- never silently `open`. `undecided` never reaches the old lexical short-circuit
    either: it is routed to its own retrieval-gap category (RG-UNDECIDED, `record.categorize`)."""
    if not retrieval.a_items and not retrieval.s_items:
        # Nothing was retrieved at all (only the S2 fair control's "other-source-only" arm can
        # hit this -- every other probe always includes the seed's own span sentences). There is
        # nothing to cite, so the answer is unambiguously `open`; asking the judge anyway invited
        # a hallucinated citation with an empty offered set (observed live: a bare "1" cited
        # against zero offered sentences), which is `undecided` by the rule below but wastes a
        # call and a cache entry on a question with no possible informative answer.
        prompt_sha = hashlib.sha256(build_prompt(seed_text, question, retrieval).encode()).hexdigest()
        return JudgeOutcome(state="open", a_hits=(), partial_hits=(), synthetic_hits=(),
                            reason="nothing retrieved to judge", model_id=judge.model_id,
                            prompt_sha256=prompt_sha, retrieved_n_a=0, retrieved_n_s=0,
                            dropped_ids=0, retrieval=retrieval)

    prompt = build_prompt(seed_text, question, retrieval)
    prompt_sha = hashlib.sha256(prompt.encode()).hexdigest()
    id_to_cid = {id_: cid for id_, cid, _s in (*retrieval.a_items, *retrieval.s_items)}
    a_ids = {id_ for id_, _c, _s in retrieval.a_items}
    s_ids = {id_ for id_, _c, _s in retrieval.s_items}
    valid = frozenset(a_ids | s_ids)

    try:
        raw = judge.ask(prompt)
    except JudgeCacheMiss:
        raise  # replay mode's cache-miss signal must propagate, never degrade to "undecided"
    except Exception as exc:  # any other broken judge degrades this one candidate, not the run
        raw, ask_error = None, str(exc)
    else:
        ask_error = None

    def _undecided(reason: str, dropped: int = 0) -> JudgeOutcome:
        return JudgeOutcome(state="undecided", a_hits=(), partial_hits=(), synthetic_hits=(),
                            reason=reason, model_id=judge.model_id, prompt_sha256=prompt_sha,
                            retrieved_n_a=len(retrieval.a_items), retrieved_n_s=len(retrieval.s_items),
                            dropped_ids=dropped, retrieval=retrieval)

    if not isinstance(raw, dict):
        return _undecided(ask_error or "the judge returned no parseable JSON object")

    states_raw = raw.get("states")
    partially_raw = raw.get("partially")
    states_raw = states_raw if isinstance(states_raw, list) else ([] if states_raw is None else [states_raw])
    partially_raw = (partially_raw if isinstance(partially_raw, list)
                     else ([] if partially_raw is None else [partially_raw]))

    resolved_states = [_resolve_id(x, valid) for x in states_raw]
    resolved_partially = [_resolve_id(x, valid) for x in partially_raw]
    unknown = sum(1 for r in (*resolved_states, *resolved_partially) if r is None)
    if unknown:
        return _undecided(f"{unknown} cited id(s) unresolved against the offered sentence numbers",
                          dropped=unknown)

    states = resolved_states
    partially = [p for p in resolved_partially if p not in states]
    if any(i in a_ids for i in states):
        state = "closed"
    elif any(i in a_ids for i in partially):
        state = "partial"
    elif any(i in s_ids for i in (*states, *partially)):
        state = "synthetic-closed"
    else:
        state = "open"
    a_hits = tuple(sorted({id_to_cid[i] for i in states if i in a_ids}))
    partial_hits = tuple(sorted({id_to_cid[i] for i in partially if i in a_ids}))
    synthetic_hits = tuple(sorted({id_to_cid[i] for i in (*states, *partially) if i in s_ids}))
    return JudgeOutcome(state=state, a_hits=a_hits, partial_hits=partial_hits,
                        synthetic_hits=synthetic_hits, reason=str(raw.get("reason", "")),
                        model_id=judge.model_id, prompt_sha256=prompt_sha,
                        retrieved_n_a=len(retrieval.a_items), retrieved_n_s=len(retrieval.s_items),
                        dropped_ids=0, retrieval=retrieval)


def judge_sentences(judge: Judge, index: link.Index, seed_ids: frozenset[str],
                    scoring_stems: frozenset[str], seed_text: str, question: str) -> JudgeOutcome:
    return judge_retrieval(judge, retrieve(index, seed_ids, scoring_stems), seed_text, question)


def _scoring(cand: lenses.Candidate) -> tuple[frozenset[str], frozenset[str]]:
    if cand.lens == "DISC":
        return text.cw(cand.anchor), cand.seeds
    return cand.closure_seed_stems, cand.seeds


def primary_probe(ledger: Ledger, cand: lenses.Candidate) -> tuple[frozenset[str], frozenset[str], str, str]:
    """`(scoring_stems, seed_ids, question, seed_text)` for a candidate's PRIMARY judge probe --
    used by the S2 mismatched-evidence control, which needs one representative probe per
    candidate even for DIAG (which otherwise judges one probe per rival): its first rival, by
    claim_id, stands in for the group."""
    if cand.lens == "DIAG":
        r = min(cand.rivals)
        cause_nc, effect_nc = cand.extra["diag_rival_stems"][r]
        split = cand.extra["diag_split"]
        question = _QUESTIONS["DIAG"].format(rival=text.trim(split[r][0]) or "(unnamed cause)")
        return cause_nc | effect_nc, frozenset({r}), question, ledger.by_id[r].assertion
    scoring_stems, seed_ids = _scoring(cand)
    question = (_QUESTIONS["DISC"].format(anchor=cand.anchor) if cand.lens == "DISC"
               else _QUESTIONS[cand.lens])
    return scoring_stems, seed_ids, question, ledger.by_id[min(cand.seeds)].assertion


def _judge_diag(ledger: Ledger, index: link.Index, judge: Judge,
               cand: lenses.Candidate) -> tuple[JudgeOutcome, lenses.Candidate]:
    rival_stems = cand.extra["diag_rival_stems"]
    split = cand.extra["diag_split"]
    per_rival: dict[str, JudgeOutcome] = {}
    for r in sorted(cand.rivals):
        cause_nc, effect_nc = rival_stems[r]
        question = _QUESTIONS["DIAG"].format(rival=text.trim(split[r][0]) or "(unnamed cause)")
        per_rival[r] = judge_sentences(judge, index, frozenset({r}), cause_nc | effect_nc,
                                       ledger.by_id[r].assertion, question)
    unsigned = [r for r in sorted(cand.rivals) if per_rival[r].state != "closed"]
    if len(unsigned) < 2:
        agg = JudgeOutcome(state="closed", a_hits=(), partial_hits=(), synthetic_hits=(),
                           reason="fewer than 2 rivals remained undiscriminated after judging",
                           model_id=judge.model_id, prompt_sha256="", retrieved_n_a=0,
                           retrieved_n_s=0, dropped_ids=sum(o.dropped_ids for o in per_rival.values()),
                           per_rival=per_rival)
        return agg, cand

    cause_lines = [f"- {text.trim(split[r][0]) or '(unnamed cause)'} "
                   f"({'sign found' if per_rival[r].state == 'closed' else 'no sign found'})"
                  for r in sorted(cand.rivals)]
    hypothesis_text = (f'Hypothesis (inferred): practitioners are predicted to tell these rival '
                      f'causes of "{cand.anchor}" apart by signs; the closure judge found a sign '
                      f'for the following (test {cand.test_id}):\n\n' + "\n".join(cause_lines))
    cause_list = "; ".join(text.trim(split[r][0]) for r in unsigned)
    relevance = frozenset().union(*(rival_stems[r][0] for r in unsigned))
    quotes = lenses._pick_quotes(ledger, frozenset(unsigned), relevance_stems=relevance)
    texts = [q[2] for q in quotes if q[2]]
    if len(texts) >= 2:
        lead = f'Sources list several causes of {cand.anchor}: "{texts[0]}", "{texts[1]}".'
    elif texts:
        lead = f'Sources list several causes of {cand.anchor}: "{texts[0]}".'
    else:
        lead = f"Sources list several causes of {cand.anchor}."
    question_text = (f"{lead} Think of the last time you diagnosed {cand.anchor}. Which cause did "
                    f"you suspect first, and what did you see, hear or measure that let you rule "
                    f"the others out?")
    # Fix 1: an undecided rival's judgement is not a genuine "unsigned" finding -- if any rival
    # counted toward `unsigned` was itself undecided (malformed JSON / an unresolvable cited id),
    # the whole group's state is undecided too, never silently "open".
    group_state = "undecided" if any(per_rival[r].state == "undecided" for r in unsigned) else "open"
    agg = JudgeOutcome(
        state=group_state,
        a_hits=tuple(sorted({h for r in unsigned for h in per_rival[r].a_hits})),
        partial_hits=tuple(sorted({h for r in unsigned for h in per_rival[r].partial_hits})),
        synthetic_hits=tuple(sorted({h for r in unsigned for h in per_rival[r].synthetic_hits})),
        reason="; ".join(f"{r}: {per_rival[r].reason}" for r in sorted(cand.rivals) if per_rival[r].reason),
        model_id=judge.model_id,
        prompt_sha256=",".join(sorted({per_rival[r].prompt_sha256 for r in cand.rivals})),
        retrieved_n_a=sum(per_rival[r].retrieved_n_a for r in unsigned),
        retrieved_n_s=sum(per_rival[r].retrieved_n_s for r in unsigned),
        dropped_ids=sum(o.dropped_ids for o in per_rival.values()), per_rival=per_rival)
    new_cand = dataclasses.replace(
        cand, rivals=frozenset(unsigned), missing=f"a discriminating sign for: {cause_list}",
        hypothesis_text=hypothesis_text, question_text=question_text,
        question_targets=tuple(cid for cid, _k, _q in quotes))
    return agg, new_cand


def judge_candidate(ledger: Ledger, index: link.Index, judge: Judge,
                    cand: lenses.Candidate) -> tuple[JudgeOutcome, lenses.Candidate]:
    """The one judged outcome for a fired candidate, plus the (possibly DIAG-finalised) candidate
    to build a `Record` from. `outcome.state == "closed"` means: no record is built (mirrors the
    old lexical short-circuit, now decided by the judge instead)."""
    if cand.lens == "DIAG":
        return _judge_diag(ledger, index, judge, cand)
    scoring_stems, seed_ids, question, seed_text = primary_probe(ledger, cand)
    outcome = judge_sentences(judge, index, seed_ids, scoring_stems, seed_text, question)
    return outcome, cand
