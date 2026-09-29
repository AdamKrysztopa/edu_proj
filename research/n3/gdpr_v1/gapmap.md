# Gap map: GDPR DPIA (run v1)

- Ledger: `cdd8e42e0a140e5d75cd9e83178479fa61ba55ed3aa0a701731f0ea7e68f004b`
- Config: `35fd0af25618f8d6e0d1c2c3707d7e932afe2ce72dbd01e956034b43bfeb04c1`

## Summary

- **HYP:** 1 total
  - RESULT: 1 (1 narrow)
- **Retrieval gaps:** RG-UNK 28, RG-SINGLE 12, RG-UNVER 4, RG-SIBLING 2
- **Control slot:** 1
- **PROMO-excluded seeds (S3 defect 1):** 8
- **§7.1 anti-renaming:** J10(low)=0.00, J10(high)=0.10, ρ(score,dens)=0.09, flags: closure-uninformative

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
| 1 | RESULT | measures, new technologies, and novel processing types. | narrow | 0/4 | 2 |

### #1 [RESULT] measures, new technologies, and novel processing types.

*lens: RESULT; category: HYP*

**OBSERVED EVIDENCE**

- `c-6370fb5b7eeb5c13` [seed] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "The nature of the processing is what you plan to do with the personal data. This should include, for example: how you collect the data; how you store the data; how you use the data; who has access to the data; who you share the data with; whether you use any processors; retention periods; security measures; whether you are using any new technologies; whether you are using any novel types of processing"
- `c-2fa57f35f4df9222` [topic] literature_supported / documentation, key `ind-s-6b6ff3689ae9ddc2`, verdict supports: "The Data Protection Impact Assessment and any ancillary documents; The respective responsibilities of the controller, joint controllers and processors involved in the processing, in particular for processing within a group of undertakings; The purposes and means of the intended processing; The measures and safeguards provided to protect the rights and freedoms of data subjects under the GDPR; The contact details of the Data Protection Officer (if applicable)"
- `c-82daadaccb91caa0` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "A systematic description of the processing is provided [article 35, paragraph 7, point a)]: The nature, scope, context and the of the processing are taken into account (recital 90) The personal data concerned, the recipients and the period for which the personal data will be kept are specified; A functional description of the processing operation is provided; The assets on which the personal data are based (hardware, software, networks, individuals, paper documents or paper transmission channels) are identified"
- `c-9847569d751f1249` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "If you are concerned that publication may reveal commercially sensitive information, undermine security or cause other risks, you should consider whether you can redact (black out) or remove sensitive details, or publish a summary."
- `c-fb7e55870abf0330` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "You should include an assessment of the security risks, including sources of risk and the potential impact of each type of breach (including illegitimate access to, modification of or loss of personal data)."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'measures, new technologies, and novel processing types.'. Re-runnable: prompt sha 92f87d71a849.

- test: `RESULT:c-6370fb5b7eeb5c13`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: Sentence 8 mentions mitigating measures but does not explicitly state expected results or next actions.
- partial hits: c-6370fb5b7eeb5c13

**HIDDEN-KNOWLEDGE HYPOTHESIS** (label: `inferred` — a prediction, never a fact)

Predicted, not observed: Hypothesis (inferred): practitioners are predicted to read the result of 'measures, new technologies, and novel processing types.' against expected values and map it to the next action; no verified claim in this ledger matched test RESULT:c-6370fb5b7eeb5c13.

- predicted knowledge type: interpretation, expectancy
- predicted tacitness: relational
- channel: CDM probes on a recalled case; process tracing

**Missing element:** a result-to-interpretation mapping for 'measures, new technologies, and novel processing types.'

**Reasoning:** 1 key(s) state measures, new technologies, and novel processing types.; 2 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-6370fb5b7eeb5c13

**Breadth:** narrow (uncalibrated; no gold) (score 0 = A1 + B0 − P1; k_step=1, k_topic=2); lexical robustness 0/4

**Alternatives:**

- [live] The interpretation is stated in paraphrase without the seed's stems. — the stem-overlap test cannot see a paraphrase (the same limitation as DISC, §9).
- [live] The test is a formality with a binary outcome. — not every prescribed test feeds a real branching decision.
- [live] The interpretation is instrument-given. — a displayed pass/fail reading needs no practitioner interpretation.

**Expert question** (channel: CDM probes on a recalled case; process tracing):

> Sources prescribe: "The nature of processing in a DPIA should include details about data collection, storage, usage, access, sharing, processors, retention periods, security measures, new technologies, and novel processing types.". Think of the last time you did this. What result did you get, what had you expected, what did that result make you do next -- and what result would have sent you down a different path?

## Control slot

The §14.2 unknown-unknowns guard: an area no hypothesis touched, walked cold.

### High-risk processing activities definition

*lens: —; category: CONTROL*

**OBSERVED EVIDENCE**

(none)

**INFERRED GAP**

Control slot: area 'High-risk processing activities definition' (a-cbfaacca47b52461) has no HYP record and the highest attested share (0.84) among candidate areas of ledger cdd8e42e.

- test: `CONTROL:a-cbfaacca47b52461`; state: open (closure judge: )

**Reasoning:** the §14.2 unknown-unknowns guard: no HYP touches this area

**Breadth:** narrow (uncalibrated; no gold) (score 0 = A0 + B0 − P0; k_step=0, k_topic=0); lexical robustness 0/4

**Expert question** (channel: control):

> Walk me through how you carry out High-risk processing activities definition, from start to finish, as if I were watching you do it. What do you check, and in what order?

## Retrieval gaps

Not hypotheses: each one's action is to search further or verify a synthetic span, never to ask an expert.

### RG-UNK: slots searched, nothing found

| area | slot / question | source |
|---|---|---|
| High-risk processing activities definition | Why is High-risk processing activities definition done the way it is? | ledger U claim `c-47fee6ae95f5aa5a` |
| DPIA exemptions and alternatives | How is work in DPIA exemptions and alternatives checked for correctness or compliance? | ledger U claim `c-9ab43988c0aeb8bf` |
| Processor involvement and consultation obligations | cue slot searched, nothing found | sidecar slot |
| DPIA exemptions and alternatives | What observable features of a situation signal that DPIA exemptions and alternatives applies or | ledger U claim `c-6f82040cf6008b01` |
| Legal triggers for DPIA requirements | cue slot searched, nothing found | sidecar slot |
| High-risk processing activities definition | check slot searched, nothing found | sidecar slot |
| DPIA exemptions and alternatives | failure_mode slot searched, nothing found | sidecar slot |
| Processor involvement and consultation obligations | Why is Processor involvement and consultation obligations done the way it is? | ledger U claim `c-16f166a8d825f4fe` |
| Legal triggers for DPIA requirements | What observable features of a situation signal that Legal triggers for DPIA requirements applies or | ledger U claim `c-d35bad4306c9fa5c` |
| Mandatory content and documentation requirements | What observable features of a situation signal that Mandatory content and documentation requirements | ledger U claim `c-40059d3365c9e3d2` |
| Legal triggers for DPIA requirements | failure_mode slot searched, nothing found | sidecar slot |
| High-risk processing activities definition | How does work in High-risk processing activities definition typically go wrong, and what are the | ledger U claim `c-a4bd5b125309bcf9` |
| Processor involvement and consultation obligations | How is work in Processor involvement and consultation obligations checked for correctness or | ledger U claim `c-60428f3091934ee7` |
| Mandatory content and documentation requirements | failure_mode slot searched, nothing found | sidecar slot |
| DPIA exemptions and alternatives | How does work in DPIA exemptions and alternatives typically go wrong, and what are the signs? | ledger U claim `c-887d4b0f297f377c` |
| Processor involvement and consultation obligations | rationale slot searched, nothing found | sidecar slot |
| Legal triggers for DPIA requirements | How does work in Legal triggers for DPIA requirements typically go wrong, and what are the signs? | ledger U claim `c-a0b6ad7fe4f3c14d` |
| DPIA exemptions and alternatives | check slot searched, nothing found | sidecar slot |
| High-risk processing activities definition | failure_mode slot searched, nothing found | sidecar slot |
| Processor involvement and consultation obligations | failure_mode slot searched, nothing found | sidecar slot |
| DPIA exemptions and alternatives | cue slot searched, nothing found | sidecar slot |
| High-risk processing activities definition | rationale slot searched, nothing found | sidecar slot |
| Processor involvement and consultation obligations | What observable features of a situation signal that Processor involvement and consultation | ledger U claim `c-a4c9012ce0a64b59` |
| Processor involvement and consultation obligations | check slot searched, nothing found | sidecar slot |
| Mandatory content and documentation requirements | cue slot searched, nothing found | sidecar slot |
| High-risk processing activities definition | How is work in High-risk processing activities definition checked for correctness or compliance? | ledger U claim `c-7cc34e97ea39bd25` |
| Processor involvement and consultation obligations | How does work in Processor involvement and consultation obligations typically go wrong, and what are | ledger U claim `c-49fd371e821afd7d` |
| Mandatory content and documentation requirements | How does work in Mandatory content and documentation requirements typically go wrong, and what are | ledger U claim `c-f3111c42cec6de09` |

### [HEDGE] Consultation with data protection officers and where appropriate with individuals and relevant experts is a requirement in the DPIA process. — RG-UNVER

*Action: verify — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-965c5dbfe1fb8a2f` [seed] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "You should consult your data protection officer (if you have one) and, where appropriate, individuals and relevant experts."
- `c-10c5d28dc341bcb1` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "DPOs and those with specific data protection responsibilities in larger organisations are likely to find it useful."
- `c-114c03552205b00b` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "We also recommend you consider seeking legal advice or advice from other independent experts such as IT experts, sociologists or ethicists where appropriate. However, there are no specific requirements to do so."
- `c-ae629243f4c8b411` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "Interested parties are involved: The opinion of the DPO is obtained (article 35, paragraph 2); The point of view of the data subjects or their representatives are gathered, where appropriate (article 35, paragraph 9)."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating an exception condition among the verified sentences retrieved (4 unverified sentences considered separately). Re-runnable: prompt sha b6796983fe68.

- test: `HEDGE:c-965c5dbfe1fb8a2f`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: Processing based on legal obligation or public task may not require DPIA.
- synthetic hits (unverified): c-509ffc8e1659d99b

**Missing element:** an exception condition

**Reasoning:** 1 key(s) state Consultation with data protection officers and where appropriate with individuals and relevant experts is a requirement in the DPIA process.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test HEDGE:c-965c5dbfe1fb8a2f

### [WHY] A DPIA should begin early in a project lifecycle, before processing starts, and run alongside the planning and development process. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-eaf0de6dab49e43f` [seed] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "A DPIA should begin early in the life of a project, before you start your processing, and run alongside the planning and development process."
- `c-f67a4b7ddcbed9ad` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "A DPIA should begin early in the life of a project, before you start your processing, and run alongside the planning and development process."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 1333b598b811.

- test: `WHY:c-eaf0de6dab49e43f`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: to identify and mitigate risks early in the project

**Missing element:** a reason

**Reasoning:** 1 key(s) state A DPIA should begin early in a project lifecycle, before processing starts, and run alongside the planning and development process.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-eaf0de6dab49e43f

### [RESULT] assessing necessity and proportionality, considerations — RG-UNVER

*Action: verify — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-682644ddc2173082` [seed] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "You should consider: Do your plans help to achieve your purpose? Is there any other reasonable way to achieve the same result?"
- `c-1d5f876623c86b1a` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "A DPIA should begin early in the life of a project, before you start your processing, and run alongside the planning and development process. It should include these steps: Step 1: identify the need for a DPIA Step 2: describe the processing Step 3: consider consultation Step 4: assess necessity and proportionality Step 5: identify and assess risks Step 6: identify measures to mitigate the risks Step 7: sign off and record outcomes"
- `c-532e4a3959d34796` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "The necessity and the proportionality are assessed [article 35, paragraph 7, point b)]: The measures envisaged to ensure compliance with the Regulation are determined, [article 35, paragraph 7, point d), and recital 90] taking into account: Measures contributing to the respect of the principles of proportionality and necessity of processing"
- `c-95c555efcf1b1916` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "Your DPIA must: describe the nature, scope, context and purposes of the processing; assess necessity, proportionality and compliance measures; identify and assess risks to individuals; and identify any additional measures to mitigate those risks."
- `c-b48bd9a9fe31d4d7` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "an assessment of the necessity and proportionality of the processing operations in relation to the purposes"
- `c-d2cd75d65c7a5378` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "The purpose of the processing is the reason why you want to process the personal data. This should include: your legitimate interests, where relevant; the intended outcome for individuals; and the expected benefits for you or for society as a whole."
+ 1 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a result-to-interpretation mapping for 'assessing necessity and proportionality, considerations' among the verified sentences retrieved (4 unverified sentences considered separately). Re-runnable: prompt sha 903882192077.

- test: `RESULT:c-682644ddc2173082`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: States less risky alternatives should be considered but does not explicitly state an expected result or next action.
- synthetic hits (unverified): c-d0f834c6dbd03ddd

**Missing element:** a result-to-interpretation mapping for 'assessing necessity and proportionality, considerations'

**Reasoning:** 1 key(s) state assessing necessity and proportionality, considerations; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-682644ddc2173082

### [RESULT] assess the likelihood and severity of any risks to — RG-UNVER

*Action: verify — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-37fdafe0ca6db276` [seed] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "We do an objective assessment of the likelihood and severity of any risks to individuals' rights and interests."
- `c-41a870a52524ab18` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "It is helpful to use a structured matrix to think about likelihood and severity of risks"
- `c-5003fe4d83ed9730` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "To assess whether something is 'high risk', the UK GDPR is clear that you need to consider both the likelihood and severity of any potential harm to individuals."
- `c-52b6d55652938282` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "To assess whether the risk is a high risk, you need to consider both the likelihood and severity of the possible harm."
- `c-a8b0720569f80d36` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "To assess the level of risk, you must consider both the likelihood and the severity of any impact on individuals."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a result-to-interpretation mapping for 'assess the likelihood and severity of any risks to' among the verified sentences retrieved (2 unverified sentences considered separately). Re-runnable: prompt sha addb11f20e87.

- test: `RESULT:c-37fdafe0ca6db276`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: Sentence 9 specifies the result and its meaning.
- synthetic hits (unverified): c-84a54f994d03523a

**Missing element:** a result-to-interpretation mapping for 'assess the likelihood and severity of any risks to'

**Reasoning:** 1 key(s) state assess the likelihood and severity of any risks to; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-37fdafe0ca6db276

### [RESULT] assessed by considering the number of individuals, volume of — RG-UNVER

*Action: verify — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-38f92abcd63ff279` [closure_near] synthetic_extrapolation / documentation, key `ind-s-505312a82b58a1e4`, verdict insufficient — flag: unverified-synthetic: "Any profiling of individuals on a large scale"
- `c-d7f4c0b3b05a9a2b` [seed] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "to decide whether processing is on a large scale you should consider: the number of individuals concerned; the volume of data; the variety of data; the duration of the processing; and the geographical extent of the processing."
- `c-361677e5d0272012` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "to decide whether processing is on a large scale you should consider: the number of individuals concerned; the volume of data; the variety of data; the duration of the processing; and the geographical extent of the processing."
- `c-81b8af3c016017b2` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "The scope of the processing is what the processing covers. This should include, for example: the nature of the personal data; the volume and variety of the personal data; the sensitivity of the personal data; the extent and frequency of the processing; the duration of the processing; the number of data subjects involved; and the geographical area covered."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a result-to-interpretation mapping for 'assessed by considering the number of individuals, volume of' among the verified sentences retrieved (4 unverified sentences considered separately). Re-runnable: prompt sha 74d77f8a407a.

- test: `RESULT:c-d7f4c0b3b05a9a2b`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: These sentences indicate actions to take based on large-scale processing.
- synthetic hits (unverified): c-1e1904ef5dc56c89, c-1ea36f2936d07b8e, c-38f92abcd63ff279

**Missing element:** a result-to-interpretation mapping for 'assessed by considering the number of individuals, volume of'

**Reasoning:** 1 key(s) state assessed by considering the number of individuals, volume of; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-d7f4c0b3b05a9a2b

### [DISC] systematic monitor — RG-SIBLING

*Action: verify — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-34c46d94cc8bd51f` [seed] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "(c)a systematic monitoring of a publicly accessible area on a large scale."
- `c-3882097b39ef919b` [seed] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "In particular, the UK GDPR says you must do a DPIA if you plan to: use systematic and extensive profiling with significant effects; process special category or criminal offence data on a large scale; or systematically monitor publicly accessible places on a large scale."
- `c-75b4dfcc59133374` [seed] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "Processing activities that consist of or include regular and systematic monitoring of employee activities - provided that they might produce legal effects concerning the employees or similarly significantly affects them"
- `c-b1fad9042198d88d` [seed] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "a systematic monitoring of a publicly accessible area on a large scale"
- `c-001378676d9bc0ce` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "a systematic and extensive evaluation of personal aspects relating to natural persons which is based on automated processing, including profiling, and on which decisions are based that produce legal effects concerning the natural person or similarly significantly affect the natural person"
- `c-3418362ac4ffa1fa` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "processing on a large scale of special categories of data referred to in Article 9(1) of the GDPR, or of personal data relating to criminal convictions and offences referred to in Article 10 of the GDPR"
- `c-a61a8a7f7977334f` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "You should also think carefully about doing a DPIA for any other processing that is large scale, involves profiling or monitoring, decides on access to services or opportunities, or involves sensitive data or vulnerable individuals."
- `c-ce8af6ca30f75288` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "a systematic and extensive evaluation of personal aspects relating to natural persons which is based on automated processing, including profiling, and on which decisions are based that produce legal effects concerning the natural person or similarly significantly affect the natural person"
- `c-d85bbd0dc09a826e` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "A data protection impact assessment referred to in paragraph 1 shall in particular be required in the case of: (a)a systematic and extensive evaluation of personal aspects relating to natural persons which is based on automated processing, including profiling, and on which decisions are based that produce legal effects concerning the natural person or similarly significantly affect the natural person"
+ 3 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a boundary for 'systematic monitor'. Re-runnable: prompt sha 89f9c0fd65c7.

- test: `DISC:systematic monitor`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): partial
- judge reason: explicitly states automatic requirement for DPIA; partially through listing conditions
- partial hits: c-3882097b39ef919b
- synthetic hits (unverified): c-1ea36f2936d07b8e, c-4103abf8561ff825, c-5b8584bc8041e654
- sibling run: closed

**Missing element:** a boundary for 'systematic monitor'

**Reasoning:** 1 key(s) state systematic monitor; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test DISC:systematic monitor

### [HEDGE] In most cases, a combination of two factors from the WP29 criteria indicates the need for a DPIA, though this is not a strict rule. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-04425373cd3694c7` [seed] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "In most cases, a combination of two of these factors indicates the need for a DPIA. However, this is not a strict rule."
- `c-008d014ea5c56f48` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "Otherwise, you need to check whether your processing is on the list of types of processing that automatically require a DPIA. If not, you need to screen for other factors that may indicate it is a type of processing that is likely to result in high risk, such as processing the data of vulnerable individuals."
- `c-a4a1629f9ba773b9` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "In most cases, a combination of two of these factors indicates the need for a DPIA. However, this is not a strict rule. You may be able to justify a decision not to carry out a DPIA if you are confident that the processing is nevertheless unlikely to result in a high risk, but you should document your reasons."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of an exception condition. Re-runnable: prompt sha b4fb9c505f4f.

- test: `HEDGE:c-04425373cd3694c7`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: Sentence 3 states this is not a strict rule.
- partial hits: c-04425373cd3694c7

**Missing element:** an exception condition

**Reasoning:** 1 key(s) state In most cases, a combination of two factors from the WP29 criteria indicates the need for a DPIA, though this is not a strict rule.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test HEDGE:c-04425373cd3694c7

### [RESULT] assessment should include sources of risk and potential — RG-SIBLING

*Action: verify — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-fb7e55870abf0330` [seed] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "You should include an assessment of the security risks, including sources of risk and the potential impact of each type of breach (including illegitimate access to, modification of or loss of personal data)."
- `c-6370fb5b7eeb5c13` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "The nature of the processing is what you plan to do with the personal data. This should include, for example: how you collect the data; how you store the data; how you use the data; who has access to the data; who you share the data with; whether you use any processors; retention periods; security measures; whether you are using any new technologies; whether you are using any novel types of processing"
- `c-9c89ae4a230668c2` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "Potential impacts on the rights and freedoms of data subjects are identified in case of events such as illegitimate access to data, an unwanted modification of data or their disappearance"

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'assessment should include sources of risk and potential'. Re-runnable: prompt sha 067869044610.

- test: `RESULT:c-fb7e55870abf0330`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: Expected results and next actions are implied but not explicitly stated.
- partial hits: c-fb7e55870abf0330
- synthetic hits (unverified): c-1173546aa8064ef3, c-54af4ffbfdfcf1be, c-61dece1b1bd9cd5a, c-bba8f9edf6c68cbc
- sibling run: closed

**Missing element:** a result-to-interpretation mapping for 'assessment should include sources of risk and potential'

**Reasoning:** 1 key(s) state assessment should include sources of risk and potential; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-fb7e55870abf0330

### [RESULT] assess the origin, nature, particularity and gravity of — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-003879ead25de590` [closure_near] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "If you have determined that the processing is likely to result in a high risk to the rights and freedoms of data subjects, you must carry out a data protection impact assessment (DPIA) for each processing operation."
- `c-9f706d60992e0c4d` [seed] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "The risks to the rights and freedoms of data subjects are managed [article 35, paragraph 7, point c)]: The origin, the nature, the particularity and the gravity of the risks are assessed (recital 84)"

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'assess the origin, nature, particularity and gravity of'. Re-runnable: prompt sha 6ed9e3ee6ebb.

- test: `RESULT:c-9f706d60992e0c4d`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: Suggests actions if high risk is identified but does not explicitly state expected results or their meaning.
- partial hits: c-003879ead25de590
- synthetic hits (unverified): c-aecb918cb8329838

**Missing element:** a result-to-interpretation mapping for 'assess the origin, nature, particularity and gravity of'

**Reasoning:** 1 key(s) state assess the origin, nature, particularity and gravity of; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-9f706d60992e0c4d

### [RESULT] assess the necessity and proportionality of processing — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-532e4a3959d34796` [seed] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "The necessity and the proportionality are assessed [article 35, paragraph 7, point b)]: The measures envisaged to ensure compliance with the Regulation are determined, [article 35, paragraph 7, point d), and recital 90] taking into account: Measures contributing to the respect of the principles of proportionality and necessity of processing"
- `c-1d5f876623c86b1a` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "A DPIA should begin early in the life of a project, before you start your processing, and run alongside the planning and development process. It should include these steps: Step 1: identify the need for a DPIA Step 2: describe the processing Step 3: consider consultation Step 4: assess necessity and proportionality Step 5: identify and assess risks Step 6: identify measures to mitigate the risks Step 7: sign off and record outcomes"
- `c-34a9732142853ea9` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "the measures envisaged to address the risks, including safeguards, security measures and mechanisms to ensure the protection of personal data and to demonstrate compliance with this Regulation taking into account the rights and legitimate interests of data subjects and other persons concerned"
- `c-682644ddc2173082` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "You should consider: Do your plans help to achieve your purpose? Is there any other reasonable way to achieve the same result?"
- `c-86c2d7d604a34b84` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "The DPIA allows the controller to: develop privacy friendly personal data processing operations and products, assess the impact on the privacy of data subjects, demonstrate that the fundamental principles of the GDPR are respected."
- `c-95c555efcf1b1916` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "Your DPIA must: describe the nature, scope, context and purposes of the processing; assess necessity, proportionality and compliance measures; identify and assess risks to individuals; and identify any additional measures to mitigate those risks."
+ 4 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'assess the necessity and proportionality of processing'. Re-runnable: prompt sha 0a56342224ca.

- test: `RESULT:c-532e4a3959d34796`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: Sentences partially indicate expected results or next actions but do not explicitly state them.
- partial hits: c-532e4a3959d34796, c-86c2d7d604a34b84

**Missing element:** a result-to-interpretation mapping for 'assess the necessity and proportionality of processing'

**Reasoning:** 1 key(s) state assess the necessity and proportionality of processing; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-532e4a3959d34796

### [RESULT] measures to protect people's rights. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-477ea8169e5e396e` [seed] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "If you intend to rely on the exception for disproportionate effort, you must be able to justify this, and you must take other measures to protect people's rights."
- `c-1ad3f7a1b2292d0b` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "'Invisible processing' occurs when you obtain personal data from somewhere other than directly from the individual themselves, and you don't provide them with the privacy information required by Article 14."
- `c-7729f9f91ae6ef8a` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "'Invisible processing' occurs when you obtain personal data from somewhere other than directly from the individual themselves, and you don't provide them with the privacy information required by Article 14. The processing is 'invisible' because the individual is unaware that you are collecting and using their personal data, even if you publish a privacy notice on your website."
- `c-b443da89de870d59` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "A DPIA is required for any intended processing operation(s) involving where the controller is relying on Article 14.5(b) when combined with any other criterion from WP248rev01"
- `c-d82d0d460fac14c0` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "Most obviously, children are regarded as vulnerable to the processing of their personal data since they may be less able to understand how their data is being used, anticipate how this might affect them, and protect themselves against any unwanted consequences."
- `c-e224ad1569d62c23` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "Most obviously, children are regarded as vulnerable to the processing of their personal data since they may be less able to understand how their data is being used, anticipate how this might affect them, and protect themselves against any unwanted consequences."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'measures to protect people's rights.'. Re-runnable: prompt sha d2a77f9a5cc1.

- test: `RESULT:c-477ea8169e5e396e`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: Sentences 1 and 2 imply expected results but do not explicitly state them.
- partial hits: c-477ea8169e5e396e
- sibling run: partial

**Missing element:** a result-to-interpretation mapping for 'measures to protect people's rights.'

**Reasoning:** 1 key(s) state measures to protect people's rights.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-477ea8169e5e396e

### [RESULT] assess and mitigate impact on individuals' ability to — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-0948649167e1de7b` [closure_near] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "If you have decided to accept a high risk, either because it is not possible to mitigate or because the costs of mitigation are too high, you must consult the ICO before you go ahead with the processing."
- `c-9600745fc043ff05` [seed] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "Your DPIA will help you assess and demonstrate whether you are taking a proportionate approach. It will help you consider how best to mitigate the impact on individuals' ability to exercise control over their data, and whether you can take other measures to support the exercise of their rights."
- `c-a14dd2aa7aaf93cb` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "To aid transparency and accountability, it is good practice to publish your DPIA. This could help foster trust in your processing activities, and improve individuals' ability to exercise their rights."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'assess and mitigate impact on individuals' ability to'. Re-runnable: prompt sha 467c9b02493b.

- test: `RESULT:c-9600745fc043ff05`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: Sentence 2 hints at the result by mentioning assessment and demonstration of proportionate approach. Sentence 6 specifies next action if high risk is accepted.
- partial hits: c-0948649167e1de7b, c-9600745fc043ff05

**Missing element:** a result-to-interpretation mapping for 'assess and mitigate impact on individuals' ability to'

**Reasoning:** 1 key(s) state assess and mitigate impact on individuals' ability to; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-9600745fc043ff05

### [RESULT] monitoring, decisions on service access or opportunities, or — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-a61a8a7f7977334f` [seed] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "You should also think carefully about doing a DPIA for any other processing that is large scale, involves profiling or monitoring, decides on access to services or opportunities, or involves sensitive data or vulnerable individuals."
- `c-001378676d9bc0ce` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "a systematic and extensive evaluation of personal aspects relating to natural persons which is based on automated processing, including profiling, and on which decisions are based that produce legal effects concerning the natural person or similarly significantly affect the natural person"
- `c-34c46d94cc8bd51f` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "(c)a systematic monitoring of a publicly accessible area on a large scale."
- `c-3882097b39ef919b` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "In particular, the UK GDPR says you must do a DPIA if you plan to: use systematic and extensive profiling with significant effects; process special category or criminal offence data on a large scale; or systematically monitor publicly accessible places on a large scale."
- `c-b1fad9042198d88d` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "a systematic monitoring of a publicly accessible area on a large scale"
- `c-e7aaad0024f89f82` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "The use of the personal data of children or other vulnerable individuals for marketing purposes, profiling or other automated decision-making, or if you intend to offer online services directly to children."
+ 1 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'monitoring, decisions on service access or opportunities, or'. Re-runnable: prompt sha 98960fa5ac20.

- test: `RESULT:c-a61a8a7f7977334f`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: Mention next actions or expected results indirectly
- partial hits: c-a61a8a7f7977334f
- synthetic hits (unverified): c-0f2778b309c5dca4, c-1173546aa8064ef3, c-16af9326fa272d7d, c-4103abf8561ff825

**Missing element:** a result-to-interpretation mapping for 'monitoring, decisions on service access or opportunities, or'

**Reasoning:** 1 key(s) state monitoring, decisions on service access or opportunities, or; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-a61a8a7f7977334f

### [WHY] DPO advice on whether processing is compliant and can go ahead should be sought and documented as part of sign-off; if advice is not followed, reasons must be recorded. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-72b9fa83c03d74eb` [seed] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "As part of the sign-off process, you should seek and document DPO advice on whether the processing is compliant and can go ahead. If you decide not to follow their advice, you need to record your reasons."
- `c-1d5f876623c86b1a` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "A DPIA should begin early in the life of a project, before you start your processing, and run alongside the planning and development process. It should include these steps: Step 1: identify the need for a DPIA Step 2: describe the processing Step 3: consider consultation Step 4: assess necessity and proportionality Step 5: identify and assess risks Step 6: identify measures to mitigate the risks Step 7: sign off and record outcomes"
- `c-337175f83999d8ef` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "If you have a Data Protection Officer (DPO), you must ask for their advice on your DPIA, and document it as part of the process."
- `c-7810d0d4dc28566f` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "If your DPIA decision differs from the views of individuals, you need to document your reasons for disregarding their views."
- `c-7f8cda40039374a9` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "You should also record any reasons for going against the views of individuals or other consultees."
- `c-b42276af26f46574` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "You should ask your DPO for advice. Record whether the measure would reduce or eliminate the risk."
+ 5 more topic claims across 1 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a reason. Re-runnable: prompt sha b441083319fe.

- test: `WHY:c-72b9fa83c03d74eb`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: Prevents non-compliance and records decision-making process.
- partial hits: c-72b9fa83c03d74eb

**Missing element:** a reason

**Reasoning:** 1 key(s) state DPO advice on whether processing is compliant and can go ahead should be sought and documented as part of sign-off; if advice is not followed, reasons must be recorded.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-72b9fa83c03d74eb

### [HEDGE] A DPIA must involve the opinion of the Data Protection Officer and, where appropriate, the point of view of data subjects or their representatives. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-ae629243f4c8b411` [seed] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "Interested parties are involved: The opinion of the DPO is obtained (article 35, paragraph 2); The point of view of the data subjects or their representatives are gathered, where appropriate (article 35, paragraph 9)."
- `c-38cfa9c10f9c0da1` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "Where appropriate, the controller shall seek the views of data subjects or their representatives on the intended processing, without prejudice to the protection of commercial or public interests or the security of processing operations."
- `c-6e0dc7586d6eee18` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "Where appropriate, the controller shall seek the views of data subjects or their representatives on the intended processing, without prejudice to the protection of commercial or public interests or the security of processing operations."
- `c-965c5dbfe1fb8a2f` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "You should consult your data protection officer (if you have one) and, where appropriate, individuals and relevant experts."
- `c-bf045a5c8aabb1c3` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "You should seek and document the views of individuals (or their representatives) unless there is a good reason not to."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of an exception condition. Re-runnable: prompt sha 0c8a5887cfa3.

- test: `HEDGE:c-ae629243f4c8b411`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: Mention exceptions related to commercial, public interests or security.
- partial hits: c-38cfa9c10f9c0da1, c-6e0dc7586d6eee18

**Missing element:** an exception condition

**Reasoning:** 1 key(s) state A DPIA must involve the opinion of the Data Protection Officer and, where appropriate, the point of view of data subjects or their representatives.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test HEDGE:c-ae629243f4c8b411

### [RESULT] review to assess if processing is performed in accordance — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-154ec754e1a92f89` [closure_near] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "Carrying out a DPIA is not a one-time exercise. It is an an on-going process that helps you to manage the risks resulting from a processing. It is important to reevaluate the DPIA when there is a change of the risk represented by the processing operation."
- `c-27af33c5674fc109` [seed] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "Where necessary, the controller shall carry out a review to assess if processing is performed in accordance with the data protection impact assessment at least when there is a change of the risk represented by processing operations."
- `c-1cf8ebc6e7a8070e` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "You need to keep your DPIA under review. You may need to repeat it if there is a substantial change to the nature, scope, context or purposes of your processing."
- `c-a0a6a634ce3d7a7f` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "Where necessary, the controller shall carry out a review to assess if processing is performed in accordance with the data protection impact assessment at least when there is a change of the risk represented by processing operations."
- `c-e31462fe998aaf03` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "Moreover, a DPIA may be necessary as a result of a risk evolution arising from processing operations, for example due to the use of new technology or the use of personal data for different purposes. Processing operations may evolve rapidly and new vulnerabilities may emerge."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'review to assess if processing is performed in accordance'. Re-runnable: prompt sha 97c42b151e18.

- test: `RESULT:c-27af33c5674fc109`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: Some sentences imply or suggest actions but do not explicitly state the result of the test and its meaning.
- partial hits: c-154ec754e1a92f89, c-1cf8ebc6e7a8070e, c-27af33c5674fc109, c-a0a6a634ce3d7a7f, c-e31462fe998aaf03
- synthetic hits (unverified): c-1c49c104ceb158de
- sibling run: partial

**Missing element:** a result-to-interpretation mapping for 'review to assess if processing is performed in accordance'

**Reasoning:** 1 key(s) state review to assess if processing is performed in accordance; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-27af33c5674fc109

### [RESULT] assessment must contain a systematic description of the — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-0e063fb010de21d5` [closure_near] synthetic_extrapolation / documentation, key `ind-s-505312a82b58a1e4`, verdict insufficient — flag: unverified-synthetic: "You must include: a description of the respective roles and responsibilities of any joint controllers or processors; the purposes and methods of the intended processing; the measures and safeguards taken to protect individuals; contact details of your DPO (if you have one); and a copy of the DPIA."
- `c-34a9732142853ea9` [closure_near] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "the measures envisaged to address the risks, including safeguards, security measures and mechanisms to ensure the protection of personal data and to demonstrate compliance with this Regulation taking into account the rights and legitimate interests of data subjects and other persons concerned"
- `c-e43f33dcbd7906c2` [seed] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "The assessment shall contain at least: (a)a systematic description of the envisaged processing operations and the purposes of the processing, including, where applicable, the legitimate interest pursued by the controller"
- `c-fb1459b330b4e176` [closure_near] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "(d)the measures envisaged to address the risks, including safeguards, security measures and mechanisms to ensure the protection of personal data and to demonstrate compliance with this Regulation taking into account the rights and legitimate interests of data subjects and other persons concerned."
- `c-7f0dc02ba850151a` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "a systematic description of the envisaged processing operations and the purposes of the processing, including, where applicable, the legitimate interest pursued by the controller"
- `c-d2cd75d65c7a5378` [topic] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "The purpose of the processing is the reason why you want to process the personal data. This should include: your legitimate interests, where relevant; the intended outcome for individuals; and the expected benefits for you or for society as a whole."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'assessment must contain a systematic description of the'. Re-runnable: prompt sha e58f564e011e.

- test: `RESULT:c-e43f33dcbd7906c2`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: Sentences 5 and 6 partially state expected results by mentioning measures to address risks; sentences 10 states a required element of description.
- partial hits: c-34a9732142853ea9, c-fb1459b330b4e176
- synthetic hits (unverified): c-0e063fb010de21d5
- sibling run: partial

**Missing element:** a result-to-interpretation mapping for 'assessment must contain a systematic description of the'

**Reasoning:** 1 key(s) state assessment must contain a systematic description of the; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-e43f33dcbd7906c2

### [RESULT] measures should be considered when deciding whether to — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-0948649167e1de7b` [closure_near] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "If you have decided to accept a high risk, either because it is not possible to mitigate or because the costs of mitigation are too high, you must consult the ICO before you go ahead with the processing."
- `c-1ab07da9589311e0` [seed] literature_supported / documentation, key `ind-s-505312a82b58a1e4`, verdict supports: "You can take into account the costs and benefits of each measure when deciding whether or not they are appropriate."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'measures should be considered when deciding whether to'. Re-runnable: prompt sha 5653b4629a5a.

- test: `RESULT:c-1ab07da9589311e0`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: Mandatory ICO consultation if high risk accepted due to costs or impossibility.
- partial hits: c-0948649167e1de7b

**Missing element:** a result-to-interpretation mapping for 'measures should be considered when deciding whether to'

**Reasoning:** 1 key(s) state measures should be considered when deciding whether to; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-1ab07da9589311e0

## §7 checks

### §7.1 Anti-renaming: is the map density in disguise?

Computed over lens candidates only (HYP, RG-SINGLE, RG-UNVER, RG-SIBLING, RG-UNDECIDED and closed candidates) -- RG-UNK and CONTROL are excluded, since their density cannot vary.

- `J10(map, D_low)` = 0.00
- `J10(map, D_high)` = 0.10
- Spearman ρ(score, dens) = 0.09
- flags: closure-uninformative

**Matched-density table** (all lens candidates, by `dens` tercile):

| tercile | n | closed | HYP |
|---|---|---|---|
| low | 17 | 9 | 0 |
| mid | 17 | 7 | 1 |
| high | 17 | 11 | 0 |

Top-tercile closed share: 0.65

**Closure rate by `k_topic` band** (all lens candidates):

| band | n | closed | rate |
|---|---|---|---|
| 0-1 | 48 | 25 | 0.52 |
| 2 | 2 | 1 | 0.50 |
| 3-4 | 1 | 1 | 1.00 |
| >=5 | 0 | 0 | 0.00 |

### S2 fair mismatched-evidence control: does the judge close because of the EVIDENCE, or because of the SEED?

Replaces the first (straw-man) control, second adversarial review, 2026-09-29: the old own-evidence arm always carried the seed's own sentences while the mismatched arm never did (17/22 of PLC's old closures cited only the seed or its source), and the mismatched sentences were off-topic (cyclic gap_id pairing). Now BOTH arms keep the seed's own sentences; the OWN arm adds this candidate's own retrieved non-seed-source sentences; the CONTROL arm replaces those with the non-seed-source sentences retrieved for the topically nearest OTHER candidate of the same lens (max seed-stem Jaccard, ties by gap_id). "other-source-only" is the OWN arm with the seed and same-source sentences excluded entirely -- how often an independent source alone closes it. `closure-uninformative` unless own_rate - control_rate >= 0.20 (of candidates); lenses with < 2 candidates are skipped.

| lens | n | own rate | control rate | other-source-only rate | flag |
|---|---|---|---|---|---|
| DISC | 13 | 1.00 | 1.00 | 0.31 | closure-uninformative |
| HEDGE | 5 | 1.00 | 1.00 | 1.00 | closure-uninformative |
| RESULT | 21 | 1.00 | 1.00 | 0.95 | closure-uninformative |
| SEL | 4 | 1.00 | 1.00 | 1.00 | closure-uninformative |
| WHY | 8 | 0.75 | 0.75 | 0.50 | closure-uninformative |
| **total** | 51 | 0.96 | 0.96 | 0.73 | closure-uninformative |

### S2 lexical donor null: why the lexical closure test was replaced

The reviewer's fair donor null for the (now-comparison-only) LEXICAL closure test: self and same-source claims are excluded from both arms, and the donor is the real non-common content stems of a random other-source A claim of the same knowledge type as the seed (`random.Random(0)`, 200 draws). A check "passes" (is informative) only if the observed count is STRICTLY ABOVE the null's 5-95% interval. DISC is excluded (anchor-regex-driven, not stem-overlap); DIAG is handled per its own closure unit (one rival's sign test, not the group).

| lens | observed closed | null mean | null 5-95% | n | flag |
|---|---|---|---|---|---|
| HEDGE | 2 | 0.4 | [0, 2] | 5 | closure-uninformative |
| RESULT | 6 | 8.2 | [5, 11] | 21 | closure-uninformative |
| SEL | 2 | 2.0 | [0, 3] | 4 | closure-uninformative |
| WHY | 1 | 2.0 | [0, 4] | 8 | closure-uninformative |
| **total** | 11 | 12.7 | [8, 17] |  | closure-uninformative |

### Judge-vs-lexical agreement

Confusion counts, `<lexical_state>-><judge_state>`, over every judged candidate (the lexical test no longer decides anything; this is diagnostic only).

| lexical -> judge | n |
|---|---|
| closed->closed | 10 |
| closed->partial | 8 |
| closed->synthetic-closed | 3 |
| open->closed | 8 |
| open->open | 2 |
| open->partial | 8 |
| open->synthetic-closed | 1 |
| partial->closed | 8 |
| partial->partial | 1 |
| synthetic-closed->closed | 1 |
| synthetic-closed->partial | 1 |

### §7.2 Cross-run stability

**this ledger → sibling** (13 open candidate(s)):

- `g-a894f01249ff` [WHY] A DPIA should begin early in a project lifecycle, before processing starts, and run alongside the planning and development process.: counterpart none
- `g-1b1e68dc5d39` [RESULT] measures, new technologies, and novel processing types.: counterpart none
- `g-a34d8523df48` [HEDGE] In most cases, a combination of two factors from the WP29 criteria indicates the need for a DPIA, though this is not a strict rule.: counterpart none
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

**sibling → this ledger** (13 open candidate(s)):

- `g-656818235091` [DISC] relevant controller: counterpart none
- `g-a2821a38f28f` [RESULT] review to assess if processing is performed in accordance: counterpart RG-SINGLE (partial)
- `g-9a3380e70b76` [DISC] vulnerable individual: counterpart none
- `g-42daa2d6e7e1` [HEDGE] In most cases, a data controller can consider that a processing meeting two criteria would require a DPIA to be carried out.: counterpart none
- `g-943c3031fd20` [RESULT] measures to protect people's rights.: counterpart RG-SINGLE (partial)
- `g-6ad618c77e8c` [RESULT] assess whether something is high risk, you need to consider: counterpart none
- `g-5b63f9ad44a6` [WHY] You may be able to justify a decision not to carry out a DPIA if you are confident that the processing is nevertheless unlikely to result in a high risk, but you should document your reasons.: counterpart none
- `g-8f95c18d62b4` [DISC] systematic description: counterpart none
- `g-a677263eb710` [RESULT] assessment must contain a systematic description of the: counterpart RG-SINGLE (partial)
- `g-d2b9d34dbb87` [DISC] appropriate controller: counterpart none
- `g-5c58e8c60b0f` [WHY] The DPIA should be considered as a living tool, not merely as a one-off exercise.: counterpart none
- `g-763a57d498bd` [WHY] A DPIA is NOT required where processing operations do not result in a high risk to the rights and freedoms of individuals.: counterpart none
- `g-e74dc1d1b656` [RESULT] measures put in place, the DPA must be consulted prior to: counterpart none

