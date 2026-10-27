# Gap-density survey: stopped at the cost estimate (2026-10-27)

**Question.** On dependence-forecastability (single owner, thorough docs), D1b's cheap closure judge
left only 7 of 35 fresh topics open in every version (gemma, validated on constructed checks only,
with G2 passed under a disclosed amendment). That is too few to test gap-map targeting
(`research/d1b_rerun/RESULT.md`). Does the open share differ across codebases (single owner vs many
authors, thin vs thorough docs)? Which codebase gives a later targeting test (D1c) at least 10
matched open and 10 matched covered topics per arm? Plan: `docs/plans/gap-density-survey.md`.

**Answer.** Not measured. The line's cap is $4.00. At D1's pipeline it covers no candidate. With a
single top-tier ledger it covers one at a time: antropy or modmrmr, not both ($6.65 together). The
brief required three, so no paid call was made.

One codebase costs about **$9.38** at D1's corpus size once both ledgers are priced complete. The
eight candidates' estimates run from $4.29 (antropy) to $12.54 (weft). No codebase has an open share
yet. No D1c codebase is recommended on data.

**Owner decision (2026-10-27).** The stop is accepted: the survey has no paid part, and ranking work
stays deferred to N3, per D1b's Change. turbo-design is excluded from any later study, because its
subject rests on conservation laws (`REORIENTATION.md` §18.1).

**Changed.** The $0 work settled four things:

- The comparison and the D1c-eligibility rule are fixed (plan §3, §4).
- A D1c codebase must be one the owner wrote.
- On the reference, a random judge passes D1b's floor where gemma does not. Passing the floor shows
  that the pool is big enough. It does not show that the judge reads the docs well.
- D1's top-tier ledger was recorded as complete. Only 41 of its 802 cross-verifications (5%)
  returned.

## How to read it

- **Illustration, not evidence**, as with D1 and D1b. No answers were collected and nothing feeds an
  N3 gate. It is not RQ-B evidence.
- **The reference count is a replay, not a rerun.** D1b's cached gemma closure states were read back
  with no model call. The replay covers every fired candidate of both D1 ledgers. It applies D1b's
  debris rule but not its D1-overlap filter or topic review.
- **The replay cannot host D1c.** It includes 14 of D1's 15 questions (Q7 falls to the debris rule),
  so it calibrates the rule only. Through `build_sheet.py count`, the same cache reproduces D1b's
  published 35 / 7 / 23 / 3.
- **The cheap judge alone settles nothing here.** The reference counts are gemma's only, because
  sol was never run on D1's full pool. Sol can only remove topics, so every bound is an upper bound.
- **The floor does not tell a judge from noise.** Two random judges were run at gemma's own
  version-level shares (31% open, 55% closed) on the two-ledger pool:
  - Drawing each version independently, it reaches 10 matched pairs on 77% of 300 seeds.
  - Drawing one state per topic, it reaches them on 98%. A 50/50 coin reaches them on 99%.
  - Gemma itself reaches 9 pairs.
  - Two independent random judges never reach the floor (0 of 300). That assumes the judges are
    independent. No comparator brackets a real, correlated pair.

  A D1c would need the closure judge re-checked on that codebase's own docs.
- **Joining the two ledgers lowers the bound through matching.** It raises the open count (16,
  against 13 and 14). But it splits the topics into strata by ledger set, and 7 of the 16 gaps find no
  partner. The bound is 9 pairs on both ledgers, against 11 and 12 on each alone.
- **Project docs, not outside pages, make the topics.** 69 of D1's 75 topics come from the project's
  own docs. A thin codebase therefore yields few topics whatever its open share.

## Figures

**The reference, dependence-forecastability** (gemma closure from D1b's cache, $0;
`reference_d1.json`)

| Pool | Topics | Open in every version | Closed | Mixed | Open share | Matched pairs, upper bound | Random judge (per version) reaches 10 |
|---|---|---|---|---|---|---|---|
| D1b's published pool (D1-overlap filter, topic review) | 35 | 7 | 23 | 5 | 0.20 | 3 | — |
| Both ledgers, debris rule only | 75 | 16 | 42 | 17 | 0.21 | 9 | 77% |
| Top-tier ledger alone | 37 | 13 | 16 | 8 | 0.35 | 11 | 41% |
| Cheap ledger alone | 57 | 14 | 35 | 8 | 0.25 | 12 | 56% |

**The candidates** (estimates only; plan §2, `estimate.json`)

| Codebase | Authorship | User-facing doc files (KB) | Project chars in corpus | D1 pipeline, USD | Top-tier ledger only, USD | Eligible by authorship |
|---|---|---|---|---|---|---|
| modmrmr | owner | 5 (34) | 31 K | 4.96 | 3.57 | yes |
| statmate-ai | owner | 27 (306) | 175 K | 11.75 | 8.45 | yes |
| sciagent | owner | 21 (320) | 175 K | 11.76 | 8.45 | yes |
| weft | owner | 48 (1,686) | 192 K | 12.54 | 9.01 | yes |
| turbo-design | fork of nasa/turbo-design, top author pjuangph (0.98 of commits); conservation content | 25 (54) | 44 K | 5.59 | 4.01 | excluded |
| antropy | 13 humans, top 0.82 | 3 (17) | 17 K | 4.29 | 3.08 | no |
| pmdarima | 24 humans, top 0.75 | 27 (92) | 75 K | 7.00 | 5.03 | no |
| tsfresh | 103 humans, top 0.33 | 30 (112) | 99 K | 8.14 | 5.85 | no |

Doc sizes count the project's own documentation files at the pinned commit. Docstrings are excluded,
as in D1. Authorship, stars, repository size and parent come from `inventory.json`.

The estimates scale D1's measured spend by truncated characters. The top-tier ledger prices every
attempted call at its task's mean paid cost. Its decoys had no paid call, so they are priced from D1's
cheap decoys, scaled by the extraction-cost ratio. The cheap ledger's missing cross-verifications were
never attempted; they are priced by scaling with claim counts.

This repricing matters for the top-tier ledger. 761 of its 802 cross-verifications, 32 of its
verifications and all 30 decoys ended in `api_error`. A complete top-tier ledger is therefore about
$6.29, not the $3.95 it spent. The estimates are upper bounds on corpus size, not on prices.

## Cost

$0.00. No OpenRouter or OpenAI model call was made. The inventory read public GitHub metadata, and
the reference replayed cached closure states. The headroom check read the key's limit and the
account balance (`headroom.json`). As with D1b, none of these figures are in
`research/results_manifest.json`, which this line may not write.
