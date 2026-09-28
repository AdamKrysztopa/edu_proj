"""The claim record: the unit of residual accounting (REORIENTATION.md §10.1).

A claim never states its own epistemic label. The label is read off its evidence, so a claim
is literature- or organisation-supported only when a verifier other than its generator has
matched it to a span in such a source (§6: 'a claim with no verifying source span gets status
unsupported whatever the model says').
"""
from __future__ import annotations

import re
from datetime import date

from pydantic import field_validator, model_validator

from residual.provenance import (
    Derivation,
    Evidence,
    Generation,
    Record,
    Search,
    Verdict,
    short_hash,
)
from residual.vocab import (
    CRITERION_LABELS,
    DIFFICULTY_KINDS,
    HUMAN_RECORD_KINDS,
    PRACTICE,
    Certainty,
    EpistemicLabel,
    KnowledgeType,
    Layer,
    Practice,
    Question,
    SourceKind,
    Tacitness,
    Voice,
    World,
)


class Scope(Record):
    domain: str
    task: str | None = None
    organisation: str | None = None


class ClaimRecord(Record):
    assertion: str
    question: Question
    layer: Layer
    knowledge_type: KnowledgeType
    tacitness: Tacitness = Tacitness.UNASSESSED
    scope: Scope
    evidence: tuple[Evidence, ...] = ()
    generation: Generation | None = None
    derivation: Derivation | None = None
    searches: tuple[Search, ...] = ()
    certainty: Certainty | None = None
    valid_from: date | None = None
    valid_until: date | None = None

    @field_validator("assertion")
    @classmethod
    def _assertion(cls, v: str) -> str:
        v = re.sub(r"\s+", " ", v).strip()
        if not v:
            raise ValueError("an assertion must not be empty")
        return v

    @field_validator("evidence", "searches")
    @classmethod
    def _canonical_order(cls, v: tuple) -> tuple:
        return tuple(sorted(v, key=lambda e: e.model_dump_json()))

    @model_validator(mode="after")
    def _coherent(self) -> ClaimRecord:
        if self.valid_from and self.valid_until and self.valid_from > self.valid_until:
            raise ValueError("valid_from is after valid_until")
        model_made = self.generation is not None and self.generation.agent.kind == "model"
        if not (self.evidence or self.searches or self.derivation or model_made):
            raise ValueError("a claim needs evidence, a search, a derivation or a model generation "
                             "to account for it")
        if self.certainty is not None and self.label not in CRITERION_LABELS:
            raise ValueError(f"certainty grades supported evidence; this claim is {self.label}")
        return self

    @property
    def claim_id(self) -> str:
        """Origin-free and model-free (§14.3): the same assertion, question and scope give the
        same id whoever produced it."""
        s = self.scope
        return short_hash("c", self.assertion.casefold(), self.question, s.domain,
                          s.task or "", s.organisation or "")

    def _exclusion(self, e: Evidence) -> str | None:
        src, verifier = e.source, e.verification.verifier
        if src.voice is Voice.MACHINE:
            return "machine-voiced source"
        if verifier is not None and verifier.kind == "software":
            return "software can check that a span exists, not that it supports the claim"
        gen = self.generation
        if (verifier is not None and verifier.kind == "model" and gen is not None
                and gen.agent.kind == "model" and verifier.family == gen.agent.family):
            return "verified by the generating model's family"
        if self.question is Question.DIFFICULTY and (
                src.kind not in DIFFICULTY_KINDS or src.voice is not Voice.NOVICE):
            return "difficulty is answered only by learner data"
        if self.question is Question.LEARNER_STATE and not (
                src.world is World.C and src.kind is SourceKind.LEARNER_RESPONSE
                and src.voice is Voice.NOVICE):
            return "learner state is answered only by this learner's own responses (World C)"
        if src.world is World.B and src.organisation != self.scope.organisation:
            return "organisational evidence supports only claims scoped to its organisation"
        return None

    @property
    def supporting(self) -> tuple[Evidence, ...]:
        return tuple(e for e in self.evidence
                     if e.verification.verdict is Verdict.SUPPORTS and self._exclusion(e) is None)

    @property
    def excluded(self) -> tuple[tuple[Evidence, str], ...]:
        """Evidence judged to support the claim that does not count, with the reason."""
        out = []
        for e in self.evidence:
            if e.verification.verdict is Verdict.SUPPORTS and (why := self._exclusion(e)):
                out.append((e, why))
        return tuple(out)

    @property
    def refuting(self) -> tuple[Evidence, ...]:
        return tuple(e for e in self.evidence if e.verification.verdict is Verdict.REFUTES)

    @property
    def pending(self) -> bool:
        return any(e.verification.verdict is Verdict.PENDING for e in self.evidence)

    @property
    def label(self) -> EpistemicLabel:
        """This claim's own label. A derivation's final label also depends on its premises,
        which only the ledger holds (Ledger.label)."""
        sup = self.supporting
        if any(e.source.world is World.C
               or (e.source.world is World.A and e.source.kind in HUMAN_RECORD_KINDS) for e in sup):
            return EpistemicLabel.OBSERVED_HUMAN_EVIDENCE
        if any(e.source.world is World.B for e in sup):
            return EpistemicLabel.ORGANISATIONAL_ARTEFACT_SUPPORTED
        if sup:
            return EpistemicLabel.LITERATURE_SUPPORTED
        if self.derivation is not None:
            return EpistemicLabel.INFERRED
        if self.generation is not None and self.generation.agent.kind == "model":
            return EpistemicLabel.SYNTHETIC_EXTRAPOLATION
        if any(e.source.voice is Voice.MACHINE for e in self.evidence):
            return EpistemicLabel.SYNTHETIC_EXTRAPOLATION
        return EpistemicLabel.UNKNOWN

    @property
    def corroboration(self) -> int:
        """Independent supporting sources; same authors or derived sources count once."""
        return len({e.source.independence_key for e in self.supporting})

    @property
    def practices(self) -> frozenset[Practice]:
        """Imagined-only support stays imagined until a record of work as done corroborates it
        (§11 step 5)."""
        return frozenset(PRACTICE[e.source.kind] for e in self.supporting)

    @property
    def worlds(self) -> frozenset[World]:
        return frozenset(e.source.world for e in self.supporting)

    def in_force(self, on: date) -> bool:
        return ((self.valid_from is None or self.valid_from <= on)
                and (self.valid_until is None or on <= self.valid_until))
