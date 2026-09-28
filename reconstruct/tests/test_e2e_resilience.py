"""Items 14 and 15: a mid-run BudgetExceeded still leaves a usable (incomplete) run dir, and
non-HTML / blocklisted URLs are recorded as failures rather than becoming Sources.
"""
from __future__ import annotations

from pathlib import Path

from reconstruct.run import reconstruct
from residual.ledger import Ledger

from e2e_support import (
    TODAY, Page, ScriptedBackend, SharedBudget, http_client, make_models, page_from_fixture,
    read_json, script_default_decoys, search_result,
)

QUOTE_A = ("Displacement is defined as the vector change in an object's position measured from a "
           "fixed reference point, which differs from distance because it captures direction as "
           "well as magnitude.")


# --- item 14: BudgetExceeded mid-run --------------------------------------------------------------

def test_budget_exceeded_mid_run_still_writes_an_incomplete_run_dir(tmp_path):
    out = tmp_path / "run"
    url_a = "https://kinematics-a.example/notes"
    url_b = "https://span-check.example/page"
    quote_b = ("Thermal conductivity measures how readily a material conducts heat energy through "
               "it under a temperature gradient.")
    pages = {url_a: page_from_fixture("happy_kinematics_a.html"),
              url_b: page_from_fixture("insufficient_source.html")}

    budget = SharedBudget(max_calls=3)  # plan + 1 search succeed; the run must exhaust budget soon after

    planner = ScriptedBackend(role="planner", family="anthropic", budget=budget)
    planner.script("plan", "", {"areas": [
        {"name": "Kinematics", "queries": ["kinematics reference"]},
        {"name": "Heat", "queries": ["heat reference"]},
    ]})
    planner.script_search("kinematics", search_result("kinematics reference", [(url_a, "t")], TODAY))
    planner.script_search("heat", search_result("heat reference", [(url_b, "t")], TODAY))

    extractor = ScriptedBackend(role="extractor", family="anthropic", budget=budget)
    extractor.script("extract", "vector change", {"claims": [
        {"assertion": "Displacement is a vector change in position.", "quote": QUOTE_A,
         "area": "Kinematics", "knowledge_type": "concept", "question": "domain"}]})
    extractor.script("extract", "Thermal conductivity", {"claims": [
        {"assertion": "Thermal conductivity measures heat conduction.", "quote": quote_b,
         "area": "Heat", "knowledge_type": "concept", "question": "domain"}]})

    verifier = ScriptedBackend(role="verifier", family="openai", budget=budget)
    verifier.script("verify", "", {"verdict": "supports", "supporting_quote": QUOTE_A})
    script_default_decoys(extractor, verifier)

    contradiction = ScriptedBackend(role="contradiction", family="openai", budget=budget)

    models = make_models(planner=planner, extractor=extractor, verifier=verifier,
                          contradiction=contradiction, out=out)

    run_dir = Path(reconstruct(domain="physics", task="t", models=models, http=http_client(pages),
                                out=out, today=TODAY, max_results=5))

    assert run_dir.exists()
    assert (run_dir / "ledger.json").exists()
    assert (run_dir / "sidecar.json").exists()

    ledger = Ledger.from_json((run_dir / "ledger.json").read_text())
    assert ledger.to_json()  # still a structurally valid ledger

    sidecar = read_json(run_dir / "sidecar.json")
    assert sidecar["complete"] is False
    assert any("budget" in r.lower() for r in sidecar["incomplete_reasons"]), (
        f"expected a budget-related incomplete reason, got {sidecar['incomplete_reasons']}")


# --- item 15: non-HTML and blocklisted URLs never become Sources ----------------------------------

def test_non_html_and_blocklisted_urls_are_fetch_failures_not_sources(tmp_path):
    out = tmp_path / "run"
    good_url = "https://goodpage.example/notes"
    pdf_url = "https://pdf-host.example/manual.pdf"
    blocked_url = "https://blocked.example/held-out"

    pages = {
        good_url: Page(body="<!doctype html><html><body><p>"
                              "The rated load of the sling must never exceed its certified working limit."
                              "</p></body></html>"),
        pdf_url: Page(body=b"%PDF-1.4 fake binary content", content_type="application/pdf"),
        blocked_url: Page(body="<!doctype html><html><body><p>This must never be fetched or used.</p></body></html>"),
    }

    planner = ScriptedBackend(role="planner", family="anthropic")
    planner.script("plan", "", {"areas": [{"name": "Rigging", "queries": ["sling rated load"]}]})
    planner.script_search("sling rated load", search_result(
        "sling rated load", [(good_url, "t"), (pdf_url, "t"), (blocked_url, "t")], TODAY))

    extractor = ScriptedBackend(role="extractor", family="anthropic")
    extractor.script("extract", "rated load", {"claims": [
        {"assertion": "A sling's rated load must never be exceeded.",
         "quote": "The rated load of the sling must never exceed its certified working limit.",
         "area": "Rigging", "knowledge_type": "concept", "question": "domain"}]})

    verifier = ScriptedBackend(role="verifier", family="openai")
    verifier.script("verify", "", {"verdict": "supports",
                                     "supporting_quote": "The rated load of the sling must never exceed its certified working limit."})
    script_default_decoys(extractor, verifier)

    contradiction = ScriptedBackend(role="contradiction", family="openai")
    models = make_models(planner=planner, extractor=extractor, verifier=verifier,
                          contradiction=contradiction, out=out)

    run_dir = Path(reconstruct(domain="rigging", task="t", models=models, http=http_client(pages),
                                out=out, today=TODAY, max_results=5, blocklist=["blocked.example"]))

    ledger = Ledger.from_json((run_dir / "ledger.json").read_text())
    source_ids = {ev.source.identifier for c in ledger.claims for ev in c.evidence}
    assert pdf_url not in source_ids
    assert blocked_url not in source_ids
    assert good_url in source_ids

    sidecar = read_json(run_dir / "sidecar.json")
    failure_urls = {f["url"]: f["reason"] for f in sidecar["fetch_failures"]}
    assert pdf_url in failure_urls, sidecar["fetch_failures"]
    assert "pdf" in failure_urls[pdf_url].lower() or "content type" in failure_urls[pdf_url].lower()
    assert blocked_url in failure_urls, sidecar["fetch_failures"]
    assert "block" in failure_urls[blocked_url].lower()
