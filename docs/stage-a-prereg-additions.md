# Stage A pre-registration: additions settled before the freeze

These items go into the Stage A pre-registration at `probe-app freeze`, alongside the registered design in `research/experiment-ai-assisted-cta-physics.md`. They add rules the design needs. They do not change K1 or any registered gate. **K1 is decided on the registered analysis alone; no analysis added here can pass or fail it.** Where an addition bears on a registered comparison, it is reported beside the registered result.

## 1. Guard calibration

Protocol, decision rule and report: `docs/guard-calibration.md`. The report is registered with the guard prompt hash.

## 2. Leading-content coding: who codes, and arm recognisability

- **Separate coders.** The leading-content coders (`probe-code export-leading`) are different people from the Stage A operation coders and the corroboration coder. The leading sheet shows each question's style next to what the expert said, so its coders could otherwise link experts and sets to arms, breaking the registered rule that operation coders are blind to interviewer.
- **The problem:** style can give the arm away. Human questions are spoken and messier; AI questions are written and polished. Each item carries an `arm_guess` column.
- **Measure:** the proportion of items whose arm the coders guessed correctly, with a Wilson 95% CI.
- **Rule:** if the CI excludes 0.5 on either side, the coders were partly unblinded. Guessing consistently wrong also reveals the arm.
  - The coder-based comparison of leading rates stays primary in both cases, labelled "partly unblinded" when the rule triggers.
- **guard-audit** is reported for the human arm only. Every AI question that was asked had already passed the same guard, so the AI arm's guard-audit rate is near zero by construction and cannot be compared with the human arm's.

## 3. Human-arm speech before the first marker

Speech recorded before the interviewer's first I/E marker in a human set cannot be given a speaker (`speaker = "unmarked"`, `probe_app/human.py`).

- **Not coded as either speaker:** it never appears on a coder sheet, and it takes no stem tick.
- **Still counted:** it stays in `key_leading.csv` and in the guard audit under source `unmarked`. `leading-rates` reports unmarked turns per arm, and per-set word counts go to `key_unmarked.csv`.
- **Console warning:** the console warns when a set has unmarked speech or no expert speech, and logs an `unmarked_speech` event.
- **Reporting:** for each session, the unmarked word count and any operation that appears only in unmarked speech are reported. K1(c) gets a sensitivity row that includes those operations. The AI arm has no matching loss, so this row shows whether the exclusion moves the human side.
- **Worst case for leading content:** every unmarked turn is also counted as a leading human question, and the result is reported as a bound.
- **Set exclusion *(project choice)*:** a human set whose unmarked speech exceeds 10% of its words is flagged, and its K1 contributions are reported with and without it. The registered analysis stays primary.

The human script tells the interviewer to press I before speaking.

## 4. Leading human questions and their answers

- **A leading human question stays in the data.** Unlike an AI question, it cannot be withheld before the expert hears it.
- **Definition:** "leading" here means the adjudicated label of the blind leading-content coders. `guard-audit` flags are reported beside it but do not define it.
- **The expert's answer to it** is kept in the transcript and coded as usual. Every human-arm result that feeds a comparison with the AI arm (the human side of K1(c), and the human probe-added operation count) is reported twice: with and without answers to leading questions. The registered analysis, with them included, stays primary. K1(b) counts AI-added operations only, so it is unaffected.
- **The AI arm is not treated symmetrically,** because its leading questions never reached the expert. The second analysis shows how much the human arm's results depend on questions the AI arm was not allowed to ask.
