"""The gap map's input record per area (REORIENTATION.md §14.2). Definitions only: computing
the features is N2's job, predicting from them is N3's. The field set is hash-frozen at N1
(freeze.py) so it cannot be tuned after gold is seen (§14.3).
"""
from __future__ import annotations

from datetime import date

from pydantic import Field

from residual.provenance import Record
from residual.vocab import EpistemicLabel, KnowledgeType, SourceKind, Tacitness


class LabelledValue(Record):
    """A predictor value that keeps its label: instability across model families is
    synthetic output, usable as a predictor and never as a criterion (§14.2, R6)."""

    value: float
    label: EpistemicLabel
    method: str


class AreaFeatures(Record):
    area_id: str
    n_claims: int = Field(ge=0)
    evidence_density: int = Field(ge=0, description="verified supporting evidence items")
    n_independent_sources: int = Field(ge=0, description="distinct independence keys")
    source_kinds: tuple[SourceKind, ...] = Field(description="source diversity and family coverage")
    n_boundary_sources: int = Field(ge=0, description="boundary-text density (§11 step 2, [25])")
    n_contradictions: int = Field(ge=0, description="claims in a detected contradiction or with refuting evidence")
    knowledge_types: tuple[KnowledgeType, ...]
    tacitness: tuple[Tacitness, ...]
    has_done_support: bool = Field(description="trace availability: a record of work as done")
    imagined_only: bool = Field(description="supported only by work-as-imagined sources [19]")
    n_single_source_claims: int = Field(ge=0, description="once-documented support [57]")
    n_inferred: int = Field(ge=0, description="unsupported inference")
    n_synthetic: int = Field(ge=0)
    n_unknown: int = Field(ge=0, description="sought and not found")
    earliest_source: date | None = Field(description="temporal coverage")
    latest_source: date | None
    n_undated_sources: int = Field(ge=0)
    rationale_present: bool = Field(description="a supported 'why' exists ([117] causal ambiguity)")
    instability: LabelledValue | None = Field(None, description="cross-model or cross-corpus disagreement [150]")
    concentration: LabelledValue | None = Field(None, description="review-weighted knowledge concentration [114]")


FEATURE_SET: tuple[str, ...] = tuple(f for f in AreaFeatures.model_fields if f != "area_id")
