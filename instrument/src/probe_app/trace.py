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
