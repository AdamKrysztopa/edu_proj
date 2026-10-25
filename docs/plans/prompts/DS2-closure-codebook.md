# DS2: Codebook anchors and κ benchmarks for "stated / partial / unstated"

**Branch:** `ds2-closure-codebook`
**Output:** `research/ds2-closure-codebook.md`
**Method:** the `research` skill, plus OpenAlex and web search. The note feeds I4's codebook, so read `research/n3_control_v3/RESULT.md` (I1c): sol marks many own arms partial, so in PLC it separates the arms on closed-or-partial (+0.43 [+0.19, +0.63]) but not on closed (+0.13 [−0.02, +0.28]). The gating split question below is live, but recommend the split from literature and codebook grounds only: I1c's split results are in-sample and are not evidence for it.

## Context
- `docs/plans/deep-search-queue.md` § DS2.
- `research/n3/README.md`, for the lenses and closure states.
- `docs/plans/n3-poc-lens-spec.md` §1.5, for the closure states.
- `report/sections/17_validation.tex`, the Phase 0 V1 labels and units.
- `research/spikes/jev/RESULTS.md`, for the per-sentence three-way question and its "topical relevance is not enough" rule.

## Questions
1. Which annotation schemes separate each of these pairs, and with which decision rules and anchor examples?
   - an element that is **stated** versus one that is only **topically related**;
   - **partial** versus **full** statement;
   - **seed** support versus **independent** support;
   - **retrieval failure** versus **absence**.

   Candidates: unanswerable-question annotation (SQuAD 2.0, Natural Questions "no answer"), NLI "neutral" vs "entailment", evidence-sufficiency and attribution annotation (AIS / attributable-to-identified-sources, FEVER "not enough info"), and claim-verification datasets.
2. What inter-annotator agreement do those tasks report, and on which split? Report κ or α with the source. That gives a realistic floor next to the proposed 0.70.
3. Which known failure modes apply here: annotator drift towards "partial", prevalence effects on κ, anchoring on the judge's answer?

## Done when
- The note gives a draft anchor rule and two worked anchor patterns (one positive, one negative) for each of closed, partial and open, for each lens type (DISC, DIAG, SEL, HEDGE, GUARD, WHY, RESULT). Paraphrase the patterns; do not quote any gold.
- It gives an agreement benchmark table with sources.
- It recommends the gating split (closed vs not; closed-or-partial vs open) and a κ floor, with the evidence for each.
- `citation-verifier` has passed on it.

## Decision it feeds
- I4's codebook, its κ floor and its gating split.
- **If the benchmarks show that comparable tasks rarely reach κ 0.70:** say so first. The owner must then decide whether MS1's floor stays (`AskUserQuestion`).
