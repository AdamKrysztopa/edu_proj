"""Item 3 (c), ADR 0009: gemma, the other-family arm, judges control2 on GDPR v1's pairs with the
same prompt and parser as sol's I1c run (equal `pairs_sha256`). Any undecided arm makes the run
incomplete. Direction: the seed-free closed 95% CI above 0.

    uv run --directory gapmap python ../research/closure_topicality/c2_gemma.py \
        [--live --max-usd X --spend-ledger ../research/closure_topicality/openrouter_spend.jsonl]
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from pathlib import Path

from residual.ledger import Ledger

from gapmap import control2, judge as judge_mod, lenses, link

HERE = Path(__file__).resolve().parent
W = HERE.parents[1]
LEDGER = W / "reconstruct" / "runs" / "20260928T135354Z-eb840a85b7d1" / "ledger.json"
SOL = W / "research" / "n3_control_v3" / "sol" / "gdpr_v1" / "control2.json"
MODEL = "google/gemma-4-31b-it"
REASONING_MAX_TOKENS = 2000


def run(judge) -> dict:
    text_ = LEDGER.read_text()
    lg = Ledger.from_json(text_)
    idx = link.build_index(lg)
    specs = control2.build_pairs(lg, idx, lenses.run_all(lg, idx, link.SETTING_1))
    sha = control2.pairs_sha256(specs)
    if sha != json.loads(SOL.read_text())["pairs_sha256"]:
        raise SystemExit("pairs differ from sol's I1c GDPR v1 pairs")
    pairs = control2.judge_pairs(specs, judge)
    summary = control2.summarise(pairs)
    undecided = sum(summary["total"]["undecided"].values())
    primary = summary["total"]["seed_free"]["closed"]
    ci = primary["ci95"]
    direction = "incomplete" if undecided else "+" if ci and ci[0] > 0 else "-" if ci and ci[1] < 0 else "0"
    return {"domain": "GDPR DPIA (run v1)", "ledger_sha256": control2._sha256_text(text_), "pairs_sha256": sha,
            "judge_model": judge.model_id, "primary": list(control2.PRIMARY), "summary": summary,
            "undecided": undecided, "complete": undecided == 0, "direction": direction,
            "length_stand_in": control2.length_stand_in(specs),
            "pairs": [dataclasses.asdict(p) for p in pairs]}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="c2_gemma")
    p.add_argument("--live", action="store_true")
    p.add_argument("--max-usd", type=float)
    p.add_argument("--spend-ledger")
    args = p.parse_args(argv)
    if args.live and args.max_usd is None:
        p.error("--live needs --max-usd")
    backend = judge_mod.OpenRouterJudge(MODEL, max_usd=args.max_usd or 0.0,
                                        spend_ledger=args.spend_ledger if args.live else None,
                                        reasoning_max_tokens=REASONING_MAX_TOKENS)
    meta = {"model": MODEL, **backend.settings}
    out = HERE / "control2_gemma" / "gdpr_v1"
    out.mkdir(parents=True, exist_ok=True)
    judge = judge_mod.CachedJudge(backend, out / "closure_judgements.json", live=args.live, meta=meta,
                                  live_flag="--live")
    try:
        res = run(judge)
    finally:
        judge.save()
    res["judge_settings"] = meta
    if args.live:
        res["spend"] = backend.spend()
    (out / "control2.json").write_text(json.dumps(res, indent=1, sort_keys=True) + "\n")
    pr = res["summary"]["total"]["seed_free"]["closed"]
    print(MODEL, "own", round(pr["own_rate"], 3), "ctrl", round(pr["control_rate"], 3), "diff", round(pr["diff"], 3),
          pr["ci95"], "direction", res["direction"], "undecided", res["undecided"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
