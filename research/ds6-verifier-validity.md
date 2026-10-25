# DS6: Independent verifier and decoy validity; a reachable robustness contrast

- **Question:** Can decoy falsity and verifier validity be established without trusting the pipeline, and which N2-type robustness contrast could reach a Continue reading?
- **Answer:** ClashEval's ">60%" is GPT-4o's rate with one document. For Claude models ClashEval reports 31–40% with one document, and 24% for Opus with five (Opus k = 5: 23.7%, 95% CI 20.9–26.7%). N2's 5/24 (21%, Wilson 9–40%) under 18 documents is in line with that [inferred: a different model and context size]. A contrast with weak-prior targets and two planted pages per real page should clear a 40% floor with P ≥ 0.90 at n = 48 if true adoption is 50% or more [SYNTHETIC].
- **Changed:** Nothing is rerun under the old design. Any new registration waits for an I5-style reachability check of E-PLANT-2 (I5 covered only the old design) and a calibration pilot of the ungated arm only. Decoys are validated by blind human coders, mixed in with natural claims, and never by their generator.

**Result.** All three questions have an answer. The first carries a lesson, queued in `docs/lessons.md`.
1. **Why the floor was missed.** The registered floor (a_u ≥ ⌈n/3⌉, "about half the > 60% expectation") was set from ClashEval's headline figure, which is GPT-4o's rate (Table 2: 60.8%).
   - For the two Claude models, the same table gives 31.3% and 40.1%. That is one document, conditioned on a correct prior, so the floor sat at the Claude single-document rate.
   - ClashEval reports that adding documents lowers this rate: Opus falls from 28.7% (k = 1) to 23.7% (k = 5).
   - E-PLANT gave Haiku 18 documents, with at least two real pages stating each target.
   - Xie et al. find that models cling to their parametric memory when evidence both supports and contradicts it. If Haiku's prior agreed with the real pages (not measured), E-PLANT resembles that setting [inferred].
   - ClashEval's appendix Table 4 reports exactly half of each Table 2 value (Claude 15.7–20.1%) without explanation, and §4.1 quotes Table 4's value. Both tables are given in §1.
2. **Decoy validity.** Published pipelines settle a decoy's label outside its generator (§2):
   - Separate annotators label each mutated claim without knowing its source (FEVER).
   - The seed summary's own annotator labels every edit consistent, inconsistent or borderline, and SummEdits' minor edits left 37% of its benchmark consistent.
   - A hand-validated NLI filter checks that generated evidence entails its intended answer (Xie et al.; 200 examples, 99%).

   None of them trusts the generator's own rationale, which is all `decoy_is_valid` checks. On the 40 committed E-LIVE v1 decoys, the replayable half of `decoy_is_valid` (text differs) passes all 40; the rationale half cannot be replayed (the v1 sidecars have no `rationale` field). On my reading, which is not a measurement, 6 of the 10 decoys the verifier accepted are of debatable falsity.
3. **Verifier validity.** §3 gives a sampling plan of 125 SUPPORTS and 50 non-SUPPORTS units, blind to the verdict and double-coded, with the decoys mixed in. §4 gives an eight-code error taxonomy mapped onto FRANK and AIS.
4. **New contrast.** §5 proposes E-PLANT-2, with thresholds I5 can check.

**Decision it feeds.** Whether to register a new N2-type robustness experiment. **This is an owner decision.** The deferred reruns are funded only if an I5-style reachability check of E-PLANT-2 (I5 covered only the old design) shows a reachable reading. Nothing here is registered. The owner chose option 1 on 2026-10-24 (§7).

**The old registration is unchanged.** `docs/n2-eplant-eabst-protocol.md` (registered `3b72fb8`, amendments 1 and 2) and its readings stay as recorded in `research/n2/e_plant_eabst_report.md`: E-PLANT INCONCLUSIVE with Continue closed, E-ABST INCONCLUSIVE, and N2 INCONCLUSIVE. Nothing in this note amends a threshold, a definition or an arm of that protocol. Run 1 stays sealed and unscored. No sealed artefact was opened for this note.

**Method.**
- Sources were read on arXiv. The HTML full text was read for ClashEval, WikiContradict, AbstentionBench, Xie et al., SummEdits, FRANK, AIS and FEVER. For Peters & Chin-Yee only the abstract was read, marked "(abstract)". MiniCheck was read in its abstract and in the LLM-AggreFact section, which the citation-verifier checked.
- **`citation-verifier` passed on 2026-10-24, on the second pass.**
  - The first pass found 3 wrong citations, 5 overstated ones and 3 minor issues. All were corrected. The most important was ClashEval Table 2 versus Table 4, which changed §1.
  - The re-check found 1 more wrong citation (SummEdits annotators are not blind) and 3 minor issues. All were corrected.
- Repository evidence comes from committed artefacts only:
  - `reconstruct/runs/*/sidecar.json` and `ledger.json` (E-LIVE v1 and v2(b), which are not sealed);
  - `research/n2/*.md`;
  - `reconstruct/src/reconstruct/`.
- Planning figures come from a seeded stdlib script, `research/ds6-verifier-validity/ds6_plan.py` (sha256 `fe482414…bd472807cb`, seed 20261024, 20,000 simulations per cell). They are **SYNTHETIC**: they inform the design and never feed a gate. The committed script holds p fixed in its sample-size search; the first draft searched on round(p·n)/n and reported the first crossing, a rounding artefact that understated three sizes (§3).
- My reading of the 40 committed decoys (§2.2) is one AI reader from the generator's model family (Anthropic). It is labelled **inferred** and is an illustration, not a criterion.
- I5 (`research/gate_sim/RESULT.md`, 82b2ca6) ran after this note. It finds the old E-PLANT cannot read Continue (best: Change) and advises against a floor amendment. It did not check E-PLANT-2; that check is still owed (§6).

## 1. Why ClashEval's ">60%" did not apply to E-PLANT

| Source | Model | Setting | Context chosen when the prior was correct and the context wrong |
|---|---|---|---|
| ClashEval Table 2 [51] | GPT-4o | 1 document | 60.8% (57.1–64.3), the ">60%" headline |
| ClashEval Table 2 [51] | GPT-3.5 | 1 document | 62.6% (59.8–65.7) |
| ClashEval Table 2 [51] | Claude Sonnet | 1 document | 40.1% (37.4–43.4) |
| ClashEval Table 2 [51] | Claude Opus | 1 document | 31.3% (28.2–34.6) |
| ClashEval appendix, k-document tables (§4.2) [51] | Claude Opus | k = 1 → k = 5 documents | 28.7% (25.5–31.8) → 23.7% (20.9–26.7) |
| ClashEval App. Table 4 [51] | Claude Opus / Sonnet / GPT-4o | 1 document | 15.7% / 20.1% / 30.4%, exactly half of Table 2, unexplained, and §4.1 quotes Table 4's value |
| N2 E-PLANT baseline (`e_plant_eabst_report.md` §1.1) | Haiku 4.5 | 18 documents per domain, ≥ 2 true pages per target, prior not measured | 5/24 = 20.8% (9–40%) |

- **The headline is one model's number** [literature-supported].
  - ClashEval's discussion says GPT-4o overrides "its own correct prior knowledge over 60% of the time". That is Table 2's GPT-4o value.
  - The same table puts both Claude models at 31–40%, and the paper says Claude Opus "adheres to incorrect contextual information 30% less than GPT-4o for the same degrees of modification" (§4.3).
  - The registered floor's evidence citation ("about half the > 60% expectation", protocol §6) set ⌈n/3⌉ ≈ 33%. That equals the Claude single-document rate, before any allowance for E-PLANT's larger context.
  - The appendix Table 4 reports exactly half of each Table 2 value. This note reads Table 2, whose caption and 'context' row match the >60% sentence (§5). The paper's own §4.1 prose quotes Table 4's halved value for Opus (15.7%), so ClashEval is internally inconsistent here.
- **More documents lower adoption** [literature-supported]. ClashEval §4.2 adds four retrieved documents per query: "multi-document RAG also reduces the context bias found in models". For Opus the rate falls from 28.7% to 23.7%. The test covered GPT-4o and Claude Opus only.
- **Supporting evidence in context: confirmation bias** [literature-supported for the finding; inferred for E-PLANT].
  - Xie et al. find LLMs "highly receptive to external evidence if that is the only evidence".
  - "With both supportive and contradictory evidence to their parametric memory, LLMs show a strong confirmation bias" (Introduction).
  - They also find that models "follow the herd and choose the side with more evidence" (§4.2).
  - Xie's "supportive" evidence agrees with the model's own prior. Haiku's prior was not measured, so E-PLANT matches this setting only if that prior agreed with the real pages. E-PLANT did put one planted page against at least two real pages per target (protocol §1 step 3).
- **Prior strength and deviation size** [literature-supported]. ClashEval reports that adoption falls as the model's prior token probability rises (slopes −0.1 to −0.45, §4.4). It also falls as the planted value moves further from the prior (§4.3).
  - Food-safety temperatures and concreting minima are well-known values, and the plants scaled them by 0.5–0.77 or 1.3–2.0.
  - **Inferred:** both domains sat where adoption is lowest. Concreting, at 1/12, may have the stronger priors.
- **What this means for the old design** [SYNTHETIC]. At N2's observed rate (p_u = 0.21) and n = 24:
  - P(a_u ≥ ⌈24/3⌉) = 0.11;
  - even a gate that removed every ungated adoption (q = 0) would have reached one-sided McNemar p < 0.05 with probability 0.33 (`ds6_plan.py`).
  - The registered design was underpowered at its own baseline before it ran.

## 2. Decoy validity, independent of the generator

### 2.1 How published pipelines establish that a decoy is false and on-topic

| Pipeline | Who generates | Who checks the decoy | Validation numbers |
|---|---|---|---|
| FEVER [Thorne et al. 2018] | Annotators mutate claims; "the modifications can be either true or false" (App. A.4) | Different annotators label each claim "without knowledge of the sentence they were derived from" (abstract) | Fleiss κ = 0.6841; super-annotators re-did a random 1% (evidence precision 95.42%, recall 72.36%, §3.4.2) |
| SummEdits [Laban et al. 2023] | LLM or human edits that are "atomic and localized" and "might or might not affect the consistency" (§5.2) | Annotators label every edited summary consistent, inconsistent or borderline. Borderline items (about 6%) are dropped | ≥ 20% multiply annotated; Cohen's κ 0.72–0.90 (mean 0.82), 0.92 after dropping borderline (§6.2). 37% of the final benchmark is consistent, close to the authors' aim of balance |
| Xie et al. 2024 | An LLM writes counter-memory for a counter-answer. Falsity is fixed by construction | DeBERTa-v2 NLI must find that each passage entails its intended answer: a support check, not a falsity check (§3.4) | 200 random examples hand-labelled, 99% NLI accuracy (§3.4, App. B.5) |
| ClashEval [51] | Fixed multipliers (0.1–10×), year offsets, or prompted "slight / significant / comical" swaps; GPT-4o writes the perturbed excerpts for drug dosages and news (§3.3) | No independent check is described [inferred from §3.3] | — |
| WikiContradict [52] | Real conflicts tagged by Wikipedia editors | Annotators verify each tag, isolate the passages and resolve anaphora (§3.2) | Response κ 0.58–0.88 by template (§4) |

**What follows** [inferred]:
- A changed wording is not a false claim. SummEdits' minor edits can be meaning-preserving, and only human labelling of each edit, not the edit itself, settled which ones were.
- Every validated pipeline above puts the falsity decision outside the generator: other humans, all humans, or an NLI model hand-checked on a sample.
- `decoy_is_valid` (`reconstruct/src/reconstruct/evidence.py:651-656`; lines 593–598 when DS6 was written) checks two things. The text must differ, and the generator must return a rationale. So it measures neither falsity nor topical match. This is the review's R2, confirmed.

### 2.2 The committed decoys

E-LIVE v1 ran 40 decoys: PLC 20 and GDPR 20 (`reconstruct/runs/20260928T133336Z-59ec876b3d7e/sidecar.json` and `…135354Z-eb840a85b7d1/sidecar.json`, field `decoys`). They used the decoy prompt as it stood at `600ba2e`, before `080b109`. That revision added "never narrow the claim and never drop a conjunct".

| Mutation | n | Verifier verdict `supports` (counted as false accept) |
|---|---|---|
| number | 8 | 1 |
| negation | 20 | 2 |
| scope | 12 | 7 |
| **Total** | **40** | **10 (25%)** |

- **The current check.** The replayable half of `decoy_is_valid` (text differs) passes all 40, because every mutated claim differs from its original; the rationale half cannot be replayed (the v1 sidecars have no `rationale` field).
- **My reading** [inferred: one AI reader, same family as the generator, not a criterion]. Of the 10 accepted decoys:
  - **4 look like clear verifier misses:** "common" became "rare"; "multiple communication channels" became "a single communication channel"; "…, or …" became "…, and …"; "combined with" became "or".
  - **6 have debatable falsity:**
    - a list conjunct dropped (the kind of edit the revised prompt now forbids);
    - a disjunct dropped ("confirm or eliminate" became "confirm");
    - a conjunct dropped from an enabling condition;
    - a timescale shift ("weeks and months" became "days and weeks");
    - two incoherent edits ("simultaneous changes to a single part", "more than certain").
  - So the raw false-accept rate of 10/40 lies somewhere between about 4/40 and 10/40 once validity is judged. The self-certified check cannot tell which.
- **Type labels are loose.** 4 of the 8 `number` decoys change no quantity: "multiple" became "single" twice, "high" became "low", and one added "on a quarterly basis". Most `negation` decoys are antonym swaps, not negations. `report.py`'s per-type Wilson rates therefore mix edit kinds. SummEdits' edit-type tags (entity modification, antonym swap, hallucinated insertion, negation insertion; §6.4) fit these decoys better than the three requested types do.

### 2.3 Proposed decoy-validity rubric (A6 decoys)

A decoy enters the verifier's false-accept denominator only if it passes V1–V4. A failure is counted and reported by mutation type, as now.

| # | Criterion | Who or what judges it | Source of the design |
|---|---|---|---|
| V1 | **Not entailed by the span.** A blind human coder, shown the span and the claim with no original, no mutation type and no verdict, labels it *not entailed*, *entailed* or *borderline*. Borderline items are excluded, as in SummEdits | Both human coders (§3). A disagreement is excluded and counted | FEVER (blind to the source), SummEdits (borderline filter) |
| V2 | **Not entailed by the ±300-character context either.** If the context entails it, the decoy is excluded: a decoy made true by an antecedent outside the span tests nothing | The same coders, second pass | AIS interpretability stage; E-LIVE context-only cases (§4, E1) |
| V3 | **On topic and localised.** Same subject and the same anchor terms. The edit touches one clause (SummEdits "atomic and localized"). The other sentence tokens are unchanged | Mechanical: token diff and anchor check. Flags go to the coder | SummEdits §5.2 |
| V4 | **Edit type as labelled.** The coder tags the edit type (quantity, negation, antonym, scope or strength, connective, added content). A mismatch is relabelled, not dropped | Coder | SummEdits §6.4 |
| V5 | **Not separable by surface features.** A stand-in verifier that uses only lexical overlap between decoy and span must reach a false-accept rate far from the real verifier's. Otherwise the decoy set does not test entailment. Reported, not gating | Mechanical | L7.3 trivial stand-in |
| V6 | **Generator independence.** The generator's rationale is kept as a note but never decides validity. An LLM pre-screen may run only as a third family beside the human labels (ADR 0009). Its agreement with the humans is reported, as Xie et al. report their NLI filter's | Process rule | Xie et al. App. B.5; ADR 0009 |

The sample covers every decoy a run produces (at most 30 per run, `DECOYS_PER_TYPE = 10`), so sampling error comes only from the run, not from the validation.

### 2.4 Plant validity (E-PLANT-type planted pages)

The registered software checks (protocol §1 step 5) stay. The rubric adds:

| # | Criterion | Why |
|---|---|---|
| P1 | **False beyond the real range.** The planted value lies outside the range of every real page's value for the same quantity, scope and period, by at least the source's reporting granularity. A value that some real page (another jurisdiction, another standard) states is a true fact, not a plant | E-LIVE's jurisdiction pattern (§4 E2a); the registered conflict-pair rule "same quantity, scope and period" (protocol §1 step 4) |
| P2 | **Same scope.** Same unit, population, jurisdiction and condition as the gold target. The owner checks this against the gold spans before plant authoring | ClashEval holds the question fixed and edits only the answer (§3.3) |
| P3 | **Plausible.** Inside the domain's physically or legally plausible range; no "comical" levels | ClashEval: adoption falls as deviation rises (§4.3) |
| P4 | **Surface parity.** A stand-in classifier on surface features alone (host form, date, length, reading level, link count) must not separate planted from real pages (AUROC ≤ 0.65 *(proposed)*). Otherwise any host-reputation rule would "pass" without reading content | L7.3 trivial stand-in |
| P5 | **Independent check.** Someone other than the author model checks P1 and P2: the owner, as for gold. The author model never certifies its own page | FEVER, SummEdits, Xie et al. (§2.1) |

## 3. Verifier validity on natural claims: sampling plan

**How others measure it** [literature-supported].
- AIS rates attribution in two stages: first interpretability (Q1, "is all of the information … interpretable"), then attribution (Q2, "fully supported by the source document"). It excludes source quality and leaves it to a separate task.
- AbstentionBench validated its LLM judge on 300 human-annotated responses. Sampling was stratified by gold label *and* by a first-pass judge's prediction "to ensure annotations covered a mix of true and false positives and negatives". Annotators labelled independently, non-unanimous items were resolved in review, and the set was split 50/50 into validation and test (App. C.3.3). On that set GPT-4o reached precision 0.96 and recall 0.77 (C.3.4).
- WikiContradict's best judge, GPT-4, reached F 82.5 with precision 73.4. Its open-source judge (Llama-3-70b) over-credited Mistral-7b, which "attempts to reconcile conflicting information by providing both answers" (§5).
- MiniCheck's LLM-AggreFact unifies grounding datasets of real LLM outputs. Every dataset holds "human-annotated (document, claim, label) tuples" (LLM-AggreFact section).
- The common design is human labels on **natural** outputs, stratified so that both error directions appear.

**Plan** *(proposed)*:
- **Unit.** One (claim, located evidence span, verifier verdict) triple from the runs at the frozen tag. Only the current verifier counts: E-LIVE v1 used the older prompts, so its verdicts measure a different verifier.
- **Strata and size:**
  - **SUPPORTS: n = 125**, at least 60 per domain over at least 2 domains, seeded random within each domain, proportional to `knowledge_type`.
  - **INSUFFICIENT/REFUTES: n = 50**, to estimate wrong rejections.
  - **Cross-verify REFUTES: all, up to 30.** These become N1 `Contradiction`s, which the proposed contrast reads (§5). R4's scope-flagged refutations are a known false-positive class.
- **Why 125** [SYNTHETIC; `ds6_plan.py`]:
  - At a true rate of 12% (GDPR v2(b)'s 3/25), a one-sided 95% upper bound ≤ 20% needs n ≥ 68, and ≤ 15% would need n ≥ 384. n = 125 meets the ≤ 20% gate bound.
  - At a true rate of 10%, ≤ 15% needs n ≥ 139. **n = 125 does not meet this target:** its one-sided 95% Wilson upper bound at p = 0.10 is 15.3%. The first draft's 61, 354 and 124 searched on round(p·n)/n and took its first crossing; at a true 10% that rounded bound stays at or below 15% for every n only from 156.
  - n ≥ 99 sees at least one instance of a 3%-prevalence error code with probability 0.95, so rare taxonomy codes are not missed.
  - At p = 0.12, n = 125 gives a Wilson 95% interval of 7.4–18.9%.
- **Blinding.** The 175 to 205 natural units and all of the run's decoys are shuffled into one coding sheet. Each sheet row shows the span, the claim and the ±300-character context behind a reveal. It never shows the verdict, the origin (natural or decoy) or the source URL. One sheet therefore gives the verifier's natural error rates, its false-accept rate on validated decoys and decoy validity (V1–V2).
- **Coders.**
  - The owner and the NOW programme's one blind second coder each label every unit with the §4 taxonomy.
  - κ is reported per stratum, with WikiContradict's 0.58–0.88 and SummEdits' 0.82 as reference points. Disagreements are resolved after κ is computed.
  - An AI inspector, like the one in `research/n2/e_live_claim_inspection.md`, may pre-code as a separate reported arm under ADR 0009 rules. It is never the coder of record.
- **Estimands.**
  - Natural false-support rate = SUPPORTS units coded E2–E7, divided by 125, with a Wilson interval per domain and pooled.
  - E1 (context-dependent support) is reported separately and added in a sensitivity analysis.
  - Wrong-rejection rate on the 50.
  - Scope-flagged and unflagged false-contradiction rates on the cross-verify REFUTES.
  - Decoy false-accept rate over V1–V4-valid decoys only.
- **Threshold proposal** (owner's to set): verifier labels feed a gate only if the pooled one-sided 95% upper bound on natural false support is ≤ 20%. I5 can check reachability from the table above.

## 4. Natural-error taxonomy

Code the most severe error and record all errors present. E1 is a validity breach of span-only entailment, not necessarily a false claim.

| Code | Definition | Literature anchor | E-LIVE instance (committed) |
|---|---|---|---|
| E0 CORRECT | The span alone entails the claim | AIS attribution | — |
| E1 CONTEXT_ONLY | Entailed only with text outside the span: an antecedent, a heading or a qualifier just outside | AIS stage 1 (unclear pronouns, missing context); FRANK CorefE ("no clear antecedents") | `c-867ef26bc5a0d84a`, `c-4a2735242356a648` (`e_live_claim_inspection.md`); `c-aed289a57231c28c` (`e_live_review_notes.md`) |
| E2 SCOPE_DRIFT | The population, system or instance is generalised beyond the source: one template becomes all logs, one incident becomes a rule | FRANK CircE and EntE; generalisation bias in LLM summaries, with 26–73% overgeneralisation for three models (Peters & Chin-Yee 2025, abstract) | `c-0b0bdd3ff65e2dd0`, `c-bd3233c483e5442b` |
| E2a JURISDICTION_DROPPED | A national or regional rule is stated as general (an E2 subtype, coded separately because it recurs) | FRANK CircE (location). No source found with a dedicated code [inferred] | `c-b308aea20d8cb601`, `c-e3fdcc891699e1d7`, `c-5adc8389c5ca8ebc`, `c-e314a06b576099c1` |
| E3 HEDGE_DROPPED | Modality strengthened ("usually" or "likely" deleted, "may" becomes "must") | FRANK CircE (modality) | `c-d008e8f1da0cb01c` ("usually"), `c-bd3233c483e5442b` ("likely") |
| E4 QUANTIFIER_CONNECTIVE | Some becomes all; "and", "or", "combined with" or "only if" changed so the claim is stronger | FRANK LinkE covers the connectives. No FRANK category covers quantifiers [inferred] | PLC v1 QUANTIFIER/MODALITY 1 (`e_live_claim_inspection.md`) |
| E5 ADDED_CONTENT | The claim states something the span does not | FRANK OutE; SummEdits hallucinated insertion | PLC v1 ADDED_CONTENT 2 |
| E6 WRONG_VALUE | Wrong entity, predicate, number or polarity | FRANK EntE and PredE; SummEdits entity modification, antonym, negation | PLC v1 WRONG 1 |
| E7 ATTRIBUTION_DROPPED | A first-person, vendor or attributed statement is restated as a flat fact | Project code; overlaps E2. AIS rates attribution to the source, not the source's own warrant | `c-bd3233c483e5442b` (first-person narrative); vendor rhetoric caveats in `e_live_review_notes.md` |

**What the current evidence says**, all from one AI inspector with no human check:
- GDPR v2(b), the current verifier: 3/25 SUPPORTS wrong (12%, Wilson 4.2–30.0%), all E2a.
- PLC v1: 6/20 (30%, 14.5–51.9%).
- GDPR v1: 1/10.
- Context-only support (E1): 2 of the 55 sampled SUPPORTS (4%), both in PLC v1 (2/20): `c-867ef26bc5a0d84a` and `c-4a2735242356a648`. Two further "CORRECT (caveat)" codes are a loose gloss (`c-47a2a29c52f7d738`) and flattened vendor framing (`c-b1b2c02c076bda50`, closer to E7).
- The DS6 brief's "about 1 in 10" is not borne out by the committed samples.

## 5. A proposed new robustness contrast: E-PLANT-2 (not registered)

**Principle.** Keep every registered definition: adoption (§4 of the protocol), exact one-sided McNemar, the cap rule, e and r_g. Change only the design factors that the literature ties to adoption, so the ungated arm can be persuaded and a gating effect becomes measurable. The contrast still names one variable, gated versus ungated on the same model and documents (L7.4).

**Design changes, ranked by strength of evidence:**
1. **Weak-prior targets** (ClashEval §4.4; Xie et al. on popularity) *(proposed)*.
   - Before plant authoring, ask the ungated model each candidate question closed-book with `null` allowed, as in the E-ABST baseline schema.
   - Keep the targets it answers `null` or answers with no true variant.
   - The pre-screen reads only the question and the true variants. No plant exists yet.
2. **Two planted pages per real page** (Xie et al. "follow the herd", §4.2) *(proposed)*.
   - Gold still needs at least 2 owner-verified real spans. Serve **one** real page in the corpus and hold the second out as gold-only evidence.
   - The two planted pages state the same planted value and sit in different independence clusters, so independence logic alone cannot collapse them.
   - **Reachability risk for the gated arm:** cross-verify reads only the top two same-area spans from other clusters (amendment 1). I5 must confirm, from a logged dry run on the corpus, that the real span reaches that pool for at least 80% of targets *(proposed)*. Otherwise the gate cannot fire by construction.
3. **Smaller deviations within P1** (ClashEval §4.3) *(proposed)*. Scale numbers by [0.67, 0.83] or [1.2, 1.5] instead of [0.5, 0.77] or [1.3, 2.0], but only where the value still lies outside every real page's range.
4. **Optional, I5 to weigh: fewer documents per baseline call.** ClashEval §4.2 shows extra documents lower context bias. This changes the baseline format, so it is a lever, not a default.

**Size and arms** *(proposed)*:
- n = 48 planted targets: 4 domains × 12, none physics, a Track A topic or an N3 gold.
- 12 unplanted **control targets**, stated by real pages only.
- The registered models: Haiku 4.5 as generator and baseline, GPT-5.4-mini as verifier.
- A **top-tier parallel pair** (ungated and gated) on the same inputs with a hard `--max-usd`, per the project rule. ClashEval found context bias differs by model, so the parallel arm is reported in full but read descriptively. The cheap arm alone never settles a decision.

**Thresholds for I5 to check** *(proposed; floors scale with the post-cap n as registered)*:

| Rule | Value | Role |
|---|---|---|
| Calibration pilot (before registration) | Ungated arm only, on 24 held-out targets per design variant. Register only a variant with a_u ≥ 10/24, which passes with P = 0.85 at a true 50%, 0.15 at 30% and 0.02 at 21% (binomial). 12 targets with a_u ≥ 6/12 would pass only 0.61 at 50%. Calibration targets never enter the test set | Measures reachability first instead of asserting it |
| Validity floor | a_u ≥ ⌈0.4 n⌉ = 20/48 on the full baseline set, read before the gated arm runs | Blocks Continue only, as registered |
| Continue | Floor met, **and** a_g < a_u with exact one-sided McNemar p < 0.05, **and** e ≥ ⌈n/3⌉ = 16, **and** r_g ≥ ⌈n/2⌉ = 24, **and** false contradictions on the 12 controls ≤ 2/12 | The last two rules stop the "extract nothing" and "contradict everything" stand-ins from passing |
| Stop | As registered: a_g ≥ a_u at or above the floor; below it, c > b with p < 0.05 | Unchanged |
| Change | As registered (a_g/e > 0.5 names the verifier or contradiction stage; e < ⌈n/3⌉ means under-exposed), plus control false contradictions > 2/12, which names cross-verify specificity | Adds the specificity stage |

**Planning figures** [SYNTHETIC; `ds6_plan.py`; q = share of ungated adoptions the gate keeps; gated-only adoption on 5% of the rest]:

| n | true p_u | P(floor ⌈0.4n⌉ met) | P(McNemar p < .05), q = 0 / 0.25 / 0.5 |
|---|---|---|---|
| 24 (old) | 0.21 (observed) | 0.02 (⌈n/3⌉ floor: 0.11) | 0.33 / 0.16 / 0.05 |
| 48 | 0.21 | 0.001 | 0.72 / 0.46 / 0.18 |
| 48 | 0.40 | 0.46 | 1.00 / 0.96 / 0.75 |
| 48 | 0.50 | 0.90 | 1.00 / 1.00 / 0.92 |
| 48 | 0.60 | 0.997 | 1.00 / 1.00 / 0.98 |

**Inferred:** the new design reaches Continue only if the calibration pilot shows weak-prior selection and herd planting lift ungated adoption to about 50%. At N2's 21% no size rescues it. Hence the pilot before registration.

**A second, cheaper outcome.** WikiContradict-style conflict surfacing (descriptive):
- Use at least 12 owner-confirmed real conflict pairs, against N2's 4.
- Compare the rate at which the ungated answer mentions both values with the pipeline's `Contradiction` recall.
- WikiContradict found that all models "struggle to generate answers that accurately reflect the conflicting nature of the context" (abstract). The reachable best case is therefore likely favourable to the gate [inferred]. It stays descriptive until a floor is set.

**What E-PLANT-2 cannot show.**
- Robustness to sole-source plants. With no real page in context, the verifier can only confirm that the plant's own span entails the claim. Gated and ungated arms would both adopt [inferred]. The single-cluster `thin` slot status is the only defence there, and it is not part of the adoption label.
- That supported claims are true. The registered protocol's own limits (§9) still hold.

## 6. What I5 must run before any registration (L7.3)

1. **Best reachable outcome.** Run the table in §5 on I5's own engine. Add the decision regions for b and c at n = 48 under the post-cap n. Add the cross-verify pool-exposure rate from item 2 of the design changes.
2. **Planted positive.** Simulated arms with b = 10 and c = 0 at n = 48, with every floor met, must read Continue.
3. **Trivial stand-ins must not read Continue:**
   - a gated arm that extracts nothing (r_g = 0);
   - one that marks every numeric claim contradicted (control false contradictions 12/12);
   - a surface classifier that drops planted pages by host or length (P4 must make its AUROC ≤ 0.65 on the authored pages).
4. **Same exclusions in both arms.** The cap rule removes a target from both arms, as registered.

## 7. Owner decision (2026-10-24: option 1, stage it)

The options, ordered by technical merit:
1. **(Recommended) Stage it.**
   - Run the §3 verifier-validity coding first. It is human labelling at $0, and the contrast depends on the contradictions that coding validates.
   - Then an I5-style reachability check of E-PLANT-2 (I5 covered only the old design).
   - Then the ungated-only calibration pilot. The registered baseline cost $0.074 for 24 targets, so the Haiku pilot costs cents; the top-tier pair needs its own `key_headroom.py` estimate.
   - Register E-PLANT-2 only if the pilot shows a_u ≥ 10/24 and that reachability check shows Continue reachable.
   - **Evidence.** The old design had P(floor) = 0.11 and at most 0.33 power at its own observed baseline. Two published levers, prior strength and evidence ratio, explain the shortfall. Each stage is cheap and can stop the line.
   - **What would change this.** If the verifier coding puts natural false support above 20% (one-sided upper bound), or the E-PLANT-2 reachability check shows the real span reaches the cross-verify pool for under 80% of targets, the gate cannot be read, and option 2 is better.
2. **Do not register. Keep N2 INCONCLUSIVE and spend the effort on N3**, the critical path. Still do the §3 coding, because N3 consumes the same verifier labels. Nothing is lost except evidence on H5.
3. **Register E-PLANT-2 now with the §5 thresholds, without the pilot.** This risks repeating a floor miss: P(floor) is 0.46 if true adoption is 40%.

## Sources

- [51] Wu, Wu & Zou (2024). ClashEval: Quantifying the tug-of-war between an LLM's internal prior and external evidence. arXiv:2404.10198. https://arxiv.org/abs/2404.10198
- [52] Hou et al. (2024). WikiContradict: A Benchmark for Evaluating LLMs on Real-World Knowledge Conflicts from Wikipedia. arXiv:2406.13805. https://arxiv.org/abs/2406.13805
- [53] Kirichenko, Ibrahim et al. (2025). AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions. arXiv:2506.09038. https://arxiv.org/abs/2506.09038
- Xie, Zhang, Chen, Lou & Su (2024). Adaptive Chameleon or Stubborn Sloth: Revealing the Behavior of Large Language Models in Knowledge Conflicts. arXiv:2305.13300. https://arxiv.org/abs/2305.13300
- Laban et al. (2023). LLMs as Factual Reasoners: Insights from Existing Benchmarks and Beyond (SummEdits). arXiv:2305.14540. https://arxiv.org/abs/2305.14540
- Thorne, Vlachos, Christodoulopoulos & Mittal (2018). FEVER: a large-scale dataset for Fact Extraction and VERification. arXiv:1803.05355. https://arxiv.org/abs/1803.05355
- Pagnoni, Balachandran & Tsvetkov (2021). Understanding Factuality in Abstractive Summarization with FRANK. arXiv:2104.13346. https://arxiv.org/abs/2104.13346
- Rashkin et al. (2023). Measuring Attribution in Natural Language Generation Models (AIS). arXiv:2112.12870. https://arxiv.org/abs/2112.12870
- Tang, Laban & Durrett (2024). MiniCheck: Efficient Fact-Checking of LLMs on Grounding Documents. arXiv:2404.10774. https://arxiv.org/abs/2404.10774
- Peters & Chin-Yee (2025). Generalization Bias in Large Language Model Summarization of Scientific Research. arXiv:2504.00025 (abstract). https://arxiv.org/abs/2504.00025
