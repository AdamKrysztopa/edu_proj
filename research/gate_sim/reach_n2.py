"""N2 reachable readings under the registered rules, from the run-1 baselines (I5 step 3).

    uv run --directory reconstruct python ../research/gate_sim/reach_n2.py

Observed (research/n2/e_plant_eabst_report.md §1.1, §2.1): E-PLANT ungated a_u = 5 of 24
(floor ⌈24/3⌉ = 8; 5 of 23 with t-conc-08 excluded); E-ABST raw arm answered 5 of 24.
The registered rules are called, not copied: reconstruct.eplant.eplant_decision and
reconstruct.eabst.e_abst_gate. Writes n2_reach.json. Not simulated: an exact enumeration.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from types import SimpleNamespace

from reconstruct.eabst import e_abst_gate
from reconstruct.eplant import eplant_decision

from residual.reach import ORDER, collect, eabst_space, eplant_space, regions

HERE = Path(__file__).resolve().parent


def eplant(**p):
    return eplant_decision(**p)[0]


def eplant_floor_met(**p):
    """eplant_decision reads a_u_full only in its validity-floor check (eplant.py:526-531), so
    a_u_full = n_full is the registered tree with the floor taken as met."""
    return eplant_decision(**{**p, "a_u_full": p["n_full"]})[0]


def eabst(**p):
    n = p["n_included"]
    v = lambda x: SimpleNamespace(value=x)  # noqa: E731
    return e_abst_gate.__wrapped__(
        far_raw=v(p["f_r"] / n if n else 0.0), far_pipe=v(p["f_p"] / n if n else 0.0),
        n_included=v(n), kappa=v(p["kappa"]), zero_extraction_or_capped=v(p["zero_extraction_or_capped"]),
    ).outcome


def eplant_block(n_full: int, a_u_full: int) -> dict:
    reg = regions(eplant, eplant_space(n_full=n_full, a_u_full=a_u_full))
    cont = collect(eplant_floor_met, eplant_space(n_full=n_full, a_u_full=a_u_full), "continue")
    bc = sorted({(p["b"], p["c"]) for p in cont})
    return {
        "n_full": n_full, "a_u_full": a_u_full, "registered_floor": math.ceil(n_full / 3),
        "outcome_counts": reg.counts, "best_reachable": reg.best,
        "example_best": reg.examples[reg.best],
        "if_floor_met": {
            "continue_points": len(cont),
            "continue_b_c": bc,
            "continue_min_n": min(p["n"] for p in cont) if cont else None,
            "continue_requires_a_u_post_cap": sorted({p["a_u"] for p in cont}),
            "example": cont[0] if cont else None,
        },
        "amendment_floor": {
            "max_floor_with_continue_reachable": a_u_full if cont else None,
            "as_fraction_of_n_full": round(a_u_full / n_full, 4) if cont else None,
            "ceil_rule": next((f"ceil(n/{d})" for d in range(2, 25) if math.ceil(n_full / d) <= a_u_full), None),
        },
    }


def main() -> None:
    plant = {"pooled_24": eplant_block(24, 5), "t_conc_08_excluded_23": eplant_block(23, 5)}
    reg = regions(eabst, eabst_space(n_items=24, raw_answered=5))
    cont = collect(eabst, eabst_space(n_items=24, raw_answered=5), "continue")
    corners = sorted({(p["n_included"], p["f_r"], p["f_p"]) for p in cont})
    out = {
        "source": "research/n2/e_plant_eabst_report.md §1.1, §2.1; rules at reconstruct HEAD",
        "label": "exact enumeration over counts the unrun arms could produce (arithmetic constraints only)",
        "order": ORDER,
        "e_plant": plant,
        "e_abst": {
            "n_items": 24, "raw_answered": 5, "outcome_counts": reg.counts, "best_reachable": reg.best,
            "continue_corners_n_included_f_r_f_p": corners,
        },
    }
    (HERE / "n2_reach.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({k: (v["best_reachable"], v["if_floor_met"]["continue_b_c"], v["amendment_floor"])
                      for k, v in plant.items()}, indent=1))
    print("E-ABST", reg.counts, corners)


if __name__ == "__main__":
    main()
