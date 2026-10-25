# N2a reconstruction report (complete)

601 claims span-located, 569 verified, decoy false-accept rate 0%, cost $3.9547. Verifier family: openai.
Failed calls by task: cross_verify 761, decoy 30, verify 32.

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
| documentation | open | 418 |

### Corroboration distribution (supported claims)

| corroboration | n claims |
| --- | --- |
| 1 | 418 |

## Slots by status

| status | n |
| --- | --- |
| covered | 16 |
| thin | 22 |
| unknown | 10 |

## Decoy false-accept rate by mutation type (Wilson 95% CI)

| mutation | attempted | valid | false accepts | rate | 95% CI |
| --- | --- | --- | --- | --- | --- |
| negation | 0 | 0 | 0 | 0% | [0%, 0%] |
| number | 0 | 0 | 0 | 0% | [0%, 0%] |
| scope | 0 | 0 | 0 | 0% | [0%, 0%] |

## Area: Significance testing and surrogate baselines

### Supported claims

- `c-12fab038edfe7399` [expectancy] (literature_supported) — In the validation run, the X to Y lags significant above the surrogate upper band were 1, 2, and 3.
  > Significant \(X \to Y\) lags above the surrogate upper band: 1, 2, and 3.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-15ffab22f9bd5b4b` [prerequisite] (literature_supported) — Surrogate significance testing requires a feasible sample size.
  > Surrogate significance is optional, requires feasible sample size, and needs at least 99 surrogates.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-227132d21dd427f9` [check] (literature_supported) — Significant-lag fields such as n_sig_raw_lags and n_sig_partial_lags should only be interpreted as evidence about absent significance when compute_surrogates is true.
  > Only interpret `n_sig_raw_lags`, `n_sig_partial_lags`, or other significant-lag fields as evidence about absent significance when `compute_surrogates` is `true`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-2ca2fcf31d35bc01` [failure_mode] (literature_supported) — When data are significance-infeasible (e.g., n=150 in regression tests), surrogates are skipped and decisions rely on route/class screening only.
  > when data are significance-infeasible (for example n=150 in regression tests), surrogates are skipped and decisions are route/class screening only
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-30f290472dd9a8df` [prerequisite] (literature_supported) — The forecastability profile requires surrogates for epsilon anchoring and inherits AMI estimator reliability.
  > Inherits AMI estimator reliability; requires surrogates for epsilon anchoring
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-363cf7e97af987a0` [failure_mode] (literature_supported) — Testing many drivers simultaneously without BH FDR correction lets uncorrected p-values inflate false-positive rates.
  > Without BH FDR correction when many drivers are tested simultaneously: uncorrected $p$-values will inflate false-positive rates.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3b4cb803f91a96fb` [concept] (literature_supported) — The diagnostics package contains surrogates, CMI backends, spectral helpers, and regression utilities.
  > `diagnostics/` Surrogates, CMI backends, spectral helpers, and regression utilities
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3d81f927bb52cba0` [representation] (literature_supported) — diagnostics/surrogates.py owns phase-randomized FFT surrogates and significance bands.
  > `diagnostics/surrogates.py` owns phase-randomized FFT surrogates and significance bands.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-42f45a11dd7e8ec9` [failure_mode] (literature_supported) — For highly periodic series, phase-randomized FFT surrogates can make significance tests conservative or uninformative even when the series is obviously structured.
  > For highly periodic series, they can make significance tests conservative or uninformative even when the underlying series is obviously structured.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-59d943a1178bead3` [prerequisite] (literature_supported) — Phase randomisation preserves the power spectrum, destroys temporal order, and assumes approximate second-order stationarity, so series with strong trends or regime changes give uninformative surrogate bands.
  > Phase randomisation preserves the power spectrum but destroys temporal order. It assumes approximate second-order stationarity. Series with strong trends or regime changes will produce uninformative surrogate bands.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5d3c43042ccb35ba` [concept] (literature_supported) — Phase-randomized FFT surrogates preserve the power spectrum.
  > Phase-randomized FFT surrogates preserve the power spectrum.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-63cb4854cea35e98` [concept] (literature_supported) — Random shuffle surrogates preserve the amplitude distribution of the original series but destroy any temporal correlation.
  > The permutations guarantee the same amplitude distribution as the original series, but destroy any temporal correlation that may have been in the original data.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-64c65e53f25de2e5` [decision] (literature_supported) — Linear surrogate methods are broadly useful for data showing irregular short-term fluctuations.
  > Broadly speaking, these methods are useful for data showing irregular fluctuations (short-term variabilities)
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-67f8bd218d91976a` [misconception] (literature_supported) — When a series is too short, surrogate significance may be unavailable and the bands are omitted, which must not be conflated with significance computed but none found.
  > When the series is too short, significance may be unavailable and the surrogate bands are omitted. This is distinct from "computed, none significant" - the two outcomes must not be conflated.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-68ecbe0d028ba50e` [prerequisite] (literature_supported) — Surrogate significance testing needs at least 99 surrogates.
  > Surrogate significance is optional, requires feasible sample size, and needs at least 99 surrogates.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6a1240b01b189feb` [rationale] (literature_supported) — Constrained surrogate methods usually preserve the linear structure of the original series, for example by preserving the autocorrelation function or periodogram.
  > These surrogate data methods are usually based on preserving the linear structure of the original series (for instance, by preserving the autocorrelation function, or equivalently the periodogram, an estimate of the sample spectrum).
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-73873204b2c6a000` [strategy] (literature_supported) — The lagged-exogenous flow reuses existing phase-randomised surrogate bands from significance_service wherever they exist.
  > Wherever phase-randomised surrogate bands already exist (via `significance_service`), the lagged-exogenous flow reuses them
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-758fbc344a59ea58` [norm] (literature_supported) — TE significance is evaluated against phase-randomized surrogate bands and should be interpreted with the same surrogate caveats used elsewhere in the repository.
  > Significance is evaluated against phase-randomized surrogate bands and should be interpreted with the same surrogate caveats used elsewhere in this repository.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-78dc7c665b2ffd85` [interpretation] (literature_supported) — The lower surrogate band is near zero for MI and usually not operationally informative.
  > Lower band is near zero for MI and usually not operationally informative.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7babc9b5fa448405` [interpretation] (literature_supported) — Phase-randomised surrogate significance bands extend to k = 0 so instantaneous coupling strength can be assessed against the noise floor.
  > When surrogate significance bands are available (phase-randomised surrogates), they extend to $k = 0$ so the strength of the instantaneous coupling can be assessed against the noise floor.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7c1495907632c4f6` [interpretation] (literature_supported) — When surrogate significance bands are unavailable because the series is too short, the AMI curve should be treated as indicative rather than authoritative.
  > As the sole decision-maker when surrogate significance bands are unavailable (too-short series): treat the curve as indicative, not authoritative.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7c5fb025ab82d5bb` [procedure_step] (literature_supported) — IAAFT repeats the AAFT steps until the autocorrelation is sufficiently similar to the original or the amplitudes stop changing.
  > The steps are repeated until the autocorrelation function is sufficiently similar to the original, or until there is no change in the amplitudes.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-7ea722f8ada851b6` [concept] (literature_supported) — AAFT surrogates attempt to preserve both the linear structure and the amplitude distribution.
  > it tries to preserve both the linear structure and the amplitude distribution.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-81491db11610460e` [concept] (literature_supported) — These techniques are called linear surrogate methods because they are based on a linear process and address a linear null hypothesis.
  > The above mentioned techniques are called linear surrogate methods, because they are based on a linear process and address a linear null hypothesis.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-863816a2948bfbf4` [interpretation] (literature_supported) — When compute_surrogates is false, significance was skipped or suppressed, which differs from a run where surrogates were computed and no lags were significant.
  > When `compute_surrogates` is `false`, significance was skipped or suppressed. That is different from a run where surrogates were computed and no lags were significant.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-89886af1d9f134a1` [decision] (literature_supported) — The choice of surrogate data method is directly tied to the null hypothesis being tested.
  > The particular surrogate data testing method to be used is directly related to the null hypothesis.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-8a56e4fe36fc1b54` [decision] (literature_supported) — Random shuffle surrogates correspond to the null hypothesis that the data are uncorrelated i.i.d. noise.
  > This method is associated to the null hypothesis of the data being uncorrelated i.i.d noise (possibly Gaussian and measured by a static nonlinear function).
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-8b25246a3f7cc3e7` [concept] (literature_supported) — Surrogate data testing is a statistical proof-by-contradiction technique similar to permutation tests and parametric bootstrapping, used to detect non-linearity in a time series.
  > is a statistical proof by contradiction technique similar to permutation tests and parametric bootstrapping. It is used to detect non-linearity in a time series.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-8b34c98f4e94b843` [norm] (literature_supported) — Surrogates should be used whenever sample size permits, i.e. n of at least 200 and n_surrogates of at least 99.
  > Use surrogates whenever sample size permits ($n \ge 200$, `n_surrogates >= 99`).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8c90b5242c0436c6` [decision] (literature_supported) — Upper-band crossings should be used to detect non-null dependence.
  > Use upper-band crossings to detect non-null dependence.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8f72491fd04e481d` [procedure_step] (literature_supported) — The final AAFT step is the inverse of the Gaussianization transformation.
  > Finally doing a transformation inverse of the first one (de-Gaussianization).
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-8fdf1b043d60cc33` [interpretation] (literature_supported) — The upper surrogate band is the operationally informative one for detecting non-null dependence, while the lower band is usually near zero for MI and typically not useful.
  > The upper band is operationally informative for detecting non-null dependence. The lower band is usually near zero for MI and is not typically operationally useful.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-90e03f0804f0d015` [procedure_step] (literature_supported) — Random phase (FT) surrogates preserve the periodogram by inverse Fourier transforming the original Fourier moduli with new uniformly random phases.
  > In order to preserve the linear correlation (the periodogram) of the series, surrogate data are created by the inverse Fourier Transform of the modules of Fourier Transform of the original data with new (uniformly random) phases.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-978b8caaa3faf80d` [interpretation] (literature_supported) — When compute_surrogates is false, significance was not assessed, which does not mean the series has no significant lags.
  > When `compute_surrogates` is `false`, significance was not assessed for that run. > That does not mean the series has no significant lags
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-9c0f849034e929bd` [norm] (literature_supported) — It is generally considered good practice to indicate the degree of uncertainty attached to forecasts.
  > it is generally considered a good practice to indicate the degree of uncertainty attaching to forecasts
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-a3262d51af0e821d` [interpretation] (literature_supported) — Lags whose partial autocorrelations fall outside the confidence interval indicate the AR order is likely at least that lag.
  > Lags with partial autocorrelations outside of the confidence interval indicate that the AR model's order is likely greater than or equal to the lag.
  (documentation, https://en.wikipedia.org/wiki/Partial_autocorrelation_function, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-abf9c3554eff3233` [procedure_step] (literature_supported) — A discriminating statistic is computed for both the original time series and all surrogate sets.
  > A discriminating statistic is then calculated for the original time series and all the surrogate set.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-ae45293ccc491bf9` [check] (literature_supported) — For random phase surrogates to be real-valued, the Fourier phases must be antisymmetric about the central value.
  > If the surrogates must be real, the Fourier phases must be antisymmetric with respect to the central value of data.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-c54385c54d5fc5bc` [interpretation] (literature_supported) — If the statistic for the original series differs significantly from that of the surrogates, the null hypothesis is rejected and non-linearity is assumed.
  > If the value of the statistic is significantly different for the original series than for the surrogate set, the null hypothesis is rejected and non-linearity assumed.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-c8ae73bd02ed3685` [concept] (literature_supported) — In this null hypothesis, linear means each value depends linearly on past values or on present and past values of an i.i.d. process, which is equivalent to the process being ARMA type.
  > Here linear means that each value is linearly dependent on past values or on present and past values of some independent identically distributed (i.i.d.) process, usually also Gaussian. This is equivalent to saying that the process is ARMA type.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-ca2ed537d5bb3a4f` [norm] (literature_supported) — At least 99 surrogates are required for a valid two-sided 95% band, and fewer must not be used as a significance threshold.
  > At least `n_surrogates = 99` is required for a valid two-sided 95% band. Fewer than 99 surrogates are not sufficient and must not be used as a significance threshold.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-cae8178a6ef69e58` [concept] (literature_supported) — Constrained realization surrogate methods do not depend on a particular model or parameters, making them non-parametric.
  > The last surrogate data methods do not depend on a particular model, nor on any parameters, thus they are non-parametric methods.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-cbda935885e1f4ac` [decision] (literature_supported) — When no lags clear the surrogate band, epsilon is set above the curve maximum so the informative horizons list is empty.
  > When no lags clear the surrogate band, $\varepsilon$ is set above the curve maximum so that `informative_horizons` is empty.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d628269f1bb058f3` [concept] (literature_supported) — Surrogate significance uses phase-randomized surrogates with two-sided 95% quantiles: the 2.5th percentile as lower band and the 97.5th percentile as upper band.
  > Surrogate significance uses phase-randomized surrogates and two-sided 95% quantiles: - lower: 2.5th percentile - upper: 97.5th percentile
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e258def66588c0c2` [decision] (literature_supported) — Because significance counts are zero across the canonical summary, actionable lag decisions should rely on class-level screening plus domain checks rather than significance-lag selection alone.
  > significance counts are currently zero across this canonical summary (`n_sig_ami=0`, `n_sig_pami=0` for all 8), so actionable lag decisions should rely on class-level screening plus domain checks rather than significance-lag selection alone
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ec4140636f5820ab` [procedure_step] (literature_supported) — To evaluate AR order, one finds the lag after which all partial autocorrelations lie within the confidence interval, and takes that lag as the likely order.
  > one examines the plot to find the lag after which the partial autocorrelations are all within the confidence interval. This lag is determined to likely be the AR model's order.
  (documentation, https://en.wikipedia.org/wiki/Partial_autocorrelation_function, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-f4065b8b6e0ce9b0` [failure_mode] (literature_supported) — Time series with strong periodicities are not consistent with linear null hypotheses, so other algorithms and null hypotheses have been proposed for them.
  > Time series exhibiting strong periodicities are clearly not consistent with the linear null hypotheses. To tackle this case, some algorithms and null hypotheses have been proposed.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-f488772626a9f8a7` [decision] (literature_supported) — When no surrogates are available, epsilon falls back to the default_epsilon parameter (default 0.05 nats) or an explicit caller-supplied override.
  > **When no surrogates are available** - $\varepsilon$ falls back to the `default_epsilon` parameter (default `0.05` nats), or to an explicit caller-supplied override.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f9792c1551303989` [norm] (literature_supported) — Epsilon should be defined relative to the surrogate upper band rather than as a global absolute constant, because an absolute threshold risks including noise lags or excluding informative ones as signal strength varies across series.
  > Define $\varepsilon$ relative to the surrogate upper band, not as a global > absolute constant. An absolute threshold risks including noise lags or > excluding genuinely informative ones as signal strength varies across series.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-fe5630356f625a80` [failure_mode] (literature_supported) — A drawback of AAFT is that the final de-Gaussianization step somewhat alters the linear structure.
  > The drawback of this method is precisely that the last step changes somewhat the linear structure.
  (documentation, https://en.wikipedia.org/wiki/Surrogate_data_testing, published None, independence ind-s-0b00932c0a642b74, corroboration 1)

### Synthetic / rejected claims

- `c-09dd01b737033b04` [failure_mode] (synthetic_extrapolation) — Because phase-randomisation surrogates preserve the amplitude spectrum, near-deterministic periodic signals like pure sinusoids may show empty informative horizons and model_now NONE even when perfectly predictable.
  > Such series will exhibit `informative_horizons = []` and > `model_now = "NONE"` even when they are perfectly predictable. This is a known > power-zero failure mode of spectral surrogate tests, not a defect in the profile > logic.
  (verdict insufficient [adds_content, connective_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md)
- `c-0fea2a8f92cf54a5` [concept] (synthetic_extrapolation) — When alpha is given to pacf, confidence intervals are returned with standard deviation computed as 1/sqrt(len(x)); alpha=.05 gives 95% intervals.
  > For instance if alpha=.05, 95 % confidence intervals are returned where the standard deviation is computed according to 1/sqrt(len(x)).
  (verdict pending, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html)
- `c-19328942b4b267a7` [failure_mode] (synthetic_extrapolation) — At small sample sizes (below 200) or very long lags, kNN MI estimates may be noise-lifted above epsilon, so occasional false-positive informative horizons should be expected, especially for AR(1) processes at long lags.
  > At small $n$ (< 200) or at very long lags where signal decays, > individual AMI values may be noise-lifted slightly above $\varepsilon$. Expect > occasional false-positive horizons in `informative_horizons`, especially for > AR(1) processes at long lags.
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md)
- `c-3450aedc4cf1b877` [procedure_step] (synthetic_extrapolation) — The second AAFT step is performing a random-phase transformation of the Gaussianized data.
  > Performing a RP transformation of the new data.
  (verdict insufficient [adds_content, scope_differs], https://en.wikipedia.org/wiki/Surrogate_data_testing)
- `c-486ab8979ad5cda0` [concept] (synthetic_extrapolation) — The static measurement function in the null hypothesis depends only on the present value of its argument, not past values.
  > the static measurement function is one which depends only on the present value of its argument, not on past ones.
  (verdict insufficient [adds_content, scope_differs], https://en.wikipedia.org/wiki/Surrogate_data_testing)
- `c-4ffc8c7eefe45c44` [procedure_step] (synthetic_extrapolation) — The first AAFT step is scaling the data to a Gaussian distribution.
  > Scaling the data to a Gaussian distribution (Gaussianization).
  (verdict insufficient [adds_content, scope_differs], https://en.wikipedia.org/wiki/Surrogate_data_testing)
- `c-50b2eedadce44878` [concept] (synthetic_extrapolation) — Passing alpha to ccf returns confidence intervals at the given level, e.g. alpha=.05 gives 95% intervals with standard deviation computed as 1/sqrt(len(x)).
  > If a number is given, the confidence intervals for the given level are returned. For instance if alpha=.05, 95 % confidence intervals are returned where the standard deviation is computed according to 1/sqrt(len(x)).
  (verdict pending, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.ccf.html)
- `c-53ccd79f175a86fc` [concept] (synthetic_extrapolation) — The usual null hypothesis is that the data are a realization of a stationary linear system, possibly measured through a monotonically increasing, possibly nonlinear but static function.
  > The data is a realization of a stationary linear system, whose output has been possibly measured by a monotonically increasing possibly nonlinear (but static) function.
  (verdict insufficient [adds_content, connective_differs], https://en.wikipedia.org/wiki/Surrogate_data_testing)
- `c-5a7ac76c0ea986b0` [procedure_step] (synthetic_extrapolation) — The shared signal configuration uses max_lag=20, n_surrogates=99, and random_state=42. (no located evidence)
- `c-6a998d458cd61130` [representation] (synthetic_extrapolation) — The services package contains internal builder and orchestration helpers used by analyzers and use cases, including a significance service. (no located evidence)
- `c-6cbcf4ad7ebf31b5` [concept] (synthetic_extrapolation) — The informative horizon set is the subset of lags where forecastability is at least the threshold epsilon.
  > **The informative horizon set** is the subset of lags where forecastability exceeds threshold $\varepsilon$:
  (verdict insufficient [connective_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md)
- `c-6fdaf773ebd03fa3` [concept] (synthetic_extrapolation) — In v0.5.0, Romano-Wolf FWER correction across lags is applied by default.
  > Romano-Wolf FWER correction > across lags by default
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md)
- `c-7895f8100ac932cc` [decision] (synthetic_extrapolation) — When surrogates are computed, epsilon is set to the minimum AMI value among lags whose AMI exceeds the 97.5th percentile of the surrogate distribution.
  > $\varepsilon$ is set to the minimum AMI value among lags whose AMI exceeds the 97.5th percentile of the surrogate distribution.
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md)
- `c-7aeba64b3b36ba74` [concept] (synthetic_extrapolation) — F8 screens exogenous drivers using cross-series mutual information at each horizon filtered by Benjamini-Hochberg FDR control.
  > The cross-series mutual information between a target series and one or more candidate exogenous drivers at each forecast horizon, filtered by Benjamini-Hochberg FDR control
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md)
- `c-856c929aa66d4517` [concept] (synthetic_extrapolation) — The v0.5.0 default number of surrogates is 999, while the quickstart explicitly overrides it to 99.
  > n_surrogates=99, # explicit override; v0.5.0 default is 999
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md)
- `c-ad36d8215348a001` [concept] (synthetic_extrapolation) — Surrogate significance testing is optional.
  > Surrogate significance is optional, requires feasible sample size, and needs at least 99 surrogates.
  (verdict insufficient, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt)
- `c-b148f935d94892cf` [concept] (synthetic_extrapolation) — In v0.5.0, significance correction defaults to Romano-Wolf FWER.
  > significance correction now defaults to Romano-Wolf FWER
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md)
- `c-b530257658202786` [expectancy] (synthetic_extrapolation) — Continuous-time white noise has an autocorrelation with a delta peak at lag zero and exactly zero at all other lags.
  > The autocorrelation of a continuous-time white noise signal will have a strong peak (represented by a Dirac delta function) at τ = 0 {\displaystyle \tau =0} and will be exactly 0
  (verdict insufficient [adds_content, scope_differs, connective_differs], https://en.wikipedia.org/wiki/Autocorrelation)
- `c-b6859c99117a5965` [representation] (synthetic_extrapolation) — For cross-correlation the significance field stays None and significance_source is recorded as "not_computed".
  > Significance field stays `None`; `significance_source = "not_computed"`
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md)
- `c-bc46a41b4ab54e39` [rationale] (synthetic_extrapolation) — Partial autocorrelations at lags greater than p for an AR(p) series are approximately independent and normal with mean 0, so a confidence interval can be formed by dividing a chosen z-score by the square root of n.
  > The partial autocorrelation of lags greater than p for an AR(p) time series are approximately independent and normal with a mean of 0. Therefore, a confidence interval can be constructed by dividing a selected z-score by n
  (verdict insufficient [adds_content], https://en.wikipedia.org/wiki/Partial_autocorrelation_function)
- `c-c1deb3e3c6269d26` [procedure_step] (synthetic_extrapolation) — The technique begins by specifying a null hypothesis describing a linear process and generating several surrogate data sets under it using Monte Carlo methods.
  > The technique involves specifying a null hypothesis H 0 {\displaystyle H_{0}} describing a linear process and then generating several surrogate data sets according to H 0
  (verdict insufficient [adds_content], https://en.wikipedia.org/wiki/Surrogate_data_testing)
- `c-d54776d517f758dd` [norm] (synthetic_extrapolation) — When a method lacks a surrogate path, the toolkit does not invent synthetic p-values and instead leaves significance None.
  > the significance field stays explicitly `None` and the row metadata records `significance_source = "not_computed"`. No synthetic p-values are invented.
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md)
- `c-ea66db3399a17134` [representation] (synthetic_extrapolation) — The confint field of the ccf result has shape (nlags, 2), covering lags 0 to nlags-1, and is None when alpha is None.
  > Confidence intervals for the CCF at lags 0, 1, ..., nlags-1 using the level given by alpha and the standard deviation calculated as 1/sqrt(len(x)) [1]. Shape (nlags, 2). None when alpha is None.
  (verdict pending, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.ccf.html)
- `c-ef5506fa1c5614af` [concept] (synthetic_extrapolation) — Exogenous screening with FDR applies BH-corrected significance to control false discovery rate across many tests.
  > BH-corrected significance Prunes redundant drivers; controls false discovery rate across many tests
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md)
- `c-fbe1db1217f01fb4` [concept] (synthetic_extrapolation) — Surrogate generation algorithms are usually classified into typical realizations (outputs of a model fitted to the data) and constrained realizations (transformations of the original data).
  > Typical realizations: data series are generated as outputs of a well-fitted model to the original data. Constrained realizations: data series are created directly from original data, generally by some suitable transformation of it.
  (verdict insufficient [adds_content, connective_differs], https://en.wikipedia.org/wiki/Surrogate_data_testing)

### UNKNOWN / thin / unverified / unexamined slots

- cue: unknown
- rationale: thin
- procedure_step: thin

### Unknown placeholders

- `c-5b92e7fc8e110a01` [cue] — What observable features of a situation signal that Significance testing and surrogate baselines applies or needs a different response?

## Area: Running an analysis pipeline and configuration

### Supported claims

- `c-02e70d053eaa8f6b` [concept] (literature_supported) — run_lag_aware_mod_mrmr blocks illegal measured lags, preserves declared known-future covariates with provenance, and returns selected, rejected, and blocked rows.
  > `run_lag_aware_mod_mrmr()` blocks illegal measured lags, preserves declared known-future covariates with provenance, and returns selected, rejected, and blocked rows with scorer diagnostics.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-039e1c7d6092b06d` [decision] (literature_supported) — The triage workflow blocks infeasible requests and routes exogenous requests separately.
  > The workflow blocks infeasible requests, routes exogenous requests separately
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-04fa21ff4fbf1bd9` [concept] (literature_supported) — The CSV adapter drops missing values column-wise and conservatively skips too-short or non-numeric series rather than forcing partial analysis.
  > The CSV adapter drops missing values column-wise and skips too-short or > non-numeric series conservatively instead of forcing a partial analysis.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-06048134e309e409` [strategy] (literature_supported) — Optional surfaces should be added only after the core path is clear.
  > Add Optional Surfaces Only After The Core Path Is Clear
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-06f340cedf08777b` [expectancy] (literature_supported) — With the known-future opt-in, k = 0 rows flip to tensor_role "known_future" and may be selected for the tensor for that driver only.
  > With the opt-in, those rows flip to `tensor_role="known_future"` and the selector may choose `selected_for_tensor=True` at $k=0$ for that driver only.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-083bb58cf308d008` [strategy] (literature_supported) — The golden path should be followed before using the CLI, API, dashboard, MCP, or agent layers.
  > Follow this path before you reach for the CLI, API, dashboard, MCP, or agent layers.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-08f486ab6170826d` [concept] (literature_supported) — The F5 largest Lyapunov exponent is experimental and excluded from automated triage decisions.
  > Largest Lyapunov exponent is experimental and excluded from automated triage decisions.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0a78c2e833b59dce` [procedure_step] (literature_supported) — The routing validation smoke path can be run with a script using the --smoke and --no-real-panel flags.
  > uv run python scripts/run_routing_validation_report.py --smoke --no-real-panel
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0e42d84b83113c1e` [procedure_step] (literature_supported) — The triage workflow uses a single entry point, run_triage, with staged readiness, routing, compute, and interpretation checks.
  > one-entry-point orchestration (`run_triage`) with staged readiness, routing, compute, and interpretation checks
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-100c68ae20f2e64f` [decision] (literature_supported) — A known-future opt-in exists for features whose contemporaneous value is available at prediction time, such as calendar flags, planned promotions, or regulator-set prices.
  > Known-future opt-in for features whose contemporaneous value is available at prediction time (e.g. calendar flags, planned promotions, regulator-set prices)
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-1044ad567134c4c3` [concept] (literature_supported) — The utils package contains config models, typed containers, datasets, validation, plotting, and repo workflow support.
  > `utils/` Config models, typed containers, datasets, validation, plotting, and repo workflow support
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-10966530aebcadb4` [procedure_step] (literature_supported) — Report artifacts are built with uv run python scripts/build_report_artifacts.py.
  > Report artifacts `uv run python scripts/build_report_artifacts.py`
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-12dca6b80e1a3b61` [procedure_step] (literature_supported) — The forecastability profile (F1) should be run after AMI curves exist and before choosing which horizons to model.
  > After AMI curves exist; before choosing which horizons to model
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-15acff43e4a5b180` [procedure_step] (literature_supported) — F1 should be used at the start of any triage pass because it is the anchor that other diagnostics contextualise.
  > At the start of any triage pass; F1 is the anchor all other diagnostics contextualise.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-1d4a70e39783471e` [norm] (literature_supported) — For time-series forecasting tasks, one should not jump directly to model fitting but start with forecastability triage first.
  > When the task is time-series forecasting, do not jump directly to model fitting. Start with forecastability triage first
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-1fa0a2c548476180` [concept] (literature_supported) — The lagged-exogenous surface classifies drivers by lag role and emits a sparse lag map usable for downstream tensor construction.
  > The lagged-exogenous surface classifies drivers by lag role and emits a sparse lag map that can be used for downstream tensor construction.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-219791a4285d8ed2` [representation] (literature_supported) — triage/models.py defines TriageRequest, TriageResult, readiness models, and method-plan models.
  > `triage/models.py` defines `TriageRequest`, `TriageResult`, readiness models, and method-plan models.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-299a9b89955b3907` [concept] (literature_supported) — The max_lag parameter of TriageRequest sets H, the length of the horizons and values arrays.
  > `max_lag` Sets $H$ - the length of the `horizons` and `values` arrays
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-2afffdd1188c4274` [failure_mode] (literature_supported) — Setting copy to False causes the initial data to be overwritten.
  > Whether to make a copy of the given data. If set to False, the initial data will be overwritten.
  (documentation, https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.mutual_info_regression.html, published None, independence ind-s-ca7d54da5b087ed3, corroboration 1)
- `c-2dcaee4b0601c2e1` [concept] (literature_supported) — F7 batch triage runs F1-F4 and F6 deterministically across a panel of series and produces a ranked diagnostic table.
  > Runs F1-F4 and F6 deterministically across a panel of series and produces a ranked diagnostic table
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-2e311a011150936e` [decision] (literature_supported) — Discrete but non-categorical features such as image pixel intensities should be marked as discrete for better results.
  > pixel intensities of an image are discrete features (but hardly categorical) and you will get better results if mark them as such.
  (documentation, https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.mutual_info_regression.html, published None, independence ind-s-ca7d54da5b087ed3, corroboration 1)
- `c-30f66f27c574f7ca` [procedure_step] (literature_supported) — The robustness study is run with MPLBACKEND=Agg uv run python scripts/archive/run_robustness_study.py.
  > Run `MPLBACKEND=Agg uv run python scripts/archive/run_robustness_study.py`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-353778e07d782e1c` [concept] (literature_supported) — Setting include_extended_fingerprint=True in run_triage attaches extended analysis only for non-exogenous requests; exogenous requests omit the field.
  > `run_triage(..., include_extended_fingerprint=True)` additively attaches > `extended_forecastability_analysis` for non-exogenous requests. Exogenous > requests keep that field omitted
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-398f05f0bcd6a88a` [norm] (literature_supported) — By default every k = 0 row receives tensor_role "diagnostic", and "known_future" is assigned only when the user explicitly opts in via known_future_drivers.
  > By default, every $k = 0$ row gets `tensor_role = "diagnostic"`. The `"known_future"` value is only assigned when the user explicitly opts in via `known_future_drivers={"driver_name": True}`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3b16f3a7b858b851` [strategy] (literature_supported) — For time-series forecasting tasks, forecastability triage should precede model fitting rather than jumping directly to fitting models.
  > When the task is time-series forecasting, do not jump directly to model fitting. Start with forecastability triage first
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3e060c858058b52f` [procedure_step] (literature_supported) — The notebook path starts by reading the notebooks README and then running the Air Passengers showcase walkthrough.
  > 1. Read [../notebooks/README.md](../notebooks/README.md). 2. Run [../notebooks/walkthroughs/00_air_passengers_showcase.ipynb]
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-44a10f4353ff9310` [procedure_step] (literature_supported) — When comparing results across routes, outputs should be normalized to the same keys.
  > Normalize each route to the same keys when comparing results
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-494510f15a0daf07` [concept] (literature_supported) — The random_state parameter seeds both the MI estimator and the surrogate generator for reproducibility.
  > `random_state` Seeds both the MI estimator and the surrogate generator for reproducibility
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4c573caecf8348b9` [procedure_step] (literature_supported) — Forecastability triage covers readiness, leakage risk, informative horizons, primary lags, seasonality structure, and covariate informativeness.
  > Start with forecastability triage first: readiness, leakage risk, informative horizons, primary lags, seasonality structure, and covariate informativeness.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-50a1415a735475a3` [concept] (literature_supported) — The profile is built by forecastability_profile_service.build_forecastability_profile() and exposed on the TriageResult returned by run_triage().
  > It is constructed by `forecastability_profile_service.build_forecastability_profile()` and is exposed on the `TriageResult` returned by `run_triage()`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-50eecfbfdfafa159` [procedure_step] (literature_supported) — The CausalRivers workflow screens graph-positive drivers and negative controls across lags, separates raw from history-adjusted dependence, applies legality constraints, then hands off a sparse feature set.
  > The workflow screens graph-positive drivers and negative controls across lags, separates raw pairwise dependence from signal that remains after target history is accounted for, applies forecast-legality constraints, and then hands off a sparse feature surface.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-51973c28cbed8096` [representation] (literature_supported) — adapters/api.py exposes the FastAPI application at forecastability.adapters.api:app.
  > `adapters/api.py` exposes the FastAPI application at `forecastability.adapters.api:app`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-562abcca1e9ab241` [procedure_step] (literature_supported) — Forecastability triage covers covariate informativeness.
  > Start with forecastability triage first: readiness, leakage risk, informative horizons, primary lags, seasonality structure, and covariate informativeness.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5b6eaf9d3f587b48` [concept] (literature_supported) — LLE is intentionally excluded from the F7 batch triage ranking table.
  > LLE is intentionally excluded from the batch triage ranking table (F7) by design.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5b8e0c5d3cc82ea7` [representation] (literature_supported) — use_cases/run_triage.py and use_cases/run_batch_triage.py are the authoritative orchestration entry points called by the public facade and adapters.
  > `use_cases/run_triage.py` and `use_cases/run_batch_triage.py` are the authoritative orchestration entry points called by the public facade and adapters.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5dc2a864468395b8` [concept] (literature_supported) — build_forecast_prep_contract() returns a ForecastPrepContract directly in the current public API.
  > `build_forecast_prep_contract()` returns a `ForecastPrepContract` directly in the current public API.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-60972c8750eef533` [procedure_step] (literature_supported) — After triage, fingerprint, and lagged-exog analysis, `build_forecast_prep_contract()` is called to convert triage outputs into a ForecastPrepContract for downstream model families.
  > After triage, fingerprint, and lagged-exog analysis, call `build_forecast_prep_contract()` to convert triage outputs into a `ForecastPrepContract` - a structured, machine-readable hand-off contract for downstream model families.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-60dc1ecde1e71d8f` [rationale] (literature_supported) — Early stopping and routing in triage reduces wasted modelling effort and enforces consistent screening paths.
  > Early stop/routing reduces wasted modelling effort and enforces consistent screening paths
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6128ba04cdbca987` [concept] (literature_supported) — Setting include_extended_fingerprint=True in run_triage attaches the extended analysis only for non-exogenous routes; exogenous requests leave the field omitted.
  > `run_triage(..., include_extended_fingerprint=True)` additively attaches `extended_forecastability_analysis` for non-exogenous routes only. Exogenous requests leave the field omitted
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-613c618ed744f62d` [procedure_step] (literature_supported) — Forecastability triage covers primary lags.
  > Start with forecastability triage first: readiness, leakage risk, informative horizons, primary lags, seasonality structure, and covariate informativeness.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-61f21974342c2405` [representation] (literature_supported) — The peak_horizon field is the 1-based horizon at which forecastability is maximal.
  > `peak_horizon` `int` $h^* = \arg\max_h F(h)$ (1-based index)
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-632cedcf139eff2c` [mental_model] (literature_supported) — CLI, API, scripts, MCP, and agents are optional access or narration layers around the same deterministic outputs.
  > CLI, API, scripts, MCP, and agents are optional access or narration layers around the same deterministic outputs.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-67213a7cebde7a96` [decision] (literature_supported) — known_future_drivers should be used only for variables whose contemporaneous future values are genuinely known at prediction time, such as calendar flags or planned promotions.
  > Use `known_future_drivers` only for variables whose contemporaneous future > values are genuinely known at prediction time, such as calendar flags, > planned promotions, or externally scheduled variables.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-68c6404b6422cea5` [concept] (literature_supported) — The Python package facade `forecastability` and the advanced triage namespace `forecastability.triage` are both marked stable.
  > Python package facade `forecastability` Stable Advanced triage namespace `forecastability.triage` Stable
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-69ac9c5a51ecdffc` [procedure_step] (literature_supported) — Forecastability triage covers readiness.
  > Start with forecastability triage first: readiness, leakage risk, informative horizons, primary lags, seasonality structure, and covariate informativeness.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6a906e77331ce824` [concept] (literature_supported) — Lagged-exogenous triage classifies each exogenous driver by lag role (contemporaneous vs predictive), applies sparse lag selection, and produces a typed lag map for tensor construction.
  > classify each exogenous driver by lag role (contemporaneous vs predictive), apply sparse lag selection, and produce a typed lag map ready for forecasting tensor construction.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6cde14ffcab162d1` [norm] (literature_supported) — For exogenous screening (F8), CrossAMI must be computed on the training window only.
  > The same leakage boundary applies to exogenous screening (F8): CrossAMI must be computed on the training window only.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6e58074dc2d03245` [representation] (literature_supported) — The top-level package facade re-exports run_triage, run_batch_triage, analyzers, config models, result models, dataset helpers, scorer registry, and validation as public contract.
  > Top-level package facade with re-exports for `run_triage`, `run_batch_triage`, analyzers, config models, result models, dataset helpers, scorer registry, and validation Public
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6e84cfb721c9cd17` [expectancy] (literature_supported) — Adapter runtime entry points are supported surfaces, but their transport details may evolve.
  > `adapters/` runtime entry points Supported runtime surfaces, but transport details may evolve
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6eb254c86a5d0ecc` [concept] (literature_supported) — The CLI supports the `triage`, `triage-batch`, and `list-scorers` commands.
  > The CLI supports `triage`, `triage-batch`, and `list-scorers`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6f755768b9633df1` [procedure_step] (literature_supported) — Canonical triage artifacts are produced with uv run python scripts/run_canonical_triage.py.
  > Canonical triage artifacts `uv run python scripts/run_canonical_triage.py`
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7073a2f73ced2593` [concept] (literature_supported) — The ForecastPrepContract is the final deterministic surface before external frameworks take over and never imports any downstream library.
  > The contract is the final deterministic surface before external frameworks take over. It never imports any downstream library.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-78820e0997930fee` [norm] (literature_supported) — In rolling-origin evaluation, AMI, pAMI and all F1-F8 diagnostics are computed only on the training window up to each origin.
  > AMI, pAMI, and all F1-F8 diagnostics are computed on the training window up to each rolling origin. No diagnostic touches the post-origin holdout.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-78a219a9a5e07751` [decision] (literature_supported) — There is no single right forecasting method; method selection should be based on one's objectives and conditions such as data.
  > There is no single right forecasting method to use. Selection of a method should be based on your objectives and your conditions (data etc.).
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-7e31aa907c7c1f63` [decision] (literature_supported) — Using the parcorr CI test backend for pcmci_ami gives a 50-200x speedup over the default knn_cmi backend.
  > use `pcmci_ami_ci_test="parcorr"` for a > 50-200× speedup over the default `"knn_cmi"` backend.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7f6b838b750e1bf6` [representation] (literature_supported) — The is_non_monotone field is True if forecastability increases at any horizon greater than 1.
  > `is_non_monotone` `bool` `True` if $F(h)$ increases at any $h > 1$
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8015191423797d4e` [concept] (literature_supported) — The pipeline package contains the analyzer facade, canonical workflow helpers, and rolling-origin support.
  > `pipeline/` Analyzer facade, canonical workflow helpers, and rolling-origin support
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-80d78fb11bef1804` [norm] (literature_supported) — Forecast errors and accuracy metrics are computed only on the post-origin holdout window.
  > Forecast errors and accuracy metrics are computed on the post-origin holdout window only.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-82315de73a1d9b6a` [norm] (literature_supported) — The largest Lyapunov exponent diagnostic is experimental, unreliable at finite sample sizes, gated behind a config flag, and never auto-included in the triage score.
  > Experimental - unreliable at finite sample sizes; gated behind config flag; never auto-included in triage score
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-862ac212d1e61a2c` [expectancy] (literature_supported) — The selector emits at least one row per (target, driver) pair.
  > **At least one row per `(target, driver)` pair** is emitted by the selector.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-878381a918e0bcbc` [representation] (literature_supported) — When alpha is not None, ccf always returns a CcfResult holding the same two values as the legacy tuple it replaces.
  > When alpha is not None a CcfResult is always returned; it holds the same two values as the legacy tuple it replaces.
  (documentation, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.ccf.html, published None, independence ind-s-5114732bc45e7988, corroboration 1)
- `c-8cf81bf631773b3c` [norm] (literature_supported) — linear_residual should be kept as the baseline for all backend studies.
  > Keep `linear_residual` as baseline for all backend studies.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-9007a8d1af71a0ce` [norm] (literature_supported) — By default, a driver cannot be selected for the tensor at lag 0.
  > `selected_for_tensor=True` is impossible at `lag=0` by default.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-90dc62500a2b29c7` [prerequisite] (literature_supported) — pAMI feasibility with the linear residual backend requires N to be at least the maximum of H plus min_pairs_pami plus 1 and 2H.
  > pAMI feasibility (linear residual backend): \[ N \ge \max\left(H + \texttt{min\_pairs\_pami} + 1,\ 2H\right) \]
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-926bd16a66d508cc` [concept] (literature_supported) — The dashboard is a thin browser UI over the deterministic adapters.
  > The dashboard is a thin browser UI over the deterministic adapters.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-92e67599c747d0d8` [prerequisite] (literature_supported) — Calendar features in a forecast-prep contract require a datetime index aligned to the training series.
  > Calendar features require a datetime index aligned to the training series
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-96b9a3b4b03651ae` [concept] (literature_supported) — When discrete_features is 'auto', it is set to False for dense X and True for sparse X.
  > If 'auto', it is assigned to False for dense X and to True for sparse X.
  (documentation, https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.mutual_info_regression.html, published None, independence ind-s-ca7d54da5b087ed3, corroboration 1)
- `c-9910bd9b7b154f68` [prerequisite] (literature_supported) — AMI feasibility requires series length N to be at least max lag H plus min_pairs_ami plus 1.
  > AMI feasibility: \[ N \ge H + \texttt{min\_pairs\_ami} + 1 \]
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a50059db985f4544` [representation] (literature_supported) — pipeline/analyzer.py contains ForecastabilityAnalyzer, ForecastabilityAnalyzerExog, and AnalyzeResult.
  > `pipeline/analyzer.py` contains `ForecastabilityAnalyzer`, `ForecastabilityAnalyzerExog`, and `AnalyzeResult`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a58de96982596cf4` [strategy] (literature_supported) — The robustness study pipeline should be used to compare all configured backends against linear_residual.
  > Use the robustness study pipeline to compare all configured backends against `linear_residual`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a7a8edea7eba504a` [interpretation] (literature_supported) — Batch ranking surfaces which series to investigate but not why, so it does not replace individual deep-dive analysis.
  > As a replacement for individual deep-dive analysis on flagged series: batch ranking surfaces which series to investigate, not why.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-aa6f789f9e883a49` [representation] (literature_supported) — adapters/mcp_server.py contains an MCP surface that is experimental.
  > `adapters/mcp_server.py` contains the experimental MCP surface.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-aad107708da7c302` [procedure_step] (literature_supported) — F5 must be explicitly enabled via experimental: true in the config and does not run in default triage mode.
  > F5 must be explicitly enabled via `experimental: true` in the config. It does not run in default triage mode.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-b1533e0303cf092a` [concept] (literature_supported) — ForecastabilityAnalyzer and ForecastabilityAnalyzerExog support method="te" for raw-curve analysis and TE surrogate significance bands.
  > `ForecastabilityAnalyzer` and `ForecastabilityAnalyzerExog` support `method="te"` for raw-curve analysis and TE surrogate significance bands.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-b4ea8c21daa0de61` [mental_model] (literature_supported) — CLI, API, notebooks, MCP, and agents are optional access or narration layers around the same deterministic outputs.
  > CLI, API, notebooks, MCP, and agents are optional access or narration layers around the same deterministic outputs.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-b57496e49437a7b2` [concept] (literature_supported) — Triage is a standardized entry point that outputs deterministic readiness flags, an interpretation class, and recommendations about which method path should run.
  > Is the signal ready for dependence analysis, and which method path should run? Standardized entry point for production-like checks and repeatable diagnostics Deterministic readiness flags, interpretation class, recommendations
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-b57b3d55d5661578` [procedure_step] (literature_supported) — run_rolling_origin_evaluation() enforces the leakage boundary internally, but diagnostics computed manually outside it require the user to enforce the same boundary to avoid look-ahead leakage.
  > The `run_rolling_origin_evaluation()` function enforces this boundary internally. If you compute diagnostics manually outside this function, you must enforce the same boundary. Violating it introduces look-ahead leakage and invalidates the evaluation.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-b93304b386e5b479` [procedure_step] (literature_supported) — Forecastability triage covers seasonality structure.
  > Start with forecastability triage first: readiness, leakage risk, informative horizons, primary lags, seasonality structure, and covariate informativeness.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-bf1996cb00988a8b` [strategy] (literature_supported) — The notebooks/triage notebooks should be used only after the walkthroughs because they are deep dives, not first-stop onboarding.
  > Use the `notebooks/triage/` notebooks only after the walkthroughs; they are deep dives, not first-stop onboarding.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c6052548d99301b5` [failure_mode] (literature_supported) — pcmci and pcmci_ami are computationally expensive optional causal methods whose runs can take minutes to hours.
  > `pcmci` and `pcmci_ami` are optional causal methods and are **computationally > expensive** - a single run can take several minutes to hours depending on > sample size, lag range, and CI test backend.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ccb61954a25b3779` [rationale] (literature_supported) — The project separates diagnostics so teams can choose the smallest useful workflow for a decision rather than the largest available.
  > separates several dependence diagnostics so teams can choose the smallest useful workflow for a decision, not the largest workflow available
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-cd82665a92a66080` [decision] (literature_supported) — The CSV batch adapter is suited to workflows with one target series per column.
  > Use the CSV adapter when your upstream workflow already has one target series per column
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ce090009b36c08f0` [procedure_step] (literature_supported) — The extended analysis can be run from the CLI with the 'forecastability extended' command specifying CSV, column, max lag, and period.
  > forecastability extended --csv data.csv --col value --max-lag 24 --period 12 --format brief
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-cf25ff45e2e01296` [concept] (literature_supported) — Valid covariant method tokens are cross_ami, cross_pami, te, gcmi, pcmci, and pcmci_ami.
  > Valid covariant method tokens are `cross_ami`, `cross_pami`, `te`, `gcmi`, `pcmci`, and `pcmci_ami`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-cf73d7a7c811e8db` [prerequisite] (literature_supported) — Data must be up to date for a forecast to be as accurate as possible.
  > the data must be up to date in order for the forecast to be as accurate as possible
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-d4b4dc39d27ffda6` [norm] (literature_supported) — The supported import surface of the toolkit is the package facade rather than the internal package tree.
  > The supported import surface is the package facade, not the internal tree.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d4da46ac1bdb3949` [prerequisite] (literature_supported) — TE requires min_pairs of at least 50, and with non-empty conditioning history at least 2 * min_pairs aligned rows are required.
  > TE sample-size guardrails require `min_pairs >= 50`; with non-empty conditioning history, at least `2 * min_pairs` aligned rows are required.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d5a7fb62b56918db` [decision] (literature_supported) — Escalation to nonlinear backends should happen only when they improve diagnostic consistency across datasets.
  > Escalate only when nonlinear backends improve diagnostic consistency across datasets.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d7d073c08a1e9cc5` [norm] (literature_supported) — In rolling-origin evaluation, diagnostics should be computed on train windows only.
  > In rolling-origin evaluation, compute diagnostics on train windows only.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d8f94829d332ef61` [procedure_step] (literature_supported) — Forecastability triage covers informative horizons.
  > Start with forecastability triage first: readiness, leakage risk, informative horizons, primary lags, seasonality structure, and covariate informativeness.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-dcbc55b58a6d0a71` [prerequisite] (literature_supported) — The internal packages, MCP surface, and agent layer are useful only after the deterministic workflow is already understood.
  > The internal packages, the MCP surface, and the agent layer are useful only after the deterministic workflow is already understood.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-dd3221b447613612` [prerequisite] (literature_supported) — With defaults min_pairs_ami=30, min_pairs_pami=50, and H=100, AMI requires N of at least 131 and pAMI requires N of at least 201.
  > With defaults (`min_pairs_ami=30`, `min_pairs_pami=50`, `H=100`): - AMI requires \(N \ge 131\) - pAMI requires \(N \ge 201\)
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-dec036ab971ae8d6` [procedure_step] (literature_supported) — Forecastability triage covers leakage risk.
  > Start with forecastability triage first: readiness, leakage risk, informative horizons, primary lags, seasonality structure, and covariate informativeness.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e7483196a093c4d4` [strategy] (literature_supported) — PCMCI methods are intended for confirmatory causal screening after a fast pairwise pass, and cross_ami plus gcmi should be preferred for initial screening.
  > They are designed for > *confirmatory* causal screening after a fast pairwise pass, not as a default > first step. Prefer `methods=["cross_ami", "gcmi"]` for fast initial > screening.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ebf4feb1b100178e` [representation] (literature_supported) — utils/datasets.py contains canonical generators and dataset loaders used by docs, tests, and scripts.
  > `utils/datasets.py` contains canonical generators and dataset loaders used by docs, tests, and scripts.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f381a79cd2f4babe` [decision] (literature_supported) — The batch workbench is used when one deterministic pass must serve both analyst and stakeholder workflows.
  > Use the batch workbench when you need one deterministic pass that serves both analyst and stakeholder workflows.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f45c7a87ad5e39dc` [concept] (literature_supported) — Lag-Aware ModMRMR selects sparse covariate lags that are informative, non-redundant with already selected features, and legal for the forecast horizon.
  > **Lag-Aware ModMRMR** selects sparse covariate lags that are informative, non-redundant against already selected features, and legal for the forecast horizon.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f7bca1999fd8f66c` [representation] (literature_supported) — The selector's sparse map is a typed Python output emitted independently from plot artifacts.
  > The selector emits `LaggedExogSelectionRow` objects independently from plot artifacts; the sparse map is a typed Python output first.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f86c34f3fb0c1a41` [procedure_step] (literature_supported) — The benchmark panel is run with uv run python scripts/run_benchmark_panel.py.
  > Benchmark panel `uv run python scripts/run_benchmark_panel.py`
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-fc362dadb96ec184` [concept] (literature_supported) — The n_surrogates parameter controls surrogate-band accuracy for epsilon resolution.
  > `n_surrogates` Controls surrogate-band accuracy for epsilon resolution
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-fc924c152b2c0cf0` [failure_mode] (literature_supported) — Calling compute_partial with method="te" raises a validation error because no validated partial-TE estimand is implemented in the analyzer path.
  > Requests for `compute_partial(..., method="te")` raise a validation error because no validated partial-TE estimand is implemented in the analyzer path.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-fcb3e56e2d8c35e5` [representation] (literature_supported) — ForecastPrepContract is a typed hand-off containing target lags, seasonal hints, covariate roles, caution flags, and advisory routing labels for downstream modeling.
  > **ForecastPrepContract** is the typed hand-off: target lags, seasonal hints, covariate roles, caution flags, and advisory routing labels for downstream modeling code.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-fd49f003f9b0fa87` [concept] (literature_supported) — In mutual_info_regression, parallelization over n_jobs is done on the columns of X, and -1 uses all processors.
  > The parallelization is done on the columns of X. None means 1 unless in a joblib.parallel_backend context. -1 means using all processors.
  (documentation, https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.mutual_info_regression.html, published None, independence ind-s-ca7d54da5b087ed3, corroboration 1)
- `c-ff1ec7bb1c217137` [concept] (literature_supported) — The HTTP API exposes GET /health, GET /scorers, POST /triage, and GET /triage/stream.
  > The HTTP API exposes `GET /health`, `GET /scorers`, `POST /triage`, and `GET /triage/stream`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)

### Synthetic / rejected claims

- `c-018f2317ede6dd4e` [concept] (synthetic_extrapolation) — By default the i-th split training set has size i * n_samples // (n_splits + 1) + n_samples % (n_splits + 1), with test size n_samples//(n_splits + 1).
  > The training set has size i * n_samples // (n_splits + 1) + n_samples % (n_splits + 1) in the i th split, with a test set of size n_samples//(n_splits + 1) by default
  (verdict pending, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html)
- `c-08e51e49b3781dbd` [concept] (synthetic_extrapolation) — The MCP server and agent/narration adapters are experimental and intentionally outside the main trust path.
  > These surfaces are intentionally outside the main trust path.
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md)
- `c-159dead581a6f9e0` [rationale] (synthetic_extrapolation) — The guide uses the same deterministic AR(1) signal across all entry surfaces so outputs remain directly comparable.
  > This guide uses the same AR(1) signal across CLI, notebook, Python API, HTTP API, and optional agent/MCP surfaces so outputs stay directly comparable.
  (verdict insufficient [adds_content, scope_differs, connective_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md)
- `c-15cf4a13083b33bc` [procedure_step] (synthetic_extrapolation) — The showcase fingerprint script can be run headlessly with MPLBACKEND=Agg and the --smoke flag. (no located evidence)
- `c-1e59c99401ebea6a` [concept] (synthetic_extrapolation) — The split method yields training and testing set indices for each split, and its y and groups arguments are ignored.
  > Yields: trainndarrayThe training set indices for that split. testndarray The testing set indices for that split.
  (verdict pending, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html)
- `c-220c6ebfd27a7767` [norm] (synthetic_extrapolation) — The n_splits parameter defaults to 5 and must be at least 2.
  > n_splitsint, default=5Number of splits. Must be at least 2.
  (verdict pending, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html)
- `c-22d1eec26c6213a0` [procedure_step] (synthetic_extrapolation) — A minimal triage runs run_triage with a TriageRequest specifying series, goal, max_lag, n_surrogates and random_state.
  > TriageRequest( series=series, goal="univariate", max_lag=20, n_surrogates=99, random_state=42, )
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md)
- `c-261858937516205c` [concept] (synthetic_extrapolation) — The max_train_size parameter sets a maximum size for a single training set.
  > max_train_sizeint, default=None Maximum size for a single training set.
  (verdict pending, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html)
- `c-261d2c3d91dd68d5` [procedure_step] (synthetic_extrapolation) — The fingerprint smoke showcase is run with a non-interactive matplotlib backend via uv. (no located evidence)
- `c-2a958ee7aa4e4f84` [procedure_step] (synthetic_extrapolation) — To allow a driver to be selected at k = 0, the user passes known_future_drivers with that driver name set to True when calling run_lagged_exogenous_triage.
  > known_future_drivers={"holiday_flag": True}, ) Without this opt-in, every $k=0$ row for `"holiday_flag"` will have `selected_for_tensor=False` and `tensor_role="diagnostic"`.
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md)
- `c-2f52502f7d346fba` [procedure_step] (synthetic_extrapolation) — After running the study, outputs/tables/robustness_backend_comparison.csv should be inspected. (no located evidence)
- `c-30f8d44ab6a264d5` [concept] (synthetic_extrapolation) — Exogenous screening with FDR uses greedy forward selection with a configurable approximate redundancy penalty.
  > Greedy forward selection; redundancy penalty is configurable approximation
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md)
- `c-3165522daf96b981` [decision] (synthetic_extrapolation) — The linear_residual backend is best used as the default benchmark and production-safe baseline. (no located evidence)
- `c-3840a96cd40fe4f1` [check] (synthetic_extrapolation) — After the showcase run, the verification report artifact should be inspected. (no located evidence)
- `c-3ce7b1849d03ae81` [decision] (synthetic_extrapolation) — The extra_trees_residual backend is best used for stress-testing nonlinear mediation robustness. (no located evidence)
- `c-3dd933886085a845` [norm] (synthetic_extrapolation) — F5 (Largest Lyapunov Exponent) is experimental, gated behind an experimental: true config flag, and excluded from automated triage or ranking decisions in F7.
  > It is gated behind `experimental: true` at the config > level and is **excluded from automated triage or ranking decisions** in F7.
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md)
- `c-4002b08767cba010` [representation] (synthetic_extrapolation) — When alpha is None, ccf returns a bare array unless result_object=True, in which case a CcfResult with confint set to None is returned.
  > When alpha is None a bare array is returned unless result_object=True, which additionally yields a CcfResult with confint set to None.
  (verdict pending, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.ccf.html)
- `c-427de32e643af0b8` [norm] (synthetic_extrapolation) — Checked-in artifacts under outputs should be treated as reference artifacts, not guaranteed-fresh build outputs.
  > Treat those as reference artifacts, not guaranteed-fresh build outputs.
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md)
- `c-49e347c5a8d3c1f3` [norm] (synthetic_extrapolation) — According to arXiv:2601.10006, frequency-specific horizon caps should be used: Yearly 6, Quarterly 8, Monthly 18, Weekly 13, Daily 14, Hourly 48.
  > Use frequency-specific horizon caps: Yearly 6, Quarterly 8, Monthly 18, Weekly 13, Daily 14, Hourly 48.
  (verdict insufficient [adds_content, connective_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md)
- `c-53dda437e923633f` [concept] (synthetic_extrapolation) — The dependence-forecastability toolkit does not train forecasting models; it determines what a model should be allowed to see.
  > It does not train forecasting models. It asks what a model should be allowed to see
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md)
- `c-56360bcd993e41cd` [concept] (synthetic_extrapolation) — In version 0.22 the n_splits default changed from 3 to 5.
  > Changed in version 0.22: n_splits default value changed from 3 to 5.
  (verdict pending, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html)
- `c-5b6a03e85e6b5a8f` [representation] (synthetic_extrapolation) — With 12 samples, n_splits=3, test_size=2 and gap=2, the first fold trains on indices 0-3 and tests on indices 6-7.
  > tscv = TimeSeriesSplit(n_splits=3, test_size=2, gap=2) >>> for i, (train_index, test_index) in enumerate(tscv.split(X)): ... print(f"Fold {i}:") ... print(f" Train: index={train_index}") ... print(f" Test: index={test_index}") Fold 0: Train: index=[0 1 2 3] Test: index=[6 7]
  (verdict pending, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html)
- `c-6277b80bceaf5307` [representation] (synthetic_extrapolation) — The backend comparison table includes the delta in number of significant pAMI lags versus the linear baseline. (no located evidence)
- `c-684ea789c843f3fd` [representation] (synthetic_extrapolation) — adapters/cli.py implements the forecastability command. (no located evidence)
- `c-6aa75ab2e01f0e87` [decision] (synthetic_extrapolation) — Using more neighbors in kNN MI estimation reduces estimation variance but could introduce bias.
  > Higher values reduce variance of the estimation, but could introduce a bias.
  (verdict insufficient [adds_content, scope_differs], https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.mutual_info_regression.html)
- `c-6cf2d63ec0ce4899` [decision] (synthetic_extrapolation) — The rf_residual backend is best used for nonlinear systems where linear residualization under-fits.
  > Nonlinear systems where linear residualization under-fits
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md)
- `c-710a0a05ff362445` [procedure_step] (synthetic_extrapolation) — The first step of the backend comparison is configuring backends in configs/robustness_study.yaml. (no located evidence)
- `c-743782eb102857c3` [concept] (synthetic_extrapolation) — The ForecastabilityProfile is a frozen Pydantic model populated from the AMI curve already computed by the pipeline, and no new estimation occurs during profile construction.
  > whose fields are populated once from the AMI curve already computed by the pipeline. No new estimation occurs during profile construction.
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md)
- `c-787b5fbdb9ef4c60` [concept] (synthetic_extrapolation) — The gap parameter is the number of samples excluded from the end of each training set before the test set.
  > gapint, default=0 Number of samples to exclude from the end of each train set before the test set.
  (verdict pending, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html)
- `c-7c6040b8b9afd927` [concept] (synthetic_extrapolation) — The use_cases package provides the main orchestration entry points for deterministic triage and batch triage, such as run_triage and run_batch_triage.
  > `use_cases/` Main orchestration entry points for deterministic triage and batch triage
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md)
- `c-7cc4344eac8d9cb9` [rationale] (synthetic_extrapolation) — Practitioners should interact with the profile rather than the raw numeric AMI array to avoid re-implementing threshold logic downstream.
  > A practitioner interacts with the profile instead of the raw numeric array to avoid re-implementing the threshold logic in downstream code.
  (verdict insufficient [connective_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md)
- `c-80433641e0497b1d` [procedure_step] (synthetic_extrapolation) — The example triage request uses goal univariate, max_lag 20, 99 surrogates and a fixed random_state for determinism. (no located evidence)
- `c-85a5620b65e95be0` [concept] (synthetic_extrapolation) — test_size defaults to n_samples // (n_splits + 1), which is the maximum allowed value when gap is 0.
  > Defaults to n_samples // (n_splits + 1), which is the maximum allowed value with gap=0.
  (verdict pending, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html)
- `c-8b95819b3b35dbb4` [concept] (synthetic_extrapolation) — The quickstart ladder is intended for fast dependence triage rather than forecast evaluation.
  > This ladder is for fast dependence triage.
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md)
- `c-8fe947f472d357b8` [representation] (synthetic_extrapolation) — The backend comparison table includes the delta of directness ratio versus the linear baseline. (no located evidence)
- `c-951b0bed828596af` [strategy] (synthetic_extrapolation) — The recommended workflow is to perform forecastability triage and lag/driver/readiness diagnostics before downstream model search, rather than starting with model search and tuning.
  > data → forecastability triage → lag / driver / readiness diagnostics → ForecastPrepContract → downstream model search
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md)
- `c-af2b682bf6c5a295` [decision] (synthetic_extrapolation) — Users should use the stable facades when they need deterministic triage, analyzers, typed results, config models, scorer registry access, or batch triage types.
  > Use these facades when you need deterministic triage, analyzers, typed results, config models, scorer registry access, or batch triage types.
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md)
- `c-b0871b97fce5f663` [representation] (synthetic_extrapolation) — The CLI command entrypoint is forecastability.adapters.cli:main. (no located evidence)
- `c-b2a8afa9094b8963` [representation] (synthetic_extrapolation) — The HTTP API is exposed at forecastability.adapters.api:app. (no located evidence)
- `c-b8fca46f24d59d36` [representation] (synthetic_extrapolation) — When alpha is None, pacf returns a bare array unless result_object=True, in which case a PacfResult with confint set to None is returned.
  > When alpha is None a bare array is returned unless result_object=True, which additionally yields a PacfResult with confint set to None.
  (verdict pending, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html)
- `c-b9a5ec5549af1752` [decision] (synthetic_extrapolation) — Predictive info learning curves (F3) are used for lookback/window-length selection before model training.
  > How many past lags does the series actually need? Lookback/window-length selection before model training
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md)
- `c-ba8ea45fb198c7fa` [representation] (synthetic_extrapolation) — A forecast-prep contract can be exported as JSON, as markdown, or as a lag table. (no located evidence)
- `c-be91fe674fa3378f` [decision] (synthetic_extrapolation) — The covariant informative showcase notebook is run if the covariant benchmark path is wanted.
  > 01_covariant_informative_showcase.ipynb) if you want the covariant benchmark path.
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md)
- `c-c06cca7f3ce1aa7b` [norm] (synthetic_extrapolation) — The largest Lyapunov exponent diagnostic (F5) is experimental, gated behind experimental: true in config, and not included in automated triage decisions.
  > largest Lyapunov exponent estimation - gated behind `experimental: true` in config, not included in automated triage decisions
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md)
- `c-c08c80d597589990` [procedure_step] (synthetic_extrapolation) — A first triage call should use the stable package facade and a simple generated series such as an AR(1) series.
  > Use the stable package facade and a simple generated series. from forecastability import TriageRequest, generate_ar1, run_triage
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md)
- `c-c1f5b7878f31d9e5` [representation] (synthetic_extrapolation) — When alpha is not None, pacf always returns a PacfResult holding the same two values as the legacy tuple.
  > When alpha is not None a PacfResult is always returned; it holds the same two values as the legacy tuple it replaces.
  (verdict pending, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html)
- `c-c643492b5806dc46` [representation] (synthetic_extrapolation) — The dashboard command entrypoint is forecastability.adapters.dashboard:main. (no located evidence)
- `c-c6d045163cfca4f8` [failure_mode] (synthetic_extrapolation) — The training-set size formula is only valid when test_size and max_train_size are left at their defaults.
  > Note that this formula is only valid when test_size and max_train_size are left to their default values.
  (verdict pending, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html)
- `c-c947da6a12db8a0e` [concept] (synthetic_extrapolation) — If nlags is not provided to ccf, the number of lags returned equals len(x).
  > Number of lags to return cross-correlations for. If not provided, the number of lags equals len(x).
  (verdict pending, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.ccf.html)
- `c-cbef914eff1fc905` [concept] (synthetic_extrapolation) — The n_neighbors parameter of mutual_info_regression defaults to 3.
  > n_neighborsint, default=3 Number of neighbors to use for MI estimation for continuous variables
  (verdict insufficient [adds_content, scope_differs], https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.mutual_info_regression.html)
- `c-d5753115d7014f4b` [representation] (synthetic_extrapolation) — adapters/dashboard.py implements the forecastability-dashboard command. (no located evidence)
- `c-e42d42f05c972fba` [representation] (synthetic_extrapolation) — The PacfResult confint field has shape (nlags + 1, 2) and is None when alpha is None.
  > Confidence intervals for the PACF at lags 0, 1, ..., nlags. Shape (nlags + 1, 2). None when alpha is None.
  (verdict pending, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html)
- `c-eb7e7c35e573b7bc` [concept] (synthetic_extrapolation) — get_n_splits returns the number of splitting iterations set by n_splits, and its X, y and groups arguments are ignored and exist only for API compatibility.
  > Returns the number of splitting iterations as set with the n_splits param when instantiating the cross-validator. Parameters: Xarray-like of shape (n_samples, n_features), default=NoneAlways ignored, exists for API compatibility.
  (verdict pending, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html)
- `c-f31c5c71b873523e` [concept] (synthetic_extrapolation) — The CLI, dashboard, and HTTP API are beta transport layers over the same deterministic core.
  > These surfaces are maintained and usable, but they remain transport layers over the same deterministic core.
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md)
- `c-f5361122893b1551` [procedure_step] (synthetic_extrapolation) — mutual_info_regression adds small random noise to continuous variables to remove repeated values, so passing an integer random_state is needed for reproducible results across calls.
  > Determines random number generation for adding small noise to continuous variables in order to remove repeated values. Pass an int for reproducible results across multiple function calls.
  (verdict insufficient [connective_differs], https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.mutual_info_regression.html)
- `c-f5c16b49f710cfdb` [representation] (synthetic_extrapolation) — The backend comparison table includes the delta of pAMI AUC versus the linear baseline. (no located evidence)
- `c-f90b6400c24e6c46` [decision] (synthetic_extrapolation) — The linear pAMI backend is the default and is faster and more stable, while the RF backend may capture more nonlinear residual structure but adds noise for short series.
  > The linear backend is faster and more stable; the RF backend may capture more nonlinear residual structure but introduces additional noise for short series.
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md)
- `c-f9ed3aaafb2d1e17` [failure_mode] (synthetic_extrapolation) — Treating a continuous variable as discrete or vice versa usually yields incorrect MI results.
  > treating a continuous variable as discrete and vice versa will usually give incorrect results, so be attentive about that.
  (verdict insufficient [adds_content, scope_differs], https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.mutual_info_regression.html)

### UNKNOWN / thin / unverified / unexamined slots

- cue: unknown
- check: unknown
- norm: thin
- rationale: thin
- procedure_step: thin

### Unknown placeholders

- `c-53315f6b0c788afa` [check] — How is work in Running an analysis pipeline and configuration checked for correctness or compliance?
- `c-a7ae14af043c2cca` [cue] — What observable features of a situation signal that Running an analysis pipeline and configuration applies or needs a different response?

## Area: Horizon-wise dependence measures (auto-mutual information, ACF)

### Supported claims

- `c-020d2cdaec4af775` [concept] (literature_supported) — pAMI measures how much dependence remains after removing linear mediation through intermediate lags.
  > pAMI How much dependence remains after removing linear mediation through intermediate lags?
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0405c67ee9e931b4` [concept] (literature_supported) — Mutual information of two random variables measures the mutual dependence between them.
  > the mutual information (MI) of two random variables is a measure of the mutual dependence between the two variables
  (documentation, https://en.wikipedia.org/wiki/Mutual_information, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-05fa35408bc5d4a1` [failure_mode] (literature_supported) — Positive MI bias is strongest when the number of nearest neighbours is large relative to local sample density, so short series with high-dimensional lag spaces are most affected.
  > Positive MI bias is strongest when the number of nearest neighbours $k$ is large relative to the local sample density. Short series with high-dimensional lag spaces (F3 at large $k$) are most affected.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-06e5bc780e1a0283` [expectancy] (literature_supported) — The ACF of an AR(p) process tails off, just like the PACF of an MA(q) process.
  > the autocorrelation function of an AR(p) process tails off just like the partial autocorrelation function of an MA(q) process
  (documentation, https://en.wikipedia.org/wiki/Partial_autocorrelation_function, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-0858ca61bdfdff65` [decision] (literature_supported) — The sample PACF plot is examined to help identify the order once an AR model is determined to be appropriate.
  > If an AR model is determined to be appropriate, then the sample partial autocorrelation plot is examined to help identify the order.
  (documentation, https://en.wikipedia.org/wiki/Partial_autocorrelation_function, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-0938aacab4017209` [representation] (literature_supported) — diagnostics/cmi.py owns alternative residual backends used by pAMI-style workflows.
  > `diagnostics/cmi.py` owns alternative residual backends used by pAMI-style workflows.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-09ea319b9e11835e` [failure_mode] (literature_supported) — The linear residualisation removes only linearly predictable dependence from intermediate lags, so nonlinear mediated dependence may not be fully removed from pAMI.
  > The conditioning-out step removes only the component of dependence that is linearly predictable from the intermediate lags. Nonlinear residual dependence that the linear backend cannot capture remains in the AMI but may not be fully removed from pAMI.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0b20865165cb900c` [misconception] (literature_supported) — pAMI measures extra lag information remaining after closer target history is linearly residualized, and is not exact nonlinear conditional mutual information nor causal proof.
  > **pAMI** asks how much extra lag information remains after closer target history is linearly residualized. It is a practical residual diagnostic, not exact nonlinear conditional mutual information and not causal proof.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0e1cf81aa6f2240e` [concept] (literature_supported) — If C is independent of (A,B), mutual information with Y exhibits supermodularity: the gain from adding B given A and C is at least the gain from adding B given A alone.
  > If C {\displaystyle C} is independent of ( A , B ) {\displaystyle (A,B)} , then I ⁡ ( Y ; A , B , C ) − I ⁡ ( Y ; A , B ) ≥ I ⁡ ( Y ; A , C ) − I ⁡ ( Y ; A )
  (documentation, https://en.wikipedia.org/wiki/Mutual_information, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-1146cef3a01d0b44` [representation] (literature_supported) — metrics/metrics.py is the core computation surface for AMI and pAMI.
  > `metrics/metrics.py` is the core AMI and pAMI computation surface.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-1d22deb50d3dab26` [interpretation] (literature_supported) — If AMI geometry is disabled or unavailable, the extended analysis output stays descriptive-only and does not emit routing-grade family recommendations.
  > If AMI geometry is disabled with > `--without-ami-geometry` or unavailable for the input, the output stays > descriptive-only and does not emit routing-grade family recommendations.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-1f4642b4414c33ad` [concept] (literature_supported) — Mutual information can be expressed as the entropy of one variable minus its conditional entropy given the other.
  > I ( X ; Y ) = H ( X ) − H ( X Y ) = H ( Y ) − H ( Y X )
  (documentation, https://en.wikipedia.org/wiki/Mutual_information, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-20daea234aca945a` [concept] (literature_supported) — sklearn's mutual_info_regression estimates MI using nonparametric entropy estimation from k-nearest neighbors distances.
  > The function relies on nonparametric methods based on entropy estimation from k-nearest neighbors distances as described in [2] and [3].
  (documentation, https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.mutual_info_regression.html, published None, independence ind-s-ca7d54da5b087ed3, corroboration 1)
- `c-23b71befef797d20` [norm] (literature_supported) — In statistics and time series analysis, the autocovariance is commonly normalized to a Pearson correlation coefficient, while in engineering the normalization is usually dropped.
  > It is common practice in some disciplines (e.g. statistics and time series analysis) to normalize the autocovariance function to get a time-dependent Pearson correlation coefficient. However, in other disciplines (e.g. engineering) the normalization is usually dropped
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-25477c43f685c841` [concept] (literature_supported) — pAMI is a project extension not native to the source paper, approximating conditional MI via linear or optional RF residualisation rather than exact conditional MI estimation.
  > pAMI is a **project extension** and is not paper-native. It approximates $I(X_t; X_{t+h} \mid X_{t+1}, \ldots, X_{t+h-1})$ via linear (or optional RF) residualisation, not by exact conditional MI estimation.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3187dc80e3fabb57` [concept] (literature_supported) — Forecastability is non-negative and equals zero only when the future target is independent of the information set.
  > $F(h;\,\mathcal{I}_t) \ge 0$ with equality only when $Y_{t+h}$ is independent of $\mathcal{I}_t$.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-332273cf42a8f158` [failure_mode] (literature_supported) — Multivariate forms of transfer entropy require still more samples.
  > although these forms require more samples again.
  (documentation, https://en.wikipedia.org/wiki/Transfer_entropy, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-33ccda62fa1e74fa` [concept] (literature_supported) — AMI is a nonlinear analog of the ACF, capturing total dependence at lag h including both direct and mediated lag paths.
  > Nonlinear analog of ACF (total dependence at lag \(h\)). - Includes both direct and mediated lag paths.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-361a6f8801f293a8` [norm] (literature_supported) — The AMI horizon-specific curve should never be collapsed before analysis.
  > Horizon-specific curve, never collapsed before analysis.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-37d90f2004a7ec0b` [concept] (literature_supported) — Mutual information is the expected value of the pointwise mutual information.
  > MI is the expected value of the pointwise mutual information (PMI).
  (documentation, https://en.wikipedia.org/wiki/Mutual_information, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-39d9ef8bb34d0bc3` [concept] (literature_supported) — The extra_trees_residual backend gives strong nonlinear fit with variance reduction from randomized splits but can still overfit noisy short series and is less interpretable.
  > `extra_trees_residual` Strong nonlinear fit with variance reduction from randomized splits Can still overfit noisy short series; less interpretable
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3a643f774689cd3d` [concept] (literature_supported) — The standard cross-correlation baseline retains the sign rather than collapsing to absolute values.
  > Cheap linear baseline; sign is retained (no premature absolute-value collapse)
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3fec04acd8d0297e` [concept] (literature_supported) — AMI at horizon h is defined as the mutual information between X_t and X_{t+h}.
  > AMI at horizon \(h\): \[ I_h = I(X_t; X_{t+h}) \]
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-41974983b0f71025` [failure_mode] (literature_supported) — Permutation entropy is amplitude-blind and its tie-breaking rule must be fixed.
  > PE is amplitude-blind; tie-breaking rule must be fixed
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-454332a294b05687` [concept] (literature_supported) — For vector auto-regressive processes, transfer entropy reduces to Granger causality.
  > Transfer entropy reduces to Granger causality for vector auto-regressive processes.
  (documentation, https://en.wikipedia.org/wiki/Transfer_entropy, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-464da2c578921c27` [mental_model] (literature_supported) — Intuitively, mutual information measures how much knowing one variable reduces uncertainty about the other.
  > It measures how much knowing one of these variables reduces uncertainty about the other.
  (documentation, https://en.wikipedia.org/wiki/Mutual_information, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-568b5eb3e646b7f5` [concept] (literature_supported) — Mutual information between two random variables is a non-negative value that measures their dependency.
  > Mutual information (MI) [1] between two random variables is a non-negative value, which measures the dependency between the variables.
  (documentation, https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.mutual_info_regression.html, published None, independence ind-s-ca7d54da5b087ed3, corroboration 1)
- `c-56a7d0c834809941` [concept] (literature_supported) — pAMI is a project extension based on residualization combined with nonlinear mutual information.
  > pAMI remains a project extension based on residualization + nonlinear MI.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-574ae465285aa0a7` [failure_mode] (literature_supported) — The v0.3.0 covariant methods start from lag k = 1 and silently drop any k = 0 structure.
  > The v0.3.0 covariant methods all start from $k = 1$ and silently drop any $k = 0$ structure.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-57521bbb1f6fbe23` [concept] (literature_supported) — The definition of transfer entropy has been extended to other entropy measures such as Rényi entropy.
  > The above definition of transfer entropy has been extended by other types of entropy measures such as Rényi entropy.
  (documentation, https://en.wikipedia.org/wiki/Transfer_entropy, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-59f1856ef2588949` [concept] (literature_supported) — Informative horizons show where the target contains usable lag information.
  > Informative horizons Shows where the target contains usable lag information
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5d73a97d4fa8af34` [concept] (literature_supported) — Mutual information is symmetric in its two arguments.
  > Moreover, mutual information is nonnegative (i.e. I ⁡ ( X ; Y ) ≥ 0 {\displaystyle \operatorname {I} (X;Y)\geq 0} see below) and symmetric
  (documentation, https://en.wikipedia.org/wiki/Mutual_information, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-5dfc565a9c336111` [concept] (literature_supported) — pAMI is a project extension that uses a linear-residual approximation rather than exact conditional mutual information.
  > pAMI is a project extension that uses a linear-residual approximation rather than exact conditional mutual information.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6088d52e83e85218` [concept] (literature_supported) — PCMCI+ / PCMCI-AMI covers lags 0 to max_lag with full_mci conditioning and inherits lag roles from the PCMCI link lag.
  > PCMCI+ / PCMCI-AMI (existing) `0..max_lag` inherits from PCMCI link lag inherits `full_mci`
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-61bbdba3c86defb2` [misconception] (literature_supported) — Different fields define autocorrelation differently, and not all definitions are equivalent; in some fields it is used interchangeably with autocovariance.
  > Different fields of study define autocorrelation differently, and not all of these definitions are equivalent. In some fields, the term is used interchangeably with autocovariance.
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-649be9381044ab08` [concept] (literature_supported) — In statistics, the autocorrelation of a random process is the Pearson correlation between values of the process at different times, as a function of the two times or the time lag.
  > the autocorrelation of a real or complex random process is the Pearson correlation between values of the process at different times, as a function of the two times or of the time lag
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-65065dfee36610b1` [procedure_step] (literature_supported) — Exogenous analysis uses CrossAMI and pCrossAMI curves to screen external drivers for lead-lag signal before multivariate forecasting or feature engineering.
  > Which external drivers show lead-lag signal with the target? Driver screening before multivariate forecasting or feature engineering CrossAMI and pCrossAMI curves + ranked drivers
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6950d4fba3c32785` [rationale] (literature_supported) — Normalization matters because it gives a scale-free measure of dependence strength and affects the statistical properties of estimated autocorrelations.
  > The normalization is important both because the interpretation of the autocorrelation as a correlation provides a scale-free measure of the strength of statistical dependence, and because the normalization has an effect on the statistical properties of the estimated autocorrelations.
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-6dfd7bd91fe8cf5a` [concept] (literature_supported) — Autocorrelation analysis is a tool for identifying repeating patterns or hidden periodicities in a signal obscured by noise.
  > The analysis of autocorrelation is a mathematical tool for identifying repeating patterns or hidden periodicities within a signal obscured by noise.
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-6f0c5679b65e4b07` [concept] (literature_supported) — The metrics package holds the core AMI/pAMI computation and the scorer registry.
  > `metrics/` Core AMI/pAMI computation and scorer registry
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-70065e795c88019f` [concept] (literature_supported) — In v0.5.0 the default AMI estimator is KSG-II, and passing estimator='ksg1_sklearn' reproduces v0.4.3 numerics.
  > the default AMI estimator is now KSG-II > (pass `estimator='ksg1_sklearn'` to reproduce v0.4.3 numerics)
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-70a4f8b51e8c1a8f` [concept] (literature_supported) — Transfer entropy is a finite version of directed information, which James Massey defined in 1990.
  > Transfer entropy is a finite version of the directed information which was defined in 1990 by James Massey
  (documentation, https://en.wikipedia.org/wiki/Transfer_entropy, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-76fa50e7b7110399` [concept] (literature_supported) — For a wide-sense stationary process, the autocovariance depends only on the time lag between values, not their position in time.
  > the autocovariance depends only on the time-distance between the pair of values but not on their position in time
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-7be7d8e5cbde9ed4` [concept] (literature_supported) — F3 measures mutual information between a k-step past embedding and the one-step-ahead future to identify the minimal sufficient lookback length.
  > The mutual information between a $k$-step past embedding and the one-step-ahead future, evaluated for $k = 1 \ldots K$, to identify the minimal sufficient lookback length
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7da304411739b286` [failure_mode] (literature_supported) — For non-stationary random-walk-like series, F3 estimates are inflated and grow with k without plateauing.
  > For non-stationary series: random-walk-like dynamics produce inflated estimates that grow with $k$ without plateauing.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8390f6c1d21a8a56` [failure_mode] (literature_supported) — AMI values beyond frequency-specific horizon caps (Yearly 6, Quarterly 8, Monthly 18, Weekly 13, Daily 14, Hourly 48) are unreliable.
  > frequency-specific cap (Yearly 6, Quarterly 8, Monthly 18, Weekly 13, Daily 14, Hourly 48): AMI values beyond these caps are unreliable.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-83f33805199dcc11` [failure_mode] (literature_supported) — Because pAMI uses linear residualisation, nonlinear mediation is not removed.
  > It uses linear residualisation, so nonlinear mediation is not removed.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-898d5dd8ca2df54d` [concept] (literature_supported) — Autocorrelation measures the correlation of a signal with a delayed copy of itself.
  > measures the correlation of a signal with a delayed copy of itself
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-8cac3f5748480efa` [concept] (literature_supported) — AMI measures how much information the target's own past contains about its future at each lag.
  > **AMI** asks how much information the target's own past contains about its future at each lag.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8eabb66a53df1fee` [norm] (literature_supported) — AMI and pAMI should be kept horizon-specific and not pre-aggregated before triage.
  > Keep AMI and pAMI horizon-specific; do not pre-aggregate before triage.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8ef77c2444206fb1` [procedure_step] (literature_supported) — Exogenous screening uses rolling-origin evaluation with raw CrossMI and conditioned pCrossAMI producing horizon-level outputs.
  > rolling-origin exogenous screening using raw CrossMI and conditioned pCrossAMI with horizon-level outputs
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-931f2ebfc2cfdad2` [concept] (literature_supported) — Transfer entropy is a non-parametric statistic that measures the amount of directed, time-asymmetric information transfer between two random processes.
  > Transfer entropy is a non-parametric statistic measuring the amount of directed (time-asymmetric) transfer of information between two random processes.
  (documentation, https://en.wikipedia.org/wiki/Transfer_entropy, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-96cf7e9e882d2a2b` [interpretation] (literature_supported) — CrossAMI shows where a raw relationship appears, while CrosspAMI tests whether it survives target-history adjustment.
  > CrossAMI says where the raw relationship appears. CrosspAMI asks whether the relationship survives the target-history adjustment.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-976548abd996fe96` [failure_mode] (literature_supported) — If AMI geometry is disabled or unavailable, the extended profile remains descriptive-only and does not emit routing-grade family recommendations.
  > AMI geometry stays first. If it is disabled or unavailable, the profile remains descriptive-only and does not emit routing-grade family recommendations.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-977ca77fbb8dd9fb` [failure_mode] (literature_supported) — pAMI is a linear approximation to conditional MI and can under-capture nonlinear mediation.
  > Linear approximation to conditional MI; can under-capture nonlinear mediation
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-9d4fc7876cd79537` [prerequisite] (literature_supported) — Reliable phase-space coverage for the Lyapunov estimate requires n much greater than 10^m, meaning n much greater than 1000 for the default m=3, with shorter series giving only indicative results.
  > Reliable phase-space coverage requires $n \gg 10^m$. For the default $m = 3$ this means $n \gg 1000$. Results for shorter series are indicative only.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a077a7d4af051704` [concept] (literature_supported) — The directness_ratio is computed as AUC(pAMI) divided by AUC(AMI), representing the share of total dependence that appears direct.
  > What share of total dependence appears direct? Portfolio-level triage or quick comparison between windows, sensors, or assets Scalar ratio: `AUC(pAMI) / AUC(AMI)`
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a0fd0ab141f1da13` [decision] (literature_supported) — Transfer entropy is advantageous when Granger causality's model assumption does not hold, such as when analysing non-linear signals.
  > Hence, it is advantageous when the model assumption of Granger causality doesn't hold, for example, analysis of non-linear signals.
  (documentation, https://en.wikipedia.org/wiki/Transfer_entropy, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-a2a6528881940785` [prerequisite] (literature_supported) — The recommended minimum series length for F1 is approximately three times the maximum evaluation horizon.
  > For series shorter than the recommended minimum (approximately 3× the maximum evaluation horizon).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a63ddd04d6950db1` [concept] (literature_supported) — The toolkit's AMI is paper-aligned: horizon-specific, kNN-based, and uses phase-surrogate significance bands.
  > AMI is paper-aligned (horizon-specific, kNN-based, with phase-surrogate significance bands).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a70c343080de7d50` [procedure_step] (literature_supported) — The strongest candidate lag by mutual information is always evaluated first in sparse selection.
  > The strongest candidate $k^\star = \arg\max_k \widehat{I}_k$ is always evaluated first.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-aa496957dfca9868` [concept] (literature_supported) — AMI includes mediated paths, while pAMI removes them approximately via residualization.
  > Mediated paths Included Removed (approximately with residualization)
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-abeb6c2cbd9f3060` [expectancy] (literature_supported) — The PACF of an AR(p) series cuts off after lag p, similar to how the ACF of an MA(q) series cuts off after lag q.
  > the partial autocorrelation function of an AR(p) series cuts off after lag p similar to the autocorrelation function of an MA(q) series with lag q
  (documentation, https://en.wikipedia.org/wiki/Partial_autocorrelation_function, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-b68f8b2a8bac8284` [concept] (literature_supported) — Transfer entropy is directional, so TE from X to Y generally differs from TE from Y to X.
  > Directional predictive dependence: in general \(TE(X \to Y) \neq TE(Y \to X)\).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-b8f64cec10bf6217` [norm] (literature_supported) — In signal processing, autocorrelation is often used without normalization, i.e., without subtracting the mean and dividing by the variance.
  > In signal processing, the above definition is often used without the normalization, that is, without subtracting the mean and dividing by the variance.
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-bd2afa2d663dd4ca` [concept] (literature_supported) — The rf_residual backend captures nonlinear interactions with moderate tuning burden but has higher variance and compute cost than linear.
  > `rf_residual` Captures nonlinear interactions with moderate tuning burden Higher variance and compute than linear
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c175d6dd122ebe3e` [concept] (literature_supported) — The partial autocorrelation at lag k is the autocorrelation between z_t and z_{t+k} not accounted for by lags 1 through k-1.
  > it is the autocorrelation between z t {\displaystyle z_{t}} and z t + k {\displaystyle z_{t+k}} that is not accounted for by lags 1 {\displaystyle 1} through k − 1
  (documentation, https://en.wikipedia.org/wiki/Partial_autocorrelation_function, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-c188954b1ee80ca3` [concept] (literature_supported) — By the Data-Processing Inequality, applying a lossy transformation to the information set cannot increase forecastability.
  > The Data-Processing Inequality states that applying a lossy transformation $T$ to the information set cannot increase forecastability:
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c6f8fe56a11dcec7` [prerequisite] (literature_supported) — Spectral predictability captures linear structure only, and non-stationary series need detrending.
  > Captures linear structure only; non-stationary series need detrending
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ca57b6f93e839173` [concept] (literature_supported) — pAMI is a project extension rather than a paper-native metric.
  > pAMI is a project extension, not a paper-native metric.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-cc061ed30e23b40e` [concept] (literature_supported) — DTW variants solve elastic-alignment similarity by searching for an alignment minimising path-cumulated distance between two series.
  > DTW (Dynamic Time Warping), FastDTW, and ShapeDTW solve **elastic-alignment similarity**: they search for the alignment $\pi$ that minimises a path-cumulated distance between two time series.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-cc54720dd752b67b` [concept] (literature_supported) — Mutual information is non-negative, which can be shown using Jensen's inequality.
  > Using Jensen's inequality on the definition of mutual information we can show that I ⁡ ( X ; Y ) {\displaystyle \operatorname {I} (X;Y)} is non-negative
  (documentation, https://en.wikipedia.org/wiki/Mutual_information, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-cc8cf8f97a6f0537` [failure_mode] (literature_supported) — The autocovariance expression is not well defined for all series, because the mean may not exist or the variance may be zero or infinite.
  > this expression is not well defined for all-time series or processes, because the mean may not exist, or the variance may be zero (for a constant process) or infinite
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-d6492b0e5cc60971` [procedure_step] (literature_supported) — The pAMI estimator then residualizes past and future on the conditioning matrix, using a linear backend by default with an optional random forest backend.
  > Residualize past and future on \(Z\) (linear backend by default; optional RF backend).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d72197202d602bbc` [concept] (literature_supported) — The Wiener-Khinchin theorem relates the autocorrelation function to the power spectral density via the Fourier transform.
  > The Wiener-Khinchin theorem relates the autocorrelation function R X X {\displaystyle \operatorname {R} _{XX}} to the power spectral density S X X {\displaystyle S_{XX}} via the Fourier transform
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-d94e037e78d09067` [concept] (literature_supported) — Mutual information equals zero exactly when the joint distribution equals the product of marginals, i.e., when the variables are independent.
  > is equal to zero precisely when the joint distribution coincides with the product of the marginals, i.e. when X {\displaystyle X} and Y {\displaystyle Y} are independent
  (documentation, https://en.wikipedia.org/wiki/Mutual_information, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-dcdb7eb284578389` [procedure_step] (literature_supported) — Each candidate lag is emitted as a LaggedExogSelectionRow with selected_for_tensor=True if and only if it is in the selected set.
  > Emit each candidate $k$ as a `LaggedExogSelectionRow` with `selected_for_tensor=True` if and only if $k \in \mathcal{S}$.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-de7ad4af178dcd84` [concept] (literature_supported) — Mutual information equals zero if and only if the two variables are independent, and higher values mean higher dependency.
  > It is equal to zero if and only if two random variables are independent, and higher values mean higher dependency.
  (documentation, https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.mutual_info_regression.html, published None, independence ind-s-ca7d54da5b087ed3, corroboration 1)
- `c-df6e61b76b35583d` [interpretation] (literature_supported) — Seasonality hints help separate short-memory structure from seasonal structure.
  > Seasonality hints Helps separate short-memory and seasonal structure
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e3d4ac9478612d7d` [concept] (literature_supported) — The partial autocorrelation function gives the partial correlation of a stationary time series with its own lagged values, regressed on the values at all shorter lags.
  > the partial autocorrelation function (PACF) gives the partial correlation of a stationary time series with its own lagged values, regressed the values of the time series at all shorter lags
  (documentation, https://en.wikipedia.org/wiki/Partial_autocorrelation_function, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-e4d7eea182767aba` [failure_mode] (literature_supported) — The Rosenstein algorithm and Takens embedding are sensitive to noise, non-stationarity and embedding parameters, so small parameter changes can meaningfully change the Lyapunov estimate.
  > The Rosenstein algorithm and Takens embedding are sensitive to noise, non-stationarity, and the choice of embedding parameters ($m$, $\tau$, Theiler window, evolution time $s$). Small parameter changes can produce meaningfully different $\hat{\lambda}$ values.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e4fdd48e39cdc70a` [concept] (literature_supported) — CrossAMI measures information a covariate lag has about the target while ignoring the target's own history.
  > **CrossAMI** asks how much information a covariate lag has about the target, ignoring the target's own history.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ee690e0fdbbb9484` [concept] (literature_supported) — The profile reuses AMI values from ForecastabilityAnalyzer.analyze(), which runs a kNN MI estimator with n_neighbors=8.
  > The profile reuses AMI values produced by `ForecastabilityAnalyzer.analyze()`, which runs a kNN MI estimator with `n_neighbors=8`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f1295b47e1678eab` [concept] (literature_supported) — The linear_residual backend is a fast, stable, interpretable baseline but misses nonlinear mediation.
  > `linear_residual` Fast, stable, interpretable baseline Misses nonlinear mediation
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f2b33459cda65e01` [concept] (literature_supported) — CrosspAMI measures covariate signal remaining after accounting for target history, using a linear-residual approximation.
  > **CrosspAMI** asks how much covariate signal remains after accounting for target history. It is also a linear-residual approximation.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f396013c8ac1b8f6` [failure_mode] (literature_supported) — A Pearson or Spearman screen would rank both nonlinear drivers below independent noise, illustrating a linear blind spot.
  > A Pearson or Spearman screen would rank both drivers below independent noise - the hallmark of a linear blind-spot.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f5a29c00a682bdda` [failure_mode] (literature_supported) — CrossAMI inherits the same finite-sample bias and minimum-length requirements as univariate AMI.
  > CrossAMI inherits the same finite-sample bias and minimum- length requirements as univariate AMI.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f794296af5782780` [rationale] (literature_supported) — Conditioning TE on target history controls for autocorrelation-driven carryover in the target.
  > Conditioning on target history controls for autocorrelation-driven carryover in \(Y\).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f869f1f9ac46542f` [rationale] (literature_supported) — Both nonlinear couplings are constructed so that driver-target covariance is exactly zero at the population level.
  > Both couplings are constructed so that the covariance between driver and target is exactly zero at the population level
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-fb4ba7b2e59535a6` [procedure_step] (literature_supported) — The sparse selector repeatedly adds a lag whose partialled score given already-selected lags meets the selection threshold, capped at max_selected_per_driver.
  > While there exists $k^\dagger \notin \mathcal{S}$ with partialled score $\tilde{I}_{k^\dagger}(X, Y \mid \{X_{t-k'}: k' \in \mathcal{S}\}) \ge \tau_{\text{select}}$, add $k^\dagger$ to $\mathcal{S}$, capped at `max_selected_per_driver`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-fcebb4cb89cd6d68` [concept] (literature_supported) — Transfer entropy from X to Y is the reduction in uncertainty about future values of Y obtained by knowing past values of X, given the past values of Y.
  > Transfer entropy from a process X to another process Y is the amount of uncertainty reduced in future values of Y by knowing the past values of X given past values of Y.
  (documentation, https://en.wikipedia.org/wiki/Transfer_entropy, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-fd06720d80de4a77` [procedure_step] (literature_supported) — The theoretical PACF of a stationary time series can be calculated with the Durbin-Levinson algorithm.
  > The theoretical partial autocorrelation function of a stationary time series can be calculated by using the Durbin-Levinson Algorithm
  (documentation, https://en.wikipedia.org/wiki/Partial_autocorrelation_function, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-fd495756e94ca657` [concept] (literature_supported) — The fingerprint release is intentionally univariate-first and AMI-first.
  > The fingerprint release is intentionally univariate-first and AMI-first.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-fd9b7a3fb89778b9` [concept] (literature_supported) — The shipped cross_pami curve remains target_only conditioned and covers only lags 1 to max_lag, with semantics unchanged in v0.3.2.
  > The v0.3.0 `cross_pami` curve remains `target_only` conditioned and covers $k \in \{1, \dots, K_{\max}\}$ only. Its semantics are not relabelled in v0.3.2.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-feebffccc52beec2` [failure_mode] (literature_supported) — The directness ratio can be numerically unstable when raw dependence is close to zero.
  > directness can be numerically unstable when raw dependence is close to zero
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-fff5555e067bd5d2` [concept] (literature_supported) — Unlike the PACF, the autocorrelation function does not control for other lags.
  > It contrasts with the autocorrelation function, which does not control for other lags.
  (documentation, https://en.wikipedia.org/wiki/Partial_autocorrelation_function, published None, independence ind-s-0b00932c0a642b74, corroboration 1)

### Synthetic / rejected claims

- `c-04eea8c065c885e0` [concept] (synthetic_extrapolation) — F1 measures horizon-wise mutual information between a series and its own future (AMI) and an approximate direct-dependence residual (pAMI), producing an informative horizon set and shape flags.
  > The horizon-wise mutual information between $X_t$ and its own future $X_{t+h}$ (AMI) and the approximate direct-dependence residual (pAMI), producing the informative horizon set
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md)
- `c-08b6f96cf3b3b252` [representation] (synthetic_extrapolation) — The unit of mutual information depends on the logarithm base: nats for natural log, bits (shannons) for base 2, and hartleys for base 10.
  > If the natural logarithm is used, the unit of mutual information is the nat. If the log base 2 is used, the unit of mutual information is the shannon, also known as the bit.
  (verdict insufficient [adds_content], https://en.wikipedia.org/wiki/Mutual_information)
- `c-158ee533c34ef2d0` [rationale] (synthetic_extrapolation) — v0.3.2 adds the k = 0 row to cross_ami so the multivariate diagnostic is visible alongside the predictive profile.
  > v0.3.2 adds the $k = 0$ row so that the multivariate diagnostic is visible alongside the predictive profile.
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md)
- `c-1d330d99bf4f2634` [concept] (synthetic_extrapolation) — The repository is a deterministic forecastability triage toolkit for time series, with AMI as the paper-aligned foundation and pAMI as a project extension.
  > A deterministic forecastability triage toolkit with AMI as the paper-aligned foundation and pAMI as a project extension.
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt)
- `c-2320ea99930d5c36` [concept] (synthetic_extrapolation) — The kNN mutual information estimator used (Kraskov et al., n_neighbors=8) is asymptotically consistent but has positive bias in finite samples, especially at short series lengths and large lag indices.
  > is asymptotically consistent but has positive bias for finite samples, particularly at short series lengths and large lag indices.
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md)
- `c-2b3c4675bb2fe243` [procedure_step] (synthetic_extrapolation) — The repository's pAMI estimator first builds a conditioning matrix from the intermediate lags X_{t+1} through X_{t+h-1}. (no located evidence)
- `c-2c660748abfbfa7f` [concept] (synthetic_extrapolation) — Because mutual information is non-negative, conditioning cannot increase entropy: H(X) is at least H(X|Y).
  > is non-negative, consequently, H ( X ) ≥ H ( X ∣ Y )
  (verdict insufficient [adds_content], https://en.wikipedia.org/wiki/Mutual_information)
- `c-2d1a0797ed2fe39d` [concept] (synthetic_extrapolation) — Transfer entropy, originally bivariate, has been extended to multivariate forms that condition on other sources or consider transfer from a collection of sources.
  > transfer entropy has been extended to multivariate forms, either conditioning on other potential source variables or considering transfer from a collection of sources
  (verdict insufficient [adds_content], https://en.wikipedia.org/wiki/Transfer_entropy)
- `c-38086ed0780ebb51` [concept] (synthetic_extrapolation) — The pacf 'ols' method regresses the time series on its lags and a constant.
  > "ols" : regression of time series on lags of it and on constant.
  (verdict pending, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html)
- `c-3a67a1ef54696b79` [mental_model] (synthetic_extrapolation) — Transfer entropy is a conditional mutual information, with the history of the influenced variable Y in the condition.
  > Transfer entropy is conditional mutual information, with the history of the influenced variable
  (verdict insufficient [adds_content], https://en.wikipedia.org/wiki/Transfer_entropy)
- `c-3c26bae4b9509111` [decision] (synthetic_extrapolation) — In simulations, the lowest-bias pacf estimators included Yule-Walker (MLE), Levinson-Durbin (MLE), Burg, OLS and OLS-adjusted.
  > The estimators with the lowest bias included included these three in addition to OLS and OLS-adjusted.
  (verdict pending, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html)
- `c-4452a1712336a5ae` [decision] (synthetic_extrapolation) — AMI is intended for first-pass screening of a target signal before model search, answering whether horizon-specific dependence exists worth exploiting.
  > Is there horizon-specific dependence worth exploiting at all? First-pass screening of a target signal before model search
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md)
- `c-47a853615915b7c1` [concept] (synthetic_extrapolation) — pAMI is a project extension defined as the mutual information between X_t and X_{t+h} conditioned on the intermediate lags, acting as a nonlinear analog of PACF.
  > Nonlinear analog of PACF (direct dependence after conditioning on intermediate lags).
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md)
- `c-4efe5ca3d6501ebd` [procedure_step] (synthetic_extrapolation) — Using sample autocorrelations in the Durbin-Levinson formula yields the sample PACF of any given time series.
  > The formula above can be used with sample autocorrelations to find the sample partial autocorrelation function of any given time series.
  (verdict insufficient [adds_content], https://en.wikipedia.org/wiki/Partial_autocorrelation_function)
- `c-5d561c77da2dcb84` [decision] (synthetic_extrapolation) — Based on simulations across low-order ARMA models, the best pacf methods by root MSE are Yule-Walker (MLE), Levinson-Durbin (MLE) and Burg.
  > Based on simulation evidence across a range of low-order ARMA models, the best methods based on root MSE are Yule-Walker (MLW), Levinson-Durbin (MLE) and Burg, respectively.
  (verdict pending, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html)
- `c-5f445b88d4805f07` [strategy] (synthetic_extrapolation) — The PACF was introduced in the Box-Jenkins approach, where plotting it is used to determine the appropriate lag order p in an AR(p) or ARIMA(p,d,q) model.
  > The use of this function was introduced as part of the Box-Jenkins approach to time series modelling, whereby plotting the partial autocorrelative functions one could determine the appropriate lags p in an AR (p) model
  (verdict insufficient [adds_content, scope_differs], https://en.wikipedia.org/wiki/Partial_autocorrelation_function)
- `c-5f96ef54fa2b30c4` [failure_mode] (synthetic_extrapolation) — Transfer entropy usually requires more samples for accurate estimation than Granger causality.
  > However, it usually requires more samples for accurate estimation.
  (verdict insufficient [adds_content], https://en.wikipedia.org/wiki/Transfer_entropy)
- `c-68edec8d7151d274` [procedure_step] (synthetic_extrapolation) — The sparse selector starts with an empty selected set. (no located evidence)
- `c-6c159565b557277a` [concept] (synthetic_extrapolation) — The autocorrelation matrix is positive semidefinite and all its eigenvalues are real and non-negative.
  > All eigenvalues of the autocorrelation matrix are real and non-negative.
  (verdict insufficient [adds_content], https://en.wikipedia.org/wiki/Autocorrelation)
- `c-6c78963f3ef9bc50` [concept] (synthetic_extrapolation) — Unlike the correlation coefficient, mutual information is not limited to real-valued variables and linear dependence; it measures how the joint distribution differs from the product of marginals.
  > Not limited to real-valued random variables and linear dependence like the correlation coefficient, MI is more general and determines how different the joint distribution of the pair ( X , Y )
  (verdict insufficient [adds_content], https://en.wikipedia.org/wiki/Mutual_information)
- `c-6eb40812548018fc` [concept] (synthetic_extrapolation) — The 'ols-inefficient' pacf method uses a single common sample to estimate all pacf coefficients.
  > "ols-inefficient" : regression of time series on lags using a single common sample to estimate all pacf coefficients.
  (verdict pending, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html)
- `c-70a8f30c7f74951f` [concept] (synthetic_extrapolation) — For a WSS process, the autocorrelation as a function of lag is an even function of the lag.
  > this would be an even function of the lag
  (verdict insufficient [adds_content, scope_differs], https://en.wikipedia.org/wiki/Autocorrelation)
- `c-753a7aacc87f29c1` [misconception] (synthetic_extrapolation) — pAMI should not be treated as an exact nonlinear conditional mutual information estimate.
  > Treating pAMI as an exact nonlinear conditional mutual information estimate.
  (verdict insufficient [adds_content, connective_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md)
- `c-77da654a663484a3` [concept] (synthetic_extrapolation) — The Forecastability Profile summarises how much predictive information is available at each forecast horizon from lag 1 to a user-specified maximum lag H.
  > The **Forecastability Profile** is a structured summary of how much predictive information $I(Y_{t+h};\,\mathcal{I}_t)$ is available at each forecast horizon $h$.
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md)
- `c-79cc51ecc7bd4a6b` [concept] (synthetic_extrapolation) — AMI is computed per horizon. (no located evidence)
- `c-80381f3a5e67197b` [concept] (synthetic_extrapolation) — The cross_ami lag profile is estimated with the same kNN mutual-information estimator used throughout the covariant surface.
  > estimated with the same kNN mutual-information estimator used throughout the covariant surface
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md)
- `c-87f0f4fd176a9816` [concept] (synthetic_extrapolation) — The element at index k of the ccf output is the correlation between x shifted by k ({x[k],...,x[n]}) and the leading part of y ({y[0],...,y[m-k]}).
  > the element at index k is the correlation between {x[k], x[k+1], ..., x[n]} and {y[0], y[1], ..., y[m-k]}, where n and m are the lengths of x and y, respectively.
  (verdict pending, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.ccf.html)
- `c-8c485a017ef0775e` [failure_mode] (synthetic_extrapolation) — In simulations, adjusted Yule-Walker (the default) and adjusted Levinson-Durbin performed consistently worse than the other pacf options.
  > Yule-Walker (adjusted) and Levinson-Durbin (adjusted) performed consistently worse than the other options.
  (verdict pending, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html)
- `c-8d34d8f2423a22d8` [representation] (synthetic_extrapolation) — The pacf output includes lag 0 (value 1), so the returned vector has size nlags + 1.
  > The returned value includes lag 0 (ie., 1) so size of the pacf vector is (nlags + 1,).
  (verdict pending, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html)
- `c-9409ca5fecdbeed8` [mental_model] (synthetic_extrapolation) — MI, TE, and GCMI measure dependence in the full joint distribution rather than only the linear second moment, so they detect dependence even when covariance is zero.
  > MI, TE, and GCMI measure dependence in the full joint distribution $P(X, Y)$, not only the linear second moment.
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md)
- `c-94a8da9a77cd9fa6` [concept] (synthetic_extrapolation) — The default pacf method is Yule-Walker with sample-size adjustment in the denominator for the autocovariance.
  > "yw", "ywa", "ywadjusted" or "yw_adjusted" : Yule-Walker with sample-size adjustment in denominator for acovf. Default.
  (verdict pending, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html)
- `c-a4cb28926bdbd23f` [concept] (synthetic_extrapolation) — For jointly discrete variables mutual information is computed as a double sum over the joint PMF, and for continuous variables the sum is replaced by a double integral over densities.
  > In the case of jointly continuous random variables, the double sum is replaced by a double integral
  (verdict insufficient [adds_content, scope_differs], https://en.wikipedia.org/wiki/Mutual_information)
- `c-a73dfb9424c4297e` [concept] (synthetic_extrapolation) — kNN MI estimators detect nonlinear dependence directly through local density structure.
  > kNN MI estimators detect this dependence directly through local density structure.
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md)
- `c-b35ea2417eb7e871` [failure_mode] (synthetic_extrapolation) — According to arXiv:2601.10006, short, sparse, and degenerate distributions should be treated as fragile for MI estimation.
  > Treat short, sparse, and degenerate distributions as fragile for MI estimation.
  (verdict insufficient [adds_content, connective_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md)
- `c-b3eafa647e6d9b59` [concept] (synthetic_extrapolation) — pacf offers Levinson-Durbin recursion with and without bias correction, and Burg's estimator.
  > "ld", "lda", "ldadjusted" or "ld_adjusted" : Levinson-Durbin recursion with bias correction. "ldb", "ldbiased" or "ld_biased" : Levinson-Durbin recursion without bias correction. "burg" : Burg's partial autocorrelation estimator.
  (verdict pending, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html)
- `c-b55e09295805b92c` [concept] (synthetic_extrapolation) — Contemporaneous association between X and Y corresponds to mutual information at lag k = 0 only, while predictive information from X's past corresponds to lags k ≥ 1.
  > Does the **past** of $X$ carry usable predictive information about the **future** of $Y$? $I(X_{t-k}\,;\,Y_t)$ for $k \ge 1$ $k \ge 1$
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md)
- `c-b996e3a6feb93a40` [decision] (synthetic_extrapolation) — FFT convolution should be preferred for computing the cross-correlation of long time series.
  > fftbool, optional If True, use FFT convolution. This method should be preferred for long time series.
  (verdict pending, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.ccf.html)
- `c-bf17180df75cb975` [concept] (synthetic_extrapolation) — The toolkit computes AMI with a kNN mutual information estimator using k=8 by default. (no located evidence)
- `c-c17d16dc8edcba72` [concept] (synthetic_extrapolation) — In this project, AMI remains aligned with the original paper. (no located evidence)
- `c-c195c233410bac52` [failure_mode] (synthetic_extrapolation) — kNN MI is unreliable for k greater than 5-8 at small sample sizes, so reliability warnings are mandatory for learning curves.
  > kNN MI unreliable for k > 5-8 at small n; mandatory reliability warnings
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md)
- `c-cb805435d4bd5398` [procedure_step] (synthetic_extrapolation) — The pAMI estimator finally computes mutual information on the residual pairs. (no located evidence)
- `c-d170a29c1587a3df` [decision] (synthetic_extrapolation) — pAMI should be used after AMI is non-trivial and direct versus mediated lag structure is needed.
  > After AMI is non-trivial and you need direct vs mediated lag structure
  (verdict insufficient [adds_content, connective_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md)
- `c-d5cd747cfd51a82f` [concept] (synthetic_extrapolation) — If each variable is a deterministic function of the other, the mutual information equals the entropy of either variable.
  > As a result, the mutual information is the same as the uncertainty contained in Y {\displaystyle Y} (or X {\displaystyle X} ) alone, namely the entropy of Y
  (verdict insufficient [adds_content, scope_differs], https://en.wikipedia.org/wiki/Mutual_information)
- `c-df4261f27343a4ee` [failure_mode] (synthetic_extrapolation) — Standard cross-correlation cannot detect symmetric nonlinear couplings, so a quadratic driver with near-zero Pearson correlation may still be a strong predictive feature.
  > **Cannot detect symmetric nonlinear couplings** - a quadratic driver with near-zero Pearson correlation can be a strong predictive feature
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md)
- `c-e05b0ef26a9332c1` [concept] (synthetic_extrapolation) — Forecastability at horizon h is defined as the mutual information between the future target and the current information set, equal to the entropy of the future target minus its conditional entropy given the information set.
  > **Forecastability at horizon $h$** is defined as the mutual information between the future target and the current information set (Catt, 2026):
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md)
- `c-e19cadc099e62745` [rationale] (synthetic_extrapolation) — Spearman correlation is near zero for the quadratic and absolute-value couplings because those functions are non-monotone in X.
  > Spearman is also near zero because $X^2$ is U-shaped (non-monotone) in $X$.
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md)
- `c-e32afe16d36f05c6` [check] (synthetic_extrapolation) — The minimum recommended series length is approximately three times the maximum evaluation horizon; below this, MI estimates for lags near the maximum horizon are unreliable.
  > Approximately $n \geq 3 \times H_{\max}$, where $H_{\max}$ is the maximum evaluation horizon. Below this threshold, MI estimates are unreliable for lags close to $H_{\max}$.
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md)
- `c-e5e64a5e4033d854` [concept] (synthetic_extrapolation) — For stationary processes, the coefficients of the best linear predictors of z_{t+k} and z_t from the intermediate values are the same but reversed.
  > For stationary processes, the coefficients in z ^ t + k {\displaystyle {\hat {z}}_{t+k}} and z ^ t {\displaystyle {\hat {z}}_{t}} are the same, but reversed
  (verdict insufficient [adds_content], https://en.wikipedia.org/wiki/Partial_autocorrelation_function)
- `c-e696598a0971ea6f` [concept] (synthetic_extrapolation) — Mutual information was defined by Claude Shannon, though the term was coined later by Robert Fano; it is also known as information gain.
  > although he did not call it "mutual information". This term was coined later by Robert Fano. Mutual Information is also known as information gain.
  (verdict insufficient [adds_content], https://en.wikipedia.org/wiki/Mutual_information)
- `c-f422fd3114692b39` [expectancy] (synthetic_extrapolation) — A monotonically decreasing forecastability profile holds for simple AR processes but is not a universal requirement; seasonal and quasi-periodic processes routinely show higher AMI at seasonal lags than short lags.
  > However, it is **not** a universal requirement. Seasonal and quasi-periodic processes routinely exhibit higher AMI at seasonal lags than at short lags.
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md)
- `c-f462c0a2e9154ea2` [concept] (synthetic_extrapolation) — When adjusted is True in statsmodels ccf, the cross-covariance denominators are the number of overlapping observations at each lag k, min(m, n-k); otherwise n is used.
  > If True, then denominators for cross-covariance are the number of overlapping observations at each lag k, min(m, n-k), otherwise n.
  (verdict pending, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.ccf.html)
- `c-f53090a18f03c118` [failure_mode] (synthetic_extrapolation) — kNN estimators degrade in high-dimensional spaces, and the toolkit enforces a hard cap of k_max = 8 on embedding dimension.
  > kNN estimators degrade in high-dimensional spaces; a hard cap $k_{\max} = 8$ is enforced.
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md)
- `c-f7004dc8e71a4fe1` [concept] (synthetic_extrapolation) — statsmodels provides related functions pccf, acf, pacf, and plot_ccf for partial cross-correlation, autocorrelation, partial autocorrelation, and plotting cross-correlations with confidence intervals.
  > statsmodels.tsa.stattools.pccf Partial cross-correlation function. statsmodels.tsa.stattools.acf Autocorrelation function. statsmodels.tsa.stattools.pacf Partial autocorrelation function. statsmodels.graphics.tsaplots.plot_ccf Plot cross-correlations and confidence intervals.
  (verdict pending, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.ccf.html)
- `c-f8200023f22bacf4` [concept] (synthetic_extrapolation) — For a WSS process, the magnitude of the autocorrelation at any lag is at most its value at lag zero.
  > Maximum at zero For a WSS process: R X X ⁡ ( τ ) ≤ R X X ⁡ ( 0 )
  (verdict insufficient [adds_content], https://en.wikipedia.org/wiki/Autocorrelation)
- `c-f8bf6bb437f5e2cd` [concept] (synthetic_extrapolation) — AMI is paper-native while pAMI is a project extension. (no located evidence)
- `c-f8d3450869eebc14` [expectancy] (synthetic_extrapolation) — In an analyst run on a synthetic lag-2 driver pair (n=1200, seed=17), TE from X to Y peaked at lag 2 with a strong directional gap versus TE from Y to X.
  > Synthetic lag-2 driver pair, \(n=1200\), `seed=17`. - \(TE(X \to Y)\) peaked at lag 2 with a strong directional gap vs \(TE(Y \to X)\).
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md)
- `c-fdee3217c5c2d8e5` [concept] (synthetic_extrapolation) — In statsmodels pacf, if nlags is not provided, the default number of lags is min(10 * log10(nobs), nobs // 2 - 1).
  > Number of lags to return autocorrelation for. If not provided, uses min(10 * np.log10(nobs), nobs // 2 - 1).
  (verdict pending, https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html)

### UNKNOWN / thin / unverified / unexamined slots

- decision: thin
- cue: unknown
- check: unknown

### Unknown placeholders

- `c-10263f7f4daab0fe` [cue] — What observable features of a situation signal that Horizon-wise dependence measures (auto-mutual information, ACF) applies or needs a different response?
- `c-69455b95b51ab3dd` [check] — How is work in Horizon-wise dependence measures (auto-mutual information, ACF) checked for correctness or compliance?

## Area: Interpreting forecastability scores against model performance

### Supported claims

- `c-00bb41a51389695f` [interpretation] (literature_supported) — If a derived feature such as a box-aggregated or coarsely discretised series yields strictly lower profile values than the raw series, the transformation has destroyed predictive information.
  > If a derived feature - for example, a box-aggregated or coarsely discretised version of the raw series - yields strictly lower profile values than the unaggregated series, the transformation has destroyed predictive information.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-01104818fadaca0b` [misconception] (literature_supported) — A positive Lyapunov estimate is consistent with chaos but can also arise from coloured noise or non-stationarity, so F5 alone cannot distinguish chaos from noise.
  > A positive $\hat{\lambda}$ is consistent with chaotic dynamics, but stochastic coloured noise and non-stationary processes also produce positive estimates. F5 alone cannot distinguish the two cases.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-03547fed47acad88` [concept] (literature_supported) — The reporting package handles deterministic interpretation and Markdown/report builders.
  > `reporting/` Deterministic interpretation and Markdown/report builders
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-04bb985feaddbfac` [interpretation] (literature_supported) — A well-defined autocorrelation coefficient lies in [-1, 1], with 1 indicating perfect correlation and -1 perfect anti-correlation.
  > its value must lie in the range [ − 1 , 1 ] {\displaystyle [-1,1]} , with 1 indicating perfect correlation and −1 indicating perfect anti-correlation
  (documentation, https://en.wikipedia.org/wiki/Autocorrelation, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-050433754eb95ea5` [representation] (literature_supported) — The model_now field gives an immediate model-complexity recommendation of HIGH, MEDIUM, LOW, or NONE.
  > `model_now` `str` Immediate model-complexity recommendation (HIGH / MEDIUM / LOW / NONE)
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-05348ecbfe93d58e` [concept] (literature_supported) — The extended analysis surface only suggests starting model families and does not fit models or wire downstream frameworks.
  > The surface suggests starting model families only; it does not fit models or wire downstream frameworks.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0e6deb75f20b2888` [interpretation] (literature_supported) — The directness_ratio is used to identify mediated versus direct structure.
  > identify mediated vs direct structure via `directness_ratio`
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-115717fdc0f1a7f4` [concept] (literature_supported) — The toolkit is a deterministic pre-modeling layer rather than a forecasting library.
  > It is **not another forecasting library**. It is a deterministic pre-modeling layer
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-11766b5fbb6a4f3a` [expectancy] (literature_supported) — The seasonal naïve method is particularly useful for data with a very high level of seasonality.
  > The seasonal naïve method is particularly useful for data that has a very high level of seasonality.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-13f6066addff28ab` [misconception] (literature_supported) — TE values are estimator- and null-model-aware diagnostics and do not constitute causal proof.
  > TE values are estimator- and null-model-aware diagnostics, not causal proof.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-146980ee0b2317e0` [expert_novice_contrast] (literature_supported) — Research has shown little difference in accuracy between conflict forecasts by knowledgeable experts and by much less knowledgeable individuals.
  > research has shown that there is little difference between the accuracy of the forecasts of experts knowledgeable in the conflict situation and those by individuals who knew much less
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-167528eeb0ed6aff` [concept] (literature_supported) — The compression ratio (observed AMI divided by limit) is a metric comparable across series.
  > the compression ratio (observed AMI / limit) is a cross-series comparable metric.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-178838d1f9220e1f` [norm] (literature_supported) — Cross-backend agreement should be required before acting on lag recommendations.
  > require cross-backend agreement before acting on lag recommendations
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-1876dc5db2ca45bf` [failure_mode] (literature_supported) — A directness_ratio greater than 1.0 signals numerical inflation, typically caused by estimator instability or finite-sample effects.
  > Numerical inflation `directness_ratio > 1.0` estimator instability, finite-sample effects
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-214d4b8a0aee9fbf` [failure_mode] (literature_supported) — In river forecasting, seasonal flow, shared weather, regime shifts and catchment structure can make a driver look predictive before it is safe or incremental.
  > Seasonal flow, shared weather systems, regime shifts, and catchment structure can all make a driver look predictive before it is actually safe or incremental.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-21f84b6c4f84e386` [interpretation] (literature_supported) — Route/class triage outputs are diagnostics and not direct proof of forecast error improvement.
  > Route/class outputs are triage diagnostics, not direct proof of forecast error improvement
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-255ac9e6dd986fa5` [representation] (literature_supported) — The avoid_horizons field lists non-informative horizons that should be excluded from model feature sets.
  > `avoid_horizons` `list[int]` Non-informative horizons - exclude from model feature sets
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-2780a9a491e73952` [interpretation] (literature_supported) — The forecastability class provides a deterministic high/medium/low style interpretation.
  > Forecastability class Gives a deterministic high / medium / low style interpretation
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-2c4e9fccf3c2cbfc` [misconception] (literature_supported) — Learning curve plateaus should not be used as proof of information exhaustion because estimator saturation can mimic genuine plateaus.
  > Using learning curve plateaus (F3) as proof of information exhaustion - estimator saturation can mimic genuine plateaus.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-2e03854f3dd5d017` [expectancy] (literature_supported) — The naïve method works quite well for economic and financial time series, which often have patterns that are difficult to predict reliably.
  > This method works quite well for economic and financial time series, which often have patterns that are difficult to reliably and accurately predict.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-2f1435153035f8c0` [misconception] (literature_supported) — A directness_ratio above 1.0 should be treated as an estimation warning, not as scientific evidence of stronger conditioned dependence.
  > at least one `directness_ratio > 1.0`, which should be treated as an estimation warning, not scientific evidence of stronger conditioned dependence
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-2fe74387530afa2c` [interpretation] (literature_supported) — Comparing residual backends is diagnostic and does not prove that any one backend is universally superior.
  > Backend comparison is diagnostic, not proof that one backend is universally superior.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3100674d3164f212` [expectancy] (literature_supported) — According to arXiv:2601.10006, AMI-error discrimination is expected to be weaker for Daily frequency than for Hourly, Weekly, Quarterly, or Yearly.
  > Expect weaker AMI-error discrimination in Daily frequency than in Hourly/Weekly/Quarterly/Yearly.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3367e06a61dc525f` [concept] (literature_supported) — In the naïve approach, forecasts are set equal to the last observed value.
  > Using the naïve approach, forecasts are produced that are equal to the last observed value.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-338a45caf4da9829` [failure_mode] (literature_supported) — For series shorter than 128 points, Welch PSD estimates rely on very few segments and Ω is unreliable beyond a coarse indicator.
  > For short series ($n < 128$): Welch PSD estimates are based on very few segments and Ω values are unreliable as anything other than a coarse indicator.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-34a436d13f16c7ff` [interpretation] (literature_supported) — A directness ratio above 1 is a numerical/assumption warning, often associated with ARCH-type behavior, rather than a physical contradiction.
  > \(r > 1\): numerical/assumption warning (often ARCH-type behavior), not a physical contradiction.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-38c1431322c64c1a` [misconception] (literature_supported) — The triage workflow supports prioritisation and method selection but does not guarantee downstream forecast accuracy gains.
  > This workflow supports prioritisation and method selection, not guaranteed downstream forecast accuracy gains.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-38de7f4f3192d75c` [check] (literature_supported) — Routines that assume monotone decay, such as naive exponential smoothers, should inspect the is_non_monotone flag before applying simplifying assumptions.
  > Routines that assume monotone decay (such as naive exponential smoothers) should inspect this flag before applying simplifying assumptions.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3d58f97e246eb170` [interpretation] (literature_supported) — If AMI greatly exceeds Ω, nonlinear methods are needed.
  > If AMI ≫ Ω → nonlinear methods needed
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3d97014e7ff9ea38` [expectancy] (literature_supported) — When the relevant factors are well understood and plenty of data is available, the final value is likely to be close to the forecast.
  > If the factors that relate to what is being forecast are known and well understood and there is a significant amount of data that can be used, it is likely the final value will be close to the forecast.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-3f3932d1bbd5d87d` [failure_mode] (literature_supported) — The directness_ratio compares corrected pAMI mass to raw AMI mass and is unstable when raw information mass is tiny.
  > **`directness_ratio`** compares corrected pAMI mass with raw AMI mass. It is useful for triage, but unstable when raw information mass is tiny.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-419dd703a4ad9df7` [expectancy] (literature_supported) — Studies have shown that extrapolations are the least accurate forecasts while company earnings forecasts are the most reliable.
  > Studies have shown that extrapolations are the least accurate, while company earnings forecasts are the most reliable.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-41d04ddb6c86efe9` [norm] (literature_supported) — The workflow is intentionally conservative and does not recommend a winning model; it provides evidence and legal inputs for where model search can begin.
  > The workflow is intentionally conservative. It does not say, "fit this winner." It says, "here is the evidence; here are the legal inputs; here is where model search can begin
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-442dc0986a937dd9` [cue] (literature_supported) — High AMI combined with low Ω signals that predictability comes from nonlinear dynamics rather than spectral structure.
  > When a divergence between high AMI and low Ω arises: this pattern signals that predictability comes from nonlinear dynamics, not spectral structure.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-49cbd37b19df2392` [check] (literature_supported) — When numeric correctness matters, users should trace results back to TriageResult and the stable package facade.
  > When numeric correctness matters, trace back to `TriageResult` and the stable package facade.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4ac40040cc033f94` [failure_mode] (literature_supported) — Large backend deltas on small sample fractions indicate short-sample fragility caused by insufficient support for residualization.
  > Short-sample fragility large backend deltas on small fractions insufficient support for residualization
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4b5419e038cc40a5` [misconception] (literature_supported) — A True is_non_monotone value should not be treated as an estimation artefact or error, since it is correct and expected for seasonal series.
  > Do not treat a `True` value as an estimation artefact or an error - it is correct and expected for seasonal series.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4df5b4d522d70d74` [check] (literature_supported) — Regression tests preserve stable screening behaviour where AR(1) classifies as high and white noise as low.
  > preserves stable screening behavior (`AR(1) -> high`, `white_noise -> low`) in regression tests
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4ef1fb406b82e453` [failure_mode] (literature_supported) — Starting forecasting projects with model search, tuning, and more features can lead to wasted compute and still poor results.
  > data → model search → tuning → more features → more compute → still poor results
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-520e7bdf665e0394` [interpretation] (literature_supported) — If spectral predictability Ω and AMI are both high, linear models may be enough.
  > if Ω high and AMI high → linear models may be enough
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-53d2494921e472c0` [interpretation] (literature_supported) — Positive TE indicates that source history adds predictive information beyond target-only history.
  > Positive TE indicates added predictive information from source history beyond target-only history.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-541ee1f6ab92a6aa` [interpretation] (literature_supported) — AMI detects dependence, not causality or guaranteed model gains.
  > Detects dependence, not causality or guaranteed model gains
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5ca9e05b6f8856f8` [rationale] (literature_supported) — TimeSeriesSplit provides train/test indices for time-ordered data because other cross-validation methods would train on future data and evaluate on past data.
  > Provides train/test indices to split time-ordered data, where other cross-validation methods are inappropriate, as they would lead to training on future data and evaluating on past data.
  (documentation, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, published None, independence ind-s-ca7d54da5b087ed3, corroboration 1)
- `c-60a2bbb9a4c6eddc` [concept] (literature_supported) — The spectral predictability score Ω is normalised to [0,1], equals 1 for a perfectly periodic signal and approaches 0 for white noise.
  > normalised to $[0, 1]$: Ω = 1 for a perfectly periodic signal, Ω → 0 for white noise
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-63f6175541e87645` [misconception] (literature_supported) — Positive Lyapunov exponent values are consistent with chaos, but stochastic noise can also produce positive values.
  > positive values are *consistent with* chaotic dynamics, but stochastic noise can also produce positive values.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-64d80b051aed3799` [prerequisite] (literature_supported) — Quantitative forecasting models are appropriate when past numerical data is available and it is reasonable to assume some data patterns will continue.
  > They are appropriate to use when past numerical data is available and when it is reasonable to assume that some of the patterns in the data are expected to continue into the future.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-663e0dd4c29290e2` [expectancy] (literature_supported) — In theory pAMI is less than or equal to AMI, but in finite samples with residual approximation pAMI can occasionally exceed AMI.
  > In theory, \(\tilde{I}_h \le I_h\). - In finite samples with residual approximation, occasional \(\tilde{I}_h > I_h\) can occur.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-67372dcb86414a6a` [procedure_step] (literature_supported) — Downstream model families or framework-specific settings should only be recommended after triage.
  > Only then recommend downstream model families or framework-specific settings.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6e752ea957b7798d` [norm] (literature_supported) — In rolling-origin evaluation, forecast errors are computed on the post-origin test window only.
  > Forecast errors are computed on post-origin test window only.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-70e62d1d3a155c97` [interpretation] (literature_supported) — A high forecastability class maps to a recommendation of complex structured models such as deep AR, nonlinear, or LSTM.
  > "recommendation": "HIGH -> Complex structured models (deep AR, nonlinear, LSTM)"
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-725ecdd8f24d140c` [interpretation] (literature_supported) — directness_ratio should be treated as informative only below 1.0; values above 1.0 indicate the residual approximation broke down at that horizon.
  > treat the ratio as informative only below 1.0; values above 1.0 indicate the residual approximation has broken down at that horizon.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7491c56b71dd1b66` [norm] (literature_supported) — Naïve forecasts provide a benchmark against which more sophisticated forecasting models can be compared.
  > Naïve forecasts are the most cost-effective forecasting model, and provide a benchmark against which more sophisticated models can be compared.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-76995d363dd487e4` [norm] (literature_supported) — In rolling-origin evaluation, diagnostics are computed on train windows only and scoring is done on post-origin holdout only.
  > In rolling-origin evaluation, diagnostics are computed on train windows only and scoring on post-origin holdout only.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-79ab5857df87819a` [interpretation] (literature_supported) — High AMI with low complexity typically indicates regular, easily modelled dynamics, while high AMI with high complexity suggests potentially nonlinear or chaotic behaviour.
  > high AMI with low complexity typically indicates regular, easily modelled dynamics; high AMI with high complexity suggests potentially nonlinear or chaotic behaviour.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7b1945260e03d29b` [misconception] (literature_supported) — pAMI quantifies approximate direct dependence after removing mediated paths but does not prove direct or Granger causality.
  > pAMI quantifies approximate direct dependence after removing mediated paths. It does not prove direct causality or Granger causality.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7bce906871359b47` [representation] (literature_supported) — A tensor_role of "diagnostic" means the lag is useful for understanding the system but is not eligible as a forecasting tensor feature.
  > `"diagnostic"` Useful for understanding the system; **not** eligible as a tensor feature
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7e9cd9194a9a6eeb` [check] (literature_supported) — Routing validation audits deterministic routing against controlled archetypes and sanity panels and does not train or benchmark forecasting models.
  > Routing validation audits deterministic routing against controlled archetypes and sanity panels. It does **not** train or benchmark forecasting models.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-855e429c6dbb7425` [representation] (literature_supported) — The primary_lags field lists informative lags identified by the deterministic workflow.
  > `primary_lags` Informative lags identified by the deterministic workflow
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8678002090ef64bf` [expectancy] (literature_supported) — Previous research shows that different forecasting methods may lead to different levels of forecasting accuracy.
  > Previous research shows that different methods may lead to different level of forecasting accuracy.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-8a5771bc0d94040b` [cue] (literature_supported) — The repository flags a directness_ratio greater than 1.0 as arch_suspected.
  > This repository flags `directness_ratio > 1.0` as `arch_suspected`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-924218078f7a6477` [prerequisite] (literature_supported) — For comparable metrics across TimeSeriesSplit folds, samples must be equally spaced.
  > To ensure comparable metrics across folds, samples must be equally spaced.
  (documentation, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, published None, independence ind-s-ca7d54da5b087ed3, corroboration 1)
- `c-9430ce2793875335` [check] (literature_supported) — The readiness report detects cases where triage should be blocked or interpreted cautiously.
  > Readiness report Detects cases where triage should be blocked or interpreted cautiously
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-9a8161ef29616bdf` [misconception] (literature_supported) — A blocked result is not the same as no forecastable structure; it means the workflow could not support the requested computation.
  > `blocked` is different from "no forecastable structure." A blocked result means the workflow could not support the requested computation.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-9f840fe121a4faf1` [strategy] (literature_supported) — Reading a triage result should start with the fields indicating whether the result is usable and whether significance was actually computed.
  > Start with the fields that tell you whether the result is usable and whether significance was actually computed.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-9f8beabb447a6f8a` [concept] (literature_supported) — A known-future covariate is one whose k = 0 value is legitimately observed before Y_t must be predicted, such as calendar features, holidays, regulator-set tariffs, or planned promotions.
  > A "known-future" exogenous covariate is one whose $k=0$ value is legitimately observed **before** $Y_t$ must be predicted: calendar features, holidays, regulator-set tariffs, planned promotional events.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a55a7eb7bbaf3151` [failure_mode] (literature_supported) — If the underlying TriageResult is wrong, agent narration will be wrong in the same way because agent numeric claims restate deterministic results.
  > Any numeric claim in an agent response is a restatement of a deterministic result. If the underlying `TriageResult` is wrong, the agent narration will be wrong in the same way.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a68a41355532b8c9` [representation] (literature_supported) — The blocked field indicates whether triage completed at all.
  > `blocked` Whether triage completed at all
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a73966b1d34d18f9` [concept] (literature_supported) — When samples are equally spaced, each test set covers the same time duration while the training set accumulates data from previous splits.
  > Once this condition is met, each test set covers the same time duration, while the train set size accumulates data from previous splits.
  (documentation, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, published None, independence ind-s-ca7d54da5b087ed3, corroboration 1)
- `c-a99d5fd0e42f848c` [concept] (literature_supported) — In the average approach, predictions of all future values equal the mean of the past data.
  > In this approach, the predictions of all future values are equal to the mean of the past data.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-aaa1529f0a2d3311` [failure_mode] (literature_supported) — For series with n < 1000, phase-space coverage is insufficient and the LLE estimate is indicative only.
  > For series with $n < 1000$: phase-space coverage is insufficient and the estimate is indicative only.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ab5eb0265a1e687f` [decision] (literature_supported) — If a time series is believed to have seasonality, the seasonal naïve approach may be more appropriate than the plain naïve approach.
  > If the time series is believed to have seasonality, the seasonal naïve approach may be more appropriate where the forecasts are equal to the value from last season.
  (documentation, https://en.wikipedia.org/wiki/Forecasting, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-ad0bb66f93cc4546` [failure_mode] (literature_supported) — For forecast evaluation, diagnostics must be computed on each rolling-origin training window only, not on the full series, to avoid false out-of-sample validity claims.
  > For forecast evaluation, compute > diagnostics on each rolling-origin training window only. Do not compute on > full series and then claim out-of-sample validity.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-b3625c94c84ad5ea` [misconception] (literature_supported) — The causal methods are optional screening tools and should not be interpreted as complete causal proof.
  > The causal methods are optional screening tools. They should not be interpreted > as a complete causal proof.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-b4dcd0ba41b5ca5a` [interpretation] (literature_supported) — The deltas versus linear baseline should be interpreted as effect-size diagnostics rather than absolute truth.
  > Interpret these as effect-size diagnostics, not absolute truth.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-b8ffb36eceea04c9` [interpretation] (literature_supported) — When directness_ratio exceeds 1.0 the system flags arch_suspected, and this flag is a warning or anomaly boundary rather than positive evidence of any architecture.
  > When `directness_ratio > 1.0` the system flags `arch_suspected`. This flag is a **warning or anomaly boundary, not positive evidence** of any particular architecture.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-bc7d2ea8224122be` [concept] (literature_supported) — xami_sparse is a triage layer that cheaply prunes redundant lags and does not condition on the driver's own autohistory; that stronger conditioning is the job of pcmci_ami.
  > `xami_sparse` is a **triage layer** - it cheaply prunes redundant lags to reduce the feature tensor. It does **not** condition on the driver's own autohistory. That stronger conditioning is the job of `pcmci_ami` (`full_mci`) from v0.3.0.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-bce8f7b6d6e3119c` [interpretation] (literature_supported) — From v0.3.3 onward, the fingerprint confidence label can be 'abstain' when the routing policy emits no primary families.
  > On v0.3.3 and later, `bundle.recommendation.confidence_label` can also be > `abstain` when the routing policy emits no primary families.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-bd65950824d7841e` [check] (literature_supported) — Any lag where a derived-feature profile exceeds the raw profile by more than estimation noise should be treated as a data-leakage candidate, not a genuine gain.
  > compare the `values` arrays element-wise across two runs; any lag where the derived profile exceeds the raw profile by more than estimation noise is a data-leakage candidate, not a genuine gain.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-bff8b6f6f1e86840` [concept] (literature_supported) — Optional narration is a communication layer only and does not create or validate numeric results.
  > Communication layer only; it does not create or validate numeric results
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-cb4fb2e0335bda2c` [misconception] (literature_supported) — The DPI is a ceiling constraint rather than a pessimistic prediction; useful transforms such as the log of a multiplicative process may preserve nearly all forecastability.
  > useful transforms (e.g. log of a multiplicative process) may preserve nearly all forecastability. The DPI is a ceiling constraint, not a pessimistic prediction.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-cbea03a6c34f69d4` [strategy] (literature_supported) — Stable lag rankings and a small directness-ratio range should be preferred over raw pAMI magnitude.
  > Prefer stable lag rankings and small directness-ratio range over raw pAMI magnitude.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-cc2819301ec26104` [interpretation] (literature_supported) — A directness ratio near 1 indicates mostly direct structure, while a ratio much less than 1 indicates mostly mediated structure.
  > \(r \approx 1\): mostly direct structure. - \(r \ll 1\): mostly mediated structure.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ce2f5d73934e59d2` [failure_mode] (literature_supported) — Look-ahead leakage is silent, producing optimistic forecastability scores without errors, so users should always verify diagnostics are computed before the origin and scoring after it.
  > Look-ahead leakage in rolling-origin evaluation is silent - it produces optimistic > forecastability scores without any error message. Always verify that diagnostics > are computed before the origin and scoring after it.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d09b1709bcc67a98` [representation] (literature_supported) — The forecastability_class field gives a high-level interpretation when triage completed.
  > `forecastability_class` High-level interpretation when triage completed
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d108f9483393334e` [interpretation] (literature_supported) — A driver that keeps most of its pairwise signal after conditioning is a better downstream candidate; one that collapses is probably borrowing strength from target memory, common forcing, seasonality or shared regime.
  > A driver that keeps most of its pairwise signal after conditioning pressure is a better candidate for downstream use; a driver that collapses is probably borrowing strength from target memory, common forcing, seasonality, or shared regime.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d3af3ac9c12c2b7c` [strategy] (literature_supported) — Model evaluation should be targeted exclusively at horizons in the informative horizon set because lags outside it carry no detectable predictive signal above the noise floor.
  > A practitioner should target model evaluation exclusively at horizons in $\mathcal{H}_\varepsilon$ - lags outside this set carry no detectable predictive signal above the noise floor.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-df93dff263d162a3` [misconception] (literature_supported) — The forecastability ceiling is set by AMI, not entropy; F6 is only a complementary contextual tool.
  > F6 is a complementary contextual tool, not a forecastability measure. The forecastability ceiling is set by AMI, not entropy.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e0f0ce6bf728fd2b` [cue] (literature_supported) — directness_ratio above 1.0 arises most commonly in noisy series, misspecified linear residual backends, or very short series with high estimation variance.
  > It arises most commonly in noisy series, misspecified linear residual backends, or very short series where estimation variance is high.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e352729f80a0f394` [misconception] (literature_supported) — The fingerprint routing output is heuristic model-family guidance, not exact model selection and not a multivariate conditional-MI claim.
  > The > routing output is heuristic family guidance, not exact-model selection and not > a multivariate conditional-MI claim.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e3653a25d7c0a396` [interpretation] (literature_supported) — A very low directness_ratio, as in sine_wave (0.0157) and air_passengers (0.0993), supports compact structured models over long-lag complexity.
  > Very low `directness_ratio` in `sine_wave` (0.0157) and `air_passengers` (0.0993) supports compact structured models over long-lag complexity.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e4eedd7dc6b28efa` [failure_mode] (literature_supported) — The directness_ratio is a diagnostic ratio only and is unstable on weak or noisy short windows.
  > Diagnostic ratio only; unstable on weak/noisy short windows
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e52681e1c88610c3` [misconception] (literature_supported) — F8 detects predictive dependence, not causal direction, so it is not a causal screening tool.
  > As a causal screening tool: F8 detects predictive dependence, not causal direction.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e7905d279df312c3` [failure_mode] (literature_supported) — Sharp pAMI spikes at isolated lags appearing only for tree backends indicate overfitting, where the backend fits noise in the conditioning space.
  > Overfitting in nonlinear backends sharp pAMI spikes at isolated lags only for tree backends backend fits noise in conditioning space
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ea150f804aab1232` [representation] (literature_supported) — The readiness_status field indicates whether the data is clear, warning-level, or blocked.
  > `readiness_status` Whether the data is clear, warning-level, or blocked
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ed9ee81df374d444` [concept] (literature_supported) — In the k-th split, TimeSeriesSplit returns the first k folds as the training set and the (k+1)-th fold as the test set.
  > In the k-th split, it returns the first k folds as the train set and the (k+1)-th fold as the test set.
  (documentation, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html, published None, independence ind-s-ca7d54da5b087ed3, corroboration 1)
- `c-edc181681f54f407` [representation] (literature_supported) — pipeline/rolling_origin.py contains rolling-origin split helpers used by evaluation workflows.
  > `pipeline/rolling_origin.py` contains rolling-origin split helpers used by evaluation workflows.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f03ade7bfe27b377` [mental_model] (literature_supported) — Downstream forecasting frameworks are consumers of triage results, not competitors.
  > Downstream frameworks are consumers of triage results, not competitors.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f7bae48e67a8e5a1` [prerequisite] (literature_supported) — For permutation entropy with embedding order m = 5, at least about 600 observations are recommended.
  > permutation entropy requires adequate pattern-frequency estimates; for $m = 5$, at least $n \approx 600$ is recommended.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f849899d8be3fc45` [interpretation] (literature_supported) — The IT limit diagnostics (F2) ceiling on prediction improvement holds under log loss only.
  > Ceiling holds under log loss only; exploitation ratio deferred (pre-model repo)
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f8b08d5427aa4b76` [norm] (literature_supported) — Downstream forecasting frameworks should be used after triage, not as a replacement for it.
  > Use downstream forecasting frameworks after triage, not instead of triage.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)

### Synthetic / rejected claims

- `c-01f4991ccdf226d8` [check] (synthetic_extrapolation) — A directness_ratio above 1.0 should be treated as a warning and verified with multiple backends and sample-size stress.
  > Treat as warning; verify with multiple backends and sample-size stress
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md)
- `c-02471dfd7d502aa5` [misconception] (synthetic_extrapolation) — Triage is not a replacement for full backtesting or deployment validation.
  > Not a replacement for full backtesting or deployment validation
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md)
- `c-05488923b7e30cd1` [expectancy] (synthetic_extrapolation) — For the AR(1) setup with phi=0.85, the expected result is not blocked, readiness warning, high forecastability class, and primary lags 1 and 7.
  > "blocked": false, "readiness_status": "warning", "forecastability_class": "high", "modeling_regime": "compact_structured_models", "primary_lags": [1, 7]
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/quickstart.md)
- `c-08feadc175daa8b5` [expectancy] (synthetic_extrapolation) — bike_cnt_temp has the strongest useful exogenous signal, with mean raw cross MI 0.0906, mean conditioned cross MI 0.0523, and no warning horizons.
  > `bike_cnt_temp` has the strongest useful signal (`mean_raw_cross_mi=0.0906`, `mean_conditioned_cross_mi=0.0523`, no warning horizons)
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md)
- `c-0f8d96b9f591b232` [norm] (synthetic_extrapolation) — The toolkit should not replace rolling-origin forecast evaluation and business KPI tracking.
  > Replacing rolling-origin forecast evaluation and business KPI tracking.
  (verdict insufficient [adds_content, connective_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md)
- `c-1760b3bf63f5043e` [norm] (synthetic_extrapolation) — In batch diagnostic ranking, composite weighting across incommensurable scales must be transparent.
  > Composite weighting across incommensurable scales must be transparent
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md)
- `c-1e2b146f3c4aa2ef` [rationale] (synthetic_extrapolation) — DTW is out of scope for lagged-exogenous triage because it does not produce a fixed-lag predictive feature set.
  > They do not: - produce a fixed-lag predictive feature set
  (verdict insufficient [adds_content, connective_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md)
- `c-209129719dbbec10` [norm] (synthetic_extrapolation) — LLE results should always be combined with AMI/pAMI evidence and the F6 complexity band before drawing conclusions. (no located evidence)
- `c-28d66926b67119a9` [decision] (synthetic_extrapolation) — Noise-linked driver cases can be deprioritised early in exogenous screening.
  > multiple noise-linked cases can be deprioritised early
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md)
- `c-299566a385f06f26` [expectancy] (synthetic_extrapolation) — In the exogenous slice, 6 of 7 cases have warning horizons and at least one directness_ratio above 1.0.
  > In this slice, 6/7 cases have warning horizons and at least one `directness_ratio > 1.0`
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md)
- `c-2d682b2ef7764e25` [decision] (synthetic_extrapolation) — If the theoretical limit is low, gains from model engineering diminish rapidly, so F2 should be checked before investing in complex models.
  > Before investing in complex models: if the limit is low, model engineering gains diminish rapidly.
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md)
- `c-2e362948f699a9c1` [failure_mode] (synthetic_extrapolation) — If the factors are not well understood or the actual outcome is affected by the forecasts, forecast reliability can be significantly lower.
  > If this is not the case or if the actual outcome is affected by the forecasts, the reliability of the forecasts can be significantly lower.
  (verdict insufficient [adds_content, scope_differs], https://en.wikipedia.org/wiki/Forecasting)
- `c-3110c09bd6d9e0ed` [expectancy] (synthetic_extrapolation) — In the current canonical run, 2 of 8 series are classed high forecastability, 1 medium, and 5 low.
  > In the current run, 2/8 series are `forecastability_class=high`, 1/8 is `medium`, and 5/8 are `low`
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md)
- `c-3410b5f3e72fcdcc` [norm] (synthetic_extrapolation) — The toolkit should not be used to set maintenance policy thresholds without domain constraints and risk-cost modeling.
  > Setting maintenance policy thresholds without domain constraints and risk-cost modeling.
  (verdict insufficient [adds_content, scope_differs, connective_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md)
- `c-3b3b4e2fac5eeccb` [check] (synthetic_extrapolation) — IT limit diagnostics flag information-destroying transforms through compression/DPI warnings.
  > Ceiling per horizon, compression/DPI warnings Sets realistic expectations before model investment; flags information-destroying transforms
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md)
- `c-3f2c13f5137857ea` [strategy] (synthetic_extrapolation) — The F3 recommended plateau k* serves as a principled starting point for selecting a forecasting model's lookback window.
  > When selecting the lookback window for a forecasting model: use the recommended plateau $k^*$ as a principled starting point.
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md)
- `c-40d677f5f3a8d01b` [failure_mode] (synthetic_extrapolation) — If a decision changes when the backend changes, this indicates false confidence from one backend, typically due to model class mismatch or noisy data.
  > False confidence from one backend decision changes when backend changes model class mismatch or noisy data
  (verdict insufficient [adds_content, connective_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md)
- `c-41afe3fc477e2aa5` [representation] (synthetic_extrapolation) — In v0.3.2, a lag_role of "instant" marks k = 0 contemporaneous association, and "predictive" marks k ≥ 1 fixed-lag predictive association.
  > `"instant"` $k = 0$ Contemporaneous association - structural / multivariate `"predictive"` $k \ge 1$ Fixed-lag predictive association - covariant-informative
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md)
- `c-46c0777fbb3fee53` [failure_mode] (synthetic_extrapolation) — For very short series, finite-sample bias inflates the estimated theoretical limit.
  > When series length is very short: finite-sample bias inflates the estimated limit.
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md)
- `c-4bc4f0652d8b92b5` [misconception] (synthetic_extrapolation) — The toolkit is not a causal-discovery guarantee. (no located evidence)
- `c-4e39016b1fbf9ac6` [representation] (synthetic_extrapolation) — mutual_info_regression returns estimated mutual information in nat units.
  > Estimated mutual information between each feature and the target in nat units.
  (verdict insufficient [adds_content, scope_differs], https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.mutual_info_regression.html)
- `c-5938d65549cba1fa` [concept] (synthetic_extrapolation) — The directness_ratio is the area under the pAMI curve divided by the area under the AMI curve.
  > `directness_ratio`: \[ r = \frac{\operatorname{AUC}(\tilde{I}_h)}{\operatorname{AUC}(I_h)} \]
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md)
- `c-59cb68f7338da37c` [failure_mode] (synthetic_extrapolation) — A common failure is running a model leaderboard first and only later discovering weak target memory, horizon mismatch, unsafe covariates, or leaking lags.
  > Run a leaderboard. Then discover the target has weak memory, the horizon is mismatched to the signal, the best covariates are unsafe at prediction time, or the strongest lags would leak future information.
  (verdict insufficient [adds_content, connective_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md)
- `c-602485784a325d8d` [rationale] (synthetic_extrapolation) — DTW is out of scope because it does not output a lag map directly consumable by ordinary regression or neural forecasting models.
  > output a lag map that is directly consumable by ordinary regression or neural forecasting models
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md)
- `c-659428711cd1d4f5` [representation] (synthetic_extrapolation) — models.py provides forecast baselines and optional model integrations used by rolling-origin workflows, as repo-facing support rather than public contract.
  > Forecast baselines and optional model integrations used by rolling-origin workflows Repo-facing support
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md)
- `c-683d3e0f3738a48e` [failure_mode] (synthetic_extrapolation) — Exogenous analysis is association-based screening, so confounding and common-cause effects can remain.
  > Association-based screening; confounding and common-cause effects can remain
  (verdict insufficient [adds_content, scope_differs, connective_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md)
- `c-740f3b542aaadaee` [check] (synthetic_extrapolation) — The triage result exposes blocked status, readiness status, and an interpretation that may be None, containing forecastability class and primary lags.
  > "forecastability_class": ( None if result.interpretation is None else result.interpretation.forecastability_class ),
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md)
- `c-76e1c8d9bbe2a761` [rationale] (synthetic_extrapolation) — Separating diagnostic training windows from forecast-error test windows is mandatory to prevent leakage.
  > This separation is mandatory to prevent leakage.
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md)
- `c-81549db28b9043fc` [check] (synthetic_extrapolation) — Overfitting in nonlinear backends is mitigated by comparing against the linear baseline and requiring ranking stability.
  > compare against linear baseline and require ranking stability
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md)
- `c-925a8b9fb40706b4` [misconception] (synthetic_extrapolation) — The toolkit should not be used to prove physical causality between variables. (no located evidence)
- `c-a0522c9edd818ce9` [procedure_step] (synthetic_extrapolation) — Downstream model families or framework-specific settings should be recommended only after triage.
  > Only then recommend downstream model families or framework-specific settings.
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt)
- `c-acf21d8af8e10934` [rationale] (synthetic_extrapolation) — A leaderboard can hide confounded driver structure that triage makes visible before modeling.
  > A leaderboard can hide that mess. Triage makes it visible before the first model is fitted.
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md)
- `c-ad07205d11f40927` [concept] (synthetic_extrapolation) — In v0.5.0, signal_to_noise was renamed to informative_mass_fraction.
  > `signal_to_noise` has been renamed to `informative_mass_fraction`
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md)
- `c-b3786eaf21f746ca` [rationale] (synthetic_extrapolation) — DTW is out of scope because it does not respect the chronological causality required by forecasting tensors.
  > respect the chronological causality required by forecasting tensors
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md)
- `c-b3abbe1bfd70b5f9` [interpretation] (synthetic_extrapolation) — F2 limit compression reveals whether low AMI reflects a genuinely low ceiling or a sampled curve that has not saturated the limit.
  > limit compression reveals whether the ceiling is genuinely low (hard limit) or whether the sampled curve has not saturated the limit.
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md)
- `c-c030e8d5e7297551` [norm] (synthetic_extrapolation) — Experimental diagnostics such as F5 Lyapunov should not be treated as automated decision criteria without expert review.
  > Treating experimental diagnostics (F5 Lyapunov) as automated decision criteria without expert review.
  (verdict insufficient [adds_content, connective_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md)
- `c-c0c29862e5d8a193` [representation] (synthetic_extrapolation) — reporting/interpretation.py owns deterministic interpretation output. (no located evidence)
- `c-c1447fb6f7d85750` [failure_mode] (synthetic_extrapolation) — Ω misses nonlinear dependence entirely and should not be used as the sole forecastability measure.
  > As the sole forecastability measure: Ω misses nonlinear dependence entirely.
  (verdict insufficient [adds_content, connective_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md)
- `c-c16fdb1ea6fb543e` [procedure_step] (synthetic_extrapolation) — The result fields should be interpreted in order: blocked, readiness_status, compute_surrogates, forecastability_class, primary_lags.
  > Interpret those fields in this order. Field What it tells you --- --- `blocked` Whether triage completed at all `readiness_status` Whether the data is clear, warning-level, or blocked `compute_surrogates` Whether significance was actually computed
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md)
- `c-c6f5589ea5d04221` [decision] (synthetic_extrapolation) — Triage should help decide when the workflow should abstain and fall back to baselines.
  > When should the workflow abstain and fall back to baselines?
  (verdict insufficient [adds_content, scope_differs, connective_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md)
- `c-d0c47e8627d61fd2` [prerequisite] (synthetic_extrapolation) — Ω should not be applied to strongly non-stationary series without prior detrending.
  > For strongly non-stationary series without prior detrending.
  (verdict insufficient [adds_content, connective_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md)
- `c-dc2775269db22561` [misconception] (synthetic_extrapolation) — Agents and MCP do not compute or validate the science; they only route or narrate deterministic outputs.
  > Agents and MCP do not compute or validate the science. They route or narrate deterministic outputs.
  (verdict insufficient [adds_content, connective_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md)
- `c-df0a162c145920ab` [expert_novice_contrast] (synthetic_extrapolation) — Unlike standard cross-validation, successive TimeSeriesSplit training sets are supersets of earlier ones.
  > Note that, unlike standard cross-validation methods, successive training sets are supersets of those that come before them.
  (verdict pending, https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html)
- `c-dfe43797f017f220` [failure_mode] (synthetic_extrapolation) — The toolkit should not be used to compare very short windows where minimum sample assumptions are not met.
  > Comparing very short windows where minimum sample assumptions are not met.
  (verdict insufficient [adds_content, connective_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/why_use_this.md)
- `c-e3540ccc2fab96d5` [mental_model] (synthetic_extrapolation) — The drift method is equivalent to drawing a line between the first and last observation and extrapolating it into the future.
  > This is equivalent to drawing a line between the first and last observation, and extrapolating it into the future.
  (verdict insufficient [adds_content, scope_differs], https://en.wikipedia.org/wiki/Forecasting)
- `c-edd946426037eb2e` [strategy] (synthetic_extrapolation) — Forecastability classes support separating rich-model candidates from baseline-first candidates before model search.
  > which supports separating rich-model candidates from baseline-first candidates before model search
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md)
- `c-f019defaaf1554b2` [rationale] (synthetic_extrapolation) — Blocking selected_for_tensor=True at k = 0 by default is an intentional chronological-causality guard rather than a library limitation.
  > This is not a library limitation - it is an intentional chronological-causality > guard.
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md)
- `c-f1eb2102b41a2a57` [check] (synthetic_extrapolation) — Cross-correlation results should always be cross-checked with cross_ami. (no located evidence)
- `c-f35b5500629fd423` [prerequisite] (synthetic_extrapolation) — F2 should not be used without F1 because the limit is derived from the AMI curve.
  > As a standalone decision without F1: the limit is derived from the AMI curve, so F1 evidence is prerequisite context.
  (verdict insufficient [scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md)
- `c-f40d91bb0184a4c3` [norm] (synthetic_extrapolation) — In rolling-origin evaluation, AMI/pAMI diagnostics are computed on each training window only.
  > Diagnostics (AMI/pAMI) are computed on each training window only.
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md)
- `c-f523ad5ae6225e41` [check] (synthetic_extrapolation) — Short-sample fragility is mitigated by enforcing a minimum length and inspecting stress table stability.
  > enforce minimum length and inspect stress table stability
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/pami_residual_backends.md)
- `c-fe929c89d57f4d35` [expectancy] (synthetic_extrapolation) — For an AR(1) series with phi 0.7 and n 300, the example triage yields a peak horizon of 1 and a HIGH model_now recommendation.
  > print(profile.peak_horizon) # 1 print(profile.model_now) # HIGH - Complex structured models
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md)
- `c-fffd03ece9a7d091` [interpretation] (synthetic_extrapolation) — Because true MI cannot be negative, negative estimates from mutual_info_regression are replaced by zero.
  > True mutual information can't be negative. If its estimate turns out to be negative, it is replaced by zero.
  (verdict insufficient [adds_content, scope_differs], https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.mutual_info_regression.html)

### UNKNOWN / thin / unverified / unexamined slots

- decision: thin
- cue: thin
- check: thin
- failure_mode: thin
- rationale: thin
- procedure_step: thin

## Area: Toolkit installation and repository setup

### Supported claims

- `c-03329bb964696b2f` [procedure_step] (literature_supported) — The package can be installed with pip install dependence-forecastability, or from GitHub as a fallback if package resolution is unavailable.
  > Install the package from the published package, or use the GitHub fallback if package resolution is not available: pip install dependence-forecastability pip install git+https://github.com/AdamKrysztopa/dependence-forecastability.git
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-086c811f0898b10c` [procedure_step] (literature_supported) — The canonical single-series workflow is run via `scripts/run_canonical_triage.py`, which builds canonical outputs for exemplar series.
  > Canonical single-series workflow `scripts/run_canonical_triage.py` Builds canonical outputs for exemplar series
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-0ed9f22467595edb` [failure_mode] (literature_supported) — Checked-in files under outputs/json, outputs/tables, and outputs/reports are reference artifacts not guaranteed to be freshly regenerated for every commit.
  > Checked-in files under `outputs/json/`, `outputs/tables/`, and `outputs/reports/` are reference artifacts. They are useful examples of the artifact surface, but they are not guaranteed to be freshly regenerated for every commit.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-2589a791f417df2a` [concept] (literature_supported) — The example notebooks live in a separate forecastability-examples repository, while the core package remains framework-agnostic.
  > These notebooks live in the sibling `forecastability-examples` repository. The core `dependence-forecastability` package remains framework-agnostic.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-369186b6ad4d560a` [procedure_step] (literature_supported) — The agent layer is installed with pip install forecastability[agent].
  > `pip install forecastability[agent]` for agent layer
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3b2be48592baf523` [concept] (literature_supported) — The package is a deterministic pre-model diagnostic layer, not a model-training or forecasting library.
  > This package is a deterministic pre-model diagnostic layer, not a downstream model-training or forecasting library.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-3d2084add72fe975` [prerequisite] (literature_supported) — PCMCI and PCMCI-AMI causal screening methods require installing the optional causal extra.
  > The PCMCI methods require the optional causal extra: pip install "dependence-forecastability[causal]"
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-42484cad0161d7fb` [concept] (literature_supported) — The MuTE toolbox is a MATLAB toolbox for computing transfer entropy with different estimators.
  > a toolbox, developed in MATLAB, for computation of transfer entropy with different estimators.
  (documentation, https://en.wikipedia.org/wiki/Transfer_entropy, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-466602fa4b3a8ec2` [concept] (literature_supported) — The exogenous workflow `scripts/run_exog_analysis.py` runs exogenous screening and related artifacts.
  > Exogenous workflow `scripts/run_exog_analysis.py` Runs exogenous screening and related artifacts
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-56ed90f241f7c02f` [procedure_step] (literature_supported) — The recommended reading order starts with README.md, then docs/quickstart.md, then docs/public_api.md.
  > Start here in this order: 1. README.md 2. docs/quickstart.md 3. docs/public_api.md
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-64f86f8f80e56da1` [prerequisite] (literature_supported) — The MCP server needs additional server-framework dependencies not included in the default install.
  > The MCP server requires additional server-framework dependencies. It is not included in the default install.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-65b7f762a1a249d5` [strategy] (literature_supported) — Most users first need the package facade documented in public_api.md.
  > Most users only need three things in order: 1. The package facade in [../public_api.md](../public_api.md).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-6d256eca9a9a2fba` [prerequisite] (literature_supported) — The supported Python versions are 3.11 and 3.12.
  > Supported Python versions: Python 3.11, 3.12
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-72d3ff3a0ef5ef37` [strategy] (literature_supported) — The notebook learning path should start with the air passengers showcase or covariant informative showcase walkthrough before deeper notebooks.
  > start with `walkthroughs/00_air_passengers_showcase.ipynb` or `walkthroughs/01_covariant_informative_showcase.ipynb` First-stop walkthrough plus the covariant benchmark walkthrough before deeper notebooks
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-75f528be67790f2a` [concept] (literature_supported) — The benchmark panel workflow `scripts/run_benchmark_panel.py` runs the benchmark panel and writes summary artifacts.
  > Benchmark panel workflow `scripts/run_benchmark_panel.py` Runs the benchmark panel and writes summary artifacts
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7a2db4ff0000aac0` [concept] (literature_supported) — The report-building workflow `scripts/build_report_artifacts.py` builds report-facing artifacts from generated outputs.
  > Report-building workflow `scripts/build_report_artifacts.py` Builds report-facing artifacts from generated outputs
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7bbe881de26b6f26` [procedure_step] (literature_supported) — The HTTP API is installed with pip install forecastability[api].
  > `pip install forecastability[api]` for HTTP API
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7eb48509de87201c` [rationale] (literature_supported) — The core/examples split is intentional so the core produces deterministic evidence and the examples show framework-specific translation.
  > That split is intentional: the core package produces deterministic evidence; the examples repository shows how to translate that evidence into framework-specific modeling recipes.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-84e044e00bcff6ae` [misconception] (literature_supported) — A working demonstration in one toolkit surface should not be taken as implying stability guarantees for all surfaces.
  > Do not assume that a working demonstration in one surface implies stability guarantees for all surfaces.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a06bce70252263b9` [representation] (literature_supported) — Worked examples live in examples/univariate/ and examples/covariant_informative/, while notebook deep dives remain under notebooks/triage/.
  > Worked examples now live in `examples/univariate/` and `examples/covariant_informative/`; notebook deep dives remain under `notebooks/triage/`
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a0b523bc132a1ec1` [procedure_step] (literature_supported) — Contributors should use the developer guide for repo workflow around scripts, notebooks, configs, outputs, and docs.
  > Use [../maintenance/developer_guide.md](../maintenance/developer_guide.md) for the repo workflow around scripts, notebooks, configs, outputs, and docs.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a1071f649e580467` [norm] (literature_supported) — Users should prefer the stable facade modules `forecastability` and `forecastability.triage`.
  > Use the stable facade first: prefer `forecastability` and `forecastability.triage`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a67245f5623db341` [concept] (literature_supported) — The deterministic core and stable facades are stable, the CLI and HTTP API are beta, and the MCP server and agent layer are experimental.
  > The deterministic core and stable facades are stable; CLI and HTTP API are beta; MCP server and agent layer are experimental.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-aeaa8912739a0289` [procedure_step] (literature_supported) — The published package can be installed from PyPI with pip install dependence-forecastability.
  > If you want the published package surface, install from PyPI. pip install dependence-forecastability
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c39785d56f9bdc5c` [concept] (literature_supported) — The package name is dependence-forecastability but the import path is forecastability.
  > The package name is `dependence-forecastability`; the public import path is `forecastability`.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d31e9925b87c3ad1` [procedure_step] (literature_supported) — The toolkit can be installed with pip or added with uv.
  > pip install dependence-forecastability # or with uv uv add dependence-forecastability
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d5bfbf382e22a63b` [prerequisite] (literature_supported) — The toolkit requires Python 3.11 or later; earlier versions produce parse errors.
  > **Python 3.11+ required.** The codebase uses 3.11-specific syntax and type features. Earlier Python versions are not supported and will produce parse errors.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-dca0d1e90a3d8d66` [procedure_step] (literature_supported) — To run the notebooks, clone the examples repository, run uv sync --all-extras, then uv run jupyter lab.
  > git clone https://github.com/AdamKrysztopa/forecastability-examples.git cd forecastability-examples uv sync --all-extras uv run jupyter lab
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e6878d07cc4c4645` [strategy] (literature_supported) — In constrained environments, only the needed extras should be installed, e.g. pip install forecastability for core only.
  > In constrained environments, install only the extras you need: - `pip install forecastability` for core only
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-f5f5715dbcec697a` [concept] (literature_supported) — The Java Information Dynamics Toolkit (JIDT) is a Java toolbox usable in MATLAB, GNU Octave and Python for computing transfer entropy and related measures on discrete and continuous-valued data.
  > a toolbox, developed in Java and usable in MATLAB, GNU Octave and Python, for computation of transfer entropy and related information-theoretic measures in both discrete and continuous-valued data.
  (documentation, https://en.wikipedia.org/wiki/Transfer_entropy, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-f8af97a8b817b032` [concept] (literature_supported) — Notebooks and walkthroughs are located in the separate `forecastability-examples` sibling repository.
  > Notebooks and walkthroughs live in the `forecastability-examples` sibling repository.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-fb5aac2a07e79b1e` [mental_model] (literature_supported) — The supported public surfaces are the package facades plus the declared runtime entry points, and the codebase is no longer a flat module layout.
  > the live codebase is not a flat module layout anymore, and the supported public surfaces are the package facades plus the declared runtime entry points
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-fff30775f8c35cd4` [procedure_step] (literature_supported) — When working in the repository, the local environment is synced with uv sync.
  > If you are working in the repository, sync the local environment. uv sync
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)

### Synthetic / rejected claims

- `c-2476bf309531cfc7` [strategy] (synthetic_extrapolation) — If opening only one notebook, the recommended one is the CausalRivers lag and feature selection walkthrough, since it combines drivers, negative controls, lag screening, sparse selection and hand-off.
  > If you open only one notebook, open [`walkthroughs/07_causal_rivers_lag_and_feature_selection.ipynb`]
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md)
- `c-275acb36295e35d8` [procedure_step] (synthetic_extrapolation) — After the public API doc, the reading order continues with the forecast-prep recipe, the minimal Python and covariant examples, and the examples index.
  > 4. docs/recipes/forecast_prep_to_external_frameworks.md 5. examples/minimal_python.py 6. examples/minimal_covariant.py 7. docs/examples_index.md
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt)
- `c-62555515e63b0bdf` [strategy] (synthetic_extrapolation) — Second, most users need the notebook path in the forecastability-examples sibling repository.
  > 2. The notebook path in the [forecastability-examples](https://github.com/AdamKrysztopa/forecastability-examples) sibling repository
  (verdict insufficient [adds_content, scope_differs, connective_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md)
- `c-9ef5597ec1971a49` [concept] (synthetic_extrapolation) — The toolkit has not been systematically tested on Windows; development and CI run on macOS and Linux.
  > Development and CI run on macOS and Linux. Windows path handling, line endings, and subprocess behaviour have not been systematically tested.
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md)
- `c-a674b63dac73e127` [prerequisite] (synthetic_extrapolation) — The n_jobs parameter of mutual_info_regression was added in version 1.5.
  > See Glossary for more details. Added in version 1.5.
  (verdict insufficient [adds_content, scope_differs], https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.mutual_info_regression.html)
- `c-ad8f61e78c3f143d` [representation] (synthetic_extrapolation) — The stable package facade lives at src/forecastability/__init__.py. (no located evidence)
- `c-ca43b02369790e49` [concept] (synthetic_extrapolation) — The core forecastability package has no import-time or runtime dependencies on Darts, MLForecast, StatsForecast, Nixtla or similar libraries; such extras live in the examples repository.
  > The core `forecastability` package has no import-time or runtime dependencies on Darts, MLForecast, StatsForecast, Nixtla, or similar forecasting libraries
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md)
- `c-df804ba62c0a5f7e` [strategy] (synthetic_extrapolation) — Third, users need the maintainer scripts documented in the developer guide only when they need repo workflows.
  > 3. The maintainer scripts documented in [../maintenance/developer_guide.md](../maintenance/developer_guide.md) when they need repo workflows.
  (verdict insufficient [adds_content, connective_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md)
- `c-e6ede8c75e012a6b` [prerequisite] (synthetic_extrapolation) — Causal methods require installing the causal extra of dependence-forecastability. (no located evidence)

### UNKNOWN / thin / unverified / unexamined slots

- decision: unknown
- cue: unknown
- check: unknown
- failure_mode: thin
- norm: thin
- rationale: thin
- procedure_step: thin

### Unknown placeholders

- `c-21de18d8f2c08309` [cue] — What observable features of a situation signal that Toolkit installation and repository setup applies or needs a different response?
- `c-270124731a55e758` [decision] — What conditions determine which option is chosen in Toolkit installation and repository setup?
- `c-31bccc8448023450` [check] — How is work in Toolkit installation and repository setup checked for correctness or compliance?

## Area: Extending the toolkit with new estimators and tests

### Supported claims

- `c-01a6d75f0ff964b4` [concept] (literature_supported) — The MCP server and agent narration surfaces are experimental adapter surfaces.
  > MCP server adapter surface Experimental Agent narration adapter surface Experimental
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-111f43a526a90d28` [mental_model] (literature_supported) — Triage, pipeline, and services consume metrics, diagnostics, reporting, and utils.
  > Triage, pipeline, and services consume metrics, diagnostics, reporting, and utils.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-111fcdab3bad80d5` [misconception] (literature_supported) — The repository does not claim that every historical helper has been perfectly normalized into a textbook hexagonal architecture.
  > it is not pretending that every historical helper has been perfectly normalized into a textbook hexagon
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-12fcd440ab5152d2` [norm] (literature_supported) — Contributors should keep deterministic orchestration in use_cases and pipeline rather than in notebooks or scripts.
  > Keep deterministic orchestration in `use_cases/` and `pipeline/` rather than notebooks or scripts.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-16eca636991e94e4` [representation] (literature_supported) — transfer_entropy_service.py is a compatibility facade that re-exports the diagnostics TE functions.
  > `src/forecastability/services/transfer_entropy_service.py`: compatibility facade re-exporting the diagnostics functions.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-19ce99b47740dfa8` [norm] (literature_supported) — Contributors should treat services as internal helpers, not as a third public API layer.
  > Treat `services/` as internal helpers, not as a third public API layer.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-1c4e8047d3bd12be` [decision] (literature_supported) — Contributors should consult public_api.md when deciding whether a symbol is part of the supported import contract.
  > Use [../public_api.md](../public_api.md) when deciding whether a symbol is part of the supported import contract.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-221f866e4872439f` [expectancy] (literature_supported) — The services, utils, pipeline, metrics, diagnostics, and reporting packages are internal structure that may continue to move during consolidation.
  > `services/`, `utils/`, `pipeline/`, `metrics/`, `diagnostics/`, `reporting/` Internal structure that may continue to move during consolidation
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-280251fefcee28f3` [representation] (literature_supported) — The core TE estimator functions compute_transfer_entropy() and compute_transfer_entropy_curve() live in src/forecastability/diagnostics/transfer_entropy.py.
  > `src/forecastability/diagnostics/transfer_entropy.py`: `compute_transfer_entropy()` and `compute_transfer_entropy_curve()` (core estimator path).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-443aa99f1861f89a` [representation] (literature_supported) — The CausalGraphFullPort contract provides both discover returning CausalGraphResult and discover_full returning PcmciAmiResult for the PCMCI-AMI three-phase path.
  > `CausalGraphFullPort` `discover(...) -> CausalGraphResult` and `discover_full(...) -> PcmciAmiResult` PCMCI-AMI full three-phase result path
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4c9d9f7275c52f3d` [norm] (literature_supported) — Any new selector that goes further, such as one conditioning on driver autohistory, must be introduced under a new method label so existing cross_pami and xami_sparse semantics are not silently extended.
  > Any new selector that goes further (PMIME-style, PC-stable with driver autohistory) must be introduced under a **new method label** so that the shipped `cross_pami` and `xami_sparse` semantics are not silently extended.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4cf8da484fd3be39` [norm] (literature_supported) — Contributors should put transport concerns in adapters, not in use cases or metrics code.
  > Put transport concerns in `adapters/`, not in use cases or metrics code.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-4ea0880906c4e577` [concept] (literature_supported) — The forecastability and forecastability.triage modules are the stable import contract.
  > `forecastability` and `forecastability.triage` Stable import contract
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-57e96f611c3a0ccb` [concept] (literature_supported) — In v0.5.0 the default estimator was upgraded to KSG-II.
  > **v0.5.0** - Default estimator upgraded to KSG-II
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5d4e1e195302a4e3` [representation] (literature_supported) — metrics/scorers.py owns the scorer registry and built-in scorer family metadata.
  > `metrics/scorers.py` owns the scorer registry and built-in scorer family metadata.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5e1cf37fab1d0e27` [failure_mode] (literature_supported) — New scorers inherit kNN estimation noise on short series.
  > new scorers inherit kNN estimation noise on short series
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-5e29ea6d046a67da` [decision] (literature_supported) — Contributors should consult architecture.md when deciding where new logic should live.
  > Use [../explanation/architecture.md](../explanation/architecture.md) when deciding where new logic should live.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-602d1e75f18618f3` [decision] (literature_supported) — Contributors should use ports for protocol-style seams when a collaborator needs to be substituted or isolated.
  > Use `ports/` for protocol-style seams when a collaborator needs to be substituted or isolated.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-69f267782709aaf0` [norm] (literature_supported) — An elastic-alignment result would require a new surface, a new method label, and an explicit chronological-causality guard before entering a forecasting tensor.
  > Any elastic-alignment result would need a new surface, a new method label, and an explicit chronological-causality guard before it could be admitted to a forecasting tensor.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-702721b0e7c013df` [norm] (literature_supported) — `docs/public_api.md` is to be treated as the supported import contract.
  > Treat `docs/public_api.md` as the supported import contract.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/llms.txt, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-7257cf68aa69d697` [concept] (literature_supported) — generate_covariant_benchmark in src/forecastability/utils/synthetic.py implements an 8-variable ground-truth system for controlled method validation.
  > `generate_covariant_benchmark` in `src/forecastability/utils/synthetic.py` implements an 8-variable ground-truth system used for controlled method validation.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-814e04c447ad4926` [concept] (literature_supported) — The CLI, HTTP API, and dashboard surfaces are Beta stability.
  > CLI `forecastability` Beta HTTP API `forecastability.adapters.api:app` Beta Dashboard `forecastability-dashboard` Beta
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/how-to/golden_path.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-87df96b4f308019b` [check] (literature_supported) — In the validation run, the analyzer's raw TE curve matched compute_transfer_entropy_curve exactly, with a maximum absolute difference of 0.0.
  > `ForecastabilityAnalyzerExog(..., method="te")` raw TE curve matched `compute_transfer_entropy_curve(...)` exactly (`max_abs_diff = 0.0`).
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-8e0fae92e47e7b4d` [mental_model] (literature_supported) — The stable public contract of the repository is small, while the internal package tree is deliberately split across many packages.
  > the stable public contract is small, while the internal package tree is deliberately split across triage models, use cases, analyzers, metrics, diagnostics, reporting, utils, adapters, services, ports, and bootstrap helpers
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-a1030c3ff960d453` [strategy] (literature_supported) — The probabilities in the transfer entropy formula can be estimated using binning or nearest-neighbour approaches.
  > The probabilities in the entropy formula can be estimated using different approaches (binning, nearest neighbors)
  (documentation, https://en.wikipedia.org/wiki/Transfer_entropy, published None, independence ind-s-0b00932c0a642b74, corroboration 1)
- `c-ac05da296c30cec6` [rationale] (literature_supported) — The nonlinear drivers are included to validate that AMI, TE, and GCMI scores remain informative where Pearson and Spearman fail, and to motivate the PCMCI-AMI-Hybrid design.
  > The nonlinear drivers are included to validate that AMI, TE, and GCMI scores remain informative exactly where Pearson and Spearman fail, and to motivate the PCMCI-AMI-Hybrid design in V3-F04.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-ae8b20ebf80f3248` [mental_model] (literature_supported) — The known_future_drivers contract is honored at the use-case layer, and the selector service itself is pure and does not read it.
  > The `known_future_drivers` contract is honored at the **use-case layer** (`run_lagged_exogenous_triage`). The selector service itself is pure and does not read it.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/lagged_exogenous_triage.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-bfda34a665d27f27` [mental_model] (literature_supported) — The package is layered and subpackage-heavy, with a small stable import facade and an internal tree organized by role.
  > The package is layered and subpackage-heavy. The stable import facade is small, but the internal tree is organized by role
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c1f3d813056e784f` [mental_model] (literature_supported) — Ports and bootstrap remain support seams rather than primary business-logic owners.
  > Ports and bootstrap remain support seams rather than primary business-logic owners.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-c6bbdec6744fb515` [decision] (literature_supported) — Contributors should add new user-facing imports through forecastability or forecastability.triage only when they want to commit to compatibility.
  > Add new user-facing imports through `forecastability` or `forecastability.triage` only when you want to commit to compatibility.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-cd9ceb59b47d756c` [concept] (literature_supported) — The paper validates only AMI; pAMI, exogenous cross-dependence, and scorer-registry abstractions are project additions.
  > Paper validates AMI only. - pAMI, exogenous cross-dependence, and scorer-registry abstractions are project additions.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d184afb5f42c512f` [mental_model] (literature_supported) — Profile reliability inherits from the underlying MI estimator, so improving estimator accuracy (more surrogates, larger samples, better n_neighbors) propagates automatically to the profile.
  > Reliability and variance properties of all profile fields inherit entirely from the underlying MI estimator; improving estimator accuracy (e.g. raising `n_surrogates`, increasing the sample size, or choosing a better-matched `n_neighbors`) propagates automatically to the profile.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-d842abf5a063991d` [norm] (literature_supported) — Adapters should not become a second business-logic layer.
  > The architecture goal is still inward dependency flow. Adapters should not become a second business-logic layer.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-dc62f92f780b404d` [rationale] (literature_supported) — The profile model is frozen so fields cannot be mutated after construction, guaranteeing cached profiles stay consistent with their source AMI run.
  > fields cannot be mutated after construction, which guarantees that cached profiles remain consistent with their source AMI run.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/forecastability_profile.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)
- `c-e280d4675236ff89` [mental_model] (literature_supported) — Entrypoints and adapters call the package facades or use cases.
  > Entrypoints and adapters call the package facades or use cases.
  (documentation, https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md, published None, independence ind-s-1ca6a2b8336de5f1, corroboration 1)

### Synthetic / rejected claims

- `c-0df8d684323a265f` [norm] (synthetic_extrapolation) — Machine-guidance files must be updated whenever the public API, import surface, or triage-first routing rules change.
  > Update these files whenever the public API, import surface, or triage-first routing rules change.
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md)
- `c-1c211f104336fdaa` [concept] (synthetic_extrapolation) — Supported covariant method names include cross_ami, cross_pami, te, gcmi, pcmci, and pcmci_ami.
  > Supported method names include: - `cross_ami` - `cross_pami` - `te` - `gcmi` - `pcmci` - `pcmci_ami`
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md)
- `c-2870c10cfe533d9b` [representation] (synthetic_extrapolation) — The F8 exogenous screening implementation, including CrossAMIResult and BH FDR, lives in extensions.py.
  > `extensions.py` source for `CrossAMIResult` and the BH FDR implementation
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/reference/diagnostics_matrix.md)
- `c-2ae69320778383b6` [concept] (synthetic_extrapolation) — In the benchmark, driver_nonlin_sq couples to target at lag 1 via a centered quadratic with coefficient 0.40.
  > `driver_nonlin_sq` couples to `target` at lag 1 via a centered quadratic
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md)
- `c-2fc11f98c4bbcb38` [check] (synthetic_extrapolation) — Golden-value snapshot regression tests (F9) ensure reproducibility across the new diagnostics.
  > golden-value snapshot tests ensure reproducibility across all new diagnostics
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md)
- `c-3949e70a533f8198` [strategy] (synthetic_extrapolation) — A non-uniform embedding can be used to estimate the probabilities in transfer entropy in order to reduce complexity.
  > or, in order to reduce complexity, using a non-uniform embedding.
  (verdict insufficient [adds_content], https://en.wikipedia.org/wiki/Transfer_entropy)
- `c-415240e5d4889ce3` [concept] (synthetic_extrapolation) — Machine-guidance files bias coding assistants and LLMs toward triage-first behavior and carry no runtime logic.
  > These files bias coding assistants and LLM consumers toward triage-first behavior on forecasting prompts. They carry no runtime logic - they are instruction surfaces only.
  (verdict insufficient [scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/surface_guide.md)
- `c-4dcc86b5bf49bce9` [concept] (synthetic_extrapolation) — The PydanticAI agent layer only narrates frozen deterministic payloads and does not perform statistical computation or validate numeric results.
  > The PydanticAI agent layer reads frozen deterministic payloads (A1-A3) and generates natural-language narration. It does not perform any statistical computation or validate the numeric results.
  (verdict insufficient [adds_content, connective_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/limitations.md)
- `c-734a31beb3f0f88b` [concept] (synthetic_extrapolation) — In v0.5.0, compute_transfer_entropy was removed in favour of compute_transfer_entropy_ksg and compute_predictive_information_gain.
  > `compute_transfer_entropy` has been removed in favour of > `compute_transfer_entropy_ksg` and `compute_predictive_information_gain`
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/medium/forecastability-triage-for-practitioners.md)
- `c-af11bc76e081e3ff` [concept] (synthetic_extrapolation) — v0.5.0 provides true Schreiber transfer entropy via compute_transfer_entropy_ksg.
  > true Schreiber transfer > entropy via `compute_transfer_entropy_ksg`
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/README.md)
- `c-cd28a008cafaaa4e` [norm] (synthetic_extrapolation) — PCMCI-AMI orchestration follows an inward-only dependency rule in which use cases depend on declared port contracts and adapters satisfy them without adapter-to-adapter helper coupling.
  > use cases depend on declared ports (protocol contracts), and adapters satisfy those contracts without adapter-to-adapter helper coupling
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/architecture.md)
- `c-d448911d043457fc` [mental_model] (synthetic_extrapolation) — The ports package provides protocol-oriented seams for the hexagonal architecture direction.
  > Protocol-oriented seams for the hexagonal architecture direction
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/code/module_map.md)
- `c-ef636edbd7c88c9e` [concept] (synthetic_extrapolation) — In the benchmark, driver_nonlin_abs couples to target at lag 1 via a centered absolute-value function with coefficient 0.35.
  > `driver_nonlin_abs` couples to `target` at lag 1 via a centered abs-value
  (verdict insufficient [adds_content], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/theory/foundations.md)
- `c-ff1c93a67a72e6f4` [representation] (synthetic_extrapolation) — Agent payload adapters provide structured Pydantic result models for deterministic consumption by agents, API consumers, or downstream pipelines.
  > structured Pydantic result models for deterministic consumption by agents, API consumers, or downstream pipelines
  (verdict insufficient [adds_content, scope_differs], https://github.com/AdamKrysztopa/dependence-forecastability/blob/904fa30c4148c98ee4be1221c461c86c8ca252e2/docs/explanation/results_summary.md)

### UNKNOWN / thin / unverified / unexamined slots

- concept: thin
- decision: thin
- cue: unknown
- check: thin
- failure_mode: thin
- norm: thin
- rationale: thin
- procedure_step: unknown

### Unknown placeholders

- `c-04b5549e0db967c9` [cue] — What observable features of a situation signal that Extending the toolkit with new estimators and tests applies or needs a different response?
- `c-80b70925cf82098a` [procedure_step] — What steps make up Extending the toolkit with new estimators and tests, and in what order?
