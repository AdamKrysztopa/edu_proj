"""Items 2, 3, 4, 8, 13: the verification step itself — fabrication, a supporting_quote outside
the span, same-family self-verification, the verifier's bounded payload, and a served-model
mismatch raised by the verifier backend.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from reconstruct.llm import ServedModelMismatch
from reconstruct.run import reconstruct
from residual.ledger import Ledger
from residual.vocab import EpistemicLabel

from e2e_support import (
    DECOY_MARKER, TODAY, ScriptedBackend, find_claim, http_client, make_models, page_from_fixture,
    read_json, script_default_decoys, search_result,
)

CRITERION_LABELS = {EpistemicLabel.OBSERVED_HUMAN_EVIDENCE, EpistemicLabel.LITERATURE_SUPPORTED,
                    EpistemicLabel.ORGANISATIONAL_ARTEFACT_SUPPORTED}


def _one_page_run(tmp_path, *, url, fixture, area, quote, verify_response=None,
                   verifier_family="openai", extractor_family="anthropic", assertion=None):
    out = tmp_path / "run"
    pages = {url: page_from_fixture(fixture)}

    planner = ScriptedBackend(role="planner", family="anthropic")
    planner.script("plan", "", {"areas": [{"name": area, "queries": ["reference"]}]})
    planner.script_search("reference", search_result("reference", [(url, "title")], TODAY))

    extractor = ScriptedBackend(role="extractor", family=extractor_family)
    extractor.script("extract", "", {
        "claims": [{"assertion": assertion or quote, "quote": quote, "area": area,
                    "knowledge_type": "concept", "question": "domain"}]
    })

    verifier = ScriptedBackend(role="verifier", family=verifier_family)
    if verify_response is not None:
        verifier.script("verify", "", verify_response)
    script_default_decoys(extractor, verifier)

    contradiction = ScriptedBackend(role="contradiction", family="openai")

    models = make_models(planner=planner, extractor=extractor, verifier=verifier,
                          contradiction=contradiction, out=out)
    run_dir = Path(reconstruct(domain="physics", task="t", models=models, http=http_client(pages),
                                out=out, today=TODAY, max_results=5))
    return run_dir, extractor, verifier


# --- item 2: fabricated quote --------------------------------------------------------------------

def test_fabricated_quote_gets_no_evidence_and_is_synthetic(tmp_path):
    fabricated = "The boundary layer is entirely imaginary and was never described on this page."
    run_dir, extractor, verifier = _one_page_run(
        tmp_path, url="https://fabricate.example/page", fixture="fabricated_source.html",
        area="Fluids", quote=fabricated)

    ledger = Ledger.from_json((run_dir / "ledger.json").read_text())
    claim = find_claim(ledger, fabricated[:30])
    assert claim.evidence == ()
    assert claim.label == EpistemicLabel.SYNTHETIC_EXTRAPOLATION
    assert verifier.calls == [], "an unlocated quote must never reach the verifier"

    sidecar = read_json(run_dir / "sidecar.json")
    extractions = [e for e in sidecar["extractions"] if e["quote"] == fabricated]
    assert extractions and extractions[0]["located"] is False
    assert sidecar["stats"]["unlocated_rate"] > 0


# --- item 3: supporting_quote not inside the located span -----------------------------------------

def test_supporting_quote_outside_span_is_recorded_insufficient_not_supported(tmp_path):
    quote = ("Thermal conductivity measures how readily a material conducts heat energy through "
             "it under a temperature gradient.")
    outside_quote = ("Convection instead relies on the bulk motion of a fluid to carry heat "
                      "energy from one place to another.")
    run_dir, extractor, verifier = _one_page_run(
        tmp_path, url="https://span-check.example/page", fixture="insufficient_source.html",
        area="Heat", quote=quote,
        verify_response={"verdict": "supports", "supporting_quote": outside_quote})

    ledger = Ledger.from_json((run_dir / "ledger.json").read_text())
    claim = find_claim(ledger, quote[:30])
    assert len(claim.evidence) == 1
    ev = claim.evidence[0]
    assert ev.verification.verdict == "insufficient"
    assert claim.label != EpistemicLabel.LITERATURE_SUPPORTED
    assert claim.supporting == ()


# --- item 4: same-family verifier == extractor family ----------------------------------------------

def test_same_family_verifier_never_produces_supports_or_criterion_labels(tmp_path):
    quote = "Momentum is the product of an object's mass and its velocity, and the total momentum of an isolated system is conserved."
    run_dir, extractor, verifier = _one_page_run(
        tmp_path, url="https://selffamily.example/page", fixture="selffamily_source.html",
        area="Mechanics", quote=quote, verifier_family="anthropic", extractor_family="anthropic",
        verify_response={"verdict": "supports", "supporting_quote": quote})

    assert verifier.calls == [], "run.py must refuse to call a same-family verifier at all"

    ledger = Ledger.from_json((run_dir / "ledger.json").read_text())
    all_evidence = [e for c in ledger.claims for e in c.evidence]
    assert all(e.verification.verdict != "supports" for e in all_evidence)
    assert all(c.label != EpistemicLabel.UNKNOWN for c in ledger.claims)
    assert all(c.label not in CRITERION_LABELS for c in ledger.claims)

    sidecar = read_json(run_dir / "sidecar.json")
    assert sidecar["slots"], "expected at least one slot to be recorded"
    assert any(s["status"] == "unverified" for s in sidecar["slots"])
    assert not any(s["status"] in ("covered", "unknown") for s in sidecar["slots"])


# --- item 8: verifier payload is bounded and never carries the page URL -----------------------------

def test_verifier_payload_excludes_url_and_is_bounded_in_size(tmp_path):
    quote = ("A safety factor is the ratio between a structure's actual capacity and the load it "
             "is required to withstand in service.")
    url = "https://bigpage.example/reference"
    run_dir, extractor, verifier = _one_page_run(
        tmp_path, url=url, fixture="payload_bound_source.html", area="Structures", quote=quote,
        verify_response={"verdict": "supports", "supporting_quote": quote})

    # A6 makes a decoy verify call unavoidable once this run has a located claim (script_default
    # _decoys, wired in by _one_page_run) — separate it from the real claim's own verify call
    # rather than dropping the bound check to one call.
    real_calls = [c for c in verifier.calls if DECOY_MARKER not in c.user]
    decoy_calls = [c for c in verifier.calls if DECOY_MARKER in c.user]
    assert len(real_calls) == 1
    assert len(decoy_calls) == 1

    for call in (real_calls[0], decoy_calls[0]):
        assert url not in call.user
        assert "bigpage.example" not in call.user
        # span (quote) + up to 2x300 chars of surrounding context + a generous heading/formatting
        # allowance — this must not be anywhere close to the size of the (huge) fetched page.
        assert len(call.user) <= len(quote) + 2 * 300 + 700


# --- item 13: ServedModelMismatch from the verifier backend -----------------------------------------

def test_served_model_mismatch_leaves_evidence_pending_and_run_continues(tmp_path):
    out = tmp_path / "run"
    url_a = "https://kinematics-a.example/notes"
    url_b = "https://span-check.example/page"
    quote_a = ("Displacement is defined as the vector change in an object's position measured from a "
               "fixed reference point, which differs from distance because it captures direction as "
               "well as magnitude.")
    quote_b = ("Thermal conductivity measures how readily a material conducts heat energy through "
               "it under a temperature gradient.")
    pages = {url_a: page_from_fixture("happy_kinematics_a.html"),
             url_b: page_from_fixture("insufficient_source.html")}

    planner = ScriptedBackend(role="planner", family="anthropic")
    planner.script("plan", "", {"areas": [
        {"name": "Kinematics", "queries": ["kinematics reference"]},
        {"name": "Heat", "queries": ["heat reference"]},
    ]})
    planner.script_search("kinematics", search_result("kinematics reference", [(url_a, "t")], TODAY))
    planner.script_search("heat", search_result("heat reference", [(url_b, "t")], TODAY))

    extractor = ScriptedBackend(role="extractor", family="anthropic")
    extractor.script("extract", "vector change", {"claims": [
        {"assertion": "Displacement is a vector change in position.", "quote": quote_a,
         "area": "Kinematics", "knowledge_type": "concept", "question": "domain"}]})
    extractor.script("extract", "Thermal conductivity", {"claims": [
        {"assertion": "Thermal conductivity measures heat conduction.", "quote": quote_b,
         "area": "Heat", "knowledge_type": "concept", "question": "domain"}]})

    verifier = ScriptedBackend(role="verifier", family="openai")
    verifier.script("verify", "vector change", ServedModelMismatch("verify: served a different model"))
    verifier.script("verify", "Thermal conductivity", {"verdict": "supports", "supporting_quote": quote_b})
    script_default_decoys(extractor, verifier)

    contradiction = ScriptedBackend(role="contradiction", family="openai")
    models = make_models(planner=planner, extractor=extractor, verifier=verifier,
                          contradiction=contradiction, out=out)

    run_dir = Path(reconstruct(domain="physics", task="t", models=models, http=http_client(pages),
                                out=out, today=TODAY, max_results=5))

    ledger = Ledger.from_json((run_dir / "ledger.json").read_text())
    mismatched = find_claim(ledger, "Displacement is a vector change")
    assert all(e.verification.verdict == "pending" for e in mismatched.evidence)

    survivor = find_claim(ledger, "Thermal conductivity measures heat conduction")
    assert survivor.label == EpistemicLabel.LITERATURE_SUPPORTED, "the run must continue past the mismatch"


# --- drift flags veto SUPPORTS (E-LIVE v1 scope-drift regression) ---------------------------------

@pytest.mark.parametrize("flag", ["adds_content", "subject_or_scope_differs",
                                  "quantifier_modality_or_connective_differs"])
def test_supports_with_any_drift_flag_is_downgraded_to_insufficient(tmp_path, flag):
    quote = ("Thermal conductivity measures how readily a material conducts heat energy through "
             "it under a temperature gradient.")
    run_dir, extractor, verifier = _one_page_run(
        tmp_path, url="https://span-check.example/page", fixture="insufficient_source.html",
        area="Heat", quote=quote, assertion="Thermal conductivity always measures heat conduction.",
        verify_response={"verdict": "supports", "supporting_quote": quote, flag: True})

    ledger = Ledger.from_json((run_dir / "ledger.json").read_text())
    claim = find_claim(ledger, "Thermal conductivity always")
    assert [e.verification.verdict for e in claim.evidence] == ["insufficient"]
    assert claim.supporting == ()
    assert claim.label == EpistemicLabel.SYNTHETIC_EXTRAPOLATION
