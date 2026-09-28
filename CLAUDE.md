# edu_proj

Research on how AI can elicit hidden expert knowledge, diagnose learner bottlenecks, and turn those gaps into effective instruction. Physics is the initial setting; transfer across disciplines remains part of the question.
`ai_education_research_map.md` is the single source of state; `PROGRESS.md` tracks work against it; `research/` holds one note per branch.

## Current priority and scope

The route is chosen: `research/roadmap.md` (steps 3–6; steps 1–2 in `research/route-comparison.md` and `research/decision-gaps.md`). Implement it milestone by milestone: M1 (early K0) and M2 (elicitation tool and pilot) first, in parallel. Each milestone ends in a continue/change/stop decision; do not start a milestone whose gate has not passed. Keep assumptions A1–A10 visibly untested until their milestone runs. The first version is static: no live LLM faces learners, diagnosis is cohort-level, and a simple mastery rule stands in for knowledge tracing.

The prepared study's registered rules (K0, K1, K2, Stage B arm matching, the 2–3-week delay) are used unchanged; roadmap additions are secondary and cannot change what a registered rule decides. Frontend work follows the workflow's actual usability needs.

Reading: `research/minimum-reading.md` is the entire minimum. All books, papers and branch notes are optional extras, never a prerequisite checklist for the user.

## Prepared experiment branch

Design: `research/experiment-ai-assisted-cta-physics.md`. Each gate can stop the study.
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

`uv run --directory instrument pytest -q` (246 tests, about 6 s); a PostToolUse hook runs it after edits under `instrument/`.
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

Never hand the user a step that involves the app (commands, URLs, certificates, microphone) before running that exact step end to end in a browser with the Playwright MCP; hand over only what passed.
