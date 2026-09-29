"""Linking and breadth (spec §1.4): the neighbourhood graph over the A pool, and the
independence-key breadth that drives the confidence rubric (§5)."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from residual.ledger import Ledger
from residual.vocab import CRITERION_LABELS, EpistemicLabel

from gapmap import config, text


@dataclass(frozen=True)
class LinkParams:
    common_cut: float
    shared_threshold: int


SETTING_1 = LinkParams(config.DEFAULT_COMMON_STEM_CUT, config.DEFAULT_SHARED_STEM_THRESHOLD)
SETTINGS = tuple(LinkParams(cut, thr)
                 for cut in config.COMMON_STEM_CUTS for thr in config.SHARED_STEM_THRESHOLDS)
"""The 4 robustness settings (spec §1.4); SETTINGS[0] == SETTING_1."""


@dataclass(frozen=True)
class Index:
    """Built once per ledger; independent of the link parameters."""

    ledger: Ledger
    a_ids: tuple[str, ...]
    s_ids: tuple[str, ...]
    u_ids: tuple[str, ...]
    assertion_cw: dict[str, frozenset[str]]
    T: dict[str, str]


def build_index(ledger: Ledger) -> Index:
    a_ids, s_ids, u_ids = [], [], []
    assertion_cw: dict[str, frozenset[str]] = {}
    t: dict[str, str] = {}
    for c in ledger.claims:
        lab = ledger.label(c.claim_id)
        if lab in CRITERION_LABELS:
            a_ids.append(c.claim_id)
        elif lab is EpistemicLabel.SYNTHETIC_EXTRAPOLATION:
            s_ids.append(c.claim_id)
        elif lab is EpistemicLabel.UNKNOWN:
            u_ids.append(c.claim_id)
        assertion_cw[c.claim_id] = text.cw(c.assertion)
        t[c.claim_id] = text.T(c)
    return Index(ledger=ledger, a_ids=tuple(a_ids), s_ids=tuple(s_ids), u_ids=tuple(u_ids),
                assertion_cw=assertion_cw, T=t)


def common_stems(index: Index, cut: float) -> frozenset[str]:
    """Stems in more than `cut` of the A pool's assertions (§1.3)."""
    counts: Counter[str] = Counter()
    for cid in index.a_ids:
        counts.update(index.assertion_cw[cid])
    n = len(index.a_ids)
    return frozenset(s for s, c in counts.items() if n and c > cut * n)


def neighbourhood(index: Index, seed_id: str, common: frozenset[str], threshold: int) -> frozenset[str]:
    """The A claims `d != seed` with `|cw(seed) ∩ cw(d) \\ common| >= threshold` (§1.4)."""
    cw_seed = index.assertion_cw[seed_id] - common
    if not cw_seed:
        return frozenset()
    out = set()
    for d in index.a_ids:
        if d == seed_id:
            continue
        cw_d = index.assertion_cw[d] - common
        if len(cw_seed & cw_d) >= threshold:
            out.add(d)
    return frozenset(out)


def explicit_part(index: Index, seeds: frozenset[str], common: frozenset[str],
                  threshold: int) -> frozenset[str]:
    """X: the seeds plus their neighbourhoods, A only (§1.4)."""
    x = set(seeds)
    for s in seeds:
        x |= neighbourhood(index, s, common, threshold)
    return frozenset(x)


def jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def breadth(ledger: Ledger, claim_ids: frozenset[str]) -> frozenset[str]:
    """Distinct independence keys over the supporting evidence of the given claims (§1.4)."""
    keys: set[str] = set()
    for cid in claim_ids:
        c = ledger.by_id[cid]
        keys.update(e.source.independence_key for e in c.supporting)
    return frozenset(keys)
