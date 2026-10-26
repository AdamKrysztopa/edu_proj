"""D1b decision rule (plan §3.4, criterion (b), owner 2026-10-26), fixed before the owner answers.

Each answer carries its arm ("gap" or "covered") and two judges' labels (j1 = judge A, Claude;
j2 = judge B, Codex): "new", "partly", "already written" or "no content". Continue iff, on the
answers both judges label alike, the gap "new" rate minus the covered rate is >= 0.30 with a
one-sided exact permutation p <= 0.10, AND the same holds on judge A's labels alone; otherwise
Change. No reading (counted as Change, plan §3.7) if fewer than 8/15 of the answers carry content
by both judges. The permutation moves the arm labels over all answers; p is computed exactly by
counting, not sampled."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

MIN_DIFF = 0.30
MAX_P = 0.10


def content_floor(n: int) -> int:
    return math.ceil(n * 8 / 15)


def _labels(rows: list[dict], mode: str) -> list[str | None]:
    if mode == "judge_a":
        return [r["j1"] for r in rows]
    return [r["j1"] if r["j1"] == r["j2"] else None for r in rows]


def _rate(new: int, n: int) -> float:
    return new / n if n else 0.0


def difference(rows: list[dict], arms: list[str], mode: str) -> float:
    labs = _labels(rows, mode)
    gap = [lab for arm, lab in zip(arms, labs) if arm == "gap" and lab is not None]
    cov = [lab for arm, lab in zip(arms, labs) if arm == "covered" and lab is not None]
    return _rate(gap.count("new"), len(gap)) - _rate(cov.count("new"), len(cov))


def permutation_p(rows: list[dict], mode: str) -> float:
    """P(difference >= observed) over every placement of the gap labels among the answers: count
    placements by how many counted answers (a) and counted "new" answers (k) land in the gap arm."""
    labs = _labels(rows, mode)
    n, n_gap = len(rows), sum(r["arm"] == "gap" for r in rows)
    m = sum(lab is not None for lab in labs)
    big_k = sum(lab == "new" for lab in labs)
    obs = difference(rows, [r["arm"] for r in rows], mode)
    hits = 0
    for a in range(max(0, n_gap - (n - m)), min(n_gap, m) + 1):
        rest = math.comb(n - m, n_gap - a)
        for k in range(max(0, a - (m - big_k)), min(a, big_k) + 1):
            if _rate(k, a) - _rate(big_k - k, m - a) >= obs - 1e-12:
                hits += math.comb(big_k, k) * math.comb(m - big_k, a - k) * rest
    return hits / math.comb(n, n_gap)


def _reading(rows: list[dict], mode: str) -> dict:
    labs = _labels(rows, mode)
    arms = [r["arm"] for r in rows]
    gap = [lab for arm, lab in zip(arms, labs) if arm == "gap" and lab is not None]
    cov = [lab for arm, lab in zip(arms, labs) if arm == "covered" and lab is not None]
    diff = difference(rows, arms, mode)
    p = permutation_p(rows, mode)
    return {"gap_new_rate": _rate(gap.count("new"), len(gap)), "covered_new_rate": _rate(cov.count("new"), len(cov)),
            "gap_counted": len(gap), "covered_counted": len(cov), "difference": diff, "p": p,
            "meets": diff >= MIN_DIFF - 1e-12 and p <= MAX_P}


def decide(rows: list[dict]) -> dict:
    with_content = sum("no content" not in (r["j1"], r["j2"]) for r in rows)
    agreed, judge_a = _reading(rows, "agreed"), _reading(rows, "judge_a")
    if with_content < content_floor(len(rows)):
        decision = "No reading"
    else:
        decision = "Continue" if agreed["meets"] and judge_a["meets"] else "Change"
    return {"n": len(rows), "n_with_content": with_content, "content_floor": content_floor(len(rows)),
            "agreed": agreed, "judge_a": judge_a, "decision": decision}


def _sheet(gap: list[str], cov: list[str]) -> list[dict]:
    return [{"arm": "gap", "j1": g, "j2": g} for g in gap] + [{"arm": "covered", "j1": c, "j2": c} for c in cov]


def l73_checks() -> dict:
    """A planted positive must fire; null, copied, filler, borderline, judge-disagreement and
    judge-A-dissent sheets must not; stances alone give No reading; at 15, 12 and 10 per arm.
    Filler is length-matched text with no content, which the judges should label "no content"
    (canary)."""
    out: dict = {}
    for n in (15, 12, 10):
        lo, hi = round(n * 7 / 15), round(n * 4 / 15)
        disagree = _sheet(["new"] * n, ["already written"] * n)
        for r in disagree[:n]:
            r["j2"] = "partly"
        a_dissent = _sheet(["new"] * n, ["already written"] * n)
        for r in a_dissent[:n]:
            r["j1"] = "partly"
        cases = {
            "planted_positive": (_sheet(["new"] * n, ["already written"] * n), "Continue"),
            "all_novel": (_sheet(["new"] * n, ["new"] * n), "Change"),
            "all_copied": (_sheet(["already written"] * n, ["already written"] * n), "Change"),
            "filler": (_sheet(["no content"] * n, ["no content"] * n), "No reading"),
            "borderline_7_vs_4_of_15": (_sheet(["new"] * lo + ["partly"] * (n - lo),
                                               ["new"] * hi + ["partly"] * (n - hi)), "Change"),
            "judges_disagree_on_gap": (disagree, "Change"),
            "judge_a_dissents_on_gap": (a_dissent, "Change"),
        }
        for name, (rows, want) in cases.items():
            out[f"{n}:{name}"] = {**decide(rows), "expected": want}
        out[f"{n}:best_case_difference"] = 1.0
        out[f"{n}:best_case_p"] = 1 / math.comb(2 * n, n)
    out["all_pass"] = all(v["decision"] == v["expected"] for v in out.values() if isinstance(v, dict))
    return out


if __name__ == "__main__":
    result = l73_checks()
    Path(__file__).with_name("rule_checks.json").write_text(json.dumps(result, indent=1, sort_keys=True) + "\n")
    print("all_pass", result["all_pass"], "best p at 15:", result["15:best_case_p"])
    sys.exit(0 if result["all_pass"] else 1)
