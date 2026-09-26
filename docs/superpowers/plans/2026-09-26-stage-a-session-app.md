# Stage A Session App Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A local web app that records an expert's think-aloud physics solution and runs a capped, contract-enforced AI or human retrospective probe session over it, plus a CLI that turns sessions into blinded coding material and agreement statistics.

**Architecture:** A FastAPI server holds one `Session` state machine per expert session, persisted as `state.json` plus an append-only `events.jsonl`. The AI interviewer is a `ProbeEngine` that asks Claude for one structured turn at a time and accepts it only if the pure `contract` checks and a Haiku leading-question guard pass. Two static pages (researcher console, expert tablet) poll the server once a second. A separate `probe_code` package reads session directories and writes coder sheets.

**Tech Stack:** Python 3.12, uv, FastAPI, uvicorn, pydantic v2, anthropic SDK, elevenlabs SDK (Scribe v2 transcription), openai SDK (whisper-1, pilot comparison only), krippendorff, numpy, pytest; plain HTML/JS.

**Spec:** `docs/superpowers/specs/2026-09-26-stage-a-session-app-design.md`

## Global Constraints

- Interviewer model `claude-opus-5`, adaptive thinking, `output_config.effort` from `config.INTERVIEWER_EFFORT`; no `temperature` (current Opus models reject it).
- Guard model `claude-haiku-4-5`, `temperature=0`.
- No server-side model fallbacks on any request.
- Transcriber default ElevenLabs `scribe_v2` with physics `keyterms`, `timestamps_granularity="word"`, words grouped into segments; `whisper-1` (`verbose_json`, segment timestamps) is selectable for the pilot comparison. The transcriber model ID is part of the frozen config.
- Probe cap 1200 s per problem set; wrap-up instruction from 1080 s.
- Stems, exactly: `cues`, `alternatives`, `checks`, `anomalies`, `novice_miss`.
- A data session (non-pilot) refuses to start unless the current config equals `instrument/prereg.json`.
- `sessions/` and `instrument/.env` are git-ignored; no expert names anywhere in the repo.
- API keys come from the environment (`ANTHROPIC_API_KEY`, `ELEVEN_LABS_API_KEY`, `OPENAI_API_KEY`), loaded from `instrument/.env` by the CLI. The file already exists and is already git-ignored; never print or commit it. Tests never need keys.
- All commands run from `instrument/` unless stated.

## Review Focus

1. The expert answers with silence, so transcription returns no segments: the answer is recorded as empty text and the interview continues (Task 7).
2. A problem's think-aloud transcribes to nothing: the probe session still runs, with canvas or no anchors for that problem (Task 6).
3. The tablet browser reloads mid-probe: the server state is unchanged and the same question is shown again, with no duplicate turn (Task 7, Task 8).
4. The expert quotes use curly quotes, capitals or filler punctuation: a follow-up's `quoted_span` still matches after normalisation (Task 4).
5. The answer upload is sent twice (double tap, retry): the second is rejected with 409 and no turn is added (Task 7, Task 8).

---

## File Structure

```
.gitignore                                  add sessions/, instrument/.env, instrument/.venv
instrument/
  pyproject.toml
  prompts/interviewer_system.md             frozen interviewer prompt (hashed)
  prompts/guard_system.md                   frozen guard prompt (hashed)
  prompts/stems.json                        stem id → bare fallback wording (hashed)
  problems/problems.json                    pilot problem sets A, B
  problems/simulated_think_aloud.json       fixture transcripts for simulate
  src/probe_app/__init__.py
  src/probe_app/config.py                   constants, hashing, prereg check, loaders
  src/probe_app/models.py                   Segment, Anchor, InterviewerTurn, DialogueTurn, GuardVerdict
  src/probe_app/storage.py                  SessionStore, clocks
  src/probe_app/transcribe.py               Transcriber protocol, OpenAI impl, retry
  src/probe_app/trace.py                    segments, corrections, rendering
  src/probe_app/contract.py                 pure turn checks and coverage
  src/probe_app/llm.py                      InterviewerLLM, Guard (Claude calls)
  src/probe_app/engine.py                   ProbeEngine: generate → check → guard → fallback
  src/probe_app/human.py                    human-arm dialogue from turn markers
  src/probe_app/session.py                  Session state machine
  src/probe_app/server.py                   FastAPI app
  src/probe_app/simulate.py                 simulated expert run
  src/probe_app/cli.py                      probe-app serve|hashes|freeze|simulate
  src/probe_code/__init__.py
  src/probe_code/loader.py
  src/probe_code/export.py                  export-blind, export-trace
  src/probe_code/corroboration.py
  src/probe_code/agreement.py
  src/probe_code/guard_audit.py
  src/probe_code/cli.py
  web/console.html  web/expert.html  web/css/app.css  web/js/console.js  web/js/expert.js
  codebook/v0.md
  pilot-protocol.md
  tests/fakes.py  tests/test_*.py
research/experiment-ai-assisted-cta-physics.md   Stage A wording amended
```

---

### Task 1: Package scaffold, frozen content and frozen config

**Files:**
- Create: `instrument/pyproject.toml`, `instrument/src/probe_app/__init__.py`, `instrument/src/probe_code/__init__.py`, `instrument/prompts/interviewer_system.md`, `instrument/prompts/guard_system.md`, `instrument/prompts/stems.json`, `instrument/problems/problems.json`, `instrument/src/probe_app/config.py`
- Modify: `.gitignore`
- Test: `instrument/tests/test_config.py`

**Interfaces:**
- Produces: `INSTRUMENT_DIR`, `PROMPTS_DIR`, `PROBLEMS_PATH`, `PREREG_PATH`, `INTERVIEWER_MODEL`, `INTERVIEWER_EFFORT`, `GUARD_MODEL`, `TRANSCRIBER_MODEL`, `CAP_S`, `WRAP_S`; `class ConfigMismatch(Exception)`; `@dataclass(frozen=True) FrozenConfig`; `sha256_file(path: Path) -> str`; `current_config(prompts_dir: Path = PROMPTS_DIR) -> FrozenConfig`; `check_preregistered(cfg: FrozenConfig, prereg_path: Path = PREREG_PATH) -> None`; `freeze(cfg: FrozenConfig, prereg_path: Path = PREREG_PATH) -> None`; `load_prompt(name: str, prompts_dir: Path = PROMPTS_DIR) -> str`; `load_stems(prompts_dir: Path = PROMPTS_DIR) -> dict[str, str]`; `load_problems(path: Path = PROBLEMS_PATH) -> dict`; `git_commit() -> str`.

- [ ] **Step 1: Create the package and dev environment**

`instrument/pyproject.toml`:

```toml
[project]
name = "probe-instrument"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
  "anthropic>=0.116",
  "elevenlabs>=2.0",
  "openai>=1.50",
  "fastapi>=0.115",
  "uvicorn>=0.30",
  "python-multipart>=0.0.9",
  "pydantic>=2.7",
  "python-dotenv>=1.0",
  "krippendorff>=0.8",
  "numpy>=1.26",
]

[project.scripts]
probe-app = "probe_app.cli:main"
probe-code = "probe_code.cli:main"

[dependency-groups]
dev = ["pytest>=8", "httpx>=0.27"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/probe_app", "src/probe_code"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["tests"]
```

Create empty `instrument/src/probe_app/__init__.py` and `instrument/src/probe_code/__init__.py`.

The repo-root `.gitignore` already ignores `sessions/`, `instrument/.env`, `instrument/.venv/` and `instrument/sessions/`. Confirm with `git check-ignore instrument/.env` (prints the path).

Run: `cd instrument && uv sync`
Expected: environment created, no errors.

- [ ] **Step 2: Write the frozen content files**

`instrument/prompts/stems.json`:

```json
{
  "cues": "At this point in your solution, what did you notice that told you what to do?",
  "alternatives": "What else could you have done at this point, and why didn't you?",
  "checks": "How did you know your result here was right?",
  "anomalies": "What would have made you stop and rethink at this point?",
  "novice_miss": "What would a first-year student miss here that you see?"
}
```

`instrument/prompts/interviewer_system.md`:

```markdown
You are conducting a retrospective cognitive task analysis interview with a physicist. A few minutes ago they solved the physics problems below while thinking aloud. You have their transcript, with segment IDs and times, and a snapshot of their written work for each problem. Your job is to recover the mental operations behind that solution: the cues they noticed, the alternatives they considered and rejected, the checks they ran, what would have made them rethink, and what a first-year student would miss. The interview is research data, so how you ask matters as much as what you learn.

Rules:
- Ask one question per turn, short enough to take in at a glance.
- Tie each question to a specific moment of their solution: transcript segments or their written work. Refer to it in their own words.
- Never suggest an operation, principle, quantity, check or strategy they have not mentioned. "Did you check the units?" is leading; "How did you know that result was right?" is not. Keep any hypothesis to yourself and ask a neutral question that would let them say it.
- Every question uses one of five stems. Word it naturally; you need not repeat the wording below.
  - cues: what they noticed that told them what to do
  - alternatives: what else they could have done there, and why not
  - checks: how they knew a step or result was right
  - anomalies: what would have made them stop and rethink
  - novice_miss: what a first-year student would miss or do wrongly there
- Use every stem at least once for every problem. You choose the order and the moments.
- Directly after a stem question you may ask at most one follow-up on the same stem and problem. A follow-up quotes something the expert said, exactly, and asks them to say more, for example: You said "it's obviously not elastic" — what told you that? Put the exact quoted words in quoted_span.
- Do not evaluate, praise or correct the expert's physics, and do not explain physics yourself.
- When time is short, prefer stems not yet used.

Return one JSON object per turn:
- utterance: the question exactly as the expert will read it
- stem_id: cues, alternatives, checks, anomalies or novice_miss
- problem_id: the problem the question is about
- anchor: {"kind": "segments", "segment_ids": [...]} for transcript segments of that problem, {"kind": "canvas", "segment_ids": []} for their written work, or {"kind": "none", "segment_ids": []}
- is_followup: true only for the one allowed follow-up
- quoted_span: the exact quoted words for a follow-up, otherwise null
- end_session: true only when every stem has been used for every problem and nothing further is worth asking; utterance is then a one-sentence thank-you
```

`instrument/prompts/guard_system.md`:

```markdown
You check interview questions for leading content. You receive the problem statements, everything an expert has said so far, and one question an interviewer proposes to ask.

A question is leading if it names or implies a specific physics principle, quantity, relation, representation, strategy or check that the expert has not said, in the same or equivalent words. Neutral questions about what the expert noticed, considered, checked or expected are not leading. Restating the expert's own words is not leading. Words that appear in the problem statements are not leading.

Return flagged true if the question is leading, with introduced naming the content the expert had not said. Otherwise return flagged false and introduced as an empty string.
```

`instrument/problems/problems.json`:

```json
{
  "sets": {"A": ["A1", "A2"], "B": ["B1", "B2"]},
  "problems": {
    "A1": {
      "statement": "A 2.0 kg block is released from rest at a height of 1.8 m on a frictionless ramp. At the bottom it collides with a 1.0 kg block at rest, and the two stick together. They then slide up a second frictionless ramp. How high do they rise?",
      "answer": "0.80 m"
    },
    "A2": {
      "statement": "A 10 g bullet moving horizontally at 300 m/s embeds itself in a 2.0 kg wooden block hanging at rest from a 1.5 m string. What is the largest angle the string makes with the vertical?",
      "answer": "about 22 degrees"
    },
    "B1": {
      "statement": "A 0.50 kg block sliding at 4.0 m/s on a frictionless surface hits and sticks to a 1.5 kg block at rest, which is attached to a horizontal spring (k = 200 N/m) whose other end is fixed to a wall. What is the maximum compression of the spring?",
      "answer": "0.10 m"
    },
    "B2": {
      "statement": "A 2.0 kg cart moving at 3.0 m/s collides elastically with a 1.0 kg cart at rest on a frictionless track. The track ahead of the 1.0 kg cart rises over a hill 0.50 m high. Does the 1.0 kg cart make it over the hill?",
      "answer": "yes: it leaves at 4.0 m/s and could climb 0.82 m"
    }
  }
}
```

- [ ] **Step 3: Write the failing test**

`instrument/tests/test_config.py`:

```python
import json
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
```

- [ ] **Step 4: Run test to verify it fails**

Run: `uv run pytest tests/test_config.py -v`
Expected: FAIL with `ImportError` / `cannot import name 'config'`.

- [ ] **Step 5: Write the implementation**

`instrument/src/probe_app/config.py`:

```python
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
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `uv run pytest tests/test_config.py -v`
Expected: 6 passed.

- [ ] **Step 7: Commit**

```bash
git add instrument/pyproject.toml instrument/uv.lock instrument/src instrument/prompts instrument/problems instrument/tests/test_config.py
git commit -m "Instrument: package, frozen prompts, pilot problems, pre-registration check"
```

---

### Task 2: Models and session storage

**Files:**
- Create: `instrument/src/probe_app/models.py`, `instrument/src/probe_app/storage.py`, `instrument/tests/fakes.py`
- Test: `instrument/tests/test_storage.py`

**Interfaces:**
- Produces (models): `STEMS: tuple[str, ...]`; `StemId` Literal; pydantic `Segment(id, problem_id, start: float, end: float, text)`; `Anchor(kind: Literal["segments","canvas","none"], segment_ids: list[str])`; `InterviewerTurn(utterance, stem_id: StemId, problem_id, anchor: Anchor, is_followup: bool, quoted_span: str | None, end_session: bool)`; `DialogueTurn(speaker: Literal["interviewer","expert"], text, t: float, stem_id=None, problem_id=None, is_followup=False, anchor=None, source=None)`; `GuardVerdict(flagged: bool, introduced: str)`.
- Produces (storage): `MonotonicClock.now() -> float`; `SessionStore(root: Path, session_id: str, clock=None)` with `.dir`, `.session_id`, `.clock`, `SessionStore.create(root, manifest: dict, clock=None) -> SessionStore`, `.manifest -> dict`, `.path(rel: str) -> Path`, `.log(type_: str, **data) -> dict`, `.events() -> list[dict]`, `.write_json(rel, obj)`, `.read_json(rel)`, `.log_llm(record: dict) -> Path`.
- Produces (tests/fakes.py): `FakeClock(t=0.0)` with `.now()`, `.advance(dt)`.

- [ ] **Step 1: Write the failing test**

`instrument/tests/fakes.py`:

```python
class FakeClock:
    def __init__(self, t: float = 0.0):
        self.t = t

    def now(self) -> float:
        return self.t

    def advance(self, dt: float) -> None:
        self.t += dt
```

`instrument/tests/test_storage.py`:

```python
import json

import pytest

from fakes import FakeClock
from probe_app.models import InterviewerTurn
from probe_app.storage import SessionStore


def test_create_writes_manifest_and_dirs(tmp_path):
    store = SessionStore.create(tmp_path, {"expert_id": "E01"})
    assert store.session_id.startswith("E01-")
    assert store.manifest == {"expert_id": "E01"}
    for d in ("audio", "canvas/snapshots", "transcripts", "llm"):
        assert (store.dir / d).is_dir()


def test_log_appends_with_both_timestamps(tmp_path):
    clock = FakeClock(5.0)
    store = SessionStore.create(tmp_path, {"expert_id": "E01"}, clock)
    store.log("keep_talking", problem_id="A1")
    clock.advance(2.5)
    store.log("probe", text="q")
    events = store.events()
    assert [e["type"] for e in events] == ["keep_talking", "probe"]
    assert events[1]["t_mono"] == 7.5
    assert "t_wall" in events[0] and events[0]["problem_id"] == "A1"


def test_write_and_read_json_roundtrip(tmp_path):
    store = SessionStore.create(tmp_path, {"expert_id": "E01"})
    store.write_json("state.json", {"phase": "ready"})
    assert store.read_json("state.json") == {"phase": "ready"}
    assert not list(store.dir.glob("*.tmp"))


def test_log_llm_numbers_files(tmp_path):
    store = SessionStore.create(tmp_path, {"expert_id": "E01"})
    a = store.log_llm({"kind": "interviewer"})
    b = store.log_llm({"kind": "guard"})
    assert (a.name, b.name) == ("0001.json", "0002.json")
    assert json.loads(b.read_text()) == {"kind": "guard"}


def test_interviewer_turn_forbids_extra_fields():
    with pytest.raises(ValueError):
        InterviewerTurn.model_validate({
            "utterance": "q", "stem_id": "cues", "problem_id": "A1",
            "anchor": {"kind": "none", "segment_ids": []}, "is_followup": False,
            "quoted_span": None, "end_session": False, "extra": 1,
        })
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_storage.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'probe_app.models'`.

- [ ] **Step 3: Write the implementation**

`instrument/src/probe_app/models.py`:

```python
from typing import Literal

from pydantic import BaseModel, ConfigDict

STEMS: tuple[str, ...] = ("cues", "alternatives", "checks", "anomalies", "novice_miss")
StemId = Literal["cues", "alternatives", "checks", "anomalies", "novice_miss"]


class Segment(BaseModel):
    id: str
    problem_id: str
    start: float
    end: float
    text: str


class Anchor(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["segments", "canvas", "none"]
    segment_ids: list[str]


class InterviewerTurn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    utterance: str
    stem_id: StemId
    problem_id: str
    anchor: Anchor
    is_followup: bool
    quoted_span: str | None
    end_session: bool


class DialogueTurn(BaseModel):
    speaker: Literal["interviewer", "expert"]
    text: str
    t: float
    stem_id: StemId | None = None
    problem_id: str | None = None
    is_followup: bool = False
    anchor: Anchor | None = None
    source: Literal["ai", "ai_fallback", "human", "transcribed", "typed", "simulated"] | None = None


class GuardVerdict(BaseModel):
    flagged: bool
    introduced: str
```

`instrument/src/probe_app/storage.py`:

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_storage.py -v`
Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add instrument/src/probe_app/models.py instrument/src/probe_app/storage.py instrument/tests/fakes.py instrument/tests/test_storage.py
git commit -m "Instrument: data models and append-only session store"
```

---

### Task 3: Transcription and trace

**Files:**
- Create: `instrument/src/probe_app/transcribe.py`, `instrument/src/probe_app/trace.py`
- Modify: `instrument/tests/fakes.py`
- Test: `instrument/tests/test_trace.py`

**Interfaces:**
- Consumes: `Segment` (Task 2), `TRANSCRIBER_MODEL` (Task 1).
- Produces: `RawSegment(start: float, end: float, text: str)` (pydantic); `Transcriber` Protocol with `.model: str`, `.transcribe(audio_path: Path) -> list[RawSegment]`; `words_to_segments(words: list[dict], max_gap: float = 0.8) -> list[RawSegment]`; `ScribeTranscriber(model="scribe_v2", client=None)`; `OpenAITranscriber(model="whisper-1", client=None)`; `make_transcriber(model: str = TRANSCRIBER_MODEL) -> Transcriber`; `class TranscriptionFailed(Exception)`; `transcribe_with_retry(t: Transcriber, audio_path: Path, attempts: int = 3) -> list[RawSegment]`; `build_segments(problem_id: str, offset: float, raw: list[RawSegment]) -> list[Segment]`; `correct_segment(segments: list[Segment], segment_id: str, text: str) -> tuple[list[Segment], dict]`; `render_transcript(segments: list[Segment]) -> str`.
- Produces (fakes): `FakeTranscriber(results: list)` — each item a `list[RawSegment]` or an `Exception` to raise; `.model = "fake"`; `.calls: list[Path]`.

- [ ] **Step 1: Write the failing test**

Append to `instrument/tests/fakes.py`:

```python
from pathlib import Path

from probe_app.transcribe import RawSegment


class FakeTranscriber:
    model = "fake"

    def __init__(self, results: list):
        self.results = list(results)
        self.calls: list[Path] = []

    def transcribe(self, audio_path: Path) -> list[RawSegment]:
        self.calls.append(audio_path)
        item = self.results.pop(0)
        if isinstance(item, Exception):
            raise item
        return item
```

`instrument/tests/test_trace.py`:

```python
from types import SimpleNamespace

import pytest

from fakes import FakeTranscriber
from probe_app.trace import build_segments, correct_segment, render_transcript
from probe_app.transcribe import (RawSegment, ScribeTranscriber, TranscriptionFailed, make_transcriber,
                                  transcribe_with_retry, words_to_segments)

RAW = [RawSegment(start=0.0, end=2.0, text="Energy first."), RawSegment(start=2.0, end=5.5, text="Then momentum.")]


def test_build_segments_offsets_and_ids():
    segs = build_segments("A1", 10.0, RAW)
    assert [s.id for s in segs] == ["A1-s001", "A1-s002"]
    assert (segs[1].start, segs[1].end) == (12.0, 15.5)
    assert segs[0].problem_id == "A1"


def test_correct_segment_returns_diff():
    segs = build_segments("A1", 0.0, RAW)
    new, diff = correct_segment(segs, "A1-s002", "Then momentum conservation.")
    assert new[1].text == "Then momentum conservation."
    assert diff == {"segment_id": "A1-s002", "old": "Then momentum.", "new": "Then momentum conservation."}
    assert segs[1].text == "Then momentum."


def test_correct_unknown_segment_raises():
    with pytest.raises(KeyError):
        correct_segment(build_segments("A1", 0.0, RAW), "A1-s999", "x")


def test_render_transcript():
    assert render_transcript(build_segments("A1", 0.0, RAW)).splitlines()[0] == "[A1-s001 0.0-2.0s] Energy first."


def test_retry_succeeds_on_third_attempt(tmp_path):
    t = FakeTranscriber([RuntimeError("a"), RuntimeError("b"), RAW])
    assert transcribe_with_retry(t, tmp_path / "x.webm") == RAW
    assert len(t.calls) == 3


def test_retry_gives_up_after_three(tmp_path):
    t = FakeTranscriber([RuntimeError("a"), RuntimeError("b"), RuntimeError("c")])
    with pytest.raises(TranscriptionFailed, match="c"):
        transcribe_with_retry(t, tmp_path / "x.webm")


def w(text, start, end, type_="word"):
    return {"text": text, "start": start, "end": end, "type": type_}


def test_words_group_on_sentence_end_and_pause():
    sp = lambda s: w(" ", s, s, "spacing")
    words = [w("Energy", 0.0, 0.4), sp(0.4), w("first.", 0.5, 0.9), sp(0.9),
             w("Then", 1.0, 1.2), sp(1.2), w("momentum", 1.3, 1.8),
             w("(laughs)", 1.9, 2.0, "audio_event"), sp(1.8), w("so", 3.0, 3.1)]
    segs = words_to_segments(words)
    assert [(x.text, x.start, x.end) for x in segs] == [
        ("Energy first.", 0.0, 0.9), ("Then momentum", 1.0, 1.8), ("so", 3.0, 3.1)]


def test_scribe_transcriber_sends_keyterms(tmp_path):
    calls = []

    def convert(**kwargs):
        calls.append(kwargs)
        return SimpleNamespace(words=[w("Momentum.", 0.0, 0.6)])

    client = SimpleNamespace(speech_to_text=SimpleNamespace(convert=convert))
    audio = tmp_path / "a.webm"
    audio.write_bytes(b"x")
    segs = ScribeTranscriber(client=client).transcribe(audio)
    assert segs[0].text == "Momentum."
    assert calls[0]["model_id"] == "scribe_v2" and "ballistic pendulum" in calls[0]["keyterms"]
    assert calls[0]["timestamps_granularity"] == "word"


def test_make_transcriber_picks_provider():
    assert type(make_transcriber("scribe_v2", client=object())).__name__ == "ScribeTranscriber"
    assert type(make_transcriber("whisper-1", client=object())).__name__ == "OpenAITranscriber"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_trace.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'probe_app.transcribe'`.

- [ ] **Step 3: Write the implementation**

`instrument/src/probe_app/transcribe.py`:

```python
import os
from pathlib import Path
from typing import Protocol

from pydantic import BaseModel

from probe_app.config import TRANSCRIBER_MODEL

PHYSICS_KEYTERMS = [
    "momentum", "kinetic energy", "potential energy", "conservation of energy", "conservation of momentum",
    "inelastic collision", "elastic collision", "ballistic pendulum", "spring constant", "compression",
    "free-body diagram", "centre of mass", "frictionless", "impulse", "joules", "newtons",
]
PHYSICS_VOCAB = ", ".join(PHYSICS_KEYTERMS)


class RawSegment(BaseModel):
    start: float
    end: float
    text: str


class Transcriber(Protocol):
    model: str

    def transcribe(self, audio_path: Path) -> list[RawSegment]: ...


class TranscriptionFailed(Exception):
    pass


def words_to_segments(words: list[dict], max_gap: float = 0.8) -> list[RawSegment]:
    segments: list[RawSegment] = []
    parts: list[str] = []
    start = end = None
    for word in words:
        if word["type"] == "audio_event":
            continue
        if word["type"] == "spacing":
            if parts:
                parts.append(word["text"])
            continue
        if parts and word["start"] - end > max_gap:
            segments.append(RawSegment(start=start, end=end, text="".join(parts).strip()))
            parts, start = [], None
        if start is None:
            start = word["start"]
        parts.append(word["text"])
        end = word["end"]
        if word["text"].rstrip().endswith((".", "?", "!")):
            segments.append(RawSegment(start=start, end=end, text="".join(parts).strip()))
            parts, start = [], None
    if parts:
        segments.append(RawSegment(start=start, end=end, text="".join(parts).strip()))
    return segments


class ScribeTranscriber:
    def __init__(self, model: str = "scribe_v2", client=None):
        if client is None:
            from elevenlabs.client import ElevenLabs

            client = ElevenLabs(api_key=os.environ.get("ELEVEN_LABS_API_KEY") or os.environ.get("ELEVENLABS_API_KEY"))
        self.model, self.client = model, client

    def transcribe(self, audio_path: Path) -> list[RawSegment]:
        with audio_path.open("rb") as f:
            result = self.client.speech_to_text.convert(
                file=f, model_id=self.model, language_code="eng", tag_audio_events=False,
                timestamps_granularity="word", keyterms=PHYSICS_KEYTERMS,
            )
        words = [w.model_dump() if hasattr(w, "model_dump") else w for w in result.words]
        return words_to_segments(words)


class OpenAITranscriber:
    def __init__(self, model: str = "whisper-1", client=None):
        from openai import OpenAI

        self.model = model
        self.client = client or OpenAI()

    def transcribe(self, audio_path: Path) -> list[RawSegment]:
        with audio_path.open("rb") as f:
            result = self.client.audio.transcriptions.create(
                model=self.model, file=f, response_format="verbose_json",
                timestamp_granularities=["segment"], prompt=PHYSICS_VOCAB,
            )
        return [RawSegment(start=s.start, end=s.end, text=s.text.strip()) for s in (result.segments or [])]


def transcribe_with_retry(t: Transcriber, audio_path: Path, attempts: int = 3) -> list[RawSegment]:
    last: Exception | None = None
    for _ in range(attempts):
        try:
            return t.transcribe(audio_path)
        except Exception as e:  # provider, network and file errors all end in the same manual fallback
            last = e
    raise TranscriptionFailed(str(last)) from last


def make_transcriber(model: str = TRANSCRIBER_MODEL, client=None) -> Transcriber:
    if model.startswith("scribe"):
        return ScribeTranscriber(model, client)
    return OpenAITranscriber(model, client)
```

`instrument/src/probe_app/trace.py`:

```python
from probe_app.models import Segment
from probe_app.transcribe import RawSegment


def build_segments(problem_id: str, offset: float, raw: list[RawSegment]) -> list[Segment]:
    return [Segment(id=f"{problem_id}-s{i:03d}", problem_id=problem_id,
                    start=offset + r.start, end=offset + r.end, text=r.text)
            for i, r in enumerate(raw, 1)]


def correct_segment(segments: list[Segment], segment_id: str, text: str) -> tuple[list[Segment], dict]:
    index = next((i for i, s in enumerate(segments) if s.id == segment_id), None)
    if index is None:
        raise KeyError(f"no segment {segment_id}")
    old = segments[index]
    updated = list(segments)
    updated[index] = old.model_copy(update={"text": text})
    return updated, {"segment_id": segment_id, "old": old.text, "new": text}


def render_transcript(segments: list[Segment]) -> str:
    return "\n".join(f"[{s.id} {s.start:.1f}-{s.end:.1f}s] {s.text}" for s in segments)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_trace.py -v`
Expected: 9 passed.

- [ ] **Step 5: Commit**

```bash
git add instrument/src/probe_app/transcribe.py instrument/src/probe_app/trace.py instrument/tests/fakes.py instrument/tests/test_trace.py
git commit -m "Instrument: Scribe v2 and whisper transcribers with retry, trace segments and corrections"
```

---

### Task 4: Interviewer contract

**Files:**
- Create: `instrument/src/probe_app/contract.py`
- Test: `instrument/tests/test_contract.py`

**Interfaces:**
- Consumes: `STEMS`, `InterviewerTurn`, `Segment` (Task 2).
- Produces: `class ContractViolation(Exception)`; pydantic `ContractState(problems: list[str], used: dict[str, int] = {}, last_primary: str | None = None, last_primary_followed: bool = False)`; `normalize(text: str) -> str`; `check_turn(turn: InterviewerTurn, state: ContractState, segments: list[Segment], expert_text: str) -> None`; `record(turn: InterviewerTurn, state: ContractState) -> None`; `uncovered(state: ContractState) -> list[str]` (keys `"A1/cues"`); `next_fallback(state: ContractState) -> tuple[str, str] | None`.

- [ ] **Step 1: Write the failing test**

`instrument/tests/test_contract.py`:

```python
import pytest

from probe_app.contract import (ContractState, ContractViolation, check_turn, next_fallback,
                                normalize, record, uncovered)
from probe_app.models import STEMS, Anchor, InterviewerTurn, Segment

SEGS = [Segment(id="A1-s001", problem_id="A1", start=0, end=1, text="It's obviously not elastic."),
        Segment(id="A2-s001", problem_id="A2", start=0, end=1, text="Bullet sticks.")]
EXPERT = " ".join(s.text for s in SEGS)


def turn(**kw) -> InterviewerTurn:
    base = dict(utterance="q", stem_id="cues", problem_id="A1",
                anchor=Anchor(kind="segments", segment_ids=["A1-s001"]),
                is_followup=False, quoted_span=None, end_session=False)
    base.update(kw)
    return InterviewerTurn(**base)


@pytest.fixture
def state() -> ContractState:
    return ContractState(problems=["A1", "A2"])


def test_primary_turn_passes(state):
    check_turn(turn(), state, SEGS, EXPERT)


def test_unknown_problem_rejected(state):
    with pytest.raises(ContractViolation, match="problem"):
        check_turn(turn(problem_id="B1"), state, SEGS, EXPERT)


def test_anchor_segment_from_other_problem_rejected(state):
    with pytest.raises(ContractViolation, match="anchor"):
        check_turn(turn(anchor=Anchor(kind="segments", segment_ids=["A2-s001"])), state, SEGS, EXPERT)


def test_empty_segment_anchor_rejected(state):
    with pytest.raises(ContractViolation, match="anchor"):
        check_turn(turn(anchor=Anchor(kind="segments", segment_ids=[])), state, SEGS, EXPERT)


def test_followup_must_follow_its_primary(state):
    with pytest.raises(ContractViolation, match="follow"):
        check_turn(turn(is_followup=True, quoted_span="not elastic"), state, SEGS, EXPERT)


def test_one_followup_only(state):
    record(turn(), state)
    fu = turn(is_followup=True, quoted_span="not elastic")
    check_turn(fu, state, SEGS, EXPERT)
    record(fu, state)
    with pytest.raises(ContractViolation, match="second follow-up"):
        check_turn(fu, state, SEGS, EXPERT)


def test_followup_quote_must_be_experts_words(state):
    record(turn(), state)
    with pytest.raises(ContractViolation, match="quoted"):
        check_turn(turn(is_followup=True, quoted_span="momentum is conserved"), state, SEGS, EXPERT)


def test_followup_quote_matches_despite_curly_quotes_and_case(state):
    record(turn(), state)
    check_turn(turn(is_followup=True, quoted_span="“It’s OBVIOUSLY not elastic”"), state, SEGS, EXPERT)


def test_end_session_needs_full_coverage(state):
    with pytest.raises(ContractViolation, match="coverage"):
        check_turn(turn(end_session=True), state, SEGS, EXPERT)
    for p in ("A1", "A2"):
        for s in STEMS:
            record(turn(problem_id=p, stem_id=s, anchor=Anchor(kind="none", segment_ids=[])), state)
    check_turn(turn(end_session=True), state, SEGS, EXPERT)


def test_uncovered_and_fallback_order(state):
    assert len(uncovered(state)) == 10
    record(turn(stem_id="cues"), state)
    assert "A1/cues" not in uncovered(state)
    assert next_fallback(state) == ("A1", "alternatives")


def test_normalize():
    assert normalize("  “It’s”  OK!! ") == "it s ok"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_contract.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'probe_app.contract'`.

- [ ] **Step 3: Write the implementation**

`instrument/src/probe_app/contract.py`:

```python
import re
import unicodedata

from pydantic import BaseModel

from probe_app.models import STEMS, InterviewerTurn, Segment


class ContractViolation(Exception):
    pass


class ContractState(BaseModel):
    problems: list[str]
    used: dict[str, int] = {}
    last_primary: str | None = None
    last_primary_followed: bool = False


def _key(problem_id: str, stem_id: str) -> str:
    return f"{problem_id}/{stem_id}"


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).lower()
    return " ".join(re.sub(r"[^\w\s]", " ", text).split())


def uncovered(state: ContractState) -> list[str]:
    return [_key(p, s) for p in state.problems for s in STEMS if state.used.get(_key(p, s), 0) == 0]


def next_fallback(state: ContractState) -> tuple[str, str] | None:
    missing = uncovered(state)
    if not missing:
        return None
    problem_id, stem_id = missing[0].split("/")
    return problem_id, stem_id


def check_turn(turn: InterviewerTurn, state: ContractState, segments: list[Segment], expert_text: str) -> None:
    if turn.end_session:
        missing = uncovered(state)
        if missing:
            raise ContractViolation(f"end_session before full coverage; unused: {missing}")
        return
    if turn.problem_id not in state.problems:
        raise ContractViolation(f"problem {turn.problem_id} is not in this set {state.problems}")
    if turn.anchor.kind == "segments":
        owner = {s.id: s.problem_id for s in segments}
        bad = [i for i in turn.anchor.segment_ids if owner.get(i) != turn.problem_id]
        if not turn.anchor.segment_ids or bad:
            raise ContractViolation(f"anchor segments must belong to {turn.problem_id}; bad: {bad or 'none given'}")
    if turn.is_followup:
        if state.last_primary != _key(turn.problem_id, turn.stem_id):
            raise ContractViolation("a follow-up must directly follow the stem question it belongs to")
        if state.last_primary_followed:
            raise ContractViolation("second follow-up on the same stem question")
        quote = normalize(turn.quoted_span or "")
        if not quote or quote not in normalize(expert_text):
            raise ContractViolation("quoted_span is not the expert's own words")


def record(turn: InterviewerTurn, state: ContractState) -> None:
    if turn.end_session:
        return
    key = _key(turn.problem_id, turn.stem_id)
    if turn.is_followup:
        state.last_primary_followed = True
        return
    state.used[key] = state.used.get(key, 0) + 1
    state.last_primary = key
    state.last_primary_followed = False
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_contract.py -v`
Expected: 11 passed.

- [ ] **Step 5: Commit**

```bash
git add instrument/src/probe_app/contract.py instrument/tests/test_contract.py
git commit -m "Instrument: interviewer turn contract (stems, anchors, one quoted follow-up, coverage)"
```

---

### Task 5: Claude clients — interviewer and guard

**Files:**
- Create: `instrument/src/probe_app/llm.py`
- Modify: `instrument/tests/fakes.py`
- Test: `instrument/tests/test_llm.py`

**Interfaces:**
- Consumes: `InterviewerTurn`, `GuardVerdict`, `DialogueTurn`, `STEMS` (Task 2); config constants (Task 1).
- Produces: `class LLMUnavailable(Exception)`, `class LLMRefused(Exception)`; `@dataclass TurnRequest(problems: dict[str, str], transcript: str, snapshots: dict[str, bytes], dialogue: list[DialogueTurn], remaining_s: float, wrap_up: bool, unused: list[str], rejection: str | None = None)`; `InterviewerLLM(client, log: Callable[[dict], object], system_prompt: str, model=INTERVIEWER_MODEL, effort=INTERVIEWER_EFFORT)` with `.next_turn(req: TurnRequest) -> InterviewerTurn`; `Guard(client, log, system_prompt, model=GUARD_MODEL)` with `.check(utterance: str, problem_text: str, expert_text: str) -> GuardVerdict`; `INTERVIEWER_TURN_SCHEMA`, `GUARD_SCHEMA` dicts.
- Produces (fakes): `FakeResponse(payload: dict | None, stop_reason="end_turn")`; `FakeAnthropic(interviewer: list | None = None, guard: list | None = None)` — each list item is a `FakeResponse` or an `Exception`; guard defaults to "not flagged" when its list is empty; `.calls: list[dict]`; `turn_payload(**overrides) -> dict`.

- [ ] **Step 1: Write the failing test**

Append to `instrument/tests/fakes.py`:

```python
import json as _json
from types import SimpleNamespace

from probe_app.config import GUARD_MODEL


class FakeResponse:
    def __init__(self, payload: dict | None, stop_reason: str = "end_turn"):
        self.stop_reason = stop_reason
        self.content = [] if payload is None else [SimpleNamespace(type="text", text=_json.dumps(payload))]

    def model_dump(self, mode: str = "json") -> dict:
        return {"stop_reason": self.stop_reason, "content": [{"type": "text", "text": c.text} for c in self.content]}


class FakeAnthropic:
    def __init__(self, interviewer: list | None = None, guard: list | None = None):
        self.queues = {"interviewer": list(interviewer or []), "guard": list(guard or [])}
        self.calls: list[dict] = []
        self.messages = self

    def create(self, **kwargs):
        self.calls.append(kwargs)
        role = "guard" if kwargs["model"] == GUARD_MODEL else "interviewer"
        queue = self.queues[role]
        if not queue and role == "guard":
            return FakeResponse({"flagged": False, "introduced": ""})
        item = queue.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


def turn_payload(**overrides) -> dict:
    payload = {"utterance": "What did you notice first?", "stem_id": "cues", "problem_id": "A1",
               "anchor": {"kind": "none", "segment_ids": []}, "is_followup": False,
               "quoted_span": None, "end_session": False}
    payload.update(overrides)
    return payload
```

`instrument/tests/test_llm.py`:

```python
import anthropic
import httpx
import pytest

from fakes import FakeAnthropic, FakeResponse, turn_payload
from probe_app.llm import Guard, InterviewerLLM, LLMRefused, LLMUnavailable, TurnRequest
from probe_app.models import DialogueTurn

PNG = bytes.fromhex("89504e470d0a1a0a")


def request(**kw) -> TurnRequest:
    base = dict(problems={"A1": "Block problem"}, transcript="[A1-s001 0.0-1.0s] Energy first.",
                snapshots={"A1": PNG}, dialogue=[DialogueTurn(speaker="expert", text="I used energy.", t=3.0)],
                remaining_s=600.0, wrap_up=False, unused=["A1/checks"])
    base.update(kw)
    return TurnRequest(**base)


def test_next_turn_parses_and_logs():
    logged = []
    client = FakeAnthropic(interviewer=[FakeResponse(turn_payload())])
    turn = InterviewerLLM(client, logged.append, "SYSTEM").next_turn(request())
    assert turn.stem_id == "cues"
    call = client.calls[0]
    assert call["model"] == "claude-opus-5"
    assert call["thinking"] == {"type": "adaptive"}
    assert call["output_config"]["effort"] == "medium"
    assert call["output_config"]["format"]["type"] == "json_schema"
    assert "temperature" not in call and "fallbacks" not in call
    assert logged[0]["kind"] == "interviewer"
    assert "base64" not in str(logged[0]["request"])


def test_dynamic_text_carries_wrap_up_and_rejection():
    client = FakeAnthropic(interviewer=[FakeResponse(turn_payload())])
    InterviewerLLM(client, lambda r: None, "S").next_turn(request(wrap_up=True, rejection="contract: bad anchor"))
    last_block = client.calls[0]["messages"][0]["content"][-1]["text"]
    assert "Less than two minutes remain" in last_block
    assert "contract: bad anchor" in last_block
    assert "A1/checks" in last_block


def test_static_blocks_are_cached():
    client = FakeAnthropic(interviewer=[FakeResponse(turn_payload())])
    InterviewerLLM(client, lambda r: None, "S").next_turn(request())
    content = client.calls[0]["messages"][0]["content"]
    assert content[-2].get("cache_control") == {"type": "ephemeral"}
    assert "cache_control" not in content[-1]


def test_refusal_raises():
    client = FakeAnthropic(interviewer=[FakeResponse(None, stop_reason="refusal")])
    with pytest.raises(LLMRefused):
        InterviewerLLM(client, lambda r: None, "S").next_turn(request())


def test_api_error_raises_unavailable():
    err = anthropic.APIConnectionError(request=httpx.Request("POST", "https://api.anthropic.com"))
    client = FakeAnthropic(interviewer=[err])
    with pytest.raises(LLMUnavailable):
        InterviewerLLM(client, lambda r: None, "S").next_turn(request())


def test_invalid_json_raises_unavailable():
    client = FakeAnthropic(interviewer=[FakeResponse({"utterance": "q"})])
    with pytest.raises(LLMUnavailable):
        InterviewerLLM(client, lambda r: None, "S").next_turn(request())


def test_guard_uses_haiku_at_temperature_zero():
    client = FakeAnthropic(guard=[FakeResponse({"flagged": True, "introduced": "units"})])
    verdict = Guard(client, lambda r: None, "G").check("Did you check units?", "A1: ...", "I used energy.")
    assert verdict.flagged and verdict.introduced == "units"
    assert client.calls[0]["model"] == "claude-haiku-4-5"
    assert client.calls[0]["temperature"] == 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_llm.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'probe_app.llm'`.

- [ ] **Step 3: Write the implementation**

`instrument/src/probe_app/llm.py`:

```python
import base64
import hashlib
from dataclasses import dataclass
from typing import Callable

import anthropic
from pydantic import ValidationError

from probe_app.config import GUARD_MODEL, INTERVIEWER_EFFORT, INTERVIEWER_MODEL
from probe_app.models import STEMS, DialogueTurn, GuardVerdict, InterviewerTurn

INTERVIEWER_TURN_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["utterance", "stem_id", "problem_id", "anchor", "is_followup", "quoted_span", "end_session"],
    "properties": {
        "utterance": {"type": "string"},
        "stem_id": {"type": "string", "enum": list(STEMS)},
        "problem_id": {"type": "string"},
        "anchor": {
            "type": "object",
            "additionalProperties": False,
            "required": ["kind", "segment_ids"],
            "properties": {
                "kind": {"type": "string", "enum": ["segments", "canvas", "none"]},
                "segment_ids": {"type": "array", "items": {"type": "string"}},
            },
        },
        "is_followup": {"type": "boolean"},
        "quoted_span": {"anyOf": [{"type": "string"}, {"type": "null"}]},
        "end_session": {"type": "boolean"},
    },
}

GUARD_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["flagged", "introduced"],
    "properties": {"flagged": {"type": "boolean"}, "introduced": {"type": "string"}},
}


class LLMUnavailable(Exception):
    pass


class LLMRefused(Exception):
    pass


@dataclass
class TurnRequest:
    problems: dict[str, str]
    transcript: str
    snapshots: dict[str, bytes]
    dialogue: list[DialogueTurn]
    remaining_s: float
    wrap_up: bool
    unused: list[str]
    rejection: str | None = None


def _call(client, log: Callable[[dict], object], kind: str, params: dict, loggable: dict):
    try:
        response = client.messages.create(**params)
    except anthropic.APIError as e:
        log({"kind": kind, "request": loggable, "error": repr(e)})
        raise LLMUnavailable(repr(e)) from e
    log({"kind": kind, "request": loggable, "response": response.model_dump(mode="json")})
    if response.stop_reason == "refusal":
        raise LLMRefused(f"{kind} refused")
    if response.stop_reason == "max_tokens":
        raise LLMUnavailable(f"{kind} output truncated")
    text = next((b.text for b in response.content if b.type == "text"), None)
    if text is None:
        raise LLMUnavailable(f"{kind} returned no text")
    return text


def _render_dialogue(dialogue: list[DialogueTurn]) -> str:
    lines = []
    for d in dialogue:
        if d.speaker == "interviewer":
            tag = f"{d.problem_id}/{d.stem_id}{' follow-up' if d.is_followup else ''}"
            lines.append(f"INTERVIEWER [{tag}]: {d.text}")
        else:
            lines.append(f"EXPERT: {d.text}")
    return "\n".join(lines) or "(no questions asked yet)"


class InterviewerLLM:
    def __init__(self, client, log: Callable[[dict], object], system_prompt: str,
                 model: str = INTERVIEWER_MODEL, effort: str = INTERVIEWER_EFFORT):
        self.client, self.log, self.system_prompt = client, log, system_prompt
        self.model, self.effort = model, effort

    def _content(self, req: TurnRequest) -> tuple[list[dict], list[dict]]:
        problems = "\n".join(f"{pid}: {text}" for pid, text in req.problems.items())
        content = [{"type": "text", "text": f"PROBLEMS\n{problems}\n\nTHINK-ALOUD TRANSCRIPT\n{req.transcript}"}]
        loggable = list(content)
        for pid, png in req.snapshots.items():
            label = {"type": "text", "text": f"Written work for {pid}:"}
            content += [label, {"type": "image", "source": {"type": "base64", "media_type": "image/png",
                                                             "data": base64.standard_b64encode(png).decode()}}]
            loggable += [label, {"type": "image", "snapshot": pid, "sha256": hashlib.sha256(png).hexdigest()}]
        content[-1] = {**content[-1], "cache_control": {"type": "ephemeral"}}
        status = [f"PROBE DIALOGUE SO FAR\n{_render_dialogue(req.dialogue)}",
                  f"Time remaining: {int(req.remaining_s)} s.",
                  f"Stems not yet used: {', '.join(req.unused) or 'none'}."]
        if req.wrap_up:
            status.append("Less than two minutes remain: ask at most one more question, "
                          "or end the session if every stem has been used.")
        if req.rejection:
            status.append(f"Your previous proposed turn was rejected ({req.rejection}). Propose a different turn.")
        status.append("Return the next turn.")
        dynamic = {"type": "text", "text": "\n\n".join(status)}
        return content + [dynamic], loggable + [dynamic]

    def next_turn(self, req: TurnRequest) -> InterviewerTurn:
        content, loggable_content = self._content(req)
        params = dict(model=self.model, max_tokens=16000, system=self.system_prompt,
                      thinking={"type": "adaptive"},
                      output_config={"effort": self.effort,
                                     "format": {"type": "json_schema", "schema": INTERVIEWER_TURN_SCHEMA}},
                      messages=[{"role": "user", "content": content}])
        loggable = {**params, "messages": [{"role": "user", "content": loggable_content}]}
        text = _call(self.client, self.log, "interviewer", params, loggable)
        try:
            return InterviewerTurn.model_validate_json(text)
        except ValidationError as e:
            raise LLMUnavailable(f"interviewer output failed validation: {e}") from e


class Guard:
    def __init__(self, client, log: Callable[[dict], object], system_prompt: str, model: str = GUARD_MODEL):
        self.client, self.log, self.system_prompt, self.model = client, log, system_prompt, model

    def check(self, utterance: str, problem_text: str, expert_text: str) -> GuardVerdict:
        user = (f"PROBLEM STATEMENTS\n{problem_text}\n\nEXPERT'S WORDS SO FAR\n{expert_text}\n\n"
                f"PROPOSED QUESTION\n{utterance}")
        params = dict(model=self.model, max_tokens=1024, temperature=0, system=self.system_prompt,
                      output_config={"format": {"type": "json_schema", "schema": GUARD_SCHEMA}},
                      messages=[{"role": "user", "content": user}])
        text = _call(self.client, self.log, "guard", params, params)
        try:
            return GuardVerdict.model_validate_json(text)
        except ValidationError as e:
            raise LLMUnavailable(f"guard output failed validation: {e}") from e
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_llm.py -v`
Expected: 7 passed.

- [ ] **Step 5: Commit**

```bash
git add instrument/src/probe_app/llm.py instrument/tests/fakes.py instrument/tests/test_llm.py
git commit -m "Instrument: interviewer and guard Claude clients with full request logging"
```

---

### Task 6: Probe engine

**Files:**
- Create: `instrument/src/probe_app/engine.py`
- Test: `instrument/tests/test_engine.py`

**Interfaces:**
- Consumes: `ContractState`, `check_turn`, `record`, `uncovered`, `next_fallback`, `ContractViolation` (Task 4); `TurnRequest`, `LLMRefused`, `LLMUnavailable` (Task 5); `render_transcript` (Task 3); models (Task 2); `SessionStore.log` (Task 2).
- Produces: `@dataclass ProbeContext(set_id: str, problems: dict[str, str], segments: list[Segment], snapshots: dict[str, bytes])`; `ProbeEngine(llm, guard, stems: dict[str, str], ctx: ProbeContext, store, contract: ContractState, cap_s: float, wrap_s: float)` with `.next_turn(dialogue: list[DialogueTurn], elapsed_s: float) -> DialogueTurn | None` (`None` means the probe session is over). `llm` needs only `.next_turn(TurnRequest) -> InterviewerTurn`; `guard` needs only `.check(utterance, problem_text, expert_text) -> GuardVerdict`.

- [ ] **Step 1: Write the failing test**

`instrument/tests/test_engine.py`:

```python
import pytest

from probe_app.config import load_stems
from probe_app.contract import ContractState
from probe_app.engine import ProbeContext, ProbeEngine
from probe_app.llm import LLMRefused, LLMUnavailable
from probe_app.models import STEMS, Anchor, DialogueTurn, GuardVerdict, InterviewerTurn, Segment
from probe_app.storage import SessionStore

SEGS = [Segment(id="A1-s001", problem_id="A1", start=0, end=1, text="Clearly they stick together.")]


class ScriptedLLM:
    def __init__(self, items):
        self.items, self.requests = list(items), []

    def next_turn(self, req):
        self.requests.append(req)
        item = self.items.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


class ScriptedGuard:
    def __init__(self, flags=()):
        self.flags = list(flags)

    def check(self, utterance, problem_text, expert_text):
        flagged = self.flags.pop(0) if self.flags else False
        return GuardVerdict(flagged=flagged, introduced="units" if flagged else "")


def t(**kw) -> InterviewerTurn:
    base = dict(utterance="What did you notice?", stem_id="cues", problem_id="A1",
                anchor=Anchor(kind="segments", segment_ids=["A1-s001"]),
                is_followup=False, quoted_span=None, end_session=False)
    base.update(kw)
    return InterviewerTurn(**base)


def make(tmp_path, llm, guard=None, segments=SEGS, problems=("A1",)):
    store = SessionStore.create(tmp_path, {"expert_id": "E01"})
    ctx = ProbeContext(set_id="A", problems={p: f"statement {p}" for p in problems},
                       segments=segments, snapshots={})
    contract = ContractState(problems=list(problems))
    engine = ProbeEngine(llm, guard or ScriptedGuard(), load_stems(), ctx, store, contract, cap_s=1200, wrap_s=1080)
    return engine, store, contract


def types(store):
    return [e["type"] for e in store.events()]


def test_valid_turn_is_emitted_and_recorded(tmp_path):
    engine, store, contract = make(tmp_path, ScriptedLLM([t()]))
    out = engine.next_turn([], 0.0)
    assert out.source == "ai" and out.stem_id == "cues"
    assert contract.used == {"A1/cues": 1}
    assert "probe" in types(store)


def test_contract_violation_regenerates_with_reason(tmp_path):
    llm = ScriptedLLM([t(problem_id="B9"), t()])
    engine, store, _ = make(tmp_path, llm)
    out = engine.next_turn([], 0.0)
    assert out.source == "ai"
    assert "problem B9" in llm.requests[1].rejection
    assert types(store).count("turn_rejected") == 1


def test_guard_flag_twice_falls_back_to_bare_stem(tmp_path):
    engine, store, contract = make(tmp_path, ScriptedLLM([t(), t()]), ScriptedGuard([True, True]))
    out = engine.next_turn([], 0.0)
    assert out.source == "ai_fallback"
    assert out.text == load_stems()["cues"]
    assert out.anchor.kind == "none"
    assert types(store).count("turn_rejected") == 2


def test_refusal_and_outage_fall_back(tmp_path):
    for exc in (LLMRefused("r"), LLMUnavailable("u")):
        engine, _, _ = make(tmp_path / type(exc).__name__, ScriptedLLM([exc]))
        assert engine.next_turn([], 0.0).source == "ai_fallback"


def test_cap_ends_session(tmp_path):
    engine, store, _ = make(tmp_path, ScriptedLLM([]))
    assert engine.next_turn([], 1200.0) is None
    assert "cap_reached" in types(store)


def test_wrap_up_flag_from_1080s(tmp_path):
    llm = ScriptedLLM([t(), t(stem_id="checks")])
    engine, _, _ = make(tmp_path, llm)
    engine.next_turn([], 1079.0)
    engine.next_turn([], 1080.0)
    assert [r.wrap_up for r in llm.requests] == [False, True]


def test_end_session_after_coverage(tmp_path):
    turns = [t(stem_id=s, anchor=Anchor(kind="none", segment_ids=[])) for s in STEMS] + [t(end_session=True)]
    engine, store, _ = make(tmp_path, ScriptedLLM(turns))
    for _ in STEMS:
        assert engine.next_turn([], 0.0) is not None
    assert engine.next_turn([], 0.0) is None
    assert "session_ended_by_interviewer" in types(store)


def test_followup_quote_checked_against_answers(tmp_path):
    answer = DialogueTurn(speaker="expert", text="I just knew it was inelastic.", t=5.0)
    fu = t(is_followup=True, quoted_span="just knew it was inelastic")
    engine, _, _ = make(tmp_path, ScriptedLLM([t(), fu]))
    first = engine.next_turn([], 0.0)
    assert engine.next_turn([first, answer], 10.0).is_followup


def test_runs_with_empty_trace_and_empty_answer(tmp_path):
    canvas = t(anchor=Anchor(kind="canvas", segment_ids=[]))
    engine, _, _ = make(tmp_path, ScriptedLLM([canvas, t(stem_id="checks", anchor=Anchor(kind="canvas", segment_ids=[]))]), segments=[])
    first = engine.next_turn([], 0.0)
    silent = DialogueTurn(speaker="expert", text="", t=4.0)
    assert engine.next_turn([first, silent], 8.0).stem_id == "checks"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_engine.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'probe_app.engine'`.

- [ ] **Step 3: Write the implementation**

`instrument/src/probe_app/engine.py`:

```python
from dataclasses import dataclass

from probe_app.contract import (ContractState, ContractViolation, check_turn, next_fallback,
                                record, uncovered)
from probe_app.llm import LLMRefused, LLMUnavailable, TurnRequest
from probe_app.models import Anchor, DialogueTurn, InterviewerTurn, Segment
from probe_app.trace import render_transcript


@dataclass
class ProbeContext:
    set_id: str
    problems: dict[str, str]
    segments: list[Segment]
    snapshots: dict[str, bytes]


class ProbeEngine:
    def __init__(self, llm, guard, stems: dict[str, str], ctx: ProbeContext, store,
                 contract: ContractState, cap_s: float, wrap_s: float):
        self.llm, self.guard, self.stems, self.ctx = llm, guard, stems, ctx
        self.store, self.contract, self.cap_s, self.wrap_s = store, contract, cap_s, wrap_s

    def _expert_text(self, dialogue: list[DialogueTurn]) -> str:
        return "\n".join([s.text for s in self.ctx.segments] +
                         [d.text for d in dialogue if d.speaker == "expert"])

    def _problem_text(self) -> str:
        return "\n".join(f"{pid}: {text}" for pid, text in self.ctx.problems.items())

    def next_turn(self, dialogue: list[DialogueTurn], elapsed_s: float) -> DialogueTurn | None:
        set_id = self.ctx.set_id
        if elapsed_s >= self.cap_s:
            self.store.log("cap_reached", set_id=set_id, uncovered=uncovered(self.contract))
            return None
        expert_text = self._expert_text(dialogue)
        rejection = None
        for attempt in (1, 2):
            request = TurnRequest(problems=self.ctx.problems, transcript=render_transcript(self.ctx.segments),
                                  snapshots=self.ctx.snapshots, dialogue=dialogue,
                                  remaining_s=self.cap_s - elapsed_s, wrap_up=elapsed_s >= self.wrap_s,
                                  unused=uncovered(self.contract), rejection=rejection)
            try:
                turn = self.llm.next_turn(request)
            except (LLMRefused, LLMUnavailable) as e:
                self.store.log("interviewer_failed", set_id=set_id, attempt=attempt, reason=repr(e))
                break
            try:
                check_turn(turn, self.contract, self.ctx.segments, expert_text)
            except ContractViolation as e:
                rejection = f"contract: {e}"
                self.store.log("turn_rejected", set_id=set_id, attempt=attempt, reason=rejection,
                               turn=turn.model_dump())
                continue
            if turn.end_session:
                self.store.log("session_ended_by_interviewer", set_id=set_id, closing=turn.utterance)
                return None
            try:
                verdict = self.guard.check(turn.utterance, self._problem_text(), expert_text)
            except (LLMRefused, LLMUnavailable) as e:
                self.store.log("guard_failed", set_id=set_id, attempt=attempt, reason=repr(e))
                break
            if verdict.flagged:
                rejection = f"leading: it introduces '{verdict.introduced}', which the expert has not said"
                self.store.log("turn_rejected", set_id=set_id, attempt=attempt, reason=rejection,
                               turn=turn.model_dump())
                continue
            record(turn, self.contract)
            return self._emit(turn, "ai", elapsed_s)
        return self._fallback(elapsed_s)

    def _fallback(self, elapsed_s: float) -> DialogueTurn | None:
        nxt = next_fallback(self.contract)
        if nxt is None:
            self.store.log("session_ended_after_fallback", set_id=self.ctx.set_id)
            return None
        problem_id, stem_id = nxt
        turn = InterviewerTurn(utterance=self.stems[stem_id], stem_id=stem_id, problem_id=problem_id,
                               anchor=Anchor(kind="none", segment_ids=[]), is_followup=False,
                               quoted_span=None, end_session=False)
        record(turn, self.contract)
        return self._emit(turn, "ai_fallback", elapsed_s)

    def _emit(self, turn: InterviewerTurn, source: str, elapsed_s: float) -> DialogueTurn:
        out = DialogueTurn(speaker="interviewer", text=turn.utterance, t=elapsed_s, stem_id=turn.stem_id,
                           problem_id=turn.problem_id, is_followup=turn.is_followup, anchor=turn.anchor,
                           source=source)
        self.store.log("probe", set_id=self.ctx.set_id, turn=out.model_dump(mode="json"))
        return out
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_engine.py -v`
Expected: 9 passed.

- [ ] **Step 5: Commit**

```bash
git add instrument/src/probe_app/engine.py instrument/tests/test_engine.py
git commit -m "Instrument: probe engine — generate, check, guard, regenerate once, bare-stem fallback"
```

---

### Task 7: Session state machine and human-arm dialogue

**Files:**
- Create: `instrument/src/probe_app/human.py`, `instrument/src/probe_app/session.py`
- Test: `instrument/tests/test_human.py`, `instrument/tests/test_session.py`

**Interfaces:**
- Consumes: everything from Tasks 1–6.
- Produces (human): `turns_from_markers(raw: list[RawSegment], markers: list[dict], ticks: list[dict]) -> list[DialogueTurn]` (markers `{"speaker", "t"}`, ticks `{"problem_id", "stem_id", "t"}`).
- Produces (session): `class PhaseError(Exception)`, `class DuplicateSubmission(Exception)`; `@dataclass Deps(transcriber, anthropic_client)`; `ProbeTimer`; `SessionState`; `Session` with `Session.create(root, deps, *, expert_id: str, cell: int, arms: dict[str, str], set_order: list[str], pilot: bool, simulated: bool = False, clock=None) -> Session`, `Session.load(root, session_id, deps, clock=None) -> Session`, `.store`, `.state`, `.start_think_aloud() -> str`, `.keep_talking()`, `.end_think_aloud(problem_id: str, audio: bytes, snapshot_png: bytes, strokes: list)`, `.correct_segment(segment_id: str, text: str)`, `.add_segment(problem_id: str, text: str)`, `.start_probe() -> str`, `.answer_ai_audio(turn_index: int, audio: bytes)`, `.answer_ai_text(turn_index: int, text: str, source: str = "typed")`, `.human_marker(speaker: str)`, `.human_stem(problem_id: str, stem_id: str)`, `.push_anchor(problem_id: str, anchor: Anchor)`, `.end_probe()`, `.upload_human_probe(set_id: str, audio: bytes)`, `.pause()`, `.resume()`, `.elapsed() -> float`, `.expert_view() -> dict`, `.console_view() -> dict`, `.snapshot_path(problem_id: str) -> Path`.

- [ ] **Step 1: Write the failing tests**

`instrument/tests/test_human.py`:

```python
from probe_app.human import turns_from_markers
from probe_app.transcribe import RawSegment


def test_turns_split_by_markers_and_ticks_attach():
    raw = [RawSegment(start=0.5, end=2, text="Tell me about the collision."),
           RawSegment(start=3, end=5, text="Well, they stick."),
           RawSegment(start=5, end=6, text="So momentum."),
           RawSegment(start=7, end=8, text="How did you check it?")]
    markers = [{"speaker": "interviewer", "t": 0.0}, {"speaker": "expert", "t": 2.5},
               {"speaker": "interviewer", "t": 6.5}]
    ticks = [{"problem_id": "A1", "stem_id": "cues", "t": 1.0}, {"problem_id": "A1", "stem_id": "checks", "t": 7.5}]
    turns = turns_from_markers(raw, markers, ticks)
    assert [(x.speaker, x.text) for x in turns] == [
        ("interviewer", "Tell me about the collision."),
        ("expert", "Well, they stick. So momentum."),
        ("interviewer", "How did you check it?")]
    assert (turns[0].stem_id, turns[2].stem_id) == ("cues", "checks")
    assert turns[0].source == "human" and turns[1].source == "transcribed"
```

`instrument/tests/test_session.py`:

```python
import pytest

from fakes import FakeAnthropic, FakeClock, FakeResponse, FakeTranscriber, turn_payload
from probe_app.config import ConfigMismatch
from probe_app.models import Anchor
from probe_app.session import Deps, DuplicateSubmission, PhaseError, Session
from probe_app.transcribe import RawSegment

PNG = bytes.fromhex("89504e470d0a1a0a")


def seg(text, start=0.0):
    return [RawSegment(start=start, end=start + 1, text=text)]


def new_session(tmp_path, interviewer=(), transcripts=(), arms=None, clock=None):
    deps = Deps(FakeTranscriber(list(transcripts)), FakeAnthropic(interviewer=list(interviewer)))
    return Session.create(tmp_path, deps, expert_id="E01", cell=1, arms=arms or {"A": "ai", "B": "human"},
                          set_order=["A", "B"], pilot=True, clock=clock or FakeClock())


def through_think_aloud(s):
    while s.state.phase == "ready":
        pid = s.start_think_aloud()
        s.end_think_aloud(pid, b"audio", PNG, [{"points": [[0, 0, 0]]}])


def test_think_aloud_order_and_trace(tmp_path):
    s = new_session(tmp_path, transcripts=[seg("A1 talk"), seg("A2 talk"), seg("B1 talk"), seg("B2 talk")])
    through_think_aloud(s)
    assert s.state.think_aloud_done == ["A1", "A2", "B1", "B2"]
    assert s.state.phase == "trace_review"
    assert [x.id for x in s.state.segments][:2] == ["A1-s001", "A2-s001"]
    assert s.snapshot_path("A1").read_bytes() == PNG


def test_data_session_refuses_without_prereg(tmp_path, monkeypatch):
    monkeypatch.setattr("probe_app.session.PREREG_PATH", tmp_path / "none.json")
    deps = Deps(FakeTranscriber([]), FakeAnthropic())
    with pytest.raises(ConfigMismatch):
        Session.create(tmp_path, deps, expert_id="E01", cell=1, arms={"A": "ai", "B": "human"},
                       set_order=["A", "B"], pilot=False)


def test_failed_transcription_sets_error_and_allows_typing(tmp_path):
    s = new_session(tmp_path, transcripts=[RuntimeError("x")] * 3 + [seg("A2"), seg("B1"), seg("B2")])
    pid = s.start_think_aloud()
    s.end_think_aloud(pid, b"a", PNG, [])
    assert "A1" in s.state.error
    s.add_segment("A1", "typed transcript")
    assert s.state.segments[-1].id == "A1-m001" and s.state.error is None


def test_ai_probe_flow_and_duplicate_answer(tmp_path):
    clock = FakeClock()
    s = new_session(tmp_path, interviewer=[FakeResponse(turn_payload()), FakeResponse(turn_payload(stem_id="checks"))],
                    transcripts=[seg("A1"), seg("A2"), seg("B1"), seg("B2"), seg("Because they stick.")], clock=clock)
    through_think_aloud(s)
    assert s.start_probe() == "A"
    view = s.expert_view()
    assert view["question"] == "What did you notice first?" and view["expected_answer_index"] == 1
    clock.advance(30)
    s.answer_ai_audio(1, b"answer")
    d = s.state.dialogue["A"]
    assert [x.speaker for x in d] == ["interviewer", "expert", "interviewer"]
    assert d[1].text == "Because they stick." and d[1].t == 30
    with pytest.raises(DuplicateSubmission):
        s.answer_ai_audio(1, b"answer")
    assert len(s.state.dialogue["A"]) == 3


def test_silent_answer_passes_empty_text(tmp_path):
    s = new_session(tmp_path, interviewer=[FakeResponse(turn_payload()), FakeResponse(turn_payload(stem_id="checks"))],
                    transcripts=[seg("A1"), seg("A2"), seg("B1"), seg("B2"), []])
    through_think_aloud(s)
    s.start_probe()
    s.answer_ai_audio(1, b"silence")
    assert s.state.dialogue["A"][1].text == ""
    assert s.state.dialogue["A"][2].stem_id == "checks"


def test_failed_answer_transcription_waits_for_typed_answer(tmp_path):
    s = new_session(tmp_path, interviewer=[FakeResponse(turn_payload()), FakeResponse(turn_payload(stem_id="checks"))],
                    transcripts=[seg("A1"), seg("A2"), seg("B1"), seg("B2")] + [RuntimeError("x")] * 3)
    through_think_aloud(s)
    s.start_probe()
    s.answer_ai_audio(1, b"a")
    assert len(s.state.dialogue["A"]) == 1 and "type it" in s.state.error
    s.answer_ai_text(1, "I saw they stick.")
    assert s.state.dialogue["A"][1].source == "typed" and len(s.state.dialogue["A"]) == 3


def test_reload_resumes_same_question(tmp_path):
    s = new_session(tmp_path, interviewer=[FakeResponse(turn_payload())],
                    transcripts=[seg("A1"), seg("A2"), seg("B1"), seg("B2")])
    through_think_aloud(s)
    s.start_probe()
    again = Session.load(tmp_path, s.store.session_id, s.deps)
    assert again.expert_view()["question"] == s.expert_view()["question"]
    assert again.state.contract["A"].used == {"A1/cues": 1}


def test_pause_stops_timer(tmp_path):
    clock = FakeClock()
    s = new_session(tmp_path, interviewer=[FakeResponse(turn_payload())],
                    transcripts=[seg("A1"), seg("A2"), seg("B1"), seg("B2")], clock=clock)
    through_think_aloud(s)
    s.start_probe()
    clock.advance(10); s.pause(); clock.advance(100); s.resume(); clock.advance(5)
    assert s.elapsed() == 15


def test_human_arm_markers_upload_and_finish(tmp_path):
    clock = FakeClock()
    s = new_session(tmp_path, arms={"A": "human", "B": "ai"}, clock=clock,
                    transcripts=[seg("A1"), seg("A2"), seg("B1"), seg("B2"),
                                 [RawSegment(start=0.2, end=1, text="What did you see?"),
                                  RawSegment(start=2, end=3, text="The stick.")]])
    through_think_aloud(s)
    s.start_probe()
    s.human_marker("interviewer"); s.human_stem("A1", "cues")
    clock.advance(1.5); s.human_marker("expert")
    s.push_anchor("A1", Anchor(kind="segments", segment_ids=["A1-s001"]))
    assert s.expert_view()["anchor_view"]["text"] == "A1"
    with pytest.raises(PhaseError):
        s.answer_ai_text(0, "x")
    s.end_probe()
    assert s.state.phase == "probe_uploading"
    s.upload_human_probe("A", b"audio")
    assert [x.speaker for x in s.state.dialogue["A"]] == ["interviewer", "expert"]
    assert s.state.dialogue["A"][0].stem_id == "cues"
    assert s.state.phase == "trace_review" and s.state.probes_done == ["A"]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_human.py tests/test_session.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'probe_app.human'`.

- [ ] **Step 3: Write `human.py`**

```python
from probe_app.models import DialogueTurn
from probe_app.transcribe import RawSegment


def turns_from_markers(raw: list[RawSegment], markers: list[dict], ticks: list[dict]) -> list[DialogueTurn]:
    marks = sorted(markers, key=lambda m: m["t"])
    turns: list[DialogueTurn] = []
    for seg in raw:
        speaker = "interviewer"
        for m in marks:
            if m["t"] > seg.start:
                break
            speaker = m["speaker"]
        if turns and turns[-1].speaker == speaker:
            turns[-1].text = f"{turns[-1].text} {seg.text}"
        else:
            turns.append(DialogueTurn(speaker=speaker, text=seg.text, t=seg.start,
                                      source="human" if speaker == "interviewer" else "transcribed"))
    for tick in sorted(ticks, key=lambda x: x["t"]):
        earlier = [x for x in turns if x.speaker == "interviewer" and x.t <= tick["t"]]
        if earlier and earlier[-1].stem_id is None:
            earlier[-1].stem_id, earlier[-1].problem_id = tick["stem_id"], tick["problem_id"]
    return turns
```

- [ ] **Step 4: Write `session.py`**

```python
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from probe_app.config import (CAP_S, PREREG_PATH, WRAP_S, check_preregistered, current_config, git_commit,
                              load_problems, load_prompt, load_stems)
from probe_app.contract import ContractState, uncovered
from probe_app.engine import ProbeContext, ProbeEngine
from probe_app.human import turns_from_markers
from probe_app.llm import Guard, InterviewerLLM
from probe_app.models import STEMS, Anchor, DialogueTurn, Segment
from probe_app.storage import SessionStore
from probe_app.trace import build_segments, correct_segment
from probe_app.transcribe import TranscriptionFailed, transcribe_with_retry


class PhaseError(Exception):
    pass


class DuplicateSubmission(Exception):
    pass


@dataclass
class Deps:
    transcriber: object
    anthropic_client: object


class ProbeTimer(BaseModel):
    started: float | None = None
    paused_total: float = 0.0
    paused_since: float | None = None

    def elapsed(self, now: float) -> float:
        if self.started is None:
            return 0.0
        end = self.paused_since if self.paused_since is not None else now
        return end - self.started - self.paused_total


class SessionState(BaseModel):
    phase: Literal["ready", "think_aloud", "trace_review", "probe", "probe_uploading", "done"] = "ready"
    sets: dict[str, list[str]]
    set_order: list[str]
    arms: dict[str, Literal["ai", "human"]]
    current_problem: str | None = None
    current_set: str | None = None
    recording_start: float | None = None
    think_aloud_done: list[str] = []
    probes_done: list[str] = []
    segments: list[Segment] = []
    dialogue: dict[str, list[DialogueTurn]] = {}
    contract: dict[str, ContractState] = {}
    timer: ProbeTimer = ProbeTimer()
    anchor: Anchor | None = None
    anchor_problem: str | None = None
    markers: dict[str, list[dict]] = {}
    ticks: dict[str, list[dict]] = {}
    paused: bool = False
    error: str | None = None

    @property
    def problem_order(self) -> list[str]:
        return [p for s in self.set_order for p in self.sets[s]]


class Session:
    def __init__(self, store: SessionStore, state: SessionState, deps: Deps):
        self.store, self.state, self.deps = store, state, deps
        self.problems = load_problems()
        self.stems = load_stems()
        self.manifest = store.manifest

    @classmethod
    def create(cls, root: Path, deps: Deps, *, expert_id: str, cell: int, arms: dict[str, str],
               set_order: list[str], pilot: bool, simulated: bool = False, clock=None) -> "Session":
        problems = load_problems()
        if sorted(set_order) != sorted(problems["sets"]) or set(arms) != set(set_order):
            raise ValueError(f"set_order and arms must cover exactly the sets {sorted(problems['sets'])}")
        if not set(arms.values()) <= {"ai", "human"}:
            raise ValueError("arms must be 'ai' or 'human'")
        cfg = current_config()
        if not pilot:
            check_preregistered(cfg, PREREG_PATH)
        manifest = {"expert_id": expert_id, "cell": cell, "arms": arms, "set_order": set_order,
                    "pilot": pilot, "simulated": simulated, "cap_s": CAP_S, "wrap_s": WRAP_S,
                    "config": asdict(cfg), "transcriber": deps.transcriber.model, "git_commit": git_commit()}
        store = SessionStore.create(root, manifest, clock)
        state = SessionState(sets={s: problems["sets"][s] for s in set_order}, set_order=set_order, arms=arms)
        session = cls(store, state, deps)
        store.log("session_created")
        session.save()
        return session

    @classmethod
    def load(cls, root: Path, session_id: str, deps: Deps, clock=None) -> "Session":
        store = SessionStore(root, session_id, clock)
        return cls(store, SessionState.model_validate(store.read_json("state.json")), deps)

    def save(self) -> None:
        self.store.write_json("state.json", self.state.model_dump(mode="json"))

    def _now(self) -> float:
        return self.store.clock.now()

    def _require(self, *phases: str) -> None:
        if self.state.phase not in phases:
            raise PhaseError(f"this action needs phase {phases}; the session is in '{self.state.phase}'")

    def elapsed(self) -> float:
        return self.state.timer.elapsed(self._now())

    def snapshot_path(self, problem_id: str) -> Path:
        return self.store.path(f"canvas/snapshots/{problem_id}.png")

    def _arm(self) -> str | None:
        return self.state.arms[self.state.current_set] if self.state.current_set else None

    # think-aloud

    def start_think_aloud(self) -> str:
        self._require("ready")
        pid = next(p for p in self.state.problem_order if p not in self.state.think_aloud_done)
        self.state.phase, self.state.current_problem, self.state.recording_start = "think_aloud", pid, self._now()
        self.store.log("think_aloud_started", problem_id=pid)
        self.save()
        return pid

    def keep_talking(self) -> None:
        self._require("think_aloud")
        self.store.log("keep_talking", problem_id=self.state.current_problem)

    def end_think_aloud(self, problem_id: str, audio: bytes, snapshot_png: bytes, strokes: list) -> None:
        self._require("think_aloud")
        if problem_id != self.state.current_problem:
            raise PhaseError(f"current problem is {self.state.current_problem}, not {problem_id}")
        audio_path = self.store.path(f"audio/think_{problem_id}.webm")
        audio_path.write_bytes(audio)
        self.snapshot_path(problem_id).write_bytes(snapshot_png)
        self.store.write_json(f"canvas/strokes_{problem_id}.json", strokes)
        self.store.log("think_aloud_ended", problem_id=problem_id, n_strokes=len(strokes))
        try:
            raw = transcribe_with_retry(self.deps.transcriber, audio_path)
            self.store.write_json(f"transcripts/think_{problem_id}.raw.json", [r.model_dump() for r in raw])
            self.state.segments += build_segments(problem_id, self.state.recording_start, raw)
        except TranscriptionFailed as e:
            self.state.error = f"Transcription failed for {problem_id}: {e}. Type the transcript in the console."
            self.store.log("transcription_failed", problem_id=problem_id, error=str(e))
        self.state.think_aloud_done.append(problem_id)
        self.state.current_problem = None
        remaining = [p for p in self.state.problem_order if p not in self.state.think_aloud_done]
        self.state.phase = "ready" if remaining else "trace_review"
        self.save()

    def correct_segment(self, segment_id: str, text: str) -> None:
        self._require("ready", "trace_review")
        self.state.segments, diff = correct_segment(self.state.segments, segment_id, text)
        self.store.log("segment_corrected", **diff)
        self.save()

    def add_segment(self, problem_id: str, text: str) -> None:
        self._require("ready", "trace_review")
        if problem_id not in self.state.think_aloud_done:
            raise PhaseError(f"{problem_id} has no think-aloud yet")
        n = sum(1 for s in self.state.segments if s.id.startswith(f"{problem_id}-m")) + 1
        segment = Segment(id=f"{problem_id}-m{n:03d}", problem_id=problem_id, start=0.0, end=0.0, text=text)
        self.state.segments.append(segment)
        self.state.error = None
        self.store.log("segment_added", **segment.model_dump())
        self.save()

    # probe

    def _engine(self, set_id: str) -> ProbeEngine:
        client = self.deps.anthropic_client
        llm = InterviewerLLM(client, self.store.log_llm, load_prompt("interviewer_system.md"))
        guard = Guard(client, self.store.log_llm, load_prompt("guard_system.md"))
        pids = self.state.sets[set_id]
        snapshots = {p: self.snapshot_path(p).read_bytes() for p in pids if self.snapshot_path(p).exists()}
        ctx = ProbeContext(set_id=set_id,
                           problems={p: self.problems["problems"][p]["statement"] for p in pids},
                           segments=[s for s in self.state.segments if s.problem_id in pids],
                           snapshots=snapshots)
        return ProbeEngine(llm, guard, self.stems, ctx, self.store, self.state.contract[set_id],
                           cap_s=self.manifest["cap_s"], wrap_s=self.manifest["wrap_s"])

    def start_probe(self) -> str:
        self._require("trace_review")
        st = self.state
        set_id = next(s for s in st.set_order if s not in st.probes_done)
        st.phase, st.current_set = "probe", set_id
        st.timer = ProbeTimer(started=self._now())
        st.contract[set_id] = ContractState(problems=st.sets[set_id])
        st.dialogue[set_id], st.markers[set_id], st.ticks[set_id] = [], [], []
        st.anchor = st.anchor_problem = None
        self.store.log("probe_started", set_id=set_id, arm=st.arms[set_id])
        if st.arms[set_id] == "ai":
            self._advance_ai()
        self.save()
        return set_id

    def _advance_ai(self) -> None:
        set_id = self.state.current_set
        turn = self._engine(set_id).next_turn(self.state.dialogue[set_id], self.elapsed())
        if turn is None:
            self._finish_probe()
            return
        self.state.dialogue[set_id].append(turn)
        self.state.anchor, self.state.anchor_problem = turn.anchor, turn.problem_id

    def _check_answer(self, turn_index: int) -> None:
        self._require("probe")
        if self._arm() != "ai":
            raise PhaseError("per-turn answers exist only in the AI arm")
        if self.state.paused:
            raise PhaseError("the session is paused")
        expected = len(self.state.dialogue[self.state.current_set])
        if turn_index != expected:
            raise DuplicateSubmission(f"expected answer {expected}, got {turn_index}")

    def answer_ai_audio(self, turn_index: int, audio: bytes) -> None:
        self._check_answer(turn_index)
        set_id = self.state.current_set
        path = self.store.path(f"audio/answer_{set_id}_{turn_index:03d}.webm")
        path.write_bytes(audio)
        try:
            raw = transcribe_with_retry(self.deps.transcriber, path)
        except TranscriptionFailed as e:
            self.state.error = f"Answer {turn_index} could not be transcribed: type it from {path.name} in the console."
            self.store.log("transcription_failed", set_id=set_id, turn_index=turn_index, error=str(e))
            self.save()
            return
        self.store.write_json(f"transcripts/answer_{set_id}_{turn_index:03d}.raw.json", [r.model_dump() for r in raw])
        self._accept_answer(" ".join(r.text for r in raw), "transcribed")

    def answer_ai_text(self, turn_index: int, text: str, source: str = "typed") -> None:
        self._check_answer(turn_index)
        self.state.error = None
        self._accept_answer(text, source)

    def _accept_answer(self, text: str, source: str) -> None:
        set_id = self.state.current_set
        answer = DialogueTurn(speaker="expert", text=text, t=self.elapsed(), source=source)
        self.state.dialogue[set_id].append(answer)
        self.store.log("expert_answer", set_id=set_id, turn=answer.model_dump(mode="json"))
        self._advance_ai()
        self.save()

    def _require_human_probe(self) -> str:
        self._require("probe")
        if self._arm() != "human":
            raise PhaseError("this control exists only in the human arm")
        return self.state.current_set

    def human_marker(self, speaker: str) -> None:
        set_id = self._require_human_probe()
        if speaker not in ("interviewer", "expert"):
            raise ValueError("speaker must be 'interviewer' or 'expert'")
        mark = {"speaker": speaker, "t": self.elapsed()}
        self.state.markers[set_id].append(mark)
        self.store.log("turn_marker", set_id=set_id, **mark)
        self.save()

    def human_stem(self, problem_id: str, stem_id: str) -> None:
        set_id = self._require_human_probe()
        if problem_id not in self.state.sets[set_id] or stem_id not in STEMS:
            raise ValueError(f"unknown problem or stem: {problem_id}/{stem_id}")
        tick = {"problem_id": problem_id, "stem_id": stem_id, "t": self.elapsed()}
        self.state.ticks[set_id].append(tick)
        self.store.log("stem_ticked", set_id=set_id, **tick)
        self.save()

    def push_anchor(self, problem_id: str, anchor: Anchor) -> None:
        set_id = self._require_human_probe()
        if problem_id not in self.state.sets[set_id]:
            raise ValueError(f"{problem_id} is not in set {set_id}")
        owner = {s.id: s.problem_id for s in self.state.segments}
        if any(owner.get(i) != problem_id for i in anchor.segment_ids):
            raise ValueError("anchor segments must belong to the problem")
        self.state.anchor, self.state.anchor_problem = anchor, problem_id
        self.store.log("anchor_pushed", set_id=set_id, problem_id=problem_id, anchor=anchor.model_dump())
        self.save()

    def end_probe(self) -> None:
        self._require("probe")
        self.store.log("probe_end_requested", set_id=self.state.current_set, elapsed=self.elapsed())
        if self._arm() == "ai":
            self._finish_probe()
        else:
            self.state.phase = "probe_uploading"
        self.save()

    def upload_human_probe(self, set_id: str, audio: bytes) -> None:
        self._require("probe_uploading")
        if set_id != self.state.current_set:
            raise PhaseError(f"current set is {self.state.current_set}, not {set_id}")
        path = self.store.path(f"audio/probe_{set_id}.webm")
        path.write_bytes(audio)
        try:
            raw = transcribe_with_retry(self.deps.transcriber, path)
            self.store.write_json(f"transcripts/probe_{set_id}.raw.json", [r.model_dump() for r in raw])
            self.state.dialogue[set_id] = turns_from_markers(raw, self.state.markers[set_id], self.state.ticks[set_id])
        except TranscriptionFailed as e:
            self.state.error = f"Probe audio for set {set_id} could not be transcribed; it is saved as {path.name}."
            self.store.log("transcription_failed", set_id=set_id, error=str(e))
        self._finish_probe()
        self.save()

    def _finish_probe(self) -> None:
        st = self.state
        set_id = st.current_set
        elapsed = self.elapsed()
        if st.timer.paused_since is None:
            st.timer.paused_since = self._now()
        missing = (uncovered(st.contract[set_id]) if st.arms[set_id] == "ai" else
                   [f"{p}/{s}" for p in st.sets[set_id] for s in STEMS
                    if not any(t["problem_id"] == p and t["stem_id"] == s for t in st.ticks[set_id])])
        self.store.log("probe_finished", set_id=set_id, elapsed=elapsed, uncovered=missing)
        st.probes_done.append(set_id)
        st.current_set, st.anchor, st.anchor_problem, st.paused = None, None, None, False
        st.phase = "trace_review" if len(st.probes_done) < len(st.set_order) else "done"

    def pause(self) -> None:
        self._require("probe")
        if not self.state.paused:
            self.state.paused, self.state.timer.paused_since = True, self._now()
            self.store.log("paused", elapsed=self.elapsed())
            self.save()

    def resume(self) -> None:
        if self.state.paused:
            timer = self.state.timer
            timer.paused_total += self._now() - timer.paused_since
            timer.paused_since, self.state.paused = None, False
            self.store.log("resumed", elapsed=self.elapsed())
            self.save()

    # views

    def _anchor_view(self) -> dict | None:
        anchor, pid = self.state.anchor, self.state.anchor_problem
        if anchor is None or anchor.kind == "none" or pid is None:
            return None
        if anchor.kind == "canvas":
            return {"kind": "canvas", "image_url": f"/api/sessions/{self.store.session_id}/snapshot/{pid}"}
        texts = {s.id: s.text for s in self.state.segments}
        return {"kind": "segments", "text": " … ".join(texts[i] for i in anchor.segment_ids if i in texts)}

    def expert_view(self) -> dict:
        st = self.state
        view = {"phase": st.phase, "current_problem": st.current_problem, "current_set": st.current_set,
                "arm": self._arm(), "paused": st.paused, "question": None, "expected_answer_index": None,
                "anchor_view": None, "problem_text": None}
        if st.current_problem:
            view["problem_text"] = self.problems["problems"][st.current_problem]["statement"]
        if st.phase == "probe":
            dialogue = st.dialogue[st.current_set]
            if self._arm() == "ai" and dialogue and dialogue[-1].speaker == "interviewer":
                view["question"] = dialogue[-1].text
                view["expected_answer_index"] = len(dialogue)
            view["anchor_view"] = self._anchor_view()
        return view

    def console_view(self) -> dict:
        st = self.state
        return {"session_id": self.store.session_id, "manifest": self.manifest,
                "state": st.model_dump(mode="json"), "expert_view": self.expert_view(),
                "elapsed": self.elapsed(), "remaining": self.manifest["cap_s"] - self.elapsed(),
                "stems": self.stems,
                "problems": {p: self.problems["problems"][p]["statement"] for p in st.problem_order},
                "uncovered": uncovered(st.contract[st.current_set]) if st.current_set and self._arm() == "ai" else None}
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `uv run pytest tests/test_human.py tests/test_session.py -v`
Expected: 10 passed.

- [ ] **Step 6: Commit**

```bash
git add instrument/src/probe_app/human.py instrument/src/probe_app/session.py instrument/tests/test_human.py instrument/tests/test_session.py
git commit -m "Instrument: session state machine for think-aloud, AI and human probe arms"
```

---

### Task 8: HTTP server

**Files:**
- Create: `instrument/src/probe_app/server.py`
- Test: `instrument/tests/test_server.py`

**Interfaces:**
- Consumes: `Session`, `Deps`, `PhaseError`, `DuplicateSubmission` (Task 7); `ConfigMismatch`, `INSTRUMENT_DIR` (Task 1); `Anchor` (Task 2).
- Produces: `create_app(root: Path, deps: Deps, clock=None) -> FastAPI`; `WEB_DIR = INSTRUMENT_DIR / "web"`. Routes (all JSON unless noted), with `{sid}` validated against `^[A-Za-z0-9_-]+$`:
  - `GET /` → console.html, `GET /expert` → expert.html, `/static/*` → `web/`
  - `POST /api/sessions` body `{expert_id, cell, set_order, arms, pilot}` → `{session_id}`
  - `GET /api/sessions/{sid}/console-view`, `GET /api/sessions/{sid}/expert-view`
  - `GET /api/sessions/{sid}/snapshot/{pid}` → PNG
  - `POST /api/sessions/{sid}/think-aloud/start`, `/keep-talking`, `/probe/start`, `/probe/end`, `/pause`, `/resume` → console view
  - `POST /api/sessions/{sid}/think-aloud/{pid}/end` multipart `audio`, `snapshot`, form `strokes` → expert view
  - `POST /api/sessions/{sid}/segments/{seg_id}` `{text}`; `POST /api/sessions/{sid}/segments` `{problem_id, text}` → console view
  - `POST /api/sessions/{sid}/probe/answer` multipart `audio`, form `turn_index` → expert view
  - `POST /api/sessions/{sid}/probe/answer-text` `{turn_index, text}` → console view
  - `POST /api/sessions/{sid}/probe/{set_id}/audio` multipart `audio` → expert view
  - `POST /api/sessions/{sid}/human/marker` `{speaker}`; `/human/stem` `{problem_id, stem_id}`; `/human/anchor` `{problem_id, kind, segment_ids}` → console view
  - Errors: `PhaseError`/`DuplicateSubmission` → 409, `ValueError`/`KeyError` → 400, `ConfigMismatch` → 400, unknown session → 404.

- [ ] **Step 1: Write the failing test**

`instrument/tests/test_server.py`:

```python
import pytest
from fastapi.testclient import TestClient

from fakes import FakeAnthropic, FakeResponse, FakeTranscriber, turn_payload
from probe_app.server import create_app
from probe_app.session import Deps
from probe_app.transcribe import RawSegment

PNG = bytes.fromhex("89504e470d0a1a0a")


def seg(text):
    return [RawSegment(start=0, end=1, text=text)]


@pytest.fixture
def client(tmp_path):
    deps = Deps(FakeTranscriber([seg("A1"), seg("A2"), seg("B1"), seg("B2"), seg("They stick.")]),
                FakeAnthropic(interviewer=[FakeResponse(turn_payload()), FakeResponse(turn_payload(stem_id="checks"))]))
    return TestClient(create_app(tmp_path, deps))


def create(client) -> str:
    r = client.post("/api/sessions", json={"expert_id": "E01", "cell": 1, "set_order": ["A", "B"],
                                           "arms": {"A": "ai", "B": "human"}, "pilot": True})
    assert r.status_code == 200
    return r.json()["session_id"]


def think_all(client, sid):
    for pid in ("A1", "A2", "B1", "B2"):
        assert client.post(f"/api/sessions/{sid}/think-aloud/start").status_code == 200
        r = client.post(f"/api/sessions/{sid}/think-aloud/{pid}/end",
                        files={"audio": ("a.webm", b"x", "audio/webm"), "snapshot": ("s.png", PNG, "image/png")},
                        data={"strokes": "[]"})
        assert r.status_code == 200, r.text


def test_pages_served(client):
    assert client.get("/").status_code == 200
    assert client.get("/expert").status_code == 200


def test_full_ai_probe_round_and_duplicate(client):
    sid = create(client)
    think_all(client, sid)
    assert client.get(f"/api/sessions/{sid}/snapshot/A1").content == PNG
    client.post(f"/api/sessions/{sid}/probe/start")
    view = client.get(f"/api/sessions/{sid}/expert-view").json()
    assert view["question"] and view["expected_answer_index"] == 1
    files = {"audio": ("a.webm", b"x", "audio/webm")}
    assert client.post(f"/api/sessions/{sid}/probe/answer", files=files, data={"turn_index": "1"}).status_code == 200
    assert client.post(f"/api/sessions/{sid}/probe/answer", files=files, data={"turn_index": "1"}).status_code == 409


def test_wrong_phase_is_409(client):
    sid = create(client)
    assert client.post(f"/api/sessions/{sid}/probe/start").status_code == 409


def test_unknown_or_malformed_session(client):
    assert client.get("/api/sessions/nope/expert-view").status_code == 404
    assert client.get("/api/sessions/..%2Fx/expert-view").status_code in (400, 404)


def test_expert_view_hides_trace(client):
    sid = create(client)
    think_all(client, sid)
    assert "segments" not in client.get(f"/api/sessions/{sid}/expert-view").json()
    assert client.get(f"/api/sessions/{sid}/console-view").json()["state"]["segments"]


def test_data_session_without_prereg_is_400(client, monkeypatch, tmp_path):
    monkeypatch.setattr("probe_app.session.PREREG_PATH", tmp_path / "none.json")
    r = client.post("/api/sessions", json={"expert_id": "E01", "cell": 1, "set_order": ["A", "B"],
                                           "arms": {"A": "ai", "B": "human"}, "pilot": False})
    assert r.status_code == 400 and "freeze" in r.text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_server.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'probe_app.server'`.

- [ ] **Step 3: Write the implementation**

`instrument/src/probe_app/server.py`:

```python
import json
import re
import threading
from collections import defaultdict
from pathlib import Path
from typing import Callable, Literal

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from probe_app.config import INSTRUMENT_DIR, ConfigMismatch
from probe_app.models import Anchor
from probe_app.session import Deps, DuplicateSubmission, PhaseError, Session

WEB_DIR = INSTRUMENT_DIR / "web"
SAFE_ID = re.compile(r"^[A-Za-z0-9_-]+$")


class CreateBody(BaseModel):
    expert_id: str
    cell: int
    set_order: list[str]
    arms: dict[str, Literal["ai", "human"]]
    pilot: bool


class TextBody(BaseModel):
    text: str


class SegmentBody(BaseModel):
    problem_id: str
    text: str


class AnswerTextBody(BaseModel):
    turn_index: int
    text: str


class MarkerBody(BaseModel):
    speaker: Literal["interviewer", "expert"]


class StemBody(BaseModel):
    problem_id: str
    stem_id: str


class AnchorBody(BaseModel):
    problem_id: str
    kind: Literal["segments", "canvas", "none"]
    segment_ids: list[str] = []


def create_app(root: Path, deps: Deps, clock=None) -> FastAPI:
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    app = FastAPI(title="Stage A session app")
    app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")
    sessions: dict[str, Session] = {}
    locks: dict[str, threading.Lock] = defaultdict(threading.Lock)

    def get(sid: str) -> Session:
        if not SAFE_ID.match(sid):
            raise HTTPException(400, "malformed session id")
        if sid not in sessions:
            if not (root / sid / "state.json").exists():
                raise HTTPException(404, f"no session {sid}")
            sessions[sid] = Session.load(root, sid, deps, clock)
        return sessions[sid]

    def act(sid: str, fn: Callable[[Session], object], view: str = "console") -> dict:
        session = get(sid)
        with locks[sid]:
            try:
                fn(session)
            except (PhaseError, DuplicateSubmission) as e:
                raise HTTPException(409, str(e))
            except (ValueError, KeyError) as e:
                raise HTTPException(400, str(e))
        return session.console_view() if view == "console" else session.expert_view()

    @app.get("/")
    def console_page():
        return FileResponse(WEB_DIR / "console.html")

    @app.get("/expert")
    def expert_page():
        return FileResponse(WEB_DIR / "expert.html")

    @app.post("/api/sessions")
    def create(body: CreateBody):
        try:
            session = Session.create(root, deps, clock=clock, **body.model_dump())
        except (ConfigMismatch, ValueError) as e:
            raise HTTPException(400, str(e))
        sessions[session.store.session_id] = session
        return {"session_id": session.store.session_id}

    @app.get("/api/sessions/{sid}/console-view")
    def console_view(sid: str):
        return get(sid).console_view()

    @app.get("/api/sessions/{sid}/expert-view")
    def expert_view(sid: str):
        return get(sid).expert_view()

    @app.get("/api/sessions/{sid}/snapshot/{pid}")
    def snapshot(sid: str, pid: str):
        if not SAFE_ID.match(pid):
            raise HTTPException(400, "malformed problem id")
        path = get(sid).snapshot_path(pid)
        if not path.exists():
            raise HTTPException(404, f"no snapshot for {pid}")
        return FileResponse(path, media_type="image/png")

    @app.post("/api/sessions/{sid}/think-aloud/start")
    def think_start(sid: str):
        return act(sid, lambda s: s.start_think_aloud())

    @app.post("/api/sessions/{sid}/keep-talking")
    def keep_talking(sid: str):
        return act(sid, lambda s: s.keep_talking())

    @app.post("/api/sessions/{sid}/think-aloud/{pid}/end")
    def think_end(sid: str, pid: str, audio: UploadFile = File(...), snapshot: UploadFile = File(...),
                  strokes: str = Form("[]")):
        a, p, st = audio.file.read(), snapshot.file.read(), json.loads(strokes)
        return act(sid, lambda s: s.end_think_aloud(pid, a, p, st), view="expert")

    @app.post("/api/sessions/{sid}/segments/{seg_id}")
    def correct(sid: str, seg_id: str, body: TextBody):
        return act(sid, lambda s: s.correct_segment(seg_id, body.text))

    @app.post("/api/sessions/{sid}/segments")
    def add_segment(sid: str, body: SegmentBody):
        return act(sid, lambda s: s.add_segment(body.problem_id, body.text))

    @app.post("/api/sessions/{sid}/probe/start")
    def probe_start(sid: str):
        return act(sid, lambda s: s.start_probe())

    @app.post("/api/sessions/{sid}/probe/answer")
    def answer(sid: str, audio: UploadFile = File(...), turn_index: int = Form(...)):
        a = audio.file.read()
        return act(sid, lambda s: s.answer_ai_audio(turn_index, a), view="expert")

    @app.post("/api/sessions/{sid}/probe/answer-text")
    def answer_text(sid: str, body: AnswerTextBody):
        return act(sid, lambda s: s.answer_ai_text(body.turn_index, body.text))

    @app.post("/api/sessions/{sid}/probe/end")
    def probe_end(sid: str):
        return act(sid, lambda s: s.end_probe())

    @app.post("/api/sessions/{sid}/probe/{set_id}/audio")
    def probe_audio(sid: str, set_id: str, audio: UploadFile = File(...)):
        a = audio.file.read()
        return act(sid, lambda s: s.upload_human_probe(set_id, a), view="expert")

    @app.post("/api/sessions/{sid}/human/marker")
    def marker(sid: str, body: MarkerBody):
        return act(sid, lambda s: s.human_marker(body.speaker))

    @app.post("/api/sessions/{sid}/human/stem")
    def stem(sid: str, body: StemBody):
        return act(sid, lambda s: s.human_stem(body.problem_id, body.stem_id))

    @app.post("/api/sessions/{sid}/human/anchor")
    def anchor(sid: str, body: AnchorBody):
        a = Anchor(kind=body.kind, segment_ids=body.segment_ids)
        return act(sid, lambda s: s.push_anchor(body.problem_id, a))

    @app.post("/api/sessions/{sid}/pause")
    def pause(sid: str):
        return act(sid, lambda s: s.pause())

    @app.post("/api/sessions/{sid}/resume")
    def resume(sid: str):
        return act(sid, lambda s: s.resume())

    return app
```

Create placeholder pages so the static mount and page routes resolve (Task 9 replaces them): `mkdir -p instrument/web/js instrument/web/css && printf '<!doctype html><title>console</title>' > instrument/web/console.html && printf '<!doctype html><title>expert</title>' > instrument/web/expert.html`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_server.py -v`
Expected: 6 passed.

- [ ] **Step 5: Commit**

```bash
git add instrument/src/probe_app/server.py instrument/tests/test_server.py instrument/web
git commit -m "Instrument: HTTP API for console and expert screens"
```

---

### Task 9: Console and expert pages

**Files:**
- Create/replace: `instrument/web/console.html`, `instrument/web/expert.html`, `instrument/web/css/app.css`, `instrument/web/js/console.js`, `instrument/web/js/expert.js`

**Interfaces:**
- Consumes: the routes of Task 8 and the view shapes of Task 7 (`expert_view` keys: `phase, current_problem, current_set, arm, paused, question, expected_answer_index, anchor_view, problem_text`; `console_view` keys: `session_id, manifest, state, expert_view, elapsed, remaining, stems, problems, uncovered`).

- [ ] **Step 1: Write `web/css/app.css`**

```css
:root { --fg: #111; --bg: #fafafa; --muted: #666; --accent: #1f5fbf; --warn: #b3261e; }
* { box-sizing: border-box; }
body { margin: 0; font: 18px/1.5 system-ui, sans-serif; color: var(--fg); background: var(--bg); }
main { max-width: 1100px; margin: 0 auto; padding: 16px; }
button { font: inherit; padding: 10px 18px; border-radius: 8px; border: 1px solid #999; background: #fff; cursor: pointer; }
button.primary { background: var(--accent); color: #fff; border-color: var(--accent); }
button:disabled { opacity: .5; cursor: default; }
.row { display: flex; gap: 12px; flex-wrap: wrap; align-items: center; margin: 12px 0; }
.problem { font-size: 20px; }
.question { font-size: 24px; font-weight: 600; }
.hint, .muted { color: var(--muted); }
#status, .error { color: var(--warn); }
canvas { width: 100%; height: auto; background: #fff; border: 1px solid #ccc; touch-action: none; }
blockquote { margin: 12px 0; padding: 8px 12px; border-left: 4px solid var(--accent); background: #fff; }
img.anchor { max-width: 100%; border: 3px solid var(--accent); }
table { border-collapse: collapse; width: 100%; font-size: 15px; }
td, th { border-bottom: 1px solid #ddd; padding: 4px 6px; text-align: left; vertical-align: top; }
td[contenteditable] { background: #fff; }
.chip { display: inline-block; padding: 2px 8px; margin: 2px; border-radius: 12px; border: 1px solid #999; cursor: pointer; font-size: 14px; }
.chip.done { background: #d7f0d7; border-color: #3a8a3a; }
.dialogue p { margin: 4px 0; }
```

- [ ] **Step 2: Write `web/expert.html` and `web/js/expert.js`**

`web/expert.html`:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Physics session</title>
<link rel="stylesheet" href="/static/css/app.css">
</head>
<body>
<main>
  <section id="join">
    <p>Enter the session code the researcher gives you.</p>
    <div class="row"><input id="sid" aria-label="Session code"><button id="joinBtn" class="primary">Join and allow microphone</button></div>
  </section>
  <section id="waiting" hidden><p>Waiting for the researcher.</p></section>
  <section id="thinkaloud" hidden>
    <p class="problem" id="problemText"></p>
    <p class="hint">Solve the problem and say everything you are thinking, including anything that feels obvious.</p>
    <canvas id="pad" width="1600" height="1000"></canvas>
    <div class="row"><button id="doneBtn" class="primary">Done with this problem</button></div>
  </section>
  <section id="probe" hidden>
    <p class="question" id="question"></p>
    <blockquote id="anchorText" hidden></blockquote>
    <img id="anchorImg" class="anchor" alt="Your written work" hidden>
    <div class="row"><button id="talkBtn" class="primary">Start answer</button></div>
  </section>
  <section id="human" hidden>
    <p>Your interviewer will ask you questions now.</p>
    <blockquote id="humanText" hidden></blockquote>
    <img id="humanImg" class="anchor" alt="Your written work" hidden>
  </section>
  <section id="done" hidden><p>Thank you. The session is complete.</p></section>
  <p id="status" role="status"></p>
</main>
<script type="module" src="/static/js/expert.js"></script>
</body>
</html>
```

`web/js/expert.js`:

```js
const $ = (id) => document.getElementById(id);
let sid = new URLSearchParams(location.search).get("session") || "";
let stream = null, recorder = null, chunks = [], recStart = 0, strokes = [];
let view = null, lastKey = "", busy = false, pending = null;

async function api(path, opts = {}) {
  const r = await fetch(`/api/sessions/${sid}${path}`, opts);
  if (!r.ok) throw new Error(`${r.status}: ${await r.text()}`);
  return r.json();
}

function show(id) {
  for (const s of document.querySelectorAll("main > section")) s.hidden = s.id !== id;
}

function startRecording() {
  chunks = [];
  recorder = new MediaRecorder(stream, { mimeType: "audio/webm;codecs=opus" });
  recorder.ondataavailable = (e) => chunks.push(e.data);
  recorder.start(1000);
  recStart = performance.now();
}

function stopRecording() {
  return new Promise((resolve) => {
    recorder.onstop = () => resolve(new Blob(chunks, { type: "audio/webm" }));
    recorder.stop();
  });
}

const pad = $("pad");
const ctx = pad.getContext("2d");
let stroke = null;

function resetPad() {
  ctx.fillStyle = "#fff";
  ctx.fillRect(0, 0, pad.width, pad.height);
  ctx.lineWidth = 3; ctx.lineCap = "round"; ctx.strokeStyle = "#111";
  strokes = [];
}

function point(e) {
  const r = pad.getBoundingClientRect();
  return [(e.clientX - r.left) * pad.width / r.width, (e.clientY - r.top) * pad.height / r.height,
          Math.round(performance.now() - recStart)];
}

pad.addEventListener("pointerdown", (e) => {
  pad.setPointerCapture(e.pointerId);
  const p = point(e);
  stroke = { points: [p] };
  ctx.beginPath(); ctx.moveTo(p[0], p[1]);
});
pad.addEventListener("pointermove", (e) => {
  if (!stroke) return;
  const p = point(e);
  stroke.points.push(p);
  ctx.lineTo(p[0], p[1]); ctx.stroke();
});
pad.addEventListener("pointerup", () => { if (stroke) strokes.push(stroke); stroke = null; });

async function send(path, form, label) {
  pending = { path, form, label };
  $("status").textContent = label;
  try {
    await api(path, { method: "POST", body: form });
    pending = null;
    $("status").textContent = "";
  } catch (err) {
    $("status").textContent = `Could not send (${err.message}). Tap to retry.`;
  }
}

$("status").addEventListener("click", () => { if (pending) send(pending.path, pending.form, pending.label); });

$("joinBtn").onclick = async () => {
  sid = sid || $("sid").value.trim();
  stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  show("waiting");
  poll();
};

$("doneBtn").onclick = async () => {
  if (busy) return;
  busy = true; $("doneBtn").disabled = true;
  const audio = await stopRecording();
  const snapshot = await new Promise((r) => pad.toBlob(r, "image/png"));
  const form = new FormData();
  form.append("audio", audio, "think.webm");
  form.append("snapshot", snapshot, "snapshot.png");
  form.append("strokes", JSON.stringify(strokes));
  await send(`/think-aloud/${view.current_problem}/end`, form, "Saving…");
  busy = false; $("doneBtn").disabled = false;
};

$("talkBtn").onclick = async () => {
  if (recorder && recorder.state === "recording") {
    $("talkBtn").disabled = true;
    const audio = await stopRecording();
    const form = new FormData();
    form.append("audio", audio, "answer.webm");
    form.append("turn_index", String(view.expected_answer_index));
    await send("/probe/answer", form, "Listening to your answer…");
    $("talkBtn").textContent = "Start answer";
    $("talkBtn").disabled = false;
  } else {
    startRecording();
    $("talkBtn").textContent = "Finish answer";
  }
};

function renderAnchor(anchor, textId, imgId) {
  $(textId).hidden = !(anchor && anchor.kind === "segments");
  $(imgId).hidden = !(anchor && anchor.kind === "canvas");
  if (anchor && anchor.kind === "segments") $(textId).textContent = anchor.text;
  if (anchor && anchor.kind === "canvas") $(imgId).src = anchor.image_url;
}

async function uploadHumanProbe(setId) {
  busy = true;
  const audio = await stopRecording();
  const form = new FormData();
  form.append("audio", audio, "probe.webm");
  await send(`/probe/${setId}/audio`, form, "Saving…");
  busy = false;
}

function render(s) {
  const key = `${s.phase}|${s.current_problem}|${s.current_set}`;
  const entering = key !== lastKey;
  lastKey = key;
  view = s;
  if (s.phase === "think_aloud") {
    if (entering) { resetPad(); $("problemText").textContent = s.problem_text; startRecording(); }
    show("thinkaloud");
  } else if (s.phase === "probe" && s.arm === "ai") {
    show("probe");
    $("question").textContent = s.question || "One moment…";
    $("talkBtn").hidden = s.question === null;
    renderAnchor(s.anchor_view, "anchorText", "anchorImg");
  } else if (s.phase === "probe" && s.arm === "human") {
    if (entering) startRecording();
    show("human");
    renderAnchor(s.anchor_view, "humanText", "humanImg");
  } else if (s.phase === "probe_uploading") {
    if (!busy && recorder && recorder.state === "recording") uploadHumanProbe(s.current_set);
  } else if (s.phase === "done") {
    show("done");
  } else {
    show("waiting");
  }
}

async function poll() {
  try { render(await api("/expert-view")); }
  catch (err) { $("status").textContent = err.message; }
  setTimeout(poll, 1000);
}
```

- [ ] **Step 3: Write `web/console.html` and `web/js/console.js`**

`web/console.html`:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Session console</title>
<link rel="stylesheet" href="/static/css/app.css">
</head>
<body>
<main>
  <section id="create">
    <h1>New session</h1>
    <div class="row">
      <label>Expert pseudonym <input id="expertId" value="E01"></label>
      <label>Cell <input id="cell" type="number" value="1" min="1" max="12"></label>
      <label>Set order <select id="setOrder"><option>A,B</option><option>B,A</option></select></label>
      <label>First set arm <select id="firstArm"><option>ai</option><option>human</option></select></label>
      <label><input id="pilot" type="checkbox" checked> Pilot</label>
      <button id="createBtn" class="primary">Create</button>
    </div>
  </section>
  <section id="run" hidden>
    <h1 id="title"></h1>
    <p>Expert link: <a id="expertLink"></a></p>
    <p><strong id="phase"></strong> <span id="clock" class="muted"></span></p>
    <p id="error" class="error"></p>
    <div class="row">
      <button data-post="/think-aloud/start">Start next problem</button>
      <button data-post="/keep-talking">Keep talking</button>
      <button data-post="/probe/start">Start probe set</button>
      <button data-post="/probe/end">End probe set</button>
      <button data-post="/pause">Pause</button>
      <button data-post="/resume">Resume</button>
    </div>
    <section id="humanPanel" hidden>
      <h2>Human interviewer</h2>
      <p class="muted">Press I when you start speaking and E when the expert starts. Tick a stem when you use it. Click a transcript row to show it to the expert.</p>
      <div class="row"><button id="markI" class="primary">I — interviewer</button><button id="markE" class="primary">E — expert</button></div>
      <div id="stemChips"></div>
    </section>
    <section id="aiPanel" hidden>
      <h2>AI interviewer</h2>
      <p>Unused stems: <span id="uncovered"></span></p>
      <div class="row"><input id="typedAnswer" size="60" placeholder="Type the expert's answer if transcription failed"><button id="typedBtn">Submit answer</button></div>
    </section>
    <h2>Dialogue</h2>
    <div id="dialogue" class="dialogue"></div>
    <h2>Trace</h2>
    <table><thead><tr><th>Segment</th><th>Time</th><th>Text (edit, then press Enter)</th></tr></thead><tbody id="trace"></tbody></table>
    <div class="row"><select id="addPid"></select><input id="addText" size="60" placeholder="Typed transcript for a failed problem"><button id="addBtn">Add segment</button></div>
  </section>
</main>
<script type="module" src="/static/js/console.js"></script>
</body>
</html>
```

`web/js/console.js`:

```js
const $ = (id) => document.getElementById(id);
let sid = new URLSearchParams(location.search).get("session");
let view = null;

async function call(path, body) {
  const opts = { method: "POST" };
  if (body !== undefined) { opts.headers = { "Content-Type": "application/json" }; opts.body = JSON.stringify(body); }
  const r = await fetch(`/api/sessions/${sid}${path}`, opts);
  if (!r.ok) { $("error").textContent = `${r.status}: ${await r.text()}`; return null; }
  $("error").textContent = "";
  view = await r.json();
  render();
  return view;
}

$("createBtn").onclick = async () => {
  const order = $("setOrder").value.split(",");
  const first = $("firstArm").value;
  const arms = { [order[0]]: first, [order[1]]: first === "ai" ? "human" : "ai" };
  const r = await fetch("/api/sessions", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ expert_id: $("expertId").value, cell: Number($("cell").value),
                           set_order: order, arms, pilot: $("pilot").checked }),
  });
  if (!r.ok) { alert(await r.text()); return; }
  sid = (await r.json()).session_id;
  history.replaceState(null, "", `?session=${sid}`);
  start();
};

for (const b of document.querySelectorAll("[data-post]")) b.onclick = () => call(b.dataset.post);
$("markI").onclick = () => call("/human/marker", { speaker: "interviewer" });
$("markE").onclick = () => call("/human/marker", { speaker: "expert" });
document.addEventListener("keydown", (e) => {
  if (e.target.tagName === "INPUT" || e.target.isContentEditable) return;
  if (e.key === "i") $("markI").click();
  if (e.key === "e") $("markE").click();
});
$("typedBtn").onclick = () => {
  const idx = view.state.dialogue[view.state.current_set].length;
  call("/probe/answer-text", { turn_index: idx, text: $("typedAnswer").value }).then(() => { $("typedAnswer").value = ""; });
};
$("addBtn").onclick = () => call("/segments", { problem_id: $("addPid").value, text: $("addText").value });

function fmt(s) { const m = Math.floor(s / 60), r = Math.floor(s % 60); return `${m}:${String(r).padStart(2, "0")}`; }

function render() {
  const st = view.state;
  const arm = st.current_set ? st.arms[st.current_set] : null;
  $("title").textContent = `Session ${view.session_id}${view.manifest.pilot ? " (pilot)" : ""}`;
  const link = `${location.origin}/expert?session=${view.session_id}`;
  $("expertLink").textContent = link; $("expertLink").href = link;
  $("phase").textContent = `${st.phase}${st.current_problem ? " · " + st.current_problem : ""}${st.current_set ? " · set " + st.current_set + " (" + arm + ")" : ""}${st.paused ? " · PAUSED" : ""}`;
  $("clock").textContent = st.current_set ? `elapsed ${fmt(view.elapsed)} · remaining ${fmt(Math.max(0, view.remaining))}` : "";
  if (st.error) $("error").textContent = st.error;
  $("humanPanel").hidden = arm !== "human";
  $("aiPanel").hidden = arm !== "ai";
  if (arm === "ai") $("uncovered").textContent = (view.uncovered || []).join(", ") || "none";
  if (arm === "human") {
    const ticked = new Set((st.ticks[st.current_set] || []).map((t) => `${t.problem_id}/${t.stem_id}`));
    $("stemChips").replaceChildren(...st.sets[st.current_set].flatMap((pid) => Object.keys(view.stems).map((stem) => {
      const chip = document.createElement("span");
      chip.className = `chip${ticked.has(`${pid}/${stem}`) ? " done" : ""}`;
      chip.textContent = `${pid}/${stem}`;
      chip.onclick = () => call("/human/stem", { problem_id: pid, stem_id: stem });
      return chip;
    })));
  }
  const dialogue = st.current_set ? st.dialogue[st.current_set] : [];
  $("dialogue").replaceChildren(...dialogue.map((d) => {
    const p = document.createElement("p");
    p.textContent = d.speaker === "interviewer"
      ? `Q [${d.problem_id || "?"}/${d.stem_id || "?"}${d.is_followup ? " follow-up" : ""}, ${d.source}]: ${d.text}`
      : `A: ${d.text}`;
    return p;
  }));
  if (!document.activeElement || document.activeElement.tagName !== "TD") {
    $("trace").replaceChildren(...st.segments.map((s) => {
      const tr = document.createElement("tr");
      const id = document.createElement("td"); id.textContent = s.id;
      const time = document.createElement("td"); time.textContent = `${s.start.toFixed(1)}s`;
      const text = document.createElement("td"); text.textContent = s.text; text.contentEditable = "true";
      text.onkeydown = (e) => { if (e.key === "Enter") { e.preventDefault(); text.blur(); call(`/segments/${s.id}`, { text: text.textContent }); } };
      tr.onclick = (e) => {
        if (e.target === text || arm !== "human" || !st.sets[st.current_set].includes(s.problem_id)) return;
        call("/human/anchor", { problem_id: s.problem_id, kind: "segments", segment_ids: [s.id] });
      };
      tr.append(id, time, text);
      return tr;
    }));
  }
  $("addPid").replaceChildren(...st.think_aloud_done.map((p) => new Option(p, p)));
}

async function poll() {
  try {
    const r = await fetch(`/api/sessions/${sid}/console-view`);
    if (r.ok) { view = await r.json(); render(); }
  } catch (err) { $("error").textContent = err.message; }
  setTimeout(poll, 1000);
}

function start() { $("create").hidden = true; $("run").hidden = false; poll(); }
if (sid) start();
```

- [ ] **Step 4: Verify the pages in a browser**

Run the page tests: `uv run pytest tests/test_server.py::test_pages_served -v` → PASS.

Then use the `run` skill (or run it yourself) with a fake backend so no keys are needed:

```bash
uv run python -c "
import uvicorn
from fakes import FakeAnthropic, FakeResponse, FakeTranscriber, turn_payload
from probe_app.server import create_app
from probe_app.session import Deps
from probe_app.transcribe import RawSegment
seg = lambda t: [RawSegment(start=0, end=2, text=t)]
deps = Deps(FakeTranscriber([seg(f'talk {i}') for i in range(40)]),
            FakeAnthropic(interviewer=[FakeResponse(turn_payload(stem_id=s)) for s in ['cues','alternatives','checks','anomalies','novice_miss']*4]))
uvicorn.run(create_app('/tmp/probe-demo', deps), host='127.0.0.1', port=8000)
" 
```

(run with `PYTHONPATH=tests`). Open `http://127.0.0.1:8000/`, create a pilot session, open the expert link in a second tab, allow the microphone, and go through: four think-aloud problems (draw a stroke, press Done), edit one trace row and press Enter, start the AI probe set (question appears, Start/Finish answer advances it), end it, start the human set (I/E markers, stem chips turn green, clicking a trace row shows it on the expert tab), end it (expert tab uploads, phase becomes done). Expected: no console errors; each step shows in the console's dialogue and phase line.

- [ ] **Step 5: Commit**

```bash
git add instrument/web
git commit -m "Instrument: researcher console and expert tablet pages"
```

---

### Task 10: CLI and simulated-expert run

**Files:**
- Create: `instrument/src/probe_app/simulate.py`, `instrument/src/probe_app/cli.py`, `instrument/problems/simulated_think_aloud.json`
- Test: `instrument/tests/test_simulate.py`, `instrument/tests/test_cli.py`

**Interfaces:**
- Consumes: `Session`, `Deps` (Task 7); `create_app` (Task 8); config (Task 1); `RawSegment` (Task 3); `render_transcript` (Task 3).
- Produces: `probe-app transcribe AUDIO --model scribe_v2|whisper-1` (prints rendered segments); `BLANK_PNG: bytes`; `FixtureTranscriber(fixture: dict[str, list[dict]])` with `.model = "fixture"`, `.load(problem_id)`, `.transcribe(path)`; `SimulatedExpert(client, model=INTERVIEWER_MODEL)` with `.answer(problems: dict[str, str], transcript: str, dialogue: list[DialogueTurn]) -> str`; `run_simulation(root: Path, deps: Deps, expert, set_order: list[str], max_turns: int = 60) -> str` (session id; AI arm on every set); `probe_app.cli.main(argv: list[str] | None = None) -> None` with subcommands `serve`, `hashes`, `freeze`, `simulate`.

- [ ] **Step 1: Write the fixture**

`instrument/problems/simulated_think_aloud.json`:

```json
{
  "A1": [
    {"start": 0.0, "end": 6.0, "text": "Okay, block slides down, frictionless, so I get its speed at the bottom from energy."},
    {"start": 6.0, "end": 12.0, "text": "Then they stick, so that part isn't energy, it's momentum, the collision loses energy."},
    {"start": 12.0, "end": 19.0, "text": "Speed after is two thirds of the speed before, then energy again up the ramp."},
    {"start": 19.0, "end": 25.0, "text": "Height scales with speed squared, so four ninths of 1.8, 0.8 metres. That's lower, which makes sense."}
  ],
  "A2": [
    {"start": 0.0, "end": 7.0, "text": "Bullet embeds, so again a sticking collision, momentum only for the impact."},
    {"start": 7.0, "end": 14.0, "text": "Speed of block and bullet is about 1.49 metres per second, then it swings up, energy."},
    {"start": 14.0, "end": 22.0, "text": "Rise is v squared over 2g, about 11 centimetres, and cos theta is one minus h over L, so around 22 degrees."}
  ],
  "B1": [
    {"start": 0.0, "end": 6.0, "text": "Sticks to the block on the spring, so first the collision with momentum, speed one metre per second."},
    {"start": 6.0, "end": 13.0, "text": "Then the pair compresses the spring, kinetic energy into spring energy, one joule equals a half k x squared."},
    {"start": 13.0, "end": 18.0, "text": "x is 0.1 metres. I shouldn't use the initial kinetic energy, that's the classic trap."}
  ],
  "B2": [
    {"start": 0.0, "end": 7.0, "text": "Elastic, so both momentum and kinetic energy are conserved, I'll use the standard result."},
    {"start": 7.0, "end": 14.0, "text": "Light cart leaves at 2 m1 over m1 plus m2 times v, four metres per second."},
    {"start": 14.0, "end": 21.0, "text": "It could climb v squared over 2g, about 0.82 metres, more than 0.5, so yes it gets over."}
  ]
}
```

- [ ] **Step 2: Write the failing tests**

`instrument/tests/test_simulate.py`:

```python
import json

from fakes import FakeAnthropic, FakeResponse, turn_payload
from probe_app.config import INSTRUMENT_DIR
from probe_app.models import STEMS
from probe_app.session import Deps
from probe_app.simulate import FixtureTranscriber, run_simulation


class EchoExpert:
    def answer(self, problems, transcript, dialogue):
        return f"Answer to: {dialogue[-1].text}"


def test_simulation_runs_ai_arm_to_completion(tmp_path):
    turns = []
    for set_problems in (["A1", "A2"], ["B1", "B2"]):
        turns += [FakeResponse(turn_payload(problem_id=p, stem_id=s)) for p in set_problems for s in STEMS]
        turns.append(FakeResponse(turn_payload(problem_id=set_problems[0], end_session=True)))
    fixture = json.loads((INSTRUMENT_DIR / "problems" / "simulated_think_aloud.json").read_text())
    deps = Deps(FixtureTranscriber(fixture), FakeAnthropic(interviewer=turns))
    sid = run_simulation(tmp_path, deps, EchoExpert(), ["A", "B"])
    state = json.loads((tmp_path / sid / "state.json").read_text())
    manifest = json.loads((tmp_path / sid / "manifest.json").read_text())
    assert state["phase"] == "done" and manifest["simulated"] is True
    assert len([d for d in state["dialogue"]["A"] if d["speaker"] == "expert"]) == 10
    assert state["dialogue"]["A"][1]["source"] == "simulated"
```

`instrument/tests/test_cli.py`:

```python
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
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `uv run pytest tests/test_simulate.py tests/test_cli.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'probe_app.simulate'`.

- [ ] **Step 4: Write `simulate.py`**

```python
import base64
from pathlib import Path

from probe_app.config import INTERVIEWER_MODEL, load_problems
from probe_app.models import DialogueTurn
from probe_app.session import Deps, Session
from probe_app.trace import render_transcript
from probe_app.transcribe import RawSegment

BLANK_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==")

EXPERT_PROMPT = (
    "You are a physics lecturer who has just solved the problems below while thinking aloud; the transcript is "
    "your own. An interviewer is asking you about your solution. Answer the interviewer's last question in the "
    "first person, in two to five spoken sentences, as you would say them aloud. Say only your answer.")


class FixtureTranscriber:
    model = "fixture"

    def __init__(self, fixture: dict[str, list[dict]]):
        self.fixture = fixture
        self.current: str | None = None

    def load(self, problem_id: str) -> None:
        self.current = problem_id

    def transcribe(self, audio_path: Path) -> list[RawSegment]:
        return [RawSegment(**s) for s in self.fixture[self.current]]


class SimulatedExpert:
    def __init__(self, client, model: str = INTERVIEWER_MODEL):
        self.client, self.model = client, model

    def answer(self, problems: dict[str, str], transcript: str, dialogue: list[DialogueTurn]) -> str:
        history = "\n".join(f"{d.speaker.upper()}: {d.text}" for d in dialogue)
        problem_text = "\n".join(f"{p}: {t}" for p, t in problems.items())
        response = self.client.messages.create(
            model=self.model, max_tokens=2000, output_config={"effort": "low"},
            messages=[{"role": "user", "content": f"{EXPERT_PROMPT}\n\nPROBLEMS\n{problem_text}\n\n"
                                                   f"YOUR THINK-ALOUD\n{transcript}\n\nINTERVIEW SO FAR\n{history}"}])
        return next(b.text for b in response.content if b.type == "text").strip()


def run_simulation(root: Path, deps: Deps, expert, set_order: list[str], max_turns: int = 60) -> str:
    session = Session.create(root, deps, expert_id="SIM", cell=0, arms={s: "ai" for s in set_order},
                             set_order=set_order, pilot=True, simulated=True)
    statements = {p: v["statement"] for p, v in load_problems()["problems"].items()}
    while session.state.phase == "ready":
        pid = session.start_think_aloud()
        deps.transcriber.load(pid)
        session.end_think_aloud(pid, b"", BLANK_PNG, [])
    while session.state.phase == "trace_review":
        set_id = session.start_probe()
        pids = session.state.sets[set_id]
        transcript = render_transcript([s for s in session.state.segments if s.problem_id in pids])
        while session.state.phase == "probe":
            dialogue = session.state.dialogue[set_id]
            if len(dialogue) >= max_turns:
                session.end_probe()
                break
            text = expert.answer({p: statements[p] for p in pids}, transcript, dialogue)
            session.answer_ai_text(len(dialogue), text, source="simulated")
    return session.store.session_id
```

- [ ] **Step 5: Write `cli.py`**

```python
import argparse
import json
from dataclasses import asdict
from pathlib import Path

from dotenv import load_dotenv

from probe_app.config import INSTRUMENT_DIR, PREREG_PATH, TRANSCRIBER_MODEL, current_config, freeze


def main(argv: list[str] | None = None) -> None:
    load_dotenv(INSTRUMENT_DIR / ".env")
    parser = argparse.ArgumentParser(prog="probe-app")
    sub = parser.add_subparsers(dest="cmd", required=True)
    serve = sub.add_parser("serve", help="run the session app")
    serve.add_argument("--root", type=Path, default=INSTRUMENT_DIR.parent / "sessions")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)
    serve.add_argument("--ssl-certfile")
    serve.add_argument("--ssl-keyfile")
    sub.add_parser("hashes", help="print the current frozen configuration")
    tr = sub.add_parser("transcribe", help="transcribe one audio file, to compare transcribers in the pilot")
    tr.add_argument("audio", type=Path)
    tr.add_argument("--model", default=TRANSCRIBER_MODEL, help="scribe_v2 or whisper-1")
    sub.add_parser("freeze", help="write the current configuration to prereg.json")
    sim = sub.add_parser("simulate", help="run a simulated AI-arm session against the real APIs")
    sim.add_argument("--root", type=Path, default=INSTRUMENT_DIR.parent / "sessions")
    sim.add_argument("--set-order", default="A,B")
    args = parser.parse_args(argv)

    if args.cmd == "hashes":
        print(json.dumps(asdict(current_config()), indent=2))
    elif args.cmd == "transcribe":
        from probe_app.trace import build_segments, render_transcript
        from probe_app.transcribe import make_transcriber

        raw = make_transcriber(args.model).transcribe(args.audio)
        print(render_transcript(build_segments("X", 0.0, raw)))
    elif args.cmd == "freeze":
        freeze(current_config(), PREREG_PATH)
        print(f"wrote {PREREG_PATH}")
    elif args.cmd == "serve":
        import anthropic
        import uvicorn

        from probe_app.server import create_app
        from probe_app.session import Deps
        from probe_app.transcribe import make_transcriber

        app = create_app(args.root, Deps(make_transcriber(), anthropic.Anthropic()))
        uvicorn.run(app, host=args.host, port=args.port,
                    ssl_certfile=args.ssl_certfile, ssl_keyfile=args.ssl_keyfile)
    elif args.cmd == "simulate":
        import anthropic

        from probe_app.session import Deps
        from probe_app.simulate import FixtureTranscriber, SimulatedExpert, run_simulation

        client = anthropic.Anthropic()
        fixture = json.loads((INSTRUMENT_DIR / "problems" / "simulated_think_aloud.json").read_text())
        sid = run_simulation(args.root, Deps(FixtureTranscriber(fixture), client), SimulatedExpert(client),
                             args.set_order.split(","))
        print(f"simulated session: {args.root / sid}")
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `uv run pytest tests/test_simulate.py tests/test_cli.py -v`
Expected: 3 passed.

- [ ] **Step 7: Live smoke run (needs keys in `instrument/.env`)**

Only when the user has put `ANTHROPIC_API_KEY` in `instrument/.env`: run `uv run probe-app simulate`. Expected: prints a session path; `events.jsonl` in it has `probe` events with `"source": "ai"`, and `llm/` holds the requests and responses. Report the turn count, the `turn_rejected` count, and the median gap between `expert_answer` and the next `probe` event (AI latency). Skip this step and say so if no key is present.

- [ ] **Step 8: Commit**

```bash
git add instrument/src/probe_app/simulate.py instrument/src/probe_app/cli.py instrument/problems/simulated_think_aloud.json instrument/tests/test_simulate.py instrument/tests/test_cli.py
git commit -m "Instrument: CLI (serve, hashes, transcribe, freeze, simulate) and simulated-expert run"
```

---

### Task 11: Coding pipeline — loading and blinded exports

**Files:**
- Create: `instrument/src/probe_code/loader.py`, `instrument/src/probe_code/export.py`
- Test: `instrument/tests/test_export.py`

**Interfaces:**
- Consumes: `SessionState` (Task 7); `DialogueTurn`, `Segment` (Task 2).
- Produces: `class SimulatedSession(Exception)`; `@dataclass LoadedSession(session_id: str, dir: Path, manifest: dict, state: SessionState)`; `load_session(path: Path, allow_simulated: bool = False) -> LoadedSession`; `split_units(text: str) -> list[str]`; `export_blind(sessions: list[LoadedSession], out_dir: Path, seed: int) -> None` writing `coder_units.csv` (`unit_id, blind_session, problem_ids, text`) and `key_units.csv` (`unit_id, blind_session, session_id, expert_id, set_id, arm, turn_index, pilot`); `export_trace(sessions, out_dir, seed) -> None` writing `trace_units.csv` (`blind_session, problem_id, segment_id, start, end, text`), `key_trace.csv` (`blind_session, session_id, expert_id`) and `snapshots/<blind>_<pid>.png`; `write_csv(path: Path, rows: list[dict]) -> None`; `read_csv(path: Path) -> list[dict]`.
- Test helper (in the test file): `make_session(tmp_path, name, arms, dialogue, simulated=False) -> Path`.

- [ ] **Step 1: Write the failing test**

`instrument/tests/test_export.py`:

```python
import json

import pytest

from probe_code.export import export_blind, export_trace, read_csv, split_units
from probe_code.loader import SimulatedSession, load_session
from probe_app.session import SessionState
from probe_app.models import DialogueTurn, Segment

PNG = bytes.fromhex("89504e470d0a1a0a")


def make_session(tmp_path, name, arms=None, simulated=False):
    d = tmp_path / name
    (d / "canvas" / "snapshots").mkdir(parents=True)
    (d / "canvas" / "snapshots" / "A1.png").write_bytes(PNG)
    state = SessionState(sets={"A": ["A1", "A2"], "B": ["B1", "B2"]}, set_order=["A", "B"],
                         arms=arms or {"A": "ai", "B": "human"}, phase="done")
    state.segments = [Segment(id="A1-s001", problem_id="A1", start=0, end=1, text="Energy first.")]
    state.dialogue = {
        "A": [DialogueTurn(speaker="interviewer", text="SECRET AI QUESTION", t=0, source="ai"),
              DialogueTurn(speaker="expert", text="They stick. So momentum!", t=1, source="transcribed")],
        "B": [DialogueTurn(speaker="interviewer", text="SECRET HUMAN QUESTION", t=0, source="human"),
              DialogueTurn(speaker="expert", text="Spring energy.", t=1, source="transcribed")]}
    (d / "state.json").write_text(state.model_dump_json())
    (d / "manifest.json").write_text(json.dumps({"expert_id": name, "pilot": True, "simulated": simulated}))
    return d


def test_split_units():
    assert split_units("They stick. So momentum! Right?") == ["They stick.", "So momentum!", "Right?"]


def test_simulated_sessions_refused(tmp_path):
    with pytest.raises(SimulatedSession):
        load_session(make_session(tmp_path, "SIM", simulated=True))
    assert load_session(make_session(tmp_path, "SIM2", simulated=True), allow_simulated=True)


def test_blind_export_has_no_interviewer_text_and_separate_key(tmp_path):
    sessions = [load_session(make_session(tmp_path, n)) for n in ("E01", "E02")]
    out = tmp_path / "out"
    export_blind(sessions, out, seed=1)
    coder_text = (out / "coder_units.csv").read_text()
    assert "SECRET" not in coder_text and "ai" not in read_csv(out / "coder_units.csv")[0].values()
    assert "arm" not in read_csv(out / "coder_units.csv")[0]
    rows = read_csv(out / "coder_units.csv")
    key = {r["unit_id"]: r for r in read_csv(out / "key_units.csv")}
    assert len(rows) == 6 and set(key) == {r["unit_id"] for r in rows}
    assert {key[r["unit_id"]]["arm"] for r in rows} == {"ai", "human"}
    assert len({r["blind_session"] for r in rows}) == 4


def test_trace_export_has_no_probe_material(tmp_path):
    sessions = [load_session(make_session(tmp_path, "E01"))]
    out = tmp_path / "trace"
    export_trace(sessions, out, seed=1)
    text = (out / "trace_units.csv").read_text()
    assert "Energy first." in text and "stick" not in text and "SECRET" not in text
    blind = read_csv(out / "key_trace.csv")[0]["blind_session"]
    assert (out / "snapshots" / f"{blind}_A1.png").read_bytes() == PNG
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_export.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'probe_code.export'`.

- [ ] **Step 3: Write the implementation**

`instrument/src/probe_code/loader.py`:

```python
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
```

`instrument/src/probe_code/export.py`:

```python
import csv
import random
import re
import shutil
from pathlib import Path

from probe_code.loader import LoadedSession

SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


def split_units(text: str) -> list[str]:
    return [u.strip() for u in SENTENCE_END.split(text) if u.strip()]


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        if not rows:
            return
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict]:
    with Path(path).open(newline="") as f:
        return list(csv.DictReader(f))


def _blind_id(rng: random.Random) -> str:
    return f"S{rng.getrandbits(32):08x}"


def export_blind(sessions: list[LoadedSession], out_dir: Path, seed: int) -> None:
    rng = random.Random(seed)
    blocks = []
    for s in sessions:
        for set_id, turns in s.state.dialogue.items():
            blind = _blind_id(rng)
            block = []
            for index, turn in enumerate(turns):
                if turn.speaker != "expert":
                    continue
                for unit in split_units(turn.text):
                    unit_id = f"U{rng.getrandbits(48):012x}"
                    block.append((
                        {"unit_id": unit_id, "blind_session": blind,
                         "problem_ids": ";".join(s.state.sets[set_id]), "text": unit},
                        {"unit_id": unit_id, "blind_session": blind, "session_id": s.session_id,
                         "expert_id": s.manifest["expert_id"], "set_id": set_id, "arm": s.state.arms[set_id],
                         "turn_index": index, "pilot": s.manifest.get("pilot", False)}))
            blocks.append(block)
    rng.shuffle(blocks)
    write_csv(out_dir / "coder_units.csv", [c for block in blocks for c, _ in block])
    write_csv(out_dir / "key_units.csv", [k for block in blocks for _, k in block])


def export_trace(sessions: list[LoadedSession], out_dir: Path, seed: int) -> None:
    rng = random.Random(seed)
    rows, key = [], []
    (out_dir / "snapshots").mkdir(parents=True, exist_ok=True)
    for s in sessions:
        blind = _blind_id(rng)
        key.append({"blind_session": blind, "session_id": s.session_id, "expert_id": s.manifest["expert_id"]})
        for seg in s.state.segments:
            rows.append({"blind_session": blind, "problem_id": seg.problem_id, "segment_id": seg.id,
                         "start": seg.start, "end": seg.end, "text": seg.text})
        for snap in (s.dir / "canvas" / "snapshots").glob("*.png"):
            shutil.copy(snap, out_dir / "snapshots" / f"{blind}_{snap.name}")
    write_csv(out_dir / "trace_units.csv", rows)
    write_csv(out_dir / "key_trace.csv", key)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_export.py -v`
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add instrument/src/probe_code/loader.py instrument/src/probe_code/export.py instrument/tests/test_export.py
git commit -m "Coding pipeline: session loader, blinded unit export, trace-only export"
```

---

### Task 12: Coding pipeline — corroboration, agreement, guard audit, CLI

**Files:**
- Create: `instrument/src/probe_code/corroboration.py`, `instrument/src/probe_code/agreement.py`, `instrument/src/probe_code/guard_audit.py`, `instrument/src/probe_code/cli.py`
- Test: `instrument/tests/test_analysis.py`

**Interfaces:**
- Consumes: `read_csv`, `write_csv`, `load_session`, `LoadedSession` (Task 11); `Guard` (Task 5); config loaders (Task 1).
- Produces: `corroboration_sheet(operations: list[dict], out_dir: Path, seed: int, ratio: int = 1) -> dict` (operations rows have `op_id, session_id, expert_id, problem_id, text, source`; targets are `source in {"ai_probe", "human_probe"}`; writes `corroboration_sheet.csv` (`item_id, blind_session, problem_id, operation_text`) and `corroboration_key.csv` (`item_id, op_id, is_decoy`); returns `{"targets": n, "decoys": n, "short": n}`); `alpha_nominal(a: dict[str, str], b: dict[str, str]) -> float`; `cohen_kappa(a: dict[str, str], b: dict[str, str]) -> float`; `decoy_false_rate(judgments: dict[str, bool], is_decoy: dict[str, bool]) -> float`; `guess_rate(guesses: dict[str, str], truth: dict[str, str]) -> float`; `guard_audit(sessions: list[LoadedSession], guard, statements: dict[str, str]) -> list[dict]`; `ai_rejection_counts(session_dir: Path) -> dict`; `probe_code.cli.main(argv=None)`.

- [ ] **Step 1: Write the failing test**

`instrument/tests/test_analysis.py`:

```python
import json

import pytest

from probe_code.agreement import alpha_nominal, cohen_kappa, decoy_false_rate, guess_rate
from probe_code.corroboration import corroboration_sheet
from probe_code.export import read_csv
from probe_code.guard_audit import ai_rejection_counts, guard_audit
from probe_code.loader import load_session
from probe_app.models import GuardVerdict
from test_export import make_session


def test_alpha_hand_computed():
    a = {"1": "a", "2": "a", "3": "b", "4": "b"}
    b = {"1": "a", "2": "b", "3": "b", "4": "b"}
    assert alpha_nominal(a, b) == pytest.approx(8 / 15)
    assert alpha_nominal(a, a) == pytest.approx(1.0)


def test_kappa_hand_computed():
    a = {"1": "a", "2": "a", "3": "b", "4": "b"}
    b = {"1": "a", "2": "b", "3": "b", "4": "b"}
    assert cohen_kappa(a, b) == pytest.approx(0.5)


def test_decoy_and_guess_rates():
    assert decoy_false_rate({"i1": True, "i2": False, "i3": True}, {"i1": True, "i2": True, "i3": False}) == 0.5
    assert guess_rate({"S1": "ai", "S2": "ai"}, {"S1": "ai", "S2": "human"}) == 0.5


def test_corroboration_mixes_decoys_from_other_experts_and_problems(tmp_path):
    ops = [
        {"op_id": "o1", "session_id": "s1", "expert_id": "E01", "problem_id": "A1", "text": "checks limiting case", "source": "ai_probe"},
        {"op_id": "o2", "session_id": "s1", "expert_id": "E01", "problem_id": "A1", "text": "notices sticking", "source": "trace_only"},
        {"op_id": "o3", "session_id": "s2", "expert_id": "E02", "problem_id": "B1", "text": "splits into stages", "source": "trace_only"},
        {"op_id": "o4", "session_id": "s2", "expert_id": "E02", "problem_id": "A1", "text": "same problem other expert", "source": "trace_only"},
    ]
    counts = corroboration_sheet(ops, tmp_path, seed=3)
    sheet = read_csv(tmp_path / "corroboration_sheet.csv")
    key = {r["item_id"]: r for r in read_csv(tmp_path / "corroboration_key.csv")}
    assert counts == {"targets": 1, "decoys": 1, "short": 0}
    decoy = next(r for r in sheet if key[r["item_id"]]["is_decoy"] == "True")
    assert key[decoy["item_id"]]["op_id"] == "o3"
    assert "is_decoy" not in sheet[0] and "op_id" not in sheet[0]


class FlagHuman:
    def check(self, utterance, problem_text, expert_text):
        return GuardVerdict(flagged="HUMAN" in utterance, introduced="x" if "HUMAN" in utterance else "")


def test_guard_audit_covers_both_arms(tmp_path):
    s = load_session(make_session(tmp_path, "E01"))
    rows = guard_audit([s], FlagHuman(), {p: p for p in ("A1", "A2", "B1", "B2")})
    by_arm = {r["arm"]: r["flagged"] for r in rows}
    assert by_arm == {"ai": False, "human": True}


def test_ai_rejection_counts(tmp_path):
    d = make_session(tmp_path, "E01")
    events = [{"type": "probe", "turn": {"source": "ai"}}, {"type": "probe", "turn": {"source": "ai_fallback"}},
              {"type": "turn_rejected", "reason": "leading: it introduces 'units'"},
              {"type": "turn_rejected", "reason": "contract: bad anchor"}]
    (d / "events.jsonl").write_text("\n".join(json.dumps(e) for e in events))
    assert ai_rejection_counts(d) == {"accepted": 1, "fallback": 1, "rejected_leading": 1, "rejected_contract": 1}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_analysis.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'probe_code.agreement'`.

- [ ] **Step 3: Write the implementation**

`instrument/src/probe_code/agreement.py`:

```python
import krippendorff
import numpy as np


def alpha_nominal(a: dict[str, str], b: dict[str, str]) -> float:
    units = sorted(set(a) | set(b))
    labels = sorted({*a.values(), *b.values()})
    code = {label: i for i, label in enumerate(labels)}
    data = np.array([[code[c[u]] if u in c else np.nan for u in units] for c in (a, b)], dtype=float)
    return float(krippendorff.alpha(reliability_data=data, level_of_measurement="nominal"))


def cohen_kappa(a: dict[str, str], b: dict[str, str]) -> float:
    units = sorted(set(a) & set(b))
    n = len(units)
    observed = sum(a[u] == b[u] for u in units) / n
    labels = {a[u] for u in units} | {b[u] for u in units}
    expected = sum((sum(a[u] == k for u in units) / n) * (sum(b[u] == k for u in units) / n) for k in labels)
    return (observed - expected) / (1 - expected)


def decoy_false_rate(judgments: dict[str, bool], is_decoy: dict[str, bool]) -> float:
    decoys = [i for i in judgments if is_decoy[i]]
    return sum(judgments[i] for i in decoys) / len(decoys)


def guess_rate(guesses: dict[str, str], truth: dict[str, str]) -> float:
    return sum(guesses[s] == truth[s] for s in guesses) / len(guesses)
```

`instrument/src/probe_code/corroboration.py`:

```python
import random
from collections import defaultdict
from pathlib import Path

from probe_code.export import write_csv

TARGET_SOURCES = {"ai_probe", "human_probe"}


def corroboration_sheet(operations: list[dict], out_dir: Path, seed: int, ratio: int = 1) -> dict:
    rng = random.Random(seed)
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for op in operations:
        if op["source"] in TARGET_SOURCES:
            groups[(op["session_id"], op["problem_id"])].append(op)
    sheet, key, used, short = [], [], set(), 0
    for (session_id, problem_id), targets in sorted(groups.items()):
        expert = targets[0]["expert_id"]
        pool = [o for o in operations if o["expert_id"] != expert and o["problem_id"] != problem_id
                and o["op_id"] not in used]
        want = len(targets) * ratio
        decoys = rng.sample(pool, min(want, len(pool)))
        short += want - len(decoys)
        used.update(o["op_id"] for o in decoys)
        blind = f"S{rng.getrandbits(32):08x}"
        items = [(o, False) for o in targets] + [(o, True) for o in decoys]
        rng.shuffle(items)
        for op, is_decoy in items:
            item_id = f"I{rng.getrandbits(40):010x}"
            sheet.append({"item_id": item_id, "blind_session": blind, "problem_id": problem_id,
                          "operation_text": op["text"]})
            key.append({"item_id": item_id, "op_id": op["op_id"], "is_decoy": is_decoy})
    write_csv(Path(out_dir) / "corroboration_sheet.csv", sheet)
    write_csv(Path(out_dir) / "corroboration_key.csv", key)
    return {"targets": sum(len(t) for t in groups.values()), "decoys": len(key) - sum(len(t) for t in groups.values()),
            "short": short}
```

`instrument/src/probe_code/guard_audit.py`:

```python
import json
from pathlib import Path

from probe_code.loader import LoadedSession


def guard_audit(sessions: list[LoadedSession], guard, statements: dict[str, str]) -> list[dict]:
    rows = []
    for s in sessions:
        for set_id, turns in s.state.dialogue.items():
            pids = s.state.sets[set_id]
            problem_text = "\n".join(f"{p}: {statements[p]}" for p in pids)
            said = [seg.text for seg in s.state.segments if seg.problem_id in pids]
            for index, turn in enumerate(turns):
                if turn.speaker == "expert":
                    said.append(turn.text)
                    continue
                verdict = guard.check(turn.text, problem_text, "\n".join(said))
                rows.append({"session_id": s.session_id, "set_id": set_id, "arm": s.state.arms[set_id],
                             "source": turn.source, "turn_index": index, "flagged": verdict.flagged,
                             "introduced": verdict.introduced})
    return rows


def ai_rejection_counts(session_dir: Path) -> dict:
    path = Path(session_dir) / "events.jsonl"
    events = [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []
    probes = [e["turn"]["source"] for e in events if e["type"] == "probe"]
    reasons = [e["reason"] for e in events if e["type"] == "turn_rejected"]
    return {"accepted": probes.count("ai"), "fallback": probes.count("ai_fallback"),
            "rejected_leading": sum(r.startswith("leading") for r in reasons),
            "rejected_contract": sum(r.startswith("contract") for r in reasons)}
```

`instrument/src/probe_code/cli.py`:

```python
import argparse
import json
from pathlib import Path

from dotenv import load_dotenv

from probe_app.config import INSTRUMENT_DIR, load_problems, load_prompt
from probe_code.agreement import alpha_nominal, cohen_kappa, decoy_false_rate, guess_rate
from probe_code.corroboration import corroboration_sheet
from probe_code.export import export_blind, export_trace, read_csv, write_csv
from probe_code.guard_audit import ai_rejection_counts, guard_audit
from probe_code.loader import load_session


def _labels(path: Path, id_col: str, label_col: str) -> dict[str, str]:
    return {r[id_col]: r[label_col] for r in read_csv(path) if r[label_col] != ""}


def _truthy(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "y", "yes"}


def main(argv: list[str] | None = None) -> None:
    load_dotenv(INSTRUMENT_DIR / ".env")
    p = argparse.ArgumentParser(prog="probe-code")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("export-blind", "export-trace", "guard-audit"):
        c = sub.add_parser(name)
        c.add_argument("sessions", nargs="+", type=Path)
        c.add_argument("--out", type=Path, required=True)
        c.add_argument("--seed", type=int, default=0)
        c.add_argument("--allow-simulated", action="store_true")
    c = sub.add_parser("corroboration")
    c.add_argument("operations", type=Path)
    c.add_argument("--out", type=Path, required=True)
    c.add_argument("--seed", type=int, default=0)
    for name in ("alpha", "kappa"):
        c = sub.add_parser(name)
        c.add_argument("a", type=Path)
        c.add_argument("b", type=Path)
        c.add_argument("--id", default="unit_id")
        c.add_argument("--label", default="label")
    c = sub.add_parser("decoys")
    c.add_argument("judgments", type=Path, help="item_id, corroborated")
    c.add_argument("key", type=Path, help="corroboration_key.csv")
    c = sub.add_parser("guesses")
    c.add_argument("guesses", type=Path, help="blind_session, arm")
    c.add_argument("key", type=Path, help="key_units.csv")
    args = p.parse_args(argv)

    if args.cmd in ("export-blind", "export-trace", "guard-audit"):
        sessions = [load_session(s, args.allow_simulated) for s in args.sessions]
        if args.cmd == "export-blind":
            export_blind(sessions, args.out, args.seed)
        elif args.cmd == "export-trace":
            export_trace(sessions, args.out, args.seed)
        else:
            import anthropic

            from probe_app.llm import Guard

            log = args.out / "guard_audit_llm.jsonl"
            args.out.mkdir(parents=True, exist_ok=True)
            guard = Guard(anthropic.Anthropic(), lambda r: log.open("a").write(json.dumps(r) + "\n"),
                          load_prompt("guard_system.md"))
            statements = {k: v["statement"] for k, v in load_problems()["problems"].items()}
            rows = guard_audit(sessions, guard, statements)
            write_csv(args.out / "guard_audit.csv", rows)
            for arm in ("ai", "human"):
                arm_rows = [r for r in rows if r["arm"] == arm]
                if arm_rows:
                    print(f"{arm}: {sum(r['flagged'] for r in arm_rows)}/{len(arm_rows)} questions flagged")
            for s in sessions:
                print(s.session_id, ai_rejection_counts(s.dir))
    elif args.cmd == "corroboration":
        print(corroboration_sheet(read_csv(args.operations), args.out, args.seed))
    elif args.cmd in ("alpha", "kappa"):
        a, b = _labels(args.a, args.id, args.label), _labels(args.b, args.id, args.label)
        print(f"{(alpha_nominal if args.cmd == 'alpha' else cohen_kappa)(a, b):.3f}")
    elif args.cmd == "decoys":
        judgments = {r["item_id"]: _truthy(r["corroborated"]) for r in read_csv(args.judgments)}
        is_decoy = {r["item_id"]: _truthy(r["is_decoy"]) for r in read_csv(args.key)}
        print(f"false corroboration on decoys: {decoy_false_rate(judgments, is_decoy):.3f}")
    elif args.cmd == "guesses":
        guesses = {r["blind_session"]: r["arm"] for r in read_csv(args.guesses)}
        truth = {r["blind_session"]: r["arm"] for r in read_csv(args.key)}
        print(f"condition guessed correctly: {guess_rate(guesses, truth):.3f} (chance 0.5)")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_analysis.py -v`
Expected: 7 passed.

- [ ] **Step 5: Run the whole suite**

Run: `uv run pytest -v`
Expected: all tests pass.

- [ ] **Step 6: Commit**

```bash
git add instrument/src/probe_code instrument/tests/test_analysis.py
git commit -m "Coding pipeline: corroboration decoys, agreement statistics, guard audit, CLI"
```

---

### Task 13: Codebook v0, pilot protocol, experiment-design amendment

**Files:**
- Create: `instrument/codebook/v0.md`, `instrument/pilot-protocol.md`
- Modify: `research/experiment-ai-assisted-cta-physics.md` (Stage A session-order step 3), `PROGRESS.md` (Experiment design section)

**Interfaces:**
- Consumes: the commands of Tasks 10 and 12; the problems of Task 1.

- [ ] **Step 1: Write `instrument/codebook/v0.md`**

```markdown
# Codebook v0: mental operations in expert physics problem solving

Status: skeleton. The two pilot sessions fill the definitions and examples; the version used for Stage A is frozen before the first data session.

## Unit

A **mental operation**: a cue, decision, representation choice, check or heuristic that a novice could be taught. One unit of the blinded export (a sentence of an expert answer) may contain zero, one or several operations.

## Type (map §9 Phase 1 taxonomy)

| Type | Definition | Include | Exclude | Example (from pilots) |
|---|---|---|---|---|
| Omitted prerequisite | Knowledge the expert uses but ordinary material assumes | | | |
| Perceptual cue | A feature of the problem the expert notices that triggers a decision | | | |
| Representation choice | Choosing a diagram, system boundary, coordinate or quantity to work in | | | |
| Decomposition strategy | Splitting the problem into stages or sub-problems | | | |
| Decision criterion | The condition that decides which principle applies | | | |
| Conceptual model | The physical picture the expert reasons with | | | |
| Error-checking routine | A check on a step or result | | | |
| Metacognitive judgment | Monitoring of progress, difficulty or confidence | | | |
| Disciplinary norm / epistemic standard | What counts as an acceptable answer or argument | | | |

## Source (assigned from the key, never by the coder)

explanation · trace-only · AI probe · human probe

## Status

| Status | Rule |
|---|---|
| trace-only | Extracted from the think-aloud and written work by a coder who has not seen probe material |
| probe-added, performed | Named first in a probe answer, then corroborated in the trace by a third coder blind to interviewer, with decoys mixed in |
| reported only | Named in a probe answer, not corroborated in the trace |
| contradicted | The trace shows the expert doing something else |

## Cross-expert matching

Two operations are **the same** if a novice taught either would perform the same action in the same situation. Record matches in `matches.csv` (`op_id_a, op_id_b, same`); agreement by κ.

## Framework tag

Tag `published=yes` if the operation appears in Heller & Reif (1984), Dufresne et al. (1992) or Docktor et al. (2015).
```

- [ ] **Step 2: Write `instrument/pilot-protocol.md`**

```markdown
# Pilot protocol: Stage A session app

**Purpose.** Check that the instrument runs a full session and build codebook v0. Pilot sessions are never Stage A data.

**Participants.** One or two physicists who have taught first-year mechanics. Not eligible for Stage A afterwards.

## Before the session

1. Ethics: pilot consent form names ElevenLabs and OpenAI (audio) and Anthropic (transcripts, written-work images) as processors; data-processing terms and retention settings confirmed for all three accounts. Stage A consent names only the transcriber that is frozen.
2. Keys in `instrument/.env` (`ANTHROPIC_API_KEY`, `ELEVEN_LABS_API_KEY`, `OPENAI_API_KEY`); never committed.
3. Tablet over the network needs HTTPS: `mkcert -install && mkcert <laptop-LAN-IP>`, install the mkcert root CA on the tablet, then
   `uv run probe-app serve --host 0.0.0.0 --ssl-certfile <ip>.pem --ssl-keyfile <ip>-key.pem`.
   In person on the laptop itself: `uv run probe-app serve` and use `http://127.0.0.1:8000`.
4. A physicist checks the four problems in `problems/problems.json`.
5. `uv run probe-app simulate` once; confirm the simulated session completes.

## Session (about 75 minutes)

1. Consent (5 min).
2. **Ordinary explanation (10 min, paper).** "Write a worked explanation of these two problems for a first-year student": one problem from set A, one from set B, not used later. Scan it into `sessions/<id>/explanation/`.
3. **Think-aloud (about 20 min).** Console: create a pilot session, give the expert the link, press "Start next problem" for each of the four problems. Instructions only: "Solve it and say everything you are thinking, including anything that feels obvious." The only allowed prompt is "Keep talking" (console button) after about 10 s of silence. Do not reload the expert page during a problem: the audio recorded so far would be lost.
4. **Trace review (5 min, researcher only).** Correct transcription errors in physics terms; do not add content.
5. **Probe session, set 1 (up to 20 min)** and **set 2 (up to 20 min)**: AI on one set, human on the other, as chosen at creation. Human interviewer: press I/E at every change of speaker, tick each stem as you use it, click a transcript row to show it to the expert, at most one follow-up per stem question and only restating the expert's words.
6. **Debrief (5 min).** "Did any question feel like it was putting words in your mouth? Which questions made you think of something you had not said before?"

## Measured

- The session ran end to end using only the console controls (note every workaround).
- AI latency: median gap between `expert_answer` and the next `probe` event (target under 6 s).
- `probe-code guard-audit` flag rates for both arms, and `turn_rejected` counts.
- Transcription errors on physics terms in 5 minutes of audio checked by hand, for both transcribers on the same files: `uv run probe-app transcribe sessions/<id>/audio/think_A1.webm --model scribe_v2` and `--model whisper-1`. Freeze the one with fewer physics-term errors.
- **Success criterion 3:** at least one operation in the think-aloud trace absent from the expert's ordinary explanation. If none, revise the probe script before recruiting.
- Debrief answers.

## After the pilots

1. Fill `codebook/v0.md` from the pilot transcripts; two coders try it on one pilot session.
2. Adjust `INTERVIEWER_EFFORT` and the prompts if the pilots require it.
3. `uv run probe-app freeze`, commit `prereg.json` together with the prompts, and list the hashes in the pre-registration. From then on, any prompt edit makes the app refuse data sessions.
```

- [ ] **Step 3: Amend the experiment design**

In `research/experiment-ai-assisted-cta-physics.md`, replace:

```
   - The model, prompt and temperature are frozen and logged. Both interviewers follow the same rule for unscripted follow-ups: at most one follow-up per scripted probe, restating the expert's own words. With one human interviewer, the claim is scoped to "vs this interviewer".
```

with:

```
   - The model ID, effort setting and prompt hashes are frozen, and the app refuses a data session if they differ from the pre-registered values. Current models do not accept a sampling temperature, so every request and response is logged in full instead. Both interviewers follow the same rule for unscripted follow-ups: at most one follow-up per scripted probe, restating the expert's own words; for the AI the app checks that the quoted words occur in the expert's speech. Both interviewers use the same session app (`instrument/`). With one human interviewer, the claim is scoped to "vs this interviewer".
```

Run: `grep -n "prompt hashes are frozen" research/experiment-ai-assisted-cta-physics.md`
Expected: one match.

- [ ] **Step 4: Update PROGRESS.md**

Under `### Experiment design`, add:

```
- [x] Stage A instrument built: session app and coding pipeline in `instrument/` ([spec](docs/superpowers/specs/2026-09-26-stage-a-session-app-design.md)). Next: pilot on 1–2 physicists (`instrument/pilot-protocol.md`), then freeze.
```

- [ ] **Step 5: Commit**

```bash
git add instrument/codebook instrument/pilot-protocol.md research/experiment-ai-assisted-cta-physics.md PROGRESS.md
git commit -m "Stage A: codebook v0 skeleton, pilot protocol, frozen-config wording in the design"
```
