import json
import re
import shutil
from pathlib import Path

import pytest

from probe_app import config


@pytest.fixture
def prompts(tmp_path: Path) -> Path:
    d = tmp_path / "prompts"
    shutil.copytree(config.PROMPTS_DIR, d)
    return d


MODELS = {
    "interviewer": {"provider": "anthropic", "model": "claude-opus-5", "effort": "medium"},
    "guard": {"provider": "anthropic", "model": "claude-haiku-4-5", "temperature": 0},
    "simulated_expert": {"provider": "anthropic", "model": "claude-sonnet-5", "effort": "low"},
    "transcriber": {"model": "scribe_v2"},
}


@pytest.fixture
def models(tmp_path: Path) -> Path:
    p = tmp_path / "models.json"
    p.write_text(json.dumps(MODELS))
    return p


def test_current_config_hashes_prompt_files(prompts, models):
    cfg = config.current_config(prompts, models)
    assert (cfg.interviewer_provider, cfg.interviewer_model, cfg.interviewer_effort) == ("anthropic", "claude-opus-5", "medium")
    assert (cfg.guard_provider, cfg.guard_model, cfg.guard_temperature) == ("anthropic", "claude-haiku-4-5", 0)
    assert cfg.transcriber_model == "scribe_v2"
    assert cfg.system_prompt_sha256 == config.sha256_file(prompts / "interviewer_system.md")


def test_committed_models_file_is_valid():
    config.load_models(config.INSTRUMENT_DIR / "models.json")


@pytest.mark.parametrize("bad", [
    {**MODELS, "interviewer": {"provider": "gemini", "model": "x"}},
    {k: v for k, v in MODELS.items() if k != "guard"},
    {**MODELS, "narrator": {"provider": "openai", "model": "x"}},
    {**MODELS, "interviewer": {"provider": "openai", "model": "x", "route": ["openai"]}},
    {**MODELS, "interviewer": {"provider": "openrouter", "model": "openai/x", "route": []}},
    {**MODELS, "interviewer": {"provider": "openai", "model": "x", "effort": "low", "temperature": 0}},
])
def test_invalid_models_file_is_refused(tmp_path, bad):
    p = tmp_path / "models.json"
    p.write_text(json.dumps(bad))
    with pytest.raises(config.ConfigMismatch, match="models.json"):
        config.load_models(p)


def test_route_is_accepted_for_openrouter(tmp_path):
    p = tmp_path / "models.json"
    p.write_text(json.dumps({**MODELS, "guard": {"provider": "openrouter", "model": "openai/x", "route": ["openai"]}}))
    assert config.current_config(models_path=p).guard_route == ["openai"]


def test_changing_the_interviewer_breaks_the_preregistration(prompts, models, tmp_path):
    prereg = tmp_path / "prereg.json"
    config.freeze(config.current_config(prompts, models), prereg)
    models.write_text(json.dumps({**MODELS, "interviewer": {"provider": "openrouter", "model": "openai/some-model"}}))
    with pytest.raises(config.ConfigMismatch, match="interviewer_provider"):
        config.check_preregistered(config.current_config(prompts, models), prereg)


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


OPENROUTER = {"provider": "openrouter", "model": "openai/x"}


@pytest.mark.parametrize("role, base, edit, frozen", [
    ("interviewer", {}, {"temperature": 0.7}, "interviewer_temperature"),
    ("guard", {}, {"effort": "high"}, "guard_effort"),
    ("interviewer", OPENROUTER, {"route": ["openai"]}, "interviewer_route"),
])
def test_editing_any_frozen_role_setting_breaks_the_preregistration(prompts, models, tmp_path, role, base, edit, frozen):
    prereg = tmp_path / "prereg.json"
    models.write_text(json.dumps({**MODELS, role: {**MODELS[role], **base}}))
    config.freeze(config.current_config(prompts, models), prereg)
    models.write_text(json.dumps({**MODELS, role: {**MODELS[role], **base, **edit}}))
    with pytest.raises(config.ConfigMismatch, match=frozen):
        config.check_preregistered(config.current_config(prompts, models), prereg)


def test_every_interviewer_and_guard_setting_is_frozen():
    frozen = set(config.FrozenConfig.__dataclass_fields__)
    missing = [f"{role}_{name}" for role in ("interviewer", "guard") for name in config.RoleModel.model_fields
               if f"{role}_{name}" not in frozen]
    assert missing == []


@pytest.fixture
def instrument_copy(tmp_path: Path) -> Path:
    d = tmp_path / "instrument"
    for rel in config.MODEL_FACING_FILES:
        (d / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(config.INSTRUMENT_DIR / rel, d / rel)
    return d


def test_model_facing_files_include_the_interviewer_and_guard_code():
    required = {f"src/probe_app/{m}.py" for m in ("llm", "engine", "contract", "models")}
    required |= {"src/probe_code/guard_audit.py", "src/probe_code/export.py"}
    assert required <= set(config.MODEL_FACING_FILES)
    assert all((config.INSTRUMENT_DIR / rel).is_file() for rel in config.MODEL_FACING_FILES)


@pytest.mark.parametrize("rel", ["src/probe_app/llm.py", "src/probe_app/engine.py", "src/probe_app/contract.py",
                                 "src/probe_app/models.py", "src/probe_app/human.py",
                                 "problems/problems.json"])
def test_editing_model_facing_code_breaks_the_preregistration(prompts, instrument_copy, tmp_path, rel):
    prereg = tmp_path / "prereg.json"
    config.freeze(config.current_config(prompts, instrument_dir=instrument_copy), prereg)
    config.check_preregistered(config.current_config(prompts, instrument_dir=instrument_copy), prereg)
    target = instrument_copy / rel
    target.write_bytes(target.read_bytes() + b"\n")
    with pytest.raises(config.ConfigMismatch, match=re.escape(rel)):
        config.check_preregistered(config.current_config(prompts, instrument_dir=instrument_copy), prereg)
