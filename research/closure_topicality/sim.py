"""SYNTHETIC: probability that one run passes RT part I on one split (plan §1.6), independent
topics, one per cluster.

    uv run --directory gapmap python ../research/closure_topicality/sim.py
"""
from __future__ import annotations

import json
import random
from pathlib import Path

import rt

HERE = Path(__file__).resolve().parent
GRID = ((0.9, 0.1), (0.8, 0.1), (0.8, 0.2), (0.7, 0.2), (0.5, 0.5))


def pass_rate(n: int, p: float, q: float, r: float = 0.02, *, reps: int = 400, seed: int = 1) -> float:
    rng = random.Random(seed)
    topics = [{"topic_id": f"t{i}", "cluster": f"c{i}"} for i in range(n)]
    wins = 0
    for _ in range(reps):
        hits = {t["topic_id"]: {"0": False, "P": rng.random() < p, "N": rng.random() < q, "R": rng.random() < r}
                for t in topics}
        wins += rt.part_one(topics, hits)["passes"]
    return wins / reps


def main() -> int:
    out = {"note": "SYNTHETIC simulation; R hit 0.02; 400 replicates per cell",
           "cells": [{"n": n, "p": p, "q": q, "pass": pass_rate(n, p, q)} for n in (13, 16) for p, q in GRID]}
    (HERE / "sim.json").write_text(json.dumps(out, indent=1) + "\n")
    for c in out["cells"]:
        print(c)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
