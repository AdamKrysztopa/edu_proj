# Decision-critical gaps (roadmap step 2)

**Question:** does published evidence settle any of the six gaps from [`route-comparison.md`](route-comparison.md) that could change the route? For those it does not settle: what assumption does the roadmap carry, and what is the cheapest test?

**Verdict:** none is settled. Three are open with no direct study: the premise, the AI interviewer and individual diagnosis. Three are partly settled by indirect evidence, enough to set a default for the first version: static delivery, a simple mastery rule, and worked examples first. The last of these qualifies the map's default for instructional order (§5.7), which is scoped to conceptual goals.

**Method:** six targeted OpenAlex searches, 2010–2026, one per gap, each told what the branch notes had already found. Sources are graded as in the branch notes. "Abstract" means only the abstract was read. Preprints and secondhand reports are marked.

## 1. Premise: do hidden expert operations cause a meaningful share of errors? — open

- Multi-principle problems: failing to recognise a needed principle is common, but the studies count students, not first errors.
  - White, Badeau, Heckler & Ding (2015), randomized order, N = 161, second-semester calculus-based course: 15–29% applied a concept correctly alone but not in the synthesis problem; solving single-concept problems first raised synthesis scores (d = 0.42). https://doi.org/10.1119/perc.2014.pr.063
  - Ibrahim, Ding, Heckler, White & Badeau (2017), N = 179 second-year majors: on a problem where energy and momentum apply at once, 36% (simple) and 12% (complex) wrote all the needed equations, against 55–61% when the principles apply in sequence; the paper does not separate wrong principle choice from setup errors. https://doi.org/10.1103/PhysRevPhysEducRes.13.020120
- Single-principle problems point the other way: of 1011 coded errors on four analysed engineering-statics problems (1493 submissions), 13% were major conceptual errors, 49% minor execution errors and 38% non-conceptual (Gross & Dinehart 2012; all errors, not first errors). https://doi.org/10.18260/1-2--21466
- The Docktor et al. (2016) rubric separates Physics Approach and Useful Description from Mathematical Procedures and can serve as the K0 coding scheme. https://doi.org/10.1103/PhysRevPhysEducRes.12.010130

**Assumption:** on problems combining conservation principles, principle selection or representation accounts for at least 30% of first errors. The support is indirect and depends on the problems needing several principles.
**Test:** early K0, as already designed, with first errors coded on the Docktor categories. Adding the matching single-principle problems in randomized order would separate a missing prerequisite (the single-principle problem also fails) from a selection bottleneck.
**Route consequence:** if K0 fails, expert elicitation is not the front end for this topic, and the route starts from diagnosis and practice.

## 2. AI as interviewer: do AI probes recover valid expert operations? — open

No study has an LLM interview domain experts and check what it recovers against observed performance. The head-to-head evidence comes from interviews of lay people about opinions:
- Chopra & Haaland (2026, working paper; earlier as https://doi.org/10.2139/ssrn.4572954), 766 AI-led interviews against open-ended surveys, no human-interviewer arm: about 95% of AI questions rated open and non-leading, and richer answers than surveys.
- Wuttke et al. (2025), students randomized to an AI or a student interviewer: the AI caused 88% of the failures to follow up on surprising or unclear answers; follow-up had worked in internal pretests, and the authors suspect minor prompt modifications. https://doi.org/10.18653/v1/2025.latechclfl-1.17
- Chan et al. (2024, preprint), N = 200 randomized, with misleading questions built in: a generative chatbot produced over three times more immediate false memories than control, and they persisted at one week. https://doi.org/10.48550/arxiv.2408.04681

**Assumption:** AI retrospective probes over an expert's trace recover operations the trace corroborates, with a contradicted rate no worse than a trained human interviewer's.
**Test:** the Stage A pilot with 1–2 physicists, computing K1's contradicted and uncorroborated rates per arm early, and coding each probe for leading content before the answer is scored.
**Design risks from this evidence:** probes must not name operations absent from the trace (suggestion), must follow up on surprising answers, and must not praise; the prompt freeze and a re-pilot after any prompt change are justified; the human comparison interviewer must be trained.
**Route consequence:** if it fails, AI stays out of elicitation, and trace-based CTA with a human interviewer is the method (K1 already provides for this).

## 3. Individual diagnosis: is any per-student diagnosis stable? — open

- No study found tests whether an individual's misconception or bottleneck label is stable on retest or across surface contexts, beyond Lasry et al. (2011). https://doi.org/10.1119/1.3602073
- Cognitive diagnostic models classify skill mastery on FCI, FMCE and EMCS data at scale with model-estimated accuracy, not retest (Le et al. 2025, N = 19,889). https://doi.org/10.1103/physrevphyseducres.21.010103 On the FCI, 14 of 30 items functioned differently between US and South African students, so the item-to-skill map does not carry over without checking (Naylor et al. 2026, preprint). https://doi.org/10.48550/arxiv.2609.12869
- Students apply correct ideas selectively across a sequence of related questions (Kryjevskaia, Stetzer & Grosz 2014). https://doi.org/10.1103/physrevstper.10.020109
- The one direct test of acting on individual diagnosis found remediation built on each student's error model not clearly better than reteaching (Sleeman et al. 1989, algebra, human tutors). https://doi.org/10.1207/s15516709cog1304_3
- Scoring a single response is feasible: GPT-4o matched human graders on physics explanations at 70–80% agreement with a 5-run majority vote (Chen & Wan 2025). https://doi.org/10.1103/physrevphyseducres.21.010126

**Assumption:** a first version diagnoses at cohort level and treats a student's label as a hypothesis for the next response to confirm, not as a basis for per-student routing.
**Test:** two parallel forms of the K0 items in different surface contexts, about a week apart, coded with the same categories; per-student agreement across forms. An individual-versus-cohort comparison is worth running only if that agreement is high.
**Route consequence:** if agreement is high, per-learner routing enters the first version; otherwise it waits.

## 4. Generation: does an LLM add learning over the same design delivered statically? — partly settled

- Pre-generated LLM feedback, checked by an LLM judge with limited human review, showed no reliable difference from teacher-written feedback on next-problem outcomes in school mathematics, pooled across two studies (Worden, EDM 2026 doctoral paper; secondhand summary of Worden et al. 2025 and 2026). https://doi.org/10.5281/zenodo.21039954
- Multimodal live LLM feedback showed no significant difference from fixed educator-written feedback on the same items (Zhao, Cao, Lin & Koedinger 2026, randomized, 197 college students online, one session, immediate test; F = 0.91, p = 0.34; no equivalence test, and the AI arm added a slide and audio). https://doi.org/10.1145/3785022.3785124
- On-demand GPT feedback added to corrective feedback helped in 2 of 7 lessons, only for learners who chose to use it (Thomas et al. 2025, adults in tutor training, observational with propensity adjustment). https://doi.org/10.1007/978-3-032-03870-8_33
- In algebra, ChatGPT help showed no significant difference from human-tutor help, and it was the only arm to beat no help (Pardos & Bhandari 2024, N = 274). https://doi.org/10.1371/journal.pone.0304013 An earlier, smaller preprint (N = 77) had favoured human hints, with ceiling and pretest imbalance. https://doi.org/10.48550/arxiv.2302.06871
- No study in physics or engineering, and none with a delayed, unassisted test, isolates live generation against matched static content.

**Assumption:** live generation adds no learning over expert-checked static feedback on the same problems; unproven, and the evidence is immediate and outside physics.
**Default:** deliver the first version statically, with feedback keyed to coded error categories. An LLM may draft it; an expert checks it. Live generation enters only as a randomized arm.
**Test:** static versus live feedback on the same self-explanation prompts, with unassisted transfer items a week later and usage logged in the live arm.

## 5. Learner model: does knowledge tracing beat a simple mastery rule? — partly settled

- No randomized comparison of a knowledge-tracing policy with N-correct-in-a-row on learning was found.
- Randomized threshold studies vary simple rules and find little difference in learning:
  - 2–5 correct in a row: more time at higher thresholds, no significant learning difference (Kelly & Heffernan 2016; abstract). https://doi.org/10.1145/2876034.2893393
  - An ALEKS A/B test with almost 33 million data points: the retention gap between thresholds was small but significant, under 0.02 after several weeks (Matayoshi et al. 2025, JEDM). https://doi.org/10.5281/zenodo.15698758
- A policy that skipped problems once BKT passed 0.9, and also reordered them, did not beat a fixed sequence (220 pupils in grades 4–5, fractions; Doroudi, Aleven & Brunskill 2019, appendix). https://doi.org/10.1007/s40593-019-00187-x
- Offline work finds the threshold and the data used matter more than the model (Pelánek & Řihák 2018; abstract). https://doi.org/10.1080/13614568.2018.1476596

**Default:** a simple rule (3–5 correct in a row, or a moving average) in the first version, with every response logged.
**Test:** fit a knowledge-tracing model to the logs offline and count how often it would have stopped practice at a different point. Only if disagreement is large, randomize the stopping rule by student and skill.

## 6. Order: explore first or model first, for multi-principle mechanics? — partly settled; it qualifies map §5.7

- Cognitive-load studies favour worked examples over problem solving for novices on high element-interactivity material. They compare levels of guidance, not the order of instruction:
  - Chen, Kalyuga & Sweller (2016), high-school trigonometry, delayed test: novices did better with worked examples on high-interactivity material, and more knowledgeable learners did better generating. https://doi.org/10.1016/j.learninstruc.2016.06.007
  - Chen, Kalyuga & Sweller (2015), the same pattern in geometry and trigonometry, on immediate and delayed tests. https://doi.org/10.1037/edu0000018
- A university classroom test of order, in two separate experiments with cohorts differing in prior knowledge, found the opposite pattern (He, Fiorella & Lemons 2025, undergraduate biochemistry): problem solving first did better for the low-prior-knowledge cohort (n = 367) and instruction first for the higher one (n = 138), on near transfer only, with no difference on far transfer. https://doi.org/10.1007/s10648-025-09993-3
- At university level, several preparation activities before instruction came out about equal (Trninić, Sinha & Kapur 2022). https://doi.org/10.1016/j.learninstruc.2022.101688
- None of these is in mechanics. The university-physics order studies in map §5.7 (Weaver et al. 2018; Bego et al. 2022; DeCaro et al. 2023) measured conceptual scores.

The map's §5.7 calls exploration with contrasting cases before modelling, "for conceptual goals", "the better-supported default beyond early primary school", from Sinha & Kapur (2021) and Loibl et al. (2017), with university physics support from one group's studies. Multi-principle problem solving is not a conceptual goal alone, and the high-interactivity evidence above favours worked examples for novices there. Neither side has a mechanics study of order.

**Default:** worked examples first for novices on multi-principle problems, fading to problem solving; not a settled finding.
**Test:** order as a factor inside a planned study, with pretest as the moderator and delayed transfer as the outcome.

## What this changes for step 3

- **Defaults the first version can take now:** cohort-level diagnosis with individual labels as hypotheses; static delivery with expert-checked content; a simple mastery rule with full logging; worked examples first with fading.
- **Gates that can still change the route:** the premise (early K0) and the AI interviewer (Stage A pilot). K0 comes first because it decides whether elicitation is the front end at all.
- **Test crowding:** gaps 1, 3, 4 and 6 each propose riding on the early K0 offering. One quiz cannot carry them all without confounding them. Step 6 must decide which ride on K0 and which wait for the first build.
