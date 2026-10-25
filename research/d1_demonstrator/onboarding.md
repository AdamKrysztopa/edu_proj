# Onboarding notes for a new contributor to dependence-forecastability (D1 draft)

Made from the owner's answers to 15 questions (2026-10-25). Each paragraph carries its evidence
label: **observed human evidence** (the owner's own words) or **organisational-artefact-supported**
(the project docs). This is a draft from short answers, for the owner to accept, edit or reject.

## Leakage: the rule behind every rule

- *Organisational-artefact-supported.* Diagnostics, including CrossAMI in exogenous screening (F8),
  are computed on training windows only; scoring uses the post-origin holdout only.
- *Observed human evidence.* Anything else is a classical leak, information from the future going
  into the past, and it shows up as failures and disappointment in production. A derived profile
  above the raw profile is treated the same way. (Q1, Q11)

## Known future drivers

- *Organisational-artefact-supported.* `known_future_drivers` is only for values genuinely known at
  prediction time: calendar flags, planned promotions, scheduled variables.
- *Observed human evidence.* The common mistake is to put predicted values there. Their errors
  then accumulate into the forecast. (Q2)

## Reading a series: the order of checks

- *Observed human evidence.* Whether the past is a fit basis is seen from the numbers: ACF and PACF
  first, then AMI and pAMI, which show the linear and nonlinear, stacked and direct relationships.
  Look at which past values really matter, not at the stack of them. (Q6, Q8)
- *Observed human evidence.* AMI can look meaningful at many horizons while pAMI shows the real,
  shorter horizon. Trust pAMI for the horizon. (Q3)

## Where the owner's practice and the docs disagree — decide which is right

- **`directness_ratio > 1.0`.** The docs say "treat as warning" (estimator instability, finite-
  sample effects). The owner says above one means a bug, a defect. (Q9)
- **Non-monotone decay.** The docs say routines assuming monotone decay should check the flag,
  since non-monotone profiles can occur. The owner's reflex was to look for a mistake in the data.
  (Q4)
- **Isolated pAMI spikes in tree backends.** The docs read them as the backend fitting noise. The
  owner has seen such spikes when there were real dependences between past events and the current
  value: "I cannot explain it; you see it." (Q7)

## Smaller points

- *Observed human evidence.* A symbol joins the public API when tests and evals pass. (Q14)
- *Observed human evidence.* 3-sigma uncertainty bands often show absurd values that neither the
  model nor reality ever reaches. The cause is not known yet; treat wide bands with suspicion. (Q10)
- *Observed human evidence.* Skipping surrogates, or using them on short series, raises the risk of
  misidentifying lags. A single absolute threshold across series is "like using soccer rules in
  chess". (Q12, Q13)

## Candidate doc additions (both judges: new)

Q2 (predicted values in `known_future_drivers` accumulate error), Q3 (AMI vs pAMI horizon), Q7
(isolated spikes can be real), Q8 (the order of checks), Q9 (ratio above one is a bug), Q10 (absurd
3-sigma bands), Q14 (public API rule). The three disagreements above need the owner's decision
before any of them goes into the docs.
