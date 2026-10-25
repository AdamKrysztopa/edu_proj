"""I12 phase 1: rules exercised only on planted and stand-in scores."""
import hashlib
import json
import random
from pathlib import Path

import pytest

from gapmap import area


@pytest.mark.parametrize("lens, state, expected", [
    ("DISC", "open", 1.0), ("DIAG", "partial", 0.75),
    ("SEL", "closed", 0.5), ("HEDGE", "synthetic-closed", 1.0),
    ("GUARD", "open", 1.0), ("WHY", "open", 0.5),
    ("RESULT", "partial", 0.25), ("WHY", "closed", 0.0),
])
def test_lens_reference_uses_only_declared_lens_and_lexical_state(lens, state, expected):
    assert area.lens_signal_reference(lens, state) == expected


@pytest.mark.parametrize("lens, state", [(None, "open"), ("WHY", ""), ("WHY", "undecided")])
def test_reference_refuses_missing_or_judge_only_states(lens, state):
    with pytest.raises(ValueError):
        area.lens_signal_reference(lens, state)


def test_pooled_ranks_remove_stratum_offsets_and_keep_score_constant_strata():
    # Two opposing pairs cancel. A singleton and a reference-constant pair
    # carry no within-stratum information and are excluded in every arm.
    result = area.lens_signal_check(
        scores=[1, 2, 200, 100, 999, 9, 8],
        reference=[0, 1, 0, 1, 0, 0, 0],
        k_topic=[2, 2, 3, 3, 4, 5, 5], text_lengths=[8, 1, 7, 2, 6, 3, 5],
    )
    assert result["within_rho"] == pytest.approx(0)
    assert (result["n_within"], result["n_strata"]) == (4, 2)
    assert not result["passes"]
    # Constant candidate scores cannot remove a difficult stratum from an arm.
    constant = area.lens_signal_check(
        scores=[1, 1, 3, 4], reference=[0, 1, 0, 1],
        k_topic=[2, 2, 3, 3], text_lengths=[1, 4, 2, 3],
    )
    assert constant["n_within"] == 4
    assert constant["within_rho"] == pytest.approx(2 ** -0.5)


def test_within_stratum_pool_uses_centered_midranks_without_reranking():
    # Centered ranks: x=(-1, 0, 1, -0.5, 0.5);
    # y=(-0.5, -0.5, 1, 0.5, -0.5). Dot=1, sums of squares=2.5,2.
    result = area.lens_signal_check(
        scores=[1, 2, 3, 10, 20], reference=[0, 0, 1, 1, 0],
        k_topic=[2, 2, 2, 3, 3], text_lengths=[2, 4, 1, 5, 3],
    )
    assert result["within_rho"] == pytest.approx(1 / 5 ** 0.5)


@pytest.mark.parametrize("scores, reference, lengths", [
    ([1, 1, 1, 1], [0, 1, 0, 1], [1, 2, 3, 4]),
    ([1, 2, 3, 4], [0, 0, 0, 0], [1, 2, 3, 4]),
    ([1, 2, 3, 4], [0, 1, 0, 1], [1, 1, 1, 1]),
])
def test_undefined_associations_never_pass(scores, reference, lengths):
    assert not area.lens_signal_check(
        scores=scores, reference=reference, k_topic=[2, 2, 3, 3], text_lengths=lengths,
    )["passes"]


@pytest.mark.parametrize("scores", [[1], [1, float("nan")], [1, float("inf")], [1, None]])
def test_rule_inputs_cannot_silently_drop_rows(scores):
    with pytest.raises(ValueError):
        area.lens_signal_check(scores=scores, reference=[0, 1], k_topic=[2, 2], text_lengths=[1, 2])


def synthetic_controls():
    """SYNTHETIC full factorial; diagnostic only, never a research criterion."""
    spec = {"label": "SYNTHETIC", "k_topic": [2, 3, 4, 5],
            "lens_states": [["WHY", "closed"], ["RESULT", "partial"],
                            ["WHY", "open"], ["DISC", "open"]],
            "lengths": [10, 20, 30, 40], "noise_seed": 0, "noise_half_width": 0.001}
    spec_sha256 = hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()
    rows = [(k, lens, state, length) for k in spec["k_topic"]
            for lens, state in spec["lens_states"] for length in spec["lengths"]]
    reference = [area.lens_signal_reference(lens, state) for _, lens, state, _ in rows]
    ks = [k for k, _, _, _ in rows]
    lengths = [length for _, _, _, length in rows]
    rng = random.Random(spec["noise_seed"])
    positive = [r + rng.uniform(-0.001, 0.001) for r in reference]
    covariates = {"k_topic": ks, "k_step": lengths, "dens": [k * 2 for k in ks],
                  "area_n_claims": [k * 10 for k in ks], "area_evidence_density": lengths}
    return spec_sha256, positive, reference, lengths, covariates


def test_planted_source_count_fails_a_in_both_directions_and_positive_passes_a():
    _, positive, _, _, covariates = synthetic_controls()
    for sign in (1, -1):
        result = area.predictor_confound_checks(
            scores=[sign * k for k in covariates["k_topic"]], covariates=covariates)
        assert not result["passes"]
        assert result["checks"]["k_topic"]["rho"] == pytest.approx(sign)
        assert result["checks"]["k_topic"]["discriminates"]
    assert area.predictor_confound_checks(scores=positive, covariates=covariates)["passes"]


def test_a_requires_every_covariate_and_refuses_undefined_or_undiscriminating_checks():
    covariates = {name: [1, 2, 3] for name in area.PREDICTOR_COVARIATES}
    assert not area.predictor_confound_checks(scores=[1, 3, 2], covariates=covariates)["passes"]
    with pytest.raises(ValueError):
        area.predictor_confound_checks(scores=[1, 3, 2], covariates={"k_topic": [1, 2, 3]})
    covariates["k_step"] = [0, 0, 0]
    assert not area.predictor_confound_checks(scores=[1, 3, 2], covariates=covariates)["passes"]


def test_synthetic_positive_passes_b_and_c_rejects_both_stand_ins_reproducibly():
    _, positive, reference, lengths, covariates = synthetic_controls()
    inputs = dict(reference=reference, k_topic=covariates["k_topic"], text_lengths=lengths)
    result = area.lens_signal_check(scores=positive, **inputs)
    assert result["passes"]
    assert result["within_rho"] >= 0.5
    assert abs(result["length_rho"]) < 0.3
    controls = area.predictor_stand_ins(**inputs)
    assert controls == area.predictor_stand_ins(**inputs)
    assert controls["draws"] == 2000 and controls["seed"] == 0
    assert controls["uniform_failures"] >= 1900
    assert controls["length_failures"] == 2000
    assert controls["passes"]


def test_c_cannot_pass_by_rejecting_everything_on_an_undefined_reference():
    assert not area.predictor_stand_ins(
        reference=[1, 1, 1, 1], k_topic=[2, 2, 3, 3], text_lengths=[1, 2, 3, 4],
    )["passes"]


def plc_controls():
    """Replay the fixed pool, then evaluate ONLY planted/stand-in scores.

    No I6 weights or replacement predictor values enter an association.
    """
    from residual.ledger import Ledger
    from gapmap import judge, rank

    root = Path(__file__).resolve().parents[2]
    run = root / "reconstruct/runs/20260928T133336Z-59ec876b3d7e"
    ledger_text = (run / "ledger.json").read_text()
    ledger = Ledger.from_json(ledger_text)
    sha = hashlib.sha256(ledger_text.encode()).hexdigest()
    cached_judge = judge.CachedJudge(
        judge.OllamaJudge(), root / "research/n3/plc/closure_judgements.json", live=False)
    records = area.candidate_records(ledger, sha, cached_judge,
                                    sidecar=json.loads((run / "sidecar.json").read_text()))
    hyps = sorted((r for r in rank.merge(records) if r.category == "HYP"), key=lambda r: r.gap_id)
    ks = [r.confidence.k_topic for r in hyps]
    reference = [area.lens_signal_reference(r.lens, r.inferred_gap.lexical_state) for r in hyps]
    lengths = [len(r.anchor) for r in hyps]
    source_plant = area.association(scores=ks, covariate=ks)
    stand_ins = area.predictor_stand_ins(reference=reference, k_topic=ks, text_lengths=lengths)
    groups = {k: [reference[i] for i, value in enumerate(ks) if value == k] for k in sorted(set(ks))}
    return {"label": "PLANTED_AND_STAND_IN_ONLY", "domain": "plc", "n": len(hyps),
            "gap_ids": [r.gap_id for r in hyps], "ledger_sha256": sha,
            "strata": [{"k_topic": k, "n": len(values), "reference_distinct": len(set(values))}
                       for k, values in groups.items()],
            "within_best_reachable": 1.0 if any(len(set(v)) > 1 for v in groups.values()) else None,
            "source_count_plant": source_plant, "stand_ins": stand_ins}


def test_plc_controls_reject_an_insufficiently_discriminating_b_check():
    result = plc_controls()
    assert result["n"] == 24
    assert result["source_count_plant"]["rho"] == 1
    assert result["source_count_plant"]["discriminates"]
    assert result["within_best_reachable"] == 1
    # This is an observed control failure, not a reason to tune the frozen rule.
    assert not result["stand_ins"]["passes"]
    assert result["stand_ins"]["uniform_failures"] == 1759
    assert result["stand_ins"]["length_failures"] == 2000


def test_b_accepts_the_signal_boundary_but_rejects_both_length_boundaries():
    scores = [1, 2, 3, 4, 5]
    result = area.lens_signal_check(scores=scores, reference=[1, 3, 5, 2, 4],
                                    k_topic=[2] * 5, text_lengths=[2, 5, 3, 1, 4])
    assert result["within_rho"] == 0.5 and result["passes"]
    for lengths in ([1, 5, 3, 2, 4], [5, 1, 3, 4, 2]):
        result = area.lens_signal_check(scores=scores, reference=scores,
                                        k_topic=[2] * 5, text_lengths=lengths)
        assert abs(result["length_rho"]) == 0.3 and not result["passes"]


def test_a_trips_at_exactly_point_eight_in_both_directions():
    for scores in ([1, 3, 2, 5, 4], [5, 3, 4, 1, 2]):
        result = area.association(scores=scores, covariate=[1, 2, 3, 4, 5])
        assert abs(result["rho"]) == 0.8 and result["trips"]
