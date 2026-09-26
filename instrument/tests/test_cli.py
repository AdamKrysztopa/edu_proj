import json

from probe_app import cli, config


def test_freeze_writes_prereg(tmp_path, monkeypatch):
    target = tmp_path / "prereg.json"
    monkeypatch.setattr(cli, "PREREG_PATH", target)
    cli.main(["freeze"])
    assert json.loads(target.read_text())["interviewer_model"] == config.INTERVIEWER_MODEL


def test_hashes_prints_config(capsys):
    cli.main(["hashes"])
    assert "system_prompt_sha256" in capsys.readouterr().out
