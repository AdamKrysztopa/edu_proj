import csv
import random
import re
import shutil
from pathlib import Path

from probe_code.guard_audit import interviewer_questions, question_source, unmarked_speech
from probe_code.loader import LoadedSession

SENTENCE_END = re.compile(r"(?<=[.!?])\s+")
FILLER = re.compile(r"\b(?:u+m+|u+h+|e+r+m*|h+m+|m+h*m+)\b[,.]?\s*", re.IGNORECASE)


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
    rng = random.Random(f"trace:{seed}")
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


def export_leading(sessions: list[LoadedSession], out_dir: Path, seed: int, statements: dict[str, str]) -> None:
    """Bare-stem fallbacks go to the key only, preset non-leading, so the AI arm's denominator keeps them.
    Unmarked human-arm speech goes to the key only, unlabelled: its speaker is unknown."""
    rng = random.Random(f"leading:{seed}")
    items, key = [], []
    for s in sessions:
        for set_id, index, turn, problem_text, said in interviewer_questions(s, statements):
            item_id = f"Q{rng.getrandbits(48):012x}"
            source = question_source(turn)
            key.append({"item_id": item_id, "session_id": s.session_id, "expert_id": s.manifest["expert_id"],
                        "set_id": set_id, "arm": s.state.arms[set_id], "source": source, "turn_index": index,
                        "pilot": s.manifest.get("pilot", False), "preset_leading": "0" if source == "ai_fallback" else ""})
            if source not in ("ai_fallback", "unmarked"):
                items.append({"item_id": item_id, "problems": problem_text, "expert_said": said,
                              "question": FILLER.sub("", turn.text).strip(), "leading": "", "introduced": "",
                              "arm_guess": ""})
    rng.shuffle(items)
    rng.shuffle(key)
    write_csv(out_dir / "leading_items.csv", items)
    write_csv(out_dir / "key_leading.csv", key)


def write_unmarked_key(sessions: list[LoadedSession], out_dir: Path) -> None:
    write_csv(out_dir / "key_unmarked.csv",
              [{"session_id": s.session_id, "set_id": set_id, "arm": s.state.arms[set_id], "words": words}
               for s in sessions for set_id, words in sorted(unmarked_speech(s).items())])
