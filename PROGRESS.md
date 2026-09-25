# Research progress

Tracks work against [`ai_education_research_map.md`](ai_education_research_map.md), which remains the single source of state. Each ticked branch links to its note in `research/`.

## Method branches (§4, §5)

### P0
- [x] **Decoding the Disciplines**: `falsify` → **narrow**. Kept as the instructional frame; elicitation (step 2) moves to CTA; evidence rating Low–moderate. [note](research/falsify-decoding-the-disciplines.md)
- [x] **Cognitive Task Analysis**: `explore` → **no rating change, scoped**. Moderate–high for training outcomes outside physics; no physics or transfer data. Provisional physics method: think-aloud while solving, then retrospective CDM probes; §14 DOI for Crandall et al. (2006) corrected. [note](research/explore-cognitive-task-analysis.md)
- [x] **Expert–Novice research**: `explore` → **no rating change, scoped**. Representation differences replicate but form a continuum; principle-first instruction helps immediate problem solving in small physics studies; one far-transfer RCT (Nokes-Malach et al. 2013), no delayed transfer. Adds a published-framework tag to Stage A and an exploratory arm × pretest interaction to Stage B. [note](research/explore-expert-novice.md)
- [x] **Pedagogical Content Knowledge**: `explore` → **no rating change, scoped; PCK layer re-sourced**. Correlational links to school achievement only (mixed in physics), no experiment isolating PCK, no university or transfer outcomes. Physics TAs and instructors miss many common FCI difficulties, so misconception entries are seeded from student response data and teachers review them; §6 moves PCK from expert elicitation to learner diagnosis. [note](research/explore-pedagogical-content-knowledge.md)

### P1
- [ ] Conceptual Change + misconceptions
- [x] **Concept Inventories**: `explore` → **no rating change, scoped to cohort-level use**. Strong class-level validity; weak for individual diagnosis (31% of FCI responses change on retest, mixed models, gender-biased items). PCK-layer seeding and Stage B EMCS use are cohort-level, so defensible; Phase 3 adds test–retest stability; EMCS drops Q16, Q22, Q23. [note](research/explore-concept-inventories.md)
- [ ] Cognitive Apprenticeship
- [ ] Worked Examples + Self-Explanation
- [ ] Intelligent Tutoring Systems
- [ ] Knowledge Tracing / Mastery models

### P2
- [ ] Threshold Concepts
- [ ] Formative assessment
- [ ] LLM-based AI tutoring

### Experiment design
- [x] `/branch experiment`: gated two-stage design (K0 exam-error check → Stage A, 12 experts, AI vs human probes validated against the trace → K1 → Stage B, RCT with about 370 students on delayed transfer → K2). `methods-critic`: no fatal flaw; the six major fixes are applied. [note](research/experiment-ai-assisted-cta-physics.md)

## Minimum reading pack (§8)
- [ ] Pace (2017), _The Decoding the Disciplines Paradigm_. **Read first:** controlled outcome data here could flip the DtD verdict back to keep.
- [ ] Shulman (1986), PCK
- [ ] Chi, Feltovich & Glaser (1981), expert–novice physics
- [ ] Clark et al. (2008), Cognitive Task Analysis
- [ ] Kulik & Fletcher (2016), ITS meta-analysis
- [ ] Kestin et al. (2025), AI tutoring RCT in physics
- [ ] _(optional)_ Hestenes, Wells & Swackhamer (1992), Force Concept Inventory

## Research phases (§9)
- [ ] **Phase 1**: validate the premise; taxonomy of hidden knowledge. Kill criterion not yet testable.
- [ ] **Phase 2**: expert-elicitation experiment (ordinary explanation vs human-led vs AI-led DtD/CTA vs think-aloud)
- [ ] **Phase 3**: learner-bottleneck diagnosis
- [ ] **Phase 4**: intervention experiment with transfer as the primary outcome
- [ ] **Phase 5**: adaptive system

## Open evidence gaps that would change a verdict
- [ ] Full text of Fukaya et al. (2025): the pooled PCK–achievement r (open access, blocked to scripts). With Park & Chan (2025) it could move PCK to **Moderate**
- [ ] A controlled university-physics study of expert-representation instruction with **delayed** transfer
- [ ] A controlled comparison of the decoding interview against CTA (would move DtD back to **keep**)
- [ ] A CTA-derived instruction study in physics or university STEM with a **transfer** outcome
- [ ] A test of the provisional physics elicitation method: think-aloud while solving, then retrospective CDM probes

## Infrastructure
- [x] `/branch` and `/elicit` skills, `citation-verifier` and `methods-critic` agents, DOI hook
- [x] Zotero local API responding
- [ ] `openalex` MCP server loaded (runs so far used the OpenAlex REST API)
- [ ] `zotero` MCP server loaded
- [ ] Zotero library seeded with this project's reading (currently no items in this area)
- [ ] DOI hook also checks that the resolved title matches the cited work. It only checks resolution now, so the Crandall et al. (2006) DOI in §14 passed while pointing to the wrong book (now corrected).
