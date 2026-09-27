---
id: 0005
status: proposed
skill: threat-model
date: 2026-09-27
commit: 30a2b8e
rules:
  - id: console-routes-loopback-only
    statement: Every console-only route of the session app (the console page, session creation, console-view, think-aloud start, keep-talking, segment corrections and additions, probe start, typed answers, probe end, human-arm controls, pause and resume) refuses any request whose client is not 127.0.0.1 or ::1; only the expert routes are reachable from the network.
    scope: ["instrument/src/probe_app/**"]
    severity: blocking
    verification: narrative
  - id: session-id-full-uuid
    statement: Session IDs carry a full uuid4 of randomness, not a truncated one.
    scope: ["instrument/src/probe_app/**"]
    severity: warning
    verification: narrative
---
# Console routes answer only the laptop itself

## Context

A threat model of the session app on 2026-09-27 found one boundary where a reachable actor meets an asset. For the tablet, the app is served on `0.0.0.0` (`instrument/pilot-protocol.md:12`), and no route checks who is calling (`instrument/src/probe_app/server.py:96-208`). The design spec says the console is used only on the laptop, but the code does not enforce it. The only credential is the session ID in the tablet's link (`<expert_id>-<8 hex>`, `instrument/src/probe_app/storage.py:29`), and `POST /api/sessions` needs none.

A device on the same network that holds the link, including the expert's tablet itself, can therefore read full transcripts through `console-view`. It can also edit trace segments through the sanctioned correction path, so the edit looks legitimate in the log, and it can end, pause or resume a probe.

Assets at stake: participant confidentiality (pseudonymised speech, drawings, LLM logs) and trace integrity, which both arms and the blinded coding depend on.

## Decision

| Asset or boundary | Actor | Impact | Control | Cost |
|---|---|---|---|---|
| Trace integrity and transcripts; network ↔ server | A device on the same network with the session link, or the tablet | Read transcripts, edit the trace, end or pause probes, create sessions | One FastAPI dependency that rejects non-loopback clients on the console-only routes; the expert routes (`expert-view`, `recording/*`, `think-aloud/{pid}/end`, `probe/answer`, `probe/finalize`, `snapshot`) stay open | About 15 lines and a test per side; the console must run on the laptop, as the protocol already assumes |

Also: session IDs use the full `uuid4().hex`, at no cost.

Gates considered and closed:
- **User accounts and login:** one researcher, one laptop.
- **Agent permission scoping:** the LLM roles have no tools.
- **CSRF tokens:** JSON routes need a CORS preflight the app never grants; the multipart expert routes also need the session ID.
- **Rate limiting:** once the console is loopback-only, the open routes need a session ID that cannot be guessed within a session.
- **App-level encryption of session files:** full-disk encryption covers a lost laptop.

Accepted assumptions:
- FileVault is on.
- Provider data-processing terms are confirmed before a real session (pilot protocol item 1).
- The pseudonym key stays outside the repository.
- Secrets live only in the git-ignored `.env`.

## Consequences (cost)

- The console can no longer be opened from a second device. If that is ever needed, it needs real authentication, and this decision reopens.
- Not bought: user accounts, client certificates for the tablet, and app-level encryption. No named actor justified them.
- Not checked here: secrets in git history (`gitleaks`) and dependency advisories (`pip-audit` or `osv-scanner` over `instrument/uv.lock`); neither tool is configured, and neither property is asserted.
- Reopen when:
  - the console leaves the laptop;
  - more than one researcher runs sessions;
  - the app is exposed beyond the local network;
  - an LLM role gains a tool or side effect;
  - session data are copied off the laptop unencrypted.
- Separate from this decision: `sessions/` is the only copy of irreplaceable data. An encrypted backup after each session is a `PROGRESS.md` item.
