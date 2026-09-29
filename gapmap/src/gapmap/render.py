"""`gapmap.md` (spec §0, §4, §6, §7): a summary block, the ranked map (an index table, then three
tiers per record, never in the indicative for a hypothesis), the control slot, retrieval gaps
(search or verify, never ask an expert) and the §7 checks."""
from __future__ import annotations

from collections import Counter

from gapmap import config, record, text

_RG_ACTION = {"RG-UNVER": "verify", "RG-SIBLING": "verify", "RG-UNDECIDED": "re-judge or inspect"}
_EVIDENCE_TOPIC_CAP = 5
_TABLE_ANCHOR_LIMIT = 60


def _header(res: record.GapMapResult) -> list[str]:
    lines = [f"# Gap map: {res.domain}", "",
            f"- Ledger: `{res.ledger_sha256}`",
            f"- Config: `{res.config_sha256}`"]
    if not res.admissible:
        lines.append(f"- **Admissibility note:** {res.admissibility_note}")
    lines.append("")
    return lines


def _summary_section(res: record.GapMapResult) -> list[str]:
    """§6 item 7: the whole map at a glance before any detail -- HYP by lens and level, RG by
    category, the control slot, and the §7.1 numbers with their flags."""
    hyp = [r for r in res.map if r.category == "HYP"]
    lines = ["## Summary", "", f"- **HYP:** {len(hyp)} total" + ("" if hyp else " (none)")]
    by_lens: dict[str, Counter] = {}
    for r in hyp:
        by_lens.setdefault(r.lens or "\u2014", Counter())[r.confidence.breadth] += 1
    for lens_name in sorted(by_lens):
        levels = by_lens[lens_name]
        breakdown = ", ".join(f"{levels[lvl]} {lvl}" for lvl in ("broad", "moderate", "narrow") if levels[lvl])
        lines.append(f"  - {lens_name}: {sum(levels.values())} ({breakdown})")
    rg_counts = Counter(r.category for r in res.retrieval_gaps)
    rg_parts = [f"{cat} {rg_counts[cat]}"
               for cat in ("RG-UNK", "RG-SINGLE", "RG-UNVER", "RG-SIBLING", "RG-UNDECIDED")
               if rg_counts.get(cat)]
    lines.append(f"- **Retrieval gaps:** {', '.join(rg_parts) if rg_parts else 'none'}")
    control_n = sum(1 for r in res.map if r.category == "CONTROL")
    lines.append(f"- **Control slot:** {control_n}")
    if "promo_excluded" in res.check_data:
        lines.append(f"- **PROMO-excluded seeds (S3 defect 1):** {res.check_data['promo_excluded']}")
    a = res.check_data["anti_renaming"]
    lines.append(f"- **§7.1 anti-renaming:** J10(low)={a['j10_low']:.2f}, J10(high)={a['j10_high']:.2f}, "
                f"\u03c1(score,dens)={a['spearman']:.2f}, flags: "
                f"{', '.join(a['flags']) if a['flags'] else 'none'}")
    lines.append("")
    return lines


def _how_to_read() -> list[str]:
    return [
        "## How to read this map", "",
        "Every record separates three tiers, and they never mix:", "",
        "- **OBSERVED EVIDENCE** — verified verbatim spans from the ledger; what a source actually says.",
        "- **INFERRED GAP** — a statement about the ledger that anyone can re-run: which claims state "
        "the topic and which do not state the missing element.",
        "- **HIDDEN-KNOWLEDGE HYPOTHESIS** — a prediction, labelled `inferred`, never a fact. It reads "
        "as a prediction (\"is predicted to\", \"practitioners are hypothesised to\"), never as an "
        "established finding.", "",
        "Retrieval gaps, below the map, are a fourth and separate thing: not hypotheses. Their action "
        "is to search further or verify an unverified span — never to ask an expert.", "",
        "**Breadth is not confidence.** Ranking among open gaps is deliberately by breadth of the "
        "attested explicit side — the opposite of low density, on purpose (§5): a gap many "
        "independent sources discuss without ever stating the missing element is a stronger claim "
        "that the element is genuinely unsaid than one only one source raises. Breadth says nothing "
        "about whether the gap is real. WHICH candidates are gaps at all is decided entirely by the "
        "lens's firing rule plus its closure test (§1.5, §2); whether that closure test is itself "
        "informative — i.e. not so easily satisfied by unrelated text that it would close almost "
        "anything — is exactly what the §7.1 checks below test.", "",
        "**These are gap candidates, not findings.** The tier label stays `inferred`; precision "
        "against a human criterion is unmeasured (there is no gold yet). What IS measured is "
        "whether the closure judge's own informativeness beats a fair null — the mismatched-"
        "evidence control and the lexical donor null, both in §7.1.", "",
        "**Lexical robustness (r/4) is not re-judged.** It is measured on the lexical construct "
        "across the 4 link-parameter settings (§1.4), not by re-asking the closure judge 4 times "
        "with different neighbourhood membership — so a record the judge closes or leaves open "
        "can still show a low or 0/4 lexical robustness; the two numbers answer different "
        "questions and neither overrides the other.", "",
    ]


def _co_location_note(rec: record.Record, seed_owner: dict[str, int]) -> str | None:
    seeds = [i.claim_id for i in rec.observed_evidence if i.role in ("seed", "rival")]
    owners = {seed_owner[s] for s in seeds if s in seed_owner and seed_owner[s] != rec.rank}
    if not owners:
        return None
    return f"*(co-located with #{min(owners)}: shares a seed claim)*"


def _table_text(s: str, limit: int) -> str:
    return text.trim(s, limit).replace("|", "\\|").replace("\n", " ")


def _pick_topic_subset(topic: tuple, cap: int) -> tuple[list, list]:
    """At most `cap` topic items, preferring distinct `independence_key`s (defect 3); the rest is
    returned for the "+ N more" summary line. `topic` is already in deterministic `claim_id` order."""
    seen_keys: set[str] = set()
    picked, leftover = [], []
    for item in topic:
        if len(picked) < cap and item.independence_key not in seen_keys:
            picked.append(item)
            seen_keys.add(item.independence_key)
        else:
            leftover.append(item)
    if len(picked) < cap:
        need = cap - len(picked)
        picked += leftover[:need]
        leftover = leftover[need:]
    return picked, leftover


def _evidence_line(e: record.EvidenceItem) -> str:
    flag = f" — flag: {e.flag}" if e.flag else ""
    return (f"- `{e.claim_id}` [{e.role}] {e.epistemic_label} / {e.source_kind}, "
           f"key `{e.independence_key}`, verdict {e.verdict}{flag}: \"{e.span}\"")


def _evidence_lines(rec: record.Record) -> list[str]:
    lines = ["**OBSERVED EVIDENCE**", ""]
    items = rec.observed_evidence
    if not items:
        lines += ["(none)", ""]
        return lines
    primary = [i for i in items if i.role != "topic"]
    topic = tuple(i for i in items if i.role == "topic")
    shown, rest = _pick_topic_subset(topic, _EVIDENCE_TOPIC_CAP)
    for e in (*primary, *shown):
        lines.append(_evidence_line(e))
    if rest:
        keys = {i.independence_key for i in topic}
        lines.append(f"+ {len(rest)} more topic claims across {len(keys)} keys (full list in gapmap.json)")
    lines.append("")
    return lines


def _inferred_gap_lines(ig: record.InferredGap) -> list[str]:
    lines = ["**INFERRED GAP**", "", ig.statement, "",
            f"- test: `{ig.test_id}`; state: {ig.closure_state} (closure judge: {ig.judge_model})"]
    if ig.lexical_state:
        lines.append(f"- lexical comparison only (§1.5, no longer decisive): {ig.lexical_state}")
    if ig.judge_reason:
        lines.append(f"- judge reason: {ig.judge_reason}")
    if ig.partial_hits:
        lines.append(f"- partial hits: {', '.join(ig.partial_hits)}")
    if ig.synthetic_hits:
        lines.append(f"- synthetic hits (unverified): {', '.join(ig.synthetic_hits)}")
    if ig.sibling.state is not None:
        lines.append(f"- sibling run: {ig.sibling.state}"
                    + (f" (`{ig.sibling.matched_gap_id}`)" if ig.sibling.matched_gap_id else ""))
    lines.append("")
    return lines


def _hypothesis_lines(hyp: record.Hypothesis) -> list[str]:
    # §4: never printed in the indicative, as if established. `hyp.text` follows the spec's §2
    # templates verbatim (for JSON fidelity); the renderer hedges it on the way to Markdown.
    return [f"**HIDDEN-KNOWLEDGE HYPOTHESIS** (label: `{hyp.label}` — a prediction, never a fact)", "",
           f"Predicted, not observed: {hyp.text}", "",
           f"- predicted knowledge type: {', '.join(hyp.predicted_knowledge_type)}",
           f"- predicted tacitness: {', '.join(hyp.predicted_tacitness)}",
           f"- channel: {hyp.channel}", ""]


def _confidence_lines(c: record.Confidence) -> list[str]:
    q = f" − Q{c.Q}" if c.Q else ""
    return [f"**Breadth:** {c.breadth} (uncalibrated; no gold) (score {c.score} = A{c.A} + B{c.B} "
           f"− P{c.P}{q}; k_step={c.k_step}, k_topic={c.k_topic}); lexical robustness {c.robustness}", ""]


def _alternatives_lines(alts: tuple) -> list[str]:
    if not alts:
        return []
    lines = ["**Alternatives:**", ""]
    for a in alts:
        lines.append(f"- [{'live' if a.live else 'not live'}] {a.text} — {a.why}")
    lines.append("")
    return lines


def _question_lines(q: record.QuestionOut) -> list[str]:
    weak = " (weak channel for this knowledge type)" if q.weak_channel else ""
    return [f"**Expert question** (channel: {q.channel}{weak}):", "", f"> {q.text}", ""]


def _record_block(rec: record.Record, heading: str, seed_owner: dict[str, int]) -> list[str]:
    lines = [heading, ""]
    if (note := _co_location_note(rec, seed_owner)) is not None:
        lines += [note, ""]
    lines.append(f"*lens: {rec.lens or '—'}; category: {rec.category}*")
    lines.append("")
    lines += _evidence_lines(rec)
    lines += _inferred_gap_lines(rec.inferred_gap)
    if rec.hypothesis is not None:
        lines += _hypothesis_lines(rec.hypothesis)
    if rec.missing:
        lines += [f"**Missing element:** {rec.missing}", ""]
    lines += [f"**Reasoning:** {rec.reasoning}", ""]
    lines += _confidence_lines(rec.confidence)
    lines += _alternatives_lines(rec.alternatives)
    if rec.question is not None:
        lines += _question_lines(rec.question)
    return lines


def _map_index_table(hyp: list[record.Record]) -> list[str]:
    lines = ["| rank | lens | anchor | breadth | lexical robustness | k_topic |",
            "|---|---|---|---|---|---|"]
    for r in hyp:
        lines.append(f"| {r.rank} | {r.lens} | {_table_text(r.anchor, _TABLE_ANCHOR_LIMIT)} | "
                    f"{r.confidence.breadth} | {r.confidence.robustness} | {r.confidence.k_topic} |")
    lines.append("")
    return lines


def _map_section(res: record.GapMapResult) -> list[str]:
    hyp = [r for r in res.map if r.category == "HYP"]
    lines = ["## Ranked gap map (candidates)", ""]
    if not hyp:
        lines += ["(no hidden-knowledge hypotheses survived the caps and gates)", ""]
        return lines
    lines += _map_index_table(hyp)
    seed_owner: dict[str, int] = {}
    for r in hyp:
        for i in r.observed_evidence:
            if i.role in ("seed", "rival"):
                seed_owner.setdefault(i.claim_id, r.rank)
    for r in hyp:
        lines += _record_block(r, f"### #{r.rank} [{r.lens}] {r.anchor}", seed_owner)
    return lines


def _control_section(res: record.GapMapResult) -> list[str]:
    control = [r for r in res.map if r.category == "CONTROL"]
    lines = ["## Control slot", "",
            "The §14.2 unknown-unknowns guard: an area no hypothesis touched, walked cold.", ""]
    if not control:
        lines += ["(no area qualified: the ledger has no areas)", ""]
        return lines
    for r in control:
        lines += _record_block(r, f"### {r.anchor}", {})
    return lines


def _rg_seed_set(rec: record.Record) -> frozenset[str]:
    return frozenset(i.claim_id for i in rec.observed_evidence if i.role in ("seed", "rival"))


def _group_retrieval_gaps(records: list[record.Record]) -> list[list[record.Record]]:
    """Defect 5: records that share a seed set and a category (co-located candidates from
    different lenses on the same claim) collapse into one listing instead of appearing once per
    lens. A record with no seed evidence (shouldn't happen outside RG-UNK, handled separately)
    never groups with another one by coincidence of both being empty."""
    groups: dict[tuple, list[record.Record]] = {}
    order: list[tuple] = []
    for rec in records:
        seeds = _rg_seed_set(rec)
        key = (seeds, rec.category) if seeds else (rec.gap_id, rec.category)
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(rec)
    return [groups[k] for k in order]


def _retrieval_gap_group_block(group: list[record.Record]) -> list[str]:
    ordered = sorted(group, key=lambda r: (r.lens or "", r.gap_id))
    primary = ordered[0]
    heading_lens = "/".join(sorted({r.lens for r in ordered if r.lens})) or "—"
    action = _RG_ACTION.get(primary.category, "search")
    lines = [f"### [{heading_lens}] {primary.anchor} — {primary.category}", "",
            f"*Action: {action} — never ask an expert.*", ""]
    lines += _evidence_lines(primary)  # one shared seed: the evidence is the same for every member
    for rec in ordered:
        if len(ordered) > 1:
            lines += [f"**[{rec.lens}]**", ""]
        lines += _inferred_gap_lines(rec.inferred_gap)
        if rec.missing:
            lines += [f"**Missing element:** {rec.missing}", ""]
        lines += [f"**Reasoning:** {rec.reasoning}", ""]
    return lines


def _rg_unk_area_and_slot(rec: record.Record) -> tuple[str, str]:
    """Splits the `" — area: <name>"` suffix `record.unk_gaps` appends onto every RG-UNK anchor
    back into (slot/question, area) table columns."""
    if " — area: " in rec.anchor:
        slot, area = rec.anchor.rsplit(" — area: ", 1)
        return slot, area
    return rec.anchor, "—"


def _rg_unk_source(rec: record.Record) -> str:
    rest = rec.inferred_gap.test_id.split(":", 1)[1]
    return "sidecar slot" if rest.startswith("slot:") else f"ledger U claim `{rest}`"


def _rg_unk_table(records: list[record.Record]) -> list[str]:
    """Defect 6: one compact table instead of one Markdown section per slot."""
    lines = ["| area | slot / question | source |", "|---|---|---|"]
    for rec in records:
        slot, area = _rg_unk_area_and_slot(rec)
        lines.append(f"| {area} | {_table_text(slot, 100)} | {_rg_unk_source(rec)} |")
    lines.append("")
    return lines


def _retrieval_gaps_section(res: record.GapMapResult) -> list[str]:
    lines = ["## Retrieval gaps", "",
            "Not hypotheses: each one's action is to search further or verify a synthetic span, "
            "never to ask an expert.", ""]
    unk = [r for r in res.retrieval_gaps if r.category == "RG-UNK"]
    other = [r for r in res.retrieval_gaps if r.category != "RG-UNK"]
    if not unk and not other:
        lines += ["(none)", ""]
        return lines
    if unk:
        lines += ["### RG-UNK: slots searched, nothing found", ""]
        lines += _rg_unk_table(unk)
    for group in _group_retrieval_gaps(other):
        lines += _retrieval_gap_group_block(group)
    return lines


def _anti_renaming_lines(a: dict) -> list[str]:
    lines = ["### §7.1 Anti-renaming: is the map density in disguise?", "",
            "Computed over lens candidates only (HYP, RG-SINGLE, RG-UNVER, RG-SIBLING, RG-UNDECIDED "
            "and closed candidates) -- RG-UNK and CONTROL are excluded, since their density cannot "
            "vary.", "",
            f"- `J10(map, D_low)` = {a['j10_low']:.2f}",
            f"- `J10(map, D_high)` = {a['j10_high']:.2f}",
            f"- Spearman ρ(score, dens) = {a['spearman']:.2f}",
            f"- flags: {', '.join(a['flags']) if a['flags'] else 'none'}", "",
            "**Matched-density table** (all lens candidates, by `dens` tercile):", "",
            "| tercile | n | closed | HYP |", "|---|---|---|---|"]
    for row in a["terciles"]:
        lines.append(f"| {row['tercile']} | {row['n']} | {row['closed']} | {row['hyp']} |")
    lines.append("")
    lines.append(f"Top-tercile closed share: {a['top_tercile_closed_share']:.2f}")
    lines.append("")
    lines += ["**Closure rate by `k_topic` band** (all lens candidates):", "",
             "| band | n | closed | rate |", "|---|---|---|---|"]
    for row in a["closure_by_k_topic"]:
        lines.append(f"| {row['band']} | {row['n']} | {row['closed']} | {row['rate']:.2f} |")
    lines.append("")
    return lines


def _mismatched_evidence_control_lines(mc: dict) -> list[str]:
    lines = ["### S2 fair mismatched-evidence control: does the judge close because of the "
            "EVIDENCE, or because of the SEED?", "",
            "Replaces the first (straw-man) control, second adversarial review, 2026-09-29: the "
            "old own-evidence arm always carried the seed's own sentences while the mismatched "
            "arm never did (17/22 of PLC's old closures cited only the seed or its source), and "
            "the mismatched sentences were off-topic (cyclic gap_id pairing). Now BOTH arms keep "
            "the seed's own sentences; the OWN arm adds this candidate's own retrieved "
            "non-seed-source sentences; the CONTROL arm replaces those with the non-seed-source "
            "sentences retrieved for the topically nearest OTHER candidate of the same lens (max "
            "seed-stem Jaccard, ties by gap_id). \"other-source-only\" is the OWN arm with the "
            "seed and same-source sentences excluded entirely -- how often an independent source "
            "alone closes it. `closure-uninformative` unless own_rate - control_rate >= 0.20 "
            "(of candidates); lenses with < 2 candidates are skipped.", "",
            "| lens | n | own rate | control rate | other-source-only rate | flag |",
            "|---|---|---|---|---|---|"]
    for lens_name in sorted(mc["by_lens"]):
        row = mc["by_lens"][lens_name]
        flag = "closure-uninformative" if row["flag"] else ""
        lines.append(f"| {lens_name} | {row['n']} | {row['own_rate']:.2f} | "
                    f"{row['control_rate']:.2f} | {row['other_source_only_rate']:.2f} | {flag} |")
    if mc["total"] is not None:
        t = mc["total"]
        t_flag = "closure-uninformative" if t["flag"] else ""
        lines.append(f"| **total** | {t['n']} | {t['own_rate']:.2f} | {t['control_rate']:.2f} | "
                    f"{t['other_source_only_rate']:.2f} | {t_flag} |")
    lines.append("")
    return lines


def _lexical_donor_null_lines(null: dict) -> list[str]:
    lines = ["### S2 lexical donor null: why the lexical closure test was replaced", "",
            "The reviewer's fair donor null for the (now-comparison-only) LEXICAL closure test: "
            "self and same-source claims are excluded from both arms, and the donor is the real "
            "non-common content stems of a random other-source A claim of the same knowledge "
            f"type as the seed (`random.Random(0)`, {config.CLOSURE_NULL_DRAWS} draws). A check "
            "\"passes\" (is informative) only if the observed count is STRICTLY ABOVE the null's "
            "5-95% interval. DISC is excluded (anchor-regex-driven, not stem-overlap); DIAG is "
            "handled per its own closure unit (one rival's sign test, not the group).", "",
            "| lens | observed closed | null mean | null 5-95% | n | flag |",
            "|---|---|---|---|---|---|"]
    for lens_name in sorted(null["by_lens"]):
        row = null["by_lens"][lens_name]
        flag = "closure-uninformative" if row["flag"] else ""
        lines.append(f"| {lens_name} | {row['observed']} | {row['null_mean']:.1f} | "
                    f"[{row['null_lo']:.0f}, {row['null_hi']:.0f}] | {row['n_candidates']} | {flag} |")
    t = null["total"]
    t_flag = "closure-uninformative" if t["flag"] else ""
    lines.append(f"| **total** | {t['observed']} | {t['null_mean']:.1f} | "
                f"[{t['null_lo']:.0f}, {t['null_hi']:.0f}] |  | {t_flag} |")
    lines.append("")
    return lines


def _judge_lexical_confusion_lines(confusion: dict) -> list[str]:
    lines = ["### Judge-vs-lexical agreement", "",
            "Confusion counts, `<lexical_state>-><judge_state>`, over every judged candidate "
            "(the lexical test no longer decides anything; this is diagnostic only).", "",
            "| lexical -> judge | n |", "|---|---|"]
    for key, n in confusion.items():
        lines.append(f"| {key} | {n} |")
    lines.append("")
    return lines


def _cross_run_lines(c: dict) -> list[str]:
    lines = ["### §7.2 Cross-run stability", ""]
    for direction, rows in (("this ledger → sibling", c["a_to_b"]), ("sibling → this ledger", c["b_to_a"])):
        lines.append(f"**{direction}** ({len(rows)} open candidate(s)):")
        lines.append("")
        if not rows:
            lines.append("(none)")
        for row in rows:
            lines.append(f"- `{row['gap_id']}` [{row['lens']}] {row['anchor']}: counterpart "
                        f"{row['counterpart_category'] or 'none'}"
                        + (f" ({row['counterpart_closure_state']})" if row["counterpart_closure_state"] else ""))
        lines.append("")
    return lines


def _checks_section(res: record.GapMapResult) -> list[str]:
    lines = ["## §7 checks", ""]
    lines += _anti_renaming_lines(res.check_data["anti_renaming"])
    if "mismatched_evidence_control" in res.check_data:
        lines += _mismatched_evidence_control_lines(res.check_data["mismatched_evidence_control"])
    if "lexical_donor_null" in res.check_data:
        lines += _lexical_donor_null_lines(res.check_data["lexical_donor_null"])
    if "judge_lexical_confusion" in res.check_data:
        lines += _judge_lexical_confusion_lines(res.check_data["judge_lexical_confusion"])
    if "cross_run_stability" in res.check_data:
        lines += _cross_run_lines(res.check_data["cross_run_stability"])
    return lines


def render(res: record.GapMapResult) -> str:
    lines: list[str] = []
    lines += _header(res)
    lines += _summary_section(res)
    lines += _how_to_read()
    lines += _map_section(res)
    lines += _control_section(res)
    lines += _retrieval_gaps_section(res)
    lines += _checks_section(res)
    return "\n".join(lines) + "\n"
