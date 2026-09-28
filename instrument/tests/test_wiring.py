import json
from dataclasses import asdict

import pytest

from fakes import FakeAnthropic, FakeResponse, turn_payload
from probe_app import llm, session as session_module
from probe_app.backends import AnthropicBackend
from probe_app.config import MODEL_FACING_FILES, current_config, load_prompt
from probe_code import cli
from probe_code.export import read_csv
from test_baseline import answer, probe, write_events
from test_export import make_session
from test_llm import TEST_MODELS
from test_session import new_session, seg, through_think_aloud


@pytest.fixture(autouse=True)
def no_dotenv(monkeypatch):
    monkeypatch.setattr(cli, "load_dotenv", lambda *a, **k: None)
    monkeypatch.setattr(cli, "make_backend", lambda name, role, env=None: AnthropicBackend(FakeAnthropic(), TEST_MODELS.guard))


def _with_current_config(path):
    manifest = json.loads((path / "manifest.json").read_text())
    manifest["config"] = asdict(current_config())
    (path / "manifest.json").write_text(json.dumps(manifest))
    return path


def test_human_script_is_frozen():
    assert "human-script.md" in MODEL_FACING_FILES


def test_guard_audit_refuses_a_drifted_session(tmp_path):
    with pytest.raises(SystemExit, match="guard_prompt_sha256"):
        cli.main(["guard-audit", str(make_session(tmp_path, "E01")), "--out", str(tmp_path / "out")])


def test_guard_audit_runs_on_a_session_with_the_current_config(tmp_path):
    path = _with_current_config(make_session(tmp_path, "E01"))
    cli.main(["guard-audit", str(path), "--out", str(tmp_path / "out")])
    assert len(read_csv(tmp_path / "out" / "guard_audit.csv")) == 2


def test_factories_load_their_frozen_prompts():
    backend = AnthropicBackend(FakeAnthropic(), TEST_MODELS.guard)
    assert llm.make_guard(backend, print).system_prompt == load_prompt("guard_system.md")
    assert llm.make_interviewer(backend, print).system_prompt == load_prompt("interviewer_system.md")


def _spy(monkeypatch, module, name):
    calls, real = [], getattr(llm, name)
    monkeypatch.setattr(module, name, lambda backend, log: calls.append(backend) or real(backend, log))
    return calls


def test_guard_audit_builds_the_live_guard(tmp_path, monkeypatch):
    client = FakeAnthropic()
    monkeypatch.setattr(cli, "make_backend", lambda name, role, env=None: AnthropicBackend(client, role))
    built = _spy(monkeypatch, cli, "make_guard")
    path = _with_current_config(make_session(tmp_path, "E01"))
    cli.main(["guard-audit", str(path), "--out", str(tmp_path / "out")])
    assert len(built) == 1 and built[0].role == cli.load_models().guard
    assert client.calls and all(c["system"] == load_prompt("guard_system.md") for c in client.calls)


def test_session_builds_interviewer_and_guard_with_the_factories(tmp_path, monkeypatch):
    guards, interviewers = (_spy(monkeypatch, session_module, "make_guard"),
                            _spy(monkeypatch, session_module, "make_interviewer"))
    s = new_session(tmp_path, interviewer=[FakeResponse(turn_payload())],
                    transcripts=[seg("A1"), seg("A2"), seg("B1"), seg("B2")])
    through_think_aloud(s)
    s.start_probe()
    assert guards == [s.deps.backends.guard] and interviewers == [s.deps.backends.interviewer]


def test_export_leading_writes_items_and_key(tmp_path):
    cli.main(["export-leading", str(make_session(tmp_path, "E01")), "--out", str(tmp_path / "out"), "--seed", "1"])
    items, key = read_csv(tmp_path / "out" / "leading_items.csv"), read_csv(tmp_path / "out" / "key_leading.csv")
    assert len(items) == 2 and len(key) == 2
    assert "arm" not in items[0]


def test_leading_rates_prints_rate_per_arm(tmp_path, capsys):
    cli.main(["export-leading", str(make_session(tmp_path, "E01")), "--out", str(tmp_path / "out"), "--seed", "1"])
    items = read_csv(tmp_path / "out" / "leading_items.csv")
    labels = tmp_path / "labels.csv"
    labels.write_text("item_id,leading\n" + "".join(f"{r['item_id']},1\n" for r in items))
    cli.main(["leading-rates", str(labels), str(tmp_path / "out" / "key_leading.csv")])
    out = capsys.readouterr().out
    assert "ai: 1/1 leading" in out and "human: 1/1 leading" in out


def test_freeze_baseline_prints_pooled_metrics_and_the_rule_outcome(tmp_path, capsys):
    d = write_events(tmp_path / "SIM-1", [probe(1.0), answer(3.0), probe(5.0), answer(8.0)],
                     config=asdict(current_config()), simulated=True)
    cli.main(["freeze-baseline", str(d)])
    out = json.loads(capsys.readouterr().out)
    assert out["pooled"]["counts"]["delivered"] == 2
    assert out["decision"]["outcome"] in {"accept", "rerun", "change one variable", "change the model"}


def test_freeze_baseline_refuses_sessions_from_a_superseded_config(tmp_path):
    d = write_events(tmp_path / "SIM-1", [probe(1.0), answer(3.0)], config={"guard_model": "old"}, simulated=True)
    with pytest.raises(SystemExit, match="superseded"):
        cli.main(["freeze-baseline", str(d)])


def test_freeze_baseline_refuses_data_sessions(tmp_path):
    d = write_events(tmp_path / "E01-x", [probe(1.0), answer(3.0)], config=asdict(current_config()))
    with pytest.raises(SystemExit, match="E01-x"):
        cli.main(["freeze-baseline", str(d)])


def test_leading_ids_share_no_random_stream_with_blind_ids(tmp_path):
    s = make_session(tmp_path, "E01")
    cli.main(["export-blind", str(s), "--out", str(tmp_path / "blind"), "--seed", "0"])
    cli.main(["export-leading", str(s), "--out", str(tmp_path / "lead"), "--seed", "0"])
    blind = {r["blind_session"][1:] for r in read_csv(tmp_path / "blind" / "coder_units.csv")}
    leading = {r["item_id"][-8:] for r in read_csv(tmp_path / "lead" / "leading_items.csv")}
    assert not blind & leading
