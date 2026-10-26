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


class Flaky:
    """Fails with the given HTTP codes in turn, then answers like FakePost."""

    def __init__(self, codes, finish_reason="stop"):
        self.codes, self.posts = list(codes), 0
        self.ok = FakePost()
        self.finish_reason = finish_reason

    def __call__(self, url, body, headers):
        import urllib.error
        self.posts += 1
        if self.codes:
            raise urllib.error.HTTPError(url, self.codes.pop(0), "err", {}, None)
        reply = self.ok(url, body, headers)
        reply["choices"][0]["finish_reason"] = self.finish_reason
        return reply


def _flaky_judge(post, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test")
    return judge_mod.OpenRouterJudge(MODEL, max_usd=5, post=post, sleep=lambda s: None)


def test_a_rate_limit_is_retried_then_answered(monkeypatch):
    post = Flaky([429, 503])
    assert _flaky_judge(post, monkeypatch).ask("p")["states"] == [1]
    assert post.posts == 3


def test_a_persistent_rate_limit_stops_the_run_instead_of_becoming_undecided(monkeypatch):
    post = Flaky([429] * 10)
    with pytest.raises(judge_mod.JudgeUnavailable):
        _flaky_judge(post, monkeypatch).ask("p")
    assert post.posts == 4


def test_a_non_transient_error_stops_at_once(monkeypatch):
    post = Flaky([400])
    with pytest.raises(judge_mod.JudgeUnavailable):
        _flaky_judge(post, monkeypatch).ask("p")
    assert post.posts == 1


def test_a_truncated_reply_stops_the_run_and_is_still_charged(monkeypatch):
    j = _flaky_judge(Flaky([], finish_reason="length"), monkeypatch)
    with pytest.raises(judge_mod.JudgeUnavailable, match="truncated"):
        j.ask("p")
    assert j.spent_usd > 0


def test_an_unavailable_judge_propagates_through_the_parser():
    from gapmap import semantic

    class Down:
        model_id = "down"

        def ask(self, prompt):
            raise judge_mod.JudgeUnavailable("429")

    retrieval = semantic.build_retrieval([("c", 0, "A sentence.")])
    with pytest.raises(judge_mod.JudgeUnavailable):
        semantic.judge_retrieval(Down(), retrieval, "seed", "question")


def test_the_default_reply_cap_leaves_room_for_reasoning_models():
    assert judge_mod.OpenRouterJudge(MODEL, max_usd=1).max_completion_tokens >= 8000


def test_a_reasoning_budget_is_sent_and_recorded_only_when_set(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test")
    post = FakePost()
    j = judge_mod.OpenRouterJudge("deepseek/deepseek-v4.1-flash", max_usd=5, post=post, reasoning_max_tokens=2000)
    j.ask("p")
    assert post.bodies[0]["reasoning"] == {"max_tokens": 2000}
    assert j.settings["reasoning_max_tokens"] == 2000
    plain = FakePost()
    judge_mod.OpenRouterJudge(MODEL, max_usd=5, post=plain).ask("p")
    assert "reasoning" not in plain.bodies[0]
    assert "reasoning_max_tokens" not in judge_mod.OpenRouterJudge(MODEL, max_usd=5).settings
