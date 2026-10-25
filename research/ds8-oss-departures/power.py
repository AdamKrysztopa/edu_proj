"""SYNTHETIC first power calculation for E-OSS (REORIENTATION.md §18, §22 threshold row
"E-OSS departures and minimum post-departure activity"; research/ds8-oss-departures.md §5).

    uv run --with numpy python research/ds8-oss-departures/power.py

Writes power.json next to this file. Every number it produces is SYNTHETIC: it sizes the
design and never feeds a gate.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
LABEL = "SYNTHETIC — planning simulation, not evidence about any project or developer"

SPEC = {
    "label": LABEL,
    "seed": 20261024,
    "replicates": 300,
    "delta": 0.10,
    "z_continue": 1.85,
    "z_stop": {"K1": 1.85, "K6": 2.55},
    "departures": [10, 15, 20, 30, 40, 60, 80, 120],
    "units_per_departure": [10, 20],
    "activity_floor": [2, 5, 10, 20],
    "temporal_size": [2.0, 10.0, None],
    "loss_prevalence_mean": 0.3,
    "loss_prevalence_beta_sum": 10.0,
    "loss_rate_ratio": 2.0,
    "label_ratio_threshold": 1.41421356,
    "latent_auroc_baseline": 0.62,
    "latent_gain_alternative": 0.20,
    "score_noise_correlation": 0.5,
    "model": (
        "Per departure d: m units the leaver owned at t (blame at t), loss prevalence "
        "pi_d ~ Beta(mean 0.3, a+b = 10), latent loss z_i ~ Bernoulli(pi_d). Pre-t expected "
        "outcome events per unit per window mu_i = floor * (1 + Exp(1)), so every unit meets the "
        "activity floor. Between-unit heterogeneity is persistent and cancels in the unit's own "
        "post/pre ratio, so only period-to-period noise is simulated: Y_pre ~ NB(mu_i, size_t), "
        "Y_post ~ NB(mu_i * RR^z_i, size_t), Poisson when size_t is None. The "
        "departure-level change in activity is assumed removed exactly by the control units of the "
        "difference-in-differences. Observed label L_i = 1 if (Y_post + 0.5) / (Y_pre + 0.5) > "
        "sqrt(2), the geometric midpoint of 1 and RR. Scores: baseline = a_b z + e_b, map = a_m z + "
        "e_m, corr(e_b, e_m) = 0.5, a = sqrt(2) * Phi^-1(latent AUROC). Null: map latent AUROC = "
        "baseline's (0.62). Alternative: map latent AUROC = 0.82. Statistic: pooled within-departure "
        "Mann-Whitney dAUROC = sum_d sum_pairs (psi_map - psi_base) / sum_d pairs, ties 1/2, with a "
        "departure-cluster ratio-estimator variance. Stop if dAUROC + z_stop * SE < delta; "
        "Continue if dAUROC - z_continue * SE > 0 and dAUROC >= delta; otherwise inconclusive."
    ),
}


def _phi_inv(p: float) -> float:
    from statistics import NormalDist
    return NormalDist().inv_cdf(p)


def _psi(pos: np.ndarray, neg: np.ndarray) -> float:
    diff = pos[:, None] - neg[None, :]
    return float((diff > 0).sum() + 0.5 * (diff == 0).sum())


def _nb(rng: np.random.Generator, mean: np.ndarray, size: float | None) -> np.ndarray:
    if size is None:
        return rng.poisson(mean)
    return rng.negative_binomial(size, size / (size + mean))


def simulate_departure(rng, m, floor, size, latent_map, latent_base, oracle=False, stand_in=False):
    a_m = np.sqrt(2) * _phi_inv(latent_map)
    a_b = np.sqrt(2) * _phi_inv(latent_base)
    mean_pi = SPEC["loss_prevalence_mean"]
    s = SPEC["loss_prevalence_beta_sum"]
    pi = rng.beta(mean_pi * s, (1 - mean_pi) * s)
    z = rng.random(m) < pi
    mu = floor * (1 + rng.exponential(1.0, m))
    y_pre = _nb(rng, mu, size)
    y_post = _nb(rng, mu * np.where(z, SPEC["loss_rate_ratio"], 1.0), size)
    label = (y_post + 0.5) / (y_pre + 0.5) > SPEC["label_ratio_threshold"]
    rho = SPEC["score_noise_correlation"]
    e_b = rng.standard_normal(m)
    e_m = rho * e_b + np.sqrt(1 - rho**2) * rng.standard_normal(m)
    base = a_b * z + e_b
    if oracle:
        score = z.astype(float) + 1e-9 * rng.standard_normal(m)
    elif stand_in:
        score = mu
    else:
        score = a_m * z + e_m
    pos, neg = label, ~label
    pairs = int(pos.sum() * neg.sum())
    if pairs == 0:
        return 0.0, 0, int(pos.sum()), z, label
    num = _psi(score[pos], score[neg]) - _psi(base[pos], base[neg])
    return num, pairs, int(pos.sum()), z, label


def run_cell(rng, D, m, floor, size, latent_map, latent_base, z_stop, **kw):
    stop = cont = 0
    deltas = []
    positives = []
    for _ in range(SPEC["replicates"]):
        nums, pairs, npos = np.empty(D), np.empty(D), 0
        for d in range(D):
            nums[d], pairs[d], p, _, _ = simulate_departure(rng, m, floor, size, latent_map, latent_base, **kw)
            npos += p
        total = pairs.sum()
        if total == 0:
            continue
        est = nums.sum() / total
        resid = nums - est * pairs
        se = np.sqrt(D / (D - 1) * (resid**2).sum()) / total
        deltas.append(est)
        positives.append(npos)
        if est + z_stop * se < SPEC["delta"]:
            stop += 1
        if est - SPEC["z_continue"] * se > 0 and est >= SPEC["delta"]:
            cont += 1
    n = SPEC["replicates"]
    return {"p_stop": round(stop / n, 3), "p_continue": round(cont / n, 3),
            "mean_delta": round(float(np.mean(deltas)), 4), "mean_positives": round(float(np.mean(positives)), 1)}


def label_reliability(rng, floor, size, n=200_000):
    mu = floor * (1 + rng.exponential(1.0, n))
    out = {}
    for name, rr in (("p_label_given_loss", SPEC["loss_rate_ratio"]), ("p_label_given_no_loss", 1.0)):
        y_pre = _nb(rng, mu, size)
        y_post = _nb(rng, mu * rr, size)
        out[name] = round(float(((y_post + 0.5) / (y_pre + 0.5) > SPEC["label_ratio_threshold"]).mean()), 3)
    return out


def main() -> None:
    spec_bytes = json.dumps(SPEC, sort_keys=True).encode()
    rng = np.random.default_rng(SPEC["seed"])
    base = SPEC["latent_auroc_baseline"]
    alt = base + SPEC["latent_gain_alternative"]
    reliability = [{"activity_floor": f, "temporal_size": s, **label_reliability(rng, f, s),
                    "oracle_map_D40_m20": run_cell(rng, 40, 20, f, s, base, base, SPEC["z_stop"]["K1"], oracle=True)}
                   for f in SPEC["activity_floor"] for s in SPEC["temporal_size"]]
    cells = []
    for m in SPEC["units_per_departure"]:
        for f in SPEC["activity_floor"]:
            for s in SPEC["temporal_size"]:
                for D in SPEC["departures"]:
                    null = {k: run_cell(rng, D, m, f, s, base, base, z) for k, z in SPEC["z_stop"].items()}
                    gain = run_cell(rng, D, m, f, s, alt, base, SPEC["z_stop"]["K1"])
                    cells.append({"departures": D, "units_per_departure": m, "activity_floor": f,
                                  "temporal_size": s, "p_stop_null_K1": null["K1"]["p_stop"],
                                  "p_stop_null_K6": null["K6"]["p_stop"],
                                  "p_continue_null": null["K1"]["p_continue"],
                                  "p_continue_gain": gain["p_continue"],
                                  "p_stop_gain": gain["p_stop"],
                                  "mean_observed_delta_gain": gain["mean_delta"],
                                  "mean_positives_null": null["K1"]["mean_positives"]})
                    print(cells[-1], file=sys.stderr)

    def first(m, f, s, key):
        rows = [c for c in cells if (c["units_per_departure"], c["activity_floor"], c["temporal_size"]) == (m, f, s)]
        hit = [c["departures"] for c in rows if c[key] >= 0.8]
        return min(hit) if hit else None

    minimum = [{"units_per_departure": m, "activity_floor": f, "temporal_size": s,
                "departures_for_p_stop_null_K1_ge_0.8": first(m, f, s, "p_stop_null_K1"),
                "departures_for_p_stop_null_K6_ge_0.8": first(m, f, s, "p_stop_null_K6"),
                "departures_for_p_continue_gain_ge_0.8": first(m, f, s, "p_continue_gain")}
               for m in SPEC["units_per_departure"] for f in SPEC["activity_floor"] for s in SPEC["temporal_size"]]

    check_rng = np.random.default_rng(SPEC["seed"] + 1)
    selfcheck = {
        "planted_oracle_map_continues": run_cell(check_rng, 40, 20, 20, None, base, base, 1.85, oracle=True),
        "activity_stand_in_does_not_continue": run_cell(check_rng, 40, 20, 20, None, base, base, 1.85, stand_in=True),
        "best_reachable_note": ("an oracle map knows z, not the observed label, so its observed dAUROC is "
                                "bounded by label noise; see label_reliability"),
    }
    out = {"label": LABEL, "spec_sha256": hashlib.sha256(spec_bytes).hexdigest(),
           "generator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           "numpy": np.__version__, "python": sys.version.split()[0], "spec": SPEC,
           "label_reliability": reliability, "selfcheck": selfcheck, "minimum_departures": minimum,
           "cells": cells}
    (HERE / "power.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
