# Gap map: GDPR DPIA (run v2)

- Ledger: `1a1d1ca74b82a933496456b0bbb2b957568453016ce160c1f57c3786dcc6788b`
- Config: `35fd0af25618f8d6e0d1c2c3707d7e932afe2ce72dbd01e956034b43bfeb04c1`
- **Admissibility note:** 140 pending verification(s) in the ledger

## Summary

- **HYP:** 6 total
  - DISC: 1 (1 narrow)
  - HEDGE: 1 (1 narrow)
  - RESULT: 3 (3 narrow)
  - WHY: 1 (1 narrow)
- **Retrieval gaps:** RG-UNK 44, RG-SINGLE 3, RG-UNVER 6, RG-SIBLING 7
- **Control slot:** 1
- **PROMO-excluded seeds (S3 defect 1):** 1
- **§7.1 anti-renaming:** J10(low)=0.14, J10(high)=0.33, ρ(score,dens)=0.16, flags: closure-uninformative

## How to read this map

Every record separates three tiers, and they never mix:

- **OBSERVED EVIDENCE** — verified verbatim spans from the ledger; what a source actually says.
- **INFERRED GAP** — a statement about the ledger that anyone can re-run: which claims state the topic and which do not state the missing element.
- **HIDDEN-KNOWLEDGE HYPOTHESIS** — a prediction, labelled `inferred`, never a fact. It reads as a prediction ("is predicted to", "practitioners are hypothesised to"), never as an established finding.

Retrieval gaps, below the map, are a fourth and separate thing: not hypotheses. Their action is to search further or verify an unverified span — never to ask an expert.

**Breadth is not confidence.** Ranking among open gaps is deliberately by breadth of the attested explicit side — the opposite of low density, on purpose (§5): a gap many independent sources discuss without ever stating the missing element is a stronger claim that the element is genuinely unsaid than one only one source raises. Breadth says nothing about whether the gap is real. WHICH candidates are gaps at all is decided entirely by the lens's firing rule plus its closure test (§1.5, §2); whether that closure test is itself informative — i.e. not so easily satisfied by unrelated text that it would close almost anything — is exactly what the §7.1 checks below test.

**These are gap candidates, not findings.** The tier label stays `inferred`; precision against a human criterion is unmeasured (there is no gold yet). What IS measured is whether the closure judge's own informativeness beats a fair null — the mismatched-evidence control and the lexical donor null, both in §7.1.

**Lexical robustness (r/4) is not re-judged.** It is measured on the lexical construct across the 4 link-parameter settings (§1.4), not by re-asking the closure judge 4 times with different neighbourhood membership — so a record the judge closes or leaves open can still show a low or 0/4 lexical robustness; the two numbers answer different questions and neither overrides the other.

## Ranked gap map (candidates)

| rank | lens | anchor | breadth | lexical robustness | k_topic |
|---|---|---|---|---|---|
| 1 | DISC | relevant controller | narrow | 2/4 | 3 |
| 2 | RESULT | review to assess if processing is performed in accordance | narrow | 0/4 | 3 |
| 3 | HEDGE | In most cases, a data controller can consider that a | narrow | 3/4 | 2 |
| 4 | RESULT | measures to protect people's rights. | narrow | 2/4 | 2 |
| 5 | RESULT | assess whether something is high risk, you need to consider | narrow | 0/4 | 2 |
| 6 | WHY | You may be able to justify a decision not to carry out a | narrow | 0/4 | 2 |

### #1 [DISC] relevant controller

*lens: DISC; category: HYP*

**OBSERVED EVIDENCE**

- `c-45c0ec0f142fd0ba` [seed] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "Compliance with approved codes of conduct referred to in Article 40 by the relevant controllers or processors shall be taken into due account in assessing the impact of the processing operations performed by such controllers or processors, in particular for the purposes of a data protection impact assessment."
- `c-c08f1d894cabec8e` [seed] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "Compliance with approved codes of conduct referred to in Article 40 by the relevant controllers or processors shall be taken into due account in assessing the impact of the processing operations performed by such controllers or processors, in particular for the purposes of a data protection impact assessment."
- `c-1ec0b9ccfcb3bbe3` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "Article 35 of the General Data Protection Regulation ("GDPR") prescribes that a Data Protection Impact Assessment ("DPIA") shall be conducted by a controller where a type of data processing, in particular using new technologies, is likely to result in a high risk to the rights and freedoms of individuals."
- `c-23491770ff1621c6` [topic] literature_supported / procedure_document, key `ind-s-3bee394d5b9eb41b`, verdict supports: "If the processing is wholly or partly performed by a data processor, the processor should assist the controller in carrying out the DPIA and provide any necessary information (in line with Article 28(3)(f))."
- `c-82aecb61fdbe2614` [topic] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "Where necessary, the controller shall carry out a review to assess if processing is performed in accordance with the data protection impact assessment at least when there is a change of the risk represented by processing operations."
- `c-d0a3efb97c5579a1` [topic] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "Where necessary, the controller shall carry out a review to assess if processing is performed in accordance with the data protection impact assessment at least when there is a change of the risk represented by processing operations."
- `c-f4fade5df45938f5` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "The Irish Data Protection Act 2018, Section 84 transposing Article 27 of the Law Enforcement Directive also requires that a DPIA shall be conducted where certain processing, in particular using new technology, is likely to result in a high risk to the rights and freedoms of individuals, and when conducted for law enforcement purposes."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a boundary for 'relevant controller'. Re-runnable: prompt sha 1cdb2e7281d5.

- test: `DISC:relevant controller`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: Does not explicitly state threshold, defining feature, or contrast.
- partial hits: c-45c0ec0f142fd0ba, c-c08f1d894cabec8e

**HIDDEN-KNOWLEDGE HYPOTHESIS** (label: `inferred` — a prediction, never a fact)

Predicted, not observed: Hypothesis (inferred): practitioners are predicted to discriminate 'relevant controller' from its neighbours by features that no verified claim in this ledger matched test DISC:relevant controller for.

- predicted knowledge type: cue
- predicted tacitness: collective
- channel: contrasting-case classification, or expert-rated written vignettes

**Missing element:** a boundary for 'relevant controller'

**Reasoning:** 1 key(s) state relevant controller; 3 key(s) discuss the topic; the closure judge found no verified sentence matching test DISC:relevant controller

**Breadth:** narrow (uncalibrated; no gold) (score 1 = A2 + B0 − P1; k_step=1, k_topic=3); lexical robustness 2/4

**Alternatives:**

- [live] The boundary is stated in paraphrase without the anchor string. — the anchor-string regex cannot see a paraphrase (the main limitation of DISC, §9).
- [live] The term 'relevant controller' is institutionally indeterminate, so experts disagree and there is nothing to recover. — 2/2 anchor claims are typed norm or concept.
- [live] The boundary is in unfetched sources. — the ledger is a bounded retrieval.

**Expert question** (channel: contrasting-case classification, or expert-rated written vignettes):

> One source writes: "Compliance with approved codes of conduct referred to in Article 40 by the relevant controllers or processors shall be taken into due account in assessing the impact of the processing operations performed by such controllers or processors, in particular for the purposes of a data protection impact assessment.". Think of a recent case where you had to judge whether something was relevant controller. Describe one case that clearly was, one that clearly was not, and one that was hard to call. What differed between them, and what did you check first?

### #2 [RESULT] review to assess if processing is performed in accordance

*lens: RESULT; category: HYP*

**OBSERVED EVIDENCE**

- `c-6a628b149b089d07` [closure_near] synthetic_extrapolation / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict pending — flag: unverified-synthetic: "agreed and documented a schedule for reviewing the DPIA regularly or when we change the nature, scope, context or purposes of the processing"
- `c-d0a3efb97c5579a1` [seed] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "Where necessary, the controller shall carry out a review to assess if processing is performed in accordance with the data protection impact assessment at least when there is a change of the risk represented by processing operations."
- `c-23491770ff1621c6` [topic] literature_supported / procedure_document, key `ind-s-3bee394d5b9eb41b`, verdict supports: "If the processing is wholly or partly performed by a data processor, the processor should assist the controller in carrying out the DPIA and provide any necessary information (in line with Article 28(3)(f))."
- `c-45c0ec0f142fd0ba` [topic] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "Compliance with approved codes of conduct referred to in Article 40 by the relevant controllers or processors shall be taken into due account in assessing the impact of the processing operations performed by such controllers or processors, in particular for the purposes of a data protection impact assessment."
- `c-ee8eb1067bc2052c` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "As a controller, under the GDPR an organisation will need to assess, decide and document whether a DPIA is necessary for each proposed data processing operation."
- `c-293382d3dd07cdee` [topic] literature_supported / procedure_document, key `ind-s-3bee394d5b9eb41b`, verdict supports: "As a matter of good practice, a DPIA should be continuously reviewed and regularly re-assessed."
- `c-82aecb61fdbe2614` [topic] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "Where necessary, the controller shall carry out a review to assess if processing is performed in accordance with the data protection impact assessment at least when there is a change of the risk represented by processing operations."
+ 1 more topic claims across 3 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'review to assess if processing is performed in accordance'. Re-runnable: prompt sha 3f736491aee5.

- test: `RESULT:c-d0a3efb97c5579a1`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: Suggests regular review but does not specify outcomes or actions.
- partial hits: c-293382d3dd07cdee
- synthetic hits (unverified): c-6a628b149b089d07
- sibling run: partial

**HIDDEN-KNOWLEDGE HYPOTHESIS** (label: `inferred` — a prediction, never a fact)

Predicted, not observed: Hypothesis (inferred): practitioners are predicted to read the result of 'review to assess if processing is performed in accordance' against expected values and map it to the next action; no verified claim in this ledger matched test RESULT:c-d0a3efb97c5579a1.

- predicted knowledge type: interpretation, expectancy
- predicted tacitness: relational
- channel: CDM probes on a recalled case; process tracing

**Missing element:** a result-to-interpretation mapping for 'review to assess if processing is performed in accordance'

**Reasoning:** 1 key(s) state review to assess if processing is performed in accordance; 3 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-d0a3efb97c5579a1

**Breadth:** narrow (uncalibrated; no gold) (score 1 = A2 + B0 − P1; k_step=1, k_topic=3); lexical robustness 0/4

**Alternatives:**

- [live] The interpretation is stated in paraphrase without the seed's stems. — the stem-overlap test cannot see a paraphrase (the same limitation as DISC, §9).
- [live] The test is a formality with a binary outcome. — not every prescribed test feeds a real branching decision.
- [live] The interpretation is instrument-given. — a displayed pass/fail reading needs no practitioner interpretation.

**Expert question** (channel: CDM probes on a recalled case; process tracing):

> Sources prescribe: "Where necessary, the controller shall carry out a review to assess if processing is performed in accordance with the data protection impact assessment at least when there is a change of the risk represented by processing operations.". Think of the last time you did this. What result did you get, what had you expected, what did that result make you do next -- and what result would have sent you down a different path?

### #3 [HEDGE] In most cases, a data controller can consider that a processing meeting two criteria would require a DPIA to be carried out.

*lens: HEDGE; category: HYP*

**OBSERVED EVIDENCE**

- `c-326ee09ef2e8f7cc` [closure_near] synthetic_extrapolation / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict pending — flag: unverified-synthetic: "you may consider in your case that just meeting one criterion could require a DPIA."
- `c-4e53c658695920f0` [seed] literature_supported / procedure_document, key `ind-s-3bee394d5b9eb41b`, verdict supports: "In most cases, a data controller can consider that a processing meeting two criteria would require a DPIA to be carried out."
- `c-36c7a706651b79fc` [topic] literature_supported / procedure_document, key `ind-s-3bee394d5b9eb41b`, verdict supports: "However, in some cases, a data controller can consider that a processing meeting only one of these criteria requires a DPIA."
- `c-ee38417f00f57d2c` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "In addition to the cases provided for in Article 35 (3) GDPR, and taking into account the exception provided for in Article 35 (10) GDPR, carrying out a DPIA shall be compulsory if the processing operation meets at least two of the following criteria"

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of an exception condition. Re-runnable: prompt sha 3f789144cc10.

- test: `HEDGE:c-4e53c658695920f0`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: mentions exceptions where processing meeting one criterion may require DPIA
- partial hits: c-36c7a706651b79fc
- synthetic hits (unverified): c-326ee09ef2e8f7cc

**HIDDEN-KNOWLEDGE HYPOTHESIS** (label: `inferred` — a prediction, never a fact)

Predicted, not observed: Hypothesis (inferred): practitioners are predicted to know the cases in which 'In most cases, a data controller can consider that a processing meeting two criteria would require a DPIA to be carried out.' does not hold; no verified claim in this ledger matched test HEDGE:c-4e53c658695920f0.

- predicted knowledge type: decision
- predicted tacitness: relational
- channel: CDM hypotheticals and boundary-case vignettes

**Missing element:** an exception condition

**Reasoning:** 1 key(s) state In most cases, a data controller can consider that a processing meeting two criteria would require a DPIA to be carried out.; 2 key(s) discuss the topic; the closure judge found no verified sentence matching test HEDGE:c-4e53c658695920f0

**Breadth:** narrow (uncalibrated; no gold) (score 0 = A1 + B0 − P1; k_step=1, k_topic=2); lexical robustness 3/4

**Alternatives:**

- [live] The exception is circular: it restates the judgement. — a hedge whose exception re-states the criterion gives no new information.
- [live] The hedge is statutory boilerplate with no practice behind it. — a hedge in a legal or standard source may carry no field practice.
- [live] A trigger is stated inside the seed itself in a form EXC does not match. — EXC is a fixed lexicon and misses e.g. 'at least when'.

**Expert question** (channel: CDM hypotheticals and boundary-case vignettes):

> "In most cases, a data controller can consider that a processing meeting two criteria would require a DPIA to be carried out.". Describe a case where this did not hold, or where you decided against it. What about that case told you it was an exception?

### #4 [RESULT] measures to protect people's rights.

*lens: RESULT; category: HYP*

**OBSERVED EVIDENCE**

- `c-140883a50259f3f8` [seed] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "If you intend to rely on the exception for disproportionate effort, you must be able to justify this, and you must take other measures to protect people's rights."
- `c-dfc4b123febd036e` [closure_near] synthetic_extrapolation / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict pending — flag: unverified-synthetic: "If you intend to rely on the exception for disproportionate effort, you must be able to justify this, and you must take other measures to protect people's rights. In particular, you must still publish your privacy information, and carry out a DPIA."
- `c-386417259349f0c5` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "Invisible processing Processing of personal data that has not been obtained direct from the data subject in circumstances where the controller considers that compliance with Article 14 would prove impossible or involve disproportionate effort"
- `c-dbaff1702d47dffe` [topic] literature_supported / documentation, key `ind-s-0a19bb05cad9af5a`, verdict supports: "In case the processing concerns personal data that has not been obtained from the data subject and the information to be provided to data subjects pursuant to Article 14 of GDPR proves impossible or would require a disproportionate effort or is likely to render impossible or seriously impair the objectives of the processing."
- `c-4ba59da83c7f8310` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "Invisible processing: processing of personal data that has not been obtained direct from the data subject in circumstances where the controller considers that compliance with Article 14 would prove impossible or involve disproportionate effort. A DPIA is required where this processing is combined with any of the criteria from the European guidelines."
- `c-a182fc579c33bb1d` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "You may be able to justify a decision not to carry out a DPIA if you are confident that the processing is nevertheless unlikely to result in a high risk, but you should document your reasons."
- `c-ba6b87dee0892628` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "Most obviously, children are regarded as vulnerable to the processing of their personal data since they may be less able to understand how their data is being used, anticipate how this might affect them, and protect themselves against any unwanted consequences."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'measures to protect people's rights.'. Re-runnable: prompt sha 3cecbf1d7e1f.

- test: `RESULT:c-140883a50259f3f8`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): synthetic-closed
- judge reason: Mention next actions or expected results.
- partial hits: c-a182fc579c33bb1d
- synthetic hits (unverified): c-b67284715da02293, c-dfc4b123febd036e
- sibling run: partial

**HIDDEN-KNOWLEDGE HYPOTHESIS** (label: `inferred` — a prediction, never a fact)

Predicted, not observed: Hypothesis (inferred): practitioners are predicted to read the result of 'measures to protect people's rights.' against expected values and map it to the next action; no verified claim in this ledger matched test RESULT:c-140883a50259f3f8.

- predicted knowledge type: interpretation, expectancy
- predicted tacitness: relational
- channel: CDM probes on a recalled case; process tracing

**Missing element:** a result-to-interpretation mapping for 'measures to protect people's rights.'

**Reasoning:** 1 key(s) state measures to protect people's rights.; 2 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-140883a50259f3f8

**Breadth:** narrow (uncalibrated; no gold) (score 0 = A1 + B0 − P1; k_step=1, k_topic=2); lexical robustness 2/4

**Alternatives:**

- [live] The interpretation is stated in paraphrase without the seed's stems. — the stem-overlap test cannot see a paraphrase (the same limitation as DISC, §9).
- [live] The test is a formality with a binary outcome. — not every prescribed test feeds a real branching decision.
- [live] The interpretation is instrument-given. — a displayed pass/fail reading needs no practitioner interpretation.

**Expert question** (channel: CDM probes on a recalled case; process tracing):

> Sources prescribe: "If you intend to rely on the exception for disproportionate effort, you must be able to justify this, and you must take other measures to protect people's rights.". Think of the last time you did this. What result did you get, what had you expected, what did that result make you do next -- and what result would have sent you down a different path?

### #5 [RESULT] assess whether something is high risk, you need to consider

*lens: RESULT; category: HYP*

**OBSERVED EVIDENCE**

- `c-75da8a1fea3e9208` [closure_near] synthetic_extrapolation / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict pending — flag: unverified-synthetic: "Instead, the question is a more high-level screening test: are there features which point to the potential for high risk? You are screening for any red flags which indicate that you need to do a DPIA to look at the risk (including the likelihood and severity of potential harm) in more detail."
- `c-dc9662f14f9b139b` [seed] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "To assess whether something is 'high risk', the UK GDPR is clear that you need to consider both the likelihood and severity of any potential harm to individuals."
- `c-2f70066be18717df` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "Instead, the question is a more high-level screening test: are there features which point to the potential for high risk? You are screening for any red flags which indicate that you need to do a DPIA to look at the risk (including the likelihood and severity of potential harm) in more detail."
- `c-660bf9a2c014e783` [topic] literature_supported / procedure_document, key `ind-s-3bee394d5b9eb41b`, verdict supports: "A "risk" is a scenario describing an event and its consequences, estimated in terms of severity and likelihood."
- `c-732434703195d916` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "'Risk' implies a more than remote chance of some harm. 'High risk' implies a higher threshold, either because the harm is more likely, or because the potential harm is more severe, or a combination of the two."
- `c-ee8eb1067bc2052c` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "As a controller, under the GDPR an organisation will need to assess, decide and document whether a DPIA is necessary for each proposed data processing operation."
- `c-fc6fbb1e60453224` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "Risk in this context is about the potential for any significant physical, material or non-material harm to individuals."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'assess whether something is high risk, you need to consider'. Re-runnable: prompt sha bbde432a9c28.

- test: `RESULT:c-dc9662f14f9b139b`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: Mention screening for red flags indicating need for DPIA.
- partial hits: c-2f70066be18717df
- synthetic hits (unverified): c-75da8a1fea3e9208

**HIDDEN-KNOWLEDGE HYPOTHESIS** (label: `inferred` — a prediction, never a fact)

Predicted, not observed: Hypothesis (inferred): practitioners are predicted to read the result of 'assess whether something is high risk, you need to consider' against expected values and map it to the next action; no verified claim in this ledger matched test RESULT:c-dc9662f14f9b139b.

- predicted knowledge type: interpretation, expectancy
- predicted tacitness: relational
- channel: CDM probes on a recalled case; process tracing

**Missing element:** a result-to-interpretation mapping for 'assess whether something is high risk, you need to consider'

**Reasoning:** 1 key(s) state assess whether something is high risk, you need to consider; 2 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-dc9662f14f9b139b

**Breadth:** narrow (uncalibrated; no gold) (score 0 = A1 + B0 − P1; k_step=1, k_topic=2); lexical robustness 0/4

**Alternatives:**

- [live] The interpretation is stated in paraphrase without the seed's stems. — the stem-overlap test cannot see a paraphrase (the same limitation as DISC, §9).
- [live] The test is a formality with a binary outcome. — not every prescribed test feeds a real branching decision.
- [live] The interpretation is instrument-given. — a displayed pass/fail reading needs no practitioner interpretation.

**Expert question** (channel: CDM probes on a recalled case; process tracing):

> Sources prescribe: "To assess whether something is 'high risk', the UK GDPR is clear that you need to consider both the likelihood and severity of any potential harm to individuals.". Think of the last time you did this. What result did you get, what had you expected, what did that result make you do next -- and what result would have sent you down a different path?

### #6 [WHY] You may be able to justify a decision not to carry out a DPIA if you are confident that the processing is nevertheless unlikely to result in a high risk, but you should document your reasons.

*lens: WHY; category: HYP*

**OBSERVED EVIDENCE**

- `c-a182fc579c33bb1d` [seed] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "You may be able to justify a decision not to carry out a DPIA if you are confident that the processing is nevertheless unlikely to result in a high risk, but you should document your reasons."
- `c-ff9e8082e026882f` [closure_near] synthetic_extrapolation / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict pending — flag: unverified-synthetic: "If we decide not to carry out a DPIA, we document our reasons."
- `c-140883a50259f3f8` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "If you intend to rely on the exception for disproportionate effort, you must be able to justify this, and you must take other measures to protect people's rights."
- `c-20a6c82b01bdeff4` [topic] literature_supported / documentation, key `ind-s-0a19bb05cad9af5a`, verdict supports: "Systematic monitoring - provided that it is fair - of the position/location of employees as well as of the content and of the metadata of employee communications with the exception of logging files for security reasons provided that the processing is limited to the absolutely necessary data and is specifically documented."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a reason. Re-runnable: prompt sha 65a554da47ac.

- test: `WHY:c-a182fc579c33bb1d`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: to ensure accountability and compliance
- partial hits: c-a182fc579c33bb1d
- synthetic hits (unverified): c-c243b249d57d60ef, c-ff9e8082e026882f

**HIDDEN-KNOWLEDGE HYPOTHESIS** (label: `inferred` — a prediction, never a fact)

Predicted, not observed: Hypothesis (inferred): practitioners are predicted to know why 'You may be able to justify a decision not to carry out a DPIA if you are confident that the processing is nevertheless unlikely to result in a high risk, but you should document your reasons.'; no verified claim in this ledger matched test WHY:c-a182fc579c33bb1d.

- predicted knowledge type: rationale
- predicted tacitness: relational
- channel: a targeted confirmation question

**Missing element:** a reason

**Reasoning:** 1 key(s) state You may be able to justify a decision not to carry out a DPIA if you are confident that the processing is nevertheless unlikely to result in a high risk, but you should document your reasons.; 2 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-a182fc579c33bb1d

**Breadth:** narrow (uncalibrated; no gold) (score 0 = A1 + B0 − P1; k_step=1, k_topic=2); lexical robustness 0/4

**Alternatives:**

- [live] The rationale is a purpose clause that RAT does not match. — RAT does not match every 'to identify...' purpose clause.
- [not live] The source is promotional. — no PROMO lexicon hit on the span; no ledger field marks promotional voice (§10).
- [live] The reason is trivial safety knowledge. — an omitted rationale may simply be too obvious to state.

**Expert question** (channel: a targeted confirmation question):

> Sources say: "You may be able to justify a decision not to carry out a DPIA if you are confident that the processing is nevertheless unlikely to result in a high risk, but you should document your reasons.". What would happen if someone did it differently, and in what situations, if any, is doing it differently acceptable?

## Control slot

The §14.2 unknown-unknowns guard: an area no hypothesis touched, walked cold.

### EDPB Guidelines and Regulatory Interpretation

*lens: —; category: CONTROL*

**OBSERVED EVIDENCE**

(none)

**INFERRED GAP**

Control slot: area 'EDPB Guidelines and Regulatory Interpretation' (a-230df69d29033e7e) has no HYP record and the highest attested share (0.35) among candidate areas of ledger 1a1d1ca7.

- test: `CONTROL:a-230df69d29033e7e`; state: open (closure judge: )

**Reasoning:** the §14.2 unknown-unknowns guard: no HYP touches this area

**Breadth:** narrow (uncalibrated; no gold) (score 0 = A0 + B0 − P0; k_step=0, k_topic=0); lexical robustness 0/4

**Expert question** (channel: control):

> Walk me through how you carry out EDPB Guidelines and Regulatory Interpretation, from start to finish, as if I were watching you do it. What do you check, and in what order?

## Retrieval gaps

Not hypotheses: each one's action is to search further or verify a synthetic span, never to ask an expert.

### RG-UNK: slots searched, nothing found

| area | slot / question | source |
|---|---|---|
| Required Contents and Elements of a DPIA | check slot searched, found but unverified | sidecar slot |
| Required Contents and Elements of a DPIA | concept slot searched, found but unverified | sidecar slot |
| EDPB Guidelines and Regulatory Interpretation | concept slot searched, only thin coverage found | sidecar slot |
| High Risk Processing Activities Under GDPR | rationale slot searched, only thin coverage found | sidecar slot |
| GDPR Mandatory Data Protection Impact Assessment Requirements | rationale slot searched, only thin coverage found | sidecar slot |
| Exemptions and Exceptions to DPIA Requirements | procedure_step slot searched, only thin coverage found | sidecar slot |
| GDPR Mandatory Data Protection Impact Assessment Requirements | decision slot searched, only thin coverage found | sidecar slot |
| High Risk Processing Activities Under GDPR | procedure_step slot searched, only thin coverage found | sidecar slot |
| EDPB Guidelines and Regulatory Interpretation | rationale slot searched, found but unverified | sidecar slot |
| Exemptions and Exceptions to DPIA Requirements | check slot searched, only thin coverage found | sidecar slot |
| GDPR Mandatory Data Protection Impact Assessment Requirements | check slot searched, only thin coverage found | sidecar slot |
| EDPB Guidelines and Regulatory Interpretation | procedure_step slot searched, found but unverified | sidecar slot |
| EDPB Guidelines and Regulatory Interpretation | cue slot searched, found but unverified | sidecar slot |
| High Risk Processing Activities Under GDPR | failure_mode slot searched, only thin coverage found | sidecar slot |
| EDPB Guidelines and Regulatory Interpretation | What conditions determine which option is chosen in EDPB Guidelines and Regulatory Interpretation? | ledger U claim `c-a45d1dafb77ab32a` |
| EDPB Guidelines and Regulatory Interpretation | failure_mode slot searched, nothing found | sidecar slot |
| GDPR Mandatory Data Protection Impact Assessment Requirements | failure_mode slot searched, nothing found | sidecar slot |
| EDPB Guidelines and Regulatory Interpretation | How is work in EDPB Guidelines and Regulatory Interpretation checked for correctness or compliance? | ledger U claim `c-6a6272a6be7d00e9` |
| Required Contents and Elements of a DPIA | What observable features of a situation signal that Required Contents and Elements of a DPIA applies | ledger U claim `c-fcd5de338c4a2880` |
| EDPB Guidelines and Regulatory Interpretation | check slot searched, nothing found | sidecar slot |
| High Risk Processing Activities Under GDPR | What conditions determine which option is chosen in High Risk Processing Activities Under GDPR? | ledger U claim `c-1862a9ebad5e3293` |
| Required Contents and Elements of a DPIA | decision slot searched, nothing found | sidecar slot |
| GDPR Mandatory Data Protection Impact Assessment Requirements | cue slot searched, nothing found | sidecar slot |
| Required Contents and Elements of a DPIA | cue slot searched, nothing found | sidecar slot |
| High Risk Processing Activities Under GDPR | check slot searched, nothing found | sidecar slot |
| Exemptions and Exceptions to DPIA Requirements | How does work in Exemptions and Exceptions to DPIA Requirements typically go wrong, and what are the | ledger U claim `c-1cb761ba08966b23` |
| Required Contents and Elements of a DPIA | What conditions determine which option is chosen in Required Contents and Elements of a DPIA? | ledger U claim `c-f5515c76cf63898b` |
| High Risk Processing Activities Under GDPR | How is work in High Risk Processing Activities Under GDPR checked for correctness or compliance? | ledger U claim `c-789bc8a34facade5` |
| Exemptions and Exceptions to DPIA Requirements | failure_mode slot searched, nothing found | sidecar slot |
| Exemptions and Exceptions to DPIA Requirements | What observable features of a situation signal that Exemptions and Exceptions to DPIA Requirements | ledger U claim `c-ff15b031cbbca59b` |
| Required Contents and Elements of a DPIA | rationale slot searched, nothing found | sidecar slot |
| Exemptions and Exceptions to DPIA Requirements | Why is Exemptions and Exceptions to DPIA Requirements done the way it is? | ledger U claim `c-40a1835ea2d5cfce` |
| Exemptions and Exceptions to DPIA Requirements | What conditions determine which option is chosen in Exemptions and Exceptions to DPIA Requirements? | ledger U claim `c-f4b50ee5b9546ce3` |
| EDPB Guidelines and Regulatory Interpretation | decision slot searched, nothing found | sidecar slot |
| GDPR Mandatory Data Protection Impact Assessment Requirements | How does work in GDPR Mandatory Data Protection Impact Assessment Requirements typically go wrong | ledger U claim `c-08662e2f3570f7e9` |
| Exemptions and Exceptions to DPIA Requirements | decision slot searched, nothing found | sidecar slot |
| Exemptions and Exceptions to DPIA Requirements | cue slot searched, nothing found | sidecar slot |
| EDPB Guidelines and Regulatory Interpretation | How does work in EDPB Guidelines and Regulatory Interpretation typically go wrong, and what are the | ledger U claim `c-b57e3cf3e9fe9306` |
| High Risk Processing Activities Under GDPR | decision slot searched, nothing found | sidecar slot |
| Required Contents and Elements of a DPIA | Why is Required Contents and Elements of a DPIA done the way it is? | ledger U claim `c-b5bfb6f866254e6c` |
| Exemptions and Exceptions to DPIA Requirements | rationale slot searched, nothing found | sidecar slot |
| Required Contents and Elements of a DPIA | failure_mode slot searched, nothing found | sidecar slot |
| GDPR Mandatory Data Protection Impact Assessment Requirements | What observable features of a situation signal that GDPR Mandatory Data Protection Impact Assessment | ledger U claim `c-b884c4e8faba643f` |
| Required Contents and Elements of a DPIA | How does work in Required Contents and Elements of a DPIA typically go wrong, and what are the | ledger U claim `c-104d1e125734f7f4` |

### [RESULT] assessment must contain the measures envisaged to address — RG-SIBLING

*Action: verify — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-7ebb9adab33f6b29` [seed] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "the measures envisaged to address the risks, including safeguards, security measures and mechanisms to ensure the protection of personal data and to demonstrate compliance with this Regulation taking into account the rights and legitimate interests of data subjects and other persons concerned"
- `c-b144f120a2befd22` [closure_near] synthetic_extrapolation / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict pending — flag: unverified-synthetic: "Furthermore, the Board is of the opinion that even if two sets of processing have very similar type, scope, context and purposes, the specific circumstances of each processing could result in a situation where certain safeguards, security measures and mechanisms that are suitable for ensuring the protection of personal data in one processing might not provide the same level of protection in the other."
- `c-378c26c8b0d52b39` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "If in any doubt, we would always recommend that you do a DPIA to ensure compliance and encourage best practice."
- `c-388cd9f24bb7051f` [topic] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "Where appropriate, the controller shall seek the views of data subjects or their representatives on the intended processing, without prejudice to the protection of commercial or public interests or the security of processing operations."
- `c-4b342e0bd11c94a3` [topic] literature_supported / procedure_document, key `ind-s-3bee394d5b9eb41b`, verdict supports: "Updating the DPIA throughout the lifecycle project will ensure that data protection and privacy are considered and will encourage the creation of solutions which promote compliance."
- `c-4a696a73a28e2228` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "It is important to remember that it is a data controller's obligation to ensure a DPIA is carried out when required, at the appropriate time and contains all the detail required by the GDPR."
- `c-8ca36c42ba05e460` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "This list does not remove the general requirement to carry out proper and effective risk assessment and risk management of proposed data processing operations nor does it exempt the controller from the obligation to ensure compliance with any other obligation of the GDPR or other applicable legislation."
+ 5 more topic claims across 3 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a result-to-interpretation mapping for 'assessment must contain the measures envisaged to address' among the verified sentences retrieved (4 unverified sentences considered separately). Re-runnable: prompt sha 7b131221a806.

- test: `RESULT:c-7ebb9adab33f6b29`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): synthetic-closed
- judge reason: indicate next actions or results of test
- synthetic hits (unverified): c-624b38eaed63252c, c-b144f120a2befd22
- sibling run: closed

**Missing element:** a result-to-interpretation mapping for 'assessment must contain the measures envisaged to address'

**Reasoning:** 1 key(s) state assessment must contain the measures envisaged to address; 3 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-7ebb9adab33f6b29

### [HEDGE] Where necessary, the controller shall carry out a review to assess if processing is performed in accordance with the data protection impact assessment at least when there is a change of the risk represented by processing operations. — RG-UNVER

*Action: verify — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-82aecb61fdbe2614` [seed] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "Where necessary, the controller shall carry out a review to assess if processing is performed in accordance with the data protection impact assessment at least when there is a change of the risk represented by processing operations."
- `c-23491770ff1621c6` [topic] literature_supported / procedure_document, key `ind-s-3bee394d5b9eb41b`, verdict supports: "If the processing is wholly or partly performed by a data processor, the processor should assist the controller in carrying out the DPIA and provide any necessary information (in line with Article 28(3)(f))."
- `c-45c0ec0f142fd0ba` [topic] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "Compliance with approved codes of conduct referred to in Article 40 by the relevant controllers or processors shall be taken into due account in assessing the impact of the processing operations performed by such controllers or processors, in particular for the purposes of a data protection impact assessment."
- `c-ee8eb1067bc2052c` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "As a controller, under the GDPR an organisation will need to assess, decide and document whether a DPIA is necessary for each proposed data processing operation."
- `c-293382d3dd07cdee` [topic] literature_supported / procedure_document, key `ind-s-3bee394d5b9eb41b`, verdict supports: "As a matter of good practice, a DPIA should be continuously reviewed and regularly re-assessed."
- `c-c08f1d894cabec8e` [topic] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "Compliance with approved codes of conduct referred to in Article 40 by the relevant controllers or processors shall be taken into due account in assessing the impact of the processing operations performed by such controllers or processors, in particular for the purposes of a data protection impact assessment."
+ 1 more topic claims across 3 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating an exception condition among the verified sentences retrieved (4 unverified sentences considered separately). Re-runnable: prompt sha d76ded40d8b2.

- test: `HEDGE:c-82aecb61fdbe2614`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: DPIA not needed if processing unchanged since prior checking.
- synthetic hits (unverified): c-330f2e85e9c1c089

**Missing element:** an exception condition

**Reasoning:** 1 key(s) state Where necessary, the controller shall carry out a review to assess if processing is performed in accordance with the data protection impact assessment at least when there is a change of the risk represented by processing operations.; 3 key(s) discuss the topic; the closure judge found no verified sentence matching test HEDGE:c-82aecb61fdbe2614

### [WHY] Processing where you obtain data from third parties requires that you must first carefully consider whether you can provide privacy information to the individuals. — RG-UNVER

*Action: verify — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-3ef51af6c7c42a9b` [closure_near] synthetic_extrapolation / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict pending — flag: unverified-synthetic: "For these reasons, processing in this way is only permitted by the UK GDPR in limited circumstances. These include where to provide the privacy information proves impossible or would involve a disproportionate effort."
- `c-84c4aea16768e242` [seed] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "So, if you are proposing processing operations that involve the use of data obtained from third parties, you must first carefully consider whether you can provide privacy information to the individuals."
- `c-0937c557b4d2a8cf` [topic] literature_supported / documentation, key `ind-s-0a19bb05cad9af5a`, verdict supports: "Matching and/or combining personal data originating from multiple sources or third parties, or for two or more data processing operations performed for different purposes and/or by different data controllers in a way that would exceed the reasonable expectations of the data subjects."
- `c-172f77d705e222c9` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "'Invisible processing' occurs when you obtain personal data from somewhere other than directly from the individual themselves, and you don't provide them with the privacy information required by Article 14."
- `c-23491770ff1621c6` [topic] literature_supported / procedure_document, key `ind-s-3bee394d5b9eb41b`, verdict supports: "If the processing is wholly or partly performed by a data processor, the processor should assist the controller in carrying out the DPIA and provide any necessary information (in line with Article 28(3)(f))."
- `c-24974ed5ff9780ad` [topic] literature_supported / documentation, key `ind-s-0a19bb05cad9af5a`, verdict supports: "Systematic processing of personal data concerning profiling for marketing purposes when the data are combined with data collected from third parties."
- `c-5af1d5358a3fe576` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "In particular, you must still publish your privacy information, and carry out a DPIA."
+ 2 more topic claims across 3 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason among the verified sentences retrieved (4 unverified sentences considered separately). Re-runnable: prompt sha a8507b87beed.

- test: `WHY:c-84c4aea16768e242`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: where providing privacy information proves impossible or would involve disproportionate effort
- synthetic hits (unverified): c-3ef51af6c7c42a9b

**Missing element:** a reason

**Reasoning:** 1 key(s) state Processing where you obtain data from third parties requires that you must first carefully consider whether you can provide privacy information to the individuals.; 3 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-84c4aea16768e242

### [DISC] systematic process — RG-UNVER

*Action: verify — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-0d60f831507cc890` [closure_near] synthetic_extrapolation / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict insufficient — flag: unverified-synthetic: "The DPO guidelines say that 'systematic' means that the processing: occurs according to a system; is pre-arranged, organised or methodical; takes place as part of a general plan for data collection; or is carried out as part of a strategy."
- `c-24974ed5ff9780ad` [seed] literature_supported / documentation, key `ind-s-0a19bb05cad9af5a`, verdict supports: "Systematic processing of personal data concerning profiling for marketing purposes when the data are combined with data collected from third parties."
- `c-80aa5bf5286c5469` [seed] literature_supported / documentation, key `ind-s-0a19bb05cad9af5a`, verdict supports: "Large scale systematic processing of data of high significance or of a highly personal nature as are 2.2.1 Data of social welfare (data concerning poverty, unemployment, social work etc.),"
- `c-e8d479708b008c7e` [seed] literature_supported / documentation, key `ind-s-0a19bb05cad9af5a`, verdict supports: "Systematic processing of personal data which may prevent the data subject from exercising its rights or using a service or a contract, especially when data collected by third parties are taken into account."
- `c-0937c557b4d2a8cf` [topic] literature_supported / documentation, key `ind-s-0a19bb05cad9af5a`, verdict supports: "Matching and/or combining personal data originating from multiple sources or third parties, or for two or more data processing operations performed for different purposes and/or by different data controllers in a way that would exceed the reasonable expectations of the data subjects."
- `c-16ddcc4c85b654e9` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "When the processing in itself prevents data subjects from exercising a right or using a service or a contract - Explanation and examples: Processing of personal data that aims at allowing, modifying or refusing data subjects' access to a service or entry into a contract"
- `c-84c4aea16768e242` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "So, if you are proposing processing operations that involve the use of data obtained from third parties, you must first carefully consider whether you can provide privacy information to the individuals."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a boundary for 'systematic process' among the verified sentences retrieved (4 unverified sentences considered separately). Re-runnable: prompt sha 0de5662c4891.

- test: `DISC:systematic process`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): synthetic-closed
- judge reason: defines systematic processing as organized or methodical.
- synthetic hits (unverified): c-0d60f831507cc890

**Missing element:** a boundary for 'systematic process'

**Reasoning:** 1 key(s) state systematic process; 2 key(s) discuss the topic; the closure judge found no verified sentence matching test DISC:systematic process

### [DISC] innovative technology — RG-SIBLING

*Action: verify — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-1cbc0daaf9d62b80` [seed] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "Examples of processing using innovative technology include: artificial intelligence, machine learning and deep learning; connected and autonomous vehicles; intelligent transport systems; smart technologies (including wearables); market research involving neuro-measurement (e.g. emotional response analysis and brain activity); some 'internet of things' applications, depending on the specific circumstances of the processing."
- `c-880ec3318f9c8b92` [closure_near] synthetic_extrapolation / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict pending — flag: unverified-synthetic: "Innovative technology: processing involving the use of innovative technologies, or the novel application of existing technologies (including AI). A DPIA is required where this processing is combined with any of the criteria from the European guidelines."
- `c-bd315da27da93dd1` [seed] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "This is because using such technology can involve novel forms of data collection and use, possibly with a high risk to individuals' rights and freedoms."
- `c-db3d63a0a619f009` [seed] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "Recital 91 says innovative technology concerns new developments in technological knowledge in the world at large, rather than technology that is new to you, and its use can trigger the need to carry out a DPIA."
- `c-ee0b5f969d47b41f` [seed] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "Innovative technology: processing involving the use of innovative technologies, or the novel application of existing technologies (including AI). A DPIA is required where this processing is combined with any of the criteria from the European guidelines."
- `c-0cd1d75bf5fdad25` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "Genetic data: any processing of genetic data, other than that processed by an individual GP or health professional for the provision of health care direct to the data subject. A DPIA is required where this processing is combined with any of the criteria from the European guidelines."
- `c-a4bacfd8f2278d06` [topic] literature_supported / documentation, key `ind-s-0a19bb05cad9af5a`, verdict supports: "Innovative use or application of new technological or organizational solutions, which can involve novel forms of data collection and usage, possibly with a high risk to individuals ' rights and freedoms, like the combined use of fingerprint and face recognition for improved physical access control, or mhealth applications, or other "smart" applications from which user profiles are generated (e.g. daily habits), or artificial intelligence applications as well as publicly accessible blockchains that include personal data."
- `c-2cd6399cecd19ed8` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "Innovative use or applying new technological or organisational solutions - Explanation and examples: Innovative use or combining existing and new technologies, where personal and societal consequences are not necessarily well researched and known"
- `c-4ba59da83c7f8310` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "Invisible processing: processing of personal data that has not been obtained direct from the data subject in circumstances where the controller considers that compliance with Article 14 would prove impossible or involve disproportionate effort. A DPIA is required where this processing is combined with any of the criteria from the European guidelines."
- `c-8924c027cd443d82` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "Processing involving the use of new technologies, or the novel application of existing technologies (including AI). A DPIA is required for any intended processing operation(s) involving innovative use of technologies"
+ 5 more topic claims across 2 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a boundary for 'innovative technology' among the verified sentences retrieved (4 unverified sentences considered separately). Re-runnable: prompt sha dd9e0db0f5c3.

- test: `DISC:innovative technology`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: Sentence 10 defines innovative technology.
- synthetic hits (unverified): c-880ec3318f9c8b92
- sibling run: closed

**Missing element:** a boundary for 'innovative technology'

**Reasoning:** 1 key(s) state innovative technology; 2 key(s) discuss the topic; the closure judge found no verified sentence matching test DISC:innovative technology

### [WHY] Records of processing operations should include relevant risk information including reasons why a DPIA needs to be carried out, or not. — RG-UNVER

*Action: verify — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-9cff610c3307c53f` [seed] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "Records of processing operations should include relevant risk information including reasons why a DPIA needs to be carried out, or not."
- `c-133d4f0f03f0e6f1` [topic] literature_supported / procedure_document, key `ind-s-3bee394d5b9eb41b`, verdict supports: "The fact that the DPIA may need to be updated once the processing has actually started is not a valid reason for postponing or not carrying out a DPIA."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason among the verified sentences retrieved (4 unverified sentences considered separately). Re-runnable: prompt sha 423183e4ae22.

- test: `WHY:c-9cff610c3307c53f`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: not carrying out a DPIA should be justified and documented
- synthetic hits (unverified): c-c243b249d57d60ef

**Missing element:** a reason

**Reasoning:** 1 key(s) state Records of processing operations should include relevant risk information including reasons why a DPIA needs to be carried out, or not.; 2 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-9cff610c3307c53f

### [HEDGE] Where appropriate, the controller shall seek the views of data subjects or their representatives on the intended processing, without prejudice to the protection of commercial or public interests or the security of processing operations. — RG-UNVER

*Action: verify — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-564347dc939f0f50` [closure_near] synthetic_extrapolation / documentation, key `ind-s-0a19bb05cad9af5a`, verdict insufficient — flag: unverified-synthetic: "Large scale systematic processing of personal data concerning health and public health for public interest purposes as is the introduction and use of electronic prescription systems and the introduction and use of electronic health records or electronic health cards."
- `c-a44d9266f9135369` [seed] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "Where appropriate, the controller shall seek the views of data subjects or their representatives on the intended processing, without prejudice to the protection of commercial or public interests or the security of processing operations."
- `c-388cd9f24bb7051f` [topic] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "Where appropriate, the controller shall seek the views of data subjects or their representatives on the intended processing, without prejudice to the protection of commercial or public interests or the security of processing operations."
- `c-7ebb9adab33f6b29` [topic] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "the measures envisaged to address the risks, including safeguards, security measures and mechanisms to ensure the protection of personal data and to demonstrate compliance with this Regulation taking into account the rights and legitimate interests of data subjects and other persons concerned"
- `c-d09c08591fae4377` [topic] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "the measures envisaged to address the risks, including safeguards, security measures and mechanisms to ensure the protection of personal data and to demonstrate compliance with this Regulation taking into account the rights and legitimate interests of data subjects and other persons concerned"

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating an exception condition among the verified sentences retrieved (4 unverified sentences considered separately). Re-runnable: prompt sha df9bf593c695.

- test: `HEDGE:c-a44d9266f9135369`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): synthetic-closed
- judge reason: Specifically mentions large scale systematic processing of personal data concerning health and public health for public interest purposes.
- synthetic hits (unverified): c-564347dc939f0f50

**Missing element:** an exception condition

**Reasoning:** 1 key(s) state Where appropriate, the controller shall seek the views of data subjects or their representatives on the intended processing, without prejudice to the protection of commercial or public interests or the security of processing operations.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test HEDGE:c-a44d9266f9135369

### [RESULT] assessment must contain an assessment of the necessity and — RG-SIBLING

*Action: verify — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-ac63eb7fe60bdcda` [seed] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "an assessment of the necessity and proportionality of the processing operations in relation to the purposes"
- `c-62b7d38ec4fb158b` [topic] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "an assessment of the necessity and proportionality of the processing operations in relation to the purposes"

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a result-to-interpretation mapping for 'assessment must contain an assessment of the necessity and' among the verified sentences retrieved (4 unverified sentences considered separately). Re-runnable: prompt sha afa1d4776d66.

- test: `RESULT:c-ac63eb7fe60bdcda`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: Describes the process and outcome of DPIA
- synthetic hits (unverified): c-42e288a0194a5d29
- sibling run: closed

**Missing element:** a result-to-interpretation mapping for 'assessment must contain an assessment of the necessity and'

**Reasoning:** 1 key(s) state assessment must contain an assessment of the necessity and; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-ac63eb7fe60bdcda

### [DISC] vulnerable individual — RG-SIBLING

*Action: verify — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-15b265ddaece9ff3` [closure_near] synthetic_extrapolation / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict pending — flag: unverified-synthetic: "Individuals can be vulnerable where circumstances may restrict their ability to freely consent or object to the processing of their personal data, or to understand its implications."
- `c-456441331e134282` [seed] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "Imbalance of power - Explanation and examples: Processing of personal data of vulnerable (groups of) individuals, where there is significant imbalance of power between data controllers and individual"
- `c-c5eb1dd6d9372e14` [seed] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "Processing of personal data related to vulnerable individuals or audiences that may have particular or special considerations related to their inherent nature, context or environment. This will likely include minors, employees, mentally ill, asylum seekers, the aged, those suffering incapacitation;"
- `c-e24e1b7839c9aaad` [seed] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "Targeting of children/other vulnerable individuals for marketing, profiling for auto decision making or the offer of online services The use of the personal data of children or other vulnerable individuals for marketing purposes, profiling or other automated decision-making, or if you intend to offer online services directly to children."
- `c-f3cdc21f1cc70b95` [seed] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "The use of the personal data of children or other vulnerable individuals for marketing purposes, profiling or other automated decision-making, or if you intend to offer online services directly to children."
- `c-0d6950574951a8b3` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "These factors include: Uses of new or novel technologies;"
- `c-ec28d5866c2a30e9` [topic] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "processing on a large scale of special categories of data referred to in Article 9(1), or of personal data relating to criminal convictions and offences referred to in Article 10"
- `c-1aef53d1b7c00c24` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "Processing of special categories of personal data - Explanation and examples: o When processing of special categories of personal data, data on criminal or minor offences, such as"
- `c-39e0246bcbafb4ba` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "Any systematic monitoring, observation or control of individuals including that taking place in a public area or where the individual may not be aware of the processing or the identity of the data controller;"
- `c-4c553f0209009ab1` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "where the list involves"processing activities which are related to the offering of goods and services to data subjects or to the monitoring of their behaviour in several Member States, or may substantially affect the free movement of personal data within the Union", it must be submitted to the consistency mechanism and must be communicated to the EDPB"
+ 7 more topic claims across 2 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a boundary for 'vulnerable individual'. Re-runnable: prompt sha d87ef769174f.

- test: `DISC:vulnerable individual`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): partial
- judge reason: defines vulnerability through inability to consent or understand implications
- partial hits: c-c5eb1dd6d9372e14, c-e24e1b7839c9aaad, c-f3cdc21f1cc70b95
- synthetic hits (unverified): c-0ec4d0ffe1df556d, c-15b265ddaece9ff3
- sibling run: closed

**Missing element:** a boundary for 'vulnerable individual'

**Reasoning:** 1 key(s) state vulnerable individual; 2 key(s) discuss the topic; the closure judge found no verified sentence matching test DISC:vulnerable individual

### [RESULT] test should take into account any links between the original — RG-UNVER

*Action: verify — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-2e1da3f5942eade5` [closure_near] synthetic_extrapolation / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict pending — flag: unverified-synthetic: "We will provide you with a written response advising you whether the risks are acceptable, or whether you need to take further action."
- `c-dfcc40a1a8989992` [seed] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "That test should take into account any links between the original and new purposes, the context in which the data was collected (in particular the relationship between the individual and the organisation, the type of personal data involved (i.e. special categories of data), the possible consequences for individuals of the further processing, and if appropriate safeguards exist (i.e. encryption or pseudonymisation)."
- `c-f7ed599f1341d482` [closure_near] synthetic_extrapolation / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict pending — flag: unverified-synthetic: "In appropriate cases we may issue a formal warning or take action to ban the processing altogether."
- `c-6cf03fd617a8de87` [topic] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "With reference to point 1 above, where an organisation wishes to use personal data for purposes other than for which it was originally collected, Article 6(4) of the GDPR requires the organisation to do a compatibility test."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a result-to-interpretation mapping for 'test should take into account any links between the original' among the verified sentences retrieved (4 unverified sentences considered separately). Re-runnable: prompt sha c9295792ca73.

- test: `RESULT:c-dfcc40a1a8989992`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: Indicate potential actions or outcomes of the test.
- synthetic hits (unverified): c-2e1da3f5942eade5, c-f7ed599f1341d482

**Missing element:** a result-to-interpretation mapping for 'test should take into account any links between the original'

**Reasoning:** 1 key(s) state test should take into account any links between the original; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-dfcc40a1a8989992

### [DISC] systematic description — RG-SIBLING

*Action: verify — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-9d039cb830be1451` [seed] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "a systematic description of the envisaged processing operations and the purposes of the processing, including, where applicable, the legitimate interest pursued by the controller"
- `c-a0b6df5604b83b75` [seed] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "a systematic description of the envisaged processing operations and the purposes of the processing, including, where applicable, the legitimate interest pursued by the controller"
- `c-f261a6124016f285` [closure_near] synthetic_extrapolation / documentation, key `ind-s-436074893ba73671`, verdict pending — flag: unverified-synthetic: "a systematic description of the envisaged processing operations and the purposes of the processing, including, where applicable, the legitimate interest pursued by the controller"
- `c-7ebb9adab33f6b29` [topic] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "the measures envisaged to address the risks, including safeguards, security measures and mechanisms to ensure the protection of personal data and to demonstrate compliance with this Regulation taking into account the rights and legitimate interests of data subjects and other persons concerned"
- `c-d09c08591fae4377` [topic] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "the measures envisaged to address the risks, including safeguards, security measures and mechanisms to ensure the protection of personal data and to demonstrate compliance with this Regulation taking into account the rights and legitimate interests of data subjects and other persons concerned"

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a boundary for 'systematic description'. Re-runnable: prompt sha 7bc761e0eab6.

- test: `DISC:systematic description`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): synthetic-closed
- judge reason: Sentence 9 defines systematic description. Sentences 3 and 10 use 'systematic' without defining it.
- partial hits: c-a0b6df5604b83b75
- synthetic hits (unverified): c-dce3e1101c91840b, c-f261a6124016f285
- sibling run: closed

**Missing element:** a boundary for 'systematic description'

**Reasoning:** 1 key(s) state systematic description; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test DISC:systematic description

### [RESULT] assessment must contain a systematic description of the — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-a0b6df5604b83b75` [seed] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "a systematic description of the envisaged processing operations and the purposes of the processing, including, where applicable, the legitimate interest pursued by the controller"
- `c-f261a6124016f285` [closure_near] synthetic_extrapolation / documentation, key `ind-s-436074893ba73671`, verdict pending — flag: unverified-synthetic: "a systematic description of the envisaged processing operations and the purposes of the processing, including, where applicable, the legitimate interest pursued by the controller"
- `c-7ebb9adab33f6b29` [topic] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "the measures envisaged to address the risks, including safeguards, security measures and mechanisms to ensure the protection of personal data and to demonstrate compliance with this Regulation taking into account the rights and legitimate interests of data subjects and other persons concerned"
- `c-9d039cb830be1451` [topic] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "a systematic description of the envisaged processing operations and the purposes of the processing, including, where applicable, the legitimate interest pursued by the controller"
- `c-d09c08591fae4377` [topic] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "the measures envisaged to address the risks, including safeguards, security measures and mechanisms to ensure the protection of personal data and to demonstrate compliance with this Regulation taking into account the rights and legitimate interests of data subjects and other persons concerned"

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'assessment must contain a systematic description of the'. Re-runnable: prompt sha b76cdadbd38d.

- test: `RESULT:c-a0b6df5604b83b75`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: Mention expected content but not result or action.
- partial hits: c-9d039cb830be1451
- synthetic hits (unverified): c-f261a6124016f285
- sibling run: partial

**Missing element:** a result-to-interpretation mapping for 'assessment must contain a systematic description of the'

**Reasoning:** 1 key(s) state assessment must contain a systematic description of the; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-a0b6df5604b83b75

### [DISC] appropriate controller — RG-SIBLING

*Action: verify — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-388cd9f24bb7051f` [seed] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "Where appropriate, the controller shall seek the views of data subjects or their representatives on the intended processing, without prejudice to the protection of commercial or public interests or the security of processing operations."
- `c-a44d9266f9135369` [seed] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "Where appropriate, the controller shall seek the views of data subjects or their representatives on the intended processing, without prejudice to the protection of commercial or public interests or the security of processing operations."
- `c-7ebb9adab33f6b29` [topic] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "the measures envisaged to address the risks, including safeguards, security measures and mechanisms to ensure the protection of personal data and to demonstrate compliance with this Regulation taking into account the rights and legitimate interests of data subjects and other persons concerned"
- `c-d09c08591fae4377` [topic] literature_supported / standard, key `ind-s-436074893ba73671`, verdict supports: "the measures envisaged to address the risks, including safeguards, security measures and mechanisms to ensure the protection of personal data and to demonstrate compliance with this Regulation taking into account the rights and legitimate interests of data subjects and other persons concerned"

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a boundary for 'appropriate controller'. Re-runnable: prompt sha fbf8ae38ac0c.

- test: `DISC:appropriate controller`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: Sentences 1-5 all use 'Where appropriate,' which suggests a threshold for when the action should be taken, but do not explicitly define what constitutes 'appropriate controller'.
- partial hits: c-388cd9f24bb7051f, c-a44d9266f9135369
- sibling run: closed

**Missing element:** a boundary for 'appropriate controller'

**Reasoning:** 1 key(s) state appropriate controller; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test DISC:appropriate controller

### [WHY] The DPIA should be considered as a living tool, not merely as a one-off exercise. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-b1f4f8f753fffa7b` [seed] literature_supported / documentation, key `ind-s-8d32412761479351`, verdict supports: "The DPIA should be conducted before the processing begins and should be considered as a living tool, not merely as a one-off exercise."
- `c-b26922d1d0f7e54d` [closure_near] literature_supported / procedure_document, key `ind-s-3bee394d5b9eb41b`, verdict supports: "The DPIA is an on-going process, especially where a processing operation is dynamic and subject to ongoing change. Carrying out a DPIA is a continual process, not a one-time exercise."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a reason. Re-runnable: prompt sha fad41b953e1b.

- test: `WHY:c-b1f4f8f753fffa7b`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: To continuously address evolving risks and changes in processing operations.
- partial hits: c-b1f4f8f753fffa7b, c-b26922d1d0f7e54d

**Missing element:** a reason

**Reasoning:** 1 key(s) state The DPIA should be considered as a living tool, not merely as a one-off exercise.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-b1f4f8f753fffa7b

### [WHY] A DPIA is NOT required where processing operations do not result in a high risk to the rights and freedoms of individuals. — RG-SIBLING

*Action: verify — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-9b29f54705f21845` [seed] literature_supported / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict supports: "A DPIA is NOT required where: Processing operations do not result in a high risk to the rights and freedoms of individuals;"

**INFERRED GAP**

Of 2 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a reason. Re-runnable: prompt sha e9ae76390000.

- test: `WHY:c-9b29f54705f21845`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: none provided
- partial hits: c-9b29f54705f21845
- sibling run: closed

**Missing element:** a reason

**Reasoning:** 1 key(s) state A DPIA is NOT required where processing operations do not result in a high risk to the rights and freedoms of individuals.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-9b29f54705f21845

### [RESULT] measures put in place, the DPA must be consulted prior to — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-181c88c27aaa0de6` [seed] literature_supported / documentation, key `ind-s-8d32412761479351`, verdict supports: "Where there are residual risks that cannot be mitigated by the measures put in place, the DPA must be consulted prior to the start of the processing."
- `c-f1efe54c739fd8cb` [closure_near] synthetic_extrapolation / procedure_document, key `ind-s-0f92cd7c7aae9817`, verdict pending — flag: unverified-synthetic: "If such risks cannot be mitigated by appropriate measures, the controller needs to consult the Data Protection Authority (DPA) before proceeding."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'measures put in place, the DPA must be consulted prior to'. Re-runnable: prompt sha e157619e5ab0.

- test: `RESULT:c-181c88c27aaa0de6`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: Some sentences imply consultation but do not explicitly state the result or next action.
- partial hits: c-181c88c27aaa0de6
- synthetic hits (unverified): c-f1efe54c739fd8cb

**Missing element:** a result-to-interpretation mapping for 'measures put in place, the DPA must be consulted prior to'

**Reasoning:** 1 key(s) state measures put in place, the DPA must be consulted prior to; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-181c88c27aaa0de6

## §7 checks

### §7.1 Anti-renaming: is the map density in disguise?

Computed over lens candidates only (HYP, RG-SINGLE, RG-UNVER, RG-SIBLING, RG-UNDECIDED and closed candidates) -- RG-UNK and CONTROL are excluded, since their density cannot vary.

- `J10(map, D_low)` = 0.14
- `J10(map, D_high)` = 0.33
- Spearman ρ(score, dens) = 0.16
- flags: closure-uninformative

**Matched-density table** (all lens candidates, by `dens` tercile):

| tercile | n | closed | HYP |
|---|---|---|---|
| low | 16 | 9 | 1 |
| mid | 16 | 4 | 4 |
| high | 16 | 11 | 2 |

Top-tercile closed share: 0.69

**Closure rate by `k_topic` band** (all lens candidates):

| band | n | closed | rate |
|---|---|---|---|
| 0-1 | 16 | 6 | 0.38 |
| 2 | 13 | 5 | 0.38 |
| 3-4 | 17 | 11 | 0.65 |
| >=5 | 2 | 2 | 1.00 |

### S2 fair mismatched-evidence control: does the judge close because of the EVIDENCE, or because of the SEED?

Replaces the first (straw-man) control, second adversarial review, 2026-09-29: the old own-evidence arm always carried the seed's own sentences while the mismatched arm never did (17/22 of PLC's old closures cited only the seed or its source), and the mismatched sentences were off-topic (cyclic gap_id pairing). Now BOTH arms keep the seed's own sentences; the OWN arm adds this candidate's own retrieved non-seed-source sentences; the CONTROL arm replaces those with the non-seed-source sentences retrieved for the topically nearest OTHER candidate of the same lens (max seed-stem Jaccard, ties by gap_id). "other-source-only" is the OWN arm with the seed and same-source sentences excluded entirely -- how often an independent source alone closes it. `closure-uninformative` unless own_rate - control_rate >= 0.20 (of candidates); lenses with < 2 candidates are skipped.

| lens | n | own rate | control rate | other-source-only rate | flag |
|---|---|---|---|---|---|
| DISC | 14 | 1.00 | 1.00 | 0.36 | closure-uninformative |
| HEDGE | 5 | 0.60 | 0.60 | 0.80 | closure-uninformative |
| RESULT | 9 | 1.00 | 1.00 | 1.00 | closure-uninformative |
| SEL | 11 | 1.00 | 1.00 | 1.00 | closure-uninformative |
| WHY | 9 | 1.00 | 1.00 | 0.56 | closure-uninformative |
| **total** | 48 | 0.96 | 0.96 | 0.71 | closure-uninformative |

### S2 lexical donor null: why the lexical closure test was replaced

The reviewer's fair donor null for the (now-comparison-only) LEXICAL closure test: self and same-source claims are excluded from both arms, and the donor is the real non-common content stems of a random other-source A claim of the same knowledge type as the seed (`random.Random(0)`, 200 draws). A check "passes" (is informative) only if the observed count is STRICTLY ABOVE the null's 5-95% interval. DISC is excluded (anchor-regex-driven, not stem-overlap); DIAG is handled per its own closure unit (one rival's sign test, not the group).

| lens | observed closed | null mean | null 5-95% | n | flag |
|---|---|---|---|---|---|
| HEDGE | 0 | 0.7 | [0, 2] | 5 | closure-uninformative |
| RESULT | 1 | 0.3 | [0, 1] | 9 | closure-uninformative |
| SEL | 6 | 4.9 | [3, 7] | 11 | closure-uninformative |
| WHY | 4 | 2.2 | [0, 4] | 8 | closure-uninformative |
| **total** | 11 | 8.1 | [5, 12] |  | closure-uninformative |

### Judge-vs-lexical agreement

Confusion counts, `<lexical_state>-><judge_state>`, over every judged candidate (the lexical test no longer decides anything; this is diagnostic only).

| lexical -> judge | n |
|---|---|
| closed->closed | 12 |
| closed->partial | 3 |
| closed->synthetic-closed | 3 |
| open->closed | 7 |
| open->partial | 7 |
| open->synthetic-closed | 4 |
| partial->closed | 2 |
| partial->partial | 1 |
| synthetic-closed->closed | 3 |
| synthetic-closed->partial | 2 |
| synthetic-closed->synthetic-closed | 4 |

### §7.2 Cross-run stability

**this ledger → sibling** (9 open candidate(s)):

- `g-656818235091` [DISC] relevant controller: counterpart none
- `g-a2821a38f28f` [RESULT] review to assess if processing is performed in accordance: counterpart RG-SINGLE (partial)
- `g-42daa2d6e7e1` [HEDGE] In most cases, a data controller can consider that a processing meeting two criteria would require a DPIA to be carried out.: counterpart none
- `g-943c3031fd20` [RESULT] measures to protect people's rights.: counterpart RG-SINGLE (partial)
- `g-6ad618c77e8c` [RESULT] assess whether something is high risk, you need to consider: counterpart none
- `g-5b63f9ad44a6` [WHY] You may be able to justify a decision not to carry out a DPIA if you are confident that the processing is nevertheless unlikely to result in a high risk, but you should document your reasons.: counterpart none
- `g-a677263eb710` [RESULT] assessment must contain a systematic description of the: counterpart RG-SINGLE (partial)
- `g-5c58e8c60b0f` [WHY] The DPIA should be considered as a living tool, not merely as a one-off exercise.: counterpart none
- `g-e74dc1d1b656` [RESULT] measures put in place, the DPA must be consulted prior to: counterpart none

**sibling → this ledger** (15 open candidate(s)):

- `g-a894f01249ff` [WHY] A DPIA should begin early in a project lifecycle, before processing starts, and run alongside the planning and development process.: counterpart none
- `g-1b1e68dc5d39` [RESULT] measures, new technologies, and novel processing types.: counterpart none
- `g-15e306b63250` [DISC] systematic monitor: counterpart RG-UNVER (open)
- `g-a34d8523df48` [HEDGE] In most cases, a combination of two factors from the WP29 criteria indicates the need for a DPIA, though this is not a strict rule.: counterpart none
- `g-ff3ef1a6aded` [RESULT] assessment should include sources of risk and potential: counterpart none
- `g-e7adf9af268f` [RESULT] assess the origin, nature, particularity and gravity of: counterpart none
- `g-d2fa456e3d16` [RESULT] assess the necessity and proportionality of processing: counterpart none
- `g-d40eee24b901` [RESULT] measures to protect people's rights.: counterpart HYP (partial)
- `g-5d3fa976af6b` [RESULT] assess and mitigate impact on individuals' ability to: counterpart none
- `g-d6f0d018e8e3` [RESULT] monitoring, decisions on service access or opportunities, or: counterpart none
- `g-be53c0a9cb9a` [WHY] DPO advice on whether processing is compliant and can go ahead should be sought and documented as part of sign-off; if advice is not followed, reasons must be recorded.: counterpart none
- `g-9e2faa1f49b7` [HEDGE] A DPIA must involve the opinion of the Data Protection Officer and, where appropriate, the point of view of data subjects or their representatives.: counterpart none
- `g-92e1456d66ad` [RESULT] review to assess if processing is performed in accordance: counterpart HYP (partial)
- `g-fcde59e37154` [RESULT] assessment must contain a systematic description of the: counterpart RG-SINGLE (partial)
- `g-dfb760b0cd9e` [RESULT] measures should be considered when deciding whether to: counterpart none

