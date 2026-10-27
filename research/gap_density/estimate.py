"""Gap-density survey, step a: the $0 cost estimate (plan `docs/plans/gap-density-survey.md` §2).

    python3 research/gap_density/estimate.py inventory OWNER/REPO ...   # gh api, public metadata only
    python3 research/gap_density/estimate.py report                      # no network

`inventory` records each candidate's file tree (paths and sizes), human contributors and their
commit shares. `report` applies D1's corpus shape (up to 16 user-facing docs from the project plus
10 outside pages, each cut at reconstruct's --max-doc-chars) and prices it with unit costs read from
D1's and D1b's own spend records, scaled by truncated characters.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent
D1 = RESEARCH / "d1_demonstrator"
D1B = RESEARCH / "d1b_rerun"
INVENTORY = HERE / "inventory.json"

MAX_DOC_CHARS = 12_000
OWNER_DOCS_MAX = 16
OUTSIDE_PAGES = 10
# D1b's two gemma gap maps (judge.json spend: 277 + 182 calls) are the last rows of its OpenRouter ledger.
GEMMA_MAP_CALLS = (277, 182)
CAP_USD = 4.00

_PROSE = re.compile(r"\.(md|rst)$|(^|/)llms\.txt$", re.I)
_SKIP_SEGMENTS = {"plan", "plans", "archive", "superpowers", ".github", ".claude", "tests", "test",
                  "fixtures", "_sources", "html", "obsolete"}
_SKIP_NAMES = re.compile(r"^(changelog|whats_new|history|contributing|code_of_conduct|security|license|"
                         r"todo|roadmap|planning_template|agents|claude|pull_request_template)\b", re.I)


def user_docs(tree: list[tuple[str, int]]) -> list[tuple[str, int]]:
    out = []
    for path, size in tree:
        parts = path.split("/")
        if not _PROSE.search(path) or _SKIP_NAMES.match(parts[-1]):
            continue
        if any(p.lower() in _SKIP_SEGMENTS for p in parts[:-1]):
            continue
        out.append((path, size))
    return out


def choose_owner_docs(tree: list[tuple[str, int]]) -> list[tuple[str, int]]:
    docs = sorted(user_docs(tree), key=lambda d: (-min(d[1], MAX_DOC_CHARS), d[0]))
    return docs[:OWNER_DOCS_MAX]


def truncated(docs: list[tuple[str, int]]) -> int:
    return sum(min(s, MAX_DOC_CHARS) for _, s in docs)


def _calls(run: str) -> list[dict]:
    (path,) = (D1 / "runs" / run).glob("*/calls.jsonl")
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _claims(run: str) -> int:
    (path,) = (D1 / "runs" / run).glob("*/ledger.json")
    return len(json.loads(path.read_text())["claims"])


def _cost(rows: list[dict], task: str | None = None) -> float:
    return sum(r.get("cost") or 0.0 for r in rows if task is None or r["task"] == task)


def _paid_mean(rows: list[dict], task: str) -> float:
    paid = [r.get("cost") or 0.0 for r in rows if r["task"] == task and r["outcome"] == "ok"]
    return sum(paid) / len(paid)


def unit_costs() -> dict:
    """A complete ledger: every attempted call priced at its task's mean paid cost. D1's top-tier run
    is marked complete but most cross-verifications and every decoy ended in api_error, unpaid."""
    top, cheap, cheap16 = _calls("toptier-26b"), _calls("cheap-26b"), _calls("cheap")
    top_tasks = {r["task"] for r in top}
    top_full = sum(sum(r["task"] == t for r in top) * _paid_mean(top, t) for t in top_tasks - {"decoy"})
    top_full += (sum(r["task"] == "decoy" for r in top) * _paid_mean(cheap16, "decoy")
                 * _paid_mean(top, "extract") / _paid_mean(cheap, "extract"))
    cheap_cross = [r for r in cheap if r["task"] == "cross_verify"]
    top_cross_calls = sum(r["task"] == "cross_verify" for r in top)
    cross_needed = top_cross_calls * _claims("cheap-26b") / _claims("toptier-26b")
    cheap_full = (_cost(cheap) - _cost(cheap_cross)
                  + _paid_mean(cheap, "cross_verify") * cross_needed + _cost(cheap16, "decoy"))
    orouter = [json.loads(line) for line in (D1B / "openrouter_spend.jsonl").read_text().splitlines()]
    maps = orouter[-sum(GEMMA_MAP_CALLS):]
    assert {r["model"] for r in maps} == {"google/gemma-4-31b-it"}
    sol = [json.loads(line) for line in (D1B / "openai_spend.jsonl").read_text().splitlines()]
    sol_per_call = sum(r["usd"] for r in sol) / len(sol)
    inv = json.loads((D1 / "corpus" / "inventory.json").read_text())["documents"]
    outside = [d for d in inv if d.get("outside")]
    return {
        "toptier_ledger_observed_usd": _cost(top),
        "toptier_ledger_usd": top_full,
        "cheap_ledger_observed_usd": _cost(cheap),
        "cheap_ledger_full_usd": cheap_full,
        "gemma_two_maps_usd": sum(r["usd"] for r in maps),
        "gemma_toptier_map_share": GEMMA_MAP_CALLS[1] / sum(GEMMA_MAP_CALLS),
        "sol_per_call_usd": sol_per_call,
        "sol_two_maps_usd": sol_per_call * sum(GEMMA_MAP_CALLS),
        "d1_docs": len(inv),
        "d1_truncated_chars": sum(min(d["source_bytes"], MAX_DOC_CHARS) for d in inv),
        "outside_mean_truncated_chars": sum(min(d["source_bytes"], MAX_DOC_CHARS) for d in outside) / len(outside),
    }


def codebase_usd(truncated_chars: float, u: dict, *, variant: str = "d1") -> float:
    scale = truncated_chars / u["d1_truncated_chars"]
    judges = u["gemma_two_maps_usd"] + u["sol_two_maps_usd"]
    if variant == "d1":
        return scale * (u["toptier_ledger_usd"] + u["cheap_ledger_full_usd"] + judges)
    if variant == "toptier-ledger-only":
        return scale * (u["toptier_ledger_usd"] + judges * u["gemma_toptier_map_share"])
    raise ValueError(variant)


def fit(costs: dict[str, float], *, cap: float) -> list[str]:
    chosen, spent = [], 0.0
    for name in sorted(costs, key=lambda n: (costs[n], n)):
        if spent + costs[name] > cap:
            break
        chosen.append(name)
        spent += costs[name]
    return chosen


def _gh(path: str, paginate: bool = False):
    cmd = ["gh", "api"] + (["--paginate"] if paginate else []) + [path]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    return json.loads(out.replace("]\n[", ",").replace("][", ","))


def cmd_inventory(repos: list[str]) -> int:
    inv = json.loads(INVENTORY.read_text()) if INVENTORY.exists() else {}
    for full in repos:
        meta = _gh(f"repos/{full}")
        sha = _gh(f"repos/{full}/commits/{meta['default_branch']}")["sha"]
        tree = _gh(f"repos/{full}/git/trees/{sha}?recursive=1")["tree"]
        people = [c for c in _gh(f"repos/{full}/contributors?per_page=100&anon=1", paginate=True)
                  if not (c.get("login") or "").endswith("[bot]") and c.get("type") != "Bot"]
        total = sum(c["contributions"] for c in people)
        top = max(people, key=lambda c: c["contributions"])
        inv[full] = {"commit": sha, "license": (meta.get("license") or {}).get("spdx_id"),
                     "fork": meta["fork"], "parent": (meta.get("parent") or {}).get("full_name"),
                     "homepage": meta.get("homepage") or None, "stars": meta["stargazers_count"],
                     "size_kb": meta["size"], "created": meta["created_at"][:10],
                     "top_author": top.get("login") or top.get("name"),
                     "humans": len(people), "commits": total,
                     "top_shares": [round(c["contributions"] / total, 3)
                                    for c in sorted(people, key=lambda c: -c["contributions"])[:3]],
                     "tree": sorted([t["path"], t.get("size", 0)] for t in tree
                                    if t["type"] == "blob" and _PROSE.search(t["path"]))}
    INVENTORY.write_text(json.dumps(inv, indent=1, sort_keys=True) + "\n")
    return 0


def cmd_report() -> int:
    u = unit_costs()
    inv = json.loads(INVENTORY.read_text())
    outside = OUTSIDE_PAGES * u["outside_mean_truncated_chars"]
    rows = {}
    for full, rec in inv.items():
        tree = [tuple(t) for t in rec["tree"]]
        docs = user_docs(tree)
        owner = choose_owner_docs(tree)
        chars = truncated(owner) + outside
        rows[full] = {"humans": rec["humans"], "top_share": rec["top_shares"][0], "fork": rec["fork"],
                      "user_docs": len(docs), "user_doc_bytes": sum(s for _, s in docs),
                      "corpus_docs": len(owner) + OUTSIDE_PAGES, "truncated_chars": round(chars),
                      "usd_d1": round(codebase_usd(chars, u, variant="d1"), 2),
                      "usd_toptier_only": round(codebase_usd(chars, u, variant="toptier-ledger-only"), 2)}
    print(json.dumps({"unit_costs": {k: round(v, 4) for k, v in u.items()}, "codebases": rows,
                      "fit_d1": fit({k: v["usd_d1"] for k, v in rows.items()}, cap=CAP_USD),
                      "fit_toptier_only": fit({k: v["usd_toptier_only"] for k, v in rows.items()}, cap=CAP_USD)},
                     indent=1))
    return 0


def main(argv: list[str]) -> int:
    if argv[:1] == ["inventory"]:
        return cmd_inventory(argv[1:])
    if argv[:1] == ["report"]:
        return cmd_report()
    raise SystemExit(__doc__)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
