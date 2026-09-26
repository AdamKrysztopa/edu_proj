import random
from collections import defaultdict
from pathlib import Path

from probe_code.export import write_csv

TARGET_SOURCES = {"ai_probe", "human_probe"}


def corroboration_sheet(operations: list[dict], out_dir: Path, seed: int, ratio: int = 1) -> dict:
    rng = random.Random(seed)
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for op in operations:
        if op["source"] in TARGET_SOURCES:
            groups[(op["session_id"], op["problem_id"])].append(op)
    sheet, key, used, short = [], [], set(), 0
    for (session_id, problem_id), targets in sorted(groups.items()):
        expert = targets[0]["expert_id"]
        pool = [o for o in operations if o["expert_id"] != expert and o["problem_id"] != problem_id
                and o["op_id"] not in used]
        want = len(targets) * ratio
        decoys = rng.sample(pool, min(want, len(pool)))
        short += want - len(decoys)
        used.update(o["op_id"] for o in decoys)
        blind = f"S{rng.getrandbits(32):08x}"
        items = [(o, False) for o in targets] + [(o, True) for o in decoys]
        rng.shuffle(items)
        for op, is_decoy in items:
            item_id = f"I{rng.getrandbits(40):010x}"
            sheet.append({"item_id": item_id, "blind_session": blind, "problem_id": problem_id,
                          "operation_text": op["text"]})
            key.append({"item_id": item_id, "op_id": op["op_id"], "is_decoy": is_decoy})
    n_targets = sum(len(t) for t in groups.values())
    write_csv(Path(out_dir) / "corroboration_sheet.csv", sheet)
    write_csv(Path(out_dir) / "corroboration_key.csv", key)
    return {"targets": n_targets, "decoys": len(key) - n_targets, "short": short}
