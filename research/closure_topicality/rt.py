"""RT: the topicality-controlled closure check on real retrievals (plan
docs/plans/closure-topicality-check.md §1).

Per topic, four arms share the lens question, the seed (header only) and a real background, the
first min(k, 7) sentences of the candidate's seed-free control2 arm: 0 (background only), P (+ a
sentence stating the element), N (+ an on-topic non-element), R (+ random letters with P's word
lengths), the insert at one seeded position. `hit(X)`: the arm is closed and the insert is cited.

Part I, per judge, split and run: hit(P) - hit(N) >= 0.50, cluster-bootstrap lower bound (5th
percentile of 2,000 resamples) >= 0.30, hit(N) <= 0.25, hit(R) <= 0.10; any undecided arm makes the
run incomplete. Part II (§1.2) needs the owner's labels of cited background sentences. A split is
run only after `stand_in_report` finds no stand-in passing part I, at the median or any threshold.

    uv run --directory gapmap python ../research/closure_topicality/rt.py --split d1|gdpr --stand-ins
    uv run --directory gapmap python ../research/closure_topicality/rt.py --split d1 --out DIR \
        --judge openrouter --model google/gemma-4-31b-it --reasoning-max-tokens 2000 --max-usd X \
        --spend-ledger ../research/closure_topicality/openrouter_spend.jsonl
    ... --judge openai --model gpt-6.1-sol --reasoning-effort high --max-usd X \
        --spend-ledger ../research/closure_topicality/openai_spend.jsonl
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import string
import sys
from pathlib import Path

from gapmap import config, judge as judge_mod, semantic, standins, text

import standins_t as st

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures"
INSERT = "insert"
ARMS = ("0", "P", "N", "R")
BACKGROUND_MAX = config.JUDGE_A_CAP - 1
BOOTSTRAP_B = 2000
BOOTSTRAP_SEED = 20261027
LENGTH_SLACK = 0.10
DIFF_MIN, LOWER_MIN, N_MAX, R_MAX = 0.50, 0.30, 0.25, 0.10
PART2_MAX, PART2_MIN_CITED = 0.25, 5
COIN_SEEDS = (0, 1, 2)


class Unconfirmed(RuntimeError):
    pass


def letters(p: str) -> str:
    rng = random.Random(hashlib.sha256(p.encode()).hexdigest())
    return " ".join("".join(rng.choice(string.ascii_lowercase) for _ in w) for w in p.split())


def background(topic: dict) -> list[tuple]:
    return [tuple(r) for r in topic["background_rows"][:BACKGROUND_MAX]]


def position(topic: dict) -> int:
    rng = random.Random(hashlib.sha256(topic["topic_id"].encode()).hexdigest())
    return rng.randrange(len(background(topic)) + 1)


def arm_rows(topic: dict, ins: dict) -> dict[str, list[tuple]]:
    bg, pos = background(topic), position(topic)

    def with_insert(sentence: str) -> list[tuple]:
        return bg[:pos] + [(INSERT, 0, sentence)] + bg[pos:]

    return {"0": bg, "P": with_insert(ins["P"]), "N": with_insert(ins["N"]), "R": with_insert(letters(ins["P"]))}


def _prompt(topic: dict, rows: list[tuple]) -> str:
    return semantic.build_prompt(topic["seed_text"], topic["question"], semantic.build_retrieval(rows))


def prompts(topics: list[dict], inserts: dict) -> list[str]:
    return [_prompt(t, rows) for t in topics for rows in arm_rows(t, inserts[t["topic_id"]]).values()]


def _judge(judge, topic: dict, rows: list[tuple]) -> dict:
    retrieval = semantic.build_retrieval(rows)
    out = semantic.judge_retrieval(judge, retrieval, topic["seed_text"], topic["question"])
    cited, partial, insert_partial = [], [], False
    if out.state != "undecided":
        # a_hits are claim ids, and background rows can share one; the reply's own numbers say which row
        raw = judge.ask(semantic.build_prompt(topic["seed_text"], topic["question"], retrieval))
        ids = lambda key: {str(x) for x in raw.get(key, [])}
        states, partially = ids("states"), ids("partially") - ids("states")
        for (cid, i, _s), (id_, _c, _x) in zip(rows, retrieval.a_items):
            if cid == INSERT:
                insert_partial = id_ in partially
            elif id_ in states and out.state == "closed":
                cited.append([cid, i])
            elif id_ in partially:
                partial.append([cid, i])
    return {"state": out.state, "insert_cited": out.state == "closed" and INSERT in out.a_hits,
            "insert_partial": insert_partial, "background_cited": cited, "background_partial": partial}


def lower90(per_topic: list[tuple[str, int]]) -> float:
    clusters: dict[str, list[int]] = {}
    for cl, d in per_topic:
        clusters.setdefault(cl, []).append(d)
    keys = sorted(clusters)
    rng = random.Random(BOOTSTRAP_SEED)
    means = []
    for _ in range(BOOTSTRAP_B):
        drawn = [d for k in (rng.choice(keys) for _ in keys) for d in clusters[k]]
        means.append(sum(drawn) / len(drawn))
    means.sort()
    return means[int(0.05 * BOOTSTRAP_B)]


def part_one(topics: list[dict], hits: dict[str, dict[str, bool]]) -> dict:
    n = len(topics)
    rate = {a: sum(hits[t["topic_id"]][a] for t in topics) / n for a in ARMS}
    per = [(t["cluster"], int(hits[t["topic_id"]]["P"]) - int(hits[t["topic_id"]]["N"])) for t in topics]
    diff = rate["P"] - rate["N"]
    low = lower90(per)
    return {"hit": rate, "diff": diff, "lower90": low,
            "passes": diff >= DIFF_MIN and low >= LOWER_MIN and rate["N"] <= N_MAX and rate["R"] <= R_MAX}


def evaluate(topics: list[dict], inserts: dict, judge) -> dict:
    per = {t["topic_id"]: {a: _judge(judge, t, rows) for a, rows in arm_rows(t, inserts[t["topic_id"]]).items()}
           for t in topics}
    undecided = sum(r["state"] == "undecided" for arms in per.values() for r in arms.values())
    hits = {tid: {a: r["insert_cited"] for a, r in arms.items()} for tid, arms in per.items()}
    closed = {tid: {a: r["state"] == "closed" for a, r in arms.items()} for tid, arms in per.items()}
    p1 = part_one(topics, hits)
    complete = undecided == 0
    if not complete:
        p1["passes"] = False
    cited_bg = {tid: sorted({tuple(k) for r in arms.values() for k in r["background_cited"]})
                for tid, arms in per.items()}
    partial_bg = {tid: sorted({tuple(k) for r in arms.values() for k in r["background_partial"]})
                  for tid, arms in per.items()}
    n = len(topics)
    return {"judge_model": judge.model_id, "n_topics": n, "n_clusters": len({t["cluster"] for t in topics}),
            "undecided": undecided, "complete": complete,
            "verdict": "incomplete" if not complete else "part1-pass" if p1["passes"] else "part1-fail",
            "part1": p1,
            "arm_closed": {a: sum(closed[t["topic_id"]][a] for t in topics) / n for a in ARMS},
            "cited_background": {tid: [list(k) for k in ks] for tid, ks in cited_bg.items()},
            "partial_background": {tid: [list(k) for k in ks] for tid, ks in partial_bg.items()},
            "insert_partial": {tid: {a: r["insert_partial"] for a, r in arms.items()} for tid, arms in per.items()},
            "states": {tid: {a: r["state"] for a, r in arms.items()} for tid, arms in per.items()},
            "hits": hits}


def part_two(cited_keys: list, labels: dict) -> dict:
    """`labels`: key -> True if the owner says the sentence states the element."""
    cited = [k for k in cited_keys if k in labels]
    non = sum(not labels[k] for k in cited)
    share = non / len(cited) if cited else 0.0
    trivial = len(cited) < PART2_MIN_CITED
    return {"cited": len(cited), "non_element": non, "share": share,
            "passes": trivial or share <= PART2_MAX, "trivial": trivial}


def _ov(topic: dict, s: str) -> int:
    return len(text.cw(topic["seed_text"] + " " + topic["question"]) & text.cw(s))


def _novel(topic: dict, s: str) -> int:
    return len(text.cw(s) - text.cw(topic["seed_text"] + " " + topic["question"]))


def insert_problem(topic: dict, ins: dict, *, strict: bool) -> str | None:
    """D1's owner-confirmed inserts meet G2's two checks (`strict=False`); new GDPR inserts meet all
    of plan §1.4."""
    p, n = ins["P"], ins["N"]
    if not len(p) <= len(n) <= len(p) * (1 + LENGTH_SLACK):
        return f"length: N is {len(n)} chars against P's {len(p)}; it must be {len(p)}-{int(len(p) * (1 + LENGTH_SLACK))}"
    if _ov(topic, n) < _ov(topic, p) or (strict and _ov(topic, n) > _ov(topic, p) + 1):
        return f"overlap: N shares {_ov(topic, n)} seed-and-question words, P {_ov(topic, p)}; N must be P or P + 1"
    if not strict:
        return None
    probe = frozenset(topic["probe"])
    if len(probe & text.cw(n)) < len(probe & text.cw(p)):
        return "probe: N shares fewer probe words than P"
    if abs(_novel(topic, n) - _novel(topic, p)) > 1:
        return f"novelty: N has {_novel(topic, n)} new content words, P {_novel(topic, p)}; they may differ by 1"
    if len(standins._SPECIFIC.findall(n)) < len(standins._SPECIFIC.findall(p)):
        return "specificity: N has fewer digits, conditionals or named settings than P"
    return None


def lexicon_problem(topics: list[dict], inserts: dict) -> str | None:
    """Per split, P and N may differ by at most 1 in hits of the closing lexicons and of every other
    lexicon (the lens-cue words among them)."""
    groups = {"closing": standins.CLOSING_LEXICONS, **{n: (n,) for n in config.PATTERNS}}
    for name, names in groups.items():
        hit = lambda s: any(config.PATTERNS[x].search(s) for x in names)
        p = sum(hit(inserts[t["topic_id"]]["P"]) for t in topics)
        n = sum(hit(inserts[t["topic_id"]]["N"]) for t in topics)
        if abs(p - n) > 1:
            return f"lexicon {name}: {p} Ps against {n} Ns"
    return None


def require_confirmed(topics: list[dict], inserts: dict, owner: dict) -> None:
    missing = [t["topic_id"] for t in topics
               if not all(owner.get(t["topic_id"], {}).get(k) is True for k in ("P", "N"))]
    if missing:
        raise Unconfirmed(f"the owner has not confirmed {len(missing)} topic(s): {', '.join(missing)}")


def _standin_judges(topics: list[dict], inserts: dict) -> list:
    ps = prompts(topics, inserts)
    out = []
    for name, stat in st.all_stats(ps).items():
        out += [st.calibrate(name, stat, mode, ps) for mode in st.MODES]
        out += [st.CiteJudge(name, stat, mode, cut=c) for c in st.sweep_cuts(stat, ps) for mode in ("ge", "le")]
    out += [st.CoinCiteJudge(s) for s in COIN_SEEDS]
    return out


def stand_in_report(topics: list[dict], inserts: dict, extra: list = ()) -> dict:
    """Part I for every citing stand-in (median, argmax, argmin and every threshold), and arm
    closure P - N for the arm-level ones under the same thresholds."""
    rows, passing = [], []
    for j in [*_standin_judges(topics, inserts), *extra]:
        r = evaluate(topics, inserts, j)
        rows.append({"judge": j.model_id, **{k: r["part1"][k] for k in ("hit", "diff", "lower90", "passes")}})
        if r["part1"]["passes"]:
            passing.append(j.model_id)
    arm_rows_ = []
    for j in st.arm_level(prompts(topics, inserts)):
        r = evaluate(topics, inserts, j)
        closed = {t["topic_id"]: {a: r["states"][t["topic_id"]][a] == "closed" for a in ARMS} for t in topics}
        p1 = part_one(topics, closed)
        arm_rows_.append({"judge": j.model_id, **{k: p1[k] for k in ("hit", "diff", "lower90", "passes")}})
        if p1["passes"]:
            passing.append(j.model_id)
    best = max(rows, key=lambda r: (r["diff"], r["lower90"])) if rows else None
    return {"usable": not passing, "passing": passing, "best_citing": best, "citing": rows, "arm_level": arm_rows_}


def load(split: str) -> tuple[list[dict], dict, dict]:
    topics = json.loads((FIXTURES / f"topics_{split}.json").read_text())["topics"]
    inserts = json.loads((FIXTURES / f"inserts_{split}.json").read_text())["inserts"]
    owner_path, key_path = FIXTURES / "owner_labels.json", FIXTURES / "owner_pack_key.json"
    owner = {}
    if owner_path.exists() and key_path.exists():
        import pack
        owner = pack.confirmations(json.loads(key_path.read_text())["key"], json.loads(owner_path.read_text())["items"])
    return topics, inserts, owner


def make_backend(args) -> tuple[object, dict | None, str]:
    if args.model in judge_mod.OPENAI_PRICES_PER_MTOK:
        backend = judge_mod.OpenAIJudge(args.model, max_usd=args.max_usd if args.judge else 0.0,
                                        reasoning_effort=args.reasoning_effort,
                                        spend_ledger=args.spend_ledger if args.judge else None)
        return backend, {"model": args.model, **backend.settings}, "openai"
    if args.model in judge_mod.OPENROUTER_PRICES_PER_MTOK:
        backend = judge_mod.OpenRouterJudge(args.model, max_usd=args.max_usd if args.judge else 0.0,
                                            spend_ledger=args.spend_ledger if args.judge else None,
                                            reasoning_max_tokens=args.reasoning_max_tokens)
        return backend, {"model": args.model, **backend.settings}, "openrouter"
    raise SystemExit(f"unknown model {args.model}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="rt")
    p.add_argument("--split", choices=["d1", "gdpr"], required=True)
    p.add_argument("--out")
    p.add_argument("--stand-ins", action="store_true", help="the $0 L7.3 report for the split")
    p.add_argument("--judge", choices=["openai", "openrouter"])
    p.add_argument("--model")
    p.add_argument("--max-usd", type=float)
    p.add_argument("--reasoning-effort", default="medium")
    p.add_argument("--reasoning-max-tokens", type=int)
    p.add_argument("--spend-ledger")
    p.add_argument("--check-inserts", action="store_true", help="the per-topic and per-split insert checks")
    args = p.parse_args(argv)
    topics, inserts, owner = load(args.split)
    if args.check_inserts:
        problems = {t["topic_id"]: insert_problem(t, inserts[t["topic_id"]], strict=args.split == "gdpr")
                    for t in topics if t["topic_id"] in inserts}
        problems = {k: v for k, v in problems.items() if v}
        missing = [t["topic_id"] for t in topics if t["topic_id"] not in inserts]
        split_problem = lexicon_problem([t for t in topics if t["topic_id"] in inserts], inserts)
        for k, v in problems.items():
            print(k, v)
        print("missing:", missing or "none", "| split:", split_problem or "ok")
        return 1 if problems or missing or split_problem else 0
    if args.stand_ins:
        rep = stand_in_report(topics, inserts)
        path = HERE / "rt" / f"standins_{args.split}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(rep, indent=1, sort_keys=True) + "\n")
        b = rep["best_citing"]
        print(args.split, "usable" if rep["usable"] else f"NOT usable: {rep['passing']}",
              "best", b["judge"], round(b["diff"], 3), round(b["lower90"], 3))
        return 0 if rep["usable"] else 1
    if not args.out or not args.model:
        p.error("--out and --model are needed for a judge run")
    if args.split == "gdpr":
        require_confirmed(topics, inserts, owner)
    standins_path = HERE / "rt" / f"standins_{args.split}.json"
    if not standins_path.exists() or not json.loads(standins_path.read_text())["usable"]:
        p.error(f"run --stand-ins first; the split must be usable ({standins_path})")
    if args.judge and args.max_usd is None:
        p.error(f"--judge {args.judge} needs --max-usd")
    backend, meta, provider = make_backend(args)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    judge = judge_mod.CachedJudge(backend, out / "closure_judgements.json", live=args.judge is not None,
                                  meta=meta, live_flag=f"--judge {provider}")
    try:
        res = evaluate(topics, inserts, judge)
    finally:
        judge.save()
    res["split"] = args.split
    res["judge_settings"] = meta
    if args.judge:
        res["spend"] = backend.spend()
    (out / "rt.json").write_text(json.dumps(res, indent=1, sort_keys=True) + "\n")
    p1 = res["part1"]
    print(res["judge_model"], args.split, res["verdict"], {a: round(v, 2) for a, v in p1["hit"].items()},
          "diff", round(p1["diff"], 2), "lower90", round(p1["lower90"], 2), "undecided", res["undecided"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
