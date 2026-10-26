# G2 fixture review (Stop A0)

For each topic, check four things and reply with only the exceptions (e.g. `t04 P no`, `t10 N no`, `t13 seed no`):
- **seed**: the seed sentence does *not* already answer the lens question;
- **P**: P *does* answer it (states the reason / exception / expected result / choice condition);
- **N**: N does *not* answer it (an on-topic fact, but no reason, exception, result or condition);
- **N+**: none of the extra sentences answers it.

These 24 topics are D1's own questions or topics excluded from the rerun, so reading them does not spoil the rerun. ⚑ marks a sentence the fixture writer was unsure about.

## t01 · WHY

**Lens question:** Does any sentence state why this is done (the reason or the failure it prevents), other than 'the law/regulation requires it'?

**Seed:** The same leakage boundary for rolling-origin evaluation applies to exogenous screening (F8), where CrossAMI must be computed on the training window only.

**P**: CrossAMI is computed on the training window only because scores taken over the full series let test-window values leak into exogenous screening.

**N**: CrossAMI for exogenous screening (F8) is computed on the training window only, and the leakage boundary is the train_end argument since version 0.3.

**N+ 1:** Exogenous screening is step F8 in the rolling-origin evaluation guide.
**N+ 2:** The CrossAMI score for each driver is listed in the screening table.

## t02 · WHY

**Lens question:** Does any sentence state why this is done (the reason or the failure it prevents), other than 'the law/regulation requires it'?

**Seed:** known_future_drivers should be used only for variables whose contemporaneous future values are genuinely known at prediction time, such as calendar flags or planned promotions.

**P**: Passing a variable whose future values are not known at prediction time into known_future_drivers gives the model information it will not have in production.

**N**: known_future_drivers takes a list of variable names, then stores the future values known at prediction time, such as calendar flags, in the forecasting config object.

**N+ 1:** Calendar flags and planned promotions are the two examples given in the drivers guide.
**N+ 2:** The known_future_drivers argument was added to the forecasting config in release 0.4.

## t03 · RESULT

**Lens question:** Does any sentence state what result of this test to expect and what a given result means or which next action it leads to?

**Seed:** Model evaluation should be targeted exclusively at horizons in the informative horizon set because lags outside it carry no detectable predictive signal above the noise floor.

**P**: If the informative horizon set comes back empty, no lag carries signal above the noise floor and model evaluation stops rather than targeting any horizon.

**N**: Model evaluation targets the horizons in the informative horizon set of the result object, and the signal above the noise floor that each lag carries is kept as a float.

**N+ 1:** Model evaluation in the tutorial uses the horizons listed in the informative horizon set.
**N+ 2:** The noise floor is drawn as a grey line in the horizon plot.

## t04 · RESULT

**Lens question:** Does any sentence state what result of this test to expect and what a given result means or which next action it leads to?

**Seed:** The is_non_monotone flag should be inspected before applying simplifying assumptions that assume monotone decay.

**P** ⚑: A True is_non_monotone flag marks a profile with a later secondary peak, and the next action is to drop the monotone decay assumption and keep each lag.

**N**: The is_non_monotone flag is a boolean field on the profile result, added in release 0.4 next to the monotone decay assumption column and the next_action field.

**N+ 1:** Monotone decay is the shape most AMI profiles take in the worked examples.
**N+ 2:** The is_non_monotone flag sits next to the peak_lag field in the profile result.

## t05 · HEDGE

**Lens question:** Does any sentence state the specific cases in which the rule does NOT hold (an exception condition that is not merely a restatement of the rule or a cross-reference)?

**Seed:** In statistics and time series analysis, the autocovariance is commonly normalized to a Pearson correlation coefficient, while in engineering the normalization is usually dropped.

**P**: The engineering convention of dropping the normalization does not apply when the autocovariance feeds a significance test, which needs the Pearson correlation scale.

**N**: The autocovariance normalized to a Pearson correlation coefficient is what the acf helper returns, and the engineering variant without normalization was added 3 months later.

**N+ 1:** Time series analysis texts use the normalized form throughout their examples.
**N+ 2:** The engineering variant of the autocovariance is exposed as acovf in the stats module.

## t06 · RESULT

**Lens question:** Does any sentence state what result of this test to expect and what a given result means or which next action it leads to?

**Seed:** To evaluate the AR model order, one should examine the plot to find the lag after which the partial autocorrelations are all within the confidence interval, and this lag is determined to likely be the AR model's order.

**P**: A plot whose partial autocorrelations all fall inside the confidence interval after lag 3 gives an AR model order of 3, and the next step is to fit an AR(3) model.

**N**: The partial autocorrelation plot is drawn by plot_pacf, then saved to the figures folder with the confidence interval shaded and each lag of the AR model order in the next panel.

**N+ 1:** The AR model order section of the guide follows the autocorrelation section.
**N+ 2:** The confidence interval on the plot uses the Bartlett formula from the stats module.

## t07 · RESULT

**Lens question:** Does any sentence state what result of this test to expect and what a given result means or which next action it leads to?

**Seed:** Numerical inflation should be treated as a warning and verified with multiple backends and sample-size stress testing.

**P**: If a high score persists across multiple backends and sample-size stress testing, the warning is cleared; if it collapses, the inflation was numerical and the result is discarded.

**N**: Numerical inflation is reported as a warning in the result object, and the multiple backends for sample-size stress testing are named in the backends parameter of the run config file.

**N+ 1:** The stress testing module lives under the diagnostics package.
**N+ 2:** Numerical inflation warnings carry the code NUM_INFLATION in the result object.

## t08 · HEDGE

**Lens question:** Does any sentence state the specific cases in which the rule does NOT hold (an exception condition that is not merely a restatement of the rule or a cross-reference)?

**Seed:** It is generally considered good practice to indicate the degree of uncertainty attached to forecasts.

**P**: The practice of attaching uncertainty does not hold for deterministic schedule values like fixed calendar holidays, which carry no forecast error at all.

**N** ⚑: The interval_width column holds the uncertainty attached to each forecast under this practice, and the plotting helper draws it as a degree band around the line.

**N+ 1:** Forecasts in the tutorial notebooks carry an interval_width column next to the point value.
**N+ 2:** The good practice note on uncertainty appears in the forecasting guide.

## t09 · WHY

**Lens question:** Does any sentence state why this is done (the reason or the failure it prevents), other than 'the law/regulation requires it'?

**Seed:** Any lag where a derived-feature profile exceeds the raw profile by more than estimation noise should be treated as a data-leakage candidate, not a genuine gain.

**P** ⚑: Such lags are treated as leakage candidates because a derived feature built from the raw series cannot hold more information about the target than the raw profile.

**N**: The derived-feature profile is computed first, then the raw profile, and each lag of both profiles is stored in the data-leakage candidate table with its estimation noise.

**N+ 1:** The derived-feature profile uses the same AMI estimator as the raw profile.
**N+ 2:** The data-leakage candidate table is written to the reports folder.

## t10 · WHY

**Lens question:** Does any sentence state why this is done (the reason or the failure it prevents), other than 'the law/regulation requires it'?

**Seed:** Surrogates should be used whenever sample size permits, specifically when n is at least 200 and n_surrogates is at least 99.

**P**: Surrogates give a series-specific noise floor, and without that floor a high AMI value at some lag cannot be told apart from chance dependence.

**N** ⚑: Surrogates are drawn by the surrogate module, with sample size n and n_surrogates set at 200 and 99 by default since version 0.2 of the package.

**N+ 1:** The surrogate module supports phase-randomised and block-shuffled surrogates.
**N+ 2:** The n_surrogates parameter is part of the diagnostics config.

## t11 · WHY

**Lens question:** Does any sentence state why this is done (the reason or the failure it prevents), other than 'the law/regulation requires it'?

**Seed:** Epsilon should be defined relative to the surrogate upper band rather than as a global absolute constant, because an absolute threshold risks including noise lags or excluding informative ones as signal strength varies across series.

**P**: Epsilon is tied to the surrogate upper band so that the threshold scales with each series' own noise level instead of admitting noise lags in weak series.

**N**: Epsilon is stored as a fraction of the surrogate upper band in epsilon_rel, and the global absolute threshold for noise lags in each series is named epsilon_abs.

**N+ 1:** The surrogate upper band is computed per lag from the surrogate draws.
**N+ 2:** Epsilon appears in the horizon selection section of the guide.

## t12 · SEL

**Lens question:** Does any sentence state a condition that says which option to choose in which situation?

**Seed:** Contributors should consult public_api.md when deciding whether a symbol is part of the supported import contract.

**P**: A symbol listed in public_api.md is part of the supported import contract and may be imported directly; any symbol absent from that list is internal and avoided.

**N**: The public_api.md file lists each symbol that is part of the supported import contract and sits in the docs/reference folder, next to the changelog for release 0.4.

**N+ 1:** Contributors edit public_api.md in the same pull request that adds a symbol.
**N+ 2:** The supported import contract covers the top-level package namespace.

## t13 · WHY

**Lens question:** Does any sentence state why this is done (the reason or the failure it prevents), other than 'the law/regulation requires it'?

**Seed:** Any new selector that goes further than xami_sparse, such as PMIME-style or PC-stable with driver autohistory, must be introduced under a new method label so that shipped cross_pami and xami_sparse semantics are not silently extended.

**P**: A new method label keeps earlier runs reproducible, since users who pinned cross_pami or xami_sparse would otherwise get different lags from the same call.

**N**: New selectors such as PMIME-style or PC-stable are listed under the method label column, then documented next to the shipped cross_pami and xami_sparse in the table.

**N+ 1:** The xami_sparse selector was shipped in release 0.5.
**N+ 2:** The method label for cross_pami is printed in every selection result.

## t14 · HEDGE

**Lens question:** Does any sentence state the specific cases in which the rule does NOT hold (an exception condition that is not merely a restatement of the rule or a cross-reference)?

**Seed:** It is generally considered a good practice to indicate the degree of uncertainty attaching to forecasts.

**P**: The practice does not hold for a point forecast fed straight into an automated order rule, where the downstream system accepts a single number and ignores any interval.

**N**: The degree of uncertainty attaching to forecasts is stored as a 90% interval by default, in the interval column of the forecast frame returned by the point forecast call.

**N+ 1:** Forecasts are returned as a frame with point and interval columns.
**N+ 2:** The good practice note on uncertainty cites the forecasting textbook.

## t15 · HEDGE

**Lens question:** Does any sentence state the specific cases in which the rule does NOT hold (an exception condition that is not merely a restatement of the rule or a cross-reference)?

**Seed:** In other disciplines like engineering, the normalization is usually dropped and the terms autocorrelation and autocovariance are used interchangeably.

**P**: The terms are not interchangeable in engineering code when a function returns values bounded by one, since those are normalized autocorrelations.

**N**: The normalization in engineering code is set by the normalize argument of the autocorrelation function, and autocovariance is its unnormalized output.

**N+ 1:** Engineering texts use the term autocorrelation for the unnormalized sum.
**N+ 2:** The autocovariance function lives in the stats module.

## t16 · RESULT

**Lens question:** Does any sentence state what result of this test to expect and what a given result means or which next action it leads to?

**Seed:** In rolling-origin evaluation, diagnostics should be computed on train windows only.

**P** ⚑: Train-window diagnostics in rolling-origin evaluation give fold scores that move gradually, and a sharp jump at one fold marks leakage that the next step traces.

**N**: Rolling-origin evaluation stores the diagnostics computed on train windows in the fold_diagnostics table, one row per fold, keyed by origin date and window size.

**N+ 1:** Train windows in rolling-origin evaluation grow by one step per fold.
**N+ 2:** The fold_diagnostics table is part of the evaluation result.

## t17 · HEDGE

**Lens question:** Does any sentence state the specific cases in which the rule does NOT hold (an exception condition that is not merely a restatement of the rule or a cross-reference)?

**Seed:** For surrogate bands, the upper band is operationally informative for detecting non-null dependence while the lower band is usually near zero for MI and is not typically operationally useful.

**P**: The lower band stops being useless when a backend's bias pushes MI estimates below zero, since the lower band then shows how far the bias reaches.

**N**: The upper band and the lower band for MI are returned as band_upper and band_lower, then drawn as dashed lines in the surrogate bands plot of the report.

**N+ 1:** Surrogate bands are computed from the same draws for every lag.
**N+ 2:** The upper band appears in the profile plot as a dashed line.

## t18 · RESULT

**Lens question:** Does any sentence state what result of this test to expect and what a given result means or which next action it leads to?

**Seed:** The robustness study pipeline should be used to compare all configured backends against linear_residual.

**P**: Backends whose lag ranks agree with linear_residual across the robustness study pipeline are kept, and a backend that reorders the top lags is dropped from the set.

**N**: The robustness study pipeline writes its comparison of all configured backends against linear_residual to robustness.csv, then prints a summary table of the backends.

**N+ 1:** The linear_residual backend is the reference estimator in the robustness study.
**N+ 2:** Configured backends are listed in the backends section of the config file.

## t19 · SEL

**Lens question:** Does any sentence state a condition that says which option to choose in which situation?

**Seed:** Contributors should consult architecture.md when deciding where new logic should live.

**P**: If new logic computes a diagnostic it belongs in the core package, and if it only formats or plots results it goes in the reporting layer described in architecture.md.

**N**: The architecture.md file describes where new logic lives across the core package and the reporting layer, and it sits in the docs/explanation folder of the repository.

**N+ 1:** Contributors open architecture.md from the contributing guide.
**N+ 2:** The core package and the reporting layer are separate subpackages for new logic.

## t20 · WHY

**Lens question:** Does any sentence state why this is done (the reason or the failure it prevents), other than 'the law/regulation requires it'?

**Seed:** At least 99 surrogates are required for a valid two-sided 95% band, and fewer must not be used as a significance threshold.

**P**: With 99 surrogates the 2.5th and 97.5th percentiles fall on actual draws, and with fewer the band edges are interpolated guesses that misstate significance.

**N** ⚑: The two-sided band uses 99 surrogates by default through the n_surrogates parameter, the significance threshold is the band_upper field, and fewer draws are refused.

**N+ 1:** The surrogates for the band are drawn by the surrogate module.
**N+ 2:** The significance threshold appears as a dashed line in the profile plot.

## t21 · SEL

**Lens question:** Does any sentence state a condition that says which option to choose in which situation?

**Seed:** Selection of a forecasting method should be based on objectives and conditions such as available data.

**P**: When fewer than two seasonal cycles of data are available, choose a seasonal naive method; with long histories and known drivers, choose a regression-based method.

**N**: The forecasting method is selected through the method argument, and the objectives and available data are logged since release 0.3 in the run metadata file of each run.

**N+ 1:** Selection of a forecasting method is covered in chapter three of the guide.
**N+ 2:** Available data are summarised in the run metadata before fitting.

## t22 · SEL

**Lens question:** Does any sentence state a condition that says which option to choose in which situation?

**Seed:** The forecastability profile (F1) should be run after AMI curves exist and before choosing which horizons to model.

**P**: Horizons whose AMI sits above the surrogate band in the forecastability profile (F1) are chosen for modelling, and horizons below the band are left out.

**N**: The forecastability profile (F1) is produced by run_profile(), then saved next to the AMI curves as profile.json, with horizons and bands stored per lag.

**N+ 1:** AMI curves are computed by the ami module for every lag.
**N+ 2:** The forecastability profile (F1) is the first step of the workflow guide.

## t23 · WHY

**Lens question:** Does any sentence state why this is done (the reason or the failure it prevents), other than 'the law/regulation requires it'?

**Seed:** F3 should be used when one suspects that longer lags add noise rather than signal, as the curve never plateauing is also informative.

**P**: F3 is run on such series because added lags that carry noise rather than signal make the curve keep rising, and that pattern is invisible in single-lag AMI.

**N**: F3 is the cumulative lag curve in the diagnostics module, and its plot of longer lags against noise and signal for each series is saved in the f3_curve folder.

**N+ 1:** The F3 curve is drawn next to the AMI profile in the report.
**N+ 2:** Longer lags are capped by the max_lag parameter of F3.

## t24 · WHY

**Lens question:** Does any sentence state why this is done (the reason or the failure it prevents), other than 'the law/regulation requires it'?

**Seed:** run_rolling_origin_evaluation() enforces the leakage boundary internally, but diagnostics computed manually outside it require the user to enforce the same boundary to avoid look-ahead leakage.

**P** ⚑: Diagnostics computed on the full series use values from after the forecast origin, which makes every fold score look better than any live forecast could be.

**N**: run_rolling_origin_evaluation() takes the forecast origin through its origin argument, and diagnostics computed manually take the same boundary as a cutoff index.

**N+ 1:** The leakage boundary is described in the rolling-origin evaluation guide.
**N+ 2:** Diagnostics computed manually are written to the user's own output folder.
