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

    padding = " ".join(f"riggingpad{i}" for i in range(80))  # clears fetch()'s 500-char near-empty floor
    pages = {
        good_url: Page(body="<!doctype html><html><body><p>"
                              "The rated load of the sling must never exceed its certified working limit."
                              f"</p><p>{padding}</p></body></html>"),
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


# --- defect 13: a failing URL cited by more than one search is fetched, and recorded, once --------

def test_a_repeatedly_cited_failing_url_is_recorded_as_one_fetch_failure(tmp_path):
    out = tmp_path / "run"
    good_url = "https://goodpage2.example/notes"
    dead_url = "https://dead-host.example/manual.pdf"  # cited by both areas below

    padding = " ".join(f"gearboxpad{i}" for i in range(80))
    pages = {
        good_url: Page(body="<!doctype html><html><body><p>"
                              "The gearbox oil must be changed every two thousand operating hours."
                              f"</p><p>{padding}</p></body></html>"),
        dead_url: Page(body=b"%PDF-1.4 fake binary content", content_type="application/pdf"),
    }

    planner = ScriptedBackend(role="planner", family="anthropic")
    planner.script("plan", "", {"areas": [
        {"name": "Gearbox", "queries": ["gearbox oil change interval"]},
        {"name": "Manuals", "queries": ["gearbox service manual"]},
    ]})
    planner.script_search("gearbox oil change interval", search_result(
        "gearbox oil change interval", [(good_url, "t"), (dead_url, "t")], TODAY))
    planner.script_search("gearbox service manual", search_result(
        "gearbox service manual", [(dead_url, "t")], TODAY))

    extractor = ScriptedBackend(role="extractor", family="anthropic")
    extractor.script("extract", "gearbox oil", {"claims": [
        {"assertion": "Gearbox oil is changed every two thousand operating hours.",
         "quote": "The gearbox oil must be changed every two thousand operating hours.",
         "area": "Gearbox", "knowledge_type": "concept", "question": "domain"}]})

    verifier = ScriptedBackend(role="verifier", family="openai")
    verifier.script("verify", "", {"verdict": "supports",
                                     "supporting_quote": "The gearbox oil must be changed every two thousand operating hours."})
    script_default_decoys(extractor, verifier)

    contradiction = ScriptedBackend(role="contradiction", family="openai")
    models = make_models(planner=planner, extractor=extractor, verifier=verifier,
                          contradiction=contradiction, out=out)

    run_dir = Path(reconstruct(domain="machinery", task="t", models=models, http=http_client(pages),
                                out=out, today=TODAY, max_results=5))

    sidecar = read_json(run_dir / "sidecar.json")
    dead_failures = [f for f in sidecar["fetch_failures"] if f["url"] == dead_url]
    assert len(dead_failures) == 1, (
        f"a URL cited by two searches must be fetched (and recorded as failed) once, not once per "
        f"citing search: {sidecar['fetch_failures']}")


# --- D3: an unexpected exception from one document must not abort the whole fetch phase -----------

def test_one_bad_document_does_not_abort_the_fetch_phase(tmp_path, monkeypatch):
    from reconstruct.web import SnapshotStore

    out = tmp_path / "run"
    good_url = "https://good-doc.example/notes"
    bad_url = "https://bad-doc.example/notes"
    good_quote = "Bearing lubrication must be checked every five hundred operating hours."
    bad_marker = "BADDOC-MARKER-TRIGGERS-AN-UNEXPECTED-CRASH"
    padding = " ".join(f"padtoken{i}" for i in range(80))
    pages = {
        good_url: Page(body=f"<!doctype html><html><body><p>{good_quote}</p><p>{padding}</p>"
                              "</body></html>"),
        bad_url: Page(body=f"<!doctype html><html><body><p>{bad_marker} some unrelated text here.</p>"
                            f"<p>{padding}</p></body></html>"),
    }

    original_write_text = SnapshotStore.write_text

    def flaky_write_text(self, text):
        if bad_marker in text:
            raise ValueError("simulated unexpected extraction crash")
        return original_write_text(self, text)

    monkeypatch.setattr(SnapshotStore, "write_text", flaky_write_text)

    planner = ScriptedBackend(role="planner", family="anthropic")
    planner.script("plan", "", {"areas": [{"name": "Bearings", "queries": ["bearing lubrication interval"]}]})
    planner.script_search("bearing lubrication interval", search_result(
        "bearing lubrication interval", [(good_url, "t"), (bad_url, "t")], TODAY))

    extractor = ScriptedBackend(role="extractor", family="anthropic")
    extractor.script("extract", "Bearing lubrication", {"claims": [
        {"assertion": "Bearing lubrication is checked every five hundred operating hours.",
         "quote": good_quote, "area": "Bearings", "knowledge_type": "concept", "question": "domain"}]})

    verifier = ScriptedBackend(role="verifier", family="openai")
    verifier.script("verify", "", {"verdict": "supports", "supporting_quote": good_quote})
    script_default_decoys(extractor, verifier)

    contradiction = ScriptedBackend(role="contradiction", family="openai")
    models = make_models(planner=planner, extractor=extractor, verifier=verifier,
                          contradiction=contradiction, out=out)

    run_dir = Path(reconstruct(domain="machinery", task="t", models=models, http=http_client(pages),
                                out=out, today=TODAY, max_results=5))

    sidecar = read_json(run_dir / "sidecar.json")
    assert sidecar["complete"] is True, sidecar["incomplete_reasons"]
    failure_urls = {f["url"]: f["reason"] for f in sidecar["fetch_failures"]}
    assert bad_url in failure_urls, sidecar["fetch_failures"]
    assert failure_urls[bad_url].startswith("fetch error:"), failure_urls[bad_url]

    ledger = Ledger.from_json((run_dir / "ledger.json").read_text())
    assert any("Bearing lubrication" in c.assertion for c in ledger.claims), (
        "the good document's claim must still make it through despite the other document's crash")


# --- a curated PDF becomes a verified claim end to end (E-LIVE v1 PDF-rejection regression) -------

def test_pdf_source_yields_a_located_verified_claim(tmp_path):
    from test_web import make_pdf

    out = tmp_path / "run"
    url = "https://pdf-manual.example/guide.pdf"
    quote = ("Bearing lubrication must be checked every five hundred operating hours per the "
             "maintenance manual issued for this class of gearbox.")
    padding = "Padding text so the extracted document clears the near-empty page floor. " * 10
    pages = {url: Page(body=make_pdf([quote, padding]), content_type="application/pdf")}

    planner = ScriptedBackend(role="planner", family="anthropic")
    planner.script("plan", "", {"areas": [{"name": "Bearings", "queries": ["bearing lubrication"]}]})
    planner.script_search("bearing lubrication",
                          search_result("bearing lubrication", [(url, "t")], TODAY))
    extractor = ScriptedBackend(role="extractor", family="anthropic")
    extractor.script("extract", "Bearing lubrication", {"claims": [
        {"assertion": "Bearing lubrication is checked every five hundred operating hours.",
         "quote": quote, "area": "Bearings", "knowledge_type": "concept", "question": "domain"}]})
    verifier = ScriptedBackend(role="verifier", family="openai")
    verifier.script("verify", "", {"verdict": "supports", "supporting_quote": quote})
    script_default_decoys(extractor, verifier)
    models = make_models(planner=planner, extractor=extractor, verifier=verifier,
                         contradiction=ScriptedBackend(role="contradiction", family="openai"),
                         out=out)

    run_dir = Path(reconstruct(domain="machinery", task="t", models=models,
                               http=http_client(pages), out=out, today=TODAY, max_results=5))

    sidecar = read_json(run_dir / "sidecar.json")
    assert sidecar["complete"] is True
    assert sidecar["fetch_failures"] == []
    ledger = Ledger.from_json((run_dir / "ledger.json").read_text())
    claim = next(c for c in ledger.claims if c.assertion.startswith("Bearing lubrication"))
    assert [e.verification.verdict for e in claim.evidence] == ["supports"]
    assert claim.evidence[0].selector.exact == quote
