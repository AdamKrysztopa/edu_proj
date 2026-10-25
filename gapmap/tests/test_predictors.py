import json
from pathlib import Path

import pytest

from gapmap import area


def test_topic_rank_centers_ties_and_singletons_without_discarding_candidates():
    assert area.topic_rank_predictor(
        reference=[0, 0, 1, 2, 5, 1, 99], k_topic=[2, 2, 2, 2, 3, 3, 4],
    ) == [-0.25, -0.25, 0.125, 0.375, 0.25, -0.25, 0.0]


def test_topic_rank_is_equivariant_to_candidate_order():
    reference, ks = [0, 1, 0, 2], [2, 2, 3, 3]
    original = area.topic_rank_predictor(reference=reference, k_topic=ks)
    order = [3, 0, 2, 1]
    assert area.topic_rank_predictor(reference=[reference[i] for i in order],
                                     k_topic=[ks[i] for i in order]) == [original[i] for i in order]


def test_topic_rank_rejects_misaligned_or_missing_inputs():
    with pytest.raises(ValueError):
        area.topic_rank_predictor(reference=[0, 1], k_topic=[2])
    with pytest.raises(ValueError):
        area.topic_rank_predictor(reference=[0, float("nan")], k_topic=[2, 2])


def test_density_adjustment_removes_the_pooled_within_stratum_projection():
    assert area.density_residual_predictor(
        reference=[0, 1, 2, 3], k_topic=[2] * 4, density=[0, 1, 0, 1],
    ) == pytest.approx([-0.25, -0.25, 0.25, 0.25])
    assert area.density_residual_predictor(
        reference=[0, 1, 2, 3], k_topic=[2] * 4, density=[3] * 4,
    ) == [-0.375, -0.125, 0.125, 0.375]


def test_density_adjustment_can_remove_all_signal_and_does_not_hide_that():
    assert area.density_residual_predictor(
        reference=[0, 1, 2, 3], k_topic=[2] * 4, density=[0, 1, 2, 3],
    ) == [0.0] * 4
    with pytest.raises(ValueError):
        area.density_residual_predictor(reference=[0, 1], k_topic=[2, 2], density=[1])


def test_mean_aggregate_is_not_a_count_score_and_preserves_empty_areas():
    before = area.predictor_area_means(scores=[0.5], area_ids=["a"], partition={"a": (), "b": ()})
    after = area.predictor_area_means(scores=[0.5, -0.5], area_ids=["a", "a"],
                                      partition={"a": (), "b": ()})
    assert before[0]["mean"] == 0.5
    assert after[0] == {"area_id": "a", "n_candidates": 2, "mean": 0.0}
    assert after[1] == {"area_id": "b", "n_candidates": 0, "mean": None}
    duplicated = area.predictor_area_means(scores=[0.5, 0.5], area_ids=["a", "a"], partition={"a": ()})
    assert duplicated[0]["mean"] == before[0]["mean"]


def test_mean_aggregate_refuses_unmapped_candidates_or_misalignment():
    with pytest.raises(ValueError):
        area.predictor_area_means(scores=[1], area_ids=[None], partition={"a": ()})
    with pytest.raises(ValueError):
        area.predictor_area_means(scores=[1, 2], area_ids=["a"], partition={"a": ()})


def test_full_evaluation_accepts_only_a_discriminating_planted_positive():
    from test_predictor_rules import synthetic_controls

    _, positive, reference, lengths, covariates = synthetic_controls()
    inputs = dict(reference=reference, covariates=covariates, text_lengths=lengths,
                  area_ids=["a"] * len(reference), partition={"a": (), "empty": ()})
    result = area.evaluate_predictor(scores=positive, **inputs)
    assert result["passes"] and result["a"]["passes"] and result["b"]["passes"] and result["c"]["passes"]
    assert result["area_spread"]["n_empty"] == 1
    assert result["area_spread"]["range"] == 0
    planted_count = area.evaluate_predictor(scores=covariates["k_topic"], **inputs)
    assert not planted_count["passes"] and not planted_count["a"]["passes"]


ROOT = Path(__file__).resolve().parents[2]
RUNS = {"plc": "20260928T133336Z-59ec876b3d7e", "gdpr_v1": "20260928T135354Z-eb840a85b7d1",
        "gdpr_v2": "20260928T145943Z-bc1cc9a30a02"}


@pytest.mark.parametrize("domain, expected_n", [("plc", 24), ("gdpr_v1", 1), ("gdpr_v2", 6)])
def test_replay_preserves_uncapped_pool_and_never_accepts_after_failed_calibration(domain, expected_n):
    run = ROOT / "reconstruct/runs" / RUNS[domain]
    sibling = {"gdpr_v1": "gdpr_v2", "gdpr_v2": "gdpr_v1"}.get(domain)
    result = area.replay_predictors(
        ledger_path=run / "ledger.json", sidecar_path=run / "sidecar.json",
        cache_path=ROOT / "research/n3" / domain / "closure_judgements.json", domain=domain,
        sibling_path=ROOT / "reconstruct/runs" / RUNS[sibling] / "ledger.json" if sibling else None,
    )
    committed = json.loads((ROOT / "research/area_score" / domain / "candidates.json").read_text())
    assert len(result["rows"]) == expected_n
    assert [r["gap_id"] for r in result["rows"]] == sorted(r["gap_id"] for r in committed["candidates"])
    assert set(result["predictors"]) == {"topic_rank", "density_residual"}
    for evaluated in [*result["predictors"].values(), result["reference_comparator"]]:
        assert not evaluated["passes"]
        assert len(evaluated["areas"]) == 5
        assert set(evaluated["a"]["checks"]) == set(area.PREDICTOR_COVARIATES)
    if domain == "plc":
        control = json.loads((ROOT / "research/area_score/phase1_controls.json").read_text())
        assert result["predictors"]["topic_rank"]["c"] == control["stand_ins"]
        assert result["source_count_plant"]["a"]["checks"]["k_topic"] == control["source_count_plant"]
    if domain == "gdpr_v2":
        assert not result["admissible"] and "pending" in result["admissibility_note"]
