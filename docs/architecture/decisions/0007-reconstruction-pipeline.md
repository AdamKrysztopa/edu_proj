---
id: 0007
status: active
skill: decide-architecture
date: 2026-09-28
commit: 3b72fb8
rules:
  - id: reconstruct-never-imports-instrument
    statement: No module under reconstruct/src/reconstruct imports instrument, probe_app or probe_code; Track A components are reused by copying and trimming them, never by importing instrument code.
    scope: ["reconstruct/**"]
    severity: blocking
    verification: deterministic
    verified_by: pytest-archon#test_modules_never_import_instrument
  - id: only-evidence-builds-evidence
    statement: Evidence, Selector and Verification are constructed only inside reconstruct/src/reconstruct/evidence.py; every other module is checked for the constructor call and must not contain it.
    scope: ["reconstruct/src/reconstruct/**"]
    severity: blocking
    verification: deterministic
    verified_by: pytest-archon#test_only_evidence_module_constructs_evidence_selector_verification
  - id: span-is-ours
    statement: Selector.exact is a slice of our own fetched, normalised text, never the model's string; a quote that cannot be located verbatim in that text creates no Evidence, and the claim stays a synthetic generation with no software verdict.
    scope: ["reconstruct/src/reconstruct/evidence.py"]
    severity: blocking
    verification: deterministic
    verified_by: pytest-archon#test_fabricated_quote_gets_no_evidence_and_is_synthetic
  - id: support-needs-other-family-and-quote-in-span
    statement: A SUPPORTS verdict is written only from a model whose family differs from the extractor's, and only when its supporting_quote is a normalised substring of the claim's own span; same-family verdicts never produce a criterion label, and a quote outside the span is recorded INSUFFICIENT, not supported.
    scope: ["reconstruct/src/reconstruct/evidence.py"]
    severity: blocking
    verification: deterministic
    verified_by: pytest-archon#test_same_family_verifier_never_produces_supports_or_criterion_labels
  - id: unknown-only-when-examined
    statement: A slot becomes an UNKNOWN ledger record only when its area was searched, at least one document was fetched and extracted, no area was wholly lost to truncation, and a verifier of another family returned a verdict on every located claim in the slot; otherwise the slot is unverified or unexamined, reported only in the sidecar, never written to the ledger.
    scope: ["reconstruct/src/reconstruct/evidence.py"]
    severity: blocking
    verification: deterministic
    verified_by: pytest-archon#test_slot_unknown_only_when_fully_examined_and_verified
  - id: independence-before-corroboration
    statement: Fetched documents are clustered by union-find on domain-grouping key or shingle containment at least 0.5 alone (no verbatim-run rule) before any claim is counted as corroborated; a shared verbatim run of at least 25 words between spans in two different clusters is not a clustering link but collapses those spans to one corroboration count, so a syndicated copy that only shares a quoted passage still counts once without merging the documents themselves into one independence key.
    scope: ["reconstruct/src/reconstruct/evidence.py"]
    severity: blocking
    verification: deterministic
    verified_by: pytest-archon#test_syndicated_passage_on_two_domains_merges_to_corroboration_one
  - id: retrieved-text-is-data
    statement: Fetched page text is passed to models only inside clearly delimited data blocks; the planner is never shown page text, the extractor call carries no tools, and a span matching a known injection pattern is flagged and left PENDING rather than reaching the verifier as an instruction.
    scope: ["reconstruct/src/reconstruct/**"]
    severity: blocking
    verification: deterministic
    verified_by: pytest-archon#test_hidden_and_flagged_visible_injection_never_reach_the_verifier
  - id: single-openrouter-backend-and-served-model-check
    statement: All model calls and search route through one OpenAI-compatible OpenRouter backend; openrouter/auto and fallback model lists are rejected at load time, and every response's served model is compared to the configured slug — a mismatch discards the verdict (evidence stays PENDING) while the served id is still logged to calls.jsonl.
    scope: ["reconstruct/src/reconstruct/llm.py"]
    severity: blocking
    verification: deterministic
    verified_by: pytest-archon#test_backend_served_model_mismatch_logs_then_raises
  - id: budget-before-every-call
    statement: A hard --max-usd budget is checked against accumulated cost before every model or search call, never after; exceeding it blocks the call before client dispatch and the run is marked incomplete.
    scope: ["reconstruct/src/reconstruct/llm.py"]
    severity: blocking
    verification: deterministic
    verified_by: pytest-archon#test_budget_blocks_the_call_before_any_client_dispatch
  - id: every-call-logs-even-on-failure
    statement: A provider error is logged to calls.jsonl exactly like a success — outcome "api_error" with its error class and HTTP status, never billed — before the caller ever sees LLMUnavailable; a transient error (rate limit, timeout, connection, 5xx) is retried up to three times with backoff, a non-transient error is logged once and raised immediately, and neither path may skip the log line to reach the exception.
    scope: ["reconstruct/src/reconstruct/llm.py"]
    severity: blocking
    verification: deterministic
    verified_by: pytest-archon#test_backend_retries_429_then_succeeds
  - id: failed-calls-counted-per-task
    statement: Every stage that skips a unit after a failed plan, verify, cross-verify or decoy call increments that call's own task label in the run's failed_calls_by_task counts; a run's sidecar must show how many calls of each task failed, not only how many succeeded, so "complete: true" never hides a silent loss.
    scope: ["reconstruct/src/reconstruct/run.py"]
    severity: blocking
    verification: deterministic
    verified_by: pytest-archon#test_failed_calls_by_task_counts_verify_failures
---
# Reconstruction pipeline: a one-way evidence-gathering walking skeleton

## Context

N2a needs a pipeline that, given only a domain and a task, builds a provenance-backed N1 Evidence Ledger from real external sources for N3 to compute a gap map over (`docs/plans/n2a-walking-skeleton.md`). Decision 0006 makes `residual-core-provider-neutral` blocking: `residual/` may depend only on pydantic and itself, so no network or LLM code can live there. The pipeline is a new sibling package, `reconstruct/`, depending on `residual` by path, that populates the frozen N1 types (`ClaimRecord`, `Evidence`, `Selector`, `Verification`, `Source`, `Ledger`) without editing them.

The design (N2a spec, accepted with amendments A1–A14 and B, C) treats retrieval as unverified: a page being fetched is not the same as a claim being supported. Support is an N1 `SUPPORTS` verdict from a model of another agent family than the extractor's, looking only at the claim and our own normalised text around its span. This is a stricter reading of §11's curated-first sourcing: N2a runs on the open web with no curated tier, so every web source is recorded at host tier `"open"` in the sidecar — a deliberate, stated departure, not an oversight.

## Decision

- **Package boundary.** `reconstruct/` is a sibling uv package (`[tool.uv.sources] residual = {path="../residual", editable=true}`), never imported by `residual/` or `instrument/`. Five modules plus prompts: `llm.py` (model boundary — Anthropic native and one OpenAI-compatible OpenRouter backend, copied and trimmed from `instrument/src/probe_app/backends.py`, never imported), `web.py` (search via the OpenRouter web plugin, our own fetch, HTML→visible text, content-addressed snapshots), `evidence.py` (the pure deterministic core — the only place that builds `Evidence`, `Selector` or `Verification`), `run.py` (one-way orchestration, no agent loop), `report.py` (Markdown rendering).
- **Provenance is real, not asserted.** The span a claim is verified against is always a slice of text we fetched and normalised ourselves, addressed by `sha256:<text>;char=<start>,<end>`, never the model's own quotation. A quote that doesn't locate verbatim in our text produces no `Evidence` at all — the claim stays synthetic.
- **Support crosses a family boundary.** Only a verifier from a different model family than the extractor's, given the claim plus a bounded window of our own text, can move a claim off *synthetic*/*unknown*; its supporting quote must itself be inside the claim's span. No second family configured means every claim is `PENDING` and the report says so in its headline.
- **UNKNOWN is provenance-gated.** A slot writes an UNKNOWN placeholder to the ledger only once it has been searched, fetched, extracted and fully verified by another family; anything less specific (nothing sought, or sought but not fully examined) stays in the sidecar and report, never in the ledger N3 reads.
- **Corroboration follows independence, not source count.** Union-find over domain, shingle overlap and shared verbatim runs collapses syndicated copies to one cluster before anything is called corroborated. This is conservative in the other direction too: identical assertions merge, but paraphrases of the same fact stay separate records, so corroboration is undercounted rather than inflated — accepted, since N3 should never see corroboration invented by wording.
- **Retrieved text is data, never instruction.** Page text reaches a model only inside delimited blocks; the planner never sees fetched content, the extractor gets no tools, and text matching known injection patterns is flagged and excluded from the verifier's input (R11).
- **One backend, checked, one budget, checked first.** Every call — model or search — goes through the single OpenRouter backend, `openrouter/auto` and fallback lists are refused at load, and the served model in the response is checked against the configured slug before its verdict counts. A `--max-usd` budget is checked from accumulated cost before dispatching any call, live runs otherwise refuse to start, and tests never call a live model or search (amendment C).
- N1's types are unchanged; `reconstruct/` only populates them.

## Consequences (cost)

- A claim with an unlocated quote, a same-family verdict, or a quote outside its span produces no criterion label — this is by design, but it means a plausible-sounding extraction can sit at *synthetic* indefinitely if the verifier family is misconfigured; `single-openrouter-backend-and-served-model-check` and the calls.jsonl log are what catch that, not a human reading the report.
- Host tier `"open"` for every N2a source is a stated gap against §11: nothing here ranks curated sources above the open web, so N3's gap map runs on a lower evidentiary floor than a curated pipeline would give it.
- Undercounting corroboration on paraphrase means N3 may see fewer independent-looking sources than actually exist; accepted as the safer error for a criterion-adjacent signal.
- The nine rules above are all blocking and deterministic, which is more test surface per change than a looser pipeline: an edit to `evidence.py`, `llm.py` or the module layout that violates any of them fails `uv run --directory reconstruct pytest -q` rather than surfacing later in a run's sidecar.
