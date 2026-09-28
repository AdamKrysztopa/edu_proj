"""Where a claim came from and what supports it, in PROV-O terms [95] without RDF:
Source is a prov:Entity, Generation and Verification are prov:Activity outcomes, Agent is a
prov:Agent, and Derivation is prov:wasDerivedFrom. Selector follows the W3C Web Annotation
TextQuoteSelector: the exact quoted text plus a locator.
"""
from __future__ import annotations

import hashlib
from datetime import date
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from residual.vocab import QUOTABLE_KINDS, WORLD_C_KINDS, SourceKind, Voice, World


class Record(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


def short_hash(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("\x1f".join(parts).encode()).hexdigest()
    return f"{prefix}-{digest[:16]}"


class Agent(Record):
    kind: Literal["human", "model", "software"]
    id: str
    family: str | None = None
    """Model provider family, e.g. 'anthropic'. Required for models: §11 step 4 verification
    counts only from a different family than the generator's."""

    @model_validator(mode="after")
    def _family(self) -> Agent:
        if (self.kind == "model") != (self.family is not None):
            raise ValueError("a model agent needs a family; only a model agent has one")
        return self


class Source(Record):
    identifier: str
    """DOI, URL, repository@commit, dataset id: what bibliographic resolution resolves."""
    kind: SourceKind
    world: World
    voice: Voice
    independence_key: str
    """Sources sharing a key count once for corroboration: same authors, or one derived from another."""
    published: date | None
    """None when undated; an undated source never counts in a dated view (Ledger.as_of)."""
    organisation: str | None = None
    boundary: bool = False
    """Boundary material (§11 step 2): a novice's error forces an expert to articulate."""

    @field_validator("identifier", "independence_key")
    @classmethod
    def _non_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("must not be empty")
        return v

    @model_validator(mode="after")
    def _world_rules(self) -> Source:
        if self.world is World.C and self.kind not in WORLD_C_KINDS:
            raise ValueError(f"a World C source records humans; {self.kind} is text")
        if (self.world is World.B) != (self.organisation is not None):
            raise ValueError("exactly the World B sources name their organisation")
        return self

    @property
    def source_id(self) -> str:
        return short_hash("s", self.identifier)


class Selector(Record):
    exact: str | None = None
    locator: str | None = None
    """Page, section, table row, file:line, commit, item or row id."""

    @model_validator(mode="after")
    def _something(self) -> Selector:
        if not (self.exact or self.locator):
            raise ValueError("a selector needs an exact quote or a locator")
        return self


class Verdict(StrEnum):
    SUPPORTS = "supports"
    REFUTES = "refutes"
    INSUFFICIENT = "insufficient"      # the span resolves but does not support the claim
    UNRESOLVABLE = "unresolvable"      # the source or span could not be found
    PENDING = "pending"


class Verification(Record):
    verdict: Verdict
    verifier: Agent | None = None
    on: date | None = None

    @model_validator(mode="after")
    def _who(self) -> Verification:
        pending = self.verdict is Verdict.PENDING
        if pending and (self.verifier or self.on) or not pending and not (self.verifier and self.on):
            raise ValueError("a pending verification has no verifier or date; any other has both")
        return self


PENDING = Verification(verdict=Verdict.PENDING)


class Evidence(Record):
    source: Source
    selector: Selector
    retrieved: date
    verification: Verification = PENDING

    @model_validator(mode="after")
    def _quote(self) -> Evidence:
        if self.source.kind in QUOTABLE_KINDS and not self.selector.exact:
            raise ValueError(f"evidence from a {self.source.kind} needs the exact quoted span")
        return self


class Generation(Record):
    """Who produced the claim's wording. A model-generated claim with no verified support is
    synthetic extrapolation (§6, §11 step 4); §12's labelling rule needs the spec hash."""

    agent: Agent
    activity: Literal["extraction", "parametric_recall", "simulation", "coding"]
    on: date
    spec_sha256: str | None = None
    tier: Literal["none", "T1", "T2", "T3", "T4"] | None = None
    """Validation tier the surrogate reached (§12); simulation only."""

    @model_validator(mode="after")
    def _labelling_rule(self) -> Generation:
        if self.agent.kind == "model" and not self.spec_sha256:
            raise ValueError("model generation records the prompt or spec hash")
        if (self.activity == "simulation") != (self.tier is not None):
            raise ValueError("a simulation records the validation tier it reached; nothing else does")
        if self.activity == "simulation" and self.agent.kind != "model":
            raise ValueError("a simulation is run by a model")
        return self


class Search(Record):
    """Evidence was sought: what makes an unsupported claim 'unknown' rather than unsourced."""

    corpus: str
    query: str
    on: date
    agent: Agent


class Derivation(Record):
    premises: tuple[str, ...]
    method: str
    agent: Agent

    @field_validator("premises")
    @classmethod
    def _premises(cls, v: tuple[str, ...]) -> tuple[str, ...]:
        if not v:
            raise ValueError("a derivation has at least one premise")
        return tuple(sorted(set(v)))
