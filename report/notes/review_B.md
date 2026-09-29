# Review B (technical / architecture), round 1

Reviewer B, 2026-09-29. Scope: whole report (`main.tex`, `sections/00`–`29`, `A`–`G`), figure sources, draft PDF, against code (`residual/src`, `reconstruct/src`, `gapmap/src`), `reconstruct/models.json`, `reconstruct/runs/*`, `research/n3/*/gapmap.json`, ADRs 0006–0008, `research/n2/*.md`, `research/n3/README.md`, git log. No other review file was read.

Summary: **0 CRITICAL, 7 MAJOR, 23 MINOR.** The headline numbers are almost all right. The main problems are (a) provenance claims stronger than the code supports, (b) a silent cap on the map that the report never mentions, (c) a validation design that needs an area-level score the code does not produce, (d) figures that draw unbuilt parts as built, and (e) a replay command that fails or overwrites committed files.

## What I ran (all offline; nothing written under `research/`)

| Command | Result |
|---|---|
| `uv run --directory residual pytest -q` | 268 passed, 0.70 s |
| `uv run --directory reconstruct pytest -q` | 416 passed, 1.26 s |
| `uv run --directory gapmap pytest -q` | 172 passed, 116.9 s |
| `uv run --directory instrument pytest -q` | 311 passed, 9.9 s |
| `uv run python -m reconstruct.verify_run runs/<run>` (PLC v1, GDPR v1, GDPR v2) | `ok` for all three: every one of 337 + 206 + 366 = 909 evidence items re-slices exactly from its local snapshot |
| gapmap replay, fresh empty `--out` in scratchpad | **fails**: `gapmap.judge.JudgeCacheMiss: no cached judgement ... pass --judge ollama` |
| gapmap replay, `closure_judgements.json` copied into scratch `--out` first, exact domain strings, `--sidecar` for all three, `--sibling` for the GDPR pair | `gapmap.json`, `gapmap.md`, `closure_judgements.json` byte-identical to the committed files for all three maps |
| Script that re-used `gapmap.__main__._primary_records`, `rank.merge` and `rank.build` with the replay cache | PLC: 24 HYP records after merge, 9 in the map (see B3) |

---

## MAJOR findings

### B1. MAJOR — "Every claim is tied to an exact span" and "memorized content cannot enter as a claim" are false
- **Where:** `00_executive_summary.tex:23` and `:49`; `05_scope.tex:8–9`; `06_architecture.tex:151`; `09_n2.tex:17`; `15_threats.tex:47` (Now column) and `:104–105`.
- **Problem:** An extraction whose quote cannot be located is **not** dropped. It enters the ledger as a claim with no evidence and is labeled `synthetic_extrapolation` (ADR 0007, rule `span-is-ours`: "the claim stays a synthetic generation"). The same goes for located claims whose verdict is `pending` or `insufficient`. So model-generated content, including memorized content, does enter the ledger as claims. The label keeps it from acting as a criterion, and the lenses read only criterion-labeled claims. But the text says it cannot enter at all.
- **Evidence:** sidecar and ledger label counts. PLC v1: 375 claims, 49 synthetic + 5 unknown. GDPR v1: 271 claims, 64 + 14. GDPR v2: 523 claims, **305** + 15. That makes 452 of 1,169 claims (39%) with no supporting span. Unlocated extractions: 370−337 = 33, 259−206 = 53, 523−366 = 157. Appendix C's own example claim, re-labeled through `residual`, reads `LABEL synthetic_extrapolation`.
- **Fix:** Write "every *criterion-labeled* claim (`literature_supported`) is tied to an exact span; claims the extractor produced without a locatable span stay in the ledger labeled `synthetic_extrapolation` and never feed a lens or a gate". In 15:104 replace "memorized content cannot enter as a claim" with "memorized content can enter only as `synthetic_extrapolation`, which no lens or gate reads; a located claim can still carry verifier drift (12–30% sampled)".

### B2. MAJOR — Lenses, anchors and even question "quotes" run on the extractor's paraphrase, not the verbatim span; "no model-written text" is false
- **Where:** `10_n3.tex:143–148` ("every quote is copied, not paraphrased"); `11_demonstrations.tex:6`, `:63`, `:199`, `:207–210` ("a template question with no model-written text"); `12_demonstrates.tex:149`; `B_lenses.tex` DIAG template (`{effect}`).
- **Problem:** Several pieces run on the model-written `assertion` rather than the verbatim span:
  - every lens firing regex;
  - the stem index (`link.py:50`);
  - every anchor;
  - the judge's seed text (`semantic.py:235`).

  Knowledge types, which gate DIAG, GUARD and HEDGE, are assigned by the extractor. `_best_sentence` in `lenses.py:107–131` falls back to `c.assertion` in three cases: when a claim has no span sentences, when a sentence opens with a bare referent, and when it has fewer than 5 words. The template then wraps that paraphrase in quotation marks as "Sources prescribe: …".
- **Evidence:**
  - **Trace 3 (`g-1b1e68dc5d39`).** The committed question says `Sources prescribe: "The nature of processing in a DPIA should include details about data collection, storage, usage, access, sharing, processors, retention periods, security measures, new technologies, and novel processing types."` That is the assertion of claim `c-6370fb5b7eeb5c13`. Its actual span is `"The nature of the processing is what you plan to do with the personal data. This should include, for example: how you collect the data; …"`. The anchor "measures, new technologies, and novel processing types." is the tail of the same assertion.
  - **Trace 1 and the failure trace.** The DIAG anchor is `_diag_anchor()` = the seed *assertion* trimmed to 80 characters (`lenses.py:364–375`). "Loose terminal connections are a common cause of intermittent PLC faults and" is a truncation of the assertion "…and should be checked during troubleshooting." The span says "Loose terminals cause many intermittent faults…". It is not "a mid-sentence fragment extracted from a source" (11:63, 11:199).
- **Fix:**
  - State once, in 06 or 10, that the lenses and the judge read the extractor's assertion and knowledge type, and that spans are kept for display and for quotes.
  - Replace "every quote is copied" with "quotes are the most relevant verbatim span sentence, falling back to the extractor's assertion when no usable sentence exists (Trace 3 is such a case)".
  - Fix the explanation of the DIAG defect: the anchor is the seed assertion cut at 80 characters.
  - Add the assertion-fallback defect to Appendix D, and add "question text may quote model paraphrase as a source" to 15 (construct validity).

### B3. MAJOR — An unreported cap silently drops most PLC hypotheses; "16 gap candidates" is a display count
- **Where:** `00_executive_summary.tex:50`; `10_n3.tex:170–197` and the fig07 caption (`10_n3.tex:202–205`); `12_demonstrates.tex:123–124`; `13_not_demonstrated.tex:26`; `14_interpretation.tex:31`. No section mentions the cap.
- **Problem:** `rank._cap` keeps at most `MAP_TOP_N = 12` records, `MAP_PER_LENS = 3` per lens and `MAP_PER_AREA = 4` per area (`config.py:88–90`). HYP records beyond those limits are removed from `map` and are **not** moved to `retrieval_gaps`, so they appear nowhere in the output.
- **Evidence:** replaying with the committed cache, PLC produces 43 non-closed lens records, which become 24 HYP after merge (RESULT 13, WHY 8, DIAG 2, GUARD 1). Only 9 are in the map (RESULT 3, WHY 3, DIAG 2, GUARD 1). The remaining 15 (10 RESULT, 5 WHY) are in neither array. GDPR v1 (1) and v2 (6) are not affected.
- **Consequences for the text:**
  - "16 gap candidates" and "13 of 16 partial" describe the capped display, not what the pipeline produced (PLC 24).
  - The fig07 caption "Most fired candidates do not survive as hypotheses" is only half right: in PLC, 24 of 56 firings survive as HYP before the cap.
  - The cap is per lens, so it also shapes the lens mix reported as "domain texture".
- **Fix:** Report both counts: "HYP after merge 24 / 1 / 6; shown after the display cap (12 total, 3 per lens, 4 per area) 9 / 1 / 6". Add the merge and cap stage to fig07. Note in 17 (V1–V5) that any area score must be computed over the uncapped set.

### B4. MAJOR — The decisive tests need an area-level score that the code does not produce, and the report never specifies one
- **Where:** `17_validation.tex:28–31` (L2), `:180–200` (V2), `:205–225` (V3), `:262–300` (V5b strata "top of the gap map (G)"); `22_roadmap.tex:48`; `23_workpackages.tex` (WP tasks); `16_residual.tex:93` ($P(\text{residual present}\mid\text{area})$).
- **Problem:**
  - ΔAUROC is defined over areas. `gapmap` emits a capped list of lens candidates keyed by claim anchors, plus one CONTROL slot. It emits no per-area score.
  - `residual.GapMapPrediction(area_id, p_missing, …)` exists as a type, but nothing produces it (grep in `gapmap/src` and `reconstruct/src`: 0 hits).
  - The gapmap CLI has no `--areas` input. `docs/plans/n3-gap-map-plan.md` §17 says planner areas (about 5 per task) "give AUROC no power" and that N3 must supply `--areas`. Its §37 warns that on World A the live features are mostly size and density, "so ΔAUROC ≈ 0 by construction".
  - The report mentions area partitions and "live vs dead features" (V0), but never the scoring function itself. That function has to answer several questions:
    - how candidates, their states (open/partial), retrieval-gap categories and breadth scores combine into $p_{\text{missing}}$ per area;
    - how areas with no candidates are scored;
    - how the cap is removed.
- **Fix:** Add a paragraph to 17 ("Rules common to every study") and a task to WP1/MS1. It should require:
  1. a pre-registered area-scoring rule from uncapped candidates to `GapMapPrediction`, frozen with `config_sha256`;
  2. an `--areas` input at task-step or KC grain;
  3. a check on the PoC ledgers that the score is not a monotone function of area size or density (the B3 and ρ = 0.91 issue).

  State plainly that this component is not built.

### B5. MAJOR — The architecture's showcase run is the defect-compromised run, and the post-fix cross-verify and decoy stages have never run live
- **Where:** `06_architecture.tex:75–95` (stage list) and `:116–120` ("A real completed run … produced 523 claims (… `synthetic_extrapolation`: 305 …) … $1.00 across 262 logged calls"); `09_n2.tex:15–17` (ten stages); `fig04`.
- **Problem:**
  - Run `20260928T145943Z-bc1cc9a30a02` is GDPR v2, the not-admissible run. 140 verify calls failed silently, which is why 305 of its 523 claims are synthetic. Its sidecar shows `cross_checks: []`, `decoys: []` and `decoy_by_type.*.attempted = 0`. Its 262 calls include no cross-verify and no decoy call.
  - The v1 runs used the older pairwise `contradict` stage (`calls.jsonl` tasks: `contradict` 50/40), which `run.py:432` says was replaced.
  - PLC v2 crashed, and v3 was blocked.
  - So the cross-verify stage and the current decoy stage have never run on live data.
  - A reader will take 305/523 synthetic and $1.00 as normal behavior.
- **Fix:**
  - In 06, label the example "GDPR v2 (defect-compromised: 140 pending verdicts, hence 305 synthetic; not N3-admissible)", or use PLC v1 instead (375 claims, 321 supported, $0.679).
  - Mark cross-verify and decoys (current form) as "implemented and offline-tested; never run live" in the stage list, fig04 and the fig11 "contradiction" box.

### B6. MAJOR — Figures draw unbuilt parts as built, against the binding solid/dashed convention
- **Where:**
  - `figures/src/fig02_model.tex:100–101`: the edge from triage to retrieval gap to "search / verify more" to `recon` is `flowimpl` (solid).
  - `figures/src/fig11_platform.tex:72`: "Contradiction records" is `implemented`.
  - `fig11_platform.tex:52`: "Weft (optional)" is `planned`, which that figure uses for "next research stage".
- **Problem:**
  - No code feeds retrieval gaps back into `reconstruct`. RG records are an output list only, so the loop is future work.
  - `18_platform.tex` tab:components rates Contradiction analysis as "Next research stage", and the post-fix cross-verify never ran live (B5).
  - The Weft subsection says integration is not justified now, and at most a candidate-passage provider in an organizational pilot (S4, long-term). A dashed next-stage box overstates that.
- **Fix:**
  - fig02: make the retrieval-to-reconstruct edge `flowplan`, or label it "manual re-run (not automated)".
  - fig11: make contradiction `planned` with the note "stage coded; never run live", or align the table and the figure.
  - fig11: make Weft `longterm`, or drop it.

### B7. MAJOR — The reproducibility appendix gives a command that fails or overwrites committed files, and misdescribes the config
- **Where:** `E_reproduce.tex:27–42`, `:74–76`, `:84–91`.
- **Problems:**
  1. **Command.** `--out ../research/n3/<name>` writes into the committed folder. `j.save()` rewrites `closure_judgements.json`, which is a repo mutation. Pointing `--out` at any fresh directory fails with `JudgeCacheMiss`, because the cache path is `<out>/closure_judgements.json` (`__main__.py:110–112`). I reproduced the failure.
  2. **Arguments.** Byte identity needs the exact `--domain` strings: "PLC intermittent-fault diagnosis", "GDPR DPIA (run v1)" and "GDPR DPIA (run v2)". It needs `--sidecar` for all three runs, `--sibling` for the GDPR pair only, and no sibling for PLC. The appendix gives placeholders and bracketed options.
  3. **Config.** "reads the frozen `config.py`" (E:39) and "the same frozen lens configuration was applied … so any difference … comes from the ledgers, not from per-domain tuning" (E:74–76) are wrong. The config is *hashed*, not frozen (CLAUDE.md: it "must be hash-frozen before any gold"). It was tuned in-sample on all three ledgers jointly (README Limitations).
  4. **Snapshots.** "was run against the snapshots while they still existed locally and cannot be repeated" (E:89–91) is wrong for the author's machine: the snapshots are present (git-ignored, not deleted). `verify_run` re-slices all 909 evidence items successfully (see "What I ran").
- **Fix:** replace the block with the tested commands:
  ```
  OUT=/tmp/gapmap-replay; R=reconstruct/runs
  for d in plc gdpr_v1 gdpr_v2; do mkdir -p $OUT/$d; cp research/n3/$d/closure_judgements.json $OUT/$d/; done
  cd gapmap
  uv run python -m gapmap --ledger ../$R/20260928T133336Z-59ec876b3d7e/ledger.json --sidecar ../$R/20260928T133336Z-59ec876b3d7e/sidecar.json --domain "PLC intermittent-fault diagnosis" --out $OUT/plc
  uv run python -m gapmap --ledger ../$R/20260928T135354Z-eb840a85b7d1/ledger.json --sibling ../$R/20260928T145943Z-bc1cc9a30a02/ledger.json --sidecar ../$R/20260928T135354Z-eb840a85b7d1/sidecar.json --domain "GDPR DPIA (run v1)" --out $OUT/gdpr_v1
  uv run python -m gapmap --ledger ../$R/20260928T145943Z-bc1cc9a30a02/ledger.json --sibling ../$R/20260928T135354Z-eb840a85b7d1/ledger.json --sidecar ../$R/20260928T145943Z-bc1cc9a30a02/sidecar.json --domain "GDPR DPIA (run v2)" --out $OUT/gdpr_v2
  cd ..; for d in plc gdpr_v1 gdpr_v2; do cmp $OUT/$d/gapmap.json research/n3/$d/gapmap.json && cmp $OUT/$d/gapmap.md research/n3/$d/gapmap.md; done
  ```
  Also:
  - add `uv run --directory reconstruct python -m reconstruct.verify_run runs/<run>` (it needs the local, git-ignored snapshots, so it cannot run from a fresh clone);
  - say "hashed (not yet frozen) configuration, tuned in-sample on these three ledgers";
  - fix the time for instrument: about 10 s here.

---

## MINOR findings

**B8. MINOR — pytest-archon does not exist in this repository, and `reconstruct` has more dependencies than stated.**
- **Where:** `06_architecture.tex:8–9`, `07_evidence_model.tex:163`, `A_claims.tex` E10.
- **Evidence:** `grep -rl archon */tests` finds nothing. The architecture tests are hand-written `ast` import checks (`*/tests/test_architecture.py`). "pytest-archon#…" is only the binding notation in the ADRs; ADR 0001:63 says the repo has no pytest-archon configuration. `reconstruct` also depends on `httpx`, `openai`, `tldextract` and `pypdf` (`pyproject.toml`), which contradicts "stdlib, pydantic, and any package to its left, and nothing else".
- **Fix:** Say "plain pytest architecture tests". Give reconstruct's actual allow-list.

**B9. MINOR — The donor-null description is wrong in two places.**
- **Where:** `10_n3.tex:78` and `:79`, `:215`.
- **Evidence:** `CLOSURE_NULL_DRAWS = 200` (`config.py:107`), not 1,000. GDPR v2 observed 11 is *above* its null mean 8.08, though inside [5, 12].
- **Fix:** Write "200 draws". Replace "at or below the null mean on every ledger" with "within or below the null range on every ledger (PLC below it)".

**B10. MINOR — The fair control is described loosely in several places.**
- **Where:** `00_executive_summary.tex:61`, `12_demonstrates.tex:22–23`, `04_approach.tex:160`.
- **Problem:** These say each candidate's evidence was "swapped for a neighbor's". In the code, the seed's own sentences stay in both arms and only other-source sentences are swapped (`checks.py:156–171`). The "closure rate" counts closed *or* partial. The pass rule is own − control ≥ 0.20. `10_n3.tex:89–91` is right.
- **Fix:** Use the 10 wording, or cross-reference it.

**B11. MINOR — The wrong file is cited for `confidence_rubric`.**
- **Where:** `10_n3.tex:137`, `13_not_demonstrated.tex:91`, `18_platform.tex` components table ("rank.py").
- **Evidence:** `confidence_rubric` is in `gapmap/src/gapmap/record.py:125`. The score is A + B − P − Q, where A buckets k_topic.
- **Fix:** Cite `record.py`, and describe the rubric in one clause.

**B12. MINOR — The RG-SIBLING record that keeps a question is a code defect, not a design choice.**
- **Where:** `10_n3.tex:125–127` ("since the sibling run already supplies an answer worth checking against"); `F_glossary.tex:136–138` and `B_lenses.tex:222` say "never".
- **Evidence:** `checks.apply_sibling` changes `category` to RG-SIBLING without clearing `hypothesis` or `question`. GDPR v2 `g-9a3380e70b76` (DISC) keeps both. This violates ADR 0008 rule `retrieval-gaps-never-hypotheses`.
- **Fix:** Call it a defect, add it to Appendix D, and make the glossary and B agree.

**B13. MINOR — PLC's RG-SIBLING count is not zero.**
- **Where:** `10_n3.tex:192`.
- **Evidence:** PLC had no sibling run, so the count is not applicable (the README writes "–").
- **Fix:** Write "n/a".

**B14. MINOR — The traces contain several factual slips.**
- **Where:** `11_demonstrations.tex`.
- **Evidence:**
  - Trace 1 says "7 rival causes" (line 37), but the record has 5 `rival` items. 7 is k_topic, the number of keys. The table's own line 40 says 5.
  - The claim shown, `c-0ae2bfae93f15f20`, is a *rival*. The seed is `c-d7bce12d16755797`.
  - The hypothesis is quoted with an edited bracket "[none of the five]", yet line 6 says the traces are "copied exactly". The real text reads "found a sign for the following … (no sign found)" for each rival. That wording is itself confusing and worth flagging as a template defect.
  - Trace 2: "three claims name 'relevant controller'". In fact 2 seed claims do, both from one key (legislation.gov.uk). The span shown comes from a topic claim that does not contain the term. "All three sources are regulator-authored PDFs" is wrong because one is legislation.gov.uk HTML.
  - Trace 3: "three independent sources". The ledger has 2 keys, because ICO and CNPD share `ind-s-505312a82b58a1e4` (the old 25-word over-merge rule).
- **Fix:** Correct the numbers, and quote the hypothesis text verbatim.

**B15. MINOR — The fig06 caption contradicts its own data.**
- **Where:** `09_n2.tex:200–202`.
- **Evidence:** Loss from extraction to location is PLC 8.9% against GDPR 21.2%. Loss from location to support is about 4.7% against 4.4%.
- **Fix:** Write "GDPR loses more than twice the share of PLC between extraction and location; both lose about 5% between location and support."

**B16. MINOR — The "Located" column mixes two definitions, and "claims" is mixed with "evidence items".**
- **Where:** `09_n2.tex` Table `tab:n2-elive`; `09_n2.tex:123` and `A_claims.tex` E23 ("140/366 claims").
- **Evidence:** PLC and GDPR v1 use sidecar `n_located` (337, 204). GDPR v2 uses located extractions / evidence items (366; sidecar `n_located` is 351; GDPR v1's extraction list gives 206). The 140 are pending *evidence items*.
- **Fix:** Use one definition, and say "evidence items".

**B17. MINOR — Appendix C mislabels one claim and one hash.**
- **Where:** `C_records.tex:40–41` and the freeze-file paragraph.
- **Evidence:** The pending claim would be `synthetic_extrapolation`, not `unknown` (verified with `ClaimRecord.label`). `features_sha256` hashes the `AreaFeatures` field-name tuple, not "the field types a claim may carry". `07_evidence_model.tex:159–160` has it right. The agent id is `anthropic/claude-haiku-4.5`, which the excerpt trims silently.
- **Fix:** Correct all three.

**B18. MINOR — Section 06 contradicts itself and Section 09 on completeness and the budget.**
- **Where:** `06_architecture.tex:167–170` and `:160–165`.
- **Evidence:** 06 says `failed_calls_by_task` means a loss "cannot hide … behind a `complete: true` flag". 09:217–219 says the opposite, and the code agrees with 09: `complete` is not derived from failures, and `n3_input = complete` (`run.py:206`, `:660`). Separately, 06:163 offers the provider's $5 key limit as proof of the in-code `Budget` safeguard. That limit was OpenRouter's HTTP 403, not `BudgetExceeded`.
- **Fix:** Align 06 with 09, and separate the two budget mechanisms.

**B19. MINOR — The status of the judge-family rule and of ADR 0008 is overstated.**
- **Where:** `06_architecture.tex:139`; `18_platform.tex` "Key architectural decisions" ("The first four are already enforced in the PoC's code").
- **Evidence:** 06:139 calls the judge "model family (local)", but "local" is a deployment, not a family (Qwen). ADR 0008 has `status: proposed`, and its judge-family rule is `verification: review` with "no test". In 18, decision #2 (typed sidecar) is marked `\evfut` and #4 is enforced only by review.
- **Fix:** Say that 0008 is proposed. Write "two of the five are enforced in code".

**B20. MINOR — The scope of the absence check is overstated.**
- **Where:** `00_executive_summary.tex:27` ("stated anywhere else in the ledger"), `04_approach.tex:118`; `10_n3.tex:88` ("up to 12 retrieved sentences").
- **Evidence:** The judge sees a *lexically retrieved* subset, capped at 8 A + 4 S sentences per probe (`config.py:129–130`). DIAG probes each rival, so Trace 1 reports 34 sentences and the failure trace 50.
- **Fix:** Write "in the sentences a lexical retriever pulls from the ledger (up to 8 verified + 4 unverified per probe)".

**B21. MINOR — The parse-defect counts are unverifiable.**
- **Where:** `10_n3.tex:243`, `15_threats.tex:70`.
- **Evidence:** The counts 24/103, 62/150 and 60/147 come only from `docs/lessons.md`. The pre-fix caches are not committed.
- **Fix:** Mark them "reported in docs/lessons.md; not re-checkable".

**B22. MINOR — The N3 "key commit" is the wrong commit.**
- **Where:** `08_evolution.tex:44`.
- **Evidence:** `754e2e6` is the ADR-0008 commit. The N3 PoC is `ec45c31`.
- **Fix:** Cite `ec45c31`, and give 754e2e6 as the ADR.

**B23. MINOR — N2 is described as both negative and inconclusive.**
- **Where:** `08_evolution.tex:50` ("a genuine negative result, not an unfinished task").
- **Evidence:** This contradicts `09_n2.tex:170` and `A_claims.tex` E29 ("not a null result on gating").
- **Fix:** Write "a floor failure that closes Continue; not evidence against gating".

**B24. MINOR — Several passages describe planned things in the present tense.**
- **Where and fixes:**
  - `19_education.tex:113`, "the instructional mechanism the pipeline currently targets": the PoC has no instructional component. Write "would target".
  - `20_organizations.tex:84`, the local judge "for exactly this reason" (confidentiality): the recorded reason is a different model family and zero cost (ADR 0008, 06:138–140).
  - `20_organizations.tex:74`, "domain-neutral by construction": the lexicons, denylist and stop-anchors are English and tuned in-sample on PLC and GDPR.
  - `04_approach.tex:245–248`, "one method that does all of this in order", where "all of this" includes expected-information-gain (EIG) selection and interview agents, which the PoC lacks. Rephrase as a list of what the PoC chains.

**B25. MINOR — Two code locations are wrong.**
- **Where:** `18_platform.tex:54`; fig11 and the 18 components table.
- **Evidence:** `WORLD_C_KINDS` is in `vocab.py:160`, not `residual.py`. "Domain model L0–L6", described as seven layers, does not match the `Layer` enum, which has only L1–L5 ("Only the layer … enumerations exist").
- **Fix:** Correct the path, and reconcile the layer counts.

**B26. MINOR — The 71-of-71 check is called "manual".**
- **Where:** `00_executive_summary.tex:37`, `12_demonstrates.tex:83`.
- **Evidence:** "Manual" suggests a human; the inspector was an AI (09 footnote). There is now stronger evidence: `verify_run` passes 909/909 on local snapshots.
- **Fix:** Report 909/909, with the caveat that it cannot be reproduced from a clone, and keep 71/71 as the AI inspection.

**B27. MINOR — "Each span" was not judged.**
- **Where:** `12_demonstrates.tex:14`, "A model from a different family then judged each span".
- **Evidence:** 140 GDPR v2 spans were never judged.
- **Fix:** Write "each span in the admissible runs".

**B28. MINOR — The replay tests are not replay of the committed maps.**
- **Where:** `12_demonstrates.tex:132–133`.
- **Evidence:** The tests assert identical output on a three-claim fixture with a `FakeJudge` (`test_main.py:20–60`). No test covers byte identity of the committed maps. I checked it by hand and it holds.
- **Fix:** Say so, or add a replay test over the committed caches.

**B29. MINOR — Figure details.**
- **fig04:** the chain lists the retired "contradict" stage and omits independence, cross-verify, slots and decoys (compare 06 and 09's ten stages). The caption says the human step is "at the far right", but it is at bottom center.
- **fig15** (`fig15_gantt.tex:99`, `:116`): "pivot H3" conflicts with the ruling that the pivot is "the interview-only pivot".

**B30. MINOR — V1 design wording.**
- **Where:** `17_validation.tex:152–175`.
- **Problem:** "Coders see neither arm" should read "coders are blind to which arm a unit belongs to". The coders must see the evidence pool to judge it. The 155 firings are not independent: seeds and topic pools overlap, and PLC #1 merged 6 records. 200 units per arm needs more than 45 new-domain units per arm. GDPR v2 is inadmissible.
- **Fix:** State the dependence, and cluster the κ CIs by seed.

---

## Number-check table (65 items)

| # | Number in report (location) | Primary artifact | Verdict |
|---|---|---|---|
| 1 | residual 268 tests (06, E) | ran suite | OK |
| 2 | reconstruct 416 tests, about 1 s | ran: 416, 1.26 s | OK |
| 3 | gapmap 172 tests, about 2 min | ran: 172, 116.9 s | OK |
| 4 | instrument 311 tests, about 7 s | ran: 311, 9.9 s | OK (time about 10 s here) |
| 5 | residual 1,281 LOC, 8 modules | `wc -l` | OK |
| 6 | reconstruct 4,803 LOC, 10 modules | `wc -l` (9 + `__init__`) | OK |
| 7 | gapmap 2,986 LOC, 12 modules | `wc -l` (11 + `__init__`) | OK |
| 8 | Models: haiku-4.5 ×3, gpt-5.4-mini verifier | `models.json`, `calls.jsonl` served_model | OK |
| 9 | GDPR v2: 523 claims, 203/305/15 | sidecar stats | OK (but see B5) |
| 10 | GDPR v2: 25 sources, 7 clusters, $1.00, 262 calls | sidecar, `calls.jsonl` | OK |
| 11 | PLC v1: 35/370/337/321/5, $0.679 | sidecar stats | OK |
| 12 | GDPR v1: 20/259/204/195/14, $0.500 | sidecar stats | OK |
| 13 | GDPR v2 "Located 366" | extractions located = 366; sidecar n_located = 351 | PARTIAL (B16) |
| 14 | 140 of 366 pending | ledger verdicts: 207 supports / 140 pending / 19 insufficient | OK (evidence items) |
| 15 | GDPR v1 UNKNOWN 14 of 35, failure_mode 5 of 5 | sidecar slots | OK |
| 16 | PLC 27 clusters, largest 11% | sidecar | OK |
| 17 | GDPR v1 4 clusters, 55% | sidecar | OK |
| 18 | Decoy false-accept 35% / 15% | sidecar | OK |
| 19 | E-LIVE $2.374 | four sidecars 0.679 + 0.500 + 0.193 + 1.002 | OK |
| 20 | E-PLANT $1.953, E-ABST $0.495, total about $4.82 | `e_plant_eabst_report.md` §3 | OK |
| 21 | a_U = 5/24, Wilson 9–40% | report §1.1; Wilson 9.2–40.5 | OK |
| 22 | E-ABST 5 answered / 19 abstained (79%) | closeout.md | OK |
| 23 | 17 of 24 items zero claims | `e_plant_eabst_report.md:97` | OK |
| 24 | Drift 30%, Wilson 15–52 (n=20) | Wilson(6/20) = 14.5–51.9 | OK |
| 25 | 12% (3/25), Wilson 4–30 | Wilson = 4.2–30.0 | OK |
| 26 | 155 firings = 56/51/48 | `anti_renaming.closure_by_k_topic` n; `judge_lexical_confusion` sums | OK |
| 27 | PLC by lens WHY 24, RESULT 19, DIAG 9, SEL 2, DISC 1, GUARD 1 | mismatched `by_lens.n` + donor `n_candidates` | OK |
| 28 | GDPR v1 RESULT 21, DISC 13, WHY 8, HEDGE 5, SEL 4 | mismatched `by_lens.n` | OK |
| 29 | GDPR v2 DISC 14, SEL 11, RESULT 9, WHY 9, HEDGE 5 | mismatched `by_lens.n` | OK |
| 30 | Promo excluded 42/8/1 | `checks.promo_excluded` | OK |
| 31 | Donor null PLC 22 vs 33.48 [26, 41] | `lexical_donor_null.total` | OK |
| 32 | GDPR v1 11 vs 12.735 [8, 17] | same | OK |
| 33 | GDPR v2 11 vs 8.08 [5, 12], "at or below mean" | same | WRONG wording (B9) |
| 34 | "1,000 random-donor draws" | `CLOSURE_NULL_DRAWS = 200` | WRONG (B9) |
| 35 | Own = control 0.889/0.961/0.958; n = 54/51/48 | `mismatched_evidence_control.total` | OK |
| 36 | Judge reads "up to 12" sentences | caps 8 + 4 per probe; DIAG 34/50 | PARTIAL (B20) |
| 37 | HYP 9/1/6 = 16 | `map` category counts | OK as display; PLC 24 before cap (B3) |
| 38 | PLC 3 open / 6 partial; 13 of 16 partial | `inferred_gap.closure_state` | OK |
| 39 | Map lengths 10/2/7 incl. CONTROL | `len(map)` | OK |
| 40 | PLC RG 11/0/0/10 | `retrieval_gaps`; no sibling run | PARTIAL (SIBLING is n/a, B13) |
| 41 | GDPR v1 12/4/2/28; GDPR v2 3/6/7/44 | `retrieval_gaps` | OK |
| 42 | RG totals 21/46/60 | `len(retrieval_gaps)` | OK |
| 43 | Spearman 0.91; J10 high 0.58; j_low 0.00 (PLC) | `anti_renaming` | OK |
| 44 | ρ 0.09 / 0.16 (GDPR) | `anti_renaming` | OK |
| 45 | j10_low 0.00 / 0.00 / 0.14 | `anti_renaming` | OK |
| 46 | Top-tercile closed share 0.16 | 0.158 | OK |
| 47 | Cross-run 3 of 13, 3 of 9 | `cross_run_stability.a_to_b` in each file | OK |
| 48 | Sibling reroutes 2 and 7 | RG-SIBLING counts | OK |
| 49 | Wilson 3/19 = 5.5–37.6; 8/19 = 23.1–63.7 | recomputed | OK (the figures themselves are unverifiable) |
| 50 | Parse-defect 24/103, 62/150, 60/147 | only `docs/lessons.md` | UNVERIFIED (B21) |
| 51 | Judge states PLC 13/30/13/0; v1 27/18/2/4; v2 24/13/0/11 (fig07) | `judge_lexical_confusion` column sums | OK |
| 52 | Trace 1 `g-59164a9db5bd` open, 34 sentences | `plc map[0]` | OK |
| 53 | Trace 1 "7 rival causes" | 5 rival items | WRONG (B14) |
| 54 | Trace 2 `g-656818235091` partial, 8 sentences; "three claims" | 2 seeds, 1 key | PARTIAL (B14) |
| 55 | Trace 3 `g-1b1e68dc5d39` partial, lexical closed, 8 sentences | `gdpr_v1 map[0]` | OK |
| 56 | Failure trace `g-994077969379` open, 11 keys, 7 rivals, 50 sentences | `plc map[1]` | OK |
| 57 | GDPR v1 one key 194 refs, 3 keys; v2 one key 274 | ledger evidence keys (206 and 366 total) | OK |
| 58 | PLC 11 of 35 error pages | `e_live_report.md:56` | OK |
| 59 | ledger_sha256 ×3, config_sha256 (App E) | `gapmap.json` | OK |
| 60 | N1 freeze hashes (App C) | `residual/frozen/n1.json` | OK |
| 61 | Commits d4fbc60, accb506, ea5c18e, 754e2e6, 080b109, 0f39ed9, 3b72fb8, 883b52a, ec45c31 | `git cat-file` | all exist; N3 key commit should be ec45c31 (B22) |
| 62 | "Every commit … carries an AI co-author line" | 90 of 90 commits up to 754e2e6 | OK |
| 63 | App C locator `char=9061,9169` and exact text | GDPR v2 ledger | OK; label claim WRONG (B17) |
| 64 | fig06 bar values | `fig06_n2.dat` vs sidecars | OK; caption WRONG (B15) |
| 65 | Hanley–McNeil 90% half-widths ±0.14 / ±0.10 / ±0.06 | recomputed: 0.142 / 0.100 / about 0.063 | OK |

Totals: 57 OK, 4 PARTIAL (rows 13, 36, 40, 54), 3 WRONG (rows 33, 34, 53), 1 UNVERIFIED (row 50). Several OK rows carry a caveat on surrounding wording (rows 9, 37, 61, 63 and 64).

---

## Items checked and found correct (no action)

- **N0–N3 representation.** The verdicts match PROGRESS.md and REORIENTATION.md §22. The owner exception to R13 is quoted accurately (REORIENTATION.md:663, PROGRESS.md:36 and :118). The N1 "2 additions at the ≤2 limit" figure matches PROGRESS.md:41.
- **Evidence model.** The following match `claims.py`, `ledger.py`, `gates.py` and `freeze.py`:
  - label order in `ClaimRecord.label`;
  - weakest-premise rule;
  - `Ledger.purpose` values;
  - `CRITERION_LABELS`;
  - `SyntheticRefused` / `GateRefusal`;
  - the three freeze hashes and the `SEMANTICS` file list.
- **Ranking** is a breadth rubric, and **questions** are f-string templates (`lenses.py:337`, `:492`, `:544`, `:594`, `:647`, `:729`). EIG is correctly described as not implemented everywhere I checked.
- **Future components** (World B ingestion, residual estimator, EIG, learner diagnostics, Weft) are marked as not built in 18's table and text, except the figure cases in B6 and the phrases in B24. `ResidualAccount` does compute recall and Res_obs, as 16 says. The estimator is a declared `Literal`, never run, as 07 says.
- **Weft spot-check.** The local clone at `~/projects/weft` has no char-offset fields in non-test code, which matches the ruling. I did not verify the pack count or the pgvector default.

---

## Recommendations to shorten the technical sections (about 6–9 pages)

1. **One pipeline description.** The stage list appears six times: 04 §1, 06 enumerate, 08 table cell, 09 "pipeline, briefly", fig02 and fig04, each with a different stage set. Keep the 06 list, corrected per B5, and fig04. Cut 09 §"The pipeline, briefly" to one sentence with a cross-reference, and drop the stage chain from the 08 table.
2. **One home for the closure-control numbers.** 0.889/0.961/0.958 appears in 00, 04 (box), 08 (twice), 10 (twice), 12 (twice), 13, 14, 17, 18 and A. Keep them in 10 §absence check and the executive summary; elsewhere write "ties its fair control (§10.2)".
3. **One home for the 3/19 caveat, ρ = 0.91 and cross-run 3/13 and 3/9.** Each is restated with full qualifiers in 10, 13, 14, 15 and 16 (and 19, 26, A). Keep the full statement in 10 or 13, and use one clause plus a reference elsewhere.
4. **Defects.** 09's 11-row defect table, 12's defects row, 15's paragraph and Appendix D overlap. Replace the 09 table with two sentences pointing to D.
5. **Worlds and labels.** 07 ("Evidence worlds…", "The label as a computed property") and 18 ("Three evidence worlds", "How evidence labels propagate") repeat the enum values and rules. In 18, keep only the future rules (B checks A, the anchoring guard, tenant confinement) and cross-reference 07 for what exists. This saves about 1 page.
6. **12 vs Appendix A.** The 12 longtable (13 rows) restates A (43 rows). Make 12 a 6-row summary citing A row IDs, or fold 12's strength column into A. This saves about 1.5 pages.
7. **05 vs 08.** The NOW table in 05 and the N0–N3 table in 08 repeat purposes. Keep N4–N9 in 05 and N0–N3 only in 08.
8. **Determinism and replay** is described in 06, 10 (built-in checks), 12 and E. Keep 06 for the mechanism and E for the commands; cut the replay bullet in 10 and the replay row in 12 to references.
9. **18 Weft subsection.** "What not to claim" repeats "Why integration is not justified now" and the adapter contract. Merge them into one paragraph and one 4-bullet contract (saves about ⅓ page). The per-fact description of Weft internals (packs, pgvector, rungs) can go to a footnote.
10. **18 NFR and 25 cost headroom.** The budget-headroom rule ("3× caps, monthly window, checked in code") is stated in 09, 17 V0, 18 and 25. Keep it in 25 only.
11. **Appendix B vs 10 table and 03.** Keep the per-lens construct and channel in B only. The 10 table can drop the "Human channel" column, which B already carries.
