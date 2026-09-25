# Minimum reading: what the research map found

This is the one document to read. It condenses the 14 branch notes in `research/` and the experiment design into what they mean for the project. Every claim here has its sources, graded, in the linked note. The books and papers in map §8 are the deep dive, for when a branch needs first-hand reading.

## The bottom line

1. **The premise is plausible but unproven.** Experts do leave most of their reasoning out when they teach: about 70% of decision steps in one small surgery study (Sullivan et al. 2014). Expert–novice differences in how physics problems are represented replicate well. But no study shows that teaching elicited expert knowledge improves *transfer* in physics, and that is what the project needs.
2. **Elicit with CTA, not the decoding interview.** Decoding the Disciplines stays as the instructional frame (bottleneck → model → practice → assess). Its interview step has never been compared with anything. The provisional physics method is: the expert solves while thinking aloud without prompts, then answers probes over the recorded trace. AI probes run after the task, never during it. No study has evaluated an LLM conducting CTA.
3. **Diagnose classes reliably, individuals cautiously.** Concept inventories are strong for class-level evaluation and weak for one student: 31% of FCI answers changed on a retest within a week. Treat a misconception label as a context-bound hypothesis. Confirm it in a second context before acting on it. Build the misconception layer from student response data: physics TAs and instructors miss many common difficulties.
4. **Teach by making the learner generate.** Worked examples with self-explanation prompts are the best-supported format (g ≈ 0.5 immediate, ≈ 0.35 delayed or transfer). Explanations handed to the learner add little. Feedback should explain, not just mark right or wrong. Refutation and predict-before-you-observe help with misconceptions. Whether to explore first or model first is contested, so test it rather than assume it.
5. **System effects shrink under honest measurement.** Tutoring systems give 0.73 SD on tests written around the tutor but 0.13 on standardized tests. LLM tutors look large when the AI is still available or the test is immediate, and small, null or harmful when the AI is removed. Always measure unassisted, delayed and on tests not aligned to the system.

## Where each method stands

- **Decoding the Disciplines:** Low–moderate. Keep as the frame; its elicitation step moves to CTA.
- **Cognitive Task Analysis:** Moderate–high for training outcomes, all outside physics, none measuring transfer.
- **Expert–Novice research:** High as foundational evidence, but expertise is a continuum. Instruction built on it helps immediate problem solving; one far-transfer RCT, no delayed transfer.
- **Pedagogical Content Knowledge:** lowered to Moderate. Its link to student achievement is weak and correlational (r = .13 n.s. to .23).
- **Conceptual Change:** High that intuitive ideas persist alongside instruction; Moderate for interventions (refutation text g = 0.41, holding at delay). The theory itself is contested.
- **Concept Inventories:** High for cohort evaluation; weak for individual diagnosis.
- **Cognitive Apprenticeship:** Moderate. Its parts have evidence, the whole model has never been tested in physics, and fading on a fixed schedule is no better than not fading.
- **Worked Examples + Self-Explanation:** High for immediate novice problem solving; smaller at delay; reverses as prior knowledge grows.
- **Intelligent Tutoring Systems:** High only on tests aligned to the tutor; about 0–0.2 SD at scale.
- **Knowledge Tracing:** Moderate–high for *prediction*. Nothing shows it teaches better than a simple "N correct in a row" rule.
- **Threshold Concepts:** lowered to Low / contested. The label cannot be identified reliably and adds nothing tested.
- **Formative assessment:** High for feedback and quizzing as practices; low–moderate as a packaged intervention (d ≈ 0.2–0.3; the quoted 0.4–0.7 has no source).
- **LLM tutoring:** Emerging / moderate. The one physics trial (Kestin et al. 2025) is large but immediate, and it bundled the AI with self-pacing and pre-structured steps.

## What the evidence consistently lacks

The same three gaps recur across nearly every branch: **transfer**, **delay** and **university physics**. Most results are immediate, many are on tests aligned to the intervention, and few are in university physics. That is why the experiment makes delayed transfer its primary outcome.

## The experiment, in one paragraph

A gated design in first-year mechanics, on selecting and combining conservation principles (`experiment-ai-assisted-cta-physics.md`):
- **K0:** code past exam errors. Stop if fewer than 30% are principle-selection or representation errors.
- **Stage A:** 12 experts solve with think-aloud, then answer AI-led or human-led probes. Operations are validated against the trace. The gate **K1** needs at least 3 shared operations missing from ordinary material, at least 2 of them added by AI probes, and an acceptable contradicted rate.
- **Stage B:** about 370 students in a two-arm RCT. Worked examples with matched self-explanation prompts, with and without the elicited operations, delivered statically. The primary outcome is delayed transfer.
- **K2:** if the 90% upper bound is below d = 0.30, stop. Stage B is honestly a futility test: the likely effect is about 0.1–0.2.

## What would change the picture

- A controlled university-physics study of instruction built on expert reasoning, with a delayed transfer outcome.
- A comparison of the decoding interview with CTA, which could move DtD back to "keep".
- A study holding a tutor's design fixed and comparing an LLM with a non-generative version, which decides whether the system needs generation at all.
- A test of a knowledge-tracing mastery policy against a simple rule, on delayed transfer.

## What happens next

K0 is the gate, and it needs your anonymized past first-year mechanics exam scripts or error data.
