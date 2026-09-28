"""Items 9 and 10: the UNKNOWN placeholder mechanism, and an area whose searches all fail
("unsought", A3) — never confused with UNKNOWN, and never silently dropped from the report.
"""
from __future__ import annotations

from pathlib import Path

from reconstruct.llm import LLMUnavailable
from reconstruct.run import reconstruct
from residual.ledger import Ledger
from residual.vocab import EpistemicLabel

from e2e_support import (
    TODAY, ScriptedBackend, http_client, make_models, page_from_fixture, read_json,
    script_default_decoys, search_result,
)

NORM_TEMPLATE = "What counts as acceptable or sufficient work in {area}?"

TORQUE_URL = "https://fastener-torque.example/handbook"
TORQUE_CLAIMS = [
    ("Torque is the rotational force applied to a fastener, expressed as the product of applied force and lever arm length.",
     "concept", "domain"),
    ("A fastener is re-torqued to specification whenever the measured preload falls below ninety percent of its target value.",
     "decision", "performance"),
    ("A dull matte ring around the bolt head signals that the coating has worn through and the joint needs inspection.",
     "cue", "performance"),
    ("Torque is checked by applying a calibrated wrench and confirming the reading matches the specification sheet within five percent.",
     "check", "performance"),
    ("A stripped thread typically shows as a wrench that keeps turning without any increase in resistance.",
     "failure_mode", "performance"),
    ("Fasteners are torqued to a specified value so that the clamped joint resists vibration without yielding the bolt material.",
     "rationale", "performance"),
]


def test_unknown_placeholder_written_only_for_the_uncovered_probe(tmp_path):
    out = tmp_path / "run"
    pages = {TORQUE_URL: page_from_fixture("fastener_torque.html")}

    planner = ScriptedBackend(role="planner", family="anthropic")
    planner.script("plan", "", {"areas": [{"name": "Fastener Torque", "queries": ["fastener torque specification"]}]})
    planner.script_search("fastener torque", search_result(
        "fastener torque specification", [(TORQUE_URL, "t")], TODAY))

    extractor = ScriptedBackend(role="extractor", family="anthropic")
    extractor.script("extract", "", {"claims": [
        {"assertion": quote, "quote": quote, "area": "Fastener Torque",
         "knowledge_type": kt, "question": q} for quote, kt, q in TORQUE_CLAIMS
    ]})

    # Full exact quote text as the match, not a short prefix: the fixture is padded with >280
    # char filler between quotes specifically so a verify call's +/-300 char context stays
    # within one quote's own neighbourhood, but a short prefix could still coincide with the
    # tail of an adjacent context — the full quote text cannot.
    verifier = ScriptedBackend(role="verifier", family="openai")
    for quote, _, _ in TORQUE_CLAIMS:
        verifier.script("verify", quote, {"verdict": "supports", "supporting_quote": quote})
    script_default_decoys(extractor, verifier)

    contradiction = ScriptedBackend(role="contradiction", family="openai")
    models = make_models(planner=planner, extractor=extractor, verifier=verifier,
                          contradiction=contradiction, out=out)
    run_dir = Path(reconstruct(domain="maintenance", task="t", models=models, http=http_client(pages),
                                out=out, today=TODAY, max_results=5))

    ledger = Ledger.from_json((run_dir / "ledger.json").read_text())
    expected_norm = NORM_TEMPLATE.format(area="Fastener Torque")
    placeholders = [c for c in ledger.claims if c.assertion == expected_norm]
    assert len(placeholders) == 1, f"expected exactly one NORM placeholder, found {len(placeholders)}"
    placeholder = placeholders[0]
    assert placeholder.label == EpistemicLabel.UNKNOWN
    area_id = ledger.area_of(placeholder.claim_id)
    assert area_id is not None
    assert ledger.by_id[placeholder.claim_id] is placeholder
    assert any(a.area_id == area_id and a.name == "Fastener Torque" for a in ledger.areas)

    for c in ledger.claims:
        if c.claim_id != placeholder.claim_id:
            assert c.label != EpistemicLabel.UNKNOWN, f"non-placeholder claim {c.assertion!r} is UNKNOWN"


def test_area_whose_searches_all_fail_is_unsought_not_unknown(tmp_path):
    out = tmp_path / "run"
    working_url = "https://workingarea.example/notes"
    pages = {working_url: page_from_fixture("working_area.html")}

    planner = ScriptedBackend(role="planner", family="anthropic")
    planner.script("plan", "", {"areas": [
        {"name": "Working Area", "queries": ["gasket replacement"]},
        {"name": "Failing Area", "queries": ["unreachable topic"]},
    ]})
    planner.script_search("gasket replacement", search_result(
        "gasket replacement", [(working_url, "t")], TODAY))
    planner.script_search("unreachable topic", LLMUnavailable("search backend unavailable"))

    extractor = ScriptedBackend(role="extractor", family="anthropic")
    extractor.script("extract", "", {"claims": [
        {"assertion": "A gasket is replaced whenever it shows visible cracking.",
         "quote": "A gasket is replaced whenever it shows visible cracking along its outer sealing edge.",
         "area": "Working Area", "knowledge_type": "concept", "question": "domain"}]})

    verifier = ScriptedBackend(role="verifier", family="openai")
    verifier.script("verify", "", {"verdict": "supports",
                                     "supporting_quote": "A gasket is replaced whenever it shows visible cracking along its outer sealing edge."})
    script_default_decoys(extractor, verifier)

    contradiction = ScriptedBackend(role="contradiction", family="openai")
    models = make_models(planner=planner, extractor=extractor, verifier=verifier,
                          contradiction=contradiction, out=out)
    run_dir = Path(reconstruct(domain="maintenance", task="t", models=models, http=http_client(pages),
                                out=out, today=TODAY, max_results=5))

    sidecar = read_json(run_dir / "sidecar.json")
    assert sidecar["complete"] is False
    assert sidecar["incomplete_reasons"], "an all-failed area must record a reason"

    ledger = Ledger.from_json((run_dir / "ledger.json").read_text())
    assert not any(a.name == "Failing Area" for a in ledger.areas), (
        "an area whose searches all failed must not appear in ledger.areas")
    assert not any("Failing Area" in c.assertion for c in ledger.claims), (
        "no UNKNOWN placeholder must be written for an unsought area")
