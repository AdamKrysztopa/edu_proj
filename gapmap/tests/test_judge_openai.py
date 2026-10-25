"""judge.py OpenAIJudge (I1b): the same Judge interface and JSON-reply contract as OllamaJudge, a
hard USD cap checked before every call, settings recorded in the cache metadata. A fake transport
stands in for the network; no test opens a socket."""
import json

import pytest
from conftest import FakeJudge
from test_control2 import _three_sel

from gapmap import control2, judge as judge_mod, semantic


class FakePost:
    def __init__(self, content='{"states": [1], "partially": [], "reason": "r"}',
                 prompt_tokens=1000, completion_tokens=500, reasoning_tokens=300, model="gpt-5.6-luna-2026"):
        self.content, self.model = content, model
        self.usage = {"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens,
                      "completion_tokens_details": {"reasoning_tokens": reasoning_tokens}}
        self.bodies = []

    def __call__(self, url, body, headers):
        self.bodies.append(body)
        return {"model": self.model, "usage": self.usage,
                "choices": [{"finish_reason": "stop", "message": {"content": self.content}}]}


def _judge(post, max_usd=5.0, **kw):
    return judge_mod.OpenAIJudge("gpt-5.6-luna", max_usd=max_usd, post=post, **kw)


def test_a_reply_parses_to_the_same_dict_contract_as_ollama():
    post = FakePost()
    assert _judge(post).ask("Respond as JSON only") == {"states": [1], "partially": [], "reason": "r"}


@pytest.mark.parametrize("content", ["not json", "[1, 2]", None, ""])
def test_unparseable_or_non_object_or_refused_content_is_none(content):
    assert _judge(FakePost(content=content)).ask("p") is None


def test_the_request_carries_the_prompt_json_mode_and_the_recorded_reasoning_setting():
    post = FakePost()
    j = _judge(post, reasoning_effort="medium")
    j.ask("the prompt")
    body = post.bodies[0]
    assert body["model"] == "gpt-5.6-luna"
    assert body["messages"] == [{"role": "user", "content": "the prompt"}]
    assert body["response_format"] == {"type": "json_object"}
    assert body["reasoning_effort"] == "medium"
    assert "temperature" not in body
    assert j.settings["reasoning_effort"] == "medium"
    assert j.settings["max_completion_tokens"] == body["max_completion_tokens"]


def test_cost_accumulates_from_reported_usage_at_the_model_price():
    post = FakePost(prompt_tokens=1_000_000, completion_tokens=1_000_000)
    j = _judge(post, max_usd=100.0, max_completion_tokens=1000)
    j.ask("p")
    pin, pout = judge_mod.OPENAI_PRICES_PER_MTOK["gpt-5.6-luna"]
    assert j.spent_usd == pytest.approx(pin + pout)
    assert j.calls[0]["served_model"] == "gpt-5.6-luna-2026"
    assert j.calls[0]["reasoning_tokens"] == 300


def test_the_budget_is_checked_before_the_call_and_a_blocked_call_never_dispatches():
    post = FakePost()
    j = _judge(post, max_usd=0.0001)
    with pytest.raises(judge_mod.BudgetExceeded):
        j.ask("p")
    assert post.bodies == [] and j.incomplete


def test_accumulated_spend_blocks_the_next_call_so_the_cap_is_never_exceeded():
    post = FakePost(prompt_tokens=10_000, completion_tokens=2_000)
    j = _judge(post, max_usd=0.02, max_completion_tokens=2_000)
    with pytest.raises(judge_mod.BudgetExceeded):
        for _ in range(100):
            j.ask("p")
    assert j.incomplete
    assert j.spent_usd <= 0.02
    assert len(post.bodies) == len(j.calls) >= 1


def test_an_unpriced_model_is_refused():
    with pytest.raises(ValueError):
        judge_mod.OpenAIJudge("gpt-unknown", max_usd=1.0, post=FakePost())


def test_a_budget_stop_propagates_through_the_parser_instead_of_becoming_undecided():
    j = _judge(FakePost(), max_usd=0.0)
    ret = semantic.build_retrieval([("c1", 0, "a sentence")])
    with pytest.raises(judge_mod.BudgetExceeded):
        semantic.judge_retrieval(j, ret, "seed", "question?")


def test_the_cached_wrapper_records_settings_and_replays_without_the_network(tmp_path):
    cache = tmp_path / "c.json"
    live = judge_mod.CachedJudge(_judge(FakePost()), cache, live=True, meta={"reasoning_effort": "medium"})
    live.ask("p")
    live.save()
    stored = json.loads(cache.read_text())
    assert stored["_meta"] == {"reasoning_effort": "medium"}

    class _NoNet:
        model_id = "gpt-5.6-luna"

        def ask(self, prompt):
            raise AssertionError("replay must not call the judge")

    replay = judge_mod.CachedJudge(_NoNet(), cache, live=False, meta={"reasoning_effort": "medium"})
    assert replay.ask("p") == {"states": [1], "partially": [], "reason": "r"}
    with pytest.raises(ValueError):
        judge_mod.CachedJudge(_NoNet(), cache, live=False, meta={"reasoning_effort": "high"})


def test_a_cache_without_meta_is_written_exactly_as_before(tmp_path):
    cache = tmp_path / "c.json"
    j = judge_mod.CachedJudge(FakeJudge(), cache, live=True)
    j.ask("p")
    j.save()
    assert "_meta" not in json.loads(cache.read_text())


def _ledger_args(tmp_path):
    """A ledger whose sidecar names no OpenAI stage, so ADR 0009 lets an OpenAI judge run alone."""
    lg, _idx, _cands, _seed = _three_sel(planted="Choose the test whose failure likelihood is highest.")
    path, sidecar = tmp_path / "ledger.json", tmp_path / "sidecar.json"
    path.write_text(lg.to_json())
    sidecar.write_text(json.dumps({"config": {"models": {"extractor": {"family": "anthropic"}}}}))
    return ["--ledger", str(path), "--sidecar", str(sidecar)]


def test_control2_cli_runs_the_openai_judge_and_records_model_spend_and_completeness(tmp_path, monkeypatch):
    post = FakePost(content='{"states": [], "partially": [], "reason": "r"}')
    monkeypatch.setattr(judge_mod, "_http_post", post)
    out = tmp_path / "out"
    control2.main([*_ledger_args(tmp_path), "--domain", "d", "--out", str(out),
                   "--judge", "openai", "--model", "gpt-5.6-luna", "--max-usd", "5"])
    res = json.loads((out / "control2.json").read_text())
    assert res["judge_model"] == "gpt-5.6-luna" and res["complete"] is True
    assert res["spend"]["calls"] == len(post.bodies) > 0
    assert res["judge_settings"]["reasoning_effort"] == "medium"
    replay_out = tmp_path / "replay"
    replay_out.mkdir()
    (replay_out / "closure_judgements.json").write_bytes((out / "closure_judgements.json").read_bytes())
    monkeypatch.setattr(judge_mod, "_http_post", None)
    control2.main([*_ledger_args(tmp_path), "--domain", "d", "--out", str(replay_out),
                   "--model", "gpt-5.6-luna"])
    assert json.loads((replay_out / "control2.json").read_text())["pairs"] == res["pairs"]


def test_control2_cli_marks_a_budget_stopped_run_incomplete(tmp_path, monkeypatch):
    monkeypatch.setattr(judge_mod, "_http_post", FakePost())
    out = tmp_path / "out"
    with pytest.raises(SystemExit):
        control2.main([*_ledger_args(tmp_path), "--domain", "d", "--out", str(out),
                       "--judge", "openai", "--model", "gpt-5.6-luna", "--max-usd", "0.00001"])
    res = json.loads((out / "control2.json").read_text())
    assert res["complete"] is False and "summary" not in res


def test_the_openai_cli_requires_a_max_usd(tmp_path):
    with pytest.raises(SystemExit):
        control2.main([*_ledger_args(tmp_path), "--domain", "d", "--out",
                       str(tmp_path / "o"), "--judge", "openai", "--model", "gpt-5.6-luna"])


# --------------------------------------------------------------------------- I1c: gpt-6.1-sol, one shared cap

def test_gpt_6_1_sol_is_priced_from_its_model_page():
    assert judge_mod.OPENAI_PRICES_PER_MTOK["gpt-6.1-sol"] == (2.0, 10.0)
    assert judge_mod.OPENAI_CACHED_INPUT_PER_MTOK["gpt-6.1-sol"] == 0.10


def test_the_control2_cli_passes_the_reasoning_effort_to_the_request(tmp_path, monkeypatch):
    post = FakePost(content='{"states": [], "partially": [], "reason": "r"}')
    monkeypatch.setattr(judge_mod, "_http_post", post)
    out = tmp_path / "out"
    control2.main([*_ledger_args(tmp_path), "--domain", "d", "--out", str(out),
                   "--judge", "openai", "--model", "gpt-6.1-sol", "--reasoning-effort", "high",
                   "--max-usd", "5"])
    assert post.bodies and {b["reasoning_effort"] for b in post.bodies} == {"high"}
    assert {b["model"] for b in post.bodies} == {"gpt-6.1-sol"}
    assert json.loads((out / "control2.json").read_text())["judge_settings"]["reasoning_effort"] == "high"


def test_a_shared_spend_ledger_makes_one_cap_cover_every_run(tmp_path):
    spend = tmp_path / "spend.jsonl"
    post = FakePost(prompt_tokens=10, completion_tokens=2_000)
    first = _judge(post, max_usd=0.03, max_completion_tokens=2_000, spend_ledger=spend)
    first.ask("p")
    assert len(spend.read_text().splitlines()) == 1
    second = _judge(post, max_usd=0.03, max_completion_tokens=2_000, spend_ledger=spend)
    assert second.prior_usd == pytest.approx(first.spent_usd)
    with pytest.raises(judge_mod.BudgetExceeded):
        for _ in range(100):
            second.ask("p")
    total = sum(json.loads(line)["usd"] for line in spend.read_text().splitlines())
    assert total <= 0.03
    assert len(spend.read_text().splitlines()) == len(first.calls) + len(second.calls)


def test_the_control2_cli_charges_the_shared_spend_ledger(tmp_path, monkeypatch):
    spend = tmp_path / "spend.jsonl"
    spend.write_text(json.dumps({"usd": 4.99}) + "\n")
    post = FakePost()
    monkeypatch.setattr(judge_mod, "_http_post", post)
    with pytest.raises(SystemExit):
        control2.main([*_ledger_args(tmp_path), "--domain", "d", "--out",
                       str(tmp_path / "o"), "--judge", "openai", "--model", "gpt-6.1-sol",
                       "--max-usd", "5", "--spend-ledger", str(spend)])
    assert post.bodies == []
    assert len(spend.read_text().splitlines()) == 1


def test_cached_prompt_tokens_are_recorded():
    post = FakePost()
    post.usage["prompt_tokens_details"] = {"cached_tokens": 640}
    j = _judge(post)
    j.ask("p")
    assert j.calls[0]["cached_tokens"] == 640
    assert j.spend()["cached_tokens"] == 640
