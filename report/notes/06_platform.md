# 06 — Future platform architecture (notes for the report)

Author role: Future Platform Architect. Date: 2026-09-29. Repository HEAD: `754e2e6`.
Weft examined at local clone HEAD `e1c50fb` (2026-09-29), public repo `AdamKrysztopa/weft`.

**Scope of this note.** It designs a platform that does not exist. Almost everything below is
FUTURE WORK. Only the parts tagged IMPLEMENTED IN PoC exist, and each one names its file. The PoC
has no human validation. Nothing here says the system "identifies tacit knowledge". The gap map
produces *gap candidates*; it has not been shown to predict where expert knowledge lies.

**Category tags used below** (from `BRIEF.md`): ESTABLISHED LITERATURE, OBSERVED IN THE PoC,
INTERPRETATION, HYPOTHESIS, FUTURE WORK. Component status tags: IMPLEMENTED IN PoC,
NEXT RESEARCH STAGE, LONG-TERM.

**No new literature citations.** This note adds no `.bib` entries. Where it leans on literature,
it points to `REORIENTATION.md` reference numbers ("R[n]"). Those are leads, not verified by this
agent. The citation agent must verify any that reach the report.

---

## 0. Numbers used in this note, checked against primary artefacts

All OBSERVED IN THE PoC. Checked by reading the JSON, not the README.

| Number | Primary artefact | Value |
|---|---|---|
| Gap candidates (HYP records) | `research/n3/{plc,gdpr_v1,gdpr_v2}/gapmap.json` → `map[].category == "HYP"` | PLC 9, GDPR v1 1, GDPR v2 6 (plus 1 CONTROL record each) |
| Retrieval gaps | same files → `retrieval_gaps` | PLC 21, GDPR v1 46, GDPR v2 60 |
| Closure judge: own rate vs fair control | same files → `checks.mismatched_evidence_control.total` | PLC 0.889 = 0.889; GDPR v1 0.961 = 0.961; GDPR v2 0.958 = 0.958 |
| GDPR v2 admissible as N3 input | same file → `admissible` | `false` |
| E-PLANT ungated adoption | `research/n2/final_adversarial_review.md` (R1) | 5 of 24 targets; validity floor 8 not met. Unverified against `eplant` result JSON by this agent |
| Adversarial precision of pre-final maps | `research/n3/README.md` | 3 of 19 strict, 8 of 19 lenient. Unverified: no JSON tally found; README states it is an adversarial judgement |

The GDPR v2 control rate is 0.958 in JSON; the README rounds it to 0.96. That rounding is fine.

---

## 1. Three evidence worlds

The worlds are already a typed field in code. `residual/src/residual/vocab.py` defines
`World.A = "public"`, `World.B = "organisational"`, `World.C = "human"` (OBSERVED IN THE PoC).
`residual/src/residual/provenance.py` enforces two rules on `Source`: a World C source must be a
human-record kind (interview, think-aloud, observation, learner response, elicitation record), and
exactly the World B sources name their `organisation`. The world is "which body of evidence a
source belongs to, not how it was accessed": public learner datasets are World A, and a public
open-source project's own artefacts are World B (docstring of `World`).

### 1.1 World A — public evidence

- **What it holds.** Textbooks, studies, standards, regulator guidance, forums, public learner
  response datasets, published task analyses.
- **What it can yield** (INTERPRETATION of `REORIENTATION.md` §13): concepts, taxonomy, taught
  heuristics, catalogued misconceptions, cohort-level difficulty from public response data. It
  cannot yield episode-specific cues, perceptual discriminations or organisation-specific practice.
- **Status.** IMPLEMENTED IN PoC for open-web text only (`reconstruct/`, two live domains in N3).
  No curated tier: every N2 web source is host tier `"open"` (decision 0007, stated departure).
  Public learner datasets are not ingested (N4, NEXT RESEARCH STAGE).

### 1.2 World B — organisation-specific evidence

- **What it holds.** Documents, SOPs, wikis, tickets, commits, review threads, logs, incident
  reports, design records. The vocabulary already has these kinds: `PROCEDURE_DOCUMENT`,
  `DOCUMENTATION`, `DESIGN_RECORD`, `ISSUE`, `COMMIT`, `REVIEW_THREAD`, `LOG`, `INCIDENT_REPORT`
  (`vocab.py` `SourceKind`, OBSERVED IN THE PoC).
- **Work-as-imagined versus work-as-done.** `vocab.py` `Practice` has three values: `imagined`
  (prescribes work), `done` (records work), `reported` (someone's account). The design rule
  (`REORIENTATION.md` §11 step 5, §13): an SOP claim stays *imagined* until a log, ticket or
  review corroborates it; the divergence between imagined and done is the organisational form of
  the residual map (HYPOTHESIS).
- **Rationale.** Commits, PRs and ADRs can yield candidate rationale. The notes report that LLM
  rationale recovery has high recall and low precision (`organisational_knowledge.md` §3
  Inferences, lead only). So recovered rationale is a *question to confirm*, never a claim
  (INTERPRETATION).
- **Status.** Schema: IMPLEMENTED IN PoC (the fields exist). Ingestion: none. The only planned
  adapter is a Git-history adapter for E-OSS over public repositories (`docs/plans/n3-gap-map-plan.md`,
  NEXT RESEARCH STAGE). Customer or employee data: LONG-TERM, after E-OSS reads out and under a
  DPIA (`REORIENTATION.md` §21, §23).

### 1.3 World C — human evidence

- **What it holds.** Expert elicitation (interviews, think-aloud, observation, contrasting-case
  classification), expert ratings, learner responses and errors, blind-coder labels.
- **Status.** Types: IMPLEMENTED IN PoC (`WORLD_C_KINDS`, `ObservedResidual` in
  `residual/src/residual/residual.py`). No World C data exist in the new tracks. Track A's
  instrument (`instrument/`) is built and frozen, and it is not part of the NOW programme.

### 1.4 How the worlds interact

The cost order is A → B → C (`REORIENTATION.md` §13). The information flow is not one-way:

1. **A and B build the reconstruction R.** Each claim is bound to a verified span in a World A or
   B source. Its label is `literature_supported` (A) or `organisational_artefact_supported` (B)
   only after a verifier of another model family returns SUPPORTS on our own text
   (decision 0006 rule `label-computed-from-verified-evidence`; decision 0007 rule
   `support-needs-other-family-and-quote-in-span`). OBSERVED IN THE PoC for A.
2. **B checks A, and done checks imagined.** A World B trace can corroborate or contradict an
   imagined claim. A public standard (A) can show that a local SOP (B) departs from it. Both
   directions produce contradiction records, not merged claims. FUTURE WORK.
3. **The gap map predicts where C is needed.** It runs over R only, before any human is asked.
   Its outputs are predictors labelled `inferred` (decision 0008 rule `gap-candidates-are-predictors`).
4. **C answers, and C measures.** Humans answer targeted questions (channel chosen by knowledge
   type, `REORIENTATION.md` §10.3). Validated human items form H. The observed residual is
   H∖R over H∪R_valid (`REORIENTATION.md` §14.1). That measurement is the criterion the gap map is
   scored against. FUTURE WORK.
5. **C feeds back, in two places only.** (a) Validated H∖R items enter the residual corpus with
   the gap-map score they had *before* elicitation (§14.5). This is the calibration set for the
   next gap map. (b) Human verdicts can raise a claim's label to `observed_human_evidence`. C never
   edits R in place: R, gold and human material live in separate ledgers
   (`Ledger.purpose ∈ {reconstruction, gold, surrogate}`, `residual/src/residual/ledger.py`).
6. **The anchoring guard.** At least one human arm stays blind to the reconstruction. Otherwise
   experts anchored on R shrink the measured residual (§13 reordering 4). This is an architectural
   constraint: the elicitation service must be able to run with no access to R.

### 1.5 How evidence labels propagate

The six labels are `observed_human_evidence`, `literature_supported`,
`organisational_artefact_supported`, `inferred`, `synthetic_extrapolation`, `unknown`
(`vocab.py` `EpistemicLabel`). Rules the platform keeps, all derived from existing code or
decisions:

- **Labels are computed, never set.** `ClaimRecord.label` is a property over evidence
  (decision 0006). IMPLEMENTED IN PoC.
- **A label is only as strong as its weakest required link.** A claim is `literature_supported`
  only with a located span *and* a cross-family SUPPORTS verdict. A fabricated quote yields no
  evidence and the claim stays synthetic (decision 0007 `span-is-ours`). IMPLEMENTED IN PoC.
- **Derived outputs are `inferred` at best.** Gap records, gap-map scores, generated questions,
  recovered rationale, domain-model edges proposed by a model: all `inferred` or
  `synthetic_extrapolation`. IMPLEMENTED IN PoC for gap records; FUTURE WORK elsewhere.
- **Synthetic may predict, never decide.** A `Measurement` separates criterion labels from
  predictor labels; an `evidential_gate` refuses a synthetic, inferred or unknown criterion
  (`residual/src/residual/gates.py`; decision 0006 rule `synthetic-never-a-gate-criterion`).
  IMPLEMENTED IN PoC.
- **Labels move up only through World C or cross-family verification.** A human verdict can
  move a claim to `observed_human_evidence`. FUTURE WORK (types exist, no data).
- **World B labels carry the organisation.** An `organisational_artefact_supported` claim cannot
  leave its organisation's tenant. FUTURE WORK (the `organisation` field exists; no enforcement).

---

## 2. Components of the full platform

Each entry: status tag, responsibility, inputs → outputs, what exists (file path), main technical
risk. "Exists" statements are OBSERVED IN THE PoC; everything else is FUTURE WORK or HYPOTHESIS.

### 2.1 Autonomous research (domain reconstruction orchestration) — IMPLEMENTED IN PoC (walking skeleton)

- **Responsibility.** Given a domain and task scope, plan searches, fetch, extract atomic claims
  bound to spans, and hand them to verification. One-way orchestration, no agent loop.
- **In → out.** Domain + task → N1 `Ledger` (`ledger.json`) + run sidecar + `calls.jsonl`.
- **Exists.** `reconstruct/src/reconstruct/run.py` (plan → search → fetch → extract → locate →
  independence → verify), `web.py`, `llm.py`, `report.py`. Hard `--max-usd` budget checked before
  every call (decision 0007 `budget-before-every-call`).
- **Risk.** Retrieval is chosen by the generator family (adversarial review R7) and host tables
  are tuned to the E-LIVE domains (R8). Extraction truncation dropped 5 of 25 documents in one run
  (R5). A curated tier does not exist. Research validation (E-PLANT, E-ABST, E-LIVE v3) is
  deferred (`research/n2/closeout.md`).

### 2.2 Evidence ledger — IMPLEMENTED IN PoC

- **Responsibility.** The single typed contract between stages: claims, evidence, sources,
  verifications, contradictions, areas, assignments. Kept apart by purpose.
- **In → out.** Claims and evidence from any producer → a frozen, hash-addressable ledger that
  every consumer reads.
- **Exists.** `residual/src/residual/{claims,provenance,ledger,vocab}.py`; schema hash-frozen in
  `residual/frozen/n1.json`; `Ledger.as_of(date)` for dated views.
- **Risk.** Python cannot stop deliberate forgery (decision 0006 Consequences). The ledger is
  not quite the *only* contract today: `gapmap` also reads the run sidecar for admissibility and
  unexamined slots (`gapmap/src/gapmap/__main__.py`, `_admissibility_note`, `unk_gaps`). The
  sidecar is untyped JSON. A platform would promote run status into a typed record. Scale: one
  JSON file per run does not scale to an organisation's corpus.

### 2.3 Provenance verification — IMPLEMENTED IN PoC (open web only)

- **Responsibility.** Make every span a slice of text we fetched and hashed; verify support with
  another model family; cluster sources by independence before counting corroboration; treat
  retrieved text as data.
- **In → out.** Fetched text + extracted claim → `Evidence(Selector(sha256:…;char=a,b))` +
  `Verification` or nothing.
- **Exists.** `reconstruct/src/reconstruct/evidence.py` (the only module allowed to build
  `Evidence`, `Selector`, `Verification`); `web.py` `SnapshotStore` (content-addressed);
  `verify_run.py` (offline re-slice of every evidence item).
- **Risk.** Decoy validity is self-certified, so decoy false-accept rates are not an estimate of
  verifier validity (adversarial review R2). Span-level duplicate detection misses short derived
  copies (R3), which inflates corroboration. `verify_run` does not rehash snapshots against their
  filenames (R9). Verifier false-support on natural claims post-fix is unmeasured
  (`docs/plans/n3-gap-map-plan.md`, "Risks carried from N2").

### 2.4 Contradiction analysis — NEXT RESEARCH STAGE (a stub exists)

- **Responsibility.** Find claims that conflict, across sources and across worlds (A vs B,
  imagined vs done), and keep them as first-class records rather than letting a synthesiser
  flatten them (`REORIENTATION.md` §10.1: claim clustering plus NLI).
- **In → out.** Ledger claims → `Contradiction` records with scope flags.
- **Exists.** The `Contradiction` type (`residual/src/residual/ledger.py`). In N2, a cross-verify
  REFUTES verdict becomes a contradiction (`reconstruct/src/reconstruct/run.py`). No clustering,
  no NLI.
- **Risk.** Scope-flagged REFUTES (different subject or jurisdiction) become false contradictions
  (adversarial review R4). Across worlds the risk grows: an SOP and a ticket often describe
  different scopes. Models adopt wrong retrieved content over correct priors often
  (`REORIENTATION.md` R[51], lead only), so the detector must not be the generator.

### 2.5 Domain learning model (layered representation) — NEXT RESEARCH STAGE / LONG-TERM

- **Responsibility.** Hold the domain as a layered composite, not an ontology: L0 terminology,
  L1 structure (index only), L2 performance and expertise (KC with condition part, decisions,
  cues), L3 learner and difficulty, L4 diagnosis, L5 instruction, L6 epistemics
  (`REORIENTATION.md` §10; `expertise_representation.md` §8).
- **In → out.** Ledger claims → typed domain units with links to the claims that support them.
- **Exists.** Only the `Layer` enum (`vocab.py`: L1–L5) and the `KnowledgeType` / `Tacitness`
  axes. No graph, no KC model. L6 epistemics is, in effect, the ledger itself.
- **Risk.** Prerequisite, causal and procedural edges are not reliably recoverable from text
  (§11). The four missing objects (cue as discrimination, bottleneck hypothesis, framework
  crosswalk, certainty for elicited knowledge) have no mature standard (§10.2). A graph-only model
  (H6) is the default to beat, not the design.

### 2.6 Methodology-guided gap detection — IMPLEMENTED IN PoC (candidates only)

- **Responsibility.** Fire methodology lenses (DISC, DIAG, SEL, HEDGE, GUARD, WHY, RESULT) where
  sources attest a construct but not its content; judge closure; emit three-tier records
  (observed evidence / inferred gap / hypothesis) and retrieval gaps.
- **In → out.** Ledger (+ sibling ledger, + sidecar) → `gapmap.json`, `gapmap.md`,
  `closure_judgements.json`.
- **Exists.** `gapmap/src/gapmap/{lenses,semantic,judge,record,rank,render,checks,config}.py`;
  maps in `research/n3/{plc,gdpr_v1,gdpr_v2}/`. Replay is offline and byte-identical.
- **Risk.** The closure step is not informative: own rate equals the fair-control rate on every
  ledger (0.889, 0.961, 0.958; §0). Precision 3 of 19 strict (unverified tally). Lexicons are
  in-sample and `config.py` is not yet hash-frozen. This is the component whose failure decides
  the programme (N3 stop rule → H3).

### 2.7 Company retrieval (World B ingestion) — NEXT RESEARCH STAGE (public Git) / LONG-TERM (customer data)

- **Responsibility.** Acquire World B artefacts with dates, authorship, and access rights; expose
  them to provenance verification as fetchable, hashable text.
- **In → out.** Repositories, ticket systems, wikis, document stores, logs → `Source` records with
  `world=B`, `organisation`, `practice`, `independence_key` (author-based), `published` date; text
  snapshots addressed by hash.
- **Exists.** Nothing. Plans name a Git-history adapter for E-OSS "Not Weft yet"
  (`docs/plans/n3-gap-map-plan.md`).
- **Candidate substrate.** Weft (section 6). Not a dependency today.
- **Risk.** Access control (a retrieval layer that ignores per-user rights leaks), prompt
  injection through ingested text (R11), personal data in every artefact, and authorship metrics
  that AI-generated code may break (R8 in `REORIENTATION.md` §16).

### 2.8 Expert elicitation — LONG-TERM for new tracks (Track A instrument exists, frozen)

- **Responsibility.** Ask experts the gap map's questions through the channel matched to the
  knowledge type; record answers as World C evidence; keep one arm blind to R.
- **In → out.** Ranked questions (target claim, type, channel, probe) → elicitation records,
  coded operations, human verdicts on claims.
- **Exists (Track A only, not reusable by import).** Turn contract
  (`instrument/src/probe_app/contract.py`: known stem, at most one follow-up per stem, quoted span
  from the expert's own words); leading-question guard called on every AI turn
  (`instrument/src/probe_app/engine.py`); guard audit and trace corroboration
  (`instrument/src/probe_code/guard_audit.py`, `corroboration.py`); pre-registered freeze of model
  IDs and prompt hashes (decision 0001, 0004). Reuse is by copying into `residual/` or a new
  package, never by importing `instrument/` (decision 0006 `track-a-reused-by-copy`).
- **Risk.** Anchoring on R; LLM interviewer leading the expert; channel mismatch (think-aloud
  surfaces only heeded information, `REORIENTATION.md` §10.3, lead only); personal data and consent.

### 2.9 Human Knowledge Residual measurement — NEXT RESEARCH STAGE (types exist)

- **Responsibility.** Compute recall of H, the unvalidated R∖H count, the observed residual
  (once validity judgements exist), and the unseen-item estimate with its known-truth check,
  stratified by knowledge type.
- **In → out.** Reconstruction ledger + gold or human ledger + matches → `ObservedResidual`,
  `EstimatedResidual`, `ResidualAccount`, `Coverage`.
- **Exists.** Types and validators in `residual/src/residual/residual.py` (`EstimatedResidual`
  allows `chao1`, `jackknife`, `mh`, `lincoln_petersen`). No estimator is implemented and no gold
  has been acquired.
- **Risk.** Fatal-class R4: never-written items are invisible to text occasions, and dependent
  occasions give stable underestimates (`REORIENTATION.md` §14.1). The matcher becoming the gold
  (R5). Never report a residual of zero.

### 2.10 EIG question selection — NEXT RESEARCH STAGE

- **Responsibility.** Choose the next question by expected information gain over contested model
  elements, with a pre-registered fraction reserved for confident-but-unverified areas
  (unknown-unknowns guard, §14.2).
- **In → out.** Gap map + current beliefs → ranked questions with target claim, type, channel.
- **Exists.** Nothing. `gapmap/src/gapmap/rank.py` orders candidates by breadth, not by
  information gain.
- **Risk.** No study was found applying EIG to expert or CTA interviews (§14.4). Adaptive
  questioning breaks equal catchability for the residual estimate (§14.1 pitfall 3), so the
  selection service and the measurement service must log which questions were adaptive.

### 2.11 Learner diagnostics — LONG-TERM (public data: NEXT RESEARCH STAGE)

- **Responsibility.** Build bottleneck hypotheses from learner responses: observation, focal
  knowledge claimed missing, named alternatives, expert–novice contrast (§10.2 object 2).
- **In → out.** Public response data (N4: E-KC, E-DIST, E-MISC), later own learner data → L3/L4
  units with evidence.
- **Exists.** `Voice.NOVICE`, `SourceKind.LEARNER_RESPONSE`, `Question.LEARNER_STATE` in `vocab.py`.
  No data, no model. The N3 ledgers hold only expert-voiced text, so no lens claims a learner
  difficulty (`research/n3/README.md`).
- **Risk.** Synthetic learners are negative evidence (§12). Per-student diagnosis falls under AI
  Act Annex III(3)(b) (`REORIENTATION.md` §21; legal status as stated there, not verified here).

### 2.12 Instructional design — LONG-TERM

- **Responsibility.** Turn validated residual items and bottleneck hypotheses into whole tasks,
  supportive and procedural information, and part-task practice (L5, 4C/ID-style per §10).
- **In → out.** Validated items (labels `observed_human_evidence` or criterion-supported) →
  instructional materials that cite their claims.
- **Exists.** Nothing.
- **Risk.** Building instruction on unvalidated gap candidates would teach predictions as facts.
  Hard rule: only criterion-labelled claims may enter instructional content.

### 2.13 Adaptive learning — LONG-TERM

- **Responsibility.** Sequence practice per learner from a learner model.
- **Exists.** Nothing. Explicitly not built now (`REORIENTATION.md` §23).
- **Risk.** Unguarded LLM help can raise practice performance and lower unassisted performance
  (§22 MUCH LATER, R[166], lead only). Legal exposure as in 2.11.

### 2.14 Validation loops — IMPLEMENTED IN PoC (gates, freezes, checks) / NEXT RESEARCH STAGE (gold tests)

- **Responsibility.** Make every stage end in a pre-registered continue/change/stop reading of an
  experiment result, computed by code.
- **Exists.** `residual/src/residual/gates.py` (`evidential_gate`, `Threshold`, `GateDecision`);
  `residual/src/residual/freeze.py`; `gapmap/src/gapmap/checks.py` (anti-renaming, mismatched
  evidence control, lexical donor null, cross-run stability); `reconstruct/src/reconstruct/{eplant,eabst}.py`
  harnesses; architecture rules enforced as tests (decisions 0006–0008, `pytest-archon` bindings).
- **Risk.** `Threshold.registered_in` is free text (decision 0006). Several thresholds in
  `REORIENTATION.md` §22 are still "to set". Two decision-0008 rules are review-only, not tested.

### 2.15 Cross-cutting: run ledger and cost (N9) — IMPLEMENTED IN PoC (per-call log)

- **Exists.** `calls.jsonl` per run, logging every call including failures, with served-model
  check and cost (decision 0007 rules). `failed_calls_by_task` counts in the sidecar.
- **Missing.** Cost per *validated* item (E-COST), which needs World C.

---

## 3. Layered architecture — specification for ONE figure

**Title suggestion.** "Platform layers: what the PoC built and what is planned."

**Visual convention.**
- Solid fill, solid border: IMPLEMENTED IN PoC.
- White fill, dashed border: NEXT RESEARCH STAGE.
- White fill, dotted grey border, grey text: LONG-TERM.
- Solid arrow: data flow that exists in code. Dashed arrow: planned flow.
- One thick red dashed arrow for the World C feedback loop (the criterion path).
- A small lock icon on components that must enforce tenant and access rights.
- Legend box bottom-right with these five items.

**Layers (bottom to top).** Draw as horizontal bands; components as boxes inside.

| Band | Components (status) | Notes for the drawer |
|---|---|---|
| **1. Evidence sources** | World A public text (solid); World A public learner data (dashed); World B public OSS Git history (dashed); World B organisational artefacts (dotted, lock); World C experts and learners (dotted, lock) | Three columns labelled A, B, C. Label B's sub-box "work-as-imagined / work-as-done" |
| **2. Acquisition** | Web search + fetch + snapshot store (solid, `reconstruct/web.py`); Git adapter (dashed); Company retrieval, candidate substrate Weft (dotted, lock, caption "optional, not a dependency"); Elicitation service with turn contract + leading-question guard (dotted; caption "Track A ideas, reused by copy") | Weft box sits only under the World B column |
| **3. Provenance and verification** | Span location on our own text, cross-family verifier, independence clustering, injection flagging (solid, `reconstruct/evidence.py`); Contradiction detector with scope flags (dashed; "REFUTES stub exists") | All acquisition arrows must pass through this band. No arrow may bypass it into band 4 |
| **4. Evidence ledger (the contract)** | Claim records, six computed labels, `Ledger.purpose` = reconstruction / gold / surrogate, `as_of` dated views, hash freeze (solid, `residual/`) | Draw as one wide band. Three stacked sub-boxes for the three ledger purposes, separated by a thick line ("never mixed") |
| **5. Analysis** | Methodology-guided gap detection (solid, `gapmap/`, caption "candidates; closure not informative"); Domain learning model L0–L6 (dashed/dotted split: dashed for L2 and L6, dotted for the rest); Residual measurement (dashed, "types exist"); EIG question selection (dashed) | Gap detection outputs go right, to band 6, labelled "predictor (inferred)" |
| **6. Human loop** | Targeted residual questions (dashed); Expert elicitation with blind arm (dotted); Learner diagnostics (dotted); Blind second coder (dashed) | Blind arm drawn with no arrow from band 4 into it |
| **7. Applications** | Organisational knowledge-at-risk report (dotted); Instructional design (dotted); Adaptive learning (dotted) | Arrow into 7 only from criterion-labelled claims in band 4 |
| **Side rail (full height, right)** | Validation loops: gates refuse synthetic criteria, pre-registered thresholds, freezes, controls (solid); Run and cost ledger `calls.jsonl` (solid); Security and privacy: tenant isolation, ACL, DPIA, audit (dotted) | Rail touches every band |

**Data flows to draw.**
1. A sources → acquisition → provenance → reconstruction ledger (solid).
2. B sources → Git adapter / company retrieval → provenance → reconstruction ledger (dashed).
3. Reconstruction ledger → gap detection → questions (solid up to "gap map", dashed to "questions").
4. Questions → elicitation (dashed) → World C records → **gold / human ledger** (dashed).
5. Human ledger + reconstruction ledger → residual measurement → gate (red dashed feedback) →
   residual corpus → gap-map calibration (red dashed, back into band 5).
6. Synthetic material (surrogate ledger) → gap detection as predictor only (thin dashed, labelled
   "predictor, never criterion"). No arrow from the surrogate ledger to any gate.
7. Validated claims → applications (dotted).

**Caption draft.** "Solid boxes exist in the PoC (`residual/`, `reconstruct/`, `gapmap/`).
Dashed boxes are the next research stage; dotted boxes are long-term. Every source passes the
provenance band before it reaches the ledger. The gap map's output is a predictor. Only World C
evidence, via residual measurement, can score it."

---

## 4. Non-functional requirements for organisational deployment

All FUTURE WORK. Each requirement names the PoC property it extends, where one exists.

### 4.1 Security

- **Retrieved text is data.** Extend decision 0007 `retrieved-text-is-data` to World B: the
  planner never sees artefact text; extractors get no tools; injection-pattern spans are flagged
  and held PENDING. Ticket and chat content is a stronger injection vector than public web pages
  (R11, `REORIENTATION.md` §16).
- **Least privilege for connectors.** Read-only credentials, scoped per repository or space.
- **Plugin trust.** Any retrieval substrate that runs third-party plugins in-process (Weft does;
  its `SECURITY.md` says "a pack runs with your full privileges") needs an allow-list and pinned,
  reviewed packs in deployment.
- **Model boundary.** One configured backend per role, served-model check on every response,
  fallback lists refused (decision 0007). Keep this for on-prem models too.

### 4.2 Privacy and GDPR

Legal points below are taken from `REORIENTATION.md` §21, which marks them as information, not
legal advice, and relies partly on secondary sources. Not re-verified here.

- **Artefact-coverage mode by default.** Output "this subsystem's rationale is undocumented",
  not "only person X knows this".
- **Person-level concentration only pseudonymised, or with consent to be named.** No use of
  outputs to evaluate or allocate people (keeps clear of AI Act Annex III(4) as §21 reads it).
- **DPIA before ingestion** (systematic processing of employee messages and Git history), a
  legitimate-interest balancing test, and a works agreement where German co-determination applies
  (§ 87(1) no. 6 BetrVG as cited in §21).
- **Data minimisation.** Store the spans that evidence claims, plus their hashes. Do not store
  whole mailboxes or chat histories in the ledger. Snapshots are kept inside the tenant and
  expire under a retention policy.
- **Right to erasure versus an immutable ledger.** A content-addressed, append-only ledger
  conflicts with erasure. Design answer: keep personal data out of claim text where possible;
  store author identity as a pseudonym whose key lives outside the ledger; on erasure, delete the
  key and the snapshot, and mark affected evidence `source_withdrawn` so labels recompute. This
  needs a schema change and a re-freeze (decision 0006). HYPOTHESIS; untested.
- **World C data.** Consent, pseudonyms, git-ignored storage and encrypted backup already exist
  in Track A (decision 0001; `probe-app backup`). Reuse the pattern, by copy.

### 4.3 Access control

- **Retrieval must enforce per-user ACLs** (§21 security bullet). A claim inherits the most
  restrictive ACL of its evidence. A gap map computed over restricted evidence is itself
  restricted.
- **Tenant isolation.** One organisation's World B claims never enter another's ledger or the
  cross-domain residual corpus without explicit, contractual release and de-identification.
- **The label depends on who can see the evidence.** A reader without access to a claim's only
  supporting span must see it as `unknown` for them, not as supported. FUTURE WORK; no current
  type expresses this.

### 4.4 On-prem models

- **Why.** Organisational artefacts often cannot leave the premises.
- **Constraint from the PoC.** Verification must cross model families (decision 0006, 0007), and
  the closure judge must differ from generator and verifier (decision 0008). On-prem therefore
  needs at least three model families available locally.
- **Precedent in the PoC.** The N3 closure judge already runs locally (Ollama
  `qwen2.5:7b-instruct`, decision 0008). OBSERVED IN THE PoC. It also shows the risk: that 7B
  judge did not beat its fair control (§0). A stronger local judge is untested.
- **Replay by default.** Cache every model verdict with its prompt hash; replay offline
  (decision 0008 `gapmap-replays-by-default`). This supports audit and air-gapped review.

### 4.5 Audit trails

- **Exists.** `calls.jsonl` logs every model and search call, including failures, with served
  model and cost; snapshots are content-addressed; `verify_run` re-slices evidence offline;
  schema and prompt hashes are frozen. OBSERVED IN THE PoC.
- **Add.** Who viewed or exported which gap map; which human verdict changed which label, with
  timestamp and pseudonym; retention and erasure events. Append-only, tamper-evident (hash chain).

### 4.6 Cost

- **Exists.** Hard `--max-usd` budget checked before every call (decision 0007). N2's reruns
  were blocked by budget, and N3 could not afford a third domain ("the OpenRouter budget is $0",
  `research/n3/README.md`). OBSERVED IN THE PoC: cost already limits research scope.
- **Metric.** Cost per *validated* item (E-COST, N9), not cost per claim. Human minutes are the
  dominant cost once World C starts (HYPOTHESIS).
- **Levers.** Local models for closure judging; caching and replay; retrieval before generation;
  incremental re-verification only of evidence whose source hash changed.

---

## 5. Key architectural decisions and their justification

Decisions 1–6 are already made in the repository (OBSERVED IN THE PoC as decisions; their benefit
is INTERPRETATION). Decisions 7–10 are proposals for the platform (HYPOTHESIS / FUTURE WORK).

1. **The evidence ledger is the single contract between stages.** Producers
   (`reconstruct/`, later adapters and elicitation) write N1 types; consumers (`gapmap/`, later
   residual measurement) read them. Justification: stages can be swapped or re-run without
   touching each other, and every consumer sees the same labels. The core package depends only on
   pydantic (decision 0006 `residual-core-provider-neutral`). Caveat: the run sidecar is a second,
   untyped input today (2.2); the platform should type it.
2. **Synthetic output may be a predictor, never a criterion.** Enforced by `evidential_gate`.
   Justification: LLM-simulated participants and panels are unreliable as ground truth
   (`REORIENTATION.md` §1, §12; R[67][72][74], leads only). Without this rule, the system would
   grade its own predictions.
3. **Labels are computed from evidence, never set.** Justification: a hand-set "supported" is
   exactly the failure the project studies (unsupported citations in deep-research systems,
   §1, leads only).
4. **Support crosses a model-family boundary, and the span is ours.** Justification: a model
   cannot verify its own output; a model's quotation is not evidence until located in text we
   fetched (decision 0007).
5. **Gold, reconstruction and surrogate material never share a ledger.** Justification:
   anti-circularity (§14.3); held-out gold must stay held out.
6. **Reuse Track A by copy, never by import.** Justification: Track A is frozen and
   pre-registered; an import would let new-track changes alter a registered instrument
   (decision 0006).
7. **Provenance is a mandatory band.** No acquisition path, including a future Weft adapter, may
   write evidence directly. Only the evidence module builds `Evidence`, `Selector`,
   `Verification` (decision 0007 `only-evidence-builds-evidence`, extended platform-wide).
8. **Gap-map outputs are routed by tier.** Retrieval gaps trigger search or verification;
   only hypotheses reach humans (decision 0008 `retrieval-gaps-never-hypotheses`). Justification:
   expert time is the scarce resource; "few sources" is not "experts know something".
9. **The elicitation service can run blind to R.** Justification: the anchoring guard (§13).
   Architecturally, the question generator and the blind arm's interviewer must be separable.
10. **Compliance defaults live in the core, not in an enterprise add-on** (§21 Decisions).
    Justification: the organisational wedge is blocked by DPIA and works-council review
    otherwise (R10).

**What is deliberately not in the architecture** (`REORIENTATION.md` §23): no GraphRAG-style
graph as the domain model (a graph indexes, it does not hold, the model); no learner-facing tutor
before learner data; no UI beyond inspection; no person-attributed expertise inference.

---

## 6. Weft

### 6.1 What Weft is today (OBSERVED, from the Weft repository)

- A retrieval-augmented generation (RAG) engine built as a microkernel. The kernel
  (`packages/weft-kernel`) holds the registry, discovery, pipeline model and payload types. All
  capabilities are plugins ("packs") discovered through Python entry points. The release set
  `weft-rag` bundles many packs. The counts disagree across Weft's own files: README says 23
  top-level packages and 21 packs; CLAUDE.md says 26 packages and 23 packs; `packages/weft-rag/src`
  holds 26 package directories. Report "about two dozen packs", not an exact count. Published on PyPI:
  `weft-rag 2.7.0`, `weft-kernel 0.2.1` (README). MIT licence. Public GitHub repository.
- **Ingestion.** Indexes a *directory* of files. Text extractor handles `.txt` and `.md`
  (`weft_extract/text.py` `EXTENSIONS`); PDF extractors handle `.pdf` (`weft_pdf`, `weft_docling`).
  No connectors for Git history, issue trackers, wikis, chat or logs were found in `packages/weft-rag/src`.
- **Storage.** Postgres + pgvector by default; Qdrant optional.
- **Retrieval and generation.** Dense retrieval is the default; many opt-in "rungs" (hybrid,
  rerankers, RAPTOR, a graph pack, whole-corpus generation, a `contradiction-aware` rung).
  Its own evidence page reports dense recall@5 0.986 on Open RAGBench and labels reused public
  benchmark results "exploratory" (`manual/evidence.md`). Most rungs show no gain, harm, or are
  unmeasured; multi-hop and corpus-wide questions have no evidence either way.
- **Provenance it keeps.** Each `Node` has immutable `Lineage` (parent node ids and the union of
  source ids), computed, not authored (`weft_kernel/payload/lineage.py`, `node.py`). Each indexed
  document has a `SourceRecord` with `uri`, `content_hash` (SHA-256), `indexed_at`, `pipeline`,
  and `pipeline_identity` (a digest of what the pipeline actually ran)
  (`weft_store/contract.py`). Deleting a source cascades to every descendant. Synthetic nodes
  (summaries with no lineage) must carry an explicit `SyntheticOrigin` reason.
- **What it does not keep.** Character offsets from a chunk back into its source:
  `weft_chunk.payload.ChunkOffset` was withdrawn on 2026-09-12 (`docs/02-extension-model.md`).
  Pages are recorded for PDFs (`page: int` in `weft_pdf/document.py`). No publication date for
  a source, only `indexed_at`.
- **Access control.** A `tenant_id` is required on every run `Context`, and the plugin instance
  cache is keyed by tenant (`weft_kernel/context.py`, `runner.py` `TenantMismatchError`). No
  per-user or per-document ACL was found.
- **Trust model.** Packs run in-process with full privileges; Weft states it cannot sandbox them.
  It offers an allow-list (excluded packs are never imported) and a record of which distributions
  ran (`SECURITY.md`).

### 6.2 Is integration justified?

**Not now.** edu_proj does not depend on Weft, and the NOW programme has no World B ingestion to
serve (plans say "Not Weft yet"). E-OSS needs only a Git-history adapter over public repositories,
which Weft does not provide.

**Possibly later, for one role only: a World B candidate-retrieval substrate** in the
organisational pilot (§20 step 6), once E-OSS has read out. INTERPRETATION of why it could fit:

- Weft and edu_proj share design values: computed lineage, content hashes, explicit synthetic
  origin, pipeline identity digests, refusal instead of silent fallback, measured-before-trusted
  retrieval rungs. That lowers the cost of a strict adapter.
- Organisational corpora are large. edu_proj's per-run JSON and open-web search do not scale to
  them; Weft's incremental indexing, reconcile and cascade delete do.

### 6.3 How: the interface (FUTURE WORK)

Weft would sit in band 2 (acquisition), under World B only. It would **propose candidates**; it
would never **produce evidence**.

**What Weft would provide.**
- `search(query, tenant, principal) → [(source_id, uri, content_hash, node_id, passage_text, page?)]`
- `fetch_source(source_id) → bytes` whose SHA-256 equals `content_hash`.
- `source_meta(source_id) → uri, content_hash, indexed_at, pipeline_identity, status`.
- A run manifest: packs loaded and `pipeline_identity`, for the audit trail.

**What the evidence model imposes (the contract).**
1. **Spans are ours.** edu_proj re-reads the source bytes, checks the SHA-256 against Weft's
   `content_hash`, normalises the text itself, and locates the passage verbatim. Only then does
   `evidence.py` build a `Selector` (`sha256:…;char=a,b`). Weft's chunk text is never the span
   (decision 0007 `span-is-ours`). Needed because Weft no longer records chunk offsets.
2. **Hashes are checked, not trusted.** A mismatch between fetched bytes and `content_hash`
   discards the candidate.
3. **Provenance fields Weft lacks are supplied by the adapter, from the system of record:**
   `SourceKind` (commit, issue, SOP…), `Practice` (imagined / done / reported), `Voice`,
   `published` date (for `Ledger.as_of`), `organisation`, and an author-based `independence_key`.
   `indexed_at` is not a publication date and must never be used as one.
4. **Access control is enforced before retrieval returns, per principal.** Weft's tenant key is
   necessary but not sufficient. Either Weft gains document-level ACL filtering (a new pack and
   store change), or the adapter post-filters against the system of record's permissions and
   logs every filtered hit. A claim inherits the most restrictive ACL of its evidence.
5. **Retrieval only.** No Weft generation rung (`*-then-generate`, `whole-corpus-then-generate`,
   `contradiction-aware`) may write into the ledger. Their outputs are synthetic by the
   project's rules and could at most be predictors.
6. **Pinned configuration.** A frozen `weft.toml` allow-list and `pipeline_identity` recorded in
   each run sidecar, so a change of embedder or chunker is visible and invalidates comparisons.
7. **Retrieval choice is measured, not inherited.** Weft's rungs were measured on public QA sets,
   not on organisational artefacts or on the question "which evidence closes this gap". Any rung
   used must be measured on the target corpus first.

A new ADR would be needed. Decisions 0006–0008 keep `residual/` and `gapmap/` free of retrieval
dependencies; the adapter would be a new sibling package that depends on both `residual` and
`weft-rag`, never the reverse.

### 6.4 Risks

- **Offset loss.** Without chunk offsets, locating the passage relies on verbatim match after
  normalisation. PDF-extracted text may differ between Weft's extractor and ours, so located-span
  yield could drop. Measure it before relying on it.
- **Retrieval bias becomes evidence bias.** Whatever Weft does not retrieve cannot be evidence,
  and a gap map over it will read retrieval misses as knowledge gaps. The RG-UNK / RG-SINGLE
  routing (decision 0008) must stay in force.
- **ACL leakage.** Tenant keying alone does not stop one employee's query surfacing another
  team's restricted document.
- **In-process plugins.** A pack runs with the adapter's credentials to the organisation's data.
- **Two moving projects.** Weft changes fast (daily commits at the time of writing); pin versions
  and re-run the adapter's contract tests on each upgrade.
- **Scope creep.** Using Weft's answer generation would reintroduce the monolithic-LLM pattern
  (H5) that the gated pipeline exists to beat.

### 6.5 What not to claim

- Do not claim edu_proj uses, depends on, or has been tested with Weft. It has not.
- Do not claim Weft provides verified provenance in edu_proj's sense. It provides lineage and
  content hashes; it does not verify that a passage supports a claim.
- Do not claim Weft retrieves organisational artefacts (tickets, commits, wikis). Today it
  indexes `.txt`, `.md` and `.pdf` files from a directory.
- Do not claim Weft enforces per-user access control. It keys runs by tenant.
- Do not cite Weft's retrieval numbers as evidence about edu_proj's World B quality. They were
  measured on public QA benchmarks, and Weft labels them exploratory.

---

## Verification lines

No bibliography entries were added by this note. Repository facts were checked in the files named
inline. Weft facts were checked in the local clone at `e1c50fb`; GitHub visibility checked with
`gh api repos/AdamKrysztopa/weft` (public). Items marked "unverified" in §0 were not traced to a
result JSON.
