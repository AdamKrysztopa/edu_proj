"""D1b plan §4 R4: sol's run-to-run stability. Replays a finished gap-map run from its cache ($0) to
recover the prompts it asked, re-asks a seeded 20% of them live with the cache bypassed, and reports
how often the closure state agrees. Writes `<out>/retest.json` (aggregates only: it travels with the
sealed closure outputs, never printed per prompt).

    uv run --directory gapmap python ../research/d1b_rerun/retest.py --run-dir DIR --ledger L --sidecar S \
        --model gpt-6.1-sol --reasoning-effort high --max-usd X --spend-ledger F
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from gapmap import __main__ as cli
from gapmap import judge as judge_mod, semantic

FRACTION = 0.20
SEED = 20261026


class Recorder:
    def __init__(self, inner):
        self.inner, self.model_id, self.prompts = inner, inner.model_id, []

    def ask(self, prompt: str):
        self.prompts.append(prompt)
        return self.inner.ask(prompt)


def state(reply) -> str:
    """The reply's state before id resolution: closed iff `states` is non-empty, partial iff only
    `partially` is, open iff both are empty, undecided otherwise (as in I1c's test-retest)."""
    if not isinstance(reply, dict) or not any(isinstance(reply.get(k), list) for k in ("states", "partially")):
        return "undecided"
    if reply.get("states"):
        return "closed"
    return "partial" if reply.get("partially") else "open"


def sample(prompts: list[str]) -> list[str]:
    unique = sorted(set(prompts))
    k = max(1, round(FRACTION * len(unique)))
    return random.Random(SEED).sample(unique, k)


def agreement(first: list, second: list) -> dict:
    pairs = list(zip(map(state, first), map(state, second)))
    same = sum(a == b for a, b in pairs)
    return {"n": len(pairs), "agree": same, "rate": same / len(pairs) if pairs else None}


def main() -> int:
    p = argparse.ArgumentParser()
    for a in ("--run-dir", "--ledger", "--sidecar", "--model", "--spend-ledger"):
        p.add_argument(a, required=True)
    p.add_argument("--reasoning-effort", default="high")
    p.add_argument("--max-usd", type=float, required=True)
    args = p.parse_args()
    run_dir = Path(args.run_dir)
    meta_backend = judge_mod.OpenAIJudge(args.model, max_usd=0.0, reasoning_effort=args.reasoning_effort)
    cached = judge_mod.CachedJudge(meta_backend, run_dir / "closure_judgements.json", live=False,
                                   meta={"model": args.model, **meta_backend.settings}, live_flag="--judge openai")
    rec = Recorder(cached)
    scratch = run_dir / "_replay"
    cli.run(args.ledger, domain="forecastability", out_dir=str(scratch), sidecar_path=args.sidecar, judge=rec)
    chosen = sample(rec.prompts)
    first = [cached.ask(q) for q in chosen]
    live = judge_mod.OpenAIJudge(args.model, max_usd=args.max_usd, reasoning_effort=args.reasoning_effort,
                                 spend_ledger=args.spend_ledger)
    second = [live.ask(q) for q in chosen]
    out = {"model": args.model, "fraction": FRACTION, "seed": SEED, "unique_prompts": len(set(rec.prompts)),
           **agreement(first, second), "spend": live.spend()}
    (run_dir / "retest.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    for f in scratch.iterdir():
        f.unlink()
    scratch.rmdir()
    print(json.dumps({k: out[k] for k in ("unique_prompts", "n", "agree", "rate")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
