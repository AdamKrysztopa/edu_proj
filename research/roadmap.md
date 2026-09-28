# Route and implementation roadmap (roadmap steps 3–6)

**Status:** the planning deliverable. The route is chosen from the evidence available on 2026-09-28 ([`route-comparison.md`](route-comparison.md), [`decision-gaps.md`](decision-gaps.md)). Its effectiveness is untested; every assumption below names the milestone that tests it and what changes if it fails.

**The route in one paragraph.** Student errors locate the bottleneck. Trace-based expert elicitation recovers the operations behind it. Those operations are taught through a static module of worked examples, self-explanation prompts and pre-authored feedback keyed to error categories. Learning is judged on unassisted, delayed transfer. LLMs work behind the scenes: as the interviewer under test, drafting materials and assisting coding. They do not face learners. Diagnosis stays at cohort level and adaptation waits for evidence.

## Step 3 — the selected approach

### Expert elicitation

- **Use Cognitive Task Analysis:** non-directed think-aloud while the expert solves, then retrospective probes over the recorded trace. An operation counts only if the trace corroborates it and at least 3 of the 12 experts share it. Expert–novice research and the published problem-solving frameworks (Heller & Reif 1984; Docktor et al. 2015) supply the coding frame and the "already published" tag.
- **Combine with Decoding the Disciplines as the frame:** bottleneck from student data → operation → model → practice → assess.
- **AI role, conditional:** AI-led probes are tested in Stage A, and K1 decides (gap 2). A pilot removes the AI arm only on the stated safety failure (M2).
- **Defer** the decoding interview (a Phase 2 comparison arm only) and capture beyond the tablet (gaze, screen).
- **Reject** Threshold Concepts as an operational construct: there are no reliability data for identifying one. The word may name a candidate bottleneck; it adds no step.

### Learner diagnosis

- **Use coded first errors on open-response problems at cohort level.** Codes combine the Docktor et al. (2016) rubric categories with the taxonomy in step 4. Each multi-principle item is paired with its single-principle components, which separates a missing prerequisite from a selection bottleneck (White et al. 2015).
- **The difficulty layer** (formerly the PCK layer) is seeded from these codes, not from expert or teacher prediction. Teachers review it.
- **An LLM may assist coding.** A 5-run majority vote with human review of the highest-variation responses matched human graders, but only for binary rubric grading of written explanations (Chen & Wan 2025). Two human coders remain the reference.
- **EMCS** (without Q16, Q22, Q23) is used for cohort evaluation only.
- **Defer** per-student routing until labels prove stable across forms (gap 3), the AI diagnostic dialogue (a Phase 3 comparison) and cognitive diagnostic models.
- **Reject** individual diagnosis from single inventory items.

### Instruction

- **Use worked examples in which each operation is performed in a worked step,** carried by a self-explanation prompt that asks the student to justify or apply it. The student's answer is locked before the model answer appears. Completion problems follow; the mastery rule, not a fixed schedule, moves the student to full problems.
- **Feedback** comes after an attempt and explains why, keyed to the coded error category. It is pre-authored: LLM-drafted, then checked by a physicist. Answers are withheld until the attempt.
- **Misconception-coded errors** (for example "energy is always conserved") get a predict-then-commit discriminating case followed by a refutation.
- **Default order:** worked example first, for novices on multi-principle problems. This default qualifies map §5.7. The nearest university evidence favoured problem solving first for low-prior-knowledge students (He et al. 2025), so order stays an untested assumption in the first version (A8), and a powered order experiment follows M6.
- **Cognitive Apprenticeship** is vocabulary for this sequence. Fixed-schedule fading is not relied on.

### Delivery

- **The ITS separation, made concrete in data:**
  - a domain model: problems, solution steps, operations and error categories;
  - a learner record: responses and mastery-rule state;
  - a policy: a fixed sequence plus the mastery rule.
- **Static.** No live LLM faces learners in the first version (gap 4). In the Stage B comparison, the sequence is fixed and the mastery rule is off, so the amount of practice does not differ by arm. Principle choice per segment and numeric results are structured steps. The module checks them against the solution model, so step-level feedback needs no generation.
- **Defer** live LLM tutoring. It enters later as a randomized arm, compared against the same design delivered statically (map §9 Phase 5).

### Evaluation and adaptation

- **Outcomes:** unassisted transfer at the registered delay of 2–3 weeks, on items not written around the module's own problems, scored for correctness, with first errors coded. Also EMCS at cohort level, time on task and usage. Never measure while help is available.
- **Learner model:** a simple rule, three correct principle choices in a row on different surfaces. Every response is logged. Knowledge tracing is deferred to an offline check on the logs (gap 5); per-learner adaptation waits for Phase 5.

### First case and generalization

The first case is selecting and combining conservation principles in first-year mechanics. The stages are the same in any domain: find the bottleneck, elicit, code, author, deliver, assess. The content of each stage is domain-specific: problems, error categories and operations. A second topic is the generalization test (roadmap step 18).

## Step 4 — a worked physics case (hypothetical)

*Everything in this section is illustrative. No data have been collected; the quoted expert remark and the student patterns are invented to show the workflow.*

### Candidate hidden-knowledge categories

The diagnosis must first rule out three ordinary explanations. Each has its own evidence:

- **Missing prerequisite:** the single-principle component item also fails. The response is to teach the component first.
- **Misconception:** a conceptual item shows a contrary belief, for example that kinetic energy is conserved when blocks stick. The response is a discriminating case and a refutation.
- **Practice or execution:** principles and setup are correct but the algebra or arithmetic fails. The response is more practice, with no new content.

A first error is a **candidate hidden operation** when the student passes the components but fails the synthesis. Map §9 names the kinds:
- an omitted prerequisite step the expert no longer states;
- a perceptual cue (for example: "stick together" signals a perfectly inelastic collision);
- a representation choice (for example: draw states 1–2–3 before writing any equation);
- a decomposition strategy (split the motion at brief, large internal forces);
- a decision criterion (for example: momentum holds if the net external impulse is negligible over the interval);
- a conceptual model;
- an error-checking routine (for example: the final kinetic energy must not exceed the initial);
- a metacognitive judgment;
- a disciplinary norm.

### The case

1. **Bottleneck.** On the K0 items, the most frequent first error is "applies mechanical-energy conservation across the collision". Students who make it pass both component items: a pure collision and a pure ramp. Whether first-year students fail to split sequential problems is exactly what K0 checks: in interviews, all 13 second-year physics majors split sequential two-concept problems into events, while 3 of 4 treated a complex simultaneous problem as one event (Ibrahim et al. 2017).
2. **Expert operation.** Every expert marks states before writing any equation, with a break at the collision. The trace shows this as state labels drawn first. The probe answer is: "the collision is where energy goes, so I cut there and check what's conserved in each piece". The operation as coded: *before writing equations, split the process at brief, large internal forces; for each segment, conserve momentum if the net external impulse is negligible and mechanical energy if no non-conservative work is done.* Its published tag is to be checked against the Heller & Reif (1984) full text. It is also absent from the course's lecture notes, which solve such problems without stating the split.
3. **Teaching response.**
   - **Worked example.** A 60 kg skater at 4 m/s grabs a 20 kg sled at rest; together they glide up a frictionless slope. The segmentation is performed as a labelled step. The self-explanation prompt reads: "Why does the solution switch from momentum to energy once the skater holds the sled?" The student's answer locks before the model answer is shown.
   - **Completion problem.** The student marks the segment boundaries and picks a principle for each, as structured steps. Choosing energy across the grab triggers pre-authored feedback: the condition check, plus the kinetic energy before and after the grab showing the loss.
   - **Full problems** follow with no marked steps. The student moves on after three correct segment-and-principle choices in a row on different surfaces.
4. **Assessment, two to three weeks later, unassisted.**
   - A near-transfer item with a different surface: a bullet embeds in a block on a spring.
   - A far-transfer item with a different event type: two skaters push off from rest, then one slides up a ramp. That is an explosion followed by energy conservation.
   - Both are scored for correctness, and first errors are coded.
   - **What failure looks like:** the transfer error share does not fall relative to control, or students split only at collisions and miss the explosion. The second means the operation was learned as bound to its surface.

## Step 5 — the first version

**Users:**
- the researcher-author: builds and runs a topic module, and may also be the instructor;
- expert physicists: are interviewed;
- students: work the module and the quizzes.

**Workflow:**

| Stage | Input | Output |
|---|---|---|
| 1. Bottleneck check | Open-response multi-principle items with their component items; two parallel forms | Coded first errors, with category shares for the cohort; difficulty-layer entries |
| 2. Elicitation | Problems; 1–2 pilot experts, then 12 | Operations list: statement, trigger condition, trace evidence, number of experts sharing it, published tag |
| 3. Authoring | Operations and error categories | One module file: worked examples, prompts, model answers, structured steps with keys, feedback per error category; checked by a physicist |
| 4. Delivery | The module; students in a browser | A response log for every attempt, prompt answer and feedback shown |
| 5. Assessment | Delayed unassisted transfer quiz | Transfer scores, coded first errors, usage |

**Essential capabilities:**
- item and form management for quizzes;
- first-error coding with two-coder agreement;
- the elicitation session app;
- a module format with authoring checks: every operation carried by a worked step and a prompt; feedback for every error category;
- a learner-facing module player with locked answers and structured steps;
- the mastery rule;
- full logging;
- exports for analysis.

**Excluded from the first version:**
- live LLM tutoring;
- per-student routing;
- knowledge tracing;
- AI diagnostic dialogue;
- the decoding interview;
- teacher dashboards;
- more than one topic;
- LMS integration beyond participant IDs;
- visual polish beyond usability.

### Reuse of existing work

| Asset | Reuse | Work needed |
|---|---|---|
| `probe-app`: session app, audio, transcription, AI interviewer with contract and guard, freeze | Stage 2 as built | Extend the freeze to the code that speaks to the model; verify HTTPS in Playwright; add E_A and E_B; a rule against probes that name an operation absent from the trace (suggestion risk, gap 2), applied identically in the AI guard and the human script |
| `probe-code`: blind and trace exports, corroboration, α and κ, decoys, guard audit | Stage 2 coding; its agreement functions reused for stage 1 | Multi-label agreement to match the codebook; smoke tests for seven `probe-code` and two `probe-app` subcommands |
| `instrument/codebook/v0.md` | Operation types for stage 2 | Add the three ordinary categories for learner errors; define trace units; fill the Include/Exclude cells |
| Stage B design (worked examples, matched self-explanation prompts, locked answers, delayed transfer, K2) | The pedagogical specification for stage 3 and the evaluation design for stage 5 | None before the module exists |
| K0 and early-K0 design | The stage 1 protocol | Add component items and a second form |
| `instrument/problems/problems.json` (A1–B2) | Stage 2 only | Keep study items out of module and transfer materials |

**New code:**
- stage 1 item forms and coding: a `probe-code` subcommand plus a code sheet;
- the module format and its validator;
- a static module player on the existing stack (FastAPI and plain JavaScript) with logging;
- the transfer-quiz export.

## Step 6 — build order, milestones and validation

Each milestone ends in a decision: continue, change or stop. The prepared study's registered rules are used unchanged: early and pretest K0, K1, K2, Stage B's arm matching and its 2–3-week delay (`experiment-ai-assisted-cta-physics.md`). Anything added here is labelled secondary and cannot change what a registered rule decides. Thresholds marked *(project choice)* are judgments, not values taken from a source, and are pre-registered before the data they judge exist.

**Cohorts.**
- Early K0 (M1), the feasibility run (M5) and Stage B (M6) each use a distinct course offering.
- Students in the M3 usability sessions come from outside every Stage B cohort. Anyone who took part in M5 is excluded from M6 and flagged.
- The lecture notes that serve as Stage A's "absent from ordinary material" baseline are frozen before any module content exists. Module content does not enter the lectures of a Stage B offering.

**M1 — Bottleneck check (early K0).** Tests gaps 1 and 3.
- **Build:**
  - the 2 registered K0 items, each on a sheet collected before the single-principle component items are handed out, so only the order of the components is randomized;
  - a second, parallel form in different surface contexts about a week later;
  - the registered code sheet, extended with the step 4 taxonomy as sub-codes nested inside the registered K0 codes, so the K0 share is unchanged;
  - two-coder agreement through `probe-code`;
  - the pre-registration.
- **Validate:** the registered two-coder agreement (κ ≥ 0.70) before the decision.
- **Decide:**
  - **K0, as registered:** early K0 decides on form 1 only. It can stop the study only with at least 100 errored solutions; with fewer it is inconclusive, and Stage A may proceed. Stop if fewer than 30% of first errors are principle selection or representation.
  - **Secondary (new):** the same share among students who pass both components, with its own threshold *(project choice)*. If most students fail the components, record the bottleneck as prerequisites for this topic and plan a prerequisite module. This does not change the K0 decision.
  - **Form agreement (new):** Cohen's κ on each student's first-error category, among students who err on both forms, with a threshold and minimum n *(project choice)*. Per-student routing is tested later only if κ clears it.
  - **LLM coding (new):** the LLM codes independently against the adjudicated human codes, with a κ threshold *(project choice)*. LLM codes never enter the K0 decision.
  - The form-2 items go to the authors of the delayed test for the isomorphism check.
- **Needs:** a course offering and ethics cover (course logistics in `PROGRESS.md`).

**M2 — Elicitation tool and pilot.** Tests gap 2. Runs in parallel with M1.
- **Build:**
  - extend the freeze to the code that speaks to the model;
  - codebook cardinality, trace units and Include/Exclude cells;
  - smoke tests for seven `probe-code` and two `probe-app` subcommands;
  - the Playwright-verified HTTPS setup, and E_A and E_B;
  - fallback- and rejection-rate thresholds (decision 0004);
  - loopback-only console routes and full uuid4 session IDs (decision 0005);
  - encrypted backup of `sessions/`;
  - a rule against probes that name an operation absent from the trace, applied identically in the AI guard and the human script. It is deterministic or frozen with the prompts, and every rejection is logged and counted against the 20-minute cap.
- **Validate:** `/preflight pilot` GO. Then 1–2 physicists, with leading content coded blind to arm.
- **Decide:** the pilots build and check the codebook; they do not choose between arms. Only a pre-stated safety failure removes the AI arm before K1: an AI turn reaching the expert without passing the contract and guard. Otherwise K1 decides at M4.

**M3 — Module v0.** Needs M1 not stopped, and M2.
- **Build:**
  - the module format and validator, the player, logging, and the mastery rule with a switch to turn it off;
  - one conservation module built from provisional operations (those seen in the M2 pilot plus the published frameworks), labelled provisional;
  - the matched ordinary-explanation version, built to the Stage B specification: the same number of structured steps, feedback categories, prompts and stems, in a fixed sequence.
- **Validate:**
  - a physicist checks every solution and feedback text;
  - 5–8 students use it with think-aloud;
  - a test proves no model answer appears before the student's answer is locked;
  - the logs replay every session completely;
  - feedback and prompt texts are within ±10% in words between the two versions.
- **Decide:** fix usability and content before any trial.

**M4 — Validated operations (Stage A).** Needs M1 not stopped, and M2.
- **Build:** freeze, pre-register and run 12 experts per the Stage A protocol.
- **Validate:** K1. An operation counts as shared when at least 3 of the 12 experts show it.
- **Decide, as registered:**
  - If K1 passes, the module's operations are replaced by those that passed.
  - If only the AI-added condition fails, Stage B tests trace-based CTA operations.
  - If K1(a) or K1(c) fails, RQ1 is answered negatively and Stage B does not run.
  - Any other continuation, such as a module built only from published-framework operations, departs from the protocol and needs a new design and pre-registration.

**M5 — Feasibility run.** Needs M3, in its own offering.
- **Build:** both module versions in one course section, randomized by student, worked example first, mastery rule off as in M6.
- **Validate:**
  - compliance of at least 70% per arm;
  - time on task within 10% between the two versions;
  - the delayed test runs at the registered delay.
- **Decide:** fix logistics and the time match before M6. No effect is estimated for a decision; the section is too small. The time match is re-checked after M4 replaces the provisional operations, in the registered prompt piloting on non-participants.

**M6 — Learning and transfer (Stage B).** Needs M4 with K1 passed, or with only K1(b) failed (then Stage B tests trace-based CTA operations), and M5.
- **Build:** the registered Stage B:
  - fixed sequence, mastery rule off;
  - the same structured steps, feedback categories and prompts in both arms;
  - only the steps that carry operations differ;
  - any refutation cases identical in both arms.
- **Validate:** the pretest K0 first, which alone decides whether Stage B continues; then K2.
- **Decide:** as registered. If the effect is below the SESOI, stop using elicited operations as instruction for this topic.

**M7 — Offline learner-model check.** Runs on the M5/M6 response logs.
- **Build:** from the logs, compute where knowledge tracing and the three-in-a-row rule would each have stopped practice, for skills with at least a minimum number of opportunities *(project choice)*; the rule is off in M6, so both stopping points are counterfactual.
- **Validate:** the rate of disagreement between the two, judged against a threshold set before the logs are opened *(project choice)*.
- **Decide:** above the threshold, randomize the stopping rule by student and skill in a later offering.

**M8 — Live generation arm.** Only after K2 passes.
- **Build:** static feedback against live LLM feedback on the same prompts.
- **Validate:** an unassisted transfer test at the registered delay, with usage logged. N, SESOI and delay are pre-registered, and the items are written by someone blind to the feedback texts.
- **Decide:** generation stays only where it beats static by at least the SESOI.

**Later:**
- a powered order experiment (A8) with the pretest as moderator;
- the Phase 3 diagnosis comparison;
- per-student routing, if M1's agreement across forms clears its threshold;
- a second topic;
- frontend polish.

### Assumptions register

| # | Assumption | Tested at | If it fails |
|---|---|---|---|
| A1 | At least 30% of first errors on the registered K0 items are principle selection or representation | M1 (early K0); pretest K0 in M6 | Stage B stops; the bottleneck for this topic is ordinary, and the next module targets prerequisites or practice |
| A2 | AI retrospective probes are no worse than a trained human's on the contradicted rate | M4 (K1(c)) | As registered: Stage B does not run; a human-led design needs a new pre-registration |
| A3 | At least 3 of the 12 experts share operations that the trace corroborates and ordinary materials omit | M4 (K1(a)) | As registered: Stage B does not run; a published-framework module is a separate question |
| A4 | Operations can be taught as structured, checkable steps with pre-authored feedback | M3 | Free-response prompts coded offline; step-level feedback limited |
| A5 | A cohort-level diagnosis suffices for the first version | M1 (form agreement) | Test per-student routing |
| A6 | Static, expert-checked feedback teaches as well as live generation | M8 | Add live generation where it wins |
| A7 | A simple mastery rule stops practice about where knowledge tracing would | M7 | Randomize stopping rules |
| A8 | Worked examples first suit novices on this material | Untested in the first version; a later powered experiment | Switch the default order |
| A9 | Teaching the operations improves delayed transfer by at least the SESOI | M6 (K2) | Stop this use for this topic |
| A10 | LLM-assisted coding matches the adjudicated human codes | M1 | Human coding only |

**Build order:**
- M1 and M2 run in parallel.
- M3 and M4 need M1 not stopped, and M2.
- M5 needs M3.
- M6 needs M4 (K1 passed, or only K1(b) failed), and M5.
- M7 needs M5 or M6 logs.
- M8 needs K2 passed.
