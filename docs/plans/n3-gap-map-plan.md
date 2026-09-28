# N3: gap map against held-out gold (plan, not started)

**Status: N3 has NOT started and needs owner approval.** It also presumes the N2 gate reads *continue*, which is not yet recorded. Nothing below is built.

**Gate** (`REORIENTATION.md` §22 N3): **stop H1, pivot to H3** if the upper 90% bound of ΔAUROC is below δ, regardless of recall. **Continue H1** if the lower 90% bound exceeds 0 and the point estimate is ≥ δ. **Otherwise inconclusive**: run the next pre-registered fallback gold once, then apply the same rule. **Change to H2** only from E-OSS, if trace inputs "dominate". Recall against the 44% unprompted-expert comparator [1] only decides whether reconstruction survives as a draft.

## What N3 consumes from N2

Per run, `ledger.json` and `sidecar.json`.
- **Ledger:** claims (`knowledge_type`, `tacitness`, evidence with `Source.kind`/`independence_key`/`published`/`boundary`, verdict), UNKNOWN placeholders, `assignments`, `contradictions` (cross-verify REFUTES only).
- **Sidecar:** `n3_input`; `slots` (`covered` ≥ 2 clusters, `thin`, `unknown`, `unverified`, `unexamined`); `cross_checks`; `sources` (`published_field`, `modified_field`, `tier`, `extract_ok`); `decoy_by_type`; `stats`; `config` hashes.

**N3 must add a mechanical admissibility check.** E-LIVE v2 (b) is marked `complete` and `n3_input: true`, yet 140 located extractions have no verdict, and cross-verify and decoys made 0 calls. A run is N3 input only if every located extraction has a verdict, cross-verify ran, and decoys ran.

## Area partition (§14.2 grain)

N3 supplies `--areas`, frozen and hash-committed in the pre-registration, before any gold is acquired. Areas are at task-step, decision-point, KC, component or SOP-section grain. Planner areas are not acceptable: they are topical search buckets, and five per task gives AUROC no power.

For E-CTA, the partition comes from a dated pre-gold procedural source by a written procedure. Any exposure to the notes' gold structure (46 steps split 14/27/5) is recorded as a deviation, following E-PLANT's blind-areas precedent. For E-OSS, the partition is the code units existing at *t* (git blame at *t*).

Power check (computed, Hanley–McNeil): 20 areas split 10 missed and 10 not missed give a 90% half-width of about ±0.20 on a single AUROC of 0.70. Minimum areas per gold is therefore a real constraint, and pooling across golds may be needed.

## AreaFeatures from a ledger

Write `area_features(ledger, sidecar, partition) -> AreaFeatures` as a pure, deterministic function under `residual/`. The feature set is frozen, so this adds no new field. It does not exist yet (N2 stage 7).

State of the features after the post-review fixes:

| Status | Features |
|---|---|
| Live | `n_claims`, `evidence_density`, `knowledge_types`, `n_unknown`, `rationale_present` |
| Live but confounded | `n_synthetic`: in v2 (b), 305 of 523 claims are synthetic, mostly unlocated (PDF text) or never verified. It measures pipeline failure, not thinness |
| Unproven | `n_independent_sources`, `n_single_source_claims`: cross-verify has produced 0 corroborations live. `source_kinds`: host rules now give three kinds in v2 (b) |
| Unreliable | Date features: in v2 (b), 8 of 17 "dated" sources carry an HTTP `Last-Modified`, four of them the run date itself |
| Dead in World A | `n_boundary_sources` (0 everywhere); `n_contradictions`; `tacitness` (all UNASSESSED); `has_done_support`/`imagined_only` (no World A kind maps to DONE); `n_inferred`; `instability` (needs multi-family reruns); `concentration` (E-OSS only) |

**Implication.** On World A the live features are mostly size and density. Those *are* the "area size" and "retrieval-support density" baselines of §14.3, so ΔAUROC ≈ 0 by construction, and a stop result would be a pipeline artefact. The pre-registration must therefore require that the dead features be revived first, or accept that E-CTA tests only size and density plus type.

## Dated corpus and `as_of` (§18.2)

N2 records `published`, and `Ledger.as_of(t)` exists, but nothing enforces `as_of` at fetch time. Live search is model-mediated Exa and returns today's page versions. Corpus mode is hard-coded `n3_input=false`, because it was built for E-PLANT.

N3 adds:
- a **dated-corpus mode** (N3-eligible) built from OpenAlex `to_publication_date < gold date` and Wayback snapshots at or before *t*, with the snapshot timestamp as the date; undated or `Last-Modified`-only documents are rejected;
- a **gold blocklist** by DOI, title and landing pages. Today's `--blocklist` matches URL substrings only;
- **per-item guided-completion memorisation probes** [151], with probe-positive items excluded from the primary analysis;
- a preference for open-weight models with documented cutoffs.

## Gold order and pre-registration checklist

Order: pre-register and hash-commit; check itemised availability by metadata only; acquire the primary gold, sealed; probe; code; score; open a fallback gold only on *inconclusive*. Leave-one-gold-out throughout; the pipeline is sandboxed from `research_notes/`.

All of the following are **to set (our choice)**:
- δ.
- Primary gold, model and baseline, plus the multiplicity rule (Holm, or pooled random-effects ΔAUROC). Suggested gold: Sullivan [1], which is itemised and has the 44% comparator. Chao & Salvendy [2] is the first fallback. This changes if [1]'s list is not itemised or is mostly probe-positive.
- Minimum gold items and missed areas per gold, and the fallback golds.
- The floor score for unmappable gold items, which count as missed areas.
- The E-OSS departure count and minimum post-departure activity (by power calculation; tens).
- "Dominate" for H2.
- The run-admissibility limits: maximum unverified share and unlocated rate.

The headline compares against the **maximum** of the §14.3 baselines. The type prior needs at least two golds.

## Matcher and coding

- **LLM matcher:** from a family other than the generator (enforced in `ResidualAccount`). A third family, distinct from the verifier, is recommended. It is adopted only if its κ ≥ 0.70 and not below the lower CI bound of the human–human κ.
- **Human double coding:** at least 20% of pairs, and all gold-item → area assignments, are coded by the owner under origin blinding (no origin, model family or P(missing)) and by **one blind second coder**, who needs owner confirmation (§22).
- **Codebook grain** is fixed before matching.
- **Fallback:** the owner codes alone, and the report states this as a limitation.

## E-OSS needs

E-OSS needs a **World B adapter over Git history** only: commits, blame at *t*, issues, PRs and review threads, and ADRs/docs dated ≤ *t*, mapped to `COMMIT`/`ISSUE`/`REVIEW_THREAD`/`DESIGN_RECORD` with author-based independence keys. That revives `has_done_support` and `concentration` (review-weighted [114]).

Outcome: blind double-coded rationale-seeking issues and defect-fix commits after *t*, as a difference-in-differences. Contamination: low-visibility repositories plus probes on post-*t* issue titles. Developers pseudonymised; legitimate-interest basis recorded. **Not Weft yet.**

## Risks carried from N2

- **Verifier scope drift.** The pre-fix natural false-support rate was 4/20 (Wilson 8–42%). The post-fix rate is unmeasured on natural claims. False support inflates coverage and biases the result toward null.
- **Corroboration sparsity.** v1 made 0 merges and v2 (b) made 0 cross-verify calls, so `thin`/`covered` and independence are untested live.
- **PDF and authority bias.** v1 lost all 12 curated PDFs. v2 (a) got 0 sources (6 over the 5 MB cap, 8 × 403). v1 (b) drew 80% of its supports from one regulator.
- **Independence over-merge.** Largest cluster share: 0.55 in v1 (b), 0.60 in v2 (b).
- **Cost and quota.** $0.50–$1.00 per run. Both v3 runs died at planning on the OpenRouter weekly key limit. N3 needs at least 3 reruns per task and multi-family instability runs, so a budget is **to set**.

## First three steps (after approval)

1. **Pre-registration draft.** Fill in the thresholds above, confirm the second coder, freeze the E-CTA partition procedure, run `methods-critic`, and hash-commit. All of this comes before any gold.
2. **`area_features()` plus the admissibility check,** tested on fixtures and then run on the E-LIVE ledgers (not gold) to report which features are live and which are dead.
3. **Dated-corpus mode** with `as_of`, the DOI/title blocklist and an N3-eligible flag, piloted on a non-gold task to measure the dated share and verification completeness. Restore the API quota first.
