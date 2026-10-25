from datetime import date

import pytest
from conftest import CODER, SCOPE, claim, evidence, generation, search, source

from residual.features import area_features, planner_partition
from residual.gapmap import FEATURE_SET, AreaFeatures
from residual.ledger import Area, Contradiction, Ledger
from residual.provenance import Derivation, Verdict
from residual.vocab import KnowledgeType, SourceKind, Tacitness


def _ledger(claims, areas=(), assignments=(), contradictions=()):
    return Ledger(purpose="reconstruction", claims=tuple(claims), areas=tuple(areas),
                  assignments=tuple(assignments), contradictions=tuple(contradictions))


def _area(aid):
    return Area(area_id=aid, scope=SCOPE, name=aid)


def _two_area_ledger():
    s1 = source("doi:1", independence_key="k1", published=date(2019, 5, 1))
    s2 = source("doi:2", independence_key="k1", published=None)
    s3 = source("log:3", kind=SourceKind.LOG, independence_key="k3", published=date(2021, 1, 1),
                boundary=True)
    c1 = claim("Step one.", evidence=(evidence(s1), evidence(s2)))
    c2 = claim("Why step one.", knowledge_type=KnowledgeType.RATIONALE, evidence=(evidence(s3),),
               tacitness=Tacitness.AUTOMATED)
    c3 = claim("Nothing found here.", knowledge_type=KnowledgeType.CUE, searches=(search(),))
    c4 = claim("A model said so.", generation=generation())
    c5 = claim("Derived.", derivation=Derivation(premises=(c1.claim_id,), method="m", agent=CODER))
    c6 = claim("Refuted.", evidence=(evidence(s1, verdict=Verdict.REFUTES), evidence(s3)))
    lg = _ledger([c1, c2, c3, c4, c5, c6], areas=[_area("a-1"), _area("a-2")],
                 assignments=[(c1.claim_id, "a-1"), (c2.claim_id, "a-1"), (c3.claim_id, "a-1"),
                              (c4.claim_id, "a-2"), (c5.claim_id, "a-2"), (c6.claim_id, "a-2")])
    return lg, (c1, c2, c3, c4, c5, c6)


def test_one_record_per_partition_area_sorted_by_id():
    lg, _ = _two_area_ledger()
    out = area_features(lg, None, planner_partition(lg))
    assert [f.area_id for f in out] == ["a-1", "a-2"]
    assert all(isinstance(f, AreaFeatures) for f in out)


def test_counts_and_support_profile():
    lg, _ = _two_area_ledger()
    a1, a2 = area_features(lg, None, planner_partition(lg))
    assert a1.n_claims == 3
    assert a1.evidence_density == 3
    assert a1.n_independent_sources == 2
    assert a1.source_kinds == (SourceKind.LOG, SourceKind.STUDY)
    assert a1.n_boundary_sources == 1
    assert a1.knowledge_types == (KnowledgeType.CUE, KnowledgeType.PROCEDURE_STEP, KnowledgeType.RATIONALE)
    assert a1.tacitness == (Tacitness.AUTOMATED, Tacitness.UNASSESSED)
    assert a1.has_done_support and not a1.imagined_only
    assert a1.n_single_source_claims == 2
    assert a1.n_unknown == 1 and a1.n_synthetic == 0 and a1.n_inferred == 0
    assert a1.rationale_present
    assert (a1.earliest_source, a1.latest_source, a1.n_undated_sources) == (
        date(2019, 5, 1), date(2021, 1, 1), 1)
    assert a1.instability is None and a1.concentration is None

    assert a2.n_synthetic == 1 and a2.n_inferred == 1
    assert a2.n_contradictions == 1
    assert not a2.rationale_present


def test_contradiction_records_count():
    lg, (c1, c2, *_rest) = _two_area_ledger()
    x = Contradiction(claims=(c1.claim_id, c2.claim_id), detected_by=CODER, method="m")
    lg = Ledger.model_validate(lg.model_dump() | {"contradictions": [x.model_dump()]})
    a1, _ = area_features(lg, None, planner_partition(lg))
    assert a1.n_contradictions == 2


def test_imagined_only_when_every_support_prescribes():
    s = source("doi:tb", kind=SourceKind.TEXTBOOK)
    c = claim("Prescribed.", evidence=(evidence(s),))
    lg = _ledger([c], areas=[_area("a")], assignments=[(c.claim_id, "a")])
    (f,) = area_features(lg, None, planner_partition(lg))
    assert f.imagined_only and not f.has_done_support


def test_empty_area_is_all_zero_and_not_imagined_only():
    c = claim("Elsewhere.", evidence=(evidence(),))
    lg = _ledger([c], areas=[_area("a"), _area("b")], assignments=[(c.claim_id, "a")])
    _, b = area_features(lg, None, planner_partition(lg))
    assert b.n_claims == 0 and b.evidence_density == 0 and b.source_kinds == ()
    assert not b.imagined_only and not b.has_done_support
    assert b.earliest_source is None


def test_a_header_date_in_the_sidecar_counts_as_undated():
    s = source("https://x.org/a", kind=SourceKind.DOCUMENTATION, published=date(2026, 9, 28))
    c = claim("Dated by the server only.", evidence=(evidence(s),))
    lg = _ledger([c], areas=[_area("a")], assignments=[(c.claim_id, "a")])
    sidecar = {"sources": {s.source_id: {"published": "2026-09-28", "published_field": None,
                                         "modified_field": "http:last-modified"}}}
    (with_sc,) = area_features(lg, sidecar, planner_partition(lg))
    (without,) = area_features(lg, None, planner_partition(lg))
    assert (with_sc.latest_source, with_sc.n_undated_sources) == (None, 1)
    assert (without.latest_source, without.n_undated_sources) == (date(2026, 9, 28), 0)
    sidecar["sources"][s.source_id]["published_field"] = "article:published_time"
    (named,) = area_features(lg, sidecar, planner_partition(lg))
    assert named.latest_source == date(2026, 9, 28)


def test_an_external_partition_overrides_the_planner_areas():
    lg, (c1, c2, c3, c4, c5, c6) = _two_area_ledger()
    part = {"step-2": (c2.claim_id,), "step-1": (c1.claim_id, c6.claim_id)}
    s1, s2 = area_features(lg, None, part)
    assert (s1.area_id, s1.n_claims, s2.area_id, s2.n_claims) == ("step-1", 2, "step-2", 1)


def test_partition_rejects_absent_and_doubly_assigned_claims():
    lg, (c1, *_rest) = _two_area_ledger()
    with pytest.raises(ValueError, match="absent"):
        area_features(lg, None, {"a": ("c-nope",)})
    with pytest.raises(ValueError, match="more than one area"):
        area_features(lg, None, {"a": (c1.claim_id,), "b": (c1.claim_id,)})


def test_deterministic_under_input_order():
    lg, _ = _two_area_ledger()
    part = planner_partition(lg)
    reversed_part = {k: tuple(reversed(v)) for k, v in reversed(list(part.items()))}
    assert area_features(lg, None, part) == area_features(lg, None, reversed_part)


def test_no_field_is_added_to_the_frozen_feature_set():
    lg, _ = _two_area_ledger()
    (f, _) = area_features(lg, None, planner_partition(lg))
    assert tuple(k for k in f.model_dump() if k != "area_id") == FEATURE_SET
