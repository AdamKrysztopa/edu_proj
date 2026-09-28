"""Offline end-to-end smoke test: a scripted fake Backend + httpx.MockTransport drive
reconstruct.run.reconstruct() through a full plan/search/fetch/extract/verify/decoy/
contradict/assemble cycle, with no network or model call ever made for real."""
from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import httpx
import pytest

from reconstruct.llm import Hit, Model, SearchResult
from reconstruct.run import reconstruct
from residual.ledger import Ledger
from residual.provenance import Agent
from residual.vocab import EpistemicLabel

TODAY = date(2026, 9, 28)

URL_A = "https://smoke-alpha.example/notes"
URL_B = "https://smoke-beta.example/notes"

QUOTE_A = "A pressure relief valve opens automatically once system pressure exceeds its set point."

# fetch() rejects near-empty pages (MUST 1: visible text < 500 chars); padding keeps these fixture
# pages realistic in length without changing the sentence each test actually locates or asserts on.
_PAD_A = " ".join(f"padsmokea{i}" for i in range(80))
_PAD_B = " ".join(f"padsmokeb{i}" for i in range(80))


@dataclass
class FakeBackend:
    """Conforms to reconstruct.llm.Backend: complete_json(task, system, user, schema) -> dict
    and search(query, *, max_results) -> SearchResult. Dispatches on `task` then on a substring
    of `user`/`query`, exactly like the pinned contract's task-name table describes."""

    family: str
    json_scripts: dict[str, list[tuple[str, dict]]] = field(default_factory=dict)
    search_scripts: list[tuple[str, SearchResult]] = field(default_factory=list)
    calls: list[tuple[str, str]] = field(default_factory=list)

    def on(self, task: str, match: str, response: dict) -> None:
        self.json_scripts.setdefault(task, []).append((match, response))

    def on_search(self, match: str, result: SearchResult) -> None:
        self.search_scripts.append((match, result))

    def complete_json(self, task: str, system: str, user: str, schema: dict) -> dict:
        self.calls.append((task, user))
        for match, response in self.json_scripts.get(task, []):
            if match in user:
                return response
        raise AssertionError(f"no script for task={task!r} matching user text: {user[:200]!r}")

    def search(self, query: str, *, max_results: int) -> SearchResult:
        for match, result in self.search_scripts:
            if match in query:
                return result
        raise AssertionError(f"no search script matching query: {query!r}")


def make_model(role: str, family: str) -> tuple[Model, FakeBackend]:
    backend = FakeBackend(family=family)
    agent = Agent(kind="model", id=f"fake/{role}", family=family)
    return Model(agent=agent, backend=backend), backend


@pytest.fixture
def run_dir(tmp_path):
    out = tmp_path / "run"
    pages = {
        URL_A: httpx.Response(200, headers={"content-type": "text/html"},
                              content=(f"<html><body><p>{QUOTE_A}</p><p>{_PAD_A}</p>"
                                       "</body></html>").encode()),
        URL_B: httpx.Response(200, headers={"content-type": "text/html"},
                              content=(f"<html><body><p>Nothing relevant on this page.</p>"
                                       f"<p>{_PAD_B}</p></body></html>").encode()),
    }

    def handler(request: httpx.Request) -> httpx.Response:
        return pages.get(str(request.url), httpx.Response(404, content=b"not found"))

    http = httpx.Client(transport=httpx.MockTransport(handler))

    planner, planner_backend = make_model("planner", "anthropic")
    planner_backend.on("plan", "", {"areas": [
        {"name": "Safety Valves", "queries": ["relief valve set point"]},
        {"name": "Maintenance", "queries": ["valve maintenance schedule"]},
    ]})
    planner_backend.on_search("relief valve", SearchResult(
        executed_query="relief valve set point", on=TODAY, hits=(Hit(url=URL_A, title="notes"),)))
    planner_backend.on_search("valve maintenance", SearchResult(
        executed_query="valve maintenance schedule", on=TODAY, hits=(Hit(url=URL_B, title="notes"),)))

    extractor, extractor_backend = make_model("extractor", "anthropic")
    extractor_backend.on("extract", "pressure relief valve", {"claims": [{
        "assertion": "A pressure relief valve opens once pressure exceeds its set point.",
        "quote": QUOTE_A, "area": "Safety Valves", "knowledge_type": "concept", "question": "domain",
    }]})
    extractor_backend.on("extract", "Nothing relevant", {"claims": []})
    extractor_backend.on("decoy", "", {"mutated_claim": "A pressure relief valve never opens.",
                                       "mutation": "negation"})

    verifier, verifier_backend = make_model("verifier", "openai")
    # The decoy's mutated claim also contains "pressure relief valve", so its more specific
    # match must be registered first or the real-claim script below would shadow it.
    verifier_backend.on("verify", "never opens", {"verdict": "refutes", "supporting_quote": QUOTE_A})
    verifier_backend.on("verify", "pressure relief valve", {"verdict": "supports", "supporting_quote": QUOTE_A})

    contradiction, contradiction_backend = make_model("contradiction", "openai")

    models = {"planner": planner, "extractor": extractor, "verifier": verifier,
              "contradiction": contradiction}

    result_dir = reconstruct(domain="industrial safety", task="relief valve inspection",
                             models=models, http=http, out=out, today=TODAY, max_results=5)
    return Path(result_dir)


def test_run_produces_every_documented_artefact(run_dir):
    for name in ("ledger.json", "sidecar.json", "report.md", "areas.json"):
        assert (run_dir / name).exists()
    assert (run_dir / "snapshots").is_dir()
    assert any((run_dir / "snapshots").iterdir())


def test_ledger_is_valid_and_supported_claim_is_literature_supported(run_dir):
    ledger = Ledger.from_json((run_dir / "ledger.json").read_text())
    claim = next(c for c in ledger.claims if "pressure relief valve" in c.assertion.casefold())
    assert claim.label == EpistemicLabel.LITERATURE_SUPPORTED
    assert claim.evidence[0].verification.verdict == "supports"


def test_areas_json_round_trips_with_its_own_sha256(run_dir):
    payload = json.loads((run_dir / "areas.json").read_text())
    assert set(payload) == {"areas", "sha256"}
    assert {a["name"] for a in payload["areas"]} == {"Safety Valves", "Maintenance"}


def test_sidecar_has_a_decoy_that_was_correctly_rejected(run_dir):
    sidecar = json.loads((run_dir / "sidecar.json").read_text())
    assert sidecar["decoys"]
    assert all(not d["false_accept"] for d in sidecar["decoys"])
    assert sidecar["stats"]["decoy_false_accept_rate"] == 0.0


def test_verify_run_accepts_the_run(run_dir):
    proc = subprocess.run([sys.executable, "-m", "reconstruct.verify_run", str(run_dir)],
                          capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_verify_run_fails_on_a_missing_snapshot(run_dir):
    snapshot = next((run_dir / "snapshots").glob("*.txt"))
    snapshot.unlink()
    proc = subprocess.run([sys.executable, "-m", "reconstruct.verify_run", str(run_dir)],
                          capture_output=True, text=True)
    assert proc.returncode != 0


def test_verify_run_fails_on_a_tampered_snapshot(run_dir):
    snapshot = next((run_dir / "snapshots").glob("*.txt"))
    original = snapshot.read_text(encoding="utf-8")
    snapshot.write_text(original.replace("pressure", "PRESSURE"), encoding="utf-8")
    proc = subprocess.run([sys.executable, "-m", "reconstruct.verify_run", str(run_dir)],
                          capture_output=True, text=True)
    assert proc.returncode != 0
