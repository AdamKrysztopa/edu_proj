"""The frozen gap-map features (gapmap.AreaFeatures) computed from a ledger: N2 stage 7.

Pure and deterministic: the same ledger, sidecar and partition give the same records, whatever
the order they arrive in. It adds no field, so the N1 feature freeze is untouched.
"""
from __future__ import annotations

from collections.abc import Collection, Mapping
from datetime import date

from residual.gapmap import AreaFeatures
from residual.ledger import Ledger
from residual.provenance import Source
from residual.vocab import CRITERION_LABELS, PRACTICE, EpistemicLabel, KnowledgeType, Practice

Partition = Mapping[str, Collection[str]]
"""area_id -> the claim ids in that area. Claims outside every area are not counted."""


def planner_partition(ledger: Ledger) -> dict[str, tuple[str, ...]]:
    """The ledger's own areas: N2's planner search buckets, not the §14.2 task-step grain."""
    out: dict[str, list[str]] = {a.area_id: [] for a in ledger.areas}
    for cid, aid in ledger.assignments:
        out[aid].append(cid)
    return {aid: tuple(sorted(cids)) for aid, cids in sorted(out.items())}


def _checked(ledger: Ledger, partition: Partition) -> dict[str, tuple[str, ...]]:
    seen: set[str] = set()
    out = {}
    for aid in sorted(partition):
        cids = tuple(sorted(set(partition[aid])))
        if missing := [c for c in cids if c not in ledger.by_id]:
            raise ValueError(f"area {aid} names absent claims {missing}")
        if twice := seen & set(cids):
            raise ValueError(f"claims {sorted(twice)} are in more than one area")
        seen |= set(cids)
        out[aid] = cids
    return out


def _date(src: Source, sidecar: Mapping | None) -> date | None:
    """A date the sidecar shows came from no document field (only the server's Last-Modified
    header, often the fetch day itself) is no publication date."""
    if src.published is None or sidecar is None:
        return src.published
    entry = (sidecar.get("sources") or {}).get(src.source_id)
    if entry is not None and entry.get("published_field") is None:
        return None
    return src.published


def _one(ledger: Ledger, sidecar: Mapping | None, area_id: str, cids: tuple[str, ...]) -> AreaFeatures:
    claims = [ledger.by_id[c] for c in cids]
    labels = [ledger.label(c) for c in cids]
    support = [e for c in claims for e in c.supporting]
    sources = {e.source.source_id: e.source for e in support}
    dates = {sid: _date(s, sidecar) for sid, s in sources.items()}
    dated = sorted(d for d in dates.values() if d is not None)
    practices = {PRACTICE[s.kind] for s in sources.values()}
    contradicted = ledger.contradicted()
    return AreaFeatures(
        area_id=area_id,
        n_claims=len(claims),
        evidence_density=len(support),
        n_independent_sources=len({s.independence_key for s in sources.values()}),
        source_kinds=tuple(sorted({s.kind for s in sources.values()})),
        n_boundary_sources=sum(s.boundary for s in sources.values()),
        n_contradictions=sum(1 for c in claims if c.claim_id in contradicted or c.refuting),
        knowledge_types=tuple(sorted({c.knowledge_type for c in claims})),
        tacitness=tuple(sorted({c.tacitness for c in claims})),
        has_done_support=Practice.DONE in practices,
        imagined_only=practices == {Practice.IMAGINED},
        n_single_source_claims=sum(1 for c, lab in zip(claims, labels)
                                   if lab in CRITERION_LABELS and c.corroboration == 1),
        n_inferred=labels.count(EpistemicLabel.INFERRED),
        n_synthetic=labels.count(EpistemicLabel.SYNTHETIC_EXTRAPOLATION),
        n_unknown=labels.count(EpistemicLabel.UNKNOWN),
        earliest_source=dated[0] if dated else None,
        latest_source=dated[-1] if dated else None,
        n_undated_sources=sum(1 for d in dates.values() if d is None),
        rationale_present=any(c.knowledge_type is KnowledgeType.RATIONALE and lab in CRITERION_LABELS
                              for c, lab in zip(claims, labels)),
        instability=None,
        concentration=None,
    )


def area_features(ledger: Ledger, sidecar: Mapping | None,
                  partition: Partition) -> tuple[AreaFeatures, ...]:
    """One AreaFeatures per partition area, ordered by area_id. `sidecar` is N2's sidecar.json
    (or None); it is read only for date provenance. Instability needs multi-family reruns and
    concentration a Git-history adapter, so both stay None here."""
    return tuple(_one(ledger, sidecar, aid, cids) for aid, cids in _checked(ledger, partition).items())
