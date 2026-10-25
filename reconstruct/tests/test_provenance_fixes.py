"""I9: the provenance fixes specified in research/n2/final_adversarial_review.md (R3, R4, R9) plus a
minimum length for `quote_in_span`. Each fix has a planted positive the old code missed and a
trivial stand-in the new rule must not fire on (L7.3)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from reconstruct.evidence import (
    CopyItem,
    collapse_verbatim_copies,
    decoy_is_valid,
    fold,
    is_verbatim_copy,
    normalise,
    quote_in_span,
    span_duplicates,
)
from reconstruct.run import _verdict_from_result, reconstruct
from reconstruct.verify_run import verify_run
from residual.ledger import Ledger
from residual.provenance import Verdict

from e2e_support import (
    TODAY, Page, ScriptedBackend, http_client, make_models, read_json, script_default_decoys,
    search_result,
)


# --- quote_in_span minimum length ---------------------------------------------------------------

SPAN = normalise("The pump loses prime when suction lift exceeds its rated limit at the inlet.")


def test_quote_in_span_rejects_a_quote_under_five_words():
    assert not quote_in_span("the", SPAN)
    assert not quote_in_span("suction lift exceeds its", SPAN)


def test_quote_in_span_accepts_a_five_word_substring():
    assert quote_in_span("suction lift exceeds its rated", SPAN)


def test_quote_in_span_on_a_span_shorter_than_five_words_needs_the_whole_span():
    short = normalise("Isolate before opening.")
    assert quote_in_span("Isolate before opening.", short)
    assert not quote_in_span("before opening.", short)


def test_quote_in_span_still_rejects_a_long_quote_outside_the_span():
    assert not quote_in_span("impellers wear faster once cavitation has begun", SPAN)


def test_a_one_word_supporting_quote_downgrades_supports_to_insufficient():
    result = {"verdict": "supports", "supporting_quote": "pump", "adds_content": False,
              "subject_or_scope_differs": False,
              "quantifier_modality_or_connective_differs": False}
    verdict, _, _ = _verdict_from_result(result, SPAN)
    assert verdict == "insufficient"


# --- R3: whitespace- and case-robust shingling, verbatim copies -----------------------------------

SHARED_30 = " ".join(f"tok{i}" for i in range(30))


def test_fold_casefolds_and_collapses_whitespace():
    assert fold("The  Pump\nLoses   PRIME") == "the pump loses prime"


def test_span_duplicates_survives_a_case_difference():
    spans = [("sp-a", "ind-1", SHARED_30), ("sp-b", "ind-2", SHARED_30.upper())]
    assert span_duplicates(spans) == {"sp-a": "sp-a", "sp-b": "sp-a"}


def test_span_duplicates_survives_a_doubled_space():
    spans = [("sp-a", "ind-1", SHARED_30), ("sp-b", "ind-2", SHARED_30.replace(" ", "  ", 3))]
    assert span_duplicates(spans)["sp-b"] == "sp-a"


def test_span_duplicates_still_ignores_a_24_word_shared_run():
    run24 = " ".join(f"tok{i}" for i in range(24))
    spans = [("sp-a", "ind-1", run24 + " alpha only"), ("sp-b", "ind-2", "beta only " + run24)]
    assert span_duplicates(spans) == {"sp-a": "sp-a", "sp-b": "sp-b"}


PASSAGE = "operators must log every manual override of the interlock in the shift book"
DOC_X = fold(f"Section 4. The interlock exists for a reason. {PASSAGE.upper()}. End of section.")
DOC_Y = fold(f"Quoting the vendor manual: {PASSAGE}. Our site adds nothing to this.")
DOC_Z = fold("Independent guidance: a shift book entry records the time, the reason and the "
             "operator's name, and the supervisor countersigns it before handover.")


def test_a_short_span_copied_verbatim_into_another_document_is_a_copy():
    assert is_verbatim_copy(PASSAGE, DOC_Y, PASSAGE, DOC_X)


def test_a_span_is_a_copy_when_either_side_contains_the_other():
    own_span = "Our site adds nothing to this."
    assert not is_verbatim_copy(own_span, DOC_Y, "Section 4. The interlock exists", DOC_X)
    assert is_verbatim_copy(own_span, DOC_Y, PASSAGE, DOC_X)


def test_spans_sharing_only_common_words_are_not_copies():
    z_span = "a shift book entry records the time, the reason and the operator's name"
    assert not is_verbatim_copy(PASSAGE, DOC_X, z_span, DOC_Z)


def test_collapse_keeps_one_of_two_verbatim_copies_across_clusters():
    items = [CopyItem("e1", "ind-x", PASSAGE, DOC_X), CopyItem("e2", "ind-y", PASSAGE, DOC_Y)]
    assert collapse_verbatim_copies(items) == {"e2": "e1"}


def test_collapse_never_collapses_within_one_cluster():
    items = [CopyItem("e1", "ind-x", PASSAGE, DOC_X), CopyItem("e2", "ind-x", PASSAGE, DOC_Y)]
    assert collapse_verbatim_copies(items) == {}


def test_collapse_drops_a_cluster_whose_only_span_the_other_cluster_also_carries():
    z_span = "the supervisor countersigns it before handover"
    doc_yz = fold(DOC_Y + " " + DOC_Z)
    items = [CopyItem("e1", "ind-x", PASSAGE, DOC_X), CopyItem("e2", "ind-y", PASSAGE, doc_yz),
             CopyItem("e3", "ind-y", z_span, doc_yz)]
    copies = collapse_verbatim_copies(items)
    assert copies == {"e1": "e2"}
    assert {i.independence_key for i in items if i.item_id not in copies} == {"ind-y"}


def test_collapse_counts_a_shared_passage_once_beside_an_independent_cluster():
    z_span = "a shift book entry records the time, the reason and the operator's name"
    items = [CopyItem("e1", "ind-x", PASSAGE, DOC_X), CopyItem("e2", "ind-y", PASSAGE, DOC_Y),
             CopyItem("e3", "ind-z", z_span, DOC_Z)]
    copies = collapse_verbatim_copies(items)
    assert copies == {"e2": "e1"}
    assert {i.independence_key for i in items if i.item_id not in copies} == {"ind-x", "ind-z"}


def test_collapse_leaves_independent_spans_alone():
    z_span = "a shift book entry records the time, the reason and the operator's name"
    items = [CopyItem("e1", "ind-x", PASSAGE, DOC_X), CopyItem("e2", "ind-z", z_span, DOC_Z)]
    assert collapse_verbatim_copies(items) == {}


# --- decoys: current behaviour only (DS6 decides the rubric) --------------------------------------

def test_decoy_is_valid_current_behaviour_is_self_certified():
    assert decoy_is_valid("Torque to 40 Nm.", "Torque to 40 Nm!", "differs")
    assert decoy_is_valid("Torque to 40 Nm.", "Torque to 40 Nm.  ", "x") is False
    assert decoy_is_valid("Torque to 40 Nm.", "TORQUE TO 40 NM.", "x") is False
    assert decoy_is_valid("Torque to 40 Nm.", "Torque to 80 Nm.", "   ") is False
    assert decoy_is_valid("Torque to 40 Nm.", "Torque to 80 Nm.", "any non-empty text")


# --- end-to-end fixtures ------------------------------------------------------------------------

def _filler(tag: str) -> str:
    return " ".join(f"{tag}pad{i}" for i in range(60))


def _page(*paragraphs: str, tag: str) -> Page:
    body = ("<!doctype html><html><body>" + "".join(f"<p>{p}</p>" for p in paragraphs)
            + f"<p>{_filler(tag)}</p></body></html>")
    return Page(body=body)


def _claim(assertion: str, quote: str, area: str) -> dict:
    return {"assertion": assertion, "quote": quote, "area": area,
            "knowledge_type": "concept", "question": "domain"}


def _marked(text: str) -> str:
    """The span under judgement; the verify prompt's own '>>>like this<<<' example comes first."""
    return text.rsplit(">>>", 1)[1].split("<<<", 1)[0]


def _verdict(verdict: str, quote: str, *, scope: bool = False) -> dict:
    return {"verdict": verdict, "supporting_quote": quote, "adds_content": False,
            "subject_or_scope_differs": scope, "quantifier_modality_or_connective_differs": False}


def _run(tmp_path, *, areas, searches, pages, extracts, verifies) -> tuple[Path, Ledger, dict]:
    out = tmp_path / "run"
    planner = ScriptedBackend(role="planner", family="anthropic")
    planner.script("plan", "", {"areas": areas})
    for query, urls in searches.items():
        planner.script_search(query, search_result(query, [(u, "t") for u in urls], TODAY))
    extractor = ScriptedBackend(role="extractor", family="anthropic")
    for marker, claims in extracts:
        extractor.script("extract", marker, {"claims": claims})
    verifier = ScriptedBackend(role="verifier", family="openai")
    for marker, response in verifies:
        verifier.script("verify", marker, response)
    script_default_decoys(extractor, verifier)
    models = make_models(planner=planner, extractor=extractor, verifier=verifier, out=out)
    run_dir = Path(reconstruct(domain="maintenance", task="t", models=models, http=http_client(pages),
                               out=out, today=TODAY, max_results=5))
    sidecar = read_json(run_dir / "sidecar.json")
    assert sidecar["complete"] is True, sidecar["incomplete_reasons"]
    return run_dir, Ledger.from_json((run_dir / "ledger.json").read_text()), sidecar


def _claim_id(ledger: Ledger, fragment: str) -> str:
    matches = [c.claim_id for c in ledger.claims if fragment in c.assertion]
    assert len(matches) == 1, matches
    return matches[0]


def _slot(sidecar: dict, ledger: Ledger, area_name: str, probe: str = "concept") -> dict:
    area_id = next(a.area_id for a in ledger.areas if a.name == area_name)
    return next(s for s in sidecar["slots"] if s["area_id"] == area_id and s["probe"] == probe)


X_URL, Y_URL = "https://vendor-manual.example/interlock", "https://site-notes.example/interlock"
U_URL, V_URL = "https://plant-u.example/log", "https://plant-v.example/log"
ORIG_X = "The interlock must be tested at the start of every shift using the bypass key."
U_TEXT = "A shift book entry records the override time and the reason for bypassing the guard."
V_TEXT = "Supervisors countersign each shift book entry before the outgoing crew leaves site."


def test_r3_copied_short_span_is_not_corroboration_and_does_not_cover_a_slot(tmp_path):
    claim_g = "The interlock is tested at every shift start with the bypass key."
    claim_h = "Every manual interlock override is logged in the shift book."
    claim_u = "Shift book entries record override time and reason."
    claim_v = "Supervisors countersign shift book entries at handover."

    def supports_own(own_text):
        return lambda text: (_verdict("supports", own_text) if f">>>{own_text}<<<" in text
                             else _verdict("supports", _marked(text)))

    def insufficient_other(own_text):
        return lambda text: (_verdict("supports", own_text) if f">>>{own_text}<<<" in text
                             else _verdict("insufficient", ""))

    run_dir, ledger, sidecar = _run(
        tmp_path,
        areas=[{"name": "Copy Area", "queries": ["copy q"]},
               {"name": "Independent Area", "queries": ["indep q"]}],
        searches={"copy q": [X_URL, Y_URL], "indep q": [U_URL, V_URL]},
        pages={X_URL: _page(ORIG_X, PASSAGE.upper() + ".", tag="vendor"),
               Y_URL: _page("Quoting the vendor manual: " + PASSAGE + ".", tag="site"),
               U_URL: _page(U_TEXT, tag="plantu"), V_URL: _page(V_TEXT, tag="plantv")},
        extracts=[("start of every shift", [_claim(claim_g, ORIG_X, "Copy Area")]),
                  ("Quoting the vendor manual", [_claim(claim_h, PASSAGE, "Copy Area")]),
                  ("override time and the reason", [_claim(claim_u, U_TEXT, "Independent Area")]),
                  ("Supervisors countersign", [_claim(claim_v, V_TEXT, "Independent Area")])],
        verifies=[(claim_g, supports_own(ORIG_X)), (claim_h, supports_own(PASSAGE)),
                  (claim_u, insufficient_other(U_TEXT)), (claim_v, insufficient_other(V_TEXT))])

    cid_g, cid_h = _claim_id(ledger, "bypass key"), _claim_id(ledger, "logged in the shift book")
    assert ledger.by_id[cid_g].corroboration == 1
    assert ledger.by_id[cid_h].corroboration == 1
    assert not [c for c in sidecar["cross_checks"] if c["claim_id"] in (cid_g, cid_h)]
    assert sidecar["stats"]["n_cross_candidates_verbatim_copy"] == 2
    copy_slot = _slot(sidecar, ledger, "Copy Area")
    assert copy_slot["status"] == "thin"
    assert copy_slot["n_verbatim_copies"] == 1

    indep_slot = _slot(sidecar, ledger, "Independent Area")
    assert indep_slot["status"] == "covered"
    assert indep_slot["n_verbatim_copies"] == 0
    assert len([c for c in sidecar["cross_checks"]
                if c["claim_id"] in (_claim_id(ledger, "override time"),
                                     _claim_id(ledger, "countersign"))]) == 2


M1_URL, M2_URL = "https://regulator-one.example/guide", "https://regulator-two.example/guide"
MERGE_PASSAGE = "a controller must consult the supervisory authority before high risk processing"


def test_r3_identical_assertion_merge_does_not_bypass_the_copy_check(tmp_path):
    assertion = "Controllers consult the authority before high-risk processing."
    run_dir, ledger, sidecar = _run(
        tmp_path,
        areas=[{"name": "Merge Area", "queries": ["merge q"]}],
        searches={"merge q": [M1_URL, M2_URL]},
        pages={M1_URL: _page("Article guidance: " + MERGE_PASSAGE + ".", tag="regone"),
               M2_URL: _page("As the statute says, " + MERGE_PASSAGE.capitalize() + ".", tag="regtwo")},
        extracts=[("Article guidance", [_claim(assertion, MERGE_PASSAGE, "Merge Area")]),
                  ("As the statute says", [_claim(assertion, MERGE_PASSAGE.capitalize(), "Merge Area")])],
        verifies=[(assertion, lambda text: _verdict(
            "supports", _marked(text)))])

    claim = ledger.by_id[_claim_id(ledger, "consult the authority")]
    assert claim.corroboration == 1
    assert len(claim.evidence) == 1
    copies = [e for e in sidecar["extractions"] if e.get("verbatim_copy_of")]
    assert len(copies) == 1
    assert copies[0]["verbatim_copy_of"] == claim.evidence[0].source.source_id
    assert sidecar["stats"]["n_verbatim_copies_merged"] == 1
    assert _slot(sidecar, ledger, "Merge Area")["status"] == "thin"


S1_URL, S2_URL = "https://dpia-guide.example/art35", "https://prior-consult.example/art36"
ART35 = "A data protection impact assessment is required before processing likely to result in high risk."
ART36 = "Prior consultation with the authority is required only where residual high risk remains."


def test_r4_scope_flagged_refutes_is_reported_apart_and_is_not_a_contradiction(tmp_path):
    claim_a = "A DPIA is required before high-risk processing."
    claim_b = "Prior consultation is needed only when residual high risk remains."
    run_dir, ledger, sidecar = _run(
        tmp_path,
        areas=[{"name": "Scope Area", "queries": ["scope q"]}],
        searches={"scope q": [S1_URL, S2_URL]},
        pages={S1_URL: _page(ART35, tag="artfive"), S2_URL: _page(ART36, tag="artsix")},
        extracts=[("impact assessment is required", [_claim(claim_a, ART35, "Scope Area")]),
                  ("Prior consultation with", [_claim(claim_b, ART36, "Scope Area")])],
        verifies=[(claim_a, lambda text: _verdict("supports", ART35) if f">>>{ART35}<<<" in text
                   else _verdict("refutes", ART36, scope=True)),
                  (claim_b, lambda text: _verdict("supports", ART36) if f">>>{ART36}<<<" in text
                   else _verdict("insufficient", ""))])

    cid_a, cid_b = _claim_id(ledger, "DPIA"), _claim_id(ledger, "Prior consultation")
    assert ledger.contradictions == ()
    assert sidecar["stats"]["n_contradictions_ledger"] == 0
    assert sidecar["stats"]["n_scope_refutes"] == 1
    [entry] = sidecar["scope_refutes"]
    assert (entry["claim_id"], entry["other_claim_id"]) == (cid_a, cid_b)
    assert entry["other_source_id"] == ledger.by_id[cid_b].evidence[0].source.source_id
    assert not [e for e in ledger.by_id[cid_a].evidence if e.verification.verdict is Verdict.REFUTES]
    assert {c["added_as"] for c in sidecar["cross_checks"] if c["claim_id"] == cid_a} == {"scope_refute"}


def test_r4_unflagged_refutes_still_becomes_a_contradiction(tmp_path):
    claim_a = "A DPIA is required before high-risk processing."
    claim_b = "Prior consultation is needed only when residual high risk remains."
    _, ledger, sidecar = _run(
        tmp_path,
        areas=[{"name": "Scope Area", "queries": ["scope q"]}],
        searches={"scope q": [S1_URL, S2_URL]},
        pages={S1_URL: _page(ART35, tag="artfive"), S2_URL: _page(ART36, tag="artsix")},
        extracts=[("impact assessment is required", [_claim(claim_a, ART35, "Scope Area")]),
                  ("Prior consultation with", [_claim(claim_b, ART36, "Scope Area")])],
        verifies=[(claim_a, lambda text: _verdict("supports", ART35) if f">>>{ART35}<<<" in text
                   else _verdict("refutes", ART36)),
                  (claim_b, lambda text: _verdict("supports", ART36) if f">>>{ART36}<<<" in text
                   else _verdict("insufficient", ""))])
    assert len(ledger.contradictions) == 1
    assert sidecar["scope_refutes"] == []


# --- R9: verify_run recomputes digests and checks Source-to-snapshot binding ----------------------

@pytest.fixture
def scope_run(tmp_path) -> Path:
    claim_a = "A DPIA is required before high-risk processing."
    claim_b = "Prior consultation is needed only when residual high risk remains."
    run_dir, _, _ = _run(
        tmp_path,
        areas=[{"name": "Scope Area", "queries": ["scope q"]}],
        searches={"scope q": [S1_URL, S2_URL]},
        pages={S1_URL: _page(ART35, tag="artfive"), S2_URL: _page(ART36, tag="artsix")},
        extracts=[("impact assessment is required", [_claim(claim_a, ART35, "Scope Area")]),
                  ("Prior consultation with", [_claim(claim_b, ART36, "Scope Area")])],
        verifies=[(claim_a, lambda text: _verdict("supports", ART35) if f">>>{ART35}<<<" in text
                   else _verdict("insufficient", "")),
                  (claim_b, lambda text: _verdict("supports", ART36) if f">>>{ART36}<<<" in text
                   else _verdict("insufficient", ""))])
    return run_dir


def test_verify_run_passes_an_untouched_run(scope_run):
    assert verify_run(scope_run) == []


def test_verify_run_catches_a_snapshot_edited_outside_every_span(scope_run):
    snapshot = next((scope_run / "snapshots").glob("*.txt"))
    snapshot.write_text(snapshot.read_text(encoding="utf-8") + " appended later", encoding="utf-8")
    problems = verify_run(scope_run)
    assert any("digest" in p for p in problems), problems


def test_verify_run_catches_a_source_bound_to_another_snapshot(scope_run):
    sidecar_path = scope_run / "sidecar.json"
    sidecar = json.loads(sidecar_path.read_text())
    a, b = list(sidecar["sources"])
    sidecar["sources"][a]["text_sha256"] = sidecar["sources"][b]["text_sha256"]
    sidecar_path.write_text(json.dumps(sidecar))
    problems = verify_run(scope_run)
    assert any("bound" in p for p in problems), problems


def test_verify_run_fails_without_a_sidecar(scope_run):
    (scope_run / "sidecar.json").unlink()
    assert any("sidecar" in p for p in verify_run(scope_run))
