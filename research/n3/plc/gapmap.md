# Gap map: PLC intermittent-fault diagnosis

- Ledger: `3d724d8ddfb78f43240f853e7dee8702cd78d72b1d0856e9f1b70be7f90e49bd`
- Config: `35fd0af25618f8d6e0d1c2c3707d7e932afe2ce72dbd01e956034b43bfeb04c1`

## Summary

- **HYP:** 9 total
  - DIAG: 2 (2 moderate)
  - GUARD: 1 (1 narrow)
  - RESULT: 3 (3 narrow)
  - WHY: 3 (3 narrow)
- **Retrieval gaps:** RG-UNK 10, RG-SINGLE 11
- **Control slot:** 1
- **PROMO-excluded seeds (S3 defect 1):** 42
- **§7.1 anti-renaming:** J10(low)=0.00, J10(high)=0.58, ρ(score,dens)=0.91, flags: closure-uninformative

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
| 1 | DIAG | Loose terminal connections are a common cause of | moderate | 3/4 | 7 |
| 2 | DIAG | Race conditions in user logic are a common source of | moderate | 2/4 | 11 |
| 3 | RESULT | tested systematically by observing sensor state, measuring | narrow | 0/4 | 9 |
| 4 | RESULT | capture current sequence state, previous state, command | narrow | 0/4 | 7 |
| 5 | RESULT | review should focus on identifying repeat faults, frequently | narrow | 0/4 | 6 |
| 6 | WHY | When a technician identifies a defect but does not | narrow | 0/4 | 6 |
| 7 | WHY | The 24 VDC supply should be monitored near the affected | narrow | 0/4 | 3 |
| 8 | WHY | An output transistor should not be replaced without first | narrow | 0/4 | 3 |
| 9 | GUARD | A common mistake in troubleshooting intermittent faults is | narrow | 2/4 | 2 |

### #1 [DIAG] Loose terminal connections are a common cause of intermittent PLC faults and

*lens: DIAG; category: HYP*

**OBSERVED EVIDENCE**

- `c-0ae2bfae93f15f20` [rival] literature_supported / documentation, key `ind-s-6c3d0a30ea4db431`, verdict supports: "Next are unwanted interactions, be they ground loops or interactions of multiple processors finding weaknesses in the hardware or software interfaces."
- `c-5f3830d3d244ed5c` [closure_near] synthetic_extrapolation / documentation, key `ind-s-6c3d0a30ea4db431`, verdict insufficient — flag: unverified-synthetic: "Aliasing, often a hardware issue, can be another difficult item to examine. A key clue is seeing a waveform from one system in another system or data at a different time scale."
- `c-8fee4e182a01cf23` [rival] literature_supported / documentation, key `ind-s-6c3d0a30ea4db431`, verdict supports: "Finally, I see interactions related to aliasing in one form or another getting into data."
- `c-afa3a127d0e11d7f` [rival] literature_supported / documentation, key `ind-s-6c3d0a30ea4db431`, verdict supports: "From my experience, intermittent faults are most commonly hardware related either damaged product or a problem with the installation. Software or firmware are root cause in some cases. In reality most software problems are not as intermittent as they may seem."
- `c-b1b2c02c076bda50` [rival] literature_supported / documentation, key `ind-s-1310a1cc1a415572`, verdict supports: "high-frequency noise from VFDs and contactors creates the "phantom faults" that disrupt your logic signals and ruin your production schedule."
- `c-d02882fa30ff11e7` [rival] literature_supported / documentation, key `ind-s-6c3d0a30ea4db431`, verdict supports: "The problem was related to some handshake lines with improper pull-ups and the use of the wrong edge of a clock on one of the processors that reduced the settling time for the handshake line. The stalled processor ended up seeing the remnants of transfer acknowledge for the first processor, aided by a bit of noise."
- `c-d7bce12d16755797` [seed] literature_supported / documentation, key `ind-s-90dc6fdae4a41cc0`, verdict supports: "Loose terminals cause many intermittent faults. A flashlight reveals problems in dark panels that you miss otherwise."
- `c-1a4dbea5c8f1f4fe` [topic] literature_supported / documentation, key `ind-s-1310a1cc1a415572`, verdict supports: "most standard MOV-based protectors are designed for high-voltage surges over 1000V. They stay dormant during the low-level transients that actually disrupt logic. These micro-surges occur thousands of times every single day."
- `c-2271e1237b9ecb46` [topic] literature_supported / documentation, key `ind-s-c84226ca6e967ec6`, verdict supports: "The signals run live onto the display at the line and are recorded in the Peakboard Hub, so availability, downtime durations and OEE stay analysable across weeks."
- `c-2c18d014757182fa` [topic] literature_supported / documentation, key `ind-s-636acef04b884b84`, verdict supports: "Intermittent faults become manageable when the system remembers what people cannot witness. First-out logic, synchronized clocks, event buffers, targeted electrical measurements and disciplined experiments transform "random" into a timeline."
- `c-54069f7826793d86` [topic] literature_supported / documentation, key `ind-s-a3eefeba9e469bb6`, verdict supports: "02The Edge connects read-only One appliance beside the line. No new controllers, no PLC changes, no cloud dependency."
- `c-75037e22b5a75d27` [topic] literature_supported / documentation, key `ind-s-648d381d8594dd5e`, verdict supports: "Check the common terminal voltage first before suspecting the card."
+ 16 more topic claims across 6 keys (full list in gapmap.json)

**INFERRED GAP**

Of 34 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a discriminating sign for: Ground loops and interactions of multiple processors finding weaknesses in; Aliasing in data can be a; by installation problems, while software problems are typically less; by high-frequency electrical noise from VFDs and contactors that creates phantom; Improper pull-up resistors and incorrect clock edge timing in handshake lines. Re-runnable: prompt sha 9c50fb9250a8.

- test: `DIAG:c-d7bce12d16755797`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: c-0ae2bfae93f15f20: Sentence 3 specifically mentions ground loops without referencing interactions of multiple processors.; c-8fee4e182a01cf23: Sentence 3 provides specific details about how aliasing occurs.; c-afa3a127d0e11d7f: Sentences 1 and 4 partially address the distinction but do not explicitly state an observable sign.; c-b1b2c02c076bda50: Sentences 1 and 3 describe high-frequency noise from VFDs and contactors as a cause of phantom faults and signal degradation.; c-d02882fa30ff11e7: mentions improper pull-ups and clock edge timing
- partial hits: c-284b605529c10565, c-ab5b29f488501794, c-afa3a127d0e11d7f, c-b1b2c02c076bda50, c-d02882fa30ff11e7
- synthetic hits (unverified): c-5f3830d3d244ed5c

**HIDDEN-KNOWLEDGE HYPOTHESIS** (label: `inferred` — a prediction, never a fact)

Predicted, not observed: Hypothesis (inferred): practitioners are predicted to tell these rival causes of "Loose terminal connections are a common cause of intermittent PLC faults and" apart by signs; the closure judge found a sign for the following (test DIAG:c-d7bce12d16755797):

- Ground loops and interactions of multiple processors finding weaknesses in (no sign found)
- Aliasing in data can be a (no sign found)
- by installation problems, while software problems are typically less (no sign found)
- by high-frequency electrical noise from VFDs and contactors that creates phantom (no sign found)
- Improper pull-up resistors and incorrect clock edge timing in handshake lines (no sign found)

- predicted knowledge type: interpretation, cue
- predicted tacitness: relational
- channel: CDM probes on a recalled case, then contrasting cases

**Missing element:** a discriminating sign for: Ground loops and interactions of multiple processors finding weaknesses in; Aliasing in data can be a; by installation problems, while software problems are typically less; by high-frequency electrical noise from VFDs and contactors that creates phantom; Improper pull-up resistors and incorrect clock edge timing in handshake lines

**Reasoning:** 1 key(s) state Loose terminal connections are a common cause of intermittent PLC faults and; 7 key(s) discuss the topic; the closure judge found no verified sentence matching test DIAG:c-d7bce12d16755797

**Breadth:** moderate (uncalibrated; no gold) (score 3 = A3 + B0 − P0; k_step=1, k_topic=7); lexical robustness 3/4

**Alternatives:**

- [live] The sign exists but is phrased without the cause's stems. — lexical linking is the binding constraint (§9, §10).
- [live] The causes co-occur, and experts test rather than discriminate. — rival causes need not be mutually exclusive.
- [live] The sign is instrument output, not tacit knowledge. — DISCR also matches instrument-reported signs.

**Expert question** (channel: CDM probes on a recalled case, then contrasting cases):

> Sources list several causes of Loose terminal connections are a common cause of intermittent PLC faults and: "Next are unwanted interactions, be they ground loops or interactions of multiple processors finding weaknesses in the hardware or software interfaces.", "high-frequency noise from VFDs and contactors creates the "phantom faults" that disrupt your logic signals and ruin your production schedule.". Think of the last time you diagnosed Loose terminal connections are a common cause of intermittent PLC faults and. Which cause did you suspect first, and what did you see, hear or measure that let you rule the others out?

### #2 [DIAG] Race conditions in user logic are a common source of intermittent faults in

*(co-located with #1: shares a seed claim)*

*lens: DIAG; category: HYP*

**OBSERVED EVIDENCE**

- `c-0ae2bfae93f15f20` [rival] literature_supported / documentation, key `ind-s-6c3d0a30ea4db431`, verdict supports: "Next are unwanted interactions, be they ground loops or interactions of multiple processors finding weaknesses in the hardware or software interfaces."
- `c-13f98c8939d6f47b` [rival] literature_supported / documentation, key `ind-s-6c3d0a30ea4db431`, verdict supports: "Interconnections at various levels are the most common cause of the faults I see: loose or contaminated connectors, soldering, wire crimping, etc."
- `c-210c933978127214` [closure_near] literature_supported / documentation, key `ind-s-1310a1cc1a415572`, verdict supports: "Loose terminals and oxidized connections are silent killers of signal integrity. They create "jitter" that a PLC processor might interpret as a false state."
- `c-5f3830d3d244ed5c` [closure_near] synthetic_extrapolation / documentation, key `ind-s-6c3d0a30ea4db431`, verdict insufficient — flag: unverified-synthetic: "Aliasing, often a hardware issue, can be another difficult item to examine. A key clue is seeing a waveform from one system in another system or data at a different time scale."
- `c-833c1d48e3a781cd` [closure_near] synthetic_extrapolation / documentation, key `ind-s-90dc6fdae4a41cc0`, verdict insufficient — flag: unverified-synthetic: "Intermittent faults are the hardest problems to diagnose. These appear randomly, making systematic testing difficult. Thermal issues cause intermittent behavior as components heat and cool. Loose connections create random failures from vibration."
- `c-8fee4e182a01cf23` [rival] literature_supported / documentation, key `ind-s-6c3d0a30ea4db431`, verdict supports: "Finally, I see interactions related to aliasing in one form or another getting into data."
- `c-afa3a127d0e11d7f` [rival] literature_supported / documentation, key `ind-s-6c3d0a30ea4db431`, verdict supports: "From my experience, intermittent faults are most commonly hardware related either damaged product or a problem with the installation. Software or firmware are root cause in some cases. In reality most software problems are not as intermittent as they may seem."
- `c-d02882fa30ff11e7` [rival] literature_supported / documentation, key `ind-s-6c3d0a30ea4db431`, verdict supports: "The problem was related to some handshake lines with improper pull-ups and the use of the wrong edge of a clock on one of the processors that reduced the settling time for the handshake line. The stalled processor ended up seeing the remnants of transfer acknowledge for the first processor, aided by a bit of noise."
- `c-dd7c2f8526ff98cf` [rival] literature_supported / documentation, key `ind-s-90dc6fdae4a41cc0`, verdict supports: "Consider environmental factors. Temperature extremes, humidity, vibration, and electrical noise cause intermittent faults that seem random. In my experience, problems appearing only in summer heat or winter cold often trace to marginal components or inadequate panel cooling."
- `c-dde847bfa2cea027` [rival] literature_supported / documentation, key `ind-s-aab556b0ece4b264`, verdict supports: "If Trend_Idx ever reaches 600 while a MOV runs, the controller takes a major fault, type 4 code 20, array subscript out of range"
- `c-ec36686ad589464b` [seed] literature_supported / documentation, key `ind-s-6c3d0a30ea4db431`, verdict supports: "In a motion controller or PLC, it's often race conditions in user logic."
- `c-05ffecbae90b2aa5` [topic] literature_supported / documentation, key `ind-s-6c3d0a30ea4db431`, verdict supports: "Physical stress on cabling and connectors as well as vibration and thermal cycling (heat gun and freeze spray) can often chase out wiring and soldering issues."
- `c-2271e1237b9ecb46` [topic] literature_supported / documentation, key `ind-s-c84226ca6e967ec6`, verdict supports: "The signals run live onto the display at the line and are recorded in the Peakboard Hub, so availability, downtime durations and OEE stay analysable across weeks."
- `c-284b605529c10565` [topic] literature_supported / documentation, key `ind-s-1310a1cc1a415572`, verdict supports: "You must ensure shielded cables are grounded at one end only to prevent ground loops. These loops introduce noise into sensitive logic circuits and are a primary source of frustration during the process of troubleshooting intermittent plc faults."
- `c-3f9f449f1a84461f` [topic] literature_supported / documentation, key `ind-s-636acef04b884b84`, verdict supports: "Add assertions or diagnostic codes at impossible transitions. If the code cannot explain how it reached the captured state, its observability or state model needs improvement."
- `c-44f1385b3ecc160b` [topic] literature_supported / documentation, key `ind-s-a55566b18355e540`, verdict supports: "Define controlled maintenance types and statuses Start with a short list that people can apply consistently. Preventive maintenance, corrective repair, inspection, calibration, warranty, and recall may be enough. Status might be open, scheduled, complete, deferred, and canceled."
+ 13 more topic claims across 10 keys (full list in gapmap.json)

**INFERRED GAP**

Of 50 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a discriminating sign for: Ground loops and interactions of multiple processors finding weaknesses in; Loose or contaminated connectors, soldering defects, and wire crimping issues; Aliasing in data can be a; by installation problems, while software problems are typically less; Improper pull-up resistors and incorrect clock edge timing in handshake lines; Environmental factors such as temperature extremes, humidity, vibration, and; array subscript out of range.. Re-runnable: prompt sha 2f10f4648482.

- test: `DIAG:c-ec36686ad589464b`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: c-0ae2bfae93f15f20: Sentence 3 specifically mentions ground loops without referencing interactions of multiple processors.; c-13f98c8939d6f47b: Loose connections create random failures from vibration.; c-8fee4e182a01cf23: Sentence 3 provides specific details about how aliasing occurs.; c-afa3a127d0e11d7f: Sentences 1 and 4 partially address the distinction but do not explicitly state an observable sign.; c-d02882fa30ff11e7: mentions improper pull-ups and clock edge timing; c-dd7c2f8526ff98cf: Sentences 1 and 3 list environmental factors but do not distinguish them from other causes.; c-dde847bfa2cea027: Sentences 1 and 2 directly state the fault cause.
- partial hits: c-210c933978127214, c-284b605529c10565, c-afa3a127d0e11d7f, c-d02882fa30ff11e7, c-dd7c2f8526ff98cf, c-dde847bfa2cea027
- synthetic hits (unverified): c-5f3830d3d244ed5c, c-833c1d48e3a781cd

**HIDDEN-KNOWLEDGE HYPOTHESIS** (label: `inferred` — a prediction, never a fact)

Predicted, not observed: Hypothesis (inferred): practitioners are predicted to tell these rival causes of "Race conditions in user logic are a common source of intermittent faults in" apart by signs; the closure judge found a sign for the following (test DIAG:c-ec36686ad589464b):

- Ground loops and interactions of multiple processors finding weaknesses in (no sign found)
- Loose or contaminated connectors, soldering defects, and wire crimping issues (no sign found)
- Aliasing in data can be a (no sign found)
- by installation problems, while software problems are typically less (no sign found)
- Improper pull-up resistors and incorrect clock edge timing in handshake lines (no sign found)
- Environmental factors such as temperature extremes, humidity, vibration, and (no sign found)
- array subscript out of range. (no sign found)

- predicted knowledge type: interpretation, cue
- predicted tacitness: relational
- channel: CDM probes on a recalled case, then contrasting cases

**Missing element:** a discriminating sign for: Ground loops and interactions of multiple processors finding weaknesses in; Loose or contaminated connectors, soldering defects, and wire crimping issues; Aliasing in data can be a; by installation problems, while software problems are typically less; Improper pull-up resistors and incorrect clock edge timing in handshake lines; Environmental factors such as temperature extremes, humidity, vibration, and; array subscript out of range.

**Reasoning:** 1 key(s) state Race conditions in user logic are a common source of intermittent faults in; 11 key(s) discuss the topic; the closure judge found no verified sentence matching test DIAG:c-ec36686ad589464b

**Breadth:** moderate (uncalibrated; no gold) (score 3 = A3 + B0 − P0; k_step=1, k_topic=11); lexical robustness 2/4

**Alternatives:**

- [live] The sign exists but is phrased without the cause's stems. — lexical linking is the binding constraint (§9, §10).
- [live] The causes co-occur, and experts test rather than discriminate. — rival causes need not be mutually exclusive.
- [live] The sign is instrument output, not tacit knowledge. — DISCR also matches instrument-reported signs.

**Expert question** (channel: CDM probes on a recalled case, then contrasting cases):

> Sources list several causes of Race conditions in user logic are a common source of intermittent faults in: "Next are unwanted interactions, be they ground loops or interactions of multiple processors finding weaknesses in the hardware or software interfaces.", "Temperature extremes, humidity, vibration, and electrical noise cause intermittent faults that seem random.". Think of the last time you diagnosed Race conditions in user logic are a common source of intermittent faults in. Which cause did you suspect first, and what did you see, hear or measure that let you rule the others out?

### #3 [RESULT] tested systematically by observing sensor state, measuring

*lens: RESULT; category: HYP*

**OBSERVED EVIDENCE**

- `c-7cbb98d224149a80` [seed] literature_supported / documentation, key `ind-s-90dc6fdae4a41cc0`, verdict supports: "Testing inputs systematically follows a clear pattern. Observe the actual sensor state physically. Measure voltage or current at the PLC terminal with a multimeter. Check if the PLC input shows the correct state in online monitoring. Verify that program logic uses this input correctly."
- `c-17c2de65f3f17ed3` [topic] literature_supported / documentation, key `ind-s-a013254b36b7055a`, verdict supports: "Before using the multimeter, verify: Correct function selected Correct range selected Leads in correct ports Probe tips in good condition Insulation not damaged Meter CAT rating is appropriate Meter battery is good Display works properly"
- `c-209a6be7d470b160` [topic] literature_supported / documentation, key `ind-s-54ea3e1f81e8133a`, verdict supports: "For each important test it explains: CHECK - What to verify WHY - Why the test matters EXPECTED - What normal behavior should look like IF YES - What the result suggests IF NO - What the result suggests"
- `c-210c933978127214` [topic] literature_supported / documentation, key `ind-s-1310a1cc1a415572`, verdict supports: "Loose terminals and oxidized connections are silent killers of signal integrity. They create "jitter" that a PLC processor might interpret as a false state."
- `c-2271e1237b9ecb46` [topic] literature_supported / documentation, key `ind-s-c84226ca6e967ec6`, verdict supports: "The signals run live onto the display at the line and are recorded in the Peakboard Hub, so availability, downtime durations and OEE stay analysable across weeks."
- `c-2ec7925ad29b0ba4` [topic] literature_supported / documentation, key `ind-s-be55778a2f55bf4f`, verdict supports: "Condition monitoring through continuous alarm and signal analysis gives your maintenance team an earlier view into PLC health, so repairs can be scheduled before a failure forces the issue."
+ 14 more topic claims across 9 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'tested systematically by observing sensor state, measuring'. Re-runnable: prompt sha 191f23fffab3.

- test: `RESULT:c-7cbb98d224149a80`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: Sentence 1 describes the testing process but does not specify expected results or actions.
- partial hits: c-7cbb98d224149a80

**HIDDEN-KNOWLEDGE HYPOTHESIS** (label: `inferred` — a prediction, never a fact)

Predicted, not observed: Hypothesis (inferred): practitioners are predicted to read the result of 'tested systematically by observing sensor state, measuring' against expected values and map it to the next action; no verified claim in this ledger matched test RESULT:c-7cbb98d224149a80.

- predicted knowledge type: interpretation, expectancy
- predicted tacitness: relational
- channel: CDM probes on a recalled case; process tracing

**Missing element:** a result-to-interpretation mapping for 'tested systematically by observing sensor state, measuring'

**Reasoning:** 1 key(s) state tested systematically by observing sensor state, measuring; 9 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-7cbb98d224149a80

**Breadth:** narrow (uncalibrated; no gold) (score 2 = A3 + B0 − P1; k_step=1, k_topic=9); lexical robustness 0/4

**Alternatives:**

- [live] The interpretation is stated in paraphrase without the seed's stems. — the stem-overlap test cannot see a paraphrase (the same limitation as DISC, §9).
- [live] The test is a formality with a binary outcome. — not every prescribed test feeds a real branching decision.
- [live] The interpretation is instrument-given. — a displayed pass/fail reading needs no practitioner interpretation.

**Expert question** (channel: CDM probes on a recalled case; process tracing):

> Sources prescribe: "Verify that program logic uses this input correctly.". Think of the last time you did this. What result did you get, what had you expected, what did that result make you do next -- and what result would have sent you down a different path?

### #4 [RESULT] capture current sequence state, previous state, command

*lens: RESULT; category: HYP*

**OBSERVED EVIDENCE**

- `c-3989533d8865691e` [seed] literature_supported / documentation, key `ind-s-636acef04b884b84`, verdict supports: "Store current sequence state, previous state, command source, permissive status, input word, output word and key analog values."
- `c-37e4c2df5a671ff3` [topic] literature_supported / documentation, key `ind-s-c84226ca6e967ec6`, verdict supports: "Machine monitoring is the continuous capture and display of the operating state of production machines."
- `c-4cb402666ee92c71` [topic] literature_supported / documentation, key `ind-s-aab556b0ece4b264`, verdict supports: "a 10 ms periodic task writing eight tags into a 600-element ring, a trigger on the fault bit, 200 more samples, then a latch that stops the writer until somebody has read the result. Four rungs. About 7 KB of memory."
- `c-4f0da260240d02f7` [topic] literature_supported / documentation, key `ind-s-648d381d8594dd5e`, verdict supports: "Check the sensor datasheet: it's a solid-state PNP output with a rated leakage current of 0.5 mA at 24 V supply. Calculate the leakage voltage: 0.5 mA through the 10 kΩ input impedance of the card = 5 V. Enough to keep a borderline input energised."
- `c-524652f455ef640a` [topic] literature_supported / documentation, key `ind-s-636acef04b884b84`, verdict supports: "For very fast phenomena, ordinary timestamps are insufficient. Use high-speed input capture, sequence-of-events modules, power-quality instruments or an oscilloscope appropriate to the circuit."
- `c-5707c242d1c1bccc` [topic] literature_supported / documentation, key `ind-s-a013254b36b7055a`, verdict supports: "One of the most dangerous mistakes is placing the meter in current mode across a voltage source. That can create a direct short through the meter."
+ 6 more topic claims across 7 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'capture current sequence state, previous state, command'. Re-runnable: prompt sha d0e733afa745.

- test: `RESULT:c-3989533d8865691e`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: Sentence 4 suggests actions to consider but does not explicitly state expected results or next actions.
- partial hits: c-d12e92b51fca73b5

**HIDDEN-KNOWLEDGE HYPOTHESIS** (label: `inferred` — a prediction, never a fact)

Predicted, not observed: Hypothesis (inferred): practitioners are predicted to read the result of 'capture current sequence state, previous state, command' against expected values and map it to the next action; no verified claim in this ledger matched test RESULT:c-3989533d8865691e.

- predicted knowledge type: interpretation, expectancy
- predicted tacitness: relational
- channel: CDM probes on a recalled case; process tracing

**Missing element:** a result-to-interpretation mapping for 'capture current sequence state, previous state, command'

**Reasoning:** 1 key(s) state capture current sequence state, previous state, command; 7 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-3989533d8865691e

**Breadth:** narrow (uncalibrated; no gold) (score 2 = A3 + B0 − P1; k_step=1, k_topic=7); lexical robustness 0/4

**Alternatives:**

- [live] The interpretation is stated in paraphrase without the seed's stems. — the stem-overlap test cannot see a paraphrase (the same limitation as DISC, §9).
- [live] The test is a formality with a binary outcome. — not every prescribed test feeds a real branching decision.
- [live] The interpretation is instrument-given. — a displayed pass/fail reading needs no practitioner interpretation.

**Expert question** (channel: CDM probes on a recalled case; process tracing):

> Sources prescribe: "Store current sequence state, previous state, command source, permissive status, input word, output word and key analog values.". Think of the last time you did this. What result did you get, what had you expected, what did that result make you do next -- and what result would have sent you down a different path?

### #5 [RESULT] review should focus on identifying repeat faults, frequently

*lens: RESULT; category: HYP*

**OBSERVED EVIDENCE**

- `c-46de7dc2c16e7b7b` [seed] literature_supported / documentation, key `ind-s-85e244f1abe530b7`, verdict supports: "Look for repeat faults, parts that fail too often, assets that absorb too many labor hours, and work orders that keep ending with "monitor." Those are usually signs that the problem hasn't been solved, only deferred."
- `c-08e44983c76a7bcd` [topic] literature_supported / documentation, key `ind-s-038f6d95bef84e11`, verdict supports: "Aggregation. Calculating MTBF, PM compliance, or labor cost per asset from paper is impractical."
- `c-186e4bb7f806fcdf` [topic] literature_supported / documentation, key `ind-s-3dd72067dd4ff05e`, verdict supports: "Good: "PRS-004, 2026-07-18, corrective, bearing 6205-2RS replaced after seizure on startup, 3.5 hrs downtime, J. Alvarez.""
- `c-2b7414660cc8d118` [topic] literature_supported / documentation, key `ind-s-c84226ca6e967ec6`, verdict supports: "patterns surface that a snapshot cannot show - such as the same asset failing in the same shift again and again."
- `c-466826867f701bb4` [topic] literature_supported / documentation, key `ind-s-85e244f1abe530b7`, verdict supports: "Logs create value when someone reviews them with intent. That review doesn't need to be dramatic. It does need to be regular."
- `c-4a2735242356a648` [topic] literature_supported / documentation, key `ind-s-a55566b18355e540`, verdict supports: "At an agreed cadence, review overdue next actions, unresolved defects, missing evidence, repeat repairs, rising cost, and unusual downtime."
+ 8 more topic claims across 6 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'review should focus on identifying repeat faults, frequently'. Re-runnable: prompt sha a3260b235c34.

- test: `RESULT:c-46de7dc2c16e7b7b`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: Sentence 2 implies next actions by suggesting signs of unresolved issues.
- partial hits: c-46de7dc2c16e7b7b

**HIDDEN-KNOWLEDGE HYPOTHESIS** (label: `inferred` — a prediction, never a fact)

Predicted, not observed: Hypothesis (inferred): practitioners are predicted to read the result of 'review should focus on identifying repeat faults, frequently' against expected values and map it to the next action; no verified claim in this ledger matched test RESULT:c-46de7dc2c16e7b7b.

- predicted knowledge type: interpretation, expectancy
- predicted tacitness: relational
- channel: CDM probes on a recalled case; process tracing

**Missing element:** a result-to-interpretation mapping for 'review should focus on identifying repeat faults, frequently'

**Reasoning:** 1 key(s) state review should focus on identifying repeat faults, frequently; 6 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-46de7dc2c16e7b7b

**Breadth:** narrow (uncalibrated; no gold) (score 2 = A3 + B0 − P1; k_step=1, k_topic=6); lexical robustness 0/4

**Alternatives:**

- [live] The interpretation is stated in paraphrase without the seed's stems. — the stem-overlap test cannot see a paraphrase (the same limitation as DISC, §9).
- [live] The test is a formality with a binary outcome. — not every prescribed test feeds a real branching decision.
- [live] The interpretation is instrument-given. — a displayed pass/fail reading needs no practitioner interpretation.

**Expert question** (channel: CDM probes on a recalled case; process tracing):

> Sources prescribe: "Look for repeat faults, parts that fail too often, assets that absorb too many labor hours, and work orders that keep ending with "monitor." Those are usually signs that the problem hasn't been solved, only deferred.". Think of the last time you did this. What result did you get, what had you expected, what did that result make you do next -- and what result would have sent you down a different path?

### #6 [WHY] When a technician identifies a defect but does not immediately repair it, the finding should be recorded as an open next action rather than written as a resolved maintenance event.

*lens: WHY; category: HYP*

**OBSERVED EVIDENCE**

- `c-478869a71c059f4d` [seed] literature_supported / documentation, key `ind-s-a55566b18355e540`, verdict supports: "If a technician notices a leak but does not repair it, record the finding as an open next action. Do not write it as though the maintenance event resolved the issue."
- `c-099467b81e3870ec` [topic] literature_supported / documentation, key `ind-s-636acef04b884b84`, verdict supports: "Under production pressure, teams may replace a sensor, move a cable, edit a timer and reset a drive simultaneously. If the fault disappears, nobody knows which action mattered."
- `c-47a2a29c52f7d738` [topic] literature_supported / documentation, key `ind-s-85e244f1abe530b7`, verdict supports: "If a machine fails once, you repair it. If it fails the same way repeatedly, your log should force a different conversation."
- `c-4a2735242356a648` [topic] literature_supported / documentation, key `ind-s-a55566b18355e540`, verdict supports: "At an agreed cadence, review overdue next actions, unresolved defects, missing evidence, repeat repairs, rising cost, and unusual downtime."
- `c-6f7b1229acfed054` [topic] literature_supported / documentation, key `ind-s-3dd72067dd4ff05e`, verdict supports: "An equipment maintenance log records every service, inspection, and repair performed on a piece of equipment - what was done, when, by whom, and what's due next."
- `c-d12e92b51fca73b5` [topic] literature_supported / documentation, key `ind-s-54ea3e1f81e8133a`, verdict supports: "The Agent will not immediately conclude that the VFD or motor is defective. It may investigate: whether the PLC RUN command remains active; motor current before the trip; mechanical load; drive temperature; acceleration parameters; motor data configuration; whether the fault correlates with temperature or operating time."
+ 2 more topic claims across 6 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a reason. Re-runnable: prompt sha beb4350e0b76.

- test: `WHY:c-478869a71c059f4d`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: Simultaneous changes prevent determining which action resolved the fault.
- partial hits: c-099467b81e3870ec

**HIDDEN-KNOWLEDGE HYPOTHESIS** (label: `inferred` — a prediction, never a fact)

Predicted, not observed: Hypothesis (inferred): practitioners are predicted to know why 'When a technician identifies a defect but does not immediately repair it, the finding should be recorded as an open next action rather than written as a resolved maintenance event.'; no verified claim in this ledger matched test WHY:c-478869a71c059f4d.

- predicted knowledge type: rationale
- predicted tacitness: relational
- channel: a targeted confirmation question

**Missing element:** a reason

**Reasoning:** 1 key(s) state When a technician identifies a defect but does not immediately repair it, the finding should be recorded as an open next action rather than written as a resolved maintenance event.; 6 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-478869a71c059f4d

**Breadth:** narrow (uncalibrated; no gold) (score 2 = A3 + B0 − P1; k_step=1, k_topic=6); lexical robustness 0/4

**Alternatives:**

- [live] The rationale is a purpose clause that RAT does not match. — RAT does not match every 'to identify...' purpose clause.
- [not live] The source is promotional. — no PROMO lexicon hit on the span; no ledger field marks promotional voice (§10).
- [live] The reason is trivial safety knowledge. — an omitted rationale may simply be too obvious to state.

**Expert question** (channel: a targeted confirmation question):

> Sources say: "If a technician notices a leak but does not repair it, record the finding as an open next action.". What would happen if someone did it differently, and in what situations, if any, is doing it differently acceptable?

### #7 [WHY] The 24 VDC supply should be monitored near the affected load, not only at the power supply terminals, to investigate power and grounding issues.

*lens: WHY; category: HYP*

**OBSERVED EVIDENCE**

- `c-17f61d2caa7a2b6c` [seed] literature_supported / documentation, key `ind-s-636acef04b884b84`, verdict supports: "Monitor the 24 VDC supply near the affected load, not only at the power supply terminals."
- `c-711f7a6d18e542e0` [topic] literature_supported / documentation, key `ind-s-636acef04b884b84`, verdict supports: "Check loading, inrush, loose terminals, protective-device behavior and shared commons."
- `c-933e695c5b497d18` [topic] literature_supported / documentation, key `ind-s-a013254b36b7055a`, verdict supports: "If the output LED is ON but the meter reads 0 VDC at the terminal, check the output common, fuse, or field power."
- `c-dfa41772e603c5af` [topic] literature_supported / documentation, key `ind-s-648d381d8594dd5e`, verdict supports: "Solution: add a 2.2 kΩ bleed resistor across the input terminal to 0 V. This drops the leakage voltage to under 1 V, well below the OFF threshold."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 2e9ad3c97612.

- test: `WHY:c-17f61d2caa7a2b6c`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: to investigate power and grounding issues

**HIDDEN-KNOWLEDGE HYPOTHESIS** (label: `inferred` — a prediction, never a fact)

Predicted, not observed: Hypothesis (inferred): practitioners are predicted to know why 'The 24 VDC supply should be monitored near the affected load, not only at the power supply terminals, to investigate power and grounding issues.'; no verified claim in this ledger matched test WHY:c-17f61d2caa7a2b6c.

- predicted knowledge type: rationale
- predicted tacitness: relational
- channel: a targeted confirmation question

**Missing element:** a reason

**Reasoning:** 1 key(s) state The 24 VDC supply should be monitored near the affected load, not only at the power supply terminals, to investigate power and grounding issues.; 3 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-17f61d2caa7a2b6c

**Breadth:** narrow (uncalibrated; no gold) (score 2 = A2 + B0 − P0; k_step=1, k_topic=3); lexical robustness 0/4

**Alternatives:**

- [live] The rationale is a purpose clause that RAT does not match. — RAT does not match every 'to identify...' purpose clause.
- [not live] The source is promotional. — no PROMO lexicon hit on the span; no ledger field marks promotional voice (§10).
- [live] The reason is trivial safety knowledge. — an omitted rationale may simply be too obvious to state.

**Expert question** (channel: a targeted confirmation question):

> Sources say: "Monitor the 24 VDC supply near the affected load, not only at the power supply terminals.". What would happen if someone did it differently, and in what situations, if any, is doing it differently acceptable?

### #8 [WHY] An output transistor should not be replaced without first verifying the load coil resistance, as a shorted coil will destroy the replacement card.

*lens: WHY; category: HYP*

**OBSERVED EVIDENCE**

- `c-6726d5a93c8ce8da` [seed] literature_supported / documentation, key `ind-s-648d381d8594dd5e`, verdict supports: "Replacing a dead output transistor without checking the load coil resistance first. A shorted coil will kill the replacement card just as fast."
- `c-5680e1d77483e8c3` [topic] literature_supported / documentation, key `ind-s-648d381d8594dd5e`, verdict supports: "If you read full supply voltage but the device does not run, the fault is in the load circuit: broken wire, open coil, or a missing return path."
- `c-b4064c9f263ef5c2` [topic] literature_supported / documentation, key `ind-s-a013254b36b7055a`, verdict supports: "A coil reads extremely low resistance. Possible conclusion: The coil may be shorted."
- `c-d8cf21cb2e1bac98` [topic] literature_supported / documentation, key `ind-s-90dc6fdae4a41cc0`, verdict supports: "Outputs working sometimes but not consistently often trace to blown fuses, marginal output cards, or loose terminal connections. The output might work for small loads but fail under full load current."
- `c-c28a73af0a0b4536` [topic] literature_supported / documentation, key `ind-s-a013254b36b7055a`, verdict supports: "A solenoid coil reads open/infinite resistance. Possible conclusion: The coil is open and may be failed."
- `c-dcdfe8e233c2abcf` [topic] literature_supported / documentation, key `ind-s-648d381d8594dd5e`, verdict supports: "A reading close to zero means a shorted coil that may have already killed the output transistor."
+ 2 more topic claims across 3 keys (full list in gapmap.json)

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a reason. Re-runnable: prompt sha ca0430bd0dc9.

- test: `WHY:c-6726d5a93c8ce8da`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: to prevent destruction of replacement card
- partial hits: c-6726d5a93c8ce8da, c-b4064c9f263ef5c2, c-dcdfe8e233c2abcf

**HIDDEN-KNOWLEDGE HYPOTHESIS** (label: `inferred` — a prediction, never a fact)

Predicted, not observed: Hypothesis (inferred): practitioners are predicted to know why 'An output transistor should not be replaced without first verifying the load coil resistance, as a shorted coil will destroy the replacement card.'; no verified claim in this ledger matched test WHY:c-6726d5a93c8ce8da.

- predicted knowledge type: rationale
- predicted tacitness: relational
- channel: a targeted confirmation question

**Missing element:** a reason

**Reasoning:** 1 key(s) state An output transistor should not be replaced without first verifying the load coil resistance, as a shorted coil will destroy the replacement card.; 3 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-6726d5a93c8ce8da

**Breadth:** narrow (uncalibrated; no gold) (score 1 = A2 + B0 − P1; k_step=1, k_topic=3); lexical robustness 0/4

**Alternatives:**

- [live] The rationale is a purpose clause that RAT does not match. — RAT does not match every 'to identify...' purpose clause.
- [not live] The source is promotional. — no PROMO lexicon hit on the span; no ledger field marks promotional voice (§10).
- [live] The reason is trivial safety knowledge. — an omitted rationale may simply be too obvious to state.

**Expert question** (channel: a targeted confirmation question):

> Sources say: "Replacing a dead output transistor without checking the load coil resistance first.". What would happen if someone did it differently, and in what situations, if any, is doing it differently acceptable?

### #9 [GUARD] A common mistake in troubleshooting intermittent faults is panicking and abandoning systematic approaches in favor of quick fixes.

*lens: GUARD; category: HYP*

**OBSERVED EVIDENCE**

- `c-e9e5424e36fdc18c` [seed] literature_supported / documentation, key `ind-s-6c3d0a30ea4db431`, verdict supports: "They sometimes panic and give up before actually trying to find the fault. Or, in an effort to fix something quickly, they take the shotgun approach and miss some obvious things that a more systematic approach would uncover."
- `c-e49d7ece8c90d13f` [topic] literature_supported / documentation, key `ind-s-54ea3e1f81e8133a`, verdict supports: "QUICK Designed for clearly defined faults where fast troubleshooting is the priority. Examples: Motor does not start Known VFD alarm Sensor permanently active Device offline after replacement Communication fault after maintenance"

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a detection cue. Re-runnable: prompt sha 5be098206307.

- test: `GUARD:c-e9e5424e36fdc18c`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: Sentences 1 and 2 hint at noticing before or as it happens through describing panic and abandoning systematic approaches.
- partial hits: c-e9e5424e36fdc18c

**HIDDEN-KNOWLEDGE HYPOTHESIS** (label: `inferred` — a prediction, never a fact)

Predicted, not observed: Hypothesis (inferred): practitioners are predicted to notice A common mistake in troubleshooting intermittent faults is panicking and abandoning systematic approaches in favor of quick fixes. before or as it happens by a check that no verified claim in this ledger matched test GUARD:c-e9e5424e36fdc18c for. This is an expert-reported error, not an observed learner difficulty.

- predicted knowledge type: check, metacognition
- predicted tacitness: automated
- channel: observation or process tracing first, a retrospective probe over a recorded trace second

**Missing element:** a detection cue

**Reasoning:** 1 key(s) state A common mistake in troubleshooting intermittent faults is panicking and abandoning systematic approaches in favor of quick fixes.; 2 key(s) discuss the topic; the closure judge found no verified sentence matching test GUARD:c-e9e5424e36fdc18c

**Breadth:** narrow (uncalibrated; no gold) (score 0 = A1 + B0 − P1; k_step=1, k_topic=2); lexical robustness 2/4

**Alternatives:**

- [live] The cue is stated in paraphrase. — DETECT is a fixed lexicon.
- [not live] The error is a vendor framing, not a practitioner error. — no PROMO lexicon hit on the span; no ledger field marks promotional voice (§10).
- [live] The guard is organisational (a checklist or procedure), not cognitive. — a procedural guard need not be an internalised cue.

**Expert question** (channel: observation or process tracing first, a retrospective probe over a recorded trace second (weak channel for this knowledge type)):

> "Or, in an effort to fix something quickly, they take the shotgun approach and miss some obvious things that a more systematic approach would uncover.". Think of the last time you or a colleague nearly did this or just had. What made you notice? What did you look at?

## Control slot

The §14.2 unknown-unknowns guard: an area no hypothesis touched, walked cold.

### Documentation and Historical Analysis

*lens: —; category: CONTROL*

**OBSERVED EVIDENCE**

(none)

**INFERRED GAP**

Control slot: area 'Documentation and Historical Analysis' (a-8c10790bb9b3111b) has no HYP record and the highest attested share (0.76) among candidate areas of ledger 3d724d8d.

- test: `CONTROL:a-8c10790bb9b3111b`; state: open (closure judge: )

**Reasoning:** the §14.2 unknown-unknowns guard: no HYP touches this area

**Breadth:** narrow (uncalibrated; no gold) (score 0 = A0 + B0 − P0; k_step=0, k_topic=0); lexical robustness 0/4

**Expert question** (channel: control):

> Walk me through how you carry out Documentation and Historical Analysis, from start to finish, as if I were watching you do it. What do you check, and in what order?

## Retrieval gaps

Not hypotheses: each one's action is to search further or verify a synthetic span, never to ask an expert.

### RG-UNK: slots searched, nothing found

| area | slot / question | source |
|---|---|---|
| Documentation and Historical Analysis | What observable features of a situation signal that Documentation and Historical Analysis applies or | ledger U claim `c-897edf646766f84b` |
| PLC Fault Diagnosis Methods | What counts as acceptable or sufficient work in PLC Fault Diagnosis Methods? | ledger U claim `c-db6661bccfa657bd` |
| Documentation and Historical Analysis | decision slot searched, nothing found | sidecar slot |
| Systematic Troubleshooting Frameworks | What observable features of a situation signal that Systematic Troubleshooting Frameworks applies or | ledger U claim `c-674d3b04ba4d0e44` |
| Systematic Troubleshooting Frameworks | cue slot searched, nothing found | sidecar slot |
| Electrical and Hardware Testing | rationale slot searched, nothing found | sidecar slot |
| Electrical and Hardware Testing | Why is Electrical and Hardware Testing done the way it is? | ledger U claim `c-f98231397170b343` |
| Documentation and Historical Analysis | What conditions determine which option is chosen in Documentation and Historical Analysis? | ledger U claim `c-08791488943acc4f` |
| PLC Fault Diagnosis Methods | norm slot searched, nothing found | sidecar slot |
| Documentation and Historical Analysis | cue slot searched, nothing found | sidecar slot |

### [WHY] Competent technicians should not mask a power problem by increasing software delays until the electrical cause is understood. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-999231909ad2e610` [seed] literature_supported / documentation, key `ind-s-636acef04b884b84`, verdict supports: "Do not mask a power problem by increasing software delays until the electrical cause is understood."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 541880e335ad.

- test: `WHY:c-999231909ad2e610`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: to prevent misunderstanding of intermittent faults

**Missing element:** a reason

**Reasoning:** 1 key(s) state Competent technicians should not mask a power problem by increasing software delays until the electrical cause is understood.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-999231909ad2e610

### [WHY] Sampling rate should be chosen according to the suspected event, not according to convenient historian defaults. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-5a47287dab362e5a` [seed] literature_supported / documentation, key `ind-s-636acef04b884b84`, verdict supports: "Choose sampling according to the suspected event, not according to convenient historian defaults."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha d6cd7514cbaf.

- test: `WHY:c-5a47287dab362e5a`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: prevents failure to capture critical events

**Missing element:** a reason

**Reasoning:** 1 key(s) state Sampling rate should be chosen according to the suspected event, not according to convenient historian defaults.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-5a47287dab362e5a

### [WHY] GMP-regulated industries should retain maintenance records for a minimum of 5-7 years, often for the life of the product. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-8df1e3c63d6a6d37` [seed] literature_supported / documentation, key `ind-s-038f6d95bef84e11`, verdict supports: "GMP-regulated industries: 5-7 years minimum, often for the life of the product."

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found none stating a reason. Re-runnable: prompt sha 2db456a438e2.

- test: `WHY:c-8df1e3c63d6a6d37`; state: open (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: 3} Too often repair technicians are placed under pressure to not necessarily find the root cause, but simply to get the equipment running again.

**Missing element:** a reason

**Reasoning:** 1 key(s) state GMP-regulated industries should retain maintenance records for a minimum of 5-7 years, often for the life of the product.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-8df1e3c63d6a6d37

### [RESULT/WHY] captured with a timestamp and not overwritten until — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-73c4b9fa7701d4a7` [seed] literature_supported / documentation, key `ind-s-636acef04b884b84`, verdict supports: "Preserve the first event Secondary alarms can appear milliseconds after the initiating condition. Capture the first-out fault with a timestamp and do not overwrite it until an authorized reset."

**[RESULT]**

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'captured with a timestamp and not overwritten until'. Re-runnable: prompt sha 699a5f0e4594.

- test: `RESULT:c-73c4b9fa7701d4a7`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: Sentences 1 and 3 describe expected behavior but do not explicitly state results or next actions.
- partial hits: c-73c4b9fa7701d4a7

**Missing element:** a result-to-interpretation mapping for 'captured with a timestamp and not overwritten until'

**Reasoning:** 1 key(s) state captured with a timestamp and not overwritten until; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-73c4b9fa7701d4a7

**[WHY]**

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a reason. Re-runnable: prompt sha ff842dc1d358.

- test: `WHY:c-73c4b9fa7701d4a7`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: Preserves initial conditions for accurate analysis and measurement.
- partial hits: c-037aaebe7854868f, c-73c4b9fa7701d4a7

**Missing element:** a reason

**Reasoning:** 1 key(s) state The first-out fault should be captured with a timestamp and not overwritten until authorized reset.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-73c4b9fa7701d4a7

### [WHY] A multimeter must be set to the proper range and function before testing. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-fa5d81773c393287` [seed] literature_supported / documentation, key `ind-s-a013254b36b7055a`, verdict supports: "The TSTrainer Lab Manual gives a very important warning: always make sure the multimeter is set to the proper range and function before testing."
- `c-17c2de65f3f17ed3` [topic] literature_supported / documentation, key `ind-s-a013254b36b7055a`, verdict supports: "Before using the multimeter, verify: Correct function selected Correct range selected Leads in correct ports Probe tips in good condition Insulation not damaged Meter CAT rating is appropriate Meter battery is good Display works properly"

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a reason. Re-runnable: prompt sha ea48f6a818f9.

- test: `WHY:c-fa5d81773c393287`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: to prevent damage to equipment or injury to personnel
- partial hits: c-fa5d81773c393287

**Missing element:** a reason

**Reasoning:** 1 key(s) state A multimeter must be set to the proper range and function before testing.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-fa5d81773c393287

### [RESULT/WHY] Verification of a fix should include running equipment — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-f41ecd20286698cd` [seed] literature_supported / documentation, key `ind-s-90dc6fdae4a41cc0`, verdict supports: "Verify the fix resolves the original symptom completely. Run the equipment through full operational cycles. Test boundary conditions that might trigger the same fault. Watch for several successful cycles before considering the problem solved."

**[RESULT]**

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'Verification of a fix should include running equipment'. Re-runnable: prompt sha f88108661839.

- test: `RESULT:c-f41ecd20286698cd`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: Sentences 1 and 5 describe actions but do not explicitly state expected results or next actions based on test outcomes.
- partial hits: c-f41ecd20286698cd

**Missing element:** a result-to-interpretation mapping for 'Verification of a fix should include running equipment'

**Reasoning:** 1 key(s) state Verification of a fix should include running equipment; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-f41ecd20286698cd

**[WHY]**

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a reason. Re-runnable: prompt sha 6c368fc69dfc.

- test: `WHY:c-f41ecd20286698cd`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): open
- judge reason: to account for end environment factors
- partial hits: c-0854575ba0113ca4

**Missing element:** a reason

**Reasoning:** 1 key(s) state Verification of a fix should include running equipment through full operational cycles and testing boundary conditions before considering the problem solved.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-f41ecd20286698cd

### [WHY] A periodic task should include a WALLCLOCKTIME GSV in only one user task, or wrap it in a UID/UIE pair if another task also reads it. — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-81d3eb38197d67ac` [seed] literature_supported / documentation, key `ind-s-aab556b0ece4b264`, verdict supports: "The manual has a note on that GSV that is easy to walk past: include the WALLCLOCKTIME GSV in only one user task, or wrap it in a UID/UIE pair if another task also reads it."
- `c-4cb402666ee92c71` [topic] literature_supported / documentation, key `ind-s-aab556b0ece4b264`, verdict supports: "a 10 ms periodic task writing eight tags into a 600-element ring, a trigger on the fault bit, 200 more samples, then a latch that stops the writer until somebody has read the result. Four rungs. About 7 KB of memory."
- `c-77967cc033e71595` [topic] literature_supported / documentation, key `ind-s-aab556b0ece4b264`, verdict supports: "A rung in the continuous task samples whenever the scan happens to come round, which on this machine is about every 8 ms and on a bad scan is 14. The timestamps drift, and a capture whose sample spacing wanders is hard to read"

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a reason. Re-runnable: prompt sha 991acec9a875.

- test: `WHY:c-81d3eb38197d67ac`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: to prevent confusion or incorrect processing
- partial hits: c-81d3eb38197d67ac

**Missing element:** a reason

**Reasoning:** 1 key(s) state A periodic task should include a WALLCLOCKTIME GSV in only one user task, or wrap it in a UID/UIE pair if another task also reads it.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-81d3eb38197d67ac

### [RESULT/WHY] capture should be avoided as the first step; instead begin — RG-SINGLE

*Action: search — never ask an expert.*

**OBSERVED EVIDENCE**

- `c-e4259b9c36af9835` [seed] literature_supported / documentation, key `ind-s-636acef04b884b84`, verdict supports: "Avoid indiscriminate packet capture as the first step. Begin with the failing connection and time window, then collect targeted traffic if switch and device diagnostics cannot distinguish the cause."

**[RESULT]**

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a result-to-interpretation mapping for 'capture should be avoided as the first step; instead begin'. Re-runnable: prompt sha d99bcee0f394.

- test: `RESULT:c-e4259b9c36af9835`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: Sentence 4 suggests collecting targeted traffic next if initial steps do not resolve the issue.
- partial hits: c-e4259b9c36af9835

**Missing element:** a result-to-interpretation mapping for 'capture should be avoided as the first step; instead begin'

**Reasoning:** 1 key(s) state capture should be avoided as the first step; instead begin; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test RESULT:c-e4259b9c36af9835

**[WHY]**

**INFERRED GAP**

Of 8 verified sentences retrieved on this topic, the closure judge (qwen2.5:7b-instruct, local) found only a partial statement of a reason. Re-runnable: prompt sha 89231615a005.

- test: `WHY:c-e4259b9c36af9835`; state: partial (closure judge: qwen2.5:7b-instruct)
- lexical comparison only (§1.5, no longer decisive): closed
- judge reason: Prevents unnecessary data and focuses on relevant issues.
- partial hits: c-e4259b9c36af9835

**Missing element:** a reason

**Reasoning:** 1 key(s) state Indiscriminate packet capture should be avoided as the first step; instead begin with the failing connection and time window.; 1 key(s) discuss the topic; the closure judge found no verified sentence matching test WHY:c-e4259b9c36af9835

## §7 checks

### §7.1 Anti-renaming: is the map density in disguise?

Computed over lens candidates only (HYP, RG-SINGLE, RG-UNVER, RG-SIBLING, RG-UNDECIDED and closed candidates) -- RG-UNK and CONTROL are excluded, since their density cannot vary.

- `J10(map, D_low)` = 0.00
- `J10(map, D_high)` = 0.58
- Spearman ρ(score, dens) = 0.91
- flags: closure-uninformative

**Matched-density table** (all lens candidates, by `dens` tercile):

| tercile | n | closed | HYP |
|---|---|---|---|
| low | 18 | 2 | 6 |
| mid | 19 | 8 | 10 |
| high | 19 | 3 | 16 |

Top-tercile closed share: 0.16

**Closure rate by `k_topic` band** (all lens candidates):

| band | n | closed | rate |
|---|---|---|---|
| 0-1 | 12 | 1 | 0.08 |
| 2 | 12 | 5 | 0.42 |
| 3-4 | 16 | 5 | 0.31 |
| >=5 | 16 | 2 | 0.12 |

### S2 fair mismatched-evidence control: does the judge close because of the EVIDENCE, or because of the SEED?

Replaces the first (straw-man) control, second adversarial review, 2026-09-29: the old own-evidence arm always carried the seed's own sentences while the mismatched arm never did (17/22 of PLC's old closures cited only the seed or its source), and the mismatched sentences were off-topic (cyclic gap_id pairing). Now BOTH arms keep the seed's own sentences; the OWN arm adds this candidate's own retrieved non-seed-source sentences; the CONTROL arm replaces those with the non-seed-source sentences retrieved for the topically nearest OTHER candidate of the same lens (max seed-stem Jaccard, ties by gap_id). "other-source-only" is the OWN arm with the seed and same-source sentences excluded entirely -- how often an independent source alone closes it. `closure-uninformative` unless own_rate - control_rate >= 0.20 (of candidates); lenses with < 2 candidates are skipped.

| lens | n | own rate | control rate | other-source-only rate | flag |
|---|---|---|---|---|---|
| DIAG | 9 | 1.00 | 1.00 | 1.00 | closure-uninformative |
| RESULT | 19 | 1.00 | 1.00 | 0.84 | closure-uninformative |
| SEL | 2 | 1.00 | 1.00 | 1.00 | closure-uninformative |
| WHY | 24 | 0.75 | 0.75 | 0.38 | closure-uninformative |
| **total** | 54 | 0.89 | 0.89 | 0.67 | closure-uninformative |

### S2 lexical donor null: why the lexical closure test was replaced

The reviewer's fair donor null for the (now-comparison-only) LEXICAL closure test: self and same-source claims are excluded from both arms, and the donor is the real non-common content stems of a random other-source A claim of the same knowledge type as the seed (`random.Random(0)`, 200 draws). A check "passes" (is informative) only if the observed count is STRICTLY ABOVE the null's 5-95% interval. DISC is excluded (anchor-regex-driven, not stem-overlap); DIAG is handled per its own closure unit (one rival's sign test, not the group).

| lens | observed closed | null mean | null 5-95% | n | flag |
|---|---|---|---|---|---|
| DIAG | 1 | 15.2 | [10, 21] | 48 | closure-uninformative |
| GUARD | 0 | 0.4 | [0, 1] | 1 | closure-uninformative |
| RESULT | 12 | 8.6 | [6, 12] | 19 | closure-uninformative |
| SEL | 0 | 0.8 | [0, 2] | 2 | closure-uninformative |
| WHY | 9 | 8.5 | [5, 12] | 24 | closure-uninformative |
| **total** | 22 | 33.5 | [26, 41] |  | closure-uninformative |

### Judge-vs-lexical agreement

Confusion counts, `<lexical_state>-><judge_state>`, over every judged candidate (the lexical test no longer decides anything; this is diagnostic only).

| lexical -> judge | n |
|---|---|
| closed->closed | 10 |
| closed->open | 2 |
| closed->partial | 23 |
| open->closed | 3 |
| open->open | 11 |
| open->partial | 7 |

