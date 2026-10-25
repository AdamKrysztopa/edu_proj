# SYNTH: the programme after waves 1–4, in one document

**Branch:** none. Work on `plans-2026-10-24` and commit only the files named under Finish.
**Output:** the existing Claude Docs document https://claude.ai/artifact/XwWjHGbKjDuBgyKX4BEME9 ("NOW programme after waves 1–4: conclusions and next steps"). Read it first and build in it; never create a second doc. Its planted pending sections are a first pass. Restructure them to the outline below, replacing or removing pending blocks as needed (`guide` topic.editing before any delete).
**Cost:** $0, with no paid model calls; Codex is used read-only.

## Who reads it and what they must come away with
The owner, a researcher who reads pictures first and opens details only to check. After two minutes on the main tab they must be able to answer, in their own words, three questions:
1. **What have we achieved?** This means what was built, what was learned and what was decided. It also means what has *not* been shown: the central hypothesis (RQ-B: does a reconstruction plus a gap map predict where the human knowledge residual lies?) has had no gold reading yet. Say so plainly, near the top.
2. **What are the next steps?** The ordered route from today to the first real N3 result, then to the later NOW items. For each step give:
   - who acts (the owner or a session);
   - what it costs;
   - what it waits on;
   - which decision its result feeds.
3. **What could the final product of the project be?** Answer for education (diagnosing learner bottlenecks and turning gaps into instruction) and for organisations (residual accounting, knowledge-at-risk). For each candidate product:
   - what it would do for a user;
   - which experiment must pass to license it;
   - what is already ruled out (for example, synthetic learners as evidence).

   Label every product statement as a plan or hypothesis, never as achieved.

Write in plain language. Define each term on first use and keep a short glossary at the end of the main tab: NOW, N0–N9, N3, gold, residual, gap map, closure, E-CTA, E-OSS, E-KC, T2, MS1, guard arm, and any other term you use.

## Main tab outline
1. **Verdict**, in two sentences: where the programme stands and what decides its fate next.
2. **What we achieved**, as three short lists (built / learned / decided), each item with its number and its wave. Follow it with **"What is not shown yet"**.
3. **Where each NOW item stands**: a drawn status diagram of N0–N9, with each item's state and what blocks it.
4. **What is next**: a drawn route (flow or timeline) from today to the first N3 reading and beyond, with its gates marked. Under it, a numbered list of the immediate steps, each with its owner, cost and the decision it feeds.
5. **What the final product could be**: a drawn path from today's evidence to each candidate product, with the experiment that licenses each step. Under it, one paragraph per product. Mark what is research output and what is product.
6. **Owner decisions due now**: each with its options ordered by merit, exactly one marked "(Recommended)", and the evidence for it.
7. **Risks** that could still sink it, at most five, each with its source.
8. **Glossary** and **Sources** (the wave report links).

The second tab, "Decisions and detail", holds:
- every owner decision taken in waves 1–4, dated and sourced;
- per-wave detail;
- anything cut from the main tab.

## Sources (read only these, and cite them)
- The four wave reports, read through the Claude Docs tools, never fetched from the web:
  - wave 1: https://claude.ai/artifact/2bdygzaVgPF6LE9DoaNDLc
  - wave 2: https://claude.ai/artifact/M1NDPick23TyXjJ1gPQis1
  - wave 3: https://claude.ai/artifact/3x2P5bJ8RKBBQ9KMw3Dnce
  - wave 4: https://claude.ai/artifact/Naa5KmhJHbUq3TZenVBHXX
- `REORIENTATION.md` on `plans-2026-10-24`:
  - for the programme: §1 (summary), §6 (the reframed problem), §7 (education and organisations), §14 (the residual and the gap map), §20 (later human validation), §21 (product implications), §22 (NOW, LATER, MUCH LATER) and §24 (next steps);
  - for "what is the product": the Final test at the end, especially Q2 and Q10.
- `CLAUDE.md`, which covers Validation Track A (physics), frozen but not retired: it is the education study's route to students.
- `PROGRESS.md`, `docs/plans/implement-queue.md`, `docs/plans/deep-search-queue.md`, `docs/plans/prompts/README.md`.
- The unmerged branches. Read them with `git show <branch>:<path>` and never check them out:
  - wave 3: `i8-admissibility`, `i10-pregold-corpus`, `i4-v1-kit` (`research/v1_closure/READY.md` and `PREREG.md`);
  - wave 4: `ds9-learner-licences`, `ds10-eig`, `ds11-sop-log`, `ds12-surrogate-t2`.

  Their `REORIENTATION.md` and queue lines carry owner decisions that are not on `plans-2026-10-24` yet; where they differ, the branch's decision is the newer one.
- `docs/lessons.md` § Open, for the process risks only.

## Method
1. Ask Codex (`gpt-5.6-sol`, effort high, read-only) for a storyboard from these sources that follows the main-tab outline above. It answers the three questions with numbers and sources, and ends with a cut list. Learn the companion's flags from its source and never pass it `--help` (lesson in `docs/lessons.md`).
2. Fill the doc one section per call. Every number comes from a committed file or a wave report's figure source, cited beside the figure or in the sentence. Screenshot every figure and fix overlaps before moving on.
3. Keep the evidence labels. A SYNTHETIC result stays labelled SYNTHETIC; a search that found nothing reads "none found", never "none exists"; a plan reads as a plan.
4. Ask Codex to review the built doc against the sources: export the main tab to a scratchpad file and give Codex that file plus the source list. Verify each finding against its source line, then apply every verified fix.
5. **Cold-read test (the done-criterion).** Give a fresh subagent only the exported main tab, with no other context, and ask it the three questions above. Compare its answers with the sources.
   - If any answer is wrong, vague or missing, the page has failed: revise it and test again.
   - Record the final test answers in the second tab.

## Never
- Take an owner decision. List each one that is due, then ask the owner with `AskUserQuestion` before you finish (options ordered by merit, exactly one "(Recommended)", with evidence).
- Merge, push or touch a wave branch. Merging is an owner step, and it carries a hazard: DS10 and DS12 both add refs [178]–[179] to `REORIENTATION.md`.
- Edit `REORIENTATION.md`, any gate, threshold or frozen file.
- Present a product as achieved, or a synthetic result as evidence.

## Finish
1. Add the doc link under the wave report links in `docs/plans/implement-queue.md`, and add one line in `PROGRESS.md` under the wave 4 entry.
2. Commit those two files on `plans-2026-10-24` with a message starting "Programme synthesis, waves 1–4".
3. Reply to the owner in five sentences or fewer: what we achieved, the next step, the most likely final product and what must pass to reach it, and the decisions due, with the doc link.
