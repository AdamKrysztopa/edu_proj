"""judge.py OpenRouterJudge (D1b, 2026-10-26): non-OpenAI judges through OpenRouter's chat API,
with the OpenAI judge's contract -- a hard USD cap checked before every call, a shared spend ledger,
settings in the cache metadata. A fake transport stands in for the network."""
import json

import pytest
from test_judge_openai import FakePost
from test_main_judges import _args

from gapmap import __main__ as cli
from gapmap import judge as judge_mod

MODEL = "google/gemini-3.5-flash-lite"


def _judge(post, max_usd=5.0, **kw):
    return judge_mod.OpenRouterJudge(MODEL, max_usd=max_usd, post=post, **kw)


def test_the_request_goes_to_openrouter_in_json_mode_at_temperature_zero(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test")
    post = FakePost()
    calls = []
    j = _judge(lambda url, body, headers: calls.append((url, headers)) or post(url, body, headers))
    assert j.ask("prompt") == {"states": [1], "partially": [], "reason": "r"}
    url, headers = calls[0]
    body = post.bodies[0]
    assert url == judge_mod.OPENROUTER_URL
    assert headers["Authorization"] == "Bearer test"
    assert body["model"] == MODEL and body["temperature"] == 0
    assert body["response_format"] == {"type": "json_object"}
    assert "reasoning_effort" not in body


def test_the_billed_cost_is_used_when_openrouter_reports_it(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test")
    post = FakePost(prompt_tokens=1000, completion_tokens=500)
    post.usage["cost"] = 0.0123
    j = _judge(post)
    j.ask("p")
    assert j.spent_usd == pytest.approx(0.0123)


def test_without_a_reported_cost_the_pinned_price_is_charged(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test")
    j = _judge(FakePost(prompt_tokens=1_000_000, completion_tokens=1_000_000))
    j.ask("p")
    pin, pout = judge_mod.OPENROUTER_PRICES_PER_MTOK[MODEL]
    assert j.spent_usd == pytest.approx(pin + pout)


def test_the_cap_blocks_the_call_before_dispatch():
    post = FakePost()
    j = _judge(post, max_usd=0.000001)
    with pytest.raises(judge_mod.BudgetExceeded):
        j.ask("p")
    assert post.bodies == []


def test_an_unpriced_model_is_refused():
    with pytest.raises(ValueError):
        judge_mod.OpenRouterJudge("google/unknown-model", max_usd=1)


def test_every_candidate_is_outside_the_openai_and_anthropic_families():
    assert {judge_mod.family(m) for m in judge_mod.OPENROUTER_PRICES_PER_MTOK} == {"other"}


def test_the_gapmap_cli_runs_an_openrouter_judge_alone_and_replays(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test")
    post = FakePost(content='{"states": [], "partially": [], "reason": "r"}')
    monkeypatch.setattr(judge_mod, "_http_post", post)
    spend = tmp_path / "spend.jsonl"
    cli.main([*_args(tmp_path), "--judge", "openrouter", "--model", MODEL, "--max-usd", "1",
              "--spend-ledger", str(spend)])
    out = tmp_path / "out"
    rec = json.loads((out / "judge.json").read_text())
    assert rec["judge_model"] == MODEL and rec["complete"] is True
    assert rec["spend"]["calls"] == len(post.bodies) > 0
    first = (out / "gapmap.json").read_bytes()
    monkeypatch.setattr(judge_mod, "_http_post", None)
    cli.main([*_args(tmp_path), "--model", MODEL])
    assert (out / "gapmap.json").read_bytes() == first


def test_an_openrouter_replay_cache_miss_names_judge_openrouter(tmp_path):
    with pytest.raises(judge_mod.JudgeCacheMiss, match="--judge openrouter"):
        cli.main([*_args(tmp_path), "--model", MODEL])
