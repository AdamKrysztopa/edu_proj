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
    interviewer_marks = [m["t"] for m in marks if m["speaker"] == "interviewer"]
    for tick in sorted(ticks, key=lambda x: x["t"]):
        since = max((t for t in interviewer_marks if t <= tick["t"]), default=float("-inf"))
        target = next((x for x in turns if x.speaker == "interviewer" and x.t >= since), None)
        if target is not None and target.stem_id is None:
            target.stem_id, target.problem_id = tick["stem_id"], tick["problem_id"]
    return turns
