# E-LIVE manual claim inspection

One inspector, an AI agent (Claude Sonnet 5), not a human and not a blind second coder, with no gold, read a reproducible sample of NATURAL
claims against their actual stored source text — re-slicing every sampled span from
`snapshots/<sha256>.txt` at the recorded `char=start,end` locator and comparing byte-for-byte to
`Selector.exact`, then reading ±300 chars of context to judge entailment. "Pipeline completed" is
not evidence of correctness; this note is the check against the stored text itself. No network or
LLM calls were made; scores are one model inspector's judgment, with no human check and no inter-rater reliability.

## Runs

- **GDPR v2(b)** `reconstruct/runs/20260928T145943Z-bc1cc9a30a02` — ran at commit `080b109`, the
  stricter verifier schema/prompts (`adds_content`, `subject_or_scope_differs`,
  `quantifier_modality_or_connective_differs`; SUPPORTS only if all three are false). `git diff 080b109
  883b52a -- reconstruct/src/reconstruct/prompts` is empty, so the prompts at tag `n2-freeze-3`
  (`883b52a`) are unchanged from this run. 523 claims, 351 located, 366 located *evidence spans*
  of which **140 are still `pending`** (the known provider-error defect) — confirmed directly from
  the ledger, matching the number in `e_live_report.md`. This is the only current-verifier run with
  live data.
- **PLC v1** `reconstruct/runs/20260928T133336Z-59ec876b3d7e` and **GDPR v1**
  `reconstruct/runs/20260928T135354Z-eb840a85b7d1` — older verifier, commit `600ba2e`.
- **PLC v2** (`20260928T145115Z-518f99363336`) crashed (0 claims); **PLC v3** / **GDPR v3**
  (`20260928T171449Z-518f99363336`, `20260928T171508Z-bc1cc9a30a02`) are empty (OpenRouter key
  capped). There is **no current-verifier PLC data** — no substitute is offered.

## Sampling

Seed `20260928`. For each stratum: `sorted(candidate_claim_ids)`, then a fresh
`random.Random(20260928).sample(sorted_ids, k)`. Claim labels/verdicts were computed by loading
`ledger.json` through `residual.ledger.Ledger` (the same `ClaimRecord.label` property the pipeline
itself uses) — not re-derived by hand.

- GDPR v2(b): 25 `literature_supported` (verdict `supports`) claims; 10 claims whose verdict is
  `insufficient`/`refutes` (pool = 19, all `insufficient`; 0 `refutes` claims exist in this run);
  10 `synthetic_extrapolation` claims; all 15 `unknown` claims (all of them, not sampled).
- PLC v1: 20 `literature_supported` claims.
- GDPR v1: 10 `literature_supported` claims, sampled from the pool of 193 minus the 15 claim ids
  already quoted in `e_live_review_notes.md`'s run-(b) section (178 remaining candidates).

Provenance re-slice check (locator sha256 + char offsets vs `Selector.exact`, all sampled
evidence, both runs' verifiers): **0/71 mismatches** (71 evidence items across the 75 sampled claims). Every sampled span is exactly what the
locator says it is.

## Per-run summary

| Run | Stratum | n | Codes | Error rate (non-CORRECT) | Wilson 95% CI |
| --- | --- | --- | --- | --- | --- |
| GDPR v2(b) | supports | 25 | CORRECT 22, SCOPE_DRIFT 3 | 12.0% (3/25) | 4.2–30.0% |
| GDPR v2(b) | insufficient/refutes | 10 | REJECT_RIGHT 7 (jurisdiction dropped, per the SCOPE_DRIFT standard), REJECT_WRONG 2, borderline 1 (after the final review's recode) | wrong rejections 2–3/10 | — |
| GDPR v2(b) | synthetic_extrapolation | 10 | 5 `pending` (all look supportable once verified), 5 `no_evidence` (never located, so genuinely unsupported today) | n/a | — |
| GDPR v2(b) | unknown (all 15) | 15 | all 15 are `performance`-question probes (failure_mode/check/decision/rationale) across 5 areas; 0 `domain`-question unknowns | n/a (gap map, not an error stratum) | — |
| PLC v1 | supports | 20 | CORRECT 10, CORRECT-caveat 4, SCOPE_DRIFT 2, ADDED_CONTENT 2, WRONG 1, QUANTIFIER/MODALITY 1 | 30.0% (6/20) | 14.5–51.9% |
| GDPR v1 | supports | 10 | CORRECT 9, SCOPE_DRIFT 1 | 10.0% (1/10) | 1.8–40.4% |

Source quality: no `JUNK_SOURCE` (error page/SEO spam) in any sample. GDPR sources are
regulator/EDPB/legislation-text pages (`tier: curated`) plus two `tier: open` national-DPA PDFs
(dpa.gr, edpb.europa.eu-hosted national lists); PLC sources are all `tier: open` vendor/blog pages
(PLCDocs, AssetCenter, Recurrr, ecsintl.com, automate.org, one SpringerLink abstract), consistent
with `e_live_review_notes.md`'s finding that PLC evidence is largely SEO/marketing content that
happens to be factually usable.

**Jurisdiction-mismatched sources (UK guidance for an "EU data protection law" task):** every
`SCOPE_DRIFT` found in the two GDPR supports samples is the same pattern — a UK ICO (or one other
member state's) **Article 35(4) national list item** (a per-country supervisory-authority
designation, not an EU-wide rule) generalised into "a DPIA is required" / "requires a DPIA" with no
jurisdiction qualifier: `c-b308aea20d8cb601` (genetic data), `c-e3fdcc891699e1d7` (tracking),
`c-e314a06b576099c1` (data matching, GDPR v1). `c-5adc8389c5ca8ebc` misattributes Slovenia's
national list to "the EDPB list" generically. By contrast, claims that *keep* the jurisdiction in
their own wording (Luxembourg's `c-ef6ab1dedaf723cb`, Ireland's `c-f4fade5df45938f5`, UK-specific
"ICO" claims `c-0948649167e1de7b`/`c-2005ed4d313463ac`) are all CORRECT — the drift is specific to
claims that strip the qualifier, not to UK/national sourcing per se.

**Correction after the final adversarial review.**
- The first pass coded all 10 sampled `insufficient` claims REJECT_WRONG and concluded that the verifier over-rejects. That applied a looser standard than the supports stratum.
- Seven of the ten are the same pattern the inspector codes as SCOPE_DRIFT when it is accepted: a national Art. 35(4) list item restated as a general DPIA requirement, with the jurisdiction dropped.
  - Greek list: `c-0b44c98d0b1f8a58`, `c-3c4f5c3f9b239a55`.
  - Luxembourg list: `c-12a4266076133e03`. Its accepted neighbour `c-ef6ab1dedaf723cb` keeps the jurisdiction ("Article 65 of the act of 1 August 2018"), so the pair is consistent, not contradictory.
  - ICO list: `c-364fa597451f575e`, `c-3c6ecdd3a6c0bb61`, `c-3ff2b8ee14481909`.
  - Finnish list: `c-5243045bcf730c1c`, which also narrows "at least one other criteria".
- On the consistent standard these rejections are right. Only `c-a38d2addea6a7e82` and `c-978f44f453c0f9ea` are clear wrong rejections, and `c-75363da4c7f1ad41` is borderline: **2–3 of 10**.
- The pattern that remains is the reverse: some jurisdiction-dropping list items were accepted (the 3 SCOPE_DRIFT in the supports sample) and sibling items were rejected. The verifier is inconsistent on this pattern, not biased towards rejection.
- No recall figure can be computed, because there is no denominator of truly supported claims.
- The 5 sampled `pending` claims are near-verbatim matches to their spans. They are stuck behind the provider-error defect, not ungrounded.

**Where the 19 rejections come from** (all 19, not the sample; read from the sidecar's
`verify_*` fields and `evidence.quote_in_span` at `n2-freeze-3`):
- **14: the verifier model set a drift flag.** The flags were `adds_content` in 12 (alone in 4) and
  `quantifier_modality_or_connective_differs` in 8, with `subject_or_scope_differs` in only 3.
  Amendment 1's rule then turns SUPPORTS into insufficient.
- **5: all three flags were false, but the verifier's `supporting_quote` is not a verbatim substring of
  the span**, so the registered quote rule downgraded it. Four of the five are near-verbatim
  "repairs" of extraction artefacts: 3 PDF, e.g. `c-a38d2addea6a7e82` quotes "organization" where the
  span reads "organi zation", and 1 HTML. The fifth (`c-62d8711459e956b4`) shares only 17 characters
  with its span.
The sidecar stores only the post-rule verdict, not the model's raw verdict, so it cannot show whether the model said SUPPORTS before the rule applied. "14 carry a drift flag; 5 have no flag and a quote not in the span" is all the artefact supports.

## Sampled claims

### GDPR v2(b) — supports (25; error rate 12.0% [4.2–30.0%])

- `c-0d6950574951a8b3` — CORRECT. List item "Uses of new or novel technologies" verbatim from IE DPC/EDPB factor list.
- `c-13149a5c7926afa0` — CORRECT. Near-verbatim Art. 35(1) restatement, GR DPA PDF.
- `c-20ad479d3a941810` — CORRECT. Verbatim Art. 35(7)(c), UK legislation.gov.uk copy of GDPR text.
- `c-47e588c2eec6cdfb` — CORRECT. Near-verbatim large-scale factors; source is ICO ("the UK GDPR does not contain a definition… but…"), interpretive not a national list, jurisdiction dropped but content not UK-exclusive.
- `c-4b342e0bd11c94a3` — CORRECT. Verbatim WP248 (EU-wide, cnil.fr-hosted) sentence on updating a DPIA.
- `c-5adc8389c5ca8ebc` — **SCOPE_DRIFT.** Claim says "the EDPB list"; span is Slovenia's national Art. 35(4)/(6) list ("The list is not exhaustive…"), only hosted on edpb.europa.eu.
- `c-5e12588fd1c6befa` — CORRECT. Near-verbatim Art. 35(1) restatement, IE DPC/EDPB.
- `c-732434703195d916` — CORRECT. Verbatim 'risk'/'high risk' definitions, ICO, general concept.
- `c-77a33ade5d4089e4` — CORRECT. Verbatim Art. 35.1 quote, Luxembourg CNPD deliberation (self-names LU).
- `c-8c664dd67d2c597d` — CORRECT. Near-verbatim "DPO should monitor performance", WP248/cnil.fr.
- `c-9ac50e648edf1e02` — CORRECT. Verbatim "concept of high risk… several factors" framing, IE DPC/EDPB.
- `c-9f5b81391ed56bbb` — CORRECT. Verbatim "denial of service" criterion, ICO, span itself attributes it to "the European Guidelines".
- `c-a8cb3db9ee88f8c2` — CORRECT. Near-verbatim "mitigate the impact on… control over their data", ICO invisible-processing guidance.
- `c-b308aea20d8cb601` — **SCOPE_DRIFT.** UK/IE Art. 35(4) national list item ("genetic data") generalised to "A DPIA is required"; both corroborating sources are the same UK ICO list (one direct, one via EDPB archive), so it is not independent EU corroboration either.
- `c-b8326043ad0ac2c1` — CORRECT. Verbatim Art. 35(3)(a), UK legislation.gov.uk copy of GDPR text.
- `c-c51057a1ca2a7b71` — CORRECT. Near-verbatim Art. 35(3) summary, IE DPC/EDPB.
- `c-cf358fcdbfdb74e7` — CORRECT. Verbatim Art. 35(1), UK legislation.gov.uk copy.
- `c-db3d63a0a619f009` — CORRECT. Near-verbatim Recital 91 paraphrase via ICO (recital is EU-wide law, not UK-only).
- `c-dc9662f14f9b139b` — CORRECT. Near-verbatim "consider both likelihood and severity", ICO.
- `c-de7d9d383506ead4` — CORRECT. Verbatim "combined data sets… beyond expectations" factor, IE DPC/EDPB.
- `c-df979a78a5b2be70` — CORRECT. Near-verbatim "significant effect" gloss via ICO, itself attributed to Art. 29 WP guidance.
- `c-e3fdcc891699e1d7` — **SCOPE_DRIFT.** UK ICO Art. 35(4) national list item ("tracking") generalised to a GDPR-wide DPIA trigger.
- `c-ef6ab1dedaf723cb` — CORRECT. Verbatim; claim itself names "Article 65 of the act of 1 August 2018" — jurisdiction (Luxembourg) preserved.
- `c-f4fade5df45938f5` — CORRECT. Verbatim; claim names "The Irish Data Protection Act 2018, Section 84" — jurisdiction (Ireland) preserved.
- `c-f8f823c57da3caea` — CORRECT. Verbatim "pseudonymisation reversal" factor, IE DPC/EDPB.

### GDPR v2(b) — insufficient/refutes (10; verdict `insufficient` in all 10, 0 `refutes`)

- `c-0b44c98d0b1f8a58` — REJECT_RIGHT (scope). Greek national list item; claim drops the jurisdiction ("subject to DPIA requirement" stated generally). First pass: REJECT_WRONG.
- `c-12a4266076133e03` — REJECT_RIGHT (scope). Luxembourg list item stated without jurisdiction; the accepted neighbour `c-ef6ab1dedaf723cb` keeps it, so the pair is consistent. First pass: REJECT_WRONG.
- `c-364fa597451f575e` — REJECT_RIGHT (scope). ICO national list item ("targeting of children") restated as a general DPIA requirement. First pass: REJECT_WRONG.
- `c-3c4f5c3f9b239a55` — REJECT_RIGHT (scope). Greek national list item "1.5" (video surveillance), jurisdiction dropped. First pass: REJECT_WRONG.
- `c-3c6ecdd3a6c0bb61` — REJECT_RIGHT (scope). ICO "data matching" list item, jurisdiction dropped (same pattern as SCOPE_DRIFT `c-e314a06b576099c1`). First pass: REJECT_WRONG.
- `c-3ff2b8ee14481909` — REJECT_RIGHT (scope). ICO "large-scale profiling" list item, jurisdiction dropped. First pass: REJECT_WRONG.
- `c-5243045bcf730c1c` — REJECT_RIGHT (scope). Finnish list item, jurisdiction dropped; also narrows "at least one other criteria". First pass: REJECT_WRONG (borderline).
- `c-75363da4c7f1ad41` — BORDERLINE (was REJECT_WRONG), directly inconsistent with accepted `c-0d6950574951a8b3` — same "These factors include…" list, adjacent bullet.
- `c-978f44f453c0f9ea` — REJECT_WRONG, inconsistent with accepted `c-a8cb3db9ee88f8c2` — same paragraph, same "It will…" antecedent.
- `c-a38d2addea6a7e82` — REJECT_WRONG. Span is byte-for-byte the claim (minus a PDF line-break in "organi zation"); the clearest over-rejection in the sample.

### GDPR v2(b) — synthetic_extrapolation (10)

Pending (evidence located, verdict stuck on the provider-error defect) — all read as correctly supported on inspection:
- `c-6628c5648a66911a` — span near-verbatim ("the UK GDPR is clear that you need to consider both the likelihood and severity…").
- `c-84320af469a401af` — span near-verbatim ("DPIAs are a legal requirement for processing that is likely to be high risk").
- `c-a0d8c38328207289` — span matches Art. 35(7)(c) text (dpocentre.com copy), same content as accepted `c-20ad479d3a941810`.
- `c-c51ad3d4a9cb2b27` — span near-verbatim ("consult with individuals and other stakeholders throughout this process").
- `c-f1efe54c739fd8cb` — span near-verbatim ("consult the Data Protection Authority (DPA) before proceeding").

No evidence located at all (genuinely unverified today):
- `c-0f9750b526572e63`, `c-3139f38fe933f7e3`, `c-5d834091752c1341`, `c-e7535b7dd533d9f5` — plausible unlocated legal claims, zero search/verification attempted.
- `c-a801e3b36ce1fbd6` — near-duplicate of `c-364fa597451f575e` (children/vulnerable targeting), extracted separately with no evidence while the other copy has a located (rejected) span.

### GDPR v2(b) — unknown (all 15, not sampled)

All 15 are `performance`-question probes ("How does work… typically go wrong", "What conditions
determine which option is chosen…", "How is work… checked for correctness…") across the 5 areas
(GDPR Mandatory DPIA Requirements; Required Contents and Elements of a DPIA; High Risk Processing
Activities Under GDPR; Exemptions and Exceptions to DPIA Requirements; EDPB Guidelines and
Regulatory Interpretation). Zero `domain`-question unknowns. This matches the expected pattern for
a corpus of regulatory/statutory text: it states obligations, not how DPIAs go wrong in practice.

### PLC v1 — supports (20; error rate 30.0% [14.5–51.9%])

- `c-099de6d81ec901b5` — CORRECT. "a line has already stopped" → "production has already stopped", faithful generalisation.
- `c-0b0bdd3ff65e2dd0` — **SCOPE_DRIFT.** "The template deliberately separates…" (one blog's specific log template) generalised to "Maintenance logs separate…".
- `c-178407cc99b8ed7c` — CORRECT. "staring at 80% of the time" → "account for approximately 80% of troubleshooting work", faithful.
- `c-272430e6b95c067d` — CORRECT. Near-verbatim "360-degree protection strategy".
- `c-284b605529c10565` — CORRECT. Near-verbatim "grounded at one end only… ground loops".
- `c-47a2a29c52f7d738` — CORRECT (caveat). "your log should force a different conversation" glossed as "identify when a repair has not resolved the underlying issue" — a reasonable but not literal gloss.
- `c-4a2735242356a648` — CORRECT (caveat). List matches span; "identifies patterns and exceptions" framing comes from the section heading just outside the span; drops "missing evidence" from the enumerated list.
- `c-4de15f10b4330643` — CORRECT. Near-verbatim "not a defect: it's physics… input impedance… residual current".
- `c-5f153b8f6953bef9` — **ADDED_CONTENT.** "rather than individual card channel failures" is not stated or implied by the span (a plausible but unlicensed inference).
- `c-6726d5a93c8ce8da` — CORRECT. Near-verbatim "load coil resistance… shorted coil will kill/destroy the replacement card".
- `c-7bbe33b04e986102` — CORRECT. Faithful 4-category summary of an 11-item field list.
- `c-867ef26bc5a0d84a` — CORRECT (caveat). "It" resolved via context to "the polygon generation method"; resolution appears correct but the antecedent sits outside the span.
- `c-999231909ad2e610` — **ADDED_CONTENT.** Span is a bare imperative ("Do not mask a power problem…"); claim invents the subject "Competent technicians should not…".
- `c-b1b2c02c076bda50` — CORRECT (caveat). Marketing-copy framing ("We'll show you how…") flattened into a flat causal claim; content matches the article's own thesis.
- `c-bd3233c483e5442b` — **SCOPE_DRIFT.** A first-person case narrative about one specific incident ("told us… the root cause was likely…") generalised into a domain rule ("is a strong indicator"), also drops the "likely" hedge.
- `c-d008e8f1da0cb01c` — **WRONG.** Matches `e_live_review_notes.md`'s own finding: "usually" hedge dropped, subject reframed from "teams that stay out of firefighting mode" to "the most effective maintenance teams".
- `c-d4d73da4a67a3c82` — CORRECT. "20-metre cable run" → "long cable runs", faithful generalisation.
- `c-dcdfe8e233c2abcf` — CORRECT. Near-verbatim "reading close to zero… shorted coil… killed/destroyed the output transistor".
- `c-e7be928f79f939b3` — **QUANTIFIER/MODALITY.** Source is a conditional describing a hypothetical *avoided* by a separate design mechanism ("if the trigger were… the reset would re-arm… rung 3 is a separate Trend_Rearm for exactly that reason"); claim flattens this into an unconditional prescriptive rule ("should not re-arm… because it would overwrite").
- `c-fd99b87af2f9d201` — CORRECT. Near-verbatim 6-step troubleshooting mindset.

### GDPR v1 — supports (10; error rate 10.0% [1.8–40.4%])

- `c-0948649167e1de7b` — CORRECT. Near-verbatim "accept a high risk… consult the ICO"; claim correctly names ICO (not generalised).
- `c-2005ed4d313463ac` — CORRECT. Near-verbatim "high risk that you cannot mitigate… consult the ICO".
- `c-477ea8169e5e396e` — CORRECT. Near-verbatim disproportionate-effort exception language; "for not providing privacy information" is an accurate gloss from context.
- `c-6370fb5b7eeb5c13` — CORRECT. 10-item list matches the span exactly (span itself excludes the source's 11th item, "screening criteria flagged").
- `c-7b56157261d38d55` — CORRECT. Verbatim Art. 35(2), UK legislation.gov.uk copy (text identical EU/UK GDPR).
- `c-a14dd2aa7aaf93cb` — CORRECT. Near-verbatim "good practice to publish your DPIA… foster trust".
- `c-cb6b607ac9ce72c1` — CORRECT. Near-verbatim Art. 35(10).
- `c-e314a06b576099c1` — **SCOPE_DRIFT.** UK ICO Art. 35(4) national list item ("data matching") generalised to "requires a DPIA".
- `c-fb7e55870abf0330` — CORRECT. Near-verbatim security-risk-assessment content list.
- `c-fbf2d326300b2154` — CORRECT. "rather than assessing whether processing is actually high risk" draws on a sentence just before the span ("the important point here is not whether…"); correctly resolved.
