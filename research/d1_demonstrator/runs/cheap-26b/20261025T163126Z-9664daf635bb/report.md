# N2a reconstruction report (INCOMPLETE)

578 claims span-located, 599 verified, decoy false-accept rate 0%, cost $1.5006. Verifier family: openai.

Incomplete reasons:
- budget exceeded: spent $1.5006 of a $1.5000 budget; refusing the next call

## Sources and clusters

| metric | value |
| --- | --- |
| sources fetched | 26 |
| fetch failures | 0 |
| independent clusters | 4 |
| largest cluster share | 62% |

## Supported claims by source kind/tier

| kind | tier | n supporting-evidence items |
| --- | --- | --- |
| documentation | open | 560 |

### Corroboration distribution (supported claims)

| corroboration | n claims |
| --- | --- |
| 1 | 522 |
| 2 | 17 |
| 3 | 1 |

## Slots by status

| status | n |
| --- | --- |

## Decoy false-accept rate by mutation type (Wilson 95% CI)

| mutation | attempted | valid | false accepts | rate | 95% CI |
| --- | --- | --- | --- | --- | --- |
| negation | 0 | 0 | 0 | 0% | [0%, 0%] |
| number | 0 | 0 | 0 | 0% | [0%, 0%] |
| scope | 0 | 0 | 0 | 0% | [0%, 0%] |

## Area: Extending Toolkit Functionality

### Supported claims

- `c-007b692334093e05` [norm] (literature_supported) — New user-facing imports should be added through forecastability or forecastability.triage only when committing to compatibility.
  > Add new user-facing imports through `forecastability` or `forecastability.triage` only when you want to commit to compatibility.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-08dd95a981ab695e` [strategy] (literature_supported) — Ports should be used for protocol-style seams when a collaborator needs to be substituted or isolated.
  > Use `ports/` for protocol-style seams when a collaborator needs to be substituted or isolated.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0da75a8364f57391` [concept] (literature_supported) — run_lag_aware_mod_mrmr blocks illegal measured lags, preserves declared known-future covariates with provenance, and returns selected, rejected, and blocked rows with scorer diagnostics.
  > `run_lag_aware_mod_mrmr()` blocks illegal measured lags, preserves declared known-future covariates with provenance, and returns selected, rejected, and blocked rows with scorer diagnostics.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-22acb9b0539eee32` [norm] (literature_supported) — Any new selector that goes further than xami_sparse, such as PMIME-style or PC-stable with driver autohistory, must be introduced under a new method label so that shipped cross_pami and xami_sparse semantics are not silently extended.
  > Any new selector that goes further (PMIME-style, PC-stable with driver autohistory) must be introduced under a **new method label** so that the shipped `cross_pami` and `xami_sparse` semantics are not silently extended.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-23bbf434d5ed3536` [concept] (literature_supported) — The driver_nonlin_sq couples to target at lag 1 via a centered quadratic with coefficient 0.40.
  > `driver_nonlin_sq` couples to `target` at lag 1 via a centered quadratic: $$\text{target}[t] \mathrel{+}= 0.40 \times (\text{nl}_1[t-1]^2 - \sigma^2_{\text{nl}_1})$$
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-261dba1aa13e6e82` [concept] (literature_supported) — The PydanticAI agent layer reads frozen deterministic payloads (A1-A3) and generates natural-language narration but does not perform any statistical computation or validate the numeric results.
  > The PydanticAI agent layer reads frozen deterministic payloads (A1-A3) and generates natural-language narration. It does not perform any statistical computation or validate the numeric results.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-2abb88ad6676aac9` [concept] (literature_supported) — The services package provides internal builder and orchestration helpers used by analyzers and use cases.
  > Internal builder/orchestration helpers used by analyzers and use cases
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3160cbd197d92b51` [concept] (literature_supported) — The driver_nonlin_abs couples to target at lag 1 via a centered abs-value with coefficient 0.35.
  > `driver_nonlin_abs` couples to `target` at lag 1 via a centered abs-value: $$\text{target}[t] \mathrel{+}= 0.35 \times ( \text{nl}_2[t-1] - \mathbb{E}[ \text{nl}_2 ])$$
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-33bdb9872d68dc9c` [rationale] (literature_supported) — The project separates dependence diagnostics so teams can choose the smallest useful workflow for a decision, not the largest workflow available.
  > This project separates several dependence diagnostics so teams can choose the smallest useful workflow for a decision, not the largest workflow available.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-356ad4fb83b96c3a` [failure_mode] (literature_supported) — New scorers inherit kNN estimation noise on short series as a limitation of the triage extension diagnostics.
  > new scorers inherit kNN estimation noise on short series
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3c9eed15a2aa4119` [failure_mode] (literature_supported) — The analyzer path for Transfer Entropy is raw-only and partial TE is intentionally unsupported.
  > Analyzer path is raw-only for TE: partial TE is intentionally unsupported.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-454033f260c0fffc` [concept] (literature_supported) — The rf_residual backend captures nonlinear interactions with moderate tuning burden.
  > rf_residual` Captures nonlinear interactions with moderate tuning burden
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4d970d03fcfa1063` [strategy] (literature_supported) — The architecture goal is inward dependency flow where adapters should not become a second business-logic layer.
  > The architecture goal is still inward dependency flow. Adapters should not become a second business-logic layer.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4ed56e3f2d31375a` [norm] (literature_supported) — Agents and MCP do not compute or validate the science but route or narrate deterministic outputs.
  > Agents and MCP do not compute or validate the science. They route or narrate deterministic outputs.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-54d5f9039aa8eac5` [norm] (literature_supported) — Deterministic orchestration must be kept in use_cases and pipeline rather than notebooks or scripts.
  > Keep deterministic orchestration in `use_cases/` and `pipeline/` rather than notebooks or scripts.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-55a3d89f479050f5` [decision] (literature_supported) — Surrogate significance is optional, requires feasible sample size, and needs at least 99 surrogates.
  > Surrogate significance is optional, requires feasible sample size, and needs at least 99 surrogates.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-61c9fd6d8db35ae9` [rationale] (literature_supported) — The known_future_drivers contract is honored at the use-case layer (run_lagged_exogenous_triage) and the selector service itself is pure and does not read it.
  > The `known_future_drivers` contract is honored at the **use-case layer** (`run_lagged_exogenous_triage`). The selector service itself is pure and does not read it.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-65eaabf429163f17` [concept] (literature_supported) — src/forecastability/extensions.py provides extension helpers used by repository workflows such as sensitivity and uncertainty studies.
  > Extension helpers used by repository workflows such as sensitivity and uncertainty studies
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6de236b6fb89f8f5` [concept] (literature_supported) — The synthetic benchmark generate_covariant_benchmark in src/forecastability/utils/synthetic.py implements an 8-variable ground-truth system for controlled method validation.
  > Synthetic benchmark: 8-variable covariant system `generate_covariant_benchmark` in `src/forecastability/utils/synthetic.py` implements an 8-variable ground-truth system used for controlled method validation.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7807c607b6a2bdd3` [norm] (literature_supported) — Triage, pipeline, and services must consume metrics, diagnostics, reporting, and utils.
  > Triage, pipeline, and services consume metrics, diagnostics, reporting, and utils.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-925a7f61d84ad74d` [norm] (literature_supported) — Use cases must orchestrate triage models, pipeline helpers, and internal services, and depend on causal discovery through declared ports contracts.
  > Use cases orchestrate triage models, pipeline helpers, and internal services, and depend on causal discovery through declared `ports/` contracts.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-97859db84d78c736` [failure_mode] (literature_supported) — The linear_residual backend misses nonlinear mediation.
  > linear_residual` Fast, stable, interpretable baseline Misses nonlinear mediation
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a09878eb59fe00c2` [norm] (literature_supported) — The toolkit should not be used for proving physical causality between variables.
  > Do Not Use This For - Proving physical causality between variables.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a3440e8a39a5da28` [failure_mode] (literature_supported) — If the underlying TriageResult is wrong, the agent narration will be wrong in the same way, as any numeric claim in an agent response is a restatement of a deterministic result.
  > Any numeric claim in an agent response is a restatement of a deterministic result. If the underlying `TriageResult` is wrong, the agent narration will be wrong in the same way.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a37e13facfd40287` [norm] (literature_supported) — The paper validates AMI only; pAMI, exogenous cross-dependence, and scorer-registry abstractions are project additions.
  > Paper validates AMI only. - pAMI, exogenous cross-dependence, and scorer-registry abstractions are project additions.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a9262473e308f988` [concept] (literature_supported) — pAMI is a project extension that is not native to the original paper and uses linear residualisation, which does not remove nonlinear mediation.
  > pAMI is a project extension, not a paper-native metric. It uses linear residualisation, so nonlinear mediation is not removed.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-af85afa8a19aa8a4` [concept] (literature_supported) — adapters/agents/ and adapters/llm/ contain optional structured payload and narration adapters.
  > `adapters/agents/` and `adapters/llm/` contain optional structured payload and narration adapters.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-bce5f39d56b978b9` [norm] (literature_supported) — Entrypoints and adapters must call the package facades or use cases.
  > Entrypoints and adapters call the package facades or use cases.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-bff8b6f6f1e86840` [cue] (literature_supported) — Optional narration is a communication layer only and does not create or validate numeric results.
  > Communication layer only; it does not create or validate numeric results
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c0b15726d1bc0e28` [concept] (literature_supported) — The largest Lyapunov exponent estimation (F5) is an experimental diagnostic gated behind `experimental: true` in config and not included in automated triage decisions.
  > **Experimental diagnostic (F5):** largest Lyapunov exponent estimation - gated behind `experimental: true` in config, not included in automated triage decisions.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c4911ab16bfee0a5` [norm] (literature_supported) — Services should be treated as internal helpers, not as a third public API layer.
  > Treat `services/` as internal helpers, not as a third public API layer.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-cc48277836d70680` [check] (literature_supported) — Diagnostic regression fixtures (F9) are golden-value snapshot tests that ensure reproducibility across all new diagnostics.
  > **Diagnostic regression fixtures (F9):** golden-value snapshot tests ensure reproducibility across all new diagnostics.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d78e9f933cd60c34` [representation] (literature_supported) — Structured Pydantic result models (A1-A3) serve as agent payload adapters for deterministic consumption by agents, API consumers, or downstream pipelines.
  > **Agent payload adapters (A1-A3):** structured Pydantic result models for deterministic consumption by agents, API consumers, or downstream pipelines.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d7f88516b54bf57e` [procedure_step] (literature_supported) — Transfer Entropy is re-exported through src/forecastability/services/transfer_entropy_service.py as a compatibility facade.
  > `src/forecastability/services/transfer_entropy_service.py`: compatibility facade re-exporting the diagnostics functions.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-da0e19ceaa2bf031` [prerequisite] (literature_supported) — PCMCI methods require the optional causal extra.
  > The PCMCI methods require the optional causal extra: pip install "dependence-forecastability[causal]"
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-dd09e76a79277cd8` [concept] (literature_supported) — Stable diagnostics include forecastability profiles (F1), theoretical information ceilings (F2), predictive-information learning curves (F3), spectral predictability indices (F4), permutation-entropy and spectral-entropy complexity bands (F6), batch diagnostic ranking (F7), and enhanced exogenous screening with redundancy detection (F8).
  > **Stable diagnostics (F1-F4, F6-F8):** forecastability profiles (F1), theoretical information ceilings (F2), predictive-information learning curves (F3), spectral predictability indices (F4), permutation-entropy and spectral-entropy complexity bands (F6), batch diagnostic ranking (F7), and enhanced exogenous screening with redundancy detection (F8).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-de53a23466bb0539` [check] (literature_supported) — Requests to compute_partial with method="te" raise a validation error because no validated partial-TE estimand is implemented.
  > Requests for `compute_partial(..., method="te")` raise a validation error because no validated partial-TE estimand is implemented in the analyzer path.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e1073e72ca3c2484` [norm] (literature_supported) — Transport concerns must be put in adapters, not in use cases or metrics code.
  > Put transport concerns in `adapters/`, not in use cases or metrics code.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e16d0b99e354a94d` [procedure_step] (literature_supported) — Transfer Entropy is implemented in src/forecastability/diagnostics/transfer_entropy.py with core estimator functions compute_transfer_entropy() and compute_transfer_entropy_curve().
  > Implemented entry points: - `src/forecastability/diagnostics/transfer_entropy.py`: `compute_transfer_entropy()` and `compute_transfer_entropy_curve()` (core estimator path).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e4adc5edce4cb39e` [rationale] (literature_supported) — The nonlinear drivers are included to validate that AMI, TE, and GCMI scores remain informative exactly where Pearson and Spearman fail.
  > The nonlinear drivers are included to validate that AMI, TE, and GCMI scores remain informative exactly where Pearson and Spearman fail, and to motivate the PCMCI-AMI-Hybrid design in V3-F04.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e7e666d57628345c` [concept] (literature_supported) — src/forecastability/ports/__init__.py implements protocol-oriented seams for the hexagonal architecture direction.
  > Protocol-oriented seams for the hexagonal architecture direction
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f6b8c1bd2f44a7f8` [strategy] (literature_supported) — Improving estimator accuracy by raising n_surrogates, increasing sample size, or choosing a better-matched n_neighbors propagates automatically to the profile.
  > improving estimator accuracy (e.g. raising `n_surrogates`, increasing the sample size, or choosing a better-matched `n_neighbors`) propagates automatically to the profile.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-fd495756e94ca657` [concept] (literature_supported) — The fingerprint release is intentionally univariate-first and AMI-first.
  > The fingerprint release is intentionally univariate-first and AMI-first.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)

### Synthetic / rejected claims

- `c-0bbcaac2cc804586` [failure_mode] (synthetic_extrapolation) — The extra_trees_residual backend can still overfit noisy short series and is less interpretable.
  > extra_trees_residual` Strong nonlinear fit with variance reduction from randomized splits Can still overfit noisy short series; less interpretable
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md)
- `c-1075314ff65f00ed` [misconception] (synthetic_extrapolation) — pAMI should not be treated as an exact nonlinear conditional mutual information estimate. (no located evidence)
- `c-1e0afd8caf027c55` [concept] (synthetic_extrapolation) — The Agent narration adapter surface has an experimental stability level. (no located evidence)
- `c-200319b608c0a082` [concept] (synthetic_extrapolation) — The extra_trees_residual backend provides strong nonlinear fit with variance reduction from randomized splits.
  > extra_trees_residual` Strong nonlinear fit with variance reduction from randomized splits
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md)
- `c-4ead62d0678a16e6` [norm] (synthetic_extrapolation) — The toolkit should not be used for replacing rolling-origin forecast evaluation and business KPI tracking. (no located evidence)
- `c-4f954287405e2778` [procedure_step] (synthetic_extrapolation) — Optional narration should be used for stakeholder communication when numeric outputs already exist. (no located evidence)
- `c-525dd6d90b6c701e` [concept] (synthetic_extrapolation) — The Dashboard surface has a beta stability level. (no located evidence)
- `c-55852aae803cdaf7` [expectancy] (synthetic_extrapolation) — Optional narration provides natural-language summary grounded in computed metrics and enables faster cross-functional handoff.
  > Natural-language summary grounded in computed metrics Faster cross-functional handoff (operations, maintenance, planning)
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md)
- `c-6091e9f88ff7d00b` [procedure_step] (synthetic_extrapolation) — The `run_triage` function with `include_extended_fingerprint=True` additively attaches extended_forecastability_analysis for non-exogenous requests. (no located evidence)
- `c-6438b0191aa2bc25` [concept] (synthetic_extrapolation) — The linear_residual backend is fast, stable, and provides an interpretable baseline. (no located evidence)
- `c-695275363028744a` [concept] (synthetic_extrapolation) — The MCP server adapter surface has an experimental stability level. (no located evidence)
- `c-7eda1bc901048e07` [norm] (synthetic_extrapolation) — Experimental diagnostics (F5 Lyapunov) should not be treated as automated decision criteria without expert review. (no located evidence)
- `c-7fd071b8a6fcd1e4` [concept] (synthetic_extrapolation) — The CLI surface has a beta stability level.
  > Surface Entry point Stability --- --- --- CLI `forecastability` Beta
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md)
- `c-888fab4c88533e63` [concept] (synthetic_extrapolation) — The HTTP API surface has a beta stability level. (no located evidence)
- `c-89769d3d50c33531` [failure_mode] (synthetic_extrapolation) — The rf_residual backend has higher variance and compute requirements than linear residualization.
  > rf_residual` Captures nonlinear interactions with moderate tuning burden Higher variance and compute than linear
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md)
- `c-9d940415d1bf0ba0` [misconception] (synthetic_extrapolation) — Learning curve plateaus (F3) should not be treated as proof of information exhaustion because estimator saturation can mimic genuine plateaus. (no located evidence)
- `c-a14221339eaf58b2` [norm] (synthetic_extrapolation) — DTW is intentionally out of scope for lagged-exogenous triage and would require a separate plan, new surface, new method label, and explicit chronological-causality guard before it could be admitted to a forecasting tensor. (no located evidence)
- `c-b1eb856c66d4ee24` [norm] (synthetic_extrapolation) — The toolkit should not be used for comparing very short windows where minimum sample assumptions are not met. (no located evidence)
- `c-bcbf695d48ed287c` [concept] (synthetic_extrapolation) — Lag-Aware ModMRMR selects sparse covariate lags that are informative, non-redundant against already selected features, and legal for the forecast horizon. (no located evidence)
- `c-be2437caf64e1e58` [norm] (synthetic_extrapolation) — For exogenous requests, the extended_forecastability_analysis field is omitted rather than pretending exogenous-aware extended analysis exists. (no located evidence)
- `c-ca32ae8847dff4f1` [concept] (synthetic_extrapolation) — The use_cases package serves as main orchestration entry points for deterministic triage and batch triage.
  > Main orchestration entry points for deterministic triage and batch triage
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md)
- `c-e28f4466aa2bd6a0` [norm] (synthetic_extrapolation) — The toolkit should not be used for setting maintenance policy thresholds without domain constraints and risk-cost modeling. (no located evidence)

### UNKNOWN / thin / unverified / unexamined slots

- none

## Area: Dependence Modeling in Forecastability

### Supported claims

- `c-0010f40040f5f30a` [concept] (literature_supported) — To handle time series with obvious periodicity, some algorithms and null hypotheses have been proposed for surrogate data testing.
  > To tackle this case, some algorithms and null hypotheses have been proposed.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-014eeea445c8fc65` [concept] (literature_supported) — The autocorrelation function of an AR(p) process tails off just like the partial autocorrelation function of an MA(q) process.
  > the autocorrelation function of an AR(p) process tails off just like the partial autocorrelation function of an MA(q) process
  (documentation, https://en.wikipedia.org/wiki/Partial_autocorrelation_function, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-01705afc324b0a2a` [concept] (literature_supported) — A "known-future" exogenous covariate is one whose k=0 value is legitimately observed before Y_t must be predicted, including calendar features, holidays, regulator-set tariffs, and planned promotional events.
  > A "known-future" exogenous covariate is one whose $k=0$ value is legitimately observed **before** $Y_t$ must be predicted: calendar features, holidays, regulator-set tariffs, planned promotional events.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-01a236bf8006dd6e` [check] (literature_supported) — F8 should be avoided without Benjamini-Hochberg FDR correction when many drivers are tested simultaneously because uncorrected p-values will inflate false-positive rates.
  > Without BH FDR correction when many drivers are tested simultaneously: uncorrected $p$-values will inflate false-positive rates.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-02293075bf7d14f3` [procedure_step] (literature_supported) — The pAMI estimator builds a conditioning matrix Z, residualizes past and future on Z using a linear backend by default with optional RF backend, then computes MI on residual pairs.
  > Current estimator in this repo: 1. Build conditioning matrix \(Z=[X_{t+1},\ldots,X_{t+h-1}]\). 2. Residualize past and future on \(Z\) (linear backend by default; optional RF backend). 3. Compute MI on residual pairs.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-036f6b526cb8eadb` [rationale] (literature_supported) — Spearman is near zero for the abs-value coupling because |X| is V-shaped (non-monotone) in X.
  > Spearman is also near zero because $ X $ is V-shaped (non-monotone) in $X$.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-04070c929c03d0c4` [norm] (literature_supported) — In other disciplines like engineering, the normalization is usually dropped and the terms autocorrelation and autocovariance are used interchangeably.
  > However, in other disciplines (e.g. engineering) the normalization is usually dropped and the terms "autocorrelation" and "autocovariance" are used interchangeably.
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-0451ed09ab140257` [concept] (literature_supported) — Many other surrogate data methods have been proposed, some based on optimizations to achieve an autocorrelation close to the original one, some based on wavelet transform and some capable of dealing with some types of non-stationary data.
  > Many other surrogate data methods have been proposed, some based on optimizations to achieve an autocorrelation close to the original one, some based on wavelet transform and some capable of dealing with some types of non-stationary data.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-0568df39c001b613` [check] (literature_supported) — F8 should be avoided for very short series because CrossAMI inherits the same finite-sample bias and minimum-length requirements as univariate AMI.
  > For very short series: CrossAMI inherits the same finite-sample bias and minimum- length requirements as univariate AMI.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-05f4e7e9efaee069` [concept] (literature_supported) — The autocovariance function is not well defined for all time series or processes because the mean may not exist, or the variance may be zero for a constant process or infinite for processes with distribution lacking well-behaved moments.
  > this expression is not well defined for all-time series or processes, because the mean may not exist, or the variance may be zero (for a constant process) or infinite (for processes with distribution lacking well-behaved moments, such as certain types of power law).
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-089073b9937202ba` [procedure_step] (literature_supported) — Algorithm 2 (Iterative AAFT) is an iterative version of AAFT with steps repeated until the autocorrelation function is sufficiently similar to the original, or until there is no change in the amplitudes.
  > Iterative algorithm 2, or IAAFT (for Iterative Amplitude Adjusted Fourier Transform): This algorithm is an iterative version of AAFT. The steps are repeated until the autocorrelation function is sufficiently similar to the original, or until there is no change in the amplitudes.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-0938aacab4017209` [concept] (literature_supported) — diagnostics/cmi.py owns alternative residual backends used by pAMI-style workflows.
  > `diagnostics/cmi.py` owns alternative residual backends used by pAMI-style workflows.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0b887799f98f043c` [concept] (literature_supported) — Both nonlinear couplings create statistically dependent joint distributions even though the marginal covariance is zero.
  > Both couplings create statistically dependent joint distributions even though the marginal covariance is zero.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0d5cc65a382f712e` [concept] (literature_supported) — Transfer entropy reduces to Granger causality for vector auto-regressive processes.
  > Transfer entropy reduces to Granger causality for vector auto-regressive processes.
  (documentation, https://en.wikipedia.org/wiki/Transfer_entropy, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-12f83d379ed3d9b0` [strategy] (literature_supported) — PCMCI-AMI orchestration follows the inward-only dependency rule where use cases depend on declared ports (protocol contracts), and adapters satisfy those contracts without adapter-to-adapter helper coupling.
  > PCMCI-AMI orchestration now follows the inward-only dependency rule: use cases depend on declared ports (protocol contracts), and adapters satisfy those contracts without adapter-to-adapter helper coupling.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-14bf0968450c6f98` [concept] (literature_supported) — MI, TE, and GCMI measure dependence in the full joint distribution P(X, Y), not only the linear second moment.
  > MI, TE, and GCMI measure dependence in the full joint distribution $P(X, Y)$, not only the linear second moment.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-17941110bd4a294c` [concept] (literature_supported) — The CausalGraphPort contract provides PCMCI+ style graph discovery with a discover(...) -> CausalGraphResult method.
  > `CausalGraphPort` `discover(...) -> CausalGraphResult` PCMCI+ style graph discovery
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-17b28a3bd81ccff9` [concept] (literature_supported) — The "burg" method for pacf uses Burg's partial autocorrelation estimator.
  > "burg" : Burg's partial autocorrelation estimator.
  (documentation, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html, published None, independence ind-s-5114732bc45e7988, corroboration 1)
- `c-18943cbbab8481d9` [concept] (literature_supported) — The Exogenous Screening (F8) diagnostic measures the cross-series mutual information between a target series and one or more candidate exogenous drivers at each forecast horizon, filtered by Benjamini-Hochberg FDR control.
  > The cross-series mutual information between a target series and one or more candidate exogenous drivers at each forecast horizon, filtered by Benjamini-Hochberg FDR control, to screen which exogenous variables carry statistically detectable predictive signal.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-1de0b0dfaac527a7` [norm] (literature_supported) — In signal processing, the autocorrelation function is often used without normalization, that is, without subtracting the mean and dividing by the variance.
  > In signal processing, the above definition is often used without the normalization, that is, without subtracting the mean and dividing by the variance.
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-1fab6f27ed690769` [concept] (literature_supported) — Transfer entropy has been used for statistical causality analysis between armed conflict events.
  > Transfer entropy has been used for estimation of functional connectivity of neurons, social influence in social networks and statistical causality between armed conflict events.
  (documentation, https://en.wikipedia.org/wiki/Transfer_entropy, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-210a18347aa678c8` [concept] (literature_supported) — Constrained realizations surrogate data methods are usually based on preserving the linear structure of the original series, such as by preserving the autocorrelation function or equivalently the periodogram.
  > These surrogate data methods are usually based on preserving the linear structure of the original series (for instance, by preserving the autocorrelation function, or equivalently the periodogram, an estimate of the sample spectrum).
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-21586c1b3ff04cdf` [concept] (literature_supported) — The CausalGraphFullPort contract provides both PCMCI-AMI full three-phase result path with discover(...) -> CausalGraphResult and discover_full(...) -> PcmciAmiResult methods.
  > `CausalGraphFullPort` `discover(...) -> CausalGraphResult` and `discover_full(...) -> PcmciAmiResult` PCMCI-AMI full three-phase result path
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-23e10779be9a4976` [failure_mode] (literature_supported) — DTW methods do not produce a fixed-lag predictive feature set, do not respect the chronological causality required by forecasting tensors, and do not output a lag map directly consumable by ordinary regression or neural forecasting models.
  > They do not: - produce a fixed-lag predictive feature set - respect the chronological causality required by forecasting tensors - output a lag map that is directly consumable by ordinary regression or neural forecasting models
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-243850c163a84204` [concept] (literature_supported) — The "ols" method for pacf performs regression of time series on lags of it and on constant.
  > "ols" : regression of time series on lags of it and on constant.
  (documentation, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html, published None, independence ind-s-5114732bc45e7988, corroboration 1)
- `c-24aa95a38d09f00a` [rationale] (literature_supported) — Based on simulation evidence across a range of low-order ARMA models, the best methods for pacf based on root MSE are Yule-Walker (MLW), Levinson-Durbin (MLE) and Burg, respectively.
  > Based on simulation evidence across a range of low-order ARMA models, the best methods based on root MSE are Yule-Walker (MLW), Levinson-Durbin (MLE) and Burg, respectively.
  (documentation, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html, published None, independence ind-s-5114732bc45e7988, corroboration 1)
- `c-24b50a94338e6f5d` [representation] (literature_supported) — Transfer entropy can be expressed as the difference between the conditional entropy of future Y given its own past and the conditional entropy of future Y given both its own past and X's past.
  > T X → Y = H ( Y t ∣ Y t − 1 : t − L ) − H ( Y t ∣ Y t − 1 : t − L , X t − 1 : t − L )
  (documentation, https://en.wikipedia.org/wiki/Transfer_entropy, published None, independence ind-s-0b00932c0a642b74, corroboration 2)
- `c-2951c6bc5a4bbd60` [concept] (literature_supported) — For an AR(p) series, the partial autocorrelation function cuts off after lag p, similar to how the autocorrelation function of an MA(q) series behaves with lag q.
  > the partial autocorrelation function of an AR(p) series cuts off after lag p similar to the autocorrelation function of an MA(q) series with lag q
  (documentation, https://en.wikipedia.org/wiki/Partial_autocorrelation_function, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-2a2178f666a2258b` [rationale] (literature_supported) — Spearman is near zero for the quadratic coupling because X² is U-shaped (non-monotone) in X.
  > Spearman is also near zero because $X^2$ is U-shaped (non-monotone) in $X$.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-2d8e9ac84a4e1468` [concept] (literature_supported) — The "ywadjusted" method for pacf uses Yule-Walker with sample-size adjustment in denominator for acovf.
  > "yw", "ywa", "ywadjusted" or "yw_adjusted" : Yule-Walker with sample-size adjustment in denominator for acovf. Default.
  (documentation, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html, published None, independence ind-s-5114732bc45e7988, corroboration 1)
- `c-33236c46fb40bf9d` [interpretation] (literature_supported) — The v0.3.0 cross_pami curve remains target_only conditioned and covers k ∈ {1, ..., K_max} only, with semantics not relabelled in v0.3.2.
  > The v0.3.0 `cross_pami` curve remains `target_only` conditioned and covers $k \in \{1, \dots, K_{\max}\}$ only. Its semantics are not relabelled in v0.3.2.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-34c60e2c3dc669be` [expectancy] (literature_supported) — selected_for_tensor is impossible at lag=0 by default.
  > `selected_for_tensor=True` is impossible at `lag=0` by default.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-398ef2085154c3de` [concept] (literature_supported) — The "ols-adjusted" method for pacf performs regression of time series on lags with a bias adjustment.
  > "ols-adjusted" : regression of time series on lags with a bias adjustment.
  (documentation, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html, published None, independence ind-s-5114732bc45e7988, corroboration 1)
- `c-39d2e6161357180a` [expert_novice_contrast] (literature_supported) — Pearson and Spearman screens would rank both nonlinear drivers below independent noise, demonstrating a linear blind-spot.
  > A Pearson or Spearman screen would rank both drivers below independent noise - the hallmark of a linear blind-spot.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3fec04acd8d0297e` [concept] (literature_supported) — AMI at horizon h is defined as the mutual information between X_t and X_{t+h}.
  > Paper-native metric AMI at horizon \(h\): \[ I_h = I(X_t; X_{t+h}) \]
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4713c4f33c2bf8fe` [rationale] (literature_supported) — The xami_sparse selector does not condition on the driver's own autohistory; that stronger conditioning is the job of pcmci_ami (full_mci) from v0.3.0.
  > It does **not** condition on the driver's own autohistory. That stronger conditioning is the job of `pcmci_ami` (`full_mci`) from v0.3.0.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-488dad8b3c64c9fd` [concept] (literature_supported) — Transfer entropy is a non-parametric statistic measuring the amount of directed, time-asymmetric transfer of information between two random processes.
  > Transfer entropy is a non-parametric statistic measuring the amount of directed (time-asymmetric) transfer of information between two random processes.
  (documentation, https://en.wikipedia.org/wiki/Transfer_entropy, published None, independence ind-s-0b00932c0a642b74, corroboration 2)
- `c-4e39686e19b92a20` [concept] (literature_supported) — Transfer Entropy is directional in that TE(X → Y) is generally not equal to TE(Y → X).
  > Transfer entropy from a process X to another process Y is the amount of uncertainty reduced in future values of Y by knowing the past values of X given past values of Y.
  (documentation, https://en.wikipedia.org/wiki/Transfer_entropy, published None, independence ind-s-0b00932c0a642b74, corroboration 2)
- `c-519997718ac5596b` [procedure_step] (literature_supported) — Algorithm 0 or RS (Random Shuffle) creates new data by random permutations of the original series.
  > Algorithm 0, or RS (for Random Shuffle): New data are created simply by random permutations of the original series.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-5690729af3aa35b6` [concept] (literature_supported) — The Data-Processing Inequality states that applying a lossy transformation T to the information set cannot increase forecastability.
  > The Data-Processing Inequality states that applying a lossy transformation $T$ to the information set cannot increase forecastability: $$ F(h;\,T(\mathcal{I}_t)) \le F(h;\,\mathcal{I}_t) $$
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-57f60d797dd50453` [mental_model] (literature_supported) — The intuitive meaning of mutual information is the amount of information (that is, reduction in uncertainty) that knowing either variable provides about the other.
  > This corroborates the intuitive meaning of mutual information as the amount of information (that is, reduction in uncertainty) that knowing either variable provides about the other.
  (documentation, https://en.wikipedia.org/wiki/Mutual_information, published None, independence ind-s-0b00932c0a642b74, corroboration 2)
- `c-599f2ed68644b97d` [failure_mode] (literature_supported) — The conditioning-out step in residualisation removes only the component of dependence that is linearly predictable from the intermediate lags, and nonlinear residual dependence that the linear backend cannot capture may remain in the AMI but not be fully removed from pAMI.
  > The conditioning-out step removes only the component of dependence that is linearly predictable from the intermediate lags. Nonlinear residual dependence that the linear backend cannot capture remains in the AMI but may not be fully removed from pAMI.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-59cd014eacf1959b` [concept] (literature_supported) — Autocorrelation is widely used in signal processing, time domain and time series analysis to understand the behavior of data over time.
  > Autocorrelation is widely used in signal processing, time domain and time series analysis to understand the behavior of data over time.
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-5dfc565a9c336111` [concept] (literature_supported) — pAMI is a project extension that uses a linear-residual approximation rather than exact conditional mutual information.
  > pAMI is a project extension that uses a linear-residual approximation rather than exact conditional mutual information.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5e20931038c7b5bf` [concept] (literature_supported) — All eigenvalues of the autocorrelation matrix are real and non-negative.
  > All eigenvalues of the autocorrelation matrix are real and non-negative.
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-5f96ef54fa2b30c4` [expectancy] (literature_supported) — Transfer entropy usually requires more samples for accurate estimation than Granger causality.
  > However, it usually requires more samples for accurate estimation.
  (documentation, https://en.wikipedia.org/wiki/Transfer_entropy, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-64a81217e097dae7` [concept] (literature_supported) — Linear surrogate methods are useful for data showing irregular fluctuations and short-term variabilities.
  > Broadly speaking, these methods are useful for data showing irregular fluctuations (short-term variabilities) and data with such a behaviour abound in the real world.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-671214eb0cca876c` [concept] (literature_supported) — For a target series and candidate exogenous series, one qualitatively different question asks whether the past of the exogenous series carries usable predictive information about the future of the target series, formalized as I(X_{t-k}; Y_t) for k ≥ 1.
  > Does the **past** of $X$ carry usable predictive information about the **future** of $Y$? $I(X_{t-k}\,;\,Y_t)$ for $k \ge 1$
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-69ec3c43f524dcb0` [concept] (literature_supported) — Partial autocorrelation is a commonly used tool for identifying the order of an autoregressive model.
  > Partial autocorrelation is a commonly used tool for identifying the order of an autoregressive model.
  (documentation, https://en.wikipedia.org/wiki/Partial_autocorrelation_function, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-6a41095a7120bd7d` [concept] (literature_supported) — The autocorrelation function definition may not have a well-defined expectation in all cases.
  > Note that the expectation may not be well defined.
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-6e5c5af4b40ecbf5` [norm] (literature_supported) — It is common practice in some disciplines like statistics and time series analysis to normalize the autocovariance function to get a time-dependent Pearson correlation coefficient.
  > It is common practice in some disciplines (e.g. statistics and time series analysis) to normalize the autocovariance function to get a time-dependent Pearson correlation coefficient.
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-70872842e6096f91` [decision] (literature_supported) — If the value of the statistic is significantly different for the original series than for the surrogate set in surrogate data testing, the null hypothesis is rejected and non-linearity is assumed.
  > If the value of the statistic is significantly different for the original series than for the surrogate set, the null hypothesis is rejected and non-linearity assumed.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-720bc05abc5fb172` [concept] (literature_supported) — The partial autocorrelation of lags greater than p for an AR(p) time series are approximately independent and normal with a mean of 0.
  > The partial autocorrelation of lags greater than p for an AR(p) time series are approximately independent and normal with a mean of 0.
  (documentation, https://en.wikipedia.org/wiki/Partial_autocorrelation_function, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-735f511d913a1d2e` [concept] (literature_supported) — The "ols-inefficient" method for pacf performs regression of time series on lags using a single common sample to estimate all pacf coefficients.
  > "ols-inefficient" : regression of time series on lags using a single common sample to estimate all pacf coefficients.
  (documentation, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html, published None, independence ind-s-5114732bc45e7988, corroboration 1)
- `c-7491c5056c4cfdef` [decision] (literature_supported) — Results from pAMI differ between the linear (default) and RF backends, with the linear backend being faster and more stable while the RF backend may capture more nonlinear residual structure but introduces additional noise for short series.
  > Results differ between the linear (default) and RF backends. The linear backend is faster and more stable; the RF backend may capture more nonlinear residual structure but introduces additional noise for short series.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-74a11951f9445a63` [concept] (literature_supported) — In the surrogate data testing null hypothesis, the static measurement function depends only on the present value of its argument, not on past ones.
  > In this hypothesis, the static measurement function is one which depends only on the present value of its argument, not on past ones.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-7615dadcd67311b0` [concept] (literature_supported) — DTW (Dynamic Time Warping), FastDTW, and ShapeDTW solve elastic-alignment similarity by searching for alignment that minimises path-cumulated distance between two time series.
  > DTW (Dynamic Time Warping), FastDTW, and ShapeDTW solve **elastic-alignment similarity**: they search for the alignment $\pi$ that minimises a path-cumulated distance between two time series.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-76c01f7f1cb3be7b` [concept] (literature_supported) — The "ldb" method for pacf uses Levinson-Durbin recursion without bias correction.
  > "ldb", "ldbiased" or "ld_biased" : Levinson-Durbin recursion without bias correction.
  (documentation, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html, published None, independence ind-s-5114732bc45e7988, corroboration 1)
- `c-7ffa88b778fa7f2b` [concept] (literature_supported) — Transfer Entropy at lag h is defined as the mutual information between Y_t and X_{t-h} conditioned on the history of Y.
  > Transfer entropy is a non-parametric statistic measuring the amount of directed (time-asymmetric) transfer of information between two random processes.
  (documentation, https://en.wikipedia.org/wiki/Transfer_entropy, published None, independence ind-s-0b00932c0a642b74, corroboration 2)
- `c-83fde0ea1c1eb453` [concept] (literature_supported) — If the log base 2 is used, the unit of mutual information is the shannon, also known as the bit.
  > If the log base 2 is used, the unit of mutual information is the shannon, also known as the bit.
  (documentation, https://en.wikipedia.org/wiki/Mutual_information, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-8474898445df52f0` [procedure_step] (literature_supported) — In surrogate data testing, a discriminating statistic is calculated for the original time series and all the surrogate set.
  > A discriminating statistic is then calculated for the original time series and all the surrogate set.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-85b0c64b18f5fceb` [concept] (literature_supported) — The PACF contrasts with the autocorrelation function, which does not control for other lags.
  > It contrasts with the autocorrelation function, which does not control for other lags.
  (documentation, https://en.wikipedia.org/wiki/Partial_autocorrelation_function, published None, independence ind-s-0b00932c0a642b74, corroboration 2)
- `c-8741b82d3972b182` [concept] (literature_supported) — If the natural logarithm is used, the unit of mutual information is the nat.
  > If the natural logarithm is used, the unit of mutual information is the nat.
  (documentation, https://en.wikipedia.org/wiki/Mutual_information, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-886adb6e1e90fe24` [rationale] (literature_supported) — Conditioning on target history in Transfer Entropy controls for autocorrelation-driven carryover in the target.
  > Transfer entropy from a process X to another process Y is the amount of uncertainty reduced in future values of Y by knowing the past values of X given past values of Y.
  (documentation, https://en.wikipedia.org/wiki/Transfer_entropy, published None, independence ind-s-0b00932c0a642b74, corroboration 2)
- `c-8929289a585563de` [procedure_step] (literature_supported) — F8 should be used when candidate exogenous variables are available and one needs to decide which, if any, are worth including in a multivariate model.
  > When candidate exogenous variables are available and you need to decide which, if any, are worth including in a multivariate model.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8c2271a217c65d37` [rationale] (literature_supported) — The pacf estimators with the lowest bias include Yule-Walker (MLW), Levinson-Durbin (MLE), Burg, OLS and OLS-adjusted.
  > The estimators with the lowest bias included included these three in addition to OLS and OLS-adjusted.
  (documentation, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html, published None, independence ind-s-5114732bc45e7988, corroboration 1)
- `c-8cbcd1ee08854a82` [concept] (literature_supported) — When adjusted is True, denominators for cross-covariance are the number of overlapping observations at each lag k, min(m, n-k).
  > If True, then denominators for cross-covariance are the number of overlapping observations at each lag k, min(m, n-k)
  (documentation, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.ccf.html, published None, independence ind-s-5114732bc45e7988, corroboration 1)
- `c-8d0dc8e266e2a5e3` [concept] (literature_supported) — Supported covariant analysis method names include cross_ami, cross_pami, te, gcmi, pcmci, and pcmci_ami.
  > Supported method names include: - `cross_ami` - `cross_pami` - `te` - `gcmi` - `pcmci` - `pcmci_ami`
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8d70357c6bf07976` [concept] (literature_supported) — In the context of surrogate data testing, linear means that each value is linearly dependent on past values or on present and past values of some independent identically distributed process, usually also Gaussian.
  > Here linear means that each value is linearly dependent on past values or on present and past values of some independent identically distributed (i.i.d.) process, usually also Gaussian.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-8d943047976ac929` [concept] (literature_supported) — Claude Shannon defined and analyzed mutual information in his paper "A Mathematical Theory of Communication", though he did not call it "mutual information".
  > The quantity was defined and analyzed by Claude Shannon in his landmark paper "A Mathematical Theory of Communication", although he did not call it "mutual information".
  (documentation, https://en.wikipedia.org/wiki/Mutual_information, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-9172d59eb6aef87e` [concept] (literature_supported) — Transfer entropy from process X to process Y is the amount of uncertainty reduced in future values of Y by knowing the past values of X given past values of Y.
  > Transfer entropy from a process X to another process Y is the amount of uncertainty reduced in future values of Y by knowing the past values of X given past values of Y.
  (documentation, https://en.wikipedia.org/wiki/Transfer_entropy, published None, independence ind-s-0b00932c0a642b74, corroboration 2)
- `c-935ed14f6571659d` [concept] (literature_supported) — Constrained realizations surrogate data methods do not depend on a particular model, nor on any parameters, and are thus non-parametric methods.
  > The last surrogate data methods do not depend on a particular model, nor on any parameters, thus they are non-parametric methods.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-9669805ba1b00cc6` [procedure_step] (literature_supported) — F8 should be used in combination with F1 because F8 extends the analysis to cross-series dependence while F1 remains the primary univariate anchor.
  > In combination with F1: F8 extends the analysis to cross-series dependence; F1 remains the primary univariate anchor.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-9abe82177371fd61` [rationale] (literature_supported) — Transfer entropy is advantageous when the model assumption of Granger causality does not hold, for example in analysis of non-linear signals.
  > Hence, it is advantageous when the model assumption of Granger causality doesn't hold, for example, analysis of non-linear signals.
  (documentation, https://en.wikipedia.org/wiki/Transfer_entropy, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-9c355ba47e7b1a70` [concept] (literature_supported) — The DPI is a ceiling constraint, not a pessimistic prediction.
  > The DPI is a ceiling constraint, not a pessimistic prediction.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-9e8423e698c7bda3` [concept] (literature_supported) — In surrogate data testing, the null hypothesis typically describes that the data is a realization of a stationary linear system whose output has been possibly measured by a monotonically increasing possibly nonlinear but static function.
  > The data is a realization of a stationary linear system, whose output has been possibly measured by a monotonically increasing possibly nonlinear (but static) function.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-9e9a2991b23920ac` [expectancy] (literature_supported) — In finite samples with residual approximation, occasional pAMI > AMI can occur.
  > In finite samples with residual approximation, occasional \(\tilde{I}_h > I_h\) can occur.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-9eaada5f5cd19a45` [concept] (literature_supported) — Algorithm 0 (Random Shuffle) is associated to the null hypothesis of the data being uncorrelated i.i.d noise, possibly Gaussian and measured by a static nonlinear function.
  > This method is associated to the null hypothesis of the data being uncorrelated i.i.d noise (possibly Gaussian and measured by a static nonlinear function).
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-a0af50e1f96be86f` [concept] (literature_supported) — The techniques mentioned are called linear surrogate methods because they are based on a linear process and address a linear null hypothesis.
  > The above mentioned techniques are called linear surrogate methods, because they are based on a linear process and address a linear null hypothesis.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-a279135b3d8affd1` [concept] (literature_supported) — Mutual information quantifies the amount of information obtained about one random variable by observing the other random variable.
  > it quantifies the "amount of information" (in units such as shannons (bits), nats or hartleys) obtained about one random variable by observing the other random variable.
  (documentation, https://en.wikipedia.org/wiki/Mutual_information, published None, independence ind-s-0b00932c0a642b74, corroboration 2)
- `c-a29d26bbe4171e33` [concept] (literature_supported) — If the log base 10 is used, the unit of mutual information is the hartley, also known as the ban or the dit.
  > If the log base 10 is used, the unit of mutual information is the hartley, also known as the ban or the dit.
  (documentation, https://en.wikipedia.org/wiki/Mutual_information, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-a53e1acd4e8c40da` [concept] (literature_supported) — The term "mutual information" was coined by Robert Fano.
  > This term was coined later by Robert Fano.
  (documentation, https://en.wikipedia.org/wiki/Mutual_information, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-a5c4c59c3f4b3044` [procedure_step] (literature_supported) — If surrogates from Algorithm 1 (Random Phases) must be real, the Fourier phases must be antisymmetric with respect to the central value of data.
  > If the surrogates must be real, the Fourier phases must be antisymmetric with respect to the central value of data.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-a6fddfea35d5480e` [concept] (literature_supported) — The "ld" method for pacf uses Levinson-Durbin recursion with bias correction.
  > "ld", "lda", "ldadjusted" or "ld_adjusted" : Levinson-Durbin recursion with bias correction.
  (documentation, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html, published None, independence ind-s-5114732bc45e7988, corroboration 1)
- `c-a73dfb9424c4297e` [concept] (literature_supported) — kNN MI estimators detect nonlinear dependence directly through local density structure.
  > kNN MI estimators detect this dependence directly through local density structure.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a99a13ed405afe53` [concept] (literature_supported) — Typical realizations are generated as outputs of a well-fitted model to the original data.
  > Typical realizations: data series are generated as outputs of a well-fitted model to the original data.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-aa736260f8be05bf` [concept] (literature_supported) — The autocorrelation matrix is used in various digital signal processing algorithms.
  > The autocorrelation matrix is used in various digital signal processing algorithms.
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-aa90dea343b1392f` [concept] (literature_supported) — Transfer entropy has been used for estimation of functional connectivity of neurons.
  > Transfer entropy has been used for estimation of functional connectivity of neurons, social influence in social networks and statistical causality between armed conflict events.
  (documentation, https://en.wikipedia.org/wiki/Transfer_entropy, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-ac8ebfd4bba1c07d` [concept] (literature_supported) — In some fields, the term autocorrelation is used interchangeably with autocovariance.
  > In some fields, the term is used interchangeably with autocovariance.
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-ad41624f4a27df8a` [rationale] (literature_supported) — The normalization of autocorrelation is important because the interpretation of autocorrelation as a correlation provides a scale-free measure of the strength of statistical dependence.
  > The normalization is important both because the interpretation of the autocorrelation as a correlation provides a scale-free measure of the strength of statistical dependence
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-ad97c00ed2b5f40b` [concept] (literature_supported) — In surrogate data testing, a process being ARMA type is equivalent to saying that each value is linearly dependent on past values or on present and past values of some independent identically distributed process.
  > This is equivalent to saying that the process is ARMA type.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-ae5530e3b2ce2de7` [concept] (literature_supported) — Autocorrelation, sometimes known as serial correlation in the discrete time case, measures the correlation of a signal with a delayed copy of itself.
  > Autocorrelation, sometimes known as serial correlation in the discrete time case, measures the correlation of a signal with a delayed copy of itself.
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-b0cf6ea03d6fd3c7` [concept] (literature_supported) — Surrogate data testing is used to detect non-linearity in a time series.
  > It is used to detect non-linearity in a time series.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-b112bf42665e56b4` [concept] (literature_supported) — Time series exhibiting strong periodicities are clearly not consistent with the linear null hypotheses used in standard surrogate data methods.
  > Time series exhibiting strong periodicities are clearly not consistent with the linear null hypotheses.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-b134e3b39c3ee09b` [concept] (literature_supported) — Transfer entropy has been used for analysis of social influence in social networks.
  > Transfer entropy has been used for estimation of functional connectivity of neurons, social influence in social networks and statistical causality between armed conflict events.
  (documentation, https://en.wikipedia.org/wiki/Transfer_entropy, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-b1b0fa637a2ffb87` [concept] (literature_supported) — AMI is a nonlinear analog of ACF and includes both direct and mediated lag paths.
  > Nonlinear analog of ACF (total dependence at lag \(h\)). - Includes both direct and mediated lag paths.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-b2381481a529a516` [concept] (literature_supported) — The autocorrelation matrix is a Hermitian matrix for complex random vectors and a symmetric matrix for real random vectors.
  > The autocorrelation matrix is a Hermitian matrix for complex random vectors and a symmetric matrix for real random vectors.
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-b5cae156d2a4fdea` [concept] (literature_supported) — The analysis of autocorrelation is a mathematical tool for identifying repeating patterns or hidden periodicities within a signal obscured by noise.
  > The analysis of autocorrelation is a mathematical tool for identifying repeating patterns or hidden periodicities within a signal obscured by noise.
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-b75a19c17f2efb10` [concept] (literature_supported) — The PACF was introduced as part of the Box-Jenkins approach to time series modelling for determining the appropriate lags p in an AR(p) model or in an extended ARIMA(p,d,q) model.
  > The use of this function was introduced as part of the Box-Jenkins approach to time series modelling, whereby plotting the partial autocorrelative functions one could determine the appropriate lags p in an AR (p) model or in an extended ARIMA (p,d,q) model.
  (documentation, https://en.wikipedia.org/wiki/Partial_autocorrelation_function, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-be5a55daceea39a6` [concept] (literature_supported) — pAMI at horizon h is defined as the mutual information between X_t and X_{t+h} conditioned on intermediate lags X_{t+1} through X_{t+h-1}.
  > Project extension metric pAMI at horizon \(h\): \[ \tilde{I}_h = I(X_t; X_{t+h} \mid X_{t+1},\ldots,X_{t+h-1}) \]
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-bf6c9c244ff994ed` [procedure_step] (literature_supported) — Algorithm 1 or RP (Random Phases, also known as FT for Fourier Transform) creates surrogate data by the inverse Fourier Transform of the modules of Fourier Transform of the original data with new uniformly random phases to preserve the linear correlation of the series.
  > Algorithm 1, or RP (for Random Phases; also known as FT, for Fourier Transform): In order to preserve the linear correlation (the periodogram) of the series, surrogate data are created by the inverse Fourier Transform of the modules of Fourier Transform of the original data with new (uniformly random) phases.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-bfb3798f2f5c42b7` [concept] (literature_supported) — The ports package contains protocol-oriented seams for the architecture direction, including causal discovery contracts CausalGraphPort and CausalGraphFullPort.
  > Protocol-oriented seams for the architecture direction, including causal discovery contracts (`CausalGraphPort`, `CausalGraphFullPort`)
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c04ac8aa3206496e` [interpretation] (literature_supported) — The v0.3.0 covariant methods all start from k = 1 and silently drop any k = 0 structure.
  > The v0.3.0 covariant methods all start from $k = 1$ and silently drop any $k = 0$ structure.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c3805fed21e78e86` [concept] (literature_supported) — Valid covariant method tokens are `cross_ami`, `cross_pami`, `te`, `gcmi`, `pcmci`, and `pcmci_ami`.
  > Valid covariant method tokens are `cross_ami`, `cross_pami`, `te`, `gcmi`, `pcmci`, and `pcmci_ami`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c5395f6d50526fad` [concept] (literature_supported) — The partial autocorrelation function (PACF) gives the partial correlation of a stationary time series with its own lagged values, with the values of the time series at all shorter lags regressed out.
  > the partial autocorrelation function (PACF) gives the partial correlation of a stationary time series with its own lagged values, regressed the values of the time series at all shorter lags
  (documentation, https://en.wikipedia.org/wiki/Partial_autocorrelation_function, published None, independence ind-s-0b00932c0a642b74, corroboration 2)
- `c-d16ac6ee4d080082` [concept] (literature_supported) — The "ywm" method for pacf uses Yule-Walker without adjustment.
  > "ywm", "ywmle" or "yw_mle" : Yule-Walker without adjustment.
  (documentation, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html, published None, independence ind-s-5114732bc45e7988, corroboration 1)
- `c-d282fffb1d0e6096` [concept] (literature_supported) — Another qualitatively different question asks whether an exogenous series co-moves with a target series at the same time step, formalized as I(X_t; Y_t) with k = 0 only.
  > Does $X$ co-move with $Y$ at the **same time step**? $I(X_t\,;\,Y_t)$ $k = 0$ only
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d45f3c78595cbf0f` [concept] (literature_supported) — Mutual information is the expected value of the pointwise mutual information (PMI).
  > MI is the expected value of the pointwise mutual information (PMI).
  (documentation, https://en.wikipedia.org/wiki/Mutual_information, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-d5ab0a27d22108fa` [concept] (literature_supported) — Different fields of study define autocorrelation differently, and not all of these definitions are equivalent.
  > Different fields of study define autocorrelation differently, and not all of these definitions are equivalent.
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-d9bb4a7de9111b5a` [concept] (literature_supported) — The particular surrogate data testing method to be used is directly related to the null hypothesis.
  > The particular surrogate data testing method to be used is directly related to the null hypothesis.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-db6ff7b8686e7abf` [concept] (literature_supported) — The PACF plays an important role in data analysis aimed at identifying the extent of the lag in an autoregressive (AR) model.
  > This function plays an important role in data analysis aimed at identifying the extent of the lag in an autoregressive (AR) model.
  (documentation, https://en.wikipedia.org/wiki/Partial_autocorrelation_function, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-de75e938914f6a9e` [concept] (literature_supported) — For a wide-sense stationary process, the autocorrelation function is an even function of the lag.
  > R X X ⁡ ( τ ) = R X X ⁡ ( − τ ) ̄
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-dfddc1297a6c1ec7` [procedure_step] (literature_supported) — Probabilities in the entropy formula can be estimated using binning, nearest neighbors, or non-uniform embedding approaches.
  > The probabilities in the entropy formula can be estimated using different approaches (binning, nearest neighbors) or, in order to reduce complexity, using a non-uniform embedding.
  (documentation, https://en.wikipedia.org/wiki/Transfer_entropy, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-e68a2c61635926a6` [concept] (literature_supported) — The normalization of autocorrelation has an effect on the statistical properties of the estimated autocorrelations.
  > The normalization is important both because the interpretation of the autocorrelation as a correlation provides a scale-free measure of the strength of statistical dependence, and because the normalization has an effect on the statistical properties of the estimated autocorrelations.
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-e88a0881a9940f09` [interpretation] (literature_supported) — The DPI does not imply that forecastability equals zero; useful transforms may preserve nearly all forecastability.
  > The DPI does not imply that $F(h;\,T(\mathcal{I}_t)) = 0$ is the expected outcome; useful transforms (e.g. log of a multiplicative process) may preserve nearly all forecastability.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 2)
- `c-e90fac75a80b2be3` [concept] (literature_supported) — Autocorrelation quantifies the similarity between observations of a random variable at different points in its domain, commonly time.
  > it quantifies the similarity between observations of a random variable at different points in its domain (commonly, time).
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-e912d8dd6492fd3c` [expectancy] (literature_supported) — Multivariate forms of transfer entropy require more samples than bivariate analysis.
  > although these forms require more samples again.
  (documentation, https://en.wikipedia.org/wiki/Transfer_entropy, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-ea0f41be7f1895c2` [check] (literature_supported) — F8 should be avoided as a causal screening tool because F8 detects predictive dependence, not causal direction.
  > As a causal screening tool: F8 detects predictive dependence, not causal direction.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ea2f36a93e19c413` [concept] (literature_supported) — In statistics, the autocorrelation of a real or complex random process is the Pearson correlation between values of the process at different times, as a function of the two times or of the time lag.
  > In statistics, the autocorrelation of a real or complex random process is the Pearson correlation between values of the process at different times, as a function of the two times or of the time lag.
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-ea93c90fff40faf1` [concept] (literature_supported) — Random Shuffle permutations guarantee the same amplitude distribution as the original series but destroy any temporal correlation that may have been in the original data.
  > The permutations guarantee the same amplitude distribution as the original series, but destroy any temporal correlation that may have been in the original data.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-ead06d4bf650829a` [concept] (literature_supported) — In surrogate data testing with continuous mappings (fluxes), linearity of system means that it can be expressed by a linear differential equation.
  > In case of fluxes (continuous mappings), linearity of system means that it can be expressed by a linear differential equation.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-eae5ef3095e7da5f` [concept] (literature_supported) — Algorithms to generate surrogate data are usually classified into two groups: typical realizations and constrained realizations.
  > They are usually classified in two groups: Typical realizations: data series are generated as outputs of a well-fitted model to the original data. Constrained realizations: data series are created directly from original data, generally by some suitable transformation of it.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-ebd6d790321f0cbd` [concept] (literature_supported) — Mutual information of two random variables is a measure of the mutual dependence between the two variables.
  > the mutual information (MI) of two random variables is a measure of the mutual dependence between the two variables.
  (documentation, https://en.wikipedia.org/wiki/Mutual_information, published None, independence ind-s-0b00932c0a642b74, corroboration 3)
- `c-ec0d9d4d3803484c` [concept] (literature_supported) — Mutual information is equal to zero if and only if two random variables are independent.
  > the mutual information (MI) of two random variables is a measure of the mutual dependence between the two variables.
  (documentation, https://en.wikipedia.org/wiki/Mutual_information, published None, independence ind-s-0b00932c0a642b74, corroboration 2)
- `c-ece84f6282e09c12` [procedure_step] (literature_supported) — F8 should be used when one needs a principled multiple-testing correction to control false positives across many candidate drivers.
  > When you need a principled multiple-testing correction to control false positives across many candidate drivers.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-efc8b9b9d125f15d` [concept] (literature_supported) — pAMI is a nonlinear analog of PACF and represents direct dependence after conditioning on intermediate lags.
  > Nonlinear analog of PACF (direct dependence after conditioning on intermediate lags).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f1603b681e8129dc` [concept] (literature_supported) — For a wide-sense stationary process, the autocorrelation at any lag is less than or equal to the autocorrelation at zero lag.
  > For a WSS process: R X X ⁡ ( τ ) ≤ R X X ⁡ ( 0 )
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-f220f92c01a374f1` [interpretation] (literature_supported) — Yule-Walker (adjusted) and Levinson-Durbin (adjusted) performed consistently worse than other pacf options.
  > Yule-Walker (adjusted) and Levinson-Durbin (adjusted) performed consistently worse than the other options.
  (documentation, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html, published None, independence ind-s-5114732bc45e7988, corroboration 1)
- `c-f227f2ced8316a0d` [concept] (literature_supported) — Surrogate data testing is a statistical proof by contradiction technique similar to permutation tests and parametric bootstrapping.
  > Surrogate data testing (or the method of surrogate data) is a statistical proof by contradiction technique similar to permutation tests and parametric bootstrapping.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-f24808efaf8ae705` [procedure_step] (literature_supported) — Algorithm 2 (AAFT) consists of scaling the data to a Gaussian distribution, performing a RP transformation of the new data, and finally doing a transformation inverse of the first one.
  > This method consists of these steps: Scaling the data to a Gaussian distribution (Gaussianization). Performing a RP transformation of the new data. Finally doing a transformation inverse of the first one (de-Gaussianization).
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-f4f0cb26f9268851` [representation] (literature_supported) — The ccf at index k is the correlation between {x[k], x[k+1], ..., x[n]} and {y[0], y[1], ..., y[m-k]], where n and m are the lengths of x and y.
  > the element at index k is the correlation between {x[k], x[k+1], ..., x[n]} and {y[0], y[1], ..., y[m-k]}, where n and m are the lengths of x and y, respectively.
  (documentation, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.ccf.html, published None, independence ind-s-5114732bc45e7988, corroboration 1)
- `c-f708a2e9c5495ce8` [concept] (literature_supported) — Various time series models incorporate autocorrelation, such as unit root processes, trend-stationary processes, autoregressive processes, and moving average processes.
  > Various time series models incorporate autocorrelation, such as unit root processes, trend-stationary processes, autoregressive processes, and moving average processes.
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-f83dfc039951a7bd` [concept] (literature_supported) — The partial autocorrelation of an AR(p) process is zero at lags greater than p.
  > the partial autocorrelation of an AR(p) process is zero at lags greater than p
  (documentation, https://en.wikipedia.org/wiki/Partial_autocorrelation_function, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-fb8bb79edf998d12` [procedure_step] (literature_supported) — For jointly continuous random variables, mutual information is calculated using a double integral with joint and marginal probability density functions.
  > In the case of jointly continuous random variables, the double sum is replaced by a double integral: I ⁡ ( X ; Y ) = ∫ Y ∫ X P ( X , Y ) ( x , y ) log ⁡ ( P ( X , Y ) ( x , y ) P X ( x ) P Y ( y ) ) d x d y
  (documentation, https://en.wikipedia.org/wiki/Mutual_information, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-fbb3665e38da1699` [representation] (literature_supported) — Mutual information can be expressed as H(X) minus H(X|Y), which equals H(Y) minus H(Y|X), which equals H(X) plus H(Y) minus H(X,Y).
  > Mutual information can be equivalently expressed as: I ⁡ ( X ; Y ) ≡ H ( X ) − H ( X ∣ Y ) ≡ H ( Y ) − H ( Y ∣ X ) ≡ H ( X ) + H ( Y ) − H ( X , Y )
  (documentation, https://en.wikipedia.org/wiki/Mutual_information, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-fe502693a5ec02a0` [failure_mode] (literature_supported) — A drawback of Algorithm 2 (AAFT) is that the last step changes somewhat the linear structure.
  > The drawback of this method is precisely that the last step changes somewhat the linear structure.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 2)
- `c-fe5bd80faf0d6a68` [concept] (literature_supported) — Constrained realizations are created directly from original data, generally by some suitable transformation of it.
  > Constrained realizations: data series are created directly from original data, generally by some suitable transformation of it.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 2)
- `c-fec1351803645fcd` [concept] (literature_supported) — Algorithm 2 or AAFT (Amplitude Adjusted Fourier Transform) tries to preserve both the linear structure and the amplitude distribution.
  > Algorithm 2, or AAFT (for Amplitude Adjusted Fourier Transform): This method has approximately the advantages of the two previous ones: it tries to preserve both the linear structure and the amplitude distribution.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)

### Synthetic / rejected claims

- `c-020e805430b697e9` [concept] (synthetic_extrapolation) — Mutual information is non-negative. (no located evidence)
- `c-02481ad484d1f226` [concept] (synthetic_extrapolation) — pAMI asks how much extra lag information remains after closer target history is linearly residualized, and it is a practical residual diagnostic, not exact nonlinear conditional mutual information and not causal proof. (no located evidence)
- `c-06c398caf130e012` [interpretation] (synthetic_extrapolation) — Mutual information represents the amount of uncertainty in Y which is removed by knowing X. (no located evidence)
- `c-06f03fafedc5fa53` [concept] (synthetic_extrapolation) — Higher mutual information values indicate higher dependency between random variables. (no located evidence)
- `c-09e9a09e40794de5` [procedure_step] (synthetic_extrapolation) — For jointly discrete random variables, mutual information is calculated as a double sum over the joint probability mass function divided by the product of marginal probability mass functions. (no located evidence)
- `c-0a0a67469611bd31` [norm] (synthetic_extrapolation) — Causal methods should not be interpreted as a complete causal proof. (no located evidence)
- `c-106313592be0268d` [concept] (synthetic_extrapolation) — The autocorrelation matrix is a positive semidefinite matrix. (no located evidence)
- `c-140779616979ce1e` [concept] (synthetic_extrapolation) — Mutual information is equal to zero precisely when the joint distribution coincides with the product of the marginals, that is, when X and Y are independent. (no located evidence)
- `c-1a95785ffb535ef0` [concept] (synthetic_extrapolation) — When adjusted is False, the denominator for cross-covariance is n. (no located evidence)
- `c-2d9b3f7851cba5f5` [interpretation] (synthetic_extrapolation) — If X and Y are independent, then knowing X does not give any information about Y and vice versa, so their mutual information is zero. (no located evidence)
- `c-2f045a1fe63b6244` [rationale] (synthetic_extrapolation) — For the quadratic nonlinear coupling, the covariance between driver and target is exactly zero at the population level because the odd central moment of any zero-mean symmetric distribution is zero.
  > Quadratic**: $\mathrm{Cov}(X,\, X^2 - \sigma^2) = \mathbb{E}[X^3] = 0$. The odd central moment of any zero-mean symmetric distribution is zero.
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md)
- `c-335df33f3b66b422` [concept] (synthetic_extrapolation) — The value of the autocorrelation coefficient must lie in the range of negative one to one, with one indicating perfect correlation and negative one indicating perfect anti-correlation. (no located evidence)
- `c-390705077d98c695` [rationale] (synthetic_extrapolation) — Because mutual information is non-negative, H(X) is greater than or equal to H(X|Y). (no located evidence)
- `c-42a027d680297fad` [rationale] (synthetic_extrapolation) — Using Jensen's inequality on the definition of mutual information, one can show that mutual information is non-negative. (no located evidence)
- `c-49214c2cbc0ebc3c` [norm] (synthetic_extrapolation) — known_future_drivers should only be used for variables whose contemporaneous future values are genuinely known at prediction time, such as calendar flags, planned promotions, or externally scheduled variables. (no located evidence)
- `c-496b192dca2206fc` [concept] (synthetic_extrapolation) — Transfer entropy is equivalent to conditional mutual information with the history of the influenced variable in the condition. (no located evidence)
- `c-5366372be6b2efc9` [concept] (synthetic_extrapolation) — The autocorrelation of a continuous-time white noise signal has a strong peak at lag zero, represented by a Dirac delta function, and is exactly zero for all other lags. (no located evidence)
- `c-57e57ceccf04932e` [concept] (synthetic_extrapolation) — pAMI approximates conditional mutual information via linear or optional RF residualisation rather than by exact conditional MI estimation. (no located evidence)
- `c-585bf3d0e0a3ad74` [concept] (synthetic_extrapolation) — CrosspAMI asks how much covariate signal remains after accounting for target history, and it is a linear-residual approximation. (no located evidence)
- `c-6d4dd809e283f7a2` [concept] (synthetic_extrapolation) — CrossAMI asks how much information a covariate lag has about the target, ignoring the target's own history. (no located evidence)
- `c-6e3f8fb5a1eeb1d8` [decision] (synthetic_extrapolation) — Using `pcmci_ami_ci_test="parcorr"` provides a 50-200× speedup over the default `"knn_cmi"` backend. (no located evidence)
- `c-6eeddce902283888` [concept] (synthetic_extrapolation) — Mutual information is symmetric, such that I(X;Y) equals I(Y;X). (no located evidence)
- `c-79bd8a4a3ffb230c` [concept] (synthetic_extrapolation) — Mutual information between two random variables is a non-negative value that measures the dependency between the variables. (no located evidence)
- `c-79cc51ecc7bd4a6b` [concept] (synthetic_extrapolation) — AMI is computed per horizon. (no located evidence)
- `c-7cde858aeb323a35` [strategy] (synthetic_extrapolation) — The `pcmci` and `pcmci_ami` causal methods are optional, computationally expensive, and designed for confirmatory causal screening after a fast pairwise pass, not as a default first step. (no located evidence)
- `c-80c573857a2a5c01` [norm] (synthetic_extrapolation) — A selected_for_tensor=True flag at k = 0 is impossible by default and requires an explicit known_future_drivers opt-in at the use-case layer as an intentional chronological-causality guard. (no located evidence)
- `c-835beb36bad6c6c0` [interpretation] (synthetic_extrapolation) — If X is a deterministic function of Y and Y is a deterministic function of X, then all information conveyed by X is shared with Y and mutual information equals the entropy of Y or X. (no located evidence)
- `c-9289479da6f7db4f` [concept] (synthetic_extrapolation) — For a wide-sense stationary process, the autocovariance function depends only on the lag between the two time points, not on their position in time. (no located evidence)
- `c-9c7fe3e4e853456c` [rationale] (synthetic_extrapolation) — For the abs-value nonlinear coupling, the covariance between driver and target is exactly zero at the population level because |X| |X| is an odd function.
  > Abs-value**: $\mathrm{Cov}(X,\, X ) = \mathbb{E}[X \cdot X ] = 0$. The function $X X $ is odd, so its expectation over any symmetric distribution is zero.
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md)
- `c-bae6d35b4c3a3e9d` [concept] (synthetic_extrapolation) — Transfer entropy has been extended to multivariate forms by conditioning on other potential source variables or considering transfer from a collection of sources. (no located evidence)
- `c-bf73365386ec590a` [concept] (synthetic_extrapolation) — For a wide-sense stationary process, the mean and variance are time-independent. (no located evidence)
- `c-c191a7b80f4c50a9` [interpretation] (synthetic_extrapolation) — H(Y|X) represents the amount of uncertainty remaining about Y after X is known. (no located evidence)
- `c-c670e706213fb109` [mental_model] (synthetic_extrapolation) — If entropy H(Y) is a measure of uncertainty about a random variable, then H(Y|X) is a measure of what X does not say about Y. (no located evidence)
- `c-c8eccfb6c33cee31` [concept] (synthetic_extrapolation) — AMI asks how much information the target's own past contains about its future at each lag. (no located evidence)
- `c-c9be3a5f8632f1f9` [concept] (synthetic_extrapolation) — Mutual information is more general than the correlation coefficient and is not limited to real-valued random variables and linear dependence. (no located evidence)
- `c-d72197202d602bbc` [concept] (synthetic_extrapolation) — The Wiener-Khinchin theorem relates the autocorrelation function to the power spectral density via the Fourier transform. (no located evidence)
- `c-e2d80cdbcf044fd5` [procedure_step] (synthetic_extrapolation) — The surrogate data testing technique involves specifying a null hypothesis describing a linear process and then generating several surrogate data sets according to that hypothesis using Monte Carlo methods. (no located evidence)
- `c-ec831b0673dcb592` [strategy] (synthetic_extrapolation) — For fast initial screening in covariant analysis, one should prefer `methods=["cross_ami", "gcmi"]`. (no located evidence)
- `c-eefe98fdacf76abc` [concept] (synthetic_extrapolation) — The autocorrelation matrix is an n by n matrix containing as elements the autocorrelations of all pairs of elements of a random vector. (no located evidence)
- `c-f11aff18a9c4b01c` [mental_model] (synthetic_extrapolation) — Intuitively, mutual information measures the information that X and Y share, or how much knowing one of these variables reduces uncertainty about the other. (no located evidence)
- `c-f71117531023b963` [concept] (synthetic_extrapolation) — Mutual information is a measure of the price for encoding (X, Y) as a pair of independent random variables when in reality they are not. (no located evidence)
- `c-fbf82d831806cdb6` [expectancy] (synthetic_extrapolation) — In theory, pAMI is less than or equal to AMI. (no located evidence)

### UNKNOWN / thin / unverified / unexamined slots

- none

## Area: Toolkit Installation and Setup

### Supported claims

- `c-01c4b80fcb469119` [concept] (literature_supported) — TimeSeriesSplit has a gap parameter that specifies the number of samples to exclude from the end of each train set before the test set.
  > gapint, default=0 Number of samples to exclude from the end of each train set before the test set.
  (documentation, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, published None, independence ind-s-ca7d54da5b087ed3, corroboration 1)
- `c-0809c56c56c402e8` [concept] (literature_supported) — The triage namespace in src/forecastability/triage/__init__.py is public and contains batch models, readiness helpers, events, bundle types, and triage-specific diagnostics.
  > Advanced triage namespace for batch models, readiness helpers, events, bundle types, and triage-specific diagnostics Public
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0c2606ffcdd0c17e` [concept] (literature_supported) — The core forecastability package has no import-time or runtime dependencies on Darts, MLForecast, StatsForecast, Nixtla, or similar forecasting libraries.
  > The core `forecastability` package has no import-time or runtime dependencies on Darts, MLForecast, StatsForecast, Nixtla, or similar forecasting libraries; any such extras and comparisons are optional and live in the separate `forecastability-examples` repository.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0ce6297954840ce0` [concept] (literature_supported) — src/forecastability/adapters/ contains transport, runtime, agent, checkpoint, and presentation adapters including CLI, API, dashboard, and MCP server implementations.
  > `cli.py`, `api.py`, `dashboard.py`, `mcp_server.py`, `settings.py`, `event_emitter.py`, `checkpoint.py`, `result_bundle_io.py`, `triage_presenter.py`, `agents/`, `llm/` Transport, runtime, agent, checkpoint, and presentation adapters
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-1a78c8e932db48e4` [concept] (literature_supported) — The top-level package facade in src/forecastability/__init__.py re-exports run_triage, run_batch_triage, analyzers, config models, result models, dataset helpers, scorer registry, and validation.
  > Top-level package facade with re-exports for `run_triage`, `run_batch_triage`, analyzers, config models, result models, dataset helpers, scorer registry, and validation
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-1f81e1f51c21c73f` [concept] (literature_supported) — The bootstrap package contains bootstrap helpers such as output directory setup.
  > Bootstrap helpers such as output directory setup
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-1fbeed60f4a9777d` [norm] (literature_supported) — Development and CI run on macOS and Linux, and Windows path handling, line endings, and subprocess behaviour have not been systematically tested.
  > Development and CI run on macOS and Linux. Windows path handling, line endings, and subprocess behaviour have not been systematically tested.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-1fd49d0c0a3c73c7` [concept] (literature_supported) — The mutual_info_regression function relies on nonparametric methods based on entropy estimation from k-nearest neighbors distances.
  > The function relies on nonparametric methods based on entropy estimation from k-nearest neighbors distances as described in [2] and [3].
  (documentation, https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.mutual_info_regression.html, published None, independence ind-s-ca7d54da5b087ed3, corroboration 1)
- `c-235ff9798ec38d98` [concept] (literature_supported) — The live codebase is not a flat module layout anymore, and the supported public surfaces are the package facades plus the declared runtime entry points.
  > the live codebase is not a flat module layout anymore, and the supported public surfaces are the package facades plus the declared runtime entry points.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-2ca293993e13f245` [strategy] (literature_supported) — After following the canonical notebook path walkthroughs, the `notebooks/triage/` notebooks should be used for deep dives, not as first-stop onboarding.
  > Use the `notebooks/triage/` notebooks only after the walkthroughs; they are deep dives, not first-stop onboarding.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-2d259e1a6347850a` [concept] (literature_supported) — The toolkit is not another forecasting library.
  > It is **not another forecasting library**.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3e111866d9a035a4` [concept] (literature_supported) — The pacf function calculates the partial autocorrelation estimate for observations of a time series.
  > This repository is a deterministic forecastability triage toolkit for time series.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 2)
- `c-4f7df5b9dd43919c` [mental_model] (literature_supported) — The live repository architecture is layered but pragmatic in its organization.
  > The live repository is layered, but it is also pragmatic
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-51973c28cbed8096` [concept] (literature_supported) — adapters/api.py exposes the FastAPI application at forecastability.adapters.api:app.
  > `adapters/api.py` exposes the FastAPI application at `forecastability.adapters.api:app`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5783b70591071f9b` [concept] (literature_supported) — The triage package contains triage-domain models, readiness and router logic, diagnostic result types, events, and result bundles.
  > Triage-domain models, readiness/router logic, diagnostic result types, events, and result bundles
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-57e4ae60f4475fe4` [procedure_step] (literature_supported) — To sync the local environment when working in the repository, run `uv sync`.
  > If you are working in the repository, sync the local environment. uv sync
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5c8d2e21672cffc3` [concept] (literature_supported) — The HTTP API exposes `GET /health`, `GET /scorers`, `POST /triage`, and `GET /triage/stream` endpoints.
  > The HTTP API exposes `GET /health`, `GET /scorers`, `POST /triage`, and `GET /triage/stream`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-632cedcf139eff2c` [concept] (literature_supported) — CLI, API, scripts, MCP, and agents are optional access or narration layers around the same deterministic outputs.
  > CLI, API, scripts, MCP, and agents are optional access or narration layers around the same deterministic outputs.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-69f30db994f8b794` [concept] (literature_supported) — If nlags is not provided to the pacf function, it uses min(10 * np.log10(nobs), nobs // 2 - 1) as the default value.
  > If not provided, uses min(10 * np.log10(nobs), nobs // 2 - 1).
  (documentation, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html, published None, independence ind-s-5114732bc45e7988, corroboration 1)
- `c-6a1a40e3376b9f4f` [cue] (literature_supported) — The stable facade should be preferred, specifically `forecastability` and `forecastability.triage`.
  > Use the stable facade first: prefer `forecastability` and `forecastability.triage`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6ccb4c89f47d7cb2` [expectancy] (literature_supported) — The internal packages, the MCP surface, and the agent layer are useful only after the deterministic workflow is already understood.
  > The internal packages, the MCP surface, and the agent layer are useful only after the deterministic workflow is already understood.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-71f952482b8d957c` [concept] (literature_supported) — The CLI supports `triage`, `triage-batch`, and `list-scorers` commands.
  > The CLI supports `triage`, `triage-batch`, and `list-scorers`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-76c6bc37bc29ed95` [concept] (literature_supported) — The toolkit does not replace downstream forecasting libraries such as Darts, MLForecast, StatsForecast, Nixtla, Prophet, sklearn, or statsmodels.
  > This package does **not** replace downstream forecasting libraries. It does not try to be: - Darts - MLForecast - StatsForecast - Nixtla - Prophet - sklearn - statsmodels
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7afa8fd0d72820f5` [concept] (literature_supported) — src/forecastability/utils/ provides config models, typed result containers, dataset helpers, validation, plotting, reproducibility, and workflow support code.
  > `config.py`, `datasets.py`, `types.py`, `validation.py`, `aggregation.py`, `io_models.py`, `plots.py`, `reproducibility.py`, `robustness.py`, `state.py` Config models, typed result containers, dataset helpers, validation, plotting, reproducibility, and workflow support code
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7b33637f32110660` [concept] (literature_supported) — The package is a deterministic pre-model diagnostic layer, not a downstream model-training or forecasting library.
  > This package is a deterministic pre-model diagnostic layer, not a downstream model-training or forecasting library.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7dbdb2e6d8461199` [concept] (literature_supported) — The utils package contains config models, typed containers, datasets, validation, plotting, and repository workflow support.
  > Config models, typed containers, datasets, validation, plotting, and repo workflow support
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7f7e4e484f073d63` [concept] (literature_supported) — The toolkit supports Python versions 3.11 and 3.12.
  > Supported Python versions: Python 3.11, 3.12
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-805080c1dca07fc6` [rationale] (literature_supported) — The core package produces deterministic evidence while the examples repository shows how to translate that evidence into framework-specific modeling recipes.
  > That split is intentional: the core package produces deterministic evidence; the examples repository shows how to translate that evidence into framework-specific modeling recipes.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8081d0aa9175a9e4` [concept] (literature_supported) — The adapters package includes CLI, dashboard, API, MCP, agent, settings, event, checkpoint, and presenter adapters.
  > CLI, dashboard, API, MCP, agent, settings, event, checkpoint, and presenter adapters
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-84dca4786db212fa` [concept] (literature_supported) — The test_size parameter in TimeSeriesSplit defaults to n_samples // (n_splits + 1), which is the maximum allowed value with gap=0.
  > Defaults to n_samples // (n_splits + 1), which is the maximum allowed value with gap=0.
  (documentation, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, published None, independence ind-s-ca7d54da5b087ed3, corroboration 1)
- `c-87434ff1844dd684` [norm] (literature_supported) — The MCP server requires additional server-framework dependencies and is not included in the default install.
  > The MCP server requires additional server-framework dependencies. It is not included in the default install.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-900c293e8a02e709` [procedure_step] (literature_supported) — HTTP API, dashboard, and transport surfaces can be installed via the 'transport' extra.
  > HTTP API, dashboard, and transport surfaces pip install "dependence-forecastability[transport]"
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-9231df45bc566169` [norm] (literature_supported) — The supported import surface for the package is the package facade, not the internal tree.
  > The supported import surface is the package facade, not the internal tree.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-926bd16a66d508cc` [concept] (literature_supported) — The dashboard is a thin browser UI over the deterministic adapters.
  > The dashboard is a thin browser UI over the deterministic adapters.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-9e387ffad4c22948` [strategy] (literature_supported) — Most users only need three things in order: the package facade, the notebook path in the forecastability-examples sibling repository, and the maintainer scripts.
  > Most users only need three things in order: 1. The package facade in [../public_api.md](../public_api.md). 2. The notebook path in the [forecastability-examples](https://github.com/AdamKrysztopa/forecastability-examples) sibling repository - see [docs/examples_index.md](../examples_index.md) for the full index. 3. The maintainer scripts documented in [../maintenance/developer_guide.md](../maintenance/developer_guide.md) when they need repo workflows.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-b87313eb035ad280` [concept] (literature_supported) — src/forecastability/bootstrap/output_dirs.py provides bootstrap helpers for output directory management.
  > Bootstrap helpers for output directory management
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ba77cf4477c5b7e5` [procedure_step] (literature_supported) — Agent-facing narration surfaces can be installed via the 'agent' extra.
  > Agent-facing narration surfaces pip install "dependence-forecastability[agent]"
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-bea4138eb4aaf4a3` [mental_model] (literature_supported) — The package is organized in layers with a small stable import facade and an internal tree organized by role including triage domain, use cases, analyzer pipeline, metrics, diagnostics, reporting, utils, adapters, services, ports, and bootstrap helpers.
  > The package is layered and subpackage-heavy. The stable import facade is small, but the internal tree is organized by role: triage domain, use cases, analyzer pipeline, metrics, diagnostics, reporting, utils, adapters, services, ports, and bootstrap helpers.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c0c8260b2f550fad` [strategy] (literature_supported) — Users should use the Python package facade `forecastability` when they need deterministic triage, analyzers, typed results, config models, scorer registry access, or batch triage types.
  > Use these facades when you need deterministic triage, analyzers, typed results, config models, scorer registry access, or batch triage types.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c1a6707518f66c66` [strategy] (literature_supported) — The golden path recommends following it before reaching for the CLI, API, dashboard, MCP, or agent layers.
  > Follow this path before you reach for the CLI, API, dashboard, MCP, or agent layers.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d15f7f776bd59267` [norm] (literature_supported) — The toolkit is not uniformly production-ready, with the deterministic core and stable facades being stable while CLI and HTTP API are beta and MCP server and agent layer are experimental.
  > The toolkit is not uniformly production- ready. The deterministic core and stable facades are stable; CLI and HTTP API are beta; MCP server and agent layer are experimental.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d41368bc8903ef51` [rationale] (literature_supported) — TimeSeriesSplit provides train/test indices to split time-ordered data, where other cross-validation methods are inappropriate because they would lead to training on future data and evaluating on past data.
  > Provides train/test indices to split time-ordered data, where other cross-validation methods are inappropriate, as they would lead to training on future data and evaluating on past data.
  (documentation, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, published None, independence ind-s-ca7d54da5b087ed3, corroboration 1)
- `c-d7cf6d34d5a4e2df` [concept] (literature_supported) — The toolkit is a deterministic pre-modeling layer that helps inspect readiness, informative horizons, target lags, seasonality structure, covariate usefulness, leakage risk, and model-family direction before spending time on downstream forecasting libraries.
  > It is a deterministic pre-modeling layer that helps you inspect readiness, informative horizons, target lags, seasonality structure, covariate usefulness, leakage risk, and model-family direction before you spend time on Darts, MLForecast, StatsForecast, Nixtla, sklearn, Prophet, or custom models.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d976fb5fb853a433` [procedure_step] (literature_supported) — To install the dependence-forecastability package from PyPI, run `pip install dependence-forecastability`.
  > If you want the published package surface, install from PyPI. pip install dependence-forecastability
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-dbc891cb0d4ca8bc` [concept] (literature_supported) — The dependence-forecastability toolkit does not train forecasting models.
  > It does not train forecasting models. It asks what a model should be allowed to see: which target lags carry memory, which covariates retain incremental signal, which lagged features are legal for the forecast horizon, and what evidence should travel into downstream model configuration.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e08a3a32780819a6` [concept] (literature_supported) — The toolkit is a deterministic forecastability triage toolkit for time series.
  > This repository is a deterministic forecastability triage toolkit for time series.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e54e2ceaa0a6696c` [norm] (literature_supported) — `docs/public_api.md` should be treated as the supported import contract.
  > Treat `docs/public_api.md` as the supported import contract.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ec9a09f50d5ca59c` [concept] (literature_supported) — adapters/mcp_server.py contains the experimental MCP surface.
  > `adapters/mcp_server.py` contains the experimental MCP surface.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f03d7fb95d9733f6` [concept] (literature_supported) — TimeSeriesSplit has a test_size parameter that is used to limit the size of the test set.
  > test_sizeint, default=None Used to limit the size of the test set.
  (documentation, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, published None, independence ind-s-ca7d54da5b087ed3, corroboration 1)
- `c-f427ee7ff79686bc` [procedure_step] (literature_supported) — Holiday calendar features in ForecastPrepContract can be installed via the 'calendar' extra.
  > Holiday calendar features in ForecastPrepContract pip install "dependence-forecastability[calendar]"
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f9340e01bd68268b` [concept] (literature_supported) — The stable public contract for the forecastability toolkit is small, while the internal package tree is deliberately split across triage models, use cases, analyzers, metrics, diagnostics, reporting, utils, adapters, services, ports, and bootstrap helpers.
  > the stable public contract is small, while the internal package tree is deliberately split across triage models, use cases, analyzers, metrics, diagnostics, reporting, utils, adapters, services, ports, and bootstrap helpers.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-fd9b19f184ed57c2` [concept] (literature_supported) — The ccf function accepts x and y as array-like time series data to use in the calculation.
  > x, yarray_likeThe time series data to use in the calculation.
  (documentation, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.ccf.html, published None, independence ind-s-5114732bc45e7988, corroboration 1)

### Synthetic / rejected claims

- `c-230469652471d5dc` [concept] (synthetic_extrapolation) — Everything else in src/forecastability/ exists to support the public facades and repository workflows.
  > Everything else in `src/forecastability/` exists to support those facades and repo workflows.
  (verdict insufficient [connective_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md)
- `c-2cbe28a7f352624e` [concept] (synthetic_extrapolation) — CLI, dashboard, and HTTP API remain transport layers over the same deterministic core. (no located evidence)
- `c-684ea789c843f3fd` [concept] (synthetic_extrapolation) — adapters/cli.py implements the forecastability command. (no located evidence)
- `c-7166a16b12a2748f` [prerequisite] (synthetic_extrapolation) — Python 3.11+ is required, as the codebase uses 3.11-specific syntax and type features, and earlier Python versions are not supported and will produce parse errors. (no located evidence)
- `c-79f10b9e9bd162e5` [procedure_step] (synthetic_extrapolation) — The [agent] extras (PydanticAI) and [api] extras (FastAPI + uvicorn) each add transitive packages, and in constrained environments you should install only the extras you need. (no located evidence)
- `c-85805e8db94b3db2` [concept] (synthetic_extrapolation) — External users should anchor on the stable public facades and entrypoints, which include the stable package facade at src/forecastability/__init__.py, the advanced triage namespace at src/forecastability/triage/__init__.py, the CLI command at forecastability.adapters.cli:main, the dashboard command at forecastability.adapters.dashboard:main, and the HTTP API at forecastability.adapters.api:app. (no located evidence)
- `c-888b448ed753b231` [procedure_step] (synthetic_extrapolation) — The kNN MI estimator with k=8 as default is used to implement AMI. (no located evidence)
- `c-9da277efb2f0f6de` [concept] (synthetic_extrapolation) — The toolkit should be applied before model selection to answer whether a time series contains exploitable structure and what a forecasting model should be allowed to use. (no located evidence)
- `c-a367df0fa8cd8f6f` [procedure_step] (synthetic_extrapolation) — The CSV adapter drops missing values column-wise and skips too-short or non-numeric series conservatively instead of forcing a partial analysis. (no located evidence)
- `c-b62d54d7bc6cb152` [prerequisite] (synthetic_extrapolation) — The causal extra must be installed when causal discovery methods are needed. (no located evidence)
- `c-d070f6ad9f793137` [procedure_step] (synthetic_extrapolation) — Optional causal screening methods such as PCMCI and PCMCI-AMI can be installed via the 'causal' extra.
  > Causal screening methods such as PCMCI / PCMCI-AMI pip install "dependence-forecastability[causal]"
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md)
- `c-d5753115d7014f4b` [concept] (synthetic_extrapolation) — adapters/dashboard.py implements the forecastability-dashboard command. (no located evidence)

### UNKNOWN / thin / unverified / unexamined slots

- none

## Area: Interpreting Forecastability Results

### Supported claims

- `c-0053ecfeef6b8786` [interpretation] (literature_supported) — A tensor_role of "diagnostic" indicates a lag is useful for understanding the system but is not eligible as a tensor feature.
  > `"diagnostic"` Useful for understanding the system; **not** eligible as a tensor feature
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-02471dfd7d502aa5` [cue] (literature_supported) — Triage is not a replacement for full backtesting or deployment validation.
  > Not a replacement for full backtesting or deployment validation
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0389d4b5eaef3a19` [check] (literature_supported) — F6 should be avoided as a sole decision-maker because F6 is a complementary contextual tool, not a forecastability measure, and the forecastability ceiling is set by AMI, not entropy.
  > As a sole decision-maker: F6 is a complementary contextual tool, not a forecastability measure. The forecastability ceiling is set by AMI, not entropy.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0570846c99e21039` [expectancy] (literature_supported) — GMDH neural network was found to have better forecasting performance than classical forecasting algorithms such as Single Exponential Smooth, Double Exponential Smooth, ARIMA and back-propagation neural network.
  > For example, GMDH neural network was found to have better forecasting performance than the classical forecasting algorithms such as Single Exponential Smooth, Double Exponential Smooth, ARIMA and back-propagation neural network.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-05db67066fb6179b` [norm] (literature_supported) — LLE (Largest Lyapunov Exponent) is intentionally excluded from the batch triage ranking table (F7) by design.
  > LLE is intentionally excluded from the batch triage ranking table (F7) by design.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-06aa9efd792338b2` [interpretation] (literature_supported) — F4 should be used when a divergence between high AMI and low Ω arises because this pattern signals that predictability comes from nonlinear dynamics, not spectral structure.
  > When a divergence between high AMI and low Ω arises: this pattern signals that predictability comes from nonlinear dynamics, not spectral structure.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-074bbf77d40d49d7` [failure_mode] (literature_supported) — Directness can be numerically unstable when raw dependence is close to zero, and in this slice, 6 out of 7 cases have warning horizons and at least one directness_ratio greater than 1.0, which should be treated as an estimation warning rather than scientific evidence.
  > directness can be numerically unstable when raw dependence is close to zero. In this slice, 6/7 cases have warning horizons and at least one `directness_ratio > 1.0`, which should be treated as an estimation warning, not scientific evidence of stronger conditioned dependence.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-07e983f3df1aeb65` [expectancy] (literature_supported) — Batch diagnostic ranking (F7) provides objective multi-criteria ranking across an entire signal portfolio.
  > Objective multi-criteria ranking across an entire signal portfolio
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0869da46b065ba5c` [check] (literature_supported) — False confidence from one backend should be mitigated by requiring cross-backend agreement before acting on lag recommendations.
  > False confidence from one backend decision changes when backend changes model class mismatch or noisy data require cross-backend agreement before acting on lag recommendations
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-092f61b7d4a02c80` [expectancy] (literature_supported) — Studies have shown that extrapolations are the least accurate forecasting methods, while company earnings forecasts are the most reliable.
  > Studies have shown that extrapolations are the least accurate, while company earnings forecasts are the most reliable.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-10e496fcc72af849` [expectancy] (literature_supported) — With the known_future_drivers opt-in, k=0 rows for that driver flip to tensor_role="known_future" and the selector may choose selected_for_tensor=True at k=0 for that driver only.
  > With the opt-in, those rows flip to `tensor_role="known_future"` and the selector may choose `selected_for_tensor=True` at $k=0$ for that driver only.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-158a4fdd8d172445` [concept] (literature_supported) — When alpha is provided to pacf, confidence intervals for the given level are returned with standard deviation computed according to 1/sqrt(len(x)).
  > If a number is given, the confidence intervals for the given level are returned. For instance if alpha=.05, 95 % confidence intervals are returned where the standard deviation is computed according to 1/sqrt(len(x)).
  (documentation, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html, published None, independence ind-s-5114732bc45e7988, corroboration 1)
- `c-176cff9ac653373b` [check] (literature_supported) — Short-sample fragility should be mitigated by enforcing minimum length and inspecting stress table stability.
  > Short-sample fragility large backend deltas on small fractions insufficient support for residualization enforce minimum length and inspect stress table stability
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-17a95fd8c5103a99` [cue] (literature_supported) — Exogenous screening with FDR (F8) uses greedy forward selection and redundancy penalty is configurable approximation.
  > Greedy forward selection; redundancy penalty is configurable approximation
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-18e07021271d95c1` [interpretation] (literature_supported) — A lag_role of "predictive" indicates k ≥ 1 and represents fixed-lag predictive association that is covariant-informative.
  > `"predictive"` $k \ge 1$ Fixed-lag predictive association - covariant-informative
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-195d659856d7237b` [expectancy] (literature_supported) — Largest Lyapunov exponent (F5) differentiates deterministic chaos from stochastic noise when sample size permits.
  > Differentiates deterministic chaos from stochastic noise (when sample size permits)
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-1c00edaea9f68485` [procedure_step] (literature_supported) — Plotting the partial autocorrelation function and drawing the lines of the confidence interval is a common way to analyze the order of an AR model.
  > Plotting the partial autocorrelation function and drawing the lines of the confidence interval is a common way to analyze the order of an AR model.
  (documentation, https://en.wikipedia.org/wiki/Partial_autocorrelation_function, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-1e3de571e58b5ba5` [failure_mode] (literature_supported) — Short-sample fragility occurs when large backend deltas appear on small fractions due to insufficient support for residualization.
  > Short-sample fragility large backend deltas on small fractions insufficient support for residualization
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-1e7a254fa6826dc0` [procedure_step] (literature_supported) — F2 should be used when one wants to know why AMI is low, as limit compression reveals whether the ceiling is genuinely low or whether the sampled curve has not saturated the limit.
  > When you want to know *why* AMI is low - limit compression reveals whether the ceiling is genuinely low (hard limit) or whether the sampled curve has not saturated the limit.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-1f011e82a7a76c5a` [expectancy] (literature_supported) — If the factors that relate to what is being forecast are known and well understood and there is a significant amount of data available, the final value will likely be close to the forecast.
  > If the factors that relate to what is being forecast are known and well understood and there is a significant amount of data that can be used, it is likely the final value will be close to the forecast.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-26da63a40cb4a204` [strategy] (literature_supported) — Very low directness_ratio in sine_wave (0.0157) and air_passengers (0.0993) supports the use of compact structured models over long-lag complexity.
  > Very low `directness_ratio` in `sine_wave` (0.0157) and `air_passengers` (0.0993) supports compact structured models over long-lag complexity.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-2716a6be49cfd593` [interpretation] (literature_supported) — By default, every k = 0 row gets tensor_role = "diagnostic".
  > By default, every $k = 0$ row gets `tensor_role = "diagnostic"`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-2818fef8c18c9e3d` [norm] (literature_supported) — It is generally considered a good practice to indicate the degree of uncertainty attaching to forecasts.
  > it is generally considered a good practice to indicate the degree of uncertainty attaching to forecasts.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-2923aabaa5421d13` [interpretation] (literature_supported) — The `blocked` field indicates whether triage completed at all.
  > Field What it tells you --- --- `blocked` Whether triage completed at all
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-29f2188e34114c86` [expectancy] (literature_supported) — Predictive info learning curves (F3) avoids over-long or too-short lookback windows.
  > Avoids over-long or too-short lookback windows
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-2af2793623bbe093` [interpretation] (literature_supported) — In the current run, 2 out of 8 univariate series are classified as high forecastability, 1 out of 8 is medium, and 5 out of 8 are low.
  > In the current run, 2/8 series are `forecastability_class=high`, 1/8 is `medium`, and 5/8 are `low`, which supports separating rich-model candidates from baseline-first candidates before model search.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-2e3890693589ca38` [check] (literature_supported) — The profile makes auditing transformation effects straightforward by comparing the values arrays element-wise across two runs.
  > The profile makes this audit straightforward: compare the `values` arrays element-wise across two runs; any lag where the derived profile exceeds the raw profile by more than estimation noise is a data-leakage candidate, not a genuine gain.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-2eaebaa88a212810` [concept] (literature_supported) — The kNN mutual information estimator with n_neighbors=8 is asymptotically consistent but has positive bias for finite samples, particularly at short series lengths and large lag indices.
  > The kNN mutual information estimator (Kraskov et al., 2004; `n_neighbors=8`) is asymptotically consistent but has positive bias for finite samples, particularly at short series lengths and large lag indices.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-32ecea3ca5b4cc35` [concept] (literature_supported) — Budgets are more specific, fixed-term financial plans used for resource allocation and control.
  > budgets are more specific, fixed-term financial plans used for resource allocation and control
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-3407a8b48ab1dafd` [misconception] (literature_supported) — Role thinking - standing in other people's shoes to forecast their decisions - does not contribute to the accuracy of the forecast according to some expert studies.
  > Similarly, experts in some studies argue that role thinking - standing in other people's shoes to forecast their decisions - does not contribute to the accuracy of the forecast.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-358419a21f3f6965` [cue] (literature_supported) — pAMI is a linear approximation to conditional MI that can under-capture nonlinear mediation.
  > Linear approximation to conditional MI; can under-capture nonlinear mediation
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-381051edb34b1411` [interpretation] (literature_supported) — A blocked result means the workflow could not support the requested computation, which is different from no forecastable structure.
  > `blocked` is different from "no forecastable structure." A blocked result means the workflow could not support the requested computation.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3ab6fb302b76f380` [concept] (literature_supported) — A person can become better calibrated, having things they give 10% credence to happening 10% of the time.
  > A person can become better calibrated - i.e. having things they give 10% credence to happening 10% of the time.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 2)
- `c-3f840b5cc33b97a0` [concept] (literature_supported) — For alpha=.05, 95% confidence intervals are returned where the standard deviation is computed according to 1/sqrt(len(x)).
  > For instance if alpha=.05, 95 % confidence intervals are returned where the standard deviation is computed according to 1/sqrt(len(x)).
  (documentation, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.ccf.html, published None, independence ind-s-5114732bc45e7988, corroboration 1)
- `c-41ed49f8bd5add25` [concept] (literature_supported) — The Theoretical Limit Diagnostics (F2) measures the information-theoretic upper bound on forecastability derived from the AMI curve, including compression ratio and predictability ceiling.
  > The information-theoretic upper bound on forecastability derived from the AMI curve, including compression ratio and predictability ceiling, to quantify how close any model can get to the fundamental limit.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-42247942360cffb2` [expectancy] (literature_supported) — A monthly series with strong annual seasonality may have higher forecastability at lag 12 than at lag 5, producing a non-monotone profile with a secondary peak.
  > For example, a monthly series with strong annual seasonality may have $F(12) > F(5)$, producing a non-monotone profile with a secondary peak at $h = 12$.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4805732d6b9f24cb` [cue] (literature_supported) — Permutation entropy is amplitude-blind and a tie-breaking rule must be fixed.
  > PE is amplitude-blind; tie-breaking rule must be fixed
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4a028079c97bc7c6` [failure_mode] (literature_supported) — False confidence from one backend occurs when decision changes when the backend changes, resulting from model class mismatch or noisy data.
  > False confidence from one backend decision changes when backend changes model class mismatch or noisy data
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4c0cd06d6a345f9c` [expectancy] (literature_supported) — Exogenous screening with FDR (F8) prunes redundant drivers and controls false discovery rate across many tests.
  > Prunes redundant drivers; controls false discovery rate across many tests
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4c37d3e8ec91ecac` [cue] (literature_supported) — IT limit diagnostics (F2) ceiling holds under log loss only and exploitation ratio is deferred.
  > Ceiling holds under log loss only; exploitation ratio deferred (pre-model repo)
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4d6032307c7e5be5` [cue] (literature_supported) — Forecastability profile (F1) inherits AMI estimator reliability and requires surrogates for epsilon anchoring.
  > Inherits AMI estimator reliability; requires surrogates for epsilon anchoring
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4ded063d84bc4156` [prerequisite] (literature_supported) — A minimum recommended series length of approximately n ≥ 3 × H_max is required, where H_max is the maximum evaluation horizon, because below this threshold MI estimates are unreliable for lags close to H_max.
  > Approximately $n \geq 3 \times H_{\max}$, where $H_{\max}$ is the maximum evaluation horizon. Below this threshold, MI estimates are unreliable for lags close to $H_{\max}$.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4e3b8d45c8106175` [concept] (literature_supported) — Forecasting can be described as predicting what the future will look like, whereas planning predicts what the future should look like.
  > Forecasting can be described as predicting what the future will look like, whereas planning predicts what the future should look like.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-4e3fb057fc905e57` [cue] (literature_supported) — When directness_ratio exceeds 1.0, the system flags arch_suspected, and this flag is a warning or anomaly boundary rather than positive evidence of any particular architecture.
  > When `directness_ratio > 1.0` the system flags `arch_suspected`. This flag is a **warning or anomaly boundary, not positive evidence** of any particular architecture.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4e9e5cf8350c9095` [procedure_step] (literature_supported) — When alpha is a number, confidence intervals for the given level are returned.
  > If a number is given, the confidence intervals for the given level are returned.
  (documentation, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.ccf.html, published None, independence ind-s-5114732bc45e7988, corroboration 1)
- `c-50d2c881f5896b3c` [expectancy] (literature_supported) — Seasonal and quasi-periodic processes routinely exhibit higher AMI at seasonal lags than at short lags.
  > Seasonal and quasi-periodic processes routinely exhibit higher AMI at seasonal lags than at short lags.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-55451c295b59e8c7` [norm] (literature_supported) — Largest Lyapunov exponent is experimental and excluded from automated triage decisions.
  > Largest Lyapunov exponent is experimental and excluded from automated triage decisions.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5588f848981103c4` [norm] (literature_supported) — A True value for is_non_monotone is correct and expected for seasonal series, not an estimation artefact or an error.
  > Do not treat a `True` value as an estimation artefact or an error - it is correct and expected for seasonal series.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5ae8a57e691e2b17` [interpretation] (literature_supported) — Positive Transfer Entropy indicates added predictive information from source history beyond target-only history.
  > Positive TE indicates added predictive information from source history beyond target-only history.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5b6586a9ad5e83ab` [failure_mode] (literature_supported) — Numerical inflation occurs when directness_ratio exceeds 1.0 due to estimator instability or finite-sample effects.
  > Numerical inflation `directness_ratio > 1.0` estimator instability, finite-sample effects
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5d3c43042ccb35ba` [concept] (literature_supported) — Phase-randomized FFT surrogates preserve the power spectrum.
  > Phase-randomized FFT surrogates preserve the power spectrum.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5deb21fa99d6290f` [prerequisite] (literature_supported) — Reliable phase-space coverage for Largest Lyapunov Exponent requires n ≫ 10^m, which for the default m = 3 means n ≫ 1000, and results for shorter series are indicative only.
  > Reliable phase-space coverage requires $n \gg 10^m$. For the default $m = 3$ this means $n \gg 1000$. Results for shorter series are indicative only.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-66bff2d55ca8d0f0` [representation] (literature_supported) — The selector emits LaggedExogSelectionRow objects independently from plot artifacts; the sparse map is a typed Python output first.
  > The selector emits `LaggedExogSelectionRow` objects independently from plot artifacts; the sparse map is a typed Python output first.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-672eba057b35b6b7` [strategy] (literature_supported) — For surrogate bands, the upper band is operationally informative for detecting non-null dependence while the lower band is usually near zero for MI and is not typically operationally useful.
  > The upper band is operationally informative for detecting non-null dependence. The lower band is usually near zero for MI and is not typically operationally useful.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6a184ca8fe15b39a` [interpretation] (literature_supported) — When `compute_surrogates` is false, significance was skipped or suppressed, which is different from a run where surrogates were computed and no lags were significant.
  > When `compute_surrogates` is `false`, significance was skipped or suppressed. That is different from a run where surrogates were computed and no lags were significant.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6c60cbc7e087bdb4` [decision] (literature_supported) — F2 should be used before investing in complex models because if the limit is low, model engineering gains diminish rapidly.
  > Before investing in complex models: if the limit is low, model engineering gains diminish rapidly.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6cd11f0e30d05f50` [cue] (literature_supported) — This repository flags directness_ratio > 1.0 as arch_suspected.
  > This repository flags `directness_ratio > 1.0` as `arch_suspected`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6d3f5a6dbc7b1178` [expectancy] (literature_supported) — Without the known_future_drivers opt-in, every k=0 row for a driver will have selected_for_tensor=False and tensor_role="diagnostic".
  > Without this opt-in, every $k=0$ row for `"holiday_flag"` will have `selected_for_tensor=False` and `tensor_role="diagnostic"`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6e81eaa5ab980b86` [strategy] (literature_supported) — Stable lag rankings and small directness-ratio range should be preferred over raw pAMI magnitude.
  > Prefer stable lag rankings and small directness-ratio range over raw pAMI magnitude.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-703f18d903194a6e` [strategy] (literature_supported) — A practitioner should interact with the profile instead of the raw numeric array to avoid re-implementing the threshold logic in downstream code.
  > A practitioner interacts with the profile instead of the raw numeric array to avoid re-implementing the threshold logic in downstream code.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-711c2d10c3a6b44a` [interpretation] (literature_supported) — A tensor_role of "known_future" indicates a lag is eligible at k = 0 via explicit known_future_drivers opt-in.
  > `"known_future"` Eligible at $k = 0$ via explicit `known_future_drivers` opt-in
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-718b8e1724271bae` [norm] (literature_supported) — pAMI quantifies approximate direct dependence after removing mediated paths but does not prove direct causality or Granger causality.
  > pAMI quantifies approximate direct dependence after removing mediated paths. It does not prove direct causality or Granger causality.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-747c5499f1f60c5a` [concept] (literature_supported) — The diagnostics package provides surrogates, CMI backends, spectral helpers, and regression utilities.
  > Surrogates, CMI backends, spectral helpers, and regression utilities
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7ab22b65453c30fb` [prerequisite] (literature_supported) — At least n_surrogates = 99 is required for a valid two-sided 95% band, and fewer than 99 surrogates are not sufficient and must not be used as a significance threshold.
  > At least `n_surrogates = 99` is required for a valid two-sided 95% band. Fewer than 99 surrogates are not sufficient and must not be used as a significance threshold.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7af7772c6efe28c5` [check] (literature_supported) — Significance counts are currently zero across the canonical summary, so actionable lag decisions should rely on class-level screening plus domain checks rather than significance-lag selection alone.
  > significance counts are currently zero across this canonical summary (`n_sig_ami=0`, `n_sig_pami=0` for all 8), so actionable lag decisions should rely on class-level screening plus domain checks rather than significance-lag selection alone.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7afe58436134c4db` [check] (literature_supported) — Overfitting in nonlinear backends should be mitigated by comparing against linear baseline and requiring ranking stability.
  > Overfitting in nonlinear backends sharp pAMI spikes at isolated lags only for tree backends backend fits noise in conditioning space compare against linear baseline and require ranking stability
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-810c2a3a56d85fd6` [interpretation] (literature_supported) — When directness_ratio exceeds 1.0, this is an anomaly boundary rather than positive evidence of direct causal structure or particularly strong direct dependence.
  > This is an **anomaly boundary, not positive evidence** of direct causal structure or particularly strong direct dependence.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-81616adcdb08062f` [cue] (literature_supported) — directness_ratio is a diagnostic ratio only and unstable on weak or noisy short windows.
  > Diagnostic ratio only; unstable on weak/noisy short windows
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8323af7405c72872` [interpretation] (literature_supported) — A positive Largest Lyapunov Exponent estimate is consistent with chaotic dynamics, but stochastic coloured noise and non-stationary processes also produce positive estimates, and F5 alone cannot distinguish the two cases.
  > A positive $\hat{\lambda}$ is consistent with chaotic dynamics, but stochastic coloured noise and non-stationary processes also produce positive estimates. F5 alone cannot distinguish the two cases.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-835ab48b9520fadc` [check] (literature_supported) — Routing validation checks whether the routing policy emits defensible family-level guidance before a downstream framework hand-off.
  > It checks whether the routing policy emits defensible family-level guidance before a downstream framework hand-off.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-84a52f4f0eefabdc` [expectancy] (literature_supported) — IT limit diagnostics (F2) sets realistic expectations before model investment and flags information-destroying transforms.
  > Sets realistic expectations before model investment; flags information-destroying transforms
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8bcff0024dacaf2c` [concept] (literature_supported) — AMI is horizon-specific, kNN-based, and uses phase-surrogate significance bands.
  > AMI is paper-aligned (horizon-specific, kNN-based, with phase-surrogate significance bands).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8c90b5242c0436c6` [strategy] (literature_supported) — Upper-band crossings should be used to detect non-null dependence.
  > Use upper-band crossings to detect non-null dependence.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-92e78f3c7c6b0970` [interpretation] (literature_supported) — bike_cnt_temp has the strongest useful signal with mean_raw_cross_mi=0.0906 and mean_conditioned_cross_mi=0.0523 with no warning horizons.
  > `bike_cnt_temp` has the strongest useful signal (`mean_raw_cross_mi=0.0906`, `mean_conditioned_cross_mi=0.0523`, no warning horizons), while multiple noise-linked cases can be deprioritised early.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-93e9a7b97c8cdde4` [interpretation] (literature_supported) — The "known_future" tensor_role value is only assigned when the user explicitly opts in via known_future_drivers={"driver_name": True}.
  > The `"known_future"` value is only assigned when the user explicitly opts in via `known_future_drivers={"driver_name": True}`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-941fc4c65cc338ea` [cue] (literature_supported) — Spectral predictability (F4) captures linear structure only and non-stationary series need detrending.
  > Captures linear structure only; non-stationary series need detrending
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-9533522b3bc5225d` [concept] (literature_supported) — In relation to supply chain management, the Du Pont model has been used to show that an increase in forecast accuracy can generate increases in sales and reductions in inventory, operating expenses and commitment of working capital.
  > In relation to supply chain management, the Du Pont model has been used to show that an increase in forecast accuracy can generate increases in sales and reductions in inventory, operating expenses and commitment of working capital.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-98c910c65938f691` [norm] (literature_supported) — The extended forecastability analysis surface suggests starting model families only and does not fit models or wire downstream frameworks.
  > The surface suggests starting model families only; it does not fit models or wire downstream frameworks.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-98f4acdc5829c239` [cue] (literature_supported) — Lags with partial autocorrelations outside of the confidence interval indicate that the AR model's order is likely greater than or equal to the lag.
  > Lags with partial autocorrelations outside of the confidence interval indicate that the AR model's order is likely greater than or equal to the lag.
  (documentation, https://en.wikipedia.org/wiki/Partial_autocorrelation_function, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-99e767adf11feef3` [expectancy] (literature_supported) — A strictly decreasing forecastability profile holds for simple AR processes and many white-noise-corrupted signals, but is not a universal requirement.
  > A strictly decreasing forecastability profile - $F(1) \ge F(2) \ge \cdots$ - holds for simple AR processes and many white-noise-corrupted signals. However, it is **not** a universal requirement.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-9ceadd7629751a08` [interpretation] (literature_supported) — Transfer Entropy values are estimator- and null-model-aware diagnostics, not causal proof.
  > TE values are estimator- and null-model-aware diagnostics, not causal proof.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a323418137e4ec1d` [concept] (literature_supported) — Risk and uncertainty are central to forecasting and prediction.
  > Risk and uncertainty are central to forecasting and prediction; it is generally considered a good practice to indicate the degree of uncertainty attaching to forecasts.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-a4b4af980507c12f` [expectancy] (literature_supported) — Different forecasting methods may lead to different levels of forecasting accuracy.
  > Previous research shows that different methods may lead to different level of forecasting accuracy.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 2)
- `c-a58d2b7c5d7500ea` [procedure_step] (literature_supported) — To evaluate the AR model order, one should examine the plot to find the lag after which the partial autocorrelations are all within the confidence interval, and this lag is determined to likely be the AR model's order.
  > To evaluate the order, one examines the plot to find the lag after which the partial autocorrelations are all within the confidence interval. This lag is determined to likely be the AR model's order.
  (documentation, https://en.wikipedia.org/wiki/Partial_autocorrelation_function, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-a9b52c4d0149e879` [failure_mode] (literature_supported) — Positive MI bias is strongest when the number of nearest neighbours k is large relative to the local sample density, with short series having high-dimensional lag spaces (F3 at large k) being most affected.
  > Positive MI bias is strongest when the number of nearest neighbours $k$ is large relative to the local sample density. Short series with high-dimensional lag spaces (F3 at large $k$) are most affected.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ab457177a15fba89` [cue] (literature_supported) — Short, sparse, and degenerate distributions should be treated as fragile for MI estimation.
  > Treat short, sparse, and degenerate distributions as fragile for MI estimation.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ab4f9f360073f8bf` [check] (literature_supported) — The is_non_monotone flag should be inspected before applying simplifying assumptions that assume monotone decay.
  > `is_non_monotone` flags this shape for downstream consumers without judgement. Routines that assume monotone decay (such as naive exponential smoothers) should inspect this flag before applying simplifying assumptions.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-abc3a8fdc46d2891` [check] (literature_supported) — F2 should be avoided as a standalone decision without F1 because the limit is derived from the AMI curve, making F1 evidence prerequisite context.
  > As a standalone decision without F1: the limit is derived from the AMI curve, so F1 evidence is prerequisite context.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-afa5f0d661961065` [procedure_step] (literature_supported) — Transfer Entropy significance is evaluated against phase-randomized surrogate bands.
  > Significance is evaluated against phase-randomized surrogate bands and should be interpreted with the same surrogate caveats used elsewhere in this repository.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-b0a136a964a61368` [expectancy] (literature_supported) — If factors are not known and well understood or if the actual outcome is affected by the forecasts, the reliability of the forecasts can be significantly lower.
  > If this is not the case or if the actual outcome is affected by the forecasts, the reliability of the forecasts can be significantly lower.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-b271bed82711edbd` [expert_novice_contrast] (literature_supported) — Research has shown that there is little difference between the accuracy of the forecasts of experts knowledgeable in conflict situations and those by individuals who knew much less.
  > However research has shown that there is little difference between the accuracy of the forecasts of experts knowledgeable in the conflict situation and those by individuals who knew much less.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-b4ef611dc20576cf` [interpretation] (literature_supported) — If a derived feature yields strictly lower profile values than the unaggregated series, the transformation has destroyed predictive information.
  > If a derived feature - for example, a box-aggregated or coarsely discretised version of the raw series - yields strictly lower profile values than the unaggregated series, the transformation has destroyed predictive information.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-b65af5fb5af0e039` [interpretation] (literature_supported) — When directness_ratio exceeds 1.0, the correct interpretation is to treat the ratio as informative only below 1.0, with values above 1.0 indicating the residual approximation has broken down at that horizon.
  > The correct interpretation: treat the ratio as informative only below 1.0; values above 1.0 indicate the residual approximation has broken down at that horizon.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-bb81e868e69be7c9` [procedure_step] (literature_supported) — Surrogate significance uses phase-randomized surrogates with two-sided 95% quantiles: lower band at 2.5th percentile and upper band at 97.5th percentile.
  > Significance bands Surrogate significance uses phase-randomized surrogates and two-sided 95% quantiles: - lower: 2.5th percentile - upper: 97.5th percentile
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-bc1390eb64e8e1ad` [decision] (literature_supported) — A driver that keeps most of its pairwise signal after conditioning pressure is a better candidate for downstream use than a driver that collapses because the collapsing driver is probably borrowing strength from target memory, common forcing, seasonality, or shared regime.
  > A driver that keeps most of its pairwise signal after conditioning pressure is a better candidate for downstream use; a driver that collapses is probably borrowing strength from target memory, common forcing, seasonality, or shared regime.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-be36b9a10f7a0b40` [expectancy] (literature_supported) — Forecastability profile (F1) narrows model evaluation to productive horizons and detects non-monotone seasonal structure.
  > Narrows model evaluation to productive horizons; detects non-monotone seasonal structure
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c1022f308b41e2bf` [failure_mode] (literature_supported) — Treating a continuous variable as discrete and vice versa will usually give incorrect results.
  > treating a continuous variable as discrete and vice versa will usually give incorrect results
  (documentation, https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.mutual_info_regression.html, published None, independence ind-s-ca7d54da5b087ed3, corroboration 1)
- `c-c2b896b883e73f0d` [procedure_step] (literature_supported) — CrosspAMI shows whether a relationship survives the target-history adjustment after CrossAMI identifies where the raw relationship appears.
  > CrossAMI says where the raw relationship appears. CrosspAMI asks whether the relationship survives the target-history adjustment.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c74cc1064e4c45f0` [concept] (literature_supported) — src/forecastability/reporting/ contains deterministic interpretation and Markdown/report builders.
  > `interpretation.py`, `reporting.py` Deterministic interpretation and Markdown/report builders
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d246c7289b23c665` [concept] (literature_supported) — reporting/reporting.py owns Markdown and report-building helpers.
  > `reporting/reporting.py` owns Markdown and report-building helpers.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d2fe4032fb3d7413` [cue] (literature_supported) — For highly periodic series, phase-randomized FFT surrogates can make significance tests conservative or uninformative even when the underlying series is obviously structured.
  > For highly periodic series, they can make significance tests conservative or uninformative even when the underlying series is obviously structured.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d4e1854a9257c96f` [representation] (literature_supported) — The PacfResult object contains confint field as an ndarray or None with confidence intervals for PACF at lags 0, 1, ..., nlags and shape (nlags + 1, 2), or None when alpha is None.
  > confintndarray or None Confidence intervals for the PACF at lags 0, 1, ..., nlags. Shape (nlags + 1, 2). None when alpha is None.
  (documentation, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html, published None, independence ind-s-5114732bc45e7988, corroboration 1)
- `c-d9dbc5bd00b743f9` [expectancy] (literature_supported) — Weaker AMI-error discrimination is expected in Daily frequency than in Hourly, Weekly, Quarterly, or Yearly.
  > Expect weaker AMI-error discrimination in Daily frequency than in Hourly/Weekly/Quarterly/Yearly.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-dae4d8a2181b192d` [representation] (literature_supported) — Every LaggedExogProfileRow and LaggedExogSelectionRow carries a lag_role field that specifies the chronological role.
  > Every `LaggedExogProfileRow` and `LaggedExogSelectionRow` carries a `lag_role` field
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-dfc30bee6ce95ce2` [prerequisite] (literature_supported) — Phase randomisation assumes approximate second-order stationarity, and series with strong trends or regime changes will produce uninformative surrogate bands.
  > Phase randomisation preserves the power spectrum but destroys temporal order. It assumes approximate second-order stationarity. Series with strong trends or regime changes will produce uninformative surrogate bands.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e1fb8518bb94b193` [interpretation] (literature_supported) — A lag_role of "instant" indicates k = 0 and represents contemporaneous association that is structural or multivariate in nature.
  > `"instant"` $k = 0$ Contemporaneous association - structural / multivariate
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e5227ad7e7d197e5` [prerequisite] (literature_supported) — Phase-randomized surrogate significance bands require a minimum series length to produce stable quantile estimates, and when the series is too short, significance may be unavailable and the surrogate bands are omitted.
  > Phase-randomized surrogate significance bands require a minimum series length to produce stable quantile estimates. When the series is too short, significance may be unavailable and the surrogate bands are omitted.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e5e1e73dba61b2c2` [interpretation] (literature_supported) — The lower band is near zero for MI and usually not operationally informative.
  > Lower band is near zero for MI and usually not operationally informative.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e68b6e04ba5d4ad3` [concept] (literature_supported) — Routing validation audits deterministic routing against controlled archetypes and sanity panels but does not train or benchmark forecasting models.
  > Routing validation audits deterministic routing against controlled archetypes and sanity panels. It does **not** train or benchmark forecasting models.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e69be58ea45c4382` [check] (literature_supported) — Numerical inflation should be treated as a warning and verified with multiple backends and sample-size stress testing.
  > Numerical inflation `directness_ratio > 1.0` estimator instability, finite-sample effects Treat as warning; verify with multiple backends and sample-size stress
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e820cb50f4fdf758` [strategy] (literature_supported) — When surrogate significance bands are available via phase-randomised surrogates, they extend to k = 0 so the strength of the instantaneous coupling can be assessed against the noise floor.
  > When surrogate significance bands are available (phase-randomised surrogates), they extend to $k = 0$ so the strength of the instantaneous coupling can be assessed against the noise floor.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-eaceff61fd0b53ca` [concept] (literature_supported) — A forecast is not to be confused with a budget.
  > A forecast is not to be confused with a Budget; budgets are more specific, fixed-term financial plans used for resource allocation and control, while forecasts provide estimates of future financial performance, allowing for flexibility and adaptability to changing circumstances.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-eb056e015c0ff76a` [cue] (literature_supported) — AMI detects dependence, not causality or guaranteed model gains.
  > Detects dependence, not causality or guaranteed model gains
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-efde45474384037f` [interpretation] (literature_supported) — F6 should be used to contextualise F1 AMI results because high AMI with low complexity typically indicates regular, easily modelled dynamics while high AMI with high complexity suggests potentially nonlinear or chaotic behaviour.
  > To contextualise F1 AMI results: high AMI with low complexity typically indicates regular, easily modelled dynamics; high AMI with high complexity suggests potentially nonlinear or chaotic behaviour.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f08b73f32120778a` [cue] (literature_supported) — Exogenous analysis is association-based screening and confounding and common-cause effects can remain.
  > Association-based screening; confounding and common-cause effects can remain
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f253f8efbf166412` [expectancy] (literature_supported) — Entropy-based complexity (F6) provides fast regime classification and complements AMI with amplitude-blind ordinal structure.
  > Fast regime classification; complements AMI with amplitude-blind ordinal structure
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f30acadec3e2a4b9` [check] (literature_supported) — Significance not assessed is different from surrogates being computed with no lags clearing the band, and interpretation of significant-lag fields should only be performed when compute_surrogates is true.
  > "Significance not assessed" is different from "surrogates were computed and no lags cleared the band." Use `compute_surrogates` to distinguish those states. Only interpret `n_sig_raw_lags`, `n_sig_partial_lags`, or other significant-lag fields as evidence about absent significance when `compute_surrogates` is `true`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f42869b67ba16526` [cue] (literature_supported) — When directness_ratio exceeds 1.0, this arises most commonly in noisy series, misspecified linear residual backends, or very short series where estimation variance is high.
  > It arises most commonly in noisy series, misspecified linear residual backends, or very short series where estimation variance is high.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f8476f85251e4685` [concept] (literature_supported) — Forecasts provide estimates of future financial performance, allowing for flexibility and adaptability to changing circumstances.
  > forecasts provide estimates of future financial performance, allowing for flexibility and adaptability to changing circumstances.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-f92a99ecd9d99e66` [procedure_step] (literature_supported) — If an AR model is determined to be appropriate, the sample partial autocorrelation plot should be examined to help identify the order.
  > If an AR model is determined to be appropriate, then the sample partial autocorrelation plot is examined to help identify the order.
  (documentation, https://en.wikipedia.org/wiki/Partial_autocorrelation_function, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-fac947a495d47b4e` [failure_mode] (literature_supported) — The Rosenstein algorithm and Takens embedding are sensitive to noise, non-stationarity, and the choice of embedding parameters (m, τ, Theiler window, evolution time s), with small parameter changes producing meaningfully different λ values.
  > The Rosenstein algorithm and Takens embedding are sensitive to noise, non-stationarity, and the choice of embedding parameters ($m$, $\tau$, Theiler window, evolution time $s$). Small parameter changes can produce meaningfully different $\hat{\lambda}$ values.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-fcf27e7c3d8165b3` [cue] (literature_supported) — Largest Lyapunov exponent (F5) is experimental, unreliable at finite sample sizes, gated behind config flag, and never auto-included in triage score.
  > Experimental - unreliable at finite sample sizes; gated behind config flag; never auto-included in triage score
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-fea5cc0c0b9e606e` [norm] (literature_supported) — When a method genuinely lacks a surrogate path such as standard cross-correlation, the significance field stays explicitly None and the row metadata records significance_source = "not_computed", with no synthetic p-values invented.
  > When a method genuinely lacks a surrogate path (standard cross-correlation), the significance field stays explicitly `None` and the row metadata records `significance_source = "not_computed"`. No synthetic p-values are invented.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ffefb722d893d833` [representation] (literature_supported) — The tensor_role field states whether a lag may legitimately enter a lagged-exogenous tensor used for ordinary forecasting.
  > The `tensor_role` field states whether the lag may legitimately enter a lagged-exogenous tensor used for ordinary forecasting
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)

### Synthetic / rejected claims

- `c-0a6395ca675ace71` [interpretation] (synthetic_extrapolation) — For standard cross-correlation, the significance field stays None and significance_source = "not_computed".
  > Significance field stays `None`; `significance_source = "not_computed"`
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md)
- `c-16b94bdf0141a593` [procedure_step] (synthetic_extrapolation) — A confidence interval for lags greater than p can be constructed by dividing a selected z-score by the square root of n. (no located evidence)
- `c-21691878aa36c4e2` [interpretation] (synthetic_extrapolation) — The `readiness_status` field indicates whether the data is clear, warning-level, or blocked. (no located evidence)
- `c-2fb33022d86042c9` [strategy] (synthetic_extrapolation) — A practitioner should target model evaluation exclusively at horizons in the informative horizon set; lags outside this set carry no detectable predictive signal above the noise floor.
  > A practitioner should target model evaluation exclusively at horizons in $\mathcal{H}_\varepsilon$ - lags outside this set carry no detectable predictive signal above the noise floor.
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md)
- `c-375871c0a6bba5e1` [interpretation] (synthetic_extrapolation) — The `recommendation` field is one of the minimum trust fields to read.
  > Start with the fields that tell you whether the result is usable and whether significance was actually computed. summary = { "blocked": result.blocked, "readiness_status": result.readiness.status.value, "compute_surrogates": None if result.method_plan is None else result.method_plan.compute_surrogates, "forecastability_class": None if result.interpretation is None else result.interpretation.forecastability_class, "primary_lags": [] if result.interpretation is None else list(result.interpretation.primary_lags), "recommendation": result.recommendation, }
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md)
- `c-6daf32efd7ca44e6` [concept] (synthetic_extrapolation) — The reporting package provides deterministic interpretation and Markdown and report builders. (no located evidence)
- `c-74064c14cad1a60e` [representation] (synthetic_extrapolation) — Confidence intervals for the CCF are computed at lags 0, 1, ..., nlags-1 with shape (nlags, 2). (no located evidence)
- `c-7aa6a60c96e403ae` [interpretation] (synthetic_extrapolation) — The fingerprint routing output is heuristic family guidance, not exact-model selection and not a multivariate conditional-MI claim. (no located evidence)
- `c-856cb8ebd2be354e` [expectancy] (synthetic_extrapolation) — On v0.3.3 and later, `bundle.recommendation.confidence_label` can be `abstain` when the routing policy emits no primary families. (no located evidence)
- `c-8713685dabdb84b3` [interpretation] (synthetic_extrapolation) — The extended analysis surface remains AMI-first, and if AMI geometry is disabled or unavailable, the output stays descriptive-only and does not emit routing-grade family recommendations. (no located evidence)
- `c-8cb32a57297200d8` [procedure_step] (synthetic_extrapolation) — F2 should be used when comparing multiple series because the compression ratio is a cross-series comparable metric.
  > When comparing multiple series: the compression ratio (observed AMI / limit) is a cross-series comparable metric.
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md)
- `c-9aeed27244c17331` [failure_mode] (synthetic_extrapolation) — Overfitting in nonlinear backends appears as sharp pAMI spikes at isolated lags, occurring only for tree backends when the backend fits noise in conditioning space.
  > Overfitting in nonlinear backends sharp pAMI spikes at isolated lags only for tree backends backend fits noise in conditioning space
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md)
- `c-a1769da1ecc73375` [interpretation] (synthetic_extrapolation) — A tensor_role of "predictive" indicates a lag is eligible to enter a lagged-exogenous tensor for ordinary forecasting.
  > `"predictive"` Eligible to enter a lagged-exogenous tensor for ordinary forecasting
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md)
- `c-a38d7aa5e20edbc4` [interpretation] (synthetic_extrapolation) — The `compute_surrogates` field indicates whether significance was actually computed. (no located evidence)
- `c-bc134346ee748c5a` [interpretation] (synthetic_extrapolation) — A directness_ratio of approximately 1 indicates mostly direct structure.
  > \(r \approx 1\): mostly direct structure.
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md)
- `c-c0066fa4ef2b92f9` [norm] (synthetic_extrapolation) — pAMI does not prove direct causality but quantifies approximate direct lag-dependence after a linear conditioning step. (no located evidence)
- `c-c0649b9cfdf7bb61` [interpretation] (synthetic_extrapolation) — The `forecastability_class` field indicates high-level interpretation when triage completed. (no located evidence)
- `c-c0c29862e5d8a193` [concept] (synthetic_extrapolation) — reporting/interpretation.py owns deterministic interpretation output. (no located evidence)
- `c-c978a689afd89de4` [interpretation] (synthetic_extrapolation) — A directness_ratio greater than 1 indicates a numerical or assumption warning, often ARCH-type behavior, not a physical contradiction.
  > \(r > 1\): numerical/assumption warning (often ARCH-type behavior), not a physical contradiction.
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md)
- `c-cfc3e998b186c13a` [interpretation] (synthetic_extrapolation) — The `primary_lags` field identifies informative lags identified by the deterministic workflow. (no located evidence)
- `c-d22741377a176c37` [interpretation] (synthetic_extrapolation) — A directness_ratio much less than 1 indicates mostly mediated structure.
  > \(r \ll 1\): mostly mediated structure.
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md)
- `c-d7253bc9451d297f` [interpretation] (synthetic_extrapolation) — When compute_surrogates is false, significance was not assessed for that run, which is distinct from computed significance bands showing no significant lags, and these two outcomes must not be conflated. (no located evidence)
- `c-da688457c5163577` [failure_mode] (synthetic_extrapolation) — Standard cross-correlation cannot detect symmetric nonlinear couplings, such as when a quadratic driver with near-zero Pearson correlation can be a strong predictive feature.
  > **Cannot detect symmetric nonlinear couplings** - a quadratic driver with near-zero Pearson correlation can be a strong predictive feature; always cross-check with `cross_ami`
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md)
- `c-e9861ffee3e2b149` [concept] (synthetic_extrapolation) — directness_ratio compares corrected pAMI mass with raw AMI mass and is useful for triage but unstable when raw information mass is tiny. (no located evidence)
- `c-f38f7c8aa579c1e3` [check] (synthetic_extrapolation) — F2 should be avoided when series length is very short because finite-sample bias inflates the estimated limit.
  > When series length is very short: finite-sample bias inflates the estimated limit.
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md)
- `c-f6ce74594f78fd34` [representation] (synthetic_extrapolation) — The directness_ratio r equals AUC(pAMI) / AUC(AMI).
  > `directness_ratio`: \[ r = \frac{\operatorname{AUC}(\tilde{I}_h)}{\operatorname{AUC}(I_h)} \]
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md)

### UNKNOWN / thin / unverified / unexamined slots

- none

## Area: Running Horizon-Wise Forecastability Analysis

### Supported claims

- `c-02a39901459fc5c2` [concept] (literature_supported) — The epsilon field is the resolved threshold for the informative horizon set.
  > `epsilon` `float` Resolved threshold $\varepsilon$ for $\mathcal{H}_\varepsilon$
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-02db4a573b917ded` [check] (literature_supported) — In rolling-origin evaluation, diagnostics are computed on train windows only and scoring on post-origin holdout only.
  > In rolling-origin evaluation, diagnostics are computed on train windows only and scoring on post-origin holdout only.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0383c186390263e0` [mental_model] (literature_supported) — The toolkit sits one step earlier: forecastability triage, then model-family choice, then framework-specific modeling.
  > Instead, it sits one step earlier: forecastability triage → model-family choice → framework-specific modeling
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-05729f84f51d52c4` [cue] (literature_supported) — kNN MI is unreliable for k > 5-8 at small n and mandatory reliability warnings are required.
  > kNN MI unreliable for k > 5-8 at small n; mandatory reliability warnings
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-05fc10f5fb9b2b9c` [procedure_step] (literature_supported) — If set to False, the copy parameter causes the initial data to be overwritten.
  > If set to False, the initial data will be overwritten.
  (documentation, https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.mutual_info_regression.html, published None, independence ind-s-ca7d54da5b087ed3, corroboration 1)
- `c-0a05f2c6d19c0805` [procedure_step] (literature_supported) — The triage workflow orchestration uses one entry point (`run_triage`) with staged readiness, routing, compute, and interpretation checks.
  > one-entry-point orchestration (`run_triage`) with staged readiness, routing, compute, and interpretation checks validated in [../tests/test_triage_run.py](../tests/test_triage_run.py), [../tests/test_triage_router.py](../tests/test_triage_router.py), and [../tests/test_triage_readiness.py](../tests/test_triage_readiness.py).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0ba98927fe267eac` [prerequisite] (literature_supported) — With linear residual backend, pAMI feasibility requires N ≥ max(H + min_pairs_pami + 1, 2H).
  > pAMI feasibility (linear residual backend): \[ N \ge \max\left(H + \texttt{min\_pairs\_pami} + 1,\ 2H\right) \]
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0bc576ddaf02fce5` [strategy] (literature_supported) — The triage workflow blocks infeasible requests and routes exogenous requests separately, preserving stable screening behavior where AR(1) yields high forecastability and white_noise yields low forecastability.
  > The workflow blocks infeasible requests, routes exogenous requests separately, and preserves stable screening behavior (`AR(1) -> high`, `white_noise -> low`) in regression tests.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0c2654257b1f515f` [procedure_step] (literature_supported) — Forecastability triage should cover readiness, leakage risk, informative horizons, primary lags, seasonality structure, and covariate informativeness.
  > Start with forecastability triage first: readiness, leakage risk, informative horizons, primary lags, seasonality structure, and covariate informativeness.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0c818ceeb5ed84c5` [concept] (literature_supported) — The pipeline package provides analyzer facade, canonical workflow helpers, and rolling-origin support.
  > Analyzer facade, canonical workflow helpers, and rolling-origin support
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0fafc1bf7c6dc020` [procedure_step] (literature_supported) — F1 should be used at the start of any triage pass as the anchor that all other diagnostics contextualise.
  > At the start of any triage pass; F1 is the anchor all other diagnostics contextualise.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-143b2f1030f42c35` [check] (literature_supported) — The run_rolling_origin_evaluation() function enforces the train-holdout leakage boundary internally, but if you compute diagnostics manually outside this function, you must enforce the same boundary.
  > The `run_rolling_origin_evaluation()` function enforces this boundary internally. If you compute diagnostics manually outside this function, you must enforce the same boundary.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-1529fd8d4983ffd9` [concept] (literature_supported) — Qualitative forecasting techniques are usually applied to intermediate- or long-range decisions.
  > They are usually applied to intermediate- or long-range decisions.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-158b572135807eda` [concept] (literature_supported) — The Entropy-Complexity Band (F6) diagnostic measures the normalised permutation entropy and spectral entropy of the series, combined to classify its disorder level into a complexity band.
  > The normalised permutation entropy and spectral entropy of the series, combined to classify its disorder level into a complexity band (regular / moderate / noise-like), providing structural context for the AMI results.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-1dc897cf8db01147` [concept] (literature_supported) — The exogenous screening evaluation uses 7 target-driver benchmark cases: bike_cnt_temp, bike_cnt_hum, bike_cnt_noise, aapl_spy, aapl_noise, btc_eth, and btc_noise.
  > Dataset: 7 target-driver benchmark cases (`bike_cnt_temp`, `bike_cnt_hum`, `bike_cnt_noise`, `aapl_spy`, `aapl_noise`, `btc_eth`, `btc_noise`).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-219791a4285d8ed2` [concept] (literature_supported) — triage/models.py defines TriageRequest, TriageResult, readiness models, and method-plan models.
  > `triage/models.py` defines `TriageRequest`, `TriageResult`, readiness models, and method-plan models.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-22c185a3e41bc04e` [prerequisite] (literature_supported) — To ensure comparable metrics across folds in TimeSeriesSplit, samples must be equally spaced.
  > To ensure comparable metrics across folds, samples must be equally spaced.
  (documentation, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, published None, independence ind-s-ca7d54da5b087ed3, corroboration 1)
- `c-24ec3429630ebcff` [expectancy] (literature_supported) — Exogenous requests leave the extended_forecastability_analysis field omitted rather than pretending exogenous-aware extended analysis exists.
  > Exogenous requests leave the field omitted rather than pretending exogenous-aware extended analysis exists.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-2568150377d7fbb9` [procedure_step] (literature_supported) — The seasonal naïve method accounts for seasonality by setting each prediction to be equal to the last observed value of the same season.
  > The seasonal naïve method accounts for seasonality by setting each prediction to be equal to the last observed value of the same season.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-27d0b3495c0ff1ed` [procedure_step] (literature_supported) — F5 should be used in exploratory research only as one piece of converging evidence that a series may exhibit chaotic dynamics, always alongside F1 and F6.
  > Exploratory research only: as one piece of converging evidence that a series may exhibit chaotic dynamics, always alongside F1 and F6.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-2a706fb8beaeaad1` [concept] (literature_supported) — AMI answers the question of whether there is horizon-specific dependence worth exploiting at all.
  > AMI Is there horizon-specific dependence worth exploiting at all?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-2c567f4bccc5fa13` [check] (literature_supported) — The sparse lag selector guarantees that at least one row per (target, driver) pair is emitted by the selector.
  > **At least one row per `(target, driver)` pair** is emitted by the selector.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-2d0686feb9e1cedd` [concept] (literature_supported) — The summary field is a one-sentence human-readable profile description.
  > `summary` `str` One-sentence human-readable profile description
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-2df65dbe0d5c0b8a` [decision] (literature_supported) — Forecastability triage should classify whether exogenous drivers are predictive, merely contemporaneous, or useless.
  > Are exogenous drivers predictive, merely contemporaneous, or useless?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3079d77ce22ec266` [check] (literature_supported) — F7 should be avoided as a replacement for individual deep-dive analysis on flagged series because batch ranking surfaces which series to investigate, not why.
  > As a replacement for individual deep-dive analysis on flagged series: batch ranking surfaces which series to investigate, not why.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-30f3bb30e38be478` [concept] (literature_supported) — IT limit diagnostics (F2) answers the question of what the theoretical ceiling on prediction improvement is.
  > IT limit diagnostics (F2) What is the theoretical ceiling on prediction improvement?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3126a1ec60af42b4` [procedure_step] (literature_supported) — The extended cross_ami lag profile estimates mutual information I_k(X, Y) = I(X_{t-k}; Y_t) using the same kNN mutual-information estimator used throughout the covariant surface.
  > estimated with the same kNN mutual-information estimator used throughout the covariant surface
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-31524d4ec7dfcb67` [concept] (literature_supported) — The `ForecastPrepContract` is a structured, machine-readable hand-off contract for downstream model families.
  > a structured, machine-readable hand-off contract for downstream model families.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-341703ae536a2333` [check] (literature_supported) — F4 should be avoided for strongly non-stationary series without prior detrending.
  > For strongly non-stationary series without prior detrending.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-366be2f127206bb4` [concept] (literature_supported) — The Predictive Information Learning Curves (F3) diagnostic measures the mutual information between a k-step past embedding and the one-step-ahead future to identify the minimal sufficient lookback length.
  > The mutual information between a $k$-step past embedding and the one-step-ahead future, evaluated for $k = 1 \ldots K$, to identify the minimal sufficient lookback length where additional history yields negligible extra predictive information.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-38fe41612e2e57b6` [procedure_step] (literature_supported) — In the average approach, the predictions of all future values are equal to the mean of the past data.
  > In this approach, the predictions of all future values are equal to the mean of the past data.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-3b62ed2670796892` [prerequisite] (literature_supported) — F5 should be used when the series is long with n much greater than 1000 for the default embedding dimension m equals 3 and approximately stationary.
  > When the series is long ($n \gg 1000$ for the default embedding dimension $m = 3$) and approximately stationary.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3be94f737a955d35` [concept] (literature_supported) — The Spectral Predictability Score (F4) diagnostic measures the concentration of spectral power across frequency bins, normalised to [0,1], where Ω equals 1 for a perfectly periodic signal and approaches 0 for white noise.
  > The concentration of spectral power across frequency bins, normalised to $[0, 1]$: Ω = 1 for a perfectly periodic signal, Ω → 0 for white noise, quantifying linear-structure predictability independently of AMI.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3cd803060e27374f` [concept] (literature_supported) — src/forecastability/metrics/ contains core AMI/pAMI computation and scorer registry infrastructure.
  > `metrics.py`, `scorers.py` Core AMI/pAMI computation and scorer registry infrastructure
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3d81f927bb52cba0` [concept] (literature_supported) — diagnostics/surrogates.py owns phase-randomized FFT surrogates and significance bands.
  > `diagnostics/surrogates.py` owns phase-randomized FFT surrogates and significance bands.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3d9ce2bed01e3e37` [concept] (literature_supported) — Naïve forecasts provide a benchmark against which more sophisticated models can be compared.
  > Naïve forecasts are the most cost-effective forecasting model, and provide a benchmark against which more sophisticated models can be compared.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-3e06b2d68146d02f` [procedure_step] (literature_supported) — In rolling-origin evaluation, AMI, pAMI, and all F1-F8 diagnostics are computed on the training window up to each rolling origin, with no diagnostic touching the post-origin holdout.
  > AMI, pAMI, and all F1-F8 diagnostics are computed on the training window up to each rolling origin. No diagnostic touches the post-origin holdout.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3f0242b32570deef` [failure_mode] (literature_supported) — Violating the leakage boundary in rolling-origin evaluation introduces look-ahead leakage and invalidates the evaluation.
  > Violating it introduces look-ahead leakage and invalidates the evaluation.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-41d3706ac7784a9e` [procedure_step] (literature_supported) — F7 should be used as the entry point for any multi-series analysis because individual series results remain accessible through the batch result object.
  > As the entry point for any multi-series analysis; individual series results remain accessible through the batch result object.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4320281ef2092ffc` [concept] (literature_supported) — The ForecastabilityProfile is a read-only, frozen Pydantic model whose fields are populated once from the AMI curve already computed by the pipeline with no new estimation occurring during profile construction.
  > The profile is a read-only, frozen Pydantic model - `ForecastabilityProfile` - whose fields are populated once from the AMI curve already computed by the pipeline. No new estimation occurs during profile construction.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-45cf1838f39e8998` [procedure_step] (literature_supported) — The data must be up to date in order for the forecast to be as accurate as possible.
  > In any case, the data must be up to date in order for the forecast to be as accurate as possible.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-466c07cfc344fb2c` [decision] (literature_supported) — Forecastability triage should answer whether the target series is forecastable at all.
  > The goal is to avoid blind model iteration by asking practical questions first: - Is the target series forecastable at all?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-482edfa97ddd9d90` [concept] (literature_supported) — src/forecastability/models.py provides forecast baselines and optional model integrations used by rolling-origin workflows.
  > Forecast baselines and optional model integrations used by rolling-origin workflows
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4834fba7cc489f65` [procedure_step] (literature_supported) — F5 (Largest Lyapunov Exponent) must be explicitly enabled via experimental: true in the config and does not run in default triage mode.
  > F5 must be explicitly enabled via `experimental: true` in the config. It does not run in default triage mode.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-49027e4da30a7b2d` [procedure_step] (literature_supported) — F3 should be used when selecting the lookback window for a forecasting model, using the recommended plateau as a principled starting point.
  > When selecting the lookback window for a forecasting model: use the recommended plateau $k^*$ as a principled starting point.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4933d8a0da8e3ab8` [concept] (literature_supported) — The Batch Triage and Multi-Series Ranking (F7) diagnostic runs F1-F4 and F6 deterministically across a panel of series and produces a ranked diagnostic table.
  > Runs F1-F4 and F6 deterministically across a panel of series and produces a ranked diagnostic table, enabling rapid comparison of forecastability structure across many signals in one pass.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-494510f15a0daf07` [concept] (literature_supported) — The random_state parameter seeds both the MI estimator and the surrogate generator for reproducibility.
  > `random_state` Seeds both the MI estimator and the surrogate generator for reproducibility
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4a95e8c666050b01` [concept] (literature_supported) — In the k-th split of TimeSeriesSplit, the first k folds are returned as the train set and the (k+1)-th fold as the test set.
  > In the k-th split, it returns the first k folds as the train set and the (k+1)-th fold as the test set.
  (documentation, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, published None, independence ind-s-ca7d54da5b087ed3, corroboration 1)
- `c-520e8d5962f8f467` [norm] (literature_supported) — Surrogates should be used whenever sample size permits, specifically when n is at least 200 and n_surrogates is at least 99.
  > Use surrogates whenever sample size permits ($n \ge 200$, `n_surrogates >= 99`).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-55260de7bbeef4fe` [concept] (literature_supported) — The Forecastability Profile (F1) diagnostic measures the horizon-wise mutual information between a time series and its own future, producing an informative horizon set and structural shape flags for triage decision.
  > The horizon-wise mutual information between $X_t$ and its own future $X_{t+h}$ (AMI) and the approximate direct-dependence residual (pAMI), producing the informative horizon set $\mathcal{H}_\varepsilon$ and structural shape flags for the triage decision.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-576ebc0779aee373` [concept] (literature_supported) — The avoid_horizons field contains non-informative horizons that should be excluded from model feature sets.
  > `avoid_horizons` `list[int]` Non-informative horizons - exclude from model feature sets
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-581833cf91dd5324` [expectancy] (literature_supported) — AMI geometry stays first in extended forecastability analysis, and if it is disabled or unavailable, the profile remains descriptive-only and does not emit routing-grade family recommendations.
  > AMI geometry stays first. If it is disabled or unavailable, the profile remains descriptive-only and does not emit routing-grade family recommendations.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-597adedb13758132` [norm] (literature_supported) — Composite weighting across incommensurable scales in batch diagnostic ranking must be transparent.
  > Composite weighting across incommensurable scales must be transparent
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-599acaa7431652b7` [concept] (literature_supported) — In TimeSeriesSplit, each test set covers the same time duration, while the train set size accumulates data from previous splits.
  > each test set covers the same time duration, while the train set size accumulates data from previous splits.
  (documentation, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, published None, independence ind-s-ca7d54da5b087ed3, corroboration 1)
- `c-59ee33682140a710` [prerequisite] (literature_supported) — Transfer Entropy sample-size guardrails require min_pairs >= 50, and with non-empty conditioning history at least 2 * min_pairs aligned rows are required.
  > TE sample-size guardrails require `min_pairs >= 50`; with non-empty conditioning history, at least `2 * min_pairs` aligned rows are required.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5b01f234004df4db` [procedure_step] (literature_supported) — To run a deterministic triage call, use the stable package facade with a simple generated series by importing TriageRequest, generate_ar1, and run_triage from forecastability.
  > Use the stable package facade and a simple generated series. from forecastability import TriageRequest, generate_ar1, run_triage
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5c1320ad70979c3f` [concept] (literature_supported) — The max_lag parameter sets H, the length of the horizons and values arrays.
  > Parameter Effect on profile --- --- `max_lag` Sets $H$ - the length of the `horizons` and `values` arrays
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5d4e1e195302a4e3` [concept] (literature_supported) — metrics/scorers.py owns the scorer registry and built-in scorer family metadata.
  > `metrics/scorers.py` owns the scorer registry and built-in scorer family metadata.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5d9b402e3eb26996` [procedure_step] (literature_supported) — F6 should be used as a cheap pre-model screening step to set expectations for model difficulty.
  > As a cheap pre-model screening step to set expectations for model difficulty.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5e176e627bce2406` [concept] (literature_supported) — Qualitative forecasting techniques are subjective, based on the opinion and judgment of consumers and experts.
  > Qualitative forecasting techniques are subjective, based on the opinion and judgment of consumers and experts
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-5f42b1909154998b` [check] (literature_supported) — F7 should be avoided when F5 output is desired in the ranking because LLE is intentionally excluded from automated batch triage by design.
  > When F5 output is desired in the ranking: LLE is intentionally excluded from automated batch triage by design.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5fe1f348a68575f6` [check] (literature_supported) — F5 should be avoided in automated batch ranking because LLE is excluded by design.
  > In automated batch ranking (F7): LLE is excluded by design.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5ff63882db181126` [decision] (literature_supported) — Escalation should occur only when nonlinear backends improve diagnostic consistency across datasets.
  > Escalate only when nonlinear backends improve diagnostic consistency across datasets.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6004576158048832` [decision] (literature_supported) — Higher values of the n_neighbors parameter reduce variance of mutual information estimation but could introduce bias.
  > Higher values reduce variance of the estimation, but could introduce a bias.
  (documentation, https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.mutual_info_regression.html, published None, independence ind-s-ca7d54da5b087ed3, corroboration 1)
- `c-6091843095dfaffa` [procedure_step] (literature_supported) — F7 should be used when producing a reproducible ranking artefact for a report or downstream pipeline.
  > When producing a reproducible ranking artefact for a report or downstream pipeline.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-622a321d0163708d` [concept] (literature_supported) — The profile compresses the AMI curve into a set of actionable fields: the informative horizon set, the peak horizon, structural shape flags, and model-selection recommendations.
  > The profile compresses the AMI curve into a set of actionable fields: the set of horizons where forecastability clears a significance threshold (the *informative horizon set* $\mathcal{H}_\varepsilon$), the peak horizon, structural shape flags, and model-selection recommendations.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-63e7e5e12bf6d309` [decision] (literature_supported) — Quantitative forecasting models are appropriate to use when past numerical data is available and when it is reasonable to assume that some of the patterns in the data are expected to continue into the future.
  > They are appropriate to use when past numerical data is available and when it is reasonable to assume that some of the patterns in the data are expected to continue into the future.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-6460f909d8219d15` [concept] (literature_supported) — The values field contains AMI values F(h) for each horizon.
  > `values` `np.ndarray` AMI values - $F(h)$ for each horizon
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-66e765555d6c48bd` [concept] (literature_supported) — The informative horizon set is the subset of lags where forecastability exceeds threshold epsilon.
  > **The informative horizon set** is the subset of lags where forecastability exceeds threshold $\varepsilon$: $$ \mathcal{H}_\varepsilon = \bigl\{h : F(h;\,\mathcal{I}_t) \ge \varepsilon\bigr\} $$
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-68d0fb9846349b77` [concept] (literature_supported) — The ForecastabilityProfile model is frozen, which guarantees that fields cannot be mutated after construction and cached profiles remain consistent with their source AMI run.
  > The model is frozen (`model_config = ConfigDict(frozen=True)`); fields cannot be mutated after construction, which guarantees that cached profiles remain consistent with their source AMI run.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-69ede20ebca293a9` [procedure_step] (literature_supported) — Forecast errors and accuracy metrics are computed on the post-origin holdout window only in rolling-origin evaluation.
  > Forecast errors and accuracy metrics are computed on the post-origin holdout window only.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6d72b5ca901657cb` [concept] (literature_supported) — The forecastability fingerprint surface summarizes AMI-first information geometry into compact diagnostic features and deterministic model-family routing hints.
  > The fingerprint surface summarizes AMI-first information geometry into compact diagnostic features and deterministic model-family routing hints.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6edcb1534a501165` [concept] (literature_supported) — The Forecastability Profile is a structured summary of how much predictive information is available at each forecast horizon.
  > The **Forecastability Profile** is a structured summary of how much predictive information $I(Y_{t+h};\,\mathcal{I}_t)$ is available at each forecast horizon $h$.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6ef635f447f3db3c` [concept] (literature_supported) — The average approach can be used with any sort of data where past data is available.
  > This approach can be used with any sort of data where past data is available.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-70db791a682a6218` [procedure_step] (literature_supported) — F7 should be used when screening a large panel of candidate series to prioritise modelling effort.
  > When screening a large panel of candidate series to prioritise modelling effort.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7108a192d336b9eb` [check] (literature_supported) — F5 should be avoided as a causal or classification proof because a positive lambda does not distinguish deterministic chaos from coloured stochastic noise.
  > As a causal or classification proof: a positive $\hat{\lambda}$ does not distinguish deterministic chaos from coloured stochastic noise.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-73b132a5aaa54568` [procedure_step] (literature_supported) — F3 should be used when one suspects that longer lags add noise rather than signal, as the curve never plateauing is also informative.
  > When you suspect that longer lags add noise rather than signal (the curve never plateauing is also informative).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-753a8326d0fec03b` [concept] (literature_supported) — The profile reuses AMI values produced by ForecastabilityAnalyzer.analyze() with kNN MI estimator using n_neighbors=8, and no separate estimation step executes during profile construction.
  > The profile reuses AMI values produced by `ForecastabilityAnalyzer.analyze()`, which runs a kNN MI estimator with `n_neighbors=8`. No separate estimation step executes during profile construction.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7571015ec44ff066` [concept] (literature_supported) — The returned pacf vector includes lag 0 (which equals 1) so its size is (nlags + 1,).
  > The returned value includes lag 0 (ie., 1) so size of the pacf vector is (nlags + 1,).
  (documentation, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html, published None, independence ind-s-5114732bc45e7988, corroboration 1)
- `c-75c34cafb73f075f` [concept] (literature_supported) — The Forecastability Profile describes the full horizon-wise relationship between the target series and the available information set, from lag 1 to a user-specified maximum lag H.
  > It describes the full horizon-wise relationship between the target series and the available information set, from lag 1 to a user-specified maximum lag $H$.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-780a8173fdbc6eae` [concept] (literature_supported) — A deterministic approach is when there is no stochastic variable involved and the forecasts depend on the selected functions and parameters.
  > A deterministic approach is when there is no stochastic variable involved and the forecasts depend on the selected functions and parameters.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-789fd2b48f481040` [procedure_step] (literature_supported) — Forecastability triage should assess readiness, leakage risk, informative horizons, primary lags, seasonality structure, and covariate informativeness.
  > Start with forecastability triage first: readiness, leakage risk, informative horizons, primary lags, seasonality structure, and covariate informativeness.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-794b61adbdf91f51` [procedure_step] (literature_supported) — The drift method allows forecasts to increase or decrease over time, where the amount of change over time is set to be the average change seen in the historical data.
  > A variation on the naïve method is to allow the forecasts to increase or decrease over time, where the amount of change over time (called the drift) is set to be the average change seen in the historical data.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-794c8566b491bb01` [concept] (literature_supported) — The metrics package performs core AMI and pAMI computation and maintains a scorer registry.
  > Core AMI/pAMI computation and scorer registry
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7b333fb06dc27753` [prerequisite] (literature_supported) — Given series length N and max lag H, AMI feasibility requires N ≥ H + min_pairs_ami + 1.
  > AMI feasibility: \[ N \ge H + \texttt{min\_pairs\_ami} + 1 \]
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7b6eef4b5e3656fd` [check] (literature_supported) — The sparse lag selector guarantees that selected_for_tensor=True is impossible at k=0 unless the driver appears in known_future_drivers.
  > **`selected_for_tensor=True` is impossible at $k=0$** unless the driver appears in `known_future_drivers`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7bad1c7c10ee31b7` [expectancy] (literature_supported) — With defaults min_pairs_ami=30, min_pairs_pami=50, and H=100, AMI requires N ≥ 131.
  > With defaults (`min_pairs_ami=30`, `min_pairs_pami=50`, `H=100`): - AMI requires \(N \ge 131\)
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7c5a34b6e50105e8` [check] (literature_supported) — F1 should not be used as the sole decision-maker when surrogate significance bands are unavailable due to series being too short, and the curve should be treated as indicative rather than authoritative.
  > As the sole decision-maker when surrogate significance bands are unavailable (too-short series): treat the curve as indicative, not authoritative.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7cdafaa3179e08ab` [strategy] (literature_supported) — FFT convolution method should be preferred for long time series.
  > This method should be preferred for long time series.
  (documentation, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.ccf.html, published None, independence ind-s-5114732bc45e7988, corroboration 1)
- `c-7ced0e8b3ba87b91` [decision] (literature_supported) — Univariate forecastability triage asks whether the downstream process should abstain or start from simple baselines.
  > Should the downstream process abstain or start from simple baselines?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7f34e267e7469f22` [procedure_step] (literature_supported) — AMI and pAMI horizons should not be pre-aggregated before triage.
  > Keep AMI and pAMI horizon-specific; do not pre-aggregate before triage.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7f6b838b750e1bf6` [concept] (literature_supported) — The is_non_monotone field is True if forecastability increases at any horizon greater than 1.
  > `is_non_monotone` `bool` `True` if $F(h)$ increases at any $h > 1$
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-819845eb5ff32edc` [procedure_step] (literature_supported) — F4 should be used for rapid cross-series ranking where a computationally cheap linear-domain signal is sufficient.
  > For rapid cross-series ranking where a computationally cheap linear-domain signal is sufficient.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-820f7fdc57a3da73` [concept] (literature_supported) — triage/batch_models.py defines the batch request, row, execution, and response types.
  > `triage/batch_models.py` defines the batch request, row, execution, and response types.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-832f11ec63500689` [strategy] (literature_supported) — When the task is time-series forecasting, forecastability triage should be performed before model fitting.
  > When the task is time-series forecasting, do not jump directly to model fitting. Start with forecastability triage first
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-84881ec721cd9e23` [procedure_step] (literature_supported) — Using the naïve approach, forecasts are produced that are equal to the last observed value.
  > Using the naïve approach, forecasts are produced that are equal to the last observed value.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-85b9dda1cec21329` [concept] (literature_supported) — The horizons field is a list of 1-based lag indices from 1 to H.
  > `horizons` `list[int]` 1-based lag indices $[1, \dots, H]$
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8a7ac04178f31200` [procedure_step] (literature_supported) — Diagnostics for AMI and pAMI are computed on each training window only, while forecast errors are computed on post-origin test window only.
  > Diagnostics (AMI/pAMI) are computed on each training window only. - Forecast errors are computed on post-origin test window only.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8e2e0dac9cf9b0f8` [procedure_step] (literature_supported) — A CcfResult is always returned when alpha is not None.
  > When alpha is not None a CcfResult is always returned
  (documentation, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.ccf.html, published None, independence ind-s-5114732bc45e7988, corroboration 1)
- `c-8ec9eaf80e7fa3bd` [decision] (literature_supported) — Forecastability triage should identify which variables are safe to use without leakage.
  > Which variables are safe to use without leakage?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8f12cc7b29b6aefd` [procedure_step] (literature_supported) — When the discrete_features parameter is set to 'auto', it is assigned to False for dense X and to True for sparse X.
  > If 'auto', it is assigned to False for dense X and to True for sparse X.
  (documentation, https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.mutual_info_regression.html, published None, independence ind-s-ca7d54da5b087ed3, corroboration 1)
- `c-90d4d05132eb2ef2` [concept] (literature_supported) — Spectral predictability (F4) answers the question of how much linear predictable structure exists.
  > Spectral predictability (F4) How much linear predictable structure exists?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-910d5c067ea619cf` [procedure_step] (literature_supported) — F4 should be used to characterise the linear spectral structure of a series as complementary context alongside the nonlinear AMI profile.
  > To characterise the *linear* spectral structure of a series as complementary context alongside the *nonlinear* AMI profile.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-921ecef08dfe6f46` [concept] (literature_supported) — Univariate forecastability triage is used to determine whether the target series itself carries useful predictive structure.
  > Use this when you want to know whether the target series itself carries useful predictive structure.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-927e071dc53fbc4a` [expert_novice_contrast] (literature_supported) — In TimeSeriesSplit, successive training sets are supersets of those that come before them.
  > unlike standard cross-validation methods, successive training sets are supersets of those that come before them.
  (documentation, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, published None, independence ind-s-ca7d54da5b087ed3, corroboration 1)
- `c-92ea97938fb3a905` [check] (literature_supported) — F4 should be avoided for short series with n less than 128 because Welch PSD estimates are based on very few segments and Ω values are unreliable.
  > For short series ($n < 128$): Welch PSD estimates are based on very few segments and Ω values are unreliable as anything other than a coarse indicator.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-96ce00df7f79171a` [mental_model] (literature_supported) — Most forecasting work starts too late, with the usual problem being that the target has weak memory, the horizon is mismatched to the signal, the best covariates are unsafe at prediction time, or the strongest lags would leak future information.
  > Pick a forecasting library. Generate lag features. Add every covariate that looks plausible. Run a leaderboard. Then discover the target has weak memory, the horizon is mismatched to the signal, the best covariates are unsafe at prediction time, or the strongest lags would leak future information.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-9a3bc75db53d568c` [procedure_step] (literature_supported) — Frequency-specific horizon caps from the paper are: Yearly 6, Quarterly 8, Monthly 18, Weekly 13, Daily 14, Hourly 48.
  > Use frequency-specific horizon caps: Yearly 6, Quarterly 8, Monthly 18, Weekly 13, Daily 14, Hourly 48.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-9adf1e1ba5526b24` [check] (literature_supported) — F5 should be avoided for series with n less than 1000 because phase-space coverage is insufficient and the estimate is indicative only.
  > For series with $n < 1000$: phase-space coverage is insufficient and the estimate is indicative only.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-9fd96f8c30ad5eb5` [decision] (literature_supported) — Forecastability triage should suggest which model families are plausible enough to test next.
  > Which model families are plausible enough to test next?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-9ff6ec0defaaebdd` [concept] (literature_supported) — Quantitative forecasting models are used to forecast future data as a function of past data.
  > Quantitative forecasting models are used to forecast future data as a function of past data.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-a50059db985f4544` [concept] (literature_supported) — pipeline/analyzer.py contains ForecastabilityAnalyzer, ForecastabilityAnalyzerExog, and AnalyzeResult.
  > `pipeline/analyzer.py` contains `ForecastabilityAnalyzer`, `ForecastabilityAnalyzerExog`, and `AnalyzeResult`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a5bfbf4dc9e5e96b` [procedure_step] (literature_supported) — The same leakage boundary for rolling-origin evaluation applies to exogenous screening (F8), where CrossAMI must be computed on the training window only.
  > The same leakage boundary applies to exogenous screening (F8): CrossAMI must be computed on the training window only.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a72ee13e1f1d9a79` [concept] (literature_supported) — There is no single right forecasting method to use.
  > There is no single right forecasting method to use.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-a9099a5660c7e084` [procedure_step] (literature_supported) — The profile is constructed by forecastability_profile_service.build_forecastability_profile() and is exposed on the TriageResult returned by run_triage().
  > It is constructed by `forecastability_profile_service.build_forecastability_profile()` and is exposed on the `TriageResult` returned by `run_triage()`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ab949eff28cb9b8f` [concept] (literature_supported) — Extended forecastability analysis provides the AMI-first extended fingerprint plus a deterministic routing summary.
  > Use this when you want the implemented AMI-first extended fingerprint plus a deterministic routing summary in one additive result.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-acdfdb36da4410cd` [expectancy] (literature_supported) — When data are significance-infeasible (for example n=150 in regression tests), surrogates are skipped and decisions are route or class screening only, so the workflow supports prioritisation and method selection but not guaranteed downstream forecast accuracy gains.
  > when data are significance-infeasible (for example n=150 in regression tests), surrogates are skipped and decisions are route/class screening only. This workflow supports prioritisation and method selection, not guaranteed downstream forecast accuracy gains.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-afbbc01c74390081` [decision] (literature_supported) — Qualitative forecasting techniques are appropriate when past data are not available.
  > they are appropriate when past data are not available.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-b0270bf019fa2c0f` [interpretation] (literature_supported) — The v0.3.0 compute_exog_raw_curve emitted only k ∈ {1, ..., K_max}, whereas v0.3.2 adds the k = 0 row so that the multivariate diagnostic is visible alongside the predictive profile.
  > The v0.3.0 `compute_exog_raw_curve` emitted only $k \in \{1, \dots, K_{\max}\}$. v0.3.2 adds the $k = 0$ row so that the multivariate diagnostic is visible alongside the predictive profile.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-b30e6f402dc333d6` [mental_model] (literature_supported) — Reliability and variance properties of all profile fields inherit entirely from the underlying MI estimator.
  > Reliability and variance properties of all profile fields inherit entirely from the underlying MI estimator; improving estimator accuracy (e.g. raising `n_surrogates`, increasing the sample size, or choosing a better-matched `n_neighbors`) propagates automatically to the profile.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-b32c8b687cda267c` [concept] (literature_supported) — Largest Lyapunov exponent (F5) answers the question of whether a series shows sensitivity to initial conditions.
  > Largest Lyapunov exponent (F5) Does this series show sensitivity to initial conditions?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-b3e84475d5b7f9cc` [concept] (literature_supported) — Predictive info learning curves (F3) answers the question of how many past lags the series actually needs.
  > Predictive info learning curves (F3) How many past lags does the series actually need?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-b7af32f16baa778d` [concept] (literature_supported) — Some have claimed that forecasting is a transferable skill with benefits to other areas of discussion and decision making.
  > Some have claimed that forecasting is a transferable skill with benefits to other areas of discussion and decision making.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-b964ad16bc5fa59e` [procedure_step] (literature_supported) — The nlags parameter specifies the number of lags to return cross-correlations for, and if not provided, equals len(x).
  > Number of lags to return cross-correlations for. If not provided, the number of lags equals len(x).
  (documentation, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.ccf.html, published None, independence ind-s-5114732bc45e7988, corroboration 1)
- `c-b9d44f81ec1203cd` [procedure_step] (literature_supported) — src/forecastability/use_cases/ contains run_triage.py and run_batch_triage.py as application entry points that orchestrate deterministic triage and batch triage.
  > `run_triage.py`, `run_batch_triage.py` Application entry points that orchestrate deterministic triage and batch triage
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-bad024770a1735d5` [expectancy] (literature_supported) — The seasonal naïve method is particularly useful for data that has a very high level of seasonality.
  > The seasonal naïve method is particularly useful for data that has a very high level of seasonality.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-bb5262f78c659159` [concept] (literature_supported) — The profile is the primary deliverable of Feature F1 in the triage pipeline.
  > The profile is the primary deliverable of Feature F1 in the triage pipeline.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-bc0f6d147e36a968` [concept] (literature_supported) — Entropy-based complexity (F6) answers the question of whether a series is periodic, chaotic, or stochastic.
  > Entropy-based complexity (F6) Is this series periodic, chaotic, or stochastic?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-be3ef64ca8b56f71` [concept] (literature_supported) — pipeline/pipeline.py contains canonical workflow helpers used by scripts and tests.
  > `pipeline/pipeline.py` contains canonical workflow helpers used by scripts and tests.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-bf72579f2ce06838` [check] (literature_supported) — F1 should be avoided directly at horizons beyond the frequency-specific cap because AMI values beyond these caps are unreliable.
  > Directly at horizons beyond the frequency-specific cap (Yearly 6, Quarterly 8, Monthly 18, Weekly 13, Daily 14, Hourly 48): AMI values beyond these caps are unreliable.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c0a2ba435cda5fbb` [strategy] (literature_supported) — The workflow is intentionally conservative and does not claim to fit a winner but presents evidence, legal inputs, and where model search can begin without pretending the data are cleaner than they are.
  > The workflow is intentionally conservative. It does not say, "fit this winner." It says, "here is the evidence; here are the legal inputs; here is where model search can begin without pretending the data are cleaner than they are."
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c0ad72fbd17e0508` [procedure_step] (literature_supported) — use_cases/run_triage.py and use_cases/run_batch_triage.py are the authoritative orchestration entry points called by the public facade and adapters.
  > `use_cases/run_triage.py` and `use_cases/run_batch_triage.py` are the authoritative orchestration entry points called by the public facade and adapters.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c15b0b387e42600c` [procedure_step] (literature_supported) — F3 should be used in combination with F1 because F1 identifies which horizons are informative while F3 identifies how much history informs the one-step horizon.
  > In combination with F1: F1 identifies *which* horizons are informative; F3 identifies *how much* history informs the one-step horizon.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c206da1384655e33` [concept] (literature_supported) — The peak_horizon field is the 1-based index of the horizon with maximum forecastability.
  > `peak_horizon` `int` $h^* = \arg\max_h F(h)$ (1-based index)
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c6978261282cbd69` [check] (literature_supported) — F6 should be avoided for very short series because permutation entropy requires adequate pattern-frequency estimates and for m equals 5, at least n approximately 600 is recommended.
  > For very short series: permutation entropy requires adequate pattern-frequency estimates; for $m = 5$, at least $n \approx 600$ is recommended.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c6ceab70fa21302c` [procedure_step] (literature_supported) — The run_triage function with include_extended_fingerprint=True additively attaches extended_forecastability_analysis for non-exogenous routes only.
  > `run_triage(..., include_extended_fingerprint=True)` additively attaches `extended_forecastability_analysis` for non-exogenous routes only.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c9890cfbb1818b09` [representation] (literature_supported) — The drift method is equivalent to drawing a line between the first and last observation, and extrapolating it into the future.
  > This is equivalent to drawing a line between the first and last observation, and extrapolating it into the future.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-ca2565db6e11ee00` [decision] (literature_supported) — Downstream model families or framework-specific settings should only be recommended after completing forecastability triage.
  > Only then recommend downstream model families or framework-specific settings.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-cc4810c2ca7437f8` [check] (literature_supported) — F3 should be avoided as a standalone triage decision because F3 produces a curve and a lookback recommendation, not a scalar forecastability score.
  > As a standalone triage decision: F3 produces a curve and a lookback recommendation, not a scalar forecastability score.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-cd1a55d4e7a8307b` [procedure_step] (literature_supported) — F1 should be used when one needs to know which forecast horizons carry detectable predictive signal above the noise floor.
  > When you need to know which forecast horizons carry detectable predictive signal above the noise floor.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-cdcf82289f074548` [procedure_step] (literature_supported) — ForecastabilityAnalyzer and ForecastabilityAnalyzerExog support method="te" for raw-curve analysis and TE surrogate significance bands.
  > `src/forecastability/pipeline/analyzer.py`: `ForecastabilityAnalyzer` and `ForecastabilityAnalyzerExog` support `method="te"` for raw-curve analysis and TE surrogate significance bands.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-cdf54414ca49d7ae` [concept] (literature_supported) — The model_now field is an immediate model-complexity recommendation with values HIGH, MEDIUM, LOW, or NONE.
  > `model_now` `str` Immediate model-complexity recommendation (HIGH / MEDIUM / LOW / NONE)
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ce46420d81fcae47` [concept] (literature_supported) — Exogenous screening with FDR (F8) answers the question of which external drivers add genuine predictive value after redundancy.
  > Exogenous screening with FDR (F8) Which external drivers add genuine predictive value after redundancy?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-cf09aef4711cd974` [concept] (literature_supported) — The univariate evaluation dataset comprises 8 canonical series: sine_wave, air_passengers, henon_map, simulated_stock_returns, bitcoin_returns, gold_returns, crude_oil_returns, and aapl_returns.
  > Dataset: 8 canonical univariate series (`sine_wave`, `air_passengers`, `henon_map`, `simulated_stock_returns`, `bitcoin_returns`, `gold_returns`, `crude_oil_returns`, `aapl_returns`).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d1909260cd634bb1` [concept] (literature_supported) — Forecastability profile (F1) answers the question of which horizons carry usable predictive information.
  > Forecastability profile (F1) Which horizons carry usable predictive information?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d59a340be97ced6a` [procedure_step] (literature_supported) — When alpha is None, a bare array is returned unless result_object=True, which yields a CcfResult with confint set to None.
  > When alpha is None a bare array is returned unless result_object=True, which additionally yields a CcfResult with confint set to None.
  (documentation, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.ccf.html, published None, independence ind-s-5114732bc45e7988, corroboration 1)
- `c-d6075340ab1388b0` [concept] (literature_supported) — The `ForecastPrepContract` never imports any downstream library.
  > It never imports any downstream library.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d6cdaea3e59d9c21` [concept] (literature_supported) — src/forecastability/services/ contains internal builder and orchestration helpers used by analyzers and use cases.
  > Internal builder and orchestration helpers used by analyzers and use cases
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d7d073c08a1e9cc5` [procedure_step] (literature_supported) — In rolling-origin evaluation, diagnostics should be computed on train windows only.
  > In rolling-origin evaluation, compute diagnostics on train windows only.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d84848d14a859e2f` [concept] (literature_supported) — Forecasts can later be compared with actual outcomes.
  > These forecasts can later be compared with actual outcomes.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-dd5237c875719d40` [expectancy] (literature_supported) — The naïve method works quite well for economic and financial time series, which often have patterns that are difficult to reliably and accurately predict.
  > This method works quite well for economic and financial time series, which often have patterns that are difficult to reliably and accurately predict.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-dda0cdb18821e98d` [norm] (literature_supported) — Linear_residual should be kept as baseline for all backend studies.
  > Keep `linear_residual` as baseline for all backend studies.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-deaeadb0c2b363e5` [procedure_step] (literature_supported) — Downstream model families or framework-specific settings should be recommended only after triage is completed.
  > Only then recommend downstream model families or framework-specific settings.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-df7d9e32c7e00f9b` [concept] (literature_supported) — The triage package contains models for forecastability profile, predictive info learning curve, spectral predictability, complexity band, Lyapunov, and theoretical limit diagnostics.
  > `forecastability_profile.py`, `predictive_info_learning_curve.py`, `spectral_predictability.py`, `complexity_band.py`, `lyapunov.py`, `theoretical_limit_diagnostics.py`
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e0043c2395d5a61b` [strategy] (literature_supported) — Selection of a forecasting method should be based on objectives and conditions such as available data.
  > Selection of a method should be based on your objectives and your conditions (data etc.).
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-e02c895a5d894eb8` [procedure_step] (literature_supported) — If a true mutual information estimate turns out to be negative, it is replaced by zero.
  > True mutual information can't be negative. If its estimate turns out to be negative, it is replaced by zero.
  (documentation, https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.mutual_info_regression.html, published None, independence ind-s-ca7d54da5b087ed3, corroboration 1)
- `c-e07ea24b3382ccfe` [concept] (literature_supported) — The lagged-exogenous triage surface classifies drivers by lag role and emits a sparse lag map that can be used for downstream tensor construction.
  > The lagged-exogenous surface classifies drivers by lag role and emits a sparse lag map that can be used for downstream tensor construction.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e0fbcad3a460593e` [concept] (literature_supported) — metrics/metrics.py is the core AMI and pAMI computation surface.
  > `metrics/metrics.py` is the core AMI and pAMI computation surface.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e420ae6d57973014` [decision] (literature_supported) — Univariate forecastability triage asks whether the signal is closer to noise, short-memory, seasonal, or structured.
  > Is the signal closer to noise, short-memory, seasonal, or structured?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e597cc0f6e1f3e54` [strategy] (literature_supported) — The xami_sparse selector is a triage layer that cheaply prunes redundant lags to reduce the feature tensor.
  > `xami_sparse` is a **triage layer** - it cheaply prunes redundant lags to reduce the feature tensor.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e65cb947aa2ae2da` [strategy] (literature_supported) — When the task is time-series forecasting, one should not jump directly to model fitting but should start with forecastability triage first.
  > When the task is time-series forecasting, do not jump directly to model fitting. Start with forecastability triage first
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e6b24e03603d4113` [concept] (literature_supported) — src/forecastability/pipeline/ contains analyzer facade, canonical workflow helpers, and rolling-origin evaluation support.
  > `analyzer.py`, `pipeline.py`, `rolling_origin.py` Analyzer facade, canonical workflow helpers, and rolling-origin evaluation support
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e780957704ac90e7` [concept] (literature_supported) — Batch diagnostic ranking (F7) answers the question of which of 50+ signals should be modeled first.
  > Batch diagnostic ranking (F7) Which of my 50+ signals should I model first?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-eaa24c568cd85c8f` [decision] (literature_supported) — If a time series is believed to have seasonality, the seasonal naïve approach may be more appropriate where forecasts are equal to the value from last season.
  > If the time series is believed to have seasonality, the seasonal naïve approach may be more appropriate where the forecasts are equal to the value from last season.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-ec5f71c99ae25d10` [strategy] (literature_supported) — Downstream forecasting frameworks should be used after triage, not instead of triage.
  > Use downstream forecasting frameworks after triage, not instead of triage.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ed73856bc95ae1b5` [concept] (literature_supported) — src/forecastability/exog_benchmark.py provides exogenous benchmark helpers used by benchmark workflows.
  > Exogenous benchmark helpers used by benchmark workflows
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-edc181681f54f407` [concept] (literature_supported) — pipeline/rolling_origin.py contains rolling-origin split helpers used by evaluation workflows.
  > `pipeline/rolling_origin.py` contains rolling-origin split helpers used by evaluation workflows.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ee281471cae8ddba` [concept] (literature_supported) — The naïve forecasting method is only suitable for time series data.
  > This forecasting method is only suitable for time series data.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-eee22c262b329887` [concept] (literature_supported) — Quantitative forecasting methods are usually applied to short- or intermediate-range decisions.
  > These methods are usually applied to short- or intermediate-range decisions.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-ef33c4bdb77a05a6` [rationale] (literature_supported) — Separation of diagnostics and forecast error computation on different windows is mandatory to prevent leakage.
  > This separation is mandatory to prevent leakage.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f17826be9ca6c52d` [strategy] (literature_supported) — When numeric correctness matters, users should trace back to `TriageResult` and the stable package facade.
  > When numeric correctness matters, trace back to `TriageResult` and the stable package facade.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f30a856322e2431f` [concept] (literature_supported) — The default_epsilon parameter is a fallback threshold when surrogates are not requested.
  > `default_epsilon` Fallback threshold when surrogates are not requested
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f501b3f688f6f5ad` [check] (literature_supported) — F1 should be avoided for series shorter than approximately 3 times the maximum evaluation horizon.
  > For series shorter than the recommended minimum (approximately 3× the maximum evaluation horizon).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f516c76b6795b5cd` [concept] (literature_supported) — The triage workflow uses deterministic inputs including AR(1), white noise, trend+seasonal, and exogenous AR(1)+noise.
  > Dataset: deterministic triage regression inputs in [../tests/test_triage_regression.py](../tests/test_triage_regression.py) (AR(1), white noise, trend+seasonal, and exogenous AR(1)+noise)
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f5e3811c6f3ec6c0` [concept] (literature_supported) — Forecasting is the process of making predictions based on past and present data.
  > Forecasting is the process of making predictions based on past and present data.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-f7cbb38a2f9f913d` [decision] (literature_supported) — Forecastability triage should determine whether there is seasonal structure worth modeling.
  > Is there a seasonal structure worth modeling?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f803ec1b7d275059` [representation] (literature_supported) — The PacfResult object contains pacf field as an ndarray of partial autocorrelations for lags 0, 1, ..., nlags with shape (nlags+1,).
  > pacfndarrayThe partial autocorrelations for lags 0, 1, ..., nlags. Shape (nlags+1,).
  (documentation, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html, published None, independence ind-s-5114732bc45e7988, corroboration 1)
- `c-f978f65a7fd92fe2` [concept] (literature_supported) — src/forecastability/diagnostics/ contains significance bands, conditional-MI backends, spectral helpers, and regression tooling.
  > `surrogates.py`, `cmi.py`, `spectral_utils.py`, `diagnostic_regression.py` Significance bands, conditional-MI backends, spectral helpers, and regression tooling
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f9b3d12bbe889e57` [strategy] (literature_supported) — The recommended workflow is data, forecastability triage, lag/driver/readiness diagnostics, ForecastPrepContract, then downstream model search, rather than data, model search, tuning, more features, more compute.
  > This package encourages a different workflow: data → forecastability triage → lag / driver / readiness diagnostics → ForecastPrepContract → downstream model search
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-fb45badd6b7c3556` [concept] (literature_supported) — The average approach can be used for cross-sectional data when predicting unobserved values.
  > the average approach can also be used for cross-sectional data (when we are predicting unobserved values; values that are not included in the data set).
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-fc362dadb96ec184` [concept] (literature_supported) — The n_surrogates parameter controls surrogate-band accuracy for epsilon resolution.
  > `n_surrogates` Controls surrogate-band accuracy for epsilon resolution
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-fe92eff22673fb46` [procedure_step] (literature_supported) — The random_state parameter determines random number generation for adding small noise to continuous variables in order to remove repeated values.
  > Determines random number generation for adding small noise to continuous variables in order to remove repeated values.
  (documentation, https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.mutual_info_regression.html, published None, independence ind-s-ca7d54da5b087ed3, corroboration 1)
- `c-febdf28d0cc17c0a` [procedure_step] (literature_supported) — After triage, fingerprint, and lagged-exog analysis, users call `build_forecast_prep_contract()` to convert triage outputs into a `ForecastPrepContract`.
  > After triage, fingerprint, and lagged-exog analysis, call `build_forecast_prep_contract()` to convert triage outputs into a `ForecastPrepContract`
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)

### Synthetic / rejected claims

- `c-09ef2653cbff9d0c` [concept] (synthetic_extrapolation) — The Largest Lyapunov Exponent (F5) is an experimental feature that is numerically fragile, excluded from automated triage decisions, and gated behind experimental: true in the config. (no located evidence)
- `c-0f06a9238ffc8295` [procedure_step] (synthetic_extrapolation) — directness_ratio should be used for portfolio-level triage or quick comparison between windows, sensors, or assets. (no located evidence)
- `c-0f2d6cc9aeae4292` [check] (synthetic_extrapolation) — For forecast evaluation, diagnostics must be computed on each rolling-origin training window only, not on the full series. (no located evidence)
- `c-1614a21ff92e85d9` [procedure_step] (synthetic_extrapolation) — Predictive info learning curves (F3) should be used for lookback or window-length selection before model training. (no located evidence)
- `c-17c148f937219247` [check] (synthetic_extrapolation) — F4 should be avoided as the sole forecastability measure because Ω misses nonlinear dependence entirely.
  > As the sole forecastability measure: Ω misses nonlinear dependence entirely.
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md)
- `c-1ca66d2af1a9829d` [procedure_step] (synthetic_extrapolation) — Spectral predictability (F4) should be used when AMI is high but you want to check if simple linear models suffice. (no located evidence)
- `c-1df17d2ac455bf82` [decision] (synthetic_extrapolation) — Forecastability triage should determine when the workflow should abstain and fall back to baselines.
  > When should the workflow abstain and fall back to baselines?
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md)
- `c-28faccaaa50a0647` [expectancy] (synthetic_extrapolation) — With defaults min_pairs_ami=30, min_pairs_pami=50, and H=100, pAMI requires N ≥ 201. (no located evidence)
- `c-2d6b67e82a4812a6` [decision] (synthetic_extrapolation) — Forecastability triage should identify which target lags are informative. (no located evidence)
- `c-328e920b79626629` [decision] (synthetic_extrapolation) — Univariate forecastability triage asks which lags should be considered before creating features.
  > Which lags should be considered before creating features?
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md)
- `c-35b01c144d543653` [procedure_step] (synthetic_extrapolation) — Largest Lyapunov exponent (F5) should be used for expert-level chaos detection and experimental use only. (no located evidence)
- `c-36e01cde169d4919` [concept] (synthetic_extrapolation) — The review_horizons field contains all informative horizons and represents model building targets.
  > `review_horizons` `list[int]` All informative horizons - model building targets
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md)
- `c-379b908d63a69bf4` [procedure_step] (synthetic_extrapolation) — Known-future features may be selected at k=0, but only via explicit known_future_drivers opt-in in run_lagged_exogenous_triage. (no located evidence)
- `c-3a1d2ce17e739515` [failure_mode] (synthetic_extrapolation) — The power-zero failure mode of spectral surrogate tests is a known limitation, not a defect in the profile logic. (no located evidence)
- `c-427a5424792b95fa` [decision] (synthetic_extrapolation) — Forecastability triage should identify which horizons contain useful information. (no located evidence)
- `c-48d9873535ca4971` [procedure_step] (synthetic_extrapolation) — pAMI should be used after AMI is non-trivial and you need direct vs mediated lag structure. (no located evidence)
- `c-5672faba3cb1daeb` [procedure_step] (synthetic_extrapolation) — Exogenous analysis should be used for driver screening before multivariate forecasting or feature engineering. (no located evidence)
- `c-59faa7aac89b2643` [procedure_step] (synthetic_extrapolation) — When fft is True, the ccf function uses FFT convolution. (no located evidence)
- `c-5e3bb865d5238f2d` [procedure_step] (synthetic_extrapolation) — Entropy-based complexity (F6) should be used for complexity-band screening before choosing model family. (no located evidence)
- `c-60be8baf7ece3e59` [procedure_step] (synthetic_extrapolation) — F6 should be used alongside F5 when enabled for convergence evidence on chaos versus stochasticity.
  > Alongside F5 (when enabled) for convergence evidence on chaos vs stochasticity.
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md)
- `c-647f394fe039ee6b` [concept] (synthetic_extrapolation) — F5 measures the average rate of exponential divergence of nearby trajectories in a reconstructed phase space, yielding a positive lambda value that is consistent with chaotic dynamics, but stochastic noise can also produce positive values.
  > The average rate of exponential divergence of nearby trajectories in a reconstructed phase space (Takens delay embedding + Rosenstein algorithm), yielding $\hat{\lambda}$: positive values are *consistent with* chaotic dynamics, but stochastic noise can also produce positive values.
  (verdict insufficient [scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md)
- `c-6da3fb106482b84e` [procedure_step] (synthetic_extrapolation) — IT limit diagnostics (F2) should be used after forecastability profile and when 'how much can we gain?' matters. (no located evidence)
- `c-71d9addf98d49842` [procedure_step] (synthetic_extrapolation) — When no lags clear the surrogate band, epsilon is set above the curve maximum so that informative_horizons is empty.
  > When no lags clear the surrogate band, $\varepsilon$ is set above the curve maximum so that `informative_horizons` is empty.
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md)
- `c-760de6e84d01ea9a` [procedure_step] (synthetic_extrapolation) — F1 should be used as the primary output for any univariate forecastability assessment.
  > As the primary output for any univariate forecastability assessment.
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md)
- `c-77d15027dacecdcf` [strategy] (synthetic_extrapolation) — Wherever phase-randomised surrogate bands already exist via significance_service, the lagged-exogenous flow reuses them, including at k = 0 once the lag-range extension is in place.
  > Wherever phase-randomised surrogate bands already exist (via `significance_service`), the lagged-exogenous flow reuses them - including at $k = 0$ once the lag-range extension is in place.
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md)
- `c-7895f8100ac932cc` [procedure_step] (synthetic_extrapolation) — When surrogates are computed, epsilon is set to the minimum AMI value among lags whose AMI exceeds the 97.5th percentile of the surrogate distribution.
  > When surrogates are computed** - $\varepsilon$ is set to the minimum AMI value among lags whose AMI exceeds the 97.5th percentile of the surrogate distribution.
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md)
- `c-7de1550bc5925cda` [failure_mode] (synthetic_extrapolation) — Look-ahead leakage in rolling-origin evaluation is silent and produces optimistic forecastability scores without any error message. (no located evidence)
- `c-864136a165f44405` [concept] (synthetic_extrapolation) — The informative_horizons field contains horizons where forecastability is at least epsilon.
  > `informative_horizons` `list[int]` $\mathcal{H}_\varepsilon$ - horizons where $F(h) \ge \varepsilon$
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md)
- `c-90c157f8170fcf0b` [check] (synthetic_extrapolation) — F3 should be avoided for embedding dimension k greater than 5-8 unless the series is very long, as kNN estimators degrade in high-dimensional spaces and a hard cap of k_max equals 8 is enforced.
  > For embedding dimension $k > 5$-$8$ unless the series is very long ($n > 1000$): kNN estimators degrade in high-dimensional spaces; a hard cap $k_{\max} = 8$ is enforced.
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md)
- `c-930fff0bcfa413e0` [strategy] (synthetic_extrapolation) — Standard cross-correlation is a cheap linear baseline that retains sign and covers k = 0 as a contemporaneous diagnostic reference. (no located evidence)
- `c-9850da0617f4e09b` [failure_mode] (synthetic_extrapolation) — For near-deterministic periodic signals like pure sinusoids, phase randomisation surrogates carry nearly identical spectral structure, making it impossible to detect forecastability above the null. (no located evidence)
- `c-98ae5224a60f2d69` [concept] (synthetic_extrapolation) — Naïve forecasts are the most cost-effective forecasting model.
  > Naïve forecasts are the most cost-effective forecasting model, and provide a benchmark against which more sophisticated models can be compared.
  (verdict insufficient, https://en.wikipedia.org/wiki/Forecasting)
- `c-9b41a55db3e3bebe` [check] (synthetic_extrapolation) — F5 should always be combined with AMI/pAMI evidence and the F6 complexity band before drawing any conclusion. (no located evidence)
- `c-a6eeecaab75237bf` [concept] (synthetic_extrapolation) — Forecastability at horizon h is defined as the mutual information between the future target and the current information set. (no located evidence)
- `c-a7e585ad25481676` [failure_mode] (synthetic_extrapolation) — The kNN MI estimator with n_neighbors=8 is consistent but has finite-sample variance, and may produce noise-lifted individual AMI values at small sample sizes or very long lags. (no located evidence)
- `c-a99174c8795ac7ab` [procedure_step] (synthetic_extrapolation) — When no surrogates are available, epsilon falls back to the default_epsilon parameter with a default value of 0.05 nats, or to an explicit caller-supplied override.
  > When no surrogates are available** - $\varepsilon$ falls back to the `default_epsilon` parameter (default `0.05` nats), or to an explicit caller-supplied override.
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md)
- `c-b1add143d8062bf9` [procedure_step] (synthetic_extrapolation) — Forecastability profile (F1) should be used after AMI curves exist and before choosing which horizons to model. (no located evidence)
- `c-b872c3c704d115ee` [procedure_step] (synthetic_extrapolation) — AMI should be used as a first-pass screening of a target signal before model search. (no located evidence)
- `c-bbb3d521c1738b03` [expectancy] (synthetic_extrapolation) — Occasional false-positive horizons in informative_horizons are expected, especially for AR(1) processes at long lags. (no located evidence)
- `c-c94a4b07858e75d2` [check] (synthetic_extrapolation) — F3 should be avoided for non-stationary series because random-walk-like dynamics produce inflated estimates that grow with k without plateauing.
  > For non-stationary series: random-walk-like dynamics produce inflated estimates that grow with $k$ without plateauing.
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md)
- `c-cec2eb00bb6ee77c` [concept] (synthetic_extrapolation) — When alpha is not None or result_object is True, pacf returns a PacfResult object; when alpha is None and result_object is False, it returns a bare array. (no located evidence)
- `c-d151e867f0c6a0f5` [decision] (synthetic_extrapolation) — Univariate forecastability triage asks whether the target has informative lags.
  > Typical questions: - Does the target have informative lags?
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md)
- `c-d3941696d9a6d660` [norm] (synthetic_extrapolation) — Epsilon should be defined relative to the surrogate upper band, not as a global absolute constant. (no located evidence)
- `c-d4ea8aaf5d3ce898` [rationale] (synthetic_extrapolation) — An absolute threshold for epsilon risks including noise lags or excluding genuinely informative ones as signal strength varies across series. (no located evidence)
- `c-d77a6f54c4bcadbd` [failure_mode] (synthetic_extrapolation) — Series with near-deterministic periodic signals will exhibit empty informative_horizons and model_now set to NONE even when they are perfectly predictable. (no located evidence)
- `c-e0bda84ce17e35c0` [procedure_step] (synthetic_extrapolation) — Batch diagnostic ranking (F7) should be used for portfolio-level signal prioritization. (no located evidence)
- `c-e4cb13f070e997ab` [procedure_step] (synthetic_extrapolation) — Triage should be used as a standardized entry point for production-like checks and repeatable diagnostics. (no located evidence)
- `c-e7db4ab37cf3d1fb` [procedure_step] (synthetic_extrapolation) — Exogenous screening with FDR (F8) should be used for multivariate feature selection before model engineering. (no located evidence)
- `c-fcffa8caf051f527` [concept] (synthetic_extrapolation) — ForecastPrepContract is a typed hand-off containing target lags, seasonal hints, covariate roles, caution flags, and advisory routing labels for downstream modeling code. (no located evidence)

### UNKNOWN / thin / unverified / unexamined slots

- none
