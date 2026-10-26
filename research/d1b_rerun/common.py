"""Shared D1b helpers: the D1 ledgers, quote keys, the debris rule and D1's 15 used items. The
debris and overlap rules are applied alike to every candidate, before any closure state is joined."""
from __future__ import annotations

import glob
import json
import re
from pathlib import Path

from residual.ledger import Ledger

from gapmap import link

HERE = Path(__file__).resolve().parent
D1 = HERE.parent / "d1_demonstrator"
LEDGER_DIRS = {"cheap-26b": D1 / "runs" / "cheap-26b", "toptier-26b": D1 / "runs" / "toptier-26b"}
SIDECAR = "sidecar.json"
FRESH_JACCARD = 0.10
TOPIC_JACCARD = 0.5
_STOP = set("sources say prescribe should would what when which with that this from have been there "
            "their about where only must".split())


def ledger_path(name: str) -> Path:
    (path,) = glob.glob(str(LEDGER_DIRS[name] / "*" / "ledger.json"))
    return Path(path)


def load(name: str) -> tuple[Ledger, link.Index, str]:
    text_ = ledger_path(name).read_text()
    lg = Ledger.from_json(text_)
    return lg, link.build_index(lg), text_


def quote(question_text: str) -> str:
    m = re.search(r'"(.{20,}?)"', question_text)
    return m.group(1) if m else question_text


def tokens(s: str) -> frozenset[str]:
    return frozenset(w for w in re.findall(r"[a-z0-9_]+", s.lower()) if len(w) > 3 and w not in _STOP)


def jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    return len(a & b) / len(a | b) if a | b else 0.0


def debris(quoted: str) -> bool:
    """Conversion debris (D1's Q7, Q15): a flattened table row, or a long span with no sentence end."""
    q = quoted.strip()
    return "|" in q or (len(q.split()) > 12 and not re.search(r"[.!?:;)]$", q))


def d1_items() -> list[dict]:
    return json.loads((D1 / "key_revealed.json").read_text())["items"]


def d1_tokens() -> list[frozenset[str]]:
    return [tokens(it["anchor"] + " " + quote(it["text"])) for it in d1_items()]


def candidate_tokens(cand) -> frozenset[str]:
    return tokens(cand.anchor + " " + quote(cand.question_text))


def max_d1_jaccard(cand, d1: list[frozenset[str]]) -> tuple[float, int]:
    scores = [jaccard(candidate_tokens(cand), t) for t in d1]
    best = max(range(len(scores)), key=lambda i: scores[i])
    return scores[best], best
