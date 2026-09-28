# K0 codebook: first substantive error

**Status:** draft, registered with `prereg-early-k0.md` before the quiz. The three top-level codes are the registered K0 codes (`research/experiment-ai-assisted-cta-physics.md`, K0). The sub-codes nest inside them (`research/roadmap.md` M1). They never move a solution between top-level codes, so the K0 share is the same with or without them. The anchors below are final at registration. Any later anchor is a logged deviation, drawn from scripts outside the coding plan.

## Unit

One solution to one item, chosen by `probe-code k0-sample`, coded at its **first substantive error**: the earliest step that departs from a correct solution. There is one code per solution. Later errors are not coded.

- **Effort rule:** a solution with no step beyond restating the givens (no equation, and no diagram with quantities) is `BLANK`, including a bare number with no work, right or wrong. It is counted and reported, not placed in the denominator.
- **Stopped after stage 1:** a correct first stage followed by nothing is `OT`.
- **Correct solutions** are `CORRECT`. They are counted and reported, not placed in the denominator.
- **Coders code the Form 1 sheet only.** The component sheet is scored right or wrong separately and is never shown to a coder of Form 1.

## Decision rule for the boundary between PM and SR

Ask where the first error lives:
- **Inside one term of a correctly chosen and correctly bounded stage** (the expression for kinetic, potential or spring energy or for momentum, a dropped factor, g or a sign) or in the mathematics: code `PM`.
- **In the choice or connection of principles**: which law is used for a stage, how the process is split, which system or masses a stage covers, which states bound it, or what carries from one stage to the next: code `SR`. A wrong system or mass after sticking is `SR.representation` in either stage.

## Codes

| Code | Definition | Include | Exclude | Anchor (illustrative, K0-1) |
|---|---|---|---|---|
| **PM** — prerequisite or maths | The first error is inside one stage's physics or in the mathematics, with the stage's principle correctly chosen | See sub-codes | A wrong law for a stage (→ SR) | — |
| `PM.prereq` | A wrong expression for one term in a correctly chosen, correctly bounded stage | Kinetic energy as ½mv or mv²; spring energy as kx or ½kx; momentum as ½mv | A wrong law for the stage (→ `SR.criterion`); a wrong system or mass (→ `SR.representation`) | "(0.50)(8.0) = (2.0) v, v = 2.0 m/s; then ½(2.0)(2.0) = (2.0)(9.8) h" |
| `PM.math` | Correct setup, then an algebra, arithmetic, unit or sign slip | Dividing instead of multiplying; grams used as kilograms; a square root dropped | A setup error discovered through the algebra (code the setup) | "v = 4.0/2.0 = 2.0; h = 2.0 / 19.6 = 0.10 m" |
| **SR** — principle selection or representation | The first error is in which principle is used, how the process is split, or what carries between stages | See sub-codes | Errors inside a correctly chosen stage (→ PM) | — |
| `SR.decompose` | The process is treated as one event: one conservation equation from the initial to the final state | ½ m₁ v₁² = (m₁ + m₂) g h written directly; momentum from the snowball to the top of the hill | A split made at the wrong point (→ `SR.representation`) | "½ (0.50)(8.0)² = (2.0)(9.8) h, so h = 0.82 m" |
| `SR.criterion` | The process is split, but the wrong conservation law is used for a stage | Mechanical energy conserved across the sticking collision; momentum conserved during the rise or the compression | A belief stated in words (→ `SR.misconception`) | "Collision: ½(0.50)(8.0)² = ½(2.0)v², so v = 4.0 m/s; then h = …" |
| `SR.misconception` | The student states a belief that licenses the wrong choice | "Energy is always conserved"; "no energy is lost because the ice is frictionless" | An unstated wrong choice (→ `SR.criterion`) | "Energy is conserved because there's no friction, so ½mv² = mgh" |
| `SR.representation` | The wrong system, masses, bounding states or carry-over between stages | Momentum written with only one mass after sticking; the snowball's mass alone in the energy stage; a final state where the speed is not zero; the incoming speed carried into the energy stage | A wrong term inside a correctly bounded stage (→ `PM.prereq`) | "(0.50)(8.0) = (0.50) v, so v = 8.0 m/s" |
| **OT** — other | The first error is not a physics or maths step in the solution | Misreading a given (a wrong number copied); answering a different question; non-physical reasoning; illegible past the first step | — | "The sled weighs 1.5 N…" |
| `BLANK` | No step beyond restating the givens | — | — | — |
| `CORRECT` | Correct answer, with the reasoning shown | A correct answer with minor rounding | A bare correct number with no work (→ `BLANK`) | — |

## Coding sheet columns

`student_id, item_id, top, code, note`
- `top` is `PM`, `SR`, `OT`, `BLANK` or `CORRECT`.
- `code` is the full code, such as `SR.criterion`. `probe-code k0` refuses a row whose `top` does not match its `code`.

## Procedure

1. `probe-code k0-sample roster.csv --items K0-1,K0-2 --seed <registered seed> --out plan.csv` fixes the coding order and one item per student. The roster is every consenting student who sat Form 1.
2. The coders work down the plan until 100 errored solutions are coded, or the scripts run out; the stopping rule counts adjudicated errors. Neither coder is the instructional designer or the PI. Scripts carry only the pseudonymous `student_id`.
3. Each coder codes independently. Agreement is computed on the top level, over the solutions either coder calls errored: `probe-code k0-kappa coder_a.csv coder_b.csv`. The target is κ ≥ 0.70. Below it, the coders retrain on the disagreements and recode once; if κ is still below 0.70, it is reported and the adjudicated codes still decide.
4. Disagreements are adjudicated by discussion. The adjudicated file decides early K0: `probe-code k0 adjudicated.csv --plan plan.csv --early`. The pretest K0 omits `--early`, and fewer than 100 errored solutions is then an error, not a decision.
5. Form 2 scripts carry their own pseudonym key and are coded blind to Form 1. Coders never see LLM codes.
