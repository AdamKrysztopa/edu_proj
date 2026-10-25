"""Reachable gate readings from an observed baseline (L7.3 step 1; I5).

The registered decision functions live in `reconstruct` (E-PLANT, E-ABST), which this package
must not import, so each is passed in as `decide(**point) -> outcome`. The spaces enumerate every
count the unrun arm could still produce, given the counts already observed; they impose only
arithmetic constraints, so the reachable set is a superset of what the pipeline could produce.
"""
from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass, field

ORDER = ("continue", "change", "inconclusive", "stop")
"""Most to least favourable reading for the arm under test."""


def eplant_space(*, n_full: int, a_u_full: int, n_min: int = 1) -> Iterator[dict[str, int]]:
    """Every (n, a_u, a_g, b, c, e, r_g) left open once the ungated arm read a_u_full of n_full.

    n is the post-cap target count; the cap rule can drop any target, so the post-cap a_u runs
    from what the dropped targets cannot hold to what the kept ones can."""
    for n in range(n_min, n_full + 1):
        dropped = n_full - n
        for a_u in range(max(0, a_u_full - dropped), min(a_u_full, n) + 1):
            for b in range(a_u + 1):
                for c in range(n - a_u + 1):
                    a_g = a_u - b + c
                    for e in range(n + 1):
                        for r_g in range(n + 1):
                            yield {"n": n, "a_u": a_u, "a_g": a_g, "b": b, "c": c, "e": e, "r_g": r_g,
                                   "a_u_full": a_u_full, "n_full": n_full}


def eabst_space(*, n_items: int, raw_answered: int) -> Iterator[dict[str, float]]:
    """Every (n_included, f_r, f_p, κ side, zero-extraction count) left open once the raw arm
    answered raw_answered of n_items: only an answer can be false, so f_r ≤ raw answers kept."""
    for n_inc in range(n_items + 1):
        dropped = n_items - n_inc
        for f_r in range(min(raw_answered, n_inc) + 1):
            for f_p in range(n_inc + 1):
                for kappa in (0.0, 1.0):
                    for zero in range(n_items + 1):
                        yield {"n_included": n_inc, "f_r": f_r, "f_p": f_p, "kappa": kappa,
                               "zero_extraction_or_capped": zero,
                               "raw_answered_kept_max": min(raw_answered, n_inc),
                               "raw_answered_kept_min": max(0, raw_answered - dropped)}


@dataclass
class Regions:
    counts: dict[str, int] = field(default_factory=dict)
    examples: dict[str, dict] = field(default_factory=dict)

    @property
    def best(self) -> str:
        for outcome in ORDER:
            if self.counts.get(outcome):
                return outcome
        raise ValueError("no reading reached")


def regions(decide: Callable[..., str], space: Iterable[dict],
            keep: Callable[[str, dict], bool] | None = None) -> Regions:
    """Count each outcome over the space. `keep(outcome, point)` returns True to store the point
    as that outcome's example (the first point is stored by default)."""
    out = Regions()
    for point in space:
        outcome = decide(**point)
        out.counts[outcome] = out.counts.get(outcome, 0) + 1
        if outcome not in out.examples or (keep is not None and keep(outcome, point)):
            out.examples[outcome] = point
    return out


def collect(decide: Callable[..., str], space: Iterable[dict], outcome: str) -> list[dict]:
    """Every point of the space that reads `outcome`."""
    return [p for p in space if decide(**p) == outcome]
