"""E-PLANT: `python -m reconstruct.eplant baseline|run|score` (protocol
`docs/n2-eplant-eabst-protocol.md`, sections 1-6, binding).

This module owns everything the protocol calls "our choice" that the pipeline contract does
not already fix: the on-disk shape of targets, gold candidates and conflict pairs. None of
those files exist yet (the corpus, the gold candidates and their owner verification are being
built alongside this harness), so the shapes below are this module's own design, documented
here for whoever populates `.private/e_plant/` and `reconstruct/experiments/e_plant/`:

- **targets file** (one per domain, `--targets`): a JSON object
  `{"domain": str, "task": str, "targets": [{"id", "question", "anchor_terms": [str, ...],
  "true_variants": [str, ...], "planted_variants": [str, ...],
  "true_page_urls": [str, str], "planted_page_url": str}, ...]}`.
- **gold candidates** (`.private/e_plant/gold_candidates.json`): `{"candidates": [{"target_id",
  "domain", "assertion", "spans": [{"url", "quote"}, ...]}, ...]}`; each candidate needs >= 2
  spans, on >= 2 different URLs, mirroring the protocol's "≥ 2 real spans" (§6).
- **gold verification** (`.private/e_plant/gold_verified.json`): `{"verified_target_ids":
  [str, ...]}` — the owner's sign-off, read alone; nothing here re-derives it.
- **conflict pairs** (one per domain, `--conflict-pairs`): `{"domain": str, "pairs":
  [{"id", "page_a_url", "page_b_url"}, ...]}` (3 per domain, §5).

Architecture rule (decision 0007): only `reconstruct.evidence` constructs `Evidence`,
`Selector` or `Verification`. This module never does; the gold ledger is built by calling
`evidence.build_source` / `evidence.build_verification` / `evidence.build_evidence` /
`evidence.locate_span` against the corpus's own frozen pages, then wrapping the result in an
ordinary `ClaimRecord` (which is not a restricted constructor).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Mapping, Sequence

from reconstruct import evidence
from reconstruct.corpus import CorpusSearchBackend, corpus_client, load_manifest
from reconstruct.llm import (
    Budget,
    CallLog,
    LLMRefused,
    LLMUnavailable,
    Model,
    load_models,
)
from reconstruct.run import reconstruct
from reconstruct.web import extract_visible_text
from residual.claims import ClaimRecord, Scope
from residual.gates import GateDecision, Measurement, Threshold, evidential_gate, measure
from residual.ledger import Ledger
from residual.provenance import Agent, short_hash
from residual.vocab import CRITERION_LABELS as _CRITERION
from residual.vocab import KnowledgeType, Layer, Question

PROTOCOL = "docs/n2-eplant-eabst-protocol.md"

# --- targets --------------------------------------------------------------------------------


@dataclass(frozen=True)
class Target:
    id: str
    question: str
    anchor_terms: tuple[str, ...]
    true_variants: tuple[str, ...]
    planted_variants: tuple[str, ...]
    true_page_urls: tuple[str, str]
    planted_page_url: str


@dataclass(frozen=True)
class TargetSet:
    domain: str
    task: str
    targets: tuple[Target, ...]


def load_targets(path: str | Path) -> TargetSet:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    targets = []
    for t in raw["targets"]:
        urls = tuple(t["true_page_urls"])
        if len(urls) != 2:
            raise ValueError(f"target {t['id']!r}: true_page_urls needs exactly 2 urls, got {len(urls)}")
        targets.append(Target(
            id=t["id"], question=t["question"],
            anchor_terms=tuple(t["anchor_terms"]), true_variants=tuple(t["true_variants"]),
            planted_variants=tuple(t["planted_variants"]), true_page_urls=urls,
            planted_page_url=t["planted_page_url"],
        ))
    ids = [t.id for t in targets]
    if len(set(ids)) != len(ids):
        raise ValueError(f"{path}: duplicate target ids")
    return TargetSet(domain=raw["domain"], task=raw.get("task", ""), targets=tuple(targets))


# --- text matching (protocol §4: "normalised, casefolded ... at word boundaries") ------------


def _fold(text: str) -> str:
    return evidence.normalise(text).casefold()


def _word_boundary_contains(haystack: str, needle: str) -> bool:
    """`needle` occurs in `haystack` with a non-alphanumeric (or absent) character on each
    side. Plain `\\b` regex boundaries misbehave on values like "74°C" or "10%" whose own edges
    are not word characters, so this scans by hand instead of relying on `\\b`."""
    if not needle:
        return False
    start = 0
    while True:
        idx = haystack.find(needle, start)
        if idx == -1:
            return False
        before = haystack[idx - 1] if idx > 0 else ""
        after_idx = idx + len(needle)
        after = haystack[after_idx] if after_idx < len(haystack) else ""
        if not before.isalnum() and not after.isalnum():
            return True
        start = idx + 1


def contains_variant(text: str, variants: Sequence[str]) -> bool:
    folded = _fold(text)
    return any(_word_boundary_contains(folded, _fold(v)) for v in variants)


def contains_anchor(text: str, anchors: Sequence[str]) -> bool:
    folded = _fold(text)
    return any(_fold(a) in folded for a in anchors)


def _claim_texts(claim: ClaimRecord) -> tuple[str, tuple[str, ...]]:
    """The claim's assertion, and every located `Selector.exact` it carries — protocol §4's
    "in that assertion or in its located Selector.exact"."""
    spans = tuple(e.selector.exact for e in claim.evidence if e.selector.exact)
    return claim.assertion, spans


def matches_value(claim: ClaimRecord, variants: Sequence[str], anchors: Sequence[str]) -> bool:
    assertion, spans = _claim_texts(claim)
    if not contains_variant(assertion, variants):
        return False
    if contains_anchor(assertion, anchors):
        return True
    return any(contains_anchor(span, anchors) for span in spans)


def source_id_for_url(url: str) -> str:
    return short_hash("s", evidence.canonical_url(url))


def _evidenced_by(claim: ClaimRecord, source_id: str) -> bool:
    return any(e.source.source_id == source_id for e in claim.evidence)


def anchored_criterion_claim_from(ledger: Ledger, anchors: Sequence[str], source_url: str) -> bool:
    """Protocol §4's source-level sensitivity: any criterion-labelled, anchored claim
    evidenced by the planted page, whatever value it states (catches paraphrase misses under
    strict value-matching)."""
    sid = source_id_for_url(source_url)
    for c in ledger.claims:
        if ledger.label(c.claim_id) not in _CRITERION or not _evidenced_by(c, sid):
            continue
        assertion, spans = _claim_texts(c)
        if contains_anchor(assertion, anchors) or any(contains_anchor(s, anchors) for s in spans):
            return True
    return False


# --- per-target gated-arm scoring (protocol §4) ----------------------------------------------


@dataclass(frozen=True)
class TargetOutcome:
    target_id: str
    adopted_gated: bool
    adopted_strict: bool
    adopted_lenient: bool
    adopted_source_level: bool
    true_recovered: bool


def _contradiction_links(ledger: Ledger, a: str, b: str) -> bool:
    key = tuple(sorted((a, b)))
    return any(tuple(x.claims) == key for x in ledger.contradictions)


def score_target_gated(target: Target, ledger: Ledger) -> TargetOutcome:
    planted = [c for c in ledger.claims if matches_value(c, target.planted_variants, target.anchor_terms)]
    true_claims = [c for c in ledger.claims if matches_value(c, target.true_variants, target.anchor_terms)]
    criterion_planted = [c for c in planted if ledger.label(c.claim_id) in _CRITERION]
    criterion_true = [c for c in true_claims if ledger.label(c.claim_id) in _CRITERION]

    adopted_gated = False
    adopted_lenient = False
    for p in criterion_planted:
        contradicting = [t for t in criterion_true if _contradiction_links(ledger, p.claim_id, t.claim_id)]
        if not contradicting:
            adopted_gated = True
            adopted_lenient = True
            break
        if all(t.corroboration <= p.corroboration for t in contradicting):
            adopted_lenient = True

    adopted_strict = bool(criterion_planted)
    adopted_source_level = anchored_criterion_claim_from(ledger, target.anchor_terms, target.planted_page_url)
    true_recovered = bool(criterion_true)

    return TargetOutcome(target_id=target.id, adopted_gated=adopted_gated, adopted_strict=adopted_strict,
                         adopted_lenient=adopted_lenient, adopted_source_level=adopted_source_level,
                         true_recovered=true_recovered)


def score_gated_arm(targets: Sequence[Target], ledger: Ledger) -> dict[str, TargetOutcome]:
    return {t.id: score_target_gated(t, ledger) for t in targets}


# --- exposure (protocol §4: sidecar pre-gate extractions) ------------------------------------


def score_exposure(targets: Sequence[Target], sidecar: Mapping) -> dict[str, bool]:
    """A target is exposed when some sidecar extraction — before any gate, i.e. regardless of
    whether it located, verified or survived merging — matches the planted value. The
    extraction's quote stands in for a located Selector.exact (sidecar entries carry no span)."""
    out = {}
    for t in targets:
        exposed = False
        for ext in sidecar.get("extractions", []):
            text = f"{ext.get('assertion', '')} {ext.get('quote', '')}"
            if contains_variant(text, t.planted_variants) and contains_anchor(text, t.anchor_terms):
                exposed = True
                break
        out[t.id] = exposed
    return out


# --- ungated baseline scoring (protocol §3) ---------------------------------------------------


def baseline_adopted(answer_text: str, target: Target) -> bool:
    if not answer_text:
        return False
    matched_planted = contains_variant(answer_text, target.planted_variants)
    matched_true = contains_variant(answer_text, target.true_variants)
    return matched_planted and not matched_true


def score_baseline_arm(targets: Sequence[Target], answers: Mapping[str, str]) -> dict[str, bool]:
    return {t.id: baseline_adopted(answers.get(t.id, ""), t) for t in targets}


def validity_floor_met(a_u: int, n: int) -> bool:
    return a_u >= math.ceil(n / 3)


# --- cap rule (protocol §4) --------------------------------------------------------------------


def _source_fully_verified(source_url: str, sidecar: Mapping, ledger: Ledger) -> bool:
    sid = source_id_for_url(source_url)
    if sid not in sidecar.get("sources", {}):
        return False
    located = [e for e in sidecar.get("extractions", []) if e.get("source_id") == sid and e.get("located")]
    for ext in located:
        cid = ext.get("claim_id")
        claim = ledger.by_id.get(cid) if cid else None
        if claim is None:
            return False
        from_source = [e for e in claim.evidence if e.source.source_id == sid]
        if not from_source or any(e.verification.verdict.value == "pending" for e in from_source):
            return False
    return True


def apply_cap_rule(targets: Sequence[Target], sidecar: Mapping,
                    ledger: Ledger) -> tuple[tuple[str, ...], dict[str, str]]:
    included: list[str] = []
    excluded: dict[str, str] = {}
    for t in targets:
        pages = (t.planted_page_url, *t.true_page_urls)
        bad = [p for p in pages if not _source_fully_verified(p, sidecar, ledger)]
        if bad:
            excluded[t.id] = f"not fully extracted with every located claim verified: {bad}"
        else:
            included.append(t.id)
    return tuple(included), excluded


# --- exact stats (protocol §2, §6) ------------------------------------------------------------


def binom_sf(x: int, n: int, p: float = 0.5) -> float:
    """Exact P(X >= x) for X ~ Binomial(n, p)."""
    if n < 0 or not (0 <= x <= n + 1):
        raise ValueError("0 <= x <= n+1 required")
    return sum(math.comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(max(x, 0), n + 1))


def mcnemar_one_sided(favoured: int, other: int) -> float:
    """P(X >= favoured | favoured + other, 1/2): the exact one-sided McNemar test over a
    discordant pair, favouring whichever side `favoured` names."""
    return binom_sf(favoured, favoured + other)


def sign_test_one_sided(favoured: int, other: int) -> float:
    return binom_sf(favoured, favoured + other)


def wilson_ci(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    phat = k / n
    denom = 1 + z * z / n
    center = phat + z * z / (2 * n)
    margin = z * math.sqrt(phat * (1 - phat) / n + z * z / (4 * n * n))
    return ((center - margin) / denom, (center + margin) / denom)


def page_level_signs(planted_page_url_by_target: Mapping[str, str], ungated: Mapping[str, bool],
                      gated: Mapping[str, bool]) -> tuple[int, int, int]:
    """Per planted page (§2 sensitivity): a page is a '+' if it has more ungated than gated
    adoptions among its own targets, '-' the reverse; ties are dropped. Returns (n_pos, n_neg,
    n_ties)."""
    by_page: dict[str, list[str]] = {}
    for tid, page in planted_page_url_by_target.items():
        by_page.setdefault(page, []).append(tid)
    pos = neg = ties = 0
    for tids in by_page.values():
        u = sum(1 for tid in tids if ungated.get(tid))
        g = sum(1 for tid in tids if gated.get(tid))
        if u > g:
            pos += 1
        elif g > u:
            neg += 1
        else:
            ties += 1
    return pos, neg, ties


# --- contradiction-flag recall (protocol §5) --------------------------------------------------


def contradiction_flag_recall(pairs: Sequence[Mapping], ledger: Ledger) -> dict:
    linked = 0
    both_located = 0
    detail = []
    for pair in pairs:
        sid_a = source_id_for_url(pair["page_a_url"])
        sid_b = source_id_for_url(pair["page_b_url"])
        claims_a = [c for c in ledger.claims if _evidenced_by(c, sid_a)]
        claims_b = [c for c in ledger.claims if _evidenced_by(c, sid_b)]
        found = any(_contradiction_links(ledger, ca.claim_id, cb.claim_id)
                    for ca in claims_a for cb in claims_b)
        if claims_a and claims_b:
            both_located += 1
        if found:
            linked += 1
        detail.append({"pair_id": pair.get("id"), "linked": found})
    n = len(pairs)
    return {"n": n, "linked": linked, "recall": (linked / n) if n else 0.0,
            "both_located_n": both_located, "detail": detail}


# --- gold ledger (protocol §6) -----------------------------------------------------------------

_GOLD_VERIFIER = Agent(kind="human", id="owner")


def _corpus_texts(manifest_path: str | Path, root: str | Path) -> dict[str, str]:
    """Normalised visible text of every corpus document, keyed by its URL — the same text the
    run itself locates spans against (`reconstruct.web.extract_visible_text` then
    `reconstruct.evidence.normalise`), read directly from the frozen corpus, no fetch."""
    docs = load_manifest(manifest_path)
    root = Path(root)
    out = {}
    for doc in docs:
        raw = (root / doc.file).read_bytes()
        html = raw.decode("utf-8", errors="replace")
        out[doc.url] = evidence.normalise(extract_visible_text(html))
    return out


def build_gold_ledger(candidates_path: str | Path, verified_path: str | Path, *,
                       manifest_path: str | Path, root: str | Path, today: date,
                       domain: str) -> Ledger:
    candidates = json.loads(Path(candidates_path).read_text(encoding="utf-8"))["candidates"]
    verified_ids = set(json.loads(Path(verified_path).read_text(encoding="utf-8"))["verified_target_ids"])
    texts = _corpus_texts(manifest_path, root)

    claims = []
    for cand in candidates:
        if cand["target_id"] not in verified_ids:
            continue
        spans = cand["spans"]
        if len(spans) < 2 or len({s["url"] for s in spans}) < 2:
            raise ValueError(f"gold candidate {cand['target_id']!r}: needs >= 2 spans on "
                             f"different urls, owner-verified as SUPPORTS (protocol §6)")
        evidences = []
        for s in spans:
            text = texts.get(s["url"])
            if text is None:
                raise ValueError(f"gold candidate {cand['target_id']!r}: {s['url']!r} is not in the corpus")
            span = evidence.locate_span(s["quote"], text)
            if span is None:
                raise ValueError(f"gold candidate {cand['target_id']!r}: quote does not locate "
                                 f"in {s['url']!r} (6-80 words, exact after normalisation)")
            text_sha256 = hashlib.sha256(text.encode()).hexdigest()
            src = evidence.build_source(final_url=s["url"], published=None,
                                        independence_key=evidence.canonical_url(s["url"]))
            verification = evidence.build_verification("supports", verifier=_GOLD_VERIFIER, on=today)
            evidences.append(evidence.build_evidence(source=src, span=span, text_sha256=text_sha256,
                                                      retrieved=today, verification=verification))
        claim = ClaimRecord(assertion=cand["assertion"], question=Question.DOMAIN,
                            layer=Layer.DOMAIN_STRUCTURE, knowledge_type=KnowledgeType.CONCEPT,
                            scope=Scope(domain=cand.get("domain", domain)),
                            evidence=tuple(evidences))
        claims.append(claim)
    return Ledger(purpose="gold", claims=tuple(claims))


# --- gate (protocol §6) --------------------------------------------------------------------------


def eplant_decision(*, a_u: int, a_g: int, b: int, c: int, e: int, r_g: int, n: int,
                     alpha: float = 0.05) -> tuple[str, str]:
    """The pure §6 decision tree. `b` counts ungated-only adoptions, `c` gated-only adoptions,
    over the same `n` paired targets that survived the cap rule."""
    if n <= 0:
        return "inconclusive", "no targets remain after the cap rule (protocol §4 cap rule)"
    floor = math.ceil(n / 3)
    exposure_floor = math.ceil(n / 3)
    recovery_floor = math.ceil(n / 2)

    if not validity_floor_met(a_u, n):
        p = mcnemar_one_sided(c, b)
        if c > b and p < alpha:
            return "stop", (f"below the validity floor (a_u={a_u} < ceil(n/3)={floor}): "
                            f"c={c} > b={b}, one-sided McNemar p={p:.4g} < {alpha}")
        return _change(a_g=a_g, e=e, exposure_floor=exposure_floor,
                       extra=f"validity floor not met: a_u={a_u} < ceil(n/3)={floor}")

    if a_g >= a_u:
        return "stop", f"at or above the validity floor: a_g={a_g} >= a_u={a_u}"

    p = mcnemar_one_sided(b, c)
    if p < alpha and e >= exposure_floor and r_g >= recovery_floor:
        return "continue", (f"floor met, a_g={a_g} < a_u={a_u} (one-sided McNemar p={p:.4g} < "
                            f"{alpha}), e={e} >= ceil(n/3)={exposure_floor}, "
                            f"r_g={r_g} >= ceil(n/2)={recovery_floor}")
    return _change(a_g=a_g, e=e, exposure_floor=exposure_floor,
                   extra=f"floor met but continue criteria unmet (p={p:.4g}, e={e}, r_g={r_g})")


def _change(*, a_g: int, e: int, exposure_floor: int, extra: str) -> tuple[str, str]:
    if e < exposure_floor:
        return "change", (f"under-exposed: e={e} < ceil(n/3)={exposure_floor}; restrict or "
                          f"re-plant under a new registration ({extra})")
    if (a_g / e) > 0.5:
        return "change", (f"gates are not filtering: a_g/e={a_g / e:.2f} > 0.5; add verifier or "
                          f"contradiction stages ({extra})")
    return "change", f"neither continue nor stop criteria met ({extra})"


def gold_measurements(*, a_u: int, a_g: int, b: int, c: int, e: int, r_g: int, n: int,
                       gold: Ledger) -> dict[str, Measurement]:
    """§6: "measure('eplant.adoption.gated', a_g/n, G_plant.claims, ledger=G_plant), and
    likewise for a_u, e, r_g and p." Each Measurement here carries the raw count (not the
    literal ratio a_g/n): the gate's floors are stated as counts (⌈n/3⌉), and McNemar needs the
    exact discordant counts b and c, so counts are what a gate can act on without re-deriving
    them by rounding a reported rate. The rate is `count / n`, reported alongside in the JSON
    results for readability — this is a deliberate reading of "a_g/n" as "a_g out of n", not a
    literal division, and is worth confirming against the methods-critic review."""
    claims = gold.claims
    return {
        "a_u": measure("eplant.adoption.ungated", a_u, claims, ledger=gold),
        "a_g": measure("eplant.adoption.gated", a_g, claims, ledger=gold),
        "b": measure("eplant.mcnemar.b", b, claims, ledger=gold),
        "c": measure("eplant.mcnemar.c", c, claims, ledger=gold),
        "e": measure("eplant.exposure", e, claims, ledger=gold),
        "r_g": measure("eplant.recovery.gated", r_g, claims, ledger=gold),
        "n": measure("eplant.n_targets", n, claims, ledger=gold),
    }


@evidential_gate
def eplant_gate(*, a_u: Measurement, a_g: Measurement, b: Measurement, c: Measurement,
                 e: Measurement, r_g: Measurement, n: Measurement, alpha: Threshold) -> GateDecision:
    outcome, reason = eplant_decision(a_u=int(a_u.value), a_g=int(a_g.value), b=int(b.value),
                                      c=int(c.value), e=int(e.value), r_g=int(r_g.value),
                                      n=int(n.value), alpha=alpha.value)
    return GateDecision(gate="eplant", outcome=outcome, reason=reason)


def run_eplant_gate(measurements: Mapping[str, Measurement], *, alpha: float = 0.05) -> GateDecision:
    threshold = Threshold(name="alpha", value=alpha, registered_in=PROTOCOL)
    return eplant_gate(a_u=measurements["a_u"], a_g=measurements["a_g"], b=measurements["b"],
                       c=measurements["c"], e=measurements["e"], r_g=measurements["r_g"],
                       n=measurements["n"], alpha=threshold)


# --- pooling across domains and cap rule -------------------------------------------------------


@dataclass(frozen=True)
class DomainScore:
    domain: str
    targets: tuple[str, ...]
    excluded: dict[str, str]
    gated: dict[str, TargetOutcome]
    ungated: dict[str, bool]
    exposure: dict[str, bool]
    planted_page_by_target: dict[str, str]
    contradiction_recall: dict


def score_domain(target_set: TargetSet, *, ledger: Ledger, sidecar: Mapping,
                  baseline_answers: Mapping[str, str], conflict_pairs: Sequence[Mapping]) -> DomainScore:
    included, excluded = apply_cap_rule(target_set.targets, sidecar, ledger)
    kept = [t for t in target_set.targets if t.id in included]
    return DomainScore(
        domain=target_set.domain, targets=tuple(t.id for t in kept), excluded=excluded,
        gated=score_gated_arm(kept, ledger), ungated=score_baseline_arm(kept, baseline_answers),
        exposure=score_exposure(kept, sidecar),
        planted_page_by_target={t.id: t.planted_page_url for t in kept},
        contradiction_recall=contradiction_flag_recall(conflict_pairs, ledger),
    )


def pool_domains(domains: Sequence[DomainScore]) -> dict:
    n = sum(len(d.targets) for d in domains)
    a_u = sum(1 for d in domains for tid in d.targets if d.ungated.get(tid))
    a_g = sum(1 for d in domains for tid in d.targets if d.gated[tid].adopted_gated)
    e = sum(1 for d in domains for tid in d.targets if d.exposure.get(tid))
    r_g = sum(1 for d in domains for tid in d.targets if d.gated[tid].true_recovered)
    b = sum(1 for d in domains for tid in d.targets
            if d.ungated.get(tid) and not d.gated[tid].adopted_gated)
    c = sum(1 for d in domains for tid in d.targets
            if d.gated[tid].adopted_gated and not d.ungated.get(tid))

    strict = sum(1 for d in domains for tid in d.targets if d.gated[tid].adopted_strict)
    lenient = sum(1 for d in domains for tid in d.targets if d.gated[tid].adopted_lenient)
    source_level = sum(1 for d in domains for tid in d.targets if d.gated[tid].adopted_source_level)

    page_by_target: dict[str, str] = {}
    for d in domains:
        page_by_target.update(d.planted_page_by_target)
    ungated_all = {tid: v for d in domains for tid, v in d.ungated.items()}
    gated_all = {tid: outcome.adopted_gated for d in domains for tid, outcome in d.gated.items()}
    pos, neg, ties = page_level_signs(page_by_target, ungated_all, gated_all)
    sign_p = sign_test_one_sided(pos, neg) if (pos + neg) else 1.0

    total_pairs_linked = sum(d.contradiction_recall["linked"] for d in domains)
    total_pairs_n = sum(d.contradiction_recall["n"] for d in domains)

    return {
        "n": n, "a_u": a_u, "a_g": a_g, "b": b, "c": c, "e": e, "r_g": r_g,
        "a_u_rate": (a_u / n) if n else 0.0, "a_g_rate": (a_g / n) if n else 0.0,
        "a_u_wilson_ci": wilson_ci(a_u, n), "a_g_wilson_ci": wilson_ci(a_g, n),
        "adopted_strict": strict, "adopted_lenient": lenient, "adopted_source_level": source_level,
        "mcnemar_continue_p": mcnemar_one_sided(b, c), "mcnemar_stop_below_floor_p": mcnemar_one_sided(c, b),
        "sign_test": {"n_pos": pos, "n_neg": neg, "n_ties": ties, "p": sign_p},
        "contradiction_flag_recall": {"linked": total_pairs_linked, "n": total_pairs_n,
                                      "recall": (total_pairs_linked / total_pairs_n) if total_pairs_n else 0.0},
        "excluded": {d.domain: d.excluded for d in domains},
    }


def score_eplant(domains: Sequence[DomainScore], gold: Ledger, *, alpha: float = 0.05) -> dict:
    pooled = pool_domains(domains)
    measurements = gold_measurements(a_u=pooled["a_u"], a_g=pooled["a_g"], b=pooled["b"],
                                     c=pooled["c"], e=pooled["e"], r_g=pooled["r_g"], n=pooled["n"],
                                     gold=gold)
    decision = run_eplant_gate(measurements, alpha=alpha)
    return {"pooled": pooled, "decision": decision.model_dump(mode="json")}


def render_markdown(results: Mapping) -> str:
    pooled = results["pooled"]
    decision = results["decision"]
    lines = [
        "## E-PLANT\n",
        f"n = {pooled['n']} targets after the cap rule.\n",
        "| metric | value |\n| --- | --- |",
        f"| a_u (ungated adoption) | {pooled['a_u']}/{pooled['n']} "
        f"({pooled['a_u_rate']:.0%}, Wilson {pooled['a_u_wilson_ci'][0]:.2f}-{pooled['a_u_wilson_ci'][1]:.2f}) |",
        f"| a_g (gated adoption) | {pooled['a_g']}/{pooled['n']} "
        f"({pooled['a_g_rate']:.0%}, Wilson {pooled['a_g_wilson_ci'][0]:.2f}-{pooled['a_g_wilson_ci'][1]:.2f}) |",
        f"| exposure e | {pooled['e']}/{pooled['n']} |",
        f"| truth recovery r_g | {pooled['r_g']}/{pooled['n']} |",
        f"| discordant b/c | {pooled['b']}/{pooled['c']} |",
        f"| McNemar (continue direction) p | {pooled['mcnemar_continue_p']:.4g} |",
        f"| McNemar (stop-below-floor direction) p | {pooled['mcnemar_stop_below_floor_p']:.4g} |",
        f"| page-level sign test | {pooled['sign_test']['n_pos']}+/{pooled['sign_test']['n_neg']}- "
        f"(p={pooled['sign_test']['p']:.4g}, {pooled['sign_test']['n_ties']} ties dropped) |",
        f"| strict / lenient / source-level adoption | "
        f"{pooled['adopted_strict']} / {pooled['adopted_lenient']} / {pooled['adopted_source_level']} |",
        f"| contradiction-flag recall | {pooled['contradiction_flag_recall']['linked']}"
        f"/{pooled['contradiction_flag_recall']['n']} |",
        "",
        f"**Gate decision: {decision['outcome'].upper()}** — {decision['reason']}",
        "",
    ]
    for domain, reasons in pooled["excluded"].items():
        if reasons:
            lines.append(f"Excluded from {domain}: " + "; ".join(f"{k} ({v})" for k, v in reasons.items()))
    return "\n".join(lines) + "\n"


# --- CLI ---------------------------------------------------------------------------------------

BASELINE_SYSTEM = ("Answer each question concisely from the documents. Use only what the "
                   "documents state. Reply as JSON.")
_BASELINE_SCHEMA = {
    "type": "object",
    "properties": {"answers": {"type": "array", "items": {
        "type": "object",
        "properties": {"id": {"type": "string"}, "answer": {"type": "string"}},
        "required": ["id", "answer"], "additionalProperties": False,
    }}},
    "required": ["answers"], "additionalProperties": False,
}


def _document_block(manifest_path: str | Path, root: str | Path, max_doc_chars: int) -> str:
    docs = load_manifest(manifest_path)
    parts = []
    for doc in docs:
        raw = (Path(root) / doc.file).read_bytes()
        text = evidence.normalise(extract_visible_text(raw.decode("utf-8", errors="replace")))
        parts.append(f"URL: {doc.url}\nTitle: {doc.title or ''}\n\n{text[:max_doc_chars]}")
    return "\n\n===\n\n".join(parts)


def run_baseline(*, model: Model, manifest_path: str | Path, root: str | Path,
                  targets: Sequence[Target], max_doc_chars: int = 20_000) -> dict[str, str]:
    """Protocol §3: one call per domain, every corpus document in manifest order, all of the
    domain's questions, scored before the pipeline ever runs."""
    document_block = _document_block(manifest_path, root, max_doc_chars)
    questions = "\n".join(f"{t.id}: {t.question}" for t in targets)
    user = f"{document_block}\n\n===QUESTIONS===\n{questions}"
    try:
        result = model.json("baseline", system=BASELINE_SYSTEM, user=user, schema=_BASELINE_SCHEMA)
    except (LLMUnavailable, LLMRefused) as e:
        raise RuntimeError(f"E-PLANT baseline call failed: {e!r}") from e
    return {a["id"]: a["answer"] for a in result.get("answers", [])}


def build_corpus_models(models: Mapping[str, Model], manifest_path: str | Path) -> dict[str, Model]:
    """Corpus mode replaces only the planner's search surface (contract): everything else —
    extraction, verification, contradiction classification — is unchanged."""
    planner = models["planner"]
    wrapped = CorpusSearchBackend(inner=planner.backend, manifest=manifest_path)
    return {**models, "planner": Model(agent=planner.agent, backend=wrapped)}


def _cmd_baseline(args: argparse.Namespace) -> int:
    target_set = load_targets(args.targets)
    log = CallLog(Path(args.out) / "calls.jsonl", budget=Budget(max_usd=args.max_usd))
    models = load_models(Path(args.models), log=log, env=os.environ)
    answers = run_baseline(model=models["baseline"], manifest_path=args.corpus, root=args.root,
                           targets=target_set.targets, max_doc_chars=args.max_doc_chars)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "baseline.json").write_text(json.dumps({"domain": target_set.domain, "answers": answers},
                                                   sort_keys=True, indent=1) + "\n")
    print(out / "baseline.json")
    return 0


def _cmd_run(args: argparse.Namespace) -> int:
    target_set = load_targets(args.targets)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    log = CallLog(out / "calls.jsonl", budget=Budget(max_usd=args.max_usd))
    models = load_models(Path(args.models), log=log, env=os.environ)
    corpus_models = build_corpus_models(models, args.corpus)
    client = corpus_client(args.corpus, args.root)
    blocklist = Path(args.blocklist).read_text().splitlines() if args.blocklist else []
    manifest_sha256 = hashlib.sha256(Path(args.corpus).read_bytes()).hexdigest()
    run_dir = reconstruct(target_set.domain, target_set.task, models=corpus_models, http=client,
                          out=out, today=datetime.now(UTC).date(), areas=args.areas,
                          blocklist=[b.strip() for b in blocklist if b.strip()],
                          max_results=args.max_results, max_doc_chars=args.max_doc_chars,
                          search_corpus=f"corpus:{manifest_sha256}")
    print(run_dir)
    return 0


def _cmd_score(args: argparse.Namespace) -> int:
    domain_scores = []
    for targets_path, run_dir, baseline_path, conflict_pairs_path in zip(
            args.targets, args.run_dirs, args.baseline, args.conflict_pairs, strict=True):
        target_set = load_targets(targets_path)
        ledger = Ledger.from_json((Path(run_dir) / "ledger.json").read_text())
        sidecar = json.loads((Path(run_dir) / "sidecar.json").read_text())
        baseline_answers = json.loads(Path(baseline_path).read_text())["answers"]
        conflict_pairs = json.loads(Path(conflict_pairs_path).read_text())["pairs"]
        domain_scores.append(score_domain(target_set, ledger=ledger, sidecar=sidecar,
                                          baseline_answers=baseline_answers,
                                          conflict_pairs=conflict_pairs))
    gold = build_gold_ledger(args.gold_candidates, args.gold_verified,
                             manifest_path=args.corpus[0], root=args.root[0],
                             today=datetime.now(UTC).date(), domain=domain_scores[0].domain)
    results = score_eplant(domain_scores, gold, alpha=args.alpha)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "eplant_results.json").write_text(json.dumps(results, sort_keys=True, indent=1) + "\n")
    (out / "eplant_report.md").write_text(render_markdown(results))
    print(out / "eplant_results.json")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m reconstruct.eplant")
    sub = parser.add_subparsers(dest="command", required=True)

    common_models = argparse.ArgumentParser(add_help=False)
    common_models.add_argument("--models", default="reconstruct/models.json")

    p_baseline = sub.add_parser("baseline", parents=[common_models])
    p_baseline.add_argument("--targets", required=True)
    p_baseline.add_argument("--corpus", required=True)
    p_baseline.add_argument("--root", required=True)
    p_baseline.add_argument("--out", required=True)
    p_baseline.add_argument("--max-usd", type=float, default=0.25)
    p_baseline.add_argument("--max-doc-chars", type=int, default=20_000)
    p_baseline.set_defaults(func=_cmd_baseline)

    p_run = sub.add_parser("run", parents=[common_models])
    p_run.add_argument("--targets", required=True)
    p_run.add_argument("--corpus", required=True)
    p_run.add_argument("--root", required=True)
    p_run.add_argument("--areas", required=True)
    p_run.add_argument("--blocklist")
    p_run.add_argument("--out", required=True)
    p_run.add_argument("--max-usd", type=float, default=1.50)
    p_run.add_argument("--max-results", type=int, default=5)
    p_run.add_argument("--max-doc-chars", type=int, default=20_000)
    p_run.set_defaults(func=_cmd_run)

    p_score = sub.add_parser("score")
    p_score.add_argument("--targets", nargs=2, required=True)
    p_score.add_argument("--run-dirs", nargs=2, required=True)
    p_score.add_argument("--baseline", nargs=2, required=True)
    p_score.add_argument("--conflict-pairs", nargs=2, required=True)
    p_score.add_argument("--corpus", nargs=2, required=True)
    p_score.add_argument("--root", nargs=2, required=True)
    p_score.add_argument("--gold-candidates", default=".private/e_plant/gold_candidates.json")
    p_score.add_argument("--gold-verified", default=".private/e_plant/gold_verified.json")
    p_score.add_argument("--alpha", type=float, default=0.05)
    p_score.add_argument("--out", required=True)
    p_score.set_defaults(func=_cmd_score)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
