"""SEL: selection criterion named, mapping absent (spec §2.3). Categorisation is now decided by
the semantic judge (S1): `run_lens` judges every fired candidate with the default `FakeJudge`,
which closes/partials a retrieved sentence containing the literal marker CLOSES_HERE/PARTIAL_HERE."""
from conftest import a_claim, a_claim_n, fillers, ledger, run_lens, s_claim


def _hits(results):
    return [(c, o, cat) for c, o, cat in results if c.lens == "SEL"]


def test_fires_stays_open_and_becomes_hyp_at_k_topic_2():
    seed = a_claim_n("Diagnostic tests should be selected based on failure likelihood.", n=2)
    hits = _hits(run_lens("SEL", ledger([seed])))
    assert len(hits) == 1
    cand, outcome, cat = hits[0]
    assert outcome.state == "open"
    assert cat == "HYP"


def test_closed_by_an_a_neighbours_span():
    seed = a_claim("Diagnostic tests should be selected based on failure likelihood.",
                   source_id="s1", independence_key="k1")
    neighbour = a_claim(
        "Selection practice for failure likelihood is documented.",
        exact="CLOSES_HERE: choose the test whose failure likelihood is highest.",
        source_id="s2", independence_key="k2")
    hits = _hits(run_lens("SEL", ledger([seed, neighbour, *fillers(40)])))
    assert len(hits) == 1
    assert hits[0][1].state == "closed"


def test_synthetic_closed_becomes_rg_unver():
    seed = a_claim("Diagnostic tests should be selected based on failure likelihood.", source_id="s1")
    synth = s_claim(
        "Selection practice for failure likelihood is discussed.",
        exact="CLOSES_HERE: pick the test with the highest failure likelihood.",
        source_id="synth-1")
    hits = _hits(run_lens("SEL", ledger([seed, synth, *fillers(40)])))
    assert len(hits) == 1
    cand, outcome, cat = hits[0]
    assert outcome.state == "synthetic-closed"
    assert cat == "RG-UNVER"


def test_k_topic_1_becomes_rg_single():
    seed = a_claim("Diagnostic tests should be selected based on failure likelihood.")
    hits = _hits(run_lens("SEL", ledger([seed])))
    assert len(hits) == 1
    assert hits[0][1].state == "open"
    assert hits[0][2] == "RG-SINGLE"


def test_regression_requires_a_prescription():
    non_prescriptive = a_claim("The technician selected the sampling rate based on the "
                               "suspected event.", knowledge_type="concept")
    assert _hits(run_lens("SEL", ledger([non_prescriptive]))) == []


def test_regression_lexical_comparison_field_gained_comparatives():
    # §9: c-111d883494ccf58b was open until COND gained comparatives. This is now only a
    # regression on the LEXICAL comparison field (S1: `lexical_state` no longer decides
    # categorisation -- the judge does).
    seed = a_claim("Testing should proceed from the most likely failure location toward the "
                   "least likely. The most likely failure location is far more likely to fail "
                   "than the least likely location.")
    hits = _hits(run_lens("SEL", ledger([seed, *fillers(40)])))
    assert len(hits) == 1
    assert hits[0][0].lexical_state == "closed"
