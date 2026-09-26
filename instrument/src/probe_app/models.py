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
