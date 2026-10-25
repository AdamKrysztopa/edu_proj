"""I2 step 6: sol's primary (seed-free, closed) with its judge noise inside the CI, offline.

Per domain, the transition matrix P(run-2 state | run-1 state) is counted over the prompts that
I1c's run 1 (`run1_asymmetric/sol`) and run 2 (`sol`) both sent, on the reply state read before
the parser validates sentence numbers (as `compare.reply_state`). Inside the seed-cluster
bootstrap (same B, seed and clusters as `control2._cluster_ci`), each drawn pair's own and
control seed-free states are redrawn from the matrix row of their committed (run-2) state.
Cluster draws use the committed bootstrap seed and noise draws a second stream, so an identity
matrix reproduces the committed CI exactly (`check_identity`). The symmetrised matrix (both
directions pooled, since run order is arbitrary) is a sensitivity row.

    python3 research/n3_control_v3/sol_noise.py > research/n3_control_v3/sol_noise.json
"""
from __future__ import annotations

import json
import random
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
DOMAINS = ("plc", "gdpr_v1", "gdpr_v2")
STATES = ("closed", "partial", "open")
B, SEED = 2000, 20261024


def reply_state(reply) -> str:
    if not isinstance(reply, dict):
        return "undecided"
    if reply.get("states"):
        return "closed"
    return "partial" if reply.get("partially") else "open"


def transitions(domain: str) -> tuple[dict, int]:
    a = json.loads((HERE / "run1_asymmetric/sol" / domain / "closure_judgements.json").read_text())
    b = json.loads((HERE / "sol" / domain / "closure_judgements.json").read_text())
    keys = sorted((set(a) & set(b)) - {"_meta"})
    counts = Counter((reply_state(a[k]), reply_state(b[k])) for k in keys)
    return {f"{s}->{t}": n for (s, t), n in sorted(counts.items())}, len(keys)


def row_probs(counts: dict, symmetric: bool) -> dict[str, list[tuple[str, float]]]:
    c = Counter()
    for st, n in counts.items():
        s, t = st.split("->")
        c[(s, t)] += n
        if symmetric:
            c[(t, s)] += n
    out = {}
    for s in STATES:
        total = sum(c[(s, t)] for t in STATES)
        out[s] = [(t, c[(s, t)] / total) for t in STATES] if total else [(s, 1.0)]
    return out


def draw(rng: random.Random, row: list[tuple[str, float]]) -> str:
    u, acc = rng.random(), 0.0
    for t, p in row:
        acc += p
        if u < acc:
            return t
    return row[-1][0]


def noisy_ci(pairs: list[dict], probs: dict) -> dict:
    by_cluster: dict[str, list[dict]] = {}
    for p in pairs:
        by_cluster.setdefault(p["seeds"][0], []).append(p)
    groups = [by_cluster[c] for c in sorted(by_cluster)]
    rng, noise = random.Random(SEED), random.Random(SEED + 1)
    means = []
    for _ in range(B):
        draw_pairs = [p for _ in groups for p in rng.choice(groups)]
        diffs = [float(draw(noise, probs[p["states"]["own_sf"]]) == "closed")
                 - float(draw(noise, probs[p["states"]["ctrl_sf"]]) == "closed") for p in draw_pairs]
        means.append(sum(diffs) / len(diffs))
    means.sort()
    return {"ci95": [means[int(0.025 * B)], means[min(B - 1, int(0.975 * B))]]}


def direction(ci) -> str:
    return "+" if ci[0] > 0 else "-" if ci[1] < 0 else "0"


def main() -> None:
    out = {"b": B, "seed": SEED, "noise_seed": SEED + 1, "domains": {}}
    for d in DOMAINS:
        c2 = json.loads((HERE / "sol" / d / "control2.json").read_text())
        pairs = [p for p in c2["pairs"] if p["k"] >= 1]
        committed = c2["summary"]["total"]["seed_free"]["closed"]
        counts, n = transitions(d)
        identity = {s: [(s, 1.0)] for s in STATES}
        check_identity = noisy_ci(pairs, identity)["ci95"] == committed["ci95"]
        noisy = noisy_ci(pairs, row_probs(counts, symmetric=False))
        sym = noisy_ci(pairs, row_probs(counts, symmetric=True))
        out["domains"][d] = {
            "admissible": c2["admissible"], "n_pairs": len(pairs), "n_retest_prompts": n,
            "transitions_run1_to_run2": counts,
            "state_agreement": sum(v for k, v in counts.items() if k.split("->")[0] == k.split("->")[1]) / n,
            "primary_diff": committed["diff"], "committed_ci95": committed["ci95"],
            "check_identity_reproduces_committed_ci": check_identity,
            "noise_inflated_ci95": noisy["ci95"], "direction_noise_inflated": direction(noisy["ci95"]),
            "symmetrised_ci95": sym["ci95"], "direction_symmetrised": direction(sym["ci95"])}
    print(json.dumps(out, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
