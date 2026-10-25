# DS6: Independent verifier and decoy validity; a reachable robustness contrast

**Branch:** `ds6-verifier-validity`
**Output:** `research/ds6-verifier-validity.md`
**Method:** the `research` skill. Sources: claim verification, attribution evaluation and adversarial or planted-source robustness (ClashEval [51], WikiContradict [52], AbstentionBench [53]).

## Context
- `docs/plans/deep-search-queue.md` § DS6.
- `research/n2/e_plant_eabst_report.md`: the run-1 baselines, the floor, and why Continue is closed.
- `research/n2/final_adversarial_review.md` and `research/n2/e_live_claim_inspection.md`: scope drift, about 1 in 10 context-only qualifiers.
- `reconstruct/src/reconstruct/evidence.py:593-598` (`decoy_is_valid`).
- `docs/n2-eplant-eabst-protocol.md` (the registered protocol: do not change it).
- `research/gate_sim/RESULT.md`, if I5 has run.

## Questions
1. How do published pipelines establish that a decoy is false and topically matched, independently of the generator? Look at rubrics, human-validation rates and sampling plans.
2. How is verifier validity measured on natural claims, and how is the natural false-support rate sampled? Find a natural-error taxonomy that covers scope drift, dropped hedges, antecedents outside the span and dropped jurisdiction.
3. ClashEval found over 60% adoption, but N2's ungated model adopted only 5 of 24 planted sources. Which planting designs actually persuade an ungated model, so that a gating effect becomes measurable? This is the reachable best case (L7.3).

## Done when
- The note gives:
  - a decoy-validity rubric;
  - a verifier-validity sampling plan with its sample size;
  - the error taxonomy;
  - a proposed **new** robustness contrast, with thresholds I5 can check for reachability.
- It states that the old registration and its INCONCLUSIVE reading stay unchanged.
- `citation-verifier` has passed on it.

## Decision it feeds
Whether to register a new N2-type robustness experiment. That is an owner decision. The deferred reruns are funded only if I5 shows a reachable reading.
