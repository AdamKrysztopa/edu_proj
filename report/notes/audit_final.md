# Final audit (editorial authority), 2026-09-29

Scope: whole report in `main.tex` order, against `00_outline.md`, `revision_R1.md`, `revision_R2.md`,
`program_structure_R2.md` (MS1 = closure verdict, MS2 = config freeze, MS2b = H-OSS freeze).
Not touched: fig13/fig14/fig15 captions, `bibliography.bib`.
Build (scratch copy, `latexmk -r latexmkrc main.tex`): 150 pages, 0 undefined references, 0 undefined
citations in the final `main.log`.

## Primary-artifact checks (all matched)

- Closure own/control rates 0.889/0.961/0.958 with n = 54/51/48 (153 pairs): `research/n3/*/gapmap.json`
  `checks.mismatched_evidence_control.total`.
- "15 of 155 firings open": `checks.judge_lexical_confusion` (PLC 13, GDPR v1 2, GDPR v2 0; totals 56/51/48).
- 909 evidence items = 337 + 206 + 366; 1,169 claims = 375 + 271 + 523 (`reconstruct/runs/*/ledger.json`).
  `n_located` 337/204/351 from the sidecars.
- Module counts incl. `__init__.py`: residual 9 (1,281 lines), reconstruct 10 (4,803), gapmap 12 (2,986).
- Budget arithmetic in §25 (tranches, Phase/Program totals, MS4/MS5 money-at-risk, WP PM sums, pivot
  line, FTE averages) recomputed: consistent.
- Repeated numbers (418, 452, 1,169, 909, 71/71, 5/24, 19/24, 4.82, 107, 155, 268/416/172/311, 3 of 19,
  rho 0.91, decoy 7/20, delta 0.05, kappa 0.70, 45 + 6 experts, M-numbers): consistent across files after
  the fixes below.
- Every MS1/MS2/MS2b occurrence read in context: MS1 always the closure verdict, MS2 always the freeze.
  MS3 is never called an H2 verdict; "no inconclusive route" present in §17/§22.

## Fixes (file:line after edit — what — why)

Program consistency (stale design remnants)
- 21_domains.tex:63,64,68,69,144,147,153,158; 22_roadmap.tex:72-81,128; 23_workpackages.tex:43,46,176-186,
  204,242; 24_team.tex:163; 25_resources.tex:35,37,85,157,159,166,177; 26_risks.tex:71,75-76;
  I_programdetail.tex:36,39,122 — "V5b" -> "V5"; V5a (expert raters with decoys) removed from §21 D4,
  §22 S2 row, WP7 tasks/deliverables, tranche 2a scope, §26 recruitment row, App. I cost row and team row —
  V5a is dropped in the final program; there is one V5.
- 26_risks.tex:53-59; 21_domains.tex:54; 23_workpackages.tex:116; 25_resources.tex:175-177 — "pre-registered
  minimum"/"MS3 cannot read continue" with too few golds -> "fewer than three eligible golds; reported at
  MS2; MS3 rule unchanged, CONTINUE harder" — matches §17 V2 ("the MS3 rule does not change").
- F_glossary.tex:61-63 — E-CTA "secondary to E-OSS and unable, alone, to decide H2" (old R1-D2 logic) ->
  recast as pooled V2 that screens H2 at MS3.
- 18_platform.tex:37; 20_organizations.tex:132,147-149,156,163-165,177; H_weft.tex:34 — E-OSS as H2's
  "organizational analogue"/"best-powered test" and pointers to §22 -> H-OSS (V3, \cref{subsec:hoss}),
  a separate hypothesis that can neither support nor refute H2; §20 pilot now states it is V7, gated on
  MS5 CONTINUE and the deferred N2 validation.
- 10_n3.tex:11-12 — registered gate (E-CTA, E-OSS) now notes it is restructured as V2 and H-OSS.
- 15_threats.tex:35 — freeze order stated as "judge chosen at MS1 (V1); hash-freeze at MS2, before gold (V0)".
- 13_not_demonstrated.tex:18-20 — D2 "beats its fair control by at least 0.20" -> human agreement plus a
  pre-registered margin (V1) — MS1 uses a pre-registered margin, not the built-in 0.20 threshold.
- 00_executive_summary.tex:22-24; 29_conclusion.tex:33-34 — V1 sample "107 firings plus new units to reach
  at least 100 double-coded" -> 107 firings in both arms (214 units) plus about 100 units from one new
  domain — matches §17 V1 and program item 1.
- 00_executive_summary.tex:93-94; 29_conclusion.tex:43 — gate reader "reads each gate"/"authority over every
  gate" -> reads MS1, MS3, MS5; signs off owner exceptions at any gate — matches program item 14.
- 08_evolution.tex:38-39 — N2 verdict cell "gated arms never run (API budget)" -> D3 phrasing (Continue
  branch closed on the validity floor; gated arms of E-PLANT and E-ABST never scored).

Evidence and claims
- 20_organizations.tex:9-11 — 3 of 19 now carries its qualifiers (one adversarial AI reviewer, pre-final
  maps, in-sample, no human coder) — ruling on the precision figure.
- 20_organizations.tex:116-117 — uncited "documentation problems are a named barrier for newcomers" ->
  cited documentation-issues finding (aghajani2019software) plus an explicit "no onboarding study reviewed".
- 20_organizations.tex:139-140 — uncited "mature computational frame in process-mining conformance
  checking" removed; the no-public-corpus statement kept as "was found".
- 18_platform.tex:146-147 — contradiction analysis "coded, never run live" -> older pairwise stage ran in v1;
  current cross-verify never ran live (matches §9).
- 18_platform.tex:261-262 — broken sentence ("\evfut{} as an enforced rule, but binding…") rewritten.
- 25_resources.tex:130; 26_risks.tex:117 — "$5 limit below the run's own caps" / "$21 of caps still
  unspent" -> limit below the experiments' registered caps (about $21) — the $21 is the sum of caps, not an
  unspent balance ($4.82 was spent).
- B_lenses.tex:30 — paraphrase-as-quote trace pointed to §11; it is Trace 3 in App. C.
- B_lenses.tex:282-283 — lexicons "are frozen before any gold" -> hashed, not frozen; must be hash-frozen at MS2.
- 09_n2.tex:56-57 — E-LIVE caption explained only GDPR v2's evidence/n_located gap; now also GDPR v1 (206 vs 204).
- A_claims.tex:125 — closure rates rounded 0.89/0.96/0.96 -> 0.889/0.961/0.958 (numbers identical everywhere).
- 06_architecture.tex:63 — residual "Eight modules" -> nine counting `__init__.py`, as App. E and the other
  two packages count them.
- E_reproduce.tex:21 — instrument "~10 s" -> "~7 s" (E14: 7.34 s). E:147 — irrelevant row E19 reference
  dropped. E:152-153 — the 71/71 sample is the closeout's, not "this report's".

Acronyms (defined at first main-text use), spelling, prose
- 00:57,101 GDPR, ROC; 03:47 CI; 03:258-259 GDPR; 03:266 NLP; 03:376 LLM; 06:14 ADR; 10:163 EIG;
  17:217 NICU; 18:32 SOP; 20:9 ICO; 21:77 RCT; 21:80 FCI spelled out; 24:8 FTE; 24:111 HCI;
  23:180 CDM no longer re-defined; B:37 CTA no longer re-defined.
- A_claims.tex:97,117 — "mislabelling", "rationalisation" -> American spelling.
- 06_architecture.tex:138,144 — dangling `\evobs{}` at paragraph end moved to the start of its paragraph.
- 07_evidence_model.tex:70-71 — redundant "Reading claims.py, claims.py computes" fixed.
- 07_evidence_model.tex:112-114 — "This is not evidence that memorized content cannot enter" (broken logic)
  -> memorized content can enter, but only under a non-criterion label.
- F_glossary.tex — added H1/H2/H3 (pivot is not H3), H-OSS, MS1–MS8/MS2b; SESOI entry now lists delta,
  the 1.25 H3 ratio and Track A's futility test.

§6/§7 spot-check: the short-sentence rewrite reads cleanly apart from the two §7 sentences fixed above; the
§6 pipeline list and §7 label-rule list kept their meaning.
Executive summary and conclusion re-read against §§8–10, 13, 17, 22, 25 after the fixes: they agree.

## Left unresolved (owner of the fix in brackets)

- fig15 caption (23_workpackages.tex:22) still says "V5b's main study" -> should be "V5's". [figure agent]
- App. I participant-cost rows no longer include V5a; their sum is now about EUR 53k–356k against §25's
  "roughly EUR 55k–360k" (within "roughly"). Tranche 2a's 29–44 PM were not re-costed for the dropped V5a
  effort. [program owner, optional]
- Bibliography: citations for OSS newcomer barriers (e.g. Steinmacher et al.) and process-mining
  conformance checking would let those two claims return; biber warns on the ISBN of meyer2003threshold.
  [bibliography auditor]
- `\repo{report/...}` links (App. A, F, G; §18 table caption) point into `report/`, which is untracked in
  git, so they 404 until the report is committed. [owner]
- Pre-existing overfull boxes from long code tokens (largest 116 pt, §8 table; 55–60 pt in §6/§7). Cosmetic.
- §21 fallback paragraph (PLC used for V5 main if no fresh expert pool) leaves unstated what then decides
  H2; not changed because it is a design choice. [program owner]
- App. A E38 "all closure-uninformative" in the anti-renaming row reads oddly; reproduced from the audit
  note and left as is.
