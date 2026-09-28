# Pre-registration draft: early K0 (roadmap M1)

**Status:** draft for the user to complete and register (e.g. on OSF) **before the quiz is given**. Fields marked *to confirm* need a decision or a fact only the user has. Thresholds marked *(project choice)* are judgments, not values from a source; each has a recommended value.

## Question

In a first-year mechanics course, after the lectures on energy and momentum conservation, are at least 30% of students' first errors on two-stage conservation problems principle selection or representation errors, as opposed to prerequisite or maths errors or other errors?

This is the Phase 1 kill criterion applied to one topic (map §9). The rule is registered in `research/experiment-ai-assisted-cta-physics.md` (early K0) and used unchanged. The component items, the second form and LLM coding are additions from `research/roadmap.md` M1. They are secondary and cannot change the K0 decision.

## Materials

- Items: `instrument/k0/items.md`. The registered items are Form 1: K0-1 and K0-2. The components are C1a, C1b, C2a and C2b. Form 2 is K0-1b and K0-2b.
- Codebook: `instrument/k0/codebook-k0.md`. Its anchors are final at registration; any later anchor is a logged deviation, drawn from scripts outside the coding plan.
- Decision code: `probe-code k0`, `k0-sample` and `form-agreement` (`instrument/src/probe_code/k0.py`, with tests), at commit *to record at registration*.

## Participants and timing

- **Course offering:** *to confirm*. It is a different offering from both the feasibility run (M5) and Stage B (M6).
- **Timing:** Form 1 runs after the course's lectures and problem sets on energy and momentum conservation, at the same point relative to the lectures as the future Stage B pretest, and is collected. Form 2 runs 6–8 days later, with no teaching of the topic in between *(to confirm with the instructor)*, and is collected. The component sheet is handed out after Form 2 is collected, so it cannot teach the split between the forms.
- **Pseudonyms:** Form 1 and Form 2 scripts carry separate pseudonym keys, so coders of Form 2 cannot link a script to its Form 1 codes. The instructor holds both keys and merges them only for the agreement analysis.
- **Credit:** completion credit where the course allows it *(to confirm)*.
- **Consent:** under the course's research consent *(ethics approval to confirm)*. Non-consenters' scripts are not kept.
- **Leakage:** scripts are collected; no item-specific solutions are released. Feedback covers the topic only.

## Sampling and unit

- The roster is every consenting student who sat Form 1. The sampling seed is fixed at registration: *to record*. `probe-code k0-sample` sorts the roster, orders it at random from the seed, and picks one Form 1 item per student.
- `probe-code k0 --plan` refuses coded rows that skip a plan position or code a different item from the one drawn, and it ignores any solution coded after the 100th errored one.
- Coding proceeds in plan order until 100 solutions containing an error are coded.
- The unit is the first substantive error; one code per solution. Blank and correct solutions are counted and reported but are not in the denominator.

## Coding

- Two coders, neither of them the instructional designer or the PI: *to name*.
- Agreement on the top-level code, over the solutions either coder calls errored (`probe-code k0-kappa`): κ ≥ 0.70. Below that, the coders retrain and recode once. If κ is still below 0.70, it is reported, and K0 is still decided on the adjudicated codes, as registered.
- K0 is decided on the adjudicated codes.
- Human coders never see LLM codes.

## Primary decision (registered rule, unchanged)

- **Stop before recruiting the 12 Stage A experts** if fewer than 30% of errored solutions are principle selection or representation (`SR`). This is judged on the point estimate and reported with its Wilson 95% CI.
- **Inconclusive** if fewer than 100 errored solutions are reached. Stage A then proceeds on the literature premise, and the pretest K0 alone decides Stage B.
- The full error profile is reported next to the decision, including sub-codes, blank and correct counts, and attempt and attendance rates.

## Registered early-K0 rules (copied unchanged from the experiment design)

- **Leakage.** Scripts are collected and no item-specific solutions are released; feedback is given on the topic only. Stage B records whether each student sat early K0; those students are left out of the pretest K0 sample and flagged in the covariate analysis.
- **Decision.** **Stop before recruiting the 12 experts** if fewer than 30% of errors are principle selection or representation. Early K0 can stop the study only if it reaches 100 errored solutions; with fewer it is reported as inconclusive and Stage A proceeds on the literature premise. A new topic needs its own early K0 on its own items before experts are recruited. A pass does not replace K0: the pretest check runs on the analysed cohort and alone decides Stage B. If the two checks fall on opposite sides of 30%, both are reported with their Wilson CIs and attempt rates, and the difference is discussed as a cohort or effort effect.
- **Use in Stage B.** Early-K0 codes may choose the four worked-example problems and which steps carry prompts, applied identically to both arms. They do not add, drop or rank operations: the treatment carries every operation that passed K1. The mapping from operations to early-K0 error codes is registered with the Stage B freeze; the report of which K0 error codes each operation addresses uses the pretest codes and is checked against that mapping.

## Secondary analyses (roadmap additions)

**No secondary result qualifies or overturns the stop/continue decision.**

1. **Components.** Among errored students, the share who passed both components of their coded item (K0-1: C1a and C1b; K0-2: C2a and C2b), and the `SR` share among them. Missing component sheets are reported.
   - Rule *(project choice)*: if fewer than half of errored students pass both components of their item, record that prerequisites weigh heavily on this topic. This is a planning note for the module, not a decision. Any prerequisite material used in Stage B goes to both arms identically.
   - Recommended: 50%. A higher value would call prerequisites dominant more readily.
2. **Form agreement.** Cohen's κ on the top-level code, among students who err on both paired items (K0-1 with K0-1b, K0-2 with K0-2b; the code refuses other pairings), computed with `probe-code form-agreement`.
   - Minimum n *(project choice)*: 60. Below it, the result is inconclusive.
   - Threshold *(project choice)*: κ ≥ 0.60 on the point estimate, reported with a bootstrap 95% CI, before any test of per-student routing. Recommended because it sits below the between-coder target of 0.70, which bounds how stable a single student's code can look.
   - Form 2 is coded under its own pseudonym key, blind to Form 1 codes.
3. **LLM-assisted coding (optional).** An LLM codes the same solutions independently, after the human codes are adjudicated. Its κ against the adjudicated codes is reported, with a target of κ ≥ 0.70 *(project choice)*. LLM codes never enter the K0 decision and are never shown to the human coders.

## Deviations

Any change to an item, code, anchor rule or sampling rule after registration is logged with its date and reason. Early K0 is not recoded under a later change. The Stage B pre-registration cites this record unchanged.

## Data

Scripts are scanned and stored under pseudonymous IDs. The key file linking IDs to names is held by the instructor, not the coders. Retention and storage follow the ethics approval *(to confirm)*.
