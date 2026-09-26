import hashlib
import json
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path

INSTRUMENT_DIR = Path(__file__).resolve().parents[2]
PROMPTS_DIR = INSTRUMENT_DIR / "prompts"
PROBLEMS_PATH = INSTRUMENT_DIR / "problems" / "problems.json"
PREREG_PATH = INSTRUMENT_DIR / "prereg.json"

INTERVIEWER_MODEL = "claude-opus-5"
INTERVIEWER_EFFORT = "medium"
GUARD_MODEL = "claude-haiku-4-5"
TRANSCRIBER_MODEL = "scribe_v2"

CAP_S = 1200.0
WRAP_S = 1080.0


class ConfigMismatch(Exception):
    pass


@dataclass(frozen=True)
class FrozenConfig:
    interviewer_model: str
    interviewer_effort: str
    guard_model: str
    transcriber_model: str
    system_prompt_sha256: str
    stems_sha256: str
    guard_prompt_sha256: str


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def current_config(prompts_dir: Path = PROMPTS_DIR) -> FrozenConfig:
    return FrozenConfig(
        interviewer_model=INTERVIEWER_MODEL,
        interviewer_effort=INTERVIEWER_EFFORT,
        guard_model=GUARD_MODEL,
        transcriber_model=TRANSCRIBER_MODEL,
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
