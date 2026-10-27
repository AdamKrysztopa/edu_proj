# RT insert spec, GDPR v1 split (plan `docs/plans/closure-topicality-check.md` §1.4)

SYNTHETIC: the sentences written from this spec are authored by an LLM subagent. They choose and
rewrite fixtures only; the owner's labels decide every verdict.

For each topic in `fixtures/topics_gdpr.json` → `topics` (not `reserve`), write two English
sentences, P and N, into `fixtures/inserts_gdpr.json`:

```json
{"spec_sha256": "<sha256 of this file>", "note": "SYNTHETIC ...", "inserts": {"g01": {"P": "...", "N": "..."}, ...}}
```

Each topic gives `lens`, `seed_text` (the seed assertion), `question` (the lens question) and
`background_rows` (real sentences from GDPR guidance that the judge will see beside the insert).

**The element** is what the lens question asks for, about the seed:
- DISC: how to tell whether something counts as the quoted term: a threshold, a defining feature,
  or a contrast between a case that is and one that is not.
- WHY: why the seed's practice is done: the reason, or the failure it prevents, other than "the
  law or regulation requires it".
- HEDGE: the specific cases in which the seed's rule does not hold: an exception condition, not a
  restatement or a cross-reference.
- SEL: a condition that says which option to choose in which situation.
- RESULT: what result of the seed's test or assessment to expect, and what a given result means or
  which next action it leads to.

**P** states the element for this seed, plainly, in one sentence, in the register of GDPR guidance.
It must not copy a background sentence. About half of the Ps (8 of 16) carry none of the closing
words "because", "so that", "unless", "except", "if", "when", "means", "indicates", "led to".

**N** is on the same topic as P and uses the same topic words, but states a concrete fact that is
not the element: a date, a document or section reference, a role, a default, a format, a
procedure step that answers nothing the question asks. A careful reader must be able to say it does
not answer the question. About half of the Ns carry one of the closing words above vacuously (for
example a "when" that only dates something).

**Constraints checked in code** (run
`uv run --directory gapmap python ../research/closure_topicality/rt.py --split gdpr --check-inserts`
from the repository root; it prints each topic's first problem and a split-level line; iterate until
it exits 0):
- length: len(P) ≤ len(N) ≤ 1.10 × len(P), in characters;
- overlap: N shares with the seed-and-question words (stemmed content words) at least as many as P
  and at most one more;
- probe: N shares at least as many of the topic's `probe` words as P;
- novelty: the counts of N's and P's content words that are not in the seed or question differ by
  at most 1;
- specificity: N has at least as many digits, conditionals ("if", "when", "whenever", "unless"),
  backticked names or snake_case names as P;
- split level: for the closing lexicons and for every other lexicon in `gapmap.config.PATTERNS`,
  the number of Ps and the number of Ns that match differ by at most 1.

Do not read any file under `research/n3_control_v3/`, `research/n3/` or any `closure_judgements.json`:
no judge state may inform the sentences.
