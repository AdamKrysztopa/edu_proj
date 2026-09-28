"""Item 12: decoys (A6). Mutated claims paired with a real span are put to the verifier to
measure a false-accept rate; they must never leak into the ledger, only the sidecar.
"""
from __future__ import annotations

from pathlib import Path

from reconstruct.run import reconstruct
from residual.ledger import Ledger

from e2e_support import TODAY, ScriptedBackend, http_client, make_models, page_from_fixture, read_json, search_result

URL = "https://decoy-source.example/facts"

QUOTES = [
    "The reservoir tank holds two hundred litres of coolant when filled to its rated capacity.",
    "The drive belt is replaced every eighteen months as part of scheduled maintenance.",
    "The control panel indicator turns amber when the filter is due for replacement soon.",
    "The backup generator starts automatically within ten seconds of a mains power interruption.",
    "The access door is fitted with an interlock switch that halts the conveyor when opened.",
]


def test_decoys_never_appear_in_the_ledger_and_false_accept_rate_matches_the_sidecar(tmp_path):
    out = tmp_path / "run"
    pages = {URL: page_from_fixture("decoy_source.html")}

    planner = ScriptedBackend(role="planner", family="anthropic")
    planner.script("plan", "", {"areas": [{"name": "Facilities", "queries": ["facilities equipment facts"]}]})
    planner.script_search("facilities equipment", search_result(
        "facilities equipment facts", [(URL, "t")], TODAY))

    extractor = ScriptedBackend(role="extractor", family="anthropic")
    extractor.script("extract", "", {"claims": [
        {"assertion": q, "quote": q, "area": "Facilities", "knowledge_type": "concept", "question": "domain"}
        for q in QUOTES
    ]})
    # decoy: models["extractor"] per the role table — a catch-all mutated claim for whichever
    # located claims get sampled.
    extractor.script("decoy", "", {"mutated_claim": "The reservoir tank holds two litres of coolant.",
                                     "mutation": "number"})

    # A decoy verify call carries the mutated claim *and* the real span (A6), so it will also
    # contain the original quote text — the decoy-specific match must be registered before the
    # real-claim ones or a real-claim script would shadow it. "two litres" is unique to the
    # mutation and appears in no real quote.
    verifier = ScriptedBackend(role="verifier", family="openai")
    verifier.script("verify", "two litres of coolant", {"verdict": "insufficient", "supporting_quote": ""})
    for q in QUOTES:
        verifier.script("verify", q[:25], {"verdict": "supports", "supporting_quote": q})

    contradiction = ScriptedBackend(role="contradiction", family="openai")
    models = make_models(planner=planner, extractor=extractor, verifier=verifier,
                          contradiction=contradiction, out=out)
    run_dir = Path(reconstruct(domain="facilities", task="t", models=models, http=http_client(pages),
                                out=out, today=TODAY, max_results=5))

    ledger = Ledger.from_json((run_dir / "ledger.json").read_text())
    mutated_texts = {"The reservoir tank holds two litres of coolant."}
    assert not any(c.assertion in mutated_texts for c in ledger.claims), (
        "a decoy's mutated claim must never appear in the ledger")

    sidecar = read_json(run_dir / "sidecar.json")
    decoys = sidecar["decoys"]
    assert decoys, "expected at least one decoy to have been sampled and verified"
    accepted = sum(1 for d in decoys if d["false_accept"])
    expected_rate = accepted / len(decoys)
    assert sidecar["stats"]["decoy_false_accept_rate"] == expected_rate
    assert expected_rate == 0.0, "every decoy was scripted to be correctly rejected"
