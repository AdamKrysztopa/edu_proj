"""D1b plan §2.2 G2: the topicality-controlled closure check, the judge's primary gate.

Per topic, five arms share the gap map's seed sentences, lens question and off-topic background,
and differ only in the inserted sentences: 0 (none), P (states the element), N (an on-topic,
concrete non-element, at least as long and as on-topic as P), N+ (N plus 2-3 more on-topic
non-elements), R (random letters with P's word lengths). Pass on a split, stated before any call:
close(P) - close(N) >= 0.50, its cluster-bootstrap lower bound (5th percentile of 2,000 resamples
of whole clusters) >= 0.30, close(N) <= 0.25, close(N+) <= 0.25, close(R) <= 0.10,
close(0) <= 0.25. Only "closed" counts as closing. Amendment (owner, 2026-10-26, post hoc, found on
gemma's gate data): every R arm contains the no-insert arm, so R is scored on what the random letters
add -- R closures among topics whose no-insert arm is open (`R_excess`); the raw R rate is reported. Any undecided arm makes the verdict incomplete,
never a fail; a judge that cannot answer (rate limit, truncation) stops the run. Runs only on fixtures the owner confirmed.
`--stand-ins` ($0) also runs an oracle that closes only P, which must pass: the fixtures can still be met.

    uv run --directory gapmap python ../research/d1b_rerun/g2.py --out DIR --split selection|gate \
        [--judge openrouter --model M --max-usd X --spend-ledger ../research/d1b_rerun/openrouter_spend.jsonl]
        [--judge openai --model gpt-6.1-sol --reasoning-effort high \
         --max-usd X --spend-ledger ../research/d1b_rerun/openai_spend.jsonl]
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

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures"
INSERT = "insert"
ARMS = ("0", "P", "N", "N+", "R")
BOOTSTRAP_B = 2000
BOOTSTRAP_SEED = 20261026
LENGTH_SLACK = 0.10


class Unconfirmed(RuntimeError):
    pass


def _random_letters(p: str) -> str:
    rng = random.Random(hashlib.sha256(p.encode()).hexdigest())
    return " ".join("".join(rng.choice(string.ascii_lowercase) for _ in w) for w in p.split())


def arms(topic: dict, ins: dict) -> dict[str, list[list]]:
    seed, bg = [list(r) for r in topic["seed_rows"]], [list(r) for r in topic["background_rows"]]
    one = lambda *sents: seed + [[INSERT, k, s] for k, s in enumerate(sents)] + bg
    return {"0": seed + bg, "P": one(ins["P"]), "N": one(ins["N"]), "N+": one(ins["N"], *ins["N_plus"]),
            "R": one(_random_letters(ins["P"]))}


def _overlap(topic: dict, sentence: str) -> int:
    return len(text.cw(topic["seed_text"] + " " + topic["question"]) & text.cw(sentence))


def insert_problem(topic: dict, ins: dict) -> str | None:
    """N must be at least as long and as on-topic as P, and at most 10% longer, so no length or
    overlap stand-in can favour P."""
    lp, ln = len(ins["P"]), len(ins["N"])
    if not lp <= ln <= lp * (1 + LENGTH_SLACK):
        return f"length: N is {ln} chars against P's {lp}; it must be {lp}-{int(lp * (1 + LENGTH_SLACK))}"
    if _overlap(topic, ins["N"]) < _overlap(topic, ins["P"]):
        return "overlap: N shares fewer seed and question words than P"
    if not 2 <= len(ins["N_plus"]) <= 3 or any(_overlap(topic, s) == 0 for s in ins["N_plus"]):
        return "N_plus: needs 2-3 sentences, each sharing a seed or question word"
    return None


def has_marker(sentence: str) -> bool:
    return any(config.PATTERNS[name].search(sentence) for name in standins.CLOSING_LEXICONS)


def marker_problem(topics: list[dict], inserts: dict) -> str | None:
    """A closing-lexicon hit in P must be as common as in N over the set, or the lexicon stand-in
    favours P (methods-critic, 2026-10-26)."""
    p = sum(has_marker(inserts[t["topic_id"]]["P"]) for t in topics)
    n = sum(has_marker(inserts[t["topic_id"]]["N"]) for t in topics)
    return None if abs(p - n) <= 1 else f"marker: {p} Ps against {n} Ns carry a closing-lexicon word"


def seed_drops(states: dict[str, dict[str, str]]) -> list[str]:
    """Topics whose no-insert arm every seed reader closed: the seed reads as stating the element."""
    return sorted(t for t, by in states.items() if by and all(v == "closed" for v in by.values()))


def kept_topics(topics: list[dict], confirmed: dict) -> list[dict]:
    dropped = confirmed.get("_dropped", {})
    return [t for t in topics if t["topic_id"] not in dropped]


def require_confirmed(topics: list[dict], inserts: dict, confirmed: dict) -> None:
    missing = [t["topic_id"] for t in topics
               if not all(confirmed.get(t["topic_id"], {}).get(k) is True for k in ("P", "N", "N_plus", "seed_open"))]
    if missing:
        raise Unconfirmed(f"the owner has not confirmed {len(missing)} topic(s): {', '.join(missing)}")
    bad = {t["topic_id"]: p for t in topics if (p := insert_problem(t, inserts[t["topic_id"]]))}
    if bad:
        raise Unconfirmed(f"unmatched inserts: {bad}")
    if problem := marker_problem(topics, inserts):
        raise Unconfirmed(problem)


def _state(judge, topic: dict, rows: list[list]) -> str:
    retrieval = semantic.build_retrieval([tuple(r) for r in rows])
    return semantic.judge_retrieval(judge, retrieval, topic["seed_text"], topic["question"]).state


def stand_ins(topics: list[dict], inserts: dict) -> list:
    rec = standins.RecordingJudge()
    for t in topics:
        for rows in arms(t, inserts[t["topic_id"]]).values():
            _state(rec, t, rows)
    return [standins.calibrate("length", standins.length, rec.prompts),
            standins.calibrate("overlap", standins.overlap, rec.prompts),
            standins.calibrate("specificity", standins.specificity, rec.prompts),
            standins.LexiconJudge(), standins.CoinFlipJudge()]


class OracleJudge:
    """Closes exactly the arms holding a P sentence: the planted positive the fixtures must let pass."""
    model_id = "oracle-p"

    def __init__(self, inserts: dict):
        self.ps = {v["P"] for v in inserts.values()}

    def ask(self, prompt: str) -> dict:
        return {"states": [i for i, s in standins.parse(prompt).sentences if s in self.ps], "partially": []}


def _lower(per_topic: list[tuple[str, int]]) -> float:
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


def evaluate(topics: list[dict], inserts: dict, judge, *, split: str) -> dict:
    chosen = [t for t in topics if split == "all" or t["split"] == split]
    states = {t["topic_id"]: {a: _state(judge, t, rows) for a, rows in arms(t, inserts[t["topic_id"]]).items()}
              for t in chosen}
    closed = {tid: {a: s == "closed" for a, s in st.items()} for tid, st in states.items()}
    rates = {a: sum(c[a] for c in closed.values()) / len(chosen) for a in ARMS}
    per_topic = [(t["cluster"], int(closed[t["topic_id"]]["P"]) - int(closed[t["topic_id"]]["N"])) for t in chosen]
    base_open = [tid for tid in closed if not closed[tid]["0"]]
    r_excess = sum(closed[tid]["R"] for tid in base_open) / len(base_open) if base_open else 0.0
    res = {"judge_model": judge.model_id, "split": split, "n_topics": len(chosen), "R_excess": r_excess,
           "n_clusters": len({t["cluster"] for t in chosen}), "rates": rates,
           "diff": rates["P"] - rates["N"], "lower90": _lower(per_topic),
           "undecided": sum(s == "undecided" for st in states.values() for s in st.values()), "states": states}
    res["complete"] = res["undecided"] == 0
    res["passes"] = passes(res)
    return res


def passes(res: dict) -> bool:
    r = res["rates"]
    return (res.get("undecided", 0) == 0 and res["diff"] >= 0.50 and res["lower90"] >= 0.30 and r["N"] <= 0.25 and r["N+"] <= 0.25
            and res.get("R_excess", r["R"]) <= 0.10 and r["0"] <= 0.25)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="g2")
    p.add_argument("--out", required=True)
    p.add_argument("--split", choices=["selection", "gate", "all"], required=True)
    p.add_argument("--judge", choices=["ollama", "openai", "openrouter"])
    p.add_argument("--model", default=config.JUDGE_MODEL)
    p.add_argument("--max-usd", type=float)
    p.add_argument("--reasoning-effort", default="medium")
    p.add_argument("--spend-ledger")
    p.add_argument("--reasoning-max-tokens", type=int, help="OpenRouter judge only: cap the model's reasoning")
    p.add_argument("--stand-ins", action="store_true", help="score the stand-ins instead of a judge ($0)")
    args = p.parse_args(argv)
    topics = json.loads((FIXTURES / "topics.json").read_text())["topics"]
    inserts = json.loads((FIXTURES / "inserts.json").read_text())
    confirmed = json.loads((FIXTURES / "confirmations.json").read_text())
    topics = kept_topics(topics, confirmed)
    require_confirmed(topics, inserts, confirmed)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    if args.stand_ins:
        rows = [evaluate(topics, inserts, j, split=args.split) for j in stand_ins(topics, inserts)]
        (out / f"g2_standins_{args.split}.json").write_text(json.dumps(rows, indent=1, sort_keys=True) + "\n")
        oracle = evaluate(topics, inserts, OracleJudge(inserts), split=args.split)
        (out / f"g2_oracle_{args.split}.json").write_text(json.dumps(oracle, indent=1, sort_keys=True) + "\n")
        for r in [*rows, oracle]:
            print(r["judge_model"], round(r["diff"], 3), "PASSES" if r["passes"] else "fails")
        return 1 if any(r["passes"] for r in rows) or not oracle["passes"] else 0
    provider = ("openai" if args.model in judge_mod.OPENAI_PRICES_PER_MTOK
                else "openrouter" if args.model in judge_mod.OPENROUTER_PRICES_PER_MTOK else "ollama")
    if args.judge in ("openai", "openrouter") and args.max_usd is None:
        p.error(f"--judge {args.judge} needs --max-usd")
    if provider == "openai":
        backend = judge_mod.OpenAIJudge(args.model, max_usd=args.max_usd if args.judge else 0.0,
                                        reasoning_effort=args.reasoning_effort,
                                        spend_ledger=args.spend_ledger if args.judge else None)
        meta = {"model": args.model, **backend.settings}
    elif provider == "openrouter":
        backend = judge_mod.OpenRouterJudge(args.model, max_usd=args.max_usd if args.judge else 0.0,
                                            spend_ledger=args.spend_ledger if args.judge else None,
                                            reasoning_max_tokens=args.reasoning_max_tokens)
        meta = {"model": args.model, **backend.settings}
    else:
        backend, meta = judge_mod.OllamaJudge(model=args.model), None
    use_openai = provider != "ollama"
    judge = judge_mod.CachedJudge(backend, out / "closure_judgements.json", live=args.judge is not None, meta=meta,
                                  live_flag=f"--judge {provider}")
    try:
        res = evaluate(topics, inserts, judge, split=args.split)
    finally:
        judge.save()
    if use_openai:
        res["spend"] = backend.spend()
    (out / f"g2_{args.split}.json").write_text(json.dumps(res, indent=1, sort_keys=True) + "\n")
    print(res["judge_model"], args.split, {a: round(v, 2) for a, v in res["rates"].items()},
          "diff", round(res["diff"], 2), "lower90", round(res["lower90"], 2), "R_excess", round(res["R_excess"], 2),
          "PASSES" if res["passes"] else "fails" if res["complete"] else f"INCOMPLETE ({res['undecided']} undecided)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
