---
name: preflight
description: Go/no-go gate before a Stage A pilot or data session — clean tree, pre-registration match, tests, live transcriber and simulated session, and a validity review of every instrument change since the last real session.
argument-hint: pilot|data
disable-model-invocation: true
---

# /preflight

Arguments: `$ARGUMENTS` (`pilot` or `data`; if missing, ask once and stop).

1. Run `bash .claude/skills/preflight/preflight.sh <mode>` from the repository root with a 600000 ms timeout. It makes live API calls (two transcriptions and a full simulated session, about 7 minutes) and prints one line per check, then `REVIEW_BASE=`.
2. Launch the `validity-reviewer` agent on `git diff <REVIEW_BASE>..HEAD -- instrument/`. If `REVIEW_BASE=none`, no real session has run yet, so have it review `instrument/src`, `instrument/web` and `instrument/prompts` in full. If the diff is empty, skip the review and say so.
3. Load the console (`https://127.0.0.1:8000`) and the expert page (`https://<LAN-IP>:8000/expert`) with the Playwright MCP, using the exact `probe-app serve` command and certificate from `instrument/pilot-protocol.md`, and join as the expert. A `curl` status code is not this check. Report NO-GO if either page fails to load or join.
4. Ask the user to confirm the items in `instrument/pilot-protocol.md` "Before the session" that no script can check: consent forms, the tablet's HTTPS certificate, the physicist's problem check, the microphone dry run.
5. Report **GO** only if the script printed no `FAIL`, the reviewer found nothing it marks as blocking, step 3 passed and the user confirmed step 4. Otherwise report **NO-GO** with each blocking line. List every `WARN` either way; a `WARN` on `interviewer_refused` is the protocol's cue to change the interviewer before freezing.

Never start the session from this skill.
