"""Novelty-judge canaries generated per codebase from its own corpus (D1c plan §5.3).

    uv run --directory gapmap python ../research/d1b_rerun/canaries.py pick --codebase CFG
    uv run --directory gapmap python ../research/d1b_rerun/canaries.py check --codebase CFG

`pick` chooses the paraphrase's source passage by seeded code (an owner-doc prose block of bounded
length) and writes the brief for a separate author, who never sees a question sheet or an arm.
The author writes `fixtures/canaries.json`; `check` applies the code checks below; the owner then
confirms the two labels and sets `owner_confirmed`. `novelty.py cases` refuses until all three
hold. Filler and the copied passage need no author: filler is fixed text, and the copy is the
eligible passage the retriever ranks first for the sheet's first question.

The checks guard what each canary is for: a paraphrase must be judged "already written" on
meaning, so it may not pass on lexical match (content-word Jaccard and longest shared word run are
capped) and its source must be among the passages the judges are shown; a planted answer must be
judged "new" on content, so it must stay on the corpus's topic and every planted term must be
absent from the whole corpus."""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
from pathlib import Path

import codebase
import common
import novelty

MIN_WORDS, MAX_WORDS = 30, 150
PARA_MAX_JACCARD = 0.50
PARA_MAX_RUN = 6
PARA_LENGTH = (0.5, 2.0)
PLANT_MIN_SHARED = 3
PLANT_MAX_JACCARD = 0.30
SPEC_KEYS = ("source_id", "paraphrase_question", "paraphrase", "planted_question", "planted_new", "planted_terms",
             "owner_confirmed")


class NotReady(RuntimeError):
    pass


def source_passages(cb: codebase.Codebase) -> list[dict]:
    return [{**b, "id": hashlib.sha256(b["text"].encode()).hexdigest()[:12], "owner": cb.owner_repo in b["url"]}
            for b in novelty.blocks(cb.corpus)]


def _sentences(text_: str) -> int:
    return len(re.findall(r"[.!?](?:\s|$)", text_))


def eligible(passages: list[dict]) -> list[dict]:
    seen, out = set(), []
    for p in sorted(passages, key=lambda p: p["id"]):
        n = len(p["text"].split())
        if (p["owner"] and p["tag"] == "p" and MIN_WORDS <= n <= MAX_WORDS and _sentences(p["text"]) >= 2
                and "|" not in p["text"] and p["id"] not in seen):
            seen.add(p["id"])
            out.append(p)
    return out


def pick(passages: list[dict], seed: int) -> dict:
    elig = eligible(passages)
    if not elig:
        raise NotReady("no eligible owner-doc passage for the paraphrase canary")
    return random.Random(seed).choice(elig)


def _longest_run(a: str, b: str) -> int:
    x, y = re.findall(r"\w+", a.lower()), re.findall(r"\w+", b.lower())
    best, prev = 0, [0] * (len(y) + 1)
    for i in range(1, len(x) + 1):
        cur = [0] * (len(y) + 1)
        for j in range(1, len(y) + 1):
            if x[i - 1] == y[j - 1]:
                cur[j] = prev[j - 1] + 1
                best = max(best, cur[j])
        prev = cur
    return best


def paraphrase_problems(source: str, question: str, paraphrase: str, retriever: novelty.Retriever) -> list[str]:
    out = []
    j = common.jaccard(common.tokens(source), common.tokens(paraphrase))
    if j > PARA_MAX_JACCARD:
        out.append(f"too close to a copy of its source (content-word Jaccard {j:.2f} > {PARA_MAX_JACCARD})")
    run = _longest_run(source, paraphrase)
    if run > PARA_MAX_RUN:
        out.append(f"shares a {run}-word run with its source (a copy; at most {PARA_MAX_RUN})")
    ratio = len(paraphrase.split()) / max(len(source.split()), 1)
    if not PARA_LENGTH[0] <= ratio <= PARA_LENGTH[1]:
        out.append(f"length {ratio:.2f} times its source, outside {PARA_LENGTH}")
    ranked = [t for _, t in retriever.top(question + " " + paraphrase, len(retriever.items))]
    rank = ranked.index(source) + 1 if source in ranked else None
    if rank is None or rank > novelty.TOP_K:
        out.append(f"its source passage is not among the {novelty.TOP_K} passages the judges are shown "
                   f"(rank {rank} for question plus paraphrase): name the passage's topic in "
                   "paraphrase_question in the documentation's own terms, as the sheet's questions quote it")
    return out


def _present(term: str, text_: str) -> bool:
    return re.search(r"(?<!\w)" + re.escape(term.lower()) + r"(?!\w)", text_.lower()) is not None


def planted_problems(question: str, planted: str, terms: list[str], passages: list[dict],
                     retriever: novelty.Retriever) -> list[str]:
    if not terms:
        return ["no planted terms: list the strings that carry the facts the corpus lacks"]
    out = [f"planted term not in the answer: {t!r}" for t in terms if not _present(t, planted)]
    corpus_text = "\n".join(p["text"] for p in passages)
    out += [f"planted term in the corpus: {t!r}" for t in terms if _present(t, corpus_text)]
    shown = [t for _, t in retriever.top(question + " " + planted)]
    toks = common.tokens(planted)
    shared = max((len(toks & common.tokens(t)) for t in shown), default=0)
    if shared < PLANT_MIN_SHARED:
        out.append(f"off-topic: shares {shared} content words with the passages shown (needs {PLANT_MIN_SHARED})")
    close = max((common.jaccard(toks, common.tokens(t)) for t in shown), default=0.0)
    if close > PLANT_MAX_JACCARD:
        out.append(f"too close to a corpus passage (content-word Jaccard {close:.2f} > {PLANT_MAX_JACCARD})")
    return out


def copied(question: str, passages: list[dict], retriever: novelty.Retriever) -> str:
    ok = {p["text"] for p in eligible(passages)}
    for _, text_ in retriever.top(question, len(retriever.items)):
        if text_ in ok:
            return text_
    raise NotReady("no eligible passage for the copied canary")


def check(spec: dict, cb: codebase.Codebase) -> list[str]:
    missing = [k for k in SPEC_KEYS if k not in spec]
    if missing:
        return [f"missing keys: {missing}"]
    passages = source_passages(cb)
    retriever = novelty.Retriever([(p["title"], p["text"]) for p in passages])
    src = next((p for p in passages if p["id"] == spec["source_id"]), None)
    if src is None:
        return [f"source_id {spec['source_id']} is not a passage of this corpus"]
    return (paraphrase_problems(src["text"], spec["paraphrase_question"], spec["paraphrase"], retriever)
            + planted_problems(spec["planted_question"], spec["planted_new"], spec["planted_terms"], passages,
                               retriever))


def ready(spec: dict, cb: codebase.Codebase, *, source_id: str) -> None:
    if spec.get("source_id") != source_id:
        raise NotReady(f"the paraphrase is not of the seeded source passage {source_id}")
    problems = check(spec, cb)
    if problems:
        raise NotReady("; ".join(problems))
    if spec.get("owner_confirmed") is not True:
        raise NotReady("the owner has not confirmed the canary labels")


def brief(src: dict, cb: codebase.Codebase | None = None, config: str = "CFG") -> str:
    repo = Path(__file__).resolve().parents[2]
    out = cb.canaries.relative_to(repo) if cb is not None else "fixtures/canaries.json"
    corpus = cb.corpus.relative_to(repo) if cb is not None else "the corpus directory"
    check = f"uv run --directory gapmap python ../research/d1b_rerun/canaries.py check --codebase {config}"
    return f"""# Canary brief

You write two short answers used to check two blind judges. Each judge compares an expert's
answer with passages from a software project's documentation and labels it "new" (it adds
knowledge the passages lack) or "already written". You never see any real question or answer.

Source passage, from the project's own documentation (id {src['id']}, "{src['title']}"):

> {src['text']}

Write one JSON object with these keys:

- `source_id`: "{src['id']}".
- `paraphrase_question`: a question a newcomer to the project could ask that the passage answers,
  naming its topic in the documentation's own terms (the judges are shown the passages retrieved
  for the question and the answer together, so the source must still be found).
- `paraphrase`: an expert's answer to it that says what the passage says in new words. Keep every
  claim, add none, never reuse a run of more than {PARA_MAX_RUN} words from the passage, and keep
  its length between half and twice the passage's.
- `planted_question`: a question on the passage's topic.
- `planted_new`: an expert's answer to it, 50 to 90 words, on the same topic, that states two or
  three concrete facts the documentation does not contain: a number with its unit, a threshold, a
  named case, a failure seen in practice. Invent them; keep them plausible.
- `planted_terms`: the exact short strings in `planted_new` that carry the invented facts (for
  example "a 3-day cutoff"). Each must occur nowhere in the documentation.
- `owner_confirmed`: false.

Paths are relative to the repository root. Save it as `{out}`. The documentation is the HTML
under `{corpus}`; you may search it. Then run `{check}` from the repository root and revise until it prints `"ready": false` with only the owner's confirmation
missing. The owner confirms both labels before use.
"""


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="canaries")
    p.add_argument("cmd", choices=("pick", "check"))
    p.add_argument("--codebase", required=True)
    args = p.parse_args(argv)
    cb = codebase.load(args.codebase)
    passages = source_passages(cb)
    src = pick(passages, cb.seed)
    if args.cmd == "pick":
        out = cb.root / "fixtures" / "canary_brief.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(brief(src, cb, args.codebase))
        print(json.dumps({"source_id": src["id"], "eligible": len(eligible(passages)), "brief": str(out)}))
        return 0
    spec = json.loads(cb.canaries.read_text())
    try:
        ready(spec, cb, source_id=src["id"])
    except NotReady as e:
        print(json.dumps({"ready": False, "why": str(e)}))
        return 1
    print(json.dumps({"ready": True}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
