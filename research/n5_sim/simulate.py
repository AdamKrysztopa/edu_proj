"""SYNTHETIC known-truth simulation for N5 (REORIENTATION.md §14.1, §12 use 1, §16 R4).

    uv run --directory residual python ../research/n5_sim/simulate.py

Two grids share one generator: the I3 default grid (cells.json) and the DS4 §7 grid
(ds4_cells.json.gz, research/ds4-identifiability.md at b4c9abf). Also writes grid.json,
selfcheck.json, counterexample.json and tables.md. Every output is SYNTHETIC: it debugs the
estimators and never feeds a gate.
"""
from __future__ import annotations

import gzip
import hashlib
import itertools
import json
import math
import random
import statistics
import sys
from functools import lru_cache, partial
from multiprocessing import Pool
from pathlib import Path
from statistics import NormalDist

from residual.estimators import NotEstimable, chao1, chapman, frequency_counts, jackknife1, mh_coverage

HERE = Path(__file__).resolve().parent
LABEL = "SYNTHETIC — not evidence about learners or experts"

COMMON = {"label": LABEL, "z": 1.96, "tau": [0.10, 0.25, 0.50], "achievable_pass_rate": 0.80,
          "replicates": 500, "seed": 20261024}
DEFAULT = {
    "source": "default grid of docs/plans/prompts/I3-residual-identifiability.md",
    "N": [50, 200], "never_written_share": [0.0, 0.2, 0.5], "k_text_occasions": [2, 3, 5],
    "heterogeneity_beta": {"low": [15.0, 35.0], "high": [1.65, 3.85], "extreme": [0.45, 1.05]},
    "rho": [0.0, 0.3, 0.6], "gold_p": [1.0, 0.6],
    "model": ("p_i ~ Beta(a, b), mean 0.3; CV 0.21 low, 0.60 high, 0.97 extreme (a < 1: infinite "
              "density at p = 0, a sensitivity case). With probability rho an item's k text captures "
              "copy one shared Bernoulli(p_i) draw, else they are independent, so the within-item "
              "correlation is rho. Never-written items: catchability 0 on every text occasion. Gold "
              "catches every item independently with probability gold_p; matching is exact."),
}
DS4 = {
    "source": "research/ds4-identifiability.md §7 (commit b4c9abf)",
    "N": [50, 200], "never_written_share": [0.0, 0.2, 0.5], "k_text_occasions": [2, 3, 5],
    "mean_p": [0.15, 0.4], "logit_sigma": [0.5, 1.5], "family": ["logit_normal", "two_class"],
    "rho": [0.0, 0.3, 0.6], "g_W": [0.6, 0.9], "g_Z_over_g_W": [0.5, 1.0, 1.5],
    "false_non_match": [0.0, 0.1], "two_class_high_weight": 0.25,
    "model": ("logit p_i ~ Normal(mu, sigma) with mu set so E[p] = mean_p; two_class matches that mean "
              "and SD with weight 0.25 on the high class. Text captures X_ij = 1{sqrt(rho) W_i + "
              "sqrt(1-rho) E_ij < Phi^-1(p_i)}: a Gaussian copula, exchangeable across text occasions, "
              "conditional on p_i. Gold catches written items with g_W and never-written with "
              "min(1, ratio * g_W). A gold item that text caught fails to match with probability "
              "false_non_match and is then counted as gold-uncaught; the corpus-presence audit "
              "(DS4 §3.3) is exact. Text, gold and match/noise use separate random streams."),
}
SPEC = {"common": COMMON, "default": DEFAULT, "ds4": DS4}
SPEC_SHA256 = hashlib.sha256(json.dumps(SPEC, sort_keys=True).encode()).hexdigest()
TAUS = COMMON["tau"]
TEXT = {"chao1": chao1, "jackknife": jackknife1, "mh": mh_coverage,
        "chao1_large_t": partial(chao1, small_t=False), "mh_lee_chao": partial(mh_coverage, coverage="lee_chao")}
"""chao1 and mh are the small-t forms; the large-t forms show what the correction buys."""
STANDINS = ("zero", "singletons", "noise", "oracle_written", "oracle_total")
"""Trivial stand-ins the tolerance rule must not pass (zero, singletons, noise), and two ceilings:
the written-universe truth, the most a text estimator can identify, and the full truth."""
FORMS = ("s22", "lp", "w_true", "w_obs")
"""The comparison target: s22 = raw gold-uncaught count (the I3 prompt and REORIENTATION §22 as
written); lp = Lincoln-Petersen unseen count; w_true = unseen written items (simulation truth);
w_obs = Lincoln-Petersen unseen count on the gold items the corpus audit finds written."""
N01 = NormalDist()


def _logit_normal_moments(mu: float, sigma: float) -> tuple[float, float]:
    zs = [-8 + 16 * i / 4000 for i in range(4001)]
    w = [math.exp(-z * z / 2) for z in zs]
    p = [1 / (1 + math.exp(-(mu + sigma * z))) for z in zs]
    tot = sum(w)
    m = sum(wi * pi for wi, pi in zip(w, p)) / tot
    return m, sum(wi * (pi - m) ** 2 for wi, pi in zip(w, p)) / tot


@lru_cache(maxsize=None)
def calibrate(mean_p: float, sigma: float) -> dict:
    lo, hi = -15.0, 15.0
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if _logit_normal_moments(mid, sigma)[0] < mean_p else (lo, mid)
    mu = (lo + hi) / 2
    m, var = _logit_normal_moments(mu, sigma)
    sd, pi = math.sqrt(var), DS4["two_class_high_weight"]
    p_hi, p_lo = m + sd * math.sqrt((1 - pi) / pi), m - sd * math.sqrt(pi / (1 - pi))
    assert 0 < p_lo < p_hi < 1, (mean_p, sigma, p_lo, p_hi)
    return {"mu": mu, "mean": m, "cv": sd / m, "p_lo": p_lo, "p_hi": p_hi, "weight_hi": pi}


def sampler(cell: dict):
    if cell["grid"] == "default":
        a, b = DEFAULT["heterogeneity_beta"][cell["het"]]
        return lambda rng: rng.betavariate(a, b)
    c = calibrate(cell["mean_p"], cell["sigma"])
    if cell["family"] == "logit_normal":
        return lambda rng: 1 / (1 + math.exp(-(c["mu"] + cell["sigma"] * rng.gauss(0, 1))))
    return lambda rng: c["p_hi"] if rng.random() < c["weight_hi"] else c["p_lo"]


def text_history(rng: random.Random, p: float, k: int, rho: float, copula: bool) -> list[bool]:
    if copula:
        thr = N01.inv_cdf(min(max(p, 1e-12), 1 - 1e-12))
        w, a, b = rng.gauss(0, 1), math.sqrt(rho), math.sqrt(1 - rho)
        return [a * w + b * rng.gauss(0, 1) < thr for _ in range(k)]
    if rng.random() < rho:
        return [rng.random() < p] * k
    return [rng.random() < p for _ in range(k)]


def replicate(streams, cell, draw_p, z):
    rt, rg, rn = streams
    n, k, rho = cell["N"], cell["k"], cell["rho"]
    n_never = round(n * cell["share"])
    nw = n - n_never
    copula = cell["grid"] == "ds4"
    text = [text_history(rt, draw_p(rt), k, rho, copula) for _ in range(nw)] + [[False] * k] * n_never
    g_z = min(1.0, cell["g_W"] * cell["g_ratio"])
    gold = [rg.random() < (cell["g_W"] if i < nw else g_z) for i in range(n)]
    caught = [any(h) for h in text]
    matched = [g and c and not (rn.random() < cell["fnm"]) for g, c in zip(gold, caught)]
    s, m = sum(caught), sum(matched)
    n_gold, n_gold_w = sum(gold), sum(gold[:nw])
    truth = {"U": n - s, "U_w": nw - s, "Z": n_never, "G": n_gold - m, "G_w": n_gold_w - m}
    lp, lp_w = chapman(s, n_gold, m, z), chapman(s, n_gold_w, m, z)
    refs = {"s22": truth["G"], "lp": lp.unseen, "w_true": truth["U_w"], "w_obs": lp_w.unseen}
    f = frequency_counts(text) if s else None
    if f and n_never:
        assert frequency_counts(text[:nw]) == f
    out = {}
    for name, est in TEXT.items():
        try:
            e = est(f, z)
            out[name] = (e.unseen, e.interval)
        except (NotEstimable, TypeError):
            out[name] = None
    out["zero"] = (0.0, None)
    out["singletons"] = (float(f[0]) if f else 0.0, None)
    out["noise"] = (rn.uniform(0, s), None)
    out["oracle_written"] = (float(truth["U_w"]), None)
    out["oracle_total"] = (float(truth["U"]), None)
    return truth, refs, (lp.unseen, lp.interval, lp_w.unseen), out


def run_cell(cell: dict) -> dict:
    tag = f"{COMMON['seed']}:{cell['grid']}:{cell['key']}"
    streams = tuple(random.Random(f"{tag}:{s}") for s in ("text", "gold", "aux"))
    draw_p = sampler(cell)
    reps = [replicate(streams, cell, draw_p, COMMON["z"]) for _ in range(COMMON["replicates"])]
    R = len(reps)
    mean = lambda xs: round(statistics.fmean(xs), 4) if xs else None
    rate = lambda n: round(n / R, 4)
    truth = {q: mean([t[q] for t, _, _, _ in reps]) for q in ("U", "U_w", "Z", "G", "G_w")}
    lp = {"rel_bias_U": round(statistics.fmean(l[0] - t["U"] for t, _, l, _ in reps) / truth["U"], 4)
          if truth["U"] else None,
          "coverage_U": rate(sum(l[1][0] <= t["U"] <= l[1][1] for t, _, l, _ in reps)),
          "wonly_unseen_mean": mean([l[2] for _, _, l, _ in reps]),
          "unseen_mean": mean([l[0] for _, _, l, _ in reps])}
    residual = {}
    for name in ("chao1", "mh"):
        ok = [(t, l, o[name]) for t, _, l, o in reps if o[name] is not None]
        residual[name] = {"bias_vs_Z": mean([l[0] - v[0] - t["Z"] for t, l, v in ok])}
    est = {}
    for name in (*TEXT, *STANDINS):
        ok = [(t, r, o[name]) for t, r, _, o in reps if o[name] is not None]
        row = {"fail": rate(R - len(ok)),
               "rel_bias_U_w": round(statistics.fmean(v[0] - t["U_w"] for t, _, v in ok) / truth["U_w"], 4)
               if ok and truth["U_w"] else None,
               "rel_bias_U": round(statistics.fmean(v[0] - t["U"] for t, _, v in ok) / truth["U"], 4)
               if ok and truth["U"] else None,
               "bound_holds": rate(sum(v[0] <= t["U_w"] for t, _, v in ok))}
        if ok and ok[0][2][1] is not None:
            row["cov_U_w"] = rate(sum(v[1][0] <= t["U_w"] <= v[1][1] for t, _, v in ok))
            row["cov_U"] = rate(sum(v[1][0] <= t["U"] <= v[1][1] for t, _, v in ok))
        row["pass"] = {form: [rate(sum(abs(v[0] - r[form]) <= tau * r[form] for _, r, v in ok)) for tau in TAUS]
                       for form in FORMS}
        est[name] = row
    return {**cell, "truth": truth, "lp": lp, "residual": residual, "est": est}


def default_cells() -> list[dict]:
    return [{"grid": "default", "key": f"N{n}_nw{sh}_k{k}_{het}_rho{rho}_g{gp}", "N": n, "share": sh, "k": k,
             "het": het, "rho": rho, "g_W": gp, "g_ratio": 1.0, "fnm": 0.0}
            for n, sh, k, het, rho, gp in itertools.product(
                DEFAULT["N"], DEFAULT["never_written_share"], DEFAULT["k_text_occasions"],
                DEFAULT["heterogeneity_beta"], DEFAULT["rho"], DEFAULT["gold_p"])]


def ds4_cells() -> list[dict]:
    return [{"grid": "ds4", "key": f"N{n}_nw{sh}_k{k}_p{mp}_s{sg}_{fam}_rho{rho}_gW{gw}_r{gr}_f{fn}",
             "N": n, "share": sh, "k": k, "mean_p": mp, "sigma": sg, "family": fam, "rho": rho,
             "g_W": gw, "g_ratio": gr, "fnm": fn}
            for n, sh, k, mp, sg, fam, rho, gw, gr, fn in itertools.product(
                DS4["N"], DS4["never_written_share"], DS4["k_text_occasions"], DS4["mean_p"],
                DS4["logit_sigma"], DS4["family"], DS4["rho"], DS4["g_W"], DS4["g_Z_over_g_W"],
                DS4["false_non_match"])]


def selfcheck() -> dict:
    """Planted checks on the generator, run before any cell."""
    rng = random.Random(f"{COMMON['seed']}:selfcheck")
    report = {}
    for het, (a, b) in DEFAULT["heterogeneity_beta"].items():
        mu, var_p = a / (a + b), a * b / ((a + b) ** 2 * (a + b + 1))
        for rho in DEFAULT["rho"]:
            x, y = zip(*(text_history(rng, rng.betavariate(a, b), 2, rho, False) for _ in range(20000)))
            corr = statistics.correlation([float(v) for v in x], [float(v) for v in y])
            expected = rho + (1 - rho) * var_p / (mu * (1 - mu))
            assert abs(statistics.fmean(x) - mu) < 0.02 and abs(corr - expected) < 0.04, (het, rho, corr)
            report[f"default_{het}_rho{rho}"] = {"p_hat": round(statistics.fmean(x), 4), "corr": round(corr, 4),
                                                 "expected_corr": round(expected, 4)}
    for mp, sg in itertools.product(DS4["mean_p"], DS4["logit_sigma"]):
        c = calibrate(mp, sg)
        assert abs(c["mean"] - mp) < 1e-6
        for fam in DS4["family"]:
            draw_p = sampler({"grid": "ds4", "mean_p": mp, "sigma": sg, "family": fam})
            ps = [draw_p(rng) for _ in range(40000)]
            assert abs(statistics.fmean(ps) - mp) < 0.01 and abs(statistics.stdev(ps) / mp - c["cv"]) < 0.05
            corrs = []
            for rho in DS4["rho"]:
                x, y = zip(*(text_history(rng, p, 2, rho, True) for p in ps[:20000]))
                corrs.append(round(statistics.correlation([float(v) for v in x], [float(v) for v in y]), 4))
                assert abs(statistics.fmean(x) - mp) < 0.015
            assert corrs[0] < corrs[1] < corrs[2]
            report[f"ds4_p{mp}_s{sg}_{fam}"] = {"cv": round(c["cv"], 3), "p_lo": round(c["p_lo"], 4),
                                                "p_hi": round(c["p_hi"], 4), "pooled_corr_by_rho": corrs}
    return report


def counterexample() -> dict:
    """Universes with identical observed text histories and different never-written counts."""
    rng = random.Random(f"{COMMON['seed']}:counterexample")
    written = [text_history(rng, rng.betavariate(15.0, 35.0), 3, 0.0, False) for _ in range(100)]
    observed = [h for h in written if any(h)]
    out = {"label": LABEL, "n_written": 100, "k": 3, "heterogeneity": "low", "rho": 0.0,
           "observed_histories": len(observed), "frequency_counts": frequency_counts(observed), "universes": []}
    for never in (0, 100, 400):
        text = written + [[False] * 3] * never
        f = frequency_counts(text)
        assert f == out["frequency_counts"]
        g_rng = random.Random(f"{COMMON['seed']}:counterexample-gold:{never}")
        row = {"never_written": never, "N": 100 + never, "true_unseen_U": len(text) - len(observed),
               "true_written_unseen_U_w": 100 - len(observed), "text_estimators": {}, "gold": {}}
        for name, est in TEXT.items():
            try:
                e = est(f)
            except NotEstimable:
                continue
            row["text_estimators"][name] = {"unseen": round(e.unseen, 2), "interval": [round(v, 2) for v in e.interval]}
        for gp in (1.0, 0.6):
            gold = [g_rng.random() < gp for _ in text]
            caught = [any(h) for h in text]
            m = sum(g and c for g, c in zip(gold, caught))
            lp = chapman(len(observed), sum(gold), m)
            row["gold"][str(gp)] = {"gold_uncaught_G": sum(g and not c for g, c in zip(gold, caught)),
                                    "lincoln_petersen_unseen": round(lp.unseen, 2),
                                    "interval": [round(v, 2) for v in lp.interval]}
        out["universes"].append(row)
    return out


def _achieved(r, form, tau_i, names=("chao1", "jackknife", "mh")):
    return max((r["est"][e]["pass"][form][tau_i], e) for e in names)


def tables(default: list[dict], ds4: list[dict]) -> str:
    A = COMMON["achievable_pass_rate"]
    L = [f"# N5 simulation tables ({LABEL})", "", f"Spec sha256 `{SPEC_SHA256}`.", "",
         "Pass = share of replicates with |f0 − ref| ≤ τ·ref; failures count as misses. Achievable = pass ≥ 0.80 "
         "(our choice). Forms: s22 = raw gold-uncaught (as written); lp = Lincoln–Petersen unseen; w_true = unseen "
         "written items (truth); w_obs = Lincoln–Petersen on gold items the corpus audit finds written.", ""]
    for grid, rows, _, low in (("default", default, lambda r: r["het"], lambda r: r["het"] == "low"),
                                    ("ds4", ds4, None, lambda r: r["sigma"] == 0.5 and r["g_W"] == 0.9
                                     and r["g_ratio"] == 1.0 and r["fnm"] == 0.0)):
        L += [f"## {grid} grid: cells where some estimator (chao1, jackknife, mh) is achievable, by form and ρ",
              "", "| ρ | cells | " + " | ".join(f"{fm} τ={t}" for fm in FORMS for t in TAUS) + " |",
              "|" + "---|" * (2 + len(FORMS) * len(TAUS))]
        for rho in sorted({r["rho"] for r in rows}):
            sub = [r for r in rows if r["rho"] == rho]
            L.append(f"| {rho} | {len(sub)} | " + " | ".join(
                str(sum(_achieved(r, fm, i)[0] >= A for r in sub)) for fm in FORMS for i in range(len(TAUS))) + " |")
        L += ["", f"## {grid} grid: stop-condition readings at ρ = 0, low heterogeneity, τ = 0.5", "",
              "Best estimator pass and the singleton stand-in, per form (ds4: g_W 0.9, g_Z/g_W 1, no false non-matches).", "",
              "| cell | s22 best | s22 f1 | lp best | lp f1 | w_true best | w_true f1 | w_obs best | w_obs f1 |",
              "|---|---|---|---|---|---|---|---|---|"]
        for r in rows:
            if r["rho"] == 0 and low(r):
                cells_ = []
                for fm in FORMS:
                    b = _achieved(r, fm, 2)
                    cells_ += [f"{b[0]:.2f} {b[1]}", f"{r['est']['singletons']['pass'][fm][2]:.2f}"]
                L.append(f"| {r['key']} | " + " | ".join(cells_) + " |")
        L.append("")
    L += ["## default grid: small-t correction, rel. bias vs U_w, nw = 0, ρ = 0, gold p = 1", "",
          "| N | k | het | chao1 | chao1_large_t | mh | mh_lee_chao | jackknife |", "|" + "---|" * 8]
    for r in default:
        if r["g_W"] == 1.0 and r["share"] == 0 and r["rho"] == 0:
            L.append(f"| {r['N']} | {r['k']} | {r['het']} | " + " | ".join(
                f"{r['est'][e]['rel_bias_U_w']:+.2f}" for e in ("chao1", "chao1_large_t", "mh", "mh_lee_chao", "jackknife")) + " |")
    L += ["", "## ds4 grid: Lincoln–Petersen and residual (LP unseen − mh) bias by g_Z/g_W and false-non-match", "",
          "| g_Z/g_W | fnm | LP rel bias vs U (median) | LP coverage U (median) | residual bias vs |Z| (median, nw > 0) |",
          "|---|---|---|---|---|"]
    for gr, fn in itertools.product(DS4["g_Z_over_g_W"], DS4["false_non_match"]):
        sub = [r for r in ds4 if r["g_ratio"] == gr and r["fnm"] == fn]
        rb = statistics.median(r["lp"]["rel_bias_U"] for r in sub if r["lp"]["rel_bias_U"] is not None)
        cv = statistics.median(r["lp"]["coverage_U"] for r in sub)
        res = [r["residual"]["mh"]["bias_vs_Z"] / r["truth"]["Z"] for r in sub
               if r["truth"]["Z"] and r["residual"]["mh"]["bias_vs_Z"] is not None]
        L.append(f"| {gr} | {fn} | {rb:+.3f} | {cv:.2f} | {statistics.median(res):+.3f} |")
    return "\n".join(L) + "\n"


def dump_cells(name: str, meta: dict, rows: list[dict]) -> None:
    body = ",\n".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) for r in rows)
    head = json.dumps(meta, ensure_ascii=False)[:-1]
    text = f'{head}, "cells": [\n{body}\n]}}\n'.encode()
    if name.endswith(".gz"):
        (HERE / name).write_bytes(gzip.compress(text, mtime=0))
    else:
        (HERE / name).write_bytes(text)


def main() -> None:
    meta = {"label": LABEL, "spec_sha256": SPEC_SHA256,
            "generator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "estimators_sha256": hashlib.sha256(Path(sys.modules["residual.estimators"].__file__).read_bytes()).hexdigest(),
            "python": sys.version.split()[0]}
    write = lambda name, obj: (HERE / name).write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n")
    write("grid.json", {**meta, "spec": SPEC,
                        "ds4_calibration": {f"p{mp}_s{sg}": calibrate(mp, sg)
                                            for mp, sg in itertools.product(DS4["mean_p"], DS4["logit_sigma"])}})
    write("selfcheck.json", {**meta, "checks": selfcheck()})
    write("counterexample.json", {**meta, **counterexample()})
    with Pool() as pool:
        default = pool.map(run_cell, default_cells())
        ds4 = pool.map(run_cell, ds4_cells(), chunksize=8)
    dump_cells("cells.json", meta, default)
    dump_cells("ds4_cells.json.gz", meta, ds4)
    (HERE / "tables.md").write_text(tables(default, ds4))


if __name__ == "__main__":
    main()
