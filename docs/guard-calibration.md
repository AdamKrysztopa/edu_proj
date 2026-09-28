# Guard calibration protocol (before `probe-app freeze`)

**Why:** the guard is the only semantic check that an AI question does not lead the expert. The tests drive it with scripted verdicts, and `guard-audit` reports how often it flags, never whether a flag was right. Decision 0004 (`guard-calibrated-before-freeze`) therefore requires, before the freeze:
- about 60 labelled probe questions and two labellers, with their κ;
- the guard's sensitivity and specificity with 95% CIs, pre-registered with the guard prompt;
- a repeat of the calibration after any change to the guard's model or prompt.

## Items (`instrument/calibration/items.csv`)

60 items, each a question with the context the live guard would have: the problem statements and everything the expert had said by then.

- **30 unaltered candidates** from the simulated sessions' 172 generated questions:
  - all 9 that the guard rejected live;
  - 21 of the accepted ones, sampled uniformly (seed 20260929).
  The rejected candidates are the only naturally leading questions the frame is likely to hold. A uniform draw would give one or two, and questions the guard had already accepted can never be false alarms.
- **30 leading variants.** Other sampled contexts (seed 20260928) have their question rewritten to introduce content absent from the expert's words and the problems:
  - 15 explicit ones name a principle, quantity or check outright;
  - 15 subtle ones only imply it.
  The author worked from contexts with the guard's verdicts hidden.
- The origin is kept in the file, but never on the labelling sheet. IDs are assigned in a random order (seed 607), so an ID says nothing about origin.

Human labels, not the construction, decide which items count as leading.

## Labelling

- **Two labellers,** neither the item author, nor the PI, nor anyone who will code operations or leading content in Stage A. They apply the rule in `instrument/human-script.md`, which is word for word the guard's definition. For each item they record:
  - `leading` (1 or 0) and `introduced`;
  - `origin_guess` (`authored` or `generated`), so that recognisable rewrites show up as a measured risk.
- **Blind** to the item's origin and to the guard's verdict. The sheet comes from `probe-code guard-calibration-sheet items.csv --seed <registered> --out sheet.csv`.
- **Adjudication:** `adjudicated.csv` holds a final label for all 60 items (the code refuses fewer), agreed items included.

## Guard run and report

1. `probe-code guard-calibrate items.csv --out verdicts.csv` runs the current guard and logs every call.
2. `probe-code calibration-report items.csv labeller_a.csv labeller_b.csv adjudicated.csv verdicts.csv` gives:
   - the class sizes;
   - sensitivity per stratum (natural, explicit, subtle);
   - the decision sensitivity over natural and subtle items only, since explicit rewrites are the easiest case;
   - specificity;
   - Wilson 95% CIs throughout;
   - labeller κ and the accuracy of their origin guesses.
3. The report, the guard prompt hash (`probe-app hashes`) and the item file are registered together.

## Decision rule *(project choice; registered before the guard is run)*

Judged on point estimates, with CIs reported:

- **Too few items:** fewer than 25 leading or 25 non-leading items after adjudication means the set is insufficient. Author more items and relabel before any judgment.
- **Labeller κ below 0.60:** the definition is unclear to humans. Revise the wording (the human script follows it word for word), then label a fresh set of items.
- **Accept** when the decision sensitivity (natural and subtle items) is at least 0.80 and specificity is at least 0.80.
- **Otherwise:** revise the guard prompt and recalibrate on fresh items. At most two revise-and-recalibrate rounds. If the guard still fails, stop: the AI arm is not frozen, and the choice between a different guard model and dropping the AI-probe condition goes to the user.
- **Origin guessed well above chance** (the lower 95% bound of accuracy above 0.5): the authored items are recognisable. The stratified sensitivities are then reported with that caveat, and the natural stratum carries the most weight in the interpretation.

Why 0.80: below it, about one leading question in five would reach the expert, or one neutral question in five would be replaced by a bare stem. About 60 items cannot resolve anything finer. A larger set would let the thresholds rise.

## After the pilots

The guard is run over the pilot's human-arm questions and compared with the blind coders' adjudicated labels on the same questions. That tests it on transcribed human speech, which the calibration items do not contain. If sensitivity or specificity there falls below 0.70 *(project choice)*, the guard is recalibrated with human-speech items before the freeze.
