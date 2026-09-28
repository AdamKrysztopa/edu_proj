import pytest
from conftest import CODER, claim, evidence, generation, search
from pydantic import ValidationError

from residual.gates import (
    GateDecision,
    GateRefusal,
    Measurement,
    SyntheticRefused,
    Threshold,
    evidential_gate,
    measure,
)
from residual.ledger import Ledger
from residual.provenance import Derivation
from residual.vocab import EpistemicLabel

L = EpistemicLabel
CALLS = []


@evidential_gate
def gate(*args, **kwargs):
    CALLS.append(args)
    return GateDecision(gate="g", outcome="continue", reason="r")


SUPPORTED = claim("Supported.", evidence=(evidence(),))
SYNTHETIC = claim("Synthetic.", generation=generation())
UNKNOWN = claim("Unknown.", searches=(search(),))
INFERRED = claim("Inferred.", derivation=Derivation(premises=(SUPPORTED.claim_id,), method="m",
                                                    agent=CODER))
TAINTED = claim("Tainted.", derivation=Derivation(premises=(SYNTHETIC.claim_id,), method="m",
                                                  agent=CODER))
THRESHOLD = Threshold(name="delta", value=0.1, registered_in="prereg/n3.json")


def refused(exc, *args, **kwargs):
    CALLS.clear()
    with pytest.raises(exc):
        gate(*args, **kwargs)
    assert CALLS == []


@pytest.mark.parametrize("wrap", [
    lambda c: c, lambda c: [c], lambda c: {"k": c}, lambda c: (SUPPORTED, [c]),
    lambda c: {"k": [THRESHOLD, {"j": c}]}, lambda c: {c},
    lambda c: Ledger(purpose="reconstruction", claims=(SUPPORTED, c)),
])
def test_synthetic_claims_are_refused_wherever_they_sit(wrap):
    refused(SyntheticRefused, wrap(SYNTHETIC))
    refused(SyntheticRefused, x=wrap(SYNTHETIC))


def test_a_derivation_over_a_synthetic_premise_is_refused_through_its_ledger():
    refused(SyntheticRefused, Ledger(purpose="reconstruction", claims=(SYNTHETIC, TAINTED)))
    refused(GateRefusal, TAINTED)


def test_synthetic_refused_is_a_gate_refusal():
    assert issubclass(SyntheticRefused, GateRefusal)


@pytest.mark.parametrize("c", [INFERRED, UNKNOWN])
def test_inferred_and_unknown_are_refused(c):
    CALLS.clear()
    with pytest.raises(GateRefusal) as info:
        gate(c)
    assert not isinstance(info.value, SyntheticRefused)
    assert CALLS == []


@pytest.mark.parametrize("value", [0.5, 3, "0.5", None, True, b"x", object(), GateDecision(
    gate="g", outcome="stop", reason="r")])
def test_bare_values_and_unrecognised_objects_are_refused(value):
    refused(GateRefusal, value)
    refused(GateRefusal, [SUPPORTED, value])


def test_criterion_claims_thresholds_and_measurements_are_accepted():
    m = measure("recall", 0.5, [SUPPORTED])
    decision = gate(SUPPORTED, THRESHOLD, m, Ledger(purpose="gold", claims=(SUPPORTED,)),
                    extra={"t": [THRESHOLD]})
    assert decision.outcome == "continue"
    assert decision.criterion_ids == (SUPPORTED.claim_id,)


def test_the_decision_records_the_criterion_ids_in_order():
    other = claim("Other.", evidence=(evidence(),))
    decision = gate(other, measure("m", 1.0, [SUPPORTED, other]))
    assert decision.criterion_ids == (other.claim_id, SUPPORTED.claim_id)


def test_a_gate_without_a_criterion_is_refused():
    refused(GateRefusal, THRESHOLD)
    refused(GateRefusal, [])


def test_synthetic_predictors_are_accepted_with_supported_criteria():
    m = measure("gapmap_auc", 0.7, [SUPPORTED],
                predictor_labels=[L.SYNTHETIC_EXTRAPOLATION, L.UNKNOWN, L.INFERRED])
    assert gate(m).criterion_ids == (SUPPORTED.claim_id,)


@pytest.mark.parametrize(("label", "exc"), [
    (L.SYNTHETIC_EXTRAPOLATION, SyntheticRefused), (L.INFERRED, GateRefusal), (L.UNKNOWN, GateRefusal)])
def test_a_measurement_with_a_weak_criterion_label_is_refused(label, exc):
    m = Measurement(name="m", value=1.0, criterion_ids=("c",),
                    criterion_labels=frozenset({L.LITERATURE_SUPPORTED, label}))
    m._sealed = True
    refused(exc, m)


def test_a_measurement_not_built_by_measure_is_refused():
    forged = Measurement(name="m", value=1.0, criterion_ids=("c",),
                         criterion_labels=frozenset({L.LITERATURE_SUPPORTED}))
    refused(GateRefusal, forged)


def test_measure_reads_labels_through_the_ledger():
    ledger = Ledger(purpose="reconstruction", claims=(SYNTHETIC, TAINTED))
    assert measure("m", 1.0, [TAINTED]).criterion_labels == {L.INFERRED}
    tainted = measure("m", 1.0, [TAINTED], ledger=ledger)
    assert tainted.criterion_labels == {L.SYNTHETIC_EXTRAPOLATION}
    refused(SyntheticRefused, tainted)
    assert measure("m", 1.0, [SYNTHETIC]).criterion_labels == {L.SYNTHETIC_EXTRAPOLATION}


def test_a_measurement_names_its_criterion():
    with pytest.raises(ValidationError, match="names the claims"):
        measure("m", 1.0, [])
    with pytest.raises(ValidationError, match="names the claims"):
        Measurement(name="m", value=1.0, criterion_ids=("c",), criterion_labels=frozenset())


@pytest.mark.parametrize("where", ["", "   "])
def test_a_threshold_names_where_it_was_registered(where):
    with pytest.raises(ValidationError, match="registered"):
        Threshold(name="delta", value=0.1, registered_in=where)


def test_a_gate_must_decide():
    @evidential_gate
    def lazy(x):
        return 0.5

    with pytest.raises(TypeError, match="GateDecision"):
        lazy(SUPPORTED)


def test_a_gate_overrides_the_criterion_ids_its_function_claims():
    @evidential_gate
    def liar(x):
        return GateDecision(gate="g", outcome="stop", reason="r", criterion_ids=("forged",))

    assert liar(SUPPORTED).criterion_ids == (SUPPORTED.claim_id,)
    assert liar.__name__ == "liar"
