# N2 closeout: engineering PoC complete, full research validation deferred

Date: 2026-09-28. **N2 ENGINEERING MILESTONE: COMPLETE. N2 FULL RESEARCH VALIDATION: DEFERRED** (future research validation). This is an addition to, not a revision of, the registered closeout in [`e_plant_eabst_report.md`](e_plant_eabst_report.md) (verdict: INCONCLUSIVE, Continue closed) and [`e_live_report.md`](e_live_report.md) (verdict: INCONCLUSIVE, provenance core passes).

## Objective

N2's registered purpose (`REORIENTATION.md` §22): build a gated reconstruction pipeline v0 and test it against E-PLANT (planted-falsehood adoption) and E-ABST (false-answer rate on private objectives), each with a pre-registered Continue/Change/Stop gate (`docs/plans/n2-reconstruction-plan.md`, `docs/n2-eplant-eabst-protocol.md`).

## What was built

- `reconstruct/`: a one-way pipeline (plan → search → fetch → extract → locate → verify → contradict → assemble) over `llm.py`, `web.py`, `evidence.py`, `run.py`, `report.py`, populating the frozen N1 types in `residual/` without editing them ([decision 0007](../../docs/architecture/decisions/0007-reconstruction-pipeline.md)).
- 416 offline tests (`uv run --directory reconstruct pytest -q`); no test calls a live model or search.
- Cross-cluster re-verification, independence clustering, decoy generation/scoring, UNKNOWN slot handling, a drift-flag veto on SUPPORTS, PDF extraction.
- E-PLANT/E-ABST harnesses (`reconstruct/src/reconstruct/eplant.py`, `eabst.py`), with scoring fixes D1–D8 (commit `883b52a`).

## Evidence produced

- **End-to-end reconstruction exists and runs on real sources.** E-LIVE v1 (PLC fault diagnosis, GDPR DPIA) completed both domains against the live web: 370/259 claims extracted, 337/204 located, 321/195 verified-supports (`e_live_report.md` §3).
- **Real sources can be acquired.** v1 fetched 35 (PLC) + 20 (GDPR) live sources; v2 added `pypdf` extraction and fetched 25 further GDPR sources including regulator PDFs (§5).
- **Atomic claims can be linked to exact evidence spans.** Every claim carries a `Selector.exact` that re-slices from a hashed, fetched snapshot, never the model's quotation (§4.1 worked example). A closeout manual sample re-sliced 71/71 evidence items exactly (§6.2).
- **Provenance can be represented and verified.** Verification runs through a different model family (`openai/gpt-5.4-mini` vs the `anthropic/claude-haiku-4.5` extractor); cross-cluster corroboration/contradiction is generated directly and tested (`test_e2e_contradictions.py`, `test_e2e_corroboration.py`).
- **Evidence Ledgers can be produced.** Every run emits an N1 `Ledger` plus a run log (model IDs, prompt hashes, cost); see the cost table in `e_plant_eabst_report.md` §3.
- **UNKNOWN/unsupported states can be represented.** UNKNOWN is written only for a searched, uncovered slot (`test_e2e_slots.py`); 14/35 GDPR (area × probe) slots returned UNKNOWN in v1, plausibly real signal — normative legal text carries no failure-mode/cue content (§4.4).
- **Live execution exposed real defects, and they were fixed.** v1 found: HTTP error pages counted as sources, curated PDFs rejected, corroboration structurally dead (0 merges on 370 and 259 extractions), independence over-merging (GDPR collapsed to 4 clusters), verifier scope drift (~20% on PLC), and one false "genuine" contradiction (Art. 35 vs Art. 36 misread as conflicting) — fixed in `080b109` (`e_live_report.md` §7). v2 exposed two more: failed verify/cross-verify/decoy calls silently vanishing behind `complete: true` (140/366 GDPR claims left "pending"), and a `UnicodeEncodeError` PDF crash that aborted an entire fetch phase (0 claims) — fixed in `0f39ed9` (§5, §7 rows 10–11). Harness scoring defects D1–D8 were found and fixed separately (`883b52a`).

## Not demonstrated

- Statistically validated reconstruction quality.
- Final robustness against planted evidence (E-PLANT gated arm sealed and unscored).
- Final abstention performance (E-ABST pipeline arm descriptive only).
- Generalisation across arbitrary domains (two live domains, one run each).
- Prediction of hidden human knowledge (that is N3's question, RQ-B).

## Limitations discovered (recorded, not fixed)

`final_adversarial_review.md` R1–R10: decoy validity is self-certified (R2); cross-verify can count a verbatim copy as independent (R3); scope-flagged REFUTES still become N1 Contradictions (R4); extraction truncation drops whole documents at 8192 tokens (R5); `complete`/`n3_input` ignore `failed_calls_by_task` (R6); retrieval/baseline asymmetry favours the baseline, which sees URLs (R7); host tables and prompts carry E-LIVE domain residue (R8). None of these block the engineering milestone; they are inputs to N3 hardening.

## Deferred validation — FUTURE RESEARCH VALIDATION

E-LIVE, E-PLANT and E-ABST's full gated-arm scoring did not complete. Their **pre-registered protocols, thresholds and stop rules are unchanged and preserved** for later execution — not weakened, not deleted:

- **E-LIVE v3** (post-fix live check at `n2-freeze-3`): blocked at the first model call by the OpenRouter weekly key limit ($5/week, $0 left at closeout); not rerun (`e_live_report.md` §6). Partial evidence stands: v1/v2 runs, the offline audit (416 tests), the manual claim inspection (`e_live_claim_inspection.md`).
- **E-PLANT** (protocol: `docs/n2-eplant-eabst-protocol.md`, registered `3b72fb8`, amendments 1–2): the ungated baseline is complete and preserved — pooled **a_U = 5/24** (21%, Wilson 95% CI 9–40%) against the >60% literature expectation, below the validity floor ⌈24/3⌉ = 8, which closes Continue by the registered rule. The gated arm (run 1, `n2-freeze`) stays **sealed and unscored**, as registered; run 2 was not executed (`e_plant_eabst_report.md` §1).
- **E-ABST**: the raw baseline is complete and preserved — 5/24 private items answered, 19 abstained. The ≥20 pp / ≥20 item margin is reachable only in a narrow arithmetic corner (§2.1). The pipeline arm (run 1) is descriptive only, not a result; run 2, owner/second coding and unsealing did not happen (§2.2).
- Nothing here is reinterpreted as PASS; the registered INCONCLUSIVE readings stand exactly as closed on 2026-09-28 (`PROGRESS.md` N2 record; `e_plant_eabst_report.md` §0).

## Why N2 is sufficient to proceed

N2's purpose for the NOW programme is to hand N3 a working reconstruction mechanism, not to prove that gating beats the ungated model — that is what E-PLANT/E-ABST measure, and remains open. The evidence above shows the mechanism exists, runs on real sources, and survived two rounds of live-web defect-finding. N3 (E-CTA, E-OSS) has its own, independent pre-registered stop/continue rule (`REORIENTATION.md` §22, N3 row) that reads N3's own ΔAUROC test, not N2's gate. Proceeding to N3 on the engineering milestone is an explicit owner exception to the general rule that a NOW item should end on an experiment result rather than a build (R13, `REORIENTATION.md` §22 Decisions); N2's own registered gate is not changed by this and stays INCONCLUSIVE.

## Next step

N3: E-CTA and E-OSS, pre-registered before gold acquisition (`docs/plans/n3-gap-map-plan.md`, `REORIENTATION.md` §22).
