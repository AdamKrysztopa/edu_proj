# Lessons — archive

Where drained queue entries land. **One dated section per drain, newest first.** One row per entry.

This file is the entire memory of the loop: a SessionStart hook injects every applied rule below
into every session, so nobody has to open it. That has a consequence for how you write:

> The one-sentence rule must be readable **cold, months later, by someone who was not there.**
> If it needs the original queue entry to make sense, it is not finished.

Nothing here is ever deleted. Reversed entries especially — the chain is the argument.

## Row format

Each drain is a `## YYYY-MM-DD` section containing one table. Rows are parsed by
`scripts/lessons_graph.py` and by the SessionStart hook, so keep the five columns exact:

```markdown
## 2026-01-31 — drain 4

| id | rule | home | commit | edges |
|------|------|------|--------|-------|
| L4.1 | Every check named in prose must have a mechanical counterpart or be deleted. | `.claude/hooks/check_docs.py` | a1b2c3d | moves L2.2 |
| L4.2 | declined: proposed a naming convention nobody could state a failure for. | — | a1b2c3d | — |
```

- **id** — `L<drain>.<n>`, assigned at drain time.
- **rule** — one sentence, imperative, readable cold. `declined: <reason>` for a declined entry.
- **home** — the exact artefact path it landed in, or `—`.
- **commit** — the commit that carried it.
- **edges** — comma-separated `<edge> <id>` pairs, or `—`.

## Edge vocabulary

Closed. Six edges, spelled exactly.

| edge | means | why it is its own edge |
|---|---|---|
| `refines` | narrows or widens a rule without contradicting it | healthy — the rule was right and imprecise |
| `supersedes` | replaces a rule with a better one, same intent | healthy — the old rule stops being live |
| `moves` | same rule, relocated (usually prose → hook) | the expected repair: a rule that was applied and did not bite was in the wrong artefact, not wrong |
| `recurs` | same defect re-learned, after a rule for it existed | a finding about the rule, not a new rule |
| `reverses` | undoes a rule that fired on correct work | legitimate once; twice in a chain is oscillation |
| `caused-by` | this defect exists because of an earlier rule | rarest and most valuable — a rule that bought a problem |

Distinguishing `moves` / `recurs` / `reverses` is the crux. Collapsing them into "we changed our
mind" is what makes oscillation undetectable.

**Two rules that appear to contradict each other are almost always one conditional rule whose
condition nobody wrote down.** Find the condition and record one `supersedes` or `refines` row
naming it. Do not record a flip.

## The oscillation rule

**A `reverses` edge pointing at an entry that itself carries a `reverses` edge is a stop, not an
entry.** What is being held is an unsettled decision wearing a lesson's clothes. It goes to
whatever this project uses for deliberate decisions — a design doc, an ADR, a grilling session —
with the whole chain as its evidence. Answering an oscillation with a third rule continues it.

`scripts/lessons_graph.py` detects this and exits non-zero.

---

## Applied

<!-- Newest drain first. Append a new `## YYYY-MM-DD — drain N` section above the previous one. -->

## 2026-09-28 — drain 6

| id | rule | home | commit | edges |
|------|------|------|--------|-------|
| L6.1 | Every provider call's failure is logged like its success (outcome "api_error", error class, HTTP status, never billed); a transient error retries with backoff before the caller sees `LLMUnavailable`, a non-transient one is logged once and raised immediately, and a stage that skips a unit on failure counts that skip under its own task label so a run's sidecar never hides a silent loss behind `complete: true`. | `docs/architecture/decisions/0007-reconstruction-pipeline.md` | 0f39ed9 | — |
| L6.2 | An invariant enforced by a pydantic validator needs a test that tries every construction path a `Record` offers — `model_copy`, direct construction, deserialisation — not just its constructor, because constructor-only tests show the invariant only where it was already safe. | `residual/tests/test_bypasses.py` | 03c1e44 | — |
| L6.3 | Before any NOW run reconstructs a domain, check it against `REORIENTATION.md` §18.1's Track A exclusion and N3's held-out gold domains; an example domain given in a request is not a vetted choice. | `.claude/agents/methods-critic.md` | — | — |
| L6.4 | A command that reads a sealed key/answer file and also prints something is asked to confirm every branch prints only shape metadata (`type`, `len`, `sorted(keys)`), never the value — a branch that prints the value on one arm and the type on the other is not a type check. | `.claude/hooks/guard-sealed-files.sh` | — | — |
| L6.5 | A rewritten matcher or regex inside a hook is run against every input form the old one covered, not just the new one, before the drain that changed it is archived. | `.claude/skills/implement-ll/SKILL.md` | — | — |
| L6.6 | A freeze of a model-role config captures the whole role object, not a hand-picked subset of its fields; this is checked by `validity-reviewer` specifically because `instrument/tests/test_gates.py` only runs when `instrument/` is edited, and a frozen Track A produces no such edits to trigger it. | `.claude/agents/validity-reviewer.md` | — | moves L3.1 |

Grouping: L6.1 merges the queue's provider-error entry with the already-shipped fix (`0f39ed9`, this checkpoint) and its tests (`reconstruct/tests/test_llm.py::test_backend_retries_429_then_succeeds` and family; `reconstruct/tests/test_e2e_call_stats.py`'s six `failed_calls_by_task` tests); the drain adds the registered, bound decision rule the fix itself did not yet have. L6.2 documents a fix and test suite (`residual/tests/test_bypasses.py`) already in place since N1 review (`03c1e44`), predating this queue entry; nothing new was built, only registered. L6.3 and L6.5 are new checklist/skill amendments with no code to bind. L6.4 is a new hook, fired once on purpose during this drain (asked correctly on a sealed-path+print command, stayed silent on a print with no sealed path and on a sealed-path read with no print) and registered in `.claude/settings.json`'s `PreToolUse`. L6.6 is the graph checker's MOVE-IT finding for L1.7 (re-learned at L2.3 and L3.1): its prior home, `instrument/tests/test_gates.py`, cannot be edited this drain (Track A frozen, off limits) and in any case only runs on an `instrument/` edit, which is exactly what a freeze period has none of — moved to `validity-reviewer`, which fires on data sessions and instrument changes without needing Track A to be mid-edit.

**Constraints this drain:** `instrument/` was not edited (L1.7's move went to an agent doc, not a test); `reconstruct/src` and `residual/src` were not edited — L6.1 and L6.2 bind already-shipped, already-tested behaviour into decision text rather than adding new code checks.

**Graph finding not acted on:** `L1.11` recurred once more (as `L5.3`) — one recurrence, below the MOVE-IT threshold. Watching; a second recurrence after `L5.3`'s move to `methods-critic` would mean that home also failed.

**Fitness check — which of this cycle's defects would a rule already in the archive have caught?** Two of five queue entries were already fully fixed and tested before this drain (`L6.1`'s code fix, `L6.2`'s validator fix) — no archived rule caused either fix; both were caught by ad hoc review (an E-LIVE run's call-count mismatch, a type-design review), which is the gap `L6.1`'s new decision rule and `L6.2`'s registration close by giving each a named, bound home. The other three (`L6.3` sealed-domain check, `L6.4` sealed-file print, `L6.5` matcher-rewrite testing) are new classes with no prior archive coverage — correctly "none" for those three.

## 2026-09-28 — drain 5

| id | rule | home | commit | edges |
|------|------|------|--------|-------|
| L5.1 | A check enumerates everything in its claimed scope and reports, never silently skips, what it cannot resolve or classify (a registered hook whose script is missing, a DOI form it does not parse, a lookup that failed, a route type it filtered out), because a silent skip reads as a clean pass. | `.claude/hooks/check-dois.py` | 2376825 | refines L1.1 |
| L5.2 | Every number in a research document is verified in the source's own text, never against an intermediate note or a summarising tool's output; a number found only there is reported as unresolvable. | `.claude/agents/citation-verifier.md` | 2376825 | refines L2.1 |
| L5.3 | Every research plan names at least one evidence route the project can reach now; if every gate waits on people or data it does not have, revise the plan before building anything. | `.claude/agents/methods-critic.md` | 2376825 | recurs L1.11 |

Grouping: L5.1 merges three queue entries: the route-surface test that filtered by route type (instance already fixed by `test_only_expert_routes_answer_a_network_client`), the settings hook pointing at a deleted `check-dois.sh`, and the DOI hook ignoring `doi:` citations. Its second home is `.claude/hooks/session_start_lessons.py`, which warns at session start when a registered hook cannot run; both homes were fired on purpose once. L5.2 merges the fabricated fetch-summary figure with the grain errors found in `REORIENTATION.md`. L5.3 is the reorientation's drift diagnosis.

**Graph finding carried, not acted on:** the checker still reports L1.7 as a recurrence whose `moves` did not go far enough. L1.7 guards the Track A freeze, and Track A is frozen with no `probe-app freeze` scheduled. Re-route it when Track A resumes, before its freeze.

**Fitness check — which of this cycle's defects would a rule already in the archive have caught?** Two, both applied. L2.1 (citation-verifier) caught the synthesis grain errors at review, which is where its home puts it; a writer told the rule still made them, so L5.2 sharpens the verifier rather than moving it. L1.11 (`/branch` skill) named "an instrument is not progress", yet the plan kept waiting on people; L5.3 moves the check to `methods-critic`, which runs on every plan. L1.1 was disabled by the dead hook path, which is L5.1's class.


## 2026-09-28 — drain 4

| id | rule | home | commit | edges |
|------|------|------|--------|-------|
| L4.1 | Never measure or compare anything with a classifier on items it already filtered: sample upstream of it, never use it as the outcome for the arm it gates, and assign item IDs after shuffling. | `instrument/tests/test_calibration.py` | 8f4d110 | — |
| L4.2 | Material of unknown status is decided twice: it may be kept off blinded coder sheets, but it stays in the key and audit denominators under its own source. | `.claude/agents/validity-reviewer.md` | 8f4d110 | refines L3.2 |
| L4.3 | Every read of stored audio has a test injecting a storage failure (a file or bytes missing after acknowledgement) as well as the transport failures. | `instrument/tests/test_streams.py` | 8f4d110 | refines L1.6 |

**Fitness check — which of this cycle's defects would a rule already in the archive have caught?** One, and it was applied too narrowly: L1.6 listed transport failures only, so a missing part file passed two validity reviews; L4.3 widens it and puts it in the invariant tests. The other two are new classes.


## 2026-09-28 — drain 3

| id | rule | home | commit | edges |
|------|------|------|--------|-------|
| L3.1 | Code that implements a registered rule carries each registered number as a constant that a test checks against the registered text, so a draft cannot drift from it. | `instrument/tests/test_registered.py` | 4eafdd0 | recurs L2.3, moves L1.7 |
| L3.2 | An item excluded from a coder's sheet stays in the key with a preset label, and a test asserts each arm's denominator is unchanged by the exclusion. | `.claude/agents/validity-reviewer.md` | 4eafdd0 | — |
| L3.3 | Re-check a time limit against the live clock after every slow call and before any state change, and test it with a clock that advances inside the fake call. | `.claude/agents/validity-reviewer.md` | 4eafdd0 | — |
| L3.4 | In a comparative study, freeze whatever produces each arm's data, arm by arm; every probe_app module is either frozen or in a pinned exemption list. | `instrument/tests/test_gates.py` | 4eafdd0 | refines L1.9 |
| L3.5 | A "written and verified" claim for data that must survive a device leaving syncs to stable storage (F_FULLFSYNC on macOS) before the verification read. | `.claude/agents/validity-reviewer.md` | 4eafdd0 | — |
| L3.6 | Every reliability statistic validates labels against the codebook's code list and reports how many units it dropped. | `.claude/agents/validity-reviewer.md` | 4eafdd0 | — |

**Fitness check — which of this cycle's defects would a rule already in the archive have caught?** One, and it was applied: L2.3 (registered constraints) sat in `methods-critic`, which caught the M1 draft only after drafting. L3.1 moves the numeric part of that rule into a test that runs at every edit; the non-numeric part stays with the reviewer. L1.9 (freeze by data flow) was applied and still produced an AI-only freeze scope; L3.4 makes the scope a ratchet.


## 2026-09-28 — drain 2

| id | rule | home | commit | edges |
|------|------|------|--------|-------|
| L2.1 | When a synthesis condenses graded evidence, every claim keeps its rating word, domain, timing, grain (item vs total, cohort vs individual) and comparison exactly as its source card states them. | `.claude/agents/citation-verifier.md` | d90df2a | — |
| L2.2 | No tool call from any agent may carry the user's email address; the hook denies it at the point the request leaves, because polite-pool APIs invite an email and subagents fill it in. | `.claude/hooks/guard-user-email.sh` | d90df2a | — |
| L2.3 | When a plan reuses a registered or reviewed study, trace each of its registered rules (arm matching, gates and failure branches, instruments, sampling units, delays) into the plan before adding anything; additions stay secondary. | `.claude/agents/methods-critic.md` | d90df2a | recurs L1.7 |

**Fitness check — which of this cycle's defects would a rule already in the archive have caught?** One, applied in the wrong form. L1.7's queue entry generalised to "trace every spec field into the plan", but drain 1 archived only its structural instance (freeze whole role objects), leaving the planning class open; the roadmap then dropped the registered Stage B constraints (L2.3). L2.3 re-routes the planning rule to the reviewer that runs on every study design.


## 2026-09-28 — drain 1

| id | rule | home | commit | edges |
|------|------|------|--------|-------|
| L1.1 | A citation check must confirm each DOI resolves to the work its line cites (first author or title words), not merely that doi.org answers. | `.claude/hooks/check-dois.py` | be141a2 | — |
| L1.2 | Keep every generated artefact (bytecode, caches, venvs) untracked and gitignored, because the data-session clean-tree gate treats any tracked change as dirty. | `instrument/tests/test_gates.py` | be141a2 | — |
| L1.3 | A change to a model, prompt or anything a live model or transcriber sees is not done until a live run passes, because the fakes never refuse. | `.claude/hooks/live-smoke-reminder.sh` | be141a2 | — |
| L1.4 | Never bulk-stage with `git add -A` or `.` while an untracked directory holds its own repository; gitignore a tool's generated directory when the tool first creates it. | `.claude/hooks/guard-nested-repo.sh` | be141a2 | refines L1.2 |
| L1.5 | Fix a codebook's labels-per-unit rule together with the agreement statistic that consumes it, and dry-run export plus coding before coders see it. | `.claude/agents/codebook-stress-tester.md` | be141a2 | — |
| L1.6 | For each recording-transport failure (missing stream, refused, dropped or out-of-order chunk) a test must inject it and assert the console sees it; a simulator that delivers audio whole reports green over data loss. | `.claude/agents/validity-reviewer.md` | be141a2 | refines L1.3 |
| L1.7 | Freeze whole model-role objects rather than hand-picked fields, so a field a plan leaves out cannot escape pre-registration. | `instrument/tests/test_gates.py` | be141a2 | — |
| L1.8 | Every CLI subcommand must be run through `main()` by a test so a changed dependency signature fails the suite; the `UNRUN` waiver only shrinks. | `instrument/tests/test_gates.py` | be141a2 | refines L1.3 |
| L1.9 | Define a freeze by data flow: hash everything that reaches the model or decides what reaches the participant, whether it lives in a prompt file or in code. | `.claude/agents/validity-reviewer.md` | be141a2 | — |
| L1.10 | Never hand the user a step involving the app before running that exact step end to end in a browser with Playwright; a `curl` status code is not the check. | `CLAUDE.md` | be141a2 | — |
| L1.11 | A built instrument or designed study is preparation, not progress on a research phase: after editing the map, re-check `PROGRESS.md`'s NEXT against map §9 and fix every copy of a changed requirement. | `.claude/skills/branch/SKILL.md` | be141a2 | — |
| L1.12 | Choosing an evidence-informed route is separate from proving it works: schedule validation that needs software after the build milestone it depends on. | `CLAUDE.md` | a540281 | refines L1.11 |

**Fitness check — which of this cycle's defects would a rule already in the archive have caught?** None: this is the first drain and the archive was empty.

Concrete defects split off as work items in `PROGRESS.md` (L1.5, L1.8, L1.9). Already fixed in code before this drain: the empty-stream and chunk-retry paths (L1.6), the dropped `effort`/`temperature` freeze fields (L1.7), the tracked bytecode (L1.2).
