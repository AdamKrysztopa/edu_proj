# Pilot protocol: Stage A session app

**Purpose.** Check that the instrument runs a full session and build codebook v0. Pilot sessions are never Stage A data.

**Participants.** One or two physicists who have taught first-year mechanics. Not eligible for Stage A afterwards.

## Before the session

1. Ethics: the pilot consent form (`consent-pilot.md`, bracketed fields filled in) names as processors the providers of the interviewer and guard in `instrument/models.json`, both transcribers compared in the pilot (ElevenLabs for `scribe_v2`, OpenAI for `whisper-1`), and, for a role on `openrouter`, OpenRouter and the upstream provider(s) in its `route`; each provider's data-processing terms and retention are confirmed. Stage A consent names only the providers in the frozen `models.json`.
2. Keys in `instrument/.env` (`ANTHROPIC_API_KEY`, `ELEVEN_LABS_API_KEY`, `OPENAI_API_KEY`, and `OPENROUTER_API_KEY` if a role uses `openrouter`); never committed.
3. Tablet over the network needs HTTPS. Once, in the repository root: `mkcert -install && mkcert <laptop-LAN-IP> 127.0.0.1 localhost`, renamed to `session-cert.pem` and `session-key.pem` (git-ignored). Install `rootCA.pem` from `mkcert -CAROOT` on the tablet and mark it fully trusted (iPad: Settings → General → About → Certificate Trust Settings). Then, from the repository root:
   `uv run --directory instrument probe-app serve --host 0.0.0.0 --ssl-certfile "$PWD/session-cert.pem" --ssl-keyfile "$PWD/session-key.pem"`.
   Console on the laptop only: `https://127.0.0.1:8000` (with TLS, `http://` gives a blank page); from any other address the console routes answer 403. At startup the server prints `Tablet: https://<laptop-LAN-IP>:8000/expert`, and the console's "Expert link" uses that address. Check that it is the laptop's Wi-Fi address and that the certificate covers it; a VPN can change which address is printed. Open that exact link on the tablet (it carries the session code, so nothing needs typing), press Join and allow the microphone. If the microphone is refused or the page was opened over `http://`, the tablet now says so. Verified end to end in a browser on 2026-09-28 (console create → tablet link → join → think-aloud → audio chunks stored; LAN access to console routes refused). A new network address needs a new certificate.
   In person on the laptop itself: `uv run --directory instrument probe-app serve` and use `http://127.0.0.1:8000`.
4. A physicist checks the four problems in `problems/problems.json` and the two ordinary-explanation problems in `problems/explanation-problems.md` (printed for step 2 of the session).
5. `/preflight pilot` (`/preflight data` before a data session): tests, both transcribers on a synthesised phrase, a live simulated session with its `interviewer_refused` rate (see "Refusals" below), and a `validity-reviewer` pass over instrument changes since the last real session.
6. Dry run with a colleague on the real tablet and microphone: the automated browser check replaced the microphone with a synthetic stream.

## Session (about 75 minutes)

1. Consent (5 min).
2. **Ordinary explanation (10 min, paper).** "Write a worked explanation of these two problems for a first-year student": one problem from set A, one from set B, not used later. Scan it into `sessions/<id>/explanation/`.
3. **Think-aloud (about 20 min).** Console: create a pilot session, give the expert the link, press "Start next problem" for each of the four problems. Instructions only: "Solve it and say everything you are thinking, including anything that feels obvious." The only allowed prompt is "Keep talking" (console button) after about 10 s of silence. Do not reload the expert page during a problem: the audio recorded so far would be lost.
4. **Trace review (5 min, researcher only).** Correct transcription errors in physics terms; do not add content.
5. **Probe session, set 1 (up to 20 min)** and **set 2 (up to 20 min)**: AI on one set, human on the other, as chosen at creation. Human interviewer: follow `human-script.md` (the stems, the leading rule word for word as the AI's guard applies it, and the follow-up rule); press I/E at every change of speaker, press I before you start speaking, tick each stem as you use it, click a segment ID to show it to the expert.
6. **Debrief (5 min).** "Did any question feel like it was putting words in your mouth? Which questions made you think of something you had not said before?"

## After each session

`sessions/` is the only copy of the data. Before leaving the laptop, back the session up, encrypted, to a drive that is not the laptop's. From the repository root:

```
read -rs PROBE_BACKUP_PASSPHRASE && export PROBE_BACKUP_PASSPHRASE
uv run --directory instrument probe-app backup <session-id> --dest /Volumes/<backup-drive>/probe-backups
```

The passphrase lives in a password manager, never in `.env` or any file in the repository (the command does not read `.env`). The command encrypts with `openssl` (AES-256-CBC, PBKDF2), then decrypts the archive to a temporary directory and compares every file's SHA-256 with the session before reporting `decrypted and verified`; no output means no backup. It flushes the archive to the drive first; eject the drive before unplugging it. A warning that the destination shares the laptop's disk means the copy is not a backup. Without a session ID it backs up every session. To restore: `uv run --directory instrument probe-app restore <archive> --out <empty-dir>`, which checks every file against the manifest inside the archive.

## Measured

- The session ran end to end using only the console controls (note every workaround).
- AI latency: median gap between `expert_answer` and the next `probe` event (target under 6 s).
- `probe-code guard-audit` flag rates for both arms, and the rejection summary it prints (`rejected_leading`, `rejected_contract`, `interviewer_refused`, `interviewer_unavailable`, `fallback`, `guard_failed`).
- Leading content, coded blind to arm: `probe-code export-leading` writes every interviewer question of both arms with what the expert had said before it; two coders fill `leading` and `introduced` by the rule in `human-script.md`, and the rate per arm is computed from `key_leading.csv`.
- Transcription errors on physics terms in 5 minutes of audio checked by hand, for both transcribers on the same files: `uv run probe-app transcribe sessions/<id>/audio/think_A1.webm --model scribe_v2` and `--model whisper-1`. Freeze the one with fewer physics-term errors.
- **Success criterion 3:** at least one operation in the think-aloud trace absent from the expert's ordinary explanation. If none, revise the probe script before recruiting.
- Debrief answers.

## Refusals

Claude Opus 5 runs a `reasoning_extraction` safety classifier. It refused every attempt to have Opus 5 role-play the expert (which is why the simulator uses Sonnet 5). A refused interviewer turn becomes a bare stem (`ai_fallback`), which weakens the AI arm. If `interviewer_refused` exceeds about 1 in 10 turns in the pilot, raise it before freezing: the options are rewording the interviewer prompt, a different interviewer model or provider in `models.json`, or an explicit fallback model, and each changes the frozen configuration.

## After the pilots

1. Fill `codebook/v0.md` from the pilot transcripts; two coders try it on one pilot session.
2. Apply the freeze rule of `docs/freeze-baseline.md` (`probe_code.baseline.freeze_decision`) to the pilots' pooled metrics. Adjust `interviewer.effort` in `models.json`, the prompts or the model only as its outcome says, one variable at a time; freeze only on "accept".
3. Drain `docs/lessons.md` with the `implement-ll` skill. After the freeze, prompt fixes cost a new pre-registration. Then `uv run probe-app freeze`, commit `prereg.json` together with the prompts, and list the hashes in the pre-registration. From then on, any edit to the prompts, `models.json` or the model-facing files listed under `model_facing_sha256` in `probe-app hashes` makes the app refuse data sessions.
