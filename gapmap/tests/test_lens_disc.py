"""DISC: undefined discrimination (spec §2.1). Categorisation is now decided by the semantic
judge (S1); see test_lens_sel.py's docstring for the FakeJudge marker convention. DISC's own
retrieval scores by the anchor term+head (not a stem-overlap test), so a "closing" sentence need
only mention the anchor to be retrieved -- the marker still decides whether the judge closes it."""
from conftest import a_claim, fillers, ledger, run_lens, s_claim


def _anchor(results, anchor):
    hits = [(c, o, cat) for c, o, cat in results if c.anchor == anchor]
    assert len(hits) <= 1
    return hits[0] if hits else None


def test_fires_stays_open_and_becomes_hyp_at_k_topic_2():
    c1 = a_claim("Loose terminal connections cause problems in the field.",
                source_id="src-1", independence_key="key-1")
    c2 = a_claim("Loose terminal issues appear intermittently in the panel.",
                source_id="src-2", independence_key="key-2")
    hit = _anchor(run_lens("DISC", ledger([c1, c2])), "loose terminal")
    assert hit is not None
    cand, outcome, cat = hit
    assert outcome.state == "open"
    assert cat == "HYP"


def test_closed_by_an_a_neighbours_span():
    c1 = a_claim("Loose terminal connections cause problems in the field.", source_id="src-1")
    c2 = a_claim(
        "Loose terminal gaps are documented.",
        exact="CLOSES_HERE: a loose terminal gap must measure at least 5 millimeters.",
        source_id="src-2")
    hit = _anchor(run_lens("DISC", ledger([c1, c2, *fillers(40)])), "loose terminal")
    assert hit is not None
    assert hit[1].state == "closed"


def test_synthetic_closed_becomes_rg_unver():
    c1 = a_claim("Loose terminal connections cause problems in the field.",
                source_id="src-1", independence_key="key-1")
    c2 = a_claim("Loose terminal issues appear intermittently in the panel.",
                source_id="src-2", independence_key="key-2")
    s1 = s_claim(
        "Loose terminal spacing is discussed.",
        exact="CLOSES_HERE: loose terminal spacing must be at least 5 millimeters.",
        source_id="synth-1")
    hit = _anchor(run_lens("DISC", ledger([c1, c2, s1])), "loose terminal")
    assert hit is not None
    cand, outcome, cat = hit
    assert outcome.state == "synthetic-closed"
    assert cat == "RG-UNVER"


def test_k_topic_1_becomes_rg_single():
    c1 = a_claim("Loose terminal connections cause problems in the field.",
                source_id="src-1", independence_key="same-key")
    c2 = a_claim("Loose terminal issues appear intermittently in the panel.",
                source_id="src-2", independence_key="same-key")
    hit = _anchor(run_lens("DISC", ledger([c1, c2])), "loose terminal")
    assert hit is not None
    cand, outcome, cat = hit
    assert outcome.state == "open"
    assert cat == "RG-SINGLE"


def test_regression_article_number_does_not_close_high_risk_lexically():
    # §8: "QUANT narrowed from 'any digit'. Article numbers had closed 'high risk'." Kept as a
    # regression on the LEXICAL comparison field only (S1: `lexical_state` no longer decides
    # categorisation).
    c1 = a_claim("Processing likely to result in a high risk requires an assessment under Article 35(3).",
                source_id="src-1")
    c2 = a_claim("A hospital's processing is high risk given the volume of data involved.",
                source_id="src-2")
    hit = _anchor(run_lens("DISC", ledger([c1, c2])), "high risk")
    assert hit is not None
    assert hit[0].lexical_state != "closed"


def test_f4_regression_case_in_the_anchor_sentence_lexically_closes():
    # F4: a stated contrast (CASE) in the anchor's sentence closes the LEXICAL comparison field.
    c1 = a_claim("Loose terminal connections cause problems in the field.", source_id="src-1")
    c2 = a_claim("A loose terminal is one that has visible play, whereas a tight terminal shows "
                "none.", source_id="src-2")
    hit = _anchor(run_lens("DISC", ledger([c1, c2])), "loose terminal")
    assert hit is not None
    assert hit[0].lexical_state == "closed"


def test_f4_regression_bare_definer_runs_over_the_whole_a_pool():
    # F4: the bare-term definer used to require the anchor bigram in the same claim; now it is
    # searched over every A claim. Kept as a regression on the LEXICAL comparison field.
    c1 = a_claim("Loose terminal connections cause problems in the field.",
                source_id="src-1", independence_key="key-1")
    c2 = a_claim("Loose terminal issues appear intermittently in the panel.",
                source_id="src-2", independence_key="key-2")
    definer = a_claim("Loose is when a fastener no longer holds its rated torque.", source_id="src-3")
    hit = _anchor(run_lens("DISC", ledger([c1, c2, definer])), "loose terminal")
    assert hit is not None
    cand, _outcome, _cat = hit
    assert cand.lexical_state == "partial"
    assert definer.claim_id in cand.lexical_partial_hits


def test_s3_defect5_stop_anchors_never_fire():
    c1 = a_claim("The audit should occur at the appropriate time in the cycle.", source_id="src-1")
    c2 = a_claim("Scheduling review happens at the appropriate time each quarter.", source_id="src-2")
    assert _anchor(run_lens("DISC", ledger([c1, c2])), "appropriate time") is None
    c3 = a_claim("The panel has a sensitive control near the door.", source_id="src-3")
    c4 = a_claim("A sensitive control should not be exposed to moisture.", source_id="src-4")
    assert _anchor(run_lens("DISC", ledger([c3, c4])), "sensitive control") is None


def test_s3_defect5_defn_now_matches_concerns():
    c1 = a_claim("Loose terminal connections cause problems in the field.", source_id="src-1")
    c2 = a_claim("A loose terminal concerns the mechanical grip of the ferrule.", source_id="src-2")
    hit = _anchor(run_lens("DISC", ledger([c1, c2])), "loose terminal")
    assert hit is not None
    assert hit[0].lexical_state == "partial"


def test_s3_defect1_promo_excluded_claim_does_not_seed_an_anchor():
    c1 = a_claim("Loose terminal connections cause problems in the field.",
                source_id="https://www.plclogs.com/post")
    c2 = a_claim("Loose terminal issues appear intermittently in the panel.", source_id="src-2")
    assert _anchor(run_lens("DISC", ledger([c1, c2])), "loose terminal") is None
