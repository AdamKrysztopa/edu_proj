import random
from statistics import NormalDist

import pytest

from residual import baselines as B
from residual.auroc import Estimate, GoldData
from residual.vocab import KnowledgeType as KT


def test_every_baseline_is_dated_and_typed():
    for b in B.BASELINES:
        assert b.dated == "2026-10-24"
        assert b.role in B.Role
        assert b.spec


def test_competing_set_is_ds3_k_and_excludes_reported_and_near_oracle():
    k2 = B.competing_set(n_golds=2)
    k3 = B.competing_set(n_golds=3)
    assert set(k2) == {"area_size", "retrieval_support_density", "corpus_term_frequency", "plain_llm",
                       "jev_text_form"}
    assert set(k3) == set(k2) | {"type_prior"}
    for name in ("random", "naive_type_rule", "verbalised_confidence", "gold_items_per_area"):
        assert name not in k3


def test_model_based_baselines_carry_model_prompt_and_date_but_no_call():
    llm = B.by_name("plain_llm")
    assert llm.model and llm.prompt and llm.role is B.Role.COMPETING
    assert B.by_name("verbalised_confidence").role is B.Role.SPEC_ONLY


def test_random_score_is_deterministic_by_seed():
    ids = [f"a{i}" for i in range(10)]
    assert B.random_score(ids, seed=1) == B.random_score(ids, seed=1)
    assert B.random_score(ids, seed=1) != B.random_score(ids, seed=2)
    assert all(0 <= v < 1 for v in B.random_score(ids, seed=1).values())


def test_naive_type_rule_marks_procedural_and_decision_areas():
    out = B.naive_type_rule({"a": (KT.PROCEDURE_STEP,), "b": (KT.CONCEPT,), "c": (KT.DECISION, KT.CUE)})
    assert out == {"a": 1.0, "b": 0.0, "c": 1.0}


def test_density_and_frequency_point_the_right_way():
    assert B.retrieval_support_density({"thin": 0, "thick": 9}) == {"thin": 0.0, "thick": -9.0}
    f = B.corpus_term_frequency({"rare": [0, 1], "common": [50, 80]})
    assert f["rare"] > f["common"]
    assert B.area_size({"big": 9, "small": 1}) == {"big": 9.0, "small": 1.0}


def test_type_prior_uses_only_other_golds():
    rates = {KT.PROCEDURE_STEP: 0.8, KT.CONCEPT: 0.2}
    out = B.type_prior({"a": (KT.PROCEDURE_STEP,), "b": (KT.CONCEPT,), "c": (KT.CUE,)}, rates,
                       n_other_golds=2)
    assert out["a"] == 0.8 and out["b"] == 0.2 and out["c"] == pytest.approx(0.5)
    with pytest.raises(ValueError):
        B.type_prior({"a": (KT.CONCEPT,)}, rates, n_other_golds=1)


def test_gold_items_per_area_is_a_near_oracle_not_in_k():
    assert B.by_name("gold_items_per_area").role is B.Role.NEAR_ORACLE
    assert B.gold_items_per_area({"a": 3}) == {"a": 3.0}


# --- the N3 gate statistic --------------------------------------------------------------------

def comps(*pairs):
    return [B.Comparison(baseline=f"b{i}", delta=d, se=s) for i, (d, s) in enumerate(pairs)]


def test_continue_needs_every_lower_bound_above_zero_and_minimum_point_at_delta():
    r = B.n3_reading(comps((0.30, 0.05), (0.25, 0.05)), c=1.85, delta=0.10)
    assert r.outcome == "continue"
    # one baseline's lower bound at or below zero blocks Continue (intersection-union)
    r = B.n3_reading(comps((0.30, 0.05), (0.12, 0.07)), c=1.85, delta=0.10)
    assert r.outcome == "inconclusive"
    # minimum point below delta blocks Continue
    r = B.n3_reading(comps((0.30, 0.01), (0.09, 0.01)), c=1.85, delta=0.10)
    assert r.outcome != "continue"


def test_stop_uses_bonferroni_upper_bounds():
    alpha = 1 - NormalDist().cdf(1.85)
    z_bonf = NormalDist().inv_cdf(1 - alpha / 2)
    se = 0.05
    edge = 0.10 - z_bonf * se
    assert B.n3_reading(comps((edge - 0.001, se), (0.5, 0.01)), c=1.85, delta=0.10).outcome == "stop"
    assert B.n3_reading(comps((edge + 0.001, se), (0.5, 0.01)), c=1.85, delta=0.10).outcome == "inconclusive"
    # unadjusted it would have stopped
    assert edge + 0.001 + 1.85 * se < 0.10


def test_continue_and_stop_never_both_hold():
    rng = random.Random(4)
    for _ in range(2000):
        cs = comps(*[(rng.uniform(-0.3, 0.5), rng.uniform(0.001, 0.2)) for _ in range(rng.randint(1, 6))])
        r = B.n3_reading(cs, c=rng.uniform(1.5, 2.5), delta=0.10)
        assert r.outcome in ("continue", "stop", "inconclusive")


def test_ms3_and_ms5_secondary_readings():
    # MS3: point >= delta and 90% lower bound > -delta/2, every baseline
    assert B.ms3_screen(comps((0.12, 0.08)), delta=0.10) is True
    assert B.ms3_screen(comps((0.12, 0.12)), delta=0.10) is False
    assert B.ms5_reading(comps((0.30, 0.05)), delta=0.10) == "continue"
    assert B.ms5_reading(comps((0.0, 0.05)), delta=0.10) == "stop"


def test_bootstrap_min_and_max_t_are_reported_readings():
    draws = [{"b0": 0.3 + 0.01 * i, "b1": 0.25 + 0.01 * i} for i in range(-20, 21)]
    cs = comps((0.30, 0.05), (0.25, 0.05))
    assert B.bootstrap_min_reading(cs, draws, c=1.85, delta=0.10) == "continue"
    assert B.max_t_reading(cs, draws, c=1.85, delta=0.10) == "continue"


def test_bootstrap_reading_uses_percentile_bounds():
    draws = [{"b0": 0.3 + 0.01 * i} for i in range(-20, 21)]
    assert B.bootstrap_reading(comps((0.30, 0.05)), draws, c=1.85, delta=0.10) == "continue"
    low = [{"b0": 0.0 + 0.001 * i} for i in range(-20, 21)]
    assert B.bootstrap_reading(comps((0.0, 0.05)), low, c=1.85, delta=0.10) == "stop"


def test_per_gold_estimates_match_paired_delta():
    from residual.auroc import paired_delta
    rng = random.Random(2)
    labels = [i < 12 for i in range(20)]
    gold = GoldData(labels=labels, clusters=list(range(20)),
                    scores={"map": [rng.gauss(y, 1) for y in labels], "x": [rng.gauss(0, 1) for _ in labels]})
    est = B.per_gold_estimates([B.gold_stats(gold, ["map", "x"])], "x")[0]
    ref = paired_delta(gold.scores["map"], gold.scores["x"], labels)
    assert est.delta == pytest.approx(ref.delta) and est.se == pytest.approx(ref.se)


def test_pooled_comparisons_from_gold_scores():
    rng = random.Random(0)
    golds = []
    for g in range(3):
        labels = [i < 16 for i in range(20)]
        golds.append(GoldData(labels=labels, clusters=[i // 4 for i in range(20)],
                              scores={"map": [float(y) + rng.gauss(0, 0.1) for y in labels],
                                      "x": [rng.gauss(0, 1) for _ in labels]}))
    cs, cov = B.pooled_comparisons(golds, "map", ["x"])
    assert cs[0].baseline == "x" and cs[0].delta > 0.3 and cs[0].se > 0
    assert len(cov) == 1 and cov[0][0] == pytest.approx(cs[0].se ** 2)
