"""Markdown rendering of a run: plain and inspectable, not a narrative answer. Reads only the
ledger and the sidecar it is handed — no filesystem access, no model or network calls.

MUST-FIX 7: a rejected claim shows its located span, verdict and drift flags (never "(no located
evidence)" for a claim that has a span); every claim line carries claim_id/knowledge_type/label
so a reader can cross-reference sidecar.json without grep; the raw per-run stats dump and the
"N1 exclusions" section (always empty for World A, REMOVE) are gone, replaced by a compact
headline: sources by fetch outcome, clusters, supported claims by source kind/tier, corroboration
distribution, slots by status (including `thin`), decoy per-type rates with a Wilson 95% CI, and
cost.
"""
from __future__ import annotations

from reconstruct.evidence import wilson_ci
from residual.ledger import Ledger
from residual.vocab import EpistemicLabel

_SLOT_STATUS_ORDER = ("covered", "thin", "unknown", "unverified", "unexamined")


def _extraction_by_claim_id(sidecar: dict) -> dict[str, dict]:
    """The most recently updated extraction record naming this claim_id — good enough for a
    rejected/synthetic claim's single located extraction; a merged claim shows its first
    member's verify record, which is the same for every member after MUST 2's rule anyway when
    the verdict is what mattered (they may differ before the rule is applied, but the ledger's
    own claim.evidence is the source of truth for a supported claim's own display)."""
    by_claim: dict[str, dict] = {}
    for e in sidecar["extractions"]:
        if e["claim_id"]:
            by_claim.setdefault(e["claim_id"], e)
    return by_claim


def _headline(sidecar: dict) -> str:
    complete = "complete" if sidecar["complete"] else "INCOMPLETE"
    stats = sidecar["stats"]
    verifier_family = next(iter({m["family"] for r, m in sidecar["config"]["models"].items()
                                 if r == "verifier"}), None)
    verified_note = (f"{stats['n_verified']} verified" if stats["n_verified"]
                     else f"{stats['n_located']} claims span-located, 0 verified: "
                          "no verifier of another family configured")
    line = (f"# N2a reconstruction report ({complete})\n\n"
            f"{stats['n_located']} claims span-located, {verified_note}, "
            f"decoy false-accept rate {stats['decoy_false_accept_rate']:.0%}, "
            f"cost ${stats['total_cost_usd']:.4f}. Verifier family: {verifier_family or 'none'}.\n")
    if not sidecar["complete"]:
        line += "\nIncomplete reasons:\n" + "\n".join(f"- {r}" for r in sidecar["incomplete_reasons"]) + "\n"
    return line


def _fetch_table(sidecar: dict) -> str:
    reasons: dict[str, int] = {}
    for f in sidecar["fetch_failures"]:
        reasons[f["reason"]] = reasons.get(f["reason"], 0) + 1
    stats = sidecar["stats"]
    lines = ["## Sources and clusters\n",
             "| metric | value |", "| --- | --- |",
             f"| sources fetched | {stats['n_sources_fetched']} |",
             f"| fetch failures | {stats['n_fetch_failures']} |",
             f"| independent clusters | {stats['n_independent_clusters']} |",
             f"| largest cluster share | {stats['largest_cluster_share']:.0%} |"]
    if reasons:
        lines.append("\n**Fetch failures by reason**\n")
        lines += ["| reason | n |", "| --- | --- |"]
        lines += [f"| {reason} | {n} |" for reason, n in sorted(reasons.items(), key=lambda kv: -kv[1])]
    return "\n".join(lines) + "\n"


def _supported_by_kind_tier(ledger: Ledger, sidecar: dict) -> str:
    counts: dict[tuple[str, str], int] = {}
    corroboration_dist: dict[int, int] = {}
    for c in ledger.claims:
        if not c.supporting:
            continue
        corroboration_dist[c.corroboration] = corroboration_dist.get(c.corroboration, 0) + 1
        for e in c.supporting:
            tier = sidecar["sources"].get(e.source.source_id, {}).get("tier", "?")
            key = (e.source.kind.value, tier)
            counts[key] = counts.get(key, 0) + 1
    lines = ["## Supported claims by source kind/tier\n"]
    if counts:
        lines += ["| kind | tier | n supporting-evidence items |", "| --- | --- | --- |"]
        for (kind, tier), n in sorted(counts.items()):
            lines.append(f"| {kind} | {tier} | {n} |")
    else:
        lines.append("- none")
    lines.append("\n### Corroboration distribution (supported claims)\n")
    if corroboration_dist:
        lines += ["| corroboration | n claims |", "| --- | --- |"]
        for k, n in sorted(corroboration_dist.items()):
            lines.append(f"| {k} | {n} |")
    else:
        lines.append("- none")
    return "\n".join(lines) + "\n"


def _slots_table(sidecar: dict) -> str:
    counts: dict[str, int] = {}
    for s in sidecar["slots"]:
        counts[s["status"]] = counts.get(s["status"], 0) + 1
    lines = ["## Slots by status\n", "| status | n |", "| --- | --- |"]
    for status in _SLOT_STATUS_ORDER:
        if counts.get(status):
            lines.append(f"| {status} | {counts[status]} |")
    return "\n".join(lines) + "\n"


def _decoy_table(sidecar: dict) -> str:
    by_type = sidecar["stats"].get("decoy_by_type", {})
    invalid_total = sum(1 for d in sidecar["decoys"] if not d.get("valid", True))
    lines = ["## Decoy false-accept rate by mutation type (Wilson 95% CI)\n",
             "| mutation | attempted | valid | false accepts | rate | 95% CI |",
             "| --- | --- | --- | --- | --- | --- |"]
    for mutation in sorted(by_type):
        t = by_type[mutation]
        valid, false_accept = t["valid"], t["false_accept"]
        rate = (false_accept / valid) if valid else 0.0
        lo, hi = wilson_ci(false_accept, valid)
        lines.append(f"| {mutation} | {t['attempted']} | {valid} | {false_accept} | "
                     f"{rate:.0%} | [{lo:.0%}, {hi:.0%}] |")
    if invalid_total:
        lines.append(f"\n{invalid_total} decoy(s) excluded as invalid (no real change, or no rationale).")
    return "\n".join(lines) + "\n"


def _claim_line(c, sidecar: dict) -> str:
    extraction = _extraction_by_claim_id(sidecar).get(c.claim_id)
    header = f"`{c.claim_id}` [{c.knowledge_type.value}] ({c.label.value}) — {c.assertion}"
    if c.supporting:
        ev = c.supporting[0]
        return (f"- {header}\n  > {ev.selector.exact}\n"
               f"  ({ev.source.kind.value}, {ev.source.identifier}, published "
               f"{ev.source.published}, independence {ev.source.independence_key}, "
               f"corroboration {c.corroboration})")
    if c.evidence and c.evidence[0].selector.exact:
        # Located but not (or no longer) counted as supporting: show the span, verdict and the
        # three drift flags the verifier recorded — never "(no located evidence)" for a claim
        # that has one (MUST-FIX 7; report.py:55 used to mislabel this a fabrication).
        ev = c.evidence[0]
        v = ev.verification
        flag_bits = []
        if extraction:
            for flag_key, label in (("verify_adds_content", "adds_content"),
                                    ("verify_subject_or_scope_differs", "scope_differs"),
                                    ("verify_quantifier_modality_or_connective_differs", "connective_differs")):
                if extraction.get(flag_key):
                    flag_bits.append(label)
        flags_note = f" [{', '.join(flag_bits)}]" if flag_bits else ""
        return (f"- {header}\n  > {ev.selector.exact}\n"
               f"  (verdict {v.verdict.value}{flags_note}, {ev.source.identifier})")
    return f"- {header} (no located evidence)"


def _area_section(ledger: Ledger, sidecar: dict, area) -> str:
    lines = [f"## Area: {area.name}\n"]
    claims = ledger.in_area(area.area_id)
    supported = [c for c in claims if c.label != EpistemicLabel.UNKNOWN and c.supporting]
    rejected = [c for c in claims if c.label != EpistemicLabel.UNKNOWN and not c.supporting]
    unknown = [c for c in claims if c.label == EpistemicLabel.UNKNOWN]

    lines.append("### Supported claims\n")
    lines.append("\n".join(_claim_line(c, sidecar) for c in supported) if supported else "- none")

    lines.append("\n### Synthetic / rejected claims\n")
    lines.append("\n".join(_claim_line(c, sidecar) for c in rejected) if rejected else "- none")

    lines.append("\n### UNKNOWN / thin / unverified / unexamined slots\n")
    slots = [s for s in sidecar["slots"] if s["area_id"] == area.area_id]
    non_covered = [s for s in slots if s["status"] != "covered"]
    if non_covered:
        for s in non_covered:
            lines.append(f"- {s['probe']}: {s['status']}")
    else:
        lines.append("- none")

    if unknown:
        lines.append("\n### Unknown placeholders\n")
        for c in unknown:
            lines.append(f"- `{c.claim_id}` [{c.knowledge_type.value}] — {c.assertion}")

    return "\n".join(lines) + "\n"


def render_report(*, ledger: Ledger, sidecar: dict) -> str:
    parts = [_headline(sidecar), _fetch_table(sidecar), _supported_by_kind_tier(ledger, sidecar),
             _slots_table(sidecar), _decoy_table(sidecar)]
    for area in ledger.areas:
        parts.append(_area_section(ledger, sidecar, area))
    return "\n".join(parts)
