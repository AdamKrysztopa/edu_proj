"""The blind owner pack (plan §1.2, §1.4, §3 (b)).

One item per (seed, question, sentence); the owner marks whether the sentence states the element
the question asks for. The pack shows no source, arm, judge or cited mark; provenance goes to a
separate key file. Sections:
- gdpr: each RT GDPR topic's P, N and background, mixed (parts I and II for that split);
- d1: background sentences any judge cited in the RT D1 runs, plus as many uncited ones from the
  same topics (part II);
- i1c: in sol's I1c GDPR v1 control2 arms, the sentences sol cited in its closed seed-free arms,
  the argmax-overlap sentence of each arm the overlap stand-in closes, plus as many uncited
  sentences from the same arms.

    uv run --directory gapmap python ../research/closure_topicality/pack.py
"""
from __future__ import annotations

import hashlib
import json
import random
import sys
from pathlib import Path

from residual.ledger import Ledger

from gapmap import control2, judge as judge_mod, lenses, link, semantic, standins, text

HERE = Path(__file__).resolve().parent
W = HERE.parents[1]
FIXTURES = HERE / "fixtures"
SOL_I1C = W / "research" / "n3_control_v3" / "sol" / "gdpr_v1"
GDPR_V1 = W / "reconstruct" / "runs" / "20260928T135354Z-eb840a85b7d1" / "ledger.json"
SOL_MODEL = "gpt-6.1-sol"

ELEMENT = {
    "DISC": "how to tell whether something counts as the quoted term: a threshold, a defining feature, "
            "or a contrast between a case that is and one that is not",
    "WHY": "why this is done: the reason, or the failure it prevents, other than 'the law requires it'",
    "HEDGE": "the specific cases in which the rule does not hold: an exception condition, not a "
             "restatement or a cross-reference",
    "SEL": "a condition that says which option to choose in which situation",
    "RESULT": "what result of this test to expect, and what a given result means or which next action it leads to",
    "GUARD": "how a practitioner notices this error before or as it happens",
    "DIAG": "an observable sign that distinguishes the named cause from the other listed causes",
}


def item_id(header: dict, sentence: str) -> str:
    return "i" + hashlib.sha256(f"{header['seed_text']}\x1f{header['question']}\x1f{sentence}".encode()).hexdigest()[:10]


def decoys(rows: list[str], *, cited: set[str], n: int, seed: str) -> list[str]:
    pool = sorted({r for r in rows if r not in cited})
    random.Random(hashlib.sha256(seed.encode()).hexdigest()).shuffle(pool)
    return pool[:n]


class Pack:
    def __init__(self):
        self.items: dict[str, dict] = {}
        self.key: dict[str, list[dict]] = {}

    def add(self, header: dict, sentence: str, provenance: dict) -> str:
        iid = item_id(header, sentence)
        self.items.setdefault(iid, {"header": {k: header[k] for k in ("seed_text", "question", "lens")},
                                    "sentence": sentence})
        self.key.setdefault(iid, []).append(provenance)
        return iid

    def markdown(self) -> str:
        groups: dict[tuple, list[str]] = {}
        for iid, it in self.items.items():
            h = it["header"]
            groups.setdefault((h["seed_text"], h["question"], h["lens"]), []).append(iid)
        lines = ["# Owner pack: does the sentence state the element?", "",
                 "For each sentence, mark **yes** if it states the element the question asks for, about "
                 "the seed, and **no** otherwise. Topical relevance alone is not enough. Reply with the "
                 "item ids you mark **yes**; every other item is read as **no**.", ""]
        order = sorted(groups, key=lambda g: hashlib.sha256("\x1f".join(g).encode()).hexdigest())
        for n, (seed, question, lens) in enumerate(order, 1):
            lines += [f"## Topic {n}", "", f"**Seed:** {seed}", "", f"**Question:** {question}", "",
                      f"**The element:** {ELEMENT[lens]}.", ""]
            ids = sorted(groups[(seed, question, lens)], key=lambda i: hashlib.sha256(i.encode()).hexdigest())
            lines += [f"- `{iid}` {self.items[iid]['sentence']}" for iid in ids] + [""]
        return "\n".join(lines)


def confirmations(key: dict, labels: dict) -> dict:
    """RT topic -> {"P": owner says P states the element, "N": owner says N does not}."""
    out: dict[str, dict] = {}
    for iid, provs in key.items():
        for pv in provs:
            if pv.get("source") == "rt-insert" and iid in labels:
                ok = labels[iid] if pv["arm"] == "P" else not labels[iid]
                out.setdefault(pv["topic"], {})[pv["arm"]] = ok
    return out


def _add_gdpr(pk: Pack) -> None:
    topics = json.loads((FIXTURES / "topics_gdpr.json").read_text())["topics"]
    inserts = json.loads((FIXTURES / "inserts_gdpr.json").read_text())["inserts"]
    import rt
    for t in topics:
        for arm in ("P", "N"):
            pk.add(t, inserts[t["topic_id"]][arm], {"source": "rt-insert", "split": "gdpr", "topic": t["topic_id"], "arm": arm})
        for cid, i, s in rt.background(t):
            pk.add(t, s, {"source": "rt-background", "split": "gdpr", "topic": t["topic_id"], "row": [cid, i]})


def _add_d1(pk: Pack) -> int:
    import rt
    topics = {t["topic_id"]: t for t in json.loads((FIXTURES / "topics_d1.json").read_text())["topics"]}
    cited: dict[str, set] = {tid: set() for tid in topics}
    partial: dict[str, set] = {tid: set() for tid in topics}
    runs = sorted((HERE / "rt" / "d1").glob("*/rt.json"))
    for path in runs:
        res = json.loads(path.read_text())
        for tid, keys in res["cited_background"].items():
            cited[tid] |= {tuple(k) for k in keys}
        for tid, keys in res.get("partial_background", {}).items():
            partial[tid] |= {tuple(k) for k in keys}
    for tid, t in topics.items():
        bg = {(cid, i): s for cid, i, s in rt.background(t)}
        for k in sorted(cited[tid]):
            pk.add(t, bg[k], {"source": "rt-background-cited", "split": "d1", "topic": tid, "row": list(k)})
        for k in sorted(partial[tid] - cited[tid]):
            pk.add(t, bg[k], {"source": "rt-background-partial", "split": "d1", "topic": tid, "row": list(k)})
        marked = cited[tid] | partial[tid]
        for s in decoys(list(bg.values()), cited={bg[k] for k in marked}, n=len(marked), seed=f"d1/{tid}"):
            pk.add(t, s, {"source": "rt-background-decoy", "split": "d1", "topic": tid})
    return len(runs)


def i1c_arms() -> list[dict]:
    """GDPR v1 control2 pairs with each seed-free arm's sentences, sol's state and cited sentences,
    and the overlap stand-in's state and argmax-overlap sentence."""
    lg = Ledger.from_json(GDPR_V1.read_text())
    idx = link.build_index(lg)
    specs = [s for s in control2.build_pairs(lg, idx, lenses.run_all(lg, idx, link.SETTING_1)) if s.k >= 1]
    cache = json.loads((SOL_I1C / "closure_judgements.json").read_text())
    prompts = [semantic.build_prompt(s.seed_text, s.question, s.arm(a)) for s in specs for a in ("own_sf", "ctrl_sf")]
    ov = standins.calibrate("overlap", standins.overlap, prompts)
    out = []
    for s in specs:
        row = {"cluster": s.seeds[0], "seeds": list(s.seeds), "lens": s.lens, "seed_text": s.seed_text,
               "question": s.question}
        for arm, name in (("own_sf", "own"), ("ctrl_sf", "ctrl")):
            ret = s.arm(arm)
            prompt = semantic.build_prompt(s.seed_text, s.question, ret)
            reply = cache[judge_mod.cache_key(SOL_MODEL, prompt)]
            sents = {id_: sent for id_, _c, sent in ret.a_items}
            sol_out = semantic.judge_retrieval(type("C", (), {"model_id": SOL_MODEL, "ask": lambda self, q, r=reply: r})(),
                                               ret, s.seed_text, s.question)
            sol_cited = [sents[str(x)] for x in reply.get("states", []) if str(x) in sents] if sol_out.state == "closed" else []
            ov_closed = ov.ask(prompt)["states"] != []
            ctx = text.cw(s.seed_text + " " + s.question)
            best = max(sents.values(), key=lambda z: len(ctx & text.cw(z))) if sents else None
            row[name] = {"sentences": list(sents.values()), "sol_state": sol_out.state, "sol_cited": sol_cited,
                         "overlap_closed": ov_closed, "overlap_cited": [best] if ov_closed and best else []}
        out.append(row)
    return out


def _add_i1c(pk: Pack) -> None:
    for n, row in enumerate(i1c_arms()):
        for name in ("own", "ctrl"):
            a = row[name]
            cited = set(a["sol_cited"]) | set(a["overlap_cited"])
            for s in a["sol_cited"]:
                pk.add(row, s, {"source": "i1c-sol-cited", "pair": n, "arm": name})
            for s in a["overlap_cited"]:
                pk.add(row, s, {"source": "i1c-overlap-cited", "pair": n, "arm": name})
            for s in decoys(a["sentences"], cited=cited, n=len(cited), seed=f"i1c/{n}/{name}"):
                pk.add(row, s, {"source": "i1c-decoy", "pair": n, "arm": name})


def main() -> int:
    pk = Pack()
    if (FIXTURES / "inserts_gdpr.json").exists():
        _add_gdpr(pk)
    runs = _add_d1(pk)
    _add_i1c(pk)
    (FIXTURES / "owner_pack.md").write_text(pk.markdown() + "\n")
    (FIXTURES / "owner_pack_key.json").write_text(json.dumps({"note": "provenance; not for the labeller",
                                                              "d1_runs_read": runs, "items": pk.items,
                                                              "key": pk.key}, indent=1, sort_keys=True) + "\n")
    by = {}
    for provs in pk.key.values():
        for pv in provs:
            by[pv["source"]] = by.get(pv["source"], 0) + 1
    print(len(pk.items), "items", by)
    return 0


if __name__ == "__main__":
    sys.exit(main())
