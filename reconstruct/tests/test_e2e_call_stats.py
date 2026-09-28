"""D2: per-task failed-call counting. `stats.failed_calls_by_task` counts, per task (plan,
extract, verify, cross_verify, decoy, web_search), how many calls returned None or raised
LLMUnavailable/LLMRefused — so a run where calls silently vanished shows it in the sidecar
instead of just quietly having fewer claims than expected. Cross-cluster re-verification is
logged under its own "cross_verify" task label (same prompt/schema/payload as "verify" — only
the label differs), and a failed decoy generation is counted rather than silently dropped.
"""
from __future__ import annotations

from pathlib import Path

from reconstruct.llm import LLMUnavailable
from reconstruct.run import reconstruct
from residual.ledger import Ledger

from e2e_support import (
    TODAY, Page, ScriptedBackend, http_client, make_models, read_json, read_jsonl,
    script_default_decoys, search_result,
)

PADDING = " ".join(f"padtoken{i}" for i in range(80))


def _page(*paragraphs: str) -> Page:
    body = "<!doctype html><html><body>" + "".join(f"<p>{p}</p>" for p in paragraphs) + \
           f"<p>{PADDING}</p></body></html>"
    return Page(body=body)


# --- web_search failures are counted -------------------------------------------------------------

def test_failed_calls_by_task_counts_web_search_failures(tmp_path):
    out = tmp_path / "run"
    url = "https://good-search.example/notes"
    quote = "The coolant pump is inspected every ninety days as part of routine maintenance."

    planner = ScriptedBackend(role="planner", family="anthropic")
    planner.script("plan", "", {"areas": [{"name": "Area", "queries": ["good query", "bad query"]}]})
    planner.script_search("good query", search_result("good query", [(url, "t")], TODAY))
    planner.script_search("bad query", LLMUnavailable("simulated web_search failure"))

    extractor = ScriptedBackend(role="extractor", family="anthropic")
    extractor.script("extract", "coolant pump", {"claims": [
        {"assertion": "The coolant pump is inspected every ninety days.", "quote": quote,
         "area": "Area", "knowledge_type": "concept", "question": "domain"}]})

    verifier = ScriptedBackend(role="verifier", family="openai")
    verifier.script("verify", "", {"verdict": "supports", "supporting_quote": quote})
    script_default_decoys(extractor, verifier)

    models = make_models(planner=planner, extractor=extractor, verifier=verifier, out=out)
    run_dir = Path(reconstruct(domain="d", task="t", models=models, http=http_client({url: _page(quote)}),
                                out=out, today=TODAY, max_results=5))

    sidecar = read_json(run_dir / "sidecar.json")
    assert sidecar["complete"] is True, sidecar["incomplete_reasons"]
    assert sidecar["stats"]["failed_calls_by_task"]["web_search"] == 1


# --- extract failures are counted ------------------------------------------------------------------

def test_failed_calls_by_task_counts_extract_failures(tmp_path):
    out = tmp_path / "run"
    good_url = "https://good-extract.example/notes"
    bad_url = "https://bad-extract.example/notes"
    good_quote = "The coolant pump is inspected every ninety days as part of routine maintenance."
    bad_quote = "BADEXTRACT-MARKER some unrelated content that will fail to extract."

    planner = ScriptedBackend(role="planner", family="anthropic")
    planner.script("plan", "", {"areas": [{"name": "Area", "queries": ["q"]}]})
    planner.script_search("q", search_result("q", [(good_url, "t"), (bad_url, "t")], TODAY))

    extractor = ScriptedBackend(role="extractor", family="anthropic")
    extractor.script("extract", "coolant pump", {"claims": [
        {"assertion": "The coolant pump is inspected every ninety days.", "quote": good_quote,
         "area": "Area", "knowledge_type": "concept", "question": "domain"}]})
    extractor.script("extract", "BADEXTRACT-MARKER", LLMUnavailable("simulated extract failure"))

    verifier = ScriptedBackend(role="verifier", family="openai")
    verifier.script("verify", "", {"verdict": "supports", "supporting_quote": good_quote})
    script_default_decoys(extractor, verifier)

    pages = {good_url: _page(good_quote), bad_url: _page(bad_quote)}
    models = make_models(planner=planner, extractor=extractor, verifier=verifier, out=out)
    run_dir = Path(reconstruct(domain="d", task="t", models=models, http=http_client(pages),
                                out=out, today=TODAY, max_results=5))

    sidecar = read_json(run_dir / "sidecar.json")
    assert sidecar["complete"] is True, sidecar["incomplete_reasons"]
    assert sidecar["stats"]["failed_calls_by_task"]["extract"] == 1


# --- verify failures are counted -------------------------------------------------------------------

def test_failed_calls_by_task_counts_verify_failures(tmp_path):
    out = tmp_path / "run"
    url = "https://verify-fail.example/notes"
    quote = "The coolant pump is inspected every ninety days as part of routine maintenance."

    planner = ScriptedBackend(role="planner", family="anthropic")
    planner.script("plan", "", {"areas": [{"name": "Area", "queries": ["q"]}]})
    planner.script_search("q", search_result("q", [(url, "t")], TODAY))

    extractor = ScriptedBackend(role="extractor", family="anthropic")
    extractor.script("extract", "coolant pump", {"claims": [
        {"assertion": "The coolant pump is inspected every ninety days.", "quote": quote,
         "area": "Area", "knowledge_type": "concept", "question": "domain"}]})

    verifier = ScriptedBackend(role="verifier", family="openai")
    verifier.script("verify", "coolant pump", LLMUnavailable("simulated verify failure"))
    script_default_decoys(extractor, verifier)

    models = make_models(planner=planner, extractor=extractor, verifier=verifier, out=out)
    run_dir = Path(reconstruct(domain="d", task="t", models=models, http=http_client({url: _page(quote)}),
                                out=out, today=TODAY, max_results=5))

    sidecar = read_json(run_dir / "sidecar.json")
    assert sidecar["complete"] is True, sidecar["incomplete_reasons"]
    assert sidecar["stats"]["failed_calls_by_task"]["verify"] >= 1


# --- cross_verify: distinct task label, and its failures are counted separately from "verify" ------

PM_A = ("The pump receives a scheduled preventive maintenance visit every calendar month "
        "regardless of how many hours it has run.")
PM_B = ("Out in the field, technicians perform preventive maintenance on the pump on a fixed "
        "monthly schedule, never tied to operating hours.")
PLANT_URL = "https://plant-log.example/pm"
HANDBOOK_URL = "https://site-handbook.example/pm"


def _claim(assertion: str, quote: str, area: str) -> dict:
    return {"assertion": assertion, "quote": quote, "area": area,
            "knowledge_type": "concept", "question": "domain"}


def _supports(quote: str) -> dict:
    return {"verdict": "supports", "supporting_quote": quote, "adds_content": False,
            "subject_or_scope_differs": False, "quantifier_modality_or_connective_differs": False}


def test_cross_verify_uses_its_own_task_label_and_its_failures_are_counted_separately(tmp_path):
    out = tmp_path / "run"
    # Distinct, tag-prefixed filler per page (not the shared `_page`/PADDING helper): identical
    # padding on both pages would give them near-identical 5-word shingles and wrongly cluster
    # them together by containment, which defeats this test's two-independent-clusters premise.
    plant_filler = " ".join(f"plantpad{i}" for i in range(80))
    handbook_filler = " ".join(f"handbookpad{i}" for i in range(80))
    pages = {
        PLANT_URL: Page(body=f"<!doctype html><html><body><p>{PM_A}</p>"
                              f"<p>{plant_filler}</p></body></html>"),
        HANDBOOK_URL: Page(body=f"<!doctype html><html><body><p>{PM_B}</p>"
                                 f"<p>{handbook_filler}</p></body></html>"),
    }

    planner = ScriptedBackend(role="planner", family="anthropic")
    planner.script("plan", "", {"areas": [{"name": "Corroborate Area", "queries": ["pump pm schedule"]}]})
    planner.script_search("pump pm schedule", search_result(
        "pump pm schedule", [(PLANT_URL, "t"), (HANDBOOK_URL, "t")], TODAY))

    CLAIM_C = "Pump preventive maintenance follows a fixed monthly schedule."
    CLAIM_D = "The pump receives monthly preventive maintenance regardless of hours run."

    extractor = ScriptedBackend(role="extractor", family="anthropic")
    extractor.script("extract", "scheduled preventive maintenance visit",
                     {"claims": [_claim(CLAIM_C, PM_A, "Corroborate Area")]})
    extractor.script("extract", "technicians perform preventive maintenance",
                     {"claims": [_claim(CLAIM_D, PM_B, "Corroborate Area")]})

    verifier = ScriptedBackend(role="verifier", family="openai")
    verifier.script("verify", CLAIM_C, _supports(PM_A))
    verifier.script("verify", CLAIM_D, _supports(PM_B))
    # Every cross-cluster re-verification call fails (a distinct task, "cross_verify"): if the
    # implementation still used task "verify" for these, this catch-all would never be reached
    # and the run would instead hit NoScriptedResponse trying to match "verify".
    verifier.script("cross_verify", "", LLMUnavailable("simulated cross_verify failure"))
    script_default_decoys(extractor, verifier)

    models = make_models(planner=planner, extractor=extractor, verifier=verifier, out=out)
    run_dir = Path(reconstruct(domain="maintenance", task="t", models=models, http=http_client(pages),
                                out=out, today=TODAY, max_results=5))

    ledger = Ledger.from_json((run_dir / "ledger.json").read_text())
    sidecar = read_json(run_dir / "sidecar.json")
    assert sidecar["complete"] is True, sidecar["incomplete_reasons"]

    claim_c = next(c for c in ledger.claims if "fixed monthly schedule" in c.assertion)
    assert claim_c.corroboration == 1, "the failed cross-verify call must never add corroboration"

    assert sidecar["stats"]["failed_calls_by_task"]["cross_verify"] >= 1
    assert sidecar["stats"]["failed_calls_by_task"]["verify"] == 0, (
        "a cross-verify failure must not be miscounted as a plain verify failure")

    logged = read_jsonl(out / "calls.jsonl")
    verifier_tasks = {c["task"] for c in logged if c["role"] == "verifier"}
    assert "verify" in verifier_tasks
    assert "cross_verify" in verifier_tasks, (
        "the cross-cluster re-verification call must be logged under its own task label")


# --- decoy: a failed generation is counted, not silently dropped -----------------------------------

def test_decoy_failed_generation_is_counted(tmp_path):
    out = tmp_path / "run"
    url = "https://decoy-fail.example/notes"
    quote = "The coolant pump is inspected every ninety days as part of routine maintenance."

    planner = ScriptedBackend(role="planner", family="anthropic")
    planner.script("plan", "", {"areas": [{"name": "Area", "queries": ["q"]}]})
    planner.script_search("q", search_result("q", [(url, "t")], TODAY))

    extractor = ScriptedBackend(role="extractor", family="anthropic")
    extractor.script("extract", "coolant pump", {"claims": [
        {"assertion": "The coolant pump is inspected every ninety days.", "quote": quote,
         "area": "Area", "knowledge_type": "concept", "question": "domain"}]})
    extractor.script("decoy", "", LLMUnavailable("simulated decoy generation failure"))

    verifier = ScriptedBackend(role="verifier", family="openai")
    verifier.script("verify", "", {"verdict": "supports", "supporting_quote": quote})

    models = make_models(planner=planner, extractor=extractor, verifier=verifier, out=out)
    run_dir = Path(reconstruct(domain="d", task="t", models=models, http=http_client({url: _page(quote)}),
                                out=out, today=TODAY, max_results=5))

    sidecar = read_json(run_dir / "sidecar.json")
    assert sidecar["complete"] is True, sidecar["incomplete_reasons"]
    assert sidecar["decoys"] == [], "a decoy that failed to generate must never reach the sidecar decoys list"
    assert sidecar["stats"]["decoy_by_type"]["number"]["failed"] == 1
    assert sidecar["stats"]["failed_calls_by_task"]["decoy"] == 1


# --- plan: a failure is counted even though the run then aborts (planner failure is fatal) ---------

def test_failed_calls_by_task_counts_plan_failures_before_the_run_aborts(tmp_path):
    out = tmp_path / "run"
    planner = ScriptedBackend(role="planner", family="anthropic")
    planner.script("plan", "", LLMUnavailable("simulated plan failure"))

    models = make_models(planner=planner, out=out)
    run_dir = Path(reconstruct(domain="d", task="t", models=models, http=http_client({}),
                                out=out, today=TODAY, max_results=5))

    sidecar = read_json(run_dir / "sidecar.json")
    assert sidecar["complete"] is False
    assert sidecar["stats"]["failed_calls_by_task"]["plan"] == 1
