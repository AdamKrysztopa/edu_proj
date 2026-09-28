# N1 gold shapes: schema-blind inventory

Test set for the N1 gate (`REORIENTATION.md:650`): the schema must express every item below without new field types. Each item is described in its source's own terms, from repository text only; no gold has been acquired (§14.3, `REORIENTATION.md:441`). Items marked ILLUSTRATIVE have invented content and the source's structure.

Path keys: **R** = `REORIENTATION.md`; **EV** = `research_notes/Tacit knowledge reorientation/evaluation_and_residual.md`; **TK** = `…/tacit_knowledge_foundations.md`; **ER** = `…/expertise_representation.md`; **OK** = `…/organisational_knowledge.md`; **AF** = `…/adjacent_fields_and_falsification.md`; **LR** = `…/llm_domain_reconstruction.md`; **CI** = `research/explore-concept-inventories.md`; **MAP** = `ai_education_research_map.md`.

---

## A. Mathematics and education

### A1. Eedi Misconception Graph [137] with NeurIPS 2020 option-level responses [138]
Refs R:867, R:868. **Used by** E-MISC (R:526), E-DIST (R:527, where the graph is excluded from the corpus), E-EIG oracle (R:533), E-SYN T3 (R:369).

**Unit.** One named maths misconception. Separately, one 4-option diagnostic multiple-choice question whose distractors "embody misconceptions" (EV:23), with per-option response counts.

| Attribute | Where |
|---|---|
| Misconception label/text; catalogue of "more than 8,000", "informed by 200 million real student responses" | EV:22, R:526 |
| Link from distractor to misconception (the graph and Kaggle labels) | EV:51, R:527 |
| Prevalence / selection rate per option, from 20M+ answers, Sept 2018 – May 2020 | EV:23, R:526 |
| Question stem, 4 options, correct option | EV:23, R:527 ("from item stems only") |
| Topic, for sampling withheld topics | EV:250 |
| Release date against each model's cutoff (decides whether the post-cutoff falsifier applies) | R:526 |
| Licence: graph CC BY 4.0; NeurIPS data and Kaggle terms unverified | R:558, EV:56 |

**Relations.** Distractor → misconception (many-to-one; Kaggle ranks the top 25 of 2,500+ misconceptions per distractor, LR:143). Question → options → selection counts. Misconception → prevalence.

**Unknown.** Whether the graph carries prevalence directly or only through the NeurIPS responses. The mismatch between "8,000+" (EV:22) and "2,500+" (LR:143), which may be different releases. The grain of a misconception label. Whether the graph holds edges between misconceptions or to KCs. The release date is not recorded in the repo.

- ILLUSTRATIVE (concept). Misconception: "Believes that you add the denominators when adding fractions." Linked distractor: option C of Q#4417 ("2/7" for 1/3 + 1/4). Selection rate 31% of wrong answers.
- ILLUSTRATIVE (procedural). Misconception: "When rounding to 1 d.p., looks at the second digit after the one being rounded." Q#8120 (round 3.4651 to 1 d.p.): A 3.5 correct 52%, B 3.4 29% (linked), C 3.46 12%, D 3.47 7%.

### A2. DataShop KC models and the LFA-discovered split [140][102][103]
Refs R:870, R:832, R:833, R:834. **Used by** E-KC (R:528, N4 R:653).

**Unit.** A dataset of logged student steps plus a KC model, the mapping from each step or item to one or more KCs (Q-matrix, R:276). The gold is behavioural fit, not a list. The expert KC model is the comparator and the LFA-best model is the ceiling.

| Attribute | Where |
|---|---|
| Dataset ID (e.g. Geometry #76) | ER:27 |
| KC model name, origin (expert-authored, LFA-discovered, Single-KC/Unique-step default) | ER:26, R:528 |
| Step/item → KC mapping | R:276 |
| Per-student, per-step opportunity count and correctness (learning-curve input) | ER:26, EV:27 |
| AFM parameters; fit as item-stratified CV RMSE, AIC, BIC; learning slope | R:528, ER:29 |
| Size (e.g. 72,404 problem steps in the confirmation dataset) | ER:29 |
| Domain (geometry; Andes physics) | ER:29, `research/explore-knowledge-tracing.md:64` |

**Relations.** KC → items/steps. An LFA split derives a child KC from a parent (the hidden "backward area" difficulty, ER:29). Discovered KC → tutor redesign → RCT effect (d = 0.47, 91 completers; R:222).

**Unknown.** Terms of use (the terms page returned HTTP 500, EV:27). Whether the "backward area" KC's exact step mapping is published. The repo disagrees on "at least 10 of 11" datasets (R:222) versus "every one" (ER:28). Physics log availability (R:559).

- ILLUSTRATIVE (split, procedural). Parent KC "compute area of composite figure". LFA split: "forward area" (dimensions → area) versus "backward area" (area and one dimension → missing dimension). The split improves item-stratified CV RMSE from 0.412 to 0.398.
- ILLUSTRATIVE (step). Dataset #76, student S0213, step "solve-for-side-1", KC [backward-area], opportunity 3, first attempt incorrect.

### A3. AAAS Project 2061 item distributions [139]
Ref R:869. **Used by** E-MISC for mechanics (R:526, excluding conservation items) and E-DIST (R:527).

**Unit.** One assessment item whose answer choices each embed a named misconception, with the national field-test distribution of responses.

| Attribute | Where |
|---|---|
| Item stem and choices; misconception embedded per choice | EV:20 |
| National response distribution; percent correct by grade, gender, language; 150,000+ students since 2004 | EV:20 |
| Topic/idea (for the conservation exclusion) | R:526 |
| Host: original down, mirror resolves; licence unverified | EV:20, R:559 |

**Relations.** Choice → misconception. Item → subgroup distributions.

**Unknown.** Licence. Whether distributions are downloadable per item or only viewable. Whether one choice can carry several misconceptions.

- ILLUSTRATIVE. Item "Energy transfer when a ball is thrown upward". B, "the ball's force runs out at the top", embeds "motion requires a continuing force". Grade 8: A 38%, B 34%, C 18%, D 10%.

### A4. FCI distractor taxonomy [108]
Ref R:838. **Used by** E-MISC (R:526) and the mechanics best-case domain (R:559).

**Unit.** One FCI distractor, classified to a common-sense conception of force (CI:19). Population structure is reported in the literature as distractor co-selection groupings, e.g. an "impetus" worldview (CI:50), and as 22 misconception dimensions in a preprint (CI:51).

| Attribute | Where |
|---|---|
| Item number, option, misconception category | CI:19, EV:19 |
| Co-selection group / IRT dimension (secondary literature) | CI:50, CI:51 |
| Known failures: open-ended answers outside the FCI choices; 31% within-week answer instability; gender DIF on 8 items | CI:52, CI:78, CI:82 |
| Expert prediction of the most common wrong answer (TAs 65%, instructors 68%) | MAP:292 |
| Contamination: GPT-4 scored 83% | R:559 |

**Relations.** Distractor → category (the taxonomy). Item → option set.

**Unknown.** PhysPort access terms (R:559). The taxonomy's category list is not written anywhere in the repo. Which items are conservation items (they are excluded).

- ILLUSTRATIVE. Item 13, option C: "the force of the throw, gradually decreasing". Category: impetus, "an impetus is dissipated".

---

## B. Clinical and professional (CTA golds)

### B1. Sullivan et al. 2014, cricothyrotomy CTA task list [1]
Ref R:731. **Used by** E-CTA primary candidate (R:525, N3 R:652) and the E-EIG oracle (R:533).

**Unit.** One step of a CTA-derived gold-standard task list (46 steps).

| Attribute | Where |
|---|---|
| Step text | EV:41 |
| Step type: clinical knowledge (14), action (27), decision (5) | TK:14, R:199 |
| Order in the procedure | EV:41 ("task list"; order implied, not stated) |
| Whether each teaching expert mentioned it unprompted; per-type omission 71% / 51% / 73% (3.6 of 5 decision steps) | TK:14 |
| Whether the "how to do it" was articulated (13% of action steps) | TK:14, TK:243 |
| Unprompted versus CTA-probed coverage (20/46 versus 31/46) | R:199 |
| Number of teaching experts (3) and CTA experts building the gold | TK:14, EV:41, EV:179 |

**Relations.** Ordered steps. Step → type. Step → which experts covered it, under which condition (unprompted or probed).

**Unknown.** Itemised list availability is unconfirmed (R:525). The repo gives the gold-building panel as "6 surgeons" (EV:41), "3 + 3" (EV:179) and "three other surgeons" (TK:14). Whether per-step, per-expert coverage is published or only aggregates. Whether decision steps state their cues. The list is CTA-derived and so partly circular (R:199).

- ILLUSTRATIVE (clinical knowledge). "The cricothyroid membrane lies between the thyroid and cricoid cartilages; the cricothyroid arteries run along its upper border." Type: clinical knowledge. Unprompted 1/3, probed 3/3.
- ILLUSTRATIVE (action with how). Step 12: "Stabilise the larynx with the non-dominant hand and keep it there until the tube is secured." Type: action. "How" articulated by 0/3.
- ILLUSTRATIVE (decision). "If landmarks cannot be palpated (obese or swollen neck), make a longer vertical skin incision before the horizontal membrane incision." Type: decision. Unprompted 0/3, probed 2/3.

### B2. Crandall & Getchell-Reiter 1993, NICU cues [4]
Ref R:734. **Used by** E-CTA (R:525).

**Unit.** One cue nurses used to detect early infant distress (sepsis), elicited by CDM (TK:17).

| Attribute | Where |
|---|---|
| Cue text; 70 cues from 17 nurses (mean 13 years' experience) | TK:17 |
| Absent from the contemporaneous training literature (25 of 70) | TK:17, R:208 |
| Category (seven previously unrecognised categories) | TK:17 |
| Date against the literature (1993; the retrieval corpus is frozen at the gold's date) | R:546 |

**Relations.** Cue → category. Cue → in or out of the literature. Categories were later "incorporated into novice training" (TK:17).

**Unknown.** The itemised 70-cue list is not verified (R:560). Whether the seven categories cover only the 25 absent cues or all 70. How many nurses mentioned each cue. Whether the cues are ordered or tied to incidents. All figures are secondary, via [3].

- ILLUSTRATIVE (perceptual cue). "Skin colour goes from pink to mottled or grey, hours before temperature changes." Category: colour. Absent from literature: yes.
- ILLUSTRATIVE (behavioural cue). "Infant stops fussing at handling and becomes limp." Category: muscle tone / activity. Absent: yes.

### B3. Chao & Salvendy 1994, programming troubleshooting [2]
Ref R:732. **Used by** E-CTA (R:525).

**Unit.** One recorded troubleshooting behaviour of six expert programmers, typed as diagnostic action, debugging action or interpretation. The gold is the recorded trace, not a CTA list (TK:13).

| Attribute | Where |
|---|---|
| Behaviour type (diagnostic / debugging / interpretation) | TK:13, R:198 |
| Reported by which expert, under which elicitation method | TK:13 |
| Per-expert ceiling 41% / 53% / 29%; pooled 87% / 88% / 62% | R:198 |

**Relations.** Expert × method × behaviour coverage. Interpretations attach to the actions whose results they read.

**Unknown.** Item counts. Whether any itemised list exists. The figures are known only via [3].

- ILLUSTRATIVE (interpretation). Diagnostic action: "insert a print before the loop exit". Interpretation: "the value never prints, so the loop condition, not the body, is at fault". Reported by 1 of 6 experts.

### B4. CDM / ACTA decision-requirement rows [16][17]
Refs R:746, R:747. **Used by** E-CTA, as the shape of "further CTA-based studies reported in [3]" (R:525). This is a format, not a dataset.

**Unit.** One row of the ACTA cognitive-demands table, with four columns: difficult cognitive element, why difficult, common errors, cues and strategies (ER:90). CDM probes an incident for cues, knowledge, goals, options, basis of choice, analogues and hypotheticals (ER:89).

**Relations.** Decision point → cues → strategies → errors. Incident → decision points (CDM sweeps).

**Unknown.** No machine-readable format exists; these are tables in reports (ER:104). Cues are free text with no link to evidence (ER:208).

- ILLUSTRATIVE. Element: "judging whether a fireground is about to flash over". Why difficult: "the cues are subtle and the time is short". Common error: "committing crews on visible flame alone". Cues and strategies: "smoke darkening and pushing from low openings; heat felt through the glove; withdraw and ventilate first".

### B5. PARI [106]
Ref R:836. **Used by** candidate text-poor residual gold (R:564). Maintenance residual prediction depends on it (R:562).

**Unit.** One troubleshooting step recorded as Precursor (why this action), Action, Result and Interpretation (what the result means for the fault hypothesis) (ER:95). From aircraft-maintenance troubleshooting, 200+ technicians (R:564).

**Relations.** Ordered steps. Interpretation updates the fault hypothesis (ER:101).

**Unknown.** Whether the itemised task list is public (R:564).

- ILLUSTRATIVE (automated check). P: "rule out the power supply first, it is cheapest". A: "measure 28 V at test point J4". R: "27.6 V". I: "supply good; the fault is downstream, in the signal path".

### B6. Chick-sexing discrimination [24]
Ref R:754. **Used by** no experiment. It is the exemplar that perceptual expertise can be analysed and taught (R:210, AF:147), and it sets the channel for perceptual cues (R:313).

**Unit.** One discriminating perceptual cue plus its instruction, with novice accuracy before and after.

**Unknown.** No numbers or cue text in the repo.

- ILLUSTRATIVE. Cue: "shape of the eminence: rounded/convex versus flat/concave". Instruction: a one-page sheet with contrasting photographs. Novice accuracy moves toward expert accuracy.

---

## C. OSS and organisational

### C1. E-OSS departures [111][112][109][110]
Refs R:839–842. **Used by** E-OSS (R:529, N3 R:652) and the E-EIG oracle ("a departed developer's later record", R:533).

**Unit.** One code unit existing at freeze time *t*, determined by git blame at *t*, in a repository where a truck-factor developer leaves after *t* (R:529).

| Attribute | Where |
|---|---|
| Repository, file/unit path at *t* | R:529 |
| Departure date of the truck-factor developer; *t* before it | R:529 |
| Developer pseudonym (pseudonymised in all outputs) | R:529 |
| Truck factor / authorship; review-weighted concentration | R:529, OK:80, OK:103 |
| Pre-*t* and post-*t* rationale-seeking issues and defect-fix commits, per unit of activity (difference-in-differences), blind double-coded | R:529 |
| Abandoned file, as covariate only | R:529 |
| Baseline covariates: prior trouble, size, churn, doc-link/comment density, KaR | R:529 |
| Project outcome: abandoned (315 of 1,932) or survived (128) | OK:78 |
| Artefacts dated ≤ *t* only | R:529 |

**Relations.** Unit → developer(s) via authorship. Issue/commit → unit. Project → departure event. Unit → pre/post window.

**Unknown.** Minimum post-departure activity and number of departures (to set, R:633). How "rationale-seeking" is coded. Unit grain (file, folder, component). Authorship validity after agentic coding (OK:84). Truck-factor algorithms disagree (OK:69).

- ILLUSTRATIVE. Repo `libfoo`, unit `src/net/retry.c`, *t* = 2019-03-01, departure 2019-04-15 of dev_07 (truck factor 1). Rationale-seeking issues per 100 commits: pre 1.2, post 6.8. Defect-fix commits: pre 3, post 11. Abandoned: yes.
- ILLUSTRATIVE (outcome item). Issue #2211, 2019-07-02: "Does anyone know why backoff is capped at 7 retries?" Coded rationale-seeking; linked unit `src/net/retry.c`.

### C2. Rationale datasets [59]
Ref R:789. **Used by** OSS coverage and rationale ground truth (R:561, OK:252–256).

**Unit.** A design decision or problem with its expert-written rationale. Three sources: the Linux OOM-killer rationale dataset; 100 Stack Overflow/GitHub problems; 30 developer-written ADDs (OK:253–255).

**Attributes.** Decision/problem text, rationale arguments, origin (SO, issue, discussion, commit), expert author (OK:95–96).

**Relations.** Decision → rationale arguments. Commit → ADD (OK:96).

**Unknown.** Argument grain. The OOM-killer dataset's structure is not described. Licences.

- ILLUSTRATIVE. Decision: "use an append-only log instead of in-place updates". Rationale: (1) crash recovery without fsync ordering; (2) cheaper replication. Source: a GitHub discussion.

### C3. Documentation-issue taxonomy [116]
Ref R:846. **Used by** E-DVP labels (R:530) and consistency labelling (OK:266).

**Unit.** One documentation issue, typed into a 162-type taxonomy built from 878 artefacts (mailing lists, SO, issue trackers, PRs). Dominant types: outdated, incomplete, inconsistent (OK:89).

**Unknown.** The taxonomy's depth and hierarchy. The per-artefact labels are not described.

- ILLUSTRATIVE. PR comment: "README still says `--legacy` flag; it was removed in 2.0". Type: outdated / content. Artefact: pull request.

### C4. E-DVP review-enforced norms
**Used by** E-DVP (R:530).

**Unit.** One norm enforced after *t* in review comments, rejected PRs or maintainer corrections, blind double-coded, and whether the docs state it before *t* (R:530). This is the collective knowledge type (R:315).

**Unknown.** No public SOP-plus-execution-log pair exists (R:530). How many enforcements make a norm.

- ILLUSTRATIVE (collective norm). "New public APIs need a CHANGELOG entry and a deprecation note." Enforced in 4 review comments and 1 rejected PR after *t*. Absent from CONTRIBUTING.md at *t*.

### C5. The residual question (R:447, OK:269)
**Unit.** One question carrying a target claim, a knowledge type, a matched channel and a concrete probe (R:447). The notes' example: "Commit a1b2 changed the retry limit from 3 to 7; no issue, PR or ADR says why." This is not gold; it is the output a gold item would answer.

**Relations.** Question → commit → unit. Question → the absent artefacts (issue, PR, ADR).

### C6. TVA/IAEA position risk [121]
Ref R:851. **Used by** no NOW experiment. It is the criticality axis (R:184) and the KLRA with no validation against realised loss (R:529).

**Unit.** One employee/position with a Total Risk Factor, combining an Attrition Risk Factor (projected departure date) with a Position Risk Factor (uniqueness, criticality, difficulty of refilling) (OK:20, OK:227).

**Unknown.** Scoring scales (OK:33). The 35% figure is unverified (R:851).

- ILLUSTRATIVE. Position: "senior reactor-protection I&C technician". Attrition RF 5 (retires within 1 year). Position RF 4. Total 20 (priority: capture).

---

## Experiment-level attributes (not per item)

| Attribute | Where |
|---|---|
| Area partition and scope decomposition, hash-frozen before gold | R:441, R:650 |
| Held-out status: leave-one-gold-out, leave-one-domain-out | R:441, R:564 |
| Gold item mapped to no area, scored as a missed area at a floor score | R:441 |
| Importance weight *wᵢ* (NOW unweighted; LATER panel or behavioural) | R:421 |
| Matcher: different model family, κ ≥ 0.70, blind to P(missing) and origin | R:521, R:427 |
| Blinding: origin-free, model-family-free item IDs; owner origin-blinded | R:441, R:521 |
| Corpus freeze date: *t* (E-OSS) or the gold's publication date (E-CTA) | R:529, R:546 |
| Memorisation-probe result per gold item; probe-positive items excluded | R:525, R:546 |
| Pre/post model-cutoff status; Eedi release date against cutoff | R:526, R:539 |
| Corpus-frequency stratum | R:566 |
| Knowledge-type stratum for recall | R:421, R:453 |
| Gap-map score before elicitation; revealing channel (residual corpus) | R:451 |
| Primary/fallback gold, minimum items and missed areas | R:521, R:631 |
