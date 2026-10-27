"""Item 3 (c): gemma's second G1 run (`research/n3_control_v3/l73.py` through D1b's `g1.py`
wrapper, rule unchanged, cold cache), compared with its first (`research/d1b_rerun/g1/
google_gemma-4-31b-it-r3`). Gemma counts as an ADR 0009 arm only if both runs pass with identical
results (`docs/plans/prompts/_common.md:35`).

    uv run --directory gapmap python ../research/closure_topicality/g1_retest.py run --max-usd X \
        --spend-ledger ../research/closure_topicality/openrouter_spend.jsonl
    uv run --directory gapmap python ../research/closure_topicality/g1_retest.py compare
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
W = HERE.parents[1]
FIRST = W / "research" / "d1b_rerun" / "g1" / "google_gemma-4-31b-it-r3" / "l73" / "l73.json"
TAG = "google_gemma-4-31b-it-r4"
SECOND = HERE / "g1" / TAG / "l73" / "l73.json"
MODEL = "google/gemma-4-31b-it"


def _states(x, path=()):
    if isinstance(x, dict):
        for k, v in sorted(x.items()):
            yield from _states(v, (*path, k))
    elif isinstance(x, list):
        for n, v in enumerate(x):
            yield from _states(v, (*path, n))
    else:
        yield path, x


def compare(first: dict, second: dict) -> dict:
    """`identical` is the pre-stated test. `seed_free_identical` ignores the equal-cap arms, which
    l73's rule does not read; reported, it does not make gemma count."""
    flags = all(first[k] == second[k] for k in ("planted_fires", "stand_in_fires", "eligible"))
    a, b = dict(_states(first["topics"])), dict(_states(second["topics"]))
    differ = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
    sf_differ = [k for k in differ if not any(x in ("own_eq", "ctrl_eq") for x in k)]
    same = flags and not differ
    return {"first_eligible": first["eligible"], "second_eligible": second["eligible"], "identical": same,
            "differing_states": len(differ), "seed_free_identical": flags and not sf_differ,
            "counts": bool(first["eligible"] and second["eligible"] and same)}


def _g1():
    spec = importlib.util.spec_from_file_location("g1", W / "research" / "d1b_rerun" / "g1.py")
    g1 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g1)
    return g1


def main(argv: list[str]) -> int:
    if argv[:1] == ["compare"]:
        res = compare(json.loads(FIRST.read_text()), json.loads(SECOND.read_text()))
        (HERE / "g1" / "compare.json").write_text(json.dumps(res, indent=1, sort_keys=True) + "\n")
        print(res)
        return 0
    if argv[:1] != ["run"] or "--max-usd" not in argv or "--spend-ledger" not in argv:
        raise SystemExit("usage: g1_retest.py run --max-usd X --spend-ledger F | compare")
    g1 = _g1()
    l73 = g1.load_l73()
    l73.HERE = HERE / "g1"
    l73.judge_mod = g1._openrouter_shim(2000)
    sys.argv = ["l73", "--tag", TAG, "--model", MODEL, "--judge", "openai", *argv[1:]]
    l73.main()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
