# D1 result: one expert, one codebase (2026-10-25)

**Question.** On the owner's project dependence-forecastability, do questions aimed at the gap map's
thin spots draw out more knowledge the docs lack than questions on well-covered spots?

**Answer.** No. **Change**: fix the gap map's ranking before the WUT pilot. 5 of 9 agreed gap
answers were new (0.56) against 2 of 3 agreed covered answers (0.67); difference −0.11, exact
permutation p = 0.68. The rule needed +0.30 and at least 5 new gap answers; the second part was met,
the first was not. The content floor was met (13 of 15 answers had content).

**Changed.** The gap map's targeting is not shown to work on this codebase. What did work is the
rest of the loop: the questions drew out 7 pieces of knowledge both judges call new, and 3 places
where the owner's practice contradicts the docs (Q4, Q7, Q9). That material is in `onboarding.md`.

## How to read it

- **Illustration, not evidence.** One expert, who also built the system, on one codebase; answers
  of one or two sentences; 15 questions. It feeds no N3 gate and is not RQ-B evidence.
- **The gap map flagged itself.** Both arms' gap maps carry `closure-uninformative`: their own null
  check found the local closure judge no better than chance (stated in `RULE.md` before answering).
  The result agrees with that flag.
- **Covered questions drew new answers too** (Q7, Q14). The owner adds knowledge almost everywhere
  the docs are prescriptive, so "covered" by the map did not mean "nothing left to say".
- **Deviations, all recorded before judging** (`RULE.md`): answers were collected question by
  question in chat after an option form produced no content; a content floor was added; the judges
  were a fresh Claude Opus 5.5 subagent and Codex gpt-5.6-sol instead of Opus 5.5 and gpt-6.1-sol
  via OpenRouter, because OpenRouter credit ran out. Both judges passed the canaries (filler → no
  content, a copied passage → already written). The owner's self-rating (prompt step 6) was not
  collected.

## Figures

| | Cheap arm | Top-tier arm |
|---|---|---|
| Models | Haiku 4.5, verifier gpt-5.4-mini | Opus 5.5, verifier gpt-6.1-sol |
| Corpus | 26 docs (16 owner, 10 outside) | same |
| Claims | 691 | 644 |
| Independence clusters | 4 | 4 |
| Run | stopped at its $1.50 cap, ledger saved | complete, $3.96 |
| Gap-map HYP | 7 | 3 |

Agreement between judges: 12 of 15 answers. Per-answer labels: `result.json`; judge reasons:
`judgements.json`; key: `key_revealed.json`.

## Cost

$12.68 in model calls: $2.61 on the 16-doc arms (superseded, one gap-map finding), $4.58 on the
26-doc arms that failed or were stopped (a budget-stop bug, fixed in `17e539f`), $5.46 on the
rerun, $0.04 on judge calls refused for lack of credit. The judges themselves ran on the session
and Codex, not on OpenRouter. The owner's cap was $8, raised to $11 and then to about $13.50.

## Step 5 (design only)

Newcomer struggle would be measured from first-time contributors: issues and questions they open,
review rounds on their first pull requests, and which onboarding paragraphs they say they used. No
learner was involved in D1; the WUT pilot is where step 5 meets real learners.
