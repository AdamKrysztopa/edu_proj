# N2 final adversarial review (pipeline and procedure, pre-rerun)

Reviewer: final adversarial reviewer, 2026-09-28, branch `n2`. Pipeline code reviewed at tag `n2-freeze-2` (`0f39ed9`). `reconstruct/src/` and `reconstruct/tests/` are unchanged from that tag to HEAD `da197c5` (the run artefacts under `reconstruct/runs/` did change — the v3 runs were added). Nothing under `.private/` was opened. E-PLANT and E-ABST are unscored, so this review covers the code, the harnesses, the procedure and the E-LIVE artefacts, not gate outcomes. Every defect below was confirmed by reading the code, and where marked, by running it. Agreement between subagents was not treated as evidence.

## Verdict

**Do not run the reruns at `n2-freeze-2`.** Four scoring defects can change a gate reading, and the E-ABST blocklist does nothing. None of these fixes touches the pipeline modules (`run.py`, `llm.py`, `evidence.py`, `web.py`), the prompts or `models.json`, so every spec and prompt hash stays the same.

To proceed, in this order:
1. Commit fixes D1–D6 (all in the `eplant.py`/`eabst.py` harnesses), with fixture tests, and tag `n2-freeze-3`.
2. Run E-LIVE v3 at that tag. It must show nonzero `cross_verify` and `decoy` calls with no crash, because neither has ever completed a live call (P1).
3. Commit protocol amendment 2 (P2–P4) before any rerun.
4. Confirm the OpenRouter key has about $11 of headroom (E-PLANT $3, E-ABST $6, v3 about $2).

Then rerun at `n2-freeze-3`.

**The E-PLANT validity floor is already not met: a_u = 5/24, below 8.** So E-PLANT cannot read Continue, and neither can N2 in this round (R1). The reruns are still worth doing, because Stop is still possible and Change names a stage.

## Ranked findings

### Implementation defects: fix before the reruns (harness and scoring only; new tag, no pipeline change)

**D1. E-ABST's primary false-answer rate (FAR) counts synthetic claims as answers.**
- `eabst.py:647-664` (`item_arm_labels`) never filters `meta["label"]`. `build_frame` (`eabst.py:479-481`) puts synthetic overlap units in the frame.
- Confirmed by running it: a single synthetic unit coded false makes the item `pipeline: false`.
- §7 says synthetic claims "are not answers" and are counted only in a sensitivity analysis. The defect raises FAR_pipe, biasing towards Stop.
- **Fix:** at `eabst.py:654`, also `continue` when `meta.get("label") == "synthetic"`. Add the synthetic-counted FAR as a separate, non-gating sensitivity in `score_eabst`.

**D2. The E-PLANT validity floor is computed after the cap rule, on the capped target set.**
- `pool_domains` (`eplant.py:537-538`) counts a_u over the kept targets only. `eplant_decision` (`eplant.py:437,441`) tests `a_u >= ceil(n/3)` on that post-cap n.
- §6 says the floor is "on the baseline's full target set". The recorded reading is 5/24 (not met).
- A cap that drops non-adopted targets can flip the floor to met (e.g. n = 12 with a_u = 5), which reopens Continue against the registration.
- **Fix:** compute `a_u_full` and `n_full` from `score_baseline_arm(target_set.targets, …)` in `score_domain`, carry them through `pool_domains`, and use them only in `validity_floor_met`. All other floors keep the post-cap n.

**D3. A hollow run can be scored as a result.**
- The E-PLANT cap rule ignores extraction failure. `_source_fully_verified` (`eplant.py:264-277`) returns True when a page has no located extractions, so a page whose extract call failed or truncated counts as "fully extracted, every claim verified".
- Neither scorer implements §8's provider-outage rule mechanically.
- In corpus mode with `--areas`, the planner and search make no calls. If the key limit (HTTP 403, which is not retried) hits after the start, every extract call fails, yet the run ends `complete: true`. E-PLANT would then score a_g = 0, e = 0 and read "Change: under-exposed". E-ABST items would silently become abstentions, lowering FAR_pipe.
- **Fix:**
  - In `_source_fully_verified`, return False unless `sidecar["sources"][sid].get("extract_ok")` is true.
  - Add one shared check, `provider_outage(run_dir)`: true when `calls.jsonl` has any `outcome == "api_error"` line and `sum(stats.failed_calls_by_task.values()) > 0`. It is conservative: a retried transient error plus an unrelated content failure also counts.
  - Apply §8 through that check: rerun once, then an E-PLANT domain is inconclusive, or an E-ABST item is excluded in `build_frame` before unsealing.

**D4. The E-ABST "extracted zero documents" counter counts fetches, not extractions.**
- `is_zero_extraction_or_capped` (`eabst.py:872-879`) tests `n_sources_fetched == 0`.
- A run that fetched three pages and extracted none (truncation, or an outage) is not counted towards the ">4 → inconclusive" rule.
- **Fix:** return True when `sum(1 for s in sidecar["sources"].values() if s.get("extract_ok")) == 0`.

**D5. The E-ABST blocklist is inert.**
- `PIPELINE_BLOCKLIST = ("github.com/AdamKrysztopa/*",)` (`eabst.py:92`) is matched by substring (`run.py:125-128`). No URL contains `*`.
- Confirmed by running it: `github.com/AdamKrysztopa/edu_proj/...` and `/informant-video` are both not blocked.
- `edu_proj` is public and names the repository. So its pages can be fetched, which then triggers the mechanical exclusion and shrinks n_included towards the 20-item floor.
- **Fix:** at `eabst.py:92`, use `"github.com/AdamKrysztopa/"`. This is the registered prefix intent, with no pipeline change.

**D6. The exposure CLI prints key-derived terms.**
- `_cmd_exposure` (`eabst.py:993-994`) prints `t.term` for every term, including the `--terms-file` identifiers taken from the key.
- §7 says the script "never displays the key".
- **Fix:** print `term {i}: HIT/NO-HIT` for extra terms.

**Fix before scoring (these do not block the reruns):**
- **D7. Contradiction-flag recall is not the registered measure.**
  - `contradiction_flag_recall` (`eplant.py:348-366`) checks no values, and the pairs file has no value fields.
  - `_evidenced_by` counts cross-verify evidence, so a claim from page C that was re-verified against page B counts as "evidenced by B".
  - As coded, it is an upper bound on a page-level link rate. Either add `value_a`/`value_b`/anchors to the sealed pairs and require `matches_value` on each side, or report it under that name.
- **D8. The source-level sensitivity counts refutations.** `anchored_criterion_claim_from` uses `_evidenced_by` over all evidence (`eplant.py:157-172`). So a true claim that the planted page's span REFUTES counts as source-level adoption of the plant. Use `c.supporting`.

### Protocol issues: amendment 2, committed before any rerun

**P1. Cross-verify and decoys have never completed a live call.**
- v1 predates them. v2(a) crashed. v2(b) logged 0 `cross_verify` calls and 0 decoy calls, and left 140 of 366 located claims PENDING. v3 got one 403 each.
- Both freezes (`n2-freeze`, `n2-freeze-2`) were declared before a clean live run, which breaks lesson L1.3 twice.
- Each unit gets one rerun, so run E-LIVE v3 at the rerun tag first. `research/n2/e_live_report.md` §9 already recommends this.

**P2. The rerun mechanics are unregistered, and each gap can waste the one rerun.**
- **E-PLANT output directory:** `eplant run --out` writes into the given directory verbatim. `CallLog` appends, and `ledger.json` and `sidecar.json` are overwritten. Reusing the first run's `--out` destroys the sealed first run and mixes the logs.
- **E-ABST skip and cap:** `run_pipeline_all` skips any item that already has a `ledger.json` (`eabst.py:357`). It also counts every `*.jsonl` under `--out` towards the $6 cap (`eabst.py:266-273`). If the first runs are left in place, or moved to a subfolder of `--out`, items are "skipped", excluded and counted.
- **Register all of the following:**
  - rerun into fresh directories, carrying over only the raw-arm `baseline.json` and `status.json` entries;
  - each attempt has its own cap ($4.00 / $6.00), and first-attempt costs are reported;
  - an attempt blocked before any billed call (the v3 pattern) is not a rerun;
  - a code crash (`complete: false`, reason starting "run failed:") triggers a rerun. The catch-all at `run.py:602-604` writes a valid `ledger.json` that passes `verify_run`, so §8 as worded would score a crash as a result.

**P3. The E-ABST per-item cap of $0.25 probably binds now.**
- Amendment 1 added cross-verify and 30 decoys per run. v2(b) measured $0.025 per extraction and $0.00106 per verify call.
- Three documents per item (≈$0.075 of extraction), plus about 45 verify calls, about 70 cross-verify calls and 30 decoys, comes to roughly $0.20–0.30 per item.
- A cap hit sets `complete: false`, which counts as "capped". More than 4 capped runs makes E-ABST inconclusive for a reason unrelated to answers.
- Before the rerun, read only the first attempt's per-item cost and `complete` flags from `calls.jsonl` and `sidecar.json`, which §8 permits. If cap hits are common, register a new per-item cap before any data.

**P4. Deviations appear only in PROGRESS.md; record them in the protocol file.**
- **Gold claims (23/24 verified):** decide now that the target without owner-verified gold is excluded from both arms and from the floor set. 5/23 still misses the floor (8).
- **Conflict pairs (4/6 confirmed):** §5's denominator and the "below 3/6" Change reading must become "confirmed pairs" and "below 50%". Do not replace the rejected pairs.
- **Gold-quote extension (two targets, full table rows):** give the old and new `gold_candidates` sha256, and when it happened relative to the first runs. The committed hash `3ff69753…` may be stale. Gold claims carry only `criterion_ids`, so the arithmetic is unaffected.
- **Key-print incident:**
  - One item's accept variants entered the agent transcript. That same agent session later edited the extract and verify prompts (`080b109`).
  - PROGRESS's "no model, pipeline or scorer saw it" is true of models, not of pipeline development.
  - Name the item (the owner can identify it without printing) and pre-register a sensitivity that excludes it.
- **Exposure check:** the §7 identifier-term searches were either not run (the `run_exposure_check` docstring admits the gap) or were printed (D6). State which.
- **Planted hostnames:** 2 of the 12 planted hostnames resolve in DNS. `safeplateguide.net` is on GoDaddy nameservers; `familyfoodwise.com` is Sedo-parked. §1 requires "fictional, non-resolving". Corpus mode never fetches them and no pipeline model sees URLs, but the E-PLANT baseline does see them.
- **Baseline prompt:** the E-PLANT baseline system prompt adds "Use only what the documents state." (`eplant.py:618-619`) to the registered instruction.
- **Areas deviation (already recorded):**
  - The public manifest, whose planted URL slugs reveal topics (`…/leftovers-after-a-power-cut`, `…/accelerators-and-protection-periods`), was committed before the areas (`d3e0bb4` before `bf35207`).
  - Areas bound cross-verify pools, so they affect contradictions and therefore a_g.
  - The areas are generic, so the risk is low but real. Disclose it.

### Research limitations: report, do not fix now

**R1. E-PLANT is nearly uninformative on its main question.**
- The plants persuaded the ungated model on 5 of 24 targets (21%), against the >60% literature baseline.
- Continue is closed. Only Stop (c > b, one-sided p < 0.05, e.g. b = 0 and c ≥ 5) or Change can follow.
- The report must say that N2 cannot read Continue this round, whatever the pipeline does.

**R2. Decoy validity is self-certified.**
- `decoy_is_valid` (`evidence.py:593-598`) checks only that the text differs and the rationale is non-empty. The rationale comes from the decoy generator, which is the extractor's model.
- The review's MUST 4 required validation by a third family or the owner. `080b109`'s "a validity check" overstates what was built.
- So decoy false-accept rates are not an estimate of verifier validity.

**R3. Cross-verify can count a verbatim copy as independent corroboration.**
- `span_duplicates` (`evidence.py:393-425`, used at `run.py:442-460`) compares span to span at 25 words or more. Most spans are 6–80 words, often under 25, so a derived copy with shingle containment below 0.5 is never caught.
- Merges of identical assertions bypass the check entirely.
- This does not affect any E-PLANT or E-ABST gate, since adoption ignores corroboration except in the lenient sensitivity. It inflates `covered` slots and corroboration for N3.
- Two documents misdescribe the code:
  - ADR 0007 rule `independence-before-corroboration` still lists the 25-word rule as a union-find link.
  - `e_live_report.md` §7 row 4 claims "span-level independence keys", but `Source.independence_key` is still document-level.
- Fix before N3: test each candidate span verbatim against the claim's own source texts.

**R4. Scope-flagged refutations become N1 Contradictions.**
- REFUTES ignores the drift flags (`run.py:485, 493-501`). A REFUTES with `subject_or_scope_differs = true` is the Art. 35/36 class of false positive.
- Adoption is protected, since it needs a link to a claim matching the true value. Recall and N3's `n_contradictions` are not.
- Report scope-flagged REFUTES separately; `cross_checks` records the flags.

**R5. Extraction output truncation drops whole documents.**
- At `max_tokens` 8192 (`llm.py:205`), v2(b) lost 5 of 25 documents, including a 17,455-character page, which is under E-PLANT's 20,000-character cap.
- This is a content failure, not a rerun trigger. With D3 fixed, the cap rule excludes the affected targets. Report the count.

**R6. Failures that are counted but still not surfaced (N3-blocking, not rerun-blocking):**
- `complete` and `n3_input` ignore `failed_calls_by_task` (`run.py:657-661`). v2(b)'s pattern would still read `complete: true` and `n3_input: true`.
- Cross-verify failures are counted only in aggregate (`run.py:482-484`), with no claim id.
- Decoy-verify failures are counted and logged as `verify` (`run.py:587, 595-596`).
- UNKNOWN needs only one extracted document per area (`run.py:289-291, 518`), so documents lost to extraction failure do not block it. PROGRESS's "only once fully … extracted" overstates this.
- Extractor area names are not constrained by an enum. An unmatched name silently drops its claim from cross-verify, slots and decoys. There were 0 such cases in E-LIVE, but the risk is higher in E-ABST, where the area name is the whole question.
- A budget hit during cross-verify is invisible to the E-PLANT cap rule.
- `search` logs a served-model mismatch as `ok` before raising (`llm.py:265-271`).

**R7. Retrieval and the baseline are asymmetric.**
- Retrieval is chosen by the generator family: the planner's `url_citation` annotations.
- The E-PLANT baseline sees URLs, and 6 hostnames per domain are recognisably invented. Pipeline models never see URLs.

**R8. Domain residue in the pipeline:**
- The host tables are tuned to E-LIVE: UK/EU data-protection regulators, PLC forums. So food and concreting regulators fall to `default-documentation/open`, and `source_kinds` is constant again.
- The verify and extract prompts quote the review's named E-LIVE claims ("most essential", "the UK regulator's list"). E-LIVE claims are therefore no longer held-out for any verifier re-measurement.

**R9. Dead code and single-implementation abstractions (clean up after N2):**
- `web.write_raw`, `read_raw` and `fetch_all`; `evidence.context_window`.
- `MergedAssertion.conflict` is computed and never persisted.
- `_verdict_from_result(allow_refutes)` is always True, and False would skip the quote check.
- The provider indirection has one provider: `KEY_ENV`, `RoleConfig.provider`, and `_default_client` ignoring `provider`.
- There are three `wilson_ci` copies with different n = 0 results.
- The `--models` default is cwd-relative (`eplant.py:876`).
- Web mode never snapshots raw bytes, yet `verify_run`'s docstring says it "re-extracts".
- `verify_run` covers cross-verify evidence, but does not rehash snapshots against their filenames or check the Source-to-snapshot binding.

**R10. Reports claim slightly more than E-LIVE shows.**
- `e_live_report.md` headlines "Pass as a sanity gate", yet the code at the freeze has zero live data. The body's §8 and §9 hedge this correctly.
- Rename the verdict "provenance core passes; post-fix pipeline unchecked".

## Checked and clean

- **No same-family verdict anywhere.** Verify, cross-verify and decoy verification all use `openai` against the `anthropic` generator. `run.py:377` and `residual.claims._exclusion` guard this twice. The plant author is a third family.
- **`Selector.exact` is always a slice of our own text.** Cross-verify and decoys reuse existing selectors. `verify_run` re-slices every evidence item, including cross-verify evidence.
- **No model string reaches the ledger.** Neither mutated decoys nor verifier quotes are written there. UNKNOWN placeholders are software templates.
- **The provenance record is not URL-only.** Evidence requires a span located in text we fetched.
- **The model boundary holds.** 100% of logged calls report the configured served model, and every billed call carries a cost, so the budget works. Provider knowledge is confined to `llm.py`, apart from the `web:openrouter-exa` corpus label.
- **The fabrication marker never reaches a model.** HTML comments are dropped (confirmed by running it).
- **Contradiction pairs are sorted by N1,** so the link check is order-safe.
- **The rerun is legitimately triggered.** The decision came from logs, before any score, and the fix is named in the protocol.
