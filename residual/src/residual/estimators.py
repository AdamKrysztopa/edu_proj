"""Unseen-item estimators for the known-truth check of §14.1, producing values that fit
`EstimatedResidual`. Kept out of residual.py, which is inside the frozen semantics hash.

Text estimators see only items some occasion caught, so they estimate the *written* universe:
an item with catchability 0 on every occasion leaves the frequency counts unchanged.
Lincoln-Petersen is the exception because its second occasion is the gold.

Every interval is Chao's (1987) log-normal interval on the unseen count f0, which keeps the
lower bound of the total at or above the observed count.
"""
from __future__ import annotations

import math
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from functools import partial
from typing import Literal

from residual.residual import EstimatedResidual

Name = Literal["chao1", "jackknife", "mh", "lincoln_petersen"]
Coverage = Literal["chao_jost", "lee_chao"]


class NotEstimable(ValueError):
    """The data carry no information for this estimator (no captures, or only singletons)."""


@dataclass(frozen=True, slots=True)
class Estimate:
    name: Name
    observed: int
    unseen: float
    se: float
    interval: tuple[float, float]
    """On the unseen count, not the total."""

    @property
    def total(self) -> float:
        return self.observed + self.unseen

    @property
    def total_interval(self) -> tuple[float, float]:
        return (self.observed + self.interval[0], self.observed + self.interval[1])


def frequency_counts(histories: Iterable[Sequence[bool]]) -> tuple[int, ...]:
    """(f_1, ..., f_t): items caught on exactly j of the t occasions. Never-caught rows vanish."""
    rows = [tuple(bool(x) for x in h) for h in histories]
    widths = {len(r) for r in rows}
    if len(widths) != 1:
        raise ValueError("every capture history needs the same number of occasions")
    (t,) = widths
    if t < 2:
        raise ValueError("capture-recapture needs at least two occasions")
    f = [0] * t
    for r in rows:
        if (j := sum(r)):
            f[j - 1] += 1
    return tuple(f)


def _lognormal(f0: float, var: float, z: float) -> tuple[float, float]:
    if f0 <= 0:
        return (0.0, 0.0)
    c = math.exp(z * math.sqrt(math.log1p(max(var, 0.0) / f0 ** 2)))
    return (f0 / c, f0 * c)


def _estimate(name: Name, observed: int, f0: float, var: float, z: float) -> Estimate:
    return Estimate(name, observed, f0, math.sqrt(max(var, 0.0)), _lognormal(f0, var, z))


def _observed(f: Sequence[int]) -> int:
    if any(x < 0 for x in f):
        raise ValueError("frequency counts are non-negative")
    if (s := sum(f)) == 0:
        raise NotEstimable("no item was caught")
    return s


def chao1(f: Sequence[int], z: float = 1.96, *, small_t: bool = True) -> Estimate:
    """Chao's (1987) Mh lower bound S + A·f1²/(2 f2) with its variance; the bias-corrected
    A·f1(f1-1)/2 when f2 = 0 (Chao 2005). A = (t-1)/t, the small-sample factor of EstimateS 9.1
    and iNEXT: without it the bound overstates f0 by t/(t-1) under homogeneity, a factor 2 at t = 2.
    `small_t=False` gives Chao's large-t form, A = 1."""
    s = _observed(f)
    t, f1, f2 = len(f), f[0], f[1]
    a = (t - 1) / t if small_t else 1.0
    if f2 > 0:
        r = f1 / f2
        var = f2 * (a * r ** 2 / 2 + a ** 2 * r ** 3 + a ** 2 * r ** 4 / 4)
        return _estimate("chao1", s, a * f1 ** 2 / (2 * f2), var, z)
    f0 = a * f1 * (f1 - 1) / 2
    var = (f0 + a ** 2 * f1 * (2 * f1 - 1) ** 2 / 4 - a ** 2 * f1 ** 4 / (4 * (s + f0))) if f0 else 0.0
    return _estimate("chao1", s, f0, var, z)


def jackknife1(f: Sequence[int], z: float = 1.96) -> Estimate:
    """First-order jackknife of Burnham & Overton (1978): S + (t-1)/t · f1, variance f1·a1·(a1-1)."""
    s = _observed(f)
    t, f1 = len(f), f[0]
    a1 = (2 * t - 1) / t
    return _estimate("jackknife", s, (t - 1) / t * f1, f1 * a1 * (a1 - 1), z)


def _coverage(f: Sequence[float], kind: Coverage) -> float:
    n = sum(k * fk for k, fk in enumerate(f, 1))
    if kind == "lee_chao" or f[0] == 0:
        return 1 - f[0] / n
    t, f1, f2 = len(f), f[0], f[1]
    f0 = (t - 1) / t * (f1 ** 2 / (2 * f2) if f2 > 0 else f1 * (f1 - 1) / 2)
    return 1 - f1 / n * (t * f0 / (t * f0 + f1))


def _mh_total(f: Sequence[float], kind: Coverage) -> float:
    t = len(f)
    s = sum(f)
    n = sum(k * fk for k, fk in enumerate(f, 1))
    coverage = _coverage(f, kind)
    if coverage <= 0:
        raise NotEstimable("sample coverage is zero")
    pairs = sum(k * (k - 1) * fk for k, fk in enumerate(f, 1))
    gamma2 = max(s / coverage * t / (t - 1) * pairs / n ** 2 - 1, 0.0)
    return s / coverage + f[0] / coverage * gamma2


def _delta_var(total: Callable[[Sequence[float]], float], f: Sequence[int], n_hat: float) -> float:
    """Delta method under the multinomial on f with N̂ cells, as Chao (1987) does; numerical
    gradient."""
    grad = []
    for i, fi in enumerate(f):
        h = max(1e-4, 1e-6 * fi)
        up = [float(x) for x in f]
        dn = list(up)
        up[i] += h
        dn[i] = max(fi - h, 0.0)
        try:
            grad.append((total(up) - total(dn)) / (up[i] - dn[i]))
        except NotEstimable:
            grad.append((total(up) - n_hat) / h)
    return sum(gi * gj * (fi * (1 - fi / n_hat) if i == j else -fi * fj / n_hat)
               for i, (gi, fi) in enumerate(zip(grad, f))
               for j, (gj, fj) in enumerate(zip(grad, f)))


def mh_coverage(f: Sequence[int], z: float = 1.96, *, coverage: Coverage = "chao_jost") -> Estimate:
    """Lee & Chao (1994) sample-coverage estimator for model Mh, N = S/C + (f1/C)·γ², with γ² the
    estimated squared CV of catchability; delta-method variance. `coverage="chao_jost"` estimates C
    as Chao & Jost (2012) do for incidence data; Lee & Chao's 1 - f1/n targets 1 - q^(t-1), not
    1 - q^t, so it overstates N when t is small."""
    s = _observed(f)
    total = partial(_mh_total, kind=coverage)
    n_hat = total(f)
    return _estimate("mh", s, n_hat - s, _delta_var(total, f, n_hat), z)


def chapman(n1: int, n2: int, m: int, z: float = 1.96) -> Estimate:
    """Lincoln-Petersen with Chapman's correction, (n1+1)(n2+1)/(m+1) - 1, and Seber's variance.
    `observed` is n1, so `unseen` is the items occasion 1 missed: with the text union as occasion 1
    and the gold as occasion 2, that is the gold-referenced count of items no text occasion caught."""
    if not 0 <= m <= min(n1, n2):
        raise ValueError("the overlap cannot exceed either occasion")
    total = (n1 + 1) * (n2 + 1) / (m + 1) - 1
    var = (n1 + 1) * (n2 + 1) * (n1 - m) * (n2 - m) / ((m + 1) ** 2 * (m + 2))
    return _estimate("lincoln_petersen", n1, max(total - n1, 0.0), var, z)


def to_record(est: Estimate, occasions: Sequence[str], gold_uncaptured: int | None = None,
              tau: float | None = None) -> EstimatedResidual:
    """`tau` is relative: the record's tolerance is tau · gold_uncaptured."""
    if (gold_uncaptured is None) != (tau is None):
        raise ValueError("a known-truth check needs both the gold count and its tolerance")
    return EstimatedResidual(
        estimator=est.name, occasions=tuple(occasions), estimate=est.unseen, interval=est.interval,
        gold_uncaptured=gold_uncaptured,
        tolerance=None if tau is None else tau * gold_uncaptured)
