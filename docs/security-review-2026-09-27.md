# Security review: Stage A session app (2026-09-27)

Recommendation: restrict the console routes to the laptop itself, derived below.

## Threat model

**System context:** `probe-app serve` runs a FastAPI app on the researcher's laptop. The expert uses a tablet on the same network, or the laptop in person. The app records think-aloud audio, drawings and probe dialogue, sends audio to a speech-to-text provider and transcripts and images to LLM providers, and writes everything to `sessions/`. A failure costs participant confidentiality (expert pseudonymised speech and work) or study validity (a trace altered outside the sanctioned correction path, a session ended early).

**Assets:**
- Session data in `sessions/<id>/`: audio, transcripts, corrections, drawings, full LLM logs. Owned by the study and the only copy (git-ignored, not backed up).
- Trace integrity. The console's segment correction is the sanctioned edit path, and every correction is stored as a diff and shown to both arms.
- API keys in `instrument/.env`, owned by the researcher.
- The pseudonym key, kept outside the repository.

**Actors:**
- **A device on the same network as the laptop:** a university Wi-Fi or conference-room peer, reachable when the app is served on `0.0.0.0` (`instrument/pilot-protocol.md:12`).
- **The expert's tablet:** holds the session link and therefore the session ID.
- **A web page open in the researcher's browser** during a session: can send cross-origin requests to `https://127.0.0.1:8000`.
- **The processors:** Anthropic, ElevenLabs, OpenAI and OpenRouter, the providers named in `models.json` and the consent form.
- **Whoever gets the laptop:** theft or loss.

**Boundaries:**
1. **Network ↔ server.** Assumed on the server side: only the tablet talks to the expert routes, and only the researcher on the laptop uses the console (design spec §2, "Console (researcher, localhost)"). What holds today: every route is served on the same host and port with no origin check. The only credential is the session ID in the URL, which is `<expert_id>-<8 hex>` (`instrument/src/probe_app/storage.py:29`), and `POST /api/sessions` needs none.
2. **Laptop → providers.** Audio, transcripts and canvas images leave the laptop over TLS under each provider's data-processing terms.
3. **Laptop disk.** Session data and `.env` at rest.

### Violations: a checker with a resolved binding failed
_None._ No security tool is configured in this repository.

### Findings: the design contradicts a stated property
| Asset or boundary | Actor | Impact | Cheapest control | Cost of that control | Evidence (file, line, structure) | Reopen when |
|---|---|---|---|---|---|---|
| Trace integrity and transcripts, boundary 1 | A device on the same network holding the session link, or the tablet itself | Reads full transcripts and the event log (`console-view`); edits or adds trace segments through the sanctioned correction path, so the edit looks legitimate in the log; ends, pauses or resumes a probe; creates junk sessions | Serve console-only routes to loopback clients only: reject any request whose `request.client.host` is not `127.0.0.1` or `::1` on `/`, `POST /api/sessions`, `console-view`, `think-aloud/start`, `keep-talking`, `segments*`, `probe/start`, `probe/answer-text`, `probe/end`, `human/*`, `pause` and `resume`. Leave the expert routes open (`expert-view`, `recording/*`, `think-aloud/{pid}/end`, `probe/answer`, `probe/finalize`, `snapshot`) | About 15 lines (one FastAPI dependency plus a test per side). The researcher must run the console on the laptop, which the protocol already assumes | `instrument/src/probe_app/server.py:96-208` (no route checks the client); `instrument/src/probe_app/cli.py:17` (`--host`); `instrument/pilot-protocol.md:12` (`--host 0.0.0.0`); design spec §2 | The console must run on a second device, which needs real authentication instead |

### Gates considered and closed: reviewed, not bought
| Gate | Why it stays closed | Reopen when |
|---|---|---|
| User accounts and login | One researcher and one expert device per session; loopback restriction plus the session-ID capability covers the named actors | More than one researcher operates sessions, or the console leaves the laptop |
| Agent permission scoping | The interviewer and guard have no tools; their only output is text that passes the contract and guard before the expert sees it. No agency surface | A tool, retrieval or any side effect is added to an LLM role |
| CSRF tokens | The JSON routes need a CORS preflight the app never grants. The multipart expert routes could be posted cross-origin, but only by a page the researcher opens during a session, and only with the session ID | The researcher browses during sessions, or the session ID appears anywhere a page could read it |
| Rate limiting | With the loopback fix, the remaining open routes need a session ID; guessing one is impractical within a 75-minute session | The session ID's randomness is reduced, or the app is exposed beyond the local network |
| Encryption of session files by the app | Full-disk encryption covers a lost laptop at no app cost (see Assumptions) | Session data are copied off the laptop unencrypted |

### Assumptions: recorded, never graded
| Assumption | Why it is accepted | What would make it false |
|---|---|---|
| The laptop has full-disk encryption (FileVault) on | Standard for a research laptop and outside the app's control | FileVault off, or sessions copied to unencrypted media |
| Each provider's data-processing terms and retention are confirmed before a real session | Pilot protocol "Before the session" item 1 requires it, and consent names the processors | A role moves to a provider not on the consent form, or OpenRouter routes to an unlisted upstream |
| The pseudonym key never enters the repository | Stated in the design spec §4 | The key is stored under `instrument/` or `sessions/` |
| Only `.env` holds secrets, and it is git-ignored | `.gitignore:6`; `guard-secrets` hook denies tool calls naming a `.env` | A key is pasted into a config, a test or a log |

### Observations: could not be completed into findings
- The session ID carries 32 random bits (`uuid4().hex[:8]`). That is enough for the actors above once the console is loopback-only. The full `uuid4().hex` costs nothing, though, and removes the question.
- `sessions/` is the only copy of irreplaceable data (CLAUDE.md: "not backed up"). That is an availability risk rather than a boundary; an encrypted copy after each session closes it.

**Controls deliberately not bought:** user accounts, TLS client certificates for the tablet, and app-level encryption of session files. No named actor needs more than the loopback restriction and disk encryption.
**Not checked here:** secrets in git history (`gitleaks`, not configured) and dependency advisories (`pip-audit` or `osv-scanner` over `instrument/uv.lock`, not configured). Neither is asserted clean.
**Primary recommendation:** make every console-only route refuse non-loopback clients, so that a device on the same network, including the expert's tablet, can reach only the expert routes.
**The proportionality check:** one small server-side check closes the only boundary where a reachable actor meets an asset; everything heavier stays closed on today's single-researcher, single-laptop setup.
