# Codex storyboard prompt for a wave report

Fill in `<N>` and the item list, then send it read-only (`gpt-5.6-sol`, effort high).

---

You are co-writing a research report with Claude. Read-only: do not edit files. Your output is a storyboard that Claude will build into a Claude Docs document (hand-drawn SVG charts and diagrams, tables, callouts and prose).

## The job
Storyboard the "Wave <N> report": a reader gets the story in 2 minutes from pictures, with detail below for checking. Its structure is that of wave 2's report: a verdict line, "Wave <N> at a glance" (worked / failed), the decision path diagram, one section per decision with a figure and a Question/Answer/Changed card, the decisions taken, and what the next wave must settle.

## Audience
The project owner, a researcher. They read the verdict, the at-a-glance bullets and the pictures, and open details only to check. Use short sentences, and gloss any jargon in one line.

## Context
- `REORIENTATION.md` §1 and §22: the NOW programme, N3 on the critical path.
- The wave's items: each one's `report.json` and the note beside it (list them with branch and path).
- The owner decisions taken during the wave: `docs/plans/implement-queue.md` and `docs/plans/deep-search-queue.md`.
- Lessons captured: `docs/lessons.md` § Open.
- The next wave's rows: `docs/plans/prompts/README.md`.

## What to deliver (markdown, in this order)
1. **Verdict line:** one sentence.
2. **One-paragraph story:** what we asked, what we learned, what changed.
3. **Wave <N> at a glance:** Worked and Failed/negative bullets, at most about 12, each ≤ 20 words and carrying its number.
4. **Decision path:** a flow diagram spec of the N3 route after this wave's decisions, each node citing its decision source.
5. **One figure per decision:**
   - its type (chart, diagram or table);
   - a title that states the finding with its number;
   - the exact data rows, citing file and field;
   - the accent;
   - the reference line or mark it is checked against.

   Add a three-line Question / Answer / Changed card for each.
6. **Decisions taken** (owner, dated) and **what the next wave must settle**: which prompts are unblocked, which stay blocked, and why.
7. **Cut list:** what belongs only in the "full notes" tab, or nowhere.

Be exact: quote every number in a figure from a file, with its path and field. If a number is not in the files, say "not found" rather than estimate.
