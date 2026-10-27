"""Item 3 (b): sol's I1c GDPR v1 reading recounted on the owner's labels (plan §3 (b)). $0.

A closure counts only if at least one sentence the judge cited is one the owner labels as stating
the element. Fixed before any label exists: the overlap stand-in's recount must have a 95% CI
lower bound <= 0, and a planted fake closing an arm iff it holds a pack sentence labelled as
stating the element must have one above 0; otherwise "no reading". Then (b) holds iff sol's
recounted lower bound is above 0. Runs only once `fixtures/owner_labels.json` exists.

    uv run --directory gapmap python ../research/closure_topicality/reread.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from gapmap import control2

import pack

HERE = Path(__file__).resolve().parent


def _lb_positive(row: dict) -> bool:
    ci = row.get("ci95")
    return ci is not None and ci[0] > 0


def recount(pairs: list[dict], labels: dict) -> dict:
    def ok(arm: dict) -> bool:
        return arm["closed"] and any(labels.get(c) for c in arm["cited"])

    def precision(side: str) -> float | None:
        cited = [c for p in pairs if p[side]["closed"] for c in p[side]["cited"] if c in labels]
        return sum(labels[c] for c in cited) / len(cited) if cited else None

    diffs = [(p["cluster"], float(ok(p["own"])) - float(ok(p["ctrl"]))) for p in pairs]
    n = len(pairs)
    return {"n": n, "own_rate": sum(ok(p["own"]) for p in pairs) / n,
            "control_rate": sum(ok(p["ctrl"]) for p in pairs) / n,
            "diff": sum(d for _c, d in diffs) / n,
            "ci95": control2._cluster_ci(diffs, control2.BOOTSTRAP_B, control2.BOOTSTRAP_SEED),
            "precision_own": precision("own"), "precision_ctrl": precision("ctrl")}


def planted(arms: list[dict], labels: dict) -> list[dict]:
    def arm(ids: list) -> dict:
        hit = [i for i in ids if labels.get(i)]
        return {"closed": bool(hit), "cited": hit}

    return [{"cluster": a["cluster"], "own": arm(a["own"]), "ctrl": arm(a["ctrl"])} for a in arms]


def reading(*, sol: dict, standin: dict, planted: dict) -> str:
    if _lb_positive(standin) or not _lb_positive(planted):
        return "no reading"
    return "holds" if _lb_positive(sol) else "does not hold"


def main() -> int:
    labels_path = HERE / "fixtures" / "owner_labels.json"
    if not labels_path.exists():
        print("no owner labels yet: fixtures/owner_labels.json is written from the owner's reply to owner_pack.md")
        return 1
    labels = json.loads(labels_path.read_text())["items"]
    rows = pack.i1c_arms()
    ids = lambda row, sents: [pack.item_id(row, s) for s in sents]
    judged = {"sol": [], "overlap": []}
    arms = []
    for row in rows:
        for who, state_key, cited_key in (("sol", "sol_state", "sol_cited"), ("overlap", "overlap_closed", "overlap_cited")):
            judged[who].append({"cluster": row["cluster"], **{
                side: {"closed": (row[side][state_key] == "closed") if who == "sol" else row[side][state_key],
                       "cited": ids(row, row[side][cited_key])} for side in ("own", "ctrl")}})
        arms.append({"cluster": row["cluster"],
                     **{side: [i for i in ids(row, row[side]["sentences"]) if i in labels] for side in ("own", "ctrl")}})
    out = {"sol": recount(judged["sol"], labels), "overlap_standin": recount(judged["overlap"], labels),
           "planted": recount(planted(arms, labels), labels)}
    out["reading"] = reading(sol=out["sol"], standin=out["overlap_standin"], planted=out["planted"])
    (HERE / "reread.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: (v if k == "reading" else {x: v[x] for x in ("diff", "ci95")}) for k, v in out.items()}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
