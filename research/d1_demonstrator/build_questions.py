"""D1 step 4: the 15-question sheet. Gap questions are the gap map's HYP questions (union of both
arms, by rank, top-tier first on ties); covered questions are lens candidates the closure judge
closed, phrased by the same lens templates, so the two arms read alike. Run in the gapmap env:

  uv run --directory gapmap python ../research/d1_demonstrator/build_questions.py \
      --arm toptier <ledger> <gapmap_dir> --arm cheap <ledger> <gapmap_dir>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
from collections import Counter
from pathlib import Path

from residual.ledger import Ledger

from gapmap import judge as judge_mod, lenses, link, semantic

HERE = Path(__file__).parent
SEED = 20261025
N_GAP, N_COVERED = 10, 5


def _key(text: str) -> str:
    quoted = re.search(r'"(.{20,}?)"', text)
    return " ".join(re.findall(r"[a-z0-9]+", (quoted.group(1) if quoted else text).lower()))


def _clean(text: str) -> str:
    """Conversion debris, removed alike in both arms: blockquote marks and markdown links."""
    text = re.sub(r"\s>\s(?![\d=])", " ", text)
    return re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)


def arm_pools(name: str, ledger_path: str, gapmap_dir: str) -> tuple[list[dict], list[dict]]:
    ledger = Ledger.from_json(Path(ledger_path).read_text())
    index = link.build_index(ledger)
    judge = judge_mod.CachedJudge(judge_mod.OllamaJudge(), Path(gapmap_dir) / "closure_judgements.json",
                                  live=False)
    gm = json.loads((Path(gapmap_dir) / "gapmap.json").read_text())
    gap = [{"arm": "gap", "source_arm": name, "rank": i, "gap_id": r["gap_id"], "lens": r["lens"],
            "anchor": r["anchor"], "k_topic": r["confidence"]["k_topic"], "text": r["question"]["text"]}
           for i, r in enumerate(x for x in gm["map"] if x["category"] == "HYP" and x.get("question"))]
    covered, single = [], []
    for cand in lenses.run_all(ledger, index, link.SETTING_1):
        if not cand.question_text or cand.excluded:
            continue
        outcome, sub = semantic.judge_candidate(ledger, index, judge, cand)
        if outcome.state == "open" and len(link.breadth(ledger, sub.x_a)) < 2:
            single.append({"arm": "gap", "source_arm": name, "rank": len(single), "fallback": "RG-SINGLE",
                           "test_id": cand.test_id, "lens": cand.lens, "anchor": cand.anchor,
                           "lexical_state": cand.lexical_state, "k_topic": 1, "text": cand.question_text})
        if outcome.state != "closed":
            continue
        covered.append({"arm": "covered", "source_arm": name, "test_id": cand.test_id, "lens": cand.lens,
                        "anchor": cand.anchor, "lexical_state": cand.lexical_state,
                        "k_topic": len(link.breadth(ledger, sub.x_a)), "text": cand.question_text})
    covered.sort(key=lambda c: (c["lexical_state"] != "closed", -c["k_topic"]))
    single.sort(key=lambda c: (c["lexical_state"] != "open", c["rank"]))
    return gap + single, covered


def pick(arms: list[tuple[str, list[dict], list[dict]]]) -> tuple[list[dict], list[dict]]:
    order = {name: i for i, (name, _, _) in enumerate(arms)}
    # HYP questions first; single-source open candidates only fill what HYP cannot
    gap_all = sorted((g for _, gaps, _ in arms for g in gaps),
                     key=lambda g: ("fallback" in g, g["rank"], order[g["source_arm"]]))
    seen, gaps = set(), []
    for g in gap_all:
        if _key(g["text"]) not in seen and len(gaps) < N_GAP:
            seen.add(_key(g["text"]))
            gaps.append(g)
    want = Counter(g["lens"] for g in gaps)
    cov_all = [c for _, _, covs in arms for c in covs if _key(c["text"]) not in seen]
    cov_all.sort(key=lambda c: (c["lexical_state"] != "closed", -c["k_topic"]))
    covered, have = [], Counter()
    # prefer the gap questions' lens mix, so the lens template does not give the arm away
    for pass_ in (0, 1):
        for c in cov_all:
            if len(covered) == N_COVERED:
                break
            k = _key(c["text"])
            if k in seen or (pass_ == 0 and have[c["lens"]] >= max(1, round(want[c["lens"]] * N_COVERED / N_GAP))):
                continue
            seen.add(k)
            have[c["lens"]] += 1
            covered.append(c)
    return gaps, covered


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", nargs=3, action="append", metavar=("NAME", "LEDGER", "GAPMAP_DIR"), required=True)
    args = ap.parse_args()
    arms = [(n, *arm_pools(n, l, d)) for n, l, d in args.arm]
    gaps, covered = pick(arms)
    if len(gaps) < N_GAP or len(covered) < N_COVERED:
        raise SystemExit(f"not enough questions: {len(gaps)} gap, {len(covered)} covered")
    items = gaps + covered
    for it in items:
        it["text"] = _clean(it["text"])
    random.Random(SEED).shuffle(items)
    for i, it in enumerate(items, 1):
        it["q"] = i

    sheet = ["# D1 questions", "",
             "Answer each question in plain prose, from memory, without the docs or the code open.",
             "A few sentences is enough. \"I don't know\" or \"this never comes up\" is a fine answer.",
             "Write your answers in `answers.md`, under the matching heading. Do not open `sealed/`.", ""]
    answers = ["# D1 answers", ""]
    for it in items:
        sheet += [f"## Q{it['q']}", "", it["text"], ""]
        answers += [f"## Q{it['q']}", "", ""]
    (HERE / "questions.md").write_text("\n".join(sheet))
    if not (HERE / "answers.md").exists():
        (HERE / "answers.md").write_text("\n".join(answers))
    sealed = HERE / "sealed"
    sealed.mkdir(exist_ok=True)
    words = {a: [len(it["text"].split()) for it in items if it["arm"] == a] for a in ("gap", "covered")}
    key = {"seed": SEED, "items": items,
           "pool_sizes": {n: {"gap": len(g), "covered": len(c)} for n, g, c in arms},
           "mean_words": {a: sum(v) / len(v) for a, v in words.items()},
           "lens_mix": {a: dict(Counter(it["lens"] for it in items if it["arm"] == a)) for a in ("gap", "covered")}}
    (sealed / "key.json").write_text(json.dumps(key, indent=1) + "\n")
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    print(json.dumps({"questions_sha256": sha(HERE / "questions.md"), "key_sha256": sha(sealed / "key.json"),
                      "pool_sizes": key["pool_sizes"], "mean_words": key["mean_words"],
                      "lens_mix": key["lens_mix"]}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
