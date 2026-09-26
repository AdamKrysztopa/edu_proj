# Lessons — queue

A **queue, not an archive**. Empty is the healthy state. An entry's job is to survive the hours
between the mistake and the next drain — not to be permanent.

Write an entry **at the moment the mistake is caught**, not at the end of the session. By the end
the bug is fixed, the diff looks clean, and the only trace is a correction nobody can reconstruct
into a rule.

**Nothing is carried across two drains.** An entry that survives one drain is an entry nobody
intends to implement, and a queue with permanent residents stops being read. Either implement it,
or decline it in the archive with the reason.

Entries are drained by the `implement-ll` skill and land in `LESSONS-ARCHIVE.md`. Ids (`L<drain>.<n>`)
are assigned at drain time — don't number entries here.

## Entry format

```markdown
### <short title>

- **What happened:** the specific fact, with `path:line` or a quotation. Include *how it was
  caught* — that is frequently the real finding.
- **Generalises to:** one sentence, stated as a rule someone could follow.
- **Candidate home:** a suggestion, explicitly not a decision.
```

`Generalises to` is the filter. If the entry cannot be written as a rule someone could follow, it
is an anecdote and does not belong in the queue.

There is no status field. Presence in this queue is the status.

## What is not a lesson

- A typo.
- A one-off misreading with no general shape.
- A decision that was correctly argued and went the other way.

A queue padded with those is a queue nobody drains.

---

## Open

<!-- Append entries below. After a drain this section is empty again. -->

### DOI hook passed a DOI that resolves to the wrong book

- **What happened:** the Crandall, Klein & Hoffman (2006) DOI in the map's §14 was
  `10.7551/mitpress/7301.001.0001`, which resolves to "Workflow Management", not *Working Minds*
  (`research/explore-cognitive-task-analysis.md:89`). `.claude/hooks/check-dois.sh` passed it,
  because it only checks that doi.org answers 30x. It was caught by hand during the CTA `explore`
  branch, when the DOI was looked up in OpenAlex.
- **Generalises to:** a citation check must confirm that the DOI resolves to the cited work
  (title and year), not just that it resolves.
- **Candidate home:** `check-dois.sh`, via an OpenAlex title lookup against the text of the
  citing line; failing that, the `citation-verifier` agent's checklist.

### Tracked bytecode made the clean-tree gate refuse after every test run

- **What happened:** `git_dirty()` (`instrument/src/probe_app/config.py:84`) refuses data
  sessions whenever `git status --porcelain -- .` is non-empty. Tracked `__pycache__/*.pyc` files
  changed on every pytest run, so the gate tripped on a tree with no real edits. It was caught by
  using the app after a test run, not by the tests, and fixed in `44d8751`.
- **Generalises to:** a gate that refuses a dirty tree needs every generated artefact
  gitignored, plus a test that runs the suite and then asserts the gate still passes.
- **Candidate home:** a test in `instrument/tests/test_config.py`, or the `/preflight` gate still
  open in `PROGRESS.md`.

### Model switch broke the simulator in a way the fakes could not show

- **What happened:** Opus 5 refuses the SimulatedExpert role-play prompt under
  `reasoning_extraction`, while Sonnet 5 accepts it (`098eaee`). The test suite runs on
  `instrument/tests/fakes.py`, which never refuses, so this surfaced only in a live simulation run.
- **Generalises to:** a change of model or prompt for any LLM role counts as done only after a
  live smoke run, because fakes cannot reproduce refusals.
- **Candidate home:** the `/preflight` gate open in `PROGRESS.md`, or `validity-reviewer`'s
  checklist for changes under `instrument/prompts` and `instrument/src/probe_app/llm.py`.

### "Commit all" nearly embedded a live git worktree

- **What happened:** `.claude/worktrees/agent-af767b3ce661b0b17` (branch `infra-finalize`),
  created by an isolated agent run on Sep 25, stayed untracked and unignored. A `git add -A` for
  "commit all" would have committed it as a nested repository. It was caught by running
  `git worktree list` before staging, and is now ignored (`5488d81`).
- **Generalises to:** a directory a tool generates (agent worktrees, caches, venvs) is gitignored
  when the tool first creates it, not when someone first tries to commit around it.
- **Candidate home:** likely the same fix as the bytecode entry above; a PreToolUse hook that
  refuses `git add -A` while an untracked directory contains `.git`.

### Codebook allows several codes per unit; the agreement tools read one

- **What happened:** `instrument/codebook/v0.md` says a unit may carry zero, one or several
  operations, but `probe-code alpha`/`kappa` read one label per `unit_id`
  (`instrument/src/probe_code/cli.py`, `_labels`). It was caught by the `codebook-stress-tester`
  agent's dry run on `SIM-2980899a` before any coder had used the codebook. The same run also
  found that trace units are undefined, that "Omitted prerequisite" can't be coded from a unit
  alone, and that the Include/Exclude cells are empty.
- **Generalises to:** a codebook's unit and label structure is fixed together with the agreement
  statistic that will consume it, and a dry export plus coding pass is run before the codebook
  goes to coders.
- **Candidate home:** a test that parses the codebook's cardinality rule against `_labels`'
  input, or a step in the pilot protocol's "After the pilots" before two coders try `v0.md`.
