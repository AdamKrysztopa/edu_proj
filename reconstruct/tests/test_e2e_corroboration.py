"""Items 5 and 6: duplicate vs. genuinely independent corroboration.

Item 5 has two sub-cases that must both merge into corroboration == 1: a syndicated passage
repeated on two different domains, and two pages on one registrable domain. Item 6 is the
control — two different domains with different wording, corroborating a claim independently.
"""
from __future__ import annotations

from pathlib import Path

from reconstruct.run import reconstruct
from residual.ledger import Ledger

from e2e_support import (
    TODAY, ScriptedBackend, find_claim, http_client, make_models, page_from_fixture, read_json,
    script_default_decoys, search_result,
)

SYNDICATED_QUOTE = ("Operators must isolate the coupling and confirm zero residual pressure before "
                     "removing the inspection hatch cover on this class of vessel.")
SAMEDOMAIN_QUOTE_1 = "The scheduler retries a failed job with exponential backoff before giving up and marking it as dead."
SAMEDOMAIN_QUOTE_2 = ("When a job fails, the scheduler waits progressively longer between each retry attempt, "
                       "using an exponential backoff schedule, until it eventually gives up.")
INDEPENDENT_QUOTE_1 = "The kernel scheduler always services a pinned interrupt thread ahead of any other runnable thread on that core."
INDEPENDENT_QUOTE_2 = "On a given core, a thread pinned to an interrupt is always run before other work waiting on that same core."

ORIGIN_URL = "https://origin-news.example/story"
MIRROR_URL = "https://mirror-blog.example/repost"
INTRO_URL = "https://docs.example.org/guide/intro"
DETAILS_URL = "https://docs.example.org/guide/details"
SITE_A_URL = "https://site-a.example/notes"
SITE_B_URL = "https://site-b.example/handbook"


def _run(tmp_path, *, area, pages, plan_query, extract_scripts):
    out = tmp_path / "run"
    planner = ScriptedBackend(role="planner", family="anthropic")
    planner.script("plan", "", {"areas": [{"name": area, "queries": [plan_query]}]})
    planner.script_search(plan_query, search_result(
        plan_query, [(u, "t") for u in pages], TODAY))

    extractor = ScriptedBackend(role="extractor", family="anthropic")
    for match, response in extract_scripts:
        extractor.script("extract", match, response)

    verifier = ScriptedBackend(role="verifier", family="openai")
    for match, quote in [(m, q) for m, q in _all_quotes(extract_scripts)]:
        verifier.script("verify", match, {"verdict": "supports", "supporting_quote": quote})
    script_default_decoys(extractor, verifier)

    contradiction = ScriptedBackend(role="contradiction", family="openai")
    models = make_models(planner=planner, extractor=extractor, verifier=verifier,
                          contradiction=contradiction, out=out)
    run_dir = Path(reconstruct(domain="ops", task="t", models=models, http=http_client(pages),
                                out=out, today=TODAY, max_results=5))
    return run_dir


def _all_quotes(extract_scripts):
    for match, response in extract_scripts:
        for claim in response["claims"]:
            yield claim["quote"][:30], claim["quote"]


def test_syndicated_passage_on_two_domains_merges_to_corroboration_one(tmp_path):
    pages = {ORIGIN_URL: page_from_fixture("syndicated_passage.html"),
              MIRROR_URL: page_from_fixture("syndicated_passage.html")}
    claim_body = {"claims": [{"assertion": "The coupling must be isolated and depressurised before the hatch is opened.",
                               "quote": SYNDICATED_QUOTE, "area": "Safety",
                               "knowledge_type": "procedure_step", "question": "performance"}]}
    run_dir = _run(tmp_path, area="Safety", pages=pages, plan_query="isolation procedure",
                    extract_scripts=[("isolate the coupling", claim_body)])

    ledger = Ledger.from_json((run_dir / "ledger.json").read_text())
    claim = find_claim(ledger, "coupling must be isolated")
    assert len(claim.evidence) == 2
    assert claim.corroboration == 1

    sidecar = read_json(run_dir / "sidecar.json")
    keys = {s["independence_key"] for s in sidecar["sources"].values()
            if s["final_url"] in (ORIGIN_URL, MIRROR_URL)}
    assert len(keys) == 1, f"syndicated sources should share one independence_key, got {keys}"


def test_two_pages_on_one_domain_merge_to_corroboration_one(tmp_path):
    pages = {INTRO_URL: page_from_fixture("samedomain_intro.html"),
              DETAILS_URL: page_from_fixture("samedomain_details.html")}
    body = {"claims": [{"assertion": "The scheduler retries a failed job with exponential backoff.",
                         "quote": SAMEDOMAIN_QUOTE_1, "area": "Scheduling",
                         "knowledge_type": "procedure_step", "question": "performance"}]}
    body2 = {"claims": [{"assertion": "The scheduler retries a failed job with exponential backoff.",
                          "quote": SAMEDOMAIN_QUOTE_2, "area": "Scheduling",
                          "knowledge_type": "procedure_step", "question": "performance"}]}
    run_dir = _run(tmp_path, area="Scheduling", pages=pages, plan_query="job retry scheduling",
                    extract_scripts=[("retries a failed job with exponential", body),
                                      ("waits progressively longer", body2)])

    ledger = Ledger.from_json((run_dir / "ledger.json").read_text())
    claim = find_claim(ledger, "retries a failed job with exponential backoff")
    assert len(claim.evidence) == 2
    assert claim.corroboration == 1

    sidecar = read_json(run_dir / "sidecar.json")
    keys = {s["independence_key"] for s in sidecar["sources"].values()
            if s["final_url"] in (INTRO_URL, DETAILS_URL)}
    assert len(keys) == 1, f"same-domain sources should share one independence_key, got {keys}"


def test_two_different_domains_with_different_wording_are_independent(tmp_path):
    pages = {SITE_A_URL: page_from_fixture("independent_a.html"),
              SITE_B_URL: page_from_fixture("independent_b.html")}
    body_a = {"claims": [{"assertion": "A pinned interrupt thread is always serviced ahead of other runnable threads on its core.",
                           "quote": INDEPENDENT_QUOTE_1, "area": "Scheduling",
                           "knowledge_type": "concept", "question": "domain"}]}
    body_b = {"claims": [{"assertion": "A pinned interrupt thread is always serviced ahead of other runnable threads on its core.",
                           "quote": INDEPENDENT_QUOTE_2, "area": "Scheduling",
                           "knowledge_type": "concept", "question": "domain"}]}
    run_dir = _run(tmp_path, area="Scheduling", pages=pages, plan_query="interrupt scheduling priority",
                    extract_scripts=[("always services a pinned interrupt", body_a),
                                      ("always run before other work", body_b)])

    ledger = Ledger.from_json((run_dir / "ledger.json").read_text())
    claim = find_claim(ledger, "always serviced ahead of other runnable threads")
    assert len(claim.evidence) == 2
    assert claim.corroboration == 2

    sidecar = read_json(run_dir / "sidecar.json")
    keys = {s["independence_key"] for s in sidecar["sources"].values()
            if s["final_url"] in (SITE_A_URL, SITE_B_URL)}
    assert len(keys) == 2, f"genuinely independent sources should not share an independence_key, got {keys}"
