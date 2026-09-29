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

### A green suite hid a grouping rule that inflated breadth-based confidence

- **What happened:** the first `gapmap/` build read the spec's DIAG rival rule as connected components rather than seed plus direct rivals (`docs/plans/n3-poc-lens-spec.md` §2.2). All 91 tests passed, but on the real PLC ledger the components chained unrelated causes ("array subscript out of range", aliasing, loose terminals) into one 40-claim group. Its 12 independence keys made DIAG "high" at #1 and #2 of the map. It was caught by reading the rendered `research/n3/plc/gapmap.md`, not by a test: the fixtures checked the rule locally and never checked how the ranking reacts to group size on real data.
- **Generalises to:** when a score rises with the size of a derived set, the grouping or linking rule that builds the set gets a test on real data that bounds the set's size, and a human reads the top of the ranked output before it counts as done.
- **Candidate home:** `gapmap/tests/test_smoke.py` (a max group size or top-record breadth assertion); `methods-critic` checklist item for any breadth- or count-weighted confidence.

### The check meant to catch "density renamed as gap" passed by construction

- **What happened:** §7.1 of `docs/plans/n3-poc-lens-spec.md` ranked a pool that included RG-UNK records, whose density is 0 by definition. So the low-density top 10 was all RG-UNK in every map, and `J10(map, D_low) = 0.00` was guaranteed. The check never compared open lens candidates against closed ones. It reported "no flag fires" on a map whose closure test the Opus adversarial review showed matches a random-neighbour null (31 of 49 closed on PLC; the null expects 32.1). This was caught by that review's ablation, not by the check or its tests.
- **Generalises to:** a check that guards against a specific failure is tested on an input built to exhibit that failure (here, a map ranked by density alone) and must flag it; any record that cannot vary on the checked quantity is excluded from the pool.
- **Candidate home:** `gapmap/tests/test_checks.py` (a density-only map must raise the flag); `methods-critic` checklist item: every "not X in disguise" check needs a planted positive and a permutation null.
- **Recurred the same day:** the replacement stem-scramble null (observed 66 vs null [14, 52] on PLC) was a straw man. Seeds could close themselves (35 of 101 closures were self or same-source), and uniformly drawn random stems almost never co-occur. A donor null with the same exclusions in both arms put observed inside the interval on every ledger (PLC 42 vs [33, 47]). Addendum to the rule: a null applies the same exclusions to both arms and draws realistic donors (real content from another unit of the same kind), never uniform tokens. **Third occurrence:** the semantic judge's mismatched-evidence control put the seed's own sentences in the own arm only. 17 of PLC's 22 own-arm closures cited only the seed or its source, so the arm "passed" (41% vs 2%). With the seed kept in both arms it was 21/45 vs 20/45.

### A judge answer the parser could not read defaulted to the finding

- **What happened:** `gapmap/src/gapmap/semantic.py` `judge_retrieval` accepted only `A1`/`S1`-style sentence ids. The local judge (qwen2.5:7b) often cited bare integers (`[3, 8]`). Those were dropped as invalid, and the candidate became `open`, i.e. a hidden-knowledge hypothesis. This hit 24 of 103, 62 of 150 and 60 of 147 responses; read positionally, 13 of 19 map hypotheses flip to partial. It was caught by the Opus final review reading cached reasons that contradicted "open", not by tests: the fake judge always answered in the expected format.
- **Generalises to:** when a model's answer cannot be parsed, the result is a distinct `undecided` state that never counts as the finding; the fake used in tests must also emit the malformed and alternative formats the real model produces.
- **Candidate home:** `gapmap/tests/conftest.py` FakeJudge variants; the `reconstruct/` verifier parse path (same shape: an unparsed verdict must never count as a verdict).

### Figure agents' "visually inspected, clean" reports were accepted without looking

- **What happened:** While building `report/`, figure subagents reported fig03, fig04, fig10, fig11, fig12, fig13 and fig14 as "rendered, visually inspected, clean". The renders actually had overlapping boxes, rule text spilling out of gate diamonds, crossing diagonal arrows (fig03) and clipped labels (fig10, fig12). fig11, fig13 and fig14 were also ~300 mm tall, so they could not fit the page at a readable size. The user caught it ("the figures are strongly glitched"); no check did. The orchestrator had accepted the self-reports and viewed only fig01/fig02. The loose briefs ("layered", "ladder") let agents hand-place nodes. What fixed it: exact grid specs (column pitch, fixed text widths, one title plus one 7 pt line per box, gate rules outside diamonds), a stronger model for layout, the TikZ manual via Context7, and the orchestrator reading every 150 dpi render before accepting it.
- **Generalises to:** A visual deliverable is accepted only after the accepting party has looked at its render. A producer's own "inspected, clean" report is a claim, not a check.
- **Candidate home:** the report/figure workflow notes (`report/notes/10_visual_language.md`), or a rule in `CLAUDE.md` next to the Playwright hand-over rule, which has the same shape: run it yourself before handing it over.

### Key-headroom miss recurred one day later, on a $0.001 spike

- **What happened:** The JEV spike (`research/spikes/jev/spike.py`) was designed, built and handed to a live-run agent. Nobody first called `GET /api/v1/key`. The key's $5 weekly limit was already spent (`usage_weekly` 5.02, `limit_remaining` 0), so the first Decisions API call returned 403 "Key limit exceeded (weekly limit)". The run needed an estimated $0.0012. The spike's own hard cap passed, because it sums only the spike's own cache. It was caught at `smoke`, which cost one build round. The queued entry "Freezes and gated reruns were planned without checking the provider key's headroom" was already in `docs/lessons.md` and did not prevent this.
- **Generalises to:** Every script that makes paid OpenRouter calls reads the key's `limit_remaining` before its first call and refuses to start when it is below the run's estimate. A per-run budget cap does not replace this check.
- **Candidate home:** A small shared pre-call helper, or a hook on `OPENROUTER_API_KEY`-using commands, merged with the earlier headroom entry at drain time.

### A spike's pre-registered "beyond density" rule was passable by word length

- **What happened:** The decision rule in the JEV spike (`research/spikes/jev/spike.py`, `classify`) counted a signal as PROMISING when it met four conditions: agreement between two paraphrases above a threshold, weak correlation with `k_topic` and with the N3 score, stable residuals after regression, and a gap of at least 0.20 over a `has_number` control. Jev passed and was labelled PROMISING. The hostile Opus review then fed the same rule two trivial word-length statistics of the anchor text, and they also passed. The control had no power: only 3 of the 61 texts contain a digit. The review caught this, not the rule. The label was corrected to INCONCLUSIVE.
- **Generalises to:** Before a rule meant to show "signal beyond X" is registered, run it on a trivial stand-in (noise, text length, a surface statistic). If the stand-in passes, the rule cannot discriminate and must be changed before any data is collected.
- **Candidate home:** `methods-critic`, as a required check on any registered decision rule. Merge at drain time with "The check meant to catch 'density renamed as gap' passed by construction" and "A 'beats the baseline' gate was registered without checking it was reachable".

### A control's conclusion was worded wider than the arms it swapped

- **What happened:** The report said the closure judge's "verdict does not depend on which evidence it is shown", from `checks.mismatched_evidence_control`. That control keeps the seed's sentences in both arms and swaps only the other-source sentences, so it cannot test dependence on evidence as such. The same wording sat in eight places across both reports and the executive summary, and an owner-named "fair" control carried it past two AI review rounds. An independent review caught it; the conclusion now names what was swapped.
- **Generalises to:** State a control's conclusion in terms of the variable its arms actually differ on, and list what both arms share. A control is not called "fair" in prose; the name says what it swaps.
- **Candidate home:** `methods-critic`, as a check on every control or null a report cites.

### A superseded headline number stayed current in a README

- **What happened:** `research/n3/README.md` and `PROGRESS.md` kept the pre-final lexical-closure figure (PLC 42 vs [33, 47]) after the final maps gave 22 vs 33.48 [26, 41], while report links pointed at the moving `main` branch. Two apparently current answers existed. Fixed with `research/results_manifest.json` (`scripts/results_manifest.py --check`) and links pinned to the audited commit.
- **Generalises to:** Headline numbers live in one generated manifest that a check recomputes from the artefacts, and a report cites an immutable commit, never a branch.
- **Candidate home:** `citation-verifier` or a pre-commit check that runs `scripts/results_manifest.py --check` when `research/` or `report/` changes.
