# Gap map: forecastability

- Ledger: `22d9ea32deda68594caf96d87c2b6d345cf4d1f0a4dc5119cd48a4e27324551d`
- Config: `35fd0af25618f8d6e0d1c2c3707d7e932afe2ce72dbd01e956034b43bfeb04c1`
- **Admissibility note:** sidecar n3_input is false: E-PLANT corpus contains planted fabrications

## Summary

- **HYP:** 7 total
  - DISC: 1 (1 narrow)
  - RESULT: 3 (3 narrow)
  - WHY: 3 (3 narrow)
- **Retrieval gaps:** RG-SINGLE 25, RG-UNVER 2
- **Control slot:** 1
- **PROMO-excluded seeds (S3 defect 1):** 5
- **§7.1 anti-renaming:** J10(low)=0.00, J10(high)=0.31, ρ(score,dens)=0.41, flags: closure-uninformative

## How to read this map

Every record separates three tiers, and they never mix:

- **OBSERVED EVIDENCE** — verified verbatim spans from the ledger; what a source actually says.
- **INFERRED GAP** — a statement about the ledger that anyone can re-run: which claims state the topic and which do not state the missing element.
- **HIDDEN-KNOWLEDGE HYPOTHESIS** — a prediction, labelled `inferred`, never a fact. It reads as a prediction ("is predicted to", "practitioners are hypothesised to"), never as an established finding.

Retrieval gaps, below the map, are a fourth and separate thing: not hypotheses. Their action is to search further or verify an unverified span — never to ask an expert.

**Breadth is not confidence.** Ranking among open gaps is deliberately by breadth of the attested explicit side — the opposite of low density, on purpose (§5): a gap many independent sources discuss without ever stating the missing element is a stronger claim that the element is genuinely unsaid than one only one source raises. Breadth says nothing about whether the gap is real. WHICH candidates are gaps at all is decided entirely by the lens's firing rule plus its closure test (§1.5, §2); whether that closure test is itself informative — i.e. not so easily satisfied by unrelated text that it would close almost anything — is exactly what the §7.1 checks below test.

**These are gap candidates, not findings.** The tier label stays `inferred`; precision against a human criterion is unmeasured (there is no gold yet). What IS measured is whether the closure judge's own informativeness beats a fair null — the mismatched-evidence control and the lexical donor null, both in §7.1.

**Lexical robustness (r/4) is not re-judged.** It is measured on the lexical construct across the 4 link-parameter settings (§1.4), not by re-asking the closure judge 4 times with different neighbourhood membership — so a record the judge closes or leaves open can still show a low or 0/4 lexical robustness; the two numbers answer different questions and neither overrides the other.

## Ranked gap map (candidates)

| rank | lens | anchor | breadth | lexical robustness | k_topic |
|---|---|---|---|---|---|
| 1 | DISC | appropriate past | narrow | 2/4 | 3 |
| 2 | WHY | Surrogates should be used whenever sample size permits | narrow | 2/4 | 2 |
| 3 | WHY | The same leakage boundary for rolling-origin evaluation | narrow | 0/4 | 2 |
| 4 | WHY | Any new selector that goes further than xami_sparse, such as | narrow | 0/4 | 2 |
| 5 | RESULT | evaluation applies to exogenous screening (F8), where | narrow | 0/4 | 2 |
| 6 | RESULT | verified with multiple backends and sample-size stress | narrow | 0/4 | 2 |
| 7 | RESULT | inspected before applying simplifying assumptions that | narrow | 0/4 | 2 |

### #1 [DISC] appropriate past

*lens: DISC; category: HYP*

**OBSERVED EVIDENCE**

- `c-63e7e5e12bf6d309` [seed] literature_supported / documentation, key `ind-s-0b00932c0a642b74`, verdict supports: "They are appropriate to use when past numerical data is available and when it is reasonable to assume that some of the patterns in the data are expected to continue into the future."
- `c-afbbc01c74390081` [seed] literature_supported / documentation, key `ind-s-0b00932c0a642b74`, verdict supports: "they are appropriate when past data are not available."
- `c-02293075bf7d14f3` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Current estimator in this repo: 1. Build conditioning matrix \(Z=[X_{t+1},\ldots,X_{t+h-1}]\). 2. Residualize past and future on \(Z\) (linear backend by default; optional RF backend). 3. Compute MI on residual pairs."
- `c-1529fd8d4983ffd9` [topic] literature_supported / documentation, key `ind-s-0b00932c0a642b74`, verdict supports: "They are usually applied to intermediate- or long-range decisions."
- `c-d41368bc8903ef51` [topic] literature_supported / documentation, key `ind-s-ca7d54da5b087ed3`, verdict supports: "Provides train/test indices to split time-ordered data, where other cross-validation methods are inappropriate, as they would lead to training on future data and evaluating on past data."
- `c-24b50a94338e6f5d` [topic] literature_supported / documentation, key `ind-s-0b00932c0a642b74`, verdict supports: "T X → Y = H ( Y t ∣ Y t − 1 : t − L ) − H ( Y t ∣ Y t − 1 : t − L , X t − 1 : t − L )"
- `c-366be2f127206bb4` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The mutual information between a $k$-step past embedding and the one-step-ahead future, evaluated for $k = 1 \ldots K$, to identify the minimal sufficient lookback length where additional history yields negligible extra predictive information."
+ 6 more topic claims across 3 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a boundary for 'appropriate past'. Re-runnable: prompt sha 5443dc71bbae.

- test: `DISC:appropriate past`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: Sentences 1 and 2 partially address the 'appropriate past' by mentioning the availability of past numerical data, but do not specify a threshold or defining feature.
- partial hits: c-63e7e5e12bf6d309

**HIDDEN-KNOWLEDGE HYPOTHESIS** (label: `inferred` — a prediction, never a fact)

Predicted, not observed: Hypothesis (inferred): practitioners are predicted to discriminate 'appropriate past' from its neighbours by features that no verified claim in this ledger matched test DISC:appropriate past for.

- predicted knowledge type: cue
- predicted tacitness: collective
- channel: contrasting-case classification, or expert-rated written vignettes

**Missing element:** a boundary for 'appropriate past'

**Reasoning:** 1 key(s) state appropriate past; 3 key(s) discuss the topic; the closure judge found no verified sentence matching test DISC:appropriate past

**Breadth:** narrow (uncalibrated; no gold) (score 1 = A2 + B0 − P1; k_step=1, k_topic=3); lexical robustness 2/4

**Alternatives:**

- [live] The boundary is stated in paraphrase without the anchor string. — the anchor-string regex cannot see a paraphrase (the main limitation of DISC, §9).
- [not live] The term 'appropriate past' is institutionally indeterminate, so experts disagree and there is nothing to recover. — 0/2 anchor claims are typed norm or concept.
- [live] The boundary is in unfetched sources. — the ledger is a bounded retrieval.

**Expert question** (channel: contrasting-case classification, or expert-rated written vignettes):

> One source writes: "Quantitative forecasting models are appropriate to use when past numerical data is available and when it is reasonable to assume that some of the patterns in the data are expected to continue into the future.". Think of a recent case where you had to judge whether something was appropriate past. Describe one case that clearly was, one that clearly was not, and one that was hard to call. What differed between them, and what did you check first?

### #2 [WHY] Surrogates should be used whenever sample size permits, specifically when n is at least 200 and n_surrogates is at least 99.

*lens: WHY; category: HYP*

**OBSERVED EVIDENCE**

- `c-520e8d5962f8f467` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Use surrogates whenever sample size permits ($n \ge 200$, `n_surrogates >= 99`)."
- `c-195d659856d7237b` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Differentiates deterministic chaos from stochastic noise (when sample size permits)"
- `c-2d8e9ac84a4e1468` [topic] literature_supported / documentation, key `ind-s-5114732bc45e7988`, verdict supports: ""yw", "ywa", "ywadjusted" or "yw_adjusted" : Yule-Walker with sample-size adjustment in denominator for acovf. Default."
- `c-55a3d89f479050f5` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Surrogate significance is optional, requires feasible sample size, and needs at least 99 surrogates."
- `c-59ee33682140a710` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "TE sample-size guardrails require `min_pairs >= 50`; with non-empty conditioning history, at least `2 * min_pairs` aligned rows are required."
- `c-e69be58ea45c4382` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Numerical inflation `directness_ratio > 1.0` estimator instability, finite-sample effects Treat as warning; verify with multiple backends and sample-size stress"
+ 2 more topic claims across 2 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 08ce434eef6e.

- test: `WHY:c-520e8d5962f8f467`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: 200 sample size reduces noise-lifted individual AMI values

**HIDDEN-KNOWLEDGE HYPOTHESIS** (label: `inferred` — a prediction, never a fact)

Predicted, not observed: Hypothesis (inferred): practitioners are predicted to know why 'Surrogates should be used whenever sample size permits, specifically when n is at least 200 and n_surrogates is at least 99.'; no verified claim in this ledger matched test WHY:c-520e8d5962f8f467.

- predicted knowledge type: rationale
- predicted tacitness: relational
- channel: a targeted confirmation question

**Missing element:** a reason

**Reasoning:** 1 key(s) state Surrogates should be used whenever sample size permits, specifically when n is at least 200 and n_surrogates is at least 99.; 2 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-520e8d5962f8f467

**Breadth:** narrow (uncalibrated; no gold) (score 1 = A1 + B0 − P0; k_step=1, k_topic=2); lexical robustness 2/4

**Alternatives:**

- [live] The rationale is a purpose clause that RAT does not match. — RAT does not match every 'to identify...' purpose clause.
- [not live] The source is promotional. — no PROMO lexicon hit on the span; no ledger field marks promotional voice (§10).
- [live] The reason is trivial safety knowledge. — an omitted rationale may simply be too obvious to state.

**Expert question** (channel: a targeted confirmation question):

> Sources say: "Use surrogates whenever sample size permits ($n \ge 200$, `n_surrogates >= 99`).". What would happen if someone did it differently, and in what situations, if any, is doing it differently acceptable?

### #3 [WHY] The same leakage boundary for rolling-origin evaluation applies to exogenous screening (F8), where CrossAMI must be computed on the training window only.

*lens: WHY; category: HYP*

**OBSERVED EVIDENCE**

- `c-a5bfbf4dc9e5e96b` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The same leakage boundary applies to exogenous screening (F8): CrossAMI must be computed on the training window only."
- `c-02db4a573b917ded` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "In rolling-origin evaluation, diagnostics are computed on train windows only and scoring on post-origin holdout only."
- `c-599acaa7431652b7` [topic] literature_supported / documentation, key `ind-s-ca7d54da5b087ed3`, verdict supports: "each test set covers the same time duration, while the train set size accumulates data from previous splits."
- `c-0568df39c001b613` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "For very short series: CrossAMI inherits the same finite-sample bias and minimum- length requirements as univariate AMI."
- `c-0bc576ddaf02fce5` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The workflow blocks infeasible requests, routes exogenous requests separately, and preserves stable screening behavior (`AR(1) -> high`, `white_noise -> low`) in regression tests."
- `c-0c818ceeb5ed84c5` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Analyzer facade, canonical workflow helpers, and rolling-origin support"
+ 18 more topic claims across 2 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 9cb9438720b3.

- test: `WHY:c-a5bfbf4dc9e5e96b`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: prevents look-ahead leakage

**HIDDEN-KNOWLEDGE HYPOTHESIS** (label: `inferred` — a prediction, never a fact)

Predicted, not observed: Hypothesis (inferred): practitioners are predicted to know why 'The same leakage boundary for rolling-origin evaluation applies to exogenous screening (F8), where CrossAMI must be computed on the training window only.'; no verified claim in this ledger matched test WHY:c-a5bfbf4dc9e5e96b.

- predicted knowledge type: rationale
- predicted tacitness: relational
- channel: a targeted confirmation question

**Missing element:** a reason

**Reasoning:** 1 key(s) state The same leakage boundary for rolling-origin evaluation applies to exogenous screening (F8), where CrossAMI must be computed on the training window only.; 2 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-a5bfbf4dc9e5e96b

**Breadth:** narrow (uncalibrated; no gold) (score 1 = A1 + B0 − P0; k_step=1, k_topic=2); lexical robustness 0/4

**Alternatives:**

- [live] The rationale is a purpose clause that RAT does not match. — RAT does not match every 'to identify...' purpose clause.
- [not live] The source is promotional. — no PROMO lexicon hit on the span; no ledger field marks promotional voice (§10).
- [live] The reason is trivial safety knowledge. — an omitted rationale may simply be too obvious to state.

**Expert question** (channel: a targeted confirmation question):

> Sources say: "The same leakage boundary applies to exogenous screening (F8): CrossAMI must be computed on the training window only.". What would happen if someone did it differently, and in what situations, if any, is doing it differently acceptable?

### #4 [WHY] Any new selector that goes further than xami_sparse, such as PMIME-style or PC-stable with driver autohistory, must be introduced under a new method label so that shipped cross_pami and xami_sparse semantics are not silently extended.

*lens: WHY; category: HYP*

**OBSERVED EVIDENCE**

- `c-22acb9b0539eee32` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Any new selector that goes further (PMIME-style, PC-stable with driver autohistory) must be introduced under a **new method label** so that the shipped `cross_pami` and `xami_sparse` semantics are not silently extended."
- `c-0938aacab4017209` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`diagnostics/cmi.py` owns alternative residual backends used by pAMI-style workflows."
- `c-b75a19c17f2efb10` [topic] literature_supported / documentation, key `ind-s-0b00932c0a642b74`, verdict supports: "The use of this function was introduced as part of the Box-Jenkins approach to time series modelling, whereby plotting the partial autocorrelative functions one could determine the appropriate lags p in an AR (p) model or in an extended ARIMA (p,d,q) model."
- `c-10e496fcc72af849` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "With the opt-in, those rows flip to `tensor_role="known_future"` and the selector may choose `selected_for_tensor=True` at $k=0$ for that driver only."
- `c-18943cbbab8481d9` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The cross-series mutual information between a target series and one or more candidate exogenous drivers at each forecast horizon, filtered by Benjamini-Hochberg FDR control, to screen which exogenous variables carry statistically detectable predictive signal."
- `c-2c567f4bccc5fa13` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "**At least one row per `(target, driver)` pair** is emitted by the selector."
+ 14 more topic claims across 2 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha e2b365fe71b2.

- test: `WHY:c-22acb9b0539eee32`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: 2

**HIDDEN-KNOWLEDGE HYPOTHESIS** (label: `inferred` — a prediction, never a fact)

Predicted, not observed: Hypothesis (inferred): practitioners are predicted to know why 'Any new selector that goes further than xami_sparse, such as PMIME-style or PC-stable with driver autohistory, must be introduced under a new method label so that shipped cross_pami and xami_sparse semantics are not silently extended.'; no verified claim in this ledger matched test WHY:c-22acb9b0539eee32.

- predicted knowledge type: rationale
- predicted tacitness: relational
- channel: a targeted confirmation question

**Missing element:** a reason

**Reasoning:** 1 key(s) state Any new selector that goes further than xami_sparse, such as PMIME-style or PC-stable with driver autohistory, must be introduced under a new method label so that shipped cross_pami and xami_sparse semantics are not silently extended.; 2 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-22acb9b0539eee32

**Breadth:** narrow (uncalibrated; no gold) (score 1 = A1 + B0 − P0; k_step=1, k_topic=2); lexical robustness 0/4

**Alternatives:**

- [live] The rationale is a purpose clause that RAT does not match. — RAT does not match every 'to identify...' purpose clause.
- [not live] The source is promotional. — no PROMO lexicon hit on the span; no ledger field marks promotional voice (§10).
- [live] The reason is trivial safety knowledge. — an omitted rationale may simply be too obvious to state.

**Expert question** (channel: a targeted confirmation question):

> Sources say: "Any new selector that goes further (PMIME-style, PC-stable with driver autohistory) must be introduced under a **new method label** so that the shipped `cross_pami` and `xami_sparse` semantics are not silently extended.". What would happen if someone did it differently, and in what situations, if any, is doing it differently acceptable?

### #5 [RESULT] evaluation applies to exogenous screening (F8), where

*(co-located with #3: shares a seed claim)*

*lens: RESULT; category: HYP*

**OBSERVED EVIDENCE**

- `c-a5bfbf4dc9e5e96b` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The same leakage boundary applies to exogenous screening (F8): CrossAMI must be computed on the training window only."
- `c-02db4a573b917ded` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "In rolling-origin evaluation, diagnostics are computed on train windows only and scoring on post-origin holdout only."
- `c-599acaa7431652b7` [topic] literature_supported / documentation, key `ind-s-ca7d54da5b087ed3`, verdict supports: "each test set covers the same time duration, while the train set size accumulates data from previous splits."
- `c-0568df39c001b613` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "For very short series: CrossAMI inherits the same finite-sample bias and minimum- length requirements as univariate AMI."
- `c-0bc576ddaf02fce5` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The workflow blocks infeasible requests, routes exogenous requests separately, and preserves stable screening behavior (`AR(1) -> high`, `white_noise -> low`) in regression tests."
- `c-0c818ceeb5ed84c5` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Analyzer facade, canonical workflow helpers, and rolling-origin support"
+ 18 more topic claims across 2 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'evaluation applies to exogenous screening (F8), where'. Re-runnable: prompt sha dca396493cc6.

- test: `RESULT:c-a5bfbf4dc9e5e96b`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: No sentence explicitly states a result, meaning, or next action.
- partial hits: c-02db4a573b917ded, c-143b2f1030f42c35, c-3e06b2d68146d02f, c-a5bfbf4dc9e5e96b, c-d7d073c08a1e9cc5
- synthetic hits (unverified): c-0f2d6cc9aeae4292, c-1614a21ff92e85d9, c-4ead62d0678a16e6, c-7de1550bc5925cda

**HIDDEN-KNOWLEDGE HYPOTHESIS** (label: `inferred` — a prediction, never a fact)

Predicted, not observed: Hypothesis (inferred): practitioners are predicted to read the result of 'evaluation applies to exogenous screening (F8), where' against expected values and map it to the next action; no verified claim in this ledger matched test RESULT:c-a5bfbf4dc9e5e96b.

- predicted knowledge type: interpretation, expectancy
- predicted tacitness: relational
- channel: CDM probes on a recalled case; process tracing

**Missing element:** a result-to-interpretation mapping for 'evaluation applies to exogenous screening (F8), where'

**Reasoning:** 1 key(s) state evaluation applies to exogenous screening (F8), where; 2 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-a5bfbf4dc9e5e96b

**Breadth:** narrow (uncalibrated; no gold) (score 0 = A1 + B0 − P1; k_step=1, k_topic=2); lexical robustness 0/4

**Alternatives:**

- [live] The interpretation is stated in paraphrase without the seed's stems. — the stem-overlap test cannot see a paraphrase (the same limitation as DISC, §9).
- [live] The test is a formality with a binary outcome. — not every prescribed test feeds a real branching decision.
- [live] The interpretation is instrument-given. — a displayed pass/fail reading needs no practitioner interpretation.

**Expert question** (channel: CDM probes on a recalled case; process tracing):

> Sources prescribe: "The same leakage boundary applies to exogenous screening (F8): CrossAMI must be computed on the training window only.". Think of the last time you did this. What result did you get, what had you expected, what did that result make you do next -- and what result would have sent you down a different path?

### #6 [RESULT] verified with multiple backends and sample-size stress

*lens: RESULT; category: HYP*

**OBSERVED EVIDENCE**

- `c-e69be58ea45c4382` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Numerical inflation `directness_ratio > 1.0` estimator instability, finite-sample effects Treat as warning; verify with multiple backends and sample-size stress"
- `c-074bbf77d40d49d7` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "directness can be numerically unstable when raw dependence is close to zero. In this slice, 6/7 cases have warning horizons and at least one `directness_ratio > 1.0`, which should be treated as an estimation warning, not scientific evidence of stronger conditioned dependence."
- `c-2d8e9ac84a4e1468` [topic] literature_supported / documentation, key `ind-s-5114732bc45e7988`, verdict supports: ""yw", "ywa", "ywadjusted" or "yw_adjusted" : Yule-Walker with sample-size adjustment in denominator for acovf. Default."
- `c-176cff9ac653373b` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Short-sample fragility large backend deltas on small fractions insufficient support for residualization enforce minimum length and inspect stress table stability"
- `c-195d659856d7237b` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Differentiates deterministic chaos from stochastic noise (when sample size permits)"
- `c-1e3de571e58b5ba5` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Short-sample fragility large backend deltas on small fractions insufficient support for residualization"
+ 6 more topic claims across 2 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'verified with multiple backends and sample-size stress'. Re-runnable: prompt sha 82f57dce654a.

- test: `RESULT:c-e69be58ea45c4382`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: Multiple backends and sample-size stress testing results indicate potential numerical instability or fragility, leading to warnings rather than scientific evidence.
- partial hits: c-074bbf77d40d49d7, c-176cff9ac653373b, c-e69be58ea45c4382

**HIDDEN-KNOWLEDGE HYPOTHESIS** (label: `inferred` — a prediction, never a fact)

Predicted, not observed: Hypothesis (inferred): practitioners are predicted to read the result of 'verified with multiple backends and sample-size stress' against expected values and map it to the next action; no verified claim in this ledger matched test RESULT:c-e69be58ea45c4382.

- predicted knowledge type: interpretation, expectancy
- predicted tacitness: relational
- channel: CDM probes on a recalled case; process tracing

**Missing element:** a result-to-interpretation mapping for 'verified with multiple backends and sample-size stress'

**Reasoning:** 1 key(s) state verified with multiple backends and sample-size stress; 2 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-e69be58ea45c4382

**Breadth:** narrow (uncalibrated; no gold) (score 0 = A1 + B0 − P1; k_step=1, k_topic=2); lexical robustness 0/4

**Alternatives:**

- [live] The interpretation is stated in paraphrase without the seed's stems. — the stem-overlap test cannot see a paraphrase (the same limitation as DISC, §9).
- [live] The test is a formality with a binary outcome. — not every prescribed test feeds a real branching decision.
- [live] The interpretation is instrument-given. — a displayed pass/fail reading needs no practitioner interpretation.

**Expert question** (channel: CDM probes on a recalled case; process tracing):

> Sources prescribe: "Numerical inflation `directness_ratio > 1.0` estimator instability, finite-sample effects Treat as warning;". Think of the last time you did this. What result did you get, what had you expected, what did that result make you do next -- and what result would have sent you down a different path?

### #7 [RESULT] inspected before applying simplifying assumptions that

*lens: RESULT; category: HYP*

**OBSERVED EVIDENCE**

- `c-ab4f9f360073f8bf` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`is_non_monotone` flags this shape for downstream consumers without judgement. Routines that assume monotone decay (such as naive exponential smoothers) should inspect this flag before applying simplifying assumptions."
- `c-036f6b526cb8eadb` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Spearman is also near zero because $ X $ is V-shaped (non-monotone) in $X$."
- `c-9abe82177371fd61` [topic] literature_supported / documentation, key `ind-s-0b00932c0a642b74`, verdict supports: "Hence, it is advantageous when the model assumption of Granger causality doesn't hold, for example, analysis of non-linear signals."
- `c-2a2178f666a2258b` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Spearman is also near zero because $X^2$ is U-shaped (non-monotone) in $X$."
- `c-42247942360cffb2` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "For example, a monthly series with strong annual seasonality may have $F(12) > F(5)$, producing a non-monotone profile with a secondary peak at $h = 12$."
- `c-5588f848981103c4` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Do not treat a `True` value as an estimation artefact or an error - it is correct and expected for seasonal series."
+ 2 more topic claims across 2 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'inspected before applying simplifying assumptions that'. Re-runnable: prompt sha e93738935091.

- test: `RESULT:c-ab4f9f360073f8bf`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: No explicit statement of expected result or consequence.
- partial hits: c-ab4f9f360073f8bf

**HIDDEN-KNOWLEDGE HYPOTHESIS** (label: `inferred` — a prediction, never a fact)

Predicted, not observed: Hypothesis (inferred): practitioners are predicted to read the result of 'inspected before applying simplifying assumptions that' against expected values and map it to the next action; no verified claim in this ledger matched test RESULT:c-ab4f9f360073f8bf.

- predicted knowledge type: interpretation, expectancy
- predicted tacitness: relational, perceptual
- channel: CDM probes on a recalled case; process tracing

**Missing element:** a result-to-interpretation mapping for 'inspected before applying simplifying assumptions that'

**Reasoning:** 1 key(s) state inspected before applying simplifying assumptions that; 2 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-ab4f9f360073f8bf

**Breadth:** narrow (uncalibrated; no gold) (score 0 = A1 + B0 − P1; k_step=1, k_topic=2); lexical robustness 0/4

**Alternatives:**

- [live] The interpretation is stated in paraphrase without the seed's stems. — the stem-overlap test cannot see a paraphrase (the same limitation as DISC, §9).
- [live] The test is a formality with a binary outcome. — not every prescribed test feeds a real branching decision.
- [live] The interpretation is instrument-given. — a displayed pass/fail reading needs no practitioner interpretation.

**Expert question** (channel: CDM probes on a recalled case; process tracing):

> Sources prescribe: "Routines that assume monotone decay (such as naive exponential smoothers) should inspect this flag before applying simplifying assumptions.". Think of the last time you did this. What result did you get, what had you expected, what did that result make you do next -- and what result would have sent you down a different path?

## Control slot

The §14.2 unknown-unknowns guard: an area no hypothesis touched, walked cold.

### Toolkit Installation and Setup

*lens: —; category: CONTROL*

**OBSERVED EVIDENCE**

(none)

**INFERRED GAP**

Control slot: area 'Toolkit Installation and Setup' (a-b3126f903e834ac0) has no HYP record and the highest attested share (0.81) among candidate areas of ledger 22d9ea32.

- test: `CONTROL:a-b3126f903e834ac0`; state: open (closure judge: )

**Reasoning:** the §14.2 unknown-unknowns guard: no HYP touches this area

**Breadth:** narrow (uncalibrated; no gold) (score 0 = A0 + B0 − P0; k_step=0, k_topic=0); lexical robustness 0/4

**Expert question** (channel: control):

> Walk me through how you carry out Toolkit Installation and Setup, from start to finish, as if I were watching you do it. What do you check, and in what order?

## Retrieval gaps

Not hypotheses: each one's action is to search further or verify a synthetic span, never to ask an expert.

### [HEDGE] For surrogate bands, the upper band is operationally informative for detecting non-null dependence while the lower band is usually near zero for MI and is not typically operationally useful. — RG-UNVER

*Action: verify — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-672eba057b35b6b7` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The upper band is operationally informative for detecting non-null dependence. The lower band is usually near zero for MI and is not typically operationally useful."
- `c-da688457c5163577` [closure_near] synthetic_extrapolation / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict insufficient — flag: unverified-synthetic: "**Cannot detect symmetric nonlinear couplings** - a quadratic driver with near-zero Pearson correlation can be a strong predictive feature; always cross-check with `cross_ami`"
- `c-036f6b526cb8eadb` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Spearman is also near zero because $ X $ is V-shaped (non-monotone) in $X$."
- `c-70872842e6096f91` [topic] literature_supported / documentation, key `ind-s-0b00932c0a642b74`, verdict supports: "If the value of the statistic is significantly different for the original series than for the surrogate set, the null hypothesis is rejected and non-linearity assumed."
- `c-074bbf77d40d49d7` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "directness can be numerically unstable when raw dependence is close to zero. In this slice, 6/7 cases have warning horizons and at least one `directness_ratio > 1.0`, which should be treated as an estimation warning, not scientific evidence of stronger conditioned dependence."
- `c-2a2178f666a2258b` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Spearman is also near zero because $X^2$ is U-shaped (non-monotone) in $X$."
- `c-33bdb9872d68dc9c` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "This project separates several dependence diagnostics so teams can choose the smallest useful workflow for a decision, not the largest workflow available."
+ 10 more topic claims across 2 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating an exception condition among the verified sentences retrieved (4 unverified sentences considered separately). Re-runnable: prompt sha 78dfff05dd3e.

- test: `HEDGE:c-672eba057b35b6b7`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): synthetic-closed
- judge reason: Specific cases where the rule does not hold are mentioned in sentences 9, 10, and 11.
- synthetic hits (unverified): c-9850da0617f4e09b, c-da688457c5163577

**Missing element:** an exception condition

**Reasoning:** 1 key(s) state For surrogate bands, the upper band is operationally informative for detecting non-null dependence while the lower band is usually near zero for MI and is not typically operationally useful.; 3 key(s) discuss the topic; the closure judge found no verified sentence matching test HEDGE:c-672eba057b35b6b7

### [HEDGE] PCMCI-AMI orchestration follows the inward-only dependency rule where use cases depend on declared ports (protocol contracts), and adapters satisfy those contracts without adapter-to-adapter helper coupling. — RG-UNVER

*Action: verify — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-12f83d379ed3d9b0` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "PCMCI-AMI orchestration now follows the inward-only dependency rule: use cases depend on declared ports (protocol contracts), and adapters satisfy those contracts without adapter-to-adapter helper coupling."
- `c-08dd95a981ab695e` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Use `ports/` for protocol-style seams when a collaborator needs to be substituted or isolated."
- `c-17941110bd4a294c` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`CausalGraphPort` `discover(...) -> CausalGraphResult` PCMCI+ style graph discovery"
- `c-21586c1b3ff04cdf` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`CausalGraphFullPort` `discover(...) -> CausalGraphResult` and `discover_full(...) -> PcmciAmiResult` PCMCI-AMI full three-phase result path"
- `c-2abb88ad6676aac9` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Internal builder/orchestration helpers used by analyzers and use cases"
- `c-4d970d03fcfa1063` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The architecture goal is still inward dependency flow. Adapters should not become a second business-logic layer."
+ 11 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating an exception condition among the verified sentences retrieved (4 unverified sentences considered separately). Re-runnable: prompt sha d7f62c36d5e2.

- test: `HEDGE:c-12f83d379ed3d9b0`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: The Agent narration adapter surface has an experimental stability level.
- synthetic hits (unverified): c-1e0afd8caf027c55

**Missing element:** an exception condition

**Reasoning:** 1 key(s) state PCMCI-AMI orchestration follows the inward-only dependency rule where use cases depend on declared ports (protocol contracts), and adapters satisfy those contracts without adapter-to-adapter helper coupling.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test HEDGE:c-12f83d379ed3d9b0

### [WHY] Downstream model families or framework-specific settings should be recommended only after triage is completed. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-deaeadb0c2b363e5` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Only then recommend downstream model families or framework-specific settings."
- `c-0383c186390263e0` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Instead, it sits one step earlier: forecastability triage → model-family choice → framework-specific modeling"
- `c-31524d4ec7dfcb67` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "a structured, machine-readable hand-off contract for downstream model families."
- `c-805080c1dca07fc6` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "That split is intentional: the core package produces deterministic evidence; the examples repository shows how to translate that evidence into framework-specific modeling recipes."
- `c-835ab48b9520fadc` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "It checks whether the routing policy emits defensible family-level guidance before a downstream framework hand-off."
- `c-98c910c65938f691` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The surface suggests starting model families only; it does not fit models or wire downstream frameworks."
+ 4 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 8ff11616e2a1.

- test: `WHY:c-deaeadb0c2b363e5`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: to ensure forecastability triage is completed

**Missing element:** a reason

**Reasoning:** 1 key(s) state Downstream model families or framework-specific settings should be recommended only after triage is completed.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-deaeadb0c2b363e5

### [WHY] The architecture goal is inward dependency flow where adapters should not become a second business-logic layer. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-4d970d03fcfa1063` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The architecture goal is still inward dependency flow. Adapters should not become a second business-logic layer."
- `c-12f83d379ed3d9b0` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "PCMCI-AMI orchestration now follows the inward-only dependency rule: use cases depend on declared ports (protocol contracts), and adapters satisfy those contracts without adapter-to-adapter helper coupling."
- `c-4f7df5b9dd43919c` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The live repository is layered, but it is also pragmatic"
- `c-bea4138eb4aaf4a3` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The package is layered and subpackage-heavy. The stable import facade is small, but the internal tree is organized by role: triage domain, use cases, analyzer pipeline, metrics, diagnostics, reporting, utils, adapters, services, ports, and bootstrap helpers."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 6fc5e8c25c5d.

- test: `WHY:c-4d970d03fcfa1063`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: to prevent adapter-to-adapter helper coupling

**Missing element:** a reason

**Reasoning:** 1 key(s) state The architecture goal is inward dependency flow where adapters should not become a second business-logic layer.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-4d970d03fcfa1063

### [WHY] When the task is time-series forecasting, one should not jump directly to model fitting but should start with forecastability triage first. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-e65cb947aa2ae2da` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "When the task is time-series forecasting, do not jump directly to model fitting. Start with forecastability triage first"
- `c-832f11ec63500689` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "When the task is time-series forecasting, do not jump directly to model fitting. Start with forecastability triage first"

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 6216d7b7d631.

- test: `WHY:c-e65cb947aa2ae2da`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: 6: Identifies specific diagnostics for forecastability triage.

**Missing element:** a reason

**Reasoning:** 1 key(s) state When the task is time-series forecasting, one should not jump directly to model fitting but should start with forecastability triage first.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-e65cb947aa2ae2da

### [WHY] New user-facing imports should be added through forecastability or forecastability.triage only when committing to compatibility. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-007b692334093e05` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Add new user-facing imports through `forecastability` or `forecastability.triage` only when you want to commit to compatibility."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 037a65709869.

- test: `WHY:c-007b692334093e05`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: prevents compatibility issues

**Missing element:** a reason

**Reasoning:** 1 key(s) state New user-facing imports should be added through forecastability or forecastability.triage only when committing to compatibility.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-007b692334093e05

### [WHY] The toolkit should not be used for proving physical causality between variables. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-a09878eb59fe00c2` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Do Not Use This For - Proving physical causality between variables."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha c5cdc9c3df69.

- test: `WHY:c-a09878eb59fe00c2`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: prevents misuse leading to incorrect conclusions

**Missing element:** a reason

**Reasoning:** 1 key(s) state The toolkit should not be used for proving physical causality between variables.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-a09878eb59fe00c2

### [WHY] False confidence from one backend should be mitigated by requiring cross-backend agreement before acting on lag recommendations. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-0869da46b065ba5c` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "False confidence from one backend decision changes when backend changes model class mismatch or noisy data require cross-backend agreement before acting on lag recommendations"
- `c-0ba98927fe267eac` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "pAMI feasibility (linear residual backend): \[ N \ge \max\left(H + \texttt{min\_pairs\_pami} + 1,\ 2H\right) \]"
- `c-4a028079c97bc7c6` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "False confidence from one backend decision changes when backend changes model class mismatch or noisy data"
- `c-7afe58436134c4db` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Overfitting in nonlinear backends sharp pAMI spikes at isolated lags only for tree backends backend fits noise in conditioning space compare against linear baseline and require ranking stability"

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 7a0475234405.

- test: `WHY:c-0869da46b065ba5c`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: prevents false confidence from one backend

**Missing element:** a reason

**Reasoning:** 1 key(s) state False confidence from one backend should be mitigated by requiring cross-backend agreement before acting on lag recommendations.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-0869da46b065ba5c

### [WHY] AMI and pAMI horizons should not be pre-aggregated before triage. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-7f34e267e7469f22` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Keep AMI and pAMI horizon-specific; do not pre-aggregate before triage."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha a96a08a99410.

- test: `WHY:c-7f34e267e7469f22`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: pre-aggregation before triage distorts pAMI's diagnostic value

**Missing element:** a reason

**Reasoning:** 1 key(s) state AMI and pAMI horizons should not be pre-aggregated before triage.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-7f34e267e7469f22

### [WHY] Deterministic orchestration must be kept in use_cases and pipeline rather than notebooks or scripts. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-54d5f9039aa8eac5` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Keep deterministic orchestration in `use_cases/` and `pipeline/` rather than notebooks or scripts."
- `c-074bbf77d40d49d7` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "directness can be numerically unstable when raw dependence is close to zero. In this slice, 6/7 cases have warning horizons and at least one `directness_ratio > 1.0`, which should be treated as an estimation warning, not scientific evidence of stronger conditioned dependence."
- `c-12f83d379ed3d9b0` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "PCMCI-AMI orchestration now follows the inward-only dependency rule: use cases depend on declared ports (protocol contracts), and adapters satisfy those contracts without adapter-to-adapter helper coupling."
- `c-2abb88ad6676aac9` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Internal builder/orchestration helpers used by analyzers and use cases"
- `c-632cedcf139eff2c` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "CLI, API, scripts, MCP, and agents are optional access or narration layers around the same deterministic outputs."
- `c-925a7f61d84ad74d` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Use cases orchestrate triage models, pipeline helpers, and internal services, and depend on causal discovery through declared `ports/` contracts."
+ 6 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 2e9e1370d7d4.

- test: `WHY:c-54d5f9039aa8eac5`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: 2

**Missing element:** a reason

**Reasoning:** 1 key(s) state Deterministic orchestration must be kept in use_cases and pipeline rather than notebooks or scripts.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-54d5f9039aa8eac5

### [WHY] Escalation should occur only when nonlinear backends improve diagnostic consistency across datasets. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-5ff63882db181126` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Escalate only when nonlinear backends improve diagnostic consistency across datasets."
- `c-1e3de571e58b5ba5` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Short-sample fragility large backend deltas on small fractions insufficient support for residualization"
- `c-454033f260c0fffc` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "rf_residual` Captures nonlinear interactions with moderate tuning burden"
- `c-4a028079c97bc7c6` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "False confidence from one backend decision changes when backend changes model class mismatch or noisy data"
- `c-599f2ed68644b97d` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The conditioning-out step removes only the component of dependence that is linearly predictable from the intermediate lags. Nonlinear residual dependence that the linear backend cannot capture remains in the AMI but may not be fully removed from pAMI."
- `c-7491c5056c4cfdef` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Results differ between the linear (default) and RF backends. The linear backend is faster and more stable; the RF backend may capture more nonlinear residual structure but introduces additional noise for short series."
+ 2 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 769618d5a70d.

- test: `WHY:c-5ff63882db181126`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: prevents false confidence from one backend

**Missing element:** a reason

**Reasoning:** 1 key(s) state Escalation should occur only when nonlinear backends improve diagnostic consistency across datasets.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-5ff63882db181126

### [WHY] Transport concerns must be put in adapters, not in use cases or metrics code. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-e1073e72ca3c2484` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Put transport concerns in `adapters/`, not in use cases or metrics code."
- `c-0ce6297954840ce0` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`cli.py`, `api.py`, `dashboard.py`, `mcp_server.py`, `settings.py`, `event_emitter.py`, `checkpoint.py`, `result_bundle_io.py`, `triage_presenter.py`, `agents/`, `llm/` Transport, runtime, agent, checkpoint, and presentation adapters"
- `c-12f83d379ed3d9b0` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "PCMCI-AMI orchestration now follows the inward-only dependency rule: use cases depend on declared ports (protocol contracts), and adapters satisfy those contracts without adapter-to-adapter helper coupling."
- `c-bce5f39d56b978b9` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Entrypoints and adapters call the package facades or use cases."
- `c-bea4138eb4aaf4a3` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The package is layered and subpackage-heavy. The stable import facade is small, but the internal tree is organized by role: triage domain, use cases, analyzer pipeline, metrics, diagnostics, reporting, utils, adapters, services, ports, and bootstrap helpers."
- `c-c0ad72fbd17e0508` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`use_cases/run_triage.py` and `use_cases/run_batch_triage.py` are the authoritative orchestration entry points called by the public facade and adapters."
+ 1 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha f2ba16ee1517.

- test: `WHY:c-e1073e72ca3c2484`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: prevents mixing of concerns

**Missing element:** a reason

**Reasoning:** 1 key(s) state Transport concerns must be put in adapters, not in use cases or metrics code.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-e1073e72ca3c2484

### [WHY] F8 should be avoided for very short series because CrossAMI inherits the same finite-sample bias and minimum-length requirements as univariate AMI. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-0568df39c001b613` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "For very short series: CrossAMI inherits the same finite-sample bias and minimum- length requirements as univariate AMI."
- `c-176cff9ac653373b` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Short-sample fragility large backend deltas on small fractions insufficient support for residualization enforce minimum length and inspect stress table stability"
- `c-1e3de571e58b5ba5` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Short-sample fragility large backend deltas on small fractions insufficient support for residualization"
- `c-29f2188e34114c86` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Avoids over-long or too-short lookback windows"
- `c-2eaebaa88a212810` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The kNN mutual information estimator (Kraskov et al., 2004; `n_neighbors=8`) is asymptotically consistent but has positive bias for finite samples, particularly at short series lengths and large lag indices."
- `c-356ad4fb83b96c3a` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "new scorers inherit kNN estimation noise on short series"
+ 9 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha b9f8f1558341.

- test: `WHY:c-0568df39c001b613`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: finite-sample bias and minimum-length requirements

**Missing element:** a reason

**Reasoning:** 1 key(s) state F8 should be avoided for very short series because CrossAMI inherits the same finite-sample bias and minimum-length requirements as univariate AMI.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-0568df39c001b613

### [WHY] F7 should be avoided when F5 output is desired in the ranking because LLE is intentionally excluded from automated batch triage by design. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-5f42b1909154998b` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "When F5 output is desired in the ranking: LLE is intentionally excluded from automated batch triage by design."
- `c-05db67066fb6179b` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "LLE is intentionally excluded from the batch triage ranking table (F7) by design."
- `c-07e983f3df1aeb65` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Objective multi-criteria ranking across an entire signal portfolio"
- `c-3079d77ce22ec266` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "As a replacement for individual deep-dive analysis on flagged series: batch ranking surfaces which series to investigate, not why."
- `c-4933d8a0da8e3ab8` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Runs F1-F4 and F6 deterministically across a panel of series and produces a ranked diagnostic table, enabling rapid comparison of forecastability structure across many signals in one pass."
- `c-55451c295b59e8c7` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Largest Lyapunov exponent is experimental and excluded from automated triage decisions."
+ 5 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 52ead9f18dbc.

- test: `WHY:c-5f42b1909154998b`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: to prevent failure of automated batch triage

**Missing element:** a reason

**Reasoning:** 1 key(s) state F7 should be avoided when F5 output is desired in the ranking because LLE is intentionally excluded from automated batch triage by design.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-5f42b1909154998b

### [WHY] F4 should be avoided for short series with n less than 128 because Welch PSD estimates are based on very few segments and Ω values are unreliable. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-92ea97938fb3a905` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "For short series ($n < 128$): Welch PSD estimates are based on very few segments and Ω values are unreliable as anything other than a coarse indicator."
- `c-01a236bf8006dd6e` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Without BH FDR correction when many drivers are tested simultaneously: uncorrected $p$-values will inflate false-positive rates."
- `c-0568df39c001b613` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "For very short series: CrossAMI inherits the same finite-sample bias and minimum- length requirements as univariate AMI."
- `c-29f2188e34114c86` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Avoids over-long or too-short lookback windows"
- `c-4ded063d84bc4156` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Approximately $n \geq 3 \times H_{\max}$, where $H_{\max}$ is the maximum evaluation horizon. Below this threshold, MI estimates are unreliable for lags close to $H_{\max}$."
- `c-bf72579f2ce06838` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Directly at horizons beyond the frequency-specific cap (Yearly 6, Quarterly 8, Monthly 18, Weekly 13, Daily 14, Hourly 48): AMI values beyond these caps are unreliable."
+ 2 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 3ac82198e20b.

- test: `WHY:c-92ea97938fb3a905`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: 2,3,4,5,6,7,8,9,10,11,12

**Missing element:** a reason

**Reasoning:** 1 key(s) state F4 should be avoided for short series with n less than 128 because Welch PSD estimates are based on very few segments and Ω values are unreliable.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-92ea97938fb3a905

### [WHY] Downstream forecasting frameworks should be used after triage, not instead of triage. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-ec5f71c99ae25d10` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Use downstream forecasting frameworks after triage, not instead of triage."
- `c-703f18d903194a6e` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "A practitioner interacts with the profile instead of the raw numeric array to avoid re-implementing the threshold logic in downstream code."
- `c-835ab48b9520fadc` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "It checks whether the routing policy emits defensible family-level guidance before a downstream framework hand-off."
- `c-98c910c65938f691` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The surface suggests starting model families only; it does not fit models or wire downstream frameworks."
- `c-ca2565db6e11ee00` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Only then recommend downstream model families or framework-specific settings."
- `c-deaeadb0c2b363e5` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Only then recommend downstream model families or framework-specific settings."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 9314fc2eeb49.

- test: `WHY:c-ec5f71c99ae25d10`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: 2

**Missing element:** a reason

**Reasoning:** 1 key(s) state Downstream forecasting frameworks should be used after triage, not instead of triage.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-ec5f71c99ae25d10

### [WHY] F5 should be used in exploratory research only as one piece of converging evidence that a series may exhibit chaotic dynamics, always alongside F1 and F6. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-27d0b3495c0ff1ed` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Exploratory research only: as one piece of converging evidence that a series may exhibit chaotic dynamics, always alongside F1 and F6."
- `c-8323af7405c72872` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "A positive $\hat{\lambda}$ is consistent with chaotic dynamics, but stochastic coloured noise and non-stationary processes also produce positive estimates. F5 alone cannot distinguish the two cases."
- `c-efde45474384037f` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "To contextualise F1 AMI results: high AMI with low complexity typically indicates regular, easily modelled dynamics; high AMI with high complexity suggests potentially nonlinear or chaotic behaviour."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha f46a0eff2adc.

- test: `WHY:c-27d0b3495c0ff1ed`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: A positive Largest Lyapunov Exponent estimate is consistent with chaotic dynamics, but stochastic coloured noise and non-stationary processes also produce positive estimates, and F5 alone cannot distinguish the two cases. (3)

**Missing element:** a reason

**Reasoning:** 1 key(s) state F5 should be used in exploratory research only as one piece of converging evidence that a series may exhibit chaotic dynamics, always alongside F1 and F6.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-27d0b3495c0ff1ed

### [DISC] stable package — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-5b01f234004df4db` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Use the stable package facade and a simple generated series. from forecastability import TriageRequest, generate_ar1, run_triage"
- `c-f17826be9ca6c52d` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "When numeric correctness matters, trace back to `TriageResult` and the stable package facade."
- `c-0c2606ffcdd0c17e` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The core `forecastability` package has no import-time or runtime dependencies on Darts, MLForecast, StatsForecast, Nixtla, or similar forecasting libraries; any such extras and comparisons are optional and live in the separate `forecastability-examples` repository."
- `c-0c818ceeb5ed84c5` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Analyzer facade, canonical workflow helpers, and rolling-origin support"
- `c-1a78c8e932db48e4` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Top-level package facade with re-exports for `run_triage`, `run_batch_triage`, analyzers, config models, result models, dataset helpers, scorer registry, and validation"
- `c-261dba1aa13e6e82` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The PydanticAI agent layer reads frozen deterministic payloads (A1-A3) and generates natural-language narration. It does not perform any statistical computation or validate the numeric results."
- `c-6a1a40e3376b9f4f` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Use the stable facade first: prefer `forecastability` and `forecastability.triage`."
+ 13 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a boundary for 'stable package'. Re-runnable: prompt sha cc120bbbf51d.

- test: `DISC:stable package`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: The stable public contract is small, and users should anchor on the stable public facades.
- partial hits: c-bea4138eb4aaf4a3, c-f9340e01bd68268b

**Missing element:** a boundary for 'stable package'

**Reasoning:** 1 key(s) state stable package; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test DISC:stable package

### [HEDGE] It is generally considered a good practice to indicate the degree of uncertainty attaching to forecasts. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-2818fef8c18c9e3d` [seed] literature_supported / documentation, key `ind-s-0b00932c0a642b74`, verdict supports: "it is generally considered a good practice to indicate the degree of uncertainty attaching to forecasts."
- `c-4e39686e19b92a20` [closure_near] literature_supported / documentation, key `ind-s-0b00932c0a642b74`, verdict supports: "Transfer entropy from a process X to another process Y is the amount of uncertainty reduced in future values of Y by knowing the past values of X given past values of Y."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of an exception condition. Re-runnable: prompt sha 341444bd7836.

- test: `HEDGE:c-2818fef8c18c9e3d`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: Sentence 4 provides an exception condition for the rule stated in sentences 1-3.
- partial hits: c-4e39686e19b92a20

**Missing element:** an exception condition

**Reasoning:** 1 key(s) state It is generally considered a good practice to indicate the degree of uncertainty attaching to forecasts.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test HEDGE:c-2818fef8c18c9e3d

### [HEDGE] In other disciplines like engineering, the normalization is usually dropped and the terms autocorrelation and autocovariance are used interchangeably. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-04070c929c03d0c4` [seed] literature_supported / documentation, key `ind-s-0b00932c0a642b74`, verdict supports: "However, in other disciplines (e.g. engineering) the normalization is usually dropped and the terms "autocorrelation" and "autocovariance" are used interchangeably."
- `c-6e5c5af4b40ecbf5` [topic] literature_supported / documentation, key `ind-s-0b00932c0a642b74`, verdict supports: "It is common practice in some disciplines (e.g. statistics and time series analysis) to normalize the autocovariance function to get a time-dependent Pearson correlation coefficient."
- `c-ac8ebfd4bba1c07d` [topic] literature_supported / documentation, key `ind-s-0b00932c0a642b74`, verdict supports: "In some fields, the term is used interchangeably with autocovariance."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of an exception condition. Re-runnable: prompt sha 366242b7cddb.

- test: `HEDGE:c-04070c929c03d0c4`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: Sentence 4 provides an exception condition.
- partial hits: c-6e5c5af4b40ecbf5

**Missing element:** an exception condition

**Reasoning:** 1 key(s) state In other disciplines like engineering, the normalization is usually dropped and the terms autocorrelation and autocovariance are used interchangeably.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test HEDGE:c-04070c929c03d0c4

### [HEDGE] Use cases must orchestrate triage models, pipeline helpers, and internal services, and depend on causal discovery through declared ports contracts. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-925a7f61d84ad74d` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Use cases orchestrate triage models, pipeline helpers, and internal services, and depend on causal discovery through declared `ports/` contracts."
- `c-0c818ceeb5ed84c5` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Analyzer facade, canonical workflow helpers, and rolling-origin support"
- `c-12f83d379ed3d9b0` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "PCMCI-AMI orchestration now follows the inward-only dependency rule: use cases depend on declared ports (protocol contracts), and adapters satisfy those contracts without adapter-to-adapter helper coupling."
- `c-17941110bd4a294c` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`CausalGraphPort` `discover(...) -> CausalGraphResult` PCMCI+ style graph discovery"
- `c-2abb88ad6676aac9` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Internal builder/orchestration helpers used by analyzers and use cases"
- `c-54d5f9039aa8eac5` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Keep deterministic orchestration in `use_cases/` and `pipeline/` rather than notebooks or scripts."
+ 11 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of an exception condition. Re-runnable: prompt sha 30c866ea3ae5.

- test: `HEDGE:c-925a7f61d84ad74d`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: PCMCI-AMI follows inward-only dependency rule, implying exceptions.
- partial hits: c-12f83d379ed3d9b0

**Missing element:** an exception condition

**Reasoning:** 1 key(s) state Use cases must orchestrate triage models, pipeline helpers, and internal services, and depend on causal discovery through declared ports contracts.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test HEDGE:c-925a7f61d84ad74d

### [WHY] Significance counts are currently zero across the canonical summary, so actionable lag decisions should rely on class-level screening plus domain checks rather than significance-lag selection alone. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-7af7772c6efe28c5` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "significance counts are currently zero across this canonical summary (`n_sig_ami=0`, `n_sig_pami=0` for all 8), so actionable lag decisions should rely on class-level screening plus domain checks rather than significance-lag selection alone."
- `c-074bbf77d40d49d7` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "directness can be numerically unstable when raw dependence is close to zero. In this slice, 6/7 cases have warning horizons and at least one `directness_ratio > 1.0`, which should be treated as an estimation warning, not scientific evidence of stronger conditioned dependence."
- `c-17a95fd8c5103a99` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Greedy forward selection; redundancy penalty is configurable approximation"
- `c-4a028079c97bc7c6` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "False confidence from one backend decision changes when backend changes model class mismatch or noisy data"
- `c-622a321d0163708d` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The profile compresses the AMI curve into a set of actionable fields: the set of horizons where forecastability clears a significance threshold (the *informative horizon set* $\mathcal{H}_\varepsilon$), the peak horizon, structural shape flags, and model-selection recommendations."
- `c-7c5a34b6e50105e8` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "As the sole decision-maker when surrogate significance bands are unavailable (too-short series): treat the curve as indicative, not authoritative."
+ 3 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a reason. Re-runnable: prompt sha 34b787b90a0f.

- test: `WHY:c-7af7772c6efe28c5`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): synthetic-closed
- judge reason: prevents false confidence from short series
- partial hits: c-acdfdb36da4410cd

**Missing element:** a reason

**Reasoning:** 1 key(s) state Significance counts are currently zero across the canonical summary, so actionable lag decisions should rely on class-level screening plus domain checks rather than significance-lag selection alone.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-7af7772c6efe28c5

### [RESULT] inspecting stress table stability. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-176cff9ac653373b` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Short-sample fragility large backend deltas on small fractions insufficient support for residualization enforce minimum length and inspect stress table stability"
- `c-f38f7c8aa579c1e3` [closure_near] synthetic_extrapolation / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict insufficient — flag: unverified-synthetic: "When series length is very short: finite-sample bias inflates the estimated limit."
- `c-0568df39c001b613` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "For very short series: CrossAMI inherits the same finite-sample bias and minimum- length requirements as univariate AMI."
- `c-1e3de571e58b5ba5` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Short-sample fragility large backend deltas on small fractions insufficient support for residualization"
- `c-2eaebaa88a212810` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The kNN mutual information estimator (Kraskov et al., 2004; `n_neighbors=8`) is asymptotically consistent but has positive bias for finite samples, particularly at short series lengths and large lag indices."
- `c-4ded063d84bc4156` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Approximately $n \geq 3 \times H_{\max}$, where $H_{\max}$ is the maximum evaluation horizon. Below this threshold, MI estimates are unreliable for lags close to $H_{\max}$."
- `c-7afe58436134c4db` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Overfitting in nonlinear backends sharp pAMI spikes at isolated lags only for tree backends backend fits noise in conditioning space compare against linear baseline and require ranking stability"
+ 3 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'inspecting stress table stability.'. Re-runnable: prompt sha 0e22eef4aa48.

- test: `RESULT:c-176cff9ac653373b`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: These sentences describe conditions and consequences but not explicit test results or next actions.
- partial hits: c-1e3de571e58b5ba5, c-e5227ad7e7d197e5
- synthetic hits (unverified): c-f38f7c8aa579c1e3

**Missing element:** a result-to-interpretation mapping for 'inspecting stress table stability.'

**Reasoning:** 1 key(s) state inspecting stress table stability.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-176cff9ac653373b

### [RESULT] tested simultaneously because uncorrected p-values will — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-01a236bf8006dd6e` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Without BH FDR correction when many drivers are tested simultaneously: uncorrected $p$-values will inflate false-positive rates."
- `c-18943cbbab8481d9` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The cross-series mutual information between a target series and one or more candidate exogenous drivers at each forecast horizon, filtered by Benjamini-Hochberg FDR control, to screen which exogenous variables carry statistically detectable predictive signal."
- `c-4c0cd06d6a345f9c` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Prunes redundant drivers; controls false discovery rate across many tests"
- `c-6d3f5a6dbc7b1178` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Without this opt-in, every $k=0$ row for `"holiday_flag"` will have `selected_for_tensor=False` and `tensor_role="diagnostic"`."
- `c-7108a192d336b9eb` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "As a causal or classification proof: a positive $\hat{\lambda}$ does not distinguish deterministic chaos from coloured stochastic noise."
- `c-92ea97938fb3a905` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "For short series ($n < 128$): Welch PSD estimates are based on very few segments and Ω values are unreliable as anything other than a coarse indicator."
+ 3 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'tested simultaneously because uncorrected p-values will'. Re-runnable: prompt sha 9243938fece1.

- test: `RESULT:c-01a236bf8006dd6e`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: Mention expected result or next action
- partial hits: c-01a236bf8006dd6e, c-ece84f6282e09c12

**Missing element:** a result-to-interpretation mapping for 'tested simultaneously because uncorrected p-values will'

**Reasoning:** 1 key(s) state tested simultaneously because uncorrected p-values will; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-01a236bf8006dd6e

### [RESULT] measure, and the forecastability ceiling is set by AMI, not — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-0389d4b5eaef3a19` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "As a sole decision-maker: F6 is a complementary contextual tool, not a forecastability measure. The forecastability ceiling is set by AMI, not entropy."
- `c-55260de7bbeef4fe` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The horizon-wise mutual information between $X_t$ and its own future $X_{t+h}$ (AMI) and the approximate direct-dependence residual (pAMI), producing the informative horizon set $\mathcal{H}_\varepsilon$ and structural shape flags for the triage decision."
- `c-7c5a34b6e50105e8` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "As the sole decision-maker when surrogate significance bands are unavailable (too-short series): treat the curve as indicative, not authoritative."
- `c-abc3a8fdc46d2891` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "As a standalone decision without F1: the limit is derived from the AMI curve, so F1 evidence is prerequisite context."
- `c-cc4810c2ca7437f8` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "As a standalone triage decision: F3 produces a curve and a lookback recommendation, not a scalar forecastability score."
- `c-ea0f41be7f1895c2` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "As a causal screening tool: F8 detects predictive dependence, not causal direction."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'measure, and the forecastability ceiling is set by AMI, not'. Re-runnable: prompt sha 701c98e0c38a.

- test: `RESULT:c-0389d4b5eaef3a19`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: Indicate next action for sole decision-maker scenario
- partial hits: c-7c5a34b6e50105e8

**Missing element:** a result-to-interpretation mapping for 'measure, and the forecastability ceiling is set by AMI, not'

**Reasoning:** 1 key(s) state measure, and the forecastability ceiling is set by AMI, not; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-0389d4b5eaef3a19

### [WHY] After following the canonical notebook path walkthroughs, the `notebooks/triage/` notebooks should be used for deep dives, not as first-stop onboarding. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-2ca293993e13f245` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Use the `notebooks/triage/` notebooks only after the walkthroughs; they are deep dives, not first-stop onboarding."
- `c-3079d77ce22ec266` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "As a replacement for individual deep-dive analysis on flagged series: batch ranking surfaces which series to investigate, not why."
- `c-9e387ffad4c22948` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Most users only need three things in order: 1. The package facade in [../public_api.md](../public_api.md). 2. The notebook path in the [forecastability-examples](https://github.com/AdamKrysztopa/forecastability-examples) sibling repository - see [docs/examples_index.md](../examples_index.md) for the full index. 3. The maintainer scripts documented in [../maintenance/developer_guide.md](../maintenance/developer_guide.md) when they need repo workflows."
- `c-c1a6707518f66c66` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Follow this path before you reach for the CLI, API, dashboard, MCP, or agent layers."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a reason. Re-runnable: prompt sha 9a67d91d535c.

- test: `WHY:c-2ca293993e13f245`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: Prevents misuse as initial onboarding material.
- partial hits: c-2ca293993e13f245

**Missing element:** a reason

**Reasoning:** 1 key(s) state After following the canonical notebook path walkthroughs, the `notebooks/triage/` notebooks should be used for deep dives, not as first-stop onboarding.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-2ca293993e13f245

### [RESULT] test next. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-9fd96f8c30ad5eb5` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Which model families are plausible enough to test next?"
- `c-98c910c65938f691` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The surface suggests starting model families only; it does not fit models or wire downstream frameworks."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'test next.'. Re-runnable: prompt sha cdce25c8e57c.

- test: `RESULT:c-9fd96f8c30ad5eb5`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: Suggests next test but not result or action.
- partial hits: c-9fd96f8c30ad5eb5
- synthetic hits (unverified): c-856cb8ebd2be354e

**Missing element:** a result-to-interpretation mapping for 'test next.'

**Reasoning:** 1 key(s) state test next.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-9fd96f8c30ad5eb5

## §7 checks

### §7.1 Anti-renaming: is the map density in disguise?

Computed over lens candidates only (HYP, RG-SINGLE, RG-UNVER, RG-SIBLING, RG-UNDECIDED and closed candidates) -- RG-UNK and CONTROL are excluded, since their density cannot vary.

- `J10(map, D_low)` = 0.00
- `J10(map, D_high)` = 0.31
- Spearman ρ(score, dens) = 0.41
- flags: closure-uninformative

**Matched-density table** (all lens candidates, by `dens` tercile):

| tercile | n | closed | HYP |
|---|---|---|---|
| low | 24 | 12 | 0 |
| mid | 24 | 14 | 3 |
| high | 24 | 10 | 5 |

Top-tercile closed share: 0.42

**Closure rate by `k_topic` band** (all lens candidates):

| band | n | closed | rate |
|---|---|---|---|
| 0-1 | 54 | 27 | 0.50 |
| 2 | 15 | 8 | 0.53 |
| 3-4 | 3 | 1 | 0.33 |
| >=5 | 0 | 0 | 0.00 |

### S2 fair mismatched-evidence control: does the judge close because of the EVIDENCE, or because of the SEED?

Replaces the first (straw-man) control, second adversarial review, 2026-09-29: the old own-evidence arm always carried the seed's own sentences while the mismatched arm never did (17/22 of PLC's old closures cited only the seed or its source), and the mismatched sentences were off-topic (cyclic gap_id pairing). Now BOTH arms keep the seed's own sentences; the OWN arm adds this candidate's own retrieved non-seed-source sentences; the CONTROL arm replaces those with the non-seed-source sentences retrieved for the topically nearest OTHER candidate of the same lens (max seed-stem Jaccard, ties by gap_id). "other-source-only" is the OWN arm with the seed and same-source sentences excluded entirely -- how often an independent source alone closes it. `closure-uninformative` unless own_rate - control_rate >= 0.20 (of candidates); lenses with < 2 candidates are skipped.

| lens | n | own rate | control rate | other-source-only rate | flag |
|---|---|---|---|---|---|
| DISC | 2 | 1.00 | 0.50 | 1.00 |  |
| HEDGE | 5 | 0.60 | 0.60 | 0.20 | closure-uninformative |
| RESULT | 13 | 1.00 | 0.85 | 0.62 | closure-uninformative |
| SEL | 8 | 1.00 | 1.00 | 0.88 | closure-uninformative |
| WHY | 44 | 0.43 | 0.34 | 0.16 | closure-uninformative |
| **total** | 72 | 0.62 | 0.53 | 0.35 | closure-uninformative |

### S2 lexical donor null: why the lexical closure test was replaced

The reviewer's fair donor null for the (now-comparison-only) LEXICAL closure test: self and same-source claims are excluded from both arms, and the donor is the real non-common content stems of a random other-source A claim of the same knowledge type as the seed (`random.Random(0)`, 200 draws). A check "passes" (is informative) only if the observed count is STRICTLY ABOVE the null's 5-95% interval. DISC is excluded (anchor-regex-driven, not stem-overlap); DIAG is handled per its own closure unit (one rival's sign test, not the group).

| lens | observed closed | null mean | null 5-95% | n | flag |
|---|---|---|---|---|---|
| HEDGE | 0 | 0.1 | [0, 1] | 5 | closure-uninformative |
| RESULT | 4 | 6.0 | [3, 9] | 13 | closure-uninformative |
| SEL | 2 | 3.8 | [1, 6] | 8 | closure-uninformative |
| WHY | 10 | 13.3 | [8, 18] | 44 | closure-uninformative |
| **total** | 16 | 23.1 | [17, 29] |  | closure-uninformative |

### Judge-vs-lexical agreement

Confusion counts, `<lexical_state>-><judge_state>`, over every judged candidate (the lexical test no longer decides anything; this is diagnostic only).

| lexical -> judge | n |
|---|---|
| closed->closed | 26 |
| closed->open | 8 |
| closed->partial | 8 |
| open->closed | 7 |
| open->open | 12 |
| open->partial | 5 |
| open->synthetic-closed | 1 |
| synthetic-closed->closed | 3 |
| synthetic-closed->partial | 1 |
| synthetic-closed->synthetic-closed | 1 |

