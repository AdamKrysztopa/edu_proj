"""Trivial stand-in closure judges (L7.3). Each answers the closure prompt `semantic.build_prompt`
writes from a surface statistic of its sentences -- length, topical overlap with the seed and
question, specificity, source count, a closing-lexicon hit, or a coin -- so a check one of them
passes is shown not to need a reader of the element. All are `Judge`s, network-free, and of the
"other" vendor family."""
from __future__ import annotations

import hashlib
import re
import statistics
from dataclasses import dataclass
from typing import Callable

from gapmap import config, text

_LINE = re.compile(r"^(\d+): (.*)$")
_SPECIFIC = re.compile(r"\d+(?:\.\d+)?|\b(?:if|when|whenever|unless)\b|`[^`]+`|\b\w+_\w+\b", re.IGNORECASE)
CLOSING_LEXICONS = ("RAT", "EXC", "COND", "DETECT", "INTERP", "QUANT")
"""Every lexicon a lens's lexical closure test reads (`lenses._lexical_state` call sites)."""


@dataclass(frozen=True)
class Parsed:
    seed: str
    question: str
    sentences: tuple[tuple[str, str], ...]


def parse(prompt: str) -> Parsed:
    lines = prompt.splitlines()
    seed = lines[0].removeprefix('Seed assertion: "').removesuffix('"')
    question = lines[1].removeprefix("Question: ")
    sents = tuple((m.group(1), m.group(2)) for m in map(_LINE.match, lines) if m)
    return Parsed(seed=seed, question=question, sentences=sents)


Score = Callable[[Parsed], float]


def length(p: Parsed) -> float:
    return sum(len(s) for _i, s in p.sentences)


def overlap(p: Parsed) -> float:
    context = text.cw(p.seed + " " + p.question)
    return sum(len(context & text.cw(s)) for _i, s in p.sentences)


def specificity(p: Parsed) -> float:
    return sum(len(_SPECIFIC.findall(s)) for _i, s in p.sentences)


def source_count(source_of: dict[str, str]) -> Score:
    """Distinct sources among the offered sentences; the prompt carries no sources, so the caller
    supplies sentence text -> source."""
    return lambda p: len({source_of.get(s, s) for _i, s in p.sentences})


def _closed(p: Parsed) -> dict:
    return {"states": [p.sentences[0][0]] if p.sentences else [], "partially": [], "reason": "stand-in"}


_OPEN = {"states": [], "partially": [], "reason": "stand-in"}


class ScoreJudge:
    def __init__(self, name: str, score: Score, *, cut: float):
        self.model_id = f"standin-{name}"
        self.score = score
        self.cut = cut

    def ask(self, prompt: str) -> dict:
        p = parse(prompt)
        return _closed(p) if self.score(p) >= self.cut else _OPEN


def calibrate(name: str, score: Score, prompts: list[str]) -> ScoreJudge:
    """The cut is the median score over the prompts the check will ask, as `control2.length_stand_in`."""
    return ScoreJudge(name, score, cut=statistics.median(score(parse(q)) for q in prompts))


class LexiconJudge:
    """Closed iff any offered sentence matches a closing lexicon: the old lexical closure test
    without its seed-stem overlap condition."""

    model_id = "standin-lexicon"

    def ask(self, prompt: str) -> dict:
        p = parse(prompt)
        hit = any(config.PATTERNS[name].search(s) for _i, s in p.sentences for name in CLOSING_LEXICONS)
        return _closed(p) if hit else _OPEN


class CoinFlipJudge:
    def __init__(self, seed: int = 0):
        self.model_id = f"standin-coin-{seed}"
        self.seed = seed

    def ask(self, prompt: str) -> dict:
        heads = hashlib.sha256(f"{self.seed}\x1f{prompt}".encode()).digest()[0] % 2 == 0
        return _closed(parse(prompt)) if heads else _OPEN


class RecordingJudge:
    """Answers open and keeps every prompt, for a first pass that collects what a check will ask."""

    model_id = "standin-recorder"

    def __init__(self):
        self.prompts: list[str] = []

    def ask(self, prompt: str) -> dict:
        self.prompts.append(prompt)
        return _OPEN
