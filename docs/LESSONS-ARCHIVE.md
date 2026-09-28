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
