# Pilot protocol: Stage A session app

**Purpose.** Check that the instrument runs a full session and build codebook v0. Pilot sessions are never Stage A data.

**Participants.** One or two physicists who have taught first-year mechanics. Not eligible for Stage A afterwards.

## Before the session

1. Ethics: pilot consent form names ElevenLabs and OpenAI (audio) and Anthropic (transcripts, written-work images) as processors; data-processing terms and retention settings confirmed for all three accounts. Stage A consent names only the transcriber that is frozen.
2. Keys in `instrument/.env` (`ANTHROPIC_API_KEY`, `ELEVEN_LABS_API_KEY`, `OPENAI_API_KEY`); never committed.
3. Tablet over the network needs HTTPS: `mkcert -install && mkcert <laptop-LAN-IP>`, install the mkcert root CA on the tablet, then
   `uv run probe-app serve --host 0.0.0.0 --ssl-certfile <ip>.pem --ssl-keyfile <ip>-key.pem`.
   In person on the laptop itself: `uv run probe-app serve` and use `http://127.0.0.1:8000`.
4. A physicist checks the four problems in `problems/problems.json`.
5. `uv run probe-app simulate` once; confirm the simulated session completes and check `interviewer_failed` in its events (see "Refusals" below).
6. Dry run with a colleague on the real tablet and microphone: the automated browser check replaced the microphone with a synthetic stream.

## Session (about 75 minutes)

1. Consent (5 min).
2. **Ordinary explanation (10 min, paper).** "Write a worked explanation of these two problems for a first-year student": one problem from set A, one from set B, not used later. Scan it into `sessions/<id>/explanation/`.
3. **Think-aloud (about 20 min).** Console: create a pilot session, give the expert the link, press "Start next problem" for each of the four problems. Instructions only: "Solve it and say everything you are thinking, including anything that feels obvious." The only allowed prompt is "Keep talking" (console button) after about 10 s of silence. Do not reload the expert page during a problem: the audio recorded so far would be lost.
4. **Trace review (5 min, researcher only).** Correct transcription errors in physics terms; do not add content.
5. **Probe session, set 1 (up to 20 min)** and **set 2 (up to 20 min)**: AI on one set, human on the other, as chosen at creation. Human interviewer: press I/E at every change of speaker, press I before you start speaking, tick each stem as you use it, click a segment ID to show it to the expert, at most one follow-up per stem question and only restating the expert's words.
6. **Debrief (5 min).** "Did any question feel like it was putting words in your mouth? Which questions made you think of something you had not said before?"

## Measured

- The session ran end to end using only the console controls (note every workaround).
- AI latency: median gap between `expert_answer` and the next `probe` event (target under 6 s).
- `probe-code guard-audit` flag rates for both arms, and the rejection summary it prints (`rejected_leading`, `rejected_contract`, `interviewer_failed`, `fallback`).
- Transcription errors on physics terms in 5 minutes of audio checked by hand, for both transcribers on the same files: `uv run probe-app transcribe sessions/<id>/audio/think_A1.webm --model scribe_v2` and `--model whisper-1`. Freeze the one with fewer physics-term errors.
- **Success criterion 3:** at least one operation in the think-aloud trace absent from the expert's ordinary explanation. If none, revise the probe script before recruiting.
- Debrief answers.

## Refusals

Claude Opus 5 runs a `reasoning_extraction` safety classifier. It refused every attempt to have Opus 5 role-play the expert (which is why the simulator uses Sonnet 5). A refused interviewer turn becomes a bare stem (`ai_fallback`), which weakens the AI arm. If `interviewer_failed` exceeds about 1 in 10 turns in the pilot, raise it before freezing: the options are rewording the interviewer prompt, a different interviewer model, or an explicit fallback model, and each changes the frozen configuration.

## After the pilots

1. Fill `codebook/v0.md` from the pilot transcripts; two coders try it on one pilot session.
2. Adjust `INTERVIEWER_EFFORT` and the prompts if the pilots require it.
3. Drain `docs/lessons.md` with the `implement-ll` skill. After the freeze, prompt fixes cost a new pre-registration. Then `uv run probe-app freeze`, commit `prereg.json` together with the prompts, and list the hashes in the pre-registration. From then on, any prompt edit makes the app refuse data sessions.
