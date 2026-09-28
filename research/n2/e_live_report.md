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
| `20260928T171449Z-518f99363336` | v3 | PLC | **blocked at first call** (OpenRouter weekly key limit); not rerun at the closeout (budget) |
| `20260928T171508Z-bc1cc9a30a02` | v3 | GDPR | **blocked at first call** (OpenRouter weekly key limit); not rerun at the closeout (budget) |

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

These are **sequential obligations** (first do the DPIA under Art. 35(1); *then*, if it shows unmitigated high risk, consult the authority under Art. 36), not contradictory ones. The contradiction guard checked only that both quotes were verbatim, not whether the pair-classifier's "contradictory" label was semantically correct — so a mis-kinded pair reached the ledger as the run's only "contradiction." Across both v1 runs the separate contradiction stage produced 90 calls, 0 correct genuine contradictions, this 1 false positive, and mostly "compatible" pairs that were actually missed corroboration.

### 4.4 UNKNOWN correctly returned

GDPR run: 14 of 35 (area × probe) slots are UNKNOWN. Two representative ones, with 0 tagged claims each:

- "Legal triggers for DPIA requirements" / **failure_mode** — regulator/statute text states obligations, not how DPIAs go wrong in practice.
- "High-risk processing activities definition" / **failure_mode** — same pattern.

Per the v1 review, `failure_mode` is UNKNOWN in 5/5 areas and `cue` in 4/5 for the GDPR run, and this looks like real signal, not an artefact: normative legal text genuinely does not carry practitioner failure-mode or perceptual-cue knowledge, which is exactly the tacit residual the gap map exists to flag. (Not all UNKNOWNs are this clean — the review also documents UNKNOWN slots that are partition artefacts from near-duplicate planner areas, e.g. PLC "norm" content split across "PLC Fault Diagnosis Methods" and "Systematic Troubleshooting Frameworks.")

## 5. v2: fix-pass code, and where it broke

Between v1 and v2, commit `080b109` ("N2 fix pass after the E-LIVE review") shipped: HTTP status/bot-wall rejection in fetch, PDF text extraction via `pypdf`, per-URL fetch caching, host-kind rules (study/standard/regulator-guidance, curated/open tier), removal of the whole-document ≥25-word quotation rule from independence clustering (keys stay document-level; see row 4), a stricter verifier schema (flags for added content, scope difference, and quantifier/modality/connective difference), extraction-prompt fixes (keep subject/quantifier/modality/jurisdiction; split conjunctive lists), a corrected decoy protocol (real verify payload, strengthening-only mutations, Wilson CI), removal of the pairwise contradiction classifier in favour of cross-cluster re-verification, a new "thin" slot status, and a new `procedure_step` probe.

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

## 6. v3: post-fix live check — NOT RUN (budget)

Both v3 attempts (at `n2-freeze-2`, 17:14:49 and 17:15:08 UTC, one logged call each) stopped at the planner's first call, before any search, fetch or billed call:

```
run failed: LLMUnavailable('PermissionDeniedError("Error code: 403 - ... Key limit exceeded (weekly limit) ...")')
```

At the closeout (2026-09-28) the OpenRouter key had a $5 weekly limit with $0 remaining. The owner decided not to raise it or spend more. No route keeps the registered models without spending: `models.json` fixes Haiku 4.5 and GPT-5.4-mini through OpenRouter, and web search runs through OpenRouter too. **v3 was not run at `n2-freeze-3`.** Amendment 2 P1's live criteria are therefore unmet:
- both domains `complete: true` and passing `verify_run`;
- nonzero `cross_verify` and `decoy` calls;
- every PENDING claim explained by a logged failed call.

That is missing execution, not a failed check.

### 6.1 What stands in for v3 (offline and from existing artefacts)

**Offline audit at `n2-freeze-3`.** No network; the scripted fake model and fixture pages. 412 tests pass at the tag, and 416 with the 4 regression cases added at the closeout.

| Property | Status | Evidence |
|---|---|---|
| No silently pending claims | Implemented and tested, with a gap | Failed verify, cross-verify, decoy, plan, search and extract calls are counted per task (`test_e2e_call_stats.py`). The gap (R6): `complete` and `n3_input` ignore `failed_calls_by_task`, and the injection-flag and same-family skips leave PENDING without a counter entry. |
| Exact-span provenance | Implemented and tested | `verify_run` re-slices every evidence item and fails on a missing or tampered snapshot (`test_smoke.py`). The manual sample re-sliced 71/71 evidence items with 0 mismatches (§6.2). |
| Cross-verification executes | Implemented and tested | The fake run makes 4 `cross_verify` calls: SUPPORTS adds corroboration, REFUTES adds one N1 Contradiction (`test_e2e_contradictions.py`). |
| Independence and corroboration | Implemented and tested | A syndicated copy counts once; corroboration reaches 2 across independent clusters (`test_e2e_corroboration.py`). R3, verbatim copies under 25 words, still stands. |
| Decoys execute | Implemented and tested | Generation and verification run, and the false-accept rate is computed (`test_e2e_decoys.py`). Decoy validity is still self-certified (R2). |
| UNKNOWN stays possible | Implemented and tested | UNKNOWN is written only for a searched, uncovered slot; an all-failed search is "unsought" (`test_e2e_slots.py`). |
| Scope drift not regressed | Implemented; **test added at the closeout** | Any drift flag turns SUPPORTS into insufficient (`test_supports_with_any_drift_flag_is_downgraded_to_insufficient`, which fails if the veto is removed). REFUTES ignores the flags (R4). |
| PDF not regressed | Implemented; **end-to-end test added at the closeout** | A PDF becomes a located, verified claim (`test_pdf_source_yields_a_located_verified_claim`). Lone surrogates are sanitised, and one bad document does not abort the fetch (`test_web.py`, `test_e2e_resilience.py`). |
| Verification completeness | Implemented and tested | Every failed attempt is logged as `api_error`; transient errors retry with backoff (`llm._dispatch_with_retry`, `0f39ed9`). |

**Live evidence for cross-verify and decoys comes only from sealed runs** (exit-status counters only, which §8 lets us read):
- E-PLANT run 1 at `n2-freeze` recorded 276 and 90 cross checks, with 0 decoys.
- E-ABST run 1 logged 3 decoy calls and no cross-verify.
- No unsealed live run shows either.

**The v2(b) PENDING cause, now diagnosed.**
- The run logged 226 verify calls, all ok, and `n_verified` = 226 = 207 supports + 19 insufficient.
- Its code (`080b109`) wrote no log line on a provider error, and it had no `failed_calls_by_task` counter.
- So the 140 PENDING evidence items are 140 verify attempts that raised and left no trace. They form one contiguous tail in extraction order (226 verified, then 140 pending, 0 injection-flagged), which rules out the deliberate skip paths. The last logged call is at 15:18:31Z.
- The 0 cross-verify and 0 decoy calls follow: both run after the verify loop.
- A provider cut-off on the shared key fits the evidence. E-PLANT run 1 (both domains, same key, running at the same time) logged its last calls at 15:18:30 and 15:18:31Z, the same second. The defect itself erased the error text.
- v2(b)'s prompt and schema hashes (plan, extract, verify, decoy) are byte-identical to `n2-freeze-3`, so its verdicts are the current verifier's.

### 6.2 Manual inspection of natural claims

Full record: [`e_live_claim_inspection.md`](e_live_claim_inspection.md). One AI inspector (Sonnet 5) coded the claims, with no gold and no blind second coder; the final review recoded 7 insufficient items. Seed 20260928. **Not held out:** the current verify and extract prompts quote the E-LIVE review's GDPR examples (R8), so the GDPR v2(b) figures, and the comparison with v1, are in-sample.

| Run (verifier) | Sample | Result |
|---|---|---|
| GDPR v2(b) (current) | 25 supported | 22 correct, 3 scope drift: **12% error** (Wilson 95% CI 4–30%) |
| GDPR v2(b) (current) | 10 of 19 insufficient | 7 correctly rejected (jurisdiction dropped), **2 wrongly rejected**, 1 borderline |
| GDPR v2(b) (current) | 10 synthetic | 5 PENDING (all near-verbatim, so stuck, not ungrounded); 5 never located |
| PLC v1 (old) | 20 supported | **30% error** (15–52%): 2 scope drift, 2 added content, 1 wrong, 1 quantifier |
| GDPR v1 (old) | 10 supported | 10% error (2–40%) |
| PLC (current) | — | **No data**: v2 crashed and v3 did not run |

**Findings from the inspection:**
- **Every GDPR scope drift has one shape.** A national Art. 35(4) list item (UK ICO, Slovenia) is generalised to "a DPIA is required" with the jurisdiction dropped. Claims that keep the jurisdiction were all correct.
- **The verifier is inconsistent on that pattern, not biased in one direction.** Some jurisdiction-dropping list items are accepted (3/25 supported) and their siblings rejected (7/10 of the rejected sample).
- **Of all 19 rejections, 14 carry a model drift flag** (`adds_content` 12, quantifier/modality 8, scope 3). **The other 5 have no flag and a quote that is not in the span.** Four of those 5 are near-verbatim "repairs" of an extraction artefact (e.g. "organi zation"). The sidecar keeps only the post-rule verdict, so the model's raw verdict is not recoverable.
- **Precision on supported claims is similar to v1** (GDPR 12% against 10%, overlapping CIs, in-sample). No recall figure exists.

## 7. Findings and the fixes they drove

| # | Finding (v1 review) | Fix shipped | Commit |
| --- | --- | --- | --- |
| 1 | HTTP error pages (403/429/404, bot walls, empty shells) counted as sources | `fetch` rejects non-2xx and near-empty/bot-wall text | `080b109` |
| 2 | Curated PDFs (standards, guides, WP248) rejected outright; only SEO/blog HTML survived | PDF text extraction via `pypdf` | `080b109` |
| 3 | Corroboration structurally zero (370→370, 259→259, 0 merges); paraphrase-based merge never fires | Cross-cluster re-verification pass generates corroboration/contradiction directly | `080b109` |
| 4 | Independence over-merged in GDPR (≥25-word shared-quotation rule unions whole documents transitively; 4 clusters, largest 55%) | Removed the whole-document ≥25-word verbatim-run rule from clustering (`independence_clusters` now unions only on domain-grouping key or ≥0.5 shingle containment; `Source.independence_key` stays document-level, not span-level); host-level keys for multi-institution domains (europa.eu etc.); a separate `span_duplicates` check (still ≥25 words) now collapses matching spans across clusters for corroboration counting only, not document clustering | `080b109` |
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
- **Not a live measurement of the post-fix pipeline.** v3 did not run (§6). The current verifier's live behaviour is known only from GDPR v2(b), whose prompts and schema match `n2-freeze-3` but whose provider-error handling does not. The rest of the current code is checked offline only (§6.1).

## 9. E-LIVE verdict

**INCONCLUSIVE: the provenance core passes, and the post-fix pipeline was never checked live.**

- **Passes (evidence):** exact-span provenance. In v1, every claim traces to a hashed snapshot, an exact re-sliceable span and an other-family verdict (§4.1). The closeout sample re-sliced 71 of 71 evidence items exactly (§6.2).
- **Implemented and tested offline (§6.1):** cross-verify, decoys, independence and corroboration, UNKNOWN, the drift veto, PDF extraction, and logging and counting of failed calls. The R6 gaps remain: failed calls do not affect `complete`, and some PENDING paths are not counted. The drift and PDF regression tests were added at the closeout.
- **Measured live on the current verifier (GDPR only, in-sample):** about 12% scope drift among supported claims, and 2–3 wrong rejections in 10 sampled rejections (§6.2). There is no current-verifier PLC data.
- **Missing:** amendment 2 P1's live check at `n2-freeze-3`. The key budget blocked it, and the owner chose not to spend.
- **Open limitations carried forward** (R1–R10 in `final_adversarial_review.md`):
  - `complete` ignores failed calls (R6);
  - REFUTES ignores the drift flags (R4);
  - cross-verify can count a verbatim copy as independent (R3);
  - decoy validity is self-certified (R2).
