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

### A "beats the baseline" gate was registered without checking it was reachable

- **What happened:** E-ABST's gate needs FAR_raw − FAR_pipe ≥ 0.20, but the raw baseline answered only 5 of 24 items (19 null), so the margin is met only in a narrow corner: all five answers false and no pipeline false answer at n_included ≥ 21, and little more at n = 20. E-PLANT's ungated arm adopted 5/24 plants against the assumed > 60%. Both baselines ran before the pipeline arms, but nobody computed the reachable range of the gate from them. Caught at the N2 closeout from counts alone.
- **Generalises to:** before any gated arm runs, compute the best case the gate can reach given the observed baseline (e.g. the maximum FAR_raw = answered/n) and record whether the gate is still reachable. Do this for every margin, not only where a validity floor exists.
- **Candidate home:** `methods-critic` checklist; a pre-run check in `eabst.py`/`eplant.py` that prints the reachable range.

### Freezes and gated reruns were planned without checking the provider key's headroom

- **What happened:** the OpenRouter key has a $5 weekly limit. It blocked both E-LIVE v3 runs at the first call (17:14 and 17:15 UTC), and at the closeout had $0 left against about $21 of registered caps. The registered route needed a live E-LIVE v3 before any rerun (amendment 2 P1), so N2 closed inconclusive on budget, not on evidence.
- **Generalises to:** before registering a sequence of live runs, read the key's remaining limit and compare it with the sum of the registered caps; record both numbers in the protocol.
- **Candidate home:** `/preflight`-style check in `reconstruct` (`GET /api/v1/key`, printing limits only).

### A drain changed a hook's output without running that hook's own tests

- **What happened:** drain 5 (`2376825`, L5.1) made `.claude/hooks/session_start_lessons.py` report unreadable `.claude/settings.json`. `scripts/lessons_loop_tests/test_lessons_loop.py` still expects silence when there is no ledger or no readable archive, and fails 2/54 ("no ledger at all: emits nothing", "unreadable archive: emits nothing rather than something reassuring"). Found at the N2 closeout by a quality-gate sweep, not by the drain.
- **Generalises to:** an edit to a hook runs every test suite that invokes that hook, not only the DOI hook test that CLAUDE.md names.
- **Candidate home:** CLAUDE.md "Tests" list; `implement-ll` drain checklist.

### L1.3 recurred: three N2 freezes were declared before a clean live run

- **What happened:** `n2-freeze`, `n2-freeze-2` and `n2-freeze-3` were each tagged before any live run completed `cross_verify` and decoy calls (final review P1). At the closeout, no unsealed live run shows either. Cross-verify ran live only inside the sealed E-PLANT run 1 (sidecar `n_cross_checks` 276 and 90, logged under task `verify` before `0f39ed9` gave it its own label), with 0 decoys there. The sealed E-ABST run 1 logged 3 decoy calls in total. L1.3 ("not done until a live run passes") existed and did not stop it, because a freeze tag is not treated as "done".
- **Generalises to:** a freeze tag on anything a live model sees requires the live check first; the tag message names the live run directory that passed.
- **Candidate home:** `live-smoke-reminder` hook extended to `git tag n2-freeze*`; decision 0007.
