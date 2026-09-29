# Revision decisions after Review Round 1 (orchestrator, binding)

Inputs: `review_A.md` (scientific: C1–C2, M1–M14, m1–m24, Cuts) and `review_B.md` (technical: B1–B7,
minor findings, number-check table, shortening list). Accept all findings unless a decision below says
otherwise. Read the findings that touch your files in full; the reviewers give exact locations and fixes.
Reviewer findings are claims too: if you check an artefact and a finding is wrong, keep the text and say
so in your final reply.

## Decisions that must read identically everywhere

D1 (C1, absence check wording). Never say or imply that the absence check found a missing element
"stated nowhere" / "absent from every source". Correct wording: "the lens fired; the absence check found
the element at most partly stated". Facts: of the 16 displayed candidates, 13 are `partial`; the two
`open` DIAG records carry 5 and 6 partial rival hits (the code counts a partial rival as unsigned); only
1 of 16 has no partial hit (verify which, from gapmap.json, before naming it).

D2 (C2, the deciding gate MS3). Use these rules verbatim in substance wherever MS3/V2/V3/V5 appear:
- With one CTA gold and δ = 0.05, V2 (E-CTA) cannot stop H2; it is inconclusive by design.
- MS3 combination rule (pre-registered): V3 (E-OSS) is primary, V2 secondary. MS3 can reach STOP only
  through V3, and only if V3's 5-departure pilot shows enough departures for the planned precision.
- The most likely MS3 reading in the lean program is INCONCLUSIVE. Say so where the lean program is sold.
- Terminal rule: a second inconclusive MS3 reading ends H2 as a funded claim; the program then takes the
  interview-only pivot.
- V5 (blind prospective elicitation, the expensive human study) starts only on CONTINUE, or on a
  pre-registered minimum: lower 90% bound of ΔAUROC > −δ/2 AND point estimate ≥ δ. Never on "any
  positive point estimate".
- The lean program buys: the closure verdict (MS2), the V3 feasibility/power decision, and a V3 reading if
  feasible. It does not buy a guaranteed H2 decision.
- Delete "powered to detect the absence of that margin"; replace: "it can show that the margin is absent
  only when enough areas exist (about 150 per class for δ = 0.05); a single CTA gold cannot."

D3 (M4, N2 verdict — one phrasing): "N2's registered research verdict is INCONCLUSIVE: E-PLANT's Continue
branch closed on the validity floor (a_U = 5/24 < 8), and the gated arms of E-PLANT and E-ABST were never
scored. Separately, the engineering milestone is complete." Never "failed", never "passed".

D4 (B1, spans). "Every evidence item carries an exact span re-sliced from the fetched snapshot (the full
check `reconstruct.verify_run` passes on all 909 evidence items from the local snapshots; a manual sample
re-sliced 71 of 71). Extractions whose quote cannot be located stay in the ledger labeled
`synthetic_extrapolation` (452 of 1,169 claims across the three runs; 305 of 523 in GDPR v2) and can never
act as a criterion." Remove "every claim is tied to an exact span" and "memorized content cannot enter as a
claim" (it can enter, labeled synthetic). Verify the 909 / 452 / 1,169 / 305 / 523 numbers against
review_B.md's evidence before use.

D5 (B2). Lenses, anchors and some question quotes run on the extractor's paraphrase (`assertion`), not the
verbatim span. State this in §10 and as a construct-validity threat. Fix Trace 3 ("Sources prescribe").

D6 (B3, counts). Report both: HYP after merge PLC 24 / GDPR v1 1 / GDPR v2 6; shown after the display cap
(12 total, 3 per lens, 4 per area) 9 / 1 / 6. "13 of 16 partial" describes the displayed set: say so.
Area scores in the validation program must use the uncapped set.

D7 (M6/B4, area score). The decisive tests rank AREAS; the code produces claim-level candidates and no area
score. The validation program must define, pre-register and build an area score before MS1 (e.g. a
pre-registered aggregation — max or noisy-OR of candidate scores over the uncapped set within an area —
chosen on pilot data only). This is FUTURE WORK and a build item in the relevant WP.

D8 (M1, fair control). Describe precisely: the judge's closure rate is the same whether it sees the
candidate's own evidence or swapped evidence (0.889/0.961/0.958 counting `partial` as closed); in 32 of
153 pairs both arms sent an identical prompt; on closed-only rates the conclusion still holds. Do NOT say
"the closures come from the seed's own text". Say: "the judge's verdict does not depend on which evidence it
is shown, so it is not yet an informative absence check."

D9 (M2). Attribute correctly: the fair-control check is built into `gapmap/checks.py` and raised the
`closure-uninformative` flag; the precision tally and the parsing defect came from an adversarial AI review.
No "the PoC found this for itself" without that split.

D10 (M5). ClashEval's >60% adoption comes from a setting where the planted document was the only retrieved
context; E-PLANT mixed each plant with ~12 true pages. The low baseline (5/24) may reflect the design, not
model robustness. Say so wherever the expectation appears.

D11 (M9). Order: choose the judge at MS2, THEN hash-freeze the config (lexicons, thresholds, judge, area
score), THEN acquire gold. Fix any schedule that freezes before the judge is chosen.

D12 (B7). Appendix E uses the replay command sequence from review_B.md that was run and reproduced all three
maps byte-identically; the config is "hashed, not frozen; tuned in-sample on the same three ledgers".

D13 (B5). Do not showcase the GDPR v2 run as the example of a clean run (it is not N3-admissible: 140
pending verdicts). State that the post-fix cross-verify and current decoy stages never ran live.

D14 (hypotheses). H3 must be stated so that a null result counts against it (M3); keep EIG selection and
breadth ranking distinct.

D15 (M13). Add the requirements-engineering tradition (automated incompleteness / tacit-knowledge detection in
requirements) to §3 and §4's closest work, briefly, ONLY with sources you verify (Crossref/OpenAlex) and add
to `report/bibliography.bib` (append; keep the file's style; no duplicates).

## Cuts (target main body ≈ 90 pages from ≈ 121)

Adopt review_A.md "Cuts" items 1–13 and review_B.md's shortening list, with these changes:
- Keep the user-mandated sections separate (do NOT merge §5/§8, §12/§13 or §27/§28); compress them instead.
  §12 becomes ≤ 1.5 pages (6-row table pointing to App. A IDs); §8 ≤ 1 page; §27 and §28 ≤ 1 page each.
- Weft subsection moves to a new appendix `sections/H_weft.tex` (\label{app:weft}); §18 keeps a 3-sentence
  summary pointing to it.
- Product-team and funding-instrument tables move to a new appendix `sections/I_programdetail.tex`
  (\label{app:program}).
- Traces 2 and 3 move to Appendix C (`C_records.tex`); §11 keeps Trace 1 (corrected per D1, m7) and the
  failure trace.
- Module inventories, determinism/budget detail and frozen-schema detail move to Appendix E.
- Numbers-once rule: each headline number appears in its home section (closure: §10; omission: §1; budget:
  §9; Rigby/Avelino: §20 or §21, whichever keeps the full statement; blind-spot studies: §3), plus the
  Executive summary and Conclusion. Elsewhere, refer with \cref and no number.

## Page budgets after revision (main body)

Summary 2 · §1 2.5 · §2 1.5 · §3 6 · §4 4 · §5 1.5 · §6 3 · §7 2.5 · §8 1 · §9 3.5 · §10 5 · §11 2.5 ·
§12 1.5 · §13 2 · §14 2.5 · §15 2.5 · §16 2.5 · §17 9 · §18 5 · §19 2.5 · §20 3 · §21 2.5 · §22 2.5 ·
§23 4 · §24 2.5 · §25 2 · §26 2.5 · §27 1 · §28 1 · §29 1  ≈ 92.

## Mechanics

- Edit only your assigned files. Keep labels stable (other sections \cref them). If you delete a labeled
  table/figure, keep the label on the nearest remaining element or tell the orchestrator.
- After editing, compile in a scratch copy: `rsync -a --exclude build --exclude notes report/ $SCRATCH/rev/`
  then `latexmk -r latexmkrc main.tex` there (SCRATCH = /private/tmp/claude-501/-Users-adamkrysztopa-projects-edu-proj/a76e7540-362d-4468-812a-bcef55968299/scratchpad/<your-name>). Fix any error you introduced.
- Final reply ≤ 200 words: findings applied (IDs), findings rejected with reason, new page counts.

## Corrections to decisions (verified by R-d)
- D4: 452 of 1,169 = synthetic_extrapolation + unknown. Synthetic alone = 418 (PLC 49 / GDPR v1 64 / GDPR v2 305).
- M1: own rate is 1.0 on 11 of 14 lens–ledger cells.
- Lexical null bounds are a 5–95% interval.
- D1: the only displayed candidate with no partial hit is PLC rank 7 (WHY, g-57de0e58c067).
- D6: PLC 32 HYP before merge → 24 after merge → 9 shown after the display cap.
