"""Regression tests for the gate bypasses a type-design review reproduced on 2026-09-28:
each one used to reach an evidential gate with a synthetic or unverified criterion."""
import math

import pytest
from conftest import CODER, GENERATOR, claim, evidence, generation
from pydantic import ValidationError

from residual.gates import GateDecision, GateRefusal, Measurement, Threshold, evidential_gate, measure
from residual.gapmap import AreaFeatures
from residual.ledger import Ledger
from residual.provenance import PENDING, Agent, Selector, Verdict
from residual.residual import EstimatedResidual, ObservedResidual
from residual.vocab import EpistemicLabel as L


@evidential_gate
def gate(*args):
    return GateDecision(gate="g", outcome="continue", reason="r")


GOOD = claim("Good.", evidence=(evidence(),))
SYNTHETIC = claim("Synthetic.", generation=generation())


def test_copying_a_measurement_cannot_forge_its_labels():
    m = measure("m", 0.1, [SYNTHETIC])
    forged = m.model_copy(update={"criterion_labels": frozenset({L.OBSERVED_HUMAN_EVIDENCE})})
    with pytest.raises(GateRefusal):
        gate(forged)


def test_measure_refuses_unsealed_inputs():
    fake = Measurement(name="w", value=1, criterion_ids=("c-fake",),
                       criterion_labels=frozenset({L.OBSERVED_HUMAN_EVIDENCE}))
    with pytest.raises(GateRefusal, match="not built by measure"):
        measure("x", 0.5, [GOOD], inputs=[fake])


def test_a_copied_ledger_is_revalidated():
    gold = Ledger(purpose="gold", claims=(GOOD,))
    swapped = GOOD.model_copy(update={"evidence": ()} | {"generation": generation()})
    with pytest.raises(ValidationError):
        gold.model_copy(update={"claims": (swapped,)})


def test_the_claim_index_is_read_only():
    gold = Ledger(purpose="gold", claims=(GOOD,))
    with pytest.raises(TypeError):
        gold.by_id[GOOD.claim_id] = SYNTHETIC


def test_a_supports_verdict_without_a_verifier_cannot_be_built_even_by_copy():
    with pytest.raises(ValidationError):
        PENDING.model_copy(update={"verdict": Verdict.SUPPORTS})


def test_model_families_compare_case_insensitively():
    shouting = Agent(kind="model", id="v", family="  FAMILY-A ")
    assert shouting.family == GENERATOR.family
    c = claim("Self-verified.", generation=generation(), evidence=(evidence(verifier=shouting),))
    assert c.label is L.SYNTHETIC_EXTRAPOLATION


def test_certainty_cannot_be_copied_onto_a_synthetic_claim():
    with pytest.raises(ValidationError, match="certainty"):
        SYNTHETIC.model_copy(update={"certainty": "high"})


@pytest.mark.parametrize("bad", [math.nan, math.inf, -math.inf])
def test_non_finite_numbers_are_refused(bad):
    with pytest.raises(ValidationError):
        measure("n", bad, [GOOD])
    with pytest.raises(ValidationError):
        Threshold(name="t", value=bad, registered_in="x")


def test_a_blank_quote_is_not_a_quote():
    with pytest.raises(ValidationError):
        Selector(exact=" ")
    with pytest.raises(ValidationError, match="exact quoted span"):
        evidence(exact=" ")


def test_restriction_does_not_depend_on_certainty():
    from conftest import search
    from residual.vocab import World
    graded = claim("Graded.", evidence=(evidence(),), searches=(search(),), certainty="high")
    plain = claim("Plain.", evidence=(evidence(),), searches=(search(),))
    ledger = Ledger(purpose="reconstruction", claims=(graded, plain))
    restricted, dropped = ledger.within({World.B})
    assert dropped == {}
    assert {c.label for c in restricted.claims} == {L.UNKNOWN}


def test_observed_residual_value_follows_its_counts():
    r = ObservedResidual(n_revealed=10, n_unrecalled=4, n_valid_extra=2)
    assert r.value == pytest.approx(4 / 12)
    with pytest.raises(ValidationError):
        ObservedResidual(n_revealed=10, n_unrecalled=11, n_valid_extra=0)


def test_occasions_are_distinct():
    with pytest.raises(ValidationError, match="distinct"):
        EstimatedResidual(estimator="chao1", occasions=("a", "a"), estimate=1, interval=(0, 2))


def test_area_features_are_consistent():
    base = dict(area_id="a", n_claims=0, evidence_density=0, n_independent_sources=0, source_kinds=(),
                n_boundary_sources=0, n_contradictions=0, knowledge_types=(), tacitness=(),
                n_single_source_claims=0, n_inferred=0, n_synthetic=0, n_unknown=0,
                n_undated_sources=0, rationale_present=False, earliest_source=None, latest_source=None)
    with pytest.raises(ValidationError, match="imagined-only"):
        AreaFeatures(**base, has_done_support=True, imagined_only=True)


def test_human_coder_is_unaffected():
    assert claim("Fine.", evidence=(evidence(verifier=CODER),)).label is L.LITERATURE_SUPPORTED


def test_self_verification_cannot_hide_by_omitting_the_generator():
    same = Agent(kind="model", id="gen", family=GENERATOR.family)
    c = claim("Unattributed.", evidence=(evidence(verifier=same),))
    assert c.label is L.UNKNOWN


def test_parametric_recall_and_simulation_are_model_work_and_coding_is_human():
    with pytest.raises(ValidationError):
        generation(Agent(kind="software", id="s"), "parametric_recall")
    with pytest.raises(ValidationError):
        generation(GENERATOR, "coding")


def test_verified_simulation_output_stays_synthetic():
    sim = claim("Simulated.", generation=generation(GENERATOR, "simulation", tier="T2"),
                evidence=(evidence(),))
    assert sim.label is L.SYNTHETIC_EXTRAPOLATION


def test_a_surrogate_ledger_never_reaches_a_gate():
    from residual.gates import SyntheticRefused
    sim = claim("Simulated.", generation=generation(GENERATOR, "simulation", tier="none"))
    with pytest.raises(SyntheticRefused):
        gate(Ledger(purpose="surrogate", claims=(sim,)))


def test_numbers_hidden_in_mapping_keys_are_refused():
    with pytest.raises(GateRefusal):
        gate({0.73: GOOD})


def test_evidence_cannot_predate_its_source():
    from datetime import date
    from conftest import source
    with pytest.raises(ValidationError, match="no earlier than it was published"):
        evidence(source(published=date(2030, 1, 1)))


def test_as_of_respects_validity_and_gives_reasons():
    from datetime import date
    later = claim("Later.", evidence=(evidence(),), valid_from=date(2022, 1, 1))
    dated, dropped = Ledger(purpose="reconstruction", claims=(later,)).as_of(date(2021, 1, 1))
    assert dropped == {later.claim_id: "not yet in force"}


def test_a_matcher_of_the_generators_family_is_refused():
    from residual.residual import Match, ResidualAccount
    recon = claim("Recon.", generation=generation())
    account = dict(reconstruction=Ledger(purpose="reconstruction", claims=(recon,)),
                   revealed=Ledger(purpose="gold", claims=(GOOD,)))
    same_family = Agent(kind="model", id="matcher", family=GENERATOR.family)
    with pytest.raises(ValidationError, match="another family"):
        ResidualAccount(**account, matches=(Match(reconstructed=recon.claim_id, revealed=GOOD.claim_id,
                                                  same=True, matcher=same_family),))


@pytest.mark.parametrize("kw", [
    dict(shares=(("A", 1.0),)),
    dict(shares=(("A", 0.5), ("A", 0.5))),
    dict(shares=(("A", 0.6), ("B", 0.6))),
    dict(shares=(("A", 0.5), ("B", 0.5)), correct="C"),
    dict(shares=(("A", 0.5), ("B", 0.5)), correct="A", of="wrong"),
])
def test_a_response_distribution_is_a_distribution(kw):
    from residual.claims import ResponseDistribution
    with pytest.raises(ValidationError):
        ResponseDistribution(**{"item": "q", "claim_id": "c", "of": "all", **kw})
