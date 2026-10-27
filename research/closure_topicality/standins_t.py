"""Stand-in closure judges for RT and the topicality-matched nulls (plan §1.6, §2.2).

`gapmap.standins` closes a whole arm and cites its first sentence, which says nothing about which
sentence a reader picked. RT scores whether the insert is cited, so these stand-ins cite sentences:
each per-sentence statistic cites every sentence at or above a cut (`ge`), at or below it (`le`),
the top-scoring sentences (`argmax`) or the bottom-scoring ones (`argmin`). All read only the
prompt `semantic.build_prompt` writes."""
from __future__ import annotations

import hashlib
import math
import re
import statistics
from typing import Callable

from gapmap import config, standins, text

FUNCTION_WORDS = frozenset("the of and to is in a an for on be are with by that it as or this was at from".split())
_QUOTED = re.compile(r"'([^']+)'")
MODES = ("ge", "le", "argmax", "argmin")

Stat = Callable[[standins.Parsed, str], float]


def context(p: standins.Parsed) -> frozenset[str]:
    return text.cw(p.seed + " " + p.question)


def probe_words(p: standins.Parsed) -> frozenset[str]:
    """The retriever's scoring words as far as the prompt shows them: DISC and DIAG quote their
    anchor or rival in the question, every other lens scores by the seed."""
    m = _QUOTED.search(p.question)
    return text.cw(m.group(1)) if m else text.cw(p.seed)


def _novel(p: standins.Parsed, s: str) -> int:
    return len(text.cw(s) - context(p))


def _novel_func(p: standins.Parsed, s: str) -> int:
    return _novel(p, s) if FUNCTION_WORDS & set(re.findall(r"[a-z]+", s.lower())) else -1


def _question_lexicon(p: standins.Parsed, s: str) -> int:
    names = [n for n, pat in config.PATTERNS.items() if pat.search(p.question)]
    return int(any(config.PATTERNS[n].search(s) for n in names))


STATS: dict[str, Stat] = {
    "length": lambda p, s: len(s),
    "overlap": lambda p, s: len(context(p) & text.cw(s)),
    "overlap_frac": lambda p, s: len(context(p) & text.cw(s)) / max(1, len(text.cw(s))),
    "probe": lambda p, s: len(probe_words(p) & text.cw(s)),
    "novel": _novel,
    "novel_func": _novel_func,
    "specificity": lambda p, s: len(standins._SPECIFIC.findall(s)),
    "closing_lexicon": lambda p, s: int(any(config.PATTERNS[n].search(s) for n in standins.CLOSING_LEXICONS)),
    "question_lexicon": _question_lexicon,
}


def idf_stat(prompts: list[str]) -> Stat:
    """Seed-and-question overlap weighted by idf over every sentence the check offers."""
    docs = [text.cw(s) for q in prompts for _i, s in standins.parse(q).sentences]
    n = len(docs)
    df: dict[str, int] = {}
    for d in docs:
        for w in d:
            df[w] = df.get(w, 0) + 1
    idf = {w: math.log((1 + n) / (1 + c)) + 1 for w, c in df.items()}
    return lambda p, s: sum(idf.get(w, 0.0) for w in context(p) & text.cw(s))


def all_stats(prompts: list[str]) -> dict[str, Stat]:
    return {**STATS, "idf_overlap": idf_stat(prompts)}


def _reply(ids: list[str]) -> dict:
    return {"states": [int(i) for i in ids], "partially": [], "reason": "stand-in"}


class CiteJudge:
    def __init__(self, name: str, stat: Stat, mode: str, *, cut: float):
        if mode not in MODES:
            raise ValueError(mode)
        self.model_id = f"cite-{name}-{mode}" + (f"@{cut:g}" if mode in ("ge", "le") else "")
        self.stat, self.mode, self.cut = stat, mode, cut

    def ask(self, prompt: str) -> dict:
        p = standins.parse(prompt)
        vals = [(i, self.stat(p, s)) for i, s in p.sentences]
        if not vals:
            return _reply([])
        if self.mode == "ge":
            ids = [i for i, v in vals if v >= self.cut]
        elif self.mode == "le":
            ids = [i for i, v in vals if v <= self.cut]
        else:
            target = (max if self.mode == "argmax" else min)(v for _i, v in vals)
            ids = [i for i, v in vals if v == target]
        return _reply(ids)


def _values(stat: Stat, prompts: list[str]) -> list[float]:
    out = []
    for q in prompts:
        p = standins.parse(q)
        out += [stat(p, s) for _i, s in p.sentences]
    return out


def calibrate(name: str, stat: Stat, mode: str, prompts: list[str]) -> CiteJudge:
    return CiteJudge(name, stat, mode, cut=statistics.median(_values(stat, prompts)))


def sweep_cuts(stat: Stat, prompts: list[str]) -> list[float]:
    return sorted(set(_values(stat, prompts)))


class CoinCiteJudge:
    def __init__(self, seed: int):
        self.model_id = f"cite-coin-{seed}"
        self.seed = seed

    def ask(self, prompt: str) -> dict:
        p = standins.parse(prompt)
        return _reply([i for i, s in p.sentences
                       if hashlib.sha256(f"{self.seed}\x1f{p.seed}\x1f{s}".encode()).digest()[0] % 2 == 0])


def arm_level(prompts: list[str]) -> list:
    """Arm-closing stand-ins: D1b's five plus the arm sum of every new statistic, cut at the median
    over the check's prompts."""
    out = [standins.calibrate("length", standins.length, prompts),
           standins.calibrate("overlap", standins.overlap, prompts),
           standins.calibrate("specificity", standins.specificity, prompts),
           standins.LexiconJudge(), standins.CoinFlipJudge()]
    for name, stat in all_stats(prompts).items():
        if name in ("length", "overlap", "specificity"):
            continue
        out.append(standins.calibrate(name, lambda p, f=stat: sum(f(p, s) for _i, s in p.sentences), prompts))
    return out
