"""Orchestration: plan -> search -> fetch -> extract -> locate -> independence -> verify ->
decoy -> contradict -> assemble. One way, no agent loop (Data flow). Every construction of
Evidence/Selector/Verification happens inside reconstruct.evidence; this module only calls it.

`out` is the run directory itself (already decided by the caller — the CLI names it
`<utc>-<confighash>` and builds the run's CallLog at `out/calls.jsonl` before any model is
constructed); `reconstruct()` writes into `out` and returns it unchanged.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Mapping, Sequence

import httpx

from reconstruct import evidence
from reconstruct.evidence import Extraction, IndependenceDoc
from reconstruct.llm import (
    Budget,
    BudgetExceeded,
    CallLog,
    LLMRefused,
    LLMUnavailable,
    Model,
    load_models,
    web_search,
)
from reconstruct.report import render_report
from reconstruct.web import FetchFailure, SnapshotStore, fetch
from residual.claims import ClaimRecord, Scope
from residual.ledger import Area, Contradiction, Ledger
from residual.provenance import PENDING, Generation, Search, Verdict, Verification, short_hash
from residual.vocab import CRITERION_LABELS, KnowledgeType, Question

PROMPTS_DIR = Path(__file__).parent / "prompts"
_KNOWLEDGE_TYPES = [k.value for k in KnowledgeType]

PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "areas": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "queries": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["name", "queries"], "additionalProperties": False,
            },
        },
    },
    "required": ["areas"], "additionalProperties": False,
}

EXTRACT_SCHEMA = {
    "type": "object",
    "properties": {
        "claims": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "assertion": {"type": "string"}, "quote": {"type": "string"},
                    "area": {"type": "string"},
                    "knowledge_type": {"type": "string", "enum": _KNOWLEDGE_TYPES},
                    "question": {"type": "string", "enum": ["domain", "performance"]},
                },
                "required": ["assertion", "quote", "area", "knowledge_type", "question"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["claims"], "additionalProperties": False,
}

VERIFY_SCHEMA = {
    "type": "object",
    "properties": {
        "verdict": {"type": "string", "enum": ["supports", "refutes", "insufficient"]},
        "supporting_quote": {"type": "string"},
    },
    "required": ["verdict", "supporting_quote"], "additionalProperties": False,
}

CONTRADICT_SCHEMA = {
    "type": "object",
    "properties": {
        "kind": {"type": "string", "enum": ["genuine", "scope", "temporal", "terminology",
                                             "insufficient", "compatible"]},
        "quote_a": {"type": "string"}, "quote_b": {"type": "string"},
    },
    "required": ["kind", "quote_a", "quote_b"], "additionalProperties": False,
}

DECOY_SCHEMA = {
    "type": "object",
    "properties": {
        "mutated_claim": {"type": "string"},
        "mutation": {"type": "string", "enum": ["number", "negation", "scope"]},
    },
    "required": ["mutated_claim", "mutation"], "additionalProperties": False,
}

_SCHEMAS = {"plan": PLAN_SCHEMA, "extract": EXTRACT_SCHEMA, "verify": VERIFY_SCHEMA,
            "contradict": CONTRADICT_SCHEMA, "decoy": DECOY_SCHEMA}


def _load_prompts() -> dict[str, str]:
    return {name: (PROMPTS_DIR / f"{name}.md").read_text(encoding="utf-8") for name in _SCHEMAS}


def _spec_hashes(prompts: Mapping[str, str]) -> dict[str, str]:
    return {name: evidence.spec_sha256(prompts[name], _SCHEMAS[name]) for name in prompts}


def _is_blocklisted(url: str, blocklist: Sequence[str]) -> bool:
    host = (httpx.URL(url).host or "").casefold()
    low = url.casefold()
    return any(p.casefold() in low or (host and host.endswith(p.casefold())) for p in blocklist)


@dataclass
class _FetchedDoc:
    source_id: str
    canonical_url: str
    final_url: str
    requested_url: str
    raw_sha256: str
    text_sha256: str
    """sha256 of the NORMALISED text — this is what is written to the snapshot store, and
    what every Selector.locator refers to."""
    normalised_text: str
    """The full normalised document text; every span is located and sliced from this."""
    extraction_text: str
    """`normalised_text`, truncated to max_doc_chars — what the extractor actually sees."""
    title: str | None
    publisher: str | None
    published: date | None
    published_field: str | None
    status: int
    content_type: str
    truncated_fraction: float
    area_ids: set[str] = field(default_factory=set)
    searches: dict[str, Search] = field(default_factory=dict)
    spans: list[tuple[int, int]] = field(default_factory=list)


@dataclass
class _Located:
    extraction: Extraction
    doc: _FetchedDoc
    span: evidence.LocatedSpan
    verification: Verification = field(default_factory=lambda: PENDING)


def _search_key(s: Search) -> str:
    return f"{s.corpus}\x1f{s.query}\x1f{s.agent.id}"


def reconstruct(domain: str, task: str, *, models: Mapping[str, Model], http: httpx.Client,
                out: str | Path, today: date, areas: str | Path | None = None,
                blocklist: Sequence[str] = (), max_results: int = 5,
                max_doc_chars: int = 40_000) -> Path:
    run_dir = Path(out)
    run_dir.mkdir(parents=True, exist_ok=True)
    snapshots = SnapshotStore(run_dir / "snapshots")
    scope = Scope(domain=domain, task=task)
    prompts = _load_prompts()
    spec_hashes = _spec_hashes(prompts)

    complete = True
    incomplete_reasons: list[str] = []
    sidecar_areas: list[dict] = []
    sidecar_searches: list[dict] = []
    sidecar_sources: dict[str, dict] = {}
    sidecar_fetch_failures: list[dict] = []
    sidecar_extractions: dict[str, dict] = {}
    """Keyed by Extraction.extraction_id."""
    sidecar_decoys: list[dict] = []
    sidecar_contradictions: list[dict] = []
    slots_sidecar: list[dict] = []

    ledger_areas: list[Area] = []
    ledger_claims: list[ClaimRecord] = []
    ledger_assignments: list[tuple[str, str]] = []
    ledger_contradictions: list[Contradiction] = []
    largest_share = 0.0

    try:
        area_specs, _ = _resolve_areas(models, domain, task, prompts, areas)
        _write_areas_json(run_dir, area_specs)

        area_by_id: dict[str, dict] = {}
        for spec in area_specs:
            area = evidence.build_area(spec["name"], scope)
            area_by_id[area.area_id] = {"area": area, "name": spec["name"], "queries": spec["queries"]}

        fetched: dict[str, _FetchedDoc] = {}
        for area_id, meta in area_by_id.items():
            records, hits = _run_area_queries(models["planner"], meta["queries"], max_results)
            if not any(h.hits for h in hits):
                records2, hits2 = _run_area_queries(models["planner"], meta["queries"], max_results)
                records, hits = records + records2, hits2
            for r in records:
                sidecar_searches.append({"area_id": area_id, **r})
            status = "searched" if any(h.hits for h in hits) else "unsought"
            sidecar_areas.append({"area_id": area_id, "name": meta["name"], "status": status})
            if status == "unsought":
                incomplete_reasons.append(f"area {meta['name']!r}: all searches failed")
                complete = False
                continue
            for h in hits:
                if not h.hits:
                    continue
                search = Search(corpus="web:openrouter-exa", query=h.executed_query, on=h.on,
                                agent=models["planner"].agent)
                for hit in h.hits:
                    if _is_blocklisted(hit.url, blocklist):
                        sidecar_fetch_failures.append({"url": hit.url, "reason": "blocklisted (A11)"})
                        continue
                    canonical = evidence.canonical_url(hit.url)
                    doc = fetched.get(canonical)
                    if doc is None:
                        doc = _fetch_one(hit.url, http=http, snapshots=snapshots,
                                         max_doc_chars=max_doc_chars,
                                         fetch_failures=sidecar_fetch_failures)
                        if doc is None:
                            continue
                        fetched[canonical] = doc
                    doc.area_ids.add(area_id)
                    doc.searches[_search_key(search)] = search

        # --- extract (one call per document; text truncated to max_doc_chars) -----------------
        docs_by_source_id = {d.source_id: d for d in fetched.values()}
        area_docs_extracted: dict[str, bool] = {aid: False for aid in area_by_id}
        accepted: list[Extraction] = []

        for doc in fetched.values():
            raw_claims, ok = _extract_document(models["extractor"], doc, area_by_id, prompts["extract"])
            if ok:
                for aid in doc.area_ids:
                    area_docs_extracted[aid] = True
            for rc in raw_claims:
                area_name, kt, q = rc.get("area", ""), rc.get("knowledge_type"), rc.get("question")
                reject_reason = None
                if evidence.is_question_or_template(rc.get("assertion", ""), area_name):
                    reject_reason = "question or template"
                elif kt not in _KNOWLEDGE_TYPES:
                    reject_reason = "unknown knowledge_type"
                elif q not in ("domain", "performance"):
                    reject_reason = "unknown question"
                if reject_reason is not None:
                    key = short_hash("x", doc.source_id, rc.get("assertion", "").casefold(), rc.get("quote", ""))
                    sidecar_extractions[key] = {
                        "source_id": doc.source_id, "assertion": rc.get("assertion"),
                        "quote": rc.get("quote"), "area": area_name, "knowledge_type": kt,
                        "located": False, "reject_reason": reject_reason, "claim_id": None,
                        "injection_flag": False,
                    }
                    continue
                ext = Extraction(source_id=doc.source_id, assertion=rc["assertion"], quote=rc["quote"],
                                 area_name=area_name, knowledge_type=KnowledgeType(kt), question=Question(q))
                accepted.append(ext)
                sidecar_extractions[ext.extraction_id] = {
                    "source_id": doc.source_id, "assertion": ext.assertion, "quote": ext.quote,
                    "area": area_name, "knowledge_type": kt, "located": False,
                    "reject_reason": None, "claim_id": None, "injection_flag": False,
                }

        # --- locate ------------------------------------------------------------------------
        located_by_extraction: dict[str, _Located] = {}
        injection_flagged_locators: set[str] = set()
        for ext in accepted:
            doc = docs_by_source_id[ext.source_id]
            span = evidence.locate_span(ext.quote, doc.normalised_text)
            entry = sidecar_extractions[ext.extraction_id]
            if span is None:
                entry["located"] = False
                continue
            entry["located"] = True
            entry["injection_flag"] = span.injection_flagged
            doc.spans.append((span.start, span.end))
            located_by_extraction[ext.extraction_id] = _Located(extraction=ext, doc=doc, span=span)
            if span.injection_flagged:
                injection_flagged_locators.add(f"sha256:{doc.text_sha256};char={span.start},{span.end}")

        # --- independence (needs spans; A7) -------------------------------------------------
        ind_docs = [IndependenceDoc(source_id=d.source_id, url=d.final_url, text=d.normalised_text,
                                    spans=tuple(d.spans)) for d in fetched.values()]
        ind_result = evidence.independence_clusters(ind_docs)
        largest_share = evidence.largest_cluster_share(ind_result.key_by_source)

        sources_by_id = {}
        for doc in fetched.values():
            classification = evidence.classify_source(doc.final_url)
            key = ind_result.key_by_source[doc.source_id]
            sources_by_id[doc.source_id] = evidence.build_source(
                final_url=doc.final_url, published=doc.published, independence_key=key)
            sidecar_sources[doc.source_id] = {
                "requested_url": doc.requested_url, "final_url": doc.final_url, "title": doc.title,
                "publisher": doc.publisher,
                "published": doc.published.isoformat() if doc.published else None,
                "published_field": doc.published_field, "modified": None,
                "retrieved_at": today.isoformat(), "status": doc.status, "content_type": doc.content_type,
                "raw_sha256": doc.raw_sha256, "text_sha256": doc.text_sha256,
                "kind": classification.kind.value, "kind_rule": classification.kind_rule,
                "voice": classification.voice.value, "voice_rule": classification.voice_rule,
                "boundary": classification.boundary, "tier": "open",
                "independence_key": key, "independence_reason": ind_result.reason_by_source[doc.source_id],
                "truncated_fraction": doc.truncated_fraction,
            }

        # --- verify (A5; A2's self-verification guard) ---------------------------------------
        verifier = models.get("verifier")
        verifier_available = verifier is not None and verifier.agent.family != models["extractor"].agent.family
        for loc in located_by_extraction.values():
            if loc.span.injection_flagged or not verifier_available:
                continue
            annotated = _annotated_context(loc.doc.normalised_text, loc.span)
            try:
                result = verifier.json("verify", system=prompts["verify"],
                                       user=_verify_user(loc.extraction.assertion, annotated),
                                       schema=VERIFY_SCHEMA)
            except (LLMUnavailable, LLMRefused):  # includes ServedModelMismatch (A13)
                continue
            verdict, quote = result.get("verdict"), result.get("supporting_quote", "")
            if verdict == "supports" and not evidence.quote_in_span(quote, loc.span.exact):
                verdict = "insufficient"
            if verdict in ("supports", "refutes", "insufficient"):
                loc.verification = evidence.build_verification(verdict, verifier=verifier.agent, on=today)

        # --- assemble claims (merge identical assertions, A10) --------------------------------
        merged_list = evidence.merge_extractions(accepted)
        extractor_generation = Generation(agent=models["extractor"].agent, activity="extraction", on=today,
                                          spec_sha256=spec_hashes["extract"])
        claim_ids_per_area_probe: dict[tuple[str, str], list[str]] = {}

        def matched_area(name: str) -> str | None:
            return next((aid for aid, m in area_by_id.items() if m["name"].casefold() == name.casefold()), None)

        for merged in merged_list:
            evidences = []
            searches_for_claim: dict[str, Search] = {}
            for member in merged.members:
                doc = docs_by_source_id[member.source_id]
                for s in doc.searches.values():
                    searches_for_claim[_search_key(s)] = s
                loc = located_by_extraction.get(member.extraction_id)
                if loc is None:
                    continue
                ev = evidence.build_evidence(source=sources_by_id[loc.doc.source_id], span=loc.span,
                                             text_sha256=loc.doc.text_sha256, retrieved=today,
                                             verification=loc.verification)
                evidences.append(ev)

            claim = evidence.build_claim(merged, evidence=tuple(evidences), generation=extractor_generation,
                                         searches=tuple(searches_for_claim.values()), scope=scope)
            ledger_claims.append(claim)
            for member in merged.members:
                sidecar_extractions[member.extraction_id]["claim_id"] = claim.claim_id

            aid = matched_area(merged.area_name)
            if aid is not None:
                ledger_assignments.append((claim.claim_id, aid))
                if merged.knowledge_type in evidence.PROBES:
                    claim_ids_per_area_probe.setdefault((aid, merged.knowledge_type.value), []).append(
                        claim.claim_id)

        claims_by_id_real = {c.claim_id: c for c in ledger_claims}

        # --- UNKNOWN placeholders + slot status (A1, A2) --------------------------------------
        unknown_claim_ids: set[str] = set()
        for area_id, meta in area_by_id.items():
            if _status_of(sidecar_areas, area_id) == "unsought":
                continue
            docs_ok = area_docs_extracted.get(area_id, False)
            lost = False  # per-area truncation-loss detection is out of scope offline (see report)
            area_searches = tuple({_search_key(s): s for d in fetched.values() if area_id in d.area_ids
                                   for s in d.searches.values()}.values())
            for probe in evidence.PROBES:
                claim_ids = claim_ids_per_area_probe.get((area_id, probe.value), [])
                has_criterion = any(claims_by_id_real[cid].label in CRITERION_LABELS for cid in claim_ids)
                verifier_ran_all = verifier_available and all(
                    not any(e.verification.verdict is Verdict.PENDING for e in claims_by_id_real[cid].evidence)
                    for cid in claim_ids)
                status = evidence.slot_status(has_criterion_claim=has_criterion,
                                              docs_fetched_and_extracted=docs_ok,
                                              area_lost_to_truncation=lost,
                                              verifier_ran_on_all_located=verifier_ran_all)
                slots_sidecar.append({"area_id": area_id, "probe": probe.value, "status": status,
                                      "claim_ids": claim_ids})
                if status == "unknown" and area_searches:
                    placeholder = evidence.build_unknown_placeholder(area_name=meta["name"], probe=probe,
                                                                     scope=scope, searches=area_searches)
                    ledger_claims.append(placeholder)
                    ledger_assignments.append((placeholder.claim_id, area_id))
                    unknown_claim_ids.add(placeholder.claim_id)

        assigned_area_ids = {aid for _, aid in ledger_assignments}
        ledger_areas = [meta["area"] for aid, meta in area_by_id.items() if aid in assigned_area_ids]

        # --- decoys (A6) -----------------------------------------------------------------------
        def clean_evidence(claim):
            return next((e for e in claim.evidence if e.selector.exact
                        and e.selector.locator not in injection_flagged_locators), None)

        located_claim_ids = sorted({cid for cid, aid in ledger_assignments
                                    if cid not in unknown_claim_ids
                                    and clean_evidence(claims_by_id_real[cid]) is not None})
        decoy_ids = evidence.select_decoy_sample(located_claim_ids)
        decoy_model = models.get("extractor")
        if verifier_available and decoy_model is not None:
            for cid in decoy_ids:
                claim = claims_by_id_real[cid]
                real_evidence = clean_evidence(claim)
                if real_evidence is None:
                    continue
                try:
                    decoy_result = decoy_model.json(
                        "decoy", system=prompts["decoy"],
                        user=_decoy_user(claim.assertion, real_evidence.selector.exact), schema=DECOY_SCHEMA)
                    verify_result = verifier.json(
                        "verify", system=prompts["verify"],
                        user=_verify_user(decoy_result["mutated_claim"], real_evidence.selector.exact),
                        schema=VERIFY_SCHEMA)
                except (LLMUnavailable, LLMRefused):
                    continue
                false_accept = verify_result.get("verdict") == "supports"
                sidecar_decoys.append({"claim_id": cid, "mutation": decoy_result["mutation"],
                                       "mutated_claim": decoy_result["mutated_claim"],
                                       "verdict": verify_result.get("verdict"), "false_accept": false_accept})

        # --- contradictions (A8) ----------------------------------------------------------------
        contradiction_model = models.get("contradiction")
        if contradiction_model is not None:
            by_area: dict[str, list[tuple[str, str, str]]] = {}
            for cid, aid in ledger_assignments:
                claim = claims_by_id_real.get(cid)
                if claim is None or cid in unknown_claim_ids or not claim.evidence:
                    continue
                ev = claim.evidence[0]
                by_area.setdefault(aid, []).append((cid, ev.source.independence_key, ev.selector.exact or ""))
            for aid, area_claims in by_area.items():
                spans_by_id = {cid: text for cid, _, text in area_claims}
                for cid_a, cid_b in evidence.contradiction_candidates(area_claims):
                    claim_a, claim_b = claims_by_id_real[cid_a], claims_by_id_real[cid_b]
                    span_a, span_b = spans_by_id[cid_a], spans_by_id[cid_b]
                    date_a = claim_a.evidence[0].source.published
                    date_b = claim_b.evidence[0].source.published
                    try:
                        result = contradiction_model.json(
                            "contradict", system=prompts["contradict"],
                            user=_contradict_user(claim_a.assertion, span_a, date_a,
                                                  claim_b.assertion, span_b, date_b),
                            schema=CONTRADICT_SCHEMA)
                    except (LLMUnavailable, LLMRefused):
                        continue
                    kind = result.get("kind")
                    quote_a, quote_b = result.get("quote_a", ""), result.get("quote_b", "")
                    matches = ((evidence.quote_in_span(quote_a, span_a) and evidence.quote_in_span(quote_b, span_b))
                              or (evidence.quote_in_span(quote_a, span_b) and evidence.quote_in_span(quote_b, span_a)))
                    genuine = kind == "genuine" and matches
                    if genuine:
                        ledger_contradictions.append(evidence.build_contradiction(
                            cid_a, cid_b, detected_by=contradiction_model.agent,
                            spec_sha256=spec_hashes["contradict"]))
                    sidecar_contradictions.append({"claims": [cid_a, cid_b], "kind": kind,
                                                   "quote_a": quote_a, "quote_b": quote_b,
                                                   "recorded_in_ledger": genuine})

    except BudgetExceeded as e:
        complete = False
        incomplete_reasons.append(f"budget exceeded: {e}")

    ledger = Ledger(purpose="reconstruction", claims=tuple(ledger_claims),
                    contradictions=tuple(ledger_contradictions), areas=tuple(ledger_areas),
                    assignments=tuple(ledger_assignments))
    assert Ledger.from_json(ledger.to_json()) == ledger

    n_located = sum(1 for c in ledger_claims if c.evidence)
    n_extracted = len(sidecar_extractions)
    n_verified = sum(1 for c in ledger_claims for e in c.evidence
                     if e.verification.verdict is not Verdict.PENDING)
    n_supports = sum(1 for c in ledger_claims for e in c.evidence
                     if e.verification.verdict is Verdict.SUPPORTS)
    label_counts: dict[str, int] = {}
    for c in ledger_claims:
        label_counts[c.label.value] = label_counts.get(c.label.value, 0) + 1
    decoy_rate = (sum(1 for d in sidecar_decoys if d["false_accept"]) / len(sidecar_decoys)
                  if sidecar_decoys else 0.0)

    stats = {
        "n_search_hits": sum(r["n_hits"] for r in sidecar_searches),
        "n_sources_fetched": len(sidecar_sources),
        "n_fetch_failures": len(sidecar_fetch_failures),
        "n_independent_clusters": len({s["independence_key"] for s in sidecar_sources.values()}),
        "largest_cluster_share": largest_share,
        "n_extracted": n_extracted,
        "n_located": n_located,
        "unlocated_rate": (1 - n_located / n_extracted) if n_extracted else 0.0,
        "n_verified": n_verified,
        "n_supports": n_supports,
        "n_claims": len(ledger_claims),
        "label_counts": label_counts,
        "n_contradictions_ledger": len(ledger_contradictions),
        "n_disagreements_other": len(sidecar_contradictions) - len(ledger_contradictions),
        "n_unknown": sum(1 for s in slots_sidecar if s["status"] == "unknown"),
        "n_unverified_slots": sum(1 for s in slots_sidecar if s["status"] == "unverified"),
        "n_unexamined_slots": sum(1 for s in slots_sidecar if s["status"] == "unexamined"),
        "decoy_false_accept_rate": decoy_rate,
        "total_cost_usd": _total_cost(models),
    }

    sidecar = {
        "complete": complete, "incomplete_reasons": incomplete_reasons,
        "config": {
            "domain": domain, "task": task,
            "models": {role: {"model": m.agent.id, "family": m.agent.family} for role, m in models.items()},
            "probes": [p.value for p in evidence.PROBES],
            "probe_sha256": hashlib.sha256(json.dumps(sorted(p.value for p in evidence.PROBES)).encode()).hexdigest(),
            "prompts": spec_hashes, "max_results": max_results, "max_doc_chars": max_doc_chars,
        },
        "areas": sidecar_areas, "searches": sidecar_searches, "sources": sidecar_sources,
        "fetch_failures": sidecar_fetch_failures, "extractions": list(sidecar_extractions.values()),
        "slots": slots_sidecar, "contradictions": sidecar_contradictions, "decoys": sidecar_decoys,
        "stats": stats,
    }

    (run_dir / "ledger.json").write_text(ledger.to_json())
    (run_dir / "sidecar.json").write_text(json.dumps(sidecar, sort_keys=True, indent=1) + "\n")
    (run_dir / "report.md").write_text(render_report(ledger=ledger, sidecar=sidecar))
    return run_dir


def _status_of(sidecar_areas: list[dict], area_id: str) -> str | None:
    return next((a["status"] for a in sidecar_areas if a["area_id"] == area_id), None)


def _total_cost(models: Mapping[str, Model]) -> float:
    seen: set[int] = set()
    total = 0.0
    for m in models.values():
        log = getattr(m.backend, "log", None)
        if log is not None and id(log) not in seen:
            seen.add(id(log))
            total += log.total_cost
    return total


def _resolve_areas(models, domain, task, prompts, areas_path):
    if areas_path is not None:
        data = json.loads(Path(areas_path).read_text())
        return data["areas"], "given"
    result = models["planner"].json("plan", system=prompts["plan"],
                                    user=f"Domain: {domain}\nTask: {task}", schema=PLAN_SCHEMA)
    areas_list = result.get("areas", [])
    if not _valid_plan(areas_list):
        result = models["planner"].json(
            "plan", system=prompts["plan"],
            user=(f"Domain: {domain}\nTask: {task}\n\nYour previous answer was invalid: give "
                  "between 3 and 6 areas, each with 1 to 3 queries, and distinct names."),
            schema=PLAN_SCHEMA)
        areas_list = result.get("areas", [])
        if not _valid_plan(areas_list):
            raise RuntimeError("planner produced invalid areas after one retry (A10)")
    return areas_list, "planner"


def _valid_plan(areas_list: list[dict]) -> bool:
    """3-6 areas with 1-3 queries each is prompt guidance for the planner, not a runtime gate —
    only A10's binding rule (unique names after casefolding) is enforced here, with a retry."""
    if not areas_list:
        return False
    names = [a["name"].casefold() for a in areas_list]
    if len(set(names)) != len(names):
        return False
    return all(a.get("queries") for a in areas_list)


def _write_areas_json(run_dir: Path, areas_list: list[dict]) -> None:
    canonical = json.dumps(areas_list, sort_keys=True)
    payload = {"areas": areas_list, "sha256": hashlib.sha256(canonical.encode()).hexdigest()}
    (run_dir / "areas.json").write_text(json.dumps(payload, sort_keys=True, indent=1) + "\n")


def _run_area_queries(model: Model, queries: Sequence[str], max_results: int):
    records, hits = [], []
    for q in queries:
        try:
            result = web_search(model, q, max_results=max_results)
            records.append({"query": q, "ok": True, "n_hits": len(result.hits), "error": None})
            hits.append(result)
        except (LLMUnavailable, LLMRefused) as e:
            records.append({"query": q, "ok": False, "n_hits": 0, "error": repr(e)})
    return records, hits


def _fetch_one(url: str, *, http: httpx.Client, snapshots: SnapshotStore, max_doc_chars: int,
               fetch_failures: list[dict]) -> _FetchedDoc | None:
    result = fetch(url, client=http)
    if isinstance(result, FetchFailure):
        fetch_failures.append({"url": url, "reason": result.reason})
        return None
    normalised = evidence.normalise(result.text)
    text_sha = snapshots.write_text(normalised)
    canonical = evidence.canonical_url(result.final_url)
    extraction_text = normalised[:max_doc_chars]
    fraction = 0.0 if len(normalised) <= max_doc_chars else (len(normalised) - max_doc_chars) / len(normalised)
    return _FetchedDoc(
        source_id=short_hash("s", canonical), canonical_url=canonical, final_url=result.final_url,
        requested_url=result.requested_url, raw_sha256=result.raw_sha256, text_sha256=text_sha,
        normalised_text=normalised, extraction_text=extraction_text, title=result.metadata.title,
        publisher=result.metadata.publisher, published=result.metadata.published,
        published_field=result.metadata.published_field, status=result.status,
        content_type=result.content_type, truncated_fraction=fraction,
    )


def _extract_document(model: Model, doc: _FetchedDoc, area_by_id: dict, prompt: str) -> tuple[list[dict], bool]:
    areas = ", ".join(m["name"] for m in area_by_id.values())
    kinds = ", ".join(_KNOWLEDGE_TYPES)
    user = (f"Areas: {areas}\nKnowledge types: {kinds}\n\n"
            f"===DOCUMENT===\n{doc.extraction_text}\n===END DOCUMENT===")
    try:
        result = model.json("extract", system=prompt, user=user, schema=EXTRACT_SCHEMA)
    except (LLMUnavailable, LLMRefused):
        return [], False
    return result.get("claims", []), True


def _annotated_context(doc_text: str, span: evidence.LocatedSpan, radius: int = 300) -> str:
    start = max(0, span.start - radius)
    end = min(len(doc_text), span.end + radius)
    return f"{doc_text[start:span.start]}>>>{doc_text[span.start:span.end]}<<<{doc_text[span.end:end]}"


def _verify_user(assertion: str, annotated_context: str) -> str:
    return (f"Claim: {assertion}\n\nContext (the exact span under judgement is marked "
            f">>>like this<<<):\n{annotated_context}")


def _decoy_user(assertion: str, quote: str) -> str:
    return f"Claim: {assertion}\nQuote: {quote}"


def _contradict_user(assertion_a, span_a, date_a, assertion_b, span_b, date_b) -> str:
    return (f"Claim A ({date_a}): {assertion_a}\nSpan A: {span_a}\n\n"
            f"Claim B ({date_b}): {assertion_b}\nSpan B: {span_b}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m reconstruct.run")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--domain", required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--areas")
    parser.add_argument("--blocklist")
    parser.add_argument("--max-usd", type=float, default=1.50)
    parser.add_argument("--max-results", type=int, default=5)
    parser.add_argument("--max-doc-chars", type=int, default=40_000)
    parser.add_argument("--out", default="reconstruct/runs")
    args = parser.parse_args(argv)

    if not args.live:
        print("refusing to run without --live", file=sys.stderr)
        return 2

    blocklist = Path(args.blocklist).read_text().splitlines() if args.blocklist else []
    blocklist = [b.strip() for b in blocklist if b.strip()]

    models_path = Path(__file__).parent.parent.parent / "models.json"
    now = datetime.now(UTC)
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    role_config = json.loads(models_path.read_text())
    confighash = hashlib.sha256(json.dumps(
        {"domain": args.domain, "task": args.task, "models": role_config, "areas": args.areas,
         "blocklist": blocklist, "max_results": args.max_results, "max_doc_chars": args.max_doc_chars},
        sort_keys=True).encode()).hexdigest()[:12]
    run_dir = Path(args.out) / f"{stamp}-{confighash}"
    run_dir.mkdir(parents=True, exist_ok=True)

    log = CallLog(run_dir / "calls.jsonl", budget=Budget(max_usd=args.max_usd))
    models = load_models(models_path, log=log, env=os.environ)

    with httpx.Client() as http:
        result = reconstruct(args.domain, args.task, models=models, http=http, out=run_dir,
                             today=now.date(), areas=args.areas, blocklist=blocklist,
                             max_results=args.max_results, max_doc_chars=args.max_doc_chars)
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
