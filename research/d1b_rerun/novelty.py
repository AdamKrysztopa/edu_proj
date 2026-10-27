"""D1b plan §3.5-3.6: blind novelty judging of the owner's answers.

    uv run --directory gapmap python ../research/d1b_rerun/novelty.py lock
    uv run --directory gapmap python ../research/d1b_rerun/novelty.py cases --out DIR
    uv run --directory gapmap python ../research/d1b_rerun/novelty.py ingest --a A.json --b B.json --cases DIR
    uv run --directory gapmap python ../research/d1b_rerun/novelty.py reveal --private-key ~/.d1b/seal.key

Every command takes `--codebase CFG` (default: D1b's `codebase.json`); its files live in that
config's directory. `cases` writes `canaries.json` and `cases.json` (question, answer, the same top-10 corpus passages,
no arm) to a directory outside the repo; each judge reads only that directory and writes
`{id: {"label", "new_content", "reason"}}`. `ingest` refuses unless every canary got its expected
label from both judges. `reveal` opens the sealed key with the owner's private key (the owner types
its passphrase), applies `rule.decide` and adds the secondary readings. D1's corpus and retriever
are reused (`research/d1_demonstrator/judge.py`); D1's script reads a plaintext key, so it is not."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
D1 = HERE.parent / "d1_demonstrator"
TOP_K = 10
LABELS = ["new", "partly", "already written", "no content"]
SYSTEM = (
    "You compare an expert's answer with passages from the written documentation of a software "
    "project and its field. Decide whether the answer adds knowledge the passages do not contain.\n"
    "- new: the answer states at least one concrete fact, check, threshold, rationale, step or "
    "failure case that none of the passages state or directly imply.\n"
    "- partly: the answer's core is in the passages, but it adds a minor detail that is not.\n"
    "- already written: everything substantive in the answer is stated or directly implied by "
    "the passages.\n"
    "- no content: the answer makes no substantive claim (filler, 'I don't know', a restatement "
    "of the question).\n"
    "Judge only against the passages shown, not against what you know. Quote the new content, if any.")
UNBLINDED_ACCURACY = 0.70


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def parse_answers(text: str) -> dict[int, str]:
    return {int(m.group(1)): m.group(2).strip()
            for m in re.finditer(r"^## Q(\d+)\s*\n(.*?)(?=^## Q\d+|\Z)", text, flags=re.M | re.S)}


def blocks(corpus: Path = D1 / "corpus") -> list[dict]:
    manifest = json.loads((corpus / "manifest.json").read_text())
    out = []
    for doc in manifest["documents"]:
        raw = (corpus / doc["file"]).read_text()
        for tag, block in re.findall(r"<(p|pre|h\d)>(.*?)</(?:p|pre|h\d)>", raw, flags=re.S):
            text = html.unescape(re.sub(r"<[^>]+>", " ", block)).strip()
            if len(text.split()) >= 6:
                out.append({"title": doc["title"], "url": doc["url"], "tag": tag, "text": text})
    return out


def passages(corpus: Path = D1 / "corpus") -> list[tuple[str, str]]:
    return [(b["title"], b["text"]) for b in blocks(corpus)]


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z][a-z0-9_]+", text.lower())


class Retriever:
    """D1's tf-idf cosine retriever, with the top-k mean similarity used to match the arms."""

    def __init__(self, items: list[tuple[str, str]]):
        self.items = items
        self.docs = [Counter(_tokens(t)) for _, t in items]
        df = Counter(w for d in self.docs for w in d)
        self.idf = {w: math.log(len(self.docs) / n) for w, n in df.items()}
        self.norms = [math.sqrt(sum((c * self.idf[w]) ** 2 for w, c in d.items())) or 1.0 for d in self.docs]

    def _scores(self, query: str) -> list[tuple[float, int]]:
        qv = {w: c * self.idf.get(w, 0.0) for w, c in Counter(_tokens(query)).items()}
        qn = math.sqrt(sum(v * v for v in qv.values())) or 1.0
        return sorted(((sum(qv.get(w, 0.0) * c * self.idf[w] for w, c in d.items()) / (n * qn), i)
                       for i, (d, n) in enumerate(zip(self.docs, self.norms))), reverse=True)

    def top(self, query: str, k: int = TOP_K) -> list[tuple[str, str]]:
        return [self.items[i] for _, i in self._scores(query)[:k]]

    def similarity(self, query: str, k: int = TOP_K) -> float:
        return sum(s for s, _ in self._scores(query)[:k]) / k


def lock(here: Path = HERE) -> dict:
    questions = parse_answers((here / "questions.md").read_text())
    answers = parse_answers((here / "answers.md").read_text())
    missing = [q for q in sorted(questions) if not answers.get(q)]
    if missing:
        raise SystemExit(f"answers missing for Q{missing}")
    out = {"answers_sha256": _sha(here / "answers.md"), "questions_sha256": _sha(here / "questions.md")}
    (here / "answers.lock.json").write_text(json.dumps(out, indent=1) + "\n")
    return out


def _canaries(question: str, retriever: Retriever, cb=None) -> tuple[list[dict], dict[str, str]]:
    """D1b's canaries are fixed by hand (`canary_mode: fixed`); a new codebase's are generated
    from its own corpus and must pass `canaries.ready` (seeded source, code checks, owner)."""
    filler = ("This is an important point and it depends on the situation, so one should think about it "
              "carefully and consider the context before deciding what to do. ").split()
    spec = json.loads((cb.canaries if cb is not None else HERE / "fixtures" / "canaries.json").read_text())
    generated = cb is not None and cb.canary_mode == "generated"
    if generated:
        sys.path.insert(0, str(HERE))
        import canaries as gen

        corpus_blocks = gen.source_passages(cb)
        gen.ready(spec, cb, source_id=gen.pick(corpus_blocks, cb.seed)["id"])
        copied = gen.copied(question, corpus_blocks, retriever)
    else:
        copied = retriever.top(question, 1)[0][1]
    rows = [{"id": f"c-filler-{n}", "question": question, "answer": " ".join((filler * 10)[:n])} for n in (40, 90)]
    rows.append({"id": "c-copied", "question": question, "answer": copied})
    rows.append({"id": "c-paraphrase", "question": spec["paraphrase_question"], "answer": spec["paraphrase"]})
    rows.append({"id": "c-new", "question": spec["planted_question"] if generated else question,
                 "answer": spec["planted_new"]})
    expected = {"c-filler-40": "no content", "c-filler-90": "no content", "c-copied": "already written",
                "c-paraphrase": "already written", "c-new": "new"}
    return rows, expected


def _with_passages(row: dict, retriever: Retriever) -> dict:
    ctx = retriever.top(row["question"] + " " + row["answer"])
    return {**row, "passages": [{"title": t, "text": x[:1200]} for t, x in ctx]}


def cmd_cases(out: Path, cb=None) -> None:
    here = cb.root if cb is not None else HERE
    lk = json.loads((here / "answers.lock.json").read_text())
    if _sha(here / "answers.md") != lk["answers_sha256"]:
        raise SystemExit("answers.md changed after locking")
    questions = parse_answers((here / "questions.md").read_text())
    answers = parse_answers((here / "answers.md").read_text())
    retriever = Retriever(passages(cb.corpus) if cb is not None else passages())
    canaries, expected = _canaries(questions[min(questions)], retriever, cb)
    out.mkdir(parents=True, exist_ok=True)
    (out / "instructions.txt").write_text(SYSTEM + "\n\nFor each case, read QUESTION, EXPERT ANSWER and PASSAGES. "
                                          "Write one JSON object {id: {\"label\": one of " + json.dumps(LABELS)
                                          + ", \"new_content\": str, \"reason\": str}}.\n")
    (out / "canaries.json").write_text(json.dumps([_with_passages(c, retriever) for c in canaries], indent=1) + "\n")
    (out / "cases.json").write_text(json.dumps(
        [_with_passages({"id": f"q{q}", "question": questions[q], "answer": answers[q]}, retriever)
         for q in sorted(questions)], indent=1) + "\n")
    (here / "canaries_expected.json").write_text(json.dumps(expected, indent=1) + "\n")


def canary_failures(expected: dict[str, str], a: dict, b: dict) -> list[str]:
    return [f"{who}:{cid}" for who, j in (("judge_a", a), ("judge_b", b)) for cid, want in expected.items()
            if (j.get(cid) or {}).get("label") != want]


def length_labels(rows: list[dict]) -> dict[int, str]:
    words = {r["q"]: len(r["answer"].split()) for r in rows}
    cut = statistics.median(words.values())
    return {q: "new" if w >= cut else "already written" for q, w in words.items()}


def guess_accuracy(guesses: dict[int, str], arms: dict[int, str]) -> dict:
    n = len(guesses)
    k = sum(guesses[q] == arms[q] for q in guesses)
    p = sum(math.comb(n, i) for i in range(k, n + 1)) / 2 ** n
    return {"n": n, "correct": k, "accuracy": k / n, "p": p,
            "unblinded": k / n >= UNBLINDED_ACCURACY and p < 0.05}


def reveal(judged: list[dict], sealed: Path, private_key: Path, opened: Path,
           guesses: dict[int, str] | None = None) -> dict:
    sys.path.insert(0, str(HERE))
    import build_sheet
    import rule

    build_sheet.unseal(sealed, private_key, opened)
    key = {it["q"]: it for it in json.loads((opened / "key.json").read_text())["items"]}
    rows = [{"q": r["q"], "arm": key[r["q"]]["arm"], "j1": r["judge_a"].get("label"), "j2": r["judge_b"].get("label")}
            for r in sorted(judged, key=lambda r: r["q"])]
    res = {**rule.decide(rows), "rows": rows}
    by_len = length_labels(judged)
    res["length_only"] = rule.decide([{**r, "j1": by_len[r["q"]], "j2": by_len[r["q"]]} for r in rows])
    if guesses is not None:
        res["blinding"] = guess_accuracy(guesses, {q: it["arm"] for q, it in key.items()})
    return res


def load_guesses(here: Path) -> dict[int, str] | None:
    """The owner's arm guesses, made after the answers were locked (plan §3.3 of D1b)."""
    path = here / "guesses.json"
    if not path.exists():
        return None
    lk = json.loads((here / "answers.lock.json").read_text())
    if _sha(here / "answers.md") != lk["answers_sha256"]:
        raise SystemExit("answers.md changed after locking")
    return {int(q): g for q, g in json.loads(path.read_text()).items()}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="novelty")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("lock")
    c = sub.add_parser("cases")
    c.add_argument("--out", required=True)
    i = sub.add_parser("ingest")
    i.add_argument("--a", required=True)
    i.add_argument("--b", required=True)
    i.add_argument("--cases", required=True)
    r = sub.add_parser("reveal")
    r.add_argument("--private-key", required=True)
    for s in sub.choices.values():
        s.add_argument("--codebase", help="codebase config (default: D1b's)")
    args = p.parse_args(argv)
    sys.path.insert(0, str(HERE))
    import codebase

    cb = codebase.load(args.codebase) if args.codebase else codebase.d1b()
    here = cb.root
    if args.cmd == "lock":
        print(json.dumps(lock(here)))
    elif args.cmd == "cases":
        cmd_cases(Path(args.out), cb)
    elif args.cmd == "ingest":
        a, b = json.loads(Path(args.a).read_text()), json.loads(Path(args.b).read_text())
        failures = canary_failures(json.loads((here / "canaries_expected.json").read_text()), a, b)
        cases = json.loads((Path(args.cases) / "cases.json").read_text())
        judged = [{"q": int(c["id"][1:]), "answer": c["answer"], "judge_a": a.get(c["id"], {}),
                   "judge_b": b.get(c["id"], {})} for c in cases]
        (here / "judgements.json").write_text(json.dumps({"canary_failures": failures, "judged": judged}, indent=1) + "\n")
        print(json.dumps({"canary_failures": failures, "judged": len(judged)}))
        return 1 if failures else 0
    else:
        doc = json.loads((here / "judgements.json").read_text())
        if doc["canary_failures"]:
            raise SystemExit(f"canaries failed: {doc['canary_failures']}")
        res = reveal(doc["judged"], here / "sealed", Path(args.private_key).expanduser(), here / "opened",
                     guesses=load_guesses(here))
        (here / "result.json").write_text(json.dumps(res, indent=1, sort_keys=True) + "\n")
        print(json.dumps({k: v for k, v in res.items() if k != "rows"}, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
