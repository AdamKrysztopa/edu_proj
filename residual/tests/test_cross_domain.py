"""The N1 gate (REORIENTATION.md §22): every illustrative gold item of docs/n1-gold-shapes.md,
from mathematics, clinical and OSS sources, is expressible in the schema, and the uses the
NOW experiments make of those items work without domain-specific code."""
from datetime import date

import pytest
from conftest import CODER, DAY, GENERATOR, generation

import cross_domain as x
from residual.claims import ClaimRecord
from residual.gates import GateDecision, SyntheticRefused, Threshold, evidential_gate, measure
from residual.ledger import Contradiction, Ledger
from residual.residual import Coverage, Match, ResidualAccount, coverage
from residual.vocab import CRITERION_LABELS, BEHAVIOUR_ONLY, EpistemicLabel, KnowledgeType, Question

GOLDS = {"mathematics": x.MATHS_GOLD, "clinical": x.CLINICAL_GOLD, "oss": x.OSS_GOLD}


@pytest.mark.parametrize("domain", GOLDS)
def test_every_gold_item_is_a_supported_claim(domain):
    ledger = GOLDS[domain]
    assert ledger.claims
    assert all(ledger.label(c.claim_id) in CRITERION_LABELS for c in ledger.claims)


@pytest.mark.parametrize("domain", GOLDS)
def test_gold_ledgers_round_trip(domain):
    ledger = GOLDS[domain]
    assert Ledger.from_json(ledger.to_json()) == ledger


def test_each_world_labels_its_own_domain():
    labels = {d: {g.label(c.claim_id) for c in g.claims} for d, g in GOLDS.items()}
    assert EpistemicLabel.OBSERVED_HUMAN_EVIDENCE in labels["mathematics"]
    assert labels["clinical"] == {EpistemicLabel.LITERATURE_SUPPORTED}
    assert labels["oss"] == {EpistemicLabel.ORGANISATIONAL_ARTEFACT_SUPPORTED}


def test_procedural_and_tacit_knowledge_not_only_concepts():
    claims = [c for g in GOLDS.values() for c in g.claims]
    types = {c.knowledge_type for c in claims}
    assert {KnowledgeType.CUE, KnowledgeType.DECISION, KnowledgeType.CHECK, KnowledgeType.INTERPRETATION,
            KnowledgeType.NORM, KnowledgeType.FAILURE_MODE, KnowledgeType.RATIONALE,
            KnowledgeType.PROCEDURE_STEP} <= types
    assert {c.tacitness for c in claims} >= BEHAVIOUR_ONLY - {x.Tacitness.SOMATIC}


def test_expert_account_of_difficulty_is_not_evidence_of_difficulty():
    assert x.FLASHOVER_WHY.label is EpistemicLabel.UNKNOWN
    assert x.FLASHOVER_WHY.excluded[0][1] == "difficulty is answered only by learner data"
    with pytest.raises(ValueError, match="gold holds only supported claims"):
        Ledger(purpose="gold", claims=(x.FLASHOVER_WHY,))


def test_misconception_taxonomy_and_its_prevalence_answer_different_questions():
    assert x.FCI_IMPETUS.question is Question.DOMAIN
    assert x.AAAS_CHOICE.question is Question.DOMAIN
    assert x.AAAS_DISTRIBUTION.question is Question.DIFFICULTY
    as_difficulty = x.FCI_IMPETUS.model_copy(update={"question": Question.DIFFICULTY})
    assert ClaimRecord.model_validate(as_difficulty.model_dump()).label is EpistemicLabel.UNKNOWN


def test_double_coding_does_not_inflate_corroboration():
    coders = {e.verification.verifier.id for e in x.RATIONALE_SOUGHT.evidence}
    assert coders == {"coder-1", "coder-2"}
    assert x.RATIONALE_SOUGHT.corroboration == 1
    assert x.CHANGELOG_NORM.corroboration == 4


def test_e_oss_outcomes_split_at_the_freeze_time():
    before, dropped = x.OSS_GOLD.as_of(x.T)
    assert set(dropped) == {x.RATIONALE_SOUGHT.claim_id, x.DEFECT_FIX.claim_id,
                            x.CHANGELOG_NORM.claim_id, x.LEGACY_DOC.claim_id,
                            x.LEGACY_REMOVED.claim_id, x.APPEND_ONLY.claim_id,
                            x.APPEND_ONLY_WHY.claim_id}
    assert [c.claim_id for c in before.in_area(x.RETRY_UNIT.area_id)] == [x.CAP_CHANGE.claim_id]
    post = [c for c in x.OSS_GOLD.in_area(x.RETRY_UNIT.area_id)
            if min(e.source.published for e in c.evidence) > x.T]
    assert {c.knowledge_type for c in post} == {KnowledgeType.RATIONALE, KnowledgeType.FAILURE_MODE}


def test_doc_versus_practice_divergence_is_a_contradiction():
    ledger = Ledger.model_validate(
        x.OSS_GOLD.model_dump() | {"contradictions": [Contradiction(
            claims=(x.LEGACY_DOC.claim_id, x.LEGACY_REMOVED.claim_id), detected_by=CODER,
            method=x.DOC_CONTRADICTION_METHOD).model_dump()]})
    assert ledger.contradicted() == {x.LEGACY_DOC.claim_id, x.LEGACY_REMOVED.claim_id}
    assert x.LEGACY_REMOVED.in_force(date(2020, 6, 1)) and not x.LEGACY_REMOVED.in_force(date(2019, 6, 1))


def test_behaviour_only_areas_are_never_covered_by_reports_alone():
    assert coverage(x.CLINICAL_GOLD, "cric:airway-access") is Coverage.WEAK
    assert coverage(x.CLINICAL_GOLD, "fire:flashover") is Coverage.WEAK


def _eedi_account(reconstructed: ClaimRecord) -> ResidualAccount:
    gold = Ledger(purpose="gold", claims=(x.ADD_DENOMINATORS, x.ROUNDING))
    recon = Ledger(purpose="reconstruction", claims=(reconstructed,))
    return ResidualAccount(reconstruction=recon, revealed=gold, matches=(Match(
        reconstructed=reconstructed.claim_id, revealed=x.ADD_DENOMINATORS.claim_id, same=True,
        matcher=CODER, blind=True),))


PARAMETRIC = ClaimRecord(assertion="Students add numerators and denominators separately.",
                         question=Question.DIFFICULTY, layer=x.Layer.LEARNER,
                         knowledge_type=KnowledgeType.MISCONCEPTION, scope=x.MATHS,
                         generation=generation(GENERATOR, "parametric_recall"))


@evidential_gate
def e_misc(recall, floor):
    return GateDecision(gate="E-MISC", outcome="continue" if recall.value >= floor.value else "change",
                        reason="prevalence-weighted recall against the registered floor")


def test_e_misc_weighted_recall_reads_a_synthetic_reconstruction_through_a_gate():
    account = _eedi_account(PARAMETRIC)
    recall = account.recall(weights=x.prevalence())
    assert recall.value == pytest.approx(0.31 / 0.60)
    assert EpistemicLabel.SYNTHETIC_EXTRAPOLATION in recall.predictor_labels
    floor = Threshold(name="E-MISC prevalence-weighted recall", value=0.6,
                        registered_in="REORIENTATION.md §22 threshold table")
    assert e_misc(recall, floor).outcome == "change"


def test_a_surrogate_prevalence_can_never_weight_a_gate():
    simulated = ClaimRecord(assertion="31% of simulated students add denominators.",
                            question=Question.DIFFICULTY, layer=x.Layer.LEARNER,
                            knowledge_type=KnowledgeType.MISCONCEPTION, scope=x.MATHS,
                            generation=generation(GENERATOR, "simulation", tier="none"))
    weights = x.prevalence() | {x.ADD_DENOMINATORS.claim_id: measure(
        "prevalence", 0.31, [x.ADD_DENOMINATORS, simulated])}
    recall = _eedi_account(PARAMETRIC).recall(weights=weights)
    floor = Threshold(name="floor", value=0.6, registered_in="REORIENTATION.md §22")
    with pytest.raises(SyntheticRefused):
        e_misc(recall, floor)


def test_memorisation_probe_is_a_measurement_over_the_gold_item():
    probe = measure("memorisation_probe_positive", 1.0, [x.STABILISE])
    assert probe.criterion_ids == (x.STABILISE.claim_id,)


def test_fixtures_are_dated_before_today():
    sources = {e.source for g in GOLDS.values() for c in g.claims for e in c.evidence}
    assert all(s.published and s.published <= DAY for s in sources)
