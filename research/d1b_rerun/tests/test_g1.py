"""The G1 wrapper routes OpenRouter model ids to OpenRouterJudge and leaves OpenAI ids alone."""
import g1
from gapmap import judge as judge_mod


def test_the_shim_builds_an_openrouter_judge_for_an_openrouter_model_and_openai_for_sol():
    shim = g1._openrouter_shim()
    assert "google/gemini-3.5-flash-lite" in shim.OPENAI_PRICES_PER_MTOK
    j = shim.OpenAIJudge("google/gemini-3.5-flash-lite", max_usd=1, reasoning_effort="medium")
    assert isinstance(j, judge_mod.OpenRouterJudge)
    s = shim.OpenAIJudge("gpt-6.1-sol", max_usd=1, reasoning_effort="high")
    assert type(s) is judge_mod.OpenAIJudge and s.settings["reasoning_effort"] == "high"

