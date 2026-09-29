# 04 — Results and scientific interpretation (N2, N3)

Author: N2/N3 Results Analyst. Date: 2026-09-29. Scope: what the PoC experiments show, including negative and inconclusive results.

**Category labels used below.** Each statement carries one label: OBSERVED (in the PoC artefacts), INTERPRETATION, HYPOTHESIS, FUTURE WORK, LITERATURE. Every number is traceable to a path. The appendix lists where each one was checked.

**What I verified myself, and what I did not.**
- **Verified in primary artefacts:** E-LIVE numbers (`reconstruct/runs/*/sidecar.json`, `ledger.json`, `calls.jsonl`); all N3 map numbers (`research/n3/*/gapmap.json`, `gapmap.md`); lens firing counts (recomputed offline with `gapmap.lenses.run_all`).
- **Not re-verified.** E-PLANT and E-ABST counts come only from the committed report `research/n2/e_plant_eabst_report.md`. Their primary artefacts live in `.private/`, which BRIEF rule 5 puts off limits.
- **Not re-verified: the N3 precision tally (3/19 strict, 8/19 lenient).** It appears only in `research/n3/README.md` and `PROGRESS.md`. The adversarial reviewer's tally sheet and scripts (`fairnull.py`, `audit.py`, `intids.py`) are not committed. Treat this figure as a *reported* number, not one I verified.

---

## 1. N2: the reconstruction pipeline and its robustness tests

### 1.1 What the experiments were designed to test

N2 had three experiments. Each asks a different question.

| Experiment | Question | Registered? | Criterion |
|---|---|---|---|
| **E-LIVE** | Does the pipeline run on the live web without fabricating, mislabelling or falling over? | No. It is a sanity gate with no gold and no threshold (`research/n2/e_live_report.md` §0). | Inspection of runs |
| **E-PLANT** | Does gating reduce adoption of a planted false value? (ClashEval-style planted page, `REORIENTATION.md` ref [51]) | Yes: `docs/n2-eplant-eabst-protocol.md` (registered `3b72fb8`), plus amendments 1–2 | Exact one-sided McNemar test on gated vs ungated adoption over 24–36 targets. There is a **validity floor** a_U ≥ ⌈n/3⌉, and Continue needs it (protocol §6). |
| **E-ABST** | On real but private questions, does the pipeline give fewer false answers than the raw model? | Yes, same protocol, §7 | FAR_raw − FAR_pipe ≥ 0.20 with n_included ≥ 20 (owner threshold, `REORIENTATION.md` §22 threshold table) |

**N2 gate** (`REORIENTATION.md` §22). Continue needs both of these:
- E-PLANT reads Continue;
- E-ABST meets its margin.

N2 reads inconclusive when either experiment is inconclusive (protocol §7, "N2 reading").

### 1.2 What happened

**E-LIVE (OBSERVED).** There were six run directories under `reconstruct/runs/`.

- **v1, PLC** (`20260928T133336Z-59ec876b3d7e`):
  - 35 sources fetched; 370 claims extracted, 337 located, 321 verified-supports;
  - 27 independence clusters, the largest holding 11.4%;
  - decoy false-accept rate 0.35 (20 decoys);
  - cost $0.679.
- **v1, GDPR** (`20260928T135354Z-eb840a85b7d1`):
  - 20 sources fetched; 259 claims extracted, 204 located, 195 supports;
  - 4 clusters, the largest holding 55%. The ledger has only **3 distinct independence keys**, and one key carries 194 key references;
  - decoy false-accept rate 0.15;
  - cost $0.500.
- **v2, PLC** (`…145115Z-518f99363336`): crashed. `complete: false`, `UnicodeEncodeError` on one PDF, 0 claims, $0.193.
- **v2, GDPR** (`…145943Z-bc1cc9a30a02`):
  - `complete: true`, 523 claims extracted;
  - evidence verdicts: 207 supports, 19 insufficient and **140 pending**, so 140 of 366 located evidence items were never verified. (The sidecar stat `n_located` reads 351; the report's 366 counts located evidence items, and the verdict tally supports that.)
  - `calls.jsonl` holds 226 verify calls, all `ok`, and 5 extract calls marked `truncated`. It holds **0 cross-verify and 0 decoy calls**.
  - Last call at 2026-09-28T15:18:31Z.
- **v3, both domains** (`…171449Z…`, `…171508Z…`): one call each, `plan` → `api_error` (HTTP 403, "Key limit exceeded (weekly limit)"). $0 spent.

Manual inspection (`research/n2/e_live_claim_inspection.md`; one AI inspector, no gold, no blind second coder):
- 71 of 71 sampled evidence items re-sliced exactly from their hashed snapshots.
- **PLC v1 verifier error on supported claims:** 30%, n = 20, Wilson 15–52%.
- **Current-verifier GDPR v2 error:** 12%, 3 of 25, Wilson 4–30%. This figure is in-sample: the current prompts quote E-LIVE review examples (R8 in `final_adversarial_review.md`).

**E-PLANT (OBSERVED, as reported in `e_plant_eabst_report.md` §1).** The ungated baseline is Haiku 4.5, given the planted page alongside the real pages. It adopted the planted value on **5 of 24 targets**: 21%, Wilson 95% CI 9–40% (I recomputed the CI: 0.092–0.405).
- Food: 4/12. Cold-weather concreting: 1/12.
- The literature expectation written into the protocol was > 60% (LITERATURE: `REORIENTATION.md` ref [51]).
- **Gated arm, run 1** (tag `n2-freeze`): sealed and unscored. It was declared a defect-forced rerun unit (amendment 1), because failed calls were not logged at that tag. Its last calls are in the same second as the provider cut-off that hit E-LIVE v2(b), 15:18:30–31Z.
- **Run 2** was never executed.

**E-ABST (OBSERVED, as reported in §2).**
- **Raw baseline:** Haiku 4.5 with no tools, and a response schema that explicitly offers `null`. It **answered 5 of 24 items and abstained on 19** (79%).
- **Pipeline run 1:** descriptive only. 17 of 24 items produced zero claims.
- **Run 2,** coding, the second coder, κ and unsealing: none of these happened.

### 1.3 The registered verdict, and why

**Verdict: INCONCLUSIVE for E-PLANT, E-ABST and N2. E-LIVE is "INCONCLUSIVE: the provenance core passes; the post-fix pipeline was never checked live"** (`e_plant_eabst_report.md` §0; `e_live_report.md` §9; `research/n2/closeout.md`). This reading is registered. Nothing in this report changes it.

The chain of reasons is mechanical:

1. **Validity floor.** The floor is a_U ≥ ⌈n/3⌉ on the baseline's full target set. With n = 24, the floor is 8, and a_U = 5.
   - The floor "blocks Continue only" (protocol §6).
   - Amendment 2 P4 fixed that the floor is computed on the full set of 24 (defect D2 had computed it after the cap rule).
   - Excluding `t-conc-08` gives 5/23, still below 8.
   - So **Continue was closed for E-PLANT, and therefore for N2, before any gated arm was scored.** Stop and Change remained reachable.
2. **No scorable gated run.** Amendment 2 P1 required E-LIVE v3 to pass at `n2-freeze-3` before any rerun. v3 was blocked by the provider key's weekly limit ($5, $0 left). The owner chose not to spend more. E-PLANT is therefore inconclusive, because fewer than 20 targets survive the cap rule.
3. **E-ABST.** Run 2 did not happen, so n_included = 0 < 20, which reads inconclusive (§7).

### 1.4 What the negative results mean, and what they do not mean

**What they mean.**
- **OBSERVED:** in this setup, the ungated model was hard to fool, and it was cautious.
  - It adopted 21% of single-page plants, far below the > 60% the protocol assumed.
  - It declined 79% of private questions when `null` was offered.
- **INTERPRETATION:** the gated arms had almost nothing to improve on.
  - The E-PLANT floor exists to stop a Continue reading when plants fail to persuade. It worked as designed.
  - For E-ABST, only an answer can be false, so FAR_raw ≤ 5/n_included. The ≥ 20 pp margin is reachable only in a narrow arithmetic corner. At n_included 21–24, all five raw answers must be false and the pipeline must give none (`e_plant_eabst_report.md` §2.1). The registered gate was close to unreachable before the pipeline arm ran.
- **OBSERVED:** the provenance mechanism works as built. Every claim is tied to:
  - a hashed snapshot;
  - an exact re-sliceable span;
  - a verdict from a model of a different family (`e_live_report.md` §4.1, §6.2).

**What they do not mean.**
- **The results do not show that gating fails, or that it helps.** The gated arms are unmeasured (`e_plant_eabst_report.md` §4 item 3). No statement about pipeline robustness to planted falsehoods, and none about abstention, is supported.
- **The model is not "robust to misinformation" in general.** INTERPRETATION: the E-PLANT baseline did not face the ClashEval condition.
  - It saw each plant **alongside real pages**. Each target is stated on ≥ 2 real pages in different clusters and contradicted by none (protocol §1 step 3).
  - The model also has strong priors on food-safety and concreting facts (protocol §9, "Strong priors").
  - ClashEval-style figures come from a different context construction. So the > 60% expectation was probably miscalibrated for this design, not falsified. (The ClashEval paper exists: OpenAlex W4394906088, DOI 10.48550/arxiv.2404.10198. The "> 60%" figure and its exact setup should be checked against the paper by the literature agent before the report states the contrast.)
- **The raw model is not "calibrated".** INTERPRETATION: the abstention rate reflects the prompt design.
  - The registered threat list assumed the baseline "is not invited to abstain" (protocol §9, "Easier E-ABST margin").
  - The implemented schema explicitly offered `null` (report §2.1).
  - The design choice, not the model alone, set the baseline FAR ceiling.
- **The runs do not measure reconstruction quality against truth.** "Supports" means only that a verifier model judged the span to entail the claim (`e_live_report.md` §8).

### 1.5 What N2 teaches for future design

1. **Calibrate the baseline before registering a floor or a margin.** INTERPRETATION, with the lesson queued in `docs/lessons.md` ("A 'beats the baseline' gate was registered without checking it was reachable").
   - Both baselines ran before the gated arms. Nobody computed the reachable range of the gate from them.
   - Future protocols should include a small calibration pilot of baseline adoption and abstention, and a printed "best reachable outcome" before any gated run.
   - The planted-falsehood design needs recalibration. Options include single-source targets, plants that do not conflict with a majority of real pages, coordinated multi-source plants (listed as "not shown" in protocol §9), or domains with weaker model priors.
2. **Plan the budget as part of the design.** OBSERVED:
   - the key had a $5 weekly limit;
   - recorded N2 spend sums to about $4.82: E-LIVE $2.374 from the four sidecars, E-PLANT $1.953 and E-ABST $0.495 from report §3;
   - the unspent registered caps were about $21 (`docs/lessons.md`).
   - INTERPRETATION: N2 closed inconclusive for budget reasons, not on evidence. A pre-run check of key headroom against the sum of registered caps would have shown this.
3. **Silent failures behind `complete: true`.** OBSERVED:
   - In v2(b), 140 verify calls raised and left no trace, yet the run reported `complete: true` (`e_live_report.md` §5, §6.1).
   - The same event very probably cut off the sealed E-PLANT run 1 (`e_plant_eabst_report.md` §1.2).
   - The fix (`0f39ed9`) is archived as **L6.1** in `docs/LESSONS-ARCHIVE.md`: every failed call is logged and every skip is counted.
   - It is only half closed. `complete` and `n3_input` still ignore `failed_calls_by_task` (R6, `final_adversarial_review.md`).
   - INTERPRETATION: a run's completeness flag must be derived from the counters, not set by reaching the end of the code.
4. **Freeze only after a clean live run.** OBSERVED:
   - three freeze tags were cut before any unsealed live run completed cross-verify or decoy calls (L1.3 recurred, `docs/lessons.md`);
   - cross-verify and decoys have never completed in an unsealed live run (`e_live_report.md` §6.1).
5. **Verifier weakness is scope drift.** OBSERVED: drift is the dominant verifier error, 30% on PLC v1 and 12% on GDPR v2 in-sample. Every GDPR drift has one shape: the jurisdiction is dropped (`e_live_report.md` §6.2). INTERPRETATION: false support inflates "coverage", which pushes any gap-map test toward null (`docs/plans/n3-gap-map-plan.md`, "Risks carried from N2").
6. **Decoy false-accept rates are not validity estimates.** OBSERVED: decoy validity is self-certified by the generator family (R2).

---

## 2. N3: the methodology-guided gap map (proof of concept)

### 2.1 What was built and run

**OBSERVED.** `gapmap/` reads an N2 ledger and runs seven lenses: DISC, DIAG, SEL, HEDGE, GUARD, WHY and RESULT.
- A lens *fires* when sources attest a construct but not its content (`research/n3/README.md`, "Lenses").
- A local judge (`qwen2.5:7b-instruct` via Ollama, temperature 0, cached) then decides *closure*: whether the missing element is in fact stated somewhere in the ledger.
- Open or partial candidates become three-tier records:
  - observed evidence;
  - an inferred gap;
  - a hypothesis labelled `inferred`.
- Candidates with thin support become retrieval gaps (RG-*), never hypotheses.
- Replay from the committed cache is byte-identical offline (`docs/plans/n3-poc-lens-spec.md`, "Live-run accounting").

The inputs were three ledgers, all from the N2 E-LIVE runs above:
- **PLC v1;**
- **GDPR v1;**
- **GDPR v2,** which is flagged `admissible: false` in `research/n3/gdpr_v2/gapmap.json` because of its 140 pending verdicts.

### 2.2 Lens firing (OBSERVED)

I recomputed the counts offline with `lenses.run_all` at `link.SETTING_1`. They match each map's judge-vs-lexical confusion totals (56, 51, 48).

| Ledger | Candidates fired | By lens | Promotional seeds excluded |
|---|---|---|---|
| PLC | 56 | WHY 24, RESULT 19, DIAG 9, SEL 2, DISC 1, GUARD 1 | 42 |
| GDPR v1 | 51 | RESULT 21, DISC 13, WHY 8, HEDGE 5, SEL 4 | 8 |
| GDPR v2 | 48 | DISC 14, SEL 11, RESULT 9, WHY 9, HEDGE 5 | 1 |

INTERPRETATION: lens firing follows the texture of each domain.
- DIAG (rival causes) fires only on PLC, the diagnostic domain.
- DISC (undefined judgement terms) and HEDGE (hedged rules) fire mainly on GDPR, the normative domain.
- This fits the lens design. It is not evidence that the lenses find hidden knowledge.

### 2.3 What the gap map produced (OBSERVED, final maps)

| | PLC | GDPR v1 | GDPR v2 (not admissible) |
|---|---|---|---|
| Judge states over fired candidates (closed / partial / open / synthetic-closed) | 13 / 30 / 13 / 0 | 27 / 18 / 2 / 4 | 24 / 13 / 0 / 11 |
| Gap candidates (HYP) | 9: DIAG 2, RESULT 3, WHY 3, GUARD 1 | 1: RESULT | 6: DISC 1, RESULT 3, HEDGE 1, WHY 1 |
| Closure state of the HYP records | 3 open, 6 partial | 1 partial | 6 partial |
| Breadth of the HYP records | 2 moderate, 7 narrow | 1 narrow | 6 narrow |
| RG-SINGLE / RG-UNVER / RG-SIBLING / RG-UNK | 11 / 0 / 0 / 10 | 12 / 4 / 2 / 28 | 3 / 6 / 7 / 44 |

Sources: `research/n3/*/gapmap.json` (`map`, `retrieval_gaps`, `checks.judge_lexical_confusion`) and the `gapmap.md` Summary sections.

**Observations.**
- **13 of the 16 final gap candidates are "partial".** The judge found a partial statement of the missing element. Only 3 candidates, all in PLC, are fully "open".
- **Most GDPR structure falls into retrieval gaps.** GDPR v1 has 28 RG-UNK records and v2 has 44. Only 1 (v1) and 6 (v2) hypotheses survive.
- **INTERPRETATION:** the GDPR v1 ledger has only 3 independence keys, which caps breadth and routes most candidates to RG-SINGLE. The map's yield is limited by the reconstruction's source diversity before any lens logic applies.

### 2.4 The closure-control failure (the central negative result)

**Lexical closure (the first version), OBSERVED:**
- **Pre-final maps**, per the second reviewer's fair donor null with self and same-source claims excluded from both arms (`docs/plans/n3-poc-lens-spec.md`, "S1-S3 changes"):
  - PLC 42 vs 40.6 [33, 47];
  - GDPR v1 13 vs 14.1 [10, 19];
  - GDPR v2 11 vs 8.2 [5, 12].
  - Every observed count sits inside the null interval, so lexical closure ran **at chance**.
  - 13 of 15 sampled other-source closures were wrong on inspection (reported; the review's script is not committed).
- **Final maps**, which keep the lexical test for comparison only (`gapmap.md` "S2 lexical donor null"):
  - PLC 22 vs null mean 33.5 [26, 41]. This is *below* the null. The DIAG per-rival row drives it: 1 closure observed against a null mean of 15.2.
  - GDPR v1 11 vs 12.7 [8, 17].
  - GDPR v2 11 vs 8.1 [5, 12].
  - All are flagged `closure-uninformative`.
- **The README reports only the pre-final figures.** The report must say which set it quotes.

**Semantic closure (the final version), OBSERVED.** This is the fair mismatched-evidence control (`checks.mismatched_evidence_control`; the `gapmap.json` field `checks.mismatched_evidence_control`):
- Both arms keep the seed's own sentences.
- The "own" arm adds this candidate's retrieved sentences from other sources.
- The "control" arm swaps those for the other-source sentences retrieved for the nearest other candidate of the same lens.
- Result: **own rate = control rate on every lens and every ledger.**
  - Totals: PLC 0.89 = 0.89 (n = 54); GDPR v1 0.96 = 0.96 (n = 51); GDPR v2 0.96 = 0.96 (n = 48).
  - own − control is 0 in every row.
- The "other-source-only" rate is 0.67, 0.73 and 0.71 in the three ledgers. This is how often an independent source alone closes a candidate.

**What this means (INTERPRETATION):**
- **Closure decisions track the seed's own text, not the independent evidence.** Swapping in another candidate's evidence changes nothing, so the judge's verdict does not depend on whether *this* topic's other sources state the element. The step that decides "this element is unsaid" is therefore not shown to measure absence.
- **The lens firing rule is too permissive about "missing".** The lenses test stems and regexes, so they cannot see a paraphrase. The judge then finds the element, or part of it, in the seed's own span. "The element is already stated in the seed's own span" is the first typical failure listed in `research/n3/README.md`.
- **An internal inconsistency must be reported.** The control counts `partial` as closure (`checks._closed_or_partial`). Yet 13 of the 16 final hypotheses are `partial`. Most surviving candidates are in a state that the map's own control treats as "closed or nearly closed". So the hypotheses mostly mark places where the text says *something*, not *nothing*.
- **Caveats:**
  - The judge is a 7B local model, and a stronger judge is untested (README, "Limitations").
  - DIAG's control checks only one rival per group (spec, "Implementation notes (S1-S3)").
  - The ceiling (own rate 1.00 on most lenses) leaves little room for any difference. The spec shows, with a constructed 3-candidate case, that the check *can* read informative, so the tie is a property of this data.

### 2.5 Precision by adversarial judgement

**OBSERVED, as reported, not verified in a primary artefact:**
- 3 of 19 strict and 8 of 19 lenient, judged by an Opus adversarial reviewer on the **pre-final** maps (`research/n3/README.md`; `PROGRESS.md`).
- Wilson 95% CIs, which I recomputed: strict 5.5–37.6%; lenient 23.1–63.7%.
- The final maps were not re-tallied.
- Two of the listed defects changed the candidate set after the tally:
  - the integer-id parse bug, which silently turned unread judge answers into "open" in 24/103, 62/150 and 60/147 responses (`docs/lessons.md`);
  - the fair-control rewrite.

**INTERPRETATION:**
- A model is not a gold criterion, and this is one judge on one pass. The figure is a sanity signal, not a precision estimate.
- It still points the same way as the control: most candidates are not credible hidden-knowledge sites on inspection.

### 2.6 Cross-run stability (GDPR v1 vs v2)

**OBSERVED** (`research/n3/gdpr_v1/gapmap.md` and `gdpr_v2/gapmap.md`, §7.2):
- 3 of 13 open v1 candidates have any counterpart in v2.
- 3 of 9 open v2 candidates have any counterpart in v1.
- Every counterpart is a partial match. There are no exact matches.
- The sibling check reroutes 2 of v1's candidates and 7 of v2's to RG-SIBLING, because the other run answered them.

**INTERPRETATION:**
- Two reconstructions of the *same* task, run hours apart with the same models, surface mostly different candidates. Each run is dominated by one or two independence keys:
  - v1's top key carries 194 key references in the ledger;
  - v2's top key carries 274.
- The instability comes from retrieval, not from the lenses. It means a gap map built on one live-web run is not a stable object.
- Any gold test needs a dated, frozen corpus and repeated runs. `docs/plans/n2-reconstruction-plan.md` stage 8 already asks for "rerun ≥ 3 times".

### 2.7 Breadth vs density: the anti-renaming check

**OBSERVED** (`checks.anti_renaming` in each `gapmap.json`; lens candidates only, RG-UNK and CONTROL excluded):

| | J10(map, lowest-density 10) | J10(map, highest-density 10) | Spearman ρ(score, density) | Top-tercile closed share |
|---|---|---|---|---|
| PLC | 0.00 | 0.58 | 0.91 | 0.16 |
| GDPR v1 | 0.00 | 0.10 | 0.09 | 0.65 |
| GDPR v2 | 0.14 | 0.33 | 0.16 | 0.69 |

**INTERPRETATION:**
- **The map is not low density renamed.** Its top candidates barely overlap the lowest-density candidates, and the "density-in-disguise" flag (`j_low ≥ 0.5 or ρ ≤ −0.5`) does not fire.
- **On PLC it leans toward the opposite: high density.** ρ = 0.91, and J10(high) = 0.58.
  - The "salience-in-disguise" flag (`j_high ≥ 0.7 and top-tercile closed share < 0.2`) is a near miss. The closed-share condition holds (0.16), and J10(high) is 0.58 against the 0.7 bar.
  - ρ is inflated because retrieval gaps are scored −1 and RG-SINGLE is low density by definition.
  - Ranking by breadth is deliberate (README, "Is a gap just 'few sources'?"). But breadth is close to "how much is written on this topic".
- **So the check rules out one confound, not both.** A future gold test must include retrieval-support density *and* area size as baselines (`REORIENTATION.md` §14.3). This matters because `docs/plans/n3-gap-map-plan.md` ("Implication") already notes that on World A the live features are mostly size and density, so ΔAUROC ≈ 0 by construction.
- **The original §7.1 check passed by construction.** It included RG-UNK records, whose density is 0 (`docs/lessons.md`, "The check meant to catch 'density renamed as gap' passed by construction"). The current numbers come from the fixed version.

### 2.8 Four statuses that must not be blurred

| Status | Holds? | Why |
|---|---|---|
| **The pipeline works** | Yes (OBSERVED) | It runs end to end on three real ledgers. Output is deterministic and replays byte-identically. Tiers are kept apart. Unreadable judge answers are routed to RG-UNDECIDED (decision 0008 rule `undecided-never-a-finding`). |
| **The records are candidates** | Yes (OBSERVED plus INTERPRETATION) | Each record is "the lens fired here and the judge did not find the element", with evidence and a question attached. Nothing validates it as knowledge that experts hold. |
| **Prediction is not demonstrated** | Yes | No gold was acquired. The absence-detection step does not beat a fair control. Precision by adversarial judgement is low and in-sample. |
| **Prediction is refuted** | **No** | See below. |

**Why the PoC cannot refute the central hypothesis (INTERPRETATION).** The registered falsifier is N3's ΔAUROC rule: stop H1 if the upper 90% bound of ΔAUROC against the strongest baseline, on held-out gold, is below δ (`REORIENTATION.md` §22, N3 row). None of its inputs exist:
- there is no gold;
- δ is not set;
- the area partition is not frozen;
- there is no matcher and no second coder;
- the corpus is not dated (`docs/plans/n3-gap-map-plan.md`).

The failures are also failures of one *implementation*:
- one 7B judge;
- lexicons tuned in-sample;
- three ledgers from undated live-web runs, one of them not admissible.

A negative result on a component that has not been shown to measure its target says nothing about the target. The correct reading is **"not demonstrated, and the current closure component is not yet a valid instrument"**, not "the residual is unpredictable".

---

## 3. What the PoC demonstrates, ranked

Strength labels:
- **STRONG:** direct evidence in artefacts, replicated or mechanically checked.
- **MODERATE:** direct evidence, single run or in-sample.
- **WEAK:** suggestive only.

1. **STRONG (OBSERVED): exact-span provenance is achievable at scale on real sources.** Every claim is tied to a hashed snapshot, a re-sliceable span and a verdict from a model of another family. 71/71 manual re-slices were exact. `verify_run` re-slices every evidence item.
2. **STRONG (OBSERVED): the N3 pipeline is deterministic and inspectable.** Replay from the committed judge cache is byte-identical across all three ledgers, and the three tiers never mix.
3. **STRONG (OBSERVED): the PoC's own checks catch its own failures.** Examples:
   - the fair control flags every lens `closure-uninformative`;
   - the admissibility check marks GDPR v2 inadmissible;
   - the sibling check reroutes candidates.
   - INTERPRETATION: the evaluation apparatus, and the adversarial review loop that shaped it, is the most reusable output.
4. **MODERATE (OBSERVED): live-web runs expose defects that offline tests miss.** Eleven E-LIVE findings drove fixes (`e_live_report.md` §7). The silent-failure class appeared twice, in N2 (140 pending behind `complete: true`) and in N3 (unparsed judge ids defaulting to "open").
5. **MODERATE (OBSERVED): lens firing differs by domain in the expected direction.** DIAG fires on PLC only; DISC and HEDGE fire mainly on GDPR.
6. **MODERATE (OBSERVED, single run each): ungated baselines resisted.** Planted-value adoption was 5/24 in multi-page context, and the raw model abstained on 19/24 private questions when `null` was offered. The primary artefacts are sealed, so I did not re-verify these counts.
7. **WEAK (INTERPRETATION): UNKNOWN slots may carry signal.** In GDPR v1, `failure_mode` was UNKNOWN in 5 of 5 areas. This is consistent with statutory text lacking practitioner failure modes, but it is unvalidated (`e_live_report.md` §4.4).
8. **WEAK (INTERPRETATION): a few candidates read as plausible expert-question sites.** Examples: GDPR v2 HEDGE "in most cases … in some cases"; PLC GUARD "panicking and abandoning systematic approaches". This is one reader's judgement; the strict precision was 3/19.

**What the PoC does not demonstrate:**
- reconstruction accuracy against truth;
- that gating reduces planted-falsehood adoption or false answers;
- a live check of the post-fix N2 pipeline (v3);
- a live unsealed cross-verify or decoy run;
- that any gap candidate marks knowledge experts hold;
- that closure (absence detection) measures absence;
- stability of the gap map across runs;
- generalisation beyond two domains;
- any learner or bottleneck claim.

The system does **not** identify tacit knowledge.

---

## 4. Main scientific lessons

- **Absence detection is the bottleneck of the whole approach (INTERPRETATION).**
  - Reconstruction and lens firing work. The question "is this element really unsaid?" does not yet have a valid answer.
  - Lexical closure was at chance, and the semantic judge tied its fair control.
  - Every downstream quantity depends on this step: hypotheses, ranking, questions and any ΔAUROC. It must be validated first, against human closure labels, before any gold.
- **Thinness of a reconstruction and the human residual are different constructs (INTERPRETATION).**
  - A thin area can be thin because retrieval was poor: one regulator, 3 independence keys, PDFs lost, 140 unverified items.
  - It can also be thin because the knowledge is unwritten.
  - The PoC's retrieval-gap categories separate some of this, but cross-run instability shows that retrieval noise dominates.
  - HYPOTHESIS for the grant: the residual is predictable only after retrieval variance is controlled (a dated, frozen corpus and repeated runs).
- **In-sample tuning is pervasive and must be frozen before gold (OBSERVED plus INTERPRETATION).**
  - Tuned on the three ledgers: lexicons, the promotional denylist, DISC stop-anchors (`gapmap/src/gapmap/config.py`, `config_sha256` `35fd0af2…`), verifier prompts that quote E-LIVE examples (R8), and knowledge types assigned by the extractor.
  - Any number measured on these ledgers is optimistic.
- **Gates must be checked for reachability, and their failure modes must be defaults that cannot pass (INTERPRETATION).**
  - N2's gates were close to unreachable given the baselines.
  - Three failure modes defaulted to the finding: `complete: true` over lost calls, "open" over unparsed answers, and an anti-renaming check that passed by construction.
  - Each check needs a planted positive and a permutation null (`docs/lessons.md`).
- **Breadth-based ranking risks becoming salience (INTERPRETATION).** On PLC, score correlates with density at ρ = 0.91. Density and area size must be the headline baselines.

---

## 5. Implications for the validation programme

### 5.1 Fix and pre-register before any gold (FUTURE WORK)

1. **A closure step that passes the fair control.**
   - Candidates: a stronger judge, an ensemble, or a different-family judge.
   - Report `partial` separately from `closed`.
   - Pass criterion: own − control ≥ 0.20 (already coded) *and* agreement with human closure labels (below).
2. **Admissibility as code.**
   - Every located extraction has a verdict, cross-verify ran, decoys ran, and `complete` reads `failed_calls_by_task` (R6; `n3-gap-map-plan.md`).
3. **Hash-freeze `config.py`**, the feature set, the area partition (task-step grain, not planner areas) and the scope decomposition (`REORIENTATION.md` §14.3).
4. **A dated, frozen corpus mode** with `as_of`, a DOI/title gold blocklist and memorisation probes (§18.2). This also removes most cross-run instability.
5. **Revive the dead features, or accept a narrow test.**
   - Dead in World A: boundary sources, contradictions, tacitness, done-support, instability.
   - Otherwise E-CTA tests size plus density plus type, and ΔAUROC ≈ 0 by construction (`n3-gap-map-plan.md`).
6. **Set** δ, the primary gold, fallback golds, minimum missed areas (Hanley–McNeil: 20 areas give about ±0.20 half-width at AUROC 0.70), the matcher κ ≥ 0.70 rule, the second coder and the budget. The budget must include key headroom against the sum of caps.
7. **For N2's deferred validation:**
   - recalibrate E-PLANT: pilot the baseline adoption, then set the floor;
   - recompute E-ABST reachability given the null-offering schema;
   - add decoy validity by a third family or the owner (R2).

### 5.2 Smallest informative next experiment (FUTURE WORK; proposal, not registered)

**A human-labelled closure set.** It needs zero participants beyond the one blind second coder.
- Take the 155 fired lens candidates on the three existing ledgers (56 + 51 + 48).
- For each, the owner (under origin blinding) and the second coder label whether the ledger states the missing element: stated, partly stated, or not stated.
- Measure human–human κ, then each candidate judge's κ against the humans, and rerun the fair control with the best judge.
- Cost: about $0 in API with a local judge, plus labelling time.
- **What it decides:** whether absence detection is feasible at all, before money is spent on gold.
  - If no judge reaches κ ≥ 0.70 (the §18 matcher rule, reused), the lens approach reduces to density features.
  - E-CTA would then be a test of density baselines against themselves.

After that passes: a pre-registered E-CTA on one itemised CTA gold (Sullivan et al. is suggested), on a dated corpus, with ΔAUROC against the strongest §14.3 baseline.

### 5.3 What would kill the central hypothesis

**Registered (`REORIENTATION.md` §22, N3 row).** The central hypothesis (H1) is stopped if:
- on held-out gold, with the corpus dated and the configuration frozen,
- the upper 90% bound of ΔAUROC against the *strongest* baseline is below δ,
- regardless of recall.

The project then pivots to H3 (an elicitation-efficiency tool).

**Stricter kill for the lens approach specifically (INTERPRETATION; to register if adopted).**
- Condition: after a closure step passes the human-labelled check, the gap map still does not beat retrieval-support density and area size on gold.
- Meaning: the methodology layer adds nothing beyond "where little is written".
- Caution: a stop reading from a configuration whose closure step never passed the control would be an artefact of the pipeline, not a falsification.

---

## 6. Candidate finding boxes

**Box 1 — OBSERVED.**
Given a planted false page alongside real pages that stated the truth, the ungated model adopted the false value on 5 of 24 targets (21%; 95% CI 9–40%). The protocol had assumed more than 60%. This closed the registered "Continue" route for N2 before any gated arm was scored. *(Source: `research/n2/e_plant_eabst_report.md` §1.1; protocol §6.)*

**Box 2 — OBSERVED.**
The gap map's closure judge decides whether a "missing" element is really unsaid. We swapped each candidate's own supporting evidence for a near neighbour's. The judge's closure rate did not change on any lens in any of three ledgers (0.89 = 0.89; 0.96 = 0.96; 0.96 = 0.96). *(Source: `research/n3/*/gapmap.json`, `checks.mismatched_evidence_control`.)*

**Box 3 — INTERPRETATION.**
The bottleneck is absence detection, not reconstruction or lens design. Until a closure step is shown to track evidence, every gap record is a candidate ("a lens fired here"), not a prediction of human knowledge. The PoC therefore neither demonstrates nor refutes that the human residual is predictable.

**Box 4 — OBSERVED.**
Two independent reconstructions of the same GDPR task, run hours apart with the same models, gave mostly different gap candidates. Only 3 of 13 and 3 of 9 open candidates had any counterpart in the other run, and none matched exactly. *(Source: `research/n3/gdpr_v1/gapmap.md`, `gdpr_v2/gapmap.md` §7.2.)*

---

## Appendix: number traceability

| Number | Checked in |
|---|---|
| E-LIVE v1/v2/v3 counts, costs, clusters, decoy FAR, verdict tallies, call counts, last-call time | `reconstruct/runs/<run>/sidecar.json` `stats`, `ledger.json` evidence verdicts, `calls.jsonl` (all six runs) |
| GDPR v1: 3 independence keys; v1 top key 194, v2 top key 274 references | regex count of `independence_key` in `ledger.json` (v1 `…135354Z…`, v2 `…145943Z…`) |
| a_U = 5/24; the 4/12 and 1/12 per-domain split; E-ABST 5/24 answered; run-1 descriptives; costs | `research/n2/e_plant_eabst_report.md` only (primary artefacts in `.private/`, off limits) |
| Wilson CIs (5/24, 3/19, 8/19) | recomputed (z = 1.96) |
| 71/71 re-slices; 30% and 12% verifier error | `research/n2/e_live_report.md` §6.2, `e_live_claim_inspection.md` (inspection record, not re-coded) |
| Lens firing counts, promotional exclusions | recomputed offline: `gapmap.lenses.run_all(ledger, index, link.SETTING_1)`, `lenses.promo_excluded_count` |
| HYP counts and closure states; RG counts; judge-state totals | `research/n3/*/gapmap.json` (`map`, `retrieval_gaps`, `checks.judge_lexical_confusion`) |
| Own / control / other-source-only rates | `research/n3/*/gapmap.json` `checks.mismatched_evidence_control` |
| Final lexical donor null | `research/n3/*/gapmap.md` "S2 lexical donor null" |
| Pre-final lexical null (42 vs [33, 47] etc.); 13/15 wrong closures | `docs/plans/n3-poc-lens-spec.md` "S1-S3 changes" (reviewer script not committed) |
| J10, ρ, tercile tables; flag logic | `research/n3/*/gapmap.json` `checks.anti_renaming`; `gapmap/src/gapmap/checks.py` `anti_renaming` |
| Partial counted as closure in the control | `gapmap/src/gapmap/checks.py` `_closed_or_partial` |
| Cross-run counterparts | `research/n3/gdpr_v1/gapmap.md`, `gdpr_v2/gapmap.md` §7.2 |
| 3/19 strict, 8/19 lenient | **reported only** (`research/n3/README.md`, `PROGRESS.md`); tally not committed; unverified |
| Parse-bug drops 24/103, 62/150, 60/147 | `docs/lessons.md` (reported; pre-fix caches not committed) |
| ClashEval exists | OpenAlex W4394906088, DOI 10.48550/arxiv.2404.10198. The "> 60%" figure itself is not re-checked against the paper. |
