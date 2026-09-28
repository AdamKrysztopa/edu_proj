---
name: session-report
description: Summarise one Stage A session directory (sessions/<id>) — interviewer turns, guard and contract rejections, refusals, stem coverage, answer latency, audio parts and transcription failures — against the pilot protocol's measures.
argument-hint: <session-dir>
disable-model-invocation: true
---

# /session-report

Session: `$ARGUMENTS` (a directory under `sessions/`; if empty, use the most recent one: `ls -td sessions/*/ | head -1`).

1. Run `python3 .claude/skills/session-report/report.py <session-dir>` and show its output unchanged.
2. Check it against `instrument/pilot-protocol.md` → "Measured" and "Refusals", and state each verdict in one line:
   - AI latency median under 6 s;
   - interviewer failures at or below about 1 in 10 AI turns;
   - every stem covered in both sets, or the cap reached (say which);
   - a human-arm set with more than one audio part means the tablet reloaded; say so;
   - any human-arm speech before the first I/E marker is excluded from every export; give its word count.
3. Flag anything that makes the session unusable as data: `simulated` or `git_dirty` in the header, an unfinished set, untranscribed problems, a transcription failure in a probe set, or a human-arm set with speech before the first I/E marker (an `unmarked_speech` event; its answers are lost to coding).
4. Do not open audio files or the instrument's API-key file. Comparing transcribers costs API calls: suggest the commands from the pilot protocol, do not run them unless asked.
