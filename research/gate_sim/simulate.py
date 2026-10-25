"""SYNTHETIC simulation of the N3 gate at the rules set on 2026-10-24 (I5 steps 4 and 5).

    uv run --directory residual python ../research/gate_sim/simulate.py [--reps N] [--time]

Every output is SYNTHETIC: a known-truth planning simulation from the specification in SPEC. It
informs the §22 threshold rows; it is never a criterion and never feeds a gate.

Model. Per gold: n areas in clusters of 4; a latent liability (cluster share = ICC) ranks the areas
and the top n1 are labelled missed (fixed class split). Every score is μ·y + noise with unit
variance; noise has a cluster part (share ICC) and an area part, each equicorrelated at r across
the map and the baselines, so a score's true AUROC is Φ(μ/√2). Ties: the map's scores below a
threshold q are set to q, with μ re-calibrated so the tied map keeps its target AUROC.
Gate: residual.baselines.n3_reading on residual.baselines.pool_stats (clustered DeLong,
Obuchowski form), primary set of k golds, then one fallback gold of the same design pooled in once.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
import math
import random
import sys
import time
from multiprocessing import Pool
from pathlib import Path
from statistics import NormalDist

from residual import auroc as AU
from residual import baselines as BL
from residual.auroc import GoldData

HERE = Path(__file__).resolve().parent
LABEL = "SYNTHETIC — planning simulation; never a criterion, never feeds a gate"
N = NormalDist()
SEED = 20261024

BASE = ("area_size", "retrieval_support_density", "corpus_term_frequency", "plain_llm", "type_prior",
        "jev_text_form")
SPEC = {
    "label": LABEL, "seed": SEED, "date": "2026-10-24",
    "set_rules": {"delta": 0.10, "c": 1.85, "pooling": "common effect, golds as fixed strata, weights n1*n0",
                  "continue": "intersection-union over K", "stop": "Bonferroni over K",
                  "looks": "primary set, then one fallback gold pooled in once, same c"},
    "variance": "clustered DeLong (Obuchowski 1997); clusters of 4 areas registered in every cell",
    "baseline_auroc": {"strongest": 0.62, "close": 0.60, "weak": 0.50},
    "spread": {"close": "area_size 0.62, every other baseline 0.60 (DS3 worst case: all within 0.02)",
               "one_strong": "area_size 0.62, every other baseline 0.50 (least favourable for false Continue)"},
    "K": "residual.baselines.competing_set(n_golds): 5 baselines, 6 once every gold has two others",
    "map_auroc": "0.62 + gain",
    "grid": {"golds": [1, 2, 3, 4, 5, 6], "areas": [15, 20, 30],
             "missed_share": [0.3, 0.45, 0.5, 0.6, 0.75, 0.8], "icc": [0.0, 0.3], "ties": [0.0, 0.3],
             "r": [0.3, 0.6, 0.9], "gain": [0.0, 0.10, 0.20]},
    "c_grid": [1.645, 1.75, 1.85, 1.95, 2.05, 2.15, 2.25, 2.35, 2.5, 2.65],
    "deltas": [0.05, 0.10, 0.15],
    "minority_floor": 25,
    "cluster_size": 4,
}


# --- calibration ---------------------------------------------------------------------------------

def _p_y_lt_x_lt_q(mu: float, q: float, steps: int = 2000) -> float:
    lo = min(q, mu) - 10.0
    if q <= lo:
        return 0.0
    h = (q - lo) / steps
    f = lambda x: N.pdf(x - mu) * N.cdf(x)  # noqa: E731
    s = f(lo) + f(q) + sum((4 if i % 2 else 2) * f(lo + i * h) for i in range(1, steps))
    return s * h / 3


def tie_threshold(mu: float, ties: float, share: float) -> float:
    lo, hi = -15.0, 15.0 + mu
    for _ in range(100):
        mid = (lo + hi) / 2
        if share * N.cdf(mid - mu) + (1 - share) * N.cdf(mid) < ties:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def tied_auroc(mu: float, ties: float, share: float) -> float:
    if ties == 0:
        return N.cdf(mu / math.sqrt(2))
    q = tie_threshold(mu, ties, share)
    return N.cdf(mu / math.sqrt(2)) - _p_y_lt_x_lt_q(mu, q) + 0.5 * N.cdf(q - mu) * N.cdf(q)


def calibrate(target: float, ties: float, share: float) -> tuple[float, float | None] | None:
    """(μ, tie threshold) giving the tied map AUROC `target`; None when ties make it unreachable."""
    if ties == 0:
        return math.sqrt(2) * N.inv_cdf(target), None
    if tied_auroc(12.0, ties, share) < target:
        return None
    lo, hi = 0.0, 12.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if tied_auroc(mid, ties, share) < target:
            lo = mid
        else:
            hi = mid
    mu = (lo + hi) / 2
    return mu, tie_threshold(mu, ties, share)


def mu_of(a: float) -> float:
    return math.sqrt(2) * N.inv_cdf(a)


# --- data ----------------------------------------------------------------------------------------

def gen_gold(rng: random.Random, cell: dict, map_spec: tuple) -> GoldData:
    n, icc, r = cell["n"], cell["icc"], cell["r"]
    n1 = cell["n1"]
    cs = SPEC["cluster_size"]
    cl = [i // cs for i in range(n)]
    nc = cl[-1] + 1
    si, sa = math.sqrt(icc), math.sqrt(1 - icc)
    sr, sq = math.sqrt(r), math.sqrt(1 - r)
    u = [rng.gauss(0, 1) for _ in range(nc)]
    liab = [si * u[cl[i]] + sa * rng.gauss(0, 1) for i in range(n)]
    order = sorted(range(n), key=lambda i: -liab[i])
    missed = set(order[:n1])
    y = [i in missed for i in range(n)]
    z0c = [rng.gauss(0, 1) for _ in range(nc)]
    z0a = [rng.gauss(0, 1) for _ in range(n)]

    def noise() -> list[float]:
        zc = [rng.gauss(0, 1) for _ in range(nc)]
        za = [rng.gauss(0, 1) for _ in range(n)]
        return [si * (sr * z0c[cl[i]] + sq * zc[cl[i]]) + sa * (sr * z0a[i] + sq * za[i]) for i in range(n)]

    scores: dict[str, list[float]] = {}
    for name, mu in zip(BASE, cell["base_mu"]):
        e = noise()
        scores[name] = [mu * y[i] + e[i] for i in range(n)]
    kind = map_spec[0]
    if kind == "binormal":
        mu, q = map_spec[1], map_spec[2]
        e = noise()
        s = [mu * y[i] + e[i] for i in range(n)]
        scores["map"] = s if q is None else [max(v, q) for v in s]
    elif kind == "perfect":
        scores["map"] = [1.0 if v else 0.0 for v in y]
    elif kind == "random":
        scores["map"] = [rng.gauss(0, 1) for _ in range(n)]
    elif kind == "size_noise":
        scores["map"] = [0.9 * v + math.sqrt(1 - 0.81) * rng.gauss(0, 1) for v in scores["area_size"]]
    else:
        raise ValueError(kind)
    return GoldData(labels=y, clusters=cl, scores=scores)


# --- readings ------------------------------------------------------------------------------------

def re_reading(stats, others, c, delta) -> str:
    alpha = BL.one_sided_alpha(c)
    res = [AU.pool_random(BL.per_gold_estimates(stats, o)) for o in others]
    if min(r.upper(alpha / len(others)) for r in res) < delta:
        return "stop"
    if min(r.lower(alpha) for r in res) > 0 and min(r.delta for r in res) >= delta:
        return "continue"
    return "inconclusive"


def two_look(r1: str, r2_fn) -> str:
    return r1 if r1 != "inconclusive" else r2_fn()


def run_cell(cell: dict) -> dict:
    key = json.dumps({k: v for k, v in cell.items() if k not in ("reps", "base_mu")}, sort_keys=True)
    rng = random.Random(f"{SEED}:{key}")
    k, reps = cell["k"], cell["reps"]
    names = ["map", *BASE]
    K1, K2 = BL.competing_set(k), BL.competing_set(k + 1)
    map_spec = cell["map_spec"]
    counts: dict[str, int] = {}
    min_point_sum = 0.0

    def bump(label: str) -> None:
        counts[label] = counts.get(label, 0) + 1

    for _ in range(reps):
        golds = [gen_gold(rng, cell, map_spec) for _ in range(k + 1)]
        st = [BL.gold_stats(g, names) for g in golds]
        c1, _ = BL.pool_stats(st[:k], K1)
        c2, _ = BL.pool_stats(st, K2)
        min_point_sum += min(x.delta for x in c1)
        for d in SPEC["deltas"]:
            for c in SPEC["c_grid"]:
                r1 = BL.n3_reading(c1, c=c, delta=d).outcome
                out = two_look(r1, lambda: BL.n3_reading(c2, c=c, delta=d).outcome)
                bump(f"gate|d={d}|c={c}|{out}")
                if c == 1.85:
                    bump(f"look1|d={d}|c={c}|{r1}")
            bump(f"ms3|d={d}|{BL.ms3_screen(c1, delta=d)}")
            bump(f"ms5|d={d}|{BL.ms5_reading(c1, delta=d)}")
        if cell.get("sensitivities"):
            if cell["icc"] > 0:
                sd = [BL.gold_stats(g, names, clustered=False) for g in golds]
                d1, _ = BL.pool_stats(sd[:k], K1)
                d2, _ = BL.pool_stats(sd, K2)
                out = two_look(BL.n3_reading(d1, c=1.85, delta=0.10).outcome,
                               lambda: BL.n3_reading(d2, c=1.85, delta=0.10).outcome)
                bump(f"unclustered|d=0.1|c=1.85|{out}")
            if k >= 2:
                out = two_look(re_reading(st[:k], K1, 1.85, 0.10), lambda: re_reading(st, K2, 1.85, 0.10))
                bump(f"random_effects|d=0.1|c=1.85|{out}")
    res = {kk: v for kk, v in cell.items() if kk not in ("base_mu",)}
    res["map_spec"] = list(map_spec)
    res["freq"] = {kk: round(v / reps, 4) for kk, v in sorted(counts.items())}
    res["mean_min_point_minus_true_gain"] = round(min_point_sum / reps - cell.get("true_min_gain", 0.0), 4)
    return res


# --- cells ---------------------------------------------------------------------------------------

def base_mu(spread: str) -> list[float]:
    a = SPEC["baseline_auroc"]
    other = a["close"] if spread == "close" else a["weak"]
    return [mu_of(a["strongest"])] + [mu_of(other)] * (len(BASE) - 1)


def make_cell(*, k, n, share, icc, ties, r, gain=None, kind="binormal", spread="close", reps, sens=False):
    n1 = max(1, min(n - 1, round(share * n)))
    cell = {"k": k, "n": n, "share": share, "n1": n1, "icc": icc, "ties": ties, "r": r, "spread": spread,
            "kind": kind, "gain": gain, "reps": reps, "base_mu": base_mu(spread),
            "pooled_minority": k * min(n1, n - n1), "sensitivities": sens}
    strongest = SPEC["baseline_auroc"]["strongest"]
    if kind == "binormal":
        cal = calibrate(strongest + gain, ties, n1 / n)
        if cal is None:
            return None
        cell["map_spec"] = ("binormal", cal[0], cal[1])
        cell["true_min_gain"] = gain
    else:
        cell["map_spec"] = (kind,)
        cell["true_min_gain"] = {"perfect": 1 - strongest, "random": 0.5 - strongest}.get(kind, float("nan"))
    return cell


def main_cells(reps: int) -> tuple[list[dict], list[dict]]:
    g = SPEC["grid"]
    cells, infeasible = [], []
    for k, n, share, icc, ties, r, gain in itertools.product(g["golds"], g["areas"], g["missed_share"], g["icc"],
                                                           g["ties"], g["r"], g["gain"]):
        cell = make_cell(k=k, n=n, share=share, icc=icc, ties=ties, r=r, gain=gain, reps=reps,
                         sens=(ties == 0 and r == 0.6))
        if cell is None:
            infeasible.append({"k": k, "n": n, "share": share, "icc": icc, "ties": ties, "r": r, "gain": gain})
        else:
            cells.append(cell)
    return cells, infeasible


def l73_cells(reps: int) -> list[dict]:
    g = SPEC["grid"]
    out = []
    for icc in (0.0, 0.3):
        out.append({**make_cell(k=3, n=20, share=0.8, icc=icc, ties=0.0, r=0.6, kind="perfect", reps=reps),
                    "role": "best_reachable"})
    for k, n, share, icc in itertools.product(g["golds"], g["areas"], g["missed_share"], g["icc"]):
        for kind in ("random", "size_noise"):
            out.append({**make_cell(k=k, n=n, share=share, icc=icc, ties=0.0, r=0.6, kind=kind, reps=reps),
                        "role": f"stand_in_{kind}"})
        out.append({**make_cell(k=k, n=n, share=share, icc=icc, ties=0.0, r=0.6, gain=0.0, spread="one_strong",
                                reps=reps), "role": "null_one_strong"})
    for n, icc, gain in itertools.product((20, 30, 40, 60, 80, 100, 120, 160, 200, 250), (0.0, 0.3), (0.0, 0.20)):
        out.append({**make_cell(k=3, n=n, share=0.8, icc=icc, ties=0.0, r=0.6, gain=gain, reps=reps),
                    "role": "min_areas"})
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=1000)
    ap.add_argument("--time", action="store_true")
    ap.add_argument("--procs", type=int, default=11)
    args = ap.parse_args()
    if args.time:
        for k in (1, 3, 6):
            cell = make_cell(k=k, n=20, share=0.8, icc=0.3, ties=0.3, r=0.6, gain=0.2, reps=20, sens=True)
            t = time.time()
            run_cell(cell)
            print(f"k={k}: {(time.time() - t) / 20 * 1000:.1f} ms/rep")
        return
    cells, infeasible = main_cells(args.reps)
    extra = l73_cells(args.reps)
    t0 = time.time()
    with Pool(args.procs) as pool:
        results = pool.map(run_cell, cells + extra, chunksize=1)
    main_res, extra_res = results[:len(cells)], results[len(cells):]
    hashes = {f: hashlib.sha256((Path(AU.__file__).parent / f).read_bytes()).hexdigest()
              for f in ("auroc.py", "baselines.py")}
    hashes["simulate.py"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    meta = {"label": LABEL, "spec": SPEC, "spec_sha256": hashlib.sha256(json.dumps(SPEC, sort_keys=True).encode()).hexdigest(),
            "code_sha256": hashes, "reps": args.reps, "python": sys.version.split()[0],
            "seconds": round(time.time() - t0), "infeasible_cells": infeasible}
    (HERE / "grid.json").write_text(json.dumps(meta, indent=1) + "\n")
    for name, res in (("cells.json.gz", main_res), ("l73_cells.json.gz", extra_res)):
        (HERE / name).write_bytes(gzip.compress((json.dumps({"label": LABEL, "cells": res}) + "\n").encode(), mtime=0))
    print(f"{len(cells)} + {len(extra)} cells in {meta['seconds']} s; {len(infeasible)} infeasible")


if __name__ == "__main__":
    main()
