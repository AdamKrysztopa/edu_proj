# DS2: Codebook anchors and κ benchmarks for "stated / partial / unstated"

- **Question:** Which annotation schemes separate "stated" from "topically related", "partial" from "full", seed from independent support, and retrieval failure from absence, and what agreement do they reach?
- **Answer:** The 10 comparable published values have a median of 0.725 (7 of 10 are ≥ 0.70, range 0.62–0.81). The six binary ones have a median of 0.75 (5 of 6 ≥ 0.70). The one scheme with a "partial" class reaches 0.62. So 0.70 is reached by 5 of the 6 binary values (four of them one scheme, AIS, on four datasets), but not shown on a scheme with a partial state.
- **Changed:** I4 gates MS1 on closed vs not closed at κ ≥ 0.70 (point estimate). The three-state weighted κ or ordinal α is reported but not gated. "Partial" becomes a count of named components rather than a degree. Seed and independent support are computed from metadata, not coded.

## Result

**The benchmarks do not show that comparable tasks rarely reach κ 0.70, so no owner decision on MS1's floor is due.** The table below (§4) counts 10 published chance-corrected values. Six are binary, three are three-way without a partial class, and one has a partial class.
- **All 10:** median 0.725, range 0.62–0.81, and 7 of the 10 are at or above 0.70.
- **The six binary values:** median 0.75, range 0.69–0.81, and 5 of the 6 are at or above 0.70 (four of the six are one scheme, AIS, on four datasets).
- **Below 0.70:**
  - WiCE, α = 0.62, the only scheme with a partial class;
  - FEVER, κ = 0.68, three-way with NOT ENOUGH INFO;
  - AIS on CNN/DM, α = 0.69, binary.
- SNLI's neutral class alone reaches κ = 0.60. It is a per-class value and is not counted.

So 5 of the 6 binary values and 2 of the 3 three-way values without a partial class reach 0.70 (four of the six binary values are one scheme, AIS, on four datasets). The one partial scheme falls short. MS1's floor is realistic on a binary gating split. No published evidence shows it is realistic on the three states. [literature-supported]

The floor sits near the middle of the published range, not below it. A two-coder study of V1's size reads a point estimate of at least 0.70 with probability 0.50 if the true κ is 0.70. That probability is 0.76–0.84 at a true κ of 0.75, and 0.92–0.98 at 0.80. This is a normal approximation that uses the report's half-widths of ±0.10 for 210 pools and ±0.14 for 107 firings (`report/sections/17_validation.tex:207-209`). It ignores clustering, which widens the interval further. [inferred]

**Recommended gating split: closed vs not closed.** This is the split the report already names (`17_validation.tex:203-204`). The recommendation rests on three grounds:
1. **Literature.** Strict full-support definitions reach 0.69–0.81: AIS and SufficientFacts. No published κ was found for "any support vs none".
2. **Prevalence.** The open state is rare: the PoC judge called 15 of 155 firings open (`17_validation.tex:211-212`). At that prevalence, κ is depressed for the same raw agreement. Closed is near balance: the cached qwen replies cite at least one "states" sentence in 311 of 641 cache entries (49%; 255 of 542 unique prompts, 47%), which the judge maps mostly to closed, or to synthetic-closed when only S sentences are cited (`research/n3/*/closure_judgements.json`; `semantic.py:195-201`). These are in-sample judge rates, used here only as a planning prevalence.
3. **Codebook.** Closed is the state that keeps a candidate out of the hypotheses. "Only open and partial can become hypotheses" (`docs/plans/n3-poc-lens-spec.md` §1.5).

The I1c split results were not used (see the item prompt).

**Recommended κ floor: Cohen's κ ≥ 0.70 on closed vs not closed, read on the point estimate.**
- Report the bias and prevalence indices beside it (Byrt et al. 1993, abstract), and PABAK. PABAK is defined in that paper's full text, which was not read.
- Report the clustered interval beside it as well.
- Keep the three-state weighted κ or ordinal α, which the report calls its primary measure (`17_validation.tex:202-204`), as a reported measure, but do not gate on it.
- Do not raise the floor to 0.80. Artstein & Poesio (2008, §5.3) recommend 0.80 but add that useful corpora have been obtained at 0.7. Only 1 of the 10 comparable values reaches 0.80.

**Decision it feeds.** I4's codebook, its κ floor and its gating split (`docs/plans/implement-queue.md` § I4). The recommendation is to **continue** to I4 with the floor and split as the report states them, and to change the codebook as in §3. The trigger condition, that comparable tasks rarely reach 0.70, does not hold for the gating split, so MS1's floor needs no owner decision.

**Method.** I read the full text of every dataset paper's annotation and agreement sections. I took the numbers from the PDF text, with table or section cited. For Feinstein & Cicchetti (1990), Byrt et al. (1993), Goddard et al. (2012), Hoskens & Wilson (2001), Krosnick (1991), Greenberg (2009) and Zobel (1998), only the abstract was read; these are marked "(abstract)". I resolved the DOIs through OpenAlex. A value cited by one paper from another is marked "as cited by". The anchor patterns in §3 are constructed illustrations in domains outside the coded set (§2, rule 9). They are not drawn from any ledger or gold, they are not checked as domain facts, and they are never a criterion.

## 1. Which schemes separate each pair

### 1.1 Stated vs only topically related

- **SQuAD 2.0** (Rajpurkar, Jia & Liang 2018) built this contrast on purpose. Crowdworkers wrote unanswerable questions that are relevant to the paragraph, where the paragraph contains a "plausible answer … of the same type as what the question asks for" (§1). Human F1 is 89.5 (Table 3, test set), against 48.9 for always abstaining (§5.2). The answer was a majority over about 4.8 human answers per question; the paper reports no κ.
  - **Codebook rule taken:** a sentence that names the construct, or holds something of the right type for the wrong referent, does not state the element.
  - The N3 judge prompt already says "topical relevance alone is not enough" (`gapmap/src/gapmap/semantic.py:114-115`). The JEV spike's examples are a qwen judge citing on-topic sentences that state no test result, and a condition on a rule taken for an exception to it (`research/spikes/jev/RESULTS.md`, "Examples").
- **AIS** (Rashkin et al. 2023) operationalises "stated" as the "according to" test: can a generic hearer affirm "According to P, s"? Annotators are told to "apply the 'according to' test strictly, without making further assumptions beyond what is conveyed in the text" (§3.4).
  - **Codebook rule taken:** a coder may not fill a gap with domain or common knowledge.
  - SufficientFacts (Atanasova et al. 2022, §4.2) found that its annotators' biggest challenge was "not to use common knowledge and assumptions".
- **NLI** separates entailment from neutral, where the premise is related but does not license the hypothesis.
  - SNLI's per-class Fleiss κ is entailment 0.72, contradiction 0.77 and neutral 0.60 (Bowman et al. 2015, Table 3).
  - "Neutral" is the least reproducible class, and it is the analogue of "related but not stated".

### 1.2 Partial vs full statement

Three schemes are relevant: an explicit partial class, a strict binary, and decomposition into atomic units.

- **An explicit partial class.**
  - WiCE labels each sub-claim SUPPORTED / PARTIALLY-SUPPORTED / NOT-SUPPORTED. Its agreement is Krippendorff's α = 0.62 on the development set, from 5 crowdworkers (Kamoi et al. 2023, §2.3).
  - WiCE gets its claim-level labels mechanically: a claim is SUPPORTED or NOT-SUPPORTED if all its sub-claims carry that label, and PARTIALLY-SUPPORTED otherwise. That derivation makes 54.7% of claims partial, against 18.2% of sub-claims (Table 2).
  - Liu, Zhang & Liang (2023) label citations as full, partial or no support. They report 82.0% pairwise agreement on "citation supports" and no chance-corrected value (Appendix E, Table 4).
- **A strict binary.**
  - AIS counts anything not fully supported as not attributable. Partial content, a slight change of detail or missing context are "all counted as 'not fully attributable'" (§4.1.2).
  - On the AIS question, crowd α is 0.69 on CNN/DM, 0.76 on QReCC, 0.79 on WoW and 0.74 on ToTTo. Against expert consensus it falls to 0.61 on CNN/DM and 0.54 on QReCC (Table 7).
- **Decomposition into atomic units.**
  - FActScore rejects a partial label because its definition "may be subjective and can lead to low agreement". Instead it splits text into atomic facts, each Supported or Not-supported. Two freelancers double-labelled 10% of the data, with raw agreement of 96%, 90% and 88% on three generators (Min et al. 2023, §3.1, §3.3).
- **A debatable middle category in an answer task.** Natural Questions added "Correct (but debatable)" after its experts found many answers that "raise some small doubt or quibble about whether they fully answer the question". This class holds 31% of long answers (Kwiatkowski et al. 2019, §4.2, Table 2).

**Codebook rule taken.** Define each lens's missing element as named components (§3), on the WiCE and FActScore pattern:
- **closed:** one sentence supplies every component;
- **partial:** at least one component is supplied, but not all;
- **open:** none is supplied.

"Partial" then means a component count, not a degree of satisfaction.

### 1.3 Seed support vs independent support

No annotation scheme found asks coders to label whether support is independent of the claim's own source. The constructs that come closest treat this as an artefact to remove, not a label to code. [inferred]

- **Label decided by the claim alone.** A claim-only BERT classifier scores 61.7% on FEVER, against a majority baseline of 33.3% (Schuster et al. 2019, §1).
- **Label decided by the hypothesis alone.** The same holds for NLI hypotheses (Poliak et al. 2018; Gururangan et al. 2018).
- **Amplification.** Greenberg (2009, abstract) documents "amplification" in a citation network: papers that present no data on a belief nonetheless expand it, so citation counts overstate independent support.
- **In this repo.** The PoC's closure failed its control because the seed's own sentences sat in both arms (`research/n3/README.md`, closure-step table). I1c's control2 drops the seed sources of both candidates from both arms (`research/n3_control_v3/RESULT.md`, "Step 1").

**Codebook rule taken.** Coders never judge independence. Each sentence's `independence_key` is compared with the seed's by metadata after coding. A closure counts as independent only if a sentence with a key different from the seed's states the element. Coders are blind to source. This extends the report's blinding to arm, judge answer, rank and run (`17_validation.tex:188`) and its origin blinding of the owner as coder (`17_validation.tex:192`).

### 1.4 Retrieval failure vs absence

Every scheme found defines "not stated" relative to a fixed pool, not to the world.
- SQuAD 2.0 judges against one paragraph.
- Natural Questions returns NULL "if there is no answer on the page" (§1).
- FEVER's NOT ENOUGH INFO is used when the claim "could not be supported or refuted by any amount of information in Wikipedia" (§3.2). Even with search, regular FEVER annotators recovered 72.36% of the evidence that super-annotators found by searching all of Wikipedia, at 95.42% precision (§3.4.2).
- In IR evaluation, pooled relevance judgements overestimate recall: "it is likely that many relevant documents have not been found" (Zobel 1998, abstract). Buckley et al. (2007) is titled for the same problem in large collections ("Bias and the limits of pooling"; only the record was read).

**Codebook rule taken.**
- "Open" means *not stated in this pool*, as the report already says (`17_validation.tex:194-195`).
- Absence from the corpus is a separate measurement: the retrieval-recall sample (`17_validation.tex:196-199`).
- FEVER's 72% says that the coder's own search in that sample is itself incomplete. The proposed recall floor of 0.80 should therefore be read as recall *relative to what a coder found*, not to the truth. [inferred]

## 2. Draft anchor rules (all lenses)

The coding unit stays the report's unit: (lens, seed span, missing element, evidence pool) (`17_validation.tex:175-177`).

1. **Code per sentence, then derive the pool.**
   - For each pool sentence the coder picks *states* (supplies every component), *partially* (supplies at least one) or *not*, and names the components supplied.
   - The pool state is derived as the judge derives it: **closed** if any attested sentence states it, **partial** if any partially states it, **open** otherwise (`semantic.py:195-203`). The judge's fourth state, synthetic-closed (only S sentences hit), is assigned after coding from the A/S label (rule 8).
   - Agreement is computed on the derived pool state, which is the gating unit. Sentence-level α is reported as a diagnostic. WiCE derives its claim labels the same way (§1.2).
2. **"According to" test.** A sentence states a component only if a reader can say "according to this sentence, \<component\>" without outside or domain knowledge (AIS).
3. **Topical relevance is not enough.** Naming the construct, the term, the cause or the test is not stating its content (SQuAD 2.0).
4. **No restatement.** A sentence that paraphrases the seed, or defines the term by itself ("excessive means too much"), does not state the element. This is the HEDGE "circular exception" alternative in the lens spec (§2.4).
5. **No authority as reason.** "The law, guideline or manufacturer requires it" is not a reason (WHY), and a cross-reference is not an exception (HEDGE). This extends the judge questions, which exclude "the law/regulation requires it" and cross-references (`semantic.py:23-28`), to any authority.
6. **Meta-statements are open.** "It depends on the situation", "use judgement" and "case by case" say that the element exists; they do not state it.
7. **One-sided examples are partial.** "Such as X" gives one side and not the separating feature (lens spec §2.1).
8. **Coders do not judge provenance or synthetic status.**
   - Independence (§1.3) is computed from metadata.
   - Synthetic-closed is computed from the A/S label after coding.
   - Coders see sentence text only, in random order, blind to arm, judge answer, rank, source and run. The report requires all of these except source (`17_validation.tex:188`).
9. **Anchor and training material.**
   - Training uses GDPR v2 only (`17_validation.tex:186`).
   - Anchors come from domains outside the coded set: never from PLC, GDPR v1 or the new out-of-sample domain.
   - Codebook rulings go into the owner's dated log (`17_validation.tex:190-191`).

## 3. Components and anchor patterns per lens

Components follow each lens's judge question (`semantic.py:18-32`). In each table, "Positive" is a pattern that **is** that state, and "Negative" is a near-miss that is **not**, with the state it gets instead. Every pattern is a constructed paraphrase, not a quotation.

### DISC: boundary of a judgement term
**Components:** (a) a separating feature or threshold; (b) applied to the term, so that a case can be placed on one side of the boundary.

| State | Positive | Negative |
|---|---|---|
| closed | Seed "check pads for *excessive wear*": "replace pads once the groove is under 1 mm deep" | "pads wear faster in wet weather": open (topical, no boundary) |
| partial | "wear depends on groove depth, rim scoring and squeal": factors named, no boundary | "excessive wear means the pads are too worn": open (circular, rule 4) |
| open | "worn pads are a common cause of poor braking" | "a pad is worn out once the wear line has gone; one still showing the line is fine": closed (contrast plus feature) |

### DIAG: a sign that tells one rival cause from the others
**Components:** (a) an observable sign; (b) tied to *this* rival, as opposed to the other listed causes.

| State | Positive | Negative |
|---|---|---|
| closed | Wi-Fi drops: "drops from interference coincide with the microwave running; drops from weak signal happen only in far rooms" | "interference is a frequent cause of drops": open |
| partial | "run a channel scan to check for interference": a discriminating test is named, but not the result that implicates the cause | "drops come from interference or from weak signal": open (rivals listed, no sign) |
| open | "common causes include interference, weak signal and overheating" | "an overheating router has a hot case and recovers after a restart, unlike interference": closed |

### SEL: condition → option mapping
**Components:** (a) a situation or condition; (b) the option it selects. One complete mapping closes.

| State | Positive | Negative |
|---|---|---|
| closed | Seed "choose the right sealant": "use silicone where the joint moves or gets wet; acrylic on dry joints you will paint" | "silicone and acrylic are both common sealants": open |
| partial | "the choice depends on movement, moisture and whether you will paint": conditions named, no mapping | "choose the sealant that suits the job": open (restates the seed) |
| open | "sealants come in many types and colours" | "if the joint will be painted, take acrylic": closed (one complete mapping) |

### HEDGE: the exception to a hedged rule
**Components:** (a) an identifiable case or condition; (b) in which the rule does not hold. It must not restate the rule's own judgement or cross-reference another rule.

| State | Positive | Negative |
|---|---|---|
| closed | Seed "generally, bleed radiators yearly": "a sealed system with an automatic air vent need not be bled" | "always bleed with the heating off": open (a condition on how the rule is applied, not an exception) |
| partial | "some newer systems may not need this": an exception class with no identifiable trigger | "unless there is no need, bleed yearly": open (circular) |
| open | "bleeding improves heating efficiency" | "skip it if every radiator heats evenly top to bottom and none gurgles": closed |

### GUARD: how the error is noticed
**Components:** (a) an observable signal or a specific check; (b) one that reveals the error before or as it happens.

| State | Positive | Negative |
|---|---|---|
| closed | Seed "a common mistake is overtightening carbon seat-post clamps": "stop when the torque wrench clicks at the value printed on the clamp" | "overtightening can crack the frame": open (a consequence, not detection; this is WHY content) |
| partial | "be careful and check your work when tightening": a check is named but not what to look at | "overtightening is a frequent error with carbon parts": open |
| open | "never overtighten carbon parts" | "if the bolt keeps turning with little added resistance, you have passed the limit": closed |

### WHY: the reason for a prohibition or contrast
**Components:** (a) a consequence, mechanism or purpose; (b) specific enough to say what goes wrong otherwise. Authority is not a reason (rule 5).

| State | Positive | Negative |
|---|---|---|
| closed | Seed "never put cast-iron pans in the dishwasher": "the dishwasher strips the seasoning and the pan rusts" | "the manufacturer says not to": open (authority) |
| partial | "it is bad for the pan": harm asserted, no mechanism | "dishwashers are not suitable for cast iron": open (restatement) |
| open | "cast-iron pans last for decades" | "hand-wash so the oil layer that stops rust is kept": closed (a purpose clause) |

### RESULT: what a test result means
**Components:** (a) an expected or criterion value of the result; (b) what a given result means or which action it leads to.

| State | Positive | Negative |
|---|---|---|
| closed | Seed "measure battery voltage": "a healthy battery reads about 12.6 V at rest; below 12.2 V, charge it before testing the alternator" | "set the meter to DC volts first": open (how to do the test, not its result) |
| partial | "a charged battery reads about 12.6 V": the expected value only | "interpret the reading carefully": open (rule 6) |
| open | "batteries lose charge in cold weather" | "below 9.6 V while cranking, the battery is failing; replace it": closed (result → meaning → action) |

## 4. Agreement benchmarks

These are chance-corrected values from the primary papers unless marked otherwise. The rows marked "yes" are the 10 values counted in the Result: six binary, three three-way without a partial class, and one with a partial class (WiCE).

| Task (source) | Labels | Coders, items | Measure | Value | Counted |
|---|---|---|---|---|---|
| SNLI validation (Bowman et al. 2015, Table 3) | entail / neutral / contradict | 5 crowd per pair, about 10% of the data | Fleiss κ, overall | 0.70 | yes |
| SNLI, neutral class only (same) | as above | as above | Fleiss κ per class | 0.60 | no (per class) |
| FEVER (Thorne et al. 2018, §3.4.1) | supported / refuted / NEI | 5 annotators, 7,506 claims | Fleiss κ | 0.6841 | yes |
| SciFact (Wadden et al. 2020, §3.3) | supports / refutes / NEI | re-annotation of 232 pairs | Cohen's κ | 0.75 | yes |
| SciFact rationale sentences (same) | in rationale / not | as above | Cohen's κ | 0.71 | yes |
| SufficientFacts (Atanasova et al. 2022, §4.2) | evidence still sufficient / not | 3 annotators | Fleiss κ | 0.81 | yes |
| AIS, CNN/DM (Rashkin et al. 2023, Table 7) | fully attributable / not | crowd | Krippendorff α | 0.69 | yes |
| AIS, QReCC (same) | as above | crowd | α | 0.76 | yes |
| AIS, WoW (same) | as above | crowd | α | 0.79 | yes |
| AIS, ToTTo (same) | as above | crowd | α | 0.74 | yes |
| WiCE sub-claims (Kamoi et al. 2023, §2.3) | supported / **partially** / not | 5 crowd, development set | Krippendorff α | 0.62 | yes |
| AIS against expert consensus (Rashkin et al. 2023, Table 7) | fully attributable / not | crowd vs 1 consensus | α | 0.61 CNN/DM, 0.54 QReCC | no (criterion validity, not inter-coder agreement) |
| HoVer, as cited by Atanasova et al. 2022 | supported / not | n/r | Fleiss κ | 0.63 | no (secondary) |
| Hanselowski et al. 2019, as cited by Wadden et al. 2020 | stance | n/r | Cohen's κ | 0.70 | no (secondary) |
| Citation support (Liu, Zhang & Liang 2023, Table 4) | full / **partial** / none | 3 annotations, 250 responses | raw pairwise | 82.0% | no (not chance-corrected) |
| QASPER answerability (Dasigi et al. 2021, §3) | answerable / not | 1.6 annotators per question | raw | 90% | no (raw) |
| FActScore atomic facts (Min et al. 2023, §3.3) | supported / not | 2 freelancers, 10% of the data | raw | 96%, 90%, 88% | no (raw) |
| Natural Questions long answer (Kwiatkowski et al. 2019, §5–6, Table 3) | span or NULL | 1 annotator against 5-way references drawn from the 25-way set (§5.2) | P / R | 80.4% / 67.6% | no (not κ) |

**Reading the table.**
- **All ten counted values:** median 0.725, range 0.62–0.81, and 7 of them ≥ 0.70.
- **The six binary values:** median 0.75, and 5 of 6 ≥ 0.70 (four of the six are one scheme, AIS, on four datasets).
- **Below 0.70:**
  - WiCE (0.62), the only counted value with a partial class;
  - FEVER (0.68), three-way;
  - AIS CNN/DM (0.69), binary.
- SNLI's neutral class (0.60) is a per-class value and is not counted.
- Comparable tasks clear 0.80 only once (SufficientFacts 0.81).
- In AIS, agreement among coders exceeds agreement with experts. The report makes the same point: κ shows that the label is reproducible, not that it is right (`17_validation.tex:33-34`).

The usual conventions run as follows:
- Landis & Koch (1977) call 0.61–0.80 "substantial", as their bands are shown in Artstein & Poesio (2008), Fig. 1.
- Krippendorff treats 0.667 as allowing "tentative conclusions" and 0.80 as the minimum for serious use, as cited by Artstein & Poesio (2008, §4.1.3).
- Artstein & Poesio (2008, §5.3) say "if a threshold needs to be set, 0.8 is a good value". They add that useful corpora have been obtained at the 0.7 level.

So 0.70 sits between the tentative and the strict convention. [literature-supported]

## 5. Failure modes that apply here

1. **Drift towards "partial".**
   - Rater severity drifts towards the group mean over a scoring session. Category-preference effects are present, but hard to detect over short periods (Hoskens & Wilson 2001, abstract). Neither shows a drift towards a middle category; they show that rater behaviour shifts within a session.
   - Krosnick (1991, abstract) proposes that under high cognitive effort, satisficing respondents choose the first reasonable alternative or say "don't know".
   - Natural Questions needed a "debatable" class for 31% of long answers (Table 2).
   - In this repo, Jev and qwen disagree mostly on "partially": qwen marked a partial on 51% of prompts, Jev on 20% (`research/spikes/jev/RESULTS.md`). These are judges, not coders, so this is consistent with the failure mode, not evidence for it.
   - **Mitigation:**
     - Define partial as a component count (§1.2).
     - Require the coder to name the component supplied.
     - Track the partial rate per batch.
     - Double-code every unit rather than a subsample.
     - Re-run anchor items at intervals and stop for recalibration if the partial rate shifts.
2. **Prevalence effects on κ.**
   - κ falls when the marginals are imbalanced, even at high observed agreement (Feinstein & Cicchetti 1990, abstract). Bias and prevalence indices should be reported beside κ (Byrt et al. 1993, abstract).
   - Arithmetic for two coders with equal marginals: at 93% raw agreement, κ is 0.61 when the rarer class is 10% (open, on closed-or-partial vs open) but 0.85 when it is 40%. At 95% the figures are 0.72 and 0.90. [inferred]
   - That is the prevalence ground for gating on closed vs not closed.
3. **Anchoring on the judge's answer.**
   - With a less accurate pre-annotator, the most accurate annotator's accuracy fell from 98.1% to 95.8%, through lapses of concentration on obvious tool errors (Fort & Sagot 2010, §4.2). The authors conclude that pre-annotation "comes with biases that should be identified and notified to the annotators" (§5).
   - Automation bias is mediated by trust, workload and time pressure, and is mitigated by training, accountability, and information rather than a recommendation (Goddard et al. 2012, abstract).
   - **Mitigation:** coders never see any judge output. The report already requires this (`17_validation.tex:188`). Anchors are never taken from units in the coded set (rule 9).
4. **The seed deciding the label.** The claim-only and hypothesis-only artefacts in §1.3. Coders see the seed only as context and code the pool sentences. Seed-source sentences are excluded by design (I1c) and flagged by metadata.
5. **Inherent disagreement.**
   - For 20% of NLI pairs, human judgements form a bimodal distribution with a non-trivial second component (Pavlick & Kwiatkowski 2019, §4.2).
   - In ChaosNLI, 100 annotations per item changed the majority label on 25% of the low-agreement SNLI items selected for re-annotation, and on 32% of the MNLI ones (Nie, Zhou & Bansal 2020, Table 2).
   - So some disputed units carry signal, not noise. The report's plan to keep disputed units out of the criterion and score them both ways (`17_validation.tex:189-190`) is the matching treatment.
6. **Domain knowledge filling the gap.** AIS's strict test and SufficientFacts' "common knowledge" errors (§1.1). Domain-expert coders are more exposed to this. This supports the report's choice of trained non-experts (`17_validation.tex:187`). [inferred]

## 6. What would change these recommendations

- **The gating split.** A training round on GDPR v2 in which coders agree less on the closed/partial boundary than on the partial/open boundary, or in which closed is as rare as open. Then closed-or-partial vs open would be the better split.
- **The floor.** A two-coder pilot on GDPR v2 whose κ on closed vs not closed is below 0.60 after recalibration. A κ that low is below every binary value in §4. It would show that the task is harder than its published analogues, and that would trigger the owner question this item names.
- **The components.** A lens where coders cannot agree on the component list itself. Then that lens's closure should be coded binary (AIS-style) and its partial dropped.

## Sources

Dataset and annotation papers. Full text read.
- Bowman, Angeli, Potts & Manning (2015). A large annotated corpus for learning natural language inference. EMNLP. https://aclanthology.org/D15-1075/
- Thorne, Vlachos, Christodoulopoulos & Mittal (2018). FEVER: a large-scale dataset for fact extraction and VERification. NAACL. https://aclanthology.org/N18-1074/
- Rajpurkar, Jia & Liang (2018). Know what you don't know: unanswerable questions for SQuAD. ACL. https://aclanthology.org/P18-2124/
- Kwiatkowski et al. (2019). Natural Questions: a benchmark for question answering research. TACL 7. https://aclanthology.org/Q19-1026/
- Rashkin et al. (2023). Measuring attribution in natural language generation models. Computational Linguistics 49(4). https://doi.org/10.1162/coli_a_00486 (read as arXiv:2112.12870)
- Kamoi, Goyal, Rodriguez & Durrett (2023). WiCE: real-world entailment for claims in Wikipedia. EMNLP. https://aclanthology.org/2023.emnlp-main.470/
- Wadden et al. (2020). Fact or fiction: verifying scientific claims. EMNLP. https://aclanthology.org/2020.emnlp-main.609/
- Atanasova, Simonsen, Lioma & Augenstein (2022). Fact checking with insufficient evidence. TACL 10. https://aclanthology.org/2022.tacl-1.43/
- Liu, Zhang & Liang (2023). Evaluating verifiability in generative search engines. Findings of EMNLP. https://aclanthology.org/2023.findings-emnlp.467/
- Dasigi et al. (2021). A dataset of information-seeking questions and answers anchored in research papers. NAACL. https://aclanthology.org/2021.naacl-main.365/
- Min et al. (2023). FActScore: fine-grained atomic evaluation of factual precision in long form text generation. EMNLP. https://aclanthology.org/2023.emnlp-main.741/
- Nie, Zhou & Bansal (2020). What can we learn from collective human opinions on natural language inference data? EMNLP. https://aclanthology.org/2020.emnlp-main.734/
- Pavlick & Kwiatkowski (2019). Inherent disagreements in human textual inferences. TACL 7. https://aclanthology.org/Q19-1043/
- Schuster et al. (2019). Towards debiasing fact verification models. EMNLP. https://aclanthology.org/D19-1341/
- Fort & Sagot (2010). Influence of pre-annotation on POS-tagged corpus development. Linguistic Annotation Workshop. https://aclanthology.org/W10-1807/
- Artstein & Poesio (2008). Inter-coder agreement for computational linguistics. Computational Linguistics 34(4). https://aclanthology.org/J08-4004/

Cited for one point. Abstract or OpenAlex record read.
- Poliak et al. (2018). Hypothesis only baselines in natural language inference. *SEM. https://doi.org/10.18653/v1/S18-2023
- Gururangan et al. (2018). Annotation artifacts in natural language inference data. NAACL. https://doi.org/10.18653/v1/N18-2017
- Landis & Koch (1977). The measurement of observer agreement for categorical data. Biometrics 33. https://doi.org/10.2307/2529310
- Feinstein & Cicchetti (1990). High agreement but low kappa: I. The problems of two paradoxes. J Clin Epidemiol 43(6). https://doi.org/10.1016/0895-4356(90)90158-L (abstract, PubMed 2348207)
- Byrt, Bishop & Carlin (1993). Bias, prevalence and kappa. J Clin Epidemiol 46(5). https://doi.org/10.1016/0895-4356(93)90018-V (abstract, PubMed 8501467)
- Goddard, Roudsari & Wyatt (2012). Automation bias: a systematic review of frequency, effect mediators, and mitigators. JAMIA 19(1). https://doi.org/10.1136/amiajnl-2011-000089 (abstract)
- Hoskens & Wilson (2001). Real-time feedback on rater drift in constructed-response items. J Educ Meas 38(2):121–145. https://doi.org/10.1111/j.1745-3984.2001.tb01119.x (abstract)
- Krosnick (1991). Response strategies for coping with the cognitive demands of attitude measures in surveys. Appl Cogn Psychol 5(3). https://doi.org/10.1002/acp.2350050305 (abstract)
- Greenberg (2009). How citation distortions create unfounded authority: analysis of a citation network. BMJ 339:b2680. https://doi.org/10.1136/bmj.b2680 (abstract)
- Zobel (1998). How reliable are the results of large-scale information retrieval experiments? SIGIR. https://doi.org/10.1145/290941.291014 (abstract)
- Buckley, Dimmick, Soboroff & Voorhees (2007). Bias and the limits of pooling for large collections. Information Retrieval 10. https://doi.org/10.1007/s10791-007-9032-x (OpenAlex record only; cited for its title claim)
