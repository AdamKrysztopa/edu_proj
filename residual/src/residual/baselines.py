"""The §14.3 baselines, typed and dated, and the N3 gate statistic over them (I5).

Every score points the same way as the map: higher means "more likely missed".

The competing set K is DS3's (§4, §7): area size from the pre-gold partition, retrieval-support
density, corpus term frequency, plain-LLM ranking, the cross-gold type prior once every gold has at
least two other golds, and Jev/text-form. Random and the naive type rule are reported only.
Verbalised confidence is a specification only. Gold items per area is a near-oracle used only in
the I5 near-oracle check.

Gate, as set by the owner on 2026-10-24 (`REORIENTATION.md` §22 threshold table):
- Continue (intersection–union): every pairwise lower bound at boundary c above 0, and the minimum
  point estimate at least δ.
- Stop (Bonferroni over K): some pairwise upper bound at z_{1-α/K}, α = 1 − Φ(c), below δ.
- Otherwise inconclusive. The bootstrap minimum and max-T are reported beside it, never the gate.
"""
from __future__ import annotations

import hashlib
import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from statistics import NormalDist

from residual.auroc import Estimate, GoldData, auroc_covariance, percentile
from residual.vocab import KnowledgeType

DATED = "2026-10-24"
_N = NormalDist()


class Role(StrEnum):
    COMPETING = "competing"          # in K: a candidate for the strongest baseline
    REPORTED = "reported"            # computed and reported, never in K
    SPEC_ONLY = "spec_only"          # specified, not computed, never in K
    NEAR_ORACLE = "near_oracle"      # computed from the target gold: the I5 near-oracle check only


@dataclass(frozen=True)
class Baseline:
    name: str
    role: Role
    spec: str
    dated: str = DATED
    min_other_golds: int = 0
    model: str | None = None
    prompt: str | None = None


PLAIN_LLM_PROMPT = ("Here is a task and its areas, as listed in the pre-gold partition. For each area, "
                    "rate from 0 to 1 how likely it is that written sources omit expert knowledge an "
                    "expert would need there. Answer as JSON: {area_id: rating}.")

BASELINES: tuple[Baseline, ...] = (
    Baseline("area_size", Role.COMPETING,
             "Size of the area in the pre-gold partition (sub-steps, else tokens); never gold items."),
    Baseline("retrieval_support_density", Role.COMPETING,
             "Minus the area's verified supporting evidence count (AreaFeatures.evidence_density): "
             "the ablation of the map's best single feature."),
    Baseline("corpus_term_frequency", Role.COMPETING,
             "Minus the mean log(1 + count) of the area's terms in the dated pre-gold corpus [56]."),
    Baseline("plain_llm", Role.COMPETING,
             "One plain-LLM rating per area from a frozen prompt, on a model outside the generator "
             "and verifier families (ADR 0009); identifier and date frozen at pre-registration. "
             "Specified here; no call is made.",
             model="other-family model, identifier frozen at pre-registration", prompt=PLAIN_LLM_PROMPT),
    Baseline("type_prior", Role.COMPETING,
             "Rate of missed areas by knowledge type, fitted leave-one-gold-out on the other golds; "
             "exists only when at least two other golds exist.", min_other_golds=2),
    Baseline("jev_text_form", Role.COMPETING,
             "The stronger of the text-form baseline (length statistics of the area's records) and "
             "Jev's per-record score (typesafe/jev-1.13, research/spikes/jev), both fixed before gold.",
             model="typesafe/jev-1.13"),
    Baseline("random", Role.REPORTED, "Uniform score from sha256(seed, area_id); seed registered."),
    Baseline("naive_type_rule", Role.REPORTED,
             "1 if the area holds a procedure step or a decision, else 0 (§14.3)."),
    Baseline("verbalised_confidence", Role.SPEC_ONLY,
             "Minus the generator's stated confidence in the area's claims; specified, not computed.",
             model="the ledger's generator"),
    Baseline("gold_items_per_area", Role.NEAR_ORACLE,
             "Number of target-gold items mapped to the area. Computed from the gold itself, so it "
             "is used only in the near-oracle check (DS3 §7, coverage-audit finding 20)."),
)


def by_name(name: str) -> Baseline:
    for b in BASELINES:
        if b.name == name:
            return b
    raise KeyError(name)


def competing_set(n_golds: int) -> tuple[str, ...]:
    """K for a leave-one-gold-out analysis over n_golds golds: each gold has n_golds − 1 others."""
    return tuple(b.name for b in BASELINES
                 if b.role is Role.COMPETING and n_golds - 1 >= b.min_other_golds)


# --- typed baseline scores -------------------------------------------------------------------------

def random_score(area_ids: Sequence[str], seed: int) -> dict[str, float]:
    return {a: int.from_bytes(hashlib.sha256(f"{seed}:{a}".encode()).digest()[:8], "big") / 2 ** 64
            for a in area_ids}


_NAIVE = {KnowledgeType.PROCEDURE_STEP, KnowledgeType.DECISION}


def naive_type_rule(types: Mapping[str, Sequence[KnowledgeType]]) -> dict[str, float]:
    return {a: 1.0 if _NAIVE & set(ts) else 0.0 for a, ts in types.items()}


def area_size(sizes: Mapping[str, int]) -> dict[str, float]:
    return {a: float(s) for a, s in sizes.items()}


def retrieval_support_density(density: Mapping[str, int]) -> dict[str, float]:
    return {a: -float(d) for a, d in density.items()}


def corpus_term_frequency(term_counts: Mapping[str, Sequence[int]]) -> dict[str, float]:
    return {a: -(sum(math.log1p(c) for c in cs) / len(cs) if cs else 0.0) for a, cs in term_counts.items()}


def type_prior(types: Mapping[str, Sequence[KnowledgeType]], other_gold_rates: Mapping[KnowledgeType, float],
               *, n_other_golds: int) -> dict[str, float]:
    """Mean missed rate of the area's types on the other golds; 0.5 for a type they never saw."""
    if n_other_golds < by_name("type_prior").min_other_golds:
        raise ValueError("the type prior needs at least two other golds")
    out = {}
    for a, ts in types.items():
        rates = [other_gold_rates.get(t, 0.5) for t in ts] or [0.5]
        out[a] = sum(rates) / len(rates)
    return out


def gold_items_per_area(counts: Mapping[str, int]) -> dict[str, float]:
    return {a: float(n) for a, n in counts.items()}


# --- the gate statistic ----------------------------------------------------------------------------

@dataclass(frozen=True)
class Comparison:
    """Pooled ΔAUROC of the map minus one baseline."""
    baseline: str
    delta: float
    se: float


@dataclass(frozen=True)
class Reading:
    outcome: str  # continue | stop | inconclusive
    min_delta: float
    min_lower: float
    min_upper_bonferroni: float


def one_sided_alpha(c: float) -> float:
    return 1 - _N.cdf(c)


def n3_reading(comparisons: Sequence[Comparison], *, c: float = 1.85, delta: float = 0.10) -> Reading:
    if not comparisons:
        raise ValueError("no baselines to compare against")
    z_bonf = _N.inv_cdf(1 - one_sided_alpha(c) / len(comparisons))
    min_delta = min(x.delta for x in comparisons)
    min_lower = min(x.delta - c * x.se for x in comparisons)
    min_upper = min(x.delta + z_bonf * x.se for x in comparisons)
    if min_upper < delta:
        outcome = "stop"
    elif min_lower > 0 and min_delta >= delta:
        outcome = "continue"
    else:
        outcome = "inconclusive"
    return Reading(outcome, min_delta, min_lower, min_upper)


def ms3_screen(comparisons: Sequence[Comparison], *, delta: float, z: float = 1.645) -> bool:
    """The report's MS3 funding screen (17_validation.tex:35-39), read against every baseline."""
    return all(x.delta >= delta and x.delta - z * x.se > -delta / 2 for x in comparisons)


def ms5_reading(comparisons: Sequence[Comparison], *, delta: float, z: float = 1.645) -> str:
    """The report's MS5 rule (17_validation.tex:40-44): 90% bounds, no adjustment across baselines."""
    if min(x.delta + z * x.se for x in comparisons) < delta:
        return "stop"
    if all(x.delta - z * x.se > 0 for x in comparisons) and min(x.delta for x in comparisons) >= delta:
        return "continue"
    return "inconclusive"


def bootstrap_min_reading(comparisons: Sequence[Comparison], draws: Sequence[Mapping[str, float]], *,
                          c: float, delta: float) -> str:
    """DS3 §4's rejected rule: the strongest baseline chosen inside each resample. Reported only."""
    alpha = one_sided_alpha(c)
    names = [x.baseline for x in comparisons]
    mins = [min(d[n] for n in names) for d in draws]
    if percentile(mins, 1 - alpha) < delta:
        return "stop"
    if percentile(mins, alpha) > 0 and min(x.delta for x in comparisons) >= delta:
        return "continue"
    return "inconclusive"


def max_t_reading(comparisons: Sequence[Comparison], draws: Sequence[Mapping[str, float]], *,
                  c: float, delta: float) -> str:
    """Single-step max-T simultaneous upper bounds for Stop (the first step of Romano & Wolf's 2005
    stepdown); Continue as the gate (intersection–union). Reported only."""
    alpha = one_sided_alpha(c)
    tmax = [max((x.delta - d[x.baseline]) / x.se if x.se > 0 else 0.0 for x in comparisons) for d in draws]
    crit = percentile(tmax, 1 - alpha)
    if min(x.delta + crit * x.se for x in comparisons) < delta:
        return "stop"
    if all(x.delta - c * x.se > 0 for x in comparisons) and min(x.delta for x in comparisons) >= delta:
        return "continue"
    return "inconclusive"


def bootstrap_reading(comparisons: Sequence[Comparison], draws: Sequence[Mapping[str, float]], *,
                      c: float, delta: float) -> str:
    """The gate rule with cluster-bootstrap percentile bounds in place of the analytic ones."""
    alpha = one_sided_alpha(c)
    k = len(comparisons)
    uppers = [percentile([d[x.baseline] for d in draws], 1 - alpha / k) for x in comparisons]
    lowers = [percentile([d[x.baseline] for d in draws], alpha) for x in comparisons]
    if min(uppers) < delta:
        return "stop"
    if min(lowers) > 0 and min(x.delta for x in comparisons) >= delta:
        return "continue"
    return "inconclusive"


@dataclass(frozen=True)
class GoldStats:
    """One gold's AUROCs of [target, *baselines] and their covariance; weight n1·n0."""
    names: tuple[str, ...]
    weight: float
    thetas: list[float]
    cov: list[list[float]]


def gold_stats(gold: GoldData, names: Sequence[str], *, clustered: bool = True) -> GoldStats:
    n1 = sum(1 for y in gold.labels if y)
    thetas, cov = auroc_covariance([gold.scores[n] for n in names], gold.labels,
                                   gold.clusters if clustered else None)
    return GoldStats(tuple(names), n1 * (len(gold.labels) - n1), thetas, cov)


def pool_stats(stats: Sequence[GoldStats], others: Sequence[str]) -> tuple[list[Comparison], list[list[float]]]:
    """Common-effect ΔAUROC of the first name against each of `others` (golds as fixed strata,
    weights n1·n0), with the covariance matrix of those differences (for max-T)."""
    k = len(others)
    wsum = 0.0
    num = [0.0] * k
    cov = [[0.0] * k for _ in range(k)]
    for s in stats:
        idx = [s.names.index(o) for o in others]
        v, w = s.cov, s.weight
        for i, a in enumerate(idx):
            num[i] += w * (s.thetas[0] - s.thetas[a])
            for j, b in enumerate(idx):
                cov[i][j] += w * w * (v[0][0] - v[0][a] - v[0][b] + v[a][b])
        wsum += w
    cov = [[x / wsum ** 2 for x in row] for row in cov]
    comps = [Comparison(baseline=o, delta=num[i] / wsum, se=math.sqrt(max(cov[i][i], 0.0)))
             for i, o in enumerate(others)]
    return comps, cov


def per_gold_estimates(stats: Sequence[GoldStats], other: str) -> list[Estimate]:
    """Each gold's ΔAUROC against one baseline, for the random-effects sensitivity."""
    out = []
    for s in stats:
        a = s.names.index(other)
        var = s.cov[0][0] + s.cov[a][a] - 2 * s.cov[0][a]
        out.append(Estimate(delta=s.thetas[0] - s.thetas[a], se=math.sqrt(max(var, 0.0)), weight=s.weight))
    return out


def pooled_comparisons(golds: Sequence[GoldData], target: str, others: Sequence[str], *,
                       clustered: bool = True) -> tuple[list[Comparison], list[list[float]]]:
    names = [target, *others]
    return pool_stats([gold_stats(g, names, clustered=clustered) for g in golds], others)
