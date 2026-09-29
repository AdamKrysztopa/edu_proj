---
id: 0008
status: proposed
skill: decide-architecture
date: 2026-09-29
commit: ec45c31
rules:
  - id: gapmap-imports-only-stdlib-pydantic-residual
    statement: The gapmap package depends at runtime only on pydantic and residual and imports nothing outside the standard library, pydantic, residual and itself; its model call goes over stdlib urllib, never an SDK.
    scope: ["gapmap/**"]
    severity: blocking
    verification: deterministic
    verified_by: pytest-archon#test_modules_import_only_stdlib_pydantic_residual_and_gapmap
  - id: gapmap-replays-by-default
    statement: The gapmap CLI replays closure judgements from the committed cache and makes no network call unless --judge ollama is passed; a cache miss in replay mode raises an error naming --judge ollama rather than calling a model.
    scope: ["gapmap/src/gapmap/**"]
    severity: blocking
    verification: deterministic
    verified_by: pytest-archon#test_replay_mode_raises_a_clear_error_naming_judge_ollama_on_cache_miss
  - id: undecided-never-a-finding
    statement: A closure judgement that is malformed, cites an unknown sentence id, or raises is the state undecided and is routed to RG-UNDECIDED; it never becomes open and never becomes a hypothesis.
    scope: ["gapmap/src/gapmap/**"]
    severity: blocking
    verification: deterministic
    verified_by: pytest-archon#test_unknown_id_is_undecided_never_open
  - id: closure-judge-other-family
    statement: The closure judge's model family differs from the families that generated and verified the ledger it judges (N2 ledgers - anthropic generator, openai verifier; judge - local qwen).
    scope: ["gapmap/src/gapmap/judge.py", "gapmap/src/gapmap/semantic.py"]
    severity: blocking
    verification: review
  - id: gap-candidates-are-predictors
    statement: Gap records and gap-map scores are predictors labelled inferred; nothing in gapmap writes a hypothesis back into a ledger as a claim, and no gap-map output is passed to a residual gate as a criterion.
    scope: ["gapmap/**"]
    severity: blocking
    verification: review
  - id: retrieval-gaps-never-hypotheses
    statement: A candidate with at most one independent source, closed only by unverified text, closed in the sibling run, searched with nothing found, or undecided is a retrieval gap whose action is search, verify or re-judge, never an expert question.
    scope: ["gapmap/src/gapmap/record.py", "gapmap/src/gapmap/render.py"]
    severity: warning
    verification: review
---
# Gap map: methodology lenses propose candidates, a separately-cached judge closes them

## Context

N3's proof of concept (`research/n3/README.md`, spec `docs/plans/n3-poc-lens-spec.md`) adds a new package, `gapmap/`, downstream of `residual/` (0006) and `reconstruct/` (0007). No active decision covers it. It also introduces the repository's first model call outside `reconstruct/`: a local Ollama judge on localhost, which carries no charge. This decision records the boundaries the PoC relies on. It supersedes nothing.

## Decision

- **Package boundary.** `gapmap/` is a sibling uv project. It imports only stdlib, pydantic and `residual`. It reads N2 ledgers and writes only to its `--out` directory, never to run directories or ledgers.
- **Candidacy.** Methodology lenses decide which candidates exist. The lenses are cue as discrimination, rival causes, selection rule, hedged rule, self-check, rationale and PARI result interpretation. Breadth of the attested side, counted over independent sources, orders the open candidates.
- **Closure.** A semantic judge decides whether a missing element is stated. The judge comes from a model family different from the ledger's generator and verifier, and runs at temperature 0. Its answers are cached with the outputs, and the CLI replays them offline by default. Unparseable answers are `undecided`.
- **Tiers.** Each record keeps three tiers apart: observed evidence (verified verbatim spans), inferred gap (a re-runnable statement about the ledger), and hypothesis (labelled `inferred`). Retrieval gaps are a separate category.
- **Checks travel with the output.** Each map carries its anti-renaming check, the fair mismatched-evidence control for the judge, and the lexical donor null.

## Consequences (cost)

- The judge does not beat its fair control on any ledger so far (own rate equals control rate). The outputs are therefore gap *candidates*. Any claim of hidden-knowledge prediction needs a closure step that passes the control, then the gold test in `docs/plans/n3-gap-map-plan.md`.
- A cached judge makes replay deterministic but freezes one model's answers. Re-judging changes outputs, and a prompt change invalidates the cache.
- The lexicons, the promotional denylist and the DISC stop-anchors are in-sample. `gapmap/src/gapmap/config.py` must be hash-frozen before any gold is acquired.
- `closure-judge-other-family` has no test. The family is set by configuration and checked in review.
