"""Dedup, order, caps and the control slot (spec §6)."""
from __future__ import annotations

from residual.ledger import Ledger
from residual.vocab import CRITERION_LABELS

from gapmap import config, link, record

CONTROL_QUESTION = ("Walk me through how you carry out {area}, from start to finish, as if I "
                    "were watching you do it. What do you check, and in what order?")


def _x_a(rec: record.Record) -> frozenset[str]:
    return frozenset(i.claim_id for i in rec.observed_evidence if i.role in ("seed", "topic", "rival"))


def _seed_area(rec: record.Record, ledger: Ledger) -> str | None:
    seeds = sorted(i.claim_id for i in rec.observed_evidence if i.role in ("seed", "rival"))
    for cid in seeds:
        if (area := ledger.area_of(cid)) is not None:
            return area
    return None


def order_key(rec: record.Record):
    """`(-score, -r, -k_topic, -|X|, gap_id)` (§6)."""
    r = int(rec.confidence.robustness.split("/")[0])
    return (-rec.confidence.score, -r, -rec.confidence.k_topic, -len(_x_a(rec)), rec.gap_id)


def merge(records: list[record.Record]) -> list[record.Record]:
    """Same lens and category, X-Jaccard >= `MERGE_JACCARD`, merges into the higher-ranked one.
    Lens-less records (RG-UNK, CONTROL) never merge: they typically carry no evidence at all, so
    an empty-set Jaccard of 1.0 would otherwise collapse every one of them into a single record."""
    kept: list[record.Record] = []
    for rec in sorted(records, key=order_key):
        target_i = next((i for i, k in enumerate(kept)
                         if k.lens is not None and k.lens == rec.lens and k.category == rec.category
                         and link.jaccard(_x_a(k), _x_a(rec)) >= config.MERGE_JACCARD), None)
        if target_i is None:
            kept.append(rec)
        else:
            target = kept[target_i]
            kept[target_i] = target.model_copy(
                update={"merged_from": tuple(sorted({*target.merged_from, rec.gap_id}))})
    return kept


def _cap(hyp_sorted: list[record.Record], ledger: Ledger) -> list[record.Record]:
    per_lens: dict[str | None, int] = {}
    per_area: dict[str | None, int] = {}
    chosen = []
    for rec in hyp_sorted:
        if len(chosen) >= config.MAP_TOP_N:
            break
        if per_lens.get(rec.lens, 0) >= config.MAP_PER_LENS:
            continue
        area = _seed_area(rec, ledger)
        if per_area.get(area, 0) >= config.MAP_PER_AREA:
            continue
        per_lens[rec.lens] = per_lens.get(rec.lens, 0) + 1
        per_area[area] = per_area.get(area, 0) + 1
        chosen.append(rec)
    return chosen


def control_slot(ledger: Ledger, hyp_records: list[record.Record], ledger_sha: str) -> record.Record | None:
    """§6, §14.2: one extra slot for the unknown-unknowns guard, in the area with no HYP and the
    highest attested (A) share, ties broken by `area_id`."""
    hyp_areas = {_seed_area(r, ledger) for r in hyp_records}
    shares: dict[str, float] = {}
    for area in ledger.areas:
        claims = ledger.in_area(area.area_id)
        if not claims:
            continue
        n_a = sum(1 for c in claims if ledger.label(c.claim_id) in CRITERION_LABELS)
        shares[area.area_id] = n_a / len(claims)
    if not shares:
        return None
    pool = sorted(aid for aid in shares if aid not in hyp_areas) or sorted(shares)
    best = max(pool, key=lambda aid: shares[aid])
    name = next(a.name for a in ledger.areas if a.area_id == best)
    conf = record.Confidence(score=0, A=0, B=0, P=0, Q=0, breadth="narrow", robustness="0/4",
                             k_step=0, k_topic=0)
    ig = record.InferredGap(
        statement=(f"Control slot: area '{name}' ({best}) has no HYP record and the highest "
                  f"attested share ({shares[best]:.2f}) among candidate areas of ledger {ledger_sha[:8]}."),
        test_id=f"CONTROL:{best}", closure_state="open")
    q = record.QuestionOut(text=CONTROL_QUESTION.format(area=name), target_claim_ids=(),
                           channel="control", weak_channel=False)
    return record.Record(
        gap_id=record.make_gap_id(config.CONFIG_SHA256, ledger_sha, "CONTROL", (best,)),
        lens=None, category="CONTROL", anchor=name, observed_evidence=(), inferred_gap=ig,
        hypothesis=None, reasoning="the §14.2 unknown-unknowns guard: no HYP touches this area",
        missing="", confidence=conf, alternatives=(), question=q)


def build(records: list[record.Record], ledger: Ledger,
         ledger_sha: str) -> tuple[list[record.Record], list[record.Record]]:
    """Returns (map records, retrieval-gap records), both ranked and gapped/capped per §6."""
    merged = merge(records)
    hyp = sorted((r for r in merged if r.category == "HYP"), key=order_key)
    rg = sorted((r for r in merged if r.category != "HYP"), key=order_key)
    capped = _cap(hyp, ledger)
    ranked = [r.model_copy(update={"rank": i + 1}) for i, r in enumerate(capped)]
    if (ctrl := control_slot(ledger, ranked, ledger_sha)) is not None:
        ranked.append(ctrl.model_copy(update={"rank": len(ranked) + 1}))
    return ranked, rg
