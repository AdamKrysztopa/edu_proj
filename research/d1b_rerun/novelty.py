"""D1b plan §3.5-3.6: blind novelty judging of the owner's answers.

    uv run --directory gapmap python ../research/d1b_rerun/novelty.py lock
    uv run --directory gapmap python ../research/d1b_rerun/novelty.py cases --out DIR
    uv run --directory gapmap python ../research/d1b_rerun/novelty.py ingest --a A.json --b B.json
    uv run --directory gapmap python ../research/d1b_rerun/novelty.py reveal --private-key ~/.d1b/seal.key

Every command takes `--codebase CFG` (default: D1b's `codebase.json`); its files live in that
config's directory. `cases` writes one `cases.json` (question, answer, the same top-10 corpus
passages, no arm) to a directory outside the repo, canaries mixed in at random positions under
random opaque ids; the id map stays in the codebase directory. Each judge reads only that
directory and writes `{id: {"label", "new_content", "reason"}}`. `ingest` runs once; a canary that
either judge mislabels voids the reading at `reveal` (No reading). `reveal` opens the sealed key
with the owner's private key (the owner types its passphrase), applies `rule.decide` and adds the
secondary readings. D1's corpus and retriever are reused (`research/d1_demonstrator/judge.py`);
D1's script reads a plaintext key, so it is not."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import random
import re
import secrets
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


def spare_questions(pool: Path, questions: Path, *, seed: int, k: int) -> list[str]:
    """Lens-template questions from pool topics that are not on the sheet, seeded: canaries that
    carry them look like real cases without repeating a real case's question."""
    on_sheet = set(parse_answers(questions.read_text()).values()) if questions.exists() else set()
    texts = sorted({t["question_text"] for t in json.loads(pool.read_text())["topics"]} - on_sheet)
    return random.Random(seed).sample(texts, min(k, len(texts)))


def _canaries(question: str, retriever: Retriever, cb=None,
              spare_questions: list[str] | None = None) -> tuple[list[dict], dict[str, str]]:
    """D1b's canaries are fixed by hand (`canary_mode: fixed`); a new codebase's are generated
    from its own corpus and must pass `canaries.ready` (seeded source, code checks, owner). With
    spare questions, the filler and copied canaries carry them instead of the sheet's first."""
    filler = ("This is an important point and it depends on the situation, so one should think about it "
              "carefully and consider the context before deciding what to do. ").split()
    spec = json.loads((cb.canaries if cb is not None else HERE / "fixtures" / "canaries.json").read_text())
    generated = cb is not None and cb.canary_mode == "generated"
    q40, q90, q_copied = (spare_questions if spare_questions and len(spare_questions) >= 3 else [question] * 3)[:3]
    if generated:
        sys.path.insert(0, str(HERE))
        import canaries as gen

        corpus_blocks = gen.source_passages(cb)
        gen.ready(spec, cb, source_id=gen.pick(corpus_blocks, cb.seed)["id"])
        copied = gen.copied(q_copied, corpus_blocks, retriever)
    else:
        copied = retriever.top(q_copied, 1)[0][1]
    rows = [{"id": f"c-filler-{n}", "question": q, "answer": " ".join((filler * 10)[:n])}
            for n, q in ((40, q40), (90, q90))]
    rows.append({"id": "c-copied", "question": q_copied, "answer": copied})
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
    spare = (spare_questions(cb.pool, here / "questions.md", seed=cb.seed, k=3)
             if cb is not None and cb.canary_mode == "generated" else None)
    canaries, expected = _canaries(questions[min(questions)], retriever, cb, spare)
    cases, case_map = build_cases(questions, answers, canaries, expected, retriever)
    out.mkdir(parents=True, exist_ok=True)
    (out / "instructions.txt").write_text(SYSTEM + "\n\nFor each case, read QUESTION, EXPERT ANSWER and PASSAGES. "
                                          "Write one JSON object {id: {\"label\": one of " + json.dumps(LABELS)
                                          + ", \"new_content\": str, \"reason\": str}}.\n")
    (out / "cases.json").write_text(json.dumps(cases, indent=1) + "\n")
    (here / "case_map.json").write_text(json.dumps(case_map, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"cases": len(cases), "case_map_sha256": _sha(here / "case_map.json"),
                      "cases_sha256": _sha(out / "cases.json")}))


def build_cases(questions: dict[int, str], answers: dict[int, str], canary_rows: list[dict],
                expected: dict[str, str], retriever: Retriever) -> tuple[list[dict], dict]:
    """Canaries and real cases in one file, in random order, under random opaque ids, so that no
    judge can tell a canary from a case by its id or file. The map stays outside the judges'
    directory. Unseeded on purpose: a seeded order could be recomputed from this code."""
    rng = random.SystemRandom()
    rows = [({"kind": "canary", "canary": c["id"], "expected": expected[c["id"]]}, c) for c in canary_rows]
    rows += [({"kind": "case", "q": q}, {"question": questions[q], "answer": answers[q]}) for q in sorted(questions)]
    rng.shuffle(rows)
    ids: set[str] = set()
    while len(ids) < len(rows):
        ids.add(secrets.token_hex(4))
    cases, case_map = [], {}
    for cid, (meta, row) in zip(sorted(ids, key=lambda _: rng.random()), rows):
        case_map[cid] = meta
        cases.append(_with_passages({"id": cid, "question": row["question"], "answer": row["answer"]}, retriever))
    return cases, case_map


def split_judgements(case_map: dict, a: dict, b: dict, answers: dict[int, str]) -> tuple[list[str], list[dict]]:
    expected = {m["canary"]: m["expected"] for m in case_map.values() if m["kind"] == "canary"}
    by_canary = {m["canary"]: cid for cid, m in case_map.items() if m["kind"] == "canary"}
    failures = canary_failures(expected, {c: a.get(by_canary[c]) for c in expected},
                               {c: b.get(by_canary[c]) for c in expected})
    judged = [{"q": m["q"], "answer": answers[m["q"]], "judge_a": a.get(cid, {}), "judge_b": b.get(cid, {})}
              for cid, m in case_map.items() if m["kind"] == "case"]
    return failures, sorted(judged, key=lambda r: r["q"])


def ingest(here: Path, a: dict, b: dict, raw: dict[str, Path] | None = None) -> dict:
    """One pass per judge: a second ingest is refused. The raw outputs' hashes are recorded; the
    plan also commits them as each judge returns, so a re-run judge would show as a hash change."""
    if (here / "judgements.json").exists():
        raise SystemExit("judgements.json exists: each judge gets one pass")
    case_map = json.loads((here / "case_map.json").read_text())
    failures, judged = split_judgements(case_map, a, b, parse_answers((here / "answers.md").read_text()))
    failures += [f"{who}:invalid: {p}" for who, out in (("judge_a", a), ("judge_b", b))
                 for p in output_problems(case_map, out)]
    doc = {"canary_failures": failures, "judged": judged,
           "raw_sha256": {k: _sha(Path(p)) for k, p in (raw or {}).items()}}
    (here / "judgements.json").write_text(json.dumps(doc, indent=1) + "\n")
    return doc


def _crosses(want: str, got: str | None) -> bool:
    """A canary error voids a judge only when it would move the decision: the rule counts "new",
    and the content floor counts "no content"; "partly" on a written-down canary moves neither."""
    if want == "new":
        return got != "new"
    if want == "no content":
        return got != "no content"
    return got in (None, "new", "no content")


def canary_failures(expected: dict[str, str], a: dict, b: dict) -> list[str]:
    return [f"{who}:{cid}" for who, j in (("judge_a", a), ("judge_b", b)) for cid, want in expected.items()
            if _crosses(want, (j.get(cid) or {}).get("label"))]


def output_problems(case_map: dict, out: dict) -> list[str]:
    problems = [f"missing id {cid}" for cid in case_map if cid not in out]
    problems += [f"label {(out[cid] or {}).get('label')!r} for {cid}" for cid in case_map
                 if cid in out and (out[cid] or {}).get("label") not in LABELS]
    return problems


def length_labels(rows: list[dict]) -> dict[int, str]:
    words = {r["q"]: len(r["answer"].split()) for r in rows}
    cut = statistics.median(words.values())
    return {q: "new" if w >= cut else "already written" for q, w in words.items()}


def overlap_labels(rows: list[dict], retriever: Retriever) -> dict[int, str]:
    """Secondary reading, never gating: "new" iff the answer's largest word overlap (Jaccard) with
    the passages the judges were shown is below the median. Lexical overlap is the stand-in that
    passed G4 on D1b, so a Continue it also reaches cannot be told from it."""
    def overlap(r):
        a = set(_tokens(r["answer"]))
        shown = [set(_tokens(t)) for _, t in retriever.top(r["question"] + " " + r["answer"])]
        return max((len(a & s) / len(a | s) for s in shown if a | s), default=0.0)

    scores = {r["q"]: overlap(r) for r in rows}
    cut = statistics.median(scores.values())
    return {q: "new" if s < cut else "already written" for q, s in scores.items()}


def guess_accuracy(guesses: dict[int, str], arms: dict[int, str]) -> dict:
    n = len(guesses)
    k = sum(guesses[q] == arms[q] for q in guesses)
    p = sum(math.comb(n, i) for i in range(k, n + 1)) / 2 ** n
    return {"n": n, "correct": k, "accuracy": k / n, "p": p,
            "unblinded": k / n >= UNBLINDED_ACCURACY and p < 0.05}


def reveal(judged: list[dict], sealed: Path, private_key: Path, opened: Path,
           guesses: dict[int, str] | None = None, canary_failures: list[str] | None = None,
           overlap: dict[int, str] | None = None) -> dict:
    """A canary failure by either judge voids the reading (No reading, which counts as Change);
    the rule's figures are still reported."""
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
    if overlap is not None:
        res["overlap_only"] = rule.decide([{**r, "j1": overlap[r["q"]], "j2": overlap[r["q"]]} for r in rows])
    if guesses is not None:
        res["blinding"] = guess_accuracy(guesses, {q: it["arm"] for q, it in key.items()})
    if canary_failures:
        res["decision"], res["void"] = "No reading", list(canary_failures)
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
        doc = ingest(here, json.loads(Path(args.a).read_text()), json.loads(Path(args.b).read_text()),
                     raw={"judge_a": Path(args.a), "judge_b": Path(args.b)})
        print(json.dumps({"canary_failures": doc["canary_failures"], "judged": len(doc["judged"])}))
        return 1 if doc["canary_failures"] else 0
    else:
        doc = json.loads((here / "judgements.json").read_text())
        questions = parse_answers((here / "questions.md").read_text())
        overlap = overlap_labels([{**r, "question": questions[r["q"]]} for r in doc["judged"]],
                                 Retriever(passages(cb.corpus)))
        res = reveal(doc["judged"], here / "sealed", Path(args.private_key).expanduser(), here / "opened",
                     guesses=load_guesses(here), canary_failures=doc["canary_failures"], overlap=overlap)
        (here / "result.json").write_text(json.dumps(res, indent=1, sort_keys=True) + "\n")
        print(json.dumps({k: v for k, v in res.items() if k != "rows"}, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
