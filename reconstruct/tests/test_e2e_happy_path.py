"""Item 1 (happy path) and item 16 (provenance invariants), against a single small run: 2 areas,
3 fetched pages, one located quote that a different-family verifier supports.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from reconstruct.run import reconstruct
from residual.ledger import Ledger
from residual.vocab import EpistemicLabel

from e2e_support import (
    TODAY, ScriptedBackend, area_by_name, find_claim, http_client, make_models,
    page_from_fixture, resolve_selector_exact, script_default_decoys, search_result,
)

QUOTE_A = ("Displacement is defined as the vector change in an object's position measured from a "
           "fixed reference point, which differs from distance because it captures direction as "
           "well as magnitude.")

URL_A = "https://kinematics-a.example/notes"
URL_B = "https://kinematics-b.example/examples"
URL_C = "https://thermo-c.example/overview"


@pytest.fixture(scope="module")
def run_dir(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("happy")
    out = tmp_path / "run"

    pages = {
        URL_A: page_from_fixture("happy_kinematics_a.html"),
        URL_B: page_from_fixture("happy_kinematics_b.html"),
        URL_C: page_from_fixture("happy_thermo_c.html"),
    }

    planner = ScriptedBackend(role="planner", family="anthropic")
    planner.script("plan", "", {
        "areas": [
            {"name": "Kinematics", "queries": ["kinematics reference"]},
            {"name": "Thermodynamics", "queries": ["thermodynamics reference"]},
        ]
    })
    planner.script_search("kinematics", search_result(
        "kinematics reference", [(URL_A, "Kinematics notes"), (URL_B, "Kinematics examples")], TODAY))
    planner.script_search("thermodynamics", search_result(
        "thermodynamics reference", [(URL_C, "Thermodynamics overview")], TODAY))

    extractor = ScriptedBackend(role="extractor", family="anthropic")
    extractor.script("extract", "vector change", {
        "claims": [{
            "assertion": "Displacement is the vector change in an object's position from a reference point.",
            "quote": QUOTE_A, "area": "Kinematics", "knowledge_type": "concept", "question": "domain",
        }]
    })
    extractor.script("extract", "worked problems", {"claims": []})
    extractor.script("extract", "external references", {"claims": []})

    verifier = ScriptedBackend(role="verifier", family="openai")
    verifier.script("verify", "vector change", {"verdict": "supports", "supporting_quote": QUOTE_A})
    script_default_decoys(extractor, verifier)

    contradiction = ScriptedBackend(role="contradiction", family="openai")

    models = make_models(planner=planner, extractor=extractor, verifier=verifier,
                          contradiction=contradiction, out=out)

    result_dir = reconstruct(domain="physics", task="kinematics problem solving", models=models,
                              http=http_client(pages), out=out, today=TODAY, max_results=5)

    yield Path(result_dir), extractor, verifier, planner


# --- item 1: happy path -----------------------------------------------------------------------

def test_run_dir_has_the_documented_artefacts(run_dir):
    rd, *_ = run_dir
    for name in ("ledger.json", "sidecar.json", "calls.jsonl", "report.md", "areas.json"):
        assert (rd / name).exists(), f"missing run artefact {name}"
    assert (rd / "snapshots").is_dir()
    assert any((rd / "snapshots").iterdir()), "no snapshots were written"


def test_ledger_round_trips_and_has_both_areas(run_dir):
    rd, *_ = run_dir
    ledger = Ledger.from_json((rd / "ledger.json").read_text())
    assert ledger.to_json()  # re-serialises without raising
    area_by_name(ledger, "Kinematics")
    area_by_name(ledger, "Thermodynamics")


def test_supported_claim_is_literature_supported_with_a_located_quote(run_dir):
    rd, *_ = run_dir
    ledger = Ledger.from_json((rd / "ledger.json").read_text())
    claim = find_claim(ledger, "Displacement is the vector change")

    assert claim.label == EpistemicLabel.LITERATURE_SUPPORTED
    assert len(claim.evidence) >= 1
    ev = claim.evidence[0]
    assert ev.verification.verdict == "supports"
    assert ev.selector.exact and ev.selector.exact.strip()
    assert ev.selector.exact in QUOTE_A or QUOTE_A in ev.selector.exact

    sliced = resolve_selector_exact(rd, ev.selector)
    assert sliced == ev.selector.exact, "Selector.exact is not a slice of its own snapshot text"


def test_verify_run_accepts_the_fixture_run(run_dir):
    rd, *_ = run_dir
    proc = subprocess.run([sys.executable, "-m", "reconstruct.verify_run", str(rd)],
                           capture_output=True, text=True)
    assert proc.returncode == 0, f"verify_run failed:\nstdout={proc.stdout}\nstderr={proc.stderr}"


def test_calls_jsonl_is_well_formed(run_dir):
    rd, *_ = run_dir
    path = rd / "calls.jsonl"
    assert path.exists()
    lines = [l for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert lines, "calls.jsonl has no entries"
    for line in lines:
        record = json.loads(line)
        assert "task" in record


# --- item 16: provenance invariants -------------------------------------------------------------

def test_every_source_identifier_is_a_fetched_url(run_dir):
    rd, extractor, verifier, planner = run_dir
    ledger = Ledger.from_json((rd / "ledger.json").read_text())
    fetched_urls = {URL_A, URL_B, URL_C}
    for claim in ledger.claims:
        for ev in claim.evidence:
            assert ev.source.identifier in fetched_urls, (
                f"Source.identifier {ev.source.identifier!r} is not one of the pages this run "
                f"actually fetched — provenance must point at a fetched page, never a bare URL")


def test_every_supported_claim_has_a_verifier_of_a_different_family_than_the_extractor(run_dir):
    rd, extractor, verifier, planner = run_dir
    ledger = Ledger.from_json((rd / "ledger.json").read_text())
    extractor_family = extractor.family
    for claim in ledger.claims:
        if not claim.supporting:
            continue
        families = {e.verification.verifier.family for e in claim.supporting if e.verification.verifier}
        assert families, f"{claim.assertion!r} is supported but its evidence names no verifier"
        assert all(f != extractor_family for f in families), (
            f"{claim.assertion!r} is supported by a verifier sharing the extractor's family "
            f"{extractor_family!r}")
