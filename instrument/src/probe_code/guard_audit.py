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
            "rejected_contract": sum(r.startswith("contract") for r in reasons),
            "interviewer_failed": sum(e["type"] == "interviewer_failed" for e in events)}
