# I6: area features, uncapped candidates and an area score

**Result (2026-10-24): the score trips the pre-stated threshold, so change the predictor before MS2.** On PLC, the candidate score has Spearman ρ = 0.96 with `k_topic` (the independent-source count) across all 24 merged HYP candidates. The check discriminates there:
- a planted score equal to `k_topic` gives ρ = 1;
- random scores reach |ρ| ≥ 0.8 in 0 of 2,000 draws.

GDPR v1, the other admissible ledger, has one HYP, so the check cannot run on it.

**The dead features stay dead.** Six of the 20 frozen features are constant in every ledger: `n_boundary_sources`, `tacitness`, `has_done_support`, `imagined_only`, `n_inferred` and `latest_source`. Two more, `instability` and `concentration`, are missing everywhere. The E-CTA pre-registration should therefore state that it tests size + density + type plus the lens signal only.

**Caps.** The display caps hide 15 of PLC's 24 candidates and none in GDPR v1 (1) or GDPR v2 (6).

Cost $0: replay only, no network. Reproduce with `sh research/area_score/run.sh`; a second replay is byte-identical. The rules in §1 were committed in `ef5131e`, before any association was computed.

## 1. Pre-stated rules (committed before any association was computed)

These rules were written and committed before any association between the score and a covariate was computed on a committed ledger. Two things were already known when they were set:
- `docs/plans/coverage-audit.md` finding 19 reports ρ ≈ 0.83 within the 9 displayed PLC HYPs and ≈ 0.87 within the 6 GDPR v2 HYPs.
- The unpaired lists of PLC's 24 uncapped `k_topic` values and scores were printed while the replay was checked against the committed maps.

The threshold is the item prompt's proposal, adopted unchanged.

**Score.** A candidate's weight is `(s + 3) / 7`, where `s` is its rubric score `A + B − P − Q` in [−2, 4]. The weight is strictly monotone in `s`, so its ranks are those of `s`. An area's score is the noisy-OR of its candidates' weights, with the max as the alternative. Neither is a probability or calibrated.

**Threshold.** The score is "close to a monotone function of source count or size" when Spearman |ρ| ≥ 0.8. Either sign counts: "both directions" is read as the score rising with the covariate, or falling with it.

**Population.** The population is the merged HYP candidates before the display caps, one ledger at a time. RG records are never pooled in.

**Covariates (candidate level).** There are four:
- `k_topic`;
- the candidate's own density `|X|` (`checks.dens`);
- its area's `n_claims` (size);
- its area's `evidence_density`.

**Discrimination (L7.3).** A covariate's check counts only if it can discriminate on that ledger:
- a planted score equal to the covariate trips it;
- uniform random scores trip it in at most 5% of 2,000 draws (seed 0).

A constant covariate gives an undefined ρ, and an undefined ρ never counts as a pass.

**Decision.** The score trips if, on any N3-admissible ledger (PLC, GDPR v1), any covariate whose check discriminates reaches |ρ| ≥ 0.8. Tripping means "change the predictor before MS2". GDPR v2 is reported but does not decide, because 140 of its verdicts are pending. Area-level associations (5 planner areas per ledger) are descriptive only.

**Feature status (by code).**
- **Dead:** at most one distinct value, or none, within every ledger.
- **Confounded (size):** pooled |ρ| with `n_claims` ≥ 0.8 across all areas of the three ledgers.
- **Live:** the rest. `n_claims` is the size baseline itself.

Tuples are counted by length for variance and ρ, and by value for ties.

## 2. Candidates hidden by the display caps

The caps are `MAP_TOP_N` 12, `MAP_PER_LENS` 3 and `MAP_PER_AREA` 4. They are set in `gapmap/src/gapmap/config.py` and applied in `rank.py`. Each `candidates.json` lists every merged HYP in map order, with `shown` marking the ones `gapmap.md` displays. The replay rebuilds each committed `research/n3/<domain>/gapmap.json` map and retrieval-gap list gap-id for gap-id; `gapmap/tests/test_area.py` asserts this for PLC.

| Ledger | Merged HYP | Shown | Hidden | Hidden by lens |
|---|---|---|---|---|
| PLC | 24 | 9 | 15 | RESULT 10, WHY 5 |
| GDPR v1 | 1 | 1 | 0 | – |
| GDPR v2 | 6 | 6 | 0 | – |

The caps hide mostly the low-breadth candidates. PLC's hidden `k_topic` values are 2 ×5, 3 ×9 and 5; the shown ones are 2, 3, 3, 6, 6, 7, 7, 9 and 11. That truncation is why ρ with `k_topic` within the 9 shown is 0.79, below the 0.96 of the full 24.

**Correction to §1, left unedited so it stays verbatim with `ef5131e`.** Finding 19's ≈ 0.83 (PLC) and ≈ 0.87 (GDPR v2) are Spearman of the score with density `|X|`, the `anti_renaming` statistic. They are not with `k_topic`. Over the same 9 shown PLC HYPs, score with `|X|` is 0.83 and score with `k_topic` is 0.79.

## 3. Association of the score with source count, size and density (merged HYP only)

`associations.json` holds every check with its n, the number of distinct covariate values, the planted ρ and the random trip rate. "Discr." means the check can discriminate (L7.3): the planted score trips it, and random scores trip it in at most 5% of draws.

| Ledger (n HYP) | Covariate | ρ | Trips | Random trip rate | Discr. |
|---|---|---|---|---|---|
| **PLC (24)** | `k_topic` | **0.96** | **yes** | 0.000 | yes |
| | own density `\|X\|` | 0.79 | no | 0.000 | yes |
| | area `n_claims` | 0.05 | no | 0.000 | yes |
| | area `evidence_density` | 0.05 | no | 0.000 | yes |
| GDPR v1 (1) | all four | undefined | no | – | no (n = 1) |
| GDPR v2 (6), not admissible | `k_topic` | 1.00 | yes | 0.133 | no (2 distinct values) |
| | own density `\|X\|` | 0.87 | yes | 0.068 | no |
| | area `n_claims` | −0.32 | no | 0.046 | yes |
| | area `evidence_density` | −0.53 | no | 0.051 | no |

Decision rule (§1): PLC trips on `k_topic`, so the score **trips**.

**Why it trips.** This is by construction: `record.confidence_rubric` sets A, the dominant term, as a step function of `k_topic`. The trip is not a property of the PLC data. It will recur on any ledger, so the remedy is a weight that does not read source count, not a different threshold.

**Size and density do not drive it.** At candidate level the score is unrelated to its area's size or density (ρ = 0.05 on PLC). The two area covariates have identical ranks over PLC's four candidate-bearing areas.

**Area level (descriptive only).** With 5 planner areas per ledger, random scores reach |ρ| ≥ 0.8 in 9–14% of draws, so no area-level check discriminates. The largest area-level value is GDPR v2's noisy-OR against `n_claims`, at 0.80.

## 4. Area scores

| Ledger | Area | Candidates | Noisy-OR | Max |
|---|---|---|---|---|
| PLC | PLC Fault Diagnosis Methods | 6 | 0.999 | 0.857 |
| | Systematic Troubleshooting Frameworks | 7 | 0.997 | 0.714 |
| | Data Logging and Monitoring | 6 | 0.995 | 0.714 |
| | Electrical and Hardware Testing | 5 | 0.991 | 0.714 |
| | Documentation and Historical Analysis | 0 | 0 | 0 |
| GDPR v1 | Mandatory content and documentation requirements | 1 | 0.429 | 0.429 |
| | the other four areas | 0 | 0 | 0 |
| GDPR v2 | GDPR Mandatory Data Protection Impact Assessment Requirements | 2 | 0.755 | 0.571 |
| | High Risk Processing Activities Under GDPR | 2 | 0.673 | 0.429 |
| | Required Contents and Elements of a DPIA | 1 | 0.571 | 0.571 |
| | Exemptions and Exceptions to DPIA Requirements | 1 | 0.429 | 0.429 |
| | EDPB Guidelines and Regulatory Interpretation | 0 | 0 | 0 |

**The noisy-OR saturates.** A HYP has `k_topic` ≥ 2, so its weight is at least 2/7; the lowest observed is 3/7. PLC's areas hold five to seven candidates each, which puts every candidate-bearing area at 0.991–0.999. The noisy-OR then separates "has candidates" from "has none" and little else. The max ties three of PLC's four candidate-bearing areas at 0.714. Neither aggregate is usable as an area-level predictor as it stands.

## 5. Feature table (planner partition, 15 areas, three ledgers)

Status is assigned by code (`gapmap.area.feature_table`), using the rule in §1.
- **Missing:** areas with no value.
- **Distinct:** distinct values pooled across ledgers.
- **Modal:** the share of areas holding the commonest value.
- **ρ(size):** pooled Spearman with `n_claims`.

| Feature | Status | Missing | Variance | Distinct | Modal | ρ(size) | Distinct per ledger (PLC / v1 / v2) |
|---|---|---|---|---|---|---|---|
| `n_claims` | live (size) | 0 | 2,100 | 13 | 0.13 | 1.00 | 5 / 5 / 5 |
| `evidence_density` | live | 0 | 732 | 14 | 0.13 | 0.76 | 5 / 5 / 5 |
| `n_single_source_claims` | live | 0 | 722 | 14 | 0.13 | 0.77 | 5 / 5 / 4 |
| `n_synthetic` | live | 0 | 1,100 | 14 | 0.13 | 0.54 | 5 / 5 / 5 |
| `knowledge_types` | live | 0 | 3.85 | 14 | 0.13 | 0.53 | 5 / 5 / 4 |
| `n_independent_sources` | live | 0 | 23 | 9 | 0.20 | 0.32 | 4 / 3 / 3 |
| `n_unknown` | live | 0 | 1.4 | 5 | 0.33 | −0.57 | 3 / 3 / 3 |
| `rationale_present` | live | 0 | 0.24 | 2 | 0.60 | 0.32 | 2 / 2 / 2 |
| `n_undated_sources` | live | 0 | 5.82 | 7 | 0.27 | 0.08 | 4 / 4 / 4 |
| `source_kinds` | live | 0 | 0.77 | 3 | 0.67 | 0.18 | 1 / 1 / 2 |
| `earliest_source` | live | 6 | 1.6e6 d² | 5 | 0.40 | −0.24 | 3 / 0 / 2 |
| `n_contradictions` | live | 0 | 0.25 | 2 | 0.93 | 0.22 | 1 / 2 / 1 |
| `latest_source` | dead | 6 | 1.1e6 d² | 2 | 0.40 | −0.09 | 1 / 0 / 1 |
| `n_boundary_sources` | dead | 0 | 0 | 1 | 1.00 | – | 1 / 1 / 1 |
| `tacitness` | dead | 0 | 0 | 1 | 1.00 | – | 1 / 1 / 1 |
| `has_done_support` | dead | 0 | 0 | 1 | 1.00 | – | 1 / 1 / 1 |
| `imagined_only` | dead | 0 | 0 | 1 | 1.00 | – | 1 / 1 / 1 |
| `n_inferred` | dead | 0 | 0 | 1 | 1.00 | – | 1 / 1 / 1 |
| `instability` | dead | 15 | – | 0 | 1.00 | – | 0 / 0 / 0 |
| `concentration` | dead | 15 | – | 0 | 1.00 | – | 0 / 0 / 0 |

Five rows need reading against `docs/plans/n3-gap-map-plan.md`'s table, because the code rule cannot see what makes them weak.

**`n_contradictions`** is live by one area only: GDPR v1's two contradicted claims. They come from the one ledger contradiction in that run, which `research/n2/e_live_review_notes.md` judged a false positive. In substance the feature is dead, as the plan says.

**`n_single_source_claims`** is collinear with `evidence_density` (pooled ρ = 0.998), because corroboration is 1 almost everywhere. Of the two, only one is a feature.

**`imagined_only`** is constant True. Every supporting source in all three runs is documentation, a standard or a procedure document, and all three kinds prescribe work.

**`n_synthetic`** is live but measures pipeline failure (the plan's "confounded"). **`n_independent_sources`** and **`source_kinds`** are live but unproven. The code rule passes all three as live.

**The date features** are dead (`latest_source`), or live only in PLC and GDPR v2 (`earliest_source`), and only after the header-date rule below.

What the table leaves is the plan's live set: size, density and type (`knowledge_types`), plus `n_unknown` and `rationale_present`.

**Header-date rule.** `area_features()` reads the sidecar only to decide whether a date is real. A source whose sidecar entry names no document date field has only an HTTP `Last-Modified` header, and that header is treated as undated. Replayed on the committed artefacts, the rule changes nothing in PLC or GDPR v1. In GDPR v2 it drops 3 supporting sources' dates and changes the date features of all 5 areas. Four areas' `latest_source` moves from 2026-09-14 or 2026-09-28 (the run date) to 2020-12-31, and one area becomes fully undated. No committed artefact read these features before, so no downstream sample shrinks.

## 6. What was built

- `residual/src/residual/features.py`: `area_features(ledger, sidecar, partition)` returns one frozen `AreaFeatures` per partition area, ordered by `area_id`. The prompt wrote `-> AreaFeatures`; a partition has several areas. `planner_partition(ledger)` gives the ledger's own areas. The module adds no field and is outside the frozen semantics hash, and `residual/frozen/n1.json` still matches (`test_freeze`).
- `gapmap/src/gapmap/area.py` provides:
  - `candidate_records`, the records `build_gapmap` ranks;
  - `uncapped`, the merged HYPs with `shown`;
  - `area_scores`, the noisy-OR and max;
  - `association` and `decide`, the pre-stated check with its planted and random controls;
  - `feature_table`;
  - `load_areas`, which reads the `--areas` file. It accepts only `"grain": "task_step"`.

  The constants (threshold, weight range, draws) live in `area.py`, not `config.py`, so `CONFIG_SHA256` and every gap id are unchanged. Nothing calls the output `P(missing)`, and a test asserts it.
- Outputs: `research/area_score/<domain>/{candidates,area_scores,features,associations}.json` and `research/area_score/summary.json`. `run.sh` replays them from the committed ledgers and judge caches, read only.

**Not done.** No task-step partition exists for any committed ledger, so every number here is at planner-area grain. `--areas` is tested on fixtures only. Planner areas are topical search buckets (`research/n2/e_live_review_notes.md`), and 5 areas per ledger cannot power an area-level check (§3).
