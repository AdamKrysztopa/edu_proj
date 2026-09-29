"""HEDGE: hedged rule, exception condition absent (spec §2.4). Categorisation is now decided by
the semantic judge (S1); see test_lens_sel.py's docstring for the FakeJudge marker convention."""
from conftest import a_claim, a_claim_n, fillers, ledger, run_lens, s_claim


def _hits(results):
    return [(c, o, cat) for c, o, cat in results if c.lens == "HEDGE"]


SEED = "In most cases, a combination of two factors indicates the need for a review."


def test_fires_stays_open_and_becomes_hyp_at_k_topic_2():
    seed = a_claim_n(SEED, n=2)
    hits = _hits(run_lens("HEDGE", ledger([seed])))
    assert len(hits) == 1
    cand, outcome, cat = hits[0]
    assert outcome.state == "open"
    assert cat == "HYP"


def test_closed_by_an_a_neighbours_span():
    seed = a_claim(SEED, source_id="s1", independence_key="k1")
    neighbour = a_claim(
        "The exception to the two-factor review rule is documented.",
        exact="CLOSES_HERE: unless the combination of two factors is trivial, skip the review.",
        source_id="s2", independence_key="k2")
    hits = _hits(run_lens("HEDGE", ledger([seed, neighbour, *fillers(40)])))
    assert len(hits) == 1
    assert hits[0][1].state == "closed"


def test_synthetic_closed_becomes_rg_unver():
    seed = a_claim(SEED, source_id="s1")
    synth = s_claim(
        "The exception to the two-factor review rule is discussed.",
        exact="CLOSES_HERE: unless the combination of two factors is trivial, skip the review.",
        source_id="synth-1")
    hits = _hits(run_lens("HEDGE", ledger([seed, synth, *fillers(40)])))
    assert len(hits) == 1
    cand, outcome, cat = hits[0]
    assert outcome.state == "synthetic-closed"
    assert cat == "RG-UNVER"


def test_k_topic_1_becomes_rg_single():
    seed = a_claim(SEED)
    hits = _hits(run_lens("HEDGE", ledger([seed])))
    assert len(hits) == 1
    assert hits[0][1].state == "open"
    assert hits[0][2] == "RG-SINGLE"


def test_regression_exc_ignores_exception_in_article():
    # §8: "EXC ignores 'exception in Article …'. That legal cross-reference had falsely closed
    # the WP248 two-criteria rule." Kept as a regression on the LEXICAL comparison field only
    # (S1: `lexical_state` no longer decides categorisation).
    seed = a_claim(SEED, source_id="s1", independence_key="k1")
    neighbour = a_claim("There is an exception in Article 35(10) for two-factor combination "
                        "reviews.", source_id="s2", independence_key="k2")
    hits = _hits(run_lens("HEDGE", ledger([seed, neighbour, *fillers(40)])))
    assert len(hits) == 1
    assert hits[0][0].lexical_state == "open"
