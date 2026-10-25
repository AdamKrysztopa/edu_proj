"""SYNTHETIC key cells beside the grid (I5 steps 2, 4 and 5).

    uv run --directory residual python ../research/gate_sim/keycells.py [--reps N] [--boot B]

1. Bootstrap: on five key cells, the gate read with the analytic clustered-DeLong bounds (the
   grid's method), with cluster-bootstrap percentile bounds, and the two reported-only rules,
   the bootstrap minimum and max-T (DS3 §4, §9.5). Both looks, c = 1.85, δ = 0.10.
2. Near-oracle: whether "gold items per area" in K makes Continue unreachable for a map that is
   truly informative (coverage-audit finding 20, DS3 §7), against a pre-gold size proxy.
Writes bootstrap.json and near_oracle.json. SYNTHETIC; never a criterion, never feeds a gate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import time
from multiprocessing import Pool
from pathlib import Path

import simulate as S

from residual import auroc as AU
from residual import baselines as BL
from residual.auroc import GoldData

HERE = Path(__file__).resolve().parent
C, DELTA = 1.85, 0.10

KEY = [
    {"name": "planted_gain_0.20_16/4_icc0.3", "k": 3, "n": 20, "share": 0.8, "icc": 0.3, "gain": 0.20},
    {"name": "gain_delta_16/4_icc0.3", "k": 3, "n": 20, "share": 0.8, "icc": 0.3, "gain": 0.10},
    {"name": "null_16/4_icc0.3", "k": 3, "n": 20, "share": 0.8, "icc": 0.3, "gain": 0.0},
    {"name": "gain_delta_balanced_icc0", "k": 3, "n": 20, "share": 0.5, "icc": 0.0, "gain": 0.10},
    {"name": "planted_gain_0.20_16/4_x5golds_icc0", "k": 5, "n": 20, "share": 0.8, "icc": 0.0, "gain": 0.20},
    {"name": "gain_delta_16/4_x5golds_icc0", "k": 5, "n": 20, "share": 0.8, "icc": 0.0, "gain": 0.10},
]


def boot_cell(spec: dict) -> dict:
    cell = S.make_cell(k=spec["k"], n=spec["n"], share=spec["share"], icc=spec["icc"], ties=0.0, r=0.6,
                       gain=spec["gain"], reps=spec["reps"])
    rng = random.Random(f"{S.SEED}:boot:{spec['name']}")
    k = cell["k"]
    names = ["map", *S.BASE]
    K = {1: BL.competing_set(k), 2: BL.competing_set(k + 1)}
    counts: dict[str, int] = {}
    agree = 0
    for _ in range(cell["reps"]):
        golds = [S.gen_gold(rng, cell, cell["map_spec"]) for _ in range(k + 1)]
        st = [BL.gold_stats(g, names) for g in golds]
        readings = {}
        for look, gs, ss in ((1, golds[:k], st[:k]), (2, golds, st)):
            comps, _ = BL.pool_stats(ss, K[look])
            draws = AU.bootstrap_pooled_deltas(gs, "map", K[look], B=spec["boot"], rng=rng)
            readings[look] = {
                "analytic": BL.n3_reading(comps, c=C, delta=DELTA).outcome,
                "bootstrap": BL.bootstrap_reading(comps, draws, c=C, delta=DELTA),
                "bootstrap_min": BL.bootstrap_min_reading(comps, draws, c=C, delta=DELTA),
                "max_t": BL.max_t_reading(comps, draws, c=C, delta=DELTA),
            }
            a, b = readings[look]["analytic"], readings[look]["bootstrap"]
            readings[look]["agreement_rule"] = a if a == b else "inconclusive"
        final = {}
        for m in readings[1]:
            r1 = readings[1][m]
            final[m] = r1 if r1 != "inconclusive" else readings[2][m]
            counts[f"{m}|{final[m]}"] = counts.get(f"{m}|{final[m]}", 0) + 1
        agree += final["analytic"] == final["bootstrap"]
    reps = cell["reps"]
    return {"cell": spec, "pooled_minority": cell["pooled_minority"],
            "freq": {kk: round(v / reps, 4) for kk, v in sorted(counts.items())},
            "analytic_bootstrap_agreement": round(agree / reps, 4)}


# --- stand-in: a map that is only the rank average of the baselines --------------------------------

def mean_of_k_cell(spec: dict) -> dict:
    """methods-critic finding 7: the gate compares the map with each baseline singly, so a map that
    merely averages weakly correlated baselines can beat each of them."""
    cell = S.make_cell(k=spec["k"], n=spec["n"], share=spec["share"], icc=spec["icc"], ties=0.0, r=spec["r"],
                       kind="random", reps=spec["reps"])
    rng = random.Random(f"{S.SEED}:meanK:{json.dumps(spec, sort_keys=True)}")
    k = cell["k"]
    names = ["map", *S.BASE]
    K = {1: BL.competing_set(k), 2: BL.competing_set(k + 1)}
    counts: dict[str, int] = {}
    auc_map = auc_strong = 0.0
    for _ in range(cell["reps"]):
        golds = []
        for _ in range(k + 1):
            g = S.gen_gold(rng, cell, cell["map_spec"])
            ranks = [AU.midranks(g.scores[b]) for b in S.BASE]
            g.scores["map"] = [sum(r[i] for r in ranks) / len(ranks) for i in range(len(g.labels))]
            golds.append(g)
        auc_map += sum(AU.auroc(g.scores["map"], g.labels) for g in golds[:k]) / k
        auc_strong += sum(AU.auroc(g.scores["area_size"], g.labels) for g in golds[:k]) / k
        st = [BL.gold_stats(g, names) for g in golds]
        r1 = BL.n3_reading(BL.pool_stats(st[:k], K[1])[0], c=C, delta=DELTA).outcome
        out = r1 if r1 != "inconclusive" else BL.n3_reading(BL.pool_stats(st, K[2])[0], c=C, delta=DELTA).outcome
        counts[out] = counts.get(out, 0) + 1
    reps = cell["reps"]
    return {"cell": spec, "mean_auroc_map": round(auc_map / reps, 3), "mean_auroc_area_size": round(auc_strong / reps, 3),
            "freq": {kk: round(v / reps, 4) for kk, v in sorted(counts.items())}}


def null_one_strong_cells(reps: int) -> list[dict]:
    """methods-critic finding 11: the least-favourable null at r = 0.3 and 0.9 as well as 0.6."""
    g = S.SPEC["grid"]
    return [{**S.make_cell(k=k, n=n, share=share, icc=icc, ties=0.0, r=r, gain=0.0, spread="one_strong", reps=reps),
             "role": "null_one_strong"}
            for k in g["golds"] for n in g["areas"] for share in g["missed_share"] for icc in g["icc"] for r in (0.3, 0.9)]


# --- near-oracle ---------------------------------------------------------------------------------

def poisson(rng: random.Random, lam: float) -> int:
    limit, k, p = math.exp(-lam), 0, 1.0
    while True:
        p *= rng.random()
        if p <= limit:
            return k
        k += 1


def oracle_gold(rng: random.Random, n: int, p_item: float, map_kind, r: float, proxy_sd: float) -> GoldData:
    while True:
        items = [1 + poisson(rng, 1.3) for _ in range(n)]
        y = [any(rng.random() < p_item for _ in range(m)) for m in items]
        if 0 < sum(y) < n:
            break
    z0 = [rng.gauss(0, 1) for _ in range(n)]
    sr, sq = math.sqrt(r), math.sqrt(1 - r)

    def noise():
        return [sr * z0[i] + sq * rng.gauss(0, 1) for i in range(n)]

    scores = {}
    for name, mu in zip(S.BASE, S.base_mu("close")):
        e = noise()
        scores[name] = [mu * y[i] + e[i] for i in range(n)]
    if map_kind == "perfect":
        scores["map"] = [float(v) for v in y]
    else:
        e = noise()
        mu = S.mu_of(map_kind)
        scores["map"] = [mu * y[i] + e[i] for i in range(n)]
    scores["gold_items_per_area"] = [float(m) for m in items]
    scores["pre_gold_size_proxy"] = [m + rng.gauss(0, proxy_sd) for m in items]
    return GoldData(labels=y, clusters=list(range(n)), scores=scores)


def oracle_cell(spec: dict) -> dict:
    rng = random.Random(f"{S.SEED}:oracle:{json.dumps(spec, sort_keys=True)}")
    k, n = spec["k"], spec["n"]
    names = ["map", *S.BASE, "gold_items_per_area", "pre_gold_size_proxy"]
    counts: dict[str, int] = {}
    auc_items = auc_proxy = auc_map = 0.0
    share = 0.0
    sets = {
        "K": lambda kk: list(BL.competing_set(kk)),
        "K+gold_items": lambda kk: [*BL.competing_set(kk), "gold_items_per_area"],
        "K+pre_gold_proxy": lambda kk: [*BL.competing_set(kk), "pre_gold_size_proxy"],
    }
    for _ in range(spec["reps"]):
        golds = [oracle_gold(rng, n, spec["p_item"], spec["map"], 0.6, spec["proxy_sd"]) for _ in range(k + 1)]
        st = [BL.gold_stats(g, names) for g in golds]
        for g in golds[:k]:
            auc_items += AU.auroc(g.scores["gold_items_per_area"], g.labels) / k
            auc_proxy += AU.auroc(g.scores["pre_gold_size_proxy"], g.labels) / k
            auc_map += AU.auroc(g.scores["map"], g.labels) / k
            share += sum(g.labels) / n / k
        for label, ks in sets.items():
            c1, _ = BL.pool_stats(st[:k], ks(k))
            r1 = BL.n3_reading(c1, c=C, delta=DELTA).outcome
            if r1 == "inconclusive":
                c2, _ = BL.pool_stats(st, ks(k + 1))
                r1 = BL.n3_reading(c2, c=C, delta=DELTA).outcome
            counts[f"{label}|{r1}"] = counts.get(f"{label}|{r1}", 0) + 1
    reps = spec["reps"]
    return {"cell": spec, "mean_missed_share": round(share / reps, 3),
            "mean_auroc": {"map": round(auc_map / reps, 3), "gold_items_per_area": round(auc_items / reps, 3),
                           "pre_gold_size_proxy": round(auc_proxy / reps, 3)},
            "freq": {kk: round(v / reps, 4) for kk, v in sorted(counts.items())}}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=300)
    ap.add_argument("--boot", type=int, default=2000)
    ap.add_argument("--oracle-reps", type=int, default=1000)
    ap.add_argument("--procs", type=int, default=11)
    args = ap.parse_args()
    t0 = time.time()
    boot_specs = [{**s, "reps": args.reps, "boot": args.boot} for s in KEY]
    oracle_specs = [{"k": k, "n": n, "p_item": 0.56, "map": m, "proxy_sd": 1.52, "reps": args.oracle_reps}
                    for k in (3, 5) for n in (20, 30) for m in (0.72, 0.82, 0.92, "perfect")]
    meank_specs = [{"k": k, "n": n, "share": share, "icc": 0.0, "r": r, "reps": args.oracle_reps}
                   for k, n, share in ((3, 20, 0.8), (5, 20, 0.8), (3, 20, 0.5), (5, 30, 0.8)) for r in (0.0, 0.3, 0.6)]
    with Pool(args.procs) as pool:
        boot = pool.map(boot_cell, boot_specs, chunksize=1)
        oracle = pool.map(oracle_cell, oracle_specs, chunksize=1)
        meank = pool.map(mean_of_k_cell, meank_specs, chunksize=1)
        nulls = pool.map(S.run_cell, null_one_strong_cells(args.oracle_reps), chunksize=1)
    code = {f: hashlib.sha256(p.read_bytes()).hexdigest()
            for f, p in (("keycells.py", Path(__file__)), ("simulate.py", Path(S.__file__)),
                         ("auroc.py", Path(AU.__file__)), ("baselines.py", Path(BL.__file__)))}
    meta = {"label": S.LABEL, "c": C, "delta": DELTA, "code_sha256": code, "seconds": round(time.time() - t0)}
    (HERE / "bootstrap.json").write_text(json.dumps({**meta, "boot": args.boot, "cells": boot}, indent=1) + "\n")
    (HERE / "stand_in_mean_of_k.json").write_text(json.dumps({**meta, "cells": meank}, indent=1) + "\n")
    (HERE / "null_one_strong_r.json").write_text(json.dumps(
        {**meta, "cells": [{kk: v for kk, v in c.items() if kk == "freq" or not isinstance(v, dict)} for c in nulls]})
        + "\n")
    (HERE / "near_oracle.json").write_text(json.dumps(
        {**meta, "model": "items per area 1 + Poisson(1.3); an area is missed if any item is missed, "
                          "per-item miss rate p_item; pre-gold proxy = items + N(0, proxy_sd), corr about 0.6",
         "cells": oracle}, indent=1) + "\n")
    print(f"done in {meta['seconds']} s")


if __name__ == "__main__":
    main()
