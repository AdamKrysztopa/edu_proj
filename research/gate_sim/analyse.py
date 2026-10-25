"""Summarise the I5 grid outputs into summary.json and tables.md (no simulation here).

    python3 research/gate_sim/analyse.py
"""
from __future__ import annotations

import gzip
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
LABEL = "SYNTHETIC — planning simulation; never a criterion, never feeds a gate"


def load(name):
    path = HERE / name
    raw = gzip.decompress(path.read_bytes()) if name.endswith(".gz") else path.read_bytes()
    return json.loads(raw)


def p(cell, key):
    return cell["freq"].get(key, 0.0)


def gate(cell, outcome, d=0.1, c=1.85):
    return p(cell, f"gate|d={d}|c={c}|{outcome}")


def design(cell):
    return {k: cell[k] for k in ("k", "n", "n1", "share", "icc", "ties", "r", "pooled_minority")}


def main() -> None:
    grid = load("grid.json")
    cells = load("cells.json.gz")["cells"]
    extra = load("l73_cells.json.gz")["cells"]
    boot = load("bootstrap.json")
    oracle = load("near_oracle.json")
    reach = load("n2_reach.json")
    floor = grid["spec"]["minority_floor"]
    c_grid = grid["spec"]["c_grid"]
    out: dict = {"label": LABEL, "reps": grid["reps"], "spec_sha256": grid["spec_sha256"]}

    best = [c for c in extra if c["role"] == "best_reachable"]
    out["best_reachable"] = [{"icc": c["icc"], "p_continue": gate(c, "continue")} for c in best]

    planted = [c for c in cells if c["gain"] == 0.2]
    above = [c for c in planted if c["pooled_minority"] >= floor]
    below = [c for c in planted if c["pooled_minority"] < floor]
    fails = sorted((c for c in above if gate(c, "continue") < 0.8), key=lambda c: gate(c, "continue"))
    out["planted_positive"] = {
        "cells_at_or_above_floor": len(above),
        "min_p_continue_above_floor": min(gate(c, "continue") for c in above),
        "n_above_floor_below_0.8": len(fails),
        "fails_above_floor": [{**design(c), "p_continue": gate(c, "continue")} for c in fails],
        "cells_below_floor": len(below),
        "below_floor_p_continue_range": [min(gate(c, "continue") for c in below),
                                         max(gate(c, "continue") for c in below)],
    }
    out["planted_positive"]["by_r"] = {
        str(r): {"cells_at_or_above_floor": len([c for c in above if c["r"] == r]),
                 "min_p_continue_above_floor": min(gate(c, "continue") for c in above if c["r"] == r),
                 "minority_floor_where_every_cell_passes": next(
                     (m for m in range(2, 200) if all(gate(c, "continue") >= 0.8 for c in planted
                                                      if c["r"] == r and c["pooled_minority"] >= m)), None)}
        for r in grid["spec"]["grid"]["r"]}
    at_delta = [c for c in cells if c["gain"] == 0.1]
    out["false_stop_at_gain_delta_by_c"] = {
        str(cc): {"max_all": max(gate(c, "stop", c=cc) for c in at_delta),
                  "max_floor": max(gate(c, "stop", c=cc) for c in at_delta if c["pooled_minority"] >= floor),
                  "median_floor": sorted(gate(c, "stop", c=cc) for c in at_delta
                                         if c["pooled_minority"] >= floor)[len([c for c in at_delta if c["pooled_minority"] >= floor]) // 2]}
        for cc in c_grid}
    out["c_holding_false_stop_0.05_floor_cells"] = next(
        (cc for cc in c_grid if out["false_stop_at_gain_delta_by_c"][str(cc)]["max_floor"] <= 0.05), None)
    for kind in ("random", "size_noise"):
        cs = [c for c in extra if c["role"] == f"stand_in_{kind}"]
        worst = max(cs, key=lambda c: gate(c, "continue"))
        out[f"stand_in_{kind}"] = {"cells": len(cs), "max_p_continue": gate(worst, "continue"),
                                   "worst": design(worst)}

    ma = defaultdict(dict)
    for c in (c for c in extra if c["role"] == "min_areas"):
        ma[c["icc"]][c["n"]] = ma[c["icc"]].get(c["n"], {}) | (
            {"p_stop_null": gate(c, "stop"), "p_continue_null": gate(c, "continue"),
             "ms5_stop_null": p(c, "ms5|d=0.1|stop")} if c["gain"] == 0.0 else
            {"p_continue_gain_0.20": gate(c, "continue")})
    out["min_areas_16_4_three_golds"] = {
        str(icc): {"by_n": {str(n): v for n, v in sorted(rows.items())},
                   "min_n_p_stop_ge_0.8": next((n for n, v in sorted(rows.items()) if v.get("p_stop_null", 0) >= 0.8), None)}
        for icc, rows in ma.items()}

    def fc_curve(cs):
        return {str(c): max(gate(x, "continue", c=c) for x in cs) for c in c_grid}

    null_close = [c for c in cells if c["gain"] == 0.0]
    null_strong = [c for c in extra if c["role"] == "null_one_strong"]
    curves = {"close_all_cells": fc_curve(null_close),
              "close_floor_cells": fc_curve([c for c in null_close if c["pooled_minority"] >= floor]),
              "one_strong_all_cells": fc_curve(null_strong),
              "one_strong_floor_cells": fc_curve([c for c in null_strong if c["pooled_minority"] >= floor])}
    out["false_continue_max_by_c"] = curves
    out["c_holding_false_continue_0.05"] = {
        k: next((float(c) for c, v in v_.items() if v <= 0.05), None) for k, v_ in curves.items()}
    worst_null = max(null_strong, key=lambda c: gate(c, "continue"))
    out["worst_false_continue_at_1.85"] = {**design(worst_null), "p_continue": gate(worst_null, "continue")}

    # the DS3 comparison and the design table at r = 0.6, ties 0
    def find(k, n, share, icc, gain, ties=0.0, r=0.6):
        for c in cells:
            if (c["k"], c["n"], c["share"], c["icc"], c["gain"], c["ties"], c["r"]) == (k, n, share, icc, gain, ties, r):
                return c
        return None

    ds3 = {}
    for share, lab in ((0.5, "balanced"), (0.75, "15/5"), (0.8, "16/4")):
        g2, g0 = find(3, 20, share, 0.0, 0.2), find(3, 20, share, 0.0, 0.0)
        ds3[lab] = {"p_continue_gain_0.20": gate(g2, "continue"), "p_stop_gain_0": gate(g0, "stop"),
                    "ms5_p_continue_gain_0.20": p(g2, "ms5|d=0.1|continue"), "ms5_p_stop_gain_0": p(g0, "ms5|d=0.1|stop")}
    out["ds3_cell_3x20_icc0_r0.6"] = ds3

    rows = []
    for k in (1, 2, 3, 4, 5, 6):
        for n in (15, 20, 30):
            for share in (0.5, 0.75, 0.8):
                for icc in (0.0, 0.3):
                    g2, g1, g0 = find(k, n, share, icc, 0.2), find(k, n, share, icc, 0.1), find(k, n, share, icc, 0.0)
                    rows.append({**design(g0),
                                 "p_continue_gain_0.20": gate(g2, "continue"),
                                 "p_continue_gain_0.10": gate(g1, "continue"),
                                 "p_stop_gain_0": gate(g0, "stop"), "p_continue_gain_0": gate(g0, "continue"),
                                 "p_stop_gain_0.20": gate(g2, "stop"),
                                 "d0.05_p_continue_0.20": gate(g2, "continue", d=0.05), "d0.05_p_stop_0": gate(g0, "stop", d=0.05),
                                 "d0.15_p_continue_0.20": gate(g2, "continue", d=0.15), "d0.15_p_stop_0": gate(g0, "stop", d=0.15),
                                 "look1_p_continue_0.20": p(g2, "look1|d=0.1|c=1.85|continue"),
                                 "look1_p_stop_0": p(g0, "look1|d=0.1|c=1.85|stop"),
                                 "ms3_release_0.20": p(g2, "ms3|d=0.1|True"), "ms3_release_0": p(g0, "ms3|d=0.1|True"),
                                 "ms5_continue_0.20": p(g2, "ms5|d=0.1|continue"), "ms5_stop_0": p(g0, "ms5|d=0.1|stop"),
                                 "unclustered_p_continue_0": p(g0, "unclustered|d=0.1|c=1.85|continue"),
                                 "random_effects_p_continue_0.20": p(g2, "random_effects|d=0.1|c=1.85|continue"),
                                 "random_effects_p_stop_0": p(g0, "random_effects|d=0.1|c=1.85|stop"),
                                 "bias_min_point_gain_0.20": g2["mean_min_point_minus_true_gain"]})
    out["design_table"] = rows

    ties_effect = []
    for share in (0.5, 0.8):
        a, b = find(3, 20, share, 0.0, 0.2, ties=0.0), find(3, 20, share, 0.0, 0.2, ties=0.3)
        ties_effect.append({"share": share, "p_continue_ties0": gate(a, "continue"),
                            "p_continue_ties0.3": gate(b, "continue") if b else None})
    out["ties_effect_3x20_icc0"] = ties_effect
    out["infeasible_cells"] = len(grid["infeasible_cells"])
    unc = [c for c in cells if c["icc"] == 0.3 and c["gain"] == 0.0 and "unclustered|d=0.1|c=1.85|continue" in c["freq"]]
    out["unclustered_vs_clustered_false_continue_icc0.3"] = {
        "max_unclustered": max(p(c, "unclustered|d=0.1|c=1.85|continue") for c in unc),
        "max_clustered": max(gate(c, "continue") for c in unc)}
    cand = []
    for k, n, n1 in ((3, 20, 16), (4, 20, 16), (5, 20, 16), (6, 20, 16), (3, 30, 24), (4, 30, 24), (5, 30, 24),
                     (6, 30, 24)):
        for r in grid["spec"]["grid"]["r"]:
            for icc in grid["spec"]["grid"]["icc"]:
                row = {c["gain"]: c for c in cells
                       if (c["k"], c["n"], c["n1"], c["r"], c["icc"], c["ties"]) == (k, n, n1, r, icc, 0.0)}
                cand.append({"k": k, "n": n, "split": f"{n1}/{n - n1}", "r": r, "icc": icc,
                             "pooled_minority": row[0.0]["pooled_minority"],
                             "p_continue_gain_0.20": gate(row[0.2], "continue"),
                             "p_stop_gain_0": gate(row[0.0], "stop"),
                             "false_stop_gain_delta": gate(row[0.1], "stop"),
                             "false_stop_gain_delta_look1": p(row[0.1], "look1|d=0.1|c=1.85|stop")})
    out["candidate_designs_16_4_or_24_6"] = cand
    unc_fs = [c for c in cells if c["gain"] == 0.1 and c["sensitivities"] and c["icc"] > 0]
    out["false_stop_gain_delta_clustered_vs_unclustered_icc0.3"] = {
        "cells": len(unc_fs),
        "max_clustered": max(gate(c, "stop") for c in unc_fs),
        "max_unclustered": max(p(c, "unclustered|d=0.1|c=1.85|stop") for c in unc_fs),
        "max_clustered_floor": max(gate(c, "stop") for c in unc_fs if c["pooled_minority"] >= floor),
        "max_unclustered_floor": max(p(c, "unclustered|d=0.1|c=1.85|stop") for c in unc_fs if c["pooled_minority"] >= floor),
        "cells_unclustered_lower": sum(p(c, "unclustered|d=0.1|c=1.85|stop") < gate(c, "stop") for c in unc_fs)}
    fl = [c for c in at_delta if c["pooled_minority"] >= floor]
    fl30 = [c for c in at_delta if c["pooled_minority"] >= 30]
    out["false_stop_gain_delta_look1_vs_two_looks_floor25"] = {
        "look1_max": max(p(c, "look1|d=0.1|c=1.85|stop") for c in fl),
        "two_look_max": max(gate(c, "stop") for c in fl),
        "two_look_max_minority_ge_30": max(gate(c, "stop") for c in fl30),
        "two_look_mean_minority_ge_30": round(sum(gate(c, "stop") for c in fl30) / len(fl30), 4),
        "cells_minority_ge_30": len(fl30),
        "cells_minority_ge_30_above_0.05": sum(gate(c, "stop") > 0.05 for c in fl30)}
    nr = load("null_one_strong_r.json")["cells"]
    out["false_continue_one_strong_r0.3_r0.9_at_1.85"] = {
        str(r): max(gate(c, "continue") for c in nr if c["r"] == r) for r in (0.3, 0.9)}
    out["stand_in_mean_of_k"] = load("stand_in_mean_of_k.json")["cells"]
    out["bootstrap"] = boot["cells"]
    out["bootstrap_B"] = boot.get("boot")
    out["near_oracle"] = oracle["cells"]
    out["n2_reach"] = {"e_plant": {k: {"best": v["best_reachable"], "counts": v["outcome_counts"],
                                       "continue_b_c_if_floor_met": v["if_floor_met"]["continue_b_c"],
                                       "amendment_floor": v["amendment_floor"]}
                                   for k, v in reach["e_plant"].items()},
                       "e_abst": {k: reach["e_abst"][k] for k in ("best_reachable", "outcome_counts",
                                                                   "continue_corners_n_included_f_r_f_p")}}
    (HERE / "summary.json").write_text(json.dumps(out, indent=1) + "\n")

    lines = [f"# I5 tables ({LABEL})", "", f"{grid['reps']} replicates per cell; δ = 0.10, c = 1.85, two looks "
             "unless stated; r = 0.6, ties 0, baselines 'close' (0.62 and 0.60).", "",
             "| golds | areas | split | ICC | pooled minority | P(C\\|0.20) | P(C\\|0.10) | P(S\\|0) | P(C\\|0) | "
             "δ=0.05 P(C\\|0.20)/P(S\\|0) | δ=0.15 P(C\\|0.20)/P(S\\|0) | MS3 release 0.20/0 | MS5 C\\|0.20 / S\\|0 |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['k']} | {r['n']} | {r['n1']}/{r['n'] - r['n1']} | {r['icc']} | {r['pooled_minority']} | "
                     f"{r['p_continue_gain_0.20']:.2f} | {r['p_continue_gain_0.10']:.2f} | {r['p_stop_gain_0']:.2f} | "
                     f"{r['p_continue_gain_0']:.3f} | {r['d0.05_p_continue_0.20']:.2f}/{r['d0.05_p_stop_0']:.2f} | "
                     f"{r['d0.15_p_continue_0.20']:.2f}/{r['d0.15_p_stop_0']:.2f} | "
                     f"{r['ms3_release_0.20']:.2f}/{r['ms3_release_0']:.2f} | {r['ms5_continue_0.20']:.2f}/{r['ms5_stop_0']:.2f} |")
    (HERE / "tables.md").write_text("\n".join(lines) + "\n")
    write_report(out)
    print(json.dumps({k: v for k, v in out.items() if k not in ("design_table", "bootstrap", "near_oracle")}, indent=1))


def write_report(s: dict) -> None:
    """report.json for the wave report; every number is read from summary.json."""
    rows = [{"primary_golds": r["k"], "areas_per_gold": r["n"], "split": f"{r['n1']}/{r['n'] - r['n1']}",
             "p_continue_true_gain_0.20": r["p_continue_gain_0.20"], "p_stop_true_gain_0": r["p_stop_gain_0"]}
            for r in s["design_table"] if r["n"] == 20 and r["n1"] == 16 and r["icc"] == 0.0]
    p3 = next(r for r in rows if r["primary_golds"] == 3)
    p5 = next(r for r in rows if r["primary_golds"] == 5)
    pp = s["planted_positive"]
    ma = s["min_areas_16_4_three_golds"]["0.0"]
    max_stop = max(r["p_stop_true_gain_0"] for r in rows)
    rep = {
        "item": "I5",
        "card": {
            "question": ("At the N3 rules set on 2026-10-24 and the expected 16/4 split, which designs can read "
                         "Continue or Stop, and can N2's registered gates still read Continue?"),
            "answer": (f"At map-baseline correlation 0.6, a true gain of 0.20 continues with P = "
                       f"{p3['p_continue_true_gain_0.20']:.3f} at 3 x 20 areas (16/4) and "
                       f"{p5['p_continue_true_gain_0.20']:.3f} at 5 x 20; a null stops with P <= {max_stop:.3f} up to "
                       f"6 x 20, and P >= 0.8 needs {ma['min_n_p_stop_ge_0.8']} areas per gold (SYNTHETIC). "
                       "E-PLANT's best reachable reading is Change."),
            "changed": ("Proposed minimum design keyed to the map-baseline correlation measured before gold: 5 golds "
                        "of 20 areas if it is at least 0.6, 5 of 30 if at least 0.3; gold items per area leaves K; "
                        "no E-PLANT floor amendment."),
        },
        "worked": (f"Stand-ins fail as required: random P(Continue) <= {s['stand_in_random']['max_p_continue']}, "
                   f"size+noise <= {s['stand_in_size_noise']['max_p_continue']}; false Continue <= "
                   f"{s['false_continue_max_by_c']['one_strong_all_cells']['1.85']} at c = 1.85."),
        "failed": (f"Planted gain 0.20 misses P(Continue) >= 0.8 in {pp['n_above_floor_below_0.8']} of "
                   f"{pp['cells_at_or_above_floor']} cells at DS3's minority floor 25 (min "
                   f"{pp['min_p_continue_above_floor']})."),
        "figure": {
            "title": (f"Three golds of 20 areas at 16/4 continue a 0.20 gain with P = "
                      f"{p3['p_continue_true_gain_0.20']:.2f}; Stop never reaches 0.8"),
            "kind": "line",
            "rows": rows,
            "reference": "P = 0.8: the L7.3 planted-positive pass mark and the decisive-Stop target",
            "source": ("research/gate_sim/summary.json design_table (n = 20, n1 = 16, icc = 0, r = 0.6, ties 0; "
                       "fields p_continue_gain_0.20, p_stop_gain_0)"),
        },
    }
    (HERE / "report.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
