"""I1c step 6: the OpenAI calls of the fixed control (steps 5 and 6), priced from I1b's measured
tokens (`research/n3_control_luna/<domain>/judge_calls.jsonl`) before any call.

Prompt tokens: the new prompts' characters at I1b's measured tokens per character. Completion tokens:
I1b's measured mean per call, for Luna at effort medium; for sol at effort high, that mean times
`--sol-multiplier` scenarios (high effort reasons longer; I1b measured only medium). The worst case
fills `max_completion_tokens` on every call.

Stop rule, stated before any call: if the x1 total exceeds $10, no OpenAI call runs. After step 5,
the sol multiplier is replaced by sol's measured completion tokens per L7.3 call over Luna's; if
the remaining domain calls of Luna and sol then exceed $10 less the step-5 spend, no domain call
runs. The cap itself is enforced per call by `OpenAIJudge` against `openai_spend.jsonl`.

    uv run --directory gapmap python ../research/n3_control_v3/estimate.py [estimate_run2.json]
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "gapmap/tests"))
from l73_fixtures import TOPICS, fixture, variants  # noqa: E402
from residual.ledger import Ledger  # noqa: E402

from gapmap import control2, judge as judge_mod, lenses, link, semantic  # noqa: E402

RUNS = {"plc": "20260928T133336Z-59ec876b3d7e", "gdpr_v1": "20260928T135354Z-eb840a85b7d1",
        "gdpr_v2": "20260928T145943Z-bc1cc9a30a02"}
SOL_MULTIPLIERS = (1.0, 3.0, 5.0)
MAX_COMPLETION = 6000


def _prompts(specs) -> set[str]:
    return {semantic.build_prompt(s.seed_text, s.question, s.arm(a)) for s in specs if s.k >= 1
            for a in control2.ARMS}


def domain_prompts(run: str) -> set[str]:
    lg = Ledger.from_json((ROOT / "reconstruct/runs" / run / "ledger.json").read_text())
    idx = link.build_index(lg)
    return _prompts(control2.build_pairs(lg, idx, lenses.run_all(lg, idx, link.SETTING_1)))


def l73_prompts() -> set[str]:
    out = set()
    for topic in TOPICS:
        for _name, sentence in variants(topic):
            lg, idx, cands, _t = fixture(topic, sentence)
            out |= _prompts(control2.build_pairs(lg, idx, cands))
    return out


def luna_measured() -> dict:
    calls = []
    for d in RUNS:
        calls += [json.loads(x) for x in (ROOT / f"research/n3_control_luna/{d}/judge_calls.jsonl").read_text().splitlines()]
    return {"calls": len(calls), "prompt_tokens": sum(c["prompt_tokens"] for c in calls),
            "completion_tokens": sum(c["completion_tokens"] for c in calls),
            "reasoning_tokens": sum(c["reasoning_tokens"] for c in calls)}


def main() -> None:
    measured = luna_measured()
    estimate_luna = json.loads((ROOT / "research/n3_control_luna/estimate.json").read_text())
    luna_chars = 4.0 * sum(v["prompt_tokens"] for v in estimate_luna["domains"].values())
    tok_per_char = measured["prompt_tokens"] / luna_chars
    completion_per_call = measured["completion_tokens"] / measured["calls"]
    sets = {d: domain_prompts(r) for d, r in RUNS.items()}
    sets["l73"] = l73_prompts()
    calls = {k: len(v) for k, v in sets.items()}
    prompt_tok = {k: sum(len(p) for p in v) * tok_per_char for k, v in sets.items()}
    n, pin_tok = sum(calls.values()), sum(prompt_tok.values())
    out = {"basis": "I1b measured (research/n3_control_luna/*/judge_calls.jsonl)",
           "luna_measured": measured, "tokens_per_prompt_char": tok_per_char,
           "completion_tokens_per_call_luna_medium": completion_per_call,
           "calls": calls, "prompt_tokens": {k: round(v) for k, v in prompt_tok.items()}, "models": {}}
    for model, scenarios in (("gpt-5.6-luna", (1.0,)), ("gpt-6.1-sol", SOL_MULTIPLIERS)):
        pin, pout = judge_mod.OPENAI_PRICES_PER_MTOK[model]
        out["models"][model] = {
            "price_usd_per_mtok": [pin, pout],
            "expected_usd": {f"x{m:g}": (pin_tok * pin + n * completion_per_call * m * pout) / 1e6
                             for m in scenarios},
            "worst_case_usd": (pin_tok * pin + n * MAX_COMPLETION * pout) / 1e6}
    luna = out["models"]["gpt-5.6-luna"]["expected_usd"]["x1"]
    out["total_expected_usd"] = {k: luna + v for k, v in out["models"]["gpt-6.1-sol"]["expected_usd"].items()}
    (HERE / (sys.argv[1] if len(sys.argv) > 1 else "estimate.json")).write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
