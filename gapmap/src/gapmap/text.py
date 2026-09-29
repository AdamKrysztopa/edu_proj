"""Tokenise, stem and split sentences (spec §1.2, §1.3). Hand-written: `gapmap` imports only
stdlib, pydantic and `residual`."""
from __future__ import annotations

import re
from urllib.parse import urlparse

from residual.claims import ClaimRecord

from gapmap.config import IRREGULAR_STEMS, STOP

_TOKEN = re.compile(r"[a-z][a-z0-9]+")
_SENT_SPLIT = re.compile(r"(?<=[.;])\s")
_SUFFIXES = (("ies", "y"), ("ing", ""), ("ed", ""), ("es", ""), ("s", ""))


def tokens(s: str) -> list[str]:
    return [t for t in _TOKEN.findall(s.lower()) if len(t) > 2 and t not in STOP]


def stem(t: str) -> str:
    """§1.3: strip the first listed suffix that leaves at least 4 characters; a word ending in
    `ss` is never stripped (it would otherwise mangle e.g. "process"). S3 defect 4:
    `config.IRREGULAR_STEMS` is checked first (folds "failure"/"failures" to "fail")."""
    if t in IRREGULAR_STEMS:
        return IRREGULAR_STEMS[t]
    if t.endswith("ss"):
        return t
    for suf, repl in _SUFFIXES:
        if t.endswith(suf):
            candidate = t[: -len(suf)] + repl
            if len(candidate) >= 4:
                return candidate
    return t


def cw(s: str) -> frozenset[str]:
    return frozenset(stem(t) for t in tokens(s))


def sentences(s: str) -> list[str]:
    return [p for p in _SENT_SPLIT.split(s) if p.strip()]


def sentence_containing(s: str, pos: int) -> str:
    """Fix 4 (DIAG anchor): the sentence (per `sentences`) whose span in `s` contains character
    index `pos`, or the last sentence if `pos` falls at/after the end (e.g. a trailing marker with
    no more text). Used to anchor on a whole sentence rather than a mid-sentence split fragment."""
    cursor = 0
    last = s
    for sent in sentences(s):
        start = s.find(sent, cursor)
        if start == -1:
            start = cursor
        end = start + len(sent)
        if start <= pos < end:
            return sent
        cursor = end
        last = sent
    return last


def trim(s: str, limit: int = 80) -> str:
    """Trim to at most `limit` characters at a word boundary, verbatim otherwise (used for
    display text quoted straight out of a claim, e.g. DIAG's effect/cause phrases)."""
    s = s.strip()
    if len(s) <= limit:
        return s
    cut = s.rfind(" ", 0, limit + 1)
    if cut <= 0:
        cut = limit
    return s[:cut].rstrip(" ,;")


def domain(identifier: str) -> str:
    """The bare domain of a source identifier (S3 defect 1's PROMO_DOMAINS check): `www.` is
    stripped, and a non-URL identifier (e.g. a DOI) yields ``""``, which matches no domain."""
    net = urlparse(identifier).netloc.lower()
    return net[4:] if net.startswith("www.") else net


def T(c: ClaimRecord) -> str:
    """§1.2: the closure-scope text — the assertion plus every verbatim evidence span. Lenses
    fire on `c.assertion` alone; only closure tests use `T`."""
    spans = [e.selector.exact for e in c.evidence if e.selector.exact]
    return c.assertion + " " + " ".join(spans) if spans else c.assertion
