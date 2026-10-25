"""D1 step 6: blind novelty check. Each answer is compared, without its arm, with the corpus
passages most similar to its question and answer, by two judges of different families (ADR 0009).
Canaries run first: length-matched filler and a copied passage must not be judged "new".

  uv run --directory reconstruct python ../research/d1_demonstrator/judge.py lock
  uv run --directory reconstruct python ../research/d1_demonstrator/judge.py judge --max-usd 1.0
  uv run --directory reconstruct python ../research/d1_demonstrator/judge.py reveal
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import os
import re
import sys
from collections import Counter
from pathlib import Path

from reconstruct.llm import Budget, BudgetExceeded, CallLog, LLMRefused, LLMUnavailable, load_models

HERE = Path(__file__).parent
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

SCHEMA = {"type": "object", "properties": {
    "label": {"type": "string", "enum": LABELS},
    "new_content": {"type": "string"},
    "reason": {"type": "string"}},
    "required": ["label", "new_content", "reason"], "additionalProperties": False}


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def parse_answers(text: str) -> dict[int, str]:
    out: dict[int, str] = {}
    for m in re.finditer(r"^## Q(\d+)\s*\n(.*?)(?=^## Q\d+|\Z)", text, flags=re.M | re.S):
        out[int(m.group(1))] = m.group(2).strip()
    return out


def passages() -> list[tuple[str, str]]:
    manifest = json.loads((HERE / "corpus" / "manifest.json").read_text())
    out = []
    for doc in manifest["documents"]:
        raw = (HERE / "corpus" / doc["file"]).read_text()
        for block in re.findall(r"<(?:p|pre|h\d)>(.*?)</(?:p|pre|h\d)>", raw, flags=re.S):
            text = html.unescape(re.sub(r"<[^>]+>", " ", block)).strip()
            if len(text.split()) >= 6:
                out.append((doc["title"], text))
    return out


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z][a-z0-9_]+", text.lower())


class Retriever:
    def __init__(self, items: list[tuple[str, str]]):
        self.items = items
        self.docs = [Counter(_tokens(t)) for _, t in items]
        df = Counter(w for d in self.docs for w in d)
        self.idf = {w: math.log(len(self.docs) / n) for w, n in df.items()}
        self.norms = [math.sqrt(sum((c * self.idf[w]) ** 2 for w, c in d.items())) or 1.0 for d in self.docs]

    def top(self, query: str, k: int = TOP_K) -> list[tuple[str, str]]:
        q = Counter(_tokens(query))
        qv = {w: c * self.idf.get(w, 0.0) for w, c in q.items()}
        qn = math.sqrt(sum(v * v for v in qv.values())) or 1.0
        scores = [(sum(qv.get(w, 0.0) * c * self.idf[w] for w, c in d.items()) / (n * qn), i)
                  for i, (d, n) in enumerate(zip(self.docs, self.norms))]
        return [self.items[i] for _, i in sorted(scores, reverse=True)[:k]]


def _user(question: str, answer: str, ctx: list[tuple[str, str]]) -> str:
    shown = "\n\n".join(f"[{i}] ({title}) {text[:1200]}" for i, (title, text) in enumerate(ctx, 1))
    return f"QUESTION\n{question}\n\nEXPERT ANSWER\n{answer}\n\nPASSAGES\n{shown}"


def canaries(items: list[dict], retriever: Retriever) -> list[dict]:
    """Filler matched to the mean answer length, and a passage copied verbatim as an answer."""
    q = items[0]["text"]
    filler_words = ("This is an important point and it depends on the situation, so one should "
                    "think about it carefully and consider the context before deciding what to do. ").split()
    out = []
    for n in (40, 90):
        out.append({"q": f"canary-filler-{n}", "question": q,
                    "answer": " ".join((filler_words * 10)[:n]), "must_not_be": "new"})
    copied = retriever.top(q, 1)[0][1]
    out.append({"q": "canary-copied", "question": q, "answer": copied, "must_not_be": "new"})
    return out


def cmd_lock(_: argparse.Namespace) -> int:
    answers = parse_answers((HERE / "answers.md").read_text())
    key_items = json.loads((HERE / "sealed" / "key.json").read_text())["items"]
    missing = [it["q"] for it in key_items if not answers.get(it["q"])]
    if missing:
        raise SystemExit(f"answers missing for Q{missing}")
    lock = {"answers_sha256": _sha(HERE / "answers.md"), "questions_sha256": _sha(HERE / "questions.md")}
    (HERE / "answers.lock.json").write_text(json.dumps(lock, indent=1) + "\n")
    print(json.dumps(lock))
    return 0


def cmd_judge(args: argparse.Namespace) -> int:
    lock = json.loads((HERE / "answers.lock.json").read_text())
    if _sha(HERE / "answers.md") != lock["answers_sha256"]:
        raise SystemExit("answers.md changed after locking")
    answers = parse_answers((HERE / "answers.md").read_text())
    questions = {it["q"]: it["text"] for it in json.loads((HERE / "sealed" / "key.json").read_text())["items"]}
    retriever = Retriever(passages())
    log = CallLog(HERE / "judge_calls.jsonl", budget=Budget(max_usd=args.max_usd))
    judges = load_models(HERE / "models_judges.json", log=log, env=os.environ)
    cases = canaries([{"text": t} for t in questions.values()], retriever) + [
        {"q": q, "question": questions[q], "answer": answers[q]} for q in sorted(questions)]
    out = []
    try:
        for case in cases:
            ctx = retriever.top(case["question"] + " " + case["answer"])
            row = {**case, "passages": [t for t, _ in ctx]}
            for role in ("judge_a", "judge_b"):
                try:
                    row[role] = judges[role].json("novelty", system=SYSTEM,
                                                  user=_user(case["question"], case["answer"], ctx), schema=SCHEMA)
                except (LLMUnavailable, LLMRefused) as e:
                    row[role] = {"label": None, "error": repr(e)}
            out.append(row)
    except BudgetExceeded as e:
        print(f"stopped: {e}", file=sys.stderr)
    (HERE / "judgements.json").write_text(json.dumps(out, indent=1) + "\n")
    bad = [r["q"] for r in out if str(r["q"]).startswith("canary")
           and "new" in (r["judge_a"].get("label"), r["judge_b"].get("label"))]
    print(json.dumps({"judged": len(out), "cost": round(log.total_cost, 4), "canary_failures": bad}))
    return 1 if bad else 0


def cmd_reveal(_: argparse.Namespace) -> int:
    sys.path.insert(0, str(HERE))
    from rule import decide

    key = {it["q"]: it for it in json.loads((HERE / "sealed" / "key.json").read_text())["items"]}
    judged = [r for r in json.loads((HERE / "judgements.json").read_text()) if isinstance(r["q"], int)]
    rows = [{"q": r["q"], "arm": key[r["q"]]["arm"], "j1": r["judge_a"].get("label"),
             "j2": r["judge_b"].get("label")} for r in judged]
    result = {**decide(rows), "rows": rows}
    (HERE / "result.json").write_text(json.dumps(result, indent=1) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "rows"}, indent=1))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("lock")
    j = sub.add_parser("judge")
    j.add_argument("--max-usd", type=float, required=True)
    sub.add_parser("reveal")
    args = ap.parse_args()
    return {"lock": cmd_lock, "judge": cmd_judge, "reveal": cmd_reveal}[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
