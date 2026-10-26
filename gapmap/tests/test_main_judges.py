"""The gap-map CLI's selectable closure judge (D1b, 2026-10-26): an Ollama model other than the
default, or an OpenAI model with a hard cap; ADR 0009's parallel-arm rule enforced before any call;
replay with no flag stays exactly as before. A fake transport stands in for the network."""
import json

import pytest
from test_judge_openai import FakePost
from test_main import _fixture_ledger

from gapmap import __main__ as cli
from gapmap import config, judge as judge_mod

_SIDECAR = {"config": {"models": {"extractor": {"family": "anthropic"}, "verifier": {"family": "openai"}}}}


def _args(tmp_path, out="out", sidecar=True):
    (tmp_path / "ledger.json").write_text(_fixture_ledger().to_json())
    args = ["--ledger", str(tmp_path / "ledger.json"), "--domain", "test", "--out", str(tmp_path / out)]
    if sidecar:
        (tmp_path / "sidecar.json").write_text(json.dumps(_SIDECAR))
        args += ["--sidecar", str(tmp_path / "sidecar.json")]
    return args


class FakeOllama:
    def __init__(self, url=config.JUDGE_URL, model=config.JUDGE_MODEL):
        self.model_id = model

    def ask(self, prompt):
        return {"states": [], "partially": [], "reason": "fake"}


def _local_arm(tmp_path, monkeypatch, model="gemma3:12b"):
    monkeypatch.setattr(judge_mod, "OllamaJudge", FakeOllama)
    cli.main([*_args(tmp_path, out="local"), "--judge", "ollama", "--model", model])
    return tmp_path / "local"


def test_a_live_ollama_run_uses_the_named_model_and_records_it(tmp_path, monkeypatch):
    out = _local_arm(tmp_path, monkeypatch)
    rec = json.loads((out / "judge.json").read_text())
    assert rec["judge_model"] == "gemma3:12b"
    assert rec["ledger_sha256"] == json.loads((out / "gapmap.json").read_text())["ledger_sha256"]


def test_replay_with_no_flag_writes_no_judge_record(tmp_path, monkeypatch):
    out = _local_arm(tmp_path, monkeypatch, model=config.JUDGE_MODEL)
    before = (out / "gapmap.json").read_bytes()
    (out / "judge.json").unlink()
    cli.main(_args(tmp_path, out="local"))
    assert (out / "gapmap.json").read_bytes() == before
    assert not (out / "judge.json").exists()


def test_the_openai_judge_needs_a_max_usd(tmp_path):
    with pytest.raises(SystemExit):
        cli.main([*_args(tmp_path), "--judge", "openai", "--model", "gpt-6.1-sol"])


def test_a_same_family_live_judge_is_refused_without_a_parallel_arm(tmp_path, monkeypatch, capsys):
    post = FakePost()
    monkeypatch.setattr(judge_mod, "_http_post", post)
    with pytest.raises(SystemExit):
        cli.main([*_args(tmp_path), "--judge", "openai", "--model", "gpt-6.1-sol", "--max-usd", "1"])
    assert "--parallel-arm" in capsys.readouterr().err
    assert post.bodies == []
    assert not (tmp_path / "out" / "closure_judgements.json").exists()


def test_a_same_family_live_judge_needs_a_sidecar(tmp_path, capsys):
    with pytest.raises(SystemExit):
        cli.main([*_args(tmp_path, sidecar=False), "--judge", "openai", "--model", "gpt-6.1-sol",
                  "--max-usd", "1"])
    assert "--sidecar" in capsys.readouterr().err


def test_the_parallel_arm_must_be_other_family_and_on_the_same_ledger(tmp_path, monkeypatch, capsys):
    arm = _local_arm(tmp_path, monkeypatch)
    rec = json.loads((arm / "judge.json").read_text())
    (arm / "judge.json").write_text(json.dumps({**rec, "judge_model": "gpt-5.6-luna"}))
    monkeypatch.setattr(judge_mod, "_http_post", FakePost())
    with pytest.raises(SystemExit):
        cli.main([*_args(tmp_path), "--judge", "openai", "--model", "gpt-6.1-sol", "--max-usd", "1",
                  "--parallel-arm", str(arm)])
    assert "other-family" in capsys.readouterr().err

    (arm / "judge.json").write_text(json.dumps({**rec, "ledger_sha256": "other"}))
    with pytest.raises(SystemExit):
        cli.main([*_args(tmp_path), "--judge", "openai", "--model", "gpt-6.1-sol", "--max-usd", "1",
                  "--parallel-arm", str(arm)])
    assert "different ledger" in capsys.readouterr().err


def test_beside_an_other_family_arm_the_openai_judge_runs_capped_and_replays(tmp_path, monkeypatch):
    arm = _local_arm(tmp_path, monkeypatch)
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    post = FakePost(content='{"states": [], "partially": [], "reason": "r"}')
    monkeypatch.setattr(judge_mod, "_http_post", post)
    spend = tmp_path / "spend.jsonl"
    cli.main([*_args(tmp_path), "--judge", "openai", "--model", "gpt-6.1-sol", "--reasoning-effort", "high",
              "--max-usd", "5", "--spend-ledger", str(spend), "--parallel-arm", str(arm)])
    out = tmp_path / "out"
    rec = json.loads((out / "judge.json").read_text())
    assert rec["judge_model"] == "gpt-6.1-sol" and rec["complete"] is True
    assert rec["settings"]["reasoning_effort"] == "high"
    assert rec["spend"]["calls"] == len(post.bodies) > 0
    assert len(spend.read_text().splitlines()) == len(post.bodies)
    first = (out / "gapmap.json").read_bytes()

    monkeypatch.setattr(judge_mod, "_http_post", None)
    cli.main([*_args(tmp_path), "--model", "gpt-6.1-sol", "--reasoning-effort", "high"])
    assert (out / "gapmap.json").read_bytes() == first


def test_a_replay_cache_miss_names_judge_openai_for_an_openai_model(tmp_path):
    with pytest.raises(judge_mod.JudgeCacheMiss, match="--judge openai"):
        cli.main([*_args(tmp_path), "--model", "gpt-6.1-sol"])


def test_a_budget_stop_saves_the_cache_and_marks_the_run_incomplete(tmp_path, monkeypatch):
    arm = _local_arm(tmp_path, monkeypatch)
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    monkeypatch.setattr(judge_mod, "_http_post", FakePost())
    with pytest.raises(SystemExit):
        cli.main([*_args(tmp_path), "--judge", "openai", "--model", "gpt-6.1-sol", "--max-usd", "0.00001",
                  "--parallel-arm", str(arm)])
    rec = json.loads((tmp_path / "out" / "judge.json").read_text())
    assert rec["complete"] is False and "stopped" in rec
    assert not (tmp_path / "out" / "gapmap.json").exists()
