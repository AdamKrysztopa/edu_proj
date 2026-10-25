"""I5: the registered N2 rules over every count left open by the run-1 baselines."""
from types import SimpleNamespace

from reconstruct.eabst import e_abst_gate
from reconstruct.eplant import eplant_decision

from residual.reach import collect, eabst_space, eplant_space, regions


def eplant(**p):
    return eplant_decision(**p)[0]


def eplant_floor_met(**p):
    return eplant_decision(**{**p, "a_u_full": p["n_full"]})[0]


def eabst(**p):
    n = p["n_included"]
    v = lambda x: SimpleNamespace(value=x)  # noqa: E731
    return e_abst_gate.__wrapped__(
        far_raw=v(p["f_r"] / n if n else 0.0), far_pipe=v(p["f_p"] / n if n else 0.0),
        n_included=v(n), kappa=v(p["kappa"]), zero_extraction_or_capped=v(p["zero_extraction_or_capped"]),
    ).outcome


def test_eplant_continue_is_unreachable_at_five_of_twenty_four():
    reg = regions(eplant, eplant_space(n_full=24, a_u_full=5, n_min=18))
    assert "continue" not in reg.counts
    assert reg.best == "change" and reg.counts["stop"] > 0


def test_eplant_continue_with_the_floor_met_needs_b5_c0():
    cont = collect(eplant_floor_met, eplant_space(n_full=24, a_u_full=5, n_min=18), "continue")
    assert cont and {(p["b"], p["c"]) for p in cont} == {(5, 0)}


def test_eabst_continue_corners_match_the_closeout_report():
    cont = collect(eabst, eabst_space(n_items=24, raw_answered=5), "continue")
    corners = {(p["n_included"], p["f_r"], p["f_p"]) for p in cont}
    assert corners == {(20, 4, 0), (20, 5, 0), (20, 5, 1), (21, 5, 0), (22, 5, 0), (23, 5, 0), (24, 5, 0)}
