# D1 questions

Answer each question in plain prose, from memory, without the docs or the code open.
A few sentences is enough. "I don't know" or "this never comes up" is a fine answer.
Write your answers in `answers.md`, under the matching heading. Do not open `sealed/`.

## Q1

Sources say: "The same leakage boundary applies to exogenous screening (F8): CrossAMI must be computed on the training window only.". What would happen if someone did it differently, and in what situations, if any, is doing it differently acceptable?

## Q2

Sources say: "Use `known_future_drivers` only for variables whose contemporaneous future values are genuinely known at prediction time, such as calendar flags, planned promotions, or externally scheduled variables.". What would happen if someone did it differently, and in what situations, if any, is doing it differently acceptable?

## Q3

Sources prescribe: "A practitioner should target model evaluation exclusively at horizons in $\mathcal{H}_\varepsilon$ - lags outside this set carry no detectable predictive signal above the noise floor.". Think of the last time you did this. What result did you get, what had you expected, what did that result make you do next -- and what result would have sent you down a different path?

## Q4

Sources prescribe: "Routines that assume monotone decay (such as naive exponential smoothers) should inspect this flag before applying simplifying assumptions.". Think of the last time you did this. What result did you get, what had you expected, what did that result make you do next -- and what result would have sent you down a different path?

## Q5

"statistics and time series analysis) to normalize the autocovariance function to get a time-dependent Pearson correlation coefficient.". Describe a case where this did not hold, or where you decided against it. What about that case told you it was an exception?

## Q6

Sources prescribe: "To evaluate the order, one examines the plot to find the lag after which the partial autocorrelations are all within the confidence interval.". Think of the last time you did this. What result did you get, what had you expected, what did that result make you do next -- and what result would have sent you down a different path?

## Q7

Sources prescribe: "Overfitting in nonlinear backends sharp pAMI spikes at isolated lags only for tree backends backend fits noise in conditioning space compare against linear baseline and require ranking stability". Think of the last time you did this. What result did you get, what had you expected, what did that result make you do next -- and what result would have sent you down a different path?

## Q8

One source writes: "Quantitative forecasting models are appropriate to use when past numerical data is available and when it is reasonable to assume that some of the patterns in the data are expected to continue into the future.". Think of a recent case where you had to judge whether something was appropriate past. Describe one case that clearly was, one that clearly was not, and one that was hard to call. What differed between them, and what did you check first?

## Q9

Sources prescribe: "Numerical inflation `directness_ratio > 1.0` estimator instability, finite-sample effects Treat as warning;". Think of the last time you did this. What result did you get, what had you expected, what did that result make you do next -- and what result would have sent you down a different path?

## Q10

"It is generally considered good practice to indicate the degree of uncertainty attached to forecasts.". Describe a case where this did not hold, or where you decided against it. What about that case told you it was an exception?

## Q11

Sources say: "any lag where the derived profile exceeds the raw profile by more than estimation noise is a data-leakage candidate, not a genuine gain.". What would happen if someone did it differently, and in what situations, if any, is doing it differently acceptable?

## Q12

Sources say: "Use surrogates whenever sample size permits ($n \ge 200$, `n_surrogates >= 99`).". What would happen if someone did it differently, and in what situations, if any, is doing it differently acceptable?

## Q13

Sources say: "An absolute threshold risks including noise lags or excluding genuinely informative ones as signal strength varies across series.". What would happen if someone did it differently, and in what situations, if any, is doing it differently acceptable?

## Q14

"Use ../public_api.md when deciding whether a symbol is part of the supported import contract.". Think of the last time you made this choice. Which options did you consider, which did you take, and what about that situation decided it? When did you last choose differently?

## Q15

Sources say: "Any new selector that goes further (PMIME-style, PC-stable with driver autohistory) must be introduced under a **new method label** so that the shipped `cross_pami` and `xami_sparse` semantics are not silently extended.". What would happen if someone did it differently, and in what situations, if any, is doing it differently acceptable?
