"""I1b step 3: the judge calls control2 will make on PLC, GDPR v1 and GDPR v2, priced before any call.

    uv run --directory gapmap python ../research/n3_control_luna/estimate.py
"""
import json
from pathlib import Path

from residual.ledger import Ledger

from gapmap import control2, judge as judge_mod, lenses, link, semantic

ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "reconstruct/runs"
DOMAINS = {"plc": "20260928T133336Z-59ec876b3d7e", "gdpr_v1": "20260928T135354Z-eb840a85b7d1",
           "gdpr_v2": "20260928T145943Z-bc1cc9a30a02"}
MODEL = "gpt-5.6-luna"
CHARS_PER_TOKEN = 4.0
EXPECTED_REASONING_TOKENS = 1000
L73_CALLS = 48


def prompts(run: str) -> list[str]:
    ledger = Ledger.from_json((RUNS / run / "ledger.json").read_text())
    index = link.build_index(ledger)
    specs = control2.build_pairs(ledger, index, lenses.run_all(ledger, index, link.SETTING_1))
    return [semantic.build_prompt(s.seed_text, s.question, s.arm(arm))
            for s in specs if s.k >= 1 for arm in control2.ARMS]


def main() -> None:
    pin, pout = judge_mod.OPENAI_PRICES_PER_MTOK[MODEL]
    cap = judge_mod.OpenAIJudge(MODEL, max_usd=0).settings["max_completion_tokens"]
    qwen = [v for d in DOMAINS for k, v in
            json.loads((ROOT / f"research/n3/{d}/closure_judgements.json").read_text()).items()
            if k != "_meta"]
    reply_tokens = sum(len(json.dumps(v)) for v in qwen) / len(qwen) / CHARS_PER_TOKEN
    out = {"model": MODEL, "price_usd_per_mtok": [pin, pout], "max_completion_tokens": cap,
           "visible_reply_tokens_mean": reply_tokens, "domains": {}}
    total_calls, total_in = 0, 0.0
    for d, run in DOMAINS.items():
        ps = prompts(run)
        unique = sorted(set(ps))
        tok = sum(len(p) for p in unique) / CHARS_PER_TOKEN
        out["domains"][d] = {"prompts": len(ps), "unique_calls": len(unique), "prompt_tokens": round(tok)}
        total_calls += len(unique)
        total_in += tok
    total_calls += L73_CALLS
    total_in += L73_CALLS * 300
    out["calls"] = total_calls
    out["expected_usd"] = (total_in * pin + total_calls * (reply_tokens + EXPECTED_REASONING_TOKENS) * pout) / 1e6
    out["worst_case_usd"] = (total_in * pin + total_calls * cap * pout) / 1e6
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
