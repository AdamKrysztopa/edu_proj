"""SHOULD 2: the cross-cluster re-verification pass replaces the pairwise contradiction stage.
For each supported claim, the top same-area located spans from OTHER independence clusters are
re-verified against the claim's own assertion with the SAME verifier: a REFUTES verdict adds a
refuting Evidence and records an N1 Contradiction; a SUPPORTS verdict adds a corroborating
Evidence (corroboration grows); a verbatim-duplicate span (A's `span_duplicates`) is filtered out
before it is ever offered as a candidate, so it adds no extra corroboration and is never even
sent to the verifier.
"""
from __future__ import annotations

from pathlib import Path

from reconstruct.run import reconstruct
from residual.ledger import Ledger

from e2e_support import (
    TODAY, Page, ScriptedBackend, http_client, make_models, read_json, script_default_decoys,
    search_result,
)

# --- Refutes Area: two claims from different clusters that genuinely disagree -------------------
GENUINE_A = ("Bench technicians must torque the coupling bolt to no more than forty newton "
             "metres before releasing the unit for testing.")
GENUINE_B = ("Field crews are instructed never to exceed eighty newton metres when tightening "
             "that same coupling bolt out in the yard.")

# --- Corroborate Area: two claims from different clusters that genuinely agree ------------------
PM_A = ("The pump receives a scheduled preventive maintenance visit every calendar month "
        "regardless of how many hours it has run.")
PM_B = ("Out in the field, technicians perform preventive maintenance on the pump on a fixed "
        "monthly schedule, never tied to operating hours.")

# --- Duplicate Span Area: two different clusters quoting the identical >=25-word passage --------
SHARED_QUOTE = ("All maintenance personnel must isolate electrical power at the source disconnect "
                "and confirm a zero energy state with a calibrated meter before opening any "
                "control panel enclosure for inspection.")

BENCH_URL = "https://bench-notes.example/entry"
FIELD_URL = "https://field-report.example/entry"
PLANT_URL = "https://plant-log.example/pm"
HANDBOOK_URL = "https://site-handbook.example/pm"
STANDARD_X_URL = "https://standard-x.example/rule"
STANDARD_Y_URL = "https://standard-y.example/rule"


def _filler(tag: str) -> str:
    """Comfortably over 500 chars of padding so the page clears the fetch layer's near-empty-page
    floor. Every token is tag-prefixed nonsense, not a shared template with `tag` substituted in a
    few places — a templated filler would give every page near-identical 5-word shingles and
    wrongly cluster all of them together by containment (the E-LIVE "SEO template" failure mode
    this test exists to guard against), regardless of their real, distinct content."""
    return " ".join(f"{tag}pad{i}" for i in range(60))


def _page(*paragraphs: str, tag: str = "generic") -> Page:
    body = ("<!doctype html><html><body>" + "".join(f"<p>{p}</p>" for p in paragraphs)
           + f"<p>{_filler(tag)}</p></body></html>")
    return Page(body=body)


def _claim(assertion: str, quote: str, area: str) -> dict:
    return {"assertion": assertion, "quote": quote, "area": area,
            "knowledge_type": "concept", "question": "domain"}


def _supports(quote: str) -> dict:
    return {"verdict": "supports", "supporting_quote": quote, "adds_content": False,
            "subject_or_scope_differs": False, "quantifier_modality_or_connective_differs": False}


def _refutes(quote: str) -> dict:
    return {"verdict": "refutes", "supporting_quote": quote, "adds_content": False,
            "subject_or_scope_differs": False, "quantifier_modality_or_connective_differs": False}


def test_cross_verify_refutes_corroborates_and_ignores_duplicate_spans(tmp_path):
    out = tmp_path / "run"
    pages = {
        BENCH_URL: _page(GENUINE_A, tag="bench"),
        FIELD_URL: _page(GENUINE_B, tag="field"),
        PLANT_URL: _page(PM_A, tag="plant"),
        HANDBOOK_URL: _page(PM_B, tag="handbook"),
        STANDARD_X_URL: _page(SHARED_QUOTE, "STANDARDX-ONLY-FILLER-MARKER unrelated to anything else here.",
                              tag="standardx"),
        STANDARD_Y_URL: _page(SHARED_QUOTE, "STANDARDY-ONLY-FILLER-MARKER covering a wholly different topic.",
                              tag="standardy"),
    }

    planner = ScriptedBackend(role="planner", family="anthropic")
    planner.script("plan", "", {"areas": [
        {"name": "Refutes Area", "queries": ["torque limit"]},
        {"name": "Corroborate Area", "queries": ["pump pm schedule"]},
        {"name": "Duplicate Span Area", "queries": ["lockout tagout rule"]},
    ]})
    planner.script_search("torque limit", search_result(
        "torque limit", [(BENCH_URL, "t"), (FIELD_URL, "t")], TODAY))
    planner.script_search("pump pm schedule", search_result(
        "pump pm schedule", [(PLANT_URL, "t"), (HANDBOOK_URL, "t")], TODAY))
    planner.script_search("lockout tagout rule", search_result(
        "lockout tagout rule", [(STANDARD_X_URL, "t"), (STANDARD_Y_URL, "t")], TODAY))

    CLAIM_A = "The safe torque limit for the coupling bolt is forty newton metres."
    CLAIM_B = "The safe torque limit for the coupling bolt is eighty newton metres."
    CLAIM_C = "Pump preventive maintenance follows a fixed monthly schedule."
    CLAIM_D = "The pump receives monthly preventive maintenance regardless of hours run."
    CLAIM_E = "Personnel must isolate power and confirm zero energy before opening a control panel."
    CLAIM_F = "Before opening a control panel, power must be isolated and zero energy confirmed."

    extractor = ScriptedBackend(role="extractor", family="anthropic")
    extractor.script("extract", "Bench technicians must torque",
                     {"claims": [_claim(CLAIM_A, GENUINE_A, "Refutes Area")]})
    extractor.script("extract", "Field crews are instructed",
                     {"claims": [_claim(CLAIM_B, GENUINE_B, "Refutes Area")]})
    extractor.script("extract", "scheduled preventive maintenance visit",
                     {"claims": [_claim(CLAIM_C, PM_A, "Corroborate Area")]})
    extractor.script("extract", "technicians perform preventive maintenance",
                     {"claims": [_claim(CLAIM_D, PM_B, "Corroborate Area")]})
    extractor.script("extract", "STANDARDX-ONLY-FILLER-MARKER",
                     {"claims": [_claim(CLAIM_E, SHARED_QUOTE, "Duplicate Span Area")]})
    extractor.script("extract", "STANDARDY-ONLY-FILLER-MARKER",
                     {"claims": [_claim(CLAIM_F, SHARED_QUOTE, "Duplicate Span Area")]})

    verifier = ScriptedBackend(role="verifier", family="openai")

    def _a_response(text):
        return _supports(GENUINE_A) if "Bench technicians must torque" in text else _refutes(GENUINE_B)

    def _b_response(text):
        return _supports(GENUINE_B) if "Field crews are instructed" in text else _refutes(GENUINE_A)

    def _c_response(text):
        return _supports(PM_A) if "every calendar month" in text else _supports(PM_B)

    def _d_response(text):
        return _supports(PM_B) if "never tied to operating hours" in text else _supports(PM_A)

    verifier.script("verify", CLAIM_A, _a_response)
    verifier.script("verify", CLAIM_B, _b_response)
    verifier.script("verify", CLAIM_C, _c_response)
    verifier.script("verify", CLAIM_D, _d_response)
    verifier.script("verify", CLAIM_E, _supports(SHARED_QUOTE))
    verifier.script("verify", CLAIM_F, _supports(SHARED_QUOTE))
    script_default_decoys(extractor, verifier)

    models = make_models(planner=planner, extractor=extractor, verifier=verifier, out=out)
    run_dir = Path(reconstruct(domain="maintenance", task="t", models=models, http=http_client(pages),
                                out=out, today=TODAY, max_results=5))

    ledger = Ledger.from_json((run_dir / "ledger.json").read_text())
    sidecar = read_json(run_dir / "sidecar.json")
    assert sidecar["complete"] is True, sidecar["incomplete_reasons"]

    def claim_id_for(fragment):
        matches = [c.claim_id for c in ledger.claims if fragment in c.assertion]
        assert len(matches) == 1, f"expected exactly one claim matching {fragment!r}, got {matches}"
        return matches[0]

    # --- REFUTES cross-check -> N1 Contradiction --------------------------------------------
    cid_a, cid_b = claim_id_for("forty newton metres"), claim_id_for("eighty newton metres")
    ledger_pairs = [set(x.claims) for x in ledger.contradictions]
    assert {cid_a, cid_b} in ledger_pairs

    # --- SUPPORTS cross-check from another cluster -> corroboration grows to 2 ----------------
    claim_c = ledger.by_id[claim_id_for("fixed monthly schedule")]
    assert claim_c.corroboration == 2

    # --- verbatim-duplicate span -> no extra corroboration, never even sent to the verifier ----
    claim_e = ledger.by_id[claim_id_for("confirm zero energy before opening")]
    assert claim_e.corroboration == 1
    assert len(claim_e.evidence) == 1
    cross_check_claim_ids = {c["claim_id"] for c in sidecar["cross_checks"]}
    assert claim_e.claim_id not in cross_check_claim_ids
