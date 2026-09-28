import json
from dataclasses import asdict
from pathlib import Path

from probe_app.config import current_config
from probe_code.loader import LoadedSession


def config_drift(session: LoadedSession) -> list[str]:
    frozen, now = session.manifest.get("config", {}), asdict(current_config())
    return sorted(k for k in now if frozen.get(k) != now[k])


def interviewer_questions(session: LoadedSession, statements: dict[str, str]):
    """Each interviewer turn with the problem text and expert words the live guard would have been given."""
    for set_id, turns in session.state.dialogue.items():
        pids = session.state.sets[set_id]
        problem_text = "\n".join(f"{p}: {statements[p]}" for p in pids)
        said = [seg.text for seg in session.state.segments if seg.problem_id in pids]
        for index, turn in enumerate(turns):
            if turn.speaker == "expert":
                said.append(turn.text)
                continue
            yield set_id, index, turn, problem_text, "\n".join(said)


def guard_audit(sessions: list[LoadedSession], guard, statements: dict[str, str]) -> list[dict]:
    rows = []
    for s in sessions:
        for set_id, index, turn, problem_text, said in interviewer_questions(s, statements):
            verdict = guard.check(turn.text, problem_text, said)
            rows.append({"session_id": s.session_id, "set_id": set_id, "arm": s.state.arms[set_id],
                         "source": turn.source, "turn_index": index, "flagged": verdict.flagged,
                         "introduced": verdict.introduced})
    return rows


def leading_by_arm(labels: dict[str, str], key: list[dict]) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    for row in key:
        label = labels.get(row["item_id"]) or row.get("preset_leading", "")
        if not label:
            continue
        counts = out.setdefault(row["arm"], {"leading": 0, "coded": 0})
        counts["coded"] += 1
        counts["leading"] += label.strip().lower() in {"1", "true", "y", "yes"}
    return out


def ai_rejection_counts(session_dir: Path) -> dict:
    path = Path(session_dir) / "events.jsonl"
    events = [json.loads(line) for line in path.read_text().splitlines() if line.strip()] if path.exists() else []
    probes = [e["turn"]["source"] for e in events if e["type"] == "probe"]
    reasons = [e["reason"] for e in events if e["type"] == "turn_rejected"]
    failures = [e["reason"] for e in events if e["type"] == "interviewer_failed"]
    return {"accepted": probes.count("ai"), "fallback": probes.count("ai_fallback"),
            "rejected_leading": sum(r.startswith("leading") for r in reasons),
            "rejected_contract": sum(r.startswith("contract") for r in reasons),
            "interviewer_refused": sum(r.startswith("LLMRefused") for r in failures),
            "interviewer_unavailable": sum(r.startswith("LLMUnavailable") for r in failures),
            "guard_failed": sum(e["type"] == "guard_failed" for e in events)}
