"""Builders shared by the tests. Every default is the plainest valid value, so a test states
only what it is about."""
from __future__ import annotations

from datetime import date

from residual.claims import ClaimRecord, Scope
from residual.provenance import (
    Agent,
    Evidence,
    Generation,
    Search,
    Selector,
    Source,
    Verdict,
    Verification,
)
from residual.vocab import KnowledgeType, Layer, Question, SourceKind, Voice, World

DAY = date(2026, 9, 28)
CODER = Agent(kind="human", id="coder-1")
GENERATOR = Agent(kind="model", id="gen-model-1", family="family-a")
VERIFIER = Agent(kind="model", id="verifier-model-1", family="family-b")
SCOPE = Scope(domain="test-domain")


def source(identifier: str = "doi:10.0000/test", *, kind: SourceKind = SourceKind.STUDY,
           world: World = World.A, voice: Voice = Voice.EXPERT, independence_key: str | None = None,
           published: date | None = date(2020, 1, 1), organisation: str | None = None,
           boundary: bool = False) -> Source:
    if world is World.B and organisation is None:
        organisation = "org-1"
    return Source(identifier=identifier, kind=kind, world=world, voice=voice,
                  independence_key=independence_key or identifier, published=published,
                  organisation=organisation, boundary=boundary)


def evidence(src: Source | None = None, *, verdict: Verdict = Verdict.SUPPORTS,
             verifier: Agent = CODER, exact: str = "the quoted span") -> Evidence:
    src = src or source()
    verification = (Verification(verdict=verdict) if verdict is Verdict.PENDING
                    else Verification(verdict=verdict, verifier=verifier, on=DAY))
    return Evidence(source=src, selector=Selector(exact=exact, locator="p. 1"), retrieved=DAY,
                    verification=verification)


def generation(agent: Agent = GENERATOR, activity: str = "extraction", **kw) -> Generation:
    if agent.kind == "model":
        kw.setdefault("spec_sha256", "0" * 64)
    return Generation(agent=agent, activity=activity, on=DAY, **kw)


def search(agent: Agent = CODER) -> Search:
    return Search(corpus="test-corpus", query="q", on=DAY, agent=agent)


def claim(assertion: str = "An assertion.", **kw) -> ClaimRecord:
    kw.setdefault("question", Question.PERFORMANCE)
    kw.setdefault("layer", Layer.PERFORMANCE)
    kw.setdefault("knowledge_type", KnowledgeType.PROCEDURE_STEP)
    kw.setdefault("scope", SCOPE)
    return ClaimRecord(assertion=assertion, **kw)
