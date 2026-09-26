# Stage A session app and coding pipeline: design

**Purpose.** Build the Stage A instrument from `research/experiment-ai-assisted-cta-physics.md`: a local web app that records an expert's think-aloud solution and then runs the retrospective probe session (AI-led or human-led) over that trace, plus the CLI that turns sessions into blinded coding material. Pilot it on 1–2 physicists; the pilots build codebook v0.

**Success.**
1. The app runs a full session (think-aloud on two problems, then a capped probe session) with the researcher touching only the defined console controls.
2. The frozen configuration is enforced: the app refuses to start a data session whose prompt or stem hashes differ from the pre-registered values.
3. For each pilot expert, at least one operation is visible in the think-aloud trace and absent from their ordinary written explanation. If not, the probe script is revised before recruitment.
4. The pipeline produces a blinded coder sheet with no interviewer text, a trace-only sheet with no probe material, and a corroboration sheet with decoys, and computes the agreement statistics the design names.

**Out of scope.** K0 exam-error coding; the Stage B module; the ordinary written explanation (session step 1), which experts write on paper before the app session; the decoding interview.

## Decisions taken

- Web app, served from the researcher's laptop; the expert uses a tablet on the same network, or the laptop in person.
- Experts speak their answers; audio is transcribed by a cloud speech-to-text service. Probe text is shown on screen, not spoken.
- The app covers the think-aloud and the probe session.
- The AI interviewer is a free conversation inside a contract that code enforces (section 3).
- The coding pipeline is part of this spec.

## 1. Stack and layout

- Python 3.12, `uv`, FastAPI + uvicorn. Both screens poll session state once a second; on a LAN this is simpler than a WebSocket and loses nothing.
- Served over HTTPS (a locally trusted certificate, e.g. `mkcert`) when the tablet connects over the network: browsers grant microphone access only on HTTPS or `localhost`.
- Frontend: static HTML and plain JavaScript, no build step. Canvas with pointer events for drawing; `MediaRecorder` for audio (webm/opus).
- Claude via the official `anthropic` Python SDK; structured output via `output_config.format` / `messages.parse` with Pydantic models.
- Transcription behind a `Transcriber` interface. Default: OpenAI `whisper-1` with `verbose_json` segment timestamps and a physics vocabulary prompt. The model ID is pinned in config and logged. Segment timestamps are a hard requirement for any replacement.

```
instrument/
  pyproject.toml
  src/probe_app/        server, session state machine, interviewer engine, transcriber, storage
  src/probe_code/       coding-pipeline CLI
  web/                  expert.html, console.html, js/, css/
  prompts/              interviewer system prompt, stems, guard prompt (hashed)
  problems/             pilot problem sets A and B
  codebook/v0.md
  pilot-protocol.md
  tests/
sessions/               one directory per session; git-ignored (personal data)
```

## 2. Session flow

**Console (researcher, localhost).** Create a session: pseudonymous expert ID, counterbalancing cell (interviewer × problem set × order, from the 4 × 3 table), arm per problem set. Controls: start, "keep talking" (the only think-aloud prompt the design allows), pause/resume, end. Shows elapsed time, stem coverage and every event as it is logged.

**Expert view (tablet).**
1. *Think-aloud*, per problem: problem statement, drawing canvas, continuous recording. Nothing else is shown.
2. *Trace build*: after each problem, audio is transcribed; strokes and transcript segments share one session clock. The researcher may correct transcription errors in the console; every correction is stored as a diff and both arms see the corrected trace.
3. *Probe session*, per problem set, 20-minute cap:
   - **AI arm.** Loop: interviewer turn (section 3) → probe text shown, with its anchor highlighted (a transcript excerpt or a region of the canvas snapshot) → the expert presses to talk and presses again to finish → transcription → next turn.
   - **Human arm.** The human interviewer asks aloud. Their console shows the trace, the stem checklist, the timer and a turn button ("interviewer" / "expert") that segments the audio. They can push the same anchor highlight to the expert's screen. Turn format in the log is identical to the AI arm's.

## 3. Interviewer engine (AI arm)

The LLM words each question and chooses stem order and anchors. Each turn it returns:

```
InterviewerTurn { utterance, stem_id, problem_id, anchor: {kind: segments | canvas | none, segment_ids[]}, is_followup, quoted_span | null, end_session }
```

Code checks the turn before the expert sees it:
- **Stems.** `stem_id` ∈ {cues, alternatives, checks, anomalies, novice_miss}. Every stem must be used at least once per problem. The model may end the session (`end_session`) only once that coverage is complete; otherwise the cap ends it and the missing coverage is logged. A canvas anchor highlights the whole snapshot of that problem.
- **Follow-ups.** At most one, immediately after the stem question it belongs to. A follow-up must carry `quoted_span`, which must occur in the expert's words (think-aloud or answers so far), compared after lower-casing and removing punctuation.
- **Rejections.** A turn that breaks the contract or is flagged by the guard is regenerated once, with the reason given to the model; a second rejection falls back to the next unused stem, shown bare.
- **Leading-question guard.** A second call (`claude-haiku-4-5`, temperature 0) returns whether the utterance names a physics operation, quantity relation or strategy the expert has not said. Flagged turns are regenerated once; a second flag falls back to the bare stem text.
- **Cap.** From 18 minutes each request tells the model to close; at 20 minutes code ends the probe session. Each turn is a single stateless request (trace, then the dialogue so far), so nothing depends on carrying the model's earlier thinking between turns.
- **Rejected or failed turns** are never shown to the expert; they are logged with the reason.

**Model and frozen configuration.** Interviewer: `claude-opus-5`, adaptive thinking, fixed `effort` (set during piloting, then frozen). Current Opus models reject `temperature`, so the frozen configuration is model ID + effort + SHA-256 of the system prompt, stem file and guard prompt, recorded in the session manifest. Outputs are not reproducible by re-running; every request and response is logged in full so the session is reproducible from the log. Server-side model fallbacks are **not** enabled, because they would substitute another model silently; a refusal is logged and the turn falls back to the bare stem.

**Context sent per turn.** Frozen system prompt; problem statements; transcript segments with IDs and timestamps; the final canvas PNG per problem (this static part is prompt-cached); then the probe dialogue so far, time remaining and unused stems.

## 4. Storage

`sessions/<session_id>/`:
- `manifest.json`: expert pseudonym, counterbalancing cell, app git commit, model IDs, effort, prompt/stem/guard hashes, transcriber model.
- `events.jsonl`: append-only; every event with a monotonic and a wall-clock timestamp.
- `audio/`, `canvas/strokes.jsonl`, `canvas/snapshots/`, `transcripts/` (raw and corrected, with diffs), `llm/` (every request and response).

Names never enter the repo; the pseudonym key is kept outside it.

## 5. Coding pipeline (`probe-code`)

- `export-blind`: removes interviewer turns, segments expert utterances into units (transcript segment, then sentence), assigns random unit and session IDs; the key file is written separately. Output: coder CSV.
- `export-trace`: think-aloud transcript and canvas only, no probe material, for the trace-only coder.
- `corroboration-sheet`: each probe-added operation mixed 1:1 with decoys sampled from other experts and other problems, shuffled; the answer key is separate.
- `agreement`: Krippendorff's α on unit-level operation presence and type over the fixed segmentation (full unitizing α_u is not implemented in v0), Cohen's κ for status tags and for cross-expert matching, the decoy false-corroboration rate, and the condition-guess rate for the blinding check.
- `guard-audit`: runs the leading-question guard over the human arm's transcribed turns after the session, so both arms report a comparable flag rate.

`codebook/v0.md` starts from the nine types of the map's §9 Phase 1 taxonomy and the four status tags (trace-only, probe-added performed, reported only, contradicted). The pilots fill it with definitions and examples.

## 6. Pilot protocol (`pilot-protocol.md`)

1–2 physicists who have taught first-year mechanics. Four pilot problems in two sets on selecting and combining conservation principles (for example a collision followed by motion up a ramp; a ballistic pendulum), drafted here and checked by a physicist. Sequence: consent → written ordinary explanation on paper → think-aloud in the app → probe session (AI on one set, human on the other) → short debrief on how natural the probes felt.

Measured: whether the session ran without intervention, AI turn latency (target median under 6 s), guard flag rate, transcription errors on physics terms (5 minutes checked by hand per session), success criterion 3, and the debrief. Pilot sessions are codebook material and are never counted as Stage A data.

## 7. Errors

- Transcription failure: retry twice; then the researcher types the segment or answer in the console (logged). A failed answer is not passed to the interviewer until it has been typed. An answer that transcribes to nothing (silence) is passed on as empty.
- API failure or refusal: retry with backoff; then the next unused stem is shown bare (logged).
- Tablet disconnect: state lives on the server; the expert view resumes where it stopped. The cap timer runs unless the researcher pauses, and pauses are logged.

## 8. Testing

- Engine contract, with a scripted fake LLM: invalid stem rejected, second follow-up rejected, quoted span not in transcript rejected, guard double-flag falls back to bare stem, cap enforced at 20 minutes, wrap-up message at 18.
- Refuses to start when a hash differs from the pre-registered value.
- Trace alignment: strokes and segments on one clock.
- Pipeline on synthetic sessions: blinded export contains no interviewer text; trace export contains no probe material; decoy key is not in the coder sheet; agreement statistics match hand-computed values on a toy set.
- `--simulate-expert` mode: an LLM plays the expert for end-to-end smoke tests. Sessions it produces are marked simulated and rejected by the pipeline.

## 9. Ethics and data

The consent form names both processors: OpenAI receives audio, Anthropic receives transcripts and canvas images. Both need a data-processing agreement and retention settings acceptable to the ethics board before any real session. Pseudonymous IDs only; `sessions/` is git-ignored.

## 10. Changes to the experiment design

`research/experiment-ai-assisted-cta-physics.md` Stage A: "the model, prompt and temperature are frozen" becomes "model ID, effort setting and prompt hashes are frozen", with the note that outputs are logged in full because sampling cannot be fixed on current models. The follow-up rule adds the verbatim-quote check. The human interviewer runs the same console.
