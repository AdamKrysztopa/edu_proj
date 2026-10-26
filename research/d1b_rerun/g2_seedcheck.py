"""D1b plan §2.2 G2 seed check (owner, 2026-10-26): before any gated judge sees the gate split, two
readers that will not be gated (deepseek-v4.1-flash and glm-5.3-flash, reasoning capped at 2,000
tokens) judge only each gate topic's no-insert arm. A topic both close is proposed for dropping;
the owner decides. Writes `g2/seedcheck.json`.

    uv run --directory gapmap python ../research/d1b_rerun/g2_seedcheck.py --max-usd 0.80 \
        --spend-ledger ../research/d1b_rerun/openrouter_spend.jsonl
"""
import argparse
import json
from pathlib import Path

from gapmap import judge as judge_mod

import g2

READERS = ("deepseek/deepseek-v4.1-flash", "z-ai/glm-5.3-flash")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--max-usd", type=float, required=True)
    p.add_argument("--spend-ledger", required=True)
    args = p.parse_args()
    topics = json.loads((g2.FIXTURES / "topics.json").read_text())["topics"]
    inserts = json.loads((g2.FIXTURES / "inserts.json").read_text())
    confirmed = json.loads((g2.FIXTURES / "confirmations.json").read_text())
    gate = [t for t in g2.kept_topics(topics, confirmed) if t["split"] == "gate"]
    out = g2.HERE / "g2" / "seedcheck"
    out.mkdir(parents=True, exist_ok=True)
    states: dict = {t["topic_id"]: {} for t in gate}
    for model in READERS:
        backend = judge_mod.OpenRouterJudge(model, max_usd=args.max_usd, spend_ledger=args.spend_ledger,
                                            reasoning_max_tokens=2000)
        judge = judge_mod.CachedJudge(backend, out / f"{model.replace('/', '_')}.json", live=True,
                                      meta={"model": model, **backend.settings})
        try:
            for t in gate:
                states[t["topic_id"]][model] = g2._state(judge, t, g2.arms(t, inserts[t["topic_id"]])["0"])
        finally:
            judge.save()
    result = {"readers": list(READERS), "states": states, "proposed_drops": g2.seed_drops(states)}
    (g2.HERE / "g2" / "seedcheck.json").write_text(json.dumps(result, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"gate_topics": len(gate), "proposed_drops": result["proposed_drops"],
                      "kept_if_dropped": len(gate) - len(result["proposed_drops"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
