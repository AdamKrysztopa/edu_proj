import json

import anthropic
import httpx2
import pytest

from fakes import FakeAnthropic, FakeOpenAI, FakeResponse, TEST_MODELS, openai_response, turn_payload
from probe_app.backends import AnthropicBackend, OpenAICompatBackend
from probe_app.config import RoleModel
from probe_app.llm import Guard, InterviewerLLM, LLMRefused, LLMUnavailable, TurnRequest
from probe_app.models import DialogueTurn

PNG = bytes.fromhex("89504e470d0a1a0a")


def request(**kw) -> TurnRequest:
    base = dict(problems={"A1": "Block problem"}, transcript="[A1-s001 0.0-1.0s] Energy first.",
                snapshots={"A1": PNG}, dialogue=[DialogueTurn(speaker="expert", text="I used energy.", t=3.0)],
                remaining_s=600.0, wrap_up=False, unused=["A1/checks"])
    base.update(kw)
    return TurnRequest(**base)


def test_next_turn_parses_and_logs():
    logged = []
    client = FakeAnthropic(interviewer=[FakeResponse(turn_payload())])
    turn = InterviewerLLM(AnthropicBackend(client, TEST_MODELS.interviewer), logged.append, "SYSTEM").next_turn(request())
    assert turn.stem_id == "cues"
    call = client.calls[0]
    assert call["model"] == "claude-opus-5"
    assert call["thinking"] == {"type": "adaptive"}
    assert call["output_config"]["effort"] == "medium"
    assert call["output_config"]["format"]["type"] == "json_schema"
    assert "temperature" not in call and "extra_body" not in call and "fallbacks" not in call
    assert logged[0]["kind"] == "interviewer"
    assert "base64" not in str(logged[0]["request"])


def test_dynamic_text_carries_wrap_up_and_rejection():
    client = FakeAnthropic(interviewer=[FakeResponse(turn_payload())])
    InterviewerLLM(AnthropicBackend(client, TEST_MODELS.interviewer), lambda r: None, "S").next_turn(request(wrap_up=True, rejection="contract: bad anchor"))
    last_block = client.calls[0]["messages"][0]["content"][-1]["text"]
    assert "Less than two minutes remain" in last_block
    assert "contract: bad anchor" in last_block
    assert "A1/checks" in last_block


def test_static_blocks_are_cached():
    client = FakeAnthropic(interviewer=[FakeResponse(turn_payload())])
    InterviewerLLM(AnthropicBackend(client, TEST_MODELS.interviewer), lambda r: None, "S").next_turn(request())
    content = client.calls[0]["messages"][0]["content"]
    assert content[-2].get("cache_control") == {"type": "ephemeral"}
    assert "cache_control" not in content[-1]


def test_refusal_raises():
    client = FakeAnthropic(interviewer=[FakeResponse(None, stop_reason="refusal")])
    with pytest.raises(LLMRefused):
        InterviewerLLM(AnthropicBackend(client, TEST_MODELS.interviewer), lambda r: None, "S").next_turn(request())


def test_api_error_raises_unavailable():
    err = anthropic.APIConnectionError(request=httpx2.Request("POST", "https://api.anthropic.com"))
    client = FakeAnthropic(interviewer=[err])
    with pytest.raises(LLMUnavailable):
        InterviewerLLM(AnthropicBackend(client, TEST_MODELS.interviewer), lambda r: None, "S").next_turn(request())


def test_invalid_json_raises_unavailable():
    client = FakeAnthropic(interviewer=[FakeResponse({"utterance": "q"})])
    with pytest.raises(LLMUnavailable):
        InterviewerLLM(AnthropicBackend(client, TEST_MODELS.interviewer), lambda r: None, "S").next_turn(request())


def test_guard_uses_haiku_at_temperature_zero():
    client = FakeAnthropic(guard=[FakeResponse({"flagged": True, "introduced": "units"})])
    verdict = Guard(AnthropicBackend(client, TEST_MODELS.guard), lambda r: None, "G").check("Did you check units?", "A1: ...", "I used energy.")
    assert verdict.flagged and verdict.introduced == "units"
    assert client.calls[0]["model"] == "claude-haiku-4-5"
    assert client.calls[0]["extra_body"] == {"temperature": 0}
    assert "temperature" not in client.calls[0]


def test_interviewer_over_openai_backend_validates_output():
    from fakes import FakeOpenAI, openai_response
    from probe_app.backends import OpenAICompatBackend
    from probe_app.config import RoleModel

    role = RoleModel(provider="openrouter", model="openai/x")
    ok = FakeOpenAI([openai_response(json.dumps(turn_payload()))])
    assert InterviewerLLM(OpenAICompatBackend(ok, role), lambda r: None, "S").next_turn(request()).stem_id == "cues"
    prose = FakeOpenAI([openai_response("Sure! Here's a question: what did you notice?")])
    with pytest.raises(LLMUnavailable):
        InterviewerLLM(OpenAICompatBackend(prose, role), lambda r: None, "S").next_turn(request())


def openai_guard(response) -> tuple[Guard, FakeOpenAI]:
    client = FakeOpenAI([response])
    return Guard(OpenAICompatBackend(client, RoleModel(provider="openai", model="m")), lambda r: None, "G"), client


def test_guard_over_openai_parses_the_verdict():
    guard, client = openai_guard(openai_response('{"flagged": true, "introduced": "units"}'))
    verdict = guard.check("Did you check units?", "A1: ...", "I used energy.")
    assert (verdict.flagged, verdict.introduced) == (True, "units")
    assert client.calls[0]["response_format"]["json_schema"]["name"] == "guard"


def test_guard_over_openai_prose_is_unavailable():
    guard, _ = openai_guard(openai_response("The question looks fine to me."))
    with pytest.raises(LLMUnavailable, match="validation"):
        guard.check("Did you check units?", "A1: ...", "I used energy.")
