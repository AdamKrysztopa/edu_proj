"""record.py: tier separation, gap_id stability and the confidence rubric (spec §4, §5, §11.4)."""
from conftest import FakeJudge, a_claim, a_claim_n, area, fillers, ledger, s_claim
from residual.vocab import EpistemicLabel, KnowledgeType

from gapmap import config, lenses, link, record, semantic


def _build(lens_name, lg, ledger_sha="deadbeef00000000", judge=None):
    idx = link.build_index(lg)
    cands = lenses.LENSES[lens_name](lg, idx, link.SETTING_1)
    j = judge if judge is not None else FakeJudge()
    out = []
    for cand in cands:
        outcome, sub = semantic.judge_candidate(lg, idx, j, cand)
        if outcome.state == "closed":
            continue
        k_topic = len(link.breadth(lg, sub.x_a))
        cat = record.categorize(outcome.state, k_topic)
        out.append(record.build_record(lg, ledger_sha, sub, outcome, cat, r=1))
    return out


def test_tiers_never_mix():
    seed = a_claim_n("Diagnostic tests should be selected based on failure likelihood.", n=2)
    [rec] = _build("SEL", ledger([seed]))
    assert rec.category == "HYP"
    for item in rec.observed_evidence:
        assert item.span is not None  # observed_evidence: verbatim spans only
    assert rec.inferred_gap.statement  # a re-runnable statement about the ledger
    assert rec.hypothesis is not None
    assert rec.hypothesis.label == "inferred"
    assert "Practitioners" in rec.hypothesis.text or "practitioners" in rec.hypothesis.text.lower()


def test_synthetic_evidence_does_not_count_as_attestation():
    seed = a_claim("Diagnostic tests should be selected based on failure likelihood.", source_id="s1")
    synth = s_claim(
        "Selection practice for failure likelihood is discussed.",
        exact="CLOSES_HERE: pick the test with the highest failure likelihood.", source_id="synth-1")
    [rec] = _build("SEL", ledger([seed, synth, *fillers(40)]))
    assert rec.category == "RG-UNVER"
    assert rec.hypothesis is None
    synth_items = [i for i in rec.observed_evidence if i.epistemic_label is EpistemicLabel.SYNTHETIC_EXTRAPOLATION]
    assert synth_items
    for item in synth_items:
        assert item.counts_as_attestation is False
        assert item.flag == "unverified-synthetic"
    for item in rec.observed_evidence:
        if item.epistemic_label in (EpistemicLabel.LITERATURE_SUPPORTED,
                                    EpistemicLabel.OBSERVED_HUMAN_EVIDENCE,
                                    EpistemicLabel.ORGANISATIONAL_ARTEFACT_SUPPORTED):
            assert item.counts_as_attestation is True
            assert item.flag is None


def test_gap_id_stable_under_seed_iteration_order():
    a = record.make_gap_id(config.CONFIG_SHA256, "ledgersha", "DISC", ["c-2", "c-1"])
    b = record.make_gap_id(config.CONFIG_SHA256, "ledgersha", "DISC", frozenset({"c-1", "c-2"}))
    assert a == b


def test_gap_id_stable_under_claim_reordering_in_the_ledger():
    c1 = a_claim("Loose terminal connections cause problems in the field.",
                source_id="src-1", independence_key="key-1")
    c2 = a_claim("Loose terminal issues appear intermittently in the panel.",
                source_id="src-2", independence_key="key-2")
    r1 = _build("DISC", ledger([c1, c2]))
    r2 = _build("DISC", ledger([c2, c1]))
    assert {r.gap_id for r in r1} == {r.gap_id for r in r2}


def test_confidence_rubric_matches_spec_formula():
    # F3: the level is renamed `breadth` and is never "high"; `broad` is decided directly by
    # (k_topic, k_step), not by score alone.
    a, b, p, q, score, breadth = record.confidence_rubric(k_topic=5, k_step=2, partial=False)
    assert (a, b, p, q, score, breadth) == (3, 1, 0, 0, 4, "broad")
    a, b, p, q, score, breadth = record.confidence_rubric(k_topic=3, k_step=1, partial=True)
    assert (a, b, p, q, score, breadth) == (2, 0, 1, 0, 1, "narrow")
    a, b, p, q, score, breadth = record.confidence_rubric(k_topic=1, k_step=2, partial=False)
    assert record.categorize("open", k_topic=1) == "RG-SINGLE"


def test_confidence_rubric_promo_penalty_subtracts_q():
    a, b, p, q, score, breadth = record.confidence_rubric(k_topic=3, k_step=1, partial=False,
                                                           promo_penalty=True)
    assert (a, b, p, q, score) == (2, 0, 0, 1, 1)


def test_inferred_gap_statement_names_the_missing_element_and_is_readable():
    # Defect 4, revised by S1: a plain sentence naming the missing element and the closure
    # judge's finding, not "matches <test_id> within scope" -- and not a raw claim count, since
    # the judge decides from retrieved SENTENCES, not `|X|` (S1's inferred_gap.statement rewrite).
    seed = a_claim_n("Diagnostic tests should be selected based on failure likelihood.", n=2)
    [rec] = _build("SEL", ledger([seed]))
    stmt = rec.inferred_gap.statement
    assert "matches" not in stmt and "within scope" not in stmt
    assert rec.missing in stmt
    assert "verified sentence" in stmt
    assert "closure judge" in stmt and config.JUDGE_MODEL in stmt
    assert "prompt sha" in stmt


def test_diag_evidence_uses_seed_and_rival_roles():
    claims = [
        a_claim("Race conditions cause intermittent faults in the system.",
               source_id="src-1", independence_key="key-1", knowledge_type=KnowledgeType.FAILURE_MODE),
        a_claim("Ground loops cause intermittent faults in the system.",
               source_id="src-2", independence_key="key-2", knowledge_type=KnowledgeType.FAILURE_MODE),
        a_claim("Loose terminals cause intermittent faults in the system.",
               source_id="src-3", independence_key="key-3", knowledge_type=KnowledgeType.FAILURE_MODE),
    ]
    recs = _build("DIAG", ledger(claims))
    assert recs
    for rec in recs:
        roles = {i.claim_id: i.role for i in rec.observed_evidence}
        seed_ids = [i.claim_id for i in rec.observed_evidence if i.role == "seed"]
        assert len(seed_ids) == 1  # one distinguished seed per group, per §2.2's literal reading
        rival_ids = [i.claim_id for i in rec.observed_evidence if i.role == "rival"]
        assert len(rival_ids) == 2
        assert "topic" not in roles.values() or set(roles.values()) <= {"seed", "rival", "topic"}


def test_undecided_judge_response_builds_an_rg_undecided_record_not_open():
    # Fix 1, end to end: a malformed judge answer must never silently become an "open" HYP.
    class _MalformedJudge:
        model_id = "malformed"

        def ask(self, prompt):
            return None

    seed = a_claim_n("Diagnostic tests should be selected based on failure likelihood.", n=2)
    recs = _build("SEL", ledger([seed]), judge=_MalformedJudge())
    assert len(recs) == 1
    rec = recs[0]
    assert rec.category == "RG-UNDECIDED"
    assert rec.inferred_gap.closure_state == "undecided"
    assert rec.hypothesis is None


def test_rg_unk_anchor_names_the_area_not_a_raw_id():
    claim = a_claim("An attested claim.", source_id="c1")
    a = area("a-xyz", "Fault Diagnosis")
    lg = ledger([claim], areas=[a], assignments=[(claim.claim_id, "a-xyz")])
    sidecar = {"slots": [{"area_id": "a-xyz", "probe": "cue", "status": "unknown", "claim_ids": []}]}
    idx = link.build_index(lg)
    [rec] = record.unk_gaps(lg, idx, sidecar, "ledgersha")
    assert "a-xyz" not in rec.anchor
    assert "Fault Diagnosis" in rec.anchor
    assert "cue" in rec.anchor
