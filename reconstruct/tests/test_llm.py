import json
import os
from datetime import date, datetime
from types import SimpleNamespace

import httpx
import openai
import pytest

from reconstruct.llm import (
    Budget,
    BudgetExceeded,
    CallLog,
    ConfigError,
    Hit,
    LLMRefused,
    LLMUnavailable,
    Model,
    OpenRouterBackend,
    SearchResult,
    ServedModelMismatch,
    load_models,
    web_search,
)
from residual.provenance import Agent


def ns(**kw):
    return SimpleNamespace(**kw)


class FakeOpenAIClient:
    def __init__(self, response):
        self.response = response
        self.calls: list[dict] = []
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

    def _create(self, **kwargs):
        self.calls.append(kwargs)
        return self.response


def make_backend(client, model_id="anthropic/claude-sonnet-5", family="anthropic", role="planner",
                  log=None, tmp_path=None):
    log = log or CallLog(tmp_path / "calls.jsonl")
    return OpenRouterBackend(client=client, model_id=model_id, family=family, role=role, log=log)


class QueueOpenAIClient:
    """Like FakeOpenAIClient, but `_create` pops one item per call — a response object is
    returned as-is, a BaseException instance is raised — so a test can script a transient
    failure followed by a success (or a run of permanent failures)."""

    def __init__(self, items):
        self._items = list(items)
        self.calls: list[dict] = []
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

    def _create(self, **kwargs):
        self.calls.append(kwargs)
        item = self._items.pop(0)
        if isinstance(item, BaseException):
            raise item
        return item


def _api_error(cls, status: int, message: str = "error"):
    request = httpx.Request("POST", "https://openrouter.ai/api/v1/chat/completions")
    if cls in (openai.APIConnectionError, openai.APITimeoutError):
        return cls(request=request)
    response = httpx.Response(status, request=request, json={"error": message})
    return cls(message, response=response, body=None)


def _ok_response(answer=1):
    return ns(choices=[ns(message=ns(content=json.dumps({"answer": answer}), refusal=None),
                          finish_reason="stop")],
              model="anthropic/claude-sonnet-5", usage=ns(prompt_tokens=1, completion_tokens=1, cost=0.001))


class RecordingSleep:
    def __init__(self):
        self.calls: list[float] = []

    def __call__(self, seconds: float) -> None:
        self.calls.append(seconds)


# --- D1: retry transient provider errors, log every failed attempt ----------------------------

def test_backend_retries_429_then_succeeds(tmp_path):
    log = CallLog(tmp_path / "calls.jsonl")
    client = QueueOpenAIClient([_api_error(openai.RateLimitError, 429), _ok_response(42)])
    backend = make_backend(client, log=log)
    sleeper = RecordingSleep()
    backend.sleep = sleeper

    data = backend.complete_json("plan", "sys", "usr", {"type": "object"})

    assert data == {"answer": 42}
    assert len(client.calls) == 2
    assert sleeper.calls == [1.0]

    lines = [json.loads(line) for line in (tmp_path / "calls.jsonl").read_text().splitlines()]
    assert [line["outcome"] for line in lines] == ["api_error", "ok"]
    assert lines[0]["task"] == "plan"
    assert lines[0]["error_class"] == "RateLimitError"
    assert lines[0]["http_status"] == 429
    assert lines[0]["cost"] is None
    assert lines[1]["cost"] == 0.001


def test_backend_permanent_500_exhausts_retries_then_raises(tmp_path):
    log = CallLog(tmp_path / "calls.jsonl")
    errors = [_api_error(openai.InternalServerError, 500) for _ in range(4)]
    client = QueueOpenAIClient(errors)
    backend = make_backend(client, log=log)
    sleeper = RecordingSleep()
    backend.sleep = sleeper

    with pytest.raises(LLMUnavailable):
        backend.complete_json("verify", "sys", "usr", {"type": "object"})

    assert len(client.calls) == 4, "1 initial attempt + 3 retries"
    assert sleeper.calls == [1.0, 2.0, 4.0]

    lines = [json.loads(line) for line in (tmp_path / "calls.jsonl").read_text().splitlines()]
    assert len(lines) == 4
    assert all(line["outcome"] == "api_error" for line in lines)
    assert all(line["error_class"] == "InternalServerError" for line in lines)
    assert all(line["http_status"] == 500 for line in lines)
    assert all(line["cost"] is None for line in lines)


def test_backend_400_is_not_retried_but_is_logged(tmp_path):
    log = CallLog(tmp_path / "calls.jsonl")
    client = QueueOpenAIClient([_api_error(openai.BadRequestError, 400)])
    backend = make_backend(client, log=log)
    sleeper = RecordingSleep()
    backend.sleep = sleeper

    with pytest.raises(LLMUnavailable):
        backend.complete_json("extract", "sys", "usr", {"type": "object"})

    assert len(client.calls) == 1
    assert sleeper.calls == []

    lines = [json.loads(line) for line in (tmp_path / "calls.jsonl").read_text().splitlines()]
    assert len(lines) == 1
    assert lines[0]["outcome"] == "api_error"
    assert lines[0]["error_class"] == "BadRequestError"
    assert lines[0]["http_status"] == 400


def test_budget_blocks_a_retry_between_attempts(tmp_path):
    """The budget check runs before every attempt, not just the first: if the running total
    crosses the cap during the backoff wait (here simulated by the injected sleep itself, standing
    in for cost spent concurrently by another role), the retry never dispatches."""
    log = CallLog(tmp_path / "calls.jsonl", budget=Budget(max_usd=1.0))
    client = QueueOpenAIClient([_api_error(openai.RateLimitError, 429), _ok_response(1)])
    backend = make_backend(client, log=log)

    def sleeper(seconds: float) -> None:
        log.total_cost = 1.0

    backend.sleep = sleeper

    with pytest.raises(BudgetExceeded):
        backend.complete_json("verify", "sys", "usr", {"type": "object"})

    assert len(client.calls) == 1, "the retry must never reach the client once the budget is spent"


def test_backend_records_no_api_error_line_on_first_try_success(tmp_path):
    log = CallLog(tmp_path / "calls.jsonl")
    client = QueueOpenAIClient([_ok_response(7)])
    backend = make_backend(client, log=log)
    backend.complete_json("plan", "sys", "usr", {"type": "object"})
    lines = [json.loads(line) for line in (tmp_path / "calls.jsonl").read_text().splitlines()]
    assert len(lines) == 1
    assert lines[0]["outcome"] == "ok"
    assert "error_class" not in lines[0]
    assert "http_status" not in lines[0]


# --- D1: search() gets the same retry/logging treatment ----------------------------------------

def test_search_retries_transient_error_then_succeeds(tmp_path):
    log = CallLog(tmp_path / "calls.jsonl")
    ok = ns(choices=[ns(message=ns(content="", annotations=[
        ns(type="url_citation", url_citation=ns(url="https://a.example/page", title="Page A")),
    ]), finish_reason="stop")], model="anthropic/claude-sonnet-5",
        usage=ns(prompt_tokens=1, completion_tokens=1, cost=0.002))
    client = QueueOpenAIClient([_api_error(openai.APIConnectionError, 0), ok])
    backend = make_backend(client, log=log)
    sleeper = RecordingSleep()
    backend.sleep = sleeper
    agent = Agent(kind="model", id="anthropic/claude-sonnet-5", family="anthropic")
    model = Model(agent=agent, backend=backend)

    result = web_search(model, "q", max_results=3)

    assert result.hits == (Hit(url="https://a.example/page", title="Page A"),)
    assert len(client.calls) == 2
    assert sleeper.calls == [1.0]
    lines = [json.loads(line) for line in (tmp_path / "calls.jsonl").read_text().splitlines()]
    assert [line["outcome"] for line in lines] == ["api_error", "ok"]
    assert lines[0]["task"] == "web_search"
    assert lines[0]["error_class"] == "APIConnectionError"


# --- Model.json / OpenRouterBackend.complete_json ---------------------------------------------

def test_backend_returns_parsed_json_object_and_logs_the_call(tmp_path):
    response = ns(
        choices=[ns(message=ns(content=json.dumps({"answer": 42}), refusal=None), finish_reason="stop")],
        model="anthropic/claude-sonnet-5",
        usage=ns(prompt_tokens=10, completion_tokens=5, cost=0.0012),
    )
    log = CallLog(tmp_path / "calls.jsonl")
    backend = make_backend(FakeOpenAIClient(response), log=log)
    agent = Agent(kind="model", id="anthropic/claude-sonnet-5", family="anthropic")
    model = Model(agent=agent, backend=backend)

    data = model.json("plan", system="sys", user="usr", schema={"type": "object"})

    assert data == {"answer": 42}
    lines = (tmp_path / "calls.jsonl").read_text().splitlines()
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert record["task"] == "plan"
    assert record["role"] == "planner"
    assert record["model"] == "anthropic/claude-sonnet-5"
    assert record["served_model"] == "anthropic/claude-sonnet-5"
    assert record["family"] == "anthropic"
    assert record["input_tokens"] == 10
    assert record["output_tokens"] == 5
    assert record["cost"] == 0.0012
    assert len(record["spec_sha256"]) == 64


def test_backend_raises_on_refusal(tmp_path):
    response = ns(choices=[ns(message=ns(content=None, refusal="policy"), finish_reason="stop")],
                  model="anthropic/claude-sonnet-5", usage=ns(prompt_tokens=1, completion_tokens=0))
    backend = make_backend(FakeOpenAIClient(response), tmp_path=tmp_path)
    with pytest.raises(LLMRefused):
        backend.complete_json("plan", "sys", "usr", {"type": "object"})


def test_backend_rejects_non_object_json(tmp_path):
    response = ns(choices=[ns(message=ns(content="[1, 2, 3]", refusal=None), finish_reason="stop")],
                  model="anthropic/claude-sonnet-5", usage=ns(prompt_tokens=1, completion_tokens=1))
    backend = make_backend(FakeOpenAIClient(response), tmp_path=tmp_path)
    with pytest.raises(LLMUnavailable):
        backend.complete_json("plan", "sys", "usr", {"type": "object"})


def test_backend_malformed_json_is_llm_unavailable_not_a_crash(tmp_path):
    """defect 2 (llm.py:131): a JSONDecodeError from json.loads must become LLMUnavailable,
    never propagate raw and kill the run."""
    response = ns(choices=[ns(message=ns(content="not json at all {", refusal=None), finish_reason="stop")],
                  model="anthropic/claude-sonnet-5", usage=ns(prompt_tokens=1, completion_tokens=1))
    backend = make_backend(FakeOpenAIClient(response), tmp_path=tmp_path)
    with pytest.raises(LLMUnavailable):
        backend.complete_json("plan", "sys", "usr", {"type": "object"})


def test_backend_logs_every_billed_outcome_with_its_cost(tmp_path):
    """defect 3 (llm.py:160-167): refusals, truncations and malformed JSON must still be logged
    (with their cost, so the budget accounts for them), not raised before log.append runs."""
    log = CallLog(tmp_path / "calls.jsonl")

    refusal = ns(choices=[ns(message=ns(content=None, refusal="policy"), finish_reason="stop")],
                 model="anthropic/claude-sonnet-5", usage=ns(prompt_tokens=1, completion_tokens=0, cost=0.01))
    backend = make_backend(FakeOpenAIClient(refusal), log=log)
    with pytest.raises(LLMRefused):
        backend.complete_json("plan", "sys", "usr", {"type": "object"})

    truncated = ns(choices=[ns(message=ns(content="{", refusal=None), finish_reason="length")],
                   model="anthropic/claude-sonnet-5", usage=ns(prompt_tokens=1, completion_tokens=1, cost=0.02))
    backend2 = make_backend(FakeOpenAIClient(truncated), log=log)
    with pytest.raises(LLMUnavailable):
        backend2.complete_json("plan", "sys", "usr", {"type": "object"})

    malformed = ns(choices=[ns(message=ns(content="{not json", refusal=None), finish_reason="stop")],
                   model="anthropic/claude-sonnet-5", usage=ns(prompt_tokens=1, completion_tokens=1, cost=0.03))
    backend3 = make_backend(FakeOpenAIClient(malformed), log=log)
    with pytest.raises(LLMUnavailable):
        backend3.complete_json("plan", "sys", "usr", {"type": "object"})

    lines = [json.loads(line) for line in (tmp_path / "calls.jsonl").read_text().splitlines()]
    assert [line["outcome"] for line in lines] == ["refusal", "truncated", "malformed_json"]
    assert log.total_cost == pytest.approx(0.06), "every billed outcome's cost must count against the budget"


def test_backend_served_model_mismatch_logs_then_raises(tmp_path):
    response = ns(choices=[ns(message=ns(content="{}", refusal=None), finish_reason="stop")],
                  model="anthropic/claude-sonnet-4-6", usage=ns(prompt_tokens=1, completion_tokens=1))
    log = CallLog(tmp_path / "calls.jsonl")
    backend = make_backend(FakeOpenAIClient(response), model_id="anthropic/claude-sonnet-5", log=log)

    with pytest.raises(ServedModelMismatch):
        backend.complete_json("plan", "sys", "usr", {"type": "object"})

    lines = (tmp_path / "calls.jsonl").read_text().splitlines()
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert record["model"] == "anthropic/claude-sonnet-5"
    assert record["served_model"] == "anthropic/claude-sonnet-4-6"


def test_backend_matching_served_model_returns_data(tmp_path):
    response = ns(
        choices=[ns(message=ns(content=json.dumps({"verdict": "supports"}), refusal=None), finish_reason="stop")],
        model="openai/gpt-5.5", usage=ns(prompt_tokens=3, completion_tokens=2))
    backend = make_backend(FakeOpenAIClient(response), model_id="openai/gpt-5.5", family="openai",
                            role="verifier", tmp_path=tmp_path)
    data = backend.complete_json("verify", "sys", "usr", {"type": "object"})
    assert data == {"verdict": "supports"}


# --- CallLog ------------------------------------------------------------------------------------

def test_call_log_line_shape(tmp_path):
    log = CallLog(tmp_path / "calls.jsonl")
    log.append(task="extract", role="extractor", model_id="anthropic/claude-sonnet-5", family="anthropic",
               served_model="anthropic/claude-sonnet-5", system="sys", user="usr",
               schema={"type": "object"}, input_tokens=7, output_tokens=3, cost=0.0005)
    lines = (tmp_path / "calls.jsonl").read_text().splitlines()
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert set(record) == {"task", "role", "model", "family", "served_model", "spec_sha256",
                            "input_tokens", "output_tokens", "cost", "outcome", "utc"}
    assert record["task"] == "extract"
    assert record["role"] == "extractor"
    assert record["model"] == "anthropic/claude-sonnet-5"
    assert record["family"] == "anthropic"
    assert record["served_model"] == "anthropic/claude-sonnet-5"
    assert record["input_tokens"] == 7
    assert record["output_tokens"] == 3
    assert record["cost"] == 0.0005
    assert record["outcome"] == "ok"
    datetime.fromisoformat(record["utc"])


def test_call_log_cost_defaults_to_none_when_not_given(tmp_path):
    log = CallLog(tmp_path / "calls.jsonl")
    log.append(task="t", role="r", model_id="m", family="f", served_model="m", system="s",
               user="u", schema={}, input_tokens=1, output_tokens=1)
    record = json.loads((tmp_path / "calls.jsonl").read_text().splitlines()[0])
    assert record["cost"] is None


def test_call_log_appends_one_line_per_call(tmp_path):
    log = CallLog(tmp_path / "calls.jsonl")
    for _ in range(3):
        log.append(task="t", role="r", model_id="m", family="f", served_model="m", system="s",
                    user="u", schema={}, input_tokens=1, output_tokens=1)
    assert len((tmp_path / "calls.jsonl").read_text().splitlines()) == 3


# --- web_search: OpenRouter web plugin (engine exa), url_citation annotations only ------------

def test_web_search_reads_only_url_citation_annotations(tmp_path):
    response = ns(
        choices=[ns(message=ns(
            content="This text must never be used as evidence.",
            annotations=[
                ns(type="url_citation", url_citation=ns(url="https://a.example/page", title="Page A")),
                ns(type="url_citation", url_citation=ns(url="https://b.example/page", title="Page B")),
                ns(type="something_else", other="ignored"),
            ],
        ), finish_reason="stop")],
        model="anthropic/claude-sonnet-5",
        usage=ns(prompt_tokens=20, completion_tokens=15, cost=0.01),
    )
    log = CallLog(tmp_path / "calls.jsonl")
    client = FakeOpenAIClient(response)
    backend = make_backend(client, log=log)
    agent = Agent(kind="model", id="anthropic/claude-sonnet-5", family="anthropic")
    model = Model(agent=agent, backend=backend)

    result = web_search(model, "pump cavitation diagnosis", max_results=5)

    assert isinstance(result, SearchResult)
    assert result.executed_query == "pump cavitation diagnosis"
    assert result.on == date.today()
    assert result.hits == (Hit(url="https://a.example/page", title="Page A"),
                            Hit(url="https://b.example/page", title="Page B"))

    sent = client.calls[0]
    assert sent["extra_body"]["plugins"] == [{"id": "web", "engine": "exa", "max_results": 5}]

    record = json.loads((tmp_path / "calls.jsonl").read_text().splitlines()[0])
    assert record["task"] == "web_search"
    assert record["cost"] == 0.01


def test_web_search_with_no_citations_returns_no_hits(tmp_path):
    response = ns(choices=[ns(message=ns(content="no hits", annotations=[]), finish_reason="stop")],
                  model="anthropic/claude-sonnet-5", usage=ns(prompt_tokens=1, completion_tokens=1))
    backend = make_backend(FakeOpenAIClient(response), tmp_path=tmp_path)
    agent = Agent(kind="model", id="anthropic/claude-sonnet-5", family="anthropic")
    model = Model(agent=agent, backend=backend)

    result = web_search(model, "an unanswerable query", max_results=3)
    assert result.hits == ()
    assert result.executed_query == "an unanswerable query"


def test_web_search_served_model_mismatch_raises(tmp_path):
    response = ns(choices=[ns(message=ns(content="", annotations=[]), finish_reason="stop")],
                  model="anthropic/claude-sonnet-4-6", usage=ns(prompt_tokens=1, completion_tokens=1))
    backend = make_backend(FakeOpenAIClient(response), model_id="anthropic/claude-sonnet-5", tmp_path=tmp_path)
    agent = Agent(kind="model", id="anthropic/claude-sonnet-5", family="anthropic")
    model = Model(agent=agent, backend=backend)
    with pytest.raises(ServedModelMismatch):
        web_search(model, "q", max_results=1)


# --- load_models / models.json validation -----------------------------------------------------

def write_models_json(tmp_path, config: dict) -> str:
    path = tmp_path / "models.json"
    path.write_text(json.dumps(config))
    return str(path)


def test_load_models_unknown_provider_fails(tmp_path):
    path = write_models_json(tmp_path, {
        "planner": {"provider": "anthropic", "model": "claude-sonnet-5", "family": "anthropic"},
    })
    with pytest.raises(ConfigError, match="unknown provider"):
        load_models(path, log=CallLog(tmp_path / "calls.jsonl"), env={}, client_factory=lambda p, k: None)


def test_load_models_openrouter_anthropic_slug_family_mismatch_fails(tmp_path):
    path = write_models_json(tmp_path, {
        "verifier": {"provider": "openrouter", "model": "anthropic/claude-sonnet-5", "family": "openai"},
    })
    with pytest.raises(ConfigError, match="slug prefix"):
        load_models(path, log=CallLog(tmp_path / "calls.jsonl"),
                     env={"OPENROUTER_API_KEY": "key"}, client_factory=lambda p, k: None)


def test_load_models_openrouter_auto_is_forbidden(tmp_path):
    path = write_models_json(tmp_path, {
        "verifier": {"provider": "openrouter", "model": "openrouter/auto", "family": "openrouter"},
    })
    with pytest.raises(ConfigError, match="forbidden"):
        load_models(path, log=CallLog(tmp_path / "calls.jsonl"),
                     env={"OPENROUTER_API_KEY": "key"}, client_factory=lambda p, k: None)


def test_load_models_rejects_fallback_models_list(tmp_path):
    path = write_models_json(tmp_path, {
        "verifier": {"provider": "openrouter", "model": "openai/gpt-5.5", "family": "openai",
                     "models": ["openai/gpt-5.6-terra", "google/gemini-3.5-flash"]},
    })
    with pytest.raises(ConfigError, match="fallback/models list"):
        load_models(path, log=CallLog(tmp_path / "calls.jsonl"),
                     env={"OPENROUTER_API_KEY": "key"}, client_factory=lambda p, k: None)


def test_load_models_missing_env_var_names_it(tmp_path):
    path = write_models_json(tmp_path, {
        "planner": {"provider": "openrouter", "model": "anthropic/claude-sonnet-5", "family": "anthropic"},
    })
    with pytest.raises(ConfigError, match="OPENROUTER_API_KEY"):
        load_models(path, log=CallLog(tmp_path / "calls.jsonl"), env={}, client_factory=lambda p, k: None)


def test_load_models_missing_env_var_fails_before_any_client_call(tmp_path):
    path = write_models_json(tmp_path, {
        "planner": {"provider": "openrouter", "model": "anthropic/claude-sonnet-5", "family": "anthropic"},
    })
    calls = []

    def factory(provider, key):
        calls.append((provider, key))
        return SimpleNamespace()

    with pytest.raises(ConfigError):
        load_models(path, log=CallLog(tmp_path / "calls.jsonl"), env={}, client_factory=factory)
    assert calls == []


def test_load_models_builds_agents_with_configured_family(tmp_path):
    path = write_models_json(tmp_path, {
        "planner": {"provider": "openrouter", "model": "anthropic/claude-sonnet-5", "family": "anthropic"},
        "verifier": {"provider": "openrouter", "model": "openai/gpt-5.5", "family": "openai"},
    })
    models = load_models(path, log=CallLog(tmp_path / "calls.jsonl"),
                          env={"OPENROUTER_API_KEY": "or-key"},
                          client_factory=lambda provider, key: SimpleNamespace(provider=provider, key=key))

    assert set(models) == {"planner", "verifier"}
    assert models["planner"].agent == Agent(kind="model", id="anthropic/claude-sonnet-5", family="anthropic")
    assert models["verifier"].agent == Agent(kind="model", id="openai/gpt-5.5", family="openai")
    assert isinstance(models["planner"].backend, OpenRouterBackend)
    assert isinstance(models["verifier"].backend, OpenRouterBackend)


def test_committed_models_json_loads(tmp_path):
    root = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(root, "models.json")
    models = load_models(path, log=CallLog(tmp_path / "calls.jsonl"),
                          env={"OPENROUTER_API_KEY": "or-key"},
                          client_factory=lambda provider, key: SimpleNamespace())
    assert set(models) == {"planner", "extractor", "baseline", "verifier"}
    assert models["planner"].agent.family == "anthropic"
    assert models["verifier"].agent.family == "openai"
    assert models["verifier"].agent.family != models["planner"].agent.family


# --- Budget: checked before every call, never after ---------------------------------------------

def test_call_log_accumulates_cost_across_calls(tmp_path):
    log = CallLog(tmp_path / "calls.jsonl")
    log.append(task="a", role="r", model_id="m", family="f", served_model="m", system="s",
               user="u", schema={}, input_tokens=1, output_tokens=1, cost=0.01)
    log.append(task="b", role="r", model_id="m", family="f", served_model="m", system="s",
               user="u", schema={}, input_tokens=1, output_tokens=1, cost=0.02)
    assert log.total_cost == pytest.approx(0.03)


def test_call_log_without_budget_never_raises(tmp_path):
    log = CallLog(tmp_path / "calls.jsonl")
    log.ensure_budget()
    log.append(task="a", role="r", model_id="m", family="f", served_model="m", system="s",
               user="u", schema={}, input_tokens=1, output_tokens=1, cost=1_000_000.0)
    log.ensure_budget()


def test_budget_check_raises_once_spent_reaches_max():
    budget = Budget(max_usd=0.05)
    budget.check(0.049)  # does not raise: still under budget
    with pytest.raises(BudgetExceeded):
        budget.check(0.05)
    with pytest.raises(BudgetExceeded):
        budget.check(0.06)


def test_budget_blocks_the_call_before_any_client_dispatch(tmp_path):
    response = ns(choices=[ns(message=ns(content="{}", refusal=None), finish_reason="stop")],
                  model="anthropic/claude-sonnet-5", usage=ns(prompt_tokens=1, completion_tokens=1, cost=0.02))
    log = CallLog(tmp_path / "calls.jsonl", budget=Budget(max_usd=0.05))
    client = FakeOpenAIClient(response)
    backend = make_backend(client, log=log)

    # First call spends 0.02, leaving the log under budget.
    backend.complete_json("t1", "sys", "usr", {"type": "object"})
    assert log.total_cost == pytest.approx(0.02)
    assert len(client.calls) == 1

    # Push the running total to the cap by hand (simulating prior spend elsewhere in the run).
    log.total_cost = 0.05
    with pytest.raises(BudgetExceeded):
        backend.complete_json("t2", "sys", "usr", {"type": "object"})
    # The budget check happens before dispatch: no second call reached the fake client.
    assert len(client.calls) == 1


def test_budget_blocks_web_search_before_dispatch(tmp_path):
    log = CallLog(tmp_path / "calls.jsonl", budget=Budget(max_usd=0.01))
    log.total_cost = 0.01
    response = ns(choices=[ns(message=ns(content="", annotations=[]), finish_reason="stop")],
                  model="anthropic/claude-sonnet-5", usage=ns(prompt_tokens=1, completion_tokens=1))
    client = FakeOpenAIClient(response)
    backend = make_backend(client, log=log)
    agent = Agent(kind="model", id="anthropic/claude-sonnet-5", family="anthropic")
    model = Model(agent=agent, backend=backend)

    with pytest.raises(BudgetExceeded):
        web_search(model, "q", max_results=1)
    assert len(client.calls) == 0
