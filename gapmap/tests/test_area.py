import json
from pathlib import Path

import pytest
from conftest import a_claim, area, ledger, mk_record
from residual.features import planner_partition
from residual.ledger import Ledger

from gapmap import __main__ as cli
from gapmap import area as area_mod
from gapmap import judge as judge_mod
from gapmap import rank

LENSES = ("DISC", "DIAG", "SEL", "HEDGE", "GUARD", "WHY", "RESULT")


def _world(n_areas: int, per_area: int):
    claims = [a_claim(f"Claim {a}-{i} about topic {a}{i}.", source_id=f"s{a}-{i}")
              for a in range(n_areas) for i in range(per_area)]
    areas = [area(f"a-{a}", f"Area {a}") for a in range(n_areas)]
    assignments = [(claims[a * per_area + i].claim_id, f"a-{a}")
                   for a in range(n_areas) for i in range(per_area)]
    return ledger(claims, areas=areas, assignments=assignments), claims


def _hyps(claims, scores, *, k_topics=None):
    k_topics = k_topics or [2] * len(scores)
    return [mk_record(f"g-{i:02d}", LENSES[i % len(LENSES)], "HYP", seeds=[claims[i].claim_id],
                      score=s, k_topic=k)
            for i, (s, k) in enumerate(zip(scores, k_topics))]


def test_uncapped_exposes_every_merged_hyp_and_marks_what_the_caps_show():
    lg, claims = _world(2, 10)
    records = _hyps(claims, [3] * 20)
    rows = area_mod.uncapped(records, lg, "sha", area_mod.claim_area(planner_partition(lg)))
    ranked, _ = rank.build(records, lg, "sha")
    shown = {r.gap_id for r in ranked if r.category == "HYP"}
    assert len(rows) == 20
    assert {r["gap_id"] for r in rows if r["shown"]} == shown
    assert sum(r["shown"] for r in rows) < 20


def test_uncapped_leaves_out_retrieval_gaps():
    lg, claims = _world(1, 3)
    records = [*_hyps(claims[:2], [1, 1]), mk_record("g-rg", "DISC", "RG-SINGLE", seeds=[claims[2].claim_id])]
    rows = area_mod.uncapped(records, lg, "sha", area_mod.claim_area(planner_partition(lg)))
    assert [r["gap_id"] for r in rows] == ["g-00", "g-01"]


def test_seed_area_matches_rank_on_the_planner_partition():
    lg, claims = _world(3, 2)
    ca = area_mod.claim_area(planner_partition(lg))
    for rec in _hyps(claims, [1] * 6):
        assert area_mod.seed_area(rec, ca) == rank._seed_area(rec, lg)


def test_weight_is_strictly_monotone_and_positive_over_the_rubric_range():
    ws = [area_mod.weight(s) for s in range(area_mod.SCORE_MIN, area_mod.SCORE_MAX + 1)]
    assert all(0 < w <= 1 for w in ws)
    assert ws == sorted(ws) and len(set(ws)) == len(ws)
    assert area_mod.weight(area_mod.SCORE_MAX) == 1


def test_noisy_or_and_max():
    assert area_mod.noisy_or([]) == 0
    assert area_mod.noisy_or([0.5, 0.5]) == pytest.approx(0.75)
    assert area_mod.noisy_or([0.2, 0.9]) >= max(0.2, 0.9)


def test_area_scores_cover_every_area_including_empty_ones_and_never_say_p_missing():
    lg, claims = _world(3, 2)
    part = planner_partition(lg)
    rows = area_mod.uncapped(_hyps(claims[:4], [4, 1, 1, 1]), lg, "sha", area_mod.claim_area(part))
    scores = area_mod.area_scores(rows, part)
    assert [s["area_id"] for s in scores] == ["a-0", "a-1", "a-2"]
    a0, a1, a2 = scores
    assert a0["n_candidates"] == 2 and a0["score_max"] == 1
    assert a1["score_noisy_or"] == pytest.approx(area_mod.noisy_or([area_mod.weight(1)] * 2))
    assert a2["n_candidates"] == 0 and a2["score_noisy_or"] == 0 and a2["score_max"] == 0
    text = json.dumps(scores).lower()
    assert "p_missing" not in text and "p(missing)" not in text and "calibrat" not in text


def test_spearman_is_undefined_on_a_constant_and_exact_on_a_monotone_map():
    assert area_mod.spearman([1, 2, 3], [5, 5, 5]) is None
    assert area_mod.spearman([1, 2, 3, 4], [10, 20, 30, 40]) == pytest.approx(1)
    assert area_mod.spearman([1, 2, 3, 4], [4, 3, 2, 1]) == pytest.approx(-1)


def test_the_association_check_fires_on_a_planted_score_and_not_on_noise():
    k_topic = [2, 2, 3, 3, 3, 4, 5, 6, 6, 7, 9, 11, 2, 3, 3, 4, 2, 3, 5, 2]
    check = area_mod.association(scores=list(k_topic), covariate=k_topic)
    assert check["trips"] and check["planted_trips"]
    assert check["random_trip_rate"] <= area_mod.RANDOM_TRIP_MAX
    assert check["discriminates"]
    noise = area_mod.association(scores=[(i * 7919) % 23 for i in range(20)], covariate=k_topic)
    assert not noise["trips"]


def test_both_directions_count():
    cov = list(range(12))
    assert area_mod.association(scores=[-c for c in cov], covariate=cov)["trips"]


def test_too_few_candidates_do_not_discriminate():
    check = area_mod.association(scores=[1, 2, 3], covariate=[1, 2, 3])
    assert check["trips"] and not check["discriminates"]


def test_a_constant_covariate_cannot_be_tested():
    check = area_mod.association(scores=[1, 2, 3, 4, 5, 6], covariate=[2] * 6)
    assert check["rho"] is None and not check["trips"] and not check["discriminates"]


def test_decision_reads_only_admissible_discriminating_ledgers():
    trip = {"rho": 0.9, "trips": True, "discriminates": True}
    weak = {"rho": 0.95, "trips": True, "discriminates": False}
    calm = {"rho": 0.1, "trips": False, "discriminates": True}
    assert area_mod.decide({"x": {"k_topic": trip}}, admissible={"x"})["tripped"]
    assert not area_mod.decide({"x": {"k_topic": trip}}, admissible=set())["tripped"]
    assert not area_mod.decide({"x": {"k_topic": weak, "size": calm}}, admissible={"x"})["tripped"]


def test_feature_table_classifies_dead_confounded_and_live():
    def feats(n_claims, dens, n_unknown, boundary):
        return {"n_claims": n_claims, "evidence_density": dens, "n_unknown": n_unknown,
                "n_boundary_sources": boundary, "earliest_source": None}
    by_ledger = {
        "l1": [feats(10, 20, 1, 0), feats(20, 40, 5, 0), feats(30, 60, 2, 0)],
        "l2": [feats(5, 10, 3, 0), feats(15, 30, 0, 0), feats(40, 80, 4, 0)],
    }
    rows = {r["feature"]: r for r in area_mod.feature_table(by_ledger)}
    assert rows["n_boundary_sources"]["status"] == "dead"
    assert rows["earliest_source"]["status"] == "dead" and rows["earliest_source"]["missing"] == 6
    assert rows["evidence_density"]["status"] == "confounded (size)"
    assert rows["n_unknown"]["status"] == "live"
    assert rows["n_claims"]["status"] == "live (size)"
    assert rows["n_boundary_sources"]["modal_share"] == 1


def test_areas_file_must_be_at_task_step_grain(tmp_path):
    lg, claims = _world(1, 2)
    good = {"grain": "task_step", "areas": [{"area_id": "step-1", "name": "Step 1",
                                             "claim_ids": [claims[0].claim_id]}]}
    p = tmp_path / "areas.json"
    p.write_text(json.dumps(good))
    part, names = area_mod.load_areas(p)
    assert part == {"step-1": (claims[0].claim_id,)} and names == {"step-1": "Step 1"}
    p.write_text(json.dumps(good | {"grain": "planner"}))
    with pytest.raises(ValueError, match="task_step"):
        area_mod.load_areas(p)


ROOT = Path(__file__).resolve().parents[2]
PLC = ROOT / "reconstruct" / "runs" / "20260928T133336Z-59ec876b3d7e"
PLC_CACHE = ROOT / "research" / "n3" / "plc" / "closure_judgements.json"


@pytest.mark.skipif(not (PLC.exists() and PLC_CACHE.exists()), reason="committed PLC run not present")
def test_on_plc_the_candidates_rebuild_the_committed_map_and_the_caps_hide_15_of_24():
    text = (PLC / "ledger.json").read_text()
    lg = Ledger.from_json(text)
    sidecar = json.loads((PLC / "sidecar.json").read_text())
    judge = judge_mod.CachedJudge(judge_mod.OllamaJudge(), PLC_CACHE, live=False)
    sha = cli._sha256_text(text)
    records = area_mod.candidate_records(lg, sha, judge, sidecar=sidecar)
    ranked, rg = rank.build(records, lg, sha)
    committed = json.loads((ROOT / "research" / "n3" / "plc" / "gapmap.json").read_text())
    assert [r.gap_id for r in ranked] == [r["gap_id"] for r in committed["map"]]
    assert [r.gap_id for r in rg] == [r["gap_id"] for r in committed["retrieval_gaps"]]
    rows = area_mod.uncapped(records, lg, sha, area_mod.claim_area(planner_partition(lg)))
    assert (len(rows), sum(not r["shown"] for r in rows)) == (24, 15)
