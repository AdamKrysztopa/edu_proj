import json
import math
import random
from pathlib import Path

import pytest

from residual import auroc as A

ASAH = json.loads((Path(__file__).parent / "data" / "asah.json").read_text())
POOR = [o == "Poor" for o in ASAH["outcome"]]


def brute_auroc(scores, labels):
    pos = [s for s, y in zip(scores, labels) if y]
    neg = [s for s, y in zip(scores, labels) if not y]
    return sum(1.0 if p > q else 0.5 if p == q else 0.0 for p in pos for q in neg) / (len(pos) * len(neg))


def test_perfect_score_gives_one():
    assert A.auroc([0.1, 0.2, 0.8, 0.9], [False, False, True, True]) == 1.0


def test_constant_score_gives_half():
    assert A.auroc([3.0] * 6, [True, False, True, False, False, True]) == 0.5


def test_ties_count_half_and_match_brute_force():
    rng = random.Random(1)
    for _ in range(50):
        n = rng.randint(4, 30)
        labels = [rng.random() < 0.4 for _ in range(n)]
        labels[0], labels[1] = True, False
        scores = [rng.randint(0, 3) for _ in range(n)]
        assert A.auroc(scores, labels) == pytest.approx(brute_auroc(scores, labels), abs=1e-12)


def test_one_class_is_refused():
    with pytest.raises(ValueError):
        A.auroc([1, 2, 3], [True, True, True])


# pROC 1.18.5, tests/testthat/test-auc.R, test-var.R and test-roc.test.R, on its aSAH data.
def test_pROC_aSAH_auroc_and_delong_variance():
    assert A.auroc(ASAH["wfns"], POOR) == pytest.approx(0.823678861788618, abs=1e-12)
    assert A.auroc(ASAH["ndka"], POOR) == pytest.approx(0.611957994579946, abs=1e-12)
    _, cov = A.auroc_covariance([ASAH["wfns"], ASAH["ndka"], ASAH["s100b"]], POOR)
    assert cov[0][0] == pytest.approx(0.00146991470882363, rel=1e-9)
    assert cov[1][1] == pytest.approx(0.0031908105493913, rel=1e-9)
    assert cov[2][2] == pytest.approx(0.00266868245717244, rel=1e-9)


def test_pROC_aSAH_paired_delong_test():
    est = A.paired_delta(ASAH["wfns"], ASAH["s100b"], POOR)
    assert est.delta / est.se == pytest.approx(2.20898359144091, rel=1e-9)
    z = 1.959963984540054
    assert est.delta - z * est.se == pytest.approx(0.0104061769564846, rel=1e-6)
    assert est.delta + z * est.se == pytest.approx(0.174214419249478, rel=1e-6)
    est2 = A.paired_delta(ASAH["wfns"], ASAH["ndka"], POOR)
    assert est2.delta / est2.se == pytest.approx(2.79777591868904, rel=1e-9)


def test_identical_scores_give_zero_delta():
    est = A.paired_delta(ASAH["wfns"], ASAH["wfns"], POOR)
    assert est.delta == 0.0 and est.se == 0.0


def test_singleton_clusters_reduce_to_delong():
    ids = list(range(len(POOR)))
    plain = A.paired_delta(ASAH["wfns"], ASAH["s100b"], POOR)
    clustered = A.paired_delta(ASAH["wfns"], ASAH["s100b"], POOR, clusters=ids)
    assert clustered.delta == plain.delta
    assert clustered.se == pytest.approx(plain.se, rel=1e-12)


def test_clustered_variance_grows_with_duplicated_clusters():
    rng = random.Random(3)
    n = 40
    labels = [i % 2 == 0 for i in range(n)]
    a = [rng.gauss(1.0 if y else 0.0, 1) for y in labels]
    b = [rng.gauss(0.5 if y else 0.0, 1) for y in labels]
    # each area copied, the copy in the same cluster: an ICC of 1 inside pairs
    labels2, a2, b2, cl = labels * 2, a * 2, b * 2, list(range(n)) * 2
    naive = A.paired_delta(a2, b2, labels2)
    clustered = A.paired_delta(a2, b2, labels2, clusters=cl)
    single = A.paired_delta(a, b, labels)
    assert clustered.delta == pytest.approx(single.delta)
    assert clustered.se > naive.se * 1.3
    assert clustered.se == pytest.approx(single.se, rel=0.05)


def test_one_class_in_one_cluster_falls_back_to_delong():
    rng = random.Random(5)
    labels = [True] * 16 + [False] * 4
    clusters = [i // 4 for i in range(20)]  # the four negatives form cluster 4
    a = [rng.gauss(1.0 if y else 0.0, 1) for y in labels]
    b = [rng.gauss(0.3 if y else 0.0, 1) for y in labels]
    clustered = A.paired_delta(a, b, labels, clusters=clusters)
    plain = A.paired_delta(a, b, labels)
    assert clustered.se == pytest.approx(plain.se) and clustered.se > 0


def test_common_effect_pooling_weights_by_n1_n0():
    e1 = A.Estimate(delta=0.2, se=0.1, weight=16 * 4)
    e2 = A.Estimate(delta=0.0, se=0.2, weight=10 * 10)
    pooled = A.pool_common([e1, e2])
    assert pooled.delta == pytest.approx((0.2 * 64) / 164)
    assert pooled.se == pytest.approx(math.sqrt(64 ** 2 * 0.01 + 100 ** 2 * 0.04) / 164)
    assert pooled.weight == 164


def test_common_effect_of_one_gold_is_that_gold():
    e = A.Estimate(delta=0.13, se=0.07, weight=60)
    assert A.pool_common([e]) == e


def test_random_effects_without_heterogeneity_has_zero_tau_and_wider_t_bound():
    ests = [A.Estimate(delta=0.1, se=0.05, weight=1), A.Estimate(delta=0.1, se=0.05, weight=1),
            A.Estimate(delta=0.1, se=0.05, weight=1)]
    re = A.pool_random(ests)
    assert re.tau2 == 0.0 and re.delta == pytest.approx(0.1)
    assert re.df == 2
    # modified Knapp-Hartung never goes below the fixed-effect standard error
    assert re.se >= 0.05 / math.sqrt(3) - 1e-12


def test_random_effects_picks_up_heterogeneity():
    ests = [A.Estimate(delta=d, se=0.02, weight=1) for d in (0.0, 0.3, 0.6)]
    re = A.pool_random(ests)
    assert re.tau2 > 0.05
    assert re.delta == pytest.approx(0.3)


@pytest.mark.parametrize("df,p,expected", [(1, 0.975, 12.706204736), (2, 0.95, 2.919985580),
                                           (4, 0.95, 2.131846782), (30, 0.99, 2.457261531)])
def test_t_quantile_matches_tables(df, p, expected):
    assert A.t_ppf(p, df) == pytest.approx(expected, rel=1e-7)


def test_cluster_resample_keeps_both_classes_and_whole_clusters():
    labels = [True] * 16 + [False] * 4
    clusters = [i // 4 for i in range(20)]
    rng = random.Random(0)
    for _ in range(200):
        idx = A.cluster_resample(labels, clusters, rng)
        assert len({clusters[i] for i in idx}) <= 5
        assert any(labels[i] for i in idx) and not all(labels[i] for i in idx)
        counts = {}
        for i in idx:
            counts[clusters[i]] = counts.get(clusters[i], 0) + 1
        assert all(v % 4 == 0 for v in counts.values())


def test_singleton_cluster_resample_is_class_stratified():
    labels = [True] * 16 + [False] * 4
    rng = random.Random(0)
    for _ in range(100):
        idx = A.cluster_resample(labels, list(range(20)), rng)
        assert sum(labels[i] for i in idx) == 16 and len(idx) == 20


def test_bootstrap_interval_agrees_with_delong_on_asah():
    rng = random.Random(7)
    golds = [A.GoldData(labels=POOR, clusters=list(range(len(POOR))),
                        scores={"wfns": ASAH["wfns"], "s100b": ASAH["s100b"]})]
    draws = A.bootstrap_pooled_deltas(golds, "wfns", ["s100b"], B=600, rng=rng)
    lo = A.percentile([d["s100b"] for d in draws], 0.025)
    hi = A.percentile([d["s100b"] for d in draws], 0.975)
    assert lo == pytest.approx(0.0104, abs=0.03)
    assert hi == pytest.approx(0.1742, abs=0.03)
