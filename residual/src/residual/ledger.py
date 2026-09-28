"""A set of claims with the relations between them, kept apart by purpose.

Gold, reconstruction and surrogate material never share a ledger (§12 labelling rule, §14.3
held-out gold, R6). Contradictions are records of their own, made by a detector, not left to
the synthesiser (§10.1).
"""
from __future__ import annotations

import json
from collections.abc import Callable
from datetime import date
from functools import cached_property
from typing import Literal

from pydantic import field_validator, model_validator

from residual.claims import ClaimRecord, Scope
from residual.provenance import Agent, Evidence, Record
from residual.vocab import CRITERION_LABELS, EpistemicLabel, World


class Contradiction(Record):
    claims: tuple[str, str]
    detected_by: Agent
    method: str

    @field_validator("claims")
    @classmethod
    def _pair(cls, v: tuple[str, str]) -> tuple[str, str]:
        if v[0] == v[1]:
            raise ValueError("a claim does not contradict itself")
        return tuple(sorted(v))


class Area(Record):
    """A unit of the area partition: task step, decision point, KC, component or SOP section."""

    area_id: str
    scope: Scope
    name: str


class Ledger(Record):
    purpose: Literal["reconstruction", "gold", "surrogate"]
    claims: tuple[ClaimRecord, ...] = ()
    contradictions: tuple[Contradiction, ...] = ()
    areas: tuple[Area, ...] = ()
    assignments: tuple[tuple[str, str], ...] = ()
    """(claim_id, area_id); a claim sits in at most one area."""

    @field_validator("claims")
    @classmethod
    def _sort_claims(cls, v: tuple[ClaimRecord, ...]) -> tuple[ClaimRecord, ...]:
        ids = [c.claim_id for c in v]
        if dupes := sorted({i for i in ids if ids.count(i) > 1}):
            raise ValueError(f"duplicate claims {dupes}: merge their evidence into one record")
        return tuple(sorted(v, key=lambda c: c.claim_id))

    @field_validator("contradictions", "areas", "assignments")
    @classmethod
    def _sort(cls, v: tuple) -> tuple:
        return tuple(sorted(v, key=lambda x: json.dumps(x.model_dump(mode="json")
                                                        if isinstance(x, Record) else x)))

    @model_validator(mode="after")
    def _integrity(self) -> Ledger:
        ids = set(self.by_id)
        sources: dict[str, object] = {}
        for c in self.claims:
            for e in c.evidence:
                if sources.setdefault(e.source.source_id, e.source) != e.source:
                    raise ValueError(f"source {e.source.identifier} is described two ways")
            if c.derivation and (missing := set(c.derivation.premises) - ids):
                raise ValueError(f"{c.claim_id} derives from absent claims {sorted(missing)}")
        for x in self.contradictions:
            if missing := set(x.claims) - ids:
                raise ValueError(f"contradiction names absent claims {sorted(missing)}")
        area_ids = {a.area_id for a in self.areas}
        if len(area_ids) != len(self.areas):
            raise ValueError("duplicate area ids")
        assigned = [cid for cid, _ in self.assignments]
        if len(assigned) != len(set(assigned)):
            raise ValueError("a claim is assigned to more than one area")
        for cid, aid in self.assignments:
            if cid not in ids or aid not in area_ids:
                raise ValueError(f"assignment ({cid}, {aid}) names an absent claim or area")
        self._check_acyclic()
        self._check_purpose()
        return self

    def _check_acyclic(self) -> None:
        state: dict[str, int] = {}

        def visit(cid: str) -> None:
            if state.get(cid) == 1:
                raise ValueError(f"derivation cycle through {cid}")
            if state.get(cid) == 2:
                return
            state[cid] = 1
            d = self.by_id[cid].derivation
            for p in d.premises if d else ():
                visit(p)
            state[cid] = 2

        for cid in self.by_id:
            visit(cid)

    def _check_purpose(self) -> None:
        simulated = {c.claim_id for c in self.claims
                     if c.generation is not None and c.generation.activity == "simulation"}
        if self.purpose == "surrogate" and len(simulated) != len(self.claims):
            raise ValueError("a surrogate ledger holds only simulation output")
        if self.purpose != "surrogate" and simulated:
            raise ValueError(f"simulation output belongs in a surrogate ledger: {sorted(simulated)}")
        if self.purpose == "gold":
            weak = sorted(cid for cid in self.by_id if self.label(cid) not in CRITERION_LABELS)
            if weak:
                raise ValueError(f"gold holds only supported claims; not supported: {weak}")

    @cached_property
    def by_id(self) -> dict[str, ClaimRecord]:
        return {c.claim_id: c for c in self.claims}

    def area_of(self, claim_id: str) -> str | None:
        return dict(self.assignments).get(claim_id)

    def in_area(self, area_id: str) -> tuple[ClaimRecord, ...]:
        return tuple(self.by_id[cid] for cid, aid in self.assignments if aid == area_id)

    def contradicted(self) -> frozenset[str]:
        return frozenset(cid for x in self.contradictions for cid in x.claims)

    def label(self, claim_id: str) -> EpistemicLabel:
        """A claim's label, with a derivation taking the weakest of its premises: an inference
        from synthetic material is synthetic, and from unsought material unknown (§6)."""
        claim = self.by_id[claim_id]
        own = claim.label
        if own is not EpistemicLabel.INFERRED:
            return own
        premises = {self.label(p) for p in claim.derivation.premises}
        for weakest in (EpistemicLabel.SYNTHETIC_EXTRAPOLATION, EpistemicLabel.UNKNOWN):
            if weakest in premises:
                return weakest
        return own

    def as_of(self, t: date) -> tuple[Ledger, tuple[str, ...]]:
        """What the evidence dated on or before t supports (§18 E-OSS, §18.2). Undated sources
        do not count. Returns the dated ledger and the claims with no remaining basis, which
        are dropped rather than relabelled."""
        return self._restrict(lambda e: e.source.published is not None and e.source.published <= t,
                              searched_by=t)

    def within(self, worlds: set[World]) -> tuple[Ledger, tuple[str, ...]]:
        """What evidence from the given worlds alone supports: public vs organisational vs
        human-revealed (§13)."""
        return self._restrict(lambda e: e.source.world in worlds)

    def _restrict(self, keep: Callable[[Evidence], bool],
                  searched_by: date | None = None) -> tuple[Ledger, tuple[str, ...]]:
        kept: dict[str, ClaimRecord] = {}
        for c in self.claims:
            searches = tuple(s for s in c.searches if searched_by is None or s.on <= searched_by)
            try:
                claim = ClaimRecord.model_validate(
                    c.model_dump() | {"evidence": [e.model_dump() for e in c.evidence if keep(e)],
                                      "searches": [s.model_dump() for s in searches]})
            except ValueError:
                continue
            if self.purpose != "gold" or claim.label in CRITERION_LABELS:
                kept[c.claim_id] = claim
        changed = True
        while changed:
            changed = False
            for cid, c in list(kept.items()):
                if c.derivation and not set(c.derivation.premises) <= kept.keys():
                    del kept[cid]
                    changed = True
        dropped = tuple(sorted(set(self.by_id) - kept.keys()))
        ledger = Ledger(
            purpose=self.purpose,
            claims=tuple(kept.values()),
            contradictions=tuple(x for x in self.contradictions if set(x.claims) <= kept.keys()),
            areas=self.areas,
            assignments=tuple(a for a in self.assignments if a[0] in kept),
        )
        return ledger, dropped

    def to_json(self) -> str:
        return json.dumps(self.model_dump(mode="json"), sort_keys=True, indent=1) + "\n"

    @classmethod
    def from_json(cls, text: str) -> Ledger:
        return cls.model_validate_json(text)
