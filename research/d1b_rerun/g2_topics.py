"""D1b plan §2.2 G2, step 1: choose the 24 fixture topics and their arms' fixed parts. Topics are
D1's 15 used candidates minus debris, filled to 24 from candidates the rerun excludes by topic
overlap (so no rerun question is contaminated). Each topic keeps the gap map's own seed sentences
and lens question, gets off-topic background from another candidate's retrieval, and joins the
cluster of its nearest D1 item; whole clusters go to the selection or the gate split. The inserted
sentences (P, N, N+) are written later by a separate author into `fixtures/inserts.json`.

    uv run --directory gapmap python ../research/d1b_rerun/g2_topics.py
"""
from __future__ import annotations

import json
import random

from gapmap import lenses, link, semantic, text

import common

N_TOPICS = 24
MIN_SELECTION = 6
SPLIT_SEED = 20261026
BACKGROUND_MAX = 3
SEED_MAX = 2
OUT = common.HERE / "fixtures" / "topics.json"


def _norm(s: str) -> str:
    return " ".join(sorted(common.tokens(s)))


def _probe(lg, index, cand):
    stems, seed_ids, question, seed_text = semantic.primary_probe(lg, cand)
    seed_rows = [list(r) for r in semantic.seed_sentences(index, seed_ids)][:SEED_MAX]
    return stems, seed_ids, question, seed_text, seed_rows


def _background(lg, index, cand, cands, context: frozenset[str]) -> list[list]:
    stems = semantic.primary_probe(lg, cand)[0]
    others = sorted((c for c in cands if c.test_id != cand.test_id and c.lens != "DIAG"),
                    key=lambda c: (link.jaccard(stems, semantic.primary_probe(lg, c)[0]), c.test_id))
    for other in others:
        o_stems, o_ids, *_ = semantic.primary_probe(lg, other)
        rows = [[cid, 0, s] for _id, cid, s in semantic.retrieve(index, o_ids, o_stems).a_items
                if cid not in o_ids and not (text.cw(s) & context)]
        if len(rows) >= BACKGROUND_MAX:
            return rows[:BACKGROUND_MAX]
    raise SystemExit(f"no off-topic background for {cand.test_id}")


def main() -> int:
    d1 = common.d1_items()
    d1_tok = common.d1_tokens()
    d1_quotes = {(_norm(common.quote(it["text"])), it["lens"]): i for i, it in enumerate(d1)}
    used, extra = {}, []
    pools = {}
    for name in common.LEDGER_DIRS:
        lg, index, _ = common.load(name)
        cands = [c for c in lenses.run_all(lg, index, link.SETTING_1)
                 if c.question_text and not c.excluded and c.lens in ("WHY", "RESULT", "HEDGE", "SEL")]
        pools[name] = (lg, index, cands)
        for c in cands:
            q = common.quote(c.question_text)
            if common.debris(q):
                continue
            key = (_norm(q), c.lens)
            if key in d1_quotes:
                used.setdefault(d1_quotes[key], (name, c))
                continue
            j, nearest = common.max_d1_jaccard(c, d1_tok)
            if j >= common.FRESH_JACCARD:
                extra.append((round(-j, 6), c.lens, name, c.test_id, nearest, c))
    topics, seen = [], set()

    def add(name, cand, cluster, origin):
        key = _norm(common.quote(cand.question_text))
        if key in seen:
            return
        seen.add(key)
        lg, index, cands = pools[name]
        _stems, _ids, question, seed_text, seed_rows = _probe(lg, index, cand)
        context = text.cw(seed_text + " " + question) | frozenset().union(*(text.cw(r[2]) for r in seed_rows))
        topics.append({"topic_id": f"t{len(topics) + 1:02d}", "cluster": f"d1-q{d1[cluster]['q']}",
                       "origin": origin, "ledger": name, "lens": cand.lens, "test_id": cand.test_id,
                       "seed_text": seed_text, "question": question, "seed_rows": seed_rows,
                       "background_rows": _background(lg, index, cand, cands, context),
                       "rerun_question_text": cand.question_text})

    for i in sorted(used):
        add(used[i][0], used[i][1], i, "d1-used")
    by_lens: dict[str, list] = {}
    for row in sorted(extra, key=lambda r: r[:4]):
        by_lens.setdefault(row[1], []).append(row)
    while len(topics) < N_TOPICS and any(by_lens.values()):
        for lens in sorted(by_lens):
            if by_lens[lens] and len(topics) < N_TOPICS:
                _j, _l, name, _t, nearest, cand = by_lens[lens].pop(0)
                add(name, cand, nearest, "rerun-excluded")
    clusters = sorted({t["cluster"] for t in topics})
    random.Random(SPLIT_SEED).shuffle(clusters)
    selection, n = set(), 0
    for cl in clusters:
        if n >= MIN_SELECTION:
            break
        selection.add(cl)
        n += sum(t["cluster"] == cl for t in topics)
    for t in topics:
        t["split"] = "selection" if t["cluster"] in selection else "gate"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"split_seed": SPLIT_SEED, "topics": topics}, indent=1) + "\n")
    print(len(topics), "topics;", sum(t["split"] == "selection" for t in topics), "selection,",
          sum(t["split"] == "gate" for t in topics), "gate;", len(clusters), "clusters;",
          "lenses", {l: sum(t["lens"] == l for t in topics) for l in sorted({t["lens"] for t in topics})},
          "origins", {o: sum(t["origin"] == o for t in topics) for o in ("d1-used", "rerun-excluded")})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
