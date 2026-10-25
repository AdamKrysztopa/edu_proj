# D1 rule, fixed before the owner answers (2026-10-25)

Light blind check (owner, 2026-10-25): no pre-registration document, no methods-critic, no hash
commit ceremony; the rule and its synthetic checks are fixed here, before any answer exists.

- **Sheet:** `questions.md`, sha256 `70fb9bb6c5fe52bdb9df9df8a787e9e3570090dbd93244a584cd75d6c08dcbf1`. 15 questions, shuffled with seed 20261025.
- **Key:** `sealed/key.json` (git-ignored, not shown to the owner), sha256 `46c10318962ac7432ce7522eace9dee93040369670484798e9ad510eefe4cfb9`.
- **Rule:** `rule.py`, sha256 `66e14d01bb8c6ae2fa3f886a7fd9f628ec227f69111f9aecb0af7e374d02f1dd`. Novelty rate = share of "new" among answers where both
  judges agree. **Continue** if the gap rate minus the covered rate is at least 0.30 and at least 5
  of the 10 gap answers are "new"; otherwise **Change**. Exact permutation p over the 15 labels.
- **Synthetic checks (L7.3):** `rule_checks.json`, all pass: planted positive gives Continue
  (p = 1/3003); all-novel, all-copied, filler, 4-of-10 new and judge disagreement give Change.
- **Judges:** `judge.py`, Opus 5.5 and gpt-6.1-sol (`models_judges.json`), each answer against
  the 10 most similar corpus passages, arm withheld; filler and copied-passage canaries first; cap $1.

**Where the questions come from.** Gap: the 10 HYP questions from both arms' gap maps, minus one
duplicate quote, plus the top single-source open candidate (the gap map judged it open, but only
one independence key discusses its topic). Covered: 5 lens candidates the closure judge closed,
in the same lens templates, matched on lens mix where possible. Mean length: gap 50.3 words,
covered 51.4.

**Known weaknesses, stated before the result.**
- Both gap maps carry the flag `closure-uninformative`: the gap map's own null check finds the
  local closure judge does not separate open from closed better than chance on these ledgers.
  The D1 check is therefore a test of whether the targeting works at all, not of a validated map.
- Some quoted sentences are flattened table rows or come from Wikipedia rather than the owner's
  docs; the owner answers them as an expert in the field.
- One expert, who also built the system, on one codebase. Illustration, not evidence; feeds no
  N3 gate.

**Amendment before judging (2026-10-25).** The first 10 answers came back as option stances with
no text (a form defect, lesson in `docs/lessons.md`). A content floor is added before any answer
is judged: if fewer than 8 of the 15 answers carry content by both judges (neither says "no
content"), the result is **No reading**, not Change. `rule_checks.json` adds the stances-only case.

**Amendment before judging: judges (owner, 2026-10-25).** OpenRouter credit ran out after 6
judge calls (HTTP 402; those labels are discarded). The owner chose to judge without new money:
judge A is a fresh Claude Opus 5.5 subagent, judge B is Codex gpt-5.6-sol (replacing gpt-6.1-sol;
still another family, ADR 0009). Each reads only `cases.json` (questions, answers, the same top-10
passages and canaries, no arm), written outside the repo; both are told not to open the repo. The
rule is unchanged. Weaker than registered: both tools could technically read the sealed key.
