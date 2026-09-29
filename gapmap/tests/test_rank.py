"""rank.py: merge, caps and the control slot (spec §6, §11.5)."""
from conftest import a_claim, area, ledger, mk_record

from gapmap import rank


def test_merge_keeps_the_higher_ranked_record_and_records_merged_from():
    hi = mk_record("g-hi", "DISC", "HYP", seeds=["c1", "c2"], score=3)
    lo = mk_record("g-lo", "DISC", "HYP", seeds=["c1", "c2", "c3"], score=2)  # X-Jaccard = 2/3
    merged = rank.merge([lo, hi])
    assert [r.gap_id for r in merged] == ["g-hi"]
    assert merged[0].merged_from == ("g-lo",)


def test_merge_does_not_touch_records_below_the_jaccard_threshold():
    a = mk_record("g-a", "DISC", "HYP", seeds=["c1", "c2"], score=3)
    b = mk_record("g-b", "DISC", "HYP", seeds=["c3", "c4"], score=2)  # disjoint, Jaccard = 0
    merged = rank.merge([a, b])
    assert {r.gap_id for r in merged} == {"g-a", "g-b"}


def test_merge_never_merges_lens_less_records_with_empty_evidence():
    # Regression: RG-UNK/CONTROL records typically carry no evidence, so |X| = set() for all of
    # them; jaccard(set(), set()) == 1.0 must not collapse unrelated U-claim gaps into one.
    a = mk_record("g-a", None, "RG-UNK", seeds=[], score=0)
    b = mk_record("g-b", None, "RG-UNK", seeds=[], score=0)
    merged = rank.merge([a, b])
    assert {r.gap_id for r in merged} == {"g-a", "g-b"}


def test_merge_never_crosses_lens_or_category():
    a = mk_record("g-a", "DISC", "HYP", seeds=["c1", "c2"], score=3)
    b = mk_record("g-b", "DIAG", "HYP", seeds=["c1", "c2"], score=2)
    c = mk_record("g-c", "DISC", "RG-SINGLE", seeds=["c1", "c2"], score=1)
    merged = rank.merge([a, b, c])
    assert {r.gap_id for r in merged} == {"g-a", "g-b", "g-c"}


def _areas_with_one_claim_each(n: int):
    claims = [a_claim(f"Claim number {i} about a distinct topic.", source_id=f"c{i}") for i in range(n)]
    areas = [area(f"a-{i}") for i in range(n)]
    assignments = [(claims[i].claim_id, f"a-{i}") for i in range(n)]
    return claims, areas, assignments


def test_map_caps_at_3_per_lens():
    claims, areas, assignments = _areas_with_one_claim_each(5)
    lg = ledger(claims, areas=areas, assignments=assignments)
    records = [mk_record(f"g-{i}", "DISC", "HYP", seeds=[claims[i].claim_id], score=5 - i)
              for i in range(5)]
    ranked, _rg = rank.build(records, lg, "sha")
    assert sum(1 for r in ranked if r.lens == "DISC") <= 3


def test_map_caps_at_4_per_area():
    claims, areas, assignments = _areas_with_one_claim_each(1)
    lg = ledger(claims, areas=areas, assignments=assignments)
    lenses_ = ["DISC", "DIAG", "SEL", "HEDGE", "GUARD"]
    records = [mk_record(f"g-{i}", lenses_[i], "HYP", seeds=[claims[0].claim_id], score=5 - i)
              for i in range(5)]
    ranked, _rg = rank.build(records, lg, "sha")
    assert sum(1 for r in ranked if r.category == "HYP") <= 4


def test_control_slot_picks_the_area_with_no_hyp_and_the_highest_a_share():
    c_full = a_claim("A fully attested claim in area one.", source_id="full")
    c_half_a = a_claim("An attested claim in area two.", source_id="half-a")
    c_half_u = a_claim("Another attested claim in area two.", source_id="half-b")
    lg = ledger([c_full, c_half_a, c_half_u],
               areas=[area("a-1", "Area One"), area("a-2", "Area Two")],
               assignments=[(c_full.claim_id, "a-1"), (c_half_a.claim_id, "a-2"),
                            (c_half_u.claim_id, "a-2")])
    ranked, _rg = rank.build([], lg, "sha")
    control = [r for r in ranked if r.category == "CONTROL"]
    assert len(control) == 1
    assert control[0].anchor == "Area One"


def test_control_slot_excludes_areas_already_covered_by_a_hyp():
    c1 = a_claim("A fully attested claim in area one.", source_id="full")
    c2 = a_claim("An attested claim in area two.", source_id="half")
    lg = ledger([c1, c2], areas=[area("a-1", "Area One"), area("a-2", "Area Two")],
               assignments=[(c1.claim_id, "a-1"), (c2.claim_id, "a-2")])
    hyp = mk_record("g-1", "DISC", "HYP", seeds=[c1.claim_id], score=5)
    ranked, _rg = rank.build([hyp], lg, "sha")
    control = [r for r in ranked if r.category == "CONTROL"]
    assert len(control) == 1
    assert control[0].anchor == "Area Two"


def test_control_slot_ties_broken_by_area_id():
    c1 = a_claim("A fully attested claim in area two.", source_id="c1")
    c2 = a_claim("A fully attested claim in area one.", source_id="c2")
    lg = ledger([c1, c2], areas=[area("a-2", "Area Two"), area("a-1", "Area One")],
               assignments=[(c1.claim_id, "a-2"), (c2.claim_id, "a-1")])
    ranked, _rg = rank.build([], lg, "sha")
    control = [r for r in ranked if r.category == "CONTROL"][0]
    assert control.anchor == "Area One"  # a-1 sorts before a-2
