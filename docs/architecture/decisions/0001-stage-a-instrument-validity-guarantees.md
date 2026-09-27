---
id: 0001
status: proposed
skill: migrate
date: 2026-09-27
commit: 30a2b8e
rules:
  - id: frozen-config-refuses-data-session
    statement: The session app refuses to start a data session whose interviewer and guard model IDs, effort, or prompt, stem and guard hashes differ from the pre-registered values in instrument/prereg.json.
    scope: ["instrument/src/probe_app/**", "instrument/prompts/**"]
    severity: blocking
    verification: narrative
  - id: ai-turn-passes-contract-and-guard
    statement: No AI interviewer turn reaches the expert unless code has checked it against the turn contract (known stem, at most one follow-up per stem carrying a quoted span that occurs in the expert's own words) and the leading-question guard has not flagged it; a second rejection falls back to the next unused stem shown bare, and rejected turns are logged, never shown.
    scope: ["instrument/src/probe_app/**"]
    severity: blocking
    verification: narrative
  - id: no-silent-model-substitution
    statement: Server-side model fallbacks are not enabled; a refusal or failure is logged and the turn falls back to the bare stem instead of another model answering.
    scope: ["instrument/src/probe_app/**"]
    severity: blocking
    verification: narrative
  - id: full-session-log
    statement: Every LLM request and response is logged in full, and session events are append-only with a monotonic and a wall-clock timestamp on one session clock shared by strokes, audio and transcript segments.
    scope: ["instrument/src/probe_app/**"]
    severity: blocking
    verification: narrative
  - id: blind-coding-material
    statement: The blinded coder export contains no interviewer text, the trace export contains no probe material, and the decoy answer key and unit-ID key are written separately from the sheets coders see.
    scope: ["instrument/src/probe_code/**"]
    severity: blocking
    verification: narrative
  - id: simulated-sessions-rejected
    statement: Sessions produced with a simulated expert are marked simulated and rejected by the coding pipeline.
    scope: ["instrument/src/probe_code/**", "instrument/src/probe_app/**"]
    severity: blocking
    verification: narrative
  - id: session-data-outside-repo
    statement: Session data live only under git-ignored session directories, identified by pseudonym; names and the pseudonym key never enter the repository.
    scope: ["instrument/src/probe_app/**"]
    severity: blocking
    verification: narrative
---
# Stage A instrument: validity guarantees enforced in code

## Context

The Stage A instrument (`instrument/`) runs think-aloud and retrospective probe sessions with expert physicists and turns them into blinded coding material. The study compares an AI interviewer with a human one, so the instrument's job is to keep that comparison fair and auditable: every expert must meet the same frozen interviewer, the AI must not lead the expert, and coders must not be able to tell the arms apart from interviewer wording. Current models accept no sampling temperature, so reproducibility has to come from the log rather than from re-running.

The source spec also fixes implementation choices that are not recorded as rules here: a laptop-served FastAPI web app with a tablet over HTTPS, one-second polling, static JavaScript with no build step, a `Transcriber` interface with timestamped segments, and a 20-minute probe cap with a close request from 18 minutes.

## Decision

Validity-critical behaviour is enforced by code, not by researcher discipline:
- the frozen configuration (model IDs, effort, prompt, stem and guard hashes) is checked against the pre-registration before any data session;
- each AI turn passes a code-checked contract and a separate leading-question guard before the expert sees it, with regenerate-once-then-bare-stem as the only fallback;
- no model is ever substituted silently;
- every LLM exchange and event is logged in full on one clock;
- the coding pipeline produces blinded, trace-only and decoy-mixed material with keys held apart, and rejects simulated sessions;
- session data stay outside version control under pseudonyms.

Every rule is `narrative`: the repository has no ast-grep, import-linter, semgrep or pytest-archon configuration to bind them to. Several are exercised by the instrument's pytest suite (hash refusal, contract rejection, blinded export contents), which a human may later choose to bind.

## Consequences (cost)

- Any prompt, stem, guard or model edit after the freeze invalidates data sessions until a re-freeze and a new pre-registration.
- A turn the model cannot produce within the contract degrades to a bare stem, so a model with a high refusal or rejection rate shortens the AI arm's effective dialogue rather than failing loudly; the refusal rate has to be watched in preflight and pilots.
- Full logging stores transcripts and images per session, which raises the data-protection burden and requires processor agreements with each provider.
- Blinding is only as strong as the export: expert replies can still echo a question, which the design checks separately with a condition-guess rate.

## Sources

- `docs/superpowers/specs/2026-09-26-stage-a-session-app-design.md` at commit 30a2b8e: "Decisions taken", sections 1–5 and 8. Its stack line "Claude via the official `anthropic` Python SDK" and the hard-coded interviewer and guard models are superseded by the model-choice spec (decision 0002) and are not carried into this decision.
