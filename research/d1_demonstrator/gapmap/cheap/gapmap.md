# Gap map: forecastability

- Ledger: `e48961dcb5b24430a6c6be8515c1e1335808fc487a2a6b90bc7278f1bf42c20b`
- Config: `35fd0af25618f8d6e0d1c2c3707d7e932afe2ce72dbd01e956034b43bfeb04c1`
- **Admissibility note:** sidecar n3_input is false: E-PLANT corpus contains planted fabrications

## Summary

- **HYP:** 0 total (none)
- **Retrieval gaps:** RG-UNK 46, RG-SINGLE 27, RG-UNVER 1, RG-UNDECIDED 2
- **Control slot:** 1
- **PROMO-excluded seeds (S3 defect 1):** 3
- **§7.1 anti-renaming:** J10(low)=0.00, J10(high)=0.00, ρ(score,dens)=0.00, flags: closure-uninformative

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

(no hidden-knowledge hypotheses survived the caps and gates)

## Control slot

The §14.2 unknown-unknowns guard: an area no hypothesis touched, walked cold.

### Interpreting forecastability results

*lens: —; category: CONTROL*

**OBSERVED EVIDENCE**

(none)

**INFERRED GAP**

Control slot: area 'Interpreting forecastability results' (a-c61a3556df64ebe7) has no HYP record and the highest attested share (0.82) among candidate areas of ledger e48961dc.

- test: `CONTROL:a-c61a3556df64ebe7`; state: open (closure judge: )

**Reasoning:** the §14.2 unknown-unknowns guard: no HYP touches this area

**Breadth:** narrow (uncalibrated; no gold) (score 0 = A0 + B0 − P0; k_step=0, k_topic=0); lexical robustness 0/4

**Expert question** (channel: control):

> Walk me through how you carry out Interpreting forecastability results, from start to finish, as if I were watching you do it. What do you check, and in what order?

## Retrieval gaps

Not hypotheses: each one's action is to search further or verify a synthetic span, never to ask an expert.

### RG-UNK: slots searched, nothing found

| area | slot / question | source |
|---|---|---|
| Understanding horizon-wise forecastability concepts | concept slot searched, only thin coverage found | sidecar slot |
| Setting up and running the toolkit | procedure_step slot searched, only thin coverage found | sidecar slot |
| Setting up and running the toolkit | concept slot searched, only thin coverage found | sidecar slot |
| Practical application and examples | procedure_step slot searched, only thin coverage found | sidecar slot |
| Interpreting forecastability results | check slot searched, only thin coverage found | sidecar slot |
| Understanding horizon-wise forecastability concepts | cue slot searched, only thin coverage found | sidecar slot |
| Setting up and running the toolkit | norm slot searched, only thin coverage found | sidecar slot |
| Interpreting forecastability results | procedure_step slot searched, only thin coverage found | sidecar slot |
| Extending toolkit functionality | norm slot searched, only thin coverage found | sidecar slot |
| Understanding horizon-wise forecastability concepts | norm slot searched, only thin coverage found | sidecar slot |
| Interpreting forecastability results | concept slot searched, only thin coverage found | sidecar slot |
| Interpreting forecastability results | cue slot searched, only thin coverage found | sidecar slot |
| Extending toolkit functionality | concept slot searched, only thin coverage found | sidecar slot |
| Interpreting forecastability results | norm slot searched, only thin coverage found | sidecar slot |
| Practical application and examples | rationale slot searched, only thin coverage found | sidecar slot |
| Understanding horizon-wise forecastability concepts | failure_mode slot searched, only thin coverage found | sidecar slot |
| Practical application and examples | concept slot searched, only thin coverage found | sidecar slot |
| Interpreting forecastability results | failure_mode slot searched, only thin coverage found | sidecar slot |
| Extending toolkit functionality | failure_mode slot searched, only thin coverage found | sidecar slot |
| Extending toolkit functionality | procedure_step slot searched, only thin coverage found | sidecar slot |
| Practical application and examples | norm slot searched, only thin coverage found | sidecar slot |
| Understanding horizon-wise forecastability concepts | rationale slot searched, only thin coverage found | sidecar slot |
| Understanding horizon-wise forecastability concepts | procedure_step slot searched, only thin coverage found | sidecar slot |
| Setting up and running the toolkit | decision slot searched, only thin coverage found | sidecar slot |
| Interpreting forecastability results | rationale slot searched, only thin coverage found | sidecar slot |
| Practical application and examples | decision slot searched, only thin coverage found | sidecar slot |
| Setting up and running the toolkit | failure_mode slot searched, nothing found | sidecar slot |
| Understanding horizon-wise forecastability concepts | decision slot searched, only thin coverage found | sidecar slot |
| Extending toolkit functionality | decision slot searched, only thin coverage found | sidecar slot |
| Practical application and examples | failure_mode slot searched, only thin coverage found | sidecar slot |
| Setting up and running the toolkit | cue slot searched, only thin coverage found | sidecar slot |
| Setting up and running the toolkit | check slot searched, only thin coverage found | sidecar slot |
| Extending toolkit functionality | rationale slot searched, only thin coverage found | sidecar slot |
| Practical application and examples | cue slot searched, only thin coverage found | sidecar slot |
| Understanding horizon-wise forecastability concepts | check slot searched, only thin coverage found | sidecar slot |
| Setting up and running the toolkit | How does work in Setting up and running the toolkit typically go wrong, and what are the signs? | ledger U claim `c-34f70d086a03cba2` |
| Extending toolkit functionality | cue slot searched, nothing found | sidecar slot |
| Practical application and examples | How is work in Practical application and examples checked for correctness or compliance? | ledger U claim `c-b7fdea204a145ce6` |
| Interpreting forecastability results | decision slot searched, nothing found | sidecar slot |
| Setting up and running the toolkit | Why is Setting up and running the toolkit done the way it is? | ledger U claim `c-0c2e3c12edad6591` |
| Setting up and running the toolkit | rationale slot searched, nothing found | sidecar slot |
| Extending toolkit functionality | check slot searched, nothing found | sidecar slot |
| Practical application and examples | check slot searched, nothing found | sidecar slot |
| Interpreting forecastability results | What conditions determine which option is chosen in Interpreting forecastability results? | ledger U claim `c-a3b40767597fb3fb` |
| Extending toolkit functionality | How is work in Extending toolkit functionality checked for correctness or compliance? | ledger U claim `c-ed27a52d0bd653b0` |
| Extending toolkit functionality | What observable features of a situation signal that Extending toolkit functionality applies or needs | ledger U claim `c-9826fd873d681840` |

### [WHY] In rolling-origin evaluation, diagnostics should be computed on train windows only. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-d7d073c08a1e9cc5` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "In rolling-origin evaluation, compute diagnostics on train windows only."
- `c-02db4a573b917ded` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "In rolling-origin evaluation, diagnostics are computed on train windows only and scoring on post-origin holdout only."
- `c-3e06b2d68146d02f` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "AMI, pAMI, and all F1-F8 diagnostics are computed on the training window up to each rolling origin. No diagnostic touches the post-origin holdout."
- `c-5e6c39566b0cc4f6` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Forecast errors and accuracy metrics are computed on the post-origin holdout window only."
- `c-792adbbd1d1fac2a` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`pipeline/rolling_origin.py` contains rolling-origin split helpers used by evaluation workflows."
- `c-7b0d037b682a6113` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "pipeline/` Analyzer facade, canonical workflow helpers, and rolling-origin support"
+ 5 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 1bc5928a9360.

- test: `WHY:c-d7d073c08a1e9cc5`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: prevents look-ahead leakage

**Missing element:** a reason

**Reasoning:** 1 key(s) state In rolling-origin evaluation, diagnostics should be computed on train windows only.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-d7d073c08a1e9cc5

### [WHY] Forecastability triage should cover readiness, leakage risk, informative horizons, primary lags, seasonality structure, and covariate informativeness before recommending downstream model families or framework-specific settings. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-57756095892fe1d8` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Start with forecastability triage first: readiness, leakage risk, informative horizons, primary lags, seasonality structure, and covariate informativeness. Only then recommend downstream model families or framework-specific settings."
- `c-09a56c0db2a8bbc8` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "This package encourages a different workflow: data → forecastability triage → lag / driver / readiness diagnostics → ForecastPrepContract → downstream model search"
- `c-31524d4ec7dfcb67` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "a `ForecastPrepContract` - a structured, machine-readable hand-off contract for downstream model families."
- `c-6215c841ac206817` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Advanced triage namespace for batch models, readiness helpers, events, bundle types, and triage-specific diagnostics"
- `c-719558607fd4468f` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Approximately $n \geq 3 \times H_{\max}$, where $H_{\max}$ is the maximum evaluation horizon. Below this threshold, MI estimates are unreliable for lags close to $H_{\max}$."
- `c-76ac2b1d44f33259` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "primary_lags` Informative lags identified by the deterministic workflow"
+ 3 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha f1e4be5c8fa1.

- test: `WHY:c-57756095892fe1d8`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): synthetic-closed
- judge reason: 2,3,4,5,6,7,8,9,10,11,12

**Missing element:** a reason

**Reasoning:** 1 key(s) state Forecastability triage should cover readiness, leakage risk, informative horizons, primary lags, seasonality structure, and covariate informativeness before recommending downstream model families or framework-specific settings.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-57756095892fe1d8

### [WHY] This toolkit should not be used for proving physical causality between variables. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-abe15f9e9273dd14` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Do Not Use This For - Proving physical causality between variables."
- `c-0d74f7eb45a93314` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Which variables are safe to use without leakage?"

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 55de9b532476.

- test: `WHY:c-abe15f9e9273dd14`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: prevents misuse leading to incorrect conclusions

**Missing element:** a reason

**Reasoning:** 1 key(s) state This toolkit should not be used for proving physical causality between variables.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-abe15f9e9273dd14

### [WHY] F5 should only be used for exploratory research as one piece of converging evidence alongside F1 and F6. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-67e5eac5fb8bec5e` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Exploratory research only: as one piece of converging evidence that a series may exhibit chaotic dynamics, always alongside F1 and F6."
- `c-e433c9acfb61e068` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Alongside F5 (when enabled) for convergence evidence on chaos vs stochasticity."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 5ed5d40753de.

- test: `WHY:c-67e5eac5fb8bec5e`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: prevents failure of relying on a single piece of evidence

**Missing element:** a reason

**Reasoning:** 1 key(s) state F5 should only be used for exploratory research as one piece of converging evidence alongside F1 and F6.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-67e5eac5fb8bec5e

### [WHY] The horizon-specific AMI curve should never be collapsed before analysis. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-d586c094984966f5` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Horizon-specific curve, never collapsed before analysis."
- `c-cdcf82289f074548` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "src/forecastability/pipeline/analyzer.py`: `ForecastabilityAnalyzer` and `ForecastabilityAnalyzerExog` support `method="te"` for raw-curve analysis and TE surrogate significance bands."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha a736836e0bc5.

- test: `WHY:c-d586c094984966f5`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: When you suspect that longer lags add noise rather than signal (the curve never plateauing is also informative).

**Missing element:** a reason

**Reasoning:** 1 key(s) state The horizon-specific AMI curve should never be collapsed before analysis.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-d586c094984966f5

### [WHY] New user-facing imports should be added through forecastability or forecastability.triage only when committing to compatibility. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-007b692334093e05` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Add new user-facing imports through `forecastability` or `forecastability.triage` only when you want to commit to compatibility."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha fe96433a8956.

- test: `WHY:c-007b692334093e05`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: ensures compatibility

**Missing element:** a reason

**Reasoning:** 1 key(s) state New user-facing imports should be added through forecastability or forecastability.triage only when committing to compatibility.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-007b692334093e05

### [WHY] AMI and pAMI should be kept horizon-specific and not pre-aggregated before triage. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-8eabb66a53df1fee` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Keep AMI and pAMI horizon-specific; do not pre-aggregate before triage."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 51e87f900358.

- test: `WHY:c-8eabb66a53df1fee`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: 4,5

**Missing element:** a reason

**Reasoning:** 1 key(s) state AMI and pAMI should be kept horizon-specific and not pre-aggregated before triage.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-8eabb66a53df1fee

### [WHY] This toolkit should not be used for setting maintenance policy thresholds without domain constraints and risk-cost modeling. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-75dbed74d0cff629` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Setting maintenance policy thresholds without domain constraints and risk-cost modeling."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha ef82a0374b2f.

- test: `WHY:c-75dbed74d0cff629`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: prevents incorrect threshold setting

**Missing element:** a reason

**Reasoning:** 1 key(s) state This toolkit should not be used for setting maintenance policy thresholds without domain constraints and risk-cost modeling.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-75dbed74d0cff629

### [WHY] pAMI should not be treated as an exact nonlinear conditional mutual information estimate. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-753a7aacc87f29c1` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Treating pAMI as an exact nonlinear conditional mutual information estimate."
- `c-8be817ba0cc340ba` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "pAMI is a project extension that uses a linear-residual approximation rather than exact conditional mutual information."
- `c-a9704cb5a8876907` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "pAMI is a **project extension** and is not paper-native. It approximates $I(X_t; X_{t+h} \mid X_{t+1}, \ldots, X_{t+h-1})$ via linear (or optional RF) residualisation, not by exact conditional MI estimation."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 47f1a55e817d.

- test: `WHY:c-753a7aacc87f29c1`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: 3

**Missing element:** a reason

**Reasoning:** 1 key(s) state pAMI should not be treated as an exact nonlinear conditional mutual information estimate.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-753a7aacc87f29c1

### [WHY] When the task is time-series forecasting, forecastability triage should be started before model fitting. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-67e99a77efcb1ef0` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "When the task is time-series forecasting, do not jump directly to model fitting. Start with forecastability triage first"
- `c-052db13533fa9643` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "When the task is time-series forecasting, do not jump directly to model fitting. Start with forecastability triage first:"
- `c-cbf35282596649f2` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "This repository is a deterministic forecastability triage toolkit for time series."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 13c992b33cd1.

- test: `WHY:c-67e99a77efcb1ef0`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: to select the lookback window for a forecasting model

**Missing element:** a reason

**Reasoning:** 1 key(s) state When the task is time-series forecasting, forecastability triage should be started before model fitting.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-67e99a77efcb1ef0

### [WHY] Escalation should occur only when nonlinear backends improve diagnostic consistency across datasets. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-5ff63882db181126` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Escalate only when nonlinear backends improve diagnostic consistency across datasets."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha b7cf8002ef32.

- test: `WHY:c-5ff63882db181126`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: prevents failure in diagnostic consistency

**Missing element:** a reason

**Reasoning:** 1 key(s) state Escalation should occur only when nonlinear backends improve diagnostic consistency across datasets.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-5ff63882db181126

### [HEDGE] The upper surrogate band is operationally informative for detecting non-null dependence, while the lower band is usually near zero for MI and is not typically operationally useful. — RG-UNVER

*Action: verify — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-53564f05f2268320` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The upper band is operationally informative for detecting non-null dependence. The lower band is usually near zero for MI and is not typically operationally useful."
- `c-d094481fb68d47bb` [closure_near] synthetic_extrapolation / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict insufficient — flag: unverified-synthetic: "When no lags clear the surrogate band, $\varepsilon$ is set above the curve maximum so that `informative_horizons` is empty."
- `c-097b7b072e068319` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Surrogate significance uses phase-randomized surrogates and two-sided 95% quantiles: - lower: 2.5th percentile - upper: 97.5th percentile"
- `c-43d3dd12bc2ea848` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Phase-randomized surrogate significance bands require a minimum series length to produce stable quantile estimates. When the series is too short, significance may be unavailable and the surrogate bands are omitted."
- `c-66c250dc8aa52432` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Narrows model evaluation to productive horizons; detects non-monotone seasonal structure"
- `c-760675ee1943db9c` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Spearman is also near zero because $ X $ is V-shaped (non-monotone) in $X$."
- `c-8a05a055c7b92455` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Use upper-band crossings to detect non-null dependence."
+ 12 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating an exception condition among the verified sentences retrieved (4 unverified sentences considered separately). Re-runnable: prompt sha 174d4e1f11b1.

- test: `HEDGE:c-53564f05f2268320`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): synthetic-closed
- judge reason: specific cases where the rule does not hold
- synthetic hits (unverified): c-40421a9af4fd9863, c-5a820dfd062f355d, c-d094481fb68d47bb

**Missing element:** an exception condition

**Reasoning:** 1 key(s) state The upper surrogate band is operationally informative for detecting non-null dependence, while the lower band is usually near zero for MI and is not typically operationally useful.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test HEDGE:c-53564f05f2268320

### [HEDGE] PCMCI-AMI orchestration follows the inward-only dependency rule: use cases depend on declared ports, and adapters satisfy those contracts without adapter-to-adapter helper coupling. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-2192244453756589` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "PCMCI-AMI orchestration now follows the inward-only dependency rule: use cases depend on declared ports (protocol contracts), and adapters satisfy those contracts without adapter-to-adapter helper coupling."
- `c-14dda9a7a271377e` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Put transport concerns in `adapters/`, not in use cases or metrics code."
- `c-390244c80805860b` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The architecture goal is still inward dependency flow."
- `c-3abcee0ac5bda578` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "CausalGraphPort` `discover(...) -> CausalGraphResult` PCMCI+ style graph discovery"
- `c-434ff0a66875fb8e` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "use_cases/` Main orchestration entry points for deterministic triage and batch triage"
- `c-488f37627b61fae5` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "CausalGraphFullPort` `discover(...) -> CausalGraphResult` and `discover_full(...) -> PcmciAmiResult` PCMCI-AMI full three-phase result path"
+ 8 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating an exception condition. Re-runnable: prompt sha e3922b4bf76b.

- test: `HEDGE:c-2192244453756589`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: No exceptions to the rule are explicitly stated.

**Missing element:** an exception condition

**Reasoning:** 1 key(s) state PCMCI-AMI orchestration follows the inward-only dependency rule: use cases depend on declared ports, and adapters satisfy those contracts without adapter-to-adapter helper coupling.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test HEDGE:c-2192244453756589

### [WHY] services/ should be treated as internal helpers, not as a third public API layer. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-86c5a454caa43627` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Treat `services/` as internal helpers, not as a third public API layer."
- `c-632cedcf139eff2c` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "CLI, API, scripts, MCP, and agents are optional access or narration layers around the same deterministic outputs."
- `c-69285d21a7b847aa` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Follow this path before you reach for the CLI, API, dashboard, MCP, or agent layers."
- `c-6ccb4c89f47d7cb2` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The internal packages, the MCP surface, and the agent layer are useful only after the deterministic workflow is already understood."
- `c-6d51ab3cf41cdb9b` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "the stable public contract is small, while the internal package tree is deliberately split across triage models, use cases, analyzers, metrics, diagnostics, reporting, utils, adapters, services, ports, and bootstrap helpers."
- `c-825cf52b99f40fe5` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Triage, pipeline, and services consume metrics, diagnostics, reporting, and utils."
+ 5 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha e81035792e9a.

- test: `WHY:c-86c5a454caa43627`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: prevents exposing internal helpers as public API

**Missing element:** a reason

**Reasoning:** 1 key(s) state services/ should be treated as internal helpers, not as a third public API layer.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-86c5a454caa43627

### [WHY] At least n_surrogates = 99 is required for a valid two-sided 95% confidence band, and fewer than 99 surrogates are not sufficient and must not be used as a significance threshold. — RG-UNDECIDED

*Action: re-judge or inspect — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-6144da63ab9a0d5a` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "At least `n_surrogates = 99` is required for a valid two-sided 95% band. Fewer than 99 surrogates are not sufficient and must not be used as a significance threshold."
- `c-05dbf0907edceed5` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Surrogate significance is optional, requires feasible sample size, and needs at least 99 surrogates."
- `c-0869da46b065ba5c` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "False confidence from one backend decision changes when backend changes model class mismatch or noisy data require cross-backend agreement before acting on lag recommendations"
- `c-097b7b072e068319` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Surrogate significance uses phase-randomized surrogates and two-sided 95% quantiles: - lower: 2.5th percentile - upper: 97.5th percentile"
- `c-0bfdaf4bd0e61712` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`default_epsilon` Fallback threshold when surrogates are not requested"
- `c-150871fa9f37946b` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Inherits AMI estimator reliability; requires surrogates for epsilon anchoring"
+ 3 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) gave an unusable answer (the reply has no 'states'/'partially' list) -- re-judge or inspect manually, rather than treat this as open. Re-runnable: prompt sha 6283425c8bad.

- test: `WHY:c-6144da63ab9a0d5a`; state: undecided (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: the reply has no 'states'/'partially' list

**Missing element:** a reason

**Reasoning:** 1 key(s) state At least n_surrogates = 99 is required for a valid two-sided 95% confidence band, and fewer than 99 surrogates are not sufficient and must not be used as a significance threshold.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-6144da63ab9a0d5a

### [WHY] Significance counts are currently zero across the canonical summary, so actionable lag decisions should rely on class-level screening plus domain checks rather than significance-lag selection alone. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-7af7772c6efe28c5` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "significance counts are currently zero across this canonical summary (`n_sig_ami=0`, `n_sig_pami=0` for all 8), so actionable lag decisions should rely on class-level screening plus domain checks rather than significance-lag selection alone."
- `c-072638895e9ad8fe` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "forecastability_class` High-level interpretation when triage completed"
- `c-1a4658f1577b2d9b` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The profile compresses the AMI curve into a set of actionable fields: the set of horizons where forecastability clears a significance threshold (the *informative horizon set* $\mathcal{H}_\varepsilon$), the peak horizon, structural shape flags, and model-selection recommendations."
- `c-28b4da9f7795b4d4` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "when data are significance-infeasible (for example n=150 in regression tests), surrogates are skipped and decisions are route/class screening only."
- `c-6b0d51a3406445eb` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Greedy forward selection; redundancy penalty is configurable approximation"
- `c-a03a397bdf37dfc0` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "a quadratic driver with near-zero Pearson correlation can be a strong predictive feature; always cross-check with `cross_ami`"
+ 3 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 0694044b53f2.

- test: `WHY:c-7af7772c6efe28c5`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): synthetic-closed
- judge reason: 3,4

**Missing element:** a reason

**Reasoning:** 1 key(s) state Significance counts are currently zero across the canonical summary, so actionable lag decisions should rely on class-level screening plus domain checks rather than significance-lag selection alone.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-7af7772c6efe28c5

### [WHY] Transport concerns should be put in adapters/, not in use cases or metrics code. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-14dda9a7a271377e` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Put transport concerns in `adapters/`, not in use cases or metrics code."
- `c-2192244453756589` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "PCMCI-AMI orchestration now follows the inward-only dependency rule: use cases depend on declared ports (protocol contracts), and adapters satisfy those contracts without adapter-to-adapter helper coupling."
- `c-4e2c69094b68cc2d` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Entrypoints and adapters call the package facades or use cases."
- `c-6d51ab3cf41cdb9b` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "the stable public contract is small, while the internal package tree is deliberately split across triage models, use cases, analyzers, metrics, diagnostics, reporting, utils, adapters, services, ports, and bootstrap helpers."
- `c-800b35d358c081ff` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`adapters/` runtime entry points Supported runtime surfaces, but transport details may evolve"
- `c-bd1e916d68bcfd18` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The dashboard is a thin browser UI over the deterministic adapters."
+ 1 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 45d781dccfac.

- test: `WHY:c-14dda9a7a271377e`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: inadmissible reason stated

**Missing element:** a reason

**Reasoning:** 1 key(s) state Transport concerns should be put in adapters/, not in use cases or metrics code.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-14dda9a7a271377e

### [WHY] In exogenous screening results, 6 out of 7 cases have warning horizons and at least one directness_ratio > 1.0, which should be treated as an estimation warning, not scientific evidence of stronger conditioned dependence. — RG-UNDECIDED

*Action: re-judge or inspect — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-a6aefd04832669ef` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "6/7 cases have warning horizons and at least one `directness_ratio > 1.0`, which should be treated as an estimation warning, not scientific evidence of stronger conditioned dependence."
- `c-6ba66a9482d8beb1` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Numerical inflation `directness_ratio > 1.0` estimator instability, finite-sample effects"
- `c-6cd11f0e30d05f50` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "This repository flags `directness_ratio > 1.0` as `arch_suspected`."
- `c-6e81eaa5ab980b86` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Prefer stable lag rankings and small directness-ratio range over raw pAMI magnitude."
- `c-8d2bbe61fa3507b7` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Numerical inflation `directness_ratio > 1.0` estimator instability, finite-sample effects Treat as warning; verify with multiple backends and sample-size stress"
- `c-98ac1392720c2bc3` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "multiple noise-linked cases can be deprioritised early."
+ 8 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) gave an unusable answer (the reply has no 'states'/'partially' list) -- re-judge or inspect manually, rather than treat this as open. Re-runnable: prompt sha b21eeb2b7a2c.

- test: `WHY:c-a6aefd04832669ef`; state: undecided (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: the reply has no 'states'/'partially' list

**Missing element:** a reason

**Reasoning:** 1 key(s) state In exogenous screening results, 6 out of 7 cases have warning horizons and at least one directness_ratio > 1.0, which should be treated as an estimation warning, not scientific evidence of stronger conditioned dependence.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-a6aefd04832669ef

### [WHY] With non-empty conditioning history in Transfer Entropy, at least 2 * min_pairs aligned rows are required. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-fd2e7d186e66bfd0` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "with non-empty conditioning history, at least `2 * min_pairs` aligned rows are required."
- `c-50fc7b0f8e7ef7f4` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Conditioning on target history controls for autocorrelation-driven carryover in \(Y\)."
- `c-56c7e2352b86c464` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Analyzer path is raw-only for TE: partial TE is intentionally unsupported."
- `c-5ae8a57e691e2b17` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Positive TE indicates added predictive information from source history beyond target-only history."
- `c-794b1929aaf9c87a` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Directional extension metric Transfer Entropy (TE) at lag \(h\): \[ TE(X \to Y \mid h) = I(Y_t ; X_{t-h} \mid Y_{t-1},\ldots,Y_{t-h+1}) \]"
- `c-8627cbdd8787a692` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Directional predictive dependence: in general \(TE(X \to Y) \neq TE(Y \to X)\)."
+ 8 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 484a26c3f995.

- test: `WHY:c-fd2e7d186e66bfd0`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: prevents failure due to insufficient data for accurate estimation

**Missing element:** a reason

**Reasoning:** 1 key(s) state With non-empty conditioning history in Transfer Entropy, at least 2 * min_pairs aligned rows are required.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-fd2e7d186e66bfd0

### [WHY] Any new selector going further than xami_sparse (PMIME-style, PC-stable with driver autohistory) must be introduced under a new method label so that shipped cross_pami and xami_sparse semantics are not silently extended. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-040cb35e6c34f7b5` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Any new selector that goes further (PMIME-style, PC-stable with driver autohistory) must be introduced under a **new method label** so that the shipped `cross_pami` and `xami_sparse` semantics are not silently extended."
- `c-00beaeea1bbcce97` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The v0.3.0 `cross_pami` curve remains `target_only` conditioned and covers $k \in \{1, \dots, K_{\max}\}$ only."
- `c-046dab40441271aa` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "In combination with F1: F8 extends the analysis to cross-series dependence; F1 remains the primary univariate anchor."
- `c-0fc8a743e95bf7e2` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "**At least one row per `(target, driver)` pair** is emitted by the selector."
- `c-1a1a3d9f0c351840` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Results differ between the linear (default) and RF backends. The linear backend is faster and more stable; the RF backend may capture more nonlinear residual structure but introduces additional noise for short series."
- `c-50f023c54f13be90` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Any elastic-alignment result would need a new surface, a new method label, and an explicit chronological-causality guard before it could be admitted to a forecasting tensor."
+ 4 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha e82e6c6042f5.

- test: `WHY:c-040cb35e6c34f7b5`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: 2

**Missing element:** a reason

**Reasoning:** 1 key(s) state Any new selector going further than xami_sparse (PMIME-style, PC-stable with driver autohistory) must be introduced under a new method label so that shipped cross_pami and xami_sparse semantics are not silently extended.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-040cb35e6c34f7b5

### [GUARD] F8 should be used when you need a principled multiple-testing correction to control false positives across many candidate drivers. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-8b83dda07034fe22` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "When you need a principled multiple-testing correction to control false positives across many candidate drivers."
- `c-2f5425786a617b4f` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The cross-series mutual information between a target series and one or more candidate exogenous drivers at each forecast horizon, filtered by Benjamini-Hochberg FDR control, to screen which exogenous variables carry statistically detectable predictive signal."
- `c-943badfd7c61d2b4` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Prunes redundant drivers; controls false discovery rate across many tests"
- `c-b76d0772fa3b2025` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Without BH FDR correction when many drivers are tested simultaneously: uncorrected $p$-values will inflate false-positive rates."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a detection cue. Re-runnable: prompt sha 3982e2ab58dc.

- test: `GUARD:c-8b83dda07034fe22`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: No sentence directly states how a practitioner notices the error before or as it happens.

**Missing element:** a detection cue

**Reasoning:** 1 key(s) state F8 should be used when you need a principled multiple-testing correction to control false positives across many candidate drivers.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test GUARD:c-8b83dda07034fe22

### [WHY] F2 should not be used as a standalone decision without F1 because the limit is derived from the AMI curve. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-4a21fbf2da550af4` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "As a standalone decision without F1: the limit is derived from the AMI curve, so F1 evidence is prerequisite context."
- `c-3a92349c4938c49e` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "When you want to know *why* AMI is low - limit compression reveals whether the ceiling is genuinely low (hard limit) or whether the sampled curve has not saturated the limit."
- `c-4827afa49c4c1a69` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "As a standalone triage decision: F3 produces a curve and a lookback recommendation, not a scalar forecastability score."
- `c-ed56aa8d28a933b8` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The information-theoretic upper bound on forecastability derived from the AMI curve, including compression ratio and predictability ceiling, to quantify how close any model can get to the fundamental limit."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 8b63380970d5.

- test: `WHY:c-4a21fbf2da550af4`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: 2,5,7

**Missing element:** a reason

**Reasoning:** 1 key(s) state F2 should not be used as a standalone decision without F1 because the limit is derived from the AMI curve.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-4a21fbf2da550af4

### [WHY] F7 should not be used as a replacement for individual deep-dive analysis on flagged series. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-949da5078b228aae` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "As a replacement for individual deep-dive analysis on flagged series: batch ranking surfaces which series to investigate, not why."
- `c-42aca8abc47b432c` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Use the `notebooks/triage/` notebooks only after the walkthroughs; they are deep dives, not first-stop onboarding."
- `c-92b5a609a6917a27` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "As the entry point for any multi-series analysis; individual series results remain accessible through the batch result object."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 46ecc3a75430.

- test: `WHY:c-949da5078b228aae`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: prevents failure to understand why a series is flagged

**Missing element:** a reason

**Reasoning:** 1 key(s) state F7 should not be used as a replacement for individual deep-dive analysis on flagged series.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-949da5078b228aae

### [WHY] F3 should not be used as a standalone triage decision because it produces a curve and a lookback recommendation, not a scalar forecastability score. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-4827afa49c4c1a69` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "As a standalone triage decision: F3 produces a curve and a lookback recommendation, not a scalar forecastability score."
- `c-1a4658f1577b2d9b` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The profile compresses the AMI curve into a set of actionable fields: the set of horizons where forecastability clears a significance threshold (the *informative horizon set* $\mathcal{H}_\varepsilon$), the peak horizon, structural shape flags, and model-selection recommendations."
- `c-4a21fbf2da550af4` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "As a standalone decision without F1: the limit is derived from the AMI curve, so F1 evidence is prerequisite context."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 0addf60fefe2.

- test: `WHY:c-4827afa49c4c1a69`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: False confidence from one backend decision changes when backend changes model class mismatch or noisy data require cross-backend agreement before acting on lag recommendations

**Missing element:** a reason

**Reasoning:** 1 key(s) state F3 should not be used as a standalone triage decision because it produces a curve and a lookback recommendation, not a scalar forecastability score.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-4827afa49c4c1a69

### [WHY] F7 should not be used when F5 output is desired in the ranking because LLE is intentionally excluded. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-7ad28c619729b90a` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "When F5 output is desired in the ranking: LLE is intentionally excluded from automated batch triage by design."
- `c-a2591283bf7e55e0` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "LLE is intentionally excluded from the batch triage ranking table (F7) by design."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 903e73c464d1.

- test: `WHY:c-7ad28c619729b90a`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: to avoid including noise lags or excluding genuinely informative ones as signal strength varies across series

**Missing element:** a reason

**Reasoning:** 1 key(s) state F7 should not be used when F5 output is desired in the ranking because LLE is intentionally excluded.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-7ad28c619729b90a

### [RESULT/WHY] measure because Ω misses nonlinear dependence entirely. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-520a1e7ba216f30b` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "As the sole forecastability measure: Ω misses nonlinear dependence entirely."
- `c-97859db84d78c736` [closure_near] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "linear_residual` Fast, stable, interpretable baseline Misses nonlinear mediation"
- `c-97be86317cc83c2d` [closure_near] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "linear_residual` Fast, stable, interpretable baseline Misses nonlinear mediation Default benchmark and production-safe baseline"

**[RESULT]**

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'measure because Ω misses nonlinear dependence entirely.'. Re-runnable: prompt sha c7c40c98f5a6.

- test: `RESULT:c-520a1e7ba216f30b`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: mentions expected results or next actions
- partial hits: c-520a1e7ba216f30b, c-97859db84d78c736, c-97be86317cc83c2d

**Missing element:** a result-to-interpretation mapping for 'measure because Ω misses nonlinear dependence entirely.'

**Reasoning:** 1 key(s) state measure because Ω misses nonlinear dependence entirely.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-520a1e7ba216f30b

**[WHY]**

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 38f16ef97edf.

- test: `WHY:c-520a1e7ba216f30b`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: Ω misses nonlinear dependence entirely.

**Missing element:** a reason

**Reasoning:** 1 key(s) state F4 should not be used as the sole forecastability measure because Ω misses nonlinear dependence entirely.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-520a1e7ba216f30b

### [WHY] F5 largest Lyapunov exponent must be explicitly enabled via experimental: true in the config and does not run in default triage mode. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-e63a68471867efe0` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "F5 must be explicitly enabled via `experimental: true` in the config. It does not run in default triage mode."
- `c-147115fe8f2a62ea` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Reliable phase-space coverage requires $n \gg 10^m$. For the default $m = 3$ this means $n \gg 1000$. Results for shorter series are indicative only."
- `c-1a78c8e932db48e4` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Top-level package facade with re-exports for `run_triage`, `run_batch_triage`, analyzers, config models, result models, dataset helpers, scorer registry, and validation"
- `c-4bb192a32090aaf8` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The Rosenstein algorithm and Takens embedding are sensitive to noise, non-stationarity, and the choice of embedding parameters ($m$, $\tau$, Theiler window, evolution time $s$). Small parameter changes can produce meaningfully different $\hat{\lambda}$ values."
- `c-5fdbc156ebef1353` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Treating experimental diagnostics (F5 Lyapunov) as automated decision criteria without expert review."
- `c-8b0f03054da11f84` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Differentiates deterministic chaos from stochastic noise (when sample size permits)"
+ 3 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a reason. Re-runnable: prompt sha 16ff552da302.

- test: `WHY:c-e63a68471867efe0`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: Unreliable at finite sample sizes, sensitive to noise, and requires large sample size
- partial hits: c-147115fe8f2a62ea, c-4bb192a32090aaf8, c-a57574d333d7a5a5

**Missing element:** a reason

**Reasoning:** 1 key(s) state F5 largest Lyapunov exponent must be explicitly enabled via experimental: true in the config and does not run in default triage mode.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-e63a68471867efe0

### [RESULT] comparing against linear baseline and requiring ranking — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-7afe58436134c4db` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Overfitting in nonlinear backends sharp pAMI spikes at isolated lags only for tree backends backend fits noise in conditioning space compare against linear baseline and require ranking stability"
- `c-0869da46b065ba5c` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "False confidence from one backend decision changes when backend changes model class mismatch or noisy data require cross-backend agreement before acting on lag recommendations"
- `c-176cff9ac653373b` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Short-sample fragility large backend deltas on small fractions insufficient support for residualization enforce minimum length and inspect stress table stability"
- `c-50a455f13a13bd70` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Composite weighting across incommensurable scales must be transparent"

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'comparing against linear baseline and requiring ranking'. Re-runnable: prompt sha 067e1a482495.

- test: `RESULT:c-7afe58436134c4db`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: False confidence mitigation leads to cross-backend agreement requirement.
- partial hits: c-0869da46b065ba5c

**Missing element:** a result-to-interpretation mapping for 'comparing against linear baseline and requiring ranking'

**Reasoning:** 1 key(s) state comparing against linear baseline and requiring ranking; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-7afe58436134c4db

### [RESULT] compare all configured backends against linear_residual. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-0bbcaac2cc804586` [closure_near] synthetic_extrapolation / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict insufficient — flag: unverified-synthetic: "extra_trees_residual` Strong nonlinear fit with variance reduction from randomized splits Can still overfit noisy short series; less interpretable"
- `c-1a1a3d9f0c351840` [closure_near] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Results differ between the linear (default) and RF backends. The linear backend is faster and more stable; the RF backend may capture more nonlinear residual structure but introduces additional noise for short series."
- `c-8a5ac1ca9abace23` [closure_near] synthetic_extrapolation / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict insufficient — flag: unverified-synthetic: "rf_residual` Captures nonlinear interactions with moderate tuning burden Higher variance and compute than linear"
- `c-a58de96982596cf4` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Use the robustness study pipeline to compare all configured backends against `linear_residual`."
- `c-67ea4dbaf12937fc` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "extra_trees_residual` Strong nonlinear fit with variance reduction from randomized splits Can still overfit noisy short series; less interpretable Stress-testing nonlinear mediation robustness"
- `c-dda0cdb18821e98d` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Keep `linear_residual` as baseline for all backend studies."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'compare all configured backends against linear_residual.'. Re-runnable: prompt sha 261f42425be1.

- test: `RESULT:c-a58de96982596cf4`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: Describes outcomes and implications but not explicitly as a test result.
- partial hits: c-1a1a3d9f0c351840
- synthetic hits (unverified): c-0bbcaac2cc804586, c-8a5ac1ca9abace23

**Missing element:** a result-to-interpretation mapping for 'compare all configured backends against linear_residual.'

**Reasoning:** 1 key(s) state compare all configured backends against linear_residual.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-a58de96982596cf4

## §7 checks

### §7.1 Anti-renaming: is the map density in disguise?

Computed over lens candidates only (HYP, RG-SINGLE, RG-UNVER, RG-SIBLING, RG-UNDECIDED and closed candidates) -- RG-UNK and CONTROL are excluded, since their density cannot vary.

- `J10(map, D_low)` = 0.00
- `J10(map, D_high)` = 0.00
- Spearman ρ(score, dens) = 0.00
- flags: closure-uninformative

**Matched-density table** (all lens candidates, by `dens` tercile):

| tercile | n | closed | HYP |
|---|---|---|---|
| low | 20 | 8 | 0 |
| mid | 21 | 13 | 0 |
| high | 21 | 8 | 0 |

Top-tercile closed share: 0.38

**Closure rate by `k_topic` band** (all lens candidates):

| band | n | closed | rate |
|---|---|---|---|
| 0-1 | 62 | 29 | 0.47 |
| 2 | 0 | 0 | 0.00 |
| 3-4 | 0 | 0 | 0.00 |
| >=5 | 0 | 0 | 0.00 |

### S2 fair mismatched-evidence control: does the judge close because of the EVIDENCE, or because of the SEED?

Replaces the first (straw-man) control, second adversarial review, 2026-09-29: the old own-evidence arm always carried the seed's own sentences while the mismatched arm never did (17/22 of PLC's old closures cited only the seed or its source), and the mismatched sentences were off-topic (cyclic gap_id pairing). Now BOTH arms keep the seed's own sentences; the OWN arm adds this candidate's own retrieved non-seed-source sentences; the CONTROL arm replaces those with the non-seed-source sentences retrieved for the topically nearest OTHER candidate of the same lens (max seed-stem Jaccard, ties by gap_id). "other-source-only" is the OWN arm with the seed and same-source sentences excluded entirely -- how often an independent source alone closes it. `closure-uninformative` unless own_rate - control_rate >= 0.20 (of candidates); lenses with < 2 candidates are skipped.

| lens | n | own rate | control rate | other-source-only rate | flag |
|---|---|---|---|---|---|
| HEDGE | 2 | 0.50 | 0.00 | 0.00 |  |
| RESULT | 11 | 1.00 | 0.91 | 0.73 | closure-uninformative |
| SEL | 6 | 1.00 | 1.00 | 1.00 | closure-uninformative |
| WHY | 41 | 0.41 | 0.22 | 0.17 | closure-uninformative |
| **total** | 60 | 0.58 | 0.42 | 0.35 | closure-uninformative |

### S2 lexical donor null: why the lexical closure test was replaced

The reviewer's fair donor null for the (now-comparison-only) LEXICAL closure test: self and same-source claims are excluded from both arms, and the donor is the real non-common content stems of a random other-source A claim of the same knowledge type as the seed (`random.Random(0)`, 200 draws). A check "passes" (is informative) only if the observed count is STRICTLY ABOVE the null's 5-95% interval. DISC is excluded (anchor-regex-driven, not stem-overlap); DIAG is handled per its own closure unit (one rival's sign test, not the group).

| lens | observed closed | null mean | null 5-95% | n | flag |
|---|---|---|---|---|---|
| GUARD | 0 | 0.3 | [0, 1] | 1 | closure-uninformative |
| HEDGE | 0 | 0.0 | [0, 0] | 2 | closure-uninformative |
| RESULT | 5 | 5.3 | [3, 8] | 11 | closure-uninformative |
| SEL | 1 | 2.3 | [1, 4] | 6 | closure-uninformative |
| WHY | 5 | 4.4 | [1, 8] | 41 | closure-uninformative |
| **total** | 11 | 12.3 | [8, 17] |  | closure-uninformative |

### Judge-vs-lexical agreement

Confusion counts, `<lexical_state>-><judge_state>`, over every judged candidate (the lexical test no longer decides anything; this is diagnostic only).

| lexical -> judge | n |
|---|---|
| closed->closed | 21 |
| closed->open | 10 |
| closed->partial | 2 |
| open->closed | 5 |
| open->open | 14 |
| open->partial | 2 |
| open->undecided | 2 |
| partial->closed | 1 |
| synthetic-closed->closed | 2 |
| synthetic-closed->open | 2 |
| synthetic-closed->synthetic-closed | 1 |

