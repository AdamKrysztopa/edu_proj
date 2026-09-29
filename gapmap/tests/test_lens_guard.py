"""GUARD: named error without a detection cue (spec §2.5). Categorisation is now decided by the
semantic judge (S1); see test_lens_sel.py's docstring for the FakeJudge marker convention."""
from conftest import a_claim, a_claim_n, fillers, ledger, run_lens, s_claim
from residual.vocab import KnowledgeType


def _hits(results):
    return [(c, o, cat) for c, o, cat in results if c.lens == "GUARD"]


SEED = ("A frequent mistake in troubleshooting is panicking and abandoning systematic "
       "approaches in favor of quick fixes.")


def test_fires_stays_open_and_becomes_hyp_at_k_topic_2():
    seed = a_claim_n(SEED, n=2)
    hits = _hits(run_lens("GUARD", ledger([seed])))
    assert len(hits) == 1
    cand, outcome, cat = hits[0]
    assert outcome.state == "open"
    assert cat == "HYP"


def test_closed_by_an_a_neighbours_span():
    seed = a_claim(SEED, source_id="s1", independence_key="k1")
    neighbour = a_claim(
        "Panicking behavior during troubleshooting is documented.",
        exact="CLOSES_HERE: technicians notice panicking and immediately refocus.",
        source_id="s2", independence_key="k2")
    hits = _hits(run_lens("GUARD", ledger([seed, neighbour, *fillers(40)])))
    assert len(hits) == 1
    assert hits[0][1].state == "closed"


def test_synthetic_closed_becomes_rg_unver():
    seed = a_claim(SEED, source_id="s1")
    synth = s_claim(
        "Panicking behavior during troubleshooting is discussed.",
        exact="CLOSES_HERE: technicians notice panicking and immediately refocus.",
        source_id="synth-1")
    hits = _hits(run_lens("GUARD", ledger([seed, synth, *fillers(40)])))
    assert len(hits) == 1
    cand, outcome, cat = hits[0]
    assert outcome.state == "synthetic-closed"
    assert cat == "RG-UNVER"


def test_k_topic_1_becomes_rg_single():
    seed = a_claim(SEED)
    hits = _hits(run_lens("GUARD", ledger([seed])))
    assert len(hits) == 1
    assert hits[0][1].state == "open"
    assert hits[0][2] == "RG-SINGLE"


def test_regression_err_dropped_assume_avoid_never_do_not():
    # §8: "'assum*', 'avoid', 'never' and 'do not' were dropped from ERR. They fired on
    # procedures and legal negations."
    claim = a_claim("Never bypass the interlock without verifying isolation first; do not "
                    "assume the circuit is dead and avoid skipping the lockout step.")
    assert _hits(run_lens("GUARD", ledger([claim]))) == []


def test_f6_regression_err_alone_without_a_human_agent_does_not_fire():
    # F6: "misconception type alone no longer fires" AND ERR must co-occur with a human
    # agent/action; this claim matches ERR ("pitfall") but names no one and nothing that acts.
    claim = a_claim("A common pitfall in the specification is an ambiguous default value.",
                    knowledge_type=KnowledgeType.MISCONCEPTION)
    assert _hits(run_lens("GUARD", ledger([claim]))) == []


def test_f6_regression_misconception_type_alone_no_longer_fires():
    claim = a_claim("The default configuration silently disables the watchdog timer.",
                    knowledge_type=KnowledgeType.MISCONCEPTION)
    assert _hits(run_lens("GUARD", ledger([claim]))) == []


def test_s3_defect1_promo_domain_seed_does_not_fire():
    claim = a_claim(SEED, source_id="https://www.plclogs.com/post")
    assert _hits(run_lens("GUARD", ledger([claim]))) == []
