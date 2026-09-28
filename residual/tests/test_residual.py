from datetime import date

import pytest
from conftest import CODER, GENERATOR, SCOPE, claim, evidence, generation, search, source
from pydantic import ValidationError

from residual.gapmap import AreaFeatures
from residual.gates import GateDecision, Measurement, evidential_gate
from residual.ledger import Area, Contradiction, Ledger
from residual.provenance import Agent, Verdict
from residual.residual import (
    Coverage,
    EstimatedResidual,
    GapMapPrediction,
    Match,
    ResidualAccount,
    ResidualNotMeasurable,
    ValidityJudgement,
    coverage,
)
from residual.vocab import EpistemicLabel, KnowledgeType, Question, SourceKind, Tacitness, World

L = EpistemicLabel
K = KnowledgeType


def gold_claim(assertion, kt=K.PROCEDURE_STEP):
    return claim(assertion, knowledge_type=kt, evidence=(evidence(source(f"gold-{assertion}")),))


H = (gold_claim("H1."), gold_claim("H2."), gold_claim("H3.", K.CUE))
R = tuple(claim(a, generation=generation()) for a in ("R1.", "R2.", "R3."))
GOLD = Ledger(purpose="gold", claims=H)
RECON = Ledger(purpose="reconstruction", claims=R)


def match(r, h, same=True, blind=True):
    return Match(reconstructed=r.claim_id, revealed=h.claim_id, same=same, matcher=CODER,
                 blind=blind)


def judge(c, valid):
    return ValidityJudgement(claim_id=c.claim_id, valid=valid, rater=CODER)


def account(matches=(), validity=()):
    return ResidualAccount(reconstruction=RECON, revealed=GOLD, matches=tuple(matches),
                           validity=tuple(validity))


@pytest.mark.parametrize(("recon", "gold"), [
    (GOLD, GOLD), (RECON, RECON), (Ledger(purpose="surrogate"), GOLD),
])
def test_an_account_compares_a_reconstruction_with_gold(recon, gold):
    with pytest.raises(ValidationError, match="reconstruction ledger with a gold"):
        ResidualAccount(reconstruction=recon, revealed=gold, matches=())


def test_an_empty_h_is_refused():
    with pytest.raises(ValidationError, match="empty"):
        ResidualAccount(reconstruction=RECON, revealed=Ledger(purpose="gold"), matches=())


def test_matches_are_blind():
    with pytest.raises(ValidationError, match="blind"):
        account([match(R[0], H[0], blind=False)])


def test_matches_name_present_claims():
    with pytest.raises(ValidationError, match="absent claim"):
        account([match(H[0], H[0])])
    with pytest.raises(ValidationError, match="absent claim"):
        account([match(R[0], R[1])])


def test_validity_judgements_are_unique_and_name_present_claims():
    with pytest.raises(ValidationError, match="one validity judgement"):
        account(validity=[judge(R[0], True), judge(R[0], False)])
    with pytest.raises(ValidationError, match="absent claims"):
        account(validity=[judge(H[0], True)])


@pytest.mark.parametrize("rater", [GENERATOR, Agent(kind="software", id="judge")])
def test_validity_is_judged_by_humans(rater):
    with pytest.raises(ValidationError, match="humans"):
        ValidityJudgement(claim_id="c", valid=True, rater=rater)


def test_recall_is_a_measurement_over_h_with_predictor_labels_from_r():
    m = account([match(R[0], H[0]), match(R[1], H[1], same=False)]).recall()
    assert isinstance(m, Measurement)
    assert m.value == pytest.approx(1 / 3)
    assert set(m.criterion_ids) == {c.claim_id for c in H}
    assert m.criterion_labels == {L.LITERATURE_SUPPORTED}
    assert m.predictor_labels == {L.SYNTHETIC_EXTRAPOLATION}


def test_a_synthetic_reconstruction_still_yields_a_gate_readable_recall():
    @evidential_gate
    def n3(recall):
        return GateDecision(gate="n3", outcome="continue", reason="r")

    decision = n3(account([match(R[0], H[0])]).recall())
    assert set(decision.criterion_ids) == {c.claim_id for c in H}


def test_recall_by_knowledge_type():
    acc = account([match(R[0], H[2])])
    cue = acc.recall(K.CUE)
    assert cue.value == 1.0 and cue.criterion_ids == (H[2].claim_id,)
    assert acc.recall(K.PROCEDURE_STEP).value == 0.0
    with pytest.raises(ResidualNotMeasurable):
        acc.recall(K.NORM)


def test_unrecalled_and_unmatched_reconstruction():
    acc = account([match(R[0], H[0]), match(R[1], H[1], same=False)])
    assert acc.unrecalled() == tuple(sorted((H[1].claim_id, H[2].claim_id)))
    assert acc.unmatched_reconstruction() == tuple(sorted((R[1].claim_id, R[2].claim_id)))
    assert acc.recalled() == {H[0].claim_id}


def test_observed_residual_needs_human_validity_judgements():
    with pytest.raises(ResidualNotMeasurable, match="validity"):
        account([match(R[0], H[0])]).observed_residual()
    with pytest.raises(ResidualNotMeasurable):
        account([match(R[0], H[0])], [judge(R[1], True)]).observed_residual()


def test_observed_residual_value():
    res = account([match(R[0], H[0])], [judge(R[1], True), judge(R[2], False)]).observed_residual()
    assert (res.n_revealed, res.n_unrecalled, res.n_valid_extra) == (3, 2, 1)
    assert res.value == pytest.approx(2 / 4)
    everything = account([match(r, h) for r, h in zip(R, H, strict=True)]).observed_residual()
    assert everything.value == 0.0


def estimated(**kw):
    return EstimatedResidual(**({"estimator": "chao1", "occasions": ("a", "b"), "estimate": 5.0,
                                 "interval": (3.0, 8.0)} | kw))


def test_estimated_residual():
    assert estimated().known_truth_passed is None
    assert estimated(gold_uncaptured=6, tolerance=1.0).known_truth_passed is True
    assert estimated(gold_uncaptured=7, tolerance=1.0).known_truth_passed is False
    for kw in ({"gold_uncaptured": 6}, {"tolerance": 1.0}):
        with pytest.raises(ValidationError, match="known-truth"):
            estimated(**kw)
    for interval in ((6.0, 8.0), (1.0, 4.0), (8.0, 3.0)):
        with pytest.raises(ValidationError, match="interval"):
            estimated(interval=interval)
    with pytest.raises(ValidationError):
        estimated(occasions=("a",))


def features(area_id="a1"):
    return AreaFeatures(area_id=area_id, n_claims=0, evidence_density=0, n_independent_sources=0,
                        source_kinds=(), n_boundary_sources=0, n_contradictions=0,
                        knowledge_types=(), tacitness=(), has_done_support=False,
                        imagined_only=False, n_single_source_claims=0, n_inferred=0, n_synthetic=0,
                        n_unknown=0, earliest_source=None, latest_source=None, n_undated_sources=0,
                        rationale_present=False)


def test_gap_map_prediction():
    GapMapPrediction(area_id="a1", p_missing=0.3, predictor="p", feature_set_sha256="0",
                     features=features())
    with pytest.raises(ValidationError, match="another area"):
        GapMapPrediction(area_id="a2", p_missing=0.3, predictor="p", feature_set_sha256="0",
                         features=features())
    for p in (-0.01, 1.01):
        with pytest.raises(ValidationError):
            GapMapPrediction(area_id="a1", p_missing=p, predictor="p", feature_set_sha256="0",
                             features=features())


def in_area(*claims, contradictions=()):
    return Ledger(purpose="reconstruction", claims=claims, areas=(
        Area(area_id="a1", scope=SCOPE, name="a1"), Area(area_id="a2", scope=SCOPE, name="a2")),
        assignments=tuple((c.claim_id, "a1") for c in claims), contradictions=contradictions)


BOOK1, BOOK2 = (source(f"book{i}", kind=SourceKind.TEXTBOOK) for i in (1, 2))
LOG = source("log", kind=SourceKind.LOG)


def two_sources(assertion="C.", *srcs, **kw):
    kw.setdefault("question", Question.DOMAIN)
    return claim(assertion, evidence=tuple(evidence(s) for s in srcs or (BOOK1, BOOK2)), **kw)


def test_coverage_unknown():
    assert coverage(in_area(), "a1") is Coverage.UNKNOWN
    ledger = in_area(two_sources())
    assert coverage(ledger, "a2") is Coverage.UNKNOWN
    unsupported = in_area(claim("G.", generation=generation()), claim("S.", searches=(search(),)))
    assert coverage(unsupported, "a1") is Coverage.UNKNOWN


def test_coverage_contradicted():
    a, b = two_sources("A."), two_sources("B.")
    x = Contradiction(claims=(a.claim_id, b.claim_id), detected_by=CODER, method="nli")
    assert coverage(in_area(a, b, contradictions=(x,)), "a1") is Coverage.CONTRADICTED
    refuted = claim("R.", question=Question.DOMAIN, evidence=(
        evidence(BOOK1), evidence(BOOK2), evidence(source("r"), verdict=Verdict.REFUTES)))
    assert coverage(in_area(refuted), "a1") is Coverage.CONTRADICTED


def test_coverage_weak_on_a_single_source():
    assert coverage(in_area(two_sources("C.", BOOK1)), "a1") is Coverage.WEAK
    same_key = source("book3", kind=SourceKind.TEXTBOOK, independence_key="book1")
    assert coverage(in_area(two_sources("C.", BOOK1, same_key)), "a1") is Coverage.WEAK


@pytest.mark.parametrize("tacitness", [Tacitness.AUTOMATED, Tacitness.PERCEPTUAL,
                                       Tacitness.SOMATIC, Tacitness.COLLECTIVE])
def test_behaviour_only_knowledge_needs_done_support(tacitness):
    tacit = claim("T.", tacitness=tacitness, generation=generation())
    assert coverage(in_area(two_sources(), tacit), "a1") is Coverage.WEAK
    assert coverage(in_area(two_sources("C.", BOOK1, LOG), tacit), "a1") is Coverage.COVERED


def test_performance_needs_done_support():
    imagined = two_sources(question=Question.PERFORMANCE)
    assert coverage(in_area(imagined), "a1") is Coverage.WEAK
    done = two_sources("C.", BOOK1, LOG, question=Question.PERFORMANCE)
    assert coverage(in_area(done), "a1") is Coverage.COVERED


def test_coverage_covered():
    assert coverage(in_area(two_sources(tacitness=Tacitness.RELATIONAL)), "a1") is Coverage.COVERED
    human = source("int", kind=SourceKind.INTERVIEW, world=World.C, published=date(2026, 1, 1))
    assert coverage(in_area(two_sources("C.", BOOK1, human)), "a1") is Coverage.COVERED
