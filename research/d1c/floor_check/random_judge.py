"""D1c plan §1: how often a random closure judge reaches the 10-pair floor on D1b's own pools.
One judge, each version open with probability p, independently; arms and matching as coded
(`build_sheet.arm_of`, `count_summary`). 500 seeds per cell. $0, no model.

    uv run --directory gapmap python ../research/d1c/floor_check/random_judge.py
"""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "d1b_rerun"))

import build_sheet as bs  # noqa: E402
import codebase  # noqa: E402

SEEDS = 500
P_OPEN = (0.2, 0.3, 0.5)


def reach_rate(topics: list[dict], p: float) -> float:
    hits = 0
    for seed in range(SEEDS):
        rng = random.Random(seed)
        states = {v: {"rand": "open" if rng.random() < p else "closed"} for t in topics for v in t["versions"]}
        gaps = [t for t in topics if bs.arm_of(t, states, ("rand",)) == "gap"]
        covs = [t for t in topics if bs.arm_of(t, states, ("rand",)) == "covered"]
        hits += not bs.count_summary(topics, gaps, covs, seed=1)["stop_at_A"]
    return hits / SEEDS


def main() -> int:
    cb = codebase.d1b()
    drop = set(json.loads(cb.review.read_text())["drop"])
    full = [t for t in json.loads(cb.pool.read_text())["topics"] if t["topic_id"] not in drop]
    cheap = json.loads(bs.pool_outputs(cb, ["cheap-26b"])[0])["topics"]
    out = {}
    for name, topics in (("d1b_full_pool_reviewed", full), ("d1b_cheap_pool_unreviewed", cheap)):
        for t in topics:
            t["versions"] = [tuple(v) for v in t["versions"]]
        out[name] = {"topics": len(topics), **{f"p_open_{p}": reach_rate(topics, p) for p in P_OPEN}}
    (HERE / "random_judge.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
