import json

import pytest

from probe_app import cli, config


def test_freeze_writes_prereg(tmp_path, monkeypatch):
    target = tmp_path / "prereg.json"
    monkeypatch.setattr(cli, "PREREG_PATH", target)
    cli.main(["freeze"])
    assert json.loads(target.read_text())["interviewer_model"] == config.load_models().interviewer.model


def test_hashes_prints_config(capsys):
    cli.main(["hashes"])
    assert "system_prompt_sha256" in capsys.readouterr().out


def test_serve_stops_before_starting_without_a_key(monkeypatch):
    import uvicorn

    monkeypatch.setattr(cli, "load_dotenv", lambda *a, **k: None)
    for key in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "OPENROUTER_API_KEY"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setattr(uvicorn, "run", lambda *a, **k: pytest.fail("server started without a key"))
    with pytest.raises(ValueError, match="_API_KEY"):
        cli.main(["serve"])
