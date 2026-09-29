# 05 — Architecture of the implemented PoC (as built, from code)

Author: Technical Architecture Author. Source: repository at commit `754e2e6` (HEAD at time of
writing). All numbers below were read from the primary artefact named, not copied from another
document.

## 1. Package map

Four independent uv packages, layered by decision. `instrument/` is frozen Track A and untouched
by NOW. `residual/` -> `reconstruct/` -> `gapmap/` is a strict one-way dependency chain
(0006, 0007, 0008): each package imports only stdlib, pydantic, and the package(s) to its left.

### `residual/` — N0/N1 evidence model (decision 0006)

Purpose: the typed record of a claim, its provenance and its epistemic label; the "residual
accounting" core. Provider-neutral: depends at runtime only on `pydantic` (enforced by
`pytest-archon` test `test_modules_import_only_stdlib_pydantic_and_residual`).

- `residual/src/residual/vocab.py` (192 lines) — closed vocabularies (enums).
- `residual/src/residual/provenance.py` (182 lines) — `Record`, `Agent`, `Source`, `Selector`,
  `Verdict`, `Verification`, `Evidence`, `Generation`, `Search`, `Derivation`.
- `residual/src/residual/claims.py` (216 lines) — `ClaimRecord`, `Scope`, `ResponseDistribution`;
  the `label` property.
- `residual/src/residual/ledger.py` (203 lines) — `Ledger`, `Contradiction`, `Area`.
- `residual/src/residual/gates.py` (141 lines) — `evidential_gate`, `Measurement`, `measure()`,
  `Threshold`, `GateDecision`, `GateRefusal`/`SyntheticRefused`.
- `residual/src/residual/gapmap.py` (56 lines) — `AreaFeatures`/`FEATURE_SET` (N1 feature
  definitions only; N2 computes them, N3 predicts from them).
- `residual/src/residual/freeze.py` (69 lines), `residual.py` (`ResidualAccount`,
  `EstimatedResidual`, `GapMapPrediction`).

Total: 1,281 lines across 8 modules (`wc -l`). Tests: 153 `def test_*` across 9 files
(`residual/tests/`); includes `test_architecture.py` (import-boundary and gate-bypass
pytest-archon checks), `test_freeze.py`, `test_cross_domain.py` (16 gold shapes from maths,
clinical, OSS sources, per `docs/n1-schema-validation.md`). No external model or network
dependency at all.

### `reconstruct/` — N2 reconstruction pipeline (decision 0007)

Purpose: populate N1's `Ledger`/`ClaimRecord` from the open web, with real provenance, for one
`(domain, task)` pair.

- `reconstruct/src/reconstruct/llm.py` — model boundary: one OpenAI-compatible OpenRouter
  backend, `Budget`/`BudgetExceeded`, `CallLog` (`calls.jsonl`), served-model check.
- `reconstruct/src/reconstruct/web.py` — search (OpenRouter web plugin), fetch, HTML→text,
  content-addressed snapshots (`SnapshotStore`).
- `reconstruct/src/reconstruct/evidence.py` (642 lines) — the only module that constructs
  `Evidence`/`Selector`/`Verification`; normalisation, span location, source classification,
  independence clustering, decoys, spec hashing.
- `reconstruct/src/reconstruct/run.py` (937 lines) — one-way orchestration: plan → search → fetch
  → extract → locate → independence → verify → cross-verify → UNKNOWN/slots → decoys → assemble.
- `reconstruct/src/reconstruct/corpus.py`, `eplant.py`, `eabst.py` — E-PLANT/E-ABST
  corpus-replay harnesses for adversarial and ablation testing.
- `reconstruct/src/reconstruct/report.py`, `verify_run.py`.

Total: 4,803 lines across 10 modules. Tests: 342 `def test_*` across 21 files, including 8
`test_e2e_*` files (happy path, verification, corroboration, contradictions, decoys, injection,
slots, resilience, call stats, corpus mode) and `test_architecture.py` enforcing 0007's rules.
Tests never call a live model or the network (fakes only).

**External models** (`reconstruct/models.json`, all via one OpenRouter backend):
- planner, extractor, baseline: `anthropic/claude-haiku-4.5` (family `anthropic`)
- verifier: `openai/gpt-5.4-mini` (family `openai`)

The verifier's family must differ from the extractor's or no claim can move off
*pending*/*synthetic* (0007 `support-needs-other-family-and-quote-in-span`).

### `gapmap/` — N3 methodology-guided gap map, proof of concept (decision 0008, proposed)

Purpose: read one N2 ledger, propose gap *candidates* (never criteria, never a hypothesis fed
back as a claim), rank and render them.

- `lenses.py` (747 lines) — the 7 firing rules.
- `semantic.py` (308 lines) — retrieval + closure judge call.
- `judge.py` (97 lines) — `Judge`/`OllamaJudge`/`CachedJudge`.
- `record.py` (333 lines) — the 3-tier `Record`, categorisation, `EvidenceItem`.
- `rank.py` (109 lines) — merge/cap/order, control slot.
- `checks.py` (429 lines) — anti-renaming, mismatched-evidence control, lexical donor null,
  cross-run stability.
- `link.py`, `text.py`, `config.py` (lexicons, thresholds, `CONFIG_SHA256`), `__main__.py`.

Total: 2,986 lines across 12 modules. Tests: 161 `def test_*` across 17 files, all offline
(fake judge; `test_main.py` covers the CLI's replay-by-default rule). Runtime deps: stdlib +
pydantic + `residual` only — `gapmap` imports no HTTP library; `judge.py` talks to Ollama over
raw `urllib.request`.

**External model**: closure judge is `qwen2.5:7b-instruct`, served by a **local Ollama** instance
(`http://localhost:11434`-style URL in `config.JUDGE_URL`, zero cost). Its family (local, distinct
from anthropic/openai) is a decision-0008 requirement, checked by code review, not a test.

### `instrument/` — Track A instrument (frozen, one paragraph)

`instrument/` is the built Stage A/B apparatus for the physics human-expert study (`probe-app`
session app, `probe-code` coding pipeline): frozen as a unit under REORIENTATION.md, started only
on its own registered preconditions, and never imported by any NOW package (0006, 0007
`reconstruct-never-imports-instrument`). Track A components are reused by copying and trimming
into `residual`/`reconstruct`, never by importing `instrument` code; 311 tests run under
`uv run --directory instrument pytest -q`.

## 2. The evidence model

**Record types** (`residual/src/residual/provenance.py`, `claims.py`, `ledger.py`):
`Record` (frozen pydantic base, revalidating `model_copy`) → `Agent` (human/model/software, family
required only for model), `Source` (identifier, kind, world, voice, `independence_key`,
published, organisation, boundary), `Selector` (exact quote and/or locator), `Verdict`
(supports/refutes/insufficient/unresolvable/pending), `Verification`, `Evidence` (source +
selector + retrieved + verification), `Generation` (agent, activity, spec hash, simulation tier),
`Search`, `Derivation`. `ClaimRecord` (assertion, question, layer, knowledge_type, tacitness,
scope, evidence, generation, derivation, searches, certainty). `Ledger` (purpose:
reconstruction|gold|surrogate; claims; `Contradiction`; `Area`; assignments) with an integrity
validator that rejects duplicate claims, dangling derivations/contradictions/assignments, and
derivation cycles.

**Epistemic labels** (`vocab.EpistemicLabel`, exact enum values): `observed_human_evidence`,
`literature_supported`, `organisational_artefact_supported`, `inferred`,
`synthetic_extrapolation`, `unknown`. `CRITERION_LABELS` = the first three; only those may be a
gate's criterion. `ClaimRecord.label` is a **computed property**, never a stored field: it reads
`self.supporting` (evidence with verdict SUPPORTS whose exclusion reasons — self-verification,
machine-voiced source, software verifier, wrong world for the question — all come back `None`),
then checks source `World` (C→observed, B→organisational, else A→literature), falls to `inferred`
if a `Derivation` exists, else `synthetic_extrapolation` if model-generated, else `unknown`.
`Ledger.label(claim_id)` extends this for derived claims: an inference takes the *weakest* of its
premises' labels (synthetic beats unknown beats inferred).

**Provenance chain**: snapshot hash → selector exact span → claim. Every fetched document is
normalised once (NFKC, quote/dash/bullet unification, whitespace collapse) and hashed
(`sha256:<text>`); `Selector.locator` is `sha256:<hash>;char=<start>,<end>` into that exact
normalised text, and `Selector.exact` is the literal slice — never the model's own quotation. A
quote that cannot be located verbatim in the fetched text produces no `Evidence` at all.

**Invariants enforced by validators**: an assertion is non-empty and whitespace-normalised; a
claim needs evidence, a search, a derivation, or a model generation to exist at all; certainty may
only be set on claims with a criterion label; a World-C source must be a human-record kind; World
B requires (and only World B has) an organisation; a Verification is either fully pending or
fully resolved (verifier+date); Evidence from a quotable source kind needs an exact quote;
`Ledger` forbids duplicate claim ids, dangling references, and derivation cycles; a `gold` ledger
holds only criterion-labelled claims; a `surrogate` ledger holds only simulation output and
nothing else.

**Gates** (`gates.py`): `evidential_gate` is a decorator that walks every argument
(`Measurement`/`ClaimRecord`/`Ledger`/`Threshold`, nested in dict/list/set) and raises
`SyntheticRefused` on any `synthetic_extrapolation` label or `GateRefusal` on anything else not in
`CRITERION_LABELS`, before the wrapped function runs. `Measurement` is built only by `measure()`,
which seals it (`_sealed=True`) and keeps `criterion_labels` apart from `predictor_labels` — a
synthetic value can be a gap-map *predictor* but never a gate criterion.

**"Residual accounting" in code** = computing what fraction of a domain's claims carry each
epistemic label, and specifically how much of the target competence has *no* criterion-labelled
support (the human knowledge residual) — via `Ledger.label`, `AreaFeatures` (per-area counts of
labels, source kinds, tacitness, contradictions), and `ResidualAccount`/`EstimatedResidual` in
`residual.py`. Nothing here yet computes an actual residual number against gold; N1 defines the
types N2/N3 populate.

**Freeze mechanism** (`freeze.py`, decision 0006): `residual/frozen/n1.json` holds three sha256
hashes — `schema_sha256` (JSON schema of `ClaimRecord`, `Ledger`, `Measurement`, etc., stripped of
prose, plus every vocabulary's enum values), `features_sha256` (the `AreaFeatures` field-name
tuple), `semantics_sha256` (byte hash of `vocab.py`, `provenance.py`, `claims.py`, `ledger.py`,
`gates.py`, `residual.py` — the code that *decides* labels/gates/coverage). A `pytest-archon`
test fails if the live fingerprint (`fingerprint()`) diverges from the committed file; re-freezing
needs `python -m residual.freeze --write` plus a commit explaining why.

## 3. The N2 pipeline (`reconstruct/src/reconstruct/run.py`, `evidence.py`)

One-way, no agent loop, one `reconstruct(domain, task, ...)` call, writing `ledger.json`,
`sidecar.json`, `report.md` into a run directory named `<utc>-<confighash>`.

1. **plan** — `models["planner"]` (haiku-4.5) proposes 3–6 areas with 1–3 search queries each
   (one retry on invalid output; only uniqueness-after-casefold is a hard gate).
2. **search** — `web_search()` via the OpenRouter web plugin, per area/query; a query with zero
   hits across all areas is retried once; a fully-failed area is `unsought` (excluded from
   coverage, `incomplete_reasons` grows, `complete=False`).
3. **fetch** — `FetchCache` dedupes by canonical URL; text is normalised and hashed once
   (`SnapshotStore`); truncation fraction is recorded per document (>max_doc_chars).
4. **extract** — one `models["extractor"]` call per fetched document (haiku-4.5), schema-bound
   (`EXTRACT_SCHEMA`); rejects assertions that are questions/unfilled templates or carry an
   unknown `knowledge_type`/`question`.
5. **locate** — `evidence.locate_span`: the extractor's quote (6–80 words) must occur verbatim,
   after normalisation, in the document's own normalised text, or the extraction has no `Evidence`
   at all.
6. **independence** — union-find over fetched documents (`evidence.independence_clusters`):
   union when `domain_grouping_key` matches (registrable domain, except a hand-listed
   `_MULTI_ORG_DOMAINS` set — e.g. europa.eu, mdpi.com, arxiv.org, medium.com — grouped by full
   host, or host+author-path for medium.com) **or** 5-shingle containment ≥ 0.5. A separate,
   span-level rule (`span_duplicates`, ≥25-word verbatim run via `difflib.SequenceMatcher`)
   collapses syndicated *spans* to one corroboration count without merging the documents'
   independence clusters themselves — this is decision 0007's stated departure from an earlier
   whole-document 25-word-run union rule (found to over-merge 11 unrelated documents).
7. **verify** — `models["verifier"]` (gpt-5.4-mini, family `openai`, checked ≠ extractor's
   `anthropic`) judges supports/refutes/insufficient on a ±300-char annotated window; a "supports"
   verdict is downgraded to "insufficient" unless its own `supporting_quote` is a substring of the
   exact span **and** all three drift flags (adds_content, subject_or_scope_differs,
   quantifier_modality_or_connective_differs) are false.
8. **cross-verify** — for claims sharing an area, up to 2 topically-nearest claims from a
   *different* independence cluster (and not already `span_duplicates`-linked) are cross-checked;
   a "refutes" verdict builds a `Contradiction` record (method `"cross-verify:<spec sha>"`).
9. **UNKNOWN placeholders + slot status** — `evidence.slot_status` per (area, probe) pair:
   `covered` (≥2 independent supporting clusters), `thin` (exactly 1 — reported, never folded into
   unknown), `unknown` (searched, fetched, extracted, fully verified, nothing found — the *only*
   condition under which a `ClaimRecord` with no evidence enters the ledger), `unverified`
   (fetched but not fully verified), `unexamined` (nothing fetched).
10. **decoys** — 10 per mutation type (number/negation/scope), round-robin over sorted claim ids;
    `decoy_is_valid` requires an actual textual change plus a rationale; false-accept rate and
    Wilson CIs reported per type (this run: 0 attempted — verifier/decoy path only fires when a
    verifier and clean, non-injection-flagged evidence exist).

**Budget-before-every-call**: `Budget`/`CallLog` in `llm.py` check accumulated cost before
dispatching, never after (0007 `budget-before-every-call`); exceeding it raises
`BudgetExceeded`, caught in `run()` to still write the three output files with `complete=False`.
**Failure accounting**: `failed_calls_by_task` counts plan/verify/cross_verify/decoy failures as
they occur, plus derived extract/web_search failure counts from the sidecar, so
`sidecar.json["stats"]["failed_calls_by_task"]` never hides a silent loss behind `complete: true`.

**A real completed run** (`reconstruct/runs/20260928T145943Z-bc1cc9a30a02/`, domain "EU data
protection law", task "DPIA"): 523 claims, label_counts `{literature_supported: 203,
synthetic_extrapolation: 305, unknown: 15}`; 25 sources fetched, 7 independent clusters,
largest-cluster share 0.6; 351/523 extractions located (unlocated rate 0.33); 226 verified, 207
supports; 0 contradictions; 9 thin slots, 5 unverified slots, 0 unexamined; total cost $1.00
(262 model/search calls in `calls.jsonl`, each logging task, role, model, served_model, tokens,
cost, outcome, UTC timestamp).

## 4. The N3 pipeline (`gapmap/src/gapmap/`)

**Seven lenses** (`lenses.py`), each firing on an assertion's regex/knowledge-type pattern over
the "A" pool (criterion-labelled claims) — never on synthetic or unknown claims:
- **DISC** — a JUDGE-lexicon term ("appropriate", "high-risk", …) attached to ≥2 distinct A
  claims and not on `DISC_STOP_ANCHORS`; fires per anchor term.
- **DIAG** — a claim matching the CAUSE pattern, with ≥2 "rivals" (other cause-effect claims
  sharing ≥2 effect stems, 0 shared non-common cause stems, cause-Jaccard below a cap).
- **SEL** — SEL lexicon + (MODAL or `knowledge_type=decision`).
- **HEDGE** — MODAL or a hedge-firing type, plus a HEDGE-lexicon hit that precedes any RAT hit.
- **GUARD** — an ERR-lexicon hit **and** a GUARD_AGENT (human-actor) hit (0008/S3-fix: type alone
  no longer fires).
- **WHY** — a prescriptive/procedural type, MODAL+CONTRA, no STANDARD-kind evidence, not an
  authority-excluded span.
- **RESULT** — a prescriptive test verb (TEST pattern) followed within 6 tokens by a non-common
  content stem.

Each fired `Candidate` gets a lexical closure state (`lexical_state`, kept only for comparison —
the S1 pre-registered change) and is then judged for real by `semantic.judge_candidate`, which
retrieves up to 8 "A"-pool + 4 "S"(synthetic)-pool sentences scored by stem overlap plus the
seed's own span sentences, and asks the closure judge a fixed per-lens yes/no-style question.

**Closure judge** (`semantic.py`, `judge.py`): local Ollama `qwen2.5:7b-instruct`, temperature 0,
seed 0, JSON-mode. Answers cache to `research/n3/<run>/closure_judgements.json`, keyed by
`sha256(model_id, prompt)`. The CLI replays that cache by default (`CachedJudge`, `live=False`);
a cache miss in replay mode raises `JudgeCacheMiss` naming `--judge ollama` rather than calling
the network (0008 `gapmap-replays-by-default`). A malformed answer or any cited sentence-id
outside the offered set is `undecided` and routed to `RG-UNDECIDED` — never silently `open`
(0008 `undecided-never-a-finding`).

**Three-tier record** (`record.py` `Record`): `observed_evidence` (verbatim `EvidenceItem`s,
each carrying its own epistemic label, verdict, independence key, span, and a
`counts_as_attestation` flag), `inferred_gap` (`InferredGap`: statement, test_id, closure_state,
partial/synthetic hits, judge metadata — re-runnable, never asserting a fact about sources),
`hypothesis` (`Hypothesis`, present only for category HYP, `label: "inferred"` fixed).

**Categories / retrieval-gap taxonomy** (`record.categorize`): `undecided` → `RG-UNDECIDED`;
`synthetic-closed` (closed only by an unverified/S-pool sentence) → `RG-UNVER`; otherwise `HYP` if
≥2 independent topic claims (`k_topic`) else `RG-SINGLE`. Two more categories are built
separately: `RG-UNK` (`record.unk_gaps`, from ledger U claims and sidecar slots marked
unknown/thin/unverified — retrieval, not analysis) and `RG-SIBLING` (`checks.apply_sibling`,
when the same anchor/lens closes in a *sibling* run of the same domain).

**Ranking** (`rank.py`): breadth-first, not confidence-calibrated (no gold to calibrate against).
`confidence_rubric` computes `score = A(k_topic banded) + B(k_step≥2) − P(partial) − Q(promo
penalty)` and a separate `breadth` (broad/moderate/narrow) decided directly from `k_topic`/`k_step`
thresholds, not from `score`. `order_key = (-score, -robustness, -k_topic, -|X_a|, gap_id)`.
Records merge when same lens+category and X-Jaccard ≥ `MERGE_JACCARD`; the map is capped per-lens
and per-area (`MAP_TOP_N`/`MAP_PER_LENS`/`MAP_PER_AREA`); one extra `CONTROL` slot targets the
highest-attested-share area with no HYP record (the "unknown-unknowns" guard).

**Rendering and expert-question generation** (`render.py`, `lenses.py`): questions are
**template-generated in code**, not LLM-generated — each lens builds `question_text` as an
f-string filled with up to 2 verbatim quotes (`_pick_quotes`, from distinct independence keys) and
a fixed interview frame (e.g. DISC: "Think of a recent case where you had to judge whether
something was {anchor}. Describe one case that clearly was, one that clearly was not…"). No model
call produces the expert-facing question text.

**Checks** (`checks.py`, travel with every map): **anti-renaming** — J10 overlap of the map
against density-sorted rankings, Spearman(score, density), a matched-density tercile table, and
closure rate by k_topic band, flagging "density-in-disguise"/"salience-in-disguise". **Closure
informativeness** — the S2 mismatched-evidence control (own-evidence closure rate minus a
topically-matched control's rate; flags `closure-uninformative` unless the gap ≥0.20) and the
lexical donor null (observed lexical-closure count vs. 1,000 random-donor draws per lens,
`random.Random(0)`). **Cross-run stability** — matches open candidates (HYP ∪ RG-SINGLE) across
sibling reconstructions of the same domain by anchor/stem-Jaccard, reporting each one's
counterpart category/state.

**Config hashing** (`config.py`): every lexicon, threshold and cap is hashed into
`CONFIG_SHA256` (sha256 of canonical JSON of the fixed values, including `JUDGE_MODEL`); decision
0008 requires this hash-frozen before any gold is acquired (not yet done).

Observed result (decision 0008's stated finding): the closure judge does not beat its own fair
control on any ledger tried so far — own_rate ≈ control_rate — so current gap-map output is a
*candidate*, not a demonstrated predictor of hidden knowledge.

## 5. Determinism / reproducibility

- **N1** (`residual/`): pure, deterministic pydantic validation; no model or network calls at all.
- **N2** (`reconstruct/`): every model/search call is logged to `calls.jsonl` (task, model,
  served-model check, tokens, cost, outcome) even on failure; snapshots are content-addressed
  (sha256 of normalised text); `assert Ledger.from_json(ledger.to_json()) == ledger` runs at the
  end of every `reconstruct()` call. Not deterministic end-to-end (live web + live LLM calls), but
  every claim traces to a byte-fixed snapshot span. `E-PLANT`/`corpus.py` replay a frozen local
  corpus for adversarial/ablation testing, offline.
  Live network/model calls require `python -m reconstruct.run --live` with `--max-usd`; tests
  never call live models or the network.
- **N3** (`gapmap/`): fully offline by default — lexicon logic is deterministic Python; the one
  model call (the closure judge) is cached and replayed by content hash
  (`sha256(model_id, prompt)`), so `uv run --directory gapmap pytest -q` and a default CLI run
  touch no network. Re-judging (`--judge ollama`) is the only way to add cache entries, and it
  invalidates comparability with a cached run if the prompt changes (config hash changes too).
- `uv run --directory residual|reconstruct|gapmap pytest -q`: 153 / 342 / 161 tests respectively
  (656 total across the three NOW packages), all offline.

## 6. Data flow for one architecture figure

**Boxes** (components), left to right:
1. **Live web** (search via OpenRouter web plugin + arbitrary HTTP fetch) — external, not owned.
2. **`reconstruct.web`** — fetch + normalise + snapshot (deterministic).
3. **OpenRouter LLM backend** (`reconstruct.llm`) — one HTTP boundary for 4 configured roles
   (planner/extractor/baseline: anthropic/claude-haiku-4.5; verifier: openai/gpt-5.4-mini) — LLM.
4. **`reconstruct.evidence` + `reconstruct.run`** — plan/extract/locate/cluster/verify/
   cross-verify/slot/decoy orchestration — mixed (LLM calls inside a deterministic control loop;
   locate/cluster/slot-status/decoy-validity are pure code).
5. **Artefacts written per run** (`reconstruct/runs/<stamp>-<hash>/`): `ledger.json` (a
   `residual.Ledger`), `sidecar.json` (searches, sources, extractions, slots, cross_checks,
   decoys, stats — everything the ledger does not carry), `report.md`, `calls.jsonl`,
   `areas.json`, `snapshots/` (content-addressed normalised text).
6. **`gapmap` lenses + link/text** — reads `ledger.json` (+ `sidecar.json`) — deterministic.
7. **Local Ollama `qwen2.5:7b-instruct`** (closure judge) — LLM, local/no-cost — cached to
   `closure_judgements.json`.
8. **`gapmap.record`/`rank`/`checks`/`render`** — assembles `Record`s, ranks, checks,
   renders — deterministic.
9. **Artefacts**: `gapmap.json` (`GapMapResult`), `gapmap.md` (human-readable map + checks),
   `closure_judgements.json` (judge cache).
10. **Human** — reads `gapmap.md`, would ask the rendered expert questions of a real expert. **This
    step does not exist yet in the PoC**: no human has answered any generated question, no gold
    ledger has been acquired, and nothing closes the loop back into `residual`'s gold ledgers or
    a gate. The `evidential_gate`/`Measurement`/`Threshold` machinery in `residual.gates` is built
    and tested but has no live NOW caller yet — it is currently exercised only by
    `residual/tests/`.

**What does not exist yet**: any gold ledger populated from real human data; any
`residual.gates.evidential_gate`-guarded NOW decision function actually called in a run; N3 config
hash-freeze (`gapmap/src/gapmap/config.py` is explicitly "in-sample" per 0008); any demonstration
that the closure judge or the ranked map predicts where real expert knowledge sits (0008: judge
does not beat its fair control on any ledger tried).

## 7. Excerpts

**A claim record's evidence** (`reconstruct/runs/20260928T145943Z-bc1cc9a30a02/ledger.json`,
domain "EU data protection law", trimmed):

```json
{
  "assertion": "A DPIA should attach any relevant additional documents referenced in the DPIA, such as Privacy Notices and consent documents.",
  "knowledge_type": "check", "layer": "L2", "question": "performance",
  "evidence": [{
    "retrieved": "2026-09-28",
    "selector": {
      "exact": "attached any relevant additional documents we reference in our DPIA, e.g. Privacy Notices, consent documents",
      "locator": "sha256:14b9bb...f8a23e7;char=9061,9169"
    },
    "source": {"identifier": "https://ico.org.uk/.../data-protection-impact-assessments/",
               "kind": "procedure_document", "world": "public", "voice": "expert"},
    "verification": {"verdict": "pending", "verifier": null}
  }],
  "generation": {"activity": "extraction",
    "agent": {"kind": "model", "family": "anthropic", "id": "anthropic/claude-haiku-4.5"}}
}
```

**N1 freeze file** (`residual/frozen/n1.json`):

```json
{
  "schema_sha256": "f2ffcfdfab6ea55a2e187c864d14a411e1a6cd2b2c54bd0fa7b9dbfb70652591",
  "features_sha256": "f2d3e07999560b5587987d31e96353a4fd526acf600dabaebc4d79cb54a3bfe9",
  "semantics_sha256": "f3e85218b9d3868467ed7c6ca646496ccfebcd6d91943ce152c7884b3b391d5d",
  "frozen_by": "N1"
}
```

**A gap-map HYP record** (`research/n3/gdpr_v1/gapmap.json`, trimmed):

```json
{
  "gap_id": "g-1b1e68dc5d39", "lens": "RESULT", "category": "HYP",
  "missing": "a result-to-interpretation mapping for 'measures, new technologies, and novel processing types.'",
  "confidence": {"A": 1, "B": 0, "P": 1, "Q": 0, "breadth": "narrow", "k_step": 1, "k_topic": 2, "robustness": "0/4", "score": 0},
  "hypothesis": {"label": "inferred", "predicted_knowledge_type": ["interpretation", "expectancy"],
    "text": "Hypothesis (inferred): practitioners are predicted to read the result of '...' against expected values..."}
}
```
