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
