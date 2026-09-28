# Human interviewer script: Stage A probe session

You run the same script as the AI interviewer (`prompts/interviewer_system.md`), under the same 20-minute cap per problem set. Train on it before the first pilot and keep this page open during the session.

## Stems

Use every stem at least once for every problem in the set, in any order, at moments of your choosing. You may reword a stem naturally; the wording below is the reference. Tick the stem in the console as you ask it.

| Stem | Reference wording |
|---|---|
| cues | At this point in your solution, what did you notice that told you what to do? |
| alternatives | What else could you have done at this point, and why didn't you? |
| checks | How did you know your result here was right? |
| anomalies | What would have made you stop and rethink at this point? |
| novice_miss | What would a first-year student miss here that you see? |

## Rules

- Press I before you say anything, and I/E at every change of speaker; tick a stem only after pressing I. Speech recorded before the first press has no speaker. The console flags it; it is still run through the guard audit and counted per set in the leading-question key, but no answer given there reaches the operation coding.
- Ask one question per turn. Tie it to a specific moment of the solution: click the segment ID to show it to the expert, or point to the written work.
- **Never lead.** The rule is the one the AI's guard applies, word for word:

  A question is leading if it names or implies a specific physics principle, quantity, relation, representation, strategy or check that the expert has not said, in the same or equivalent words. Neutral questions about what the expert noticed, considered, checked or expected are not leading. Restating the expert's own words is not leading. Words that appear in the problem statements are not leading.

  "What the expert has said" is the think-aloud trace of the problems in this set plus the expert's answers so far. Keep any hypothesis to yourself and ask a neutral stem question that would let the expert say it. If you catch yourself about to name something the expert has not said, ask the stem instead.
- **Follow-ups.** Directly after a stem question you may ask at most one follow-up on the same stem and problem. It quotes the expert's own words exactly and asks them to say more: You said "it's obviously not elastic" — what told you that?
- Do not evaluate, praise or correct the expert's physics, and do not explain physics yourself.
- When time is short, prefer stems not yet used.

## How the rule is checked

The AI's guard rejects a leading question before the expert sees it; each rejection is logged, the time it takes runs on the same clock as the cap, and a question finished after the cap is discarded unseen. A human question cannot be stopped before it is spoken, so the same guard is run over every human question after the session (`probe-code guard-audit`), with the same inputs it would have had live. Every question in both arms (except the AI's bare-stem fallbacks) is also coded for leading content by coders who do not see the arm (`probe-code export-leading`); fillers are stripped from both, and coders guess each item's arm so that the residual unblinding is measured.
