"""D1b's Stop A count, per codebase (plan `docs/plans/gap-density-survey.md` §3), reusing D1b's own
topic clustering, arm rule and matching (`research/d1b_rerun/build_sheet.py`) unchanged.

    uv run --directory gapmap python ../research/gap_density/stop_a.py reference --arm gemma=DIR

`reference` replays D1b's cached gemma closure states on dependence-forecastability (no model call)
over every fired, non-debris candidate of both D1 ledgers, without D1b's D1-overlap filter and owner
review, which a codebase with no earlier sheet does not have. It splits the count by ledger and by
source origin.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "d1b_rerun"))
import build_sheet  # noqa: E402
import common  # noqa: E402

OUT = Path(__file__).resolve().parent / "reference_d1.json"


def counts(topics: list[dict], states: dict, judges: tuple[str, ...]) -> dict:
    arms = [build_sheet.arm_of(t, states, judges) for t in topics]
    gaps = [t for t, a in zip(topics, arms) if a == "gap"]
    covs = [t for t, a in zip(topics, arms) if a == "covered"]
    pairs = build_sheet.match(gaps, covs, n=len(topics), seed=build_sheet.SEED)
    try:
        build_sheet.choose_size(gaps, covs, seed=build_sheet.SEED)
        floor = True
    except build_sheet.TooFew:
        floor = False
    return {"topics": len(topics), "all_open": len(gaps), "all_closed": len(covs),
            "mixed": len(topics) - len(gaps) - len(covs),
            "open_share": round(len(gaps) / len(topics), 3) if topics else 0.0,
            "matched_pairs_upper_bound": len(pairs), "reaches_floor": floor}


def by_origin(topics: list[dict], states: dict, judges: tuple[str, ...]) -> dict:
    return {o: counts([t for t in topics if t["source_origin"] == o], states, judges)
            for o in sorted({t["source_origin"] for t in topics})}


def marginals(states: dict, judge: str) -> dict:
    seen = [s[judge] for s in states.values() if judge in s]
    return {k: round(seen.count(k) / len(seen), 4) for k in ("open", "closed")}


def noise_floor_rate(topics: list[dict], *, p_open: float, p_closed: float, seeds: int = 300,
                     per_topic: bool = False) -> float:
    """Share of seeds on which a judge drawing states at random, at the given marginals, reaches the
    floor: the L7.3 trivial stand-in for the eligibility rule. Draws once per version, or once per
    topic for all its versions."""
    hits = 0
    for seed in range(seeds):
        rng = random.Random(seed)
        states = {}
        for t in topics:
            groups = [t["versions"]] if per_topic else [[v] for v in t["versions"]]
            for group in groups:
                x = rng.random()
                s = "open" if x < p_open else "closed" if x < p_open + p_closed else "partial"
                for v in group:
                    states[tuple(v)] = {"noise": s}
        hits += counts(topics, states, ("noise",))["reaches_floor"]
    return hits / seeds


def _rows(ledgers) -> list[dict]:
    from gapmap import lenses, link, semantic

    retriever = build_sheet._retriever()
    rows = []
    for name in ledgers:
        lg, index, _ = common.load(name)
        for c in lenses.run_all(lg, index, link.SETTING_1):
            if not c.question_text or c.excluded or common.debris(common.quote(c.question_text)):
                continue
            src = lg.by_id[min(semantic.primary_probe(lg, c)[1])].evidence[0].source.identifier
            question = build_sheet._clean(c.question_text)
            rows.append({"ledger": name, "test_id": c.test_id, "lens": c.lens,
                         "quote": common.quote(c.question_text), "anchor": c.anchor,
                         "k_topic": len(link.breadth(lg, c.x_a)),
                         "source_origin": "owner" if build_sheet.OWNER_REPO in src else "outside",
                         "words": len(question.split()), "similarity": retriever.similarity(question),
                         "question_text": question})
    return rows


def cmd_reference(args) -> int:
    arm_dirs = dict((k, Path(v)) for k, v in (a.split("=", 1) for a in args.arm))
    judges = tuple(sorted(arm_dirs))
    out = {"codebase": "AdamKrysztopa/dependence-forecastability", "judges": list(judges),
           "filters": "debris only (no D1-overlap filter, no owner review)"}
    for label, ledgers in (("both_ledgers", tuple(common.LEDGER_DIRS)),
                           *((f"only_{n}", (n,)) for n in common.LEDGER_DIRS)):
        rows = _rows(ledgers)
        topics = build_sheet.cluster(rows)
        for t in topics:
            t["versions"] = [tuple(v) for v in t["versions"]]
        states = build_sheet._states(arm_dirs, {(r["ledger"], r["test_id"]): r for r in rows})
        m = marginals(states, judges[0])
        out[label] = {"versions": len(rows), **counts(topics, states, judges),
                      "by_origin": by_origin(topics, states, judges),
                      "version_marginals": m, "versions_per_topic": round(len(rows) / len(topics), 3),
                      "noise_floor_rate": noise_floor_rate(topics, p_open=m["open"], p_closed=m["closed"]),
                      "noise_floor_rate_coin": noise_floor_rate(topics, p_open=0.5, p_closed=0.5),
                      "noise_floor_rate_per_topic": noise_floor_rate(
                          topics, p_open=m["open"], p_closed=m["closed"], per_topic=True),
                      "noise_floor_rate_two_independent_judges": noise_floor_rate(
                          topics, p_open=m["open"] ** 2, p_closed=m["closed"] ** 2)}
    OUT.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="stop_a")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("reference")
    s.add_argument("--arm", action="append", required=True, metavar="NAME=DIR")
    args = p.parse_args(argv)
    return {"reference": cmd_reference}[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
