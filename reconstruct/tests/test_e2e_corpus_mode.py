"""Corpus mode (E-PLANT): `reconstruct()`'s `search_corpus` kwarg tags every Search record with
where it came from, and the sidecar's `n3_input` gate reflects it — a corpus run is never valid
N3 input (E-PLANT's corpus contains a deliberately planted fabrication), regardless of whether it
completed; a live run is valid N3 input exactly when it completed. Offline only: the "corpus"
here is a manifest + local file built in a temp dir, read through `reconstruct.corpus.corpus_client`
and `CorpusSearchBackend`, exactly as `python -m reconstruct.run --corpus` wires them.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from reconstruct.corpus import CorpusSearchBackend, corpus_client
from reconstruct.llm import Model
from reconstruct.run import reconstruct
from residual.ledger import Ledger
from residual.provenance import Agent

from e2e_support import (
    TODAY, ScriptedBackend, find_claim, make_models, read_json, script_default_decoys, search_result,
)

DOC_URL = "https://corpus-doc.example/reference"
QUOTE = ("The rated load of the sling must never exceed its certified working limit under "
         "normal operating conditions.")


def _build_corpus(tmp_path: Path) -> tuple[Path, Path]:
    root = tmp_path / "corpus_bytes"
    root.mkdir()
    padding = " ".join(f"corpuspad{i}" for i in range(80))  # clears the near-empty-page floor
    (root / "doc.html").write_text(
        f"<!doctype html><html><body><p>{QUOTE}</p><p>{padding}</p></body></html>", encoding="utf-8")
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps({"documents": [
        {"url": DOC_URL, "content_type": "text/html", "file": "doc.html", "title": "Reference"},
    ]}), encoding="utf-8")
    return manifest_path, root


def _models(out: Path):
    planner = ScriptedBackend(role="planner", family="anthropic")
    planner.script("plan", "", {"areas": [{"name": "Rigging", "queries": ["sling rated load"]}]})

    extractor = ScriptedBackend(role="extractor", family="anthropic")
    extractor.script("extract", "rated load", {"claims": [
        {"assertion": "A sling's rated load must never be exceeded.", "quote": QUOTE,
         "area": "Rigging", "knowledge_type": "concept", "question": "domain"}]})

    verifier = ScriptedBackend(role="verifier", family="openai")
    verifier.script("verify", "", {"verdict": "supports", "supporting_quote": QUOTE,
                                    "adds_content": False, "subject_or_scope_differs": False,
                                    "quantifier_modality_or_connective_differs": False})
    script_default_decoys(extractor, verifier)

    return make_models(planner=planner, extractor=extractor, verifier=verifier, out=out)


def test_corpus_mode_tags_searches_and_is_never_n3_input(tmp_path):
    manifest_path, root = _build_corpus(tmp_path)
    out = tmp_path / "run"
    models = _models(out)
    manifest_sha = hashlib.sha256(manifest_path.read_bytes()).hexdigest()

    corpus_planner = models["planner"]
    models = {**models, "planner": Model(
        agent=corpus_planner.agent,
        backend=CorpusSearchBackend(inner=corpus_planner.backend, manifest=manifest_path))}
    client = corpus_client(manifest_path, root)

    run_dir = Path(reconstruct(domain="rigging", task="t", models=models, http=client, out=out,
                                today=TODAY, max_results=5, search_corpus=f"corpus:{manifest_sha}"))

    ledger = Ledger.from_json((run_dir / "ledger.json").read_text())
    claim = find_claim(ledger, "sling's rated load")
    assert claim.searches, "the claim must record the search that turned up its source"
    assert all(s.corpus == f"corpus:{manifest_sha}" for s in claim.searches)

    sidecar = read_json(run_dir / "sidecar.json")
    assert sidecar["complete"] is True, sidecar["incomplete_reasons"]
    assert sidecar["n3_input"] is False
    assert sidecar["n3_input_reason"] == "E-PLANT corpus contains planted fabrications"


def test_web_mode_is_n3_input_exactly_when_complete(tmp_path):
    manifest_path, root = _build_corpus(tmp_path)  # reused only to serve the same page over http
    out = tmp_path / "run"
    models = _models(out)
    models["planner"].backend.script_search(
        "sling rated load", search_result("sling rated load", [(DOC_URL, "t")], TODAY))
    client = corpus_client(manifest_path, root)  # a plain httpx.Client would do too; reuses the page

    run_dir = Path(reconstruct(domain="rigging", task="t", models=models, http=client, out=out,
                                today=TODAY, max_results=5))

    sidecar = read_json(run_dir / "sidecar.json")
    assert sidecar["complete"] is True
    assert sidecar["n3_input"] is True
    assert sidecar["n3_input_reason"] is None

    ledger = Ledger.from_json((run_dir / "ledger.json").read_text())
    claim = find_claim(ledger, "sling's rated load")
    assert all(s.corpus == "web:openrouter-exa" for s in claim.searches)


# --- CLI wiring: `python -m reconstruct.run --corpus ...` ---------------------------------------

def test_cli_wires_corpus_mode_into_reconstruct(tmp_path, monkeypatch):
    """main() must: build its http client from corpus_client (not a live httpx.Client), wrap the
    planner backend in CorpusSearchBackend, and pass a "corpus:<sha256>" search_corpus through —
    without ever touching the network or a real model (load_models and reconstruct are both
    monkeypatched to capture what they were called with)."""
    import reconstruct.run as run_module

    manifest_path, root = _build_corpus(tmp_path)
    out_dir = tmp_path / "cli-runs"
    captured: dict = {}

    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")

    def fake_load_models(path, *, log, env):
        backend = ScriptedBackend(role="planner", family="anthropic")
        agent = Agent(kind="model", id="fake/planner", family="anthropic")
        return {"planner": Model(agent=agent, backend=backend)}

    def fake_reconstruct(domain, task, *, models, http, out, today, areas, blocklist,
                          max_results, max_doc_chars, search_corpus):
        captured["models"] = models
        captured["search_corpus"] = search_corpus
        # the http client is closed by main()'s `with` block right after this returns, so any
        # request through it must happen here, while it is still open.
        captured["response_status"] = http.get(DOC_URL).status_code
        out = Path(out)
        out.mkdir(parents=True, exist_ok=True)
        (out / "marker").write_text("ok")
        return out

    monkeypatch.setattr(run_module, "load_models", fake_load_models)
    monkeypatch.setattr(run_module, "reconstruct", fake_reconstruct)

    rc = run_module.main([
        "--live", "--domain", "rigging", "--task", "t", "--out", str(out_dir),
        "--corpus", str(manifest_path), "--corpus-root", str(root),
    ])
    assert rc == 0
    assert captured["search_corpus"].startswith("corpus:")
    assert isinstance(captured["models"]["planner"].backend, CorpusSearchBackend)
    assert captured["response_status"] == 200, (
        "the CLI's http client must be corpus_client's, serving the manifest")
