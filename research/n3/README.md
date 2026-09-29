# N3 proof of concept: methodology-guided gap map

**Status (2026-09-29): PoC pipeline complete; hidden-knowledge prediction not demonstrated.** The pipeline runs end to end on real N2 ledgers in two domains, and it produces inspectable three-tier records and expert questions. An Opus adversarial review found two problems:
- Its absence-detection step (deciding that a missing element really is unsaid) does not beat a fair control.
- By adversarial judgement, precision on the pre-final maps was 3 of 19 strict (8 of 19 lenient).

So the records are **candidates**, not validated hypotheses. This is not the N3 gate: `docs/plans/n3-gap-map-plan.md`, the gold-based validation, is future research.

- Design: `docs/plans/n3-poc-lens-spec.md`, whose post-review sections list every change.
- Code: `gapmap/`.
- Maps: `plc/`, `gdpr_v1/`, `gdpr_v2/`, each holding `gapmap.md`, `gapmap.json` and `closure_judgements.json`.

## Pipeline

```
Domain
 → N2 live reconstruction                 reconstruct/runs/<run>/ledger.json
 → explicit knowledge                     verified claims (literature_supported), verbatim spans
 → methodology lenses (7)                 gapmap/src/gapmap/lenses.py      fire on a construct whose content is missing
 → closure judge                          gapmap/src/gapmap/semantic.py    local qwen2.5:7b via Ollama, cached, replayable
 → three-tier gap records                 gapmap/src/gapmap/record.py      observed evidence / inferred gap / hypothesis (inferred)
 → ranked gap map + questions             gapmap/src/gapmap/{rank,render}.py → research/n3/<domain>/gapmap.md
 → checks                                 gapmap/src/gapmap/checks.py      anti-renaming, closure controls, cross-run stability
```

Retrieval gaps have their own section and are never hypotheses: RG-UNK (searched, nothing found), RG-SINGLE (one independent source), RG-UNVER (answered only by unverified text), RG-SIBLING (answered in the other GDPR run) and RG-UNDECIDED (judge answer unreadable). Their action is *search, verify or re-judge*, never *ask an expert*.

## Demo domains

The two domains differ in kind:
- **PLC intermittent-fault diagnosis** (run `20260928T133336Z-59ec876b3d7e`) is diagnostic craft: rival causes, perceptual cues, and test results to interpret.
- **GDPR DPIA** is normative-interpretive judgement: undefined statutory terms, and hedged rules with unstated exceptions. It has two independent reconstructions:
  - v1 is `20260928T135354Z-eb840a85b7d1`;
  - v2 is `20260928T145943Z-bc1cc9a30a02`. It is not N3-admissible because 140 of its verdicts are pending, and its map says so.

A third domain would have needed a paid N2 run, and the OpenRouter budget is $0.

## Lenses (the methodology layer)

Each lens names a construct from the project's methods research. It fires when sources attest that construct but not its content.

| Lens | Construct (source) | Missing element | Predicted type | Human channel |
|---|---|---|---|---|
| DISC | Cue as discrimination (CDM; `REORIENTATION.md` §10.2) | boundary of a judgement term | cue, perceptual/collective | contrasting cases |
| DIAG | Rival causes (PARI interpretation, ECD rival KSAs) | a sign that tells causes apart | interpretation, cue | CDM on a recalled case |
| SEL | Selection rule (GOMS, HTA plan, KC condition) | situation → option mapping | decision | CDM options and basis |
| HEDGE | Conditional knowledge (CBM, KLI "when not") | the exception condition | decision | boundary vignettes |
| GUARD | Automated self-check (`tacit_knowledge_foundations.md` §7) | how the error is noticed | check, automated | observation first |
| WHY | Rationale (Szulanski causal ambiguity) | the reason | rationale | confirmation question |
| RESULT | PARI result → interpretation ("A→B→C, but what decides B vs D") | what a result means and where it leads | interpretation, expectancy | CDM; process tracing |

DtD, PCK and misconception research shape the bottleneck framing and the limits. The ledgers hold only expert-voiced text, so no lens claims a learner difficulty (`explore-pedagogical-content-knowledge.md`).

## Is a gap just "few sources"?

No. The check measures this directly:
- **Which** candidates become gaps is decided by lens firing plus closure, not by density. A candidate with one independent source becomes RG-SINGLE, not a hypothesis.
- **Order** among open candidates is deliberately by *breadth*: how many independent sources discuss the attested side without stating the missing element. That is the opposite of low density.
- On the pre-final maps, the top 10 shared 0.00–0.07 (Jaccard) with the ten lowest-density candidates.

The real weakness is different: whether a missing element is truly unsaid is not decided reliably.

| Closure step | Result against a fair control |
|---|---|
| Lexical (stem co-occurrence), v1 of the PoC | At chance. Donor-claim null with self and same-source excluded in both arms: PLC 42 vs [33, 47], GDPR v1 13 vs [10, 19], GDPR v2 11 vs [5, 12]. 13 of 15 sampled closures were wrong |
| Semantic judge (local Qwen 7B), final | No better than the control. The seed's own sentences sit in both arms, and the other sources are swapped for the nearest other candidate's. Own rate = control rate on every lens and ledger: PLC 0.89 = 0.89, GDPR v1 0.96 = 0.96, GDPR v2 0.96 = 0.96. The judge's closures come from the seed's own text, not from independent evidence |

Both results are rendered in each map's §7, with the `closure-uninformative` flag raised.

## Results (final maps)

| | PLC | GDPR v1 | GDPR v2 |
|---|---|---|---|
| Gap candidates (HYP) | 9 (DIAG 2, RESULT 3, WHY 3, GUARD 1) | 1 (RESULT) | 6 (DISC 1, RESULT 3, HEDGE 1, WHY 1) |
| RG-SINGLE / RG-UNVER / RG-SIBLING / RG-UNK | 11 / 0 / – / 10 | 12 / 4 / 2 / 28 | 3 / 6 / 7 / 44 |
| Replay | byte-identical, offline | byte-identical | byte-identical |

**Cross-run stability** between the two GDPR runs is low. Each run is dominated by one or two independence keys and retrieved different documents, so most candidates have no counterpart in the other run. The sibling check still does useful work: it reroutes 2 of v1's candidates and 7 of v2's to RG-SIBLING.

**Good examples:**
- **GDPR v2 #3, HEDGE.** WP248 says a DPIA is needed "in most cases" when two criteria are met, and "in some cases" when only one is. No source says *which* cases. The candidate is partial, not open: the judge found a partial exception statement in a same-source claim. Question: "Describe a case where this did not hold, or where you decided against it. What about that case told you it was an exception?"
- **PLC #9, GUARD.** "A common mistake … is panicking and abandoning systematic approaches". No source says how a troubleshooter notices the drift. The prediction is metacognition and automated, so the channel is observation.
- **PLC `loose terminal`, DISC.** This was the best record in both review rounds: three keys, and the span "push-in spring terminals … release their grip on a ferrule without looking damaged" implies a tactile discrimination. It dropped out of the final map after the judge-parsing fix, once the judge read a partial boundary. How easily a good candidate falls out is itself the finding.

**Typical failures:**
- the element is already stated in the seed's own span;
- statutory text treated as practice;
- promotional sources, now excluded by a domain denylist;
- DIAG records whose cause phrases and question are sentence fragments. For example, "Think of the last time you diagnosed Loose terminal connections are a common cause of…" is a known readability defect left in place.

## Limitations

- **The closure step is not informative against a fair control.** The lexical version runs at chance, and the semantic judge's closures come from the seed's own text. Every candidate should be read as "the lens fired here", not "experts know something here".
- **Precision is low and in-sample.** It was 3 of 19 strict by adversarial judgement on the pre-final maps, and the final maps were not re-tallied. It is not measured against gold.
- **Everything the lenses read is extractor-output or in-sample:**
  - knowledge types are assigned by the extractor and gate DIAG and GUARD;
  - linking and retrieval are lexical;
  - lexicons, the promotional denylist and the DISC stop-anchors were all tuned in-sample on these three ledgers.

  `config_sha256` must be frozen before any gold is acquired.
- **Independence keys are coarse** (3 in GDPR v1), which caps breadth. The result is that GDPR v1 yields only 1 candidate.
- **All sources are expert-voiced World A text.** There is no work-as-done, no learner data and no difficulty claims.
- **Two domains only.**
- **The judge is a 7B local model.** A stronger judge might pass the control; that is untested.

## What remains for scientific validation (future research / grant roadmap)

- **An informative closure step.** A stronger or ensemble judge, checked against the fair control and a small human-labelled closure set (blind second coder), before any gold.
- **E-CTA and E-OSS against held-out gold.** ΔAUROC against the strongest §14.3 baseline under the pre-registered N3 rule. Requires:
  - the config hash-frozen first;
  - dated corpora and memorisation probes;
  - a matcher meeting κ ≥ 0.70 (`docs/plans/n3-gap-map-plan.md`).
- **Later items:**
  - N5 human knowledge residual measurement;
  - N6 EIG question selection against gold oracles;
  - N4 learner data for any bottleneck or misconception claim;
  - real expert interviews with a blind arm (LATER).
- **N2's deferred validation:** E-PLANT, E-ABST and E-LIVE v3 (`research/n2/closeout.md`).

## Reproduce

```
cd gapmap
uv run python -m gapmap --ledger ../reconstruct/runs/<run>/ledger.json \
  [--sibling ../reconstruct/runs/<other>/ledger.json] [--sidecar ../reconstruct/runs/<run>/sidecar.json] \
  --domain <name> --out ../research/n3/<name>          # replay from the committed judge cache, no network
# add --judge ollama to re-judge live (needs a local Ollama with qwen2.5:7b-instruct)
uv run pytest -q
```
