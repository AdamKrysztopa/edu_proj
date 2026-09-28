import json
import os
from datetime import date, datetime
from types import SimpleNamespace

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
                            "input_tokens", "output_tokens", "cost", "utc"}
    assert record["task"] == "extract"
    assert record["role"] == "extractor"
    assert record["model"] == "anthropic/claude-sonnet-5"
    assert record["family"] == "anthropic"
    assert record["served_model"] == "anthropic/claude-sonnet-5"
    assert record["input_tokens"] == 7
    assert record["output_tokens"] == 3
    assert record["cost"] == 0.0005
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
    assert set(models) == {"planner", "extractor", "baseline", "verifier", "contradiction"}
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
