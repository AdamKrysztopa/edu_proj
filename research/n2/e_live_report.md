# E-LIVE report: real-web reconstruction sanity gate

Branch `n2`. Sources: `reconstruct/runs/` artefacts (`ledger.json`, `sidecar.json`, `report.md`, `calls.jsonl`) read and computed on directly; `research/n2/e_live_review_notes.md` (the prior review of v1); `docs/lessons.md`; git history on `reconstruct/`. All numbers below are computed from the artefacts, not copied from prose.

## 0. What E-LIVE is, and is not

**E-LIVE is a SANITY gate on the real web, not a scientific benchmark.** The question it answers is narrow: *given only a domain and a task, does the pipeline produce something genuinely useful* — located, verifiable, correctly-labelled evidence — *or does it silently fabricate, mislabel, or fall over?* It runs against the live internet (OpenRouter/Exa search, arbitrary fetched pages), so its numbers are not comparable across runs or reproducible, and it carries no gold and no pre-registered threshold. It is not E-PLANT (planted-claim recovery) and not E-ABST (abstention scoring), which are the actual gated pipeline-trust experiments; E-LIVE is a cheaper, earlier check that the plumbing does something real before those are trusted.

**N2 is an enabling milestone for N3, not N3 itself.** The strategic hypothesis under test across the NOW programme (RQ-B) is whether a reconstruction from public/organisational evidence, plus a gap map, predicts where the human knowledge residual lies. N2 builds and hardens the reconstruction pipeline (the "reconstructable" half); N3 (E-CTA, E-OSS) is the critical path that tests whether the *residual* — what the reconstruction does not and cannot cover — is predictable. E-LIVE's job is only to confirm N2's pipeline is not broken in a way that would make its N3 inputs meaningless. Nothing in E-LIVE is a criterion for N3; per decision 0006, synthetic/reconstructed output is a predictor, never a criterion, and never feeds a gate.

## 1. Domains and why

Two tasks, one technical/procedural and one legal/normative, run through the identical pipeline and model config:

| Run | Domain | Task |
| --- | --- | --- |
| PLC | industrial machine maintenance | "How does a maintenance technician diagnose an intermittent fault in a PLC-controlled machine?" |
| GDPR | EU data protection law | "When must a controller carry out a data protection impact assessment under the GDPR, and what must it contain?" |

PLC fault diagnosis was substituted for centrifugal **pump cavitation**, the domain originally drafted from the owner's example (`docs/plans/n2a-walking-skeleton.md` step 2). Per `docs/lessons.md`:

> The N2a plan … adopted centrifugal pump cavitation as the E-LIVE technical domain … without checking `REORIENTATION.md` §18.1: NPSH is fluid energy conservation, and anyone who has seen reconstructed conservation content is ineligible for a Track A human role. No check caught it. It surfaced only because the Opus agent drafting the E-PLANT protocol independently avoided pump cavitation for that reason. Swapped to PLC intermittent-fault diagnosis.

GDPR DPIA was chosen as a legal/normative counterpart with a different evidence texture (statute, regulator guidance, checklists) to see whether pipeline failure modes are domain-general or domain-specific — they turned out to be the same architecture, different failure modes (§8 below).

## 2. Runs and their status

| Run dir | Version | Domain | Status |
| --- | --- | --- | --- |
| `20260928T133336Z-59ec876b3d7e` | v1 | PLC | complete, reviewed |
| `20260928T135354Z-eb840a85b7d1` | v1 | GDPR | complete, reviewed |
| `20260928T145115Z-518f99363336` | v2 | PLC | **crashed** (`UnicodeEncodeError`, PDF surrogate) |
| `20260928T145943Z-bc1cc9a30a02` | v2 | GDPR | completed but **defect-compromised** (see §5) |
| `20260928T171449Z-518f99363336` | v3 | PLC | **blocked at first call** (OpenRouter weekly key limit) |
| `20260928T171508Z-bc1cc9a30a02` | v3 | GDPR | **blocked at first call** (OpenRouter weekly key limit) |

v1 ran at commit `600ba2e`. The fix pass at `080b109` (below) responded to the v1 review. v2 ran at the fix-pass code, after `375c09f`/`bf35207`/`d3e0bb4` (E-PLANT scaffolding, unrelated to E-LIVE mechanics) and before `0f39ed9`. v3 ran at `0f39ed9` ("n2-freeze-2").

## 3. v1: per-run detail

Both use `models.json`: planner/extractor/baseline = `anthropic/claude-haiku-4.5`; verifier/contradiction = `openai/gpt-5.4-mini` (different model family from the extractor, as required for an independent verify pass). 7 probes: concept, decision, cue, check, failure_mode, norm, rationale.

### PLC (v1)

| Metric | Value |
| --- | --- |
| Areas / sources fetched / fetch failures | 5 / 35 / 12 |
| Extracted / located / verified (supports) claims | 370 / 337 / 321 |
| Unlocated rate | 8.9% |
| Independent clusters (largest share) | 27 (11.4%) |
| Labels | literature_supported 321, synthetic_extrapolation 49, unknown 5 |
| Ledger contradictions / other disagreements | 0 / 50 |
| Decoy false-accept rate | 35% (20 decoys) |
| Cost | $0.679 |

Source kinds/tiers: all 35 sources typed `documentation`/`open` (no host-kind rules yet — a known v1 gap). HTTP statuses: 200×24, 403×10, 429×1 — **11 of 35 "sources" are error pages** (bot walls, access-denied, empty shells), a defect, not signal.

### GDPR (v1)

| Metric | Value |
| --- | --- |
| Areas / sources fetched / fetch failures | 5 / 20 / 18 |
| Extracted / located / verified (supports) claims | 259 / 204 / 195 |
| Unlocated rate | 21.2% |
| Independent clusters (largest share) | 4 (55%) |
| Labels | literature_supported 193, synthetic_extrapolation 64, unknown 14 |
| Ledger contradictions / other disagreements | 1 / 39 |
| Decoy false-accept rate | 15% (20 decoys) |
| Cost | $0.500 |

Source kinds/tiers: all 20 sources typed `documentation`/`open`. HTTP statuses: 200×15, 404×3, 403×2 — 5 of 20 are error pages, same defect as PLC.

Cross-domain contrast (from `research/n2/e_live_review_notes.md`, independently verified against the artefacts above):

| | PLC | GDPR |
| --- | --- | --- |
| Corpus | junk-heavy: vendor/SEO blogs | authoritative: statute/regulators, but UK-centred (80% of supports from ico.org.uk or the UK statute copy in an "EU" task) |
| Independence | many small clusters | over-merged into 4 (the ≥25-word shared-quotation rule unions whole documents transitively — e.g. legislation.gov.uk + 6 ICO pages + CNPD merge into one cluster because all three quote Art. 35 verbatim) |
| Verifier on natural claims | passes generalisation/scope drift ≈1 in 5 (Wilson 95% CI ≈8–42%, n=20) | ≈9/10 right (near-verbatim legal text), but misses and/or swaps |
| Corroboration | dead: 370 extractions → 370 claims, 0 merges | dead: 259 → 259, 0 merges (independence over-merge would suppress it anyway) |

## 4. v1 worked examples (verbatim)

### 4.1 GOOD reconstruction — full provenance trace

Claim `c-001378676d9bc0ce`, GDPR run, area "High-risk processing activities definition":

- **Claim (assertion):** "A DPIA is required for systematic and extensive evaluation of personal aspects of natural persons based on automated processing including profiling where decisions with legal or similarly significant effects are based on such processing."
- **Source URL:** `https://www.legislation.gov.uk/eur/2016/679/article/35` — retrieved 2026-09-28 — text sha256 `291faeca63f48b4898c902c23f7419576ebf053ddde7ea8dc3976ef3385811ea`
- **Locator:** `sha256:291faeca...;char=6084,6373` (re-slices from the stored snapshot)
- **Exact span (`Selector.exact`):** "a systematic and extensive evaluation of personal aspects relating to natural persons which is based on automated processing, including profiling, and on which decisions are based that produce legal effects concerning the natural person or similarly significantly affect the natural person"
- **Verifier:** `openai/gpt-5.4-mini` (family `openai`, different family from the `anthropic/claude-haiku-4.5` extractor) — verdict **supports**, on 2026-09-28.

This is the mechanism working exactly as designed: claim → cited source → content hash → exact re-sliceable byte offset → an independent-family model's verdict, all inspectable without trusting the extractor's paraphrase.

### 4.2 BAD reconstruction — verifier passes a heading/scope-drift error

Claim `c-d4ac349735a8502c`, PLC run, verdict **supports** (should have been rejected):

- **Assertion:** "Diagnosing intermittent **software** faults requires understanding whether communication loss triggered a stop or resulted from a device power interruption."
- **Span actually says:** "Confirm whether communication loss triggered the stop or resulted from a device power interruption." — from `https://plcscadaacademy.blogspot.com/2026/04/how-to-diagnose-random-plc-faults-and.html`, which is in that page's **network-troubleshooting** section, not its software-fault section.
- The extractor silently reassigned the span's topic (borrowed from a nearby heading), and the verifier's SUPPORTS check at v1 did not test for subject/scope drift — only for verbatim-quote presence. This is exactly the class of error the v1 review flagged as the verifier's dominant failure mode (≈20% of sampled natural PLC claims): additions are caught, generalisation and scope reassignment are not.

A second, cleaner instance the verifier caught correctly (contrast case): `c-970e29651ce716ce` — assertion "A quality multimeter is the **most essential** tool…" against a span reading "A quality multimeter is the **most used** tool…" — verdict **insufficient**. So the verifier is not blind to all drift, just to the reassignment/generalisation class illustrated above.

### 4.3 The false "genuine" contradiction — Art. 35 vs Art. 36

The one ledger contradiction recorded across both v1 runs, and it is a **false positive**:

- `c-592a2fadc6f4283c`: "A data controller must consult the Supervisory Authority when a DPIA indicates that processing would result in high risk to data protection rights and mitigating measures cannot eliminate the residual risks." — span from `dataprotection.ie` (Art. 36 prior-consultation duty), verdict supports.
- `c-a8d67e2f019b7cce`: "A Data Protection Impact Assessment must be conducted when a type of processing is likely to result in a high risk to the rights and freedoms of individuals." — span from `ico.org.uk`, quoting Art. 35(1), verdict supports.

These are **sequential obligations** (first do the DPIA under Art. 35(1); *then*, if it shows unmitigated high risk, consult the authority under Art. 36), not contradictory ones. The contradiction guard checked only that both quotes were verbatim, not whether the pair-classifier's "contradictory" label was semantically correct — so a mis-kinded pair reached the ledger as the run's only "contradiction." Across both v1 runs the separate contradiction stage produced 89 calls, 0 correct genuine contradictions, this 1 false positive, and mostly "compatible" pairs that were actually missed corroboration.

### 4.4 UNKNOWN correctly returned

GDPR run: 14 of 35 (area × probe) slots are UNKNOWN. Two representative ones, with 0 tagged claims each:

- "Legal triggers for DPIA requirements" / **failure_mode** — regulator/statute text states obligations, not how DPIAs go wrong in practice.
- "High-risk processing activities definition" / **failure_mode** — same pattern.

Per the v1 review, `failure_mode` is UNKNOWN in 5/5 areas and `cue` in 4/5 for the GDPR run, and this looks like real signal, not an artefact: normative legal text genuinely does not carry practitioner failure-mode or perceptual-cue knowledge, which is exactly the tacit residual the gap map exists to flag. (Not all UNKNOWNs are this clean — the review also documents UNKNOWN slots that are partition artefacts from near-duplicate planner areas, e.g. PLC "norm" content split across "PLC Fault Diagnosis Methods" and "Systematic Troubleshooting Frameworks.")

## 5. v2: fix-pass code, and where it broke

Between v1 and v2, commit `080b109` ("N2 fix pass after the E-LIVE review") shipped: HTTP status/bot-wall rejection in fetch, PDF text extraction via `pypdf`, per-URL fetch caching, host-kind rules (study/standard/regulator-guidance, curated/open tier), span-level (not whole-document) independence merging, a stricter verifier schema (flags for added content, scope difference, and quantifier/modality/connective difference), extraction-prompt fixes (keep subject/quantifier/modality/jurisdiction; split conjunctive lists), a corrected decoy protocol (real verify payload, strengthening-only mutations, Wilson CI), removal of the pairwise contradiction classifier in favour of cross-cluster re-verification, a new "thin" slot status, and a new `procedure_step` probe.

**PLC v2 (`20260928T145115Z-518f99363336`): crashed, 0 claims.** `sidecar.json` records `complete: false`, `incomplete_reasons: ["run failed: UnicodeEncodeError('utf-8', ...'surrogates not allowed')"]`. The failing document is a `pypdf`-extracted PDF ("Review of Typical Interference Suppression Measures for Industrial Control Systems") whose extracted text contained a lone UTF-16 surrogate that could not be UTF-8-encoded for hashing, and the fetch phase aborted entirely on that one document rather than recording a fetch failure and continuing. 18 fetch failures were logged before the crash; cost $0.193 (planning/search only — no extraction or verification ran).

**GDPR v2 (`20260928T145943Z-bc1cc9a30a02`): completed, but defect-compromised.**

| Metric | Value |
| --- | --- |
| Areas / sources fetched / fetch failures | 5 / 25 / 2 |
| Extracted / located claims | 523 / 366 (from `located: true` counts in `sidecar.json` extractions) |
| **Located claims with verdict "pending" (unverified)** | **140 / 366** |
| Verified (supports) / insufficient | 207 / 19 |
| Cross-checks | 0 (`n_cross_checks: 0`) |
| Decoys | 0 attempted, all types (`decoy_by_type` all-zero) |
| Labels | literature_supported 203, synthetic_extrapolation 305, unknown 15 |
| Independent clusters (largest share) | 7 (60%) |
| Cost | $1.002 |

The 140 pending verdicts are evidence items whose `verification` object is `{"on": null, "verdict": "pending", "verifier": null}` — i.e., the verify call for those claims never completed. This traces to the same class of defect fixed later in `0f39ed9`: provider errors during verify/cross-verify/decoy calls were raised *before* being logged, so failed calls silently vanished from `calls.jsonl` while the run still reported `complete: true`. The **0 cross-checks and 0 decoys** in this run are a symptom of the same defect family: the new cross-cluster re-verification pass and the rebuilt decoy protocol (both shipped in `080b109`) never got a chance to run to completion because their underlying verify calls were being dropped on provider error.

**Fix (`0f39ed9`, "N2 defect fix: log and retry provider errors; surrogate-safe text; fetch never aborts"):** transient provider errors now retry with backoff; every failed attempt is logged as `api_error`; skips are counted per task in the sidecar; cross-verify calls carry their own task label; lone UTF-16 surrogates from `pypdf` no longer crash hashing; one bad document becomes a fetch failure instead of aborting the fetch phase. No prompt, schema, model or logic change. The v2 runs that exposed these defects were committed as evidence in this same commit.

## 6. v3: post-fix live check — PENDING

**v3 results: PENDING.**

Both v3 runs (`20260928T171449Z-518f99363336` PLC, `20260928T171508Z-bc1cc9a30a02` GDPR) are blocked at the very first model call (the planner), before any search, fetch, extraction or verification occurred:

```
Incomplete reasons:
- run failed: LLMUnavailable('PermissionDeniedError("Error code: 403 - {\'error\': {\'message\': \'Key limit exceeded (weekly limit). Manage it using https://openrouter.ai/workspaces/default/keys/...\', \'code\': 403}}")')
```

`n_claims`, `n_sources_fetched`, `n_located`, `n_verified` etc. are all 0 in both runs; cost $0.0000. This is an OpenRouter account-level rate limit, not a pipeline defect — it says nothing about whether `0f39ed9`'s fixes work. **v3 must be re-run once the weekly key limit resets (or on a different key) before this section can be filled in.** When it runs, the numbers to fill in are: crash/non-crash on the PLC PDF corpus, the pending-verdict count on GDPR (target: 0, or explained), cross-check and decoy counts (target: > 0, matching the `080b109` cross-cluster design), and the same headline table as §3 for both domains.

## 7. Findings and the fixes they drove

| # | Finding (v1 review) | Fix shipped | Commit |
| --- | --- | --- | --- |
| 1 | HTTP error pages (403/429/404, bot walls, empty shells) counted as sources | `fetch` rejects non-2xx and near-empty/bot-wall text | `080b109` |
| 2 | Curated PDFs (standards, guides, WP248) rejected outright; only SEO/blog HTML survived | PDF text extraction via `pypdf` | `080b109` |
| 3 | Corroboration structurally zero (370→370, 259→259, 0 merges); paraphrase-based merge never fires | Cross-cluster re-verification pass generates corroboration/contradiction directly | `080b109` |
| 4 | Independence over-merged in GDPR (≥25-word shared-quotation rule unions whole documents transitively; 4 clusters, largest 55%) | Span-level (not whole-document) independence keys; host-level keys for multi-institution domains (europa.eu etc.) | `080b109` |
| 5 | Verifier passes generalisation/scope drift (~20% PLC) and and/or swaps (GDPR); decoys measured off-condition (no ±300-char context) | New verifier schema flags (added content / scope difference / quantifier-modality-connective difference); decoys use the real verify payload, strengthening-only mutations, Wilson CI | `080b109` |
| 6 | Ledger contradiction guard checks only verbatim-quote presence, not classification correctness → false positive (Art. 35 vs Art. 36) | Pairwise contradiction classifier removed; contradictions now come from cross-cluster REFUTES verdicts | `080b109` |
| 7 | Coverage rule too lenient (1 supported claim = "covered"); `procedure_step`/`strategy` claims (39% of PLC claims) never probed | New "thin" slot status (single-cluster support); `procedure_step` added to probe set | `080b109` |
| 8 | Failed fetches not cached; same failing URL refetched every hit (WP248 ×4) | Per-URL fetch caching | `080b109` |
| 9 | Report mislabels verifier-rejected (`insufficient`) claims as "(no located evidence)"; no `claim_id`/verdict on report lines | Report fix | `080b109` |
| 10 | (v2) Provider errors during verify/cross-verify/decoy calls raised before logging → calls silently vanish, run still reports `complete: true`; 140/366 GDPR claims left "pending" | Retry with backoff; every failed attempt logged as `api_error`; skips counted per task | `0f39ed9` |
| 11 | (v2) `UnicodeEncodeError` on a `pypdf`-extracted PDF with a lone UTF-16 surrogate aborts the entire fetch phase (PLC run: 0 claims) | Surrogate-safe text handling; one bad document becomes a fetch failure, not a fetch-phase abort | `0f39ed9` |

## 8. What E-LIVE does NOT show

- **Not accuracy against gold.** There is no ground truth here; "supports" means the verifier model judged the span entails the claim, nothing more. E-PLANT (planted claims with known answers) is the actual recovery-accuracy measurement.
- **Not abstention calibration.** UNKNOWN/thin rates are suggestive (§4.4) but unvalidated; E-ABST is the calibrated abstention measurement.
- **Not a residual-prediction test.** E-LIVE cannot and does not speak to RQ-B (whether the gap map predicts the human residual) — that is N3 (E-CTA, E-OSS), which has not started.
- **Not reproducible or comparable across runs.** Live web search and fetch mean v1/v2/v3 see different pages even for the same task; cost and claim counts are not comparable run-to-run.
- **Not a measurement of the post-fix pipeline.** v3, the only run at the current code, produced zero data (§6). Everything in §3–§5 is pre- or mid-fix.

## 9. E-LIVE verdict

**Pass as a sanity gate, with the fix cycle working as intended — but incomplete.** Be precise about what "pass" means here:

- v1 showed the provenance core genuinely works: every claim traces through an exact, re-sliceable span to a hashed snapshot and an independent-family verifier verdict (§4.1), across two structurally different domains. That is the thing E-LIVE exists to check, and it holds.
- v1 also surfaced real, serious defects (source-quality contamination, dead corroboration, over-merged independence, a verifier blind to scope/subject drift, a false contradiction) that would have made any N3-adjacent output misleading. All of them got concrete, targeted fixes in `080b109`, checked against the review's own evidence (§7).
- v2, run at the fixed code, immediately surfaced two *new* defects the fix pass introduced or exposed (a fetch-phase-aborting encoding bug, and a silent-failure mode in provider-error handling that hid 140/366 unverified claims behind a `complete: true` flag). These are exactly the kind of thing a sanity gate should catch before anything downstream trusts the pipeline, and they were fixed in turn (`0f39ed9`).
- **v3 — the live check of that second fix — has not run.** It is blocked by an account-level rate limit unrelated to the code. Until v3 produces real data, there is no live-web evidence that the current code (`0f39ed9`) is defect-free; there is only evidence that the *previous* two defect generations were each caught and fixed. The gate is "passing" in the sense that every defect found so far was found and closed quickly, not in the sense that the current code has been checked.

**Recommendation:** treat N2 as not yet cleared for E-PLANT/E-ABST-adjacent trust until v3 runs clean (or its findings are fixed and a v4 does). Re-run v3 as soon as the OpenRouter weekly key limit resets, and fill in §6 before relying on this pipeline for anything beyond what E-PLANT/E-ABST themselves independently re-verify.
