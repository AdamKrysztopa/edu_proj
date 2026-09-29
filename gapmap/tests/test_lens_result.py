"""RESULT: PARI result interpretation, "A -> B -> C, but what decides B vs D" (spec §2.8, F7).
Categorisation is now decided by the semantic judge (S1); see test_lens_sel.py's docstring for
the FakeJudge marker convention."""
from conftest import a_claim, a_claim_n, fillers, ledger, run_lens, s_claim
from residual.vocab import KnowledgeType

SEED = "Technicians should measure the coil resistance before replacing the card."


def _hits(results):
    return [(c, o, cat) for c, o, cat in results if c.lens == "RESULT"]


def test_fires_stays_open_and_becomes_hyp_at_k_topic_2():
    seed = a_claim_n(SEED, n=2, knowledge_type=KnowledgeType.CHECK)
    hits = _hits(run_lens("RESULT", ledger([seed, *fillers(40)])))
    assert len(hits) == 1
    cand, outcome, cat = hits[0]
    assert outcome.state == "open"
    assert cat == "HYP"
    assert "measure the coil resistance" in cand.anchor


def test_closed_by_an_a_neighbours_span():
    seed = a_claim(SEED, source_id="s1", independence_key="k1", knowledge_type=KnowledgeType.CHECK)
    neighbour = a_claim(
        "Coil resistance interpretation is documented.",
        exact="CLOSES_HERE: a coil resistance reading below expected indicates a shorted winding.",
        source_id="s2", independence_key="k2")
    hits = _hits(run_lens("RESULT", ledger([seed, neighbour, *fillers(40)])))
    assert len(hits) == 1
    assert hits[0][1].state == "closed"


def test_synthetic_closed_becomes_rg_unver():
    seed = a_claim(SEED, source_id="s1", knowledge_type=KnowledgeType.CHECK)
    synth = s_claim(
        "Coil resistance interpretation is discussed.",
        exact="CLOSES_HERE: a coil resistance reading below expected indicates a shorted winding.",
        source_id="synth-1")
    hits = _hits(run_lens("RESULT", ledger([seed, synth, *fillers(40)])))
    assert len(hits) == 1
    cand, outcome, cat = hits[0]
    assert outcome.state == "synthetic-closed"
    assert cat == "RG-UNVER"


def test_k_topic_1_becomes_rg_single():
    seed = a_claim(SEED, knowledge_type=KnowledgeType.CHECK)
    hits = _hits(run_lens("RESULT", ledger([seed, *fillers(40)])))
    assert len(hits) == 1
    assert hits[0][1].state == "open"
    assert hits[0][2] == "RG-SINGLE"


def test_regression_object_must_be_within_the_6_token_window():
    # §2.8: the verb must be followed within 6 tokens by >= 1 non-common content stem (the
    # object); a bare test verb with no nearby object does not fire.
    seed = a_claim("Technicians should measure it as needed for the ongoing overall general "
                   "routine periodic scheduled maintenance visit today.", knowledge_type=KnowledgeType.CHECK)
    assert _hits(run_lens("RESULT", ledger([seed]))) == []


def test_regression_only_procedure_check_strategy_or_decision_types_fire():
    seed = a_claim(SEED, knowledge_type=KnowledgeType.CONCEPT)
    assert _hits(run_lens("RESULT", ledger([seed]))) == []


def test_s3_defect2_precondition_text_does_not_fire():
    # S3 defect 2: "should only be performed when a circuit is de-energized" is a precondition,
    # not a prescriptive result-yielding test -- excluded regardless of MODAL.
    seed = a_claim("This test should only be performed when a circuit is de-energized.",
                   knowledge_type=KnowledgeType.CHECK)
    assert _hits(run_lens("RESULT", ledger([seed]))) == []
    seed2 = a_claim("Do not measure the coil resistance before using the calibrated meter.",
                    knowledge_type=KnowledgeType.CHECK)
    assert _hits(run_lens("RESULT", ledger([seed2]))) == []


def test_s3_defect2_imperative_sentence_opening_with_the_test_verb_fires():
    # S3 defect 2: RESULT now also fires on an imperative sentence that OPENS with the TEST verb
    # (no MODAL needed), as long as it is not a precondition.
    seed = a_claim("Measure the coil resistance before replacing the card.",
                   knowledge_type=KnowledgeType.CHECK)
    hits = _hits(run_lens("RESULT", ledger([seed, *fillers(40)])))
    assert len(hits) == 1


def test_s3_defect1_promo_excluded_seed_does_not_fire():
    seed = a_claim(SEED, source_id="https://www.plclogs.com/post", knowledge_type=KnowledgeType.CHECK)
    assert _hits(run_lens("RESULT", ledger([seed]))) == []
