"""AUROC, the paired ΔAUROC and its pooling across golds (REORIENTATION.md §14.3; I5).

Labels are booleans, True for the positive class (an area the reconstruction missed); a higher
score means "more likely missed". Ties count one half throughout. Stdlib only.

- DeLong, DeLong & Clarke-Pearson (1988) covariance of correlated AUROCs from placement values;
  with `clusters`, the clustered form of Obuchowski (1997), which is identical to DeLong when
  every area is its own cluster.
- Common-effect pooling over golds as fixed strata: the stratified Mann–Whitney, each gold
  weighted by n1·n0, so pairs are formed only inside a gold (DS3 §3).
- Random-effects pooling (DerSimonian–Laird τ², modified Knapp–Hartung) as a sensitivity only.
- A cluster bootstrap that resamples whole clusters inside each gold.
"""
from __future__ import annotations

import functools
import math
import random
from collections.abc import Hashable, Mapping, Sequence
from dataclasses import dataclass


def midranks(values: Sequence[float]) -> list[float]:
    order = sorted(range(len(values)), key=values.__getitem__)
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = r
        i = j + 1
    return ranks


def _split(labels: Sequence[bool]) -> tuple[list[int], list[int]]:
    pos = [i for i, y in enumerate(labels) if y]
    neg = [i for i, y in enumerate(labels) if not y]
    if not pos or not neg:
        raise ValueError("AUROC needs at least one positive and one negative")
    return pos, neg


def auroc(scores: Sequence[float], labels: Sequence[bool]) -> float:
    if len(scores) != len(labels):
        raise ValueError("scores and labels differ in length")
    pos, neg = _split(labels)
    ranks = midranks(scores)
    n1, n0 = len(pos), len(neg)
    return (sum(ranks[i] for i in pos) - n1 * (n1 + 1) / 2) / (n1 * n0)


@dataclass(frozen=True)
class Placements:
    """θ, then each positive's share of negatives it outranks (V10) and each negative's share of
    positives that outrank it (V01), in label order."""
    theta: float
    v10: tuple[float, ...]
    v01: tuple[float, ...]


def placements(scores: Sequence[float], labels: Sequence[bool]) -> Placements:
    pos, neg = _split(labels)
    n1, n0 = len(pos), len(neg)
    r_all = midranks(scores)
    r_pos = midranks([scores[i] for i in pos])
    r_neg = midranks([scores[i] for i in neg])
    v10 = tuple((r_all[i] - r_pos[k]) / n0 for k, i in enumerate(pos))
    v01 = tuple(1.0 - (r_all[i] - r_neg[k]) / n1 for k, i in enumerate(neg))
    return Placements(theta=sum(v10) / n1, v10=v10, v01=v01)


def auroc_covariance(score_sets: Sequence[Sequence[float]], labels: Sequence[bool],
                     clusters: Sequence[Hashable] | None = None) -> tuple[list[float], list[list[float]]]:
    """AUROCs of several scores on the same areas and their covariance matrix.

    Clustered (Obuchowski 1997): with V10_i and V01_i the placement sums of cluster i and m_i, n_i
    its positive and negative counts,
        S10 = I1/((I1-1) N1) Σ (V10_i - m_i θ)(V10_i - m_i θ'),  S01 likewise with I0, N0,
        S11 = I/(I-1) Σ (V10_i - m_i θ)(V01_i - n_i θ'),
        cov = S10/N1 + S01/N0 + (S11 + S11ᵀ)/(N1 N0),
    where I1, I0 count the clusters holding a positive, a negative. Singleton clusters give DeLong,
    and so does a gold whose positives or negatives all sit in one cluster (I1 or I0 below 2).
    """
    pos, neg = _split(labels)
    n1, n0 = len(pos), len(neg)
    clustered = clusters is not None
    if clusters is None:
        clusters = list(range(len(labels)))
    plc =[placements(s, labels) for s in score_sets]
    ids = list(dict.fromkeys(clusters))
    index = {c: k for k, c in enumerate(ids)}
    m = [0] * len(ids)
    nn = [0] * len(ids)
    for i in pos:
        m[index[clusters[i]]] += 1
    for i in neg:
        nn[index[clusters[i]]] += 1
    dev10, dev01 = [], []
    for p in plc:
        s10 = [0.0] * len(ids)
        s01 = [0.0] * len(ids)
        for k, i in enumerate(pos):
            s10[index[clusters[i]]] += p.v10[k]
        for k, i in enumerate(neg):
            s01[index[clusters[i]]] += p.v01[k]
        dev10.append([s10[c] - m[c] * p.theta for c in range(len(ids))])
        dev01.append([s01[c] - nn[c] * p.theta for c in range(len(ids))])
    i1 = sum(1 for x in m if x)
    i0 = sum(1 for x in nn if x)
    if clustered and (i1 < 2 or i0 < 2):
        # a class held by one cluster leaves its variance component inestimable from clusters
        return auroc_covariance(score_sets, labels, None)
    i_all = len(ids)
    f10 = i1 / ((i1 - 1) * n1) if i1 > 1 else 0.0
    f01 = i0 / ((i0 - 1) * n0) if i0 > 1 else 0.0
    f11 = i_all / (i_all - 1) if i_all > 1 else 0.0
    k = len(score_sets)
    cov = [[0.0] * k for _ in range(k)]
    for a in range(k):
        for b in range(a, k):
            s10 = f10 * sum(x * y for x, y in zip(dev10[a], dev10[b]))
            s01 = f01 * sum(x * y for x, y in zip(dev01[a], dev01[b]))
            s11 = f11 * sum(x * y for x, y in zip(dev10[a], dev01[b]))
            s11t = f11 * sum(x * y for x, y in zip(dev10[b], dev01[a]))
            v = s10 / n1 + s01 / n0 + (s11 + s11t) / (n1 * n0)
            cov[a][b] = cov[b][a] = v
    return [p.theta for p in plc], cov


@dataclass(frozen=True)
class Estimate:
    """A ΔAUROC (or AUROC) with its standard error; `weight` is n1·n0 of the gold(s) behind it."""
    delta: float
    se: float
    weight: float = 1.0


def paired_delta(a: Sequence[float], b: Sequence[float], labels: Sequence[bool],
                 clusters: Sequence[Hashable] | None = None) -> Estimate:
    """AUROC(a) − AUROC(b) on the same areas, with its DeLong (or clustered) standard error."""
    thetas, cov = auroc_covariance([a, b], labels, clusters)
    var = cov[0][0] + cov[1][1] - 2 * cov[0][1]
    n1 = sum(1 for y in labels if y)
    return Estimate(delta=thetas[0] - thetas[1], se=math.sqrt(max(var, 0.0)),
                    weight=n1 * (len(labels) - n1))


def pool_common(estimates: Sequence[Estimate]) -> Estimate:
    """Common effect over golds as fixed strata, weighted by n1·n0 (DS3 §3)."""
    if len(estimates) == 1:
        return estimates[0]
    w = sum(e.weight for e in estimates)
    delta = sum(e.weight * e.delta for e in estimates) / w
    se = math.sqrt(sum((e.weight * e.se) ** 2 for e in estimates)) / w
    return Estimate(delta=delta, se=se, weight=w)


@dataclass(frozen=True)
class RandomEffects:
    delta: float
    se: float
    tau2: float
    df: int

    def lower(self, alpha: float) -> float:
        return self.delta - t_ppf(1 - alpha, self.df) * self.se

    def upper(self, alpha: float) -> float:
        return self.delta + t_ppf(1 - alpha, self.df) * self.se


def pool_random(estimates: Sequence[Estimate]) -> RandomEffects:
    """DerSimonian–Laird τ² with the modified Knapp–Hartung variance (Röver, Knapp & Friede 2015):
    a sensitivity analysis, never the gate."""
    k = len(estimates)
    if k < 2:
        raise ValueError("random effects need at least two golds")
    floor = 1e-12
    w = [1 / max(e.se ** 2, floor) for e in estimates]
    sw = sum(w)
    fe = sum(wi * e.delta for wi, e in zip(w, estimates)) / sw
    q = sum(wi * (e.delta - fe) ** 2 for wi, e in zip(w, estimates))
    tau2 = max(0.0, (q - (k - 1)) / (sw - sum(wi * wi for wi in w) / sw))
    ws = [1 / max(e.se ** 2 + tau2, floor) for e in estimates]
    sws = sum(ws)
    mu = sum(wi * e.delta for wi, e in zip(ws, estimates)) / sws
    qhk = sum(wi * (e.delta - mu) ** 2 for wi, e in zip(ws, estimates)) / (k - 1)
    return RandomEffects(delta=mu, se=math.sqrt(max(1.0, qhk) / sws), tau2=tau2, df=k - 1)


# --- Student t, for the Knapp–Hartung bound -------------------------------------------------------


def _betacf(a: float, b: float, x: float) -> float:
    tiny, eps = 1e-300, 3e-16
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / (d if abs(d) > tiny else tiny)
    h = d
    for m in range(1, 400):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d
        d = 1 / (d if abs(d) > tiny else tiny)
        c = 1 + aa / c if abs(1 + aa / c) > tiny else tiny
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d
        d = 1 / (d if abs(d) > tiny else tiny)
        c = 1 + aa / c if abs(1 + aa / c) > tiny else tiny
        delta = d * c
        h *= delta
        if abs(delta - 1) < eps:
            break
    return h


def _betainc(a: float, b: float, x: float) -> float:
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    front = math.exp(lbeta + a * math.log(x) + b * math.log1p(-x))
    if x < (a + 1) / (a + b + 2):
        return front * _betacf(a, b, x) / a
    return 1 - front * _betacf(b, a, 1 - x) / b


def t_cdf(x: float, df: float) -> float:
    tail = 0.5 * _betainc(df / 2, 0.5, df / (df + x * x))
    return 1 - tail if x >= 0 else tail


@functools.lru_cache(maxsize=4096)
def t_ppf(p: float, df: float) -> float:
    if not 0 < p < 1:
        raise ValueError("p must lie in (0, 1)")
    lo, hi = -1e3, 1e3
    for _ in range(200):
        mid = (lo + hi) / 2
        if t_cdf(mid, df) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# --- cluster bootstrap ----------------------------------------------------------------------------


def cluster_resample(labels: Sequence[bool], clusters: Sequence[Hashable],
                     rng: random.Random, max_tries: int = 1000) -> list[int]:
    """Indices of one resample of one gold: whole clusters drawn with replacement, separately among
    all-positive, all-negative and mixed clusters, so singleton clusters give a class-stratified
    bootstrap. A draw left without both classes is redrawn."""
    members: dict[Hashable, list[int]] = {}
    for i, c in enumerate(clusters):
        members.setdefault(c, []).append(i)
    groups: dict[str, list[list[int]]] = {"pos": [], "neg": [], "mixed": []}
    for idx in members.values():
        kinds = {labels[i] for i in idx}
        groups["mixed" if len(kinds) == 2 else "pos" if True in kinds else "neg"].append(idx)
    for _ in range(max_tries):
        out: list[int] = []
        for g in groups.values():
            for _ in range(len(g)):
                out.extend(g[rng.randrange(len(g))])
        n_pos = sum(1 for i in out if labels[i])
        if 0 < n_pos < len(out):
            return out
    raise ValueError("could not draw a resample holding both classes")


@dataclass(frozen=True)
class GoldData:
    labels: Sequence[bool]
    clusters: Sequence[Hashable]
    scores: Mapping[str, Sequence[float]]


def pooled_deltas(golds: Sequence[GoldData], target: str, others: Sequence[str],
                  index_sets: Sequence[Sequence[int]] | None = None) -> dict[str, float]:
    """Common-effect ΔAUROC(target − other) for each other score, on the given resample."""
    num = {o: 0.0 for o in others}
    wsum = 0.0
    for g, gold in enumerate(golds):
        idx = index_sets[g] if index_sets is not None else range(len(gold.labels))
        labels = [gold.labels[i] for i in idx]
        n1 = sum(labels)
        w = n1 * (len(labels) - n1)
        a = auroc([gold.scores[target][i] for i in idx], labels)
        for o in others:
            num[o] += w * (a - auroc([gold.scores[o][i] for i in idx], labels))
        wsum += w
    return {o: num[o] / wsum for o in others}


def bootstrap_pooled_deltas(golds: Sequence[GoldData], target: str, others: Sequence[str], *,
                            B: int, rng: random.Random) -> list[dict[str, float]]:
    return [pooled_deltas(golds, target, others,
                          [cluster_resample(g.labels, g.clusters, rng) for g in golds])
            for _ in range(B)]


def percentile(values: Sequence[float], q: float) -> float:
    """Linear-interpolation quantile (type 7)."""
    xs = sorted(values)
    if not xs:
        raise ValueError("no values")
    h = (len(xs) - 1) * q
    lo = math.floor(h)
    hi = min(lo + 1, len(xs) - 1)
    return xs[lo] + (h - lo) * (xs[hi] - xs[lo])
