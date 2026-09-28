# N2a: reconstruction walking skeleton (plan)

N2 is an **enabling milestone for N3**. It is not a generic research agent and not the product. Its job is to show that, given only a domain and a task, the system can build a provenance-backed Evidence Ledger from real external sources, one that N3 can compute a gap map over. It is optimised for evidence N3 can use, not for answers, reports or retrieval breadth.

This plan replaces the build order of [`n2-reconstruction-plan.md`](n2-reconstruction-plan.md). That plan's gate, experiments (E-PLANT, E-ABST) and N1 hand-over still stand. What changed and why is in its "Revision" section.

## Shape

A sibling uv package, `reconstruct/`, depends on `residual` by path. Decision 0006 forbids network or LLM code inside `residual/`, so the pipeline cannot live there. It populates the frozen N1 types and never edits them.

| Module | Role |
|---|---|
| `llm.py` | The model boundary. One `Model(agent).json(task, system, user, schema) -> dict`. Anthropic native plus one OpenAI-compatible backend (OpenRouter), trimmed from Track A's pattern by copy. Every call is logged to `calls.jsonl`. |
| `web.py` | Anthropic `web_search`, used for URLs only. We fetch each URL ourselves and convert HTML to visible text (hidden, script and style content dropped). Page metadata comes from citation, OG or JSON-LD tags. Snapshots are content-addressed. |
| `evidence.py` | The pure, deterministic core: normalisation, span location, independence clusters, N1 record construction, slots and UNKNOWN, contradiction filtering. Only this module builds `Evidence`, `Selector` or `Verification`. |
| `run.py` | A one-way pipeline: plan → search → fetch → extract → locate → verify → contradict → assemble. There is no agent loop and no framework. |
| `report.py` | Renders the ledger and sidecar to Markdown. |
| `prompts/*.md` | Each prompt's sha256 becomes its `Generation.spec_sha256` or its contradiction `method`. |

## Semantics (summary; details in the code's docstrings)

- **Retrieved is not the same as supports.** Retrieval lives in `sidecar.json`. Support exists only as an N1 `SUPPORTS` verdict from a model of another family than the extractor, given only the claim and our own text around the span.
- **The span is ours.** `Selector.exact` is a slice of our normalised text, never the model's string. `locator = sha256:<text>;char=a,b`. A quote not found verbatim gets `UNRESOLVABLE` from software and no model verdict.
- **Independence.** Documents are clustered by union-find over three links: the same registrable domain, 5-shingle Jaccard ≥ 0.5, or a shared verbatim run of ≥ 25 words. The key is `ind-<smallest source_id>`, so a syndicated copy counts once.
- **UNKNOWN.** Areas come from one planner call (recorded as *inferred*), crossed with a fixed probe set. Each slot is covered, UNKNOWN (sought, nothing reached a criterion label) or unsought (every search failed). An UNKNOWN slot is a ClaimRecord whose assertion is a software-templated question, with no generation and only its area's searches.
- **Contradictions.** Only same-slot pairs with located spans are compared, by one classification call. Only `genuine`, with both conflicting quotes verbatim in their spans, becomes an N1 `Contradiction`. Scope, temporal, terminology and insufficient differences go to the sidecar.
- **No second family.** If none is configured, evidence stays `PENDING`, claims compute as synthetic, and the report headline says so. No same-family verdict is ever run.

## Order

1. N2a skeleton plus offline tests (fixture HTML, a scripted fake model).
2. **E-LIVE**, a sanity gate, not a benchmark, on two structurally different domains: centrifugal pump cavitation diagnosis (technical, procedural) and GDPR DPIA obligations (legal and normative, with scope and temporal disagreement). `reconstruct/runs/` persists the artefacts. The report is `research/n2/e_live_report.md`.
3. Skeptical review; remove whatever N3 does not need.
4. Rest of N2: corpus mode (a manifest of local documents), E-PLANT (planted sources, decoy spans, the ungated baseline), E-ABST (private objectives, raw-model baseline). Methods-critic reviews the protocol before any run.

**Not built:** OpenAlex resolution, NLI, `as_of` at fetch time, gap-map features (N3), reruns for stability (after E-LIVE), PDFs (rejected and counted), any vector store, graph, agent framework or Weft.
