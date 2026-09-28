import csv
from pathlib import Path

import pytest

from probe_code import cli, k0


def _write(path: Path, rows: list[dict]) -> Path:
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return path


def _codes(sr: int, pm: int, ot: int, blank: int = 0, correct: int = 0, item: str = "K0-1") -> list[dict]:
    codes = ["SR.decompose"] * sr + ["PM.math"] * pm + ["OT"] * ot + ["BLANK"] * blank + ["CORRECT"] * correct
    return [{"student_id": f"S{i:03d}", "item_id": item, "code": c} for i, c in enumerate(codes)]


def _plan(rows: list[dict], extra: int = 0) -> list[dict]:
    ids = [r["student_id"] for r in rows] + [f"X{i:03d}" for i in range(extra)]
    return [{"order": i, "student_id": s, "item_id": "K0-1"} for i, s in enumerate(ids, 1)]


def test_wilson_interval_matches_hand_computation():
    lo, hi = k0.wilson(30, 100)
    assert lo == pytest.approx(0.2189, abs=1e-4)
    assert hi == pytest.approx(0.3958, abs=1e-4)


def test_share_counts_only_errored_solutions_by_top_level_code():
    rows = _codes(sr=35, pm=50, ot=15, blank=7, correct=20)
    rows = rows[100:] + rows[:100]
    r = k0.decide(rows, _plan(rows))
    assert (r.errored, r.selection_representation, r.blank, r.correct) == (100, 35, 7, 20)
    assert r.share == pytest.approx(0.35)
    assert r.decision == "continue"


def test_below_threshold_stops():
    rows = _codes(sr=29, pm=60, ot=11)
    assert k0.decide(rows, _plan(rows)).decision == "stop"


def test_threshold_is_inclusive_at_thirty_percent():
    rows = _codes(sr=30, pm=60, ot=10)
    assert k0.decide(rows, _plan(rows)).decision == "continue"


def test_coding_stops_at_the_hundredth_errored_solution():
    rows = _codes(sr=0, pm=100, ot=0) + [{"student_id": f"T{i}", "item_id": "K0-1", "code": "SR.decompose"}
                                          for i in range(40)]
    r = k0.decide(rows, _plan(rows))
    assert (r.errored, r.selection_representation, r.ignored) == (100, 0, 40)
    assert r.decision == "stop"


def test_rows_must_be_a_contiguous_prefix_of_the_plan():
    rows = _codes(sr=60, pm=40, ot=0)
    plan = _plan(rows)
    with pytest.raises(ValueError, match="S050"):
        k0.decide(rows[:50] + rows[51:], plan)


def test_coded_item_must_be_the_planned_item():
    rows = _codes(sr=60, pm=40, ot=0)
    rows[3] = {**rows[3], "item_id": "K0-2"}
    with pytest.raises(ValueError, match="S003"):
        k0.decide(rows, _plan(rows))


def test_early_k0_under_minimum_is_inconclusive():
    rows = _codes(sr=5, pm=80, ot=14)
    assert k0.decide(rows, _plan(rows), early=True).decision == "inconclusive"


def test_pretest_k0_under_minimum_is_an_error_not_a_decision():
    rows = _codes(sr=5, pm=80, ot=14)
    with pytest.raises(ValueError, match="100"):
        k0.decide(rows, _plan(rows))


def test_unknown_code_is_refused():
    rows = [{"student_id": "S1", "item_id": "K0-1", "code": "XX.foo"}]
    with pytest.raises(ValueError, match="XX"):
        k0.decide(rows, _plan(rows), early=True)


def test_top_column_must_match_the_code_prefix():
    rows = [{"student_id": "S1", "item_id": "K0-1", "top": "PM", "code": "SR.decompose"}]
    with pytest.raises(ValueError, match="S1"):
        k0.decide(rows, _plan(rows), early=True)


def test_sample_plan_is_reproducible_independent_of_roster_order():
    ids = [f"S{i}" for i in range(20)]
    a = k0.sample_plan(ids, ["K0-1", "K0-2"], seed=7)
    assert a == k0.sample_plan(list(reversed(ids)), ["K0-1", "K0-2"], seed=7)
    assert sorted(r["student_id"] for r in a) == sorted(ids)
    assert {r["item_id"] for r in a} <= {"K0-1", "K0-2"}
    assert [r["order"] for r in a] == list(range(1, 21))
    assert k0.sample_plan(ids, ["K0-1", "K0-2"], seed=8) != a


def test_coder_kappa_uses_solutions_either_coder_calls_errored():
    a = [{"student_id": s, "item_id": "K0-1", "code": c} for s, c in
         [("A", "SR.decompose"), ("B", "PM.math"), ("C", "CORRECT"), ("D", "CORRECT"), ("E", "SR.criterion")]]
    b = [{"student_id": s, "item_id": "K0-1", "code": c} for s, c in
         [("A", "SR.criterion"), ("B", "PM.prereq"), ("C", "PM.math"), ("D", "CORRECT"), ("E", "PM.math")]]
    plan = [{"order": i, "student_id": s, "item_id": "K0-1"} for i, s in enumerate("ABCDE", 1)]
    r = k0.coder_kappa(a, b, plan)
    assert r.n == 4
    assert r.raw_agreement == pytest.approx(0.5)


def test_component_share_uses_the_coded_items_components_and_reports_missing_sheets():
    codes = [{"student_id": "A", "item_id": "K0-1", "code": "SR.decompose"},
             {"student_id": "B", "item_id": "K0-2", "code": "PM.math"},
             {"student_id": "C", "item_id": "K0-1", "code": "SR.criterion"}]
    comps = [{"student_id": "A", "component_id": "C1a", "correct": "1"},
             {"student_id": "A", "component_id": "C1b", "correct": "1"},
             {"student_id": "A", "component_id": "C2a", "correct": "0"},
             {"student_id": "B", "component_id": "C2a", "correct": "1"},
             {"student_id": "B", "component_id": "C2b", "correct": "0"}]
    r = k0.component_share(codes, comps)
    assert (r.passed_both, r.selection_representation, r.failed_any, r.missing) == (1, 1, 1, 1)


def test_form_agreement_pairs_items_and_uses_students_who_err_on_both():
    f1 = [{"student_id": s, "item_id": i, "code": c} for s, i, c in
          [("A", "K0-1", "SR.decompose"), ("B", "K0-2", "PM.math"), ("C", "K0-1", "OT"), ("D", "K0-1", "CORRECT")]]
    f2 = [{"student_id": s, "item_id": i, "code": c} for s, i, c in
          [("A", "K0-1b", "SR.criterion"), ("B", "K0-2b", "PM.prereq"), ("C", "K0-1b", "SR.decompose"),
           ("D", "K0-1b", "SR.decompose")]]
    r = k0.form_agreement(f1, f2)
    assert r.n == 3
    assert r.raw_agreement == pytest.approx(2 / 3)
    assert r.sufficient is False


def test_form_agreement_refuses_unpaired_items():
    f1 = [{"student_id": "A", "item_id": "K0-1", "code": "SR.decompose"}]
    f2 = [{"student_id": "A", "item_id": "K0-2b", "code": "SR.decompose"}]
    with pytest.raises(ValueError, match="A"):
        k0.form_agreement(f1, f2)


def test_cli_k0_prints_decision(tmp_path, capsys):
    rows = _codes(sr=40, pm=50, ot=10)
    cli.main(["k0", str(_write(tmp_path / "codes.csv", rows)), "--plan", str(_write(tmp_path / "plan.csv", _plan(rows)))])
    out = capsys.readouterr().out
    assert "continue" in out and "0.400" in out


def test_cli_k0_sample_writes_plan(tmp_path):
    roster = _write(tmp_path / "roster.csv", [{"student_id": f"S{i}"} for i in range(5)])
    cli.main(["k0-sample", str(roster), "--items", "K0-1,K0-2", "--seed", "3", "--out", str(tmp_path / "plan.csv")])
    with (tmp_path / "plan.csv").open() as f:
        assert len(list(csv.DictReader(f))) == 5


def test_cli_k0_kappa(tmp_path, capsys):
    rows = _codes(sr=5, pm=5, ot=0)
    cli.main(["k0-kappa", str(_write(tmp_path / "a.csv", rows)), str(_write(tmp_path / "b.csv", rows)), "--plan", str(_write(tmp_path / "plan.csv", _plan(rows)))])
    assert "n=10" in capsys.readouterr().out


def test_cli_form_agreement(tmp_path, capsys):
    f1 = _codes(sr=5, pm=5, ot=0)
    f2 = _codes(sr=5, pm=5, ot=0, item="K0-1b")
    cli.main(["form-agreement", str(_write(tmp_path / "a.csv", f1)), str(_write(tmp_path / "b.csv", f2))])
    assert "n=10" in capsys.readouterr().out


def test_form_agreement_reports_a_reproducible_bootstrap_interval_around_kappa():
    codes = ["SR.decompose", "PM.math", "OT", "SR.criterion", "PM.prereq"] * 14
    swapped = codes[1:] + codes[:1]
    f1 = [{"student_id": f"S{i}", "item_id": "K0-1", "code": c} for i, c in enumerate(codes)]
    f2 = [{"student_id": f"S{i}", "item_id": "K0-1b", "code": c if i % 3 else swapped[i]} for i, c in enumerate(codes)]
    r = k0.form_agreement(f1, f2)
    assert r.sufficient is True
    assert r.ci[0] <= r.kappa <= r.ci[1]
    assert r.ci == k0.form_agreement(f1, f2).ci


def test_sample_plan_excludes_listed_students(tmp_path):
    roster = _write(tmp_path / "roster.csv", [{"student_id": f"S{i}"} for i in range(6)])
    excluded = _write(tmp_path / "early.csv", [{"student_id": "S1"}, {"student_id": "S4"}])
    cli.main(["k0-sample", str(roster), "--items", "K0-1,K0-2", "--seed", "3", "--out", str(tmp_path / "plan.csv"),
              "--exclude", str(excluded)])
    with (tmp_path / "plan.csv").open() as f:
        assert {r["student_id"] for r in csv.DictReader(f)} == {"S0", "S2", "S3", "S5"}


def test_decision_refuses_a_plan_on_unregistered_items():
    rows = _codes(sr=60, pm=40, ot=0, item="K0-1b")
    plan = [{**r, "item_id": "K0-1b"} for r in _plan(rows)]
    with pytest.raises(ValueError, match="K0-1b"):
        k0.decide(rows, plan)


def test_coder_kappa_is_limited_to_the_plan_prefix():
    a = _codes(sr=60, pm=40, ot=0) + [{"student_id": "T1", "item_id": "K0-1", "code": "SR.decompose"}]
    b = _codes(sr=60, pm=40, ot=0) + [{"student_id": "T1", "item_id": "K0-1", "code": "PM.math"}]
    r = k0.coder_kappa(a, b, _plan(a))
    assert r.n == 100 and r.raw_agreement == 1.0
