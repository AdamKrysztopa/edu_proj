"""I1b tables: control2 under gpt-5.6-luna, and back-to-back against I1's qwen arm when given.

    python3 research/n3_control_luna/compare.py [--qwen research/n3_control]
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
DOMAINS = ("plc", "gdpr_v1", "gdpr_v2")
LABELS = ("closed", "partial", "open")


def load(root: Path, d: str) -> dict | None:
    p = root / d / "control2.json"
    return json.loads(p.read_text()) if p.exists() else None


def fmt(row: dict) -> str:
    if not row.get("n"):
        return "n=0"
    ci = row["ci95"]
    ci_s = f"[{ci[0]:+.2f}, {ci[1]:+.2f}]" if ci else "n/a"
    return f"{row['own_rate']:.2f} vs {row['control_rate']:.2f}, {row['diff']:+.2f} {ci_s}"


def table(res: dict, name: str) -> list[str]:
    lines = [f"| {name} lens | pairs | discriminable | equal-cap, closed or partial | equal-cap, closed "
             "| seed-free, closed or partial | seed-free, closed (primary) | undecided arms |",
             "|---|---|---|---|---|---|---|---|"]
    groups = {**res["summary"]["by_lens"], "all": res["summary"]["total"]}
    for lens, g in groups.items():
        lines.append(f"| {lens} | {g['n_pairs']} | {g['n_discriminable']} ({g['share_discriminable']:.2f}) "
                     f"| {fmt(g['equal_cap']['closed_or_partial'])} | {fmt(g['equal_cap']['closed'])} "
                     f"| {fmt(g['seed_free']['closed_or_partial'])} | {fmt(g['seed_free']['closed'])} "
                     f"| {sum(g['undecided'].values())} |")
    return lines


def kappa(pairs: list[tuple[str, str]]) -> float | None:
    n = len(pairs)
    if not n:
        return None
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[x] * cb[x] for x in LABELS) / n ** 2
    return None if pe == 1 else (po - pe) / (1 - pe)


def agreement(luna: dict, qwen: dict) -> dict:
    q = {(p["lens"], tuple(p["seeds"])): p for p in qwen["pairs"]}
    by_lens: dict[str, list] = {}
    excluded = Counter()
    for p in luna["pairs"]:
        other = q.get((p["lens"], tuple(p["seeds"])))
        if other is None or not p["states"]:
            continue
        for arm, s in p["states"].items():
            t = other["states"][arm]
            if s not in LABELS or t not in LABELS:
                excluded[p["lens"]] += 1
                continue
            by_lens.setdefault(p["lens"], []).append((s, t))
    rows = {ln: {"n": len(v), "agree": sum(a == b for a, b in v) / len(v), "kappa": kappa(v),
                 "excluded_undecided": excluded[ln]} for ln, v in sorted(by_lens.items())}
    allv = [x for v in by_lens.values() for x in v]
    rows["all"] = {"n": len(allv), "agree": sum(a == b for a, b in allv) / len(allv) if allv else None,
                   "kappa": kappa(allv), "excluded_undecided": sum(excluded.values()),
                   "confusion_luna_by_qwen": {f"{a}/{b}": c for (a, b), c in sorted(Counter(allv).items())}}
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--qwen", type=Path)
    args = ap.parse_args()
    out = []
    for d in DOMAINS:
        res = load(HERE, d)
        if res is None:
            out.append(f"## {d}: missing")
            continue
        out.append(f"## {res['domain']} (admissible: {res['admissible']}; complete: {res.get('complete')})")
        out.append(f"spend: {json.dumps(res.get('spend'))}")
        out.append(f"length stand-in: {json.dumps(res['length_stand_in'])}")
        out += table(res, "luna")
        if args.qwen and (qr := load(args.qwen, d)) is not None:
            out += table(qr, "qwen")
            out.append("agreement: " + json.dumps(agreement(res, qr)))
        out.append("")
    print("\n".join(out))


if __name__ == "__main__":
    main()
