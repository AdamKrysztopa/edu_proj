import json
from dataclasses import dataclass
from pathlib import Path

from probe_app.session import SessionState


class SimulatedSession(Exception):
    pass


@dataclass
class LoadedSession:
    session_id: str
    dir: Path
    manifest: dict
    state: SessionState


def load_session(path: Path, allow_simulated: bool = False) -> LoadedSession:
    path = Path(path)
    manifest = json.loads((path / "manifest.json").read_text())
    if manifest.get("simulated") and not allow_simulated:
        raise SimulatedSession(f"{path.name} is a simulated session; pass --allow-simulated to include it")
    state = SessionState.model_validate_json((path / "state.json").read_text())
    return LoadedSession(path.name, path, manifest, state)
