import hashlib
import json
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

INSTRUMENT_DIR = Path(__file__).resolve().parents[2]
PROMPTS_DIR = INSTRUMENT_DIR / "prompts"
PROBLEMS_PATH = INSTRUMENT_DIR / "problems" / "problems.json"
PREREG_PATH = INSTRUMENT_DIR / "prereg.json"
MODELS_PATH = INSTRUMENT_DIR / "models.json"

CAP_S = 1200.0
WRAP_S = 1080.0


class ConfigMismatch(Exception):
    pass


class RoleModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    provider: Literal["anthropic", "openai", "openrouter"]
    model: str
    effort: str | None = None
    temperature: float | None = None
    route: list[str] | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def _provider_accepts_settings(self) -> "RoleModel":
        if self.route is not None and self.provider != "openrouter":
            raise ValueError("route names OpenRouter upstream providers; it needs provider openrouter")
        if self.provider == "openai" and self.effort is not None and self.temperature is not None:
            raise ValueError("OpenAI reasoning models reject temperature: set effort or temperature, not both")
        return self


class TranscriberModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    model: str


class Models(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    interviewer: RoleModel
    guard: RoleModel
    simulated_expert: RoleModel
    transcriber: TranscriberModel


def load_models(path: Path | None = None) -> Models:
    path = path or MODELS_PATH
    try:
        return Models.model_validate_json(path.read_text())
    except ValidationError as e:
        raise ConfigMismatch(f"{path.name} is invalid: {e}") from e


@dataclass(frozen=True)
class FrozenConfig:
    interviewer_provider: str
    interviewer_model: str
    interviewer_effort: str | None
    interviewer_temperature: float | None
    interviewer_route: list[str] | None
    guard_provider: str
    guard_model: str
    guard_effort: str | None
    guard_temperature: float | None
    guard_route: list[str] | None
    transcriber_model: str
    system_prompt_sha256: str
    stems_sha256: str
    guard_prompt_sha256: str


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def current_config(prompts_dir: Path = PROMPTS_DIR, models_path: Path | None = None) -> FrozenConfig:
    m = load_models(models_path)
    return FrozenConfig(
        interviewer_provider=m.interviewer.provider,
        interviewer_model=m.interviewer.model,
        interviewer_effort=m.interviewer.effort,
        interviewer_temperature=m.interviewer.temperature,
        interviewer_route=m.interviewer.route,
        guard_provider=m.guard.provider,
        guard_model=m.guard.model,
        guard_effort=m.guard.effort,
        guard_temperature=m.guard.temperature,
        guard_route=m.guard.route,
        transcriber_model=m.transcriber.model,
        system_prompt_sha256=sha256_file(prompts_dir / "interviewer_system.md"),
        stems_sha256=sha256_file(prompts_dir / "stems.json"),
        guard_prompt_sha256=sha256_file(prompts_dir / "guard_system.md"),
    )


def check_preregistered(cfg: FrozenConfig, prereg_path: Path = PREREG_PATH) -> None:
    if not prereg_path.exists():
        raise ConfigMismatch(f"{prereg_path} is missing: run `probe-app freeze` before data sessions")
    registered = json.loads(prereg_path.read_text())
    diffs = {k: {"registered": registered.get(k), "current": v}
             for k, v in asdict(cfg).items() if registered.get(k) != v}
    if diffs:
        raise ConfigMismatch(f"frozen config differs from pre-registration: {diffs}")


def freeze(cfg: FrozenConfig, prereg_path: Path = PREREG_PATH) -> None:
    prereg_path.write_text(json.dumps(asdict(cfg), indent=2) + "\n")


def load_prompt(name: str, prompts_dir: Path = PROMPTS_DIR) -> str:
    return (prompts_dir / name).read_text()


def load_stems(prompts_dir: Path = PROMPTS_DIR) -> dict[str, str]:
    return json.loads((prompts_dir / "stems.json").read_text())


def load_problems(path: Path = PROBLEMS_PATH) -> dict:
    return json.loads(path.read_text())


def git_commit() -> str:
    out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=INSTRUMENT_DIR,
                         capture_output=True, text=True)
    return out.stdout.strip() or "unknown"


def git_dirty() -> bool:
    out = subprocess.run(["git", "status", "--porcelain", "--", "."], cwd=INSTRUMENT_DIR,
                         capture_output=True, text=True)
    return bool(out.stdout.strip())
