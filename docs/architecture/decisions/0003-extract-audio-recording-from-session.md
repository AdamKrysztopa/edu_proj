---
id: 0003
status: proposed
skill: decide-architecture
date: 2026-09-27
commit: 30a2b8e
rules:
  - id: recording-module-owns-audio-streams
    statement: Audio part and chunk bookkeeping, completeness checks and assembly live in one recording module that Session calls; Session keeps only the phase transitions.
    scope: ["instrument/src/probe_app/**"]
    severity: warning
    verification: narrative
  - id: empty-stream-is-an-error
    statement: Assembling a stream with no parts, or with missing or out-of-order chunks, raises or reports an error; it never yields an empty result that lets a problem be probed without its audio.
    scope: ["instrument/src/probe_app/**"]
    severity: blocking
    verification: narrative
  - id: extract-before-freeze
    statement: The extraction lands after the pilots and before probe-app freeze, with the stream-invariant tests written against the current code first and the code moved under them unchanged.
    scope: ["instrument/src/probe_app/**", "instrument/tests/**"]
    severity: warning
    verification: narrative
---
# Extract audio recording from the session state machine

## Context

An architecture review of `instrument/` on 2026-09-27 found the layered, single-process shape (HTTP adapter over one session state machine over narrow services, about 2,000 lines of Python) right-sized for a one-laptop lab instrument, with one exception. Audio-stream handling (`Session.recording_start`, `recording_chunk`, `_store_single_part`, `_transcribe_stream`, `finalize_human_probe` in `instrument/src/probe_app/session.py`) mixes part and sequence bookkeeping with phase transitions. It needed two rounds of fixes (9ce748a, 737aa8e), and two silent audio-loss paths passed the full test suite and `/preflight pilot` and were caught only by `validity-reviewer` (`docs/lessons.md`). Lost think-aloud audio is unrecoverable study data.

## Decision

| Axis | Pick | Why it fits | Cost to accept |
|------|------|-------------|----------------|
| Structure (inside `probe_app`) | A small recording module, one object per stream, behind a narrow interface: accept a part or chunk, report completeness, assemble, never yield an empty stream silently | Puts the fragile invariants where tests can pin them directly, without driving the whole state machine | About 100 lines moved and one more seam to keep in step with `web/js/expert.js` |

First step: tests on the stream invariants against today's code, then move the code under them unchanged. No other structural change:
- the layering and the LLM backend seam (`backends.py` behind `llm.py`) stay;
- `probe_code` keeps importing `SessionState` from `probe_app`: one schema for the session files is the right coupling for a pipeline that must read exactly what the app wrote;
- polling, no build step and file storage stay, being right-sized for one expert on a LAN;
- the rest of `session.py` stays, being the phase transitions, which belong together.

## Consequences (cost)

- A refactor of validity-critical code needs a `validity-reviewer` pass and a clean `/preflight` afterwards, like any change under `instrument/src`.
- Timing is after the pilots so a regression cannot cost pilot audio, and before `probe-app freeze` so data sessions run on the extracted code from the start. If the pilots show audio loss anyway, the order reverses: fix first, extract with the fix.
- Least-architecture check: this is a module extraction, not a new layer or process. Reopen the wider structure only if another part of `session.py` shows the same repeated-fix pattern.
