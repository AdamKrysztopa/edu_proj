import json

import httpx2
import openai
import pytest

from fakes import TEST_MODELS, FakeAnthropic, FakeOpenAI, FakeResponse, openai_response
from probe_app.backends import (AnthropicBackend, LLMRefused, LLMUnavailable, OpenAICompatBackend, Part,
                                make_backend, make_backends)
from probe_app.config import RoleModel

PNG = bytes.fromhex("89504e470d0a1a0a")
SCHEMA = {"type": "object", "additionalProperties": False, "required": ["a"], "properties": {"a": {"type": "string"}}}
PARTS = [Part(text="static"), Part(png=PNG, name="A1", cache=True), Part(text="dynamic")]


def oa(provider="openai", **kw) -> OpenAICompatBackend:
    return OpenAICompatBackend(kw.pop("client"), RoleModel(provider=provider, model="m", **kw))


def test_openai_request_shape():
    client = FakeOpenAI([openai_response('{"a": "x"}')])
    logged = []
    text = oa(client=client, effort="high").complete("interviewer", "SYS", PARTS, SCHEMA, 500, logged.append)
    assert text == '{"a": "x"}'
    call = client.calls[0]
    assert call["messages"][0] == {"role": "system", "content": "SYS"}
    image = call["messages"][1]["content"][1]
    assert image["type"] == "image_url" and image["image_url"]["url"].startswith("data:image/png;base64,")
    assert call["response_format"]["json_schema"]["strict"] is True
    assert call["max_completion_tokens"] == 500 and "max_tokens" not in call
    assert call["reasoning_effort"] == "high"
    assert "temperature" not in call
    assert "base64" not in json.dumps(logged[0]["request"])


def test_openrouter_uses_its_own_token_and_reasoning_fields():
    client = FakeOpenAI([openai_response("ok")])
    oa("openrouter", client=client, effort="low", temperature=0).complete("guard", "S", [Part(text="t")], None, 50,
                                                                          lambda r: None)
    call = client.calls[0]
    assert call["max_tokens"] == 50 and "max_completion_tokens" not in call
    assert call["extra_body"] == {"reasoning": {"effort": "low"},
                                  "provider": {"require_parameters": True, "data_collection": "deny"}}
    assert call["temperature"] == 0
    assert "response_format" not in call


def test_openrouter_route_pins_the_upstream_without_fallbacks():
    client = FakeOpenAI([openai_response("ok")])
    oa("openrouter", client=client, route=["anthropic", "google-vertex"]).complete(
        "guard", "S", [Part(text="t")], None, 50, lambda r: None)
    assert client.calls[0]["extra_body"] == {"provider": {
        "require_parameters": True, "data_collection": "deny",
        "order": ["anthropic", "google-vertex"], "allow_fallbacks": False}}


def test_openai_sends_no_openrouter_routing():
    client = FakeOpenAI([openai_response("ok")])
    oa(client=client).complete("guard", "S", [Part(text="t")], None, 50, lambda r: None)
    assert "extra_body" not in client.calls[0]


@pytest.mark.parametrize("response, exc", [
    (openai_response(None, refusal="I can't help with that."), LLMRefused),
    (openai_response("", finish_reason="content_filter"), LLMRefused),
    (openai_response('{"a": "tr', finish_reason="length"), LLMUnavailable),
    (openai_response(None), LLMUnavailable),
])
def test_openai_outcomes_map_to_the_two_exceptions(response, exc):
    with pytest.raises(exc):
        oa(client=FakeOpenAI([response])).complete("interviewer", "S", PARTS, SCHEMA, 10, lambda r: None)


def test_openai_empty_choices_is_unavailable():
    empty = openai_response("x")
    empty.choices = []
    with pytest.raises(LLMUnavailable):
        oa(client=FakeOpenAI([empty])).complete("interviewer", "S", PARTS, SCHEMA, 10, lambda r: None)


def test_openai_api_error_is_unavailable_and_logged():
    err = openai.APIConnectionError(request=httpx2.Request("POST", "https://api.openai.com"))
    logged = []
    with pytest.raises(LLMUnavailable):
        oa(client=FakeOpenAI([err])).complete("interviewer", "S", PARTS, SCHEMA, 10, logged.append)
    assert "error" in logged[0]


def test_anthropic_sends_temperature_only_when_configured():
    client = FakeAnthropic(interviewer=[FakeResponse({"a": "x"})], guard=[FakeResponse({"a": "y"})])
    AnthropicBackend(client, TEST_MODELS.interviewer).complete("interviewer", "S", PARTS, SCHEMA, 10, lambda r: None)
    AnthropicBackend(client, TEST_MODELS.guard).complete("guard", "S", [Part(text="t")], SCHEMA, 10, lambda r: None)
    assert "extra_body" not in client.calls[0]
    assert client.calls[1]["extra_body"] == {"temperature": 0}


def test_make_backend_names_the_missing_key():
    role = RoleModel(provider="openrouter", model="openai/x")
    with pytest.raises(ValueError, match="OPENROUTER_API_KEY"):
        make_backend("interviewer", role, env={})


def test_make_backends_picks_backend_per_provider():
    env = {"ANTHROPIC_API_KEY": "a", "OPENROUTER_API_KEY": "o"}
    models = TEST_MODELS.model_copy(update={"interviewer": RoleModel(provider="openrouter", model="openai/x")})
    b = make_backends(models, env)
    assert isinstance(b.interviewer, OpenAICompatBackend) and isinstance(b.guard, AnthropicBackend)
    assert str(b.interviewer.client.base_url).startswith("https://openrouter.ai/api/v1")
