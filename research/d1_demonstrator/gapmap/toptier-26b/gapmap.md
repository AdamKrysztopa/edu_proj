# Gap map: forecastability

- Ledger: `1641e931dbd914657ee76dc70a232f1c15b60e5bbc2fda5215ffb744c8c97bf2`
- Config: `35fd0af25618f8d6e0d1c2c3707d7e932afe2ce72dbd01e956034b43bfeb04c1`
- **Admissibility note:** sidecar n3_input is false: E-PLANT corpus contains planted fabrications; 32 pending verification(s) in the ledger

## Summary

- **HYP:** 3 total
  - HEDGE: 1 (1 narrow)
  - RESULT: 1 (1 narrow)
  - WHY: 1 (1 narrow)
- **Retrieval gaps:** RG-UNK 42, RG-SINGLE 25, RG-UNVER 4
- **Control slot:** 1
- **PROMO-excluded seeds (S3 defect 1):** 3
- **§7.1 anti-renaming:** J10(low)=0.00, J10(high)=0.30, ρ(score,dens)=0.33, flags: closure-uninformative

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
| 1 | WHY | known_future_drivers should be used only for variables whose | narrow | 0/4 | 3 |
| 2 | HEDGE | In statistics and time series analysis, the autocovariance | narrow | 2/4 | 2 |
| 3 | RESULT | evaluation should be targeted exclusively at horizons in the | narrow | 0/4 | 2 |

### #1 [WHY] known_future_drivers should be used only for variables whose contemporaneous future values are genuinely known at prediction time, such as calendar flags or planned promotions.

*lens: WHY; category: HYP*

**OBSERVED EVIDENCE**

- `c-67213a7cebde7a96` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Use `known_future_drivers` only for variables whose contemporaneous future > values are genuinely known at prediction time, such as calendar flags, > planned promotions, or externally scheduled variables."
- `c-02e70d053eaa8f6b` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`run_lag_aware_mod_mrmr()` blocks illegal measured lags, preserves declared known-future covariates with provenance, and returns selected, rejected, and blocked rows with scorer diagnostics."
- `c-5ca9e05b6f8856f8` [topic] literature_supported / documentation, key `ind-s-ca7d54da5b087ed3`, verdict supports: "Provides train/test indices to split time-ordered data, where other cross-validation methods are inappropriate, as they would lead to training on future data and evaluating on past data."
- `c-a99d5fd0e42f848c` [topic] literature_supported / documentation, key `ind-s-0b00932c0a642b74`, verdict supports: "In this approach, the predictions of all future values are equal to the mean of the past data."
- `c-06f340cedf08777b` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "With the opt-in, those rows flip to `tensor_role="known_future"` and the selector may choose `selected_for_tensor=True` at $k=0$ for that driver only."
- `c-100c68ae20f2e64f` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Known-future opt-in for features whose contemporaneous value is available at prediction time (e.g. calendar flags, planned promotions, regulator-set prices)"
+ 4 more topic claims across 3 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 0dd30a456509.

- test: `WHY:c-67213a7cebde7a96`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: 2,3,5,7

**HIDDEN-KNOWLEDGE HYPOTHESIS** (label: `inferred` — a prediction, never a fact)

Predicted, not observed: Hypothesis (inferred): practitioners are predicted to know why 'known_future_drivers should be used only for variables whose contemporaneous future values are genuinely known at prediction time, such as calendar flags or planned promotions.'; no verified claim in this ledger matched test WHY:c-67213a7cebde7a96.

- predicted knowledge type: rationale
- predicted tacitness: relational
- channel: a targeted confirmation question

**Missing element:** a reason

**Reasoning:** 1 key(s) state known_future_drivers should be used only for variables whose contemporaneous future values are genuinely known at prediction time, such as calendar flags or planned promotions.; 3 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-67213a7cebde7a96

**Breadth:** narrow (uncalibrated; no gold) (score 2 = A2 + B0 − P0; k_step=1, k_topic=3); lexical robustness 0/4

**Alternatives:**

- [live] The rationale is a purpose clause that RAT does not match. — RAT does not match every 'to identify...' purpose clause.
- [not live] The source is promotional. — no PROMO lexicon hit on the span; no ledger field marks promotional voice (§10).
- [live] The reason is trivial safety knowledge. — an omitted rationale may simply be too obvious to state.

**Expert question** (channel: a targeted confirmation question):

> Sources say: "Use `known_future_drivers` only for variables whose contemporaneous future > values are genuinely known at prediction time, such as calendar flags, > planned promotions, or externally scheduled variables.". What would happen if someone did it differently, and in what situations, if any, is doing it differently acceptable?

### #2 [HEDGE] In statistics and time series analysis, the autocovariance is commonly normalized to a Pearson correlation coefficient, while in engineering the normalization is usually dropped.

*lens: HEDGE; category: HYP*

**OBSERVED EVIDENCE**

- `c-23b71befef797d20` [seed] literature_supported / documentation, key `ind-s-0b00932c0a642b74`, verdict supports: "It is common practice in some disciplines (e.g. statistics and time series analysis) to normalize the autocovariance function to get a time-dependent Pearson correlation coefficient. However, in other disciplines (e.g. engineering) the normalization is usually dropped"
- `c-04bb985feaddbfac` [topic] literature_supported / documentation, key `ind-s-0b00932c0a642b74`, verdict supports: "its value must lie in the range [ − 1 , 1 ] {\displaystyle [-1,1]} , with 1 indicating perfect correlation and −1 indicating perfect anti-correlation"
- `c-65065dfee36610b1` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Which external drivers show lead-lag signal with the target? Driver screening before multivariate forecasting or feature engineering CrossAMI and pCrossAMI curves + ranked drivers"
- `c-649be9381044ab08` [topic] literature_supported / documentation, key `ind-s-0b00932c0a642b74`, verdict supports: "the autocorrelation of a real or complex random process is the Pearson correlation between values of the process at different times, as a function of the two times or of the time lag"
- `c-76fa50e7b7110399` [topic] literature_supported / documentation, key `ind-s-0b00932c0a642b74`, verdict supports: "the autocovariance depends only on the time-distance between the pair of values but not on their position in time"
- `c-931f2ebfc2cfdad2` [topic] literature_supported / documentation, key `ind-s-0b00932c0a642b74`, verdict supports: "Transfer entropy is a non-parametric statistic measuring the amount of directed (time-asymmetric) transfer of information between two random processes."
+ 2 more topic claims across 2 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of an exception condition. Re-runnable: prompt sha 26cb8cf76068.

- test: `HEDGE:c-23b71befef797d20`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: Partial exceptions are mentioned but not explicitly stated.
- partial hits: c-23b71befef797d20

**HIDDEN-KNOWLEDGE HYPOTHESIS** (label: `inferred` — a prediction, never a fact)

Predicted, not observed: Hypothesis (inferred): practitioners are predicted to know the cases in which 'In statistics and time series analysis, the autocovariance is commonly normalized to a Pearson correlation coefficient, while in engineering the normalization is usually dropped.' does not hold; no verified claim in this ledger matched test HEDGE:c-23b71befef797d20.

- predicted knowledge type: decision
- predicted tacitness: collective
- channel: CDM hypotheticals and boundary-case vignettes

**Missing element:** an exception condition

**Reasoning:** 1 key(s) state In statistics and time series analysis, the autocovariance is commonly normalized to a Pearson correlation coefficient, while in engineering the normalization is usually dropped.; 2 key(s) discuss the topic; the closure judge found no verified sentence matching test HEDGE:c-23b71befef797d20

**Breadth:** narrow (uncalibrated; no gold) (score 0 = A1 + B0 − P1; k_step=1, k_topic=2); lexical robustness 2/4

**Alternatives:**

- [live] The exception is circular: it restates the judgement. — a hedge whose exception re-states the criterion gives no new information.
- [live] The hedge is statutory boilerplate with no practice behind it. — a hedge in a legal or standard source may carry no field practice.
- [live] A trigger is stated inside the seed itself in a form EXC does not match. — EXC is a fixed lexicon and misses e.g. 'at least when'.

**Expert question** (channel: CDM hypotheticals and boundary-case vignettes):

> "statistics and time series analysis) to normalize the autocovariance function to get a time-dependent Pearson correlation coefficient.". Describe a case where this did not hold, or where you decided against it. What about that case told you it was an exception?

### #3 [RESULT] evaluation should be targeted exclusively at horizons in the

*lens: RESULT; category: HYP*

**OBSERVED EVIDENCE**

- `c-d3af3ac9c12c2b7c` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "A practitioner should target model evaluation exclusively at horizons in $\mathcal{H}_\varepsilon$ - lags outside this set carry no detectable predictive signal above the noise floor."
- `c-255ac9e6dd986fa5` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`avoid_horizons` `list[int]` Non-informative horizons - exclude from model feature sets"
- `c-6dfd7bd91fe8cf5a` [topic] literature_supported / documentation, key `ind-s-0b00932c0a642b74`, verdict supports: "The analysis of autocorrelation is a mathematical tool for identifying repeating patterns or hidden periodicities within a signal obscured by noise."
- `c-3187dc80e3fabb57` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "$F(h;\,\mathcal{I}_t) \ge 0$ with equality only when $Y_{t+h}$ is independent of $\mathcal{I}_t$."
- `c-4c573caecf8348b9` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Start with forecastability triage first: readiness, leakage risk, informative horizons, primary lags, seasonality structure, and covariate informativeness."
- `c-53d2494921e472c0` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Positive TE indicates added predictive information from source history beyond target-only history."
+ 13 more topic claims across 2 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'evaluation should be targeted exclusively at horizons in the'. Re-runnable: prompt sha 304c0a2511be.

- test: `RESULT:c-d3af3ac9c12c2b7c`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: State expectations or next actions not explicitly stated; sentences 3 and 4 describe conditions leading to an empty informative horizon set.
- partial hits: c-cbda935885e1f4ac

**HIDDEN-KNOWLEDGE HYPOTHESIS** (label: `inferred` — a prediction, never a fact)

Predicted, not observed: Hypothesis (inferred): practitioners are predicted to read the result of 'evaluation should be targeted exclusively at horizons in the' against expected values and map it to the next action; no verified claim in this ledger matched test RESULT:c-d3af3ac9c12c2b7c.

- predicted knowledge type: interpretation, expectancy
- predicted tacitness: relational
- channel: CDM probes on a recalled case; process tracing

**Missing element:** a result-to-interpretation mapping for 'evaluation should be targeted exclusively at horizons in the'

**Reasoning:** 1 key(s) state evaluation should be targeted exclusively at horizons in the; 2 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-d3af3ac9c12c2b7c

**Breadth:** narrow (uncalibrated; no gold) (score 0 = A1 + B0 − P1; k_step=1, k_topic=2); lexical robustness 0/4

**Alternatives:**

- [live] The interpretation is stated in paraphrase without the seed's stems. — the stem-overlap test cannot see a paraphrase (the same limitation as DISC, §9).
- [live] The test is a formality with a binary outcome. — not every prescribed test feeds a real branching decision.
- [live] The interpretation is instrument-given. — a displayed pass/fail reading needs no practitioner interpretation.

**Expert question** (channel: CDM probes on a recalled case; process tracing):

> Sources prescribe: "A practitioner should target model evaluation exclusively at horizons in $\mathcal{H}_\varepsilon$ - lags outside this set carry no detectable predictive signal above the noise floor.". Think of the last time you did this. What result did you get, what had you expected, what did that result make you do next -- and what result would have sent you down a different path?

## Control slot

The §14.2 unknown-unknowns guard: an area no hypothesis touched, walked cold.

### Toolkit installation and repository setup

*lens: —; category: CONTROL*

**OBSERVED EVIDENCE**

(none)

**INFERRED GAP**

Control slot: area 'Toolkit installation and repository setup' (a-7b6acca02019d0e2) has no HYP record and the highest attested share (0.73) among candidate areas of ledger 1641e931.

- test: `CONTROL:a-7b6acca02019d0e2`; state: open (closure judge: )

**Reasoning:** the §14.2 unknown-unknowns guard: no HYP touches this area

**Breadth:** narrow (uncalibrated; no gold) (score 0 = A0 + B0 − P0; k_step=0, k_topic=0); lexical robustness 0/4

**Expert question** (channel: control):

> Walk me through how you carry out Toolkit installation and repository setup, from start to finish, as if I were watching you do it. What do you check, and in what order?

## Retrieval gaps

Not hypotheses: each one's action is to search further or verify a synthetic span, never to ask an expert.

### RG-UNK: slots searched, nothing found

| area | slot / question | source |
|---|---|---|
| Running an analysis pipeline and configuration | procedure_step slot searched, only thin coverage found | sidecar slot |
| Interpreting forecastability scores against model performance | failure_mode slot searched, only thin coverage found | sidecar slot |
| Running an analysis pipeline and configuration | norm slot searched, only thin coverage found | sidecar slot |
| Extending the toolkit with new estimators and tests | concept slot searched, only thin coverage found | sidecar slot |
| Interpreting forecastability scores against model performance | check slot searched, only thin coverage found | sidecar slot |
| Toolkit installation and repository setup | procedure_step slot searched, only thin coverage found | sidecar slot |
| Extending the toolkit with new estimators and tests | norm slot searched, only thin coverage found | sidecar slot |
| Significance testing and surrogate baselines | procedure_step slot searched, only thin coverage found | sidecar slot |
| Horizon-wise dependence measures (auto-mutual information, ACF) | decision slot searched, only thin coverage found | sidecar slot |
| Interpreting forecastability scores against model performance | rationale slot searched, only thin coverage found | sidecar slot |
| Running an analysis pipeline and configuration | rationale slot searched, only thin coverage found | sidecar slot |
| Extending the toolkit with new estimators and tests | decision slot searched, only thin coverage found | sidecar slot |
| Interpreting forecastability scores against model performance | decision slot searched, only thin coverage found | sidecar slot |
| Interpreting forecastability scores against model performance | procedure_step slot searched, only thin coverage found | sidecar slot |
| Interpreting forecastability scores against model performance | cue slot searched, only thin coverage found | sidecar slot |
| Extending the toolkit with new estimators and tests | check slot searched, only thin coverage found | sidecar slot |
| Significance testing and surrogate baselines | rationale slot searched, only thin coverage found | sidecar slot |
| Extending the toolkit with new estimators and tests | rationale slot searched, only thin coverage found | sidecar slot |
| Horizon-wise dependence measures (auto-mutual information, ACF) | check slot searched, nothing found | sidecar slot |
| Toolkit installation and repository setup | rationale slot searched, only thin coverage found | sidecar slot |
| Toolkit installation and repository setup | norm slot searched, only thin coverage found | sidecar slot |
| Toolkit installation and repository setup | failure_mode slot searched, only thin coverage found | sidecar slot |
| Extending the toolkit with new estimators and tests | failure_mode slot searched, only thin coverage found | sidecar slot |
| Toolkit installation and repository setup | What observable features of a situation signal that Toolkit installation and repository setup | ledger U claim `c-21de18d8f2c08309` |
| Running an analysis pipeline and configuration | cue slot searched, nothing found | sidecar slot |
| Running an analysis pipeline and configuration | check slot searched, nothing found | sidecar slot |
| Running an analysis pipeline and configuration | How is work in Running an analysis pipeline and configuration checked for correctness or compliance? | ledger U claim `c-53315f6b0c788afa` |
| Significance testing and surrogate baselines | What observable features of a situation signal that Significance testing and surrogate baselines | ledger U claim `c-5b92e7fc8e110a01` |
| Toolkit installation and repository setup | What conditions determine which option is chosen in Toolkit installation and repository setup? | ledger U claim `c-270124731a55e758` |
| Toolkit installation and repository setup | decision slot searched, nothing found | sidecar slot |
| Toolkit installation and repository setup | cue slot searched, nothing found | sidecar slot |
| Horizon-wise dependence measures (auto-mutual information, ACF) | What observable features of a situation signal that Horizon-wise dependence measures (auto-mutual | ledger U claim `c-10263f7f4daab0fe` |
| Running an analysis pipeline and configuration | What observable features of a situation signal that Running an analysis pipeline and configuration | ledger U claim `c-a7ae14af043c2cca` |
| Extending the toolkit with new estimators and tests | What steps make up Extending the toolkit with new estimators and tests, and in what order? | ledger U claim `c-80b70925cf82098a` |
| Extending the toolkit with new estimators and tests | procedure_step slot searched, nothing found | sidecar slot |
| Horizon-wise dependence measures (auto-mutual information, ACF) | How is work in Horizon-wise dependence measures (auto-mutual information, ACF) checked for | ledger U claim `c-69455b95b51ab3dd` |
| Significance testing and surrogate baselines | cue slot searched, nothing found | sidecar slot |
| Toolkit installation and repository setup | How is work in Toolkit installation and repository setup checked for correctness or compliance? | ledger U claim `c-31bccc8448023450` |
| Horizon-wise dependence measures (auto-mutual information, ACF) | cue slot searched, nothing found | sidecar slot |
| Extending the toolkit with new estimators and tests | cue slot searched, nothing found | sidecar slot |
| Extending the toolkit with new estimators and tests | What observable features of a situation signal that Extending the toolkit with new estimators and | ledger U claim `c-04b5549e0db967c9` |
| Toolkit installation and repository setup | check slot searched, nothing found | sidecar slot |

### [WHY] Cross-backend agreement should be required before acting on lag recommendations. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-178838d1f9220e1f` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "require cross-backend agreement before acting on lag recommendations"
- `c-90dc62500a2b29c7` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "pAMI feasibility (linear residual backend): \[ N \ge \max\left(H + \texttt{min\_pairs\_pami} + 1,\ 2H\right) \]"

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha d73198a56553.

- test: `WHY:c-178838d1f9220e1f`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: prevents failure of cross-backend agreement

**Missing element:** a reason

**Reasoning:** 1 key(s) state Cross-backend agreement should be required before acting on lag recommendations.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-178838d1f9220e1f

### [WHY] Adapters should not become a second business-logic layer. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-d842abf5a063991d` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The architecture goal is still inward dependency flow. Adapters should not become a second business-logic layer."
- `c-c1f3d813056e784f` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Ports and bootstrap remain support seams rather than primary business-logic owners."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 09bc44b118e4.

- test: `WHY:c-d842abf5a063991d`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: inward dependency flow

**Missing element:** a reason

**Reasoning:** 1 key(s) state Adapters should not become a second business-logic layer.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-d842abf5a063991d

### [WHY] Contributors should add new user-facing imports through forecastability or forecastability.triage only when they want to commit to compatibility. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-c6bbdec6744fb515` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Add new user-facing imports through `forecastability` or `forecastability.triage` only when you want to commit to compatibility."
- `c-1c4e8047d3bd12be` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Use [../public_api.md](../public_api.md) when deciding whether a symbol is part of the supported import contract."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 11db74e707a8.

- test: `WHY:c-c6bbdec6744fb515`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: ensures compatibility

**Missing element:** a reason

**Reasoning:** 1 key(s) state Contributors should add new user-facing imports through forecastability or forecastability.triage only when they want to commit to compatibility.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-c6bbdec6744fb515

### [HEDGE] It is generally considered good practice to indicate the degree of uncertainty attached to forecasts. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-9c0f849034e929bd` [seed] literature_supported / documentation, key `ind-s-0b00932c0a642b74`, verdict supports: "it is generally considered a good practice to indicate the degree of uncertainty attaching to forecasts"

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating an exception condition. Re-runnable: prompt sha 271a237f7c18.

- test: `HEDGE:c-9c0f849034e929bd`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: No sentences explicitly state exceptions to the rule.

**Missing element:** an exception condition

**Reasoning:** 1 key(s) state It is generally considered good practice to indicate the degree of uncertainty attached to forecasts.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test HEDGE:c-9c0f849034e929bd

### [WHY] Optional surfaces should be added only after the core path is clear. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-06048134e309e409` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Add Optional Surfaces Only After The Core Path Is Clear"

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 6701c551dc82.

- test: `WHY:c-06048134e309e409`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: prevents premature optional feature implementation

**Missing element:** a reason

**Reasoning:** 1 key(s) state Optional surfaces should be added only after the core path is clear.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-06048134e309e409

### [WHY] Contributors should treat services as internal helpers, not as a third public API layer. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-19ce99b47740dfa8` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Treat `services/` as internal helpers, not as a third public API layer."
- `c-083bb58cf308d008` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Follow this path before you reach for the CLI, API, dashboard, MCP, or agent layers."
- `c-1c4e8047d3bd12be` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Use [../public_api.md](../public_api.md) when deciding whether a symbol is part of the supported import contract."
- `c-221f866e4872439f` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`services/`, `utils/`, `pipeline/`, `metrics/`, `diagnostics/`, `reporting/` Internal structure that may continue to move during consolidation"
- `c-56ed90f241f7c02f` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Start here in this order: 1. README.md 2. docs/quickstart.md 3. docs/public_api.md"
- `c-5dc2a864468395b8` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`build_forecast_prep_contract()` returns a `ForecastPrepContract` directly in the current public API."
+ 9 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 8ff2f721ef7d.

- test: `WHY:c-19ce99b47740dfa8`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: prevents exposing internal implementation details

**Missing element:** a reason

**Reasoning:** 1 key(s) state Contributors should treat services as internal helpers, not as a third public API layer.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-19ce99b47740dfa8

### [WHY] In constrained environments, only the needed extras should be installed, e.g. pip install forecastability for core only. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-e6878d07cc4c4645` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "In constrained environments, install only the extras you need: - `pip install forecastability` for core only"
- `c-03329bb964696b2f` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Install the package from the published package, or use the GitHub fallback if package resolution is not available: pip install dependence-forecastability pip install git+https://github.com/AdamKrysztopa/dependence-forecastability.git"
- `c-369186b6ad4d560a` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`pip install forecastability[agent]` for agent layer"
- `c-3d2084add72fe975` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The PCMCI methods require the optional causal extra: pip install "dependence-forecastability[causal]""
- `c-64f86f8f80e56da1` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The MCP server requires additional server-framework dependencies. It is not included in the default install."
- `c-7bbe881de26b6f26` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`pip install forecastability[api]` for HTTP API"
+ 2 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 5c0c121c5ba0.

- test: `WHY:c-e6878d07cc4c4645`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: to prevent unnecessary resource consumption

**Missing element:** a reason

**Reasoning:** 1 key(s) state In constrained environments, only the needed extras should be installed, e.g. pip install forecastability for core only.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-e6878d07cc4c4645

### [WHY] Downstream model families or framework-specific settings should only be recommended after triage. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-67372dcb86414a6a` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Only then recommend downstream model families or framework-specific settings."
- `c-05348ecbfe93d58e` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The surface suggests starting model families only; it does not fit models or wire downstream frameworks."
- `c-60972c8750eef533` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "After triage, fingerprint, and lagged-exog analysis, call `build_forecast_prep_contract()` to convert triage outputs into a `ForecastPrepContract` - a structured, machine-readable hand-off contract for downstream model families."
- `c-7073a2f73ced2593` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The contract is the final deterministic surface before external frameworks take over. It never imports any downstream library."
- `c-7eb48509de87201c` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "That split is intentional: the core package produces deterministic evidence; the examples repository shows how to translate that evidence into framework-specific modeling recipes."
- `c-f03ade7bfe27b377` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Downstream frameworks are consumers of triage results, not competitors."
+ 1 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 877722507075.

- test: `WHY:c-67372dcb86414a6a`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: to prevent premature model recommendation

**Missing element:** a reason

**Reasoning:** 1 key(s) state Downstream model families or framework-specific settings should only be recommended after triage.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-67372dcb86414a6a

### [WHY] Contributors should keep deterministic orchestration in use_cases and pipeline rather than in notebooks or scripts. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-12fcd440ab5152d2` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Keep deterministic orchestration in `use_cases/` and `pipeline/` rather than notebooks or scripts."
- `c-115717fdc0f1a7f4` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "It is **not another forecasting library**. It is a deterministic pre-modeling layer"
- `c-4cf8da484fd3be39` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Put transport concerns in `adapters/`, not in use cases or metrics code."
- `c-5b8e0c5d3cc82ea7` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`use_cases/run_triage.py` and `use_cases/run_batch_triage.py` are the authoritative orchestration entry points called by the public facade and adapters."
- `c-632cedcf139eff2c` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "CLI, API, scripts, MCP, and agents are optional access or narration layers around the same deterministic outputs."
- `c-a0b523bc132a1ec1` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Use [../maintenance/developer_guide.md](../maintenance/developer_guide.md) for the repo workflow around scripts, notebooks, configs, outputs, and docs."
+ 1 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 8858685a3e3e.

- test: `WHY:c-12fcd440ab5152d2`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: prevents non-deterministic execution

**Missing element:** a reason

**Reasoning:** 1 key(s) state Contributors should keep deterministic orchestration in use_cases and pipeline rather than in notebooks or scripts.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-12fcd440ab5152d2

### [WHY] Contributors should put transport concerns in adapters, not in use cases or metrics code. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-4cf8da484fd3be39` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Put transport concerns in `adapters/`, not in use cases or metrics code."
- `c-12fcd440ab5152d2` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Keep deterministic orchestration in `use_cases/` and `pipeline/` rather than notebooks or scripts."
- `c-5b8e0c5d3cc82ea7` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`use_cases/run_triage.py` and `use_cases/run_batch_triage.py` are the authoritative orchestration entry points called by the public facade and adapters."
- `c-6e84cfb721c9cd17` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`adapters/` runtime entry points Supported runtime surfaces, but transport details may evolve"
- `c-e280d4675236ff89` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Entrypoints and adapters call the package facades or use cases."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 1bac448580f2.

- test: `WHY:c-4cf8da484fd3be39`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: prevents adapter-to-adapter helper coupling

**Missing element:** a reason

**Reasoning:** 1 key(s) state Contributors should put transport concerns in adapters, not in use cases or metrics code.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-4cf8da484fd3be39

### [WHY] Escalation to nonlinear backends should happen only when they improve diagnostic consistency across datasets. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-d5a7fb62b56918db` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Escalate only when nonlinear backends improve diagnostic consistency across datasets."
- `c-39d9ef8bb34d0bc3` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`extra_trees_residual` Strong nonlinear fit with variance reduction from randomized splits Can still overfit noisy short series; less interpretable"
- `c-bd2afa2d663dd4ca` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`rf_residual` Captures nonlinear interactions with moderate tuning burden Higher variance and compute than linear"
- `c-f1295b47e1678eab` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`linear_residual` Fast, stable, interpretable baseline Misses nonlinear mediation"

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 3a65016d2e66.

- test: `WHY:c-d5a7fb62b56918db`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: to prevent overfitting and ensure ranking stability

**Missing element:** a reason

**Reasoning:** 1 key(s) state Escalation to nonlinear backends should happen only when they improve diagnostic consistency across datasets.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-d5a7fb62b56918db

### [WHY] AMI and pAMI should be kept horizon-specific and not pre-aggregated before triage. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-8eabb66a53df1fee` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Keep AMI and pAMI horizon-specific; do not pre-aggregate before triage."
- `c-361a6f8801f293a8` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Horizon-specific curve, never collapsed before analysis."
- `c-8390f6c1d21a8a56` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "frequency-specific cap (Yearly 6, Quarterly 8, Monthly 18, Weekly 13, Daily 14, Hourly 48): AMI values beyond these caps are unreliable."
- `c-a63ddd04d6950db1` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "AMI is paper-aligned (horizon-specific, kNN-based, with phase-surrogate significance bands)."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha ae543f78ec05.

- test: `WHY:c-8eabb66a53df1fee`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: 2,3,4,5,6,7,8,9,10,11,12

**Missing element:** a reason

**Reasoning:** 1 key(s) state AMI and pAMI should be kept horizon-specific and not pre-aggregated before triage.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-8eabb66a53df1fee

### [WHY] Surrogates should be used whenever sample size permits, i.e. n of at least 200 and n_surrogates of at least 99. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-8b34c98f4e94b843` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Use surrogates whenever sample size permits ($n \ge 200$, `n_surrogates >= 99`)."
- `c-15ffab22f9bd5b4b` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Surrogate significance is optional, requires feasible sample size, and needs at least 99 surrogates."
- `c-82315de73a1d9b6a` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Experimental - unreliable at finite sample sizes; gated behind config flag; never auto-included in triage score"

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 1589541dc120.

- test: `WHY:c-8b34c98f4e94b843`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: 4: Surrogate significance testing requires a feasible sample size.

**Missing element:** a reason

**Reasoning:** 1 key(s) state Surrogates should be used whenever sample size permits, i.e. n of at least 200 and n_surrogates of at least 99.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-8b34c98f4e94b843

### [WHY] F5 must be explicitly enabled via experimental: true in the config and does not run in default triage mode. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-aad107708da7c302` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "F5 must be explicitly enabled via `experimental: true` in the config. It does not run in default triage mode."
- `c-398f05f0bcd6a88a` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "By default, every $k = 0$ row gets `tensor_role = "diagnostic"`. The `"known_future"` value is only assigned when the user explicitly opts in via `known_future_drivers={"driver_name": True}`."
- `c-82315de73a1d9b6a` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Experimental - unreliable at finite sample sizes; gated behind config flag; never auto-included in triage score"

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 99168225702f.

- test: `WHY:c-aad107708da7c302`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: 2,3,9,10,11,12

**Missing element:** a reason

**Reasoning:** 1 key(s) state F5 must be explicitly enabled via experimental: true in the config and does not run in default triage mode.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-aad107708da7c302

### [WHY] For time-series forecasting tasks, forecastability triage should precede model fitting rather than jumping directly to fitting models. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-3b16f3a7b858b851` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "When the task is time-series forecasting, do not jump directly to model fitting. Start with forecastability triage first"
- `c-1d4a70e39783471e` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "When the task is time-series forecasting, do not jump directly to model fitting. Start with forecastability triage first"

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha b192cec0f6eb.

- test: `WHY:c-3b16f3a7b858b851`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: 2,3,4,5 prevent jumping to model fitting without assessing forecastability first, avoiding model fitting on non-forecastable data.

**Missing element:** a reason

**Reasoning:** 1 key(s) state For time-series forecasting tasks, forecastability triage should precede model fitting rather than jumping directly to fitting models.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-3b16f3a7b858b851

### [WHY] The forecastability profile (F1) should be run after AMI curves exist and before choosing which horizons to model. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-12dca6b80e1a3b61` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "After AMI curves exist; before choosing which horizons to model"

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 5885baa5fbf0.

- test: `WHY:c-12dca6b80e1a3b61`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: 2,3 prevent premature horizon selection

**Missing element:** a reason

**Reasoning:** 1 key(s) state The forecastability profile (F1) should be run after AMI curves exist and before choosing which horizons to model.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-12dca6b80e1a3b61

### [WHY] An elastic-alignment result would require a new surface, a new method label, and an explicit chronological-causality guard before entering a forecasting tensor. — RG-UNVER

*Action: verify — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-69f267782709aaf0` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Any elastic-alignment result would need a new surface, a new method label, and an explicit chronological-causality guard before it could be admitted to a forecasting tensor."
- `c-f019defaaf1554b2` [closure_near] synthetic_extrapolation / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict insufficient — flag: unverified-synthetic: "This is not a library limitation - it is an intentional chronological-causality > guard."
- `c-1fa0a2c548476180` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The lagged-exogenous surface classifies drivers by lag role and emits a sparse lag map that can be used for downstream tensor construction."
- `c-cc061ed30e23b40e` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "DTW (Dynamic Time Warping), FastDTW, and ShapeDTW solve **elastic-alignment similarity**: they search for the alignment $\pi$ that minimises a path-cumulated distance between two time series."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason among the verified sentences retrieved (4 unverified sentences considered separately). Re-runnable: prompt sha 0cdb8c736d0a.

- test: `WHY:c-69f267782709aaf0`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): synthetic-closed
- judge reason: it prevents models from being misaligned temporally
- synthetic hits (unverified): c-f019defaaf1554b2

**Missing element:** a reason

**Reasoning:** 1 key(s) state An elastic-alignment result would require a new surface, a new method label, and an explicit chronological-causality guard before entering a forecasting tensor.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-69f267782709aaf0

### [WHY] At least 99 surrogates are required for a valid two-sided 95% band, and fewer must not be used as a significance threshold. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-ca2ed537d5bb3a4f` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "At least `n_surrogates = 99` is required for a valid two-sided 95% band. Fewer than 99 surrogates are not sufficient and must not be used as a significance threshold."
- `c-15ffab22f9bd5b4b` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Surrogate significance is optional, requires feasible sample size, and needs at least 99 surrogates."
- `c-3d81f927bb52cba0` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`diagnostics/surrogates.py` owns phase-randomized FFT surrogates and significance bands."
- `c-67f8bd218d91976a` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "When the series is too short, significance may be unavailable and the surrogate bands are omitted. This is distinct from "computed, none significant" - the two outcomes must not be conflated."
- `c-73873204b2c6a000` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Wherever phase-randomised surrogate bands already exist (via `significance_service`), the lagged-exogenous flow reuses them"
- `c-758fbc344a59ea58` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Significance is evaluated against phase-randomized surrogate bands and should be interpreted with the same surrogate caveats used elsewhere in this repository."
+ 6 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha fda64cf188c7.

- test: `WHY:c-ca2ed537d5bb3a4f`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: 2,3

**Missing element:** a reason

**Reasoning:** 1 key(s) state At least 99 surrogates are required for a valid two-sided 95% band, and fewer must not be used as a significance threshold.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-ca2ed537d5bb3a4f

### [WHY] In rolling-origin evaluation, diagnostics should be computed on train windows only. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-d7d073c08a1e9cc5` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "In rolling-origin evaluation, compute diagnostics on train windows only."
- `c-6cde14ffcab162d1` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The same leakage boundary applies to exogenous screening (F8): CrossAMI must be computed on the training window only."
- `c-6e752ea957b7798d` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Forecast errors are computed on post-origin test window only."
- `c-76995d363dd487e4` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "In rolling-origin evaluation, diagnostics are computed on train windows only and scoring on post-origin holdout only."
- `c-78820e0997930fee` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "AMI, pAMI, and all F1-F8 diagnostics are computed on the training window up to each rolling origin. No diagnostic touches the post-origin holdout."
- `c-8015191423797d4e` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`pipeline/` Analyzer facade, canonical workflow helpers, and rolling-origin support"
+ 6 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha dd801ae18cc0.

- test: `WHY:c-d7d073c08a1e9cc5`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: to avoid false out-of-sample validity claims

**Missing element:** a reason

**Reasoning:** 1 key(s) state In rolling-origin evaluation, diagnostics should be computed on train windows only.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-d7d073c08a1e9cc5

### [WHY] Significant-lag fields such as n_sig_raw_lags and n_sig_partial_lags should only be interpreted as evidence about absent significance when compute_surrogates is true. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-227132d21dd427f9` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Only interpret `n_sig_raw_lags`, `n_sig_partial_lags`, or other significant-lag fields as evidence about absent significance when `compute_surrogates` is `true`."
- `c-353778e07d782e1c` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`run_triage(..., include_extended_fingerprint=True)` additively attaches > `extended_forecastability_analysis` for non-exogenous requests. Exogenous > requests keep that field omitted"
- `c-6128ba04cdbca987` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`run_triage(..., include_extended_fingerprint=True)` additively attaches `extended_forecastability_analysis` for non-exogenous routes only. Exogenous requests leave the field omitted"
- `c-758fbc344a59ea58` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Significance is evaluated against phase-randomized surrogate bands and should be interpreted with the same surrogate caveats used elsewhere in this repository."
- `c-7f6b838b750e1bf6` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`is_non_monotone` `bool` `True` if $F(h)$ increases at any $h > 1$"
- `c-863816a2948bfbf4` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "When `compute_surrogates` is `false`, significance was skipped or suppressed. That is different from a run where surrogates were computed and no lags were significant."
+ 5 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 02f88e0b8829.

- test: `WHY:c-227132d21dd427f9`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: 2,3,4

**Missing element:** a reason

**Reasoning:** 1 key(s) state Significant-lag fields such as n_sig_raw_lags and n_sig_partial_lags should only be interpreted as evidence about absent significance when compute_surrogates is true.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-227132d21dd427f9

### [WHY] Any new selector that goes further, such as one conditioning on driver autohistory, must be introduced under a new method label so existing cross_pami and xami_sparse semantics are not silently extended. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-4c9d9f7275c52f3d` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Any new selector that goes further (PMIME-style, PC-stable with driver autohistory) must be introduced under a **new method label** so that the shipped `cross_pami` and `xami_sparse` semantics are not silently extended."
- `c-1fa0a2c548476180` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The lagged-exogenous surface classifies drivers by lag role and emits a sparse lag map that can be used for downstream tensor construction."
- `c-50eecfbfdfafa159` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The workflow screens graph-positive drivers and negative controls across lags, separates raw pairwise dependence from signal that remains after target history is accounted for, applies forecast-legality constraints, and then hands off a sparse feature surface."
- `c-6a906e77331ce824` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "classify each exogenous driver by lag role (contemporaneous vs predictive), apply sparse lag selection, and produce a typed lag map ready for forecasting tensor construction."
- `c-862ac212d1e61a2c` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "**At least one row per `(target, driver)` pair** is emitted by the selector."
- `c-ae8b20ebf80f3248` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The `known_future_drivers` contract is honored at the **use-case layer** (`run_lagged_exogenous_triage`). The selector service itself is pure and does not read it."
+ 5 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 06dfef7231e5.

- test: `WHY:c-4c9d9f7275c52f3d`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: 2

**Missing element:** a reason

**Reasoning:** 1 key(s) state Any new selector that goes further, such as one conditioning on driver autohistory, must be introduced under a new method label so existing cross_pami and xami_sparse semantics are not silently extended.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-4c9d9f7275c52f3d

### [RESULT] compare all configured backends against linear_residual. — RG-UNVER

*Action: verify — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-a58de96982596cf4` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Use the robustness study pipeline to compare all configured backends against `linear_residual`."
- `c-0938aacab4017209` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`diagnostics/cmi.py` owns alternative residual backends used by pAMI-style workflows."
- `c-2fe74387530afa2c` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Backend comparison is diagnostic, not proof that one backend is universally superior."
- `c-30f66f27c574f7ca` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Run `MPLBACKEND=Agg uv run python scripts/archive/run_robustness_study.py`."
- `c-39d9ef8bb34d0bc3` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`extra_trees_residual` Strong nonlinear fit with variance reduction from randomized splits Can still overfit noisy short series; less interpretable"
- `c-8cf81bf631773b3c` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Keep `linear_residual` as baseline for all backend studies."
+ 4 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a result-to-interpretation mapping for 'compare all configured backends against linear_residual.' among the verified sentences retrieved (4 unverified sentences considered separately). Re-runnable: prompt sha 887bdc45baf1.

- test: `RESULT:c-a58de96982596cf4`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: Sentence 10 explicitly states the expected result and next action.
- synthetic hits (unverified): c-2f52502f7d346fba

**Missing element:** a result-to-interpretation mapping for 'compare all configured backends against linear_residual.'

**Reasoning:** 1 key(s) state compare all configured backends against linear_residual.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-a58de96982596cf4

### [RESULT/WHY] checks rather than significance-lag selection alone. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-e258def66588c0c2` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "significance counts are currently zero across this canonical summary (`n_sig_ami=0`, `n_sig_pami=0` for all 8), so actionable lag decisions should rely on class-level screening plus domain checks rather than significance-lag selection alone"
- `c-2ca2fcf31d35bc01` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "when data are significance-infeasible (for example n=150 in regression tests), surrogates are skipped and decisions are route/class screening only"
- `c-7c1495907632c4f6` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "As the sole decision-maker when surrogate significance bands are unavailable (too-short series): treat the curve as indicative, not authoritative."
- `c-8ef77c2444206fb1` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "rolling-origin exogenous screening using raw CrossMI and conditioned pCrossAMI with horizon-level outputs"
- `c-ccb61954a25b3779` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "separates several dependence diagnostics so teams can choose the smallest useful workflow for a decision, not the largest workflow available"
- `c-d09b1709bcc67a98` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`forecastability_class` High-level interpretation when triage completed"
+ 2 more topic claims across 1 keys (full list in gapmap.json)

**[RESULT]**

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'checks rather than significance-lag selection alone.'. Re-runnable: prompt sha 0dc8531d1acc.

- test: `RESULT:c-e258def66588c0c2`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: Sentences 1 and 2 suggest reliance on class-level screening and domain checks when significance counts are zero, but do not explicitly state expected results or next actions.
- partial hits: c-e258def66588c0c2

**Missing element:** a result-to-interpretation mapping for 'checks rather than significance-lag selection alone.'

**Reasoning:** 1 key(s) state checks rather than significance-lag selection alone.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-e258def66588c0c2

**[WHY]**

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 21dd8ef34c4a.

- test: `WHY:c-e258def66588c0c2`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: prevents reliance on insignificant data

**Missing element:** a reason

**Reasoning:** 1 key(s) state Because significance counts are zero across the canonical summary, actionable lag decisions should rely on class-level screening plus domain checks rather than significance-lag selection alone.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-e258def66588c0c2

### [RESULT] comparing results across routes, outputs should be — RG-UNVER

*Action: verify — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-05488923b7e30cd1` [closure_near] synthetic_extrapolation / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict insufficient — flag: unverified-synthetic: ""blocked": false, "readiness_status": "warning", "forecastability_class": "high", "modeling_regime": "compact_structured_models", "primary_lags": [1, 7]"
- `c-44a10f4353ff9310` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Normalize each route to the same keys when comparing results"
- `c-1d22deb50d3dab26` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "If AMI geometry is disabled with > `--without-ami-geometry` or unavailable for the input, the output stays > descriptive-only and does not emit routing-grade family recommendations."
- `c-632cedcf139eff2c` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "CLI, API, scripts, MCP, and agents are optional access or narration layers around the same deterministic outputs."
- `c-9a8161ef29616bdf` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`blocked` is different from "no forecastable structure." A blocked result means the workflow could not support the requested computation."
- `c-a55a7eb7bbaf3151` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Any numeric claim in an agent response is a restatement of a deterministic result. If the underlying `TriageResult` is wrong, the agent narration will be wrong in the same way."
- `c-b4ea8c21daa0de61` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "CLI, API, notebooks, MCP, and agents are optional access or narration layers around the same deterministic outputs."
+ 1 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a result-to-interpretation mapping for 'comparing results across routes, outputs should be' among the verified sentences retrieved (4 unverified sentences considered separately). Re-runnable: prompt sha 17fb9dfee147.

- test: `RESULT:c-44a10f4353ff9310`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: Expected results are stated in sentence 12.
- synthetic hits (unverified): c-05488923b7e30cd1

**Missing element:** a result-to-interpretation mapping for 'comparing results across routes, outputs should be'

**Reasoning:** 1 key(s) state comparing results across routes, outputs should be; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-44a10f4353ff9310

### [WHY] The notebook learning path should start with the air passengers showcase or covariant informative showcase walkthrough before deeper notebooks. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-72d3ff3a0ef5ef37` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "start with `walkthroughs/00_air_passengers_showcase.ipynb` or `walkthroughs/01_covariant_informative_showcase.ipynb` First-stop walkthrough plus the covariant benchmark walkthrough before deeper notebooks"
- `c-3e060c858058b52f` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "1. Read [../notebooks/README.md](../notebooks/README.md). 2. Run [../notebooks/walkthroughs/00_air_passengers_showcase.ipynb]"
- `c-574ae465285aa0a7` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The v0.3.0 covariant methods all start from $k = 1$ and silently drop any $k = 0$ structure."
- `c-a06bce70252263b9` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Worked examples now live in `examples/univariate/` and `examples/covariant_informative/`; notebook deep dives remain under `notebooks/triage/`"
- `c-bf1996cb00988a8b` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Use the `notebooks/triage/` notebooks only after the walkthroughs; they are deep dives, not first-stop onboarding."
- `c-e3653a25d7c0a396` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Very low `directness_ratio` in `sine_wave` (0.0157) and `air_passengers` (0.0993) supports compact structured models over long-lag complexity."
+ 1 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 9f4a9b5e646a.

- test: `WHY:c-72d3ff3a0ef5ef37`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: none explicitly stated

**Missing element:** a reason

**Reasoning:** 1 key(s) state The notebook learning path should start with the air passengers showcase or covariant informative showcase walkthrough before deeper notebooks.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-72d3ff3a0ef5ef37

### [WHY] The AMI horizon-specific curve should never be collapsed before analysis. — RG-UNVER

*Action: verify — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-361a6f8801f293a8` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Horizon-specific curve, never collapsed before analysis."
- `c-4452a1712336a5ae` [closure_near] synthetic_extrapolation / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict insufficient — flag: unverified-synthetic: "Is there horizon-specific dependence worth exploiting at all? First-pass screening of a target signal before model search"
- `c-8390f6c1d21a8a56` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "frequency-specific cap (Yearly 6, Quarterly 8, Monthly 18, Weekly 13, Daily 14, Hourly 48): AMI values beyond these caps are unreliable."
- `c-8eabb66a53df1fee` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Keep AMI and pAMI horizon-specific; do not pre-aggregate before triage."
- `c-a63ddd04d6950db1` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "AMI is paper-aligned (horizon-specific, kNN-based, with phase-surrogate significance bands)."
- `c-b1533e0303cf092a` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`ForecastabilityAnalyzer` and `ForecastabilityAnalyzerExog` support `method="te"` for raw-curve analysis and TE surrogate significance bands."
- `c-cbda935885e1f4ac` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "When no lags clear the surrogate band, $\varepsilon$ is set above the curve maximum so that `informative_horizons` is empty."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason among the verified sentences retrieved (4 unverified sentences considered separately). Re-runnable: prompt sha 9d080d4c548b.

- test: `WHY:c-361a6f8801f293a8`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: Prevents false negatives in first-pass screening
- synthetic hits (unverified): c-4452a1712336a5ae

**Missing element:** a reason

**Reasoning:** 1 key(s) state The AMI horizon-specific curve should never be collapsed before analysis.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-361a6f8801f293a8

### [DISC] stable import — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-0df8d684323a265f` [closure_near] synthetic_extrapolation / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict insufficient — flag: unverified-synthetic: "Update these files whenever the public API, import surface, or triage-first routing rules change."
- `c-4ea0880906c4e577` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "`forecastability` and `forecastability.triage` Stable import contract"
- `c-bfda34a665d27f27` [seed] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "The package is layered and subpackage-heavy. The stable import facade is small, but the internal tree is organized by role"
- `c-19ce99b47740dfa8` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Treat `services/` as internal helpers, not as a third public API layer."
- `c-1c4e8047d3bd12be` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Use [../public_api.md](../public_api.md) when deciding whether a symbol is part of the supported import contract."
- `c-3b2be48592baf523` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "This package is a deterministic pre-model diagnostic layer, not a downstream model-training or forecasting library."
- `c-49cbd37b19df2392` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "When numeric correctness matters, trace back to `TriageResult` and the stable package facade."
- `c-65b7f762a1a249d5` [topic] literature_supported / documentation, key `ind-s-1ca6a2b8336de5f1`, verdict supports: "Most users only need three things in order: 1. The package facade in [../public_api.md](../public_api.md)."
+ 11 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a boundary for 'stable import'. Re-runnable: prompt sha 03838d911857.

- test: `DISC:stable import`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: Symbols are part of supported import contract if documented in public_api.md, mentioned in files update instructions.
- partial hits: c-1c4e8047d3bd12be
- synthetic hits (unverified): c-0df8d684323a265f

**Missing element:** a boundary for 'stable import'

**Reasoning:** 1 key(s) state stable import; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test DISC:stable import

### [SEL] There is no single right forecasting method; method selection should be based on one's objectives and conditions such as data. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-78a219a9a5e07751` [seed] literature_supported / documentation, key `ind-s-0b00932c0a642b74`, verdict supports: "There is no single right forecasting method to use. Selection of a method should be based on your objectives and your conditions (data etc.)."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a mapping from situation to option. Re-runnable: prompt sha bccba9083797.

- test: `SEL:c-78a219a9a5e07751`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: mentions conditions for selection but not specific options
- partial hits: c-78a219a9a5e07751

**Missing element:** a mapping from situation to option

**Reasoning:** 1 key(s) state There is no single right forecasting method; method selection should be based on one's objectives and conditions such as data.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test SEL:c-78a219a9a5e07751

## §7 checks

### §7.1 Anti-renaming: is the map density in disguise?

Computed over lens candidates only (HYP, RG-SINGLE, RG-UNVER, RG-SIBLING, RG-UNDECIDED and closed candidates) -- RG-UNK and CONTROL are excluded, since their density cannot vary.

- `J10(map, D_low)` = 0.00
- `J10(map, D_high)` = 0.30
- Spearman ρ(score, dens) = 0.33
- flags: closure-uninformative

**Matched-density table** (all lens candidates, by `dens` tercile):

| tercile | n | closed | HYP |
|---|---|---|---|
| low | 15 | 5 | 0 |
| mid | 15 | 2 | 1 |
| high | 16 | 3 | 2 |

Top-tercile closed share: 0.19

**Closure rate by `k_topic` band** (all lens candidates):

| band | n | closed | rate |
|---|---|---|---|
| 0-1 | 41 | 8 | 0.20 |
| 2 | 4 | 2 | 0.50 |
| 3-4 | 1 | 0 | 0.00 |
| >=5 | 0 | 0 | 0.00 |

### S2 fair mismatched-evidence control: does the judge close because of the EVIDENCE, or because of the SEED?

Replaces the first (straw-man) control, second adversarial review, 2026-09-29: the old own-evidence arm always carried the seed's own sentences while the mismatched arm never did (17/22 of PLC's old closures cited only the seed or its source), and the mismatched sentences were off-topic (cyclic gap_id pairing). Now BOTH arms keep the seed's own sentences; the OWN arm adds this candidate's own retrieved non-seed-source sentences; the CONTROL arm replaces those with the non-seed-source sentences retrieved for the topically nearest OTHER candidate of the same lens (max seed-stem Jaccard, ties by gap_id). "other-source-only" is the OWN arm with the seed and same-source sentences excluded entirely -- how often an independent source alone closes it. `closure-uninformative` unless own_rate - control_rate >= 0.20 (of candidates); lenses with < 2 candidates are skipped.

| lens | n | own rate | control rate | other-source-only rate | flag |
|---|---|---|---|---|---|
| HEDGE | 2 | 0.50 | 1.00 | 0.00 | closure-uninformative |
| RESULT | 5 | 0.60 | 0.60 | 0.40 | closure-uninformative |
| SEL | 6 | 1.00 | 1.00 | 0.83 | closure-uninformative |
| WHY | 32 | 0.22 | 0.12 | 0.12 | closure-uninformative |
| **total** | 45 | 0.38 | 0.33 | 0.24 | closure-uninformative |

### S2 lexical donor null: why the lexical closure test was replaced

The reviewer's fair donor null for the (now-comparison-only) LEXICAL closure test: self and same-source claims are excluded from both arms, and the donor is the real non-common content stems of a random other-source A claim of the same knowledge type as the seed (`random.Random(0)`, 200 draws). A check "passes" (is informative) only if the observed count is STRICTLY ABOVE the null's 5-95% interval. DISC is excluded (anchor-regex-driven, not stem-overlap); DIAG is handled per its own closure unit (one rival's sign test, not the group).

| lens | observed closed | null mean | null 5-95% | n | flag |
|---|---|---|---|---|---|
| HEDGE | 0 | 0.1 | [0, 1] | 2 | closure-uninformative |
| RESULT | 3 | 2.2 | [1, 4] | 5 | closure-uninformative |
| SEL | 2 | 1.9 | [0, 4] | 6 | closure-uninformative |
| WHY | 11 | 11.0 | [7, 15] | 32 | closure-uninformative |
| **total** | 16 | 15.2 | [10, 20] |  | closure-uninformative |

### Judge-vs-lexical agreement

Confusion counts, `<lexical_state>-><judge_state>`, over every judged candidate (the lexical test no longer decides anything; this is diagnostic only).

| lexical -> judge | n |
|---|---|
| closed->closed | 5 |
| closed->open | 9 |
| closed->partial | 3 |
| closed->synthetic-closed | 3 |
| open->closed | 4 |
| open->open | 17 |
| open->partial | 3 |
| synthetic-closed->closed | 1 |
| synthetic-closed->synthetic-closed | 1 |

