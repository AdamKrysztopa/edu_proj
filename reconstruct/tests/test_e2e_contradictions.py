"""Item 11: contradiction candidates are same-area pairs of located claims from different
independence clusters (A8). Only a "genuine" verdict with both quotes verbatim in their spans
becomes an N1 Contradiction; "scope"/"temporal" verdicts, and a "genuine" verdict whose quote is
not actually in the span, must never reach the ledger even though the model called it genuine.
"""
from __future__ import annotations

from pathlib import Path

from reconstruct.run import reconstruct
from residual.ledger import Ledger

from e2e_support import (
    TODAY, ScriptedBackend, http_client, make_models, page_from_fixture, read_json,
    script_default_decoys, search_result,
)

LABNOTES_URL = "https://labnotes.example/entry"
FIELDREPORT_URL = "https://fieldreport.example/entry"

# Deliberately dissimilar phrasing between the A/B pair of each fact (different sentence
# structure and vocabulary, not just a swapped number): the two pages must land in DIFFERENT
# independence clusters (A7), and near-identical templated sentences across the whole page
# push the 5-shingle containment over the 0.5 merge threshold regardless of area.
GENUINE_A = "Bench technicians must torque the coupling bolt to no more than forty newton metres before releasing the unit for testing."
GENUINE_B = "Field crews are instructed never to exceed eighty newton metres when tightening that same coupling bolt out in the yard."
SCOPE_A = "The pump receives its preventive maintenance visit every week without regard to how many hours it has actually run."
SCOPE_B = "Out in the field, however, nobody touches the pump for maintenance until it has logged five hundred hours of continuous operation."
BADQUOTE_A = "Feeler gauges are used to confirm the impeller sits three tenths of a millimetre clear of the housing wall."
BADQUOTE_B = "A different inspection method calls for six tenths of a millimetre of clearance around the impeller, measured with digital calipers instead."
UNRELATED_QUOTE = "The bench itself was resurfaced last spring and now has a bright yellow safety stripe painted along its front edge."


def _claim(assertion, quote, area):
    return {"assertion": assertion, "quote": quote, "area": area,
            "knowledge_type": "concept", "question": "domain"}


def test_contradiction_kinds_are_filtered_before_the_ledger(tmp_path):
    out = tmp_path / "run"
    pages = {LABNOTES_URL: page_from_fixture("contradictions_labnotes.html"),
              FIELDREPORT_URL: page_from_fixture("contradictions_fieldreport.html")}

    planner = ScriptedBackend(role="planner", family="anthropic")
    planner.script("plan", "", {"areas": [
        {"name": "Genuine Area", "queries": ["torque limit"]},
        {"name": "Scope Area", "queries": ["pump maintenance schedule"]},
        {"name": "Bad Quote Area", "queries": ["impeller clearance"]},
    ]})
    planner.script_search("torque limit", search_result(
        "torque limit", [(LABNOTES_URL, "t"), (FIELDREPORT_URL, "t")], TODAY))
    planner.script_search("pump maintenance schedule", search_result(
        "pump maintenance schedule", [(LABNOTES_URL, "t"), (FIELDREPORT_URL, "t")], TODAY))
    planner.script_search("impeller clearance", search_result(
        "impeller clearance", [(LABNOTES_URL, "t"), (FIELDREPORT_URL, "t")], TODAY))

    extractor = ScriptedBackend(role="extractor", family="anthropic")
    extractor.script("extract", "Field crews are instructed", {"claims": [
        _claim("The safe torque limit for the coupling bolt is eighty newton metres.", GENUINE_B, "Genuine Area"),
        _claim("Pump preventive maintenance runs after five hundred operating hours.", SCOPE_B, "Scope Area"),
        _claim("Impeller clearance is set to six tenths of a millimetre.", BADQUOTE_B, "Bad Quote Area"),
    ]})
    extractor.script("extract", "Bench technicians must torque", {"claims": [
        _claim("The safe torque limit for the coupling bolt is forty newton metres.", GENUINE_A, "Genuine Area"),
        _claim("Pump preventive maintenance runs on a fixed weekly schedule.", SCOPE_A, "Scope Area"),
        _claim("Impeller clearance is set to three tenths of a millimetre.", BADQUOTE_A, "Bad Quote Area"),
    ]})

    # distinctive fragments, not quote[:N] — GENUINE_A/B (and the other pairs) share a long
    # identical prefix, so a plain prefix match would let the first-registered entry steal the
    # second call.
    verifier = ScriptedBackend(role="verifier", family="openai")
    for fragment, quote in [("forty newton metres", GENUINE_A), ("eighty newton metres", GENUINE_B),
                              ("fixed weekly schedule", SCOPE_A), ("five hundred operating hours", SCOPE_B),
                              ("three tenths of a millimetre", BADQUOTE_A), ("six tenths of a millimetre", BADQUOTE_B)]:
        verifier.script("verify", fragment, {"verdict": "supports", "supporting_quote": quote})
    script_default_decoys(extractor, verifier)

    contradiction = ScriptedBackend(role="contradiction", family="openai")
    contradiction.script("contradict", "coupling bolt",
                          {"kind": "genuine", "quote_a": GENUINE_A, "quote_b": GENUINE_B})
    contradiction.script("contradict", "Pump preventive maintenance runs",
                          {"kind": "scope", "quote_a": SCOPE_A, "quote_b": SCOPE_B})
    contradiction.script("contradict", "Impeller clearance is set to",
                          {"kind": "genuine", "quote_a": UNRELATED_QUOTE, "quote_b": BADQUOTE_B})

    models = make_models(planner=planner, extractor=extractor, verifier=verifier,
                          contradiction=contradiction, out=out)
    run_dir = Path(reconstruct(domain="maintenance", task="t", models=models, http=http_client(pages),
                                out=out, today=TODAY, max_results=5))

    ledger = Ledger.from_json((run_dir / "ledger.json").read_text())
    sidecar = read_json(run_dir / "sidecar.json")

    def claim_id_for(fragment):
        matches = [c.claim_id for c in ledger.claims if fragment in c.assertion]
        assert len(matches) == 1, f"expected exactly one claim matching {fragment!r}, got {matches}"
        return matches[0]

    genuine_pair = {claim_id_for("forty newton metres"), claim_id_for("eighty newton metres")}
    scope_pair = {claim_id_for("fixed weekly schedule"), claim_id_for("five hundred operating hours")}
    badquote_pair = {claim_id_for("three tenths of a millimetre"), claim_id_for("six tenths of a millimetre")}

    ledger_pairs = [set(x.claims) for x in ledger.contradictions]
    assert genuine_pair in ledger_pairs, "a genuine verdict with both quotes verbatim in span must reach the ledger"
    assert scope_pair not in ledger_pairs, "a scope verdict must never reach the ledger"
    assert badquote_pair not in ledger_pairs, "a genuine verdict whose quote is not in the span must not reach the ledger"
    assert len(ledger.contradictions) == 1

    sidecar_kinds = {(frozenset(x["claims"]), x["kind"]): x["recorded_in_ledger"]
                      for x in sidecar["contradictions"]}
    scope_entries = [v for (pair, kind), v in sidecar_kinds.items() if kind == "scope"]
    assert scope_entries and all(v is False for v in scope_entries)
