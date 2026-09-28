"""Residual accounting (REORIENTATION.md §14). Three quantities are kept as separate types
because they answer different questions and are validated differently:

- ObservedResidual: what humans supplied that the reconstruction lacked, after the fact (§14.1).
- EstimatedResidual: the unseen-item estimate from text occasions, with its known-truth check.
- GapMapPrediction: P(important knowledge missing) per area, before any human is asked (§14.2).

NOW reports recall of H and an unvalidated R∖H count; an observed residual needs human
validity judgements for R∖H, which arrive LATER.
"""
from __future__ import annotations

from collections.abc import Mapping
from enum import StrEnum
from typing import Literal

from pydantic import Field, model_validator

from residual.gapmap import AreaFeatures
from residual.gates import Measurement, measure
from residual.ledger import Ledger
from residual.provenance import Agent, Record
from residual.vocab import BEHAVIOUR_ONLY, CRITERION_LABELS, KnowledgeType, Practice, Question


class ResidualNotMeasurable(Exception):
    pass


class Match(Record):
    """One matcher's verdict on a reconstructed and a revealed item, made blind to origin and
    to P(missing) (§14.1 pitfall 5, §18 common rules)."""

    reconstructed: str
    revealed: str
    same: bool
    matcher: Agent


class ValidityJudgement(Record):
    """A human rater's verdict that a reconstructed item absent from H is nonetheless valid.
    An LLM judge may not be the criterion (§14.1)."""

    claim_id: str
    valid: bool
    rater: Agent

    @model_validator(mode="after")
    def _human(self) -> ValidityJudgement:
        if self.rater.kind != "human":
            raise ValueError("validity of reconstructed items is judged by humans")
        return self


class ObservedResidual(Record):
    n_revealed: int = Field(gt=0)
    n_unrecalled: int = Field(ge=0)
    n_valid_extra: int = Field(ge=0)

    @model_validator(mode="after")
    def _counts(self) -> ObservedResidual:
        if self.n_unrecalled > self.n_revealed:
            raise ValueError("more unrecalled items than revealed ones")
        return self

    @property
    def value(self) -> float:
        return self.n_unrecalled / (self.n_revealed + self.n_valid_extra)


class ResidualAccount(Record):
    reconstruction: Ledger
    revealed: Ledger
    matches: tuple[Match, ...]
    validity: tuple[ValidityJudgement, ...] = ()

    @model_validator(mode="after")
    def _consistent(self) -> ResidualAccount:
        if self.reconstruction.purpose != "reconstruction" or self.revealed.purpose != "gold":
            raise ValueError("an account compares a reconstruction ledger with a gold ledger")
        if not self.revealed.claims:
            raise ValueError("the revealed set H is empty")
        for m in self.matches:
            if m.reconstructed not in self.reconstruction.by_id or m.revealed not in self.revealed.by_id:
                raise ValueError(f"match ({m.reconstructed}, {m.revealed}) names an absent claim")
            gen = self.reconstruction.by_id[m.reconstructed].generation
            if (m.matcher.kind == "model" and gen is not None and gen.agent.kind == "model"
                    and m.matcher.family == gen.agent.family):
                raise ValueError("a model matcher is of another family than the generator (§18)")
        judged = [j.claim_id for j in self.validity]
        if len(judged) != len(set(judged)):
            raise ValueError("one validity judgement per claim")
        if missing := set(judged) - set(self.reconstruction.by_id):
            raise ValueError(f"judgements name absent claims {sorted(missing)}")
        return self

    def recalled(self) -> frozenset[str]:
        return frozenset(m.revealed for m in self.matches if m.same)

    def unrecalled(self) -> tuple[str, ...]:
        """H∖R: revealed items the reconstruction lacks."""
        return tuple(sorted(set(self.revealed.by_id) - self.recalled()))

    def unmatched_reconstruction(self) -> tuple[str, ...]:
        """R∖H, unvalidated: reconstructed items no revealed item matches."""
        matched = {m.reconstructed for m in self.matches if m.same}
        return tuple(sorted(set(self.reconstruction.by_id) - matched))

    def recall(self, knowledge_type: KnowledgeType | None = None,
               weights: Mapping[str, Measurement] | None = None) -> Measurement:
        """Recall of H, optionally within one knowledge type (§14.1, §14.5). Unweighted is
        NOW's primary analysis; E-MISC weights each item by a measurement over that item, such
        as its prevalence, whose criterion labels the result inherits (§12: a surrogate's
        prevalence can never weight a gate)."""
        h = [c for c in self.revealed.claims
             if knowledge_type is None or c.knowledge_type is knowledge_type]
        if not h:
            raise ResidualNotMeasurable(f"no revealed items of type {knowledge_type}")
        hit = self.recalled()
        predictors = {self.reconstruction.label(c.claim_id) for c in self.reconstruction.claims}
        if weights is None:
            return measure(f"recall_of_H[{knowledge_type or 'all'}]",
                           sum(c.claim_id in hit for c in h) / len(h), h, ledger=self.revealed,
                           predictor_labels=predictors)
        w = {}
        for c in h:
            m = weights.get(c.claim_id)
            if m is None or c.claim_id not in m.criterion_ids or m.value < 0:
                raise ResidualNotMeasurable(f"{c.claim_id} has no non-negative weight measured over it")
            w[c.claim_id] = m.value
        if not sum(w.values()):
            raise ResidualNotMeasurable("the weights sum to zero")
        return measure(f"weighted_recall_of_H[{knowledge_type or 'all'}]",
                       sum(v for cid, v in w.items() if cid in hit) / sum(w.values()), h,
                       ledger=self.revealed, predictor_labels=predictors,
                       inputs=[weights[cid] for cid in w])

    def observed_residual(self) -> ObservedResidual:
        """Res_obs = |H∖R| / |H ∪ R_valid|, unweighted, NOW's primary analysis (§14.1)."""
        extra = self.unmatched_reconstruction()
        verdicts = {j.claim_id: j.valid for j in self.validity}
        if unjudged := [cid for cid in extra if cid not in verdicts]:
            raise ResidualNotMeasurable(
                f"{len(unjudged)} reconstructed items outside H have no human validity judgement; "
                "report recall of H and the unvalidated R∖H count instead")
        n_valid_extra = sum(verdicts[cid] for cid in extra)
        n_h, n_miss = len(self.revealed.claims), len(self.unrecalled())
        return ObservedResidual(n_revealed=n_h,
                                n_unrecalled=n_miss, n_valid_extra=n_valid_extra)


class EstimatedResidual(Record):
    """Unseen items estimated from text occasions, checked against gold as an independent
    occasion (§14.1). Occasions share authors and pretraining, so a stable estimate is not
    evidence of a correct one; only the known-truth check is."""

    estimator: Literal["chao1", "jackknife", "mh", "lincoln_petersen"]
    occasions: tuple[str, ...] = Field(min_length=2)
    """Distinct text occasions: source families or model families."""
    estimate: float = Field(ge=0)
    interval: tuple[float, float]
    gold_uncaptured: int | None = Field(None, ge=0)
    tolerance: float | None = Field(None, ge=0)

    @model_validator(mode="after")
    def _check_pair(self) -> EstimatedResidual:
        if (self.gold_uncaptured is None) != (self.tolerance is None):
            raise ValueError("a known-truth check needs both the gold count and its tolerance")
        if len(set(self.occasions)) != len(self.occasions):
            raise ValueError("occasions are distinct")
        if not self.interval[0] <= self.estimate <= self.interval[1]:
            raise ValueError("the estimate lies outside its interval")
        return self

    @property
    def known_truth_passed(self) -> bool | None:
        if self.gold_uncaptured is None:
            return None
        return abs(self.estimate - self.gold_uncaptured) <= self.tolerance


class GapMapPrediction(Record):
    area_id: str
    p_missing: float = Field(ge=0, le=1)
    predictor: str
    feature_set_sha256: str
    features: AreaFeatures

    @model_validator(mode="after")
    def _same_area(self) -> GapMapPrediction:
        if self.features.area_id != self.area_id:
            raise ValueError("features describe another area")
        return self


class Coverage(StrEnum):
    COVERED = "covered"
    WEAK = "weak"
    CONTRADICTED = "contradicted"
    UNKNOWN = "unknown"


def coverage(ledger: Ledger, area_id: str) -> Coverage:
    """What the evidence says about an area, descriptively. Not a gate and not the gap map:
    'where knowledge might be missing' is GapMapPrediction's question.

    Covered needs a supported claim with at least two independent sources, a record of work as
    done where performance is at stake (§11 step 5), and such a record wherever behaviour-only
    knowledge sits (R12)."""
    claims = ledger.in_area(area_id)
    if not claims:
        return Coverage.UNKNOWN
    contested = ledger.contradicted()
    if any(c.claim_id in contested or c.refuting for c in claims):
        return Coverage.CONTRADICTED
    supported = [c for c in claims if ledger.label(c.claim_id) in CRITERION_LABELS]
    if not supported:
        return Coverage.UNKNOWN
    done = any(Practice.DONE in c.practices for c in supported)
    if not done and any(c.tacitness in BEHAVIOUR_ONLY for c in claims):
        return Coverage.WEAK
    if not done and any(c.question is Question.PERFORMANCE for c in supported):
        return Coverage.WEAK
    if max(c.corroboration for c in supported) < 2:
        return Coverage.WEAK
    return Coverage.COVERED

