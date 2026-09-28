"""Markdown rendering of a run: plain and inspectable, not a narrative answer. Reads only the
ledger and the sidecar it is handed — no filesystem access, no model or network calls."""
from __future__ import annotations

from residual.ledger import Ledger
from residual.vocab import EpistemicLabel


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


def _stats_table(sidecar: dict) -> str:
    stats = sidecar["stats"]
    rows = "\n".join(f"| {k} | {v} |" for k, v in sorted(stats.items()) if k != "label_counts")
    labels = "\n".join(f"| {k} | {v} |" for k, v in sorted(stats["label_counts"].items()))
    return (f"## Summary statistics\n\n| metric | value |\n| --- | --- |\n{rows}\n\n"
            f"### Claims by epistemic label\n\n| label | n |\n| --- | --- |\n{labels}\n")


def _area_section(ledger: Ledger, sidecar: dict, area) -> str:
    lines = [f"## Area: {area.name}\n"]
    claims = ledger.in_area(area.area_id)
    supported = [c for c in claims if c.label != EpistemicLabel.UNKNOWN and c.supporting]
    synthetic = [c for c in claims if c.label == EpistemicLabel.SYNTHETIC_EXTRAPOLATION]
    unknown = [c for c in claims if c.label == EpistemicLabel.UNKNOWN]

    lines.append("### Supported claims\n")
    if supported:
        for c in supported:
            ev = c.supporting[0]
            lines.append(f"- {c.assertion}\n  > {ev.selector.exact}\n"
                         f"  ({ev.source.kind.value}, {ev.source.identifier}, published "
                         f"{ev.source.published}, independence {ev.source.independence_key}, "
                         f"corroboration {c.corroboration})")
    else:
        lines.append("- none")

    lines.append("\n### Synthetic / pending claims\n")
    if synthetic:
        for c in synthetic:
            lines.append(f"- {c.assertion} ({'pending' if c.pending else 'no located evidence'})")
    else:
        lines.append("- none")

    lines.append("\n### UNKNOWN / unverified / unexamined slots\n")
    slots = [s for s in sidecar["slots"] if s["area_id"] == area.area_id]
    for s in slots:
        if s["status"] != "covered":
            lines.append(f"- {s['probe']}: {s['status']}")
    if not any(s["status"] != "covered" for s in slots):
        lines.append("- none")

    lines.append("\n### Contradictions and disagreements\n")
    area_claim_ids = {c.claim_id for c in claims}
    contradictions = [x for x in sidecar["contradictions"] if set(x["claims"]) & area_claim_ids]
    if contradictions:
        for x in contradictions:
            lines.append(f"- {x['kind']}: {x['claims']} (in ledger: {x['recorded_in_ledger']})")
    else:
        lines.append("- none")

    lines.append("\n### N1 exclusions\n")
    excluded_any = False
    for c in claims:
        for ev, reason in c.excluded:
            excluded_any = True
            lines.append(f"- {c.assertion}: {reason}")
    if not excluded_any:
        lines.append("- none")

    if unknown:
        lines.append("\n### Unknown placeholders\n")
        for c in unknown:
            lines.append(f"- {c.assertion}")

    return "\n".join(lines) + "\n"


def _sources_section(sidecar: dict) -> str:
    n_sources = len(sidecar["sources"])
    n_supporting = len({s["independence_key"] for s in sidecar["sources"].values()})
    lines = [f"## Sources\n\n{n_sources} sources retrieved; {n_supporting} independence clusters.\n"]
    if sidecar["fetch_failures"]:
        lines.append("\n### Fetch failures\n")
        for f in sidecar["fetch_failures"]:
            lines.append(f"- {f['url']}: {f['reason']}")
    unlocated = [e for e in sidecar["extractions"] if not e["located"] and e["reject_reason"] is None]
    lines.append(f"\n### Unlocated quotes (fabrication rate: {sidecar['stats']['unlocated_rate']:.0%})\n")
    for e in unlocated:
        lines.append(f"- {e['quote'][:80]!r} ({e['source_id']})")
    if not unlocated:
        lines.append("- none")
    return "\n".join(lines) + "\n"


def render_report(*, ledger: Ledger, sidecar: dict) -> str:
    parts = [_headline(sidecar), _stats_table(sidecar)]
    for area in ledger.areas:
        parts.append(_area_section(ledger, sidecar, area))
    parts.append(_sources_section(sidecar))
    return "\n".join(parts)
