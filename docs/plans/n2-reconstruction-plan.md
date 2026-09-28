# N2: gated reconstruction pipeline v0 (plan, not started)

**Gate** (`REORIENTATION.md` §22 N2):
- **Continue** if planted-falsehood adoption is below the ungated model's (baseline over 60% [51]), and the false-answer rate on real-but-private objectives is below the raw model's by the pre-set margin.
- **Change** by adding verifier stages or restricting corpora.
- **Stop** building on it if gating does not beat the ungated model at all.

**First, before any code:** set the E-ABST false-answer margin (threshold table, "to set"). It needs the owner. Also choose the E-ABST private objective (the owner's own code conventions, §18).

## What N1 hands over

The pipeline populates, and never edits, the frozen N1 types in `residual/`:
- `ClaimRecord` with `Evidence`, `Verification`, `Generation`, `Derivation` and `Search`;
- a `Ledger` with `purpose="reconstruction"`, plus `Area` and `Contradiction`;
- `AreaFeatures`, and `measure()` / `@evidential_gate`.

New code goes in new modules, so `residual/frozen/n1.json` still matches. Anything that would change an N1 type is a re-freeze, counted against N1's threshold (≤ 2 field types, 1 used).

## Stages

Each stage is a module under `residual/src/residual/pipeline/`, one Protocol per stage, with fakes for tests. There are no network calls in tests.

| # | Stage | Input → output | Writes into N1 as | Mechanical check (code, not prompt) |
|---|---|---|---|---|
| 1 | Scope | domain/task → areas | `Area` records; each decomposition claim is *inferred* | Hash the decomposition and partition; they are frozen with the N3 pre-registration |
| 2 | Research planner | areas → queries per source family | `Search` records (corpus, query, date, agent) | Every area gets at least one search, so "unknown" is always "sought" |
| 3 | Source acquisition adapters | queries → documents | `Source` (kind, world, voice, `independence_key`, `published`, boundary) | Bibliographic resolution (OpenAlex/DOI). A liveness filter drops hallucinated URLs [37]. Curated full text before the open web [39]. An `as_of` date is enforced at fetch time for dated corpora (§18.2) |
| 4 | Evidence extraction | document → atomic claims with spans | `ClaimRecord` + `Evidence` (`PENDING`) + `Generation(extraction, spec hash)` | Each claim bound to an exact span; parametric-only output is left unverified and so labelled synthetic |
| 5 | Provenance verification | pending evidence → verdicts | `Verification` by a verifier of a different model family | A software exact-match check that the quote occurs in the fetched text runs *before* the model verdict and blocks it if absent. False-accept rate on decoys, reusing Track A's `corroboration.py` pattern by copy (§11) |
| 6 | Contradiction detection | claims → pairs | `Contradiction(detected_by, method)` | Claim clustering plus NLI, separate from the synthesiser [52] |
| 7 | Gap-map feature generation | ledger + areas → per-area features | `AreaFeatures`; instability as a synthetic `LabelledValue` | A deterministic function of the ledger; the feature set is already frozen |
| 8 | Evidence ledger | runs → ledger + run log | `Ledger.to_json()` and a run log (model IDs, dates, prompt hashes, tokens, dollars, tool calls) | Rerun ≥ 3 times; report the stability of claim and area sets (§11 step 7). Feeds N9 |

**Not in N2:** World B ingestion of customer data (§23); the gap-map predictor (N3); question selection (N6); surrogates (N7); any UI.

## Experiments that close N2

- **E-PLANT.** Inject a known-false plausible source (ClashEval-style [51]) and a real conflict (WikiContradict-style [52]) into a small curated corpus. Measure adoption of the planted falsehood and contradiction-flag recall, for the gated pipeline and for the same model ungated. The criterion is the planted truth, a claim in a gold ledger, so the gate reads it through `measure()`.
- **E-ABST.** Real-but-private objectives. Measure the false-answer rate and the share of "insufficient evidence" (unknown-labelled) outputs, against the raw model.

## Order and size

1. Stages 3–5 plus the run log, with fakes.
2. A live smoke run on one small curated domain (the lesson L1.3 needs a live run for anything a model sees).
3. Stages 1, 2 and 6.
4. E-PLANT and E-ABST, then the gate decision.
5. Stage 7, which N3 needs, but not the N2 gate.

Two model families are needed: generator and verifier. Their identifiers and cutoffs are recorded in the run log. Open-weight models with documented cutoffs are preferred (§18.2).

## Known inputs from N1

- `AreaFeatures.concentration` and E-OSS covariates need Git mining. That belongs to N3's E-OSS adapter, not N2.
- N4 needs an L3 representation of learner-response tables (see `docs/n1-schema-validation.md`, "Deferred").
