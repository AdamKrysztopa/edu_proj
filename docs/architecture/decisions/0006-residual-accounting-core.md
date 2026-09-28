---
id: 0006
status: active
skill: decide-architecture
date: 2026-09-28
commit: 3c544c1
rules:
  - id: synthetic-never-a-gate-criterion
    statement: A function decorated with residual.gates.evidential_gate refuses any criterion input labelled synthetic extrapolation (SyntheticRefused), unknown or inferred (GateRefusal), any bare value, and any Measurement not built by measure(); synthetic labels are allowed only as a Measurement's predictor labels.
    scope: ["residual/src/residual/**"]
    severity: blocking
    verification: deterministic
    verified_by: pytest-archon#test_synthetic_claims_are_refused_wherever_they_sit
  - id: label-computed-from-verified-evidence
    statement: A claim's epistemic label is computed from its evidence, never set; a criterion label needs a supports verdict from a human, or from a model of another family than the claim's generating model, on a source that is not machine-voiced.
    scope: ["residual/src/residual/**"]
    severity: blocking
    verification: deterministic
    verified_by: pytest-archon#test_a_criterion_label_needs_support_verified_by_a_human_or_another_family_any_verifier
  - id: residual-core-provider-neutral
    statement: The residual package depends at runtime only on pydantic and imports nothing outside the standard library, pydantic and itself; no LLM client, retrieval, graph or vector store, web framework or instrument code.
    scope: ["residual/**"]
    severity: blocking
    verification: deterministic
    verified_by: pytest-archon#test_modules_import_only_stdlib_pydantic_and_residual
  - id: n1-schema-frozen
    statement: The schema, the gap-map feature set and the label-deciding code match residual/frozen/n1.json; a change needs a re-freeze commit that says what changed and, once any gold is acquired, precedes that gold's pre-registration.
    scope: ["residual/src/residual/**", "residual/frozen/**"]
    severity: blocking
    verification: deterministic
    verified_by: pytest-archon#test_the_schema_matches_its_freeze
  - id: track-a-reused-by-copy
    statement: New-track code never imports from or edits instrument/; a Track A component is reused by copying and generalising it into residual/.
    scope: ["residual/**", "instrument/**"]
    severity: blocking
    verification: narrative
---
# Residual accounting core: labels are computed, gates refuse synthetic input

## Context

`REORIENTATION.md` makes residual accounting the first build (§1, §10, §22 N1) and requires that synthetic material never reach a gate (§6, §12, R6), "enforced in code". Decisions 0001–0005 are Track A's validity constitution and stay scoped to it. Decision 0001 rejects simulated sessions outright. The new tracks instead admit labelled synthetic material and never let it count as evidence (§5).

## Decision

- **Package boundary.** A separate uv project, `residual/`, whose only dependency is pydantic. Nothing under `instrument/` changes. Track A components are copied into it when a NOW item needs them (§4), not imported.
- **Labels are derived, not stored.** `ClaimRecord.label` is a property over the evidence. Only verified support moves a claim out of *synthetic* or *unknown*. The generating model's family cannot verify its own output, and a software check cannot judge support. The six questions have consequences: evidence that cannot answer a question (§2) is excluded, and the exclusion is reported with its reason.
- **Gates are a decorator over typed inputs.** A gate reads `Measurement`, `ClaimRecord`, `Ledger` and `Threshold` only. A `Measurement` keeps criterion labels apart from predictor labels. That lets N3's gate read the ΔAUROC of a gap map built on synthetic predictors (§14.2), while a synthetic criterion, including a surrogate's prevalence used as a weight, is refused.
- **Separation by purpose.** Gold, reconstruction and surrogate material live in different ledgers.
- **Freeze by data flow.** The freeze hashes the schema structure, the feature set and the source of the modules that decide labels, admission and coverage (L1.9, §14.3).

## Consequences (cost)

- A claim cannot be marked "supported" by hand. Tests and fixtures must build evidence with verifications, which is more verbose.
- A `Measurement` loaded from JSON is unsealed, so a gate refuses it: measurements are recomputed, not loaded.
- Any edit to a semantic module fails the freeze test until it is re-frozen, which is deliberate friction. N2 code goes in new modules.
- A `Measurement` certifies the labels of the claims it was scored against, not the arithmetic behind its value. A surrogate number passed to `measure()` over a gold claim is caught by review and the N2 run log, not by the type. `Threshold.registered_in` is free text.
- Python cannot stop deliberate forgery (setting `_sealed`, faking an agent family). The rules guard against accidents and pipeline bugs, not adversaries. A verifier's false-accept rate is measured on decoys in N2 (§11).
