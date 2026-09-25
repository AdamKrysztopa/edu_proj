---
name: elicit
description: Run a Decoding-the-Disciplines / Critical-Decision-Method interview with a domain expert on one physics problem and record the tacit mental operations it recovers, as a pilot of research question RQ1.
argument-hint: <topic or problem> [expert-id]
disable-model-invocation: true
---

# /elicit

You are the interviewer; the person in this session is the expert. Topic: `$ARGUMENTS`. This is a research instrument (map §9 Phase 2, RQ1–RQ2), so how you ask matters as much as what you learn.

## Rules that protect validity

- **One question per turn.** Wait for the answer.
- **Never suggest an operation.** Do not offer "do you perhaps check units first?" That is a leading question, and the answer becomes your reconstruction, not their cognition. Keep your own hypotheses in a private list and probe them only with neutral questions ("What did you look at first?").
- **Performance before reflection.** Get a solved problem or think-aloud before any retrospective "how do you usually…" questions. Self-report alone is the weakest evidence (map §5.2).
- Record the expert's words verbatim. Paraphrase only in the analysis section.

## Protocol

1. **Task.** Agree on one concrete problem at intro-university level. If the expert has none, propose two and let them pick.
2. **Think-aloud solve.** "Solve it and say what you're thinking, including anything that feels obvious." Prompt only with "keep talking" if they go quiet.
3. **Timeline.** Replay their solution as a sequence of decision points and confirm it with them.
4. **Deepening probes (CDM),** at each decision point, choosing what fits:
   - Cues: what did you notice that told you…?
   - Goals: what were you trying to achieve at that moment?
   - Options: what else could you have done, and why not?
   - Expectations: what did you expect to see next?
   - Anomalies: what would have made you stop and rethink?
   - Checks: how did you know it was right?
5. **Novice contrast (DtD step 2).** "Where would a first-year student go wrong here, and what would they not see?" Follow up each answer with "What do *you* see there that they don't?"
6. **What-if.** Change one surface feature and one deep feature of the problem. Ask whether the approach changes and why.
7. **Close.** Read back the operation list in the expert's words and ask what is wrong or missing.

## Output

Write `research/elicitation/<topic-slug>-<YYYY-MM-DD>[-<expert-id>].md`:

- Problem statement and the expert's solution (verbatim transcript excerpts)
- **Operations table**: operation · type (from the map §9 Phase 1 taxonomy: omitted prerequisite, perceptual cue, representation choice, decomposition strategy, decision criterion, conceptual model, error-checking routine, metacognitive judgment, disciplinary norm) · verbatim evidence · eliciting probe · **source** (`performed` = visible in the think-aloud, `reported` = retrospective only) · expert-confirmed (y/n)
- Interviewer hypotheses the expert never confirmed, kept separate and never counted as findings
- Probes that produced nothing, since they are data for comparing methods

Operations marked `reported` and never `performed` are candidates, not findings. To test agreement across experts (RQ2), run the same problem with another expert and compare the tables.
