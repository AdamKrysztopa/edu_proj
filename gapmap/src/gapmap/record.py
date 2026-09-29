"""Candidate -> tier-separated `Record` (spec §4): the schema, confidence rubric (§5), robustness
and the RG-UNK retrieval-gap rows (§3) that come from the U pool and the sidecar rather than a
lens. `Record` never mixes tiers: `observed_evidence` is verbatim spans only, `inferred_gap` is a
re-runnable statement, `hypothesis` is always `label: "inferred"` and only present for HYP."""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Literal

from residual.ledger import Ledger
from residual.provenance import Record as Base
from residual.provenance import Verdict
from residual.vocab import CRITERION_LABELS, EpistemicLabel, KnowledgeType, SourceKind, Tacitness

from gapmap import config, lenses, link, semantic

Category = Literal["HYP", "RG-UNK", "RG-SINGLE", "RG-UNVER", "RG-SIBLING", "RG-UNDECIDED", "CONTROL"]


class EvidenceItem(Base):
    claim_id: str
    epistemic_label: EpistemicLabel
    knowledge_type: KnowledgeType
    area_id: str | None
    source_identifier: str
    independence_key: str
    source_kind: SourceKind
    verdict: Verdict
    span: str | None
    role: Literal["seed", "topic", "rival", "closure_near"]
    counts_as_attestation: bool
    flag: str | None = None


class Sibling(Base):
    matched_gap_id: str | None = None
    state: str | None = None


class InferredGap(Base):
    statement: str
    test_id: str
    closure_state: Literal["open", "partial", "undecided"]
    partial_hits: tuple[str, ...] = ()
    synthetic_hits: tuple[str, ...] = ()
    lexical_state: str = ""          # S1: the old lexical test's result, kept for comparison only
    judge_model: str = ""
    judge_reason: str = ""
    judge_prompt_sha256: str = ""
    judge_retrieved_a: int = 0
    judge_retrieved_s: int = 0
    judge_dropped_ids: int = 0
    sibling: Sibling = Sibling()


class Hypothesis(Base):
    text: str
    label: Literal["inferred"] = "inferred"
    predicted_knowledge_type: tuple[KnowledgeType, ...]
    predicted_tacitness: tuple[Tacitness, ...]
    channel: str


class Confidence(Base):
    score: int
    A: int
    B: int
    P: int
    Q: int = 0
    breadth: Literal["broad", "moderate", "narrow"]
    robustness: str
    k_step: int
    k_topic: int


class AlternativeOut(Base):
    text: str
    live: bool
    why: str


class QuestionOut(Base):
    text: str
    target_claim_ids: tuple[str, ...]
    channel: str
    weak_channel: bool


class Record(Base):
    gap_id: str
    lens: str | None
    category: Category
    anchor: str
    observed_evidence: tuple[EvidenceItem, ...]
    inferred_gap: InferredGap
    hypothesis: Hypothesis | None
    reasoning: str
    missing: str
    confidence: Confidence
    alternatives: tuple[AlternativeOut, ...]
    question: QuestionOut | None
    rank: int | None = None
    merged_from: tuple[str, ...] = ()


def make_gap_id(config_sha: str, ledger_sha: str, lens_name: str, seeds) -> str:
    """`"g-" + sha256(config_sha256 | ledger_sha256 | lens | sorted seed claim_ids)[:12]` (§4)."""
    parts = [config_sha, ledger_sha, lens_name, *sorted(seeds)]
    digest = hashlib.sha256("\x1f".join(parts).encode()).hexdigest()
    return f"g-{digest[:12]}"


def categorize(closure_state: str, k_topic: int) -> Category:
    # Fix 1: `undecided` (malformed judge JSON, or a cited id that could not be resolved) is not
    # a hypothesis and never falls through to "open" -- it gets its own retrieval-gap category,
    # routed for a re-judge or a manual inspection, never an expert question.
    if closure_state == "undecided":
        return "RG-UNDECIDED"
    if closure_state == "synthetic-closed":
        return "RG-UNVER"
    return "HYP" if k_topic >= 2 else "RG-SINGLE"


def confidence_rubric(k_topic: int, k_step: int, partial: bool,
                      promo_penalty: bool = False) -> tuple[int, int, int, int, int, str]:
    """`score = A + B - P - Q` (§5, F6's promo penalty). F3: the level is renamed `breadth` and
    is never "high" -- `broad` is decided directly by breadth (k_topic, k_step), not by score,
    since ranking among open gaps is deliberately by breadth of the attested explicit side, not
    by a calibrated confidence (there is no gold to calibrate against, §5)."""
    a = 0 if k_topic <= 1 else 1 if k_topic == 2 else 2 if k_topic <= 4 else 3
    b = 1 if k_step >= 2 else 0
    p = 1 if partial else 0
    q = 1 if promo_penalty else 0
    score = a + b - p - q
    if k_topic >= config.BREADTH_BROAD_K_TOPIC_MIN and k_step >= config.BREADTH_BROAD_K_STEP_MIN:
        breadth = "broad"
    elif score >= config.BREADTH_MODERATE_SCORE_MIN:
        breadth = "moderate"
    else:
        breadth = "narrow"
    return a, b, p, q, score, breadth


def robustness(primary: lenses.Candidate, category: Category,
               settings_results: list[list[tuple[lenses.Candidate, Category]]]) -> int:
    """How many of the 4 robustness settings (§1.4) reproduce this record: same lens and
    category, and the same anchor (DISC) or an X-Jaccard of at least `ROBUSTNESS_JACCARD`."""
    count = 0
    for results in settings_results:
        for cand, cat in results:
            if cand.lens != primary.lens or cat != category:
                continue
            same = (cand.anchor == primary.anchor if primary.lens == "DISC"
                    else link.jaccard(cand.x_a, primary.x_a) >= config.ROBUSTNESS_JACCARD)
            if same:
                count += 1
                break
    return count


def _evidence_item(ledger: Ledger, cid: str, role: str) -> EvidenceItem | None:
    c = ledger.by_id[cid]
    lab = ledger.label(cid)
    pool_a = lab in CRITERION_LABELS
    ev = c.supporting[0] if c.supporting else (c.evidence[0] if c.evidence else None)
    if ev is None:
        return None
    return EvidenceItem(
        claim_id=cid, epistemic_label=lab, knowledge_type=c.knowledge_type,
        area_id=ledger.area_of(cid), source_identifier=ev.source.identifier,
        independence_key=ev.source.independence_key, source_kind=ev.source.kind,
        verdict=ev.verification.verdict, span=ev.selector.exact, role=role,
        counts_as_attestation=pool_a, flag=None if pool_a else "unverified-synthetic")


def _build_evidence(ledger: Ledger, cand: lenses.Candidate,
                    outcome: "semantic.JudgeOutcome") -> tuple[EvidenceItem, ...]:
    items: dict[str, EvidenceItem | None] = {}
    for cid in cand.seeds:
        items[cid] = _evidence_item(ledger, cid, "seed")
    for cid in cand.rivals - cand.seeds:
        items.setdefault(cid, _evidence_item(ledger, cid, "rival"))
    for cid in cand.x_a - cand.seeds - cand.rivals:
        items.setdefault(cid, _evidence_item(ledger, cid, "topic"))
    for cid in (*outcome.partial_hits, *outcome.synthetic_hits):
        items.setdefault(cid, _evidence_item(ledger, cid, "closure_near"))
    return tuple(v for k in sorted(items) if (v := items[k]) is not None)


def _plural(n: int, word: str) -> str:
    return f"{n} {word}" if n == 1 else f"{n} {word}s"


_JUDGE_LABEL = f"{config.JUDGE_MODEL}, local"


def _statement(cand: lenses.Candidate, outcome: "semantic.JudgeOutcome") -> str:
    """S1: "Of N verified sentences retrieved on this topic, the closure judge (<model>, local)
    found none stating <missing>. Re-runnable: prompt sha <sha>." -- replaces the earlier claim-
    count wording (defect 4) now that a candidate's state comes from retrieval, not `|X|`."""
    n_a = outcome.retrieved_n_a
    if outcome.state == "undecided":
        # Fix 1: never phrased as a finding about the sources -- this is a report about the judge
        # call itself (malformed JSON, or a cited id outside the offered sentence numbers).
        return (f"Of {_plural(n_a, 'verified sentence')} retrieved on this topic, the closure "
               f"judge ({_JUDGE_LABEL}) gave an unusable answer ({outcome.reason or 'no reason given'}) "
               f"-- re-judge or inspect manually, rather than treat this as open. "
               f"Re-runnable: prompt sha {outcome.prompt_sha256[:12]}.")
    lead = f"Of {_plural(n_a, 'verified sentence')} retrieved on this topic, the closure judge ({_JUDGE_LABEL})"
    if outcome.state == "partial":
        finding = f"found only a partial statement of {cand.missing}"
    elif outcome.state == "synthetic-closed":
        finding = (f"found none stating {cand.missing} among the verified sentences retrieved "
                  f"({_plural(outcome.retrieved_n_s, 'unverified sentence')} considered separately)")
    else:
        finding = f"found none stating {cand.missing}"
    return f"{lead} {finding}. Re-runnable: prompt sha {outcome.prompt_sha256[:12]}."


def build_record(ledger: Ledger, ledger_sha: str, cand: lenses.Candidate,
                 outcome: "semantic.JudgeOutcome", category: Category, r: int) -> Record:
    k_step = len(link.breadth(ledger, cand.seeds))
    k_topic = len(link.breadth(ledger, cand.x_a))
    partial = outcome.state == "partial"
    a, b, p, q, score, breadth = confidence_rubric(k_topic, k_step, partial, cand.promo_penalty)
    conf = Confidence(score=score, A=a, B=b, P=p, Q=q, breadth=breadth, robustness=f"{r}/4",
                      k_step=k_step, k_topic=k_topic)
    closure_state = "undecided" if outcome.state == "undecided" else ("partial" if partial else "open")
    ig = InferredGap(statement=_statement(cand, outcome), test_id=cand.test_id,
                     closure_state=closure_state,
                     partial_hits=outcome.partial_hits, synthetic_hits=outcome.synthetic_hits,
                     lexical_state=cand.lexical_state, judge_model=outcome.model_id,
                     judge_reason=outcome.reason, judge_prompt_sha256=outcome.prompt_sha256,
                     judge_retrieved_a=outcome.retrieved_n_a, judge_retrieved_s=outcome.retrieved_n_s,
                     judge_dropped_ids=outcome.dropped_ids)
    hyp, q_out = None, None
    if category == "HYP":
        hyp = Hypothesis(text=cand.hypothesis_text, predicted_knowledge_type=cand.predicted_knowledge_type,
                         predicted_tacitness=cand.predicted_tacitness, channel=cand.channel)
        q_out = QuestionOut(text=cand.question_text, target_claim_ids=cand.question_targets,
                            channel=cand.channel, weak_channel=cand.weak_channel)
    # F5: reasoning must not assert a fact about sources ("none states X"); use the inferred-gap
    # wording, which is explicitly qualified to what was actually searched and re-runnable.
    reasoning = (f"{k_step} key(s) state {cand.anchor}; {k_topic} key(s) discuss the topic; the "
                f"closure judge found no verified sentence matching test {cand.test_id}")
    alts = tuple(AlternativeOut(text=a_.text, live=a_.live, why=a_.why) for a_ in cand.alternatives)
    return Record(gap_id=make_gap_id(config.CONFIG_SHA256, ledger_sha, cand.lens, cand.seeds),
                 lens=cand.lens, category=category, anchor=cand.anchor,
                 observed_evidence=_build_evidence(ledger, cand, outcome), inferred_gap=ig, hypothesis=hyp,
                 reasoning=reasoning, missing=cand.missing, confidence=conf, alternatives=alts,
                 question=q_out)


_RG_UNK_FINDING = {"unknown": "nothing found", "thin": "only thin coverage found",
                   "unverified": "found but unverified"}


def _area_name(ledger: Ledger, area_id: str | None) -> str | None:
    if not area_id:
        return None
    return next((a.name for a in ledger.areas if a.area_id == area_id), area_id)


def _with_area(main: str, area_name: str | None) -> str:
    """Defect 6: a readable heading ("... — area: <name>"), never a raw area_id; render.py's
    RG-UNK table (§3) splits this back into (slot/question, area) columns on the same separator."""
    return f"{main} — area: {area_name}" if area_name else main


def unk_gaps(ledger: Ledger, index: link.Index, sidecar: dict | None, ledger_sha: str) -> list[Record]:
    """RG-UNK (§3): ledger U claims, plus sidecar slots not fully covered."""
    out = []
    zero_conf = Confidence(score=0, A=0, B=0, P=0, Q=0, breadth="narrow", robustness="0/4", k_step=0, k_topic=0)
    for cid in sorted(index.u_ids):
        c = ledger.by_id[cid]
        area_name = _area_name(ledger, ledger.area_of(cid))
        ig = InferredGap(statement=f"Ledger {ledger_sha[:8]} claim {cid} ({c.knowledge_type}) is a slot "
                                  f"probe with nothing found in the ledger.",
                         test_id=f"RG-UNK:{cid}", closure_state="open")
        out.append(Record(gap_id=make_gap_id(config.CONFIG_SHA256, ledger_sha, "RG-UNK", (cid,)),
                          lens=None, category="RG-UNK", anchor=_with_area(c.assertion, area_name),
                          observed_evidence=(), inferred_gap=ig, hypothesis=None,
                          reasoning="a ledger U claim: sought (a recorded search) and not found",
                          missing="", confidence=zero_conf, alternatives=(), question=None))
    for slot in (sidecar or {}).get("slots", ()):
        status = slot.get("status")
        if status not in ("unknown", "thin", "unverified"):
            continue
        area_id, probe = slot.get("area_id", ""), slot.get("probe", "")
        area_name = _area_name(ledger, area_id)
        key = f"{area_id}|{probe}|{status}"
        claim_ids = tuple(sorted(slot.get("claim_ids") or ()))
        finding = _RG_UNK_FINDING.get(status, status)
        anchor = _with_area(f"{probe} slot searched, {finding}", area_name)
        ig = InferredGap(statement=f"Sidecar slot '{probe}' in area {area_name or area_id} of ledger "
                                  f"{ledger_sha[:8]} is {status} ({len(claim_ids)} claim(s)).",
                         test_id=f"RG-UNK:slot:{key}", closure_state="open")
        ev = tuple(e for cid in claim_ids if (e := _evidence_item(ledger, cid, "topic")) is not None)
        out.append(Record(gap_id=make_gap_id(config.CONFIG_SHA256, ledger_sha, "RG-UNK", (key,)),
                          lens=None, category="RG-UNK", anchor=anchor,
                          observed_evidence=ev, inferred_gap=ig, hypothesis=None,
                          reasoning=f"a sidecar slot: {status}", missing="", confidence=zero_conf,
                          alternatives=(), question=None))
    return out


@dataclass(frozen=True)
class GapMapResult:
    """The whole run's output: what `__main__.py` writes and `render.py` reads."""

    domain: str
    ledger_sha256: str
    config_sha256: str
    admissible: bool
    admissibility_note: str | None
    map: list[Record]
    retrieval_gaps: list[Record]
    check_data: dict


def to_json_dict(res: GapMapResult) -> dict:
    return {
        "domain": res.domain,
        "ledger_sha256": res.ledger_sha256,
        "config_sha256": res.config_sha256,
        "admissible": res.admissible,
        "admissibility_note": res.admissibility_note,
        "map": [r.model_dump(mode="json") for r in res.map],
        "retrieval_gaps": [r.model_dump(mode="json") for r in res.retrieval_gaps],
        "checks": res.check_data,
    }
