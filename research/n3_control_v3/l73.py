"""I1c step 5: control2 (donor arm seed-free) run through a real judge on plain-text L7.3 fixtures.

Fixtures: `gapmap/tests/l73_fixtures.py`, three SEL topics with one planted pair each; per topic the
plant, three random-letter stand-ins (RNG seeds 7, 8, 9) and one plain-English length-matched
stand-in.

Eligibility rule, stated before any judge call (commit holding this file):
- The planted positive fires iff, on the planted pair of EVERY topic, the seed-free arms give
  own = closed and control != closed.
- A stand-in fires iff, on the target pair of ANY topic and ANY stand-in, the own seed-free arm is
  closed (it states no element, so a closure there is a false positive).
- A judge is eligible iff the planted positive fires and no stand-in fires. A judge failing either
  arm is ineligible; equal-cap arms are reported, not ruled on.

    uv run --directory gapmap python ../research/n3_control_v3/l73.py --tag qwen \
        --model qwen2.5:7b-instruct [--judge ollama]
    uv run --directory gapmap python ../research/n3_control_v3/l73.py --tag sol --model gpt-6.1-sol \
        --reasoning-effort high [--judge openai --max-usd 10 --spend-ledger ../research/n3_control_v3/openai_spend.jsonl]
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "gapmap/tests"))
from l73_fixtures import TOPICS, fixture, variants  # noqa: E402

from gapmap import control2, judge as judge_mod  # noqa: E402


def check(judge, topic, sentence: str) -> dict:
    lg, idx, cands, target = fixture(topic, sentence)
    specs = control2.build_pairs(lg, idx, cands)
    pairs = control2.judge_pairs(specs, judge)
    pair = next(p for p in pairs if target in p.seeds)
    return {"k": pair.k, "target_states": pair.states,
            "fires_seed_free": pair.states["own_sf"] == "closed" and pair.states["ctrl_sf"] != "closed",
            "fires_equal_cap": pair.states["own_eq"] == "closed" and pair.states["ctrl_eq"] != "closed",
            "own_sf_closed": pair.states["own_sf"] == "closed",
            "all_pairs": [{"seeds": p.seeds, "donor_seeds": p.donor_seeds, "states": p.states} for p in pairs]}


def evaluate(judge) -> dict:
    topics = {}
    for topic in TOPICS:
        rows = {name: {"sentence": s, **check(judge, topic, s)} for name, s in variants(topic)}
        topics[topic.name] = rows
    planted = all(t["planted"]["fires_seed_free"] for t in topics.values())
    stand_in = any(row["own_sf_closed"] for t in topics.values() for name, row in t.items() if name != "planted")
    return {"topics": topics, "planted_fires": planted, "stand_in_fires": stand_in,
            "eligible": planted and not stand_in}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--judge", choices=["ollama", "openai"])
    ap.add_argument("--max-usd", type=float)
    ap.add_argument("--reasoning-effort", default="medium")
    ap.add_argument("--spend-ledger")
    args = ap.parse_args()
    use_openai = args.model in judge_mod.OPENAI_PRICES_PER_MTOK
    if use_openai:
        if args.judge == "openai" and (args.max_usd is None or args.spend_ledger is None):
            ap.error("--judge openai needs --max-usd and --spend-ledger")
        backend = judge_mod.OpenAIJudge(args.model, max_usd=args.max_usd or 0.0,
                                        reasoning_effort=args.reasoning_effort,
                                        spend_ledger=args.spend_ledger if args.judge else None)
        meta = {"model": args.model, **backend.settings}
    else:
        backend, meta = judge_mod.OllamaJudge(model=args.model), None
    out = HERE / args.tag / "l73"
    out.mkdir(parents=True, exist_ok=True)
    judge = judge_mod.CachedJudge(backend, out / "closure_judgements.json", live=args.judge is not None,
                                  meta=meta)
    try:
        result = {"judge_model": backend.model_id, "judge_settings": meta, **evaluate(judge)}
    finally:
        judge.save()
        if use_openai and backend.calls:
            with (out / "judge_calls.jsonl").open("a") as f:
                f.writelines(json.dumps(c, sort_keys=True) + "\n" for c in backend.calls)
    if use_openai:
        result["spend"] = backend.spend()
    (out / "l73.json").write_text(json.dumps(result, sort_keys=True, indent=1) + "\n")
    print(json.dumps({k: result[k] for k in ("planted_fires", "stand_in_fires", "eligible")}))


if __name__ == "__main__":
    main()
