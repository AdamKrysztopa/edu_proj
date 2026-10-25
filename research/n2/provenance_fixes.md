# I9: Provenance fixes (R3, R4, R9, `quote_in_span`): before and after on the committed runs

**Result (2026-10-24).** All four fixes are in `reconstruct/` and tested: each one fires on a planted positive that the old code missed, and none fires on its trivial stand-in. On the six committed runs, the fixes change almost nothing:
- no slot changes status;
- the ledger contradiction count does not change;
- `verify_run` still reports 0 problems.

The fixes have little to act on, because no committed run ever executed cross-verify. v1 predates it, and in v2 the calls were dropped by the defect fixed in `0f39ed9` (`e_live_report.md` §5). The fixes therefore guard the next run more than they correct the past ones. The R3 copy test fires on real data: on GDPR v2 it withholds 242 of 6,114 cross-verify candidate pairs, across 6 source pairs (`legislation.gov.uk` Article 35 with the ICO's DPIA page or WP248). Half of them (121) are statute text quoted verbatim. The other half are the ICO's or WP248's own prose, withheld because their document quotes the claim's own statute span. Only 1 of the 404 cross-verify calls the old rule would have sent changes.

**Decision it feeds: continue.** On provenance, the fixed pipeline is ready for I4's out-of-sample domain run (the effective E-LIVE v3). That run is also the first time the fixed cross-verify, R3 and R4 paths will execute live. Its sidecar's `n_scope_refutes`, `n_cross_candidates_verbatim_copy`, `n_verbatim_copies_merged` and `n_slot_verbatim_copies` are the first real readings of these fixes. R2 (decoy validity) is not fixed here: DS6 decides it, so decoy false-accept rates still cannot estimate verifier validity.

**Caveat for I4.** The copy test runs in both directions, so it also withholds a regulator's own commentary whenever that regulator's document quotes the claim's statute span. That undercounts corroboration, which is the error direction ADR 0007 accepts. The alternative is the review's literal one-direction wording, and it lets a pure copy be corroborated by its own original (see "Reading the counts"). Read I4's `n_cross_candidates_verbatim_copy` with this in mind.

## What changed

- **`quote_in_span` minimum length** (`evidence.py`, `QUOTE_MIN_WORDS = 5`):
  - A supporting or refuting quote must be at least 5 words long, or the whole span when the span is shorter. Before, any non-empty substring counted, so a one-word quote such as "the" could support a claim.
  - The rule still applies to SUPPORTS and to REFUTES alike, through `run._verdict_from_result`.
- **R3: verbatim copies are not independent corroboration** (`evidence.fold`, `is_verbatim_copy`, `collapse_verbatim_copies`; `run.py`):
  - `span_duplicates` now matches 25-word runs on `fold()`ed text, which is case-folded with collapsed whitespace. The 25-word floor is unchanged.
  - **Cross-verify.** A candidate span from another cluster is withheld if it appears verbatim, after `fold()`, in any of the claim's own source texts, or if any of the claim's own spans appears verbatim in the candidate's document. The second direction catches a claim whose own support is itself a copy of the candidate's document.
  - **Identical-assertion merges.** The merge no longer bypasses the copy check. Among a merged claim's SUPPORTS members, one from a cluster whose spans are copies of another member's document is not attached as evidence. The sidecar records it as `verbatim_copy_of: <kept source_id>`.
  - **Slot coverage.** A slot's `covered`/`thin` now counts independence clusters after copies are collapsed (`run._independent_support`). Each slot also records `n_independent_clusters` and `n_verbatim_copies`.
  - **How the collapse works.** It is greedy and deterministic: the least-entangled items come first, ties are broken by key and then id, and one item is kept per cluster. The result is a lower bound on the independent count. This is the conservative direction that ADR 0007 already accepts for paraphrase.
- **R4: scope-flagged REFUTES are not contradictions** (`run.py`):
  - A cross-verify REFUTES whose verifier set `subject_or_scope_differs` goes to the sidecar's `scope_refutes` list, with the claim, the other claim, the source, the locator and all three flags.
  - Its `cross_checks` entry reads `added_as: "scope_refute"`.
  - It adds no REFUTES evidence and no N1 Contradiction.
  - An unflagged REFUTES still becomes a Contradiction, exactly as before.
- **R9: `verify_run` recomputes digests and binding** (`verify_run.py`):
  - Every snapshot that a locator or a sidecar source names is rehashed against its filename.
  - Every Evidence locator must name the snapshot that the sidecar binds its Source to.
  - A missing `sidecar.json` is a problem, not a skip.
  - The docstring no longer claims a re-extraction, since web mode stores normalised text only.
- **Decoys.** `decoy_is_valid` is unchanged. One test now documents its current, self-certified behaviour: a decoy is accepted whenever its rationale is non-empty and its text differs after `strip().casefold()` (`test_decoy_is_valid_current_behaviour_is_self_certified`).

## Replay: counts before and after, per run

`research/n2/provenance_fixes_replay.py` re-applies the rules in `evidence.py` and `verify_run.py` at `d413a4b` (before) and in the working tree (after) to the verdicts, quotes and flags each run recorded. Before-slot status is the current `slot_status` applied to the recorded supporting keys, and R4's "after" subtracts the scope-flagged REFUTES. The script runs against the git-ignored snapshots, offline and at $0. Runs `145115Z`, `171449Z` and `171508Z` hold 0 claims, and `verify_run` passes on them before and after. They are omitted below.

| Run | PLC v1 `133336Z` | GDPR v1 `135354Z` | GDPR v2 `145943Z` |
|---|---|---|---|
| `verify_run` problems, before → after | 0 → 0 (35 sources bound, 30 snapshots rehashed) | 0 → 0 (20 bound, 18 rehashed) | 0 → 0 (25 bound, 23 rehashed) |
| Ledger contradictions, before → after | 0 → 0 | 1 → 1 | 0 → 0 |
| Scope-flagged REFUTES in `cross_checks` | no `cross_checks` (v1) | no `cross_checks` (v1) | 0 of 0 recorded |
| `quote_in_span`: recorded verdicts rechecked | not replayable (v1 records no quote) | not replayable | 207 |
| `quote_in_span`: SUPPORTS → INSUFFICIENT | n/a | n/a | 1 |
| Claims with corroboration ≥ 2, before → after | 0 → 0 | 0 → 0 | 0 → 0 |
| Merge members dropped as copies | 0 | 0 | 0 |
| Cross-verify candidate pairs, before → after | 21,302 → 21,302 | 738 → 738 | 6,114 → 5,872 |
| Top-2 cross-verify calls, before → after (withheld) | 642 → 642 (0) | 274 → 274 (0) | 404 → 404 (1) |
| `span_duplicates` groups, before → after | 0 → 0 | 0 → 0 | 8 → 8 |
| Copy spans collapsed inside slots | 0 | 0 | 1 |
| Slots changing status | 0 of 35 | 0 of 35 | 0 of 40 |

### Coverage per slot

Each status below reads as recorded / replayed under the current rule / fixed:

- **PLC v1:**
  - covered / covered / covered: 28;
  - covered / thin / thin: 2;
  - unknown: 5.
- **GDPR v1:**
  - covered / covered / covered: 5;
  - covered / thin / thin: 16;
  - unknown: 14.
- **GDPR v2:**
  - covered: 11;
  - thin: 9;
  - unknown: 15;
  - unverified: 5.

These are unchanged in every column. The v1 "covered → thin" shifts are not caused by I9. v1 predates the `thin` status (SHOULD 3), and the current rule already splits v1's single-cluster "covered" slots.

### Reading the counts

- **R3 fires on real copies, and over-withholds.**
  - The 242 withheld GDPR v2 pairs fall in 6 source pairs. Each one links `legislation.gov.uk` Article 35 (two URL forms) with the ICO's "When do we need to do a DPIA?" page or the CNIL-hosted WP248 PDF. The withheld spans are 12 words or more (median 28).
  - Half of the pairs (121) withhold statute text that the regulator quotes, for example "a systematic monitoring of a publicly accessible area on a large scale" (Art. 35(3)(c)). This is the R3 case: a regulator quoting the statute is not a second witness to it.
  - The other 121 withhold the regulator's own prose. For example: "Decisions that have little impact generally could still significantly affect more vulnerable people, such as children." These are withheld only because the regulator's document quotes the claim's own statute span somewhere. That is independent commentary losing witness status: the cost of the second direction.
  - The second direction is kept because the same structure arises when a page is a pure copy. A claim supported by copied text could otherwise be corroborated by the document it copied (the `Copy Area` planted positive). From text alone, the rule cannot tell who copied whom.
  - The old `span_duplicates` caught none of these pairs, because it compares span to span at 25 words or more. The copy test compares a span against the other document's full text.
- **R3 barely moves slots.** A copy was collapsed in only one slot (GDPR v2 `a-4ff2451b30f75877`/concept), and there the cluster lost its only span. That span is WP248's own definition of "risk", collapsed because the WP248 document quotes the Art. 35(3)(a) span of claim `c-b8326043ad0ac2c1`. The slot fell from 4 to 3 independent clusters and stayed `covered`. This is the same over-withholding as above.
- **The one `quote_in_span` flip may be a lost true support.**
  - The verifier quoted the list item "Evaluation or scoring." (3 words) from a span on the WP29 criteria, for the claim "Evaluation or scoring is a criterion which may act as an indicator of likely high risk processing".
  - The 5-word floor turns that SUPPORTS into INSUFFICIENT. That is 1 of 207 rechecked verdicts (0.5%), and no slot changes.
  - This is the cost of the threshold. The protection it buys is against one-word quotes, which the old rule accepted.
  - Decoy verdicts and v1 verdicts cannot be rechecked, because their quotes were never recorded.
- **R4 has nothing to flip.** The single ledger contradiction in GDPR v1 came from v1's pair-classifier (`pair-classify:3c91…`). That stage recorded no drift flags, so the R4 rule cannot be replayed on it. `080b109` replaced the stage, and `closeout.md` records the false Art. 35/36 contradiction as fixed there. GDPR v2 recorded 0 cross-checks.

## Discrimination checks (L7.3)

All tests are in `reconstruct/tests/test_provenance_fixes.py` and run offline.

- **Best reachable outcome.** On the committed runs, no fix could change a slot status or a contradiction count. No claim has corroboration ≥ 2 anywhere, and no cross-checks were recorded. The ceiling for a visible effect is therefore set by the next live run, not by these runs.
- **Planted positives fire, and fail on the old code.** The R3, R4 and R9 end-to-end tests were run against `run.py` and `verify_run.py` at `d413a4b`, and all fail there. The planted positives are:
  - a 13-word passage copied across clusters, which the 25-word rule cannot see: cross-verify withholds it and the slot is `thin`, not `covered`;
  - an identical assertion merged from two documents that both quote one sentence: corroboration is 1, not 2;
  - a scope-flagged REFUTES: no contradiction, one `scope_refutes` entry;
  - a snapshot edited outside every span: the digest mismatch is caught;
  - a Source rebound to another snapshot: caught;
  - a one-word supporting quote: downgraded.
- **Trivial stand-ins do not pass:**
  - two documents sharing only common words ("shift book entry"): not a copy, and that slot stays `covered` with 2 cross-checks;
  - a 24-word shared run: no `span_duplicates` link;
  - two copies within one cluster: no collapse;
  - an unflagged REFUTES: still a contradiction;
  - an untouched run: `verify_run` passes.
- **Control.** None: these are rules, not arm comparisons.

## Rules at session start

The active rules of ADR 0007 still hold, and `test_architecture.py` passes:
- `independence-before-corroboration`: the 25-word span collapse is kept, and the copy test only adds to it;
- `support-needs-other-family-and-quote-in-span`: the quote rule is stricter, never looser;
- `budget-before-every-call`: no call path changed.

ADR 0007's Decision prose ("Union-find over domain, shingle overlap and shared verbatim runs") still misdescribes document clustering. R3 flagged the same error in the rule statement, and `2c4c8dd` corrected that; this bullet was missed. This item leaves the ADR as it is.

## Tests

The suites, all passing:
- `uv run --directory reconstruct pytest -q`: 460 passed (434 before, plus 26 new);
- `uv run --directory residual pytest -q`: 302 passed;
- `uv run --directory gapmap pytest -q`: 233 passed.
