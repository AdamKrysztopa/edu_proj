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



def test_wrapper_flags_are_taken_out_of_argv_before_l73_parses_it(monkeypatch):
    monkeypatch.setattr(g1.sys, "argv", ["g1.py", "--tag", "t", "--out-root", "/x", "--model", "m"])
    assert g1._take("--out-root") == "/x" and g1._take("--reasoning-max-tokens") is None
    assert g1.sys.argv == ["g1.py", "--tag", "t", "--model", "m"]
