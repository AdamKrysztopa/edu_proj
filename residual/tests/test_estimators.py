import math

import pytest

from residual.estimators import (
    Estimate,
    NotEstimable,
    chao1,
    chapman,
    frequency_counts,
    jackknife1,
    mh_coverage,
    to_record,
)

KREBS_HARES = ["1111", "1101", "1100", "1101", "1101", "1001", "1000", "1111", "1110", "1100",
               "1101", "1101", "1001", "1100", "0111", "0111", "0101", "0001"]
"""Krebs, Ecological Methodology, ch. 2 (2021 web edition), Box 2.4: 18 snowshoe hares, 4 sessions
(Krebs et al. 2001 data), https://www.zoology.ubc.ca/~krebs/downloads/krebs_chapter_02_2021.pdf"""

COTTONTAIL = (43, 16, 8, 6, 0, 2, 1) + (0,) * 11
"""Edwards & Eberhardt (1967), J. Wildl. Manage. 31(1):87-96: 76 rabbits caught on t = 18 trapping
nights (SpadeR `ChaoSpeciesData` documentation) from a confined population of known size (abstract);
the size 135 is reported secondhand and not verified here. f_j = rabbits caught on exactly j nights. The counts were decoded
from `data(cottontail)` in the CRAN package SPECIES (Wang 2011), documented as "analyzed in Chao 1987"."""


def histories(rows):
    return [[c == "1" for c in row] for row in rows]


def test_frequency_counts_of_the_krebs_hares():
    assert frequency_counts(histories(KREBS_HARES)) == (2, 6, 8, 2)


def test_never_caught_rows_do_not_change_the_counts():
    """The zero-catchability counterexample at unit level: every text estimator is a function of
    the counts, and an item no occasion caught leaves the counts unchanged."""
    caught = histories(KREBS_HARES)
    assert frequency_counts(caught + histories(["0000"] * 50)) == frequency_counts(caught)


def test_ragged_or_single_occasion_histories_are_refused():
    with pytest.raises(ValueError):
        frequency_counts(histories(["11", "101"]))
    with pytest.raises(ValueError):
        frequency_counts(histories(["1", "1"]))


def test_jackknife_reproduces_capture_on_the_krebs_hares():
    """Krebs (2021) Box 2.4 prints Program CAPTURE's Mh jackknife for these hares as 20 (19-26).
    First order (Burnham & Overton 1978, Biometrika 65:625): 18 + (3/4)·2 = 19.5. The printed interval
    matches Chao's (1987) log-normal interval with the Burnham-Overton variance f1·a1·(a1 - 1),
    a1 = (2t - 1)/t, printed as ceil(lower), round(upper)."""
    est = jackknife1(frequency_counts(histories(KREBS_HARES)))
    assert est.total == pytest.approx(19.5)
    assert round(est.total) == 20
    assert est.se == pytest.approx(math.sqrt(2.625))
    lo, hi = est.total_interval
    assert (math.ceil(lo), round(hi)) == (19, 26)


def test_chao1_on_the_cottontail_data():
    """Chao (1987), Biometrics 43:783-791, the Mh lower bound S + f1²/(2 f2) (the same formula is Krebs
    2021 eq. 2.35, credited there to Chao 1988) and its variance (EstimateS 9.1 User's Guide App. B eq. 5) f2·[(f1/f2)⁴/4 + (f1/f2)³ + (f1/f2)²/2], on the data that paper analysed.
    Chao's printed table was not accessible here, so the expected values are recomputed from the
    published formulas; the enclosure size 135 (secondhand, unverified) is the external anchor."""
    est = chao1(COTTONTAIL, small_t=False)
    r = 43 / 16
    assert est.observed == 76
    assert est.unseen == pytest.approx(43 ** 2 / 32)
    assert est.se == pytest.approx(math.sqrt(16 * (r ** 4 / 4 + r ** 3 + r ** 2 / 2)))
    assert est.total < 135
    lo, hi = est.total_interval
    assert lo < 135 < hi


HOMOGENEOUS = {(500, 250): 250, (384, 96, 8): 512}
"""Expected frequencies C(t, j)·p^j·q^(t-j)·N under homogeneous catchability, mapped to the true
f0 = q^t·N: N = 1000 with p = 0.5, t = 2, and p = 0.2, t = 3."""


@pytest.mark.parametrize("f", HOMOGENEOUS)
def test_chao1_small_t_factor_is_exact_under_homogeneity(f):
    """f1²/(2 f2) has expectation f0·t/(t-1) under homogeneity, so with few occasions the classic
    form is not a lower bound; the (t-1)/t factor is the one EstimateS 9.1 applies to Chao2
    (Colwell, EstimateS User's Guide: "all versions of the Chao1 and Chao2 estimators include
    small-sample adjustment factors of the form (n-1)/n") and iNEXT's Chat.Sam uses."""
    t = len(f)
    assert chao1(f).unseen == pytest.approx(HOMOGENEOUS[f])
    assert chao1(f, small_t=False).unseen == pytest.approx(HOMOGENEOUS[f] * t / (t - 1))


def test_chao1_falls_back_to_the_bias_corrected_form_without_doubletons():
    """EstimateS 9.1 User's Guide App. B eq. 4 and iNEXT's Chat.Sam (Chao 2005, Encyclopedia of
    Statistical Sciences 2nd ed., not opened): f0 = ((t-1)/t)·f1(f1 - 1)/2 when f2 = 0."""
    assert chao1((5, 0, 3)).unseen == pytest.approx(2 / 3 * 10)
    assert chao1((5, 0, 3), small_t=False).unseen == pytest.approx(10)
    assert chao1((1, 0, 3)).unseen == 0


def test_mh_sample_coverage_on_the_cottontail_data():
    """Lee & Chao (1994), Biometrics 50:88-97, sample-coverage estimator for model Mh:
    C = 1 - f1/n, n = Σ k f_k; γ² = max{(S/C)·t/(t-1)·Σ k(k-1) f_k / n² - 1, 0}; N = S/C + (f1/C)·γ².
    Hand computation: n = 142, C = 99/142, S/C = 109.01, γ² = 0.4540, N = 137.0. Recomputed from the
    formula; the anchor is the enclosure size 135 (Edwards & Eberhardt 1967; secondhand, unverified)."""
    est = mh_coverage(COTTONTAIL, coverage="lee_chao")
    c = 1 - 43 / 142
    gamma2 = (76 / c) * (18 / 17) * 254 / 142 ** 2 - 1
    assert est.total == pytest.approx(76 / c + 43 / c * gamma2)
    assert abs(est.total - 135) < 5
    lo, hi = est.total_interval
    assert lo < 135 < hi


@pytest.mark.parametrize("f", HOMOGENEOUS)
def test_mh_with_chao_jost_coverage_is_exact_under_homogeneity(f):
    """Chao & Jost (2012), Ecology 93:2533 (not opened), incidence coverage C = 1 - (f1/n)·A with
    A = t·f0/(t·f0 + f1), f0 the small-t Chao estimate, as coded in iNEXT's Chat.Sam
    (https://github.com/cran/iNEXT/blob/3.0.2/R/iNEXT.r). Lee & Chao's 1 - f1/n has expectation
    1 - q^(t-1), not the coverage 1 - q^t, which overstates N at small t."""
    assert mh_coverage(f).unseen == pytest.approx(HOMOGENEOUS[f])
    assert mh_coverage(f, coverage="lee_chao").unseen > 1.5 * HOMOGENEOUS[f]


def test_mh_reduces_to_the_coverage_estimate_without_heterogeneity():
    """With every item caught on all t occasions there is no heterogeneity left to correct."""
    est = mh_coverage((0, 0, 10))
    assert est.unseen == 0


def test_mh_is_not_estimable_from_singletons_alone():
    with pytest.raises(NotEstimable):
        mh_coverage((7, 0, 0), coverage="lee_chao")


def test_nothing_is_estimable_from_no_captures():
    for estimator in (chao1, jackknife1, mh_coverage):
        with pytest.raises(NotEstimable):
            estimator((0, 0, 0))


def test_chapman_reproduces_krebs_box_2_1():
    """Krebs (2021) Box 2.1: Green & Evans (1940) snowshoe hares, M = 948 tagged, C = 421 caught,
    R = 167 recaptured; the Chapman form (M+1)(C+1)/(R+1) - 1, Krebs's "unbiased estimator" eq. 2.2,
    is printed as 2383 hares."""
    est = chapman(948, 421, 167)
    assert round(est.total) == 2383
    assert est.observed == 948
    assert est.unseen == pytest.approx(est.total - 948)
    assert est.se == pytest.approx(math.sqrt(949 * 422 * 781 * 254 / (168 ** 2 * 169)))


def test_chapman_matches_the_wikipedia_worked_example():
    """https://en.wikipedia.org/wiki/Mark_and_recapture: n = 10, K = 15, k = 5 gives a Chapman
    estimate of 28 (printed truncated)."""
    assert math.floor(chapman(10, 15, 5).total) == 28


def test_chapman_refuses_impossible_overlaps():
    with pytest.raises(ValueError):
        chapman(10, 5, 6)


def test_every_interval_contains_its_estimate():
    for est in (chao1(COTTONTAIL), jackknife1(COTTONTAIL), mh_coverage(COTTONTAIL),
                chapman(948, 421, 167)):
        lo, hi = est.interval
        assert 0 <= lo <= est.unseen <= hi


def test_no_unseen_items_gives_a_degenerate_interval():
    est = jackknife1((0, 4, 4))
    assert est.unseen == 0
    assert est.interval == (0.0, 0.0)


def test_to_record_fits_estimated_residual():
    est = chao1(COTTONTAIL)
    rec = to_record(est, ("source_family_a", "source_family_b"), gold_uncaptured=60, tau=0.25)
    assert rec.estimator == "chao1"
    assert rec.estimate == est.unseen
    assert rec.tolerance == pytest.approx(15)
    assert rec.known_truth_passed is True
    assert to_record(est, ("a", "b")).known_truth_passed is None


def test_to_record_needs_tau_with_gold():
    with pytest.raises(ValueError):
        to_record(chao1(COTTONTAIL), ("a", "b"), gold_uncaptured=60)


def test_estimate_is_immutable():
    est = chao1(COTTONTAIL)
    assert isinstance(est, Estimate)
    with pytest.raises(AttributeError):
        est.unseen = 0
