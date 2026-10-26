"""D1b plan §2.2 G1: the N3 L7.3 fixtures through `research/n3_control_v3/l73.py`, rule unchanged,
with outputs under `research/d1b_rerun/g1/<tag>/` instead of the N3 control record. l73.py builds
its own judge and knows only OpenAI and Ollama models; for an OpenRouter model id the wrapper hands
it a `judge` module whose OpenAI judge is `OpenRouterJudge` (pass `--judge openai`, as for sol);
`--reasoning-max-tokens N` is taken by the wrapper and passed to that judge.

    uv run --directory gapmap python ../research/d1b_rerun/g1.py --tag gemini --judge openai \
        --model google/gemini-3.5-flash-lite --max-usd X --spend-ledger ../research/d1b_rerun/openrouter_spend.jsonl
"""
import importlib.util
import sys
import types
from pathlib import Path

from gapmap import judge as judge_mod

HERE = Path(__file__).resolve().parent


def load_l73() -> types.ModuleType:
    spec = importlib.util.spec_from_file_location("l73", HERE.parent / "n3_control_v3" / "l73.py")
    l73 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(l73)
    l73.HERE = HERE / "g1"
    return l73


def _openrouter_shim(reasoning_max_tokens: int | None = None) -> types.ModuleType:
    shim = types.ModuleType("judge_openrouter_shim")
    shim.__dict__.update(judge_mod.__dict__)
    shim.OPENAI_PRICES_PER_MTOK = {**judge_mod.OPENAI_PRICES_PER_MTOK, **judge_mod.OPENROUTER_PRICES_PER_MTOK}

    def make(model, *, max_usd, reasoning_effort=None, spend_ledger=None, **_kw):
        if model in judge_mod.OPENROUTER_PRICES_PER_MTOK:
            return judge_mod.OpenRouterJudge(model, max_usd=max_usd, spend_ledger=spend_ledger,
                                             reasoning_max_tokens=reasoning_max_tokens)
        return judge_mod.OpenAIJudge(model, max_usd=max_usd, reasoning_effort=reasoning_effort,
                                     spend_ledger=spend_ledger)

    shim.OpenAIJudge = make
    return shim


if __name__ == "__main__":
    l73 = load_l73()
    budget = None
    if "--reasoning-max-tokens" in sys.argv:
        i = sys.argv.index("--reasoning-max-tokens")
        budget = int(sys.argv[i + 1])
        del sys.argv[i:i + 2]
    if "--model" in sys.argv and sys.argv[sys.argv.index("--model") + 1] in judge_mod.OPENROUTER_PRICES_PER_MTOK:
        l73.judge_mod = _openrouter_shim(budget)
    l73.main()
