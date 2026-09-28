"""Black-box test support for N2a — independent of the implementer's internal functions.

Everything here talks only to the pinned interface: reconstruct.llm's Model/Backend/SearchResult/
Hit/exceptions, residual.provenance.Agent (needed to construct a Model), and the run directory's
own files (ledger.json, sidecar.json, calls.jsonl, snapshots/). No test in this suite makes a
live network or model call: every backend here is scripted, and every page is served from a
fixture by httpx.MockTransport.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Mapping

import httpx

from reconstruct.llm import BudgetExceeded, Hit, Model, SearchResult
from residual.provenance import Agent

FIXTURES = Path(__file__).parent / "fixtures" / "e2e"

TODAY = date(2026, 9, 28)

ROLE_FAMILIES = {"planner": "anthropic", "extractor": "anthropic",
                  "verifier": "openai", "contradiction": "openai"}


def read_fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


# --- scripted model backend ---------------------------------------------------------------------

@dataclass
class Call:
    task: str
    system: str
    user: str
    schema: dict


class NoScriptedResponse(LookupError):
    """A test forgot to script a response for a call the run actually made. This is a test
    fixture gap, not necessarily a defect in the implementation under test."""


@dataclass
class ScriptedBackend:
    """A reconstruct.llm.Backend driven entirely by scripts: complete_json dispatches on task
    name, then on the first scripted entry whose substring is found in the user text (entries
    are tried in the order they were added — put more specific matches before a catch-all "").
    A scripted response is a dict (returned as-is), a BaseException instance (raised) or a
    callable taking the matched text and returning a dict.

    Every call is recorded (task/system/user/schema for model calls; query/max_results for
    search) so a test can assert on exactly what the run sent a given role.
    """

    role: str
    family: str
    calls: list[Call] = field(default_factory=list)
    search_calls: list[dict] = field(default_factory=list)
    scripts: dict[str, list[tuple[str, object]]] = field(default_factory=dict)
    search_scripts: list[tuple[str, object]] = field(default_factory=list)
    budget: "SharedBudget | None" = None
    calls_log_path: Path | None = None

    def script(self, task: str, match: str, response: object) -> "ScriptedBackend":
        self.scripts.setdefault(task, []).append((match, response))
        return self

    def script_search(self, match: str, response: object) -> "ScriptedBackend":
        self.search_scripts.append((match, response))
        return self

    def complete_json(self, task: str, system: str, user: str, schema: dict) -> dict:
        if self.budget is not None:
            self.budget.check()
        self.calls.append(Call(task=task, system=system, user=user, schema=schema))
        self._log(task)
        return self._dispatch(self.scripts.get(task, []), user, f"task={task!r}")

    def search(self, query: str, *, max_results: int) -> SearchResult:
        if self.budget is not None:
            self.budget.check()
        self.search_calls.append({"query": query, "max_results": max_results})
        self._log("search")
        return self._dispatch(self.search_scripts, query, f"query={query!r}")

    def _dispatch(self, entries, text, what):
        for substr, response in entries:
            if substr in text:
                if isinstance(response, BaseException):
                    raise response
                if callable(response) and not isinstance(response, (dict, SearchResult)):
                    return response(text)
                return response
        raise NoScriptedResponse(f"no scripted response matches {what}: {text[:300]!r}")

    def _log(self, task: str) -> None:
        if self.calls_log_path is None:
            return
        self.calls_log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.calls_log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"task": task, "role": self.role, "family": self.family,
                                 "utc": datetime.now(UTC).isoformat()}) + "\n")


@dataclass
class SharedBudget:
    """Simulates a run-level cost budget shared across every role's backend: the call that
    reaches `max_calls` (counted across every role, mirroring a single running cost total)
    raises reconstruct.llm.BudgetExceeded, matching CallLog.ensure_budget's "before dispatch,
    not after" contract."""

    max_calls: int
    made: int = 0

    def check(self) -> None:
        if self.made >= self.max_calls:
            raise BudgetExceeded(f"scripted budget exhausted after {self.max_calls} calls")
        self.made += 1


def search_result(query: str, hits: list[tuple[str, str]], on: date = TODAY) -> SearchResult:
    return SearchResult(executed_query=query, on=on, hits=tuple(Hit(url=u, title=t) for u, t in hits))


DECOY_MARKER = "ZZZ-decoy-mutation-marker"
"""Public: present only in a decoy's own mutated-claim text (script_default_decoys), never in
any fixture page or real claim — a test can use it to tell a decoy verify call apart from a
real one when both land in the same ScriptedBackend.calls list (A6 makes a decoy call
unavoidable once a run has any located claim)."""

_DEFAULT_DECOY_MUTATION = (f"{DECOY_MARKER}: this sentence was synthetically altered by the "
                           "test harness and does not appear on any fixture page.")


def script_default_decoys(extractor: ScriptedBackend, verifier: ScriptedBackend, *,
                           mutated_claim: str = _DEFAULT_DECOY_MUTATION, mutation: str = "number") -> None:
    """Opt-in helper for tests that do not care about decoys but must not choke on one: A6
    samples decoys from EVERY run with at least one located claim, so any test whose extractor
    has no scripted "decoy" response — or whose verifier has no response for the decoy's verify
    call — hits NoScriptedResponse, which is a test-fixture gap, not a defect under test.

    Registers a catch-all "decoy" response on `extractor` (decoy: models["extractor"] per the
    role table, now also carrying a `rationale` so `evidence.decoy_is_valid` accepts it — MUST-FIX
    4's validity check excludes a decoy that has none) and a decoy-specific "insufficient"
    response on `verifier`. The verifier entry is inserted ahead of every other scripted response
    (regardless of when this is called) because a decoy's verify call plausibly also carries the
    real span it was paired with (A6): without priority, a real-claim script already registered
    for that span could shadow the decoy's own response, or (called the other way around) a
    generically-matched decoy entry could shadow a real claim's response. The marker text is
    unique to the mutation and never appears in any fixture page, so it can only ever match a
    genuine decoy call. A6/MUST-FIX 4 samples up to 10 decoys per mutation type (not just one), so
    this same catch-all may be hit once per sampled claim in a run with several located claims.
    """
    extractor.script("decoy", "", {"mutated_claim": mutated_claim, "mutation": mutation,
                                    "rationale": "synthetically mutated by the test harness"})
    marker = mutated_claim[:26]
    verifier.scripts.setdefault("verify", []).insert(
        0, (marker, {"verdict": "insufficient", "supporting_quote": ""}))


def make_models(*, planner: ScriptedBackend | None = None, extractor: ScriptedBackend | None = None,
                 verifier: ScriptedBackend | None = None, contradiction: ScriptedBackend | None = None,
                 families: Mapping[str, str] | None = None,
                 out: Path | None = None) -> dict[str, Model]:
    """Assembles the {role: Model} mapping reconstruct.run.reconstruct needs. Any role left
    unspecified gets an empty ScriptedBackend (it will raise NoScriptedResponse if the run
    actually calls it — a loud signal that the test under-scripted, not a silent pass).

    A backend's own `.family` (set when the test constructed it, e.g. to deliberately test a
    same-family scenario) is always authoritative and is never silently overwritten. `families`
    only fills in a role whose backend was left unspecified; if it's given for a role AND that
    role's backend was also given, the two must agree — this is a test-authoring error, not a
    run-time condition, so it raises rather than picking one silently.
    """
    backends = {"planner": planner, "extractor": extractor, "verifier": verifier,
                "contradiction": contradiction}
    explicit_families = families or {}
    resolved: dict[str, str] = {}
    for role, backend in backends.items():
        override = explicit_families.get(role)
        if backend is not None:
            if override is not None and override != backend.family:
                raise ValueError(
                    f"role {role!r}: families[{role!r}]={override!r} disagrees with the "
                    f"backend's own family {backend.family!r} — construct the backend with the "
                    f"family you want and omit it from `families`, don't pass both")
            resolved[role] = backend.family
        else:
            resolved[role] = override or ROLE_FAMILIES[role]

    models: dict[str, Model] = {}
    for role, backend in backends.items():
        family = resolved[role]
        backend = backend or ScriptedBackend(role=role, family=family)
        backend.role = role
        if out is not None and backend.calls_log_path is None:
            backend.calls_log_path = out / "calls.jsonl"
        agent = Agent(kind="model", id=f"scripted/{role}-v1", family=family)
        models[role] = Model(agent=agent, backend=backend)
    return models


# --- fixture-page HTTP transport ------------------------------------------------------------------

@dataclass
class Page:
    body: str | bytes = ""
    status: int = 200
    content_type: str = "text/html; charset=utf-8"
    redirect_to: str | None = None


def fixture_transport(pages: Mapping[str, Page], *, default_status: int = 404) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        page = pages.get(str(request.url))
        if page is None:
            return httpx.Response(default_status, headers={"content-type": "text/plain"},
                                   content=b"not found")
        if page.redirect_to is not None:
            return httpx.Response(302, headers={"location": page.redirect_to})
        body = page.body.encode("utf-8") if isinstance(page.body, str) else page.body
        return httpx.Response(page.status, headers={"content-type": page.content_type}, content=body)
    return httpx.MockTransport(handler)


def http_client(pages: Mapping[str, Page]) -> httpx.Client:
    return httpx.Client(transport=fixture_transport(pages))


def page_from_fixture(name: str, **kw) -> Page:
    return Page(body=read_fixture(name), **kw)


# --- reading run-dir artefacts ---------------------------------------------------------------------

def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


_LOCATOR_RE = re.compile(r"^sha256:([0-9a-f]{64});char=(\d+),(\d+)$")


def resolve_selector_exact(run_dir: Path, selector) -> str:
    """Independently re-slices a Selector's locator against the run's own snapshot text — the
    same check verify_run performs, done here so a test does not have to trust verify_run alone
    (risk check 1: verify_run re-extracts from snapshots and re-slices every locator)."""
    m = _LOCATOR_RE.match(selector.locator or "")
    assert m, f"locator does not match the pinned sha256:...;char=start,end format: {selector.locator!r}"
    sha, start, end = m.group(1), int(m.group(2)), int(m.group(3))
    text = (run_dir / "snapshots" / f"{sha}.txt").read_text(encoding="utf-8")
    return text[start:end]


def find_claim(ledger, assertion_contains: str):
    matches = [c for c in ledger.claims if assertion_contains in c.assertion]
    assert matches, (f"no claim with assertion containing {assertion_contains!r}; "
                      f"have {[c.assertion for c in ledger.claims]}")
    assert len(matches) == 1, f"ambiguous match for {assertion_contains!r}: {[c.assertion for c in matches]}"
    return matches[0]


def area_by_name(ledger, name: str):
    matches = [a for a in ledger.areas if a.name.strip().casefold() == name.strip().casefold()]
    assert matches, f"no area named {name!r}; have {[a.name for a in ledger.areas]}"
    return matches[0]


def all_evidence(ledger):
    return [e for c in ledger.claims for e in c.evidence]
