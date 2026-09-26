import json
import os
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Protocol

SUBDIRS = ("audio", "canvas/snapshots", "transcripts", "llm")


class Clock(Protocol):
    def now(self) -> float: ...


class MonotonicClock:
    def now(self) -> float:
        return time.monotonic()


class SessionStore:
    def __init__(self, root: Path, session_id: str, clock: Clock | None = None):
        self.session_id = session_id
        self.dir = Path(root) / session_id
        self.clock = clock or MonotonicClock()

    @classmethod
    def create(cls, root: Path, manifest: dict, clock: Clock | None = None) -> "SessionStore":
        session_id = f"{manifest['expert_id']}-{uuid.uuid4().hex[:8]}"
        store = cls(root, session_id, clock)
        store.dir.mkdir(parents=True, exist_ok=False)
        for sub in SUBDIRS:
            (store.dir / sub).mkdir(parents=True)
        store.write_json("manifest.json", manifest)
        return store

    @property
    def manifest(self) -> dict:
        return self.read_json("manifest.json")

    def path(self, rel: str) -> Path:
        return self.dir / rel

    def log(self, type_: str, **data) -> dict:
        event = {"type": type_, "t_mono": self.clock.now(),
                 "t_wall": datetime.now(timezone.utc).isoformat(), **data}
        with self.path("events.jsonl").open("a") as f:
            f.write(json.dumps(event) + "\n")
        return event

    def events(self) -> list[dict]:
        p = self.path("events.jsonl")
        return [json.loads(line) for line in p.read_text().splitlines()] if p.exists() else []

    def write_json(self, rel: str, obj) -> None:
        target = self.path(rel)
        tmp = target.with_name(target.name + ".tmp")
        tmp.write_text(json.dumps(obj, indent=2))
        os.replace(tmp, target)

    def read_json(self, rel: str):
        return json.loads(self.path(rel).read_text())

    def log_llm(self, record: dict) -> Path:
        n = len(list(self.path("llm").glob("*.json"))) + 1
        target = self.path(f"llm/{n:04d}.json")
        target.write_text(json.dumps(record, indent=2))
        return target
