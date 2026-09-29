# Evidence audit: what N0–N3 built and demonstrated

Reconstructed from artefacts (code, tests run live on 2026-09-29, committed JSON and reports),
cross-checked against `PROGRESS.md` where it summarises the same facts. Track A (`instrument/`)
covered briefly at the end. All test counts below were produced by running the suites during this
audit, not copied from a prior report.

## 1. Timeline

| Item | Purpose | What it produced | Registered verdict | Key commits |
|---|---|---|---|---|
| **N0** | Reset after the 2026-09-28 reorientation: fix the DOI hook, freeze Track A, create the domain-neutral `residual/` package | `scripts/hook_tests/test_check_dois.py` proven to fire; `residual/` scaffold with its own test hook | **Done, gate passed** (2026-09-28) | `d4fbc60`, `d89a0c4` |
| **N1** | Pre-register and build the evidence model: `ClaimRecord`, six epistemic labels, gap-map field types, a freeze | `residual/src/residual/{claims,vocab,ledger,provenance,gates,gapmap,freeze,residual}.py`; `residual/frozen/n1.json` | **Done, gate: continue with 2 additions** (`KnowledgeType.INTERPRETATION`, `ResponseDistribution`), at the registered ≤2 limit | `b7c0e5d`, `accb506`, `3c544c1`, `03c1e44` |
| **N2** | Build a gated reconstruction pipeline (`reconstruct/`) and test it live (E-LIVE) and against planted falsehoods / private questions (E-PLANT, E-ABST) | One-way pipeline (plan→search→fetch→extract→locate→verify→contradict→assemble); E-LIVE runs on PLC + GDPR; E-PLANT/E-ABST harnesses and baselines | **Engineering PoC: COMPLETE. Full research validation: DEFERRED.** E-PLANT/E-ABST registered gate reads **INCONCLUSIVE** (Continue closed by the validity floor); gated arms never scored (API budget) | `aaef38e`, `7566744`, `600ba2e` (E-LIVE v1), `080b109`/`0f39ed9` (fixes), `319d9a5` (closeout), `ea5c18e`, `10048b0` |
| **N3** | Build a methodology-guided gap map over N2's ledgers (`gapmap/`) that turns silences into candidate hidden-knowledge hypotheses and expert questions | Seven lenses (DISC, DIAG/RESULT, SEL, HEDGE, GUARD, WHY) over PLC and two independent GDPR reconstructions; ranked maps; built-in adversarial checks (anti-renaming, closure null, fair mismatched-evidence control, cross-run stability) | **PoC: pipeline COMPLETE, hidden-knowledge prediction NOT demonstrated.** Closure step is `closure-uninformative` on every lens tested; adversarial-judged precision 3/19 strict (8/19 lenient). **Gate not run** — gold (E-CTA/E-OSS) not acquired | `95325c3` (plan), `ec45c31` (PoC), `754e2e6` (decision 0008) |

## 2. Claim / evidence table

Test suites were run live for this audit (2026-09-29): `residual` 268 passed (0.73s), `reconstruct`
416 passed (1.14s), `gapmap` 172 passed (117.5s), `instrument` 311 passed (7.34s).

| ID | Claim | Evidence | Repository artefact | Strength | Limitation |
|---|---|---|---|---|---|
| E01 | A typed claim record (`ClaimRecord`) exists as the atomic evidence unit | `class ClaimRecord(Record)` defined | `residual/src/residual/claims.py:49` | STRONG | Structure only; says nothing about content quality |
| E02 | Exactly six epistemic labels form a closed, computed (not asserted) vocabulary | `EpistemicLabel(StrEnum)` with `OBSERVED_HUMAN_EVIDENCE, LITERATURE_SUPPORTED, ORGANISATIONAL_ARTEFACT_SUPPORTED, INFERRED, SYNTHETIC_EXTRAPOLATION, UNKNOWN` | `residual/src/residual/vocab.py` (class `EpistemicLabel`) | STRONG | Label semantics still depend on the verifier being honest; no human calibration of the labels exists |
| E03 | Only 3 of 6 labels may ever be a gate's criterion | `CRITERION_LABELS = frozenset({OBSERVED_HUMAN_EVIDENCE, LITERATURE_SUPPORTED, ORGANISATIONAL_ARTEFACT_SUPPORTED})` | `residual/src/residual/vocab.py` | STRONG | Enforced by `evidential_gate`; not proof no gate anywhere reads a bare value bypassing it |
| E04 | Labels are computed from evidence, never set by hand | `Ledger.label()` derives label from verdicts; decision rule "label-computed-from-verified-evidence" | `residual/src/residual/ledger.py:134`; `docs/architecture/decisions/0006-residual-accounting-core.md` | STRONG | Test-enforced (`test_a_criterion_label_needs_support_verified_by_a_human_or_another_family_any_verifier`), not a live-run audit of every path |
| E05 | Gates refuse synthetic/unknown/inferred criteria; a `Measurement` separates criterion from predictor labels | `evidential_gate` decorator; `SyntheticRefused`, `GateRefusal`; `measure()` | `residual/src/residual/gates.py:21,29,45,127` | STRONG | Decision 0006 admits Python "cannot stop deliberate forgery... guards against accidents, not adversaries" |
| E06 | Provenance types (`Selector`, `Evidence`, `Verification`, `Source`, `Generation`, `Search`) exist and are distinct from claims | `class Selector(Record)`, `class Evidence(Record)`, `class Verification(Record)` etc. | `residual/src/residual/provenance.py:52,86,98,106,122,138,162` | STRONG | Type existence, not proof every reconstructed claim actually has one (see E15) |
| E07 | The N1 schema, feature set and label-deciding code are hash-frozen | `schema_sha256`, `features_sha256`, `semantics_sha256`, `frozen_by: "N1"` | `residual/frozen/n1.json` | STRONG | A freeze test (`test_the_schema_matches_its_freeze`) checks the hash matches current code, not that the frozen design is correct |
| E08 | The Ledger enforces structural integrity (acyclic derivations, purpose-consistent evidence) | `_check_acyclic`, `_check_purpose` methods | `residual/src/residual/ledger.py:92,109` | MODERATE | Structural checks only; does not check factual correctness of claims |
| E09 | UNKNOWN is written only for a slot that was searched, fetched and fully examined by another model family | Decision text + `test_e2e_slots.py`; 14/35 GDPR (area×probe) slots UNKNOWN in E-LIVE v1 | `docs/architecture/decisions/0007-reconstruction-pipeline.md`; `research/n2/e_live_report.md` §4.4 | STRONG | "Plausibly real signal" per the report's own hedge — not independently verified against a ground truth |
| E10 | `residual/` depends only on pydantic; no network/LLM/instrument code can live there | Decision rule `residual-core-provider-neutral`; test `test_modules_import_only_stdlib_pydantic_and_residual` | `docs/architecture/decisions/0006-residual-accounting-core.md` | STRONG | Enforced by an architecture test, verified live in this audit's own `pytest-archon` collection (268 passed includes it) |
| E11 | `residual` package: 268 offline tests pass | Ran `uv run --directory residual pytest -q` during this audit | `residual/` (test run 2026-09-29) | STRONG | Offline only; no live model call is exercised by this package |
| E12 | `reconstruct` package: 416 offline tests pass, no test calls a live model or search | Ran `uv run --directory reconstruct pytest -q` during this audit; matches N2 closeout's own count | `reconstruct/` (test run 2026-09-29); `research/n2/closeout.md` "What was built" | STRONG | Matching an independently-run count to the committed report is a good cross-check, but offline tests cannot validate live behaviour |
| E13 | `gapmap` package: 172 offline tests pass (fake judge, no network) | Ran `uv run --directory gapmap pytest -q` during this audit (117.5s) | `gapmap/` (test run 2026-09-29) | STRONG | Confirms the pipeline runs deterministically offline; says nothing about judgement quality |
| E14 | `instrument` (Track A, frozen): 311 offline tests pass | Ran `uv run --directory instrument pytest -q` during this audit (7.34s); matches `CLAUDE.md`'s stated count | `instrument/` (test run 2026-09-29) | STRONG | Track A itself is frozen pending experts/course/ethics; no data has been collected |
| E15 | E-LIVE v1 PLC: 370 claims extracted → 337 located → 321 verified-supports | Per-run table | `research/n2/e_live_report.md` §3 "PLC (v1)" | STRONG | Live run on real web; 11/35 fetched "sources" were later found to be error pages (defect, fixed after this run) |
| E16 | E-LIVE v1 GDPR: 259 claims extracted → 204 located → 195 verified-supports | Per-run table | `research/n2/e_live_report.md` §3 "GDPR (v1)" | STRONG | 80% of GDPR supports trace to UK-specific sources (ico.org.uk / UK statute) despite the task framing as "EU" |
| E17 | PLC v1 sources: 35 fetched, 12 fetch failures, 11/35 were error pages (bot walls, 403/429) | HTTP status breakdown | `research/n2/e_live_report.md` §3 "PLC (v1)" | MODERATE | Reported as a defect, not evidence of reconstruction quality; fixed in `080b109` but not re-verified live (budget exhausted) |
| E18 | GDPR v1 independence over-merged: 4 clusters, largest holding 55% of sources | Cross-domain contrast table | `research/n2/e_live_report.md` §3 | MODERATE | Explicitly attributed to a since-fixed bug (whole-document ≥25-word verbatim rule); the fix itself was never re-checked live |
| E19 | Corroboration was structurally dead in v1: 0 merges on 370 and 259 extractions | Cross-domain contrast table | `research/n2/e_live_report.md` §3, §7 finding 3 | STRONG (as a negative finding) | This is a defect finding, not a capability; the report is honest about it |
| E20 | Decoy false-accept rate: PLC 35% (20 decoys), GDPR 15% (20 decoys) | Per-run table | `research/n2/e_live_report.md` §3 | MODERATE | Small n (20); no CI given in the per-run table itself |
| E21 | E-LIVE v1 run cost: PLC $0.679, GDPR $0.500 | Per-run table | `research/n2/e_live_report.md` §3 | STRONG | Verified in the primary report table |
| E22 | 11 real defects were found live and fixed (error-page sources, PDF rejection, dead corroboration, independence over-merge, verifier scope drift, false contradiction, coverage rule, fetch caching, report mislabelling, silently-vanishing provider errors, PDF Unicode crash) | Numbered findings-and-fixes table with commit hashes | `research/n2/e_live_report.md` §7 (commits `080b109`, `0f39ed9`) | STRONG | Fixes were never re-verified with a live v3 run (blocked by budget, see E30) |
| E23 | v2 GDPR run left 140 of 366 claims "pending" behind a `complete: true` flag (a defect, since fixed) | v2 run detail | `research/n2/e_live_report.md` §7 row 10 | STRONG (as a negative finding) | Fix (`0f39ed9`) is offline-tested only; not confirmed live |
| E24 | v2 PLC run crashed entirely (0 claims) on a `UnicodeEncodeError` from a PDF surrogate | Run status table | `research/n2/e_live_report.md` §2, §7 row 11 | STRONG (as a negative finding) | — |
| E25 | Closeout manual sample re-sliced 71 of 71 evidence spans exactly against stored snapshots | §6.2 manual inspection | `research/n2/e_live_report.md` §6.2; `research/n2/e_live_claim_inspection.md` | STRONG | Inspector was an AI agent (Claude Sonnet 5), not a human, no gold, no inter-rater reliability — stated explicitly in the artefact |
| E26 | GDPR v2(b) supports sample: error rate 12.0% (3/25), Wilson CI 4.2–30.0% | Per-run summary table | `research/n2/e_live_claim_inspection.md` "Per-run summary" | MODERATE | n=25, one AI inspector, no human check |
| E27 | E-LIVE v3 (post-fix live check) never ran: blocked at first model call by OpenRouter's $5/week key limit, $0 remaining | Literal error log + narrative | `research/n2/e_live_report.md` §6 | STRONG | This is the budget/API-limit event; it is the reason N2's gated arms and v3 stayed unexecuted |
| E28 | E-PLANT ungated baseline: pooled a_U = 5/24 (21%, Wilson 95% CI 9–40%), below the registered validity floor ⌈24/3⌉ = 8 | Recomputed table with `load_targets`/`score_baseline_arm`/`validity_floor_met` | `research/n2/e_plant_eabst_report.md` §1.1 | STRONG | This single number closes N2's Continue gate; it is a floor failure, not a reconstruction-quality result |
| E29 | E-PLANT gated arm (run 1) stays sealed and unscored; run 2 never executed | Status table | `research/n2/e_plant_eabst_report.md` §0, §1.2 | STRONG (absence of evidence) | Owner chose not to spend further API budget; not a null result on gating |
| E30 | E-ABST raw baseline: 5/24 private items answered, 19 abstained, cost $0.007 | §2.1, §3 cost table | `research/n2/e_plant_eabst_report.md` §2.1, §3 | STRONG | The ≥20pp/≥20-item margin needed for Continue is "reachable only in a narrow arithmetic corner" per the report itself |
| E31 | E-ABST pipeline arm (run 1) is descriptive only; run 2, owner/second coding and unsealing never happened | §2.2 | `research/n2/e_plant_eabst_report.md` §2.2 | STRONG (absence of evidence) | No gated-arm abstention result exists at all |
| E32 | N2 total measured spend: E-PLANT $0.074+$0.121+$1.758, E-ABST $0.007+$0.488 (all within registered caps) | Costs table | `research/n2/e_plant_eabst_report.md` §3 | STRONG | Confirms the budget story is real and bounded, not a rationalisation |
| E33 | N3 final maps hold 9 (PLC), 1 (GDPR v1) and 6 (GDPR v2) ranked candidates | `map` array length in each JSON, matches `PROGRESS.md`'s stated counts | `research/n3/plc/gapmap.json`, `research/n3/gdpr_v1/gapmap.json`, `research/n3/gdpr_v2/gapmap.json` (`len(d['map'])`) | STRONG | Verified directly by parsing the JSON in this audit, not copied from the summary |
| E34 | GDPR v2 (140 pending verdicts inherited from the E-LIVE v2 defect) is explicitly marked not N3-admissible | Admissibility note | `PROGRESS.md` line 30; `research/n3/gdpr_v2/gapmap.json` field `admissible`/`admissibility_note` | STRONG | GDPR v2's map still exists and is used for cross-run-stability checks, just not as a standalone finding |
| E35 | Retrieval-gap counts (RG-UNK, ledger U-claims with nothing found): PLC 5, GDPR v1 14, GDPR v2 15 | RG-UNK tables; matches E-LIVE's own U-claim counts | `research/n3/plc/gapmap.md` "Retrieval gaps"; `research/n2/e_live_report.md` §3 labels rows | STRONG | Consistent across two independently-produced artefacts (E-LIVE report and gap map) |
| E36 | Closure-control (S2, fair mismatched-evidence): own rate ≈ control rate for every lens in every domain (PLC 0.89/0.89, GDPR v1 0.96/0.96, GDPR v2 0.96/0.96), all flagged `closure-uninformative` | S2 tables per domain | `research/n3/plc/gapmap.md`, `research/n3/gdpr_v1/gapmap.md`, `research/n3/gdpr_v2/gapmap.md` §7 checks | STRONG | This is the core negative finding: the judge closes candidates whether or not the evidence is on-topic, i.e. absence-detection does not beat a fair control |
| E37 | Precision by adversarial (Opus) judgement on the pre-final maps: 3/19 strict, 8/19 lenient | Stated verdict | `research/n3/README.md` "Status" paragraph | MODERATE | Judged by a single AI reviewer against the author's own reading, in-sample, no independent human coder; "pre-final maps," so not byte-identical to the committed `gapmap.json` files |
| E38 | Anti-renaming check (is the map just ranking density?): PLC J10(D_high)=0.58, ρ=0.91; GDPR v1 J10(D_high)=0.10, ρ=0.09; GDPR v2 J10(D_high)=0.33, ρ=0.16 — all `closure-uninformative` | §7.1 tables per domain | `research/n3/plc/gapmap.md`, `research/n3/gdpr_v1/gapmap.md`, `research/n3/gdpr_v2/gapmap.md` §7.1 | STRONG | PLC's high Spearman ρ=0.91 between score and evidence density is a real warning sign the map partly tracks "how much is written," not absence, even though it stays under the 0.5-positive/−0.5-negative disguise thresholds as defined |
| E39 | Judge-vs-lexical agreement is weak/mixed (e.g. PLC: 23/56 "closed→partial", GDPR v1 has states moving in both directions) | Confusion-count tables | `research/n3/plc/gapmap.md`, `research/n3/gdpr_v1/gapmap.md` §7 checks | MODERATE | Shows the semantic judge frequently overrules the cheap lexical heuristic, not which one is "right" — no gold exists |
| E40 | Cross-run stability (GDPR v1 vs v2, independent reconstructions): most open candidates in one run have no counterpart in the sibling run | Per-run "this ledger → sibling" tables | `research/n3/gdpr_v1/gapmap.md`, `research/n3/gdpr_v2/gapmap.md` §7.2 | MODERATE | Current numbers are per-record lists, not an aggregate like the design doc's pre-review prototype figures (16/25 and 14/21 no-counterpart); the direction (mostly unstable) is consistent between prototype and current artefacts |
| E41 | The closure judge is `qwen2.5:7b-instruct` via local Ollama, replayed by default from a committed cache; a live judge call requires `--judge ollama` | Field `judge_model`; `judge_prompt_sha256`; decision rule `gapmap-replays-by-default` | `research/n3/plc/gapmap.json` (`inferred_gap.judge_model`); `docs/architecture/decisions/0008-gapmap-methodology-gap-candidates.md` | STRONG | Confirms reproducibility of the committed maps without a live model; does not bear on judgement quality |
| E42 | `gapmap` package imports only stdlib, pydantic and `residual`; no SDK | Decision rule `gapmap-imports-only-stdlib-pydantic-residual`; test `test_modules_import_only_stdlib_pydantic_and_residual_and_gapmap` | `docs/architecture/decisions/0008-gapmap-methodology-gap-candidates.md` | STRONG | Architecture-test enforced; part of why 172 tests run in ~2 min with zero network |
| E43 | N1 gate: exactly 2 new field types were needed (`KnowledgeType.INTERPRETATION`, `ResponseDistribution`), within the registered ≤2 threshold | Gate record | `PROGRESS.md` N1 row; `residual/frozen/n1.json` | STRONG | Confirms the pre-registered threshold was met, not exceeded, before any gold was seen |

## 3. Claims the report must NOT make

- "The system identifies tacit/hidden expert knowledge." No human has been asked; every N3 output
  is labelled `inferred`, a hypothesis, and RQ-B (does the map predict where the residual lies) is
  untested — no gold, no E-CTA/E-OSS run. (`research/n3/README.md`, `PROGRESS.md` N3 row.)
- "The gap map's ranking reflects real epistemic gaps rather than how much is written about a
  topic." The anti-renaming check does not clear this for PLC (Spearman ρ = 0.91 between score and
  evidence density) even though it falls short of the design's own "disguise" flag threshold (E38).
- "The closure judge distinguishes real absence from off-topic evidence." The S2 fair-control check
  shows own-evidence and control-evidence close candidates at statistically indistinguishable rates
  for every lens tested; every domain is flagged `closure-uninformative` (E36).
- "N2's reconstruction pipeline was shown to resist planted falsehoods or answer abstention
  correctly under gating." The gated arms were never scored; only the *ungated* baselines ran
  (E28–E31). Any claim about gating's effect is unsupported.
- "The pipeline generalises across domains." Only two live domains, one run each (plus a second
  independent GDPR run), all in English, all public web text (`research/n2/closeout.md`, "Not
  demonstrated").
- "N2 is validated" or "N2 passed." The registered gate reading is INCONCLUSIVE, not PASS; the
  engineering-complete/research-deferred split is the owner's own framing, not a weakened re-read
  of the registered result (`research/n2/closeout.md`).
- "The 3/19 (or 8/19) precision figure is a validated accuracy rate." It is one AI reviewer's
  in-sample judgement against pre-final maps, with no human coder and no independent gold
  (`research/n3/README.md`).
- Any number from `docs/plans/n3-poc-lens-spec.md` §8 or §9 presented as current. That section is
  explicitly the pre-review throwaway prototype's numbers, "not what the current `gapmap/` code
  produces" — the spec says so itself.

## 4. Three candidate end-to-end traces for a worked-example figure

**Trace 1 — PLC, `g-59164a9db5bd`, lens DIAG (rival causes), category HYP, closure_state `open`.**
Best trace: real URLs, verbatim spans, an open (undemonstrated) hypothesis, and a concrete
question — nothing here is smoothed over.
- Source URLs (verbatim from `observed_evidence[].source_identifier`):
  `https://www.automate.org/motion-control/industry-insights/troubleshooting-tips-isolating-intermittent-faults`
  and `https://www.ecsintl.com/troubleshooting-intermittent-plc-faults-a-guide-to-ending-nuisance-shutdowns/`.
- Verbatim evidence spans: "Next are unwanted interactions, be they ground loops or interactions of
  multiple processors finding weaknesses in the hardware or software interfaces." and "Loose
  terminals and oxidized connections are silent killers of signal integrity. They create 'jitter'
  that a PLC processor might interpret as a false state."
- Claim/label: `c-0ae2bfae93f15f20`, `literature_supported`, verdict `supports`.
- Lens: DIAG. Missing element: "a discriminating sign for" five rival causes (ground loops,
  aliasing, installation vs. software, VFD/contactor noise, pull-up/clock timing).
- Hypothesis (verbatim, label `inferred`): "practitioners are predicted to tell these rival causes
  of 'Loose terminal connections are a common cause of intermittent PLC faults and' apart by signs;
  the closure judge found a sign for [none of the five]."
- Generated question (channel): "CDM probes on a recalled case, then contrasting cases."
- Artefact: `research/n3/plc/gapmap.json`, `map[0]` (also `research/n3/plc/gapmap.md` "#1 [DIAG]").
- Weakness: the pre-review prototype (`docs/plans/n3-poc-lens-spec.md` §9) illustrates a *different*
  record at the same anchor text — a DISC (boundary-of-"loose") construct — which is **not** in the
  current final map at all. If this figure is used, say explicitly that the DISC framing of
  "loose terminal" was superseded/dropped between the prototype and the reviewed pipeline; it can
  still be shown only from the spec's §9 worked-examples section, marked there as "not re-verified
  against the current `gapmap/` code's output."

**Trace 2 — GDPR v2, `g-656818235091`, lens DISC ("relevant controller"), category HYP, closure_state `partial`.**
- Source URLs: `https://www.edpb.europa.eu/system/files_en?file=decisions%2Fie_dpc_data-protection-impact-assessment.pdf`,
  `https://cnil.fr/sites/default/files/atoms/files/20171013_wp248_rev01_enpdf_4.pdf`,
  `https://www.legislation.gov.uk/eur/2016/679/article/35`.
- Verbatim span: "Article 35 of the General Data Protection Regulation ('GDPR') prescribes that a
  Data Protection Impact Assessment ('DPIA') shall be conducted by a controller where a type of
  data processing, in particular..." (claim `c-1ec0b9ccfcb3bbe3`, `literature_supported`, `supports`).
  Second span: "If the processing is wholly or partly performed by a data processor, the processor
  should assist the controller in carrying out the DPIA..." (`c-23491770ff1621c6`).
- Missing element: "a boundary for 'relevant controller'."
- Hypothesis: "practitioners are predicted to discriminate 'relevant controller' from its
  neighbours by features that no verified claim in this ledger matched."
- Question channel: "contrasting-case classification, or expert-rated written vignettes."
- Artefact: `research/n3/gdpr_v2/gapmap.json`, `map[0]`.
- Weakness: closure_state is `partial`, not `open` — the judge found some but not all of a
  boundary statement, which is the weaker, more ambiguous outcome of the three states, and this
  gap comes from a regulator-authored PDF, not from expert practice, which is a good example of
  "authoritative legal text still leaves a boundary case unstated" but a less clean illustration of
  tacit *practitioner* knowledge than Trace 1.

**Trace 3 — GDPR v1, `g-1b1e68dc5d39`, lens RESULT ("measures, new technologies, and novel processing types"), category HYP, closure_state `partial`.**
- Source URLs: `https://www.dataprotection.ie/en/organisations/know-your-obligations/data-protection-impact-assessments/prior-consultation`,
  `https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/data-protection-impact-assessments-dpias/how-do-we-do-a-dpia/`,
  `https://cnpd.public.lu/en/professionnels/obligations/AIPD.html`.
- Verbatim span: "The nature of the processing is what you plan to do with the personal data. This
  should include, for example: how you collect the data; how you store the data; how you use the
  data; who has access to..." (claim `c-6370fb5b7eeb5c13`).
- Missing element: "a result-to-interpretation mapping for 'measures, new technologies, and novel
  processing types.'"
- Hypothesis: "practitioners are predicted to read the result... against expected values and map it
  to the next action; no verified claim in this ledger matched test."
- Question channel: "CDM probes on a recalled case; process tracing."
- Artefact: `research/n3/gdpr_v1/gapmap.json`, `map[0]` — this is GDPR v1's **only** admissible
  candidate in the whole final map (n=1), which is itself worth stating if this trace is used: the
  domain's yield was extremely thin.
- Weakness: sourced from three national-regulator sites (Ireland, UK, Luxembourg) whose relation to
  each other is exactly the kind of cross-jurisdiction merging the E-LIVE review flagged as an
  independence risk; treat the "three independent sources" framing cautiously.

**Recommendation if only one trace is used:** Trace 1 (PLC DIAG, `g-59164a9db5bd`). It has the
richest verbatim evidence, an `open` (not merely `partial`) closure state, and a clean statement of
what a human expert would be asked — while Trace 1's own DISC-prototype confusion (above) is the
kind of provenance subtlety this audit exists to catch, so flag it in the caption if used.

## 5. Failures, negative and inconclusive results

- N2's registered gate: **INCONCLUSIVE**, Continue closed by the E-PLANT validity floor
  (a_U=5/24 < 8). `research/n2/e_plant_eabst_report.md` §0, §1.1.
- E-ABST's gated arm never ran; no abstention result exists under gating.
  `research/n2/e_plant_eabst_report.md` §2.2.
- E-LIVE v3 (the post-fix live check) never ran — blocked by the OpenRouter $5/week key limit, $0
  remaining. `research/n2/e_live_report.md` §6.
- N2's corroboration mechanism was measured structurally dead in v1 (0 merges on 370 and 259
  extractions) before the fix. `research/n2/e_live_report.md` §3, §7.
- N2's independence clustering over-merged GDPR sources into 4 clusters (55% in the largest) before
  the fix. `research/n2/e_live_report.md` §3.
- N3's closure step does not beat a fair control on any lens in any domain — every lens/domain
  combination is flagged `closure-uninformative`. `research/n3/{plc,gdpr_v1,gdpr_v2}/gapmap.md` §7.
- N3's cross-run stability (GDPR v1 vs v2) is low: most open candidates in one run have no
  counterpart in the independent sibling run. `research/n3/gdpr_v1/gapmap.md`,
  `research/n3/gdpr_v2/gapmap.md` §7.2; prototype figures in `docs/plans/n3-poc-lens-spec.md` §7.2.
- GDPR v2's reconstruction is not N3-admissible on its own (140 pending verdicts inherited from an
  E-LIVE v2 defect); it is used only for the cross-run check. `PROGRESS.md` line 30.
- N3's own adversarial (Opus) review found precision of 3/19 strict (8/19 lenient) on the pre-final
  maps — roughly half or worse, in-sample, unvalidated against gold. `research/n3/README.md`.
- N3's PLC anti-renaming check shows a high correlation (Spearman ρ=0.91) between candidate score
  and evidence density — a warning that ranking partly tracks "how much is written," even though it
  does not cross the design's own disguise-flag threshold. `research/n3/plc/gapmap.md` §7.1.

## Verification notes

- All four test counts (residual 268, reconstruct 416, gapmap 172, instrument 311) were produced by
  running the suites directly during this audit on 2026-09-29, not copied from `PROGRESS.md` or
  `CLAUDE.md` (though they match both).
- `map` array lengths for the three gap maps (9, 1, 6) were verified by parsing the committed JSON
  directly (`json.load(...)['map']`), matching `PROGRESS.md`'s stated "Final maps" line.
- Where `docs/plans/n3-poc-lens-spec.md` and the committed `research/n3/*/gapmap.md` disagree
  (§7.2 cross-run-stability numbers, §8/§9 lens-output and worked-example numbers), the spec itself
  labels its own figures "pre-review prototype" / "not what the current code produces" — this audit
  used the current `gapmap.md`/`gapmap.json` figures as authoritative and flagged the prototype
  numbers as historical only (see Trace 1's weakness note and row E37/E40).
