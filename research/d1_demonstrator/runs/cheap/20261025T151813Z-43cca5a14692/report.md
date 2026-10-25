# N2a reconstruction report (complete)

369 claims span-located, 369 verified, decoy false-accept rate 40%, cost $0.7118. Verifier family: openai.

## Sources and clusters

| metric | value |
| --- | --- |
| sources fetched | 16 |
| fetch failures | 0 |
| independent clusters | 1 |
| largest cluster share | 100% |

## Supported claims by source kind/tier

| kind | tier | n supporting-evidence items |
| --- | --- | --- |
| documentation | open | 344 |

### Corroboration distribution (supported claims)

| corroboration | n claims |
| --- | --- |
| 1 | 344 |

## Slots by status

| status | n |
| --- | --- |
| thin | 34 |
| unknown | 6 |

## Decoy false-accept rate by mutation type (Wilson 95% CI)

| mutation | attempted | valid | false accepts | rate | 95% CI |
| --- | --- | --- | --- | --- | --- |
| negation | 10 | 10 | 3 | 30% | [11%, 60%] |
| number | 10 | 10 | 4 | 40% | [17%, 69%] |
| scope | 10 | 10 | 5 | 50% | [24%, 76%] |

## Area: Practical application and examples

### Supported claims

- `c-04d54d1447edcb23` [procedure_step] (literature_supported) — F3 should be used to select the lookback window for a forecasting model by using the recommended plateau as a principled starting point.
  > When selecting the lookback window for a forecasting model: use the recommended plateau $k^*$ as a principled starting point.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-052db13533fa9643` [strategy] (literature_supported) — When the task is time-series forecasting, do not jump directly to model fitting; start with forecastability triage first.
  > When the task is time-series forecasting, do not jump directly to model fitting. Start with forecastability triage first:
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-09a56c0db2a8bbc8` [strategy] (literature_supported) — The recommended workflow for forecasting projects should be: data → forecastability triage → lag / driver / readiness diagnostics → ForecastPrepContract → downstream model search.
  > This package encourages a different workflow: data → forecastability triage → lag / driver / readiness diagnostics → ForecastPrepContract → downstream model search
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0b887799f98f043c` [concept] (literature_supported) — Both nonlinear couplings create statistically dependent joint distributions even though the marginal covariance is zero.
  > Both couplings create statistically dependent joint distributions even though the marginal covariance is zero.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-16f05d840158bd7e` [cue] (literature_supported) — The is_non_monotone flag should be inspected by routines that assume monotone decay before applying simplifying assumptions.
  > Routines that assume monotone decay (such as naive exponential smoothers) should inspect this flag before applying simplifying assumptions.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-1c1bb61b51070c7f` [rationale] (literature_supported) — Separation of diagnostics computation and forecast error computation on different windows is mandatory to prevent leakage.
  > This separation is mandatory to prevent leakage.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-1d5e845d6532a20c` [norm] (literature_supported) — From arXiv:2601.10006, frequency-specific horizon caps should be used: Yearly 6, Quarterly 8, Monthly 18, Weekly 13, Daily 14, Hourly 48.
  > Use frequency-specific horizon caps: Yearly 6, Quarterly 8, Monthly 18, Weekly 13, Daily 14, Hourly 48.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3e06b2d68146d02f` [procedure_step] (literature_supported) — In rolling-origin evaluation, AMI, pAMI, and all F1-F8 diagnostics are computed on the training window up to each rolling origin, with no diagnostic touching the post-origin holdout.
  > AMI, pAMI, and all F1-F8 diagnostics are computed on the training window up to each rolling origin. No diagnostic touches the post-origin holdout.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-42aca8abc47b432c` [procedure_step] (literature_supported) — The walkthrough notebooks in notebooks/walkthroughs/ should be run before using the notebooks in notebooks/triage/, which are deep dives rather than first-stop onboarding.
  > Use the `notebooks/triage/` notebooks only after the walkthroughs; they are deep dives, not first-stop onboarding.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-57756095892fe1d8` [procedure_step] (literature_supported) — Forecastability triage should cover readiness, leakage risk, informative horizons, primary lags, seasonality structure, and covariate informativeness before recommending downstream model families or framework-specific settings.
  > Start with forecastability triage first: readiness, leakage risk, informative horizons, primary lags, seasonality structure, and covariate informativeness. Only then recommend downstream model families or framework-specific settings.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5e6c39566b0cc4f6` [procedure_step] (literature_supported) — In rolling-origin evaluation, forecast errors and accuracy metrics are computed on the post-origin holdout window only.
  > Forecast errors and accuracy metrics are computed on the post-origin holdout window only.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5ff63882db181126` [decision] (literature_supported) — Escalation should occur only when nonlinear backends improve diagnostic consistency across datasets.
  > Escalate only when nonlinear backends improve diagnostic consistency across datasets.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6091843095dfaffa` [procedure_step] (literature_supported) — F7 should be used when producing a reproducible ranking artefact for a report or downstream pipeline.
  > When producing a reproducible ranking artefact for a report or downstream pipeline.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-67e5eac5fb8bec5e` [procedure_step] (literature_supported) — F5 should only be used for exploratory research as one piece of converging evidence alongside F1 and F6.
  > Exploratory research only: as one piece of converging evidence that a series may exhibit chaotic dynamics, always alongside F1 and F6.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-67e99a77efcb1ef0` [strategy] (literature_supported) — When the task is time-series forecasting, forecastability triage should be started before model fitting.
  > When the task is time-series forecasting, do not jump directly to model fitting. Start with forecastability triage first
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6c60cbc7e087bdb4` [strategy] (literature_supported) — F2 should be used before investing in complex models because if the limit is low, model engineering gains diminish rapidly.
  > Before investing in complex models: if the limit is low, model engineering gains diminish rapidly.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6c675b36abbcdc51` [procedure_step] (literature_supported) — An 8-variable covariant system is used in the synthetic benchmark for controlled method validation.
  > 8-variable covariant system `generate_covariant_benchmark` in `src/forecastability/utils/synthetic.py` implements an 8-variable ground-truth system used for controlled method validation.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6e81eaa5ab980b86` [strategy] (literature_supported) — Stable lag rankings and small directness-ratio range should be preferred over raw pAMI magnitude.
  > Prefer stable lag rankings and small directness-ratio range over raw pAMI magnitude.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-703f18d903194a6e` [rationale] (literature_supported) — A practitioner should interact with the profile instead of the raw numeric array to avoid re-implementing the threshold logic in downstream code.
  > A practitioner interacts with the profile instead of the raw numeric array to avoid re-implementing the threshold logic in downstream code.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-70db791a682a6218` [procedure_step] (literature_supported) — F7 should be used when screening a large panel of candidate series to prioritise modelling effort.
  > When screening a large panel of candidate series to prioritise modelling effort.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-760675ee1943db9c` [rationale] (literature_supported) — Spearman correlation is near zero for the abs-value coupling because |X| is V-shaped (non-monotone) in X.
  > Spearman is also near zero because $ X $ is V-shaped (non-monotone) in $X$.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-819845eb5ff32edc` [procedure_step] (literature_supported) — F4 should be used for rapid cross-series ranking where a computationally cheap linear-domain signal is sufficient.
  > For rapid cross-series ranking where a computationally cheap linear-domain signal is sufficient.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-872ab3369308aa73` [misconception] (literature_supported) — Most forecasting work begins before determining whether the target has weak memory, whether the horizon matches the signal, whether the best covariates are safe at prediction time, or whether the strongest lags would leak future information.
  > Most forecasting work starts too late. The usual story is familiar. Pick a forecasting library. Generate lag features. Add every covariate that looks plausible. Run a leaderboard. Then discover the target has weak memory, the horizon is mismatched to the signal, the best covariates are unsafe at prediction time, or the strongest lags would leak future information.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8b83dda07034fe22` [procedure_step] (literature_supported) — F8 should be used when you need a principled multiple-testing correction to control false positives across many candidate drivers.
  > When you need a principled multiple-testing correction to control false positives across many candidate drivers.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-92b5a609a6917a27` [procedure_step] (literature_supported) — F7 should be used as the entry point for any multi-series analysis with individual series results remaining accessible.
  > As the entry point for any multi-series analysis; individual series results remain accessible through the batch result object.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-98ac1392720c2bc3` [strategy] (literature_supported) — Multiple noise-linked cases in exogenous screening can be deprioritised early.
  > multiple noise-linked cases can be deprioritised early.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-9d52493e5d0144b7` [procedure_step] (literature_supported) — Known-future features may be selected at k=0 only via the known_future_drivers parameter with explicit opt-in.
  > Such features may be selected at $k=0$, but only via: bundle = run_lagged_exogenous_triage( target, drivers, target_name="target", max_lag=6, n_surrogates=99, random_state=42, known_future_drivers={"holiday_flag": True}, )
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-9dc8eb6218cbf2d9` [procedure_step] (literature_supported) — After forecastability triage, downstream model families or framework-specific settings should be recommended.
  > Only then recommend downstream model families or framework-specific settings.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-9e2fc60c4104e7ee` [rationale] (literature_supported) — Spearman correlation is near zero for the quadratic coupling because X^2 is U-shaped (non-monotone) in X.
  > Spearman is also near zero because $X^2$ is U-shaped (non-monotone) in $X$.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a03a397bdf37dfc0` [failure_mode] (literature_supported) — A quadratic driver with near-zero Pearson correlation can be a strong predictive feature, requiring cross-check with cross_ami.
  > a quadratic driver with near-zero Pearson correlation can be a strong predictive feature; always cross-check with `cross_ami`
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-b37fd1a38ab1ecef` [procedure_step] (literature_supported) — F8 should be used to decide which exogenous variables are worth including in a multivariate model when candidate exogenous variables are available.
  > When candidate exogenous variables are available and you need to decide which, if any, are worth including in a multivariate model.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-b8ac607dea7634ac` [representation] (literature_supported) — Of 8 canonical univariate series evaluated, 2 are classified as forecastability_class=high, 1 is medium, and 5 are low.
  > In the current run, 2/8 series are `forecastability_class=high`, 1/8 is `medium`, and 5/8 are `low`
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-bae7171f5604af2f` [concept] (literature_supported) — The nonlinear driver driver_nonlin_sq couples to target at lag 1 via a centered quadratic function.
  > driver_nonlin_sq` couples to `target` at lag 1 via a centered quadratic: $$\text{target}[t] \mathrel{+}= 0.40 \times (\text{nl}_1[t-1]^2 - \sigma^2_{\text{nl}_1})$$
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-bc32b7223cc33c47` [procedure_step] (literature_supported) — Diagnostics (AMI/pAMI) are computed on each training window only in rolling-origin analysis.
  > Diagnostics (AMI/pAMI) are computed on each training window only.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d7d073c08a1e9cc5` [procedure_step] (literature_supported) — In rolling-origin evaluation, diagnostics should be computed on train windows only.
  > In rolling-origin evaluation, compute diagnostics on train windows only.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-dda0cdb18821e98d` [norm] (literature_supported) — Linear_residual should be kept as baseline for all backend studies.
  > Keep `linear_residual` as baseline for all backend studies.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e5d899d63d4b3d59` [rationale] (literature_supported) — The nonlinear drivers validate that AMI, TE, and GCMI scores remain informative exactly where Pearson and Spearman fail.
  > The nonlinear drivers are included to validate that AMI, TE, and GCMI scores remain informative exactly where Pearson and Spearman fail
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e7fe9c1433304ed0` [norm] (literature_supported) — The same leakage boundary in rolling-origin evaluation applies to exogenous workflows, where CrossAMI must be computed on the training window only.
  > The same leakage boundary applies to exogenous screening (F8): CrossAMI must be computed on the training window only.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ec5f71c99ae25d10` [strategy] (literature_supported) — Downstream forecasting frameworks should be used after triage, not instead of triage.
  > Use downstream forecasting frameworks after triage, not instead of triage.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-efc3c9d42ed99d8e` [procedure_step] (literature_supported) — Forecast errors in rolling-origin analysis are computed on post-origin test window only.
  > Forecast errors are computed on post-origin test window only.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ffcf5952655ac1df` [procedure_step] (literature_supported) — The run_rolling_origin_evaluation() function enforces the train-test leakage boundary internally, but if diagnostics are computed manually outside this function, the caller must enforce the same boundary or introduce look-ahead leakage.
  > The `run_rolling_origin_evaluation()` function enforces this boundary internally. If you compute diagnostics manually outside this function, you must enforce the same boundary. Violating it introduces look-ahead leakage and invalidates the evaluation.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)

### Synthetic / rejected claims

- `c-104662c75c7025ee` [concept] (synthetic_extrapolation) — The nonlinear driver driver_nonlin_abs couples to target at lag 1 via a centered abs-value function.
  > driver_nonlin_abs` couples to `target` at lag 1 via a centered abs-value: $$\text{target}[t] \mathrel{+}= 0.35 \times ( \text{nl}_2[t-1] - \mathbb{E}[ \text{nl}_2 ])$$
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md)
- `c-1ed49ad32232deac` [procedure_step] (synthetic_extrapolation) — Exogenous analysis is used for driver screening before multivariate forecasting or feature engineering. (no located evidence)
- `c-3420ad5fa9523f47` [procedure_step] (synthetic_extrapolation) — IT limit diagnostics is used after forecastability profile exists and when how much we can gain matters. (no located evidence)
- `c-3583fcb123e7844a` [procedure_step] (synthetic_extrapolation) — Forecastability profile is used after AMI curves exist and before choosing which horizons to model. (no located evidence)
- `c-3f6d4075618ade25` [strategy] (synthetic_extrapolation) — The first-stop notebook learning path includes `walkthroughs/00_air_passengers_showcase.ipynb` or `walkthroughs/01_covariant_informative_showcase.ipynb` in the `forecastability-examples` repository. (no located evidence)
- `c-47482c8aa9cdc885` [rationale] (synthetic_extrapolation) — For the abs-value nonlinear coupling, the function |X| is odd, so its expectation over any symmetric distribution is zero, making covariance exactly zero at population level.
  > Abs-value**: $\mathrm{Cov}(X,\, X ) = \mathbb{E}[X \cdot X ] = 0$. The function $X X $ is odd, so its expectation over any symmetric distribution is zero.
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md)
- `c-64b02dfd7dcc18e6` [procedure_step] (synthetic_extrapolation) — selected_for_tensor is impossible at lag=0 by default; known_future_drivers should only be used for variables whose contemporaneous future values are genuinely known at prediction time. (no located evidence)
- `c-6d7ea2576fedbe20` [procedure_step] (synthetic_extrapolation) — pAMI is used after AMI is non-trivial and you need direct vs mediated lag structure. (no located evidence)
- `c-71d64588967b42c9` [representation] (synthetic_extrapolation) — bike_cnt_temp has the strongest useful signal with mean_raw_cross_mi=0.0906 and mean_conditioned_cross_mi=0.0523 with no warning horizons. (no located evidence)
- `c-9c865526504566d2` [procedure_step] (synthetic_extrapolation) — AMI is used as a first-pass screening of a target signal before model search. (no located evidence)
- `c-a703a55c65e75170` [check] (synthetic_extrapolation) — For forecast evaluation, compute diagnostics on each rolling-origin training window only, not on the full series. (no located evidence)
- `c-ac84fa6cd4b77147` [procedure_step] (synthetic_extrapolation) — Entropy-based complexity is used for complexity-band screening before choosing model family. (no located evidence)
- `c-bb0d61cce8c53d35` [procedure_step] (synthetic_extrapolation) — Largest Lyapunov exponent is used for expert-level chaos detection and experimental use only. (no located evidence)
- `c-c661377a7e380c4b` [strategy] (synthetic_extrapolation) — For fast initial screening in causal discovery, prefer `methods=["cross_ami", "gcmi"]` rather than default causal methods. (no located evidence)
- `c-ce3454174a21817d` [procedure_step] (synthetic_extrapolation) — Batch diagnostic ranking is used for portfolio-level signal prioritization. (no located evidence)
- `c-d2ff5da1f5fca4d8` [procedure_step] (synthetic_extrapolation) — Optional narration is used for stakeholder communication when numeric outputs already exist. (no located evidence)
- `c-d70c8a3bf3ee6c48` [procedure_step] (synthetic_extrapolation) — Triage is used as a standardized entry point for production-like checks and repeatable diagnostics. (no located evidence)
- `c-e1da27609b280bef` [procedure_step] (synthetic_extrapolation) — Spectral predictability is used when AMI is high but you want to check if simple linear models suffice. (no located evidence)
- `c-e2780605ca1ecaad` [rationale] (synthetic_extrapolation) — For the quadratic nonlinear coupling, covariance between driver and target is exactly zero at the population level because the odd central moment of any zero-mean symmetric distribution is zero. (no located evidence)
- `c-efc62f765f470747` [failure_mode] (synthetic_extrapolation) — Look-ahead leakage in rolling-origin evaluation is silent and produces optimistic forecastability scores without any error message, requiring users to verify that diagnostics are computed before the origin and scoring after it. (no located evidence)
- `c-f03698069e7a3111` [strategy] (synthetic_extrapolation) — A practitioner should target model evaluation exclusively at horizons in the informative horizon set, as lags outside this set carry no detectable predictive signal above the noise floor.
  > A practitioner should target model evaluation exclusively at horizons in $\mathcal{H}_\varepsilon$ - lags outside this set carry no detectable predictive signal above the noise floor.
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md)
- `c-f44bffbfa95f1040` [procedure_step] (synthetic_extrapolation) — Predictive info learning curves is used for lookback or window-length selection before model training. (no located evidence)
- `c-fec701f7092f70f7` [procedure_step] (synthetic_extrapolation) — Exogenous screening with FDR is used for multivariate feature selection before model engineering. (no located evidence)

### UNKNOWN / thin / unverified / unexamined slots

- concept: thin
- decision: thin
- cue: thin
- check: unknown
- failure_mode: thin
- norm: thin
- rationale: thin
- procedure_step: thin

### Unknown placeholders

- `c-b7fdea204a145ce6` [check] — How is work in Practical application and examples checked for correctness or compliance?

## Area: Extending toolkit functionality

### Supported claims

- `c-007b692334093e05` [norm] (literature_supported) — New user-facing imports should be added through forecastability or forecastability.triage only when committing to compatibility.
  > Add new user-facing imports through `forecastability` or `forecastability.triage` only when you want to commit to compatibility.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-040cb35e6c34f7b5` [norm] (literature_supported) — Any new selector going further than xami_sparse (PMIME-style, PC-stable with driver autohistory) must be introduced under a new method label so that shipped cross_pami and xami_sparse semantics are not silently extended.
  > Any new selector that goes further (PMIME-style, PC-stable with driver autohistory) must be introduced under a **new method label** so that the shipped `cross_pami` and `xami_sparse` semantics are not silently extended.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0e0d118df5b9dbf0` [decision] (literature_supported) — pAMI, exogenous cross-dependence, and scorer-registry abstractions are project additions.
  > pAMI, exogenous cross-dependence, and scorer-registry abstractions are project additions.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-14dda9a7a271377e` [norm] (literature_supported) — Transport concerns should be put in adapters/, not in use cases or metrics code.
  > Put transport concerns in `adapters/`, not in use cases or metrics code.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3615334c41f169d1` [procedure_step] (literature_supported) — The "known_future" tensor_role value is only assigned when the user explicitly opts in via known_future_drivers parameter.
  > The `"known_future"` value is only assigned when the user explicitly opts in via `known_future_drivers={"driver_name": True}`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3abcee0ac5bda578` [concept] (literature_supported) — The CausalGraphPort contract specifies discover(...) -> CausalGraphResult for PCMCI+ style graph discovery.
  > CausalGraphPort` `discover(...) -> CausalGraphResult` PCMCI+ style graph discovery
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3b4cb803f91a96fb` [concept] (literature_supported) — The diagnostics package contains surrogates, CMI backends, spectral helpers, and regression utilities.
  > diagnostics/` Surrogates, CMI backends, spectral helpers, and regression utilities
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-454033f260c0fffc` [concept] (literature_supported) — The rf_residual backend captures nonlinear interactions with moderate tuning burden.
  > rf_residual` Captures nonlinear interactions with moderate tuning burden
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-488f37627b61fae5` [concept] (literature_supported) — The CausalGraphFullPort contract specifies discover(...) -> CausalGraphResult and discover_full(...) -> PcmciAmiResult for PCMCI-AMI full three-phase result path.
  > CausalGraphFullPort` `discover(...) -> CausalGraphResult` and `discover_full(...) -> PcmciAmiResult` PCMCI-AMI full three-phase result path
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-50f023c54f13be90` [norm] (literature_supported) — Any elastic-alignment result would need a new surface, a new method label, and an explicit chronological-causality guard before it could be admitted to a forecasting tensor.
  > Any elastic-alignment result would need a new surface, a new method label, and an explicit chronological-causality guard before it could be admitted to a forecasting tensor.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5484004a1aa89e3f` [norm] (literature_supported) — Agents and MCP do not compute or validate the science; they route or narrate deterministic outputs.
  > Agents and MCP do not compute or validate the science. They route or narrate deterministic outputs.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5e1cf37fab1d0e27` [failure_mode] (literature_supported) — New scorers inherit kNN estimation noise on short series.
  > new scorers inherit kNN estimation noise on short series
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-67ea4dbaf12937fc` [strategy] (literature_supported) — The extra_trees_residual backend is best for stress-testing nonlinear mediation robustness.
  > extra_trees_residual` Strong nonlinear fit with variance reduction from randomized splits Can still overfit noisy short series; less interpretable Stress-testing nonlinear mediation robustness
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-792adbbd1d1fac2a` [representation] (literature_supported) — The pipeline/rolling_origin.py module contains rolling-origin split helpers used by evaluation workflows.
  > `pipeline/rolling_origin.py` contains rolling-origin split helpers used by evaluation workflows.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7f1dd906c98ffd2c` [norm] (literature_supported) — The forecast prep contract never imports any downstream library.
  > It never imports any downstream library.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8063ceeb05310354` [concept] (literature_supported) — The ports package contains protocol-oriented seams for the architecture direction, including causal discovery contracts.
  > ports/` Protocol-oriented seams for the architecture direction, including causal discovery contracts
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8384a9156e43e57e` [norm] (literature_supported) — Deterministic orchestration should be kept in use_cases/ and pipeline/ rather than notebooks or scripts.
  > Keep deterministic orchestration in `use_cases/` and `pipeline/` rather than notebooks or scripts.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8650ddfa1a51868c` [rationale] (literature_supported) — Reliability and variance properties of all profile fields inherit entirely from the underlying MI estimator; improving estimator accuracy propagates automatically to the profile.
  > Reliability and variance properties of all profile fields inherit entirely from the underlying MI estimator; improving estimator accuracy (e.g. raising `n_surrogates`, increasing the sample size, or choosing a better-matched `n_neighbors`) propagates automatically to the profile.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-86c5a454caa43627` [norm] (literature_supported) — services/ should be treated as internal helpers, not as a third public API layer.
  > Treat `services/` as internal helpers, not as a third public API layer.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8eabb66a53df1fee` [procedure_step] (literature_supported) — AMI and pAMI should be kept horizon-specific and not pre-aggregated before triage.
  > Keep AMI and pAMI horizon-specific; do not pre-aggregate before triage.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a89c711eece4c314` [norm] (literature_supported) — ports/ should be used for protocol-style seams when a collaborator needs to be substituted or isolated.
  > Use `ports/` for protocol-style seams when a collaborator needs to be substituted or isolated.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c17b7d6f8b9bc557` [norm] (literature_supported) — DTW methods remain out of scope for lagged-exogenous triage until a separate plan justifies a constrained forecasting-causal use.
  > They remain out of scope for lagged-exogenous triage until a separate plan justifies a constrained forecasting-causal use.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-cea1019b18f4e03e` [concept] (literature_supported) — The services package contains internal builder/orchestration helpers used by analyzers and use cases.
  > services/` Internal builder/orchestration helpers used by analyzers and use cases
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d1e60fd3fb5965cd` [representation] (literature_supported) — The pipeline/analyzer.py module contains ForecastabilityAnalyzer, ForecastabilityAnalyzerExog, and AnalyzeResult.
  > `pipeline/analyzer.py` contains `ForecastabilityAnalyzer`, `ForecastabilityAnalyzerExog`, and `AnalyzeResult`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d842abf5a063991d` [norm] (literature_supported) — Adapters should not become a second business-logic layer.
  > Adapters should not become a second business-logic layer.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)

### Synthetic / rejected claims

- `c-0426d5b08b273120` [decision] (synthetic_extrapolation) — The paper validates AMI only. (no located evidence)
- `c-089391d4f6c03760` [procedure_step] (synthetic_extrapolation) — The Transfer Entropy compatibility facade is in src/forecastability/services/transfer_entropy_service.py.
  > src/forecastability/services/transfer_entropy_service.py`: compatibility facade re-exporting the diagnostics functions.
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md)
- `c-0bbcaac2cc804586` [failure_mode] (synthetic_extrapolation) — The extra_trees_residual backend can still overfit noisy short series and is less interpretable.
  > extra_trees_residual` Strong nonlinear fit with variance reduction from randomized splits Can still overfit noisy short series; less interpretable
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md)
- `c-232ffbb560f931a5` [concept] (synthetic_extrapolation) — Lag-Aware ModMRMR is used when a forecast-safe sparse covariate-lag selector is needed before the ForecastPrepContract hand-off. (no located evidence)
- `c-33600811a3a4d92a` [procedure_step] (synthetic_extrapolation) — Exogenous requests do not include an `extended_forecastability_analysis` field rather than pretending exogenous-aware extended analysis exists. (no located evidence)
- `c-402faff4caf3ccfb` [failure_mode] (synthetic_extrapolation) — When routing is based on AMI geometry and AMI geometry is disabled or unavailable for the input, the output stays descriptive-only and does not emit routing-grade family recommendations. (no located evidence)
- `c-4690274119365806` [decision] (synthetic_extrapolation) — Largest Lyapunov exponent estimation is an experimental diagnostic gated behind experimental: true in config and not included in automated triage decisions. (no located evidence)
- `c-509007f905a6b39e` [norm] (synthetic_extrapolation) — A selected_for_tensor=True flag at k=0 is impossible by default and requires an explicit known_future_drivers opt-in at the use-case layer as an intentional chronological-causality guard. (no located evidence)
- `c-8a5ac1ca9abace23` [failure_mode] (synthetic_extrapolation) — The rf_residual backend has higher variance and compute than linear.
  > rf_residual` Captures nonlinear interactions with moderate tuning burden Higher variance and compute than linear
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md)
- `c-a5c8c2ffc1688127` [concept] (synthetic_extrapolation) — The extra_trees_residual backend has strong nonlinear fit with variance reduction from randomized splits.
  > extra_trees_residual` Strong nonlinear fit with variance reduction from randomized splits
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md)
- `c-b1e2f46637e68dfc` [strategy] (synthetic_extrapolation) — The `pcmci` and `pcmci_ami` causal discovery methods are optional and computationally expensive, designed for confirmatory causal screening after a fast pairwise pass, not as a default first step. (no located evidence)
- `c-bcbf695d48ed287c` [concept] (synthetic_extrapolation) — Lag-Aware ModMRMR selects sparse covariate lags that are informative, non-redundant against already selected features, and legal for the forecast horizon. (no located evidence)
- `c-c0fb77683f1d5619` [procedure_step] (synthetic_extrapolation) — When causal discovery is needed, using `pcmci_ami_ci_test="parcorr"` provides a 50-200× speedup over the default `"knn_cmi"` backend. (no located evidence)
- `c-d141380c5aaf5c59` [concept] (synthetic_extrapolation) — The triage pipeline includes stable diagnostics consisting of forecastability profiles, theoretical information ceilings, predictive-information learning curves, spectral predictability indices, permutation-entropy and spectral-entropy complexity bands, batch diagnostic ranking, and enhanced exogenous screening with redundancy detection. (no located evidence)
- `c-dc2967dbddfbaaac` [strategy] (synthetic_extrapolation) — The rf_residual backend is best for nonlinear systems where linear residualization under-fits.
  > rf_residual` Captures nonlinear interactions with moderate tuning burden Higher variance and compute than linear Nonlinear systems where linear residualization under-fits
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md)
- `c-ff1c93a67a72e6f4` [concept] (synthetic_extrapolation) — Agent payload adapters provide structured Pydantic result models for deterministic consumption by agents, API consumers, or downstream pipelines. (no located evidence)

### UNKNOWN / thin / unverified / unexamined slots

- concept: thin
- decision: thin
- cue: unknown
- check: unknown
- failure_mode: thin
- norm: thin
- rationale: thin
- procedure_step: thin

### Unknown placeholders

- `c-9826fd873d681840` [cue] — What observable features of a situation signal that Extending toolkit functionality applies or needs a different response?
- `c-ed27a52d0bd653b0` [check] — How is work in Extending toolkit functionality checked for correctness or compliance?

## Area: Setting up and running the toolkit

### Supported claims

- `c-009688818ddbd942` [strategy] (literature_supported) — Users should use the facades when they need deterministic triage, analyzers, typed results, config models, scorer registry access, or batch triage types.
  > Use these facades when you need deterministic triage, analyzers, typed results, config models, scorer registry access, or batch triage types.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-04dcf0bed80727d4` [expectancy] (literature_supported) — The triage workflow supports prioritisation and method selection, not guaranteed downstream forecast accuracy gains.
  > This workflow supports prioritisation and method selection, not guaranteed downstream forecast accuracy gains.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-07070096de4d9c45` [prerequisite] (literature_supported) — F3 enforces a hard cap on embedding dimension of k_max = 8 for k > 5-8 unless the series is very long (n > 1000).
  > For embedding dimension $k > 5$-$8$ unless the series is very long ($n > 1000$): kNN estimators degrade in high-dimensional spaces; a hard cap $k_{\max} = 8$ is enforced.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0bfdaf4bd0e61712` [concept] (literature_supported) — The TriageRequest default_epsilon parameter is a fallback threshold when surrogates are not requested.
  > `default_epsilon` Fallback threshold when surrogates are not requested
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0d56f24961747654` [norm] (literature_supported) — The CLI is a beta transport surface that supports `triage`, `triage-batch`, and `list-scorers` commands.
  > The CLI supports `triage`, `triage-batch`, and `list-scorers`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0f314c31b3365a47` [concept] (literature_supported) — The profile is exposed on the TriageResult returned by run_triage().
  > It is constructed by `forecastability_profile_service.build_forecastability_profile()` and is exposed on the `TriageResult` returned by `run_triage()`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-1044ad567134c4c3` [concept] (literature_supported) — The utils package contains config models, typed containers, datasets, validation, plotting, and repo workflow support.
  > utils/` Config models, typed containers, datasets, validation, plotting, and repo workflow support
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-10d927ca341cda5e` [procedure_step] (literature_supported) — Users should prefer the stable facade `forecastability` and `forecastability.triage` when using the toolkit.
  > Use the stable facade first: prefer `forecastability` and `forecastability.triage`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-14f162fab7563476` [procedure_step] (literature_supported) — Standard cross-correlation for each lag k computes the Pearson correlation coefficient between X at lag k and Y.
  > For each $k \in \{0, 1, \dots, K_{\max}\}$: $$\hat{\rho}_k(X, Y) = \frac{\sum_{t} (X_{t-k} - \bar{X})(Y_t - \bar{Y})}{\sqrt{\sum_{t}(X_{t-k} - \bar{X})^2 \sum_{t}(Y_t - \bar{Y})^2}}$$
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-155a2b21f0331176` [procedure_step] (literature_supported) — The pAMI estimator residualizes past and future variables on the conditioning matrix Z using a linear backend by default.
  > Residualize past and future on \(Z\) (linear backend by default; optional RF backend).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-1a78c8e932db48e4` [representation] (literature_supported) — The top-level package facade in src/forecastability/__init__.py re-exports run_triage, run_batch_triage, analyzers, config models, result models, dataset helpers, scorer registry, and validation.
  > Top-level package facade with re-exports for `run_triage`, `run_batch_triage`, analyzers, config models, result models, dataset helpers, scorer registry, and validation
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-1f81e1f51c21c73f` [concept] (literature_supported) — The bootstrap package contains bootstrap helpers such as output directory setup.
  > bootstrap/` Bootstrap helpers such as output directory setup
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-2192244453756589` [norm] (literature_supported) — PCMCI-AMI orchestration follows the inward-only dependency rule: use cases depend on declared ports, and adapters satisfy those contracts without adapter-to-adapter helper coupling.
  > PCMCI-AMI orchestration now follows the inward-only dependency rule: use cases depend on declared ports (protocol contracts), and adapters satisfy those contracts without adapter-to-adapter helper coupling.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-2464b450de4285f5` [representation] (literature_supported) — The adapters/api.py module exposes the FastAPI application at forecastability.adapters.api:app.
  > `adapters/api.py` exposes the FastAPI application at `forecastability.adapters.api:app`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-28b4da9f7795b4d4` [decision] (literature_supported) — When data are significance-infeasible, surrogates are skipped and decisions are route and class screening only.
  > when data are significance-infeasible (for example n=150 in regression tests), surrogates are skipped and decisions are route/class screening only.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3112fa33996fc9b4` [procedure_step] (literature_supported) — The benchmark panel workflow entry point is `scripts/run_benchmark_panel.py` and it runs the benchmark panel and writes summary artifacts.
  > Benchmark panel workflow `scripts/run_benchmark_panel.py` Runs the benchmark panel and writes summary artifacts
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-36753f68e2d3a1dd` [mental_model] (literature_supported) — Any numeric claim in an agent response is a restatement of a deterministic result, so if the underlying TriageResult is wrong, the agent narration will be wrong in the same way.
  > Any numeric claim in an agent response is a restatement of a deterministic result. If the underlying `TriageResult` is wrong, the agent narration will be wrong in the same way.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-38980f0e174c2bf6` [prerequisite] (literature_supported) — F5 should be used only when the series is long (n ≫ 1000 for default embedding dimension m = 3) and approximately stationary.
  > When the series is long ($n \gg 1000$ for the default embedding dimension $m = 3$) and approximately stationary.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-390244c80805860b` [norm] (literature_supported) — The architecture goal is inward dependency flow.
  > The architecture goal is still inward dependency flow.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-434ff0a66875fb8e` [concept] (literature_supported) — The use_cases package contains main orchestration entry points for deterministic triage and batch triage.
  > use_cases/` Main orchestration entry points for deterministic triage and batch triage
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-44996892950d6563` [procedure_step] (literature_supported) — The exogenous workflow entry point is `scripts/run_exog_analysis.py` and it runs exogenous screening and related artifacts.
  > Exogenous workflow `scripts/run_exog_analysis.py` Runs exogenous screening and related artifacts
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-496ce0075e9e2f04` [concept] (literature_supported) — The TriageRequest random_state parameter seeds both the MI estimator and the surrogate generator for reproducibility.
  > `random_state` Seeds both the MI estimator and the surrogate generator for reproducibility
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4a1da696ae821fe9` [procedure_step] (literature_supported) — To work in the repository, the local environment should be synced with uv sync.
  > If you are working in the repository, sync the local environment. uv sync
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4e2c69094b68cc2d` [concept] (literature_supported) — Entrypoints and adapters call the package facades or use cases as the first level of practical dependency direction.
  > Entrypoints and adapters call the package facades or use cases.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-50131c1b5596f902` [check] (literature_supported) — Requests for compute_partial with method="te" raise a validation error because no validated partial-TE estimand is implemented in the analyzer path.
  > Requests for `compute_partial(..., method="te")` raise a validation error because no validated partial-TE estimand is implemented in the analyzer path.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-56c7e2352b86c464` [decision] (literature_supported) — The Analyzer path is raw-only for Transfer Entropy; partial TE is intentionally unsupported.
  > Analyzer path is raw-only for TE: partial TE is intentionally unsupported.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5731821947eb7627` [procedure_step] (literature_supported) — The canonical single-series workflow entry point is `scripts/run_canonical_triage.py` and it builds canonical outputs for exemplar series.
  > Canonical single-series workflow `scripts/run_canonical_triage.py` Builds canonical outputs for exemplar series
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5c72f83f3c14bb32` [norm] (literature_supported) — forecastability and forecastability.triage have a stable import contract.
  > `forecastability` and `forecastability.triage` Stable import contract
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5cf177e1e7d4a1b4` [concept] (literature_supported) — The PydanticAI agent layer reads frozen deterministic payloads and generates natural-language narration but does not perform any statistical computation or validate the numeric results.
  > The PydanticAI agent layer reads frozen deterministic payloads (A1-A3) and generates natural-language narration. It does not perform any statistical computation or validate the numeric results.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5fd328af850e4669` [procedure_step] (literature_supported) — The triage workflow uses one-entry-point orchestration called run_triage with staged readiness, routing, compute, and interpretation checks.
  > one-entry-point orchestration (`run_triage`) with staged readiness, routing, compute, and interpretation checks
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6144da63ab9a0d5a` [norm] (literature_supported) — At least n_surrogates = 99 is required for a valid two-sided 95% confidence band, and fewer than 99 surrogates are not sufficient and must not be used as a significance threshold.
  > At least `n_surrogates = 99` is required for a valid two-sided 95% band. Fewer than 99 surrogates are not sufficient and must not be used as a significance threshold.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6215c841ac206817` [representation] (literature_supported) — src/forecastability/triage/__init__.py provides an advanced triage namespace for batch models, readiness helpers, events, bundle types, and triage-specific diagnostics.
  > Advanced triage namespace for batch models, readiness helpers, events, bundle types, and triage-specific diagnostics
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-632cedcf139eff2c` [concept] (literature_supported) — CLI, API, scripts, MCP, and agents are optional access or narration layers around the same deterministic outputs.
  > CLI, API, scripts, MCP, and agents are optional access or narration layers around the same deterministic outputs.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-69285d21a7b847aa` [procedure_step] (literature_supported) — The opinionated path from install to a trustworthy first result should be followed before reaching for the CLI, API, dashboard, MCP, or agent layers.
  > Follow this path before you reach for the CLI, API, dashboard, MCP, or agent layers.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6989ef77c4068b6b` [procedure_step] (literature_supported) — After triage, fingerprint, and lagged-exog analysis, users should call `build_forecast_prep_contract()` to convert triage outputs into a `ForecastPrepContract`.
  > After triage, fingerprint, and lagged-exog analysis, call `build_forecast_prep_contract()` to convert triage outputs into a `ForecastPrepContract`
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6ccb4c89f47d7cb2` [expectancy] (literature_supported) — The internal packages, the MCP surface, and the agent layer are useful only after the deterministic workflow is already understood.
  > The internal packages, the MCP surface, and the agent layer are useful only after the deterministic workflow is already understood.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6d51ab3cf41cdb9b` [concept] (literature_supported) — The stable public contract of the repository is small, while the internal package tree is deliberately split across triage models, use cases, analyzers, metrics, diagnostics, reporting, utils, adapters, services, ports, and bootstrap helpers.
  > the stable public contract is small, while the internal package tree is deliberately split across triage models, use cases, analyzers, metrics, diagnostics, reporting, utils, adapters, services, ports, and bootstrap helpers.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7076702eb911c14b` [procedure_step] (literature_supported) — Extended cross_ami lag profile computes mutual information for each lag k from 0 to K_max using a kNN mutual-information estimator.
  > For each $k \in \{0, 1, \dots, K_{\max}\}$: $$\widehat{I}_k(X, Y) = \widehat{I}(X_{t-k}\,;\,Y_t)$$ estimated with the same kNN mutual-information estimator
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-72adce2b61986e14` [procedure_step] (literature_supported) — To get the published package surface, installation should be from PyPI.
  > If you want the published package surface, install from PyPI.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-73746b4f1f17893a` [norm] (literature_supported) — The known_future_drivers contract is honored at the use-case layer (run_lagged_exogenous_triage); the selector service itself is pure and does not read it.
  > The `known_future_drivers` contract is honored at the **use-case layer** (`run_lagged_exogenous_triage`). The selector service itself is pure and does not read it.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-73809d9fb3250ea5` [prerequisite] (literature_supported) — F4 should be avoided for strongly non-stationary series without prior detrending.
  > For strongly non-stationary series without prior detrending.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-740b4d94544b44cf` [concept] (literature_supported) — The core dependence-forecastability package has no import-time or runtime dependencies on forecasting libraries like Darts, MLForecast, StatsForecast, or Nixtla.
  > The core `forecastability` package has no import-time or runtime dependencies on Darts, MLForecast, StatsForecast, Nixtla, or similar forecasting libraries; any such extras and comparisons are optional and live in the separate `forecastability-examples` repository.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7ad28c619729b90a` [norm] (literature_supported) — F7 should not be used when F5 output is desired in the ranking because LLE is intentionally excluded.
  > When F5 output is desired in the ranking: LLE is intentionally excluded from automated batch triage by design.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7b0d037b682a6113` [concept] (literature_supported) — The pipeline package contains analyzer facade, canonical workflow helpers, and rolling-origin support.
  > pipeline/` Analyzer facade, canonical workflow helpers, and rolling-origin support
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-800b35d358c081ff` [expectancy] (literature_supported) — adapters/ are supported runtime surfaces, but transport details may evolve.
  > `adapters/` runtime entry points Supported runtime surfaces, but transport details may evolve
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-825cf52b99f40fe5` [concept] (literature_supported) — Triage, pipeline, and services consume metrics, diagnostics, reporting, and utils as the third level of practical dependency direction.
  > Triage, pipeline, and services consume metrics, diagnostics, reporting, and utils.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-83ad73dd37bcd274` [procedure_step] (literature_supported) — The report-building workflow entry point is `scripts/build_report_artifacts.py` and it builds report-facing artifacts from generated outputs.
  > Report-building workflow `scripts/build_report_artifacts.py` Builds report-facing artifacts from generated outputs
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-87434ff1844dd684` [prerequisite] (literature_supported) — The MCP server requires additional server-framework dependencies and is not included in the default install.
  > The MCP server requires additional server-framework dependencies. It is not included in the default install.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8888e1c66b9f1320` [norm] (literature_supported) — The supported import surface for the toolkit is the package facade, not the internal tree.
  > The supported import surface is the package facade, not the internal tree.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8a2e067ac1d08f0e` [procedure_step] (literature_supported) — Transfer Entropy sample-size guardrails require min_pairs >= 50.
  > TE sample-size guardrails require `min_pairs >= 50`
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8aedfe6a5eb93e45` [concept] (literature_supported) — The TriageRequest max_lag parameter sets H - the length of the horizons and values arrays.
  > `max_lag` Sets $H$ - the length of the `horizons` and `values` arrays
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8e661bdd184f87de` [norm] (literature_supported) — The sparse selector emits LaggedExogSelectionRow objects independently from plot artifacts; the sparse map is a typed Python output first.
  > The selector emits `LaggedExogSelectionRow` objects independently from plot artifacts; the sparse map is a typed Python output first.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-94cbcad1aa437634` [concept] (literature_supported) — The triage package contains triage-domain models, readiness/router logic, diagnostic result types, events, and result bundles.
  > triage/` Triage-domain models, readiness/router logic, diagnostic result types, events, and result bundles
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-97be86317cc83c2d` [norm] (literature_supported) — The linear_residual backend is the default benchmark and production-safe baseline.
  > linear_residual` Fast, stable, interpretable baseline Misses nonlinear mediation Default benchmark and production-safe baseline
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a2dd58383bac2072` [prerequisite] (literature_supported) — F8 should be avoided for very short series because CrossAMI inherits finite-sample bias and minimum-length requirements from univariate AMI.
  > For very short series: CrossAMI inherits the same finite-sample bias and minimum- length requirements as univariate AMI.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a58de96982596cf4` [procedure_step] (literature_supported) — The robustness study pipeline should be used to compare all configured backends against linear_residual.
  > Use the robustness study pipeline to compare all configured backends against `linear_residual`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a9f19e828898e2a0` [procedure_step] (literature_supported) — The triage workflow blocks infeasible requests, routes exogenous requests separately, and preserves stable screening behavior.
  > The workflow blocks infeasible requests, routes exogenous requests separately, and preserves stable screening behavior (`AR(1) -> high`, `white_noise -> low`)
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ab9c418ee5ffb971` [procedure_step] (literature_supported) — The Transfer Entropy core estimator is located in src/forecastability/diagnostics/transfer_entropy.py with functions compute_transfer_entropy() and compute_transfer_entropy_curve().
  > src/forecastability/diagnostics/transfer_entropy.py`: `compute_transfer_entropy()` and `compute_transfer_entropy_curve()` (core estimator path).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-b172e870fc882773` [concept] (literature_supported) — The Forecastability Profile is a read-only, frozen Pydantic model whose fields are populated once from the AMI curve already computed by the pipeline, with no new estimation occurring during profile construction.
  > The profile is a read-only, frozen Pydantic model - `ForecastabilityProfile` - whose fields are populated once from the AMI curve already computed by the pipeline. No new estimation occurs during profile construction.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-b3fe95913327f517` [expectancy] (literature_supported) — services/, utils/, pipeline/, metrics/, diagnostics/, and reporting/ are internal structure that may continue to move during consolidation.
  > `services/`, `utils/`, `pipeline/`, `metrics/`, `diagnostics/`, `reporting/` Internal structure that may continue to move during consolidation
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-bd1e916d68bcfd18` [concept] (literature_supported) — The dashboard is a beta transport surface and is a thin browser UI over the deterministic adapters.
  > The dashboard is a thin browser UI over the deterministic adapters.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c4c95455620fc6e1` [norm] (literature_supported) — The supported public surfaces are the package facades plus the declared runtime entry points.
  > the supported public surfaces are the package facades plus the declared runtime entry points.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-cb6160b35a702204` [concept] (literature_supported) — Ports and bootstrap remain support seams rather than primary business-logic owners as the fourth level of practical dependency direction.
  > Ports and bootstrap remain support seams rather than primary business-logic owners.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-cd1d40991a06fafa` [prerequisite] (literature_supported) — F6 requires at least n ≈ 600 for m = 5 because permutation entropy requires adequate pattern-frequency estimates.
  > For very short series: permutation entropy requires adequate pattern-frequency estimates; for $m = 5$, at least $n \approx 600$ is recommended.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-cdcf82289f074548` [procedure_step] (literature_supported) — ForecastabilityAnalyzer and ForecastabilityAnalyzerExog support method="te" for raw-curve analysis and TE surrogate significance bands.
  > src/forecastability/pipeline/analyzer.py`: `ForecastabilityAnalyzer` and `ForecastabilityAnalyzerExog` support `method="te"` for raw-curve analysis and TE surrogate significance bands.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d02f7cb6014ca8ab` [concept] (literature_supported) — The metrics package contains core AMI/pAMI computation and scorer registry.
  > metrics/` Core AMI/pAMI computation and scorer registry
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d0a3775a32b0d918` [prerequisite] (literature_supported) — F1 should be avoided for series shorter than approximately 3× the maximum evaluation horizon.
  > For series shorter than the recommended minimum (approximately 3× the maximum evaluation horizon).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d15f7f776bd59267` [norm] (literature_supported) — The toolkit is not uniformly production-ready, with the deterministic core and stable facades being stable while CLI and HTTP API are beta and MCP server and agent layer are experimental.
  > The toolkit is not uniformly production- ready. The deterministic core and stable facades are stable; CLI and HTTP API are beta; MCP server and agent layer are experimental.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d1d7e1cad07f0f7e` [prerequisite] (literature_supported) — F4 Ω values are unreliable for short series (n < 128) as anything other than a coarse indicator because Welch PSD estimates are based on very few segments.
  > For short series ($n < 128$): Welch PSD estimates are based on very few segments and Ω values are unreliable as anything other than a coarse indicator.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d55932d207537908` [procedure_step] (literature_supported) — Given series length N and max lag H, AMI feasibility requires N >= H + min_pairs_ami + 1.
  > AMI feasibility: \[ N \ge H + \texttt{min\_pairs\_ami} + 1 \]
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d5edfecd62102abb` [procedure_step] (literature_supported) — The file `docs/public_api.md` defines the supported import contract for the package.
  > Treat `docs/public_api.md` as the supported import contract.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-df5264430040a5e5` [procedure_step] (literature_supported) — With defaults min_pairs_ami=30, min_pairs_pami=50, and H=100, AMI requires N >= 131.
  > With defaults (`min_pairs_ami=30`, `min_pairs_pami=50`, `H=100`): - AMI requires \(N \ge 131\)
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e1b581bc10fd30b8` [representation] (literature_supported) — The stable import facade of the forecastability package is small, while the internal tree is organized by role including triage domain, use cases, analyzer pipeline, metrics, diagnostics, reporting, utils, adapters, services, ports, and bootstrap helpers.
  > The package is layered and subpackage-heavy. The stable import facade is small, but the internal tree is organized by role: triage domain, use cases, analyzer pipeline, metrics, diagnostics, reporting, utils, adapters, services, ports, and bootstrap helpers.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e548741ed8be78a3` [procedure_step] (literature_supported) — Given series length N and max lag H, pAMI feasibility with linear residual backend requires N >= max(H + min_pairs_pami + 1, 2H).
  > pAMI feasibility (linear residual backend): \[ N \ge \max\left(H + \texttt{min\_pairs\_pami} + 1,\ 2H\right) \]
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e63a68471867efe0` [procedure_step] (literature_supported) — F5 largest Lyapunov exponent must be explicitly enabled via experimental: true in the config and does not run in default triage mode.
  > F5 must be explicitly enabled via `experimental: true` in the config. It does not run in default triage mode.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e86f46321e90a6a9` [concept] (literature_supported) — The Forecastability Profile model is frozen; fields cannot be mutated after construction, which guarantees that cached profiles remain consistent with their source AMI run.
  > The model is frozen (`model_config = ConfigDict(frozen=True)`); fields cannot be mutated after construction, which guarantees that cached profiles remain consistent with their source AMI run.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-eace56da56b7b667` [concept] (literature_supported) — The profile reuses AMI values produced by ForecastabilityAnalyzer.analyze(), which runs a kNN MI estimator with n_neighbors=8, and no separate estimation step executes during profile construction.
  > The profile reuses AMI values produced by `ForecastabilityAnalyzer.analyze()`, which runs a kNN MI estimator with `n_neighbors=8`. No separate estimation step executes during profile construction.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f3815d4bf1b2cf27` [norm] (literature_supported) — Surrogates should be used whenever sample size permits (n ≥ 200, n_surrogates ≥ 99).
  > Use surrogates whenever sample size permits ($n \ge 200$, `n_surrogates >= 99`).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f3cb377af9f60410` [concept] (literature_supported) — The adapters package contains CLI, dashboard, API, MCP, agent, settings, event, checkpoint, and presenter adapters.
  > adapters/` CLI, dashboard, API, MCP, agent, settings, event, checkpoint, and presenter adapters
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f5e20b0412b1132b` [norm] (literature_supported) — The HTTP API is a beta transport surface that exposes `GET /health`, `GET /scorers`, `POST /triage`, and `GET /triage/stream` endpoints.
  > The HTTP API exposes `GET /health`, `GET /scorers`, `POST /triage`, and `GET /triage/stream`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f7fc6c32c09e091d` [concept] (literature_supported) — The TriageRequest n_surrogates parameter controls surrogate-band accuracy for epsilon resolution.
  > `n_surrogates` Controls surrogate-band accuracy for epsilon resolution
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-fd2e7d186e66bfd0` [procedure_step] (literature_supported) — With non-empty conditioning history in Transfer Entropy, at least 2 * min_pairs aligned rows are required.
  > with non-empty conditioning history, at least `2 * min_pairs` aligned rows are required.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-fdf1780fb5c513d1` [cue] (literature_supported) — Checked-in files under `outputs/json/`, `outputs/tables/`, and `outputs/reports/` are reference artifacts but are not guaranteed to be freshly regenerated for every commit.
  > Checked-in files under `outputs/json/`, `outputs/tables/`, and `outputs/reports/` are reference artifacts. They are useful examples of the artifact surface, but they are not guaranteed to be freshly regenerated for every commit.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)

### Synthetic / rejected claims

- `c-177df078da444389` [concept] (synthetic_extrapolation) — Everything else in src/forecastability/ exists to support the public facades and repo workflows.
  > Everything else in `src/forecastability/` exists to support those facades and repo workflows.
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md)
- `c-2ce66f0ac49ae727` [procedure_step] (synthetic_extrapolation) — The default kNN MI estimator uses k=8. (no located evidence)
- `c-3681ece67583bdb2` [norm] (synthetic_extrapolation) — F5 should not be used in automated batch ranking.
  > In automated batch ranking (F7): LLE is excluded by design.
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md)
- `c-41d54a259a1da6ef` [concept] (synthetic_extrapolation) — The dependence-forecastability toolkit is a Python package for answering whether a time series contains exploitable structure before model selection. (no located evidence)
- `c-5e50c01be566a2de` [concept] (synthetic_extrapolation) — The advanced triage namespace is located at src/forecastability/triage/__init__.py. (no located evidence)
- `c-5fac8aa852479c48` [procedure_step] (synthetic_extrapolation) — The pAMI estimator builds a conditioning matrix Z containing intermediate lags from X_{t+1} to X_{t+h-1}. (no located evidence)
- `c-6b55180d2b856236` [norm] (synthetic_extrapolation) — F5 is experimental and excluded from automated triage decisions. (no located evidence)
- `c-73a5545acb9774cb` [concept] (synthetic_extrapolation) — The HTTP API is located at forecastability.adapters.api:app. (no located evidence)
- `c-788001eab5c8cd22` [representation] (synthetic_extrapolation) — The adapters/cli.py module implements the forecastability command. (no located evidence)
- `c-823854ec012d0ede` [norm] (synthetic_extrapolation) — The Python package facade `forecastability` is a stable import surface. (no located evidence)
- `c-8aaff12aa1fa219e` [procedure_step] (synthetic_extrapolation) — Optional extras for agent and API each add transitive packages, and in constrained environments one should install only the extras needed. (no located evidence)
- `c-8d200adae5e75d2c` [concept] (synthetic_extrapolation) — The toolkit is not another forecasting library but rather a deterministic pre-modeling layer. (no located evidence)
- `c-9964e80b6c339c8e` [concept] (synthetic_extrapolation) — The linear_residual backend is fast, stable, and interpretable. (no located evidence)
- `c-9b864efbd9220b1c` [strategy] (synthetic_extrapolation) — Most users only need the package facade, the notebook path in the `forecastability-examples` repository, and the maintainer scripts in order. (no located evidence)
- `c-a2c34f47e1899ab4` [concept] (synthetic_extrapolation) — The dashboard command is located at forecastability.adapters.dashboard:main. (no located evidence)
- `c-a3d315cab35d81a0` [norm] (synthetic_extrapolation) — The forecast prep contract `build_forecast_prep_contract()` is a stable import surface. (no located evidence)
- `c-abde6ecddebe0793` [norm] (synthetic_extrapolation) — External users should anchor on the Public Facades And Entrypoints surfaces, which include the stable package facade, advanced triage namespace, CLI command, dashboard command, and HTTP API.
  > These are the surfaces that external users should anchor on.
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md)
- `c-ac3391fbea4ab780` [concept] (synthetic_extrapolation) — The dependence-forecastability toolkit does not train forecasting models but instead asks what a model should be allowed to see. (no located evidence)
- `c-adade6962e55c89a` [procedure_step] (synthetic_extrapolation) — The CSV adapter drops missing values column-wise and skips too-short or non-numeric series conservatively instead of forcing a partial analysis. (no located evidence)
- `c-b431dad9881bc73d` [procedure_step] (synthetic_extrapolation) — With defaults min_pairs_ami=30, min_pairs_pami=50, and H=100, pAMI requires N >= 201. (no located evidence)
- `c-b6101554bbca77ab` [concept] (synthetic_extrapolation) — Use cases orchestrate triage models, pipeline helpers, and internal services, and depend on causal discovery through declared ports contracts as the second level of practical dependency direction.
  > Use cases orchestrate triage models, pipeline helpers, and internal services, and depend on causal discovery through declared `ports/` contracts.
  (verdict insufficient [adds_content, connective_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md)
- `c-bcb4f2b6969ea4c9` [failure_mode] (synthetic_extrapolation) — Windows path handling, line endings, and subprocess behaviour have not been systematically tested, as development and CI run on macOS and Linux only. (no located evidence)
- `c-bddbf9fe407573c2` [norm] (synthetic_extrapolation) — The advanced triage namespace `forecastability.triage` is a stable import surface. (no located evidence)
- `c-c12c8710867325c9` [check] (synthetic_extrapolation) — Diagnostic regression fixtures provide golden-value snapshot tests to ensure reproducibility across all new diagnostics. (no located evidence)
- `c-caeda29fdb65a76d` [concept] (synthetic_extrapolation) — The stable package facade is located at src/forecastability/__init__.py. (no located evidence)
- `c-cd61662a39763ad4` [concept] (synthetic_extrapolation) — The CLI command is located at forecastability.adapters.cli:main. (no located evidence)
- `c-ce2931b9225df24b` [concept] (synthetic_extrapolation) — The profile is the primary deliverable of Feature F1 in the triage pipeline and is constructed by forecastability_profile_service.build_forecastability_profile(). (no located evidence)
- `c-df52f03f79e64dc3` [concept] (synthetic_extrapolation) — ForecastPrepContract is a typed hand-off comprising target lags, seasonal hints, covariate roles, caution flags, and advisory routing labels for downstream modeling code. (no located evidence)
- `c-e36496dc034bb634` [procedure_step] (synthetic_extrapolation) — The pAMI estimator computes MI on residual pairs. (no located evidence)
- `c-e6a7cc73f02324b0` [procedure_step] (synthetic_extrapolation) — The sparse lag selector algorithm starts with an empty set and iteratively adds lags with partialled mutual information score above threshold, up to a maximum count, always evaluating the strongest candidate first.
  > Start with $\mathcal{S} \leftarrow \emptyset$. 2. While there exists $k^\dagger \notin \mathcal{S}$ with partialled score $\tilde{I}_{k^\dagger}(X, Y \mid \{X_{t-k'}: k' \in \mathcal{S}\}) \ge \tau_{\text{select}}$, add $k^\dagger$ to $\mathcal{S}$, capped at `max_selected_per_driver`. 3. Emit each candidate $k$ as a `LaggedExogSelectionRow` with `selected_for_tensor=True` if and only if $k \in \mathcal{S}$. The strongest candidate $k^\star = \arg\max_k \widehat{I}_k$ is always evaluated first.
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md)
- `c-f1b517c040601ebc` [procedure_step] (synthetic_extrapolation) — When no surrogates are available, epsilon falls back to the default_epsilon parameter (default 0.05 nats), or to an explicit caller-supplied override.
  > **When no surrogates are available** - $\varepsilon$ falls back to the `default_epsilon` parameter (default `0.05` nats), or to an explicit caller-supplied override.
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md)
- `c-f9f26c2e6fbef285` [prerequisite] (synthetic_extrapolation) — F5 is excluded for series with n < 1000 because phase-space coverage is insufficient and the estimate is indicative only.
  > For series with $n < 1000$: phase-space coverage is insufficient and the estimate is indicative only.
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md)
- `c-fc2d4857f78433d0` [prerequisite] (synthetic_extrapolation) — Python 3.11 or later is required, as the codebase uses 3.11-specific syntax and type features and earlier Python versions will produce parse errors. (no located evidence)
- `c-fe9b90d4b8ea5f8c` [failure_mode] (synthetic_extrapolation) — F2 should be avoided when series length is very short because finite-sample bias inflates the estimated limit.
  > When series length is very short: finite-sample bias inflates the estimated limit.
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md)

### UNKNOWN / thin / unverified / unexamined slots

- concept: thin
- decision: thin
- cue: thin
- check: thin
- failure_mode: unknown
- norm: thin
- rationale: unknown
- procedure_step: thin

### Unknown placeholders

- `c-0c2e3c12edad6591` [rationale] — Why is Setting up and running the toolkit done the way it is?
- `c-34f70d086a03cba2` [failure_mode] — How does work in Setting up and running the toolkit typically go wrong, and what are the signs?

## Area: Interpreting forecastability results

### Supported claims

- `c-02630e449b097ef1` [interpretation] (literature_supported) — IT limit diagnostics sets realistic expectations before model investment and flags information-destroying transforms.
  > Sets realistic expectations before model investment; flags information-destroying transforms
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-02db4a573b917ded` [concept] (literature_supported) — In rolling-origin evaluation, diagnostics are computed on train windows only and scoring on post-origin holdout only.
  > In rolling-origin evaluation, diagnostics are computed on train windows only and scoring on post-origin holdout only.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-046dab40441271aa` [procedure_step] (literature_supported) — F8 should be used in combination with F1 to extend analysis to cross-series dependence with F1 remaining the primary univariate anchor.
  > In combination with F1: F8 extends the analysis to cross-series dependence; F1 remains the primary univariate anchor.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-05dbf0907edceed5` [concept] (literature_supported) — Surrogate significance is optional, requires feasible sample size, and needs at least 99 surrogates.
  > Surrogate significance is optional, requires feasible sample size, and needs at least 99 surrogates.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-06cbf6026495296f` [procedure_step] (literature_supported) — CrosspAMI determines whether a covariate relationship survives the target-history adjustment after CrossAMI indicates where the raw relationship appears.
  > CrossAMI says where the raw relationship appears. CrosspAMI asks whether the relationship survives the target-history adjustment. Forecast-legality rules remove lags that would not be available at prediction time.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-072638895e9ad8fe` [interpretation] (literature_supported) — The forecastability_class field indicates high-level interpretation when triage completed.
  > forecastability_class` High-level interpretation when triage completed
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0869da46b065ba5c` [check] (literature_supported) — False confidence from one backend should be mitigated by requiring cross-backend agreement before acting on lag recommendations.
  > False confidence from one backend decision changes when backend changes model class mismatch or noisy data require cross-backend agreement before acting on lag recommendations
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-097b7b072e068319` [procedure_step] (literature_supported) — Significance bands for surrogacy use phase-randomized surrogates and two-sided 95% quantiles with lower band at 2.5th percentile and upper band at 97.5th percentile.
  > Surrogate significance uses phase-randomized surrogates and two-sided 95% quantiles: - lower: 2.5th percentile - upper: 97.5th percentile
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0d90e0d9e452ab98` [procedure_step] (literature_supported) — F3 should be used when you suspect that longer lags add noise rather than signal.
  > When you suspect that longer lags add noise rather than signal (the curve never plateauing is also informative).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0fc8a743e95bf7e2` [norm] (literature_supported) — At least one row per (target, driver) pair is emitted by the sparse selector.
  > **At least one row per `(target, driver)` pair** is emitted by the selector.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-10e496fcc72af849` [norm] (literature_supported) — With the known_future_drivers opt-in, k=0 rows for that driver flip to tensor_role="known_future" and the selector may choose selected_for_tensor=True at k=0 for that driver only.
  > With the opt-in, those rows flip to `tensor_role="known_future"` and the selector may choose `selected_for_tensor=True` at $k=0$ for that driver only.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-11938f1ded48143a` [procedure_step] (literature_supported) — F1 should be used when you need to know which forecast horizons carry detectable predictive signal above the noise floor.
  > When you need to know which forecast horizons carry detectable predictive signal above the noise floor.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-133f1d804bafb198` [cue] (literature_supported) — A driver that keeps most of its pairwise signal after conditioning pressure is a better candidate for downstream use than one that collapses.
  > A driver that keeps most of its pairwise signal after conditioning pressure is a better candidate for downstream use; a driver that collapses is probably borrowing strength from target memory, common forcing, seasonality, or shared regime.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-176cff9ac653373b` [check] (literature_supported) — Short-sample fragility should be mitigated by enforcing minimum length and inspecting stress table stability.
  > Short-sample fragility large backend deltas on small fractions insufficient support for residualization enforce minimum length and inspect stress table stability
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-177fd53b85f3607b` [representation] (literature_supported) — The diagnostics/surrogates.py module owns phase-randomized FFT surrogates and significance bands.
  > `diagnostics/surrogates.py` owns phase-randomized FFT surrogates and significance bands.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-31524d4ec7dfcb67` [concept] (literature_supported) — The `ForecastPrepContract` is a structured, machine-readable hand-off contract for downstream model families.
  > a `ForecastPrepContract` - a structured, machine-readable hand-off contract for downstream model families.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3a92349c4938c49e` [procedure_step] (literature_supported) — F2 should be used to determine why AMI is low by revealing whether the ceiling is genuinely low or whether the sampled curve has not saturated the limit.
  > When you want to know *why* AMI is low - limit compression reveals whether the ceiling is genuinely low (hard limit) or whether the sampled curve has not saturated the limit.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-41c0d5e51f484735` [check] (literature_supported) — To audit Data-Processing Inequality violations, compare the values arrays element-wise across two runs; any lag where the derived profile exceeds the raw profile by more than estimation noise is a data-leakage candidate, not a genuine gain.
  > The profile makes this audit straightforward: compare the `values` arrays element-wise across two runs; any lag where the derived profile exceeds the raw profile by more than estimation noise is a data-leakage candidate, not a genuine gain.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-46140a6e5ef1dada` [norm] (literature_supported) — By default, every k=0 row gets tensor_role="diagnostic".
  > By default, every $k = 0$ row gets `tensor_role = "diagnostic"`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4827afa49c4c1a69` [check] (literature_supported) — F3 should not be used as a standalone triage decision because it produces a curve and a lookback recommendation, not a scalar forecastability score.
  > As a standalone triage decision: F3 produces a curve and a lookback recommendation, not a scalar forecastability score.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-49d043b5f8cf1852` [interpretation] (literature_supported) — Optional narration enables faster cross-functional handoff between operations, maintenance, and planning.
  > Faster cross-functional handoff (operations, maintenance, planning)
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4a21fbf2da550af4` [check] (literature_supported) — F2 should not be used as a standalone decision without F1 because the limit is derived from the AMI curve.
  > As a standalone decision without F1: the limit is derived from the AMI curve, so F1 evidence is prerequisite context.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4f97b581ddee90a5` [representation] (literature_supported) — The reporting/reporting.py module owns Markdown and report-building helpers.
  > `reporting/reporting.py` owns Markdown and report-building helpers.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-520a1e7ba216f30b` [check] (literature_supported) — F4 should not be used as the sole forecastability measure because Ω misses nonlinear dependence entirely.
  > As the sole forecastability measure: Ω misses nonlinear dependence entirely.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-53564f05f2268320` [strategy] (literature_supported) — The upper surrogate band is operationally informative for detecting non-null dependence, while the lower band is usually near zero for MI and is not typically operationally useful.
  > The upper band is operationally informative for detecting non-null dependence. The lower band is usually near zero for MI and is not typically operationally useful.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-66c250dc8aa52432` [interpretation] (literature_supported) — Forecastability profile narrows model evaluation to productive horizons and detects non-monotone seasonal structure.
  > Narrows model evaluation to productive horizons; detects non-monotone seasonal structure
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-68a27a535380bf9d` [cue] (literature_supported) — Large backend deltas on small fractions are an observable symptom of short-sample fragility caused by insufficient support for residualization.
  > Short-sample fragility large backend deltas on small fractions insufficient support for residualization
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6ba66a9482d8beb1` [cue] (literature_supported) — A directness_ratio greater than 1.0 is an observable symptom of numerical inflation caused by estimator instability or finite-sample effects.
  > Numerical inflation `directness_ratio > 1.0` estimator instability, finite-sample effects
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6cd11f0e30d05f50` [cue] (literature_supported) — This repository flags directness_ratio > 1.0 as arch_suspected.
  > This repository flags `directness_ratio > 1.0` as `arch_suspected`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6d3f5a6dbc7b1178` [norm] (literature_supported) — Without the known_future_drivers opt-in, every k=0 row for a driver will have selected_for_tensor=False and tensor_role="diagnostic".
  > Without this opt-in, every $k=0$ row for `"holiday_flag"` will have `selected_for_tensor=False` and `tensor_role="diagnostic"`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6d7a06227ef683da` [norm] (literature_supported) — When a method genuinely lacks a surrogate path, the significance field stays explicitly None and row metadata records significance_source="not_computed"; no synthetic p-values are invented.
  > When a method genuinely lacks a surrogate path (standard cross-correlation), the significance field stays explicitly `None` and the row metadata records `significance_source = "not_computed"`. No synthetic p-values are invented.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7416db3bcd35aab6` [interpretation] (literature_supported) — Entropy-based complexity enables fast regime classification and complements AMI with amplitude-blind ordinal structure.
  > Fast regime classification; complements AMI with amplitude-blind ordinal structure
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-760de6e84d01ea9a` [procedure_step] (literature_supported) — F1 should be used as the primary output for any univariate forecastability assessment.
  > As the primary output for any univariate forecastability assessment.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-76ac2b1d44f33259` [interpretation] (literature_supported) — The primary_lags field identifies informative lags identified by the deterministic workflow.
  > primary_lags` Informative lags identified by the deterministic workflow
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7a572b62a6fcc85d` [failure_mode] (literature_supported) — Directness can be numerically unstable when raw dependence is close to zero.
  > directness can be numerically unstable when raw dependence is close to zero.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7af7772c6efe28c5` [check] (literature_supported) — Significance counts are currently zero across the canonical summary, so actionable lag decisions should rely on class-level screening plus domain checks rather than significance-lag selection alone.
  > significance counts are currently zero across this canonical summary (`n_sig_ami=0`, `n_sig_pami=0` for all 8), so actionable lag decisions should rely on class-level screening plus domain checks rather than significance-lag selection alone.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7afe58436134c4db` [check] (literature_supported) — Overfitting in nonlinear backends should be mitigated by comparing against linear baseline and requiring ranking stability.
  > Overfitting in nonlinear backends sharp pAMI spikes at isolated lags only for tree backends backend fits noise in conditioning space compare against linear baseline and require ranking stability
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-80ca212bb3e57548` [interpretation] (literature_supported) — If AMI geometry is disabled or unavailable in extended analysis, the profile remains descriptive-only and does not emit routing-grade family recommendations.
  > AMI geometry stays first. If it is disabled or unavailable, the profile remains descriptive-only and does not emit routing-grade family recommendations.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8a05a055c7b92455` [strategy] (literature_supported) — Upper-band crossings should be used to detect non-null dependence in significance bands.
  > Use upper-band crossings to detect non-null dependence.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8b0f03054da11f84` [interpretation] (literature_supported) — Largest Lyapunov exponent differentiates deterministic chaos from stochastic noise when sample size permits.
  > Differentiates deterministic chaos from stochastic noise (when sample size permits)
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8d2bbe61fa3507b7` [check] (literature_supported) — Numerical inflation should be treated as a warning and verified with multiple backends and sample-size stress.
  > Numerical inflation `directness_ratio > 1.0` estimator instability, finite-sample effects Treat as warning; verify with multiple backends and sample-size stress
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8dad330ef2b8c2c9` [procedure_step] (literature_supported) — F1 should be used at the start of any triage pass because it is the anchor all other diagnostics contextualise.
  > At the start of any triage pass; F1 is the anchor all other diagnostics contextualise.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8de83114ee5d299d` [interpretation] (literature_supported) — The compute_surrogates field indicates whether significance was actually computed.
  > compute_surrogates` Whether significance was actually computed
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-910d5c067ea619cf` [procedure_step] (literature_supported) — F4 should be used to characterise the linear spectral structure of a series as complementary context alongside the nonlinear AMI profile.
  > To characterise the *linear* spectral structure of a series as complementary context alongside the *nonlinear* AMI profile.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-92cdbc6b7d262834` [interpretation] (literature_supported) — The toolkit's triage should indicate when the workflow should abstain and fall back to baselines.
  > When should the workflow abstain and fall back to baselines?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-935d90355873c7a5` [expectancy] (literature_supported) — The lower significance band is near zero for MI and usually not operationally informative.
  > Lower band is near zero for MI and usually not operationally informative.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-943badfd7c61d2b4` [interpretation] (literature_supported) — Exogenous screening with FDR prunes redundant drivers and controls false discovery rate across many tests.
  > Prunes redundant drivers; controls false discovery rate across many tests
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-949da5078b228aae` [check] (literature_supported) — F7 should not be used as a replacement for individual deep-dive analysis on flagged series.
  > As a replacement for individual deep-dive analysis on flagged series: batch ranking surfaces which series to investigate, not why.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-9550b0e4ed916b44` [check] (literature_supported) — Significance not assessed is different from surrogates computed with no lags clearing the band, and one should use compute_surrogates to distinguish those states.
  > "Significance not assessed" is different from "surrogates were computed and no lags cleared the band." Use `compute_surrogates` to distinguish those states. Only interpret `n_sig_raw_lags`, `n_sig_partial_lags`, or other significant-lag fields as evidence about absent significance when `compute_surrogates` is `true`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-976381c9c65dc8d7` [interpretation] (literature_supported) — The blocked field indicates whether triage completed at all.
  > Field What it tells you --- --- `blocked` Whether triage completed at all
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-9ceadd7629751a08` [interpretation] (literature_supported) — Transfer Entropy values are estimator- and null-model-aware diagnostics, not causal proof.
  > TE values are estimator- and null-model-aware diagnostics, not causal proof.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-9e6dc6ee2a9f59ad` [misconception] (literature_supported) — A True value for is_non_monotone should not be treated as an estimation artefact or an error - it is correct and expected for seasonal series.
  > Do not treat a `True` value as an estimation artefact or an error - it is correct and expected for seasonal series.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-9ea919497a5681f1` [check] (literature_supported) — F5 should not be used as a causal or classification proof because a positive λ̂ does not distinguish deterministic chaos from coloured stochastic noise.
  > As a causal or classification proof: a positive $\hat{\lambda}$ does not distinguish deterministic chaos from coloured stochastic noise.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a642c4504cd09b3e` [concept] (literature_supported) — The forecast prep contract is the final deterministic surface before external frameworks take over.
  > The contract is the final deterministic surface before external frameworks take over.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a6aefd04832669ef` [check] (literature_supported) — In exogenous screening results, 6 out of 7 cases have warning horizons and at least one directness_ratio > 1.0, which should be treated as an estimation warning, not scientific evidence of stronger conditioned dependence.
  > 6/7 cases have warning horizons and at least one `directness_ratio > 1.0`, which should be treated as an estimation warning, not scientific evidence of stronger conditioned dependence.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a7bab55744cba271` [interpretation] (literature_supported) — When directness_ratio exceeds 1.0, it is an anomaly boundary indicating the residual approximation has broken down at that horizon, and one should treat the ratio as informative only below 1.0.
  > The correct interpretation: treat the ratio as informative only below 1.0; values above 1.0 indicate the residual approximation has broken down at that horizon.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-aa3bad6cf4645015` [cue] (literature_supported) — F4 should be used when divergence between high AMI and low Ω arises because this pattern signals that predictability comes from nonlinear dynamics.
  > When a divergence between high AMI and low Ω arises: this pattern signals that predictability comes from nonlinear dynamics, not spectral structure.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ab457177a15fba89` [check] (literature_supported) — Short, sparse, and degenerate distributions should be treated as fragile for MI estimation.
  > Treat short, sparse, and degenerate distributions as fragile for MI estimation.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-abfc67f32b61b659` [strategy] (literature_supported) — Where phase-randomised surrogate bands exist via significance_service, the lagged-exogenous flow reuses them including at k=0 once the lag-range extension is in place.
  > Wherever phase-randomised surrogate bands already exist (via `significance_service`), the lagged-exogenous flow reuses them - including at $k = 0$ once the lag-range extension is in place.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-afa5f0d661961065` [interpretation] (literature_supported) — Transfer Entropy significance is evaluated against phase-randomized surrogate bands.
  > Significance is evaluated against phase-randomized surrogate bands and should be interpreted with the same surrogate caveats used elsewhere in this repository.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-b71bb920566c79ff` [interpretation] (literature_supported) — When directness_ratio exceeds 1.0, the system flags arch_suspected as a warning or anomaly boundary, not positive evidence of any particular architecture.
  > When `directness_ratio > 1.0` the system flags `arch_suspected`. This flag is a **warning or anomaly boundary, not positive evidence** of any particular architecture.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-b76d0772fa3b2025` [check] (literature_supported) — F8 should not be used without BH FDR correction when many drivers are tested simultaneously because uncorrected p-values will inflate false-positive rates.
  > Without BH FDR correction when many drivers are tested simultaneously: uncorrected $p$-values will inflate false-positive rates.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-bc38f8bc36c7b27b` [strategy] (literature_supported) — When phase-randomised surrogate significance bands are available, they extend to k=0 in v0.3.2 so the strength of instantaneous coupling can be assessed against the noise floor.
  > When surrogate significance bands are available (phase-randomised surrogates), they extend to $k = 0$ so the strength of the instantaneous coupling can be assessed against the noise floor.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c05256a493ed49b7` [concept] (literature_supported) — The toolkit's triage should suggest which model families are plausible enough to test next.
  > Which model families are plausible enough to test next?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c990f0c03b6728cd` [interpretation] (literature_supported) — If a derived feature yields strictly lower profile values than the unaggregated series, the transformation has destroyed predictive information.
  > If a derived feature - for example, a box-aggregated or coarsely discretised version of the raw series - yields strictly lower profile values than the unaggregated series, the transformation has destroyed predictive information.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-cca6ba358c257c2a` [check] (literature_supported) — F6 should not be used as a sole decision-maker because it is a complementary contextual tool and the forecastability ceiling is set by AMI, not entropy.
  > As a sole decision-maker: F6 is a complementary contextual tool, not a forecastability measure. The forecastability ceiling is set by AMI, not entropy.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d31d4b4796bb125a` [interpretation] (literature_supported) — Backend deltas should be interpreted as effect-size diagnostics, not absolute truth.
  > Interpret these as effect-size diagnostics, not absolute truth.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d405857082dac931` [check] (literature_supported) — F8 should not be used as a causal screening tool because it detects predictive dependence, not causal direction.
  > As a causal screening tool: F8 detects predictive dependence, not causal direction.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d586c094984966f5` [check] (literature_supported) — The horizon-specific AMI curve should never be collapsed before analysis.
  > Horizon-specific curve, never collapsed before analysis.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-da2a5962fc3f5bdf` [interpretation] (literature_supported) — Predictive info learning curves avoids over-long or too-short lookback windows.
  > Avoids over-long or too-short lookback windows
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-dbf7848941afc840` [expectancy] (literature_supported) — AMI-error discrimination is weaker in Daily frequency than in Hourly/Weekly/Quarterly/Yearly.
  > Expect weaker AMI-error discrimination in Daily frequency than in Hourly/Weekly/Quarterly/Yearly.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-dc64b584d30d42bb` [interpretation] (literature_supported) — Very low directness_ratio in sine_wave (0.0157) and air_passengers (0.0993) supports compact structured models over long-lag complexity.
  > Very low `directness_ratio` in `sine_wave` (0.0157) and `air_passengers` (0.0993) supports compact structured models over long-lag complexity.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e433c9acfb61e068` [procedure_step] (literature_supported) — F6 should be used alongside F5 (when enabled) for convergence evidence on chaos versus stochasticity.
  > Alongside F5 (when enabled) for convergence evidence on chaos vs stochasticity.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ed1afb107c22da36` [interpretation] (literature_supported) — Batch diagnostic ranking provides objective multi-criteria ranking across an entire signal portfolio.
  > Objective multi-criteria ranking across an entire signal portfolio
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-edd8f224d7221de6` [procedure_step] (literature_supported) — F3 combined with F1 identifies which horizons are informative and how much history informs the one-step horizon.
  > In combination with F1: F1 identifies *which* horizons are informative; F3 identifies *how much* history informs the one-step horizon.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ee652772963bae87` [failure_mode] (literature_supported) — F3 should be avoided for non-stationary series because random-walk-like dynamics produce inflated estimates that grow with k without plateauing.
  > For non-stationary series: random-walk-like dynamics produce inflated estimates that grow with $k$ without plateauing.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ee9e1c2c6b497796` [norm] (literature_supported) — For standard cross-correlation, the significance field stays None and significance_source="not_computed".
  > Significance field stays `None`; `significance_source = "not_computed"`
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f17826be9ca6c52d` [strategy] (literature_supported) — When numeric correctness matters, users should trace back to `TriageResult` and the stable package facade.
  > When numeric correctness matters, trace back to `TriageResult` and the stable package facade.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f5b8f2a907cdeb9f` [failure_mode] (literature_supported) — For highly periodic series, phase-randomized FFT surrogates can make significance tests conservative or uninformative even when the underlying series is obviously structured.
  > For highly periodic series, they can make significance tests conservative or uninformative even when the underlying series is obviously structured.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f9b9ad7180b2a1f5` [concept] (literature_supported) — The reporting package contains deterministic interpretation and Markdown/report builders.
  > reporting/` Deterministic interpretation and Markdown/report builders
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-fa160f653ed647fc` [check] (literature_supported) — F1 should not be used as the sole decision-maker when surrogate significance bands are unavailable due to too-short series.
  > As the sole decision-maker when surrogate significance bands are unavailable (too-short series): treat the curve as indicative, not authoritative.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-fa9bb8b511e390d3` [concept] (literature_supported) — When compute_surrogates is false, significance was skipped or suppressed, which is different from a run where surrogates were computed and no lags were significant.
  > When `compute_surrogates` is `false`, significance was skipped or suppressed. That is different from a run where surrogates were computed and no lags were significant.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-fc6acd9178c25076` [concept] (literature_supported) — Blocked result means the workflow could not support the requested computation, which is different from "no forecastable structure."
  > A blocked result means the workflow could not support the requested computation.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-fe58d6817c3cdbb0` [rationale] (literature_supported) — The workflow is intentionally conservative and does not prescribe a winner but instead provides evidence, legal inputs, and where model search can begin without pretending the data are cleaner than they are.
  > The workflow is intentionally conservative. It does not say, "fit this winner." It says, "here is the evidence; here are the legal inputs; here is where model search can begin without pretending the data are cleaner than they are."
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)

### Synthetic / rejected claims

- `c-06ca66bfe45cd824` [procedure_step] (synthetic_extrapolation) — F6 should be used to contextualise F1 AMI results and set expectations for model difficulty. (no located evidence)
- `c-195e87819ca7701a` [interpretation] (synthetic_extrapolation) — A directness_ratio greater than 1 is a numerical or assumption warning often due to ARCH-type behavior, not a physical contradiction. (no located evidence)
- `c-2c24a2845dacc8fb` [representation] (synthetic_extrapolation) — The directness_ratio r is computed as the ratio of AUC of pAMI to AUC of AMI.
  > Directness summary `directness_ratio`: \[ r = \frac{\operatorname{AUC}(\tilde{I}_h)}{\operatorname{AUC}(I_h)} \]
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md)
- `c-2c5f23c99204afbb` [representation] (synthetic_extrapolation) — The reporting/interpretation.py module owns deterministic interpretation output. (no located evidence)
- `c-32c5147f0dacffd8` [rationale] (synthetic_extrapolation) — The Data-Processing Inequality does not imply that F(h; T(I_t)) = 0 is the expected outcome; useful transforms may preserve nearly all forecastability and the DPI is a ceiling constraint, not a pessimistic prediction. (no located evidence)
- `c-3e3d48c5c1cc514e` [representation] (synthetic_extrapolation) — F2 compression ratio is a cross-series comparable metric for comparing multiple series. (no located evidence)
- `c-5523cecf25395b41` [interpretation] (synthetic_extrapolation) — The fingerprint release is intentionally univariate-first and AMI-first, and the routing output is heuristic family guidance, not exact-model selection and not a multivariate conditional-MI claim. (no located evidence)
- `c-5bc7c453e36bd717` [representation] (synthetic_extrapolation) — The lag_role field on LaggedExogProfileRow and LaggedExogSelectionRow indicates chronological role: "instant" for k=0 (contemporaneous association) or "predictive" for k≥1 (fixed-lag predictive association).
  > Every `LaggedExogProfileRow` and `LaggedExogSelectionRow` carries a `lag_role` field
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md)
- `c-6941fc189355cd8f` [interpretation] (synthetic_extrapolation) — The readiness_status field indicates whether the data is clear, warning-level, or blocked.
  > readiness_status` Whether the data is clear, warning-level, or blocked
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md)
- `c-83bd107b9f92d559` [check] (synthetic_extrapolation) — When compute_surrogates is false, significance was not assessed for that run, which is distinct from computed but non-significant results. (no located evidence)
- `c-856cb8ebd2be354e` [representation] (synthetic_extrapolation) — On v0.3.3 and later, `bundle.recommendation.confidence_label` can be `abstain` when the routing policy emits no primary families. (no located evidence)
- `c-8d30b97541a263a2` [representation] (synthetic_extrapolation) — The tensor_role field states whether a lag may legitimately enter a lagged-exogenous tensor used for ordinary forecasting, with values "diagnostic", "predictive", or "known_future".
  > The `tensor_role` field states whether the lag may legitimately enter a lagged-exogenous tensor used for ordinary forecasting
  (verdict insufficient [adds_content, connective_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md)
- `c-aece8a83a8c7aede` [cue] (synthetic_extrapolation) — Decision changes when backend changes are an observable symptom of false confidence from one backend caused by model class mismatch or noisy data.
  > False confidence from one backend decision changes when backend changes model class mismatch or noisy data
  (verdict insufficient [adds_content, connective_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md)
- `c-ba75b0e7ff974f18` [cue] (synthetic_extrapolation) — Sharp pAMI spikes at isolated lags only for tree backends are an observable symptom of overfitting in nonlinear backends caused by the backend fitting noise in conditioning space.
  > Overfitting in nonlinear backends sharp pAMI spikes at isolated lags only for tree backends backend fits noise in conditioning space
  (verdict insufficient [connective_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md)
- `c-bbb3d521c1738b03` [expectancy] (synthetic_extrapolation) — Occasional false-positive horizons in informative_horizons are expected, especially for AR(1) processes at long lags. (no located evidence)
- `c-bc134346ee748c5a` [interpretation] (synthetic_extrapolation) — A directness_ratio of approximately 1 indicates mostly direct structure. (no located evidence)
- `c-d22741377a176c37` [interpretation] (synthetic_extrapolation) — A directness_ratio much less than 1 indicates mostly mediated structure. (no located evidence)
- `c-e68b6e04ba5d4ad3` [concept] (synthetic_extrapolation) — Routing validation audits deterministic routing against controlled archetypes and sanity panels but does not train or benchmark forecasting models. (no located evidence)

### UNKNOWN / thin / unverified / unexamined slots

- concept: thin
- decision: unknown
- cue: thin
- check: thin
- failure_mode: thin
- norm: thin
- rationale: thin
- procedure_step: thin

### Unknown placeholders

- `c-a3b40767597fb3fb` [decision] — What conditions determine which option is chosen in Interpreting forecastability results?

## Area: Understanding horizon-wise forecastability concepts

### Supported claims

- `c-00beaeea1bbcce97` [norm] (literature_supported) — The v0.3.0 shipped cross_pami method remains target_only conditioned and covers k∈{1,...,K_max} only, with semantics unchanged in v0.3.2.
  > The v0.3.0 `cross_pami` curve remains `target_only` conditioned and covers $k \in \{1, \dots, K_{\max}\}$ only.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-020d2cdaec4af775` [concept] (literature_supported) — pAMI measures how much dependence remains after removing linear mediation through intermediate lags.
  > pAMI How much dependence remains after removing linear mediation through intermediate lags?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-02471dfd7d502aa5` [cue] (literature_supported) — Triage is not a replacement for full backtesting or deployment validation.
  > Not a replacement for full backtesting or deployment validation
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-031765460e495629` [concept] (literature_supported) — The horizons field contains 1-based lag indices [1, ..., H].
  > `horizons` `list[int]` 1-based lag indices $[1, \dots, H]$
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-043dbf002770f388` [concept] (literature_supported) — The review_horizons field contains all informative horizons - model building targets.
  > `review_horizons` `list[int]` All informative horizons - model building targets
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-080bfc398b3aad1f` [concept] (literature_supported) — Exogenous analysis identifies which external drivers show lead-lag signal with the target.
  > Exogenous analysis Which external drivers show lead-lag signal with the target?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0c7cccfdfe8d5874` [concept] (literature_supported) — The peak_horizon field contains h* = argmax_h F(h), the 1-based index with maximum forecastability.
  > `peak_horizon` `int` $h^* = \arg\max_h F(h)$ (1-based index)
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0cac27b3131df938` [concept] (literature_supported) — Triage determines if the signal is ready for dependence analysis and which method path should run.
  > Triage Is the signal ready for dependence analysis, and which method path should run?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0d195aa9127c759c` [concept] (literature_supported) — pAMI is a nonlinear analog of the partial autocorrelation function (PACF).
  > Nonlinear analog of PACF (direct dependence after conditioning on intermediate lags).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0d74f7eb45a93314` [concept] (literature_supported) — The toolkit's triage should identify which variables are safe to use without leakage.
  > Which variables are safe to use without leakage?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-1321f8253a6a450f` [concept] (literature_supported) — Forecastability profile answers which horizons carry usable predictive information.
  > Forecastability profile (F1) Which horizons carry usable predictive information?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-147115fe8f2a62ea` [expectancy] (literature_supported) — Reliable phase-space coverage for largest Lyapunov exponent requires n >> 10^m, which for the default m = 3 means n >> 1000, and results for shorter series are indicative only.
  > Reliable phase-space coverage requires $n \gg 10^m$. For the default $m = 3$ this means $n \gg 1000$. Results for shorter series are indicative only.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-150871fa9f37946b` [cue] (literature_supported) — Forecastability profile inherits AMI estimator reliability and requires surrogates for epsilon anchoring.
  > Inherits AMI estimator reliability; requires surrogates for epsilon anchoring
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-1a1a3d9f0c351840` [cue] (literature_supported) — Results from pAMI differ between the linear and RF backends, with the linear backend being faster and more stable while the RF backend may capture more nonlinear residual structure but introduces additional noise for short series.
  > Results differ between the linear (default) and RF backends. The linear backend is faster and more stable; the RF backend may capture more nonlinear residual structure but introduces additional noise for short series.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-1a4658f1577b2d9b` [concept] (literature_supported) — The Forecastability Profile compresses the AMI curve into a set of actionable fields: the set of horizons where forecastability clears a significance threshold (the informative horizon set), the peak horizon, structural shape flags, and model-selection recommendations.
  > The profile compresses the AMI curve into a set of actionable fields: the set of horizons where forecastability clears a significance threshold (the *informative horizon set* $\mathcal{H}_\varepsilon$), the peak horizon, structural shape flags, and model-selection recommendations.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-1ba655fcef579961` [cue] (literature_supported) — AMI values are unreliable directly at horizons beyond frequency-specific caps: Yearly 6, Quarterly 8, Monthly 18, Weekly 13, Daily 14, Hourly 48.
  > Directly at horizons beyond the frequency-specific cap (Yearly 6, Quarterly 8, Monthly 18, Weekly 13, Daily 14, Hourly 48): AMI values beyond these caps are unreliable.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-2c3348a6673eed2e` [mental_model] (literature_supported) — Backend comparison is diagnostic, not proof that one backend is universally superior.
  > Backend comparison is diagnostic, not proof that one backend is universally superior.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-2df7db6283080ac0` [norm] (literature_supported) — This toolkit should not be used for comparing very short windows where minimum sample assumptions are not met.
  > Comparing very short windows where minimum sample assumptions are not met.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-2eaebaa88a212810` [prerequisite] (literature_supported) — The kNN mutual information estimator with n_neighbors=8 is asymptotically consistent but has positive bias for finite samples, particularly at short series lengths and large lag indices.
  > The kNN mutual information estimator (Kraskov et al., 2004; `n_neighbors=8`) is asymptotically consistent but has positive bias for finite samples, particularly at short series lengths and large lag indices.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-2f5425786a617b4f` [concept] (literature_supported) — F8 measures cross-series mutual information between a target series and candidate exogenous drivers at each forecast horizon, filtered by Benjamini-Hochberg FDR control.
  > The cross-series mutual information between a target series and one or more candidate exogenous drivers at each forecast horizon, filtered by Benjamini-Hochberg FDR control, to screen which exogenous variables carry statistically detectable predictive signal.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-33609c31a8ef689e` [concept] (literature_supported) — The epsilon field contains the resolved threshold ε for H_ε.
  > `epsilon` `float` Resolved threshold $\varepsilon$ for $\mathcal{H}_\varepsilon$
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3c77e2cbb1f7e3ee` [cue] (literature_supported) — Predictive info learning curves uses kNN MI which is unreliable for k > 5-8 at small n and mandatory reliability warnings are required.
  > kNN MI unreliable for k > 5-8 at small n; mandatory reliability warnings
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3d335684b4c82440` [concept] (literature_supported) — Univariate forecastability triage is used to determine whether the target series itself carries useful predictive structure.
  > Use this when you want to know whether the target series itself carries useful predictive structure.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3fec04acd8d0297e` [concept] (literature_supported) — AMI at horizon h is defined as the mutual information between X_t and X_{t+h}.
  > Paper-native metric AMI at horizon \(h\): \[ I_h = I(X_t; X_{t+h}) \]
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-41bc88a961c89484` [concept] (literature_supported) — AMI answers the question of whether horizon-specific dependence is worth exploiting at all.
  > AMI Is there horizon-specific dependence worth exploiting at all?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-43c00c313309cbd7` [cue] (literature_supported) — IT limit diagnostics ceiling holds under log loss only and exploitation ratio is deferred.
  > Ceiling holds under log loss only; exploitation ratio deferred (pre-model repo)
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-43d3dd12bc2ea848` [failure_mode] (literature_supported) — Phase-randomized surrogate significance bands require a minimum series length to produce stable quantile estimates, and when the series is too short, significance may be unavailable and surrogate bands are omitted.
  > Phase-randomized surrogate significance bands require a minimum series length to produce stable quantile estimates. When the series is too short, significance may be unavailable and the surrogate bands are omitted.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-44478fab721cadb7` [concept] (literature_supported) — F7 runs F1-F4 and F6 deterministically across a panel of series and produces a ranked diagnostic table.
  > Runs F1-F4 and F6 deterministically across a panel of series and produces a ranked diagnostic table, enabling rapid comparison of forecastability structure across many signals in one pass.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-477542b2629c3dda` [norm] (literature_supported) — pAMI does not prove direct causality or Granger causality, but instead quantifies approximate direct dependence after removing mediated paths.
  > pAMI quantifies approximate direct dependence after removing mediated paths. It does not prove direct causality or Granger causality.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4a60079601c7e25a` [failure_mode] (literature_supported) — The conditioning-out step in residualisation removes only the component of dependence that is linearly predictable from the intermediate lags, leaving nonlinear residual dependence that the linear backend cannot fully capture in pAMI.
  > The conditioning-out step removes only the component of dependence that is linearly predictable from the intermediate lags. Nonlinear residual dependence that the linear backend cannot capture remains in the AMI but may not be fully removed from pAMI.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4b1c8c5f88a9b4c8` [concept] (literature_supported) — IT limit diagnostics answers what the theoretical ceiling on prediction improvement is.
  > IT limit diagnostics (F2) What is the theoretical ceiling on prediction improvement?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4bb192a32090aaf8` [failure_mode] (literature_supported) — The Rosenstein algorithm for largest Lyapunov exponent is sensitive to noise, non-stationarity, and the choice of embedding parameters, such that small parameter changes can produce meaningfully different lambda hat values.
  > The Rosenstein algorithm and Takens embedding are sensitive to noise, non-stationarity, and the choice of embedding parameters ($m$, $\tau$, Theiler window, evolution time $s$). Small parameter changes can produce meaningfully different $\hat{\lambda}$ values.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4dfc648b53295bce` [failure_mode] (literature_supported) — Learning curve plateaus from F3 should not be used as proof of information exhaustion because estimator saturation can mimic genuine plateaus.
  > Using learning curve plateaus (F3) as proof of information exhaustion - estimator saturation can mimic genuine plateaus.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4fe71c9a44ca4122` [concept] (literature_supported) — Lagged-exogenous triage classifies drivers by lag role and emits a sparse lag map that can be used for downstream tensor construction.
  > The lagged-exogenous surface classifies drivers by lag role and emits a sparse lag map that can be used for downstream tensor construction.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-50a455f13a13bd70` [check] (literature_supported) — Batch diagnostic ranking requires composite weighting across incommensurable scales to be transparent.
  > Composite weighting across incommensurable scales must be transparent
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-50d2c881f5896b3c` [expectancy] (literature_supported) — Seasonal and quasi-periodic processes routinely exhibit higher AMI at seasonal lags than at short lags.
  > Seasonal and quasi-periodic processes routinely exhibit higher AMI at seasonal lags than at short lags.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-50fc7b0f8e7ef7f4` [rationale] (literature_supported) — Conditioning on target history in Transfer Entropy controls for autocorrelation-driven carryover in the target variable.
  > Conditioning on target history controls for autocorrelation-driven carryover in \(Y\).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-510d49adfa4082a3` [concept] (literature_supported) — pAMI is a project extension, not a paper-native metric, and uses linear residualisation so nonlinear mediation is not removed.
  > pAMI is a project extension, not a paper-native metric. It uses linear residualisation, so nonlinear mediation is not removed.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-541ee1f6ab92a6aa` [cue] (literature_supported) — AMI detects dependence, not causality or guaranteed model gains.
  > Detects dependence, not causality or guaranteed model gains
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-595c89287b0ba5f4` [concept] (literature_supported) — Predictive info learning curves answer how many past lags the series actually needs.
  > Predictive info learning curves (F3) How many past lags does the series actually need?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5ae8a57e691e2b17` [concept] (literature_supported) — Positive Transfer Entropy indicates added predictive information from source history beyond target-only history.
  > Positive TE indicates added predictive information from source history beyond target-only history.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5c50cdff1fbaf42d` [concept] (literature_supported) — The informative_horizons field contains H_ε - horizons where F(h) ≥ ε.
  > `informative_horizons` `list[int]` $\mathcal{H}_\varepsilon$ - horizons where $F(h) \ge \varepsilon$
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5caf1bc6ad85c84b` [cue] (literature_supported) — Standard cross-correlation is a cheap linear baseline that retains sign and covers k=0, but cannot detect symmetric nonlinear couplings.
  > Cheap linear baseline; sign is retained (no premature absolute-value collapse) - Covers $k = 0$, giving the contemporaneous correlation as a diagnostic reference - **Cannot detect symmetric nonlinear couplings**
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5d3c43042ccb35ba` [concept] (literature_supported) — Phase-randomized FFT surrogates preserve the power spectrum.
  > Phase-randomized FFT surrogates preserve the power spectrum.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5fdbc156ebef1353` [norm] (literature_supported) — Experimental diagnostics such as F5 Lyapunov should not be treated as automated decision criteria without expert review.
  > Treating experimental diagnostics (F5 Lyapunov) as automated decision criteria without expert review.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-63aa264242193728` [cue] (literature_supported) — Entropy-based complexity is amplitude-blind and the tie-breaking rule must be fixed.
  > PE is amplitude-blind; tie-breaking rule must be fixed
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6b0d51a3406445eb` [cue] (literature_supported) — Exogenous screening with FDR uses greedy forward selection and redundancy penalty is a configurable approximation.
  > Greedy forward selection; redundancy penalty is configurable approximation
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6d72b5ca901657cb` [concept] (literature_supported) — The forecastability fingerprint surface summarizes AMI-first information geometry into compact diagnostic features and deterministic model-family routing hints.
  > The fingerprint surface summarizes AMI-first information geometry into compact diagnostic features and deterministic model-family routing hints.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6eca93cb644d1902` [concept] (literature_supported) — AMI is a nonlinear analog of the autocorrelation function (ACF).
  > Nonlinear analog of ACF (total dependence at lag \(h\)).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-719558607fd4468f` [expectancy] (literature_supported) — The minimum recommended series length is approximately n ≥ 3 × H_max, where H_max is the maximum evaluation horizon, below which MI estimates are unreliable for lags close to H_max.
  > Approximately $n \geq 3 \times H_{\max}$, where $H_{\max}$ is the maximum evaluation horizon. Below this threshold, MI estimates are unreliable for lags close to $H_{\max}$.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-73867d43cf16f89e` [concept] (literature_supported) — F5 measures the average rate of exponential divergence of nearby trajectories in a reconstructed phase space using Takens delay embedding and Rosenstein algorithm.
  > The average rate of exponential divergence of nearby trajectories in a reconstructed phase space (Takens delay embedding + Rosenstein algorithm), yielding $\hat{\lambda}$: positive values are *consistent with* chaotic dynamics, but stochastic noise can also produce positive values.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-753a7aacc87f29c1` [norm] (literature_supported) — pAMI should not be treated as an exact nonlinear conditional mutual information estimate.
  > Treating pAMI as an exact nonlinear conditional mutual information estimate.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-75c34cafb73f075f` [concept] (literature_supported) — The Forecastability Profile describes the full horizon-wise relationship between the target series and the available information set, from lag 1 to a user-specified maximum lag H.
  > It describes the full horizon-wise relationship between the target series and the available information set, from lag 1 to a user-specified maximum lag $H$.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-75dbed74d0cff629` [norm] (literature_supported) — This toolkit should not be used for setting maintenance policy thresholds without domain constraints and risk-cost modeling.
  > Setting maintenance policy thresholds without domain constraints and risk-cost modeling.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7895f8100ac932cc` [procedure_step] (literature_supported) — When surrogates are computed, epsilon is set to the minimum AMI value among lags whose AMI exceeds the 97.5th percentile of the surrogate distribution.
  > **When surrogates are computed** - $\varepsilon$ is set to the minimum AMI value among lags whose AMI exceeds the 97.5th percentile of the surrogate distribution.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-792885af51e4e3f6` [concept] (literature_supported) — F4 measures the concentration of spectral power across frequency bins, normalised to [0, 1], with Ω = 1 for perfectly periodic signals and Ω → 0 for white noise.
  > The concentration of spectral power across frequency bins, normalised to $[0, 1]$: Ω = 1 for a perfectly periodic signal, Ω → 0 for white noise, quantifying linear-structure predictability independently of AMI.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-794b1929aaf9c87a` [concept] (literature_supported) — Transfer Entropy (TE) at lag h measures directional predictive dependence from X to Y as the mutual information between Y_t and X_{t-h} conditioned on Y's history from t-1 to t-h+1.
  > Directional extension metric Transfer Entropy (TE) at lag \(h\): \[ TE(X \to Y \mid h) = I(Y_t ; X_{t-h} \mid Y_{t-1},\ldots,Y_{t-h+1}) \]
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-79e653832ab89246` [concept] (literature_supported) — DTW (Dynamic Time Warping), FastDTW, and ShapeDTW solve elastic-alignment similarity by searching for alignment that minimises path-cumulated distance, but do not produce fixed-lag predictive feature sets or respect chronological causality required by forecasting tensors.
  > DTW (Dynamic Time Warping), FastDTW, and ShapeDTW solve **elastic-alignment similarity**: they search for the alignment $\pi$ that minimises a path-cumulated distance between two time series. They do not: - produce a fixed-lag predictive feature set - respect the chronological causality required by forecasting tensors
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7b33637f32110660` [concept] (literature_supported) — The package is a deterministic pre-model diagnostic layer, not a downstream model-training or forecasting library.
  > This package is a deterministic pre-model diagnostic layer, not a downstream model-training or forecasting library.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7be7d8e5cbde9ed4` [concept] (literature_supported) — F3 measures mutual information between a k-step past embedding and the one-step-ahead future to identify the minimal sufficient lookback length.
  > The mutual information between a $k$-step past embedding and the one-step-ahead future, evaluated for $k = 1 \ldots K$, to identify the minimal sufficient lookback length where additional history yields negligible extra predictive information.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8382cbdd5c5c6e29` [concept] (literature_supported) — AMI includes both direct and mediated lag paths.
  > Includes both direct and mediated lag paths.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8627cbdd8787a692` [concept] (literature_supported) — Transfer Entropy is directional; in general TE(X → Y) is not equal to TE(Y → X).
  > Directional predictive dependence: in general \(TE(X \to Y) \neq TE(Y \to X)\).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8bcff0024dacaf2c` [concept] (literature_supported) — AMI is horizon-specific, kNN-based, and uses phase-surrogate significance bands.
  > AMI is paper-aligned (horizon-specific, kNN-based, with phase-surrogate significance bands).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8be817ba0cc340ba` [concept] (literature_supported) — pAMI uses a linear-residual approximation rather than exact conditional mutual information.
  > pAMI is a project extension that uses a linear-residual approximation rather than exact conditional mutual information.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8f8e1923b87ad171` [concept] (literature_supported) — The model_now field provides an immediate model-complexity recommendation (HIGH / MEDIUM / LOW / NONE).
  > `model_now` `str` Immediate model-complexity recommendation (HIGH / MEDIUM / LOW / NONE)
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-913badca64a7ed37` [concept] (literature_supported) — Largest Lyapunov exponent answers whether a series shows sensitivity to initial conditions.
  > Largest Lyapunov exponent (F5) Does this series show sensitivity to initial conditions?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-947c6927ca835d8a` [concept] (literature_supported) — Entropy-based complexity answers whether a series is periodic, chaotic, or stochastic.
  > Entropy-based complexity (F6) Is this series periodic, chaotic, or stochastic?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-9573da8242fe1a40` [concept] (literature_supported) — F6 measures normalised permutation entropy and spectral entropy to classify disorder level into a complexity band.
  > The normalised permutation entropy and spectral entropy of the series, combined to classify its disorder level into a complexity band (regular / moderate / noise-like), providing structural context for the AMI results.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-977ca77fbb8dd9fb` [cue] (literature_supported) — pAMI is a linear approximation to conditional MI and can under-capture nonlinear mediation.
  > Linear approximation to conditional MI; can under-capture nonlinear mediation
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-97859db84d78c736` [failure_mode] (literature_supported) — The linear_residual backend misses nonlinear mediation.
  > linear_residual` Fast, stable, interpretable baseline Misses nonlinear mediation
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-996611e831aa1eb3` [concept] (literature_supported) — The toolkit's triage should determine whether there is seasonal structure worth modeling.
  > Is there a seasonal structure worth modeling?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-99e767adf11feef3` [concept] (literature_supported) — A strictly decreasing forecastability profile holds for simple AR processes and many white-noise-corrupted signals, but is not a universal requirement.
  > A strictly decreasing forecastability profile - $F(1) \ge F(2) \ge \cdots$ - holds for simple AR processes and many white-noise-corrupted signals. However, it is **not** a universal requirement.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-9d6dafa4d6cd94ea` [concept] (literature_supported) — The is_non_monotone field is True if F(h) increases at any h > 1.
  > `is_non_monotone` `bool` `True` if $F(h)$ increases at any $h > 1$
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-9e9a2991b23920ac` [expectancy] (literature_supported) — In finite samples with residual approximation, occasional pAMI > AMI can occur.
  > In finite samples with residual approximation, occasional \(\tilde{I}_h > I_h\) can occur.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a2591283bf7e55e0` [decision] (literature_supported) — LLE is intentionally excluded from the batch triage ranking table F7 by design.
  > LLE is intentionally excluded from the batch triage ranking table (F7) by design.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a294d89b66d79105` [concept] (literature_supported) — Spectral predictability answers how much linear predictable structure exists.
  > Spectral predictability (F4) How much linear predictable structure exists?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a46f1f28c4e5c48b` [concept] (literature_supported) — A known-future exogenous covariate has its k=0 value legitimately observed before the target must be predicted, such as calendar features, holidays, tariffs, or planned promotional events.
  > A "known-future" exogenous covariate is one whose $k=0$ value is legitimately observed **before** $Y_t$ must be predicted: calendar features, holidays, regulator-set tariffs, planned promotional events.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a57574d333d7a5a5` [cue] (literature_supported) — Largest Lyapunov exponent is experimental and unreliable at finite sample sizes, gated behind config flag, and never auto-included in triage score.
  > Experimental - unreliable at finite sample sizes; gated behind config flag; never auto-included in triage score
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a73dfb9424c4297e` [rationale] (literature_supported) — kNN MI estimators detect nonlinear dependence directly through local density structure.
  > kNN MI estimators detect this dependence directly through local density structure.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a9704cb5a8876907` [concept] (literature_supported) — pAMI approximates conditional mutual information via linear or optional RF residualisation, not by exact conditional MI estimation.
  > pAMI is a **project extension** and is not paper-native. It approximates $I(X_t; X_{t+h} \mid X_{t+1}, \ldots, X_{t+h-1})$ via linear (or optional RF) residualisation, not by exact conditional MI estimation.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-aaf17f6c1f8dd528` [representation] (literature_supported) — The metrics/metrics.py module is the core surface for AMI and pAMI computation.
  > `metrics/metrics.py` is the core AMI and pAMI computation surface.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ab63cb11575f8c4b` [concept] (literature_supported) — Exogenous screening with FDR answers which external drivers add genuine predictive value after redundancy.
  > Exogenous screening with FDR (F8) Which external drivers add genuine predictive value after redundancy?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-abaa9cb7e59f2b24` [cue] (literature_supported) — directness_ratio is a diagnostic ratio only and is unstable on weak or noisy short windows.
  > Diagnostic ratio only; unstable on weak/noisy short windows
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-abe15f9e9273dd14` [norm] (literature_supported) — This toolkit should not be used for proving physical causality between variables.
  > Do Not Use This For - Proving physical causality between variables.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ae4ff7674bb2fa84` [mental_model] (literature_supported) — xami_sparse is a triage layer that cheaply prunes redundant lags but does not condition on the driver's own autohistory; stronger conditioning is provided by pcmci_ami (full_mci).
  > `xami_sparse` is a **triage layer** - it cheaply prunes redundant lags to reduce the feature tensor. It does **not** condition on the driver's own autohistory. That stronger conditioning is the job of `pcmci_ami` (`full_mci`)
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-b383d9ab14977bca` [concept] (literature_supported) — Mutual Information measures dependence in the full joint distribution P(X,Y), not only the linear second moment.
  > MI, TE, and GCMI measure dependence in the full joint distribution $P(X, Y)$, not only the linear second moment.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-b7b66ce7ddbf284f` [cue] (literature_supported) — Positive MI bias is strongest when the number of nearest neighbours k is large relative to the local sample density, with short series having high-dimensional lag spaces most affected.
  > Positive MI bias is strongest when the number of nearest neighbours $k$ is large relative to the local sample density. Short series with high-dimensional lag spaces (F3 at large $k$) are most affected.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-bc410b618d7a6d04` [concept] (literature_supported) — directness_ratio answers the question of what share of total dependence appears direct.
  > directness_ratio What share of total dependence appears direct?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-bc594de5c1ed584f` [concept] (literature_supported) — The values field contains AMI values - F(h) for each horizon.
  > `values` `np.ndarray` AMI values - $F(h)$ for each horizon
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-be5a55daceea39a6` [concept] (literature_supported) — pAMI at horizon h is defined as the mutual information between X_t and X_{t+h} conditioned on intermediate lags X_{t+1} through X_{t+h-1}.
  > Project extension metric pAMI at horizon \(h\): \[ \tilde{I}_h = I(X_t; X_{t+h} \mid X_{t+1},\ldots,X_{t+h-1}) \]
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-bff8b6f6f1e86840` [cue] (literature_supported) — Optional narration is a communication layer only and does not create or validate numeric results.
  > Communication layer only; it does not create or validate numeric results
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c042b4eacf50d4d7` [concept] (literature_supported) — Batch diagnostic ranking answers which of 50 or more signals should be modeled first.
  > Batch diagnostic ranking (F7) Which of my 50+ signals should I model first?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c51fdf4c228ff6d2` [misconception] (literature_supported) — A positive largest Lyapunov exponent estimate is consistent with chaotic dynamics, but stochastic coloured noise and non-stationary processes also produce positive estimates, and F5 alone cannot distinguish the two cases.
  > A positive $\hat{\lambda}$ is consistent with chaotic dynamics, but stochastic coloured noise and non-stationary processes also produce positive estimates. F5 alone cannot distinguish the two cases.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c55c4260ff395874` [concept] (literature_supported) — For a target series and candidate exogenous series, practitioners may ask whether the exogenous series co-moves with the target at the same time step, formalized as mutual information at lag k=0.
  > Does $X$ co-move with $Y$ at the **same time step**? $I(X_t\,;\,Y_t)$ $k = 0$ only
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ca37b6e312fc5ce9` [concept] (literature_supported) — Optional narration should explain deterministic outputs to non-specialists.
  > Optional narration How should deterministic outputs be explained to non-specialists?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-cbf35282596649f2` [concept] (literature_supported) — The toolkit is a deterministic forecastability triage toolkit designed for time series forecasting tasks.
  > This repository is a deterministic forecastability triage toolkit for time series.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ce34075d0ab73c27` [concept] (literature_supported) — pAMI removes mediated paths approximately through residualization.
  > Mediated paths Included Removed (approximately with residualization)
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-cec4044b7174de44` [representation] (literature_supported) — The metrics/scorers.py module owns the scorer registry and built-in scorer family metadata.
  > `metrics/scorers.py` owns the scorer registry and built-in scorer family metadata.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d511baec26cc90ca` [cue] (literature_supported) — Spectral predictability captures linear structure only and non-stationary series need detrending.
  > Captures linear structure only; non-stationary series need detrending
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-da4a9683b757595c` [concept] (literature_supported) — The summary field contains a one-sentence human-readable profile description.
  > `summary` `str` One-sentence human-readable profile description
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-dd329be633b2a9b2` [concept] (literature_supported) — The v0.3.0 covariant methods all start from k=1 and silently drop any k=0 structure.
  > The v0.3.0 covariant methods all start from $k = 1$ and silently drop any $k = 0$ structure.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-dfc30bee6ce95ce2` [prerequisite] (literature_supported) — Phase randomisation assumes approximate second-order stationarity, and series with strong trends or regime changes will produce uninformative surrogate bands.
  > Phase randomisation preserves the power spectrum but destroys temporal order. It assumes approximate second-order stationarity. Series with strong trends or regime changes will produce uninformative surrogate bands.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e54e201e768fc908` [norm] (literature_supported) — This toolkit should not be used for replacing rolling-origin forecast evaluation and business KPI tracking.
  > Replacing rolling-origin forecast evaluation and business KPI tracking.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-eab9fbdaed1507b4` [concept] (literature_supported) — The toolkit's triage should classify exogenous drivers as predictive, merely contemporaneous, or useless.
  > Are exogenous drivers predictive, merely contemporaneous, or useless?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-eb30fca06e217ffc` [concept] (literature_supported) — For a target series and candidate exogenous series, practitioners may ask whether the past of the exogenous series carries usable predictive information about the future of the target, formalized as mutual information at lag k≥1.
  > Does the **past** of $X$ carry usable predictive information about the **future** of $Y$? $I(X_{t-k}\,;\,Y_t)$ for $k \ge 1$ $k \ge 1$
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ec2ca0292773a3a5` [concept] (literature_supported) — A monthly series with strong annual seasonality may have F(12) > F(5), producing a non-monotone profile with a secondary peak at h = 12.
  > For example, a monthly series with strong annual seasonality may have $F(12) > F(5)$, producing a non-monotone profile with a secondary peak at $h = 12$.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ed1c97e0c8d035da` [concept] (literature_supported) — Extended forecastability analysis provides an AMI-first extended fingerprint plus a deterministic routing summary in one additive result.
  > Use this when you want the implemented AMI-first extended fingerprint plus a deterministic routing summary in one additive result.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ed56aa8d28a933b8` [concept] (literature_supported) — F2 measures the information-theoretic upper bound on forecastability derived from the AMI curve, including compression ratio and predictability ceiling.
  > The information-theoretic upper bound on forecastability derived from the AMI curve, including compression ratio and predictability ceiling, to quantify how close any model can get to the fundamental limit.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f08b73f32120778a` [cue] (literature_supported) — Exogenous analysis is association-based screening and confounding and common-cause effects can remain.
  > Association-based screening; confounding and common-cause effects can remain
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f13d51e781ecfbbb` [concept] (literature_supported) — The avoid_horizons field contains non-informative horizons - exclude from model feature sets.
  > `avoid_horizons` `list[int]` Non-informative horizons - exclude from model feature sets
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f42874b3a7adbdd7` [concept] (literature_supported) — Forecastability triage should assess readiness, leakage risk, informative horizons, primary lags, seasonality structure, and covariate informativeness.
  > Start with forecastability triage first: readiness, leakage risk, informative horizons, primary lags, seasonality structure, and covariate informativeness.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)

### Synthetic / rejected claims

- `c-00469fe161a2957e` [concept] (synthetic_extrapolation) — CrossAMI measures how much information a covariate lag has about the target, ignoring the target's own history. (no located evidence)
- `c-1c1c8f6fbcb50719` [concept] (synthetic_extrapolation) — In v0.3.2, cross_ami adds the k=0 row so that the multivariate diagnostic is visible alongside the predictive profile, whereas v0.3.0 emitted only k∈{1,...,K_max}.
  > The v0.3.0 `compute_exog_raw_curve` emitted only $k \in \{1, \dots, K_{\max}\}$. v0.3.2 adds the $k = 0$ row
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md)
- `c-1ddea5de90de08a8` [concept] (synthetic_extrapolation) — pAMI asks how much extra lag information remains after closer target history is linearly residualized. (no located evidence)
- `c-23ac757c244a0053` [concept] (synthetic_extrapolation) — The toolkit's triage should identify which target lags are informative. (no located evidence)
- `c-23de30042d89d05e` [rationale] (synthetic_extrapolation) — Epsilon should be defined relative to the surrogate upper band, not as a global absolute constant, to avoid including noise lags or excluding genuinely informative ones as signal strength varies across series. (no located evidence)
- `c-316aa52933f6ce07` [representation] (synthetic_extrapolation) — The forecastability profile is the map h → F(h; I_t) for h in {1, ..., H}, represented in the model by the paired lists horizons and values. (no located evidence)
- `c-40421a9af4fd9863` [failure_mode] (synthetic_extrapolation) — Near-deterministic periodic series will exhibit informative_horizons = [] and model_now = "NONE" even when they are perfectly predictable, due to a known power-zero failure mode of spectral surrogate tests. (no located evidence)
- `c-546d292aa7150550` [concept] (synthetic_extrapolation) — Covariant / exogenous analysis screens whether another series contains information about the target using methods including cross_ami, cross_pami, te, gcmi, pcmci, and pcmci_ami. (no located evidence)
- `c-5a820dfd062f355d` [failure_mode] (synthetic_extrapolation) — The default surrogate method (phase randomisation) preserves the amplitude spectrum of the series, making it impossible to detect forecastability above the null for near-deterministic periodic signals. (no located evidence)
- `c-63283b3f11d88ef8` [norm] (synthetic_extrapolation) — pAMI does not prove direct causality, but rather quantifies approximate direct lag-dependence after a linear conditioning step, with no causal inference standard claimed or implied. (no located evidence)
- `c-79cc51ecc7bd4a6b` [concept] (synthetic_extrapolation) — AMI is computed per horizon. (no located evidence)
- `c-8cac3f5748480efa` [concept] (synthetic_extrapolation) — AMI measures how much information the target's own past contains about its future at each lag. (no located evidence)
- `c-8e1930255e0c7a95` [failure_mode] (synthetic_extrapolation) — The kNN MI estimator (n_neighbors=8) is consistent but has finite-sample variance, and at small n (< 200) or at very long lags individual AMI values may be noise-lifted slightly above ε. (no located evidence)
- `c-9cc09a04bf70c696` [concept] (synthetic_extrapolation) — CrosspAMI asks how much covariate signal remains after accounting for target history. (no located evidence)
- `c-9d7c7435b1a6f9a8` [concept] (synthetic_extrapolation) — The Data-Processing Inequality states that applying a lossy transformation T to the information set cannot increase forecastability: F(h; T(I_t)) ≤ F(h; I_t). (no located evidence)
- `c-9e9f120bb170762f` [concept] (synthetic_extrapolation) — The informative horizon set is the subset of lags where forecastability exceeds threshold ε: H_ε = {h : F(h; I_t) ≥ ε}. (no located evidence)
- `c-a53cb05f1fc02260` [concept] (synthetic_extrapolation) — The Forecastability Profile is a structured summary of how much predictive information is available at each forecast horizon h. (no located evidence)
- `c-ba8d6c301bdfdd89` [concept] (synthetic_extrapolation) — The toolkit's triage should identify which horizons contain useful information. (no located evidence)
- `c-c7b4e4c0d147002e` [concept] (synthetic_extrapolation) — The toolkit's forecastability triage should answer whether the target series is forecastable at all before proceeding to model selection. (no located evidence)
- `c-c877a2cf002b43f8` [concept] (synthetic_extrapolation) — The directness_ratio compares corrected pAMI mass with raw AMI mass and is useful for triage but unstable when raw information mass is tiny. (no located evidence)
- `c-ca57b6f93e839173` [concept] (synthetic_extrapolation) — pAMI is a project extension rather than a paper-native metric. (no located evidence)
- `c-d094481fb68d47bb` [procedure_step] (synthetic_extrapolation) — When no lags clear the surrogate band, epsilon is set above the curve maximum so that the informative_horizons field is empty.
  > When no lags clear the surrogate band, $\varepsilon$ is set above the curve maximum so that `informative_horizons` is empty.
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md)
- `c-f15587a46e3be362` [concept] (synthetic_extrapolation) — Forecastability F(h; I_t) is greater than or equal to zero, with equality only when Y_{t+h} is independent of I_t. (no located evidence)
- `c-fbf82d831806cdb6` [expectancy] (synthetic_extrapolation) — In theory, pAMI is less than or equal to AMI. (no located evidence)
- `c-fd8a79a3a42014d9` [concept] (synthetic_extrapolation) — F1 measures horizon-wise mutual information between a series and its own future, producing the informative horizon set and structural shape flags for the triage decision.
  > The horizon-wise mutual information between $X_t$ and its own future $X_{t+h}$ (AMI) and the approximate direct-dependence residual (pAMI), producing the informative horizon set $\mathcal{H}_\varepsilon$ and structural shape flags for the triage decision.
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md)
- `c-ffd43a85a3445d0f` [concept] (synthetic_extrapolation) — Forecastability at horizon h is defined as the mutual information between the future target and the current information set: F(h; I_t) = I(Y_{t+h}; I_t) = H(Y_{t+h}) - H(Y_{t+h} | I_t). (no located evidence)

### UNKNOWN / thin / unverified / unexamined slots

- concept: thin
- decision: thin
- cue: thin
- check: thin
- failure_mode: thin
- norm: thin
- rationale: thin
- procedure_step: thin
