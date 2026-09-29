"""WHY: prohibitive or contrastive prescription without rationale (spec §2.6). Categorisation is
now decided by the semantic judge (S1); see test_lens_sel.py's docstring for the FakeJudge marker
convention."""
from conftest import a_claim, a_claim_n, fillers, ledger, run_lens, s_claim
from residual.vocab import KnowledgeType, SourceKind


def _hits(results):
    return [(c, o, cat) for c, o, cat in results if c.lens == "WHY"]


SEED = "Technicians must not bypass the interlock before verifying isolation."


def test_fires_stays_open_and_becomes_hyp_at_k_topic_2():
    seed = a_claim_n(SEED, n=2)
    hits = _hits(run_lens("WHY", ledger([seed])))
    assert len(hits) == 1
    cand, outcome, cat = hits[0]
    assert outcome.state == "open"
    assert cat == "HYP"


def test_closed_by_an_a_neighbours_span():
    seed = a_claim(SEED, source_id="s1", independence_key="k1")
    neighbour = a_claim(
        "The rationale for interlock isolation is documented.",
        exact="CLOSES_HERE: bypassing the interlock before verification can destroy the "
             "actuator because stored energy remains live.",
        source_id="s2", independence_key="k2")
    hits = _hits(run_lens("WHY", ledger([seed, neighbour, *fillers(40)])))
    assert len(hits) == 1
    assert hits[0][1].state == "closed"


def test_synthetic_closed_becomes_rg_unver():
    seed = a_claim(SEED, source_id="s1")
    synth = s_claim(
        "The rationale for interlock isolation is discussed.",
        exact="CLOSES_HERE: bypassing the interlock before verification can destroy the "
             "actuator because stored energy remains live.",
        source_id="synth-1")
    hits = _hits(run_lens("WHY", ledger([seed, synth, *fillers(40)])))
    assert len(hits) == 1
    cand, outcome, cat = hits[0]
    assert outcome.state == "synthetic-closed"
    assert cat == "RG-UNVER"


def test_k_topic_1_becomes_rg_single():
    seed = a_claim(SEED)
    hits = _hits(run_lens("WHY", ledger([seed])))
    assert len(hits) == 1
    assert hits[0][1].state == "open"
    assert hits[0][2] == "RG-SINGLE"


def test_regression_rat_gained_comma_as_and_consequence_verbs():
    # §9: "RAT gained ', as' and consequence verbs." Kept as a regression on the LEXICAL
    # comparison field only (S1: `lexical_state` no longer decides categorisation).
    seed = a_claim("Technicians must verify the load coil resistance before installing a "
                   "replacement card. A shorted load coil will destroy the replacement card, "
                   "as the coil resistance draws excess current.")
    hits = _hits(run_lens("WHY", ledger([seed, *fillers(40)])))
    assert len(hits) == 1
    assert hits[0][0].lexical_state == "closed"


def test_f6_regression_only_the_named_types_fire():
    seed = a_claim(SEED, knowledge_type=KnowledgeType.CONCEPT)
    assert _hits(run_lens("WHY", ledger([seed]))) == []


def test_f6_regression_standard_source_kind_is_excluded():
    seed = a_claim(SEED, source_kind=SourceKind.STANDARD)
    assert _hits(run_lens("WHY", ledger([seed]))) == []


def test_f6_regression_descriptive_disjunction_is_excluded():
    seed = a_claim("The record must not indicate whether the process requires or does not "
                   "require a review before archiving.")
    assert _hits(run_lens("WHY", ledger([seed]))) == []


def test_f6_regression_auth_gains_regulator_and_guideline_terms():
    seed = a_claim("Operators must not deviate from the guideline before consulting the "
                   "regulator.")
    assert _hits(run_lens("WHY", ledger([seed]))) == []


def test_s3_defect1_promo_excluded_seed_does_not_fire():
    seed = a_claim(SEED, source_id="https://www.plclogs.com/post")
    assert _hits(run_lens("WHY", ledger([seed]))) == []
