# N1 schema validation: cross-domain gold items

**Gate** (`REORIENTATION.md` §22 N1). *Continue* if every gold item from mathematics, clinical and OSS sources can be expressed without new field types. *Change* the schema if more than a handful need ad-hoc fields. "A handful" was registered before the claim model existed (`b7c0e5d`): **≤ 2 new field types**, where a field type is a new field, model or closed-vocabulary member.

**Result: continue, with 1 addition.** `KnowledgeType.INTERPRETATION` was added. Nothing else was needed.

## Method

- **Test set.** `docs/n1-gold-shapes.md` lists 16 gold shapes and 25 illustrative items in the sources' own terms. It was written by an agent that never saw the claim model, and committed before `claims.py` existed. No gold was acquired (§14.3).
- **Fixtures.** Every item is expressed in `residual/tests/cross_domain.py`, and `residual/tests/test_cross_domain.py` checks it. The three gold ledgers validate, round-trip through JSON, and carry only criterion labels.
- **When an attribute counts as expressed.** It is in a typed field; or it is in assertion or locator text and no registered NOW metric (§18, §22) computes on it. An attribute that a NOW metric computes on, but that lives only in text, would need a field and would count.
- **Counting rule** (applying the registered wording). A new model counts 1, including its own fields. A new field on an existing model counts 1. A new member of an existing vocabulary counts 1. A new parameter on a function is interface, not a field type; it is listed separately below.

## Additions

| # | Addition | Forced by | Why no existing type fits |
|---|---|---|---|
| 1 | `KnowledgeType.INTERPRETATION`: what an observed result means for the working hypothesis | B3 Chao & Salvendy (interpretations); B5 PARI (the I of P-A-R-I) | §14.2 uses "interpretations" as a gap-map knowledge-type distinction: they have the lowest pooled coverage [2]. Mapping them to `cue`, `decision` or `expectancy` would erase that feature. |

**Interface additions, not field types.** `ResidualAccount.recall(weights=...)`: E-MISC's prevalence-weighted recall (§18, N4) weights each gold item by a `Measurement` over that item. The weighted recall inherits those measurements' criterion labels, so a surrogate's prevalence can never weight a gate (§12).

## Where each attribute lives

**Mathematics.** Gold ledger labels: observed human evidence for items resting on response data, literature-supported for the rest.

| Shape | Attribute | Lives in |
|---|---|---|
| A1 Eedi + NeurIPS 2020 | Misconception text | `assertion`, `knowledge_type=misconception`, `question=difficulty` |
| | Link from distractor to misconception; question and option | `Selector.locator` ("Q#4417 option C") |
| | Prevalence / selection rate | Locator text on a `learner_response` source, plus a `Measurement` over the item used as E-MISC's weight |
| | Topic | `Scope.task` |
| | Release date | `Source.published` |
| A2 DataShop / LFA | Discovered KC split | A `difficulty` claim on a `log` source (World A, novice), `tacitness=automated` |
| | Step → KC row | A `domain` claim, `layer=L3`, `knowledge_type=prerequisite` |
| | AFM fit (RMSE, AIC, BIC) | A `Measurement` whose criterion is the claims it scores |
| A3 AAAS | Choice → misconception | A `domain` claim at layer L4, expert voice |
| | National distribution | A separate `difficulty` claim on a `learner_response` source |
| A4 FCI | Distractor → category | A `domain` claim at layer L4 on the Hestenes 1992 study |

The taxonomy is a `domain` claim, and the same text posed as `difficulty` is refused, because expert voice cannot answer §2's "what is difficult" (tested).

**Clinical.** All items are literature-supported: a published CTA list is a synthesis in published work (§6).

| Shape | Attribute | Lives in |
|---|---|---|
| B1 Sullivan | Step text | `assertion` |
| | Step type: clinical knowledge / action / decision | `concept` / `procedure_step` / `decision` |
| | Order | `Selector.locator` ("action step 12"); no NOW metric uses order |
| | Unprompted vs probed coverage | Aggregate comparator (44%, 66%) as a literature claim or `Measurement`. See the per-step limitation below |
| B2 NICU | Cue | `cue`, `tacitness=perceptual` |
| | Category | Locator text; no NOW metric uses it |
| | "Absent from the 1993 literature" | Recomputable as coverage in a ledger restricted `as_of(1993-09-01)`; the published flag itself is locator text |
| B3 Chao & Salvendy | Diagnostic action | `check` |
| | Interpretation | **`interpretation`** (addition 1) |
| B4 CDM/ACTA row | Element's cues / strategies / common errors | `cue` / `strategy` / `failure_mode`, one claim each, grouped by an `Area` (the decision point) |
| | "Why difficult" | Expert voice, so it is excluded from `difficulty` and labelled unknown. It cannot enter gold (tested). This is §2 working, not a gap |
| B5 PARI | Precursor / action / result / interpretation | `rationale` / `check` / assertion text / **`interpretation`** |
| B6 chick-sexing | Discriminating cue | `cue`, `tacitness=perceptual`; the contrasting cases are the evidence locator |

**OSS and organisational.** All items are organisational-artefact-supported, World B, scoped to the project.

| Shape | Attribute | Lives in |
|---|---|---|
| C1 E-OSS unit | Code unit at *t* | `Area` (scope carries the organisation) |
| | Artefacts dated ≤ *t* | `Ledger.as_of(t)` |
| | Pre/post rationale-seeking issues and defect-fix commits | One dated claim each (`rationale`, `failure_mode`) assigned to the unit. Counts and difference-in-differences come from `Source.published` against *t* (tested) |
| | Blind double coding | Two `Evidence` entries on the same span, one per coder. They count once for corroboration (tested) |
| | Developer pseudonym, truck factor, departure date, covariates | Concentration is `AreaFeatures.concentration` (a `LabelledValue`); departure date and covariates belong to the N3 pre-registration |
| C2 Rationale datasets | Decision and its rationale | A `decision` claim and `rationale` claims in one `Area` |
| C3 Documentation issue | An outdated README | Two claims (documentation, imagined; release commit, done) plus a `Contradiction` whose method names the taxonomy type (tested) |
| C4 E-DVP norm | Norm | `norm`, `tacitness=collective`, supported by four review threads (corroboration 4). Absence from the docs at *t* is coverage in `as_of(t)` |
| C5 Residual question | — | Not gold. It is N6's output (target claim, type, channel, probe); see "Deferred" |
| C6 TVA/IAEA position risk | — | Person-level; no NOW experiment uses it. §21 keeps person-attributed concentration out of the default; area-level concentration is a `LabelledValue` |

**Experiment-level attributes** (the inventory's last table):

| Attribute | Lives in |
|---|---|
| Area partition | `Area`, frozen with the N3 pre-registration |
| Held-out gold | A separate `purpose="gold"` ledger |
| Matcher and blinding | `Match` (a match that is not blind is refused) |
| Origin-free IDs | Content-hash `claim_id` |
| Corpus freeze date | `as_of` |
| Memorisation-probe result per item | A `Measurement` over the gold item |
| Gap-map score before elicitation | `GapMapPrediction` |
| Floor score, δ, fallback golds | `Threshold` |
| Weights | `recall(weights=...)` |

Model cutoffs and the corpus-frequency stratum belong in the N3 pre-registration (§24 step 4), not in the claim schema.

## Deferred (not counted, and not quietly absorbed)

- **Learner-response data as tables** (Q-matrix, per-step logs, option distributions) for fitting E-KC and E-DIST. The *items* are expressed. The criterion is a dataset, which §10 schedules as layer L3 after L2 and L6 ("then L3 over public data"). N4 will need an L3 data representation. If it adds claim-schema fields, they count against this gate's threshold.
- **Residual questions and channels** (C5, §10.3, §14.4): N6.

## Limitations

- **The items are illustrative.** Real items are checked on acquisition, and any field they force counts against the same threshold, with a re-freeze before that gold's pre-registration.
- **Sullivan per-step coverage.** If the paper publishes per-step, per-expert coverage (unknown, inventory B1), using it as capture-recapture occasions would need a capture-history record: one more field type, bringing the total to 2.
- **The gate is a build check (R13).** It shows that the schema can express the three domains without domain-specific code. It says nothing about whether the gap map predicts anything; that is N3.
- **Designer contamination.** `vocab.py` and `provenance.py` were drafted before the inventory was read. `claims.py` and later modules were written after it, from a design fixed in `docs/plans/n0-n1-plan.md` (the plan's semantics section predates the inventory). A reviewer should treat the one-addition result with that in mind.
