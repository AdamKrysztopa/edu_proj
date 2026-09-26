# edu_proj

Research on eliciting the hidden reasoning of expert physicists and testing whether teaching it improves novice transfer (topic: selecting and combining conservation principles in first-year mechanics).
`ai_education_research_map.md` is the single source of state; `PROGRESS.md` tracks work against it; `research/` holds one note per branch.

## The experiment

Design: `research/experiment-ai-assisted-cta-physics.md`. Each gate can stop the study.
- **K0**: code about 100 past exam errors; stop if under 30% are principle selection or representation. Waiting on exam data from the user.
- **Stage A** (within-expert, 12 physicists): ordinary explanation, think-aloud solving, then retrospective probes by an AI and a human interviewer on counterbalanced problem sets. Operations are coded blind and corroborated against the trace. Instrument: `instrument/` (`probe-app` session app, `probe-code` coding pipeline).
- **K1**: at least 3 new shared operations, at least 2 of them AI-probe-added, and the AI-minus-human contradicted-rate CI bound at most 15 pp.
- **Stage B**: two-arm RCT, about 370 first-year students, delayed transfer; a futility test at d = 0.30.
- **K2**: kill if the effect is below that SESOI, valid only with at least 70% compliance per arm.

Now: the instrument is built; next are 1–2 pilot physicists per `instrument/pilot-protocol.md`, then `probe-app freeze`.

## Off limits

- `instrument/.env`: API keys; the app loads it itself. `guard-secrets` denies any tool call that names a `.env`.
- `instrument/prompts/`: frozen once `instrument/prereg.json` exists (not yet); an edit invalidates every data session until a re-freeze and a new pre-registration. `guard-frozen-prompts` asks first.
- `sessions/`, `instrument/sessions/`: study data, git-ignored and not backed up; only the app writes there, corrections go through the console's trace review. `guard-session-data` denies file writes and asks before destructive Bash.
- `research/pdf/`: copyrighted PDFs, git-ignored; never commit them.

## Tests

`uv run --directory instrument pytest -q` (131 tests, about 2 s); a PostToolUse hook runs it after edits under `instrument/`.
The fakes never refuse, so live transcribers and interviewer refusals are checked only by `/preflight`, never by the tests.

## Agents

- `citation-verifier`: after writing or editing the map or anything in `research/`; checks each citation resolves and supports its claim.
- `methods-critic`: before committing to any study design, and at the end of `/branch experiment`.
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
