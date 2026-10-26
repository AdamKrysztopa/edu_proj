"""The D1b decision rule (plan §3.4, criterion (b)) and its L7.3 checks."""
import json
from pathlib import Path

import pytest

import rule

D1 = Path(__file__).resolve().parents[2] / "d1_demonstrator"


def _rows(gap, cov, n=15):
    return ([{"arm": "gap", "j1": g, "j2": g} for g in gap] + [{"arm": "covered", "j1": c, "j2": c} for c in cov])


def test_the_exact_permutation_p_reproduces_d1():
    rows = json.loads((D1 / "result.json").read_text())["rows"]
    assert rule.permutation_p(rows, "agreed") == pytest.approx(0.682983682983683)


def test_the_exact_p_matches_brute_force_on_a_small_sheet():
    import itertools
    rows = _rows(["new", "new", "partly", "new"], ["new", "already written", "partly", "partly"])
    rows[1]["j2"] = "partly"
    obs = rule.difference(rows, [r["arm"] for r in rows], "agreed")
    hits = total = 0
    for idx in itertools.combinations(range(8), 4):
        arms = ["gap" if i in idx else "covered" for i in range(8)]
        hits += rule.difference(rows, arms, "agreed") >= obs - 1e-12
        total += 1
    assert rule.permutation_p(rows, "agreed") == pytest.approx(hits / total)


def test_a_planted_positive_continues_with_the_best_case_p():
    res = rule.decide(_rows(["new"] * 15, ["already written"] * 15))
    assert res["decision"] == "Continue"
    assert res["agreed"]["p"] == pytest.approx(1 / 155117520)


@pytest.mark.parametrize("gap,cov", [(["new"] * 15, ["new"] * 15),
                                     (["already written"] * 15, ["already written"] * 15),
                                     (["new"] * 7 + ["partly"] * 8, ["new"] * 4 + ["partly"] * 11)])
def test_null_and_borderline_sheets_change(gap, cov):
    assert rule.decide(_rows(gap, cov))["decision"] == "Change"


def test_judge_disagreement_on_the_gap_answers_changes():
    rows = _rows(["new"] * 15, ["already written"] * 15)
    for r in rows[:15]:
        r["j2"] = "partly"
    assert rule.decide(rows)["decision"] == "Change"


def test_a_continue_must_also_hold_on_judge_a_alone():
    rows = _rows(["new"] * 15, ["already written"] * 15)
    for r in rows[:15]:
        r["j1"] = "partly"
    for r in rows[:9]:
        r["j2"] = "partly"
    res = rule.decide(rows)
    assert res["judge_a"]["difference"] < rule.MIN_DIFF
    assert res["decision"] == "Change"


def test_stances_only_is_no_reading():
    assert rule.decide(_rows(["no content"] * 15, ["no content"] * 15))["decision"] == "No reading"


def test_the_content_floor_scales_with_the_sheet():
    assert rule.content_floor(30) == 16 and rule.content_floor(24) == 13 and rule.content_floor(20) == 11


@pytest.mark.parametrize("n", [12, 10])
def test_the_checks_hold_at_the_fallback_sizes(n):
    assert rule.decide(_rows(["new"] * n, ["already written"] * n))["decision"] == "Continue"
    assert rule.decide(_rows(["new"] * n, ["new"] * n))["decision"] == "Change"


def test_l73_checks_all_pass():
    assert rule.l73_checks()["all_pass"]
