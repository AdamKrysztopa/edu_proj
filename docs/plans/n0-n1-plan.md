# N0 + N1 implementation plan

Scope: `REORIENTATION.md` §22 N0 and N1 only. N2 is not started.

## Registered before the claim model was written (owner, 2026-09-28)

- **"A handful"** (§22 threshold table): **≤ 2 new field types** across the three domains together. A *field type* is a new field, a new model, or a new member of a closed vocabulary. Every model forbids extra keys and there is no free-text attributes catch-all, so nothing can dodge the count.
- **Outcomes.** 0 new field types: **continue**. 1–2: **continue**, with each addition documented. More than 2: **change**; work stops and N1 is reported as needing redesign (§22 N1 has no stop condition; "stop" here means stop implementing).
- **Freeze.** The schema and the gap-map feature set are hash-frozen at N1. The area partition is frozen with the N3 pre-registration, still before gold, because it needs a scope decomposition (§11 step 1). Recorded in the §22 threshold table.
- **Validation material.** The repository holds no item-level gold, and §14.3 forbids acquiring it before the freeze. The check therefore runs on `docs/n1-gold-shapes.md`, a schema-blind inventory of what each gold item carries in its source's own terms. A separate agent wrote it before `claims.py` existed; `vocab.py` and `provenance.py` had been drafted and were not shown to it. When real items are acquired, they are re-checked. Any field they force counts against the same threshold and needs a re-freeze, with its diff, before that gold's pre-registration.
- **Limitation (R13).** The fixtures are self-authored from that inventory, so this gate checks expressiveness, not an experiment result. REORIENTATION defines N1's gate this way.

## N0

1. DOI hook proven to fire (`scripts/hook_tests/test_check_dois.py`, plus a live Write). **Done** (`d4fbc60`); it found and fixed the regression that skipped `doi.org` links.
2. Domain-neutral package `residual/`: a uv project separate from `instrument/`, whose only dependency is `pydantic`. Its PostToolUse test hook is `run-residual-tests.sh`. Nothing is copied from Track A beyond the vocabulary N1 needs.

## N1 model (`residual/src/residual/`)

| Module | Holds |
|---|---|
| `vocab.py` | Six labels, worlds A/B/C, six questions, layers L1–L5, knowledge type (content) and tacitness (why unsaid) as separate axes, source kinds with practice (imagined / done / reported) and voice (expert / novice / mixed / machine) |
| `provenance.py` | PROV-O-aligned `Agent`, `Source`, `Selector` (W3C TextQuoteSelector: exact + locator), `Verification`, `Evidence`, `Generation` (§12 labelling fields), `Derivation`, `Search` |
| `claims.py` | `Scope`, `ClaimRecord`; the label is computed from evidence, never asserted |
| `ledger.py` | Purpose-typed ledgers (reconstruction / gold / surrogate), contradictions, areas, integrity, derivation taint, `as_of(t)`, `within(worlds)`, deterministic JSON |
| `gates.py` | `Measurement` (criterion labels kept apart from predictor labels), `Threshold`, `GateDecision`, `@evidential_gate` |
| `residual.py` | `Match`, `ResidualAccount`, `ObservedResidual`, `EstimatedResidual`, `GapMapPrediction` as separate types; area `coverage()` |
| `gapmap.py` | Frozen feature definitions and the `AreaFeatures` record; no computation, no predictor (N2+) |
| `freeze.py` | Schema and feature-set hash, checked by a test against `residual/frozen/n1.json` |

### Semantics enforced in code

- **Label**, first match wins:
  1. Verified support from a World C record, or from a raw human record in World A (public learner responses, published observations, transcripts): **observed human evidence**.
  2. Verified support from a World B artefact of the organisation the claim is scoped to: **organisational-artefact-supported**.
  3. Verified support from other World A material, including published CTA task lists, which are syntheses in published work (§6): **literature-supported**.
  4. A derivation: **inferred**. The ledger downgrades it to synthetic or unknown if any premise is.
  5. Model-generated, or supported only by machine-voiced sources: **synthetic extrapolation**.
  6. Sought and not found (a failed evidence attempt or a search record): **unknown**.

  A claim with no evidence, derivation, generation or search is invalid.
- **Verified** means a `supports` verdict from a human, or from a model whose family differs from the generating model's (§11 step 4). The generating model's own say-so never counts. A verifier's false-accept rate is measured on decoys by the N2 verifier, not stored here.
- **Six questions.** *Difficulty* counts only learner data: learner responses, error logs, or studies reporting them, all novice-voiced. *Learner state* counts only World C novice responses. Evidence excluded this way is listed with its reason, never dropped silently.
- **Gates.** A decorated gate accepts only `Measurement`, criterion `ClaimRecord`, `Threshold` and containers of them. A bare number is refused. Synthetic criterion input raises `SyntheticRefused`, and unknown or inferred criterion input raises `GateRefusal`. Predictor labels may be synthetic (§6, §14.2), which is what lets N3's gate read a gap map built on synthetic predictors. A gate must return a `GateDecision`.
- **Separation.** A gold ledger holds only criterion-labelled claims. A surrogate ledger holds only simulation output. A reconstruction ledger holds none (§12, R6).
- **R12.** An area holding automated, perceptual, somatic or collective knowledge is never "covered" without done-practice support.
- **Residuals.** Observed residual, estimated residual and gap-map prediction are separate types. The observed residual refuses to compute without validity judgements; NOW gets recall of H and an unvalidated R∖H count (§14.1).

### Not in N1

- Feature computation and any predictor.
- The verifier, retrieval, contradiction detection and LLM calls (all N2).
- A per-claim licence field; a public/private flag (contamination handling is N3).
- The four §10.2 objects beyond what a fixture forces; a conformal layer.

## Close

Fresh-agent reviews (type design; REORIENTATION conformance; Track A untouched), an ADR, `PROGRESS.md` and `CLAUDE.md`, and `docs/plans/n2-reconstruction-plan.md`.
