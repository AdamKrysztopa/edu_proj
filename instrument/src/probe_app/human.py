from probe_app.models import DialogueTurn
from probe_app.transcribe import RawSegment


def turns_from_markers(raw: list[RawSegment], markers: list[dict], ticks: list[dict]) -> list[DialogueTurn]:
    """Markers, ticks and segments must share one clock. A segment belongs to whoever held the floor at its midpoint;
    before the first marker nobody did, so that speech is "unmarked" and kept out of every export and audit."""
    marks = sorted(markers, key=lambda m: m["t"])
    turns: list[DialogueTurn] = []
    midpoints: list[float] = []
    for seg in raw:
        mid = (seg.start + seg.end) / 2
        speaker = "unmarked"
        for m in marks:
            if m["t"] > mid:
                break
            speaker = m["speaker"]
        if turns and turns[-1].speaker == speaker:
            turns[-1].text = f"{turns[-1].text} {seg.text}"
        else:
            turns.append(DialogueTurn(speaker=speaker, text=seg.text, t=seg.start,
                                      source="human" if speaker == "interviewer" else "transcribed"))
            midpoints.append(mid)
    interviewer_marks = [m["t"] for m in marks if m["speaker"] == "interviewer"]
    for tick in sorted(ticks, key=lambda x: x["t"]):
        since = max((t for t in interviewer_marks if t <= tick["t"]), default=float("-inf"))
        target = next((x for x, mid in zip(turns, midpoints) if x.speaker == "interviewer" and mid >= since), None)
        if target is not None and target.stem_id is None:
            target.stem_id, target.problem_id = tick["stem_id"], tick["problem_id"]
    return turns


def unmarked_words(turns: list[DialogueTurn]) -> int:
    return sum(len(t.text.split()) for t in turns if t.speaker == "unmarked")


def unmarked_warning(turns: list[DialogueTurn]) -> str | None:
    words = unmarked_words(turns)
    if not any(t.speaker == "expert" for t in turns):
        return f"no speech is marked as the expert's (E); {words} unmarked words are excluded from coding"
    if words:
        return f"{words} words before the first I/E marker are excluded from coding"
    return None
