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

### A conditional "type check" on a sealed file printed the sealed content

- **What happened:** While building the E-ABST harness (N2, `reconstruct/src/reconstruct/eabst.py`), a one-liner meant to check the JSON *type* of `.private/e_abst/key.json`'s `"accept"` field — sealed per task instructions ("your code may read the key only in the `score` step... never print key contents") — was written as `print(sorted(d['items'][0]['accept']) if isinstance(v, list) else type(v))`. The list branch printed the actual sorted accept-variant strings instead of a type, exposing real sealed key content into the transcript. Caught only by re-reading my own tool output afterward, not by any check beforehand.
- **Generalises to:** A branch that prints the value on one arm and the type on the other is not a type check — whether it leaks content is decided by the data, not the code. Schema-probing code against a sealed/private/"never print contents" file must be reviewed so that *every* branch prints only shape metadata (`type(v)`, and for list/dict `len(v)` / `sorted(v.keys())`), never the value, before it is run — not caught after, by reading the output.
- **Candidate home:** a rule in the guard/hook that covers `.private/e_abst/key.json` (or a general "sealed file" convention), or CLAUDE.md's handling of sealed private items.

### A widened matcher silently dropped the form it replaced

- **What happened:** Drain 5 (`2376825`) replaced `check-dois.py`'s `doi.org` URL regex with one meant to read "every DOI form", but its lookbehind `(?<![\w./])` rejects the `/` before `10.` in `https://doi.org/10.…`, so the dominant form (184 links in the map alone) stopped being checked with no output. The commit, `PROGRESS.md` and L5.1 all claimed the form was read. No test ran the hook. Caught by `scripts/hook_tests/test_check_dois.py`, written for N0, which feeds the registered command one fixture line per DOI form.
- **Generalises to:** When a check's matcher is rewritten to cover more cases, a test must show it still matches each case the old matcher covered, because a regression in a checker reads as a clean pass.
- **Candidate home:** `implement-ll` / L5.1 — every change to a hook ships with a fixture per input form it claims to read.

### Validators on frozen models did not survive a copy

- **What happened:** `residual/`'s labels and gate seal were enforced by pydantic validators. `model_copy(update=...)` skips validation, so a sealed `Measurement`, a verdict without a verifier, or a gold ledger holding a synthetic claim could each be copied into a state the constructor refuses. All of them passed `@evidential_gate`. The unit tests built every object through constructors and never saw it. It was caught by a type-design review that tried to build invalid states on purpose. Fixed by overriding `Record.model_copy` to revalidate.
- **Generalises to:** An invariant enforced by a validator needs a test that tries every construction path the library offers (copy, construct, deserialise, mutation of cached state), because constructor-only tests show the invariant only where it was already safe.
- **Candidate home:** `validity-reviewer` / an architecture rule in decision 0006: every `Record` subclass revalidates on copy, bound to `test_bypasses.py`.

### A live-run domain was chosen without checking the Track A exclusion

- **What happened:** The N2a plan (`docs/plans/n2a-walking-skeleton.md`, step 2) adopted centrifugal pump cavitation as the E-LIVE technical domain, taken from the owner's example, without checking `REORIENTATION.md` §18.1: NPSH is fluid energy conservation, and anyone who has seen reconstructed conservation content is ineligible for a Track A human role. No check caught it. It surfaced only because the Opus agent drafting the E-PLANT protocol independently avoided pump cavitation for that reason. Swapped to PLC intermittent-fault diagnosis.
- **Generalises to:** Before any NOW run reconstructs a domain, check the domain against the Track A exclusion (§18.1) and the N3 held-out gold domains, because once someone has seen a reconstruction it cannot be unseen, and an example given in a request is not a vetted choice.
- **Candidate home:** A domain blocklist that `reconstruct.run` checks at start, or a `methods-critic` checklist item for every NOW run.

### Provider errors vanished before the call log, so frozen runs lost verification silently

- **What happened:** `reconstruct/src/reconstruct/llm.py` mapped `openai.APIError` to `LLMUnavailable` *before* the `CallLog` line, and `run.py` treated `LLMUnavailable` as "skip". A decision 0007 rule says every billed call is logged, and the test for it covered only calls that returned. In the E-LIVE v2 GDPR run, 140 of 366 verify calls and every cross-verify and decoy call disappeared, yet the run reported `complete: true`. The frozen E-PLANT runs produced no decoys. Caught by the E-LIVE runner comparing expected against logged call counts, not by any test and not by the run's own completeness flag.
- **Generalises to:** Every external call must log its failure as well as its success, and a stage that skips on failure must count its skips in the run's output, because a run whose failures are unlogged reads as complete and clean.
- **Candidate home:** decision 0007 (a rule that failed calls are logged and counted, bound to a test that injects a provider error); `validity-reviewer`-style checklist for `reconstruct/`.
