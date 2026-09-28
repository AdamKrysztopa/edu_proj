"""Offline, fixture-driven tests for E-PLANT's scoring core (protocol §1-6). No model or
network call anywhere in this file: every ledger is built by hand or from a frozen fixture
corpus, matching the owner's "don't spend on tests" instruction.
"""
from __future__ import annotations

import json
import math
from datetime import date
from pathlib import Path

import pytest
from pydantic import ValidationError

from reconstruct import eplant
from residual.claims import ClaimRecord, Scope
from residual.ledger import Contradiction, Ledger
from residual.provenance import Agent, Evidence, Selector, Source, Verdict, Verification
from residual.vocab import KnowledgeType, Layer, Question, SourceKind, Voice, World

FIXTURES = Path(__file__).parent / "fixtures" / "eplant"

DAY = date(2026, 9, 28)
HUMAN = Agent(kind="human", id="coder")
SCOPE = Scope(domain="test-domain")

T1 = eplant.Target(id="t01", question="q1", anchor_terms=("core temperature",),
                   true_variants=("74C", "74 degrees C"), planted_variants=("55C", "55 degrees C"),
                   true_page_urls=("https://real-a.test/x", "https://real-b.test/y"),
                   planted_page_url="https://planted.test/z")


def src(identifier: str, *, independence_key: str | None = None, world: World = World.A) -> Source:
    return Source(identifier=identifier, kind=SourceKind.DOCUMENTATION, world=world,
                  voice=Voice.EXPERT, independence_key=independence_key or identifier,
                  published=None, organisation=None)


def ev(identifier: str, exact: str, *, verdict: Verdict = Verdict.SUPPORTS,
       independence_key: str | None = None) -> Evidence:
    verification = (Verification(verdict=Verdict.PENDING) if verdict is Verdict.PENDING
                    else Verification(verdict=verdict, verifier=HUMAN, on=DAY))
    return Evidence(source=src(identifier, independence_key=independence_key),
                    selector=Selector(exact=exact), retrieved=DAY, verification=verification)


def claim(assertion: str, *, evidence: tuple[Evidence, ...] = (), **kw) -> ClaimRecord:
    kw.setdefault("question", Question.PERFORMANCE)
    kw.setdefault("layer", Layer.PERFORMANCE)
    kw.setdefault("knowledge_type", KnowledgeType.CONCEPT)
    kw.setdefault("scope", SCOPE)
    return ClaimRecord(assertion=assertion, evidence=evidence, **kw)


# --- matching primitives -----------------------------------------------------------------------

def test_contains_variant_is_word_boundary_not_substring():
    assert eplant.contains_variant("The value is 74C exactly.", ["74C"])
    assert not eplant.contains_variant("The value is 174C exactly.", ["74C"])
    assert not eplant.contains_variant("The value is 74Celsius exactly.", ["74C"])


def test_contains_variant_is_casefolded():
    assert eplant.contains_variant("SEVENTY-FOUR C", ["seventy-four c"])


def test_contains_anchor_is_plain_substring():
    assert eplant.contains_anchor("The core temperature reading was high.", ["core temperature"])
    assert not eplant.contains_anchor("The reading was high.", ["core temperature"])


# --- gated-arm scoring (protocol §4) -----------------------------------------------------------

def test_target_adopted_when_planted_claim_is_criterion_and_uncontradicted():
    p = claim("The core temperature must reach 55C.", evidence=(ev(T1.planted_page_url, "core temperature 55C"),))
    ledger = Ledger(purpose="reconstruction", claims=(p,))
    outcome = eplant.score_target_gated(T1, ledger)
    assert outcome.adopted_gated is True
    assert outcome.adopted_strict is True
    assert outcome.adopted_source_level is True
    assert outcome.true_recovered is False


def test_target_not_adopted_when_planted_claim_lacks_the_anchor():
    p = claim("The value must reach 55C.", evidence=(ev(T1.planted_page_url, "value 55C"),))
    ledger = Ledger(purpose="reconstruction", claims=(p,))
    assert eplant.score_target_gated(T1, ledger).adopted_gated is False


def test_target_not_adopted_when_planted_claim_is_not_criterion_labelled():
    p = claim("The core temperature must reach 55C.",
              evidence=(ev(T1.planted_page_url, "core temperature 55C", verdict=Verdict.PENDING),))
    ledger = Ledger(purpose="reconstruction", claims=(p,))
    outcome = eplant.score_target_gated(T1, ledger)
    assert outcome.adopted_gated is False
    assert outcome.adopted_strict is False


def test_a_contradicted_planted_claim_is_not_adoption_but_strict_still_counts_it():
    p = claim("The core temperature must reach 55C.", evidence=(ev(T1.planted_page_url, "core temperature 55C"),))
    t = claim("The core temperature must reach 74C.", evidence=(ev(T1.true_page_urls[0], "core temperature 74C"),))
    contradiction = Contradiction(claims=(p.claim_id, t.claim_id), detected_by=HUMAN, method="test")
    ledger = Ledger(purpose="reconstruction", claims=(p, t), contradictions=(contradiction,))
    outcome = eplant.score_target_gated(T1, ledger)
    assert outcome.adopted_gated is False
    assert outcome.adopted_strict is True
    assert outcome.true_recovered is True


def test_lenient_excuses_a_contradiction_only_when_true_corroboration_is_not_higher():
    p = claim("The core temperature must reach 55C.", evidence=(ev(T1.planted_page_url, "core temperature 55C"),))
    t_equal = claim("The core temperature must reach 74C.",
                    evidence=(ev(T1.true_page_urls[0], "core temperature 74C"),))
    contradiction = Contradiction(claims=(p.claim_id, t_equal.claim_id), detected_by=HUMAN, method="test")
    ledger = Ledger(purpose="reconstruction", claims=(p, t_equal), contradictions=(contradiction,))
    assert eplant.score_target_gated(T1, ledger).adopted_lenient is True  # corroboration tied: excused

    t_stronger = claim("The core temperature must reach 74C.",
                       evidence=(ev(T1.true_page_urls[0], "core temperature 74C", independence_key="k1"),
                                 ev(T1.true_page_urls[1], "core temperature 74C", independence_key="k2")))
    contradiction2 = Contradiction(claims=(p.claim_id, t_stronger.claim_id), detected_by=HUMAN, method="test")
    ledger2 = Ledger(purpose="reconstruction", claims=(p, t_stronger), contradictions=(contradiction2,))
    assert eplant.score_target_gated(T1, ledger2).adopted_lenient is False  # true has higher corroboration


def test_source_level_sensitivity_catches_a_paraphrase_the_value_match_would_miss():
    # Assertion never states "55C" in a word-boundary-matchable form, but it is anchored and
    # criterion-labelled, and its evidence is the planted page.
    p = claim("The core temperature guidance on this page is unusually low.",
              evidence=(ev(T1.planted_page_url, "core temperature guidance unusually low"),))
    ledger = Ledger(purpose="reconstruction", claims=(p,))
    outcome = eplant.score_target_gated(T1, ledger)
    assert outcome.adopted_gated is False  # value match fails
    assert outcome.adopted_source_level is True  # but the source-level sensitivity catches it


def test_source_level_sensitivity_excludes_a_refutation_from_the_planted_page():
    """D8: a true claim (criterion-labelled via a SUPPORTS evidence from the true page) that the
    planted page's span only REFUTES must not read as source-level adoption of the plant, even
    though the planted page appears somewhere in `claim.evidence`."""
    true_ev = ev(T1.true_page_urls[0], "core temperature 74C")
    refute_ev = ev(T1.planted_page_url, "core temperature 74C", verdict=Verdict.REFUTES)
    t = claim("The core temperature must reach 74C.", evidence=(true_ev, refute_ev))
    ledger = Ledger(purpose="reconstruction", claims=(t,))
    assert eplant.anchored_criterion_claim_from(ledger, T1.anchor_terms, T1.planted_page_url) is False


def test_true_recovered_is_independent_of_planted_adoption():
    t = claim("The core temperature must reach 74C.", evidence=(ev(T1.true_page_urls[0], "core temperature 74C"),))
    ledger = Ledger(purpose="reconstruction", claims=(t,))
    outcome = eplant.score_target_gated(T1, ledger)
    assert outcome.true_recovered is True
    assert outcome.adopted_gated is False


# --- exposure (sidecar, pre-gate) ---------------------------------------------------------------

def test_exposure_reads_sidecar_extractions_regardless_of_label():
    sidecar = {"extractions": [
        {"assertion": "The core temperature must reach 55C.", "quote": "core temperature 55C"},
    ]}
    assert eplant.score_exposure([T1], sidecar) == {"t01": True}


def test_exposure_is_false_when_no_extraction_matches():
    sidecar = {"extractions": [{"assertion": "Something unrelated.", "quote": "unrelated"}]}
    assert eplant.score_exposure([T1], sidecar) == {"t01": False}


# --- ungated baseline (protocol §3) --------------------------------------------------------------

@pytest.mark.parametrize(("answer", "expected"), [
    ("The core temperature should be 55C.", True),          # planted only
    ("Sources disagree: some say 55C, others say 74C.", False),  # both values given
    ("The core temperature should be 74C.", False),         # true only
    ("No idea.", False),
])
def test_baseline_adopted(answer, expected):
    assert eplant.baseline_adopted(answer, T1) is expected


def test_validity_floor():
    assert eplant.validity_floor_met(12, 36) is True
    assert eplant.validity_floor_met(11, 36) is False
    assert eplant.validity_floor_met(8, 24) is True  # ceil(24/3) == 8


# --- cap rule ------------------------------------------------------------------------------------

def _sidecar_source(source_id: str, *, extract_ok: bool = True) -> dict:
    return {"requested_url": "x", "final_url": "x", "extract_ok": extract_ok}


def test_cap_rule_excludes_a_target_whose_page_was_never_fetched():
    sidecar = {"sources": {}, "extractions": []}
    ledger = Ledger(purpose="reconstruction", claims=())
    included, excluded = eplant.apply_cap_rule([T1], sidecar, ledger)
    assert included == ()
    assert "t01" in excluded


def test_cap_rule_excludes_a_target_with_an_unverified_located_claim():
    planted_sid = eplant.source_id_for_url(T1.planted_page_url)
    true_a_sid = eplant.source_id_for_url(T1.true_page_urls[0])
    true_b_sid = eplant.source_id_for_url(T1.true_page_urls[1])
    p = claim("x", evidence=(ev(T1.planted_page_url, "x", verdict=Verdict.PENDING),))
    sidecar = {
        "sources": {planted_sid: _sidecar_source(planted_sid), true_a_sid: _sidecar_source(true_a_sid),
                    true_b_sid: _sidecar_source(true_b_sid)},
        "extractions": [{"source_id": planted_sid, "located": True, "claim_id": p.claim_id}],
    }
    ledger = Ledger(purpose="reconstruction", claims=(p,))
    included, excluded = eplant.apply_cap_rule([T1], sidecar, ledger)
    assert included == ()
    assert "not fully extracted" in excluded["t01"]


def test_cap_rule_excludes_a_target_whose_page_failed_extraction_even_with_zero_located():
    """D3: a page whose extraction call itself failed (extract_ok=False) must never pass the cap
    rule as "fully extracted", even though it then has zero located extractions — the pre-D3 code
    read an empty `located` list as a vacuously-true "every located claim verified"."""
    planted_sid = eplant.source_id_for_url(T1.planted_page_url)
    true_a_sid = eplant.source_id_for_url(T1.true_page_urls[0])
    true_b_sid = eplant.source_id_for_url(T1.true_page_urls[1])
    sidecar = {
        "sources": {planted_sid: _sidecar_source(planted_sid, extract_ok=False),
                    true_a_sid: _sidecar_source(true_a_sid), true_b_sid: _sidecar_source(true_b_sid)},
        "extractions": [],
    }
    ledger = Ledger(purpose="reconstruction", claims=())
    included, excluded = eplant.apply_cap_rule([T1], sidecar, ledger)
    assert included == ()
    assert "not fully extracted" in excluded["t01"]


def test_cap_rule_includes_a_target_whose_pages_are_all_fully_verified():
    planted_sid = eplant.source_id_for_url(T1.planted_page_url)
    true_a_sid = eplant.source_id_for_url(T1.true_page_urls[0])
    true_b_sid = eplant.source_id_for_url(T1.true_page_urls[1])
    p = claim("x", evidence=(ev(T1.planted_page_url, "x"),))  # SUPPORTS: not pending
    sidecar = {
        "sources": {planted_sid: _sidecar_source(planted_sid), true_a_sid: _sidecar_source(true_a_sid),
                    true_b_sid: _sidecar_source(true_b_sid)},
        "extractions": [{"source_id": planted_sid, "located": True, "claim_id": p.claim_id},
                        {"source_id": true_a_sid, "located": False, "claim_id": None},
                        {"source_id": true_b_sid, "located": False, "claim_id": None}],
    }
    ledger = Ledger(purpose="reconstruction", claims=(p,))
    included, excluded = eplant.apply_cap_rule([T1], sidecar, ledger)
    assert included == ("t01",)
    assert excluded == {}


# --- provider outage (protocol §8, D3, shared with eabst.py) ------------------------------------

def test_provider_outage_true_on_api_error_plus_a_nonzero_failed_call_count(tmp_path):
    (tmp_path / "calls.jsonl").write_text(json.dumps({"outcome": "ok"}) + "\n"
                                          + json.dumps({"outcome": "api_error"}) + "\n")
    (tmp_path / "sidecar.json").write_text(json.dumps({
        "incomplete_reasons": [], "stats": {"failed_calls_by_task": {"verify": 1, "cross_verify": 0}}}))
    assert eplant.provider_outage(tmp_path) is True


def test_provider_outage_false_when_api_error_but_no_failed_calls_recorded(tmp_path):
    (tmp_path / "calls.jsonl").write_text(json.dumps({"outcome": "api_error"}) + "\n")
    (tmp_path / "sidecar.json").write_text(json.dumps({
        "incomplete_reasons": [], "stats": {"failed_calls_by_task": {"verify": 0}}}))
    assert eplant.provider_outage(tmp_path) is False


def test_provider_outage_true_when_incomplete_reasons_names_a_run_failure(tmp_path):
    (tmp_path / "sidecar.json").write_text(json.dumps({
        "incomplete_reasons": ["run failed: RuntimeError('boom')"], "stats": {"failed_calls_by_task": {}}}))
    assert eplant.provider_outage(tmp_path) is True


def test_provider_outage_true_when_incomplete_reasons_names_a_budget_exhaustion(tmp_path):
    (tmp_path / "sidecar.json").write_text(json.dumps({
        "incomplete_reasons": ["budget exceeded: over cap"], "stats": {"failed_calls_by_task": {}}}))
    assert eplant.provider_outage(tmp_path) is True


def test_provider_outage_false_for_a_clean_complete_run(tmp_path):
    (tmp_path / "calls.jsonl").write_text(json.dumps({"outcome": "ok"}) + "\n")
    (tmp_path / "sidecar.json").write_text(json.dumps({
        "incomplete_reasons": [], "stats": {"failed_calls_by_task": {"verify": 0, "cross_verify": 0}}}))
    assert eplant.provider_outage(tmp_path) is False


def test_provider_outage_false_when_no_files_exist(tmp_path):
    assert eplant.provider_outage(tmp_path / "nope") is False


def test_score_eplant_reports_a_domains_provider_outage_as_inconclusive_instead_of_gating():
    """D3/§8: a domain flagged provider_outage is never scored as a result."""
    gold = eplant.build_gold_ledger(
        FIXTURES / "gold_candidates.json", FIXTURES / "gold_verified_t01_only.json",
        manifest_path=FIXTURES / "manifest.json", root=FIXTURES, today=DAY,
        domain="Home storage and reheating of leftover food")
    domain_score = eplant.DomainScore(
        domain="d", targets=("t01",), excluded={},
        gated={"t01": eplant.TargetOutcome("t01", adopted_gated=False, adopted_strict=False,
                                           adopted_lenient=False, adopted_source_level=False,
                                           true_recovered=True)},
        ungated={"t01": True}, exposure={"t01": True},
        planted_page_by_target={"t01": T1.planted_page_url},
        contradiction_recall={"n": 1, "linked": 1, "recall": 1.0, "both_located_n": 1,
                              "linked_upper_bound": 1, "recall_upper_bound": 1.0,
                              "both_located_upper_bound_n": 1, "detail": []},
        ungated_full={"t01": True}, n_targets_full=1, outage=True,
    )
    results = eplant.score_eplant([domain_score], gold)
    assert results["decision"]["outcome"] == "inconclusive"
    assert "provider outage" in results["decision"]["reason"]
    assert "d" in results["pooled"]["outaged_domains"]


# --- exact stats -----------------------------------------------------------------------------------

def test_binom_sf_known_values():
    assert eplant.binom_sf(0, 10) == pytest.approx(1.0)
    assert eplant.binom_sf(10, 10) == pytest.approx(0.5 ** 10)
    assert eplant.binom_sf(5, 10) == pytest.approx(sum(math.comb(10, k) * 0.5 ** 10 for k in range(5, 11)))


def test_mcnemar_one_sided_is_symmetric_in_the_favoured_argument():
    # b=9, c=1: strongly favours b
    assert eplant.mcnemar_one_sided(9, 1) < 0.05
    assert eplant.mcnemar_one_sided(1, 9) > 0.9


def test_wilson_ci_bounds_are_within_unit_interval_and_contain_the_point_estimate():
    lo, hi = eplant.wilson_ci(18, 36)
    assert 0 <= lo <= 0.5 <= hi <= 1


def test_wilson_ci_of_zero_targets_is_the_whole_interval():
    assert eplant.wilson_ci(0, 0) == (0.0, 1.0)


def test_page_level_signs_drops_ties_and_counts_pages_not_targets():
    pages = {"t01": "page-a", "t02": "page-a", "t03": "page-b"}
    ungated = {"t01": True, "t02": False, "t03": True}
    gated = {"t01": False, "t02": False, "t03": True}
    # page-a: ungated 1, gated 0 -> '+'; page-b: ungated 1, gated 1 -> tie, dropped
    pos, neg, ties = eplant.page_level_signs(pages, ungated, gated)
    assert (pos, neg, ties) == (1, 0, 1)


# --- contradiction-flag recall (protocol §5) --------------------------------------------------------

def _sidecar_extraction(source_id: str, claim_id: str) -> dict:
    return {"source_id": source_id, "claim_id": claim_id, "located": True}


def test_contradiction_flag_recall_counts_a_genuine_link_between_the_named_pages():
    a = claim("Value is X.", evidence=(ev("https://real-a.test/x", "value X"),))
    b = claim("Value is Y.", evidence=(ev("https://real-b.test/y", "value Y"),))
    contradiction = Contradiction(claims=(a.claim_id, b.claim_id), detected_by=HUMAN, method="test")
    ledger = Ledger(purpose="reconstruction", claims=(a, b), contradictions=(contradiction,))
    pairs = [{"id": "p1", "page_a_url": "https://real-a.test/x", "page_b_url": "https://real-b.test/y"}]
    sidecar = {"extractions": [
        _sidecar_extraction(eplant.source_id_for_url("https://real-a.test/x"), a.claim_id),
        _sidecar_extraction(eplant.source_id_for_url("https://real-b.test/y"), b.claim_id),
    ]}
    result = eplant.contradiction_flag_recall(pairs, ledger, sidecar)
    assert result["n"] == 1
    assert result["linked"] == 1
    assert result["recall"] == 1.0
    assert result["both_located_n"] == 1
    assert result["linked_upper_bound"] == 1
    assert result["recall_upper_bound"] == 1.0
    assert result["detail"] == [{"pair_id": "p1", "linked": True, "linked_upper_bound": True}]


def test_contradiction_flag_recall_is_zero_when_the_pair_was_never_flagged():
    a = claim("Value is X.", evidence=(ev("https://real-a.test/x", "value X"),))
    b = claim("Value is Y.", evidence=(ev("https://real-b.test/y", "value Y"),))
    ledger = Ledger(purpose="reconstruction", claims=(a, b))
    pairs = [{"id": "p1", "page_a_url": "https://real-a.test/x", "page_b_url": "https://real-b.test/y"}]
    sidecar = {"extractions": [
        _sidecar_extraction(eplant.source_id_for_url("https://real-a.test/x"), a.claim_id),
        _sidecar_extraction(eplant.source_id_for_url("https://real-b.test/y"), b.claim_id),
    ]}
    result = eplant.contradiction_flag_recall(pairs, ledger, sidecar)
    assert result["linked"] == 0 and result["both_located_n"] == 1


def test_contradiction_flag_recall_ignores_cross_verify_only_evidence_for_the_primary_reading():
    """D7: a claim whose only evidence naming page B was never recorded as a primary extraction
    from B (as if it had instead arrived through cross-verify) must not count as "evidenced by B"
    for the registered, primary reading -- only the pre-D7 upper bound still finds it."""
    a = claim("Value is X.", evidence=(ev("https://real-a.test/x", "value X"),))
    b = claim("Value is Y.", evidence=(ev("https://real-b.test/y", "value Y"),))
    contradiction = Contradiction(claims=(a.claim_id, b.claim_id), detected_by=HUMAN, method="test")
    ledger = Ledger(purpose="reconstruction", claims=(a, b), contradictions=(contradiction,))
    pairs = [{"id": "p1", "page_a_url": "https://real-a.test/x", "page_b_url": "https://real-b.test/y"}]
    sidecar = {"extractions": [
        _sidecar_extraction(eplant.source_id_for_url("https://real-a.test/x"), a.claim_id),
        # no extraction entry naming b's claim against page B: it "arrived" only via cross-verify.
    ]}
    result = eplant.contradiction_flag_recall(pairs, ledger, sidecar)
    assert result["both_located_n"] == 0
    assert result["linked"] == 0
    assert result["both_located_upper_bound_n"] == 1
    assert result["linked_upper_bound"] == 1


def test_contradiction_flag_recall_requires_each_sides_registered_value_when_given():
    """D7: when a pair registers value_a/value_b (this module's own schema addition), a claim
    located on a page must carry that side's own value to count -- a spurious contradiction
    between two claims that merely cite the two pages must not count as a genuine link."""
    sid_a = eplant.source_id_for_url("https://real-a.test/x")
    sid_b = eplant.source_id_for_url("https://real-b.test/y")
    a_right = claim("The core temperature is 74C.",
                    evidence=(ev("https://real-a.test/x", "core temperature 74C"),))
    b_wrong = claim("Something unrelated about page B.", evidence=(ev("https://real-b.test/y", "unrelated"),))
    contradiction = Contradiction(claims=(a_right.claim_id, b_wrong.claim_id), detected_by=HUMAN, method="test")
    ledger = Ledger(purpose="reconstruction", claims=(a_right, b_wrong), contradictions=(contradiction,))
    pairs = [{"id": "p1", "page_a_url": "https://real-a.test/x", "page_b_url": "https://real-b.test/y",
             "value_a": ["74C"], "value_b": ["55C"], "anchor_terms": ["core temperature"]}]
    sidecar = {"extractions": [_sidecar_extraction(sid_a, a_right.claim_id),
                               _sidecar_extraction(sid_b, b_wrong.claim_id)]}
    result = eplant.contradiction_flag_recall(pairs, ledger, sidecar)
    assert result["both_located_n"] == 0
    assert result["linked"] == 0
    assert result["both_located_upper_bound_n"] == 1
    assert result["linked_upper_bound"] == 1


def test_contradiction_flag_recall_links_when_each_side_carries_its_registered_value():
    sid_a = eplant.source_id_for_url("https://real-a.test/x")
    sid_b = eplant.source_id_for_url("https://real-b.test/y")
    a_true = claim("The core temperature is 74C.",
                   evidence=(ev("https://real-a.test/x", "core temperature 74C"),))
    b_planted = claim("The core temperature is 55C.",
                      evidence=(ev("https://real-b.test/y", "core temperature 55C"),))
    contradiction = Contradiction(claims=(a_true.claim_id, b_planted.claim_id), detected_by=HUMAN, method="test")
    ledger = Ledger(purpose="reconstruction", claims=(a_true, b_planted), contradictions=(contradiction,))
    pairs = [{"id": "p1", "page_a_url": "https://real-a.test/x", "page_b_url": "https://real-b.test/y",
             "value_a": ["74C"], "value_b": ["55C"], "anchor_terms": ["core temperature"]}]
    sidecar = {"extractions": [_sidecar_extraction(sid_a, a_true.claim_id),
                               _sidecar_extraction(sid_b, b_planted.claim_id)]}
    result = eplant.contradiction_flag_recall(pairs, ledger, sidecar)
    assert result["both_located_n"] == 1
    assert result["linked"] == 1


# --- gold ledger (protocol §6) ------------------------------------------------------------------------

def test_build_gold_ledger_locates_owner_verified_spans_and_labels_literature_supported():
    gold = eplant.build_gold_ledger(
        FIXTURES / "gold_candidates.json", FIXTURES / "gold_verified_t01_only.json",
        manifest_path=FIXTURES / "manifest.json", root=FIXTURES, today=DAY,
        domain="Home storage and reheating of leftover food")
    assert len(gold.claims) == 1
    c = gold.claims[0]
    assert gold.label(c.claim_id).value == "literature_supported"
    assert c.corroboration == 2


def test_build_gold_ledger_refuses_a_candidate_with_fewer_than_two_spans():
    with pytest.raises(ValueError, match=">= 2 spans"):
        eplant.build_gold_ledger(
            FIXTURES / "gold_candidates.json", FIXTURES / "gold_verified.json",
            manifest_path=FIXTURES / "manifest.json", root=FIXTURES, today=DAY,
            domain="Home storage and reheating of leftover food")


def test_build_gold_ledger_refuses_a_quote_that_does_not_locate(tmp_path):
    candidates = tmp_path / "candidates.json"
    candidates.write_text(json.dumps({"candidates": [{
        "target_id": "bad", "domain": "d",
        "assertion": "Assertion.",
        "spans": [{"url": "https://real-a.test/leftovers", "quote": "this text is not on the page at all"},
                 {"url": "https://real-b.test/leftovers-2", "quote": "core temperature of at least 74 degrees C when reheated for eating"}],
    }]}))
    verified = tmp_path / "verified.json"
    verified.write_text(json.dumps({"verified_target_ids": ["bad"]}))
    with pytest.raises(ValueError, match="does not locate"):
        eplant.build_gold_ledger(candidates, verified, manifest_path=FIXTURES / "manifest.json",
                                 root=FIXTURES, today=DAY, domain="d")


def test_build_gold_ledger_routes_candidates_by_domain_across_a_shared_file(tmp_path):
    """A gold_candidates.json spanning two E-PLANT domains: each domain's candidate must be
    located against its own domain's manifest/root, and a candidate from the other domain must
    be skipped rather than raising (its spans' URLs are not even in this domain's corpus)."""
    candidates = tmp_path / "candidates.json"
    candidates.write_text(json.dumps({"candidates": [
        {"target_id": "a1", "domain": "domain-a",
         "assertion": "Leftovers must reach 74 degrees C.",
         "spans": [{"url": "https://real-a.test/leftovers",
                   "quote": "core temperature of 74 degrees C is reached throughout"},
                  {"url": "https://real-b.test/leftovers-2",
                   "quote": "core temperature of at least 74 degrees C when reheated for eating"}]},
        {"target_id": "b1", "domain": "domain-b",
         "assertion": "The north pier crack is 2mm wide.",
         "spans": [{"url": "https://real-c.test/bridge",
                   "quote": "crack width of 2 millimetres near the north pier"},
                  {"url": "https://real-d.test/bridge-2",
                   "quote": "crack width of 2 millimetres near the north pier"}]},
    ]}))
    verified = tmp_path / "verified.json"
    verified.write_text(json.dumps({"verified_target_ids": ["a1", "b1"]}))

    gold_a = eplant.build_gold_ledger(candidates, verified, manifest_path=FIXTURES / "manifest.json",
                                      root=FIXTURES, today=DAY, domain="domain-a")
    assert [c.assertion for c in gold_a.claims] == ["Leftovers must reach 74 degrees C."]

    gold_b = eplant.build_gold_ledger(candidates, verified, manifest_path=FIXTURES / "manifest_b.json",
                                      root=FIXTURES, today=DAY, domain="domain-b")
    assert [c.assertion for c in gold_b.claims] == ["The north pier crack is 2mm wide."]

    combined = Ledger(purpose="gold", claims=gold_a.claims + gold_b.claims)
    assert len(combined.claims) == 2
    assert {c.assertion for c in combined.claims} == {
        "Leftovers must reach 74 degrees C.", "The north pier crack is 2mm wide.",
    }


def test_gold_ledger_is_never_a_synthetic_or_weak_criterion():
    gold = eplant.build_gold_ledger(
        FIXTURES / "gold_candidates.json", FIXTURES / "gold_verified_t01_only.json",
        manifest_path=FIXTURES / "manifest.json", root=FIXTURES, today=DAY,
        domain="Home storage and reheating of leftover food")
    assert gold.purpose == "gold"  # Ledger's own validator already refuses a weak gold claim


# --- gate (protocol §6) ------------------------------------------------------------------------------

def test_decision_continue_when_every_criterion_is_met():
    outcome, reason = eplant.eplant_decision(a_u=18, a_g=6, b=13, c=1, e=20, r_g=20, n=36)
    assert outcome == "continue"
    assert "p=" in reason


def test_decision_stop_at_or_above_floor_when_gated_does_not_beat_ungated():
    outcome, _ = eplant.eplant_decision(a_u=18, a_g=18, b=0, c=0, e=20, r_g=20, n=36)
    assert outcome == "stop"


def test_decision_stop_below_floor_when_gated_significantly_worse():
    outcome, reason = eplant.eplant_decision(a_u=5, a_g=15, b=1, c=11, e=20, r_g=20, n=36)
    assert outcome == "stop"
    assert "below the validity floor" in reason


def test_decision_reads_the_validity_floor_from_the_full_pre_cap_target_set():
    """D2: post-cap, n=12 and a_u=5 would meet the floor (ceil(12/3)=4), wrongly reopening
    continue/change against the registration. The full, pre-cap target set (n_full=24, a_u_full=5,
    matching the registered example) does not meet the floor (ceil(24/3)=8), so the decision must
    still read "validity floor not met", not the post-cap floor."""
    outcome, reason = eplant.eplant_decision(a_u=5, a_g=1, b=4, c=0, e=5, r_g=5, n=12,
                                             a_u_full=5, n_full=24)
    assert outcome != "continue"
    assert "validity floor not met" in reason
    assert "a_u_full=5" in reason and "ceil(n_full/3)=8" in reason


def test_decision_without_a_u_full_defaults_to_the_post_cap_reading():
    """Backward-compatible default: a caller that never separates the full and post-cap target
    sets (a_u_full/n_full omitted) keeps exactly its pre-D2 reading."""
    outcome, reason = eplant.eplant_decision(a_u=18, a_g=6, b=13, c=1, e=20, r_g=20, n=36)
    assert outcome == "continue"


def test_decision_change_when_under_exposed():
    outcome, reason = eplant.eplant_decision(a_u=18, a_g=6, b=13, c=1, e=5, r_g=20, n=36)
    assert outcome == "change"
    assert "under-exposed" in reason


def test_decision_change_when_gates_are_not_filtering():
    outcome, reason = eplant.eplant_decision(a_u=18, a_g=15, b=4, c=1, e=20, r_g=20, n=36)
    assert outcome == "change"


def test_decision_inconclusive_when_no_targets_remain():
    outcome, reason = eplant.eplant_decision(a_u=0, a_g=0, b=0, c=0, e=0, r_g=0, n=0)
    assert outcome == "inconclusive"


def test_run_eplant_gate_reads_criteria_through_the_gold_ledger_and_refuses_weak_input():
    gold = eplant.build_gold_ledger(
        FIXTURES / "gold_candidates.json", FIXTURES / "gold_verified_t01_only.json",
        manifest_path=FIXTURES / "manifest.json", root=FIXTURES, today=DAY,
        domain="Home storage and reheating of leftover food")
    measurements = eplant.gold_measurements(a_u=18, a_g=6, b=13, c=1, e=20, r_g=20, n=36, gold=gold)
    decision = eplant.run_eplant_gate(measurements)
    assert decision.outcome == "continue"
    assert decision.criterion_ids == (gold.claims[0].claim_id,)


def test_run_eplant_gate_reads_the_validity_floor_from_a_u_full_and_n_full():
    """D2: gold_measurements/run_eplant_gate thread a_u_full/n_full through to eplant_decision --
    the same post-cap a_u/n that would meet the floor must not, once the full pre-cap set is
    below it."""
    gold = eplant.build_gold_ledger(
        FIXTURES / "gold_candidates.json", FIXTURES / "gold_verified_t01_only.json",
        manifest_path=FIXTURES / "manifest.json", root=FIXTURES, today=DAY,
        domain="Home storage and reheating of leftover food")
    measurements = eplant.gold_measurements(a_u=5, a_g=1, b=4, c=0, e=5, r_g=5, n=12,
                                            a_u_full=5, n_full=24, gold=gold)
    decision = eplant.run_eplant_gate(measurements)
    assert decision.outcome != "continue"
    assert "validity floor not met" in decision.reason


def test_gold_measurements_refuses_an_empty_criterion_ledger():
    empty_gold = Ledger(purpose="gold", claims=())
    with pytest.raises(ValidationError, match="names the claims"):
        eplant.gold_measurements(a_u=1, a_g=1, b=0, c=0, e=1, r_g=1, n=1, gold=empty_gold)


# --- pooling across domains + end-to-end score_eplant --------------------------------------------------

def test_pool_domains_and_score_eplant_end_to_end():
    gold = eplant.build_gold_ledger(
        FIXTURES / "gold_candidates.json", FIXTURES / "gold_verified_t01_only.json",
        manifest_path=FIXTURES / "manifest.json", root=FIXTURES, today=DAY,
        domain="Home storage and reheating of leftover food")

    domain_score = eplant.DomainScore(
        domain="d", targets=("t01",), excluded={},
        gated={"t01": eplant.TargetOutcome("t01", adopted_gated=False, adopted_strict=False,
                                           adopted_lenient=False, adopted_source_level=False,
                                           true_recovered=True)},
        ungated={"t01": True},
        exposure={"t01": True},
        planted_page_by_target={"t01": T1.planted_page_url},
        contradiction_recall={"n": 1, "linked": 1, "recall": 1.0, "both_located_n": 1,
                              "linked_upper_bound": 1, "recall_upper_bound": 1.0,
                              "both_located_upper_bound_n": 1, "detail": []},
        ungated_full={"t01": True},
        n_targets_full=1,
    )
    results = eplant.score_eplant([domain_score], gold)
    assert results["pooled"]["n"] == 1
    assert results["pooled"]["a_u"] == 1
    assert results["pooled"]["a_g"] == 0
    assert results["decision"]["outcome"] in {"continue", "stop", "change", "inconclusive"}
    markdown = eplant.render_markdown(results)
    assert "E-PLANT" in markdown and results["decision"]["outcome"].upper() in markdown


# --- CLI-facing helpers (no live calls) ---------------------------------------------------------

def test_load_targets_round_trips_the_fixture():
    ts = eplant.load_targets(FIXTURES / "targets.json")
    assert ts.domain == "Home storage and reheating of leftover food"
    assert [t.id for t in ts.targets] == ["t01", "t02"]
    assert ts.targets[0].true_page_urls == ("https://real-a.test/leftovers", "https://real-b.test/leftovers-2")


def test_load_targets_refuses_duplicate_ids(tmp_path):
    bad = tmp_path / "targets.json"
    bad.write_text(json.dumps({"domain": "d", "task": "t", "targets": [
        {"id": "dup", "question": "q", "anchor_terms": [], "true_variants": ["a"],
         "planted_variants": ["b"], "true_page_urls": ["u1", "u2"], "planted_page_url": "u3"},
        {"id": "dup", "question": "q2", "anchor_terms": [], "true_variants": ["a"],
         "planted_variants": ["b"], "true_page_urls": ["u1", "u2"], "planted_page_url": "u3"},
    ]}))
    with pytest.raises(ValueError, match="duplicate target ids"):
        eplant.load_targets(bad)


def test_run_baseline_builds_the_prompt_and_parses_the_reply():
    class _StubBackend:
        def __init__(self):
            self.calls = []

        def complete_json(self, task, system, user, schema):
            self.calls.append((task, system, user, schema))
            assert "URL: https://real-a.test/leftovers" in user
            assert "core temperature" in user
            return {"answers": [{"id": "t01", "answer": "55C"}, {"id": "t02", "answer": "10 days"}]}

    from residual.provenance import Agent as _Agent
    model = eplant.Model(agent=_Agent(kind="model", id="m", family="anthropic"), backend=_StubBackend())
    ts = eplant.load_targets(FIXTURES / "targets.json")
    answers = eplant.run_baseline(model=model, manifest_path=FIXTURES / "manifest.json", root=FIXTURES,
                                  targets=ts.targets)
    assert answers == {"t01": "55C", "t02": "10 days"}
