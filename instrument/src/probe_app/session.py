import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from probe_app.backends import Backends
from probe_app.config import (CAP_S, PREREG_PATH, WRAP_S, ConfigMismatch, check_preregistered, current_config, git_commit,
                              git_dirty, load_models, load_problems, load_stems)
from probe_app.contract import ContractState, uncovered
from probe_app.engine import ProbeContext, ProbeEngine
from probe_app.human import turns_from_markers, unmarked_warning, unmarked_words
from probe_app.llm import make_guard, make_interviewer
from probe_app.models import STEMS, Anchor, DialogueTurn, Segment
from probe_app.storage import SessionStore
from probe_app.trace import build_segments, correct_segment
from probe_app.transcribe import RawSegment, TranscriptionFailed, transcribe_with_retry


CHUNK_S = 1.0  # MediaRecorder timeslice in web/js/expert.js
HOLE_S = 2.0


class PhaseError(Exception):
    pass


class DuplicateSubmission(Exception):
    pass


@dataclass
class Deps:
    transcriber: object
    backends: Backends


def check_deps_match_models(deps: Deps, simulated: bool) -> None:
    models = load_models()
    stale = [role for role in ("interviewer", "guard") if getattr(deps.backends, role).role != getattr(models, role)]
    if not simulated and deps.transcriber.model != models.transcriber.model:
        stale.append("transcriber")
    if stale:
        raise ConfigMismatch(f"models.json changed since the server started ({', '.join(stale)}): restart probe-app serve")


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
    untranscribed: list[str] = []
    probes_done: list[str] = []
    segments: list[Segment] = []
    dialogue: dict[str, list[DialogueTurn]] = {}
    contract: dict[str, ContractState] = {}
    timer: ProbeTimer = ProbeTimer()
    anchor: Anchor | None = None
    anchor_problem: str | None = None
    markers: dict[str, list[dict]] = {}
    recordings: dict[str, list[dict]] = {}
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
        if not re.fullmatch(r"[A-Za-z0-9_-]+", expert_id):
            raise ValueError("expert_id may contain only letters, digits, '-' and '_'")
        problems = load_problems()
        if sorted(set_order) != sorted(problems["sets"]) or set(arms) != set(set_order):
            raise ValueError(f"set_order and arms must cover exactly the sets {sorted(problems['sets'])}")
        if not set(arms.values()) <= {"ai", "human"}:
            raise ValueError("arms must be 'ai' or 'human'")
        cfg = current_config()
        check_deps_match_models(deps, simulated)
        dirty = git_dirty()
        if not pilot:
            models = load_models()
            unrouted = [r for r in ("interviewer", "guard")
                        if getattr(models, r).provider == "openrouter" and not getattr(models, r).route]
            if unrouted:
                raise ConfigMismatch(f"{', '.join(unrouted)} on openrouter without a route: pin the upstream "
                                     "in models.json before a data session")
            check_preregistered(cfg, PREREG_PATH)
            if dirty:
                raise ConfigMismatch("instrument/ has uncommitted changes: commit them before a data session")
        manifest = {"expert_id": expert_id, "cell": cell, "arms": arms, "set_order": set_order,
                    "pilot": pilot, "simulated": simulated, "cap_s": CAP_S, "wrap_s": WRAP_S,
                    "config": asdict(cfg), "transcriber": deps.transcriber.model, "git_commit": git_commit(), "git_dirty": dirty}
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

    # recordings: the tablet streams 1 s chunks; each (re)start of its recorder opens a new part on the server clock

    def _current_stream(self) -> str | None:
        st = self.state
        if st.phase == "think_aloud":
            return f"think_{st.current_problem}"
        if st.phase in ("probe", "probe_uploading") and self._arm() == "human":
            return f"probe_{st.current_set}"
        return None

    def _require_stream(self, stream: str) -> list[dict]:
        if stream != self._current_stream():
            raise PhaseError(f"recording '{stream}' is not open; the session is in '{self.state.phase}'")
        return self.state.recordings.setdefault(stream, [])

    def recording_start(self, stream: str) -> int:
        parts = self._require_stream(stream)
        now = self._now()
        if parts:
            prev = parts[-1]
            hole = now - prev["start"] - prev["chunks"] * CHUNK_S
            if hole > HOLE_S:
                prev["hole_s"] = round(hole, 1)
                self.state.error = (f"Audio hole in {stream}: {prev['hole_s']} s after part {prev['part']} "
                                    "never arrived (tablet reloaded?).")
                self.store.log("audio_hole", stream=stream, part=prev["part"], hole_s=prev["hole_s"])
        parts.append({"part": len(parts) + 1, "start": now, "chunks": 0})
        self.store.log("recording_started", stream=stream, part=len(parts))
        self.save()
        return len(parts)

    def recording_chunk(self, stream: str, part: int, seq: int, data: bytes) -> bool:
        parts = self._require_stream(stream)
        if not 1 <= part <= len(parts):
            raise ValueError(f"unknown part {part} of {stream}")
        entry = parts[part - 1]
        if seq < entry["chunks"]:
            return False
        if seq > entry["chunks"]:
            if "gap_at" not in entry:
                entry["gap_at"] = entry["chunks"]
                self.state.error = (f"Audio gap in {stream} part {part} from chunk {entry['chunks']}; "
                                    "the tablet starts a new part.")
                self.store.log("chunk_refused", stream=stream, part=part, seq=seq, expected=entry["chunks"])
                self.save()
            return True
        with self.store.path(f"audio/{stream}.part{part}.webm").open("ab") as f:
            f.write(data)
        entry["chunks"] += 1
        self.save()
        return False

    def _store_single_part(self, stream: str, audio: bytes, start: float) -> None:
        if any(e["chunks"] for e in self.state.recordings.get(stream, [])):
            raise ValueError(f"{stream} was already streamed; a whole-audio upload would replace it")
        self.store.path(f"audio/{stream}.part1.webm").write_bytes(audio)
        self.state.recordings[stream] = [{"part": 1, "start": start, "chunks": 1}]

    def _transcribe_stream(self, stream: str) -> list[RawSegment]:
        merged: list[RawSegment] = []
        missing: list[str] = []
        for entry in self.state.recordings.get(stream, []):
            path = self.store.path(f"audio/{stream}.part{entry['part']}.webm")
            if not path.exists():
                if entry["chunks"]:
                    missing.append(path.name)
                continue
            raw = transcribe_with_retry(self.deps.transcriber, path)
            self.store.write_json(f"transcripts/{stream}.part{entry['part']}.raw.json", [r.model_dump() for r in raw])
            merged += [r.model_copy(update={"start": r.start + entry["start"], "end": r.end + entry["start"]})
                       for r in raw]
        if missing:
            raise TranscriptionFailed(f"audio file {', '.join(missing)} is missing")
        return merged

    def _stream_holes(self, stream: str) -> list[str]:
        holes = []
        for e in self.state.recordings.get(stream, []):
            if "gap_at" in e:
                holes.append(f"part {e['part']} from chunk {e['gap_at']}")
            if "hole_s" in e:
                holes.append(f"{e['hole_s']} s after part {e['part']}")
        return holes

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

    def end_think_aloud(self, problem_id: str, audio: bytes | None, snapshot_png: bytes, strokes: list) -> None:
        self._require("think_aloud")
        if problem_id != self.state.current_problem:
            raise PhaseError(f"current problem is {self.state.current_problem}, not {problem_id}")
        stream = f"think_{problem_id}"
        if audio is not None:
            self._store_single_part(stream, audio, self.state.recording_start)
        self.snapshot_path(problem_id).write_bytes(snapshot_png)
        self.store.write_json(f"canvas/strokes_{problem_id}.json", strokes)
        self.store.log("think_aloud_ended", problem_id=problem_id, n_strokes=len(strokes))
        try:
            segments = build_segments(problem_id, 0.0, self._transcribe_stream(stream))
            if not segments:
                raise TranscriptionFailed("no speech was recorded")
            self.state.segments += segments
            holes = self._stream_holes(stream)
            if holes:
                self.state.untranscribed.append(problem_id)
                self.state.error = (f"Audio missing in {stream} ({'; '.join(holes)}): add what the expert said "
                                    f"there as a segment of {problem_id}, or accept the gap, before probing.")
                self.store.log("audio_incomplete", problem_id=problem_id, holes=holes)
        except TranscriptionFailed as e:
            self.state.untranscribed.append(problem_id)
            self.state.error = f"Transcription failed for {problem_id}: {e}. Type the transcript in the console."
            self.store.log("transcription_failed", problem_id=problem_id, error=str(e))
        self.state.think_aloud_done.append(problem_id)
        self.state.current_problem = None
        remaining = [p for p in self.state.problem_order if p not in self.state.think_aloud_done]
        self.state.phase = "ready" if remaining else "trace_review"
        self.save()

    def _require_unlocked(self, problem_id: str) -> None:
        probed = set(self.state.probes_done) | ({self.state.current_set} if self.state.current_set else set())
        if any(problem_id in self.state.sets[s] for s in probed):
            raise PhaseError(f"the trace of {problem_id} is locked: its probe set has already run")

    def correct_segment(self, segment_id: str, text: str) -> None:
        self._require("ready", "trace_review")
        owner = next((s.problem_id for s in self.state.segments if s.id == segment_id), None)
        if owner is None:
            raise KeyError(f"no segment {segment_id}")
        self._require_unlocked(owner)
        self.state.segments, diff = correct_segment(self.state.segments, segment_id, text)
        self.store.log("segment_corrected", **diff)
        self.save()

    def add_segment(self, problem_id: str, text: str) -> None:
        self._require("ready", "trace_review")
        if problem_id not in self.state.think_aloud_done:
            raise PhaseError(f"{problem_id} has no think-aloud yet")
        self._require_unlocked(problem_id)
        n = sum(1 for s in self.state.segments if s.id.startswith(f"{problem_id}-m")) + 1
        segment = Segment(id=f"{problem_id}-m{n:03d}", problem_id=problem_id, start=0.0, end=0.0, text=text)
        self.state.segments.append(segment)
        if problem_id in self.state.untranscribed:
            self.state.untranscribed.remove(problem_id)
        if not self.state.untranscribed:
            self.state.error = None
        self.store.log("segment_added", **segment.model_dump())
        self.save()

    def acknowledge_incomplete_audio(self, problem_id: str, note: str) -> None:
        self._require("ready", "trace_review")
        self._require_unlocked(problem_id)
        transcribed = any(s.problem_id == problem_id for s in self.state.segments)
        if problem_id not in self.state.untranscribed or not transcribed \
                or not self._stream_holes(f"think_{problem_id}"):
            raise PhaseError(f"{problem_id} has no transcribed audio with a gap to accept: type the transcript")
        self.state.untranscribed.remove(problem_id)
        if not self.state.untranscribed:
            self.state.error = None
        self.store.log("audio_incomplete_acknowledged", problem_id=problem_id, note=note)
        self.save()

    # probe

    def _check_config(self) -> None:
        frozen, now = self.manifest["config"], asdict(current_config())
        drift = sorted(k for k in now if frozen.get(k) != now[k])
        if drift:
            raise ConfigMismatch(f"configuration changed since this session was created: {drift}")
        check_deps_match_models(self.deps, self.manifest["simulated"])

    def _engine(self, set_id: str) -> ProbeEngine:
        self._check_config()
        llm = make_interviewer(self.deps.backends.interviewer, self.store.log_llm)
        guard = make_guard(self.deps.backends.guard, self.store.log_llm)
        pids = self.state.sets[set_id]
        snapshots = {p: self.snapshot_path(p).read_bytes() for p in pids if self.snapshot_path(p).exists()}
        ctx = ProbeContext(set_id=set_id,
                           problems={p: self.problems["problems"][p]["statement"] for p in pids},
                           segments=[s for s in self.state.segments if s.problem_id in pids],
                           snapshots=snapshots)
        return ProbeEngine(llm, guard, self.stems, ctx, self.store, self.state.contract[set_id],
                           cap_s=self.manifest["cap_s"], wrap_s=self.manifest["wrap_s"], elapsed=self.elapsed)

    def start_probe(self) -> str:
        self._require("trace_review")
        st = self.state
        set_id = next(s for s in st.set_order if s not in st.probes_done)
        missing = [p for p in st.sets[set_id] if p in st.untranscribed]
        if missing:
            raise PhaseError(f"type the transcript for {missing} (or accept its audio gap) before probing set {set_id}")
        self._check_config()
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
        self._check_config()
        if speaker not in ("interviewer", "expert"):
            raise ValueError("speaker must be 'interviewer' or 'expert'")
        mark = {"speaker": speaker, "t": self.elapsed(), "mono": self._now()}
        self.state.markers[set_id].append(mark)
        self.store.log("turn_marker", set_id=set_id, **mark)
        self.save()

    def human_stem(self, problem_id: str, stem_id: str) -> None:
        set_id = self._require_human_probe()
        self._check_config()
        if problem_id not in self.state.sets[set_id] or stem_id not in STEMS:
            raise ValueError(f"unknown problem or stem: {problem_id}/{stem_id}")
        tick = {"problem_id": problem_id, "stem_id": stem_id, "t": self.elapsed(), "mono": self._now()}
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

    def finalize_human_probe(self, audio: bytes | None = None) -> None:
        self._require("probe_uploading")
        st = self.state
        set_id, stream = st.current_set, f"probe_{st.current_set}"
        if audio is not None:
            self._store_single_part(stream, audio, st.timer.started)
        try:
            raw = self._transcribe_stream(stream)
            markers = [{"speaker": m["speaker"], "t": m["mono"]} for m in st.markers[set_id]]
            ticks = [{**t, "t": t["mono"]} for t in st.ticks[set_id]]
            turns = turns_from_markers(raw, markers, ticks)
            if not turns:
                raise TranscriptionFailed("no speech was recorded")
            for turn in turns:
                turn.t -= st.timer.started
            st.dialogue[set_id] = turns
            problems = []
            warning = unmarked_warning(turns)
            if warning:
                problems.append(f"Probe set {set_id}: {warning}.")
                self.store.log("unmarked_speech", set_id=set_id, words=unmarked_words(turns), warning=warning)
            holes = self._stream_holes(stream)
            if holes:
                problems.append(f"Audio missing in {stream} ({'; '.join(holes)}): the dialogue of set {set_id} "
                                "is incomplete there.")
                self.store.log("audio_incomplete", set_id=set_id, holes=holes)
            if problems:
                st.error = " ".join(problems)
        except TranscriptionFailed as e:
            st.error = f"Probe audio for set {set_id} could not be transcribed ({e}); any audio is saved under audio/{stream}.part*.webm."
            self.store.log("transcription_failed", set_id=set_id, error=str(e))
        self._finish_probe()
        self.save()

    def enforce_cap(self) -> bool:
        if self.state.phase != "probe" or self.state.paused or self.elapsed() < self.manifest["cap_s"]:
            return False
        self.store.log("cap_reached", set_id=self.state.current_set, elapsed=self.elapsed())
        self.end_probe()
        return True

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
