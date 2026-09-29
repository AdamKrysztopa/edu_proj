"""Fixture-ledger builders for gapmap tests (mirrors residual/tests/conftest.py). Every claim
built here carries the plainest evidence that gives it the intended pool (A/S/U, spec §1.1)."""
from __future__ import annotations

from datetime import date

from residual.claims import ClaimRecord, Scope
from residual.ledger import Area, Ledger
from residual.provenance import Agent, Evidence, Generation, Search, Selector, Source, Verdict, Verification
from residual.vocab import EpistemicLabel, KnowledgeType, Layer, Question, SourceKind, Tacitness, Voice, World

from gapmap import link, lenses, record

DAY = date(2026, 9, 28)
CODER = Agent(kind="human", id="coder-1")
EXTRACTOR = Agent(kind="model", id="extractor-1", family="family-a")
SCOPE = Scope(domain="test-domain")


def source(identifier: str = "doi:10.0/test", *, kind: SourceKind = SourceKind.DOCUMENTATION,
           world: World = World.A, voice: Voice = Voice.EXPERT, independence_key: str | None = None,
           published: date | None = date(2020, 1, 1), organisation: str | None = None) -> Source:
    if world is World.B and organisation is None:
        organisation = "org-1"
    return Source(identifier=identifier, kind=kind, world=world, voice=voice,
                  independence_key=independence_key or identifier, published=published,
                  organisation=organisation)


def a_claim(assertion: str, *, exact: str | None = None, question: Question = Question.PERFORMANCE,
            layer: Layer = Layer.PERFORMANCE, knowledge_type: KnowledgeType = KnowledgeType.PROCEDURE_STEP,
            source_id: str = "doi:10.0/test-1", independence_key: str | None = None,
            source_kind: SourceKind = SourceKind.DOCUMENTATION, **kw) -> ClaimRecord:
    """An attested (pool A) claim: one span of supporting, human-verified evidence."""
    exact = assertion if exact is None else exact
    src = source(source_id, kind=source_kind, independence_key=independence_key)
    ev = Evidence(source=src, selector=Selector(exact=exact, locator="p. 1"), retrieved=DAY,
                  verification=Verification(verdict=Verdict.SUPPORTS, verifier=CODER, on=DAY))
    return ClaimRecord(assertion=assertion, question=question, layer=layer,
                        knowledge_type=knowledge_type, scope=SCOPE, evidence=(ev,), **kw)


def s_claim(assertion: str, *, exact: str | None = None, question: Question = Question.PERFORMANCE,
            layer: Layer = Layer.PERFORMANCE, knowledge_type: KnowledgeType = KnowledgeType.PROCEDURE_STEP,
            source_id: str = "doi:10.0/synth", **kw) -> ClaimRecord:
    """A synthetic (pool S) claim: extracted, verdict still pending."""
    exact = assertion if exact is None else exact
    src = source(source_id)
    ev = Evidence(source=src, selector=Selector(exact=exact, locator="p. 1"), retrieved=DAY,
                  verification=Verification(verdict=Verdict.PENDING))
    gen = Generation(agent=EXTRACTOR, activity="extraction", on=DAY, spec_sha256="0" * 64)
    return ClaimRecord(assertion=assertion, question=question, layer=layer, knowledge_type=knowledge_type,
                        scope=SCOPE, evidence=(ev,), generation=gen, **kw)


def a_claim_n(assertion: str, *, n: int = 2, question: Question = Question.PERFORMANCE,
              layer: Layer = Layer.PERFORMANCE, knowledge_type: KnowledgeType = KnowledgeType.PROCEDURE_STEP,
              **kw) -> ClaimRecord:
    """An attested claim with `n` supporting spans from `n` distinct independence keys: the
    cheapest way to give a single-seed lens candidate `k_step`/`k_topic` >= `n` without depending
    on neighbourhood linking (which tiny fixture ledgers distort, see `fillers`)."""
    evs = tuple(Evidence(source=source(f"multi-{i}", independence_key=f"multi-key-{i}"),
                         selector=Selector(exact=assertion, locator="p. 1"), retrieved=DAY,
                         verification=Verification(verdict=Verdict.SUPPORTS, verifier=CODER, on=DAY))
               for i in range(n))
    return ClaimRecord(assertion=assertion, question=question, layer=layer, knowledge_type=knowledge_type,
                       scope=SCOPE, evidence=evs, **kw)


def u_claim(assertion: str, *, question: Question = Question.PERFORMANCE, layer: Layer = Layer.PERFORMANCE,
            knowledge_type: KnowledgeType = KnowledgeType.CONCEPT, **kw) -> ClaimRecord:
    """An unknown (pool U) claim: a slot probe with nothing found."""
    se = Search(corpus="c", query="q", on=DAY, agent=CODER)
    return ClaimRecord(assertion=assertion, question=question, layer=layer, knowledge_type=knowledge_type,
                        scope=SCOPE, searches=(se,), **kw)


def ledger(claims, *, areas=(), assignments=(), purpose: str = "reconstruction") -> Ledger:
    return Ledger(purpose=purpose, claims=tuple(claims), areas=tuple(areas), assignments=tuple(assignments))


def area(area_id: str, name: str = "area") -> Area:
    return Area(area_id=area_id, scope=SCOPE, name=name)


def fillers(n: int, *, prefix: str = "filler") -> list:
    """Distinct filler A claims with vocabulary disjoint from a scenario's claims, so that with
    enough of them a scenario's shared stems stay under the 5% common-stem cut (spec §1.3):
    without dilution, tiny fixture ledgers make almost every stem 'common'."""
    return [a_claim(f"Component code {prefix}{i:03d} was inspected without incident.",
                    source_id=f"{prefix}-{i}")
            for i in range(n)]


def mk_record(gap_id: str, lens: str, category: str, seeds=(), *, score: int = 1, r: int = 4,
             k_topic: int = 2, k_step: int = 1, rank=None) -> record.Record:
    """A bare Record for rank.py tests: real lens output is exercised in test_lens_*.py, so rank
    tests build records directly instead of re-running a lens."""
    conf = record.Confidence(score=score, A=0, B=0, P=0, Q=0, breadth="narrow", robustness=f"{r}/4",
                             k_step=k_step, k_topic=k_topic)
    ig = record.InferredGap(statement="stmt", test_id="t", closure_state="open")
    ev = tuple(record.EvidenceItem(
        claim_id=cid, epistemic_label=EpistemicLabel.LITERATURE_SUPPORTED,
        knowledge_type=KnowledgeType.PROCEDURE_STEP, area_id=None, source_identifier=cid,
        independence_key=cid, source_kind=SourceKind.DOCUMENTATION, verdict=Verdict.SUPPORTS,
        span="span", role="seed", counts_as_attestation=True) for cid in seeds)
    hyp = (record.Hypothesis(text="t", predicted_knowledge_type=(KnowledgeType.CUE,),
                             predicted_tacitness=(Tacitness.RELATIONAL,), channel="c")
          if category == "HYP" else None)
    return record.Record(gap_id=gap_id, lens=lens, category=category, anchor="anchor",
                         observed_evidence=ev, inferred_gap=ig, hypothesis=hyp, reasoning="r",
                         missing="m", confidence=conf, alternatives=(), question=None, rank=rank)


import re as _re


class FakeJudge:
    """A deterministic, network-free `Judge` (S1: "tests use a fake judge"). It reads the numbered
    `<n>:` sentence lines a real prompt carries (fix 1: a single bare-integer scheme, never
    `A<n>`/`S<n>`) and marks an id "states" if its sentence contains the literal marker
    `CLOSES_HERE`, "partially" if it contains `PARTIAL_HERE`; a fixture spells one of these into
    the exact evidence span it wants the judge to find, the same way lexical fixtures spelled out
    a regex-triggering phrase (e.g. "5 millimeters" for QUANT)."""

    _LINE = _re.compile(r"^(\d+): (.*)$")

    def __init__(self, model_id: str = "fake-judge-v1"):
        self.model_id = model_id

    def ask(self, prompt: str) -> dict:
        states, partially = [], []
        for line in prompt.splitlines():
            m = self._LINE.match(line)
            if not m:
                continue
            id_, sent = m.group(1), m.group(2)
            if "CLOSES_HERE" in sent:
                states.append(id_)
            elif "PARTIAL_HERE" in sent:
                partially.append(id_)
        return {"states": states, "partially": partially, "reason": "fake"}


def run_lens(name: str, lg, judge=None):
    """Fire one lens at the canonical setting, judge each candidate (a `FakeJudge` by default) and
    categorize it, for lens tests. Returns `(candidate, outcome, category)` triples; `candidate`
    may be a judge-finalised replacement of the fired one (DIAG)."""
    from gapmap import semantic
    idx = link.build_index(lg)
    j = judge if judge is not None else FakeJudge()
    out = []
    for cand in lenses.LENSES[name](lg, idx, link.SETTING_1):
        outcome, sub = semantic.judge_candidate(lg, idx, j, cand)
        k_topic = len(link.breadth(lg, sub.x_a))
        cat = None if outcome.state == "closed" else record.categorize(outcome.state, k_topic)
        out.append((sub, outcome, cat))
    return out
