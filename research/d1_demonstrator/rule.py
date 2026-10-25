"""D1 decision rule (prompt step 7), fixed before the owner answers, and its L7.3 checks.

Each answer carries its arm ("gap" or "covered") and two judges' labels ("new", "partly",
"already written"). Only answers where both judges agree count."""
from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

MIN_DIFF = 0.30
MIN_GAP_NEW = 5
MIN_WITH_CONTENT = 8


def _rates(rows: list[dict], arms: list[str]) -> tuple[float, float, int]:
    agreed = [(arm, r["j1"]) for arm, r in zip(arms, rows) if r["j1"] == r["j2"]]
    gap = [lab for arm, lab in agreed if arm == "gap"]
    cov = [lab for arm, lab in agreed if arm == "covered"]
    rate = lambda labs: sum(lab == "new" for lab in labs) / len(labs) if labs else 0.0
    return rate(gap), rate(cov), sum(lab == "new" for lab in gap)


def decide(rows: list[dict]) -> dict:
    arms = [r["arm"] for r in rows]
    gap_rate, cov_rate, gap_new = _rates(rows, arms)
    diff = gap_rate - cov_rate
    n_gap = arms.count("gap")
    # exact permutation p over every way to place the gap labels among the answers
    hits = total = 0
    for idx in itertools.combinations(range(len(rows)), n_gap):
        perm = ["gap" if i in idx else "covered" for i in range(len(rows))]
        g, c, _ = _rates(rows, perm)
        hits += (g - c) >= diff - 1e-12
        total += 1
    with_content = sum("no content" not in (r["j1"], r["j2"]) for r in rows)
    if with_content < MIN_WITH_CONTENT:
        decision = "No reading"
    else:
        decision = "Continue" if diff >= MIN_DIFF and gap_new >= MIN_GAP_NEW else "Change"
    return {"gap_new_rate": gap_rate, "covered_new_rate": cov_rate, "difference": diff,
            "gap_answers_new": gap_new, "n_agreed": sum(r["j1"] == r["j2"] for r in rows),
            "permutation_p": hits / total, "n_with_content": with_content, "decision": decision}


def _sheet(gap: str, cov: str, n_gap: int = 10, n_cov: int = 5) -> list[dict]:
    return ([{"arm": "gap", "j1": gap, "j2": gap}] * n_gap
            + [{"arm": "covered", "j1": cov, "j2": cov}] * n_cov)


def l73_checks() -> dict:
    """Planted positive must fire; all-novel, all-copied and filler stand-ins must not. Filler is
    length-matched text with no content, which the judges should label "already written"; a judge
    canary in step 6 checks that they do."""
    cases = {
        "planted_positive": (_sheet("new", "already written"), "Continue"),
        "all_novel": (_sheet("new", "new"), "Change"),
        "all_copied": (_sheet("already written", "already written"), "Change"),
        "filler": (_sheet("already written", "already written"), "Change"),
        "borderline_4_of_10_new": (
            [{"arm": "gap", "j1": "new", "j2": "new"}] * 4
            + [{"arm": "gap", "j1": "partly", "j2": "partly"}] * 6
            + [{"arm": "covered", "j1": "already written", "j2": "already written"}] * 5, "Change"),
        "stances_only": (_sheet("no content", "no content"), "No reading"),
        "judges_disagree_on_gap": (
            [{"arm": "gap", "j1": "new", "j2": "partly"}] * 10
            + [{"arm": "covered", "j1": "already written", "j2": "already written"}] * 5, "Change"),
    }
    out = {name: {**decide(rows), "expected": want} for name, (rows, want) in cases.items()}
    out["best_case_difference"] = 1.0
    out["all_pass"] = all(v["decision"] == v["expected"] for k, v in out.items()
                          if isinstance(v, dict))
    return out


if __name__ == "__main__":
    result = l73_checks()
    Path(__file__).with_name("rule_checks.json").write_text(json.dumps(result, indent=1) + "\n")
    print("all_pass", result["all_pass"], "planted p", round(result["planted_positive"]["permutation_p"], 5))
    sys.exit(0 if result["all_pass"] else 1)
