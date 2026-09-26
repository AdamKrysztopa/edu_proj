import shutil
from pathlib import Path

import pytest

from probe_app import config


@pytest.fixture
def prompts(tmp_path: Path) -> Path:
    d = tmp_path / "prompts"
    shutil.copytree(config.PROMPTS_DIR, d)
    return d


def test_current_config_hashes_prompt_files(prompts):
    cfg = config.current_config(prompts)
    assert cfg.interviewer_model == "claude-opus-5"
    assert cfg.guard_model == "claude-haiku-4-5"
    assert cfg.system_prompt_sha256 == config.sha256_file(prompts / "interviewer_system.md")


def test_hash_changes_when_prompt_changes(prompts):
    before = config.current_config(prompts)
    (prompts / "stems.json").write_text('{"cues": "changed"}')
    assert config.current_config(prompts).stems_sha256 != before.stems_sha256


def test_check_passes_on_match(prompts, tmp_path):
    cfg = config.current_config(prompts)
    prereg = tmp_path / "prereg.json"
    config.freeze(cfg, prereg)
    config.check_preregistered(cfg, prereg)


def test_check_raises_on_mismatch(prompts, tmp_path):
    prereg = tmp_path / "prereg.json"
    config.freeze(config.current_config(prompts), prereg)
    (prompts / "guard_system.md").write_text("edited")
    with pytest.raises(config.ConfigMismatch, match="guard_prompt_sha256"):
        config.check_preregistered(config.current_config(prompts), prereg)


def test_check_raises_when_not_frozen(prompts, tmp_path):
    with pytest.raises(config.ConfigMismatch, match="freeze"):
        config.check_preregistered(config.current_config(prompts), tmp_path / "missing.json")


def test_loaders():
    assert list(config.load_stems()) == ["cues", "alternatives", "checks", "anomalies", "novice_miss"]
    problems = config.load_problems()
    assert problems["sets"]["A"] == ["A1", "A2"]
    assert "statement" in problems["problems"]["B2"]
