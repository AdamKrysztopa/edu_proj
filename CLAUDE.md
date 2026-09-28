# edu_proj

Research on how AI can recover the knowledge experts leave unsaid, diagnose learner bottlenecks, and turn those gaps into instruction, in education and inside organisations. The domain is universal; physics is one benchmark domain and the setting of the frozen Validation Track A.
`REORIENTATION.md` is the strategic plan (adopted 2026-09-28); `ai_education_research_map.md` holds the graded evidence; `PROGRESS.md` tracks work against both; `research/` holds one note per branch and `research_notes/` the evidence notes behind the reorientation (raw; `REORIENTATION.md` wins where they differ).

## Current priority and scope

The route is `REORIENTATION.md` §22: the NOW programme, items N0–N9. NOW uses zero participants, zero proprietary data, zero microphones and zero live expert interviews; its one human input is one blind second coder (labelling, not participation). The central question is whether a reconstruction from public and organisational evidence, plus a gap map, predicts where the human knowledge residual lies (RQ-B). N3 (E-CTA and E-OSS) is the critical path, and its stop rule is pre-registered before any gold is acquired. Every NOW item ends in a continue/change/stop decision that reads an experiment result, not a build. Fill in the threshold table before acquiring gold.

Evidence labels are first-class: observed human evidence, literature-supported, organisational-artefact-supported, inferred, synthetic extrapolation, unknown. Synthetic output may be a predictor, never a criterion, and never feeds a gate. Reuse Track A components by copying them into the domain-neutral package `residual/` (decision 0006); nothing under `instrument/` changes.

Reading: `REORIENTATION.md` §1 is the entire minimum. §25, all books, papers and notes are optional extras, never a prerequisite checklist for the user.

## Validation Track A — Physics / Human Expert Elicitation (frozen)

Frozen as a unit, not retired. It starts only on its own registered preconditions (experts, a course, ethics), independent of the NOW programme; its registered rules (K0, K1, K2, Stage B arm matching, the 2–3-week delay) are used unchanged, and additions stay secondary and cannot change what a registered rule decides. Anyone who has seen reconstructed conservation content is ineligible for a Track A human role (`REORIENTATION.md` §18.1).

Design: `research/experiment-ai-assisted-cta-physics.md`; plan: `research/roadmap.md` (M1–M8, assumptions A1–A10 untested). Each gate can stop the study.
- **Stage A** (within-expert, 12 physicists): ordinary explanation, think-aloud solving, then retrospective probes by an AI and a human interviewer on counterbalanced problem sets. Operations are coded blind and corroborated against the trace. Instrument: `instrument/` (`probe-app` session app, `probe-code` coding pipeline).
- **K1**: at least 3 new shared operations, at least 2 of them AI-probe-added, and the AI-minus-human contradicted-rate CI bound at most 15 pp.
- **K0**: no past exam scripts exist, so about 100 errors are coded on open-response conservation problems in the Stage B pretest; stop Stage B if under 30% are principle selection or representation. Early K0 runs the same items as a quiz in an earlier offering and can stop the study before the 12 experts.
- **Stage B**: two-arm RCT, about 370 first-year students, delayed transfer; a futility test at d = 0.30.
- **K2**: kill if the effect is below that SESOI, valid only with at least 70% compliance per arm.

The instrument is built. Stage A is roadmap M4 and Stage B is M6; the pilot and its pre-pilot items are M2, and `probe-app freeze` gates M4.

## Off limits

- `instrument/.env`: API keys; the app loads it itself. `guard-secrets` denies any tool call that names a `.env`.
- `instrument/prompts/`: frozen once `instrument/prereg.json` exists (not yet); an edit invalidates every data session until a re-freeze and a new pre-registration. `guard-frozen-prompts` asks first.
- `sessions/`, `instrument/sessions/`: study data, git-ignored; back up after every session with `probe-app backup` (encrypted, passphrase from `PROBE_BACKUP_PASSPHRASE`); only the app writes there, corrections go through the console's trace review. `guard-session-data` denies file writes and asks before destructive Bash.
- `research/pdf/`: copyrighted PDFs, git-ignored; never commit them.

## Tests

`uv run --directory instrument pytest -q` (311 tests, about 7 s); a PostToolUse hook runs it after edits under `instrument/`.
`uv run --directory residual pytest -q` (the NOW package, about 1 s); a PostToolUse hook runs it after edits under `residual/`. `residual/frozen/n1.json` freezes the N1 schema, feature set and label code: a change needs a deliberate re-freeze (`uv run --directory residual python -m residual.freeze --write`) and a commit saying why (decision 0006).
`uv run --directory reconstruct pytest -q` (the N2 package; offline); a PostToolUse hook runs it after edits under `reconstruct/`. A live run is only `python -m reconstruct.run --live` with a hard `--max-usd`, never inside tests.
`python3 scripts/hook_tests/test_check_dois.py` proves the DOI hook fires; run it after any hook edit.
The fakes never refuse, so live transcribers and interviewer refusals are checked only by `/preflight`, never by the tests.

## Agents

- `citation-verifier`: after writing or editing the map, `REORIENTATION.md` or anything in `research/`; checks each citation resolves and supports its claim against the source, not against intermediate notes.
- `methods-critic`: before committing to any study design or NOW pre-registration, and at the end of `/branch experiment`.
- `validity-reviewer`: after any change under `instrument/src`, `instrument/web` or `instrument/prompts`, and before a data session.
- `codebook-stress-tester`: before a pilot or after a codebook edit; applies `instrument/codebook/v0.md` to simulated exports and flags overlapping, unused or low-confidence codes. Never a coder of record.

## Skills

- `/branch explore|compare|falsify|experiment`: to investigate one branch of the map; updates it only where evidence justifies.
- `/elicit`: to run a DtD/CDM interview with one expert on one problem (RQ1 pilot).
- `/session-report <session-dir>`: after a Stage A session, summarised against the pilot protocol's measures.
- `/preflight pilot|data`: go/no-go before every pilot or data session.
- `lessons`: the moment a mistake is caught; capture only.
- `implement-ll`: at a checkpoint (work item closing, queue non-empty, before `probe-app freeze`); drains the queue into `docs/LESSONS-ARCHIVE.md`.

## Definition of done

A task isn't done while a mistake caught during it is uncaptured: record it with `lessons` in `docs/lessons.md`; `implement-ll` drains the queue before `probe-app freeze`.

Never hand the user a step that involves the app (commands, URLs, certificates, microphone) before running that exact step end to end in a browser with the Playwright MCP; hand over only what passed.
