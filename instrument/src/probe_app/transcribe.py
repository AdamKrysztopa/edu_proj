import os
from pathlib import Path
from typing import Protocol

from pydantic import BaseModel

from probe_app.config import load_models

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
        if client is None:
            from openai import OpenAI

            client = OpenAI()
        self.model, self.client = model, client

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


def make_transcriber(model: str | None = None, client=None) -> Transcriber:
    model = model or load_models().transcriber.model
    if model.startswith("scribe"):
        return ScribeTranscriber(model, client)
    return OpenAITranscriber(model, client)
