"""Evidential gates refuse synthetic material in code (REORIENTATION.md §6, §12, R6).

A gate reads only typed, labelled inputs. Synthetic output may still shape what a gate reads,
as a gap-map predictor (§14.2), because a measurement keeps the labels of its criterion (what
it is scored against) apart from those of its predictors.
"""
from __future__ import annotations

import functools
from collections.abc import Callable, Iterable, Iterator, Mapping
from typing import Literal, ParamSpec

from pydantic import PrivateAttr, field_validator, model_validator

from residual.claims import ClaimRecord
from residual.ledger import Ledger
from residual.provenance import Record
from residual.vocab import CRITERION_LABELS, EpistemicLabel


class GateRefusal(Exception):
    """An input a gate may not read as a criterion."""


class SyntheticRefused(GateRefusal):
    """Synthetic extrapolation offered to a gate as a criterion."""


class Measurement(Record):
    name: str
    value: float
    criterion_ids: tuple[str, ...]
    criterion_labels: frozenset[EpistemicLabel]
    predictor_labels: frozenset[EpistemicLabel] = frozenset()
    _sealed: bool = PrivateAttr(default=False)
    """Set only by measure(): a gate refuses a Measurement whose labels were typed in by hand."""

    @model_validator(mode="after")
    def _has_criterion(self) -> Measurement:
        if not self.criterion_ids or not self.criterion_labels:
            raise ValueError("a measurement names the claims it was scored against")
        return self


def measure(name: str, value: float, criterion: Iterable[ClaimRecord], *,
            ledger: Ledger | None = None,
            predictor_labels: Iterable[EpistemicLabel] = (),
            inputs: Iterable[Measurement] = ()) -> Measurement:
    """The one way to build a Measurement a gate will read. Labels are read off the criterion
    claims, through their ledger when given so that derivations carry their premises' labels;
    measurements used as inputs, such as weights, add their criterion labels and ids."""
    claims, inputs = tuple(criterion), tuple(inputs)
    labels = {ledger.label(c.claim_id) if ledger else c.label for c in claims}
    if unsealed := [m.name for m in inputs if not m._sealed]:
        raise GateRefusal(f"inputs {unsealed} were not built by measure()")
    labels |= {label for m in inputs for label in m.criterion_labels}
    ids = dict.fromkeys([*(c.claim_id for c in claims), *(i for m in inputs for i in m.criterion_ids)])
    m = Measurement(name=name, value=value, criterion_ids=tuple(ids),
                    criterion_labels=frozenset(labels), predictor_labels=frozenset(predictor_labels))
    m._sealed = True
    return m


class Threshold(Record):
    """A pre-registered number, such as δ, with where it was registered."""

    name: str
    value: float
    registered_in: str

    @field_validator("registered_in")
    @classmethod
    def _where(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("a threshold names where it was registered")
        return v


class GateDecision(Record):
    gate: str
    outcome: Literal["continue", "change", "stop", "inconclusive"]
    reason: str
    criterion_ids: tuple[str, ...] = ()


def _check(label: EpistemicLabel, what: str) -> None:
    if label is EpistemicLabel.SYNTHETIC_EXTRAPOLATION:
        raise SyntheticRefused(f"{what} is synthetic extrapolation; it may never be a criterion")
    if label not in CRITERION_LABELS:
        raise GateRefusal(f"{what} is {label}; a gate reads only supported evidence")


def _walk(value: object, ledger: Ledger | None = None) -> Iterator[str]:
    """Check every input and yield the criterion claim ids it carries."""
    if isinstance(value, Measurement):
        if not value._sealed:
            raise GateRefusal(f"measurement {value.name!r} was not built by measure()")
        for label in value.criterion_labels:
            _check(label, f"measurement {value.name!r}")
        yield from value.criterion_ids
    elif isinstance(value, ClaimRecord):
        _check(ledger.label(value.claim_id) if ledger else value.label, f"claim {value.claim_id}")
        yield value.claim_id
    elif isinstance(value, Ledger):
        if value.purpose == "surrogate":
            raise SyntheticRefused("a surrogate ledger holds simulation output; it is never a criterion")
        for claim in value.claims:
            yield from _walk(claim, value)
    elif isinstance(value, Threshold):
        return
    elif isinstance(value, Mapping):
        for k, v in value.items():
            if not isinstance(k, str):
                yield from _walk(k, ledger)
            yield from _walk(v, ledger)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for v in value:
            yield from _walk(v, ledger)
    else:
        raise GateRefusal(f"a gate reads Measurement, ClaimRecord, Ledger and Threshold only; "
                          f"got {type(value).__name__}, which carries no evidence label")


P = ParamSpec("P")


def evidential_gate(fn: Callable[P, GateDecision]) -> Callable[P, GateDecision]:
    """Make fn a gate: every argument is checked before fn runs, and fn must decide."""

    @functools.wraps(fn)
    def gate(*args: P.args, **kwargs: P.kwargs) -> GateDecision:
        ids = tuple(dict.fromkeys(i for v in (*args, *kwargs.values()) for i in _walk(v)))
        if not ids:
            raise GateRefusal(f"gate {fn.__name__} was given no criterion to decide on")
        decision = fn(*args, **kwargs)
        if not isinstance(decision, GateDecision):
            raise TypeError(f"gate {fn.__name__} must return a GateDecision")
        return decision.model_copy(update={"criterion_ids": ids})

    return gate
