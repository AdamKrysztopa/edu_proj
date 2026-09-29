"""Built-in checks printed in `gapmap.md` (spec §7, S2): anti-renaming (§7.1, F2), the S2
mismatched-evidence control and lexical donor null (replacing the F2 stem-scramble null), and
cross-run stability (§7.2), including the RG-SIBLING reroute and the sibling-partial downgrade."""
from __future__ import annotations

import random
import re
from dataclasses import dataclass

from residual.ledger import Ledger

from gapmap import config, lenses, link, record, semantic, text


@dataclass(frozen=True)
class CandidateStat:
    """One raw lens firing, judged or not: the input to both the matched-density table (§7.1)
    and cross-run matching (§7.2), which both need to see candidates a Record never carries."""

    lens: str
    anchor: str
    dens: int
    state: str          # open | partial | synthetic-closed | closed (judged)
    category: str | None  # None when state == "closed" (no Record is ever built for it)
    k_topic: int = 0
    lexical_state: str = ""


def candidate_stats(ledger: Ledger, index: link.Index, judge) -> list[CandidateStat]:
    out = []
    for cand in lenses.run_all(ledger, index, link.SETTING_1):
        outcome, sub = semantic.judge_candidate(ledger, index, judge, cand)
        k_topic = len(link.breadth(ledger, sub.x_a))
        closed = outcome.state == "closed"
        cat = None if closed else record.categorize(outcome.state, k_topic)
        out.append(CandidateStat(lens=sub.lens, anchor=sub.anchor, dens=len(sub.x_a),
                                 state=outcome.state, category=cat, k_topic=k_topic,
                                 lexical_state=cand.lexical_state))
    return out


def dens(rec: record.Record) -> int:
    """§7.1: `|X|`, the number of verified (A) supporting evidence items."""
    return sum(1 for i in rec.observed_evidence if i.role in ("seed", "topic", "rival"))


def j10(a: list[str], b: list[str]) -> float:
    ta, tb = set(a[:10]), set(b[:10])
    if not ta and not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def _rank_avg(values: list[float]) -> list[float]:
    """Average (fractional) ranks; tied values share the mean rank."""
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg_rank = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = avg_rank
        i = j + 1
    return ranks


def spearman(pairs: list[tuple[float, float]]) -> float:
    """Hand-rolled Spearman rank correlation with ties: Pearson's r over average ranks."""
    if len(pairs) < 2:
        return 0.0
    rx = _rank_avg([p[0] for p in pairs])
    ry = _rank_avg([p[1] for p in pairs])
    n = len(pairs)
    mx, my = sum(rx) / n, sum(ry) / n
    cov = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    vx = sum((r - mx) ** 2 for r in rx)
    vy = sum((r - my) ** 2 for r in ry)
    if vx == 0 or vy == 0:
        return 0.0
    return cov / (vx * vy) ** 0.5


_K_TOPIC_BANDS = ((0, 1, "0-1"), (2, 2, "2"), (3, 4, "3-4"), (5, 10 ** 9, ">=5"))


def closure_rate_by_k_topic(stats: list[CandidateStat]) -> list[dict]:
    """F2: closure rate by k_topic band, over every raw lens candidate (closed or not)."""
    rows = []
    for lo, hi, label in _K_TOPIC_BANDS:
        bucket = [s for s in stats if lo <= s.k_topic <= hi]
        n = len(bucket)
        closed = sum(1 for s in bucket if s.state == "closed")
        rows.append({"band": label, "n": n, "closed": closed, "rate": (closed / n) if n else 0.0})
    return rows


def anti_renaming(map_records: list[record.Record], pool: list[record.Record],
                  stats: list[CandidateStat]) -> dict:
    """§7.1 (F2): computed over lens candidates only -- `pool` must already exclude RG-UNK and
    CONTROL, whose density cannot vary. J10 against ascending/descending density rankings of the
    pool, Spearman(score, dens) over the pool (RG scored -1), the matched-density tercile table
    over `stats` (every raw lens firing, judged or not), and the closure rate by k_topic band."""
    map_ids = [r.gap_id for r in map_records]
    d_low = [r.gap_id for r in sorted(pool, key=lambda r: (dens(r), r.gap_id))]
    d_high = [r.gap_id for r in sorted(pool, key=lambda r: (-dens(r), r.gap_id))]
    j_low, j_high = j10(map_ids, d_low), j10(map_ids, d_high)
    pairs = [(float(r.confidence.score) if r.category == "HYP" else -1.0, float(dens(r))) for r in pool]
    rho = spearman(pairs)

    ordered = sorted(stats, key=lambda s: s.dens)
    n = len(ordered)
    thirds = [ordered[: n // 3], ordered[n // 3: 2 * n // 3], ordered[2 * n // 3:]] if n else [[], [], []]
    table = [{"tercile": label, "n": len(bucket),
             "closed": sum(1 for s in bucket if s.state == "closed"),
             "hyp": sum(1 for s in bucket if s.category == "HYP")}
            for label, bucket in zip(("low", "mid", "high"), thirds)]
    top = thirds[2]
    top_closed_share = (sum(1 for s in top if s.state == "closed") / len(top)) if top else 0.0

    flags = []
    if j_low >= 0.5 or rho <= -0.5:
        flags.append("density-in-disguise")
    if j_high >= 0.7 and top_closed_share < 0.2:
        flags.append("salience-in-disguise")
    return {"j10_low": j_low, "j10_high": j_high, "spearman": rho, "terciles": table,
           "top_tercile_closed_share": top_closed_share,
           "closure_by_k_topic": closure_rate_by_k_topic(stats), "flags": flags}


# ---------------------------------------------------------------------- S2 informativeness checks

def _closed_or_partial(state: str) -> bool:
    return state in ("closed", "partial")


def _nearest_other(i: int, stems: list[frozenset[str]], gap_ids: list[str]) -> int:
    """Second adversarial review, S2 fair control: the topically nearest OTHER candidate of the
    same lens by max seed-stem Jaccard, ties broken by (smaller) gap_id."""
    best_j, best_score = None, -1.0
    for j in range(len(stems)):
        if j == i:
            continue
        score = link.jaccard(stems[i], stems[j])
        if score > best_score or (score == best_score and (best_j is None or gap_ids[j] < gap_ids[best_j])):
            best_j, best_score = j, score
    return best_j


def _rows(items) -> list[tuple[str, int, str]]:
    return [(cid, 0, sent) for _id, cid, sent in items]


def mismatched_evidence_control(ledger: Ledger, ledger_sha: str, index: link.Index, judge,
                                candidates: list) -> dict:
    """S2, rewritten after the second adversarial review: the first version was a straw man -- the
    own-evidence arm always contained the seed's own sentences (17 of PLC's 22 closures cited only
    the seed or its source) while the mismatched arm never did, and the mismatched sentences were
    off-topic (cyclic gap_id pairing). Fair version: in BOTH arms the seed's own sentences are kept
    (`_source_of` gives the seed's own source, so its sentences never count as "other"); the OWN
    arm adds this candidate's own retrieved non-seed-source sentences; the CONTROL arm replaces
    those with the non-seed-source sentences retrieved for the topically nearest OTHER candidate
    of the same lens (max seed-stem Jaccard over each candidate's `primary_probe` scoring stems,
    ties by gap_id). Also reports the OWN arm with the seed and same-source sentences excluded
    entirely (how often OTHER, unrelated-to-the-seed sources alone close it). Flags
    `closure-uninformative` unless own_rate - control_rate >= 0.20 (of candidates); a lens with
    < 2 candidates is skipped (no "other candidate" to pair with)."""
    by_lens: dict[str, list] = {}
    for cand in candidates:
        by_lens.setdefault(cand.lens, []).append(cand)

    def gap_id(c) -> str:
        return record.make_gap_id(config.CONFIG_SHA256, ledger_sha, c.lens, c.seeds)

    per_lens: dict[str, dict] = {}
    tot_own = tot_ctrl = tot_other = tot_n = 0
    for lens_name in sorted(by_lens):
        cs = sorted(by_lens[lens_name], key=gap_id)
        if len(cs) < 2:
            continue
        gap_ids = [gap_id(c) for c in cs]
        probes = [semantic.primary_probe(ledger, c) for c in cs]
        retrievals = [semantic.retrieve(index, ids, stems) for stems, ids, _q, _t in probes]
        own_closed = ctrl_closed = other_closed = 0
        for i in range(len(cs)):
            stems_i, ids_i, question_i, seed_text_i = probes[i]
            ret_i = retrievals[i]
            seed_srcs_i = {_source_of(ledger, s) for s in ids_i}
            seed_items = [x for x in ret_i.a_items if x[1] in ids_i]
            other_i = [x for x in ret_i.a_items if _source_of(ledger, x[1]) not in seed_srcs_i]

            own_out = semantic.judge_retrieval(
                judge, semantic.build_retrieval(_rows(seed_items) + _rows(other_i)),
                seed_text_i, question_i)
            own_closed += _closed_or_partial(own_out.state)

            other_out = semantic.judge_retrieval(
                judge, semantic.build_retrieval(_rows(other_i)), seed_text_i, question_i)
            other_closed += _closed_or_partial(other_out.state)

            j = _nearest_other(i, [p[0] for p in probes], gap_ids)
            other_j = [x for x in retrievals[j].a_items if _source_of(ledger, x[1]) not in seed_srcs_i]
            ctrl_out = semantic.judge_retrieval(
                judge, semantic.build_retrieval(_rows(seed_items) + _rows(other_j)),
                seed_text_i, question_i)
            ctrl_closed += _closed_or_partial(ctrl_out.state)

        n = len(cs)
        own_rate, ctrl_rate, other_rate = own_closed / n, ctrl_closed / n, other_closed / n
        flag = not (own_rate - ctrl_rate >= 0.20)
        per_lens[lens_name] = {"n": n, "own_rate": own_rate, "control_rate": ctrl_rate,
                               "other_source_only_rate": other_rate, "flag": flag}
        tot_own += own_closed
        tot_ctrl += ctrl_closed
        tot_other += other_closed
        tot_n += n
    total = None
    if tot_n:
        own_rate, ctrl_rate, other_rate = tot_own / tot_n, tot_ctrl / tot_n, tot_other / tot_n
        total = {"n": tot_n, "own_rate": own_rate, "control_rate": ctrl_rate,
                "other_source_only_rate": other_rate, "flag": not (own_rate - ctrl_rate >= 0.20)}
    return {"by_lens": per_lens, "total": total}


def _source_of(ledger: Ledger, cid: str) -> str | None:
    c = ledger.by_id[cid]
    ev = c.supporting[0] if c.supporting else (c.evidence[0] if c.evidence else None)
    return ev.source.identifier if ev else None


def _same_source_index(ledger: Ledger, index: link.Index) -> dict[str, frozenset[str]]:
    by_source: dict[str | None, set[str]] = {}
    for cid in index.a_ids:
        by_source.setdefault(_source_of(ledger, cid), set()).add(cid)
    return {cid: frozenset(by_source[_source_of(ledger, cid)]) for cid in index.a_ids}


def _donor_pool(ledger: Ledger, index: link.Index, common: frozenset[str], same_source, exclude_cid: str,
               knowledge_type) -> list[str]:
    pool = [d for d in index.a_ids if d not in same_source[exclude_cid]
           and len(index.assertion_cw[d] - common) >= 2 and ledger.by_id[d].knowledge_type is knowledge_type]
    if len(pool) < 5:
        pool = [d for d in index.a_ids if d not in same_source[exclude_cid]
               and len(index.assertion_cw[d] - common) >= 2]
    return pool


def _lexical_closes(index: link.Index, stems: frozenset[str], pattern_names: tuple[str, ...],
                    exclude: frozenset[str]) -> bool:
    if not stems:
        return False
    required = min(2, len(stems))
    pats = [config.PATTERNS[name] for name in pattern_names]
    for cid in index.a_ids:
        if cid in exclude:
            continue
        for sent in text.sentences(index.T[cid]):
            if any(p.search(sent) for p in pats) and len(stems & text.cw(sent)) >= required:
                return True
    return False


def _donor_null_for(index: link.Index, common: frozenset[str], same_source, ledger: Ledger, rng: random.Random,
                    items: list[tuple[str, frozenset[str], tuple[str, ...]]]) -> tuple[int, list[int]]:
    """`items`: (seed_or_rival_cid, real_non_common_stems, pattern_names). Returns (observed,
    per-draw null-closed counts) with self and same-source excluded from both arms."""
    observed = 0
    draws = [0] * config.CLOSURE_NULL_DRAWS
    for cid, stems, pats in items:
        excl = same_source[cid] | {cid}
        if _lexical_closes(index, stems, pats, excl):
            observed += 1
        kt = ledger.by_id[cid].knowledge_type
        pool = _donor_pool(ledger, index, common, same_source, cid, kt)
        for i in range(config.CLOSURE_NULL_DRAWS):
            if not pool:
                continue
            donor = rng.choice(pool)
            donor_stems = index.assertion_cw[donor] - common
            if _lexical_closes(index, donor_stems, pats, same_source[donor] | {donor}):
                draws[i] += 1
    return observed, draws


def _percentile(values: list[int], pct: float) -> float:
    s = sorted(values)
    if not s:
        return 0.0
    idx = min(len(s) - 1, round(pct / 100 * (len(s) - 1)))
    return float(s[idx])


def lexical_donor_null(ledger: Ledger, index: link.Index, candidates: list) -> dict:
    """S2 "Lexical baseline": the reviewer's fair donor null for the LEXICAL closure test (self and
    same-source claims excluded from both the observed and the null arm; donor = the real
    non-common content stems of a random other-source A claim of the same knowledge type as the
    seed; one `random.Random(0)` per run, `CLOSURE_NULL_DRAWS` draws). Documents why the lexical
    test (§1.5) was replaced by the semantic judge (S1) -- it no longer decides any candidate's
    state. DISC is excluded (its closure is anchor-regex-driven, not stem-overlap). DIAG is
    handled per its own closure unit: one rival's sign test, not the group's."""
    common = link.common_stems(index, link.SETTING_1.common_cut)
    same_source = _same_source_index(ledger, index)
    rng = random.Random(0)

    by_lens: dict[str, list[tuple[str, frozenset[str], tuple[str, ...]]]] = {}
    for cand in candidates:
        if cand.lens == "DISC" or not cand.closure_seed_stems:
            continue
        if cand.lens == "DIAG":
            continue
        seed = min(cand.seeds)
        by_lens.setdefault(cand.lens, []).append((seed, cand.closure_seed_stems, cand.closure_pattern_names))
    diag_items = []
    for cand in candidates:
        if cand.lens != "DIAG":
            continue
        rival_stems = cand.extra.get("diag_rival_stems", {})
        for r in sorted(rival_stems):  # F8: dict built from a frozenset iterates hash-randomised
            cause_nc, _effect_nc = rival_stems[r]
            diag_items.append((r, cause_nc, ("DISCR",)))
    if diag_items:
        by_lens["DIAG"] = diag_items

    per_lens: dict[str, dict] = {}
    total_observed = 0
    total_draws = [0] * config.CLOSURE_NULL_DRAWS
    for lens_name in sorted(by_lens):
        observed, draws = _donor_null_for(index, common, same_source, ledger, rng, by_lens[lens_name])
        mean = sum(draws) / config.CLOSURE_NULL_DRAWS
        lo, hi = _percentile(draws, 5), _percentile(draws, 95)
        # S2 fix: a check "passes" (informative) only if observed is strictly ABOVE the null
        # interval -- previously "inside [lo, hi]" was the only failure mode, which never flagged
        # an observed count that fell BELOW the null (worse than chance).
        per_lens[lens_name] = {"observed": observed, "null_mean": mean, "null_lo": lo, "null_hi": hi,
                               "n_candidates": len(by_lens[lens_name]), "flag": observed <= hi}
        total_observed += observed
        for i in range(config.CLOSURE_NULL_DRAWS):
            total_draws[i] += draws[i]

    total_mean = sum(total_draws) / config.CLOSURE_NULL_DRAWS if by_lens else 0.0
    total_lo, total_hi = _percentile(total_draws, 5), _percentile(total_draws, 95)
    total = {"observed": total_observed, "null_mean": total_mean, "null_lo": total_lo,
            "null_hi": total_hi, "flag": total_observed <= total_hi}
    return {"by_lens": per_lens, "total": total}


def judge_lexical_confusion(stats: list[CandidateStat]) -> dict:
    """S2: judge-vs-lexical agreement, as confusion counts over every judged candidate."""
    counts: dict[str, int] = {}
    for s in stats:
        key = f"{s.lexical_state or 'n/a'}->{s.state}"
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))


# ------------------------------------------------------------------------------------- §7.2 -----

def _split_anchor(anchor: str) -> tuple[str, str]:
    parts = anchor.split(" ", 1)
    return parts[0], (parts[1] if len(parts) > 1 else "")


def _match(lens_name: str, anchor: str, pool, own_claims_text: str = "") -> tuple[object, float] | None:
    """§7.2 (F4): DISC matches on the same term and either the same head stem, or the OTHER run's
    anchor head appearing in THIS run's own anchor claims (`own_claims_text`) -- an exact-anchor
    match was too strict, since the same discrimination is often anchored by a different head word
    across independent reconstructions. Every other lens keeps the seed-stem Jaccard match."""
    same_lens = [s for s in pool if s.lens == lens_name]
    if not same_lens:
        return None
    if lens_name == "DISC":
        term, head = _split_anchor(anchor)
        hits = []
        for s in same_lens:
            s_term, s_head = _split_anchor(s.anchor)
            if s_term != term:
                continue
            same_head = s_head == head
            other_head_in_mine = bool(s_head) and re.search(rf"\b{re.escape(s_head)}\w*",
                                                             own_claims_text, re.IGNORECASE)
            if same_head or other_head_in_mine:
                hits.append((s, 1.0))
    else:
        my = text.cw(anchor)
        hits = [(s, j) for s in same_lens if (j := link.jaccard(my, text.cw(s.anchor))) >= config.SIBLING_JACCARD]
    return max(hits, key=lambda t: t[1]) if hits else None


def _own_claims_text(rec: record.Record) -> str:
    return " ".join(i.span or "" for i in rec.observed_evidence if i.role == "seed")


def match_candidate(rec: record.Record, sibling_records: list[record.Record]):
    hit = _match(rec.lens, rec.anchor, sibling_records, _own_claims_text(rec))
    return hit[0] if hit else None


def cross_run_stability(open_a: list[record.Record], open_b: list[record.Record],
                        records_b: list[record.Record], records_a: list[record.Record]) -> dict:
    """§7.2: for each direction, the counterpart category of each open candidate (HYP ∪
    RG-SINGLE)."""
    def direction(opens, other_records):
        rows = []
        for rec in opens:
            m = match_candidate(rec, other_records)
            rows.append({"gap_id": rec.gap_id, "lens": rec.lens, "anchor": rec.anchor,
                        "counterpart_category": m.category if m else None,
                        "counterpart_closure_state": m.inferred_gap.closure_state if m else None})
        return rows
    return {"a_to_b": direction(open_a, records_b), "b_to_a": direction(open_b, records_a)}


def apply_sibling(rec: record.Record, sibling_stats: list[CandidateStat]) -> record.Record:
    """§3 RG-SIBLING and §7.2's partial downgrade, applied to one record against the sibling
    ledger's full candidate stats (closed included, since only there can a match be `closed`)."""
    hit = _match(rec.lens, rec.anchor, sibling_stats, _own_claims_text(rec))
    if hit is None:
        return rec
    stat, _score = hit
    sib = record.Sibling(matched_gap_id=None, state=stat.state)
    ig = rec.inferred_gap.model_copy(update={"sibling": sib})
    if stat.state == "closed":
        return rec.model_copy(update={"category": "RG-SIBLING", "inferred_gap": ig})
    if stat.state == "partial" and ig.closure_state == "open":
        ig = ig.model_copy(update={"closure_state": "partial"})
    return rec.model_copy(update={"inferred_gap": ig})
