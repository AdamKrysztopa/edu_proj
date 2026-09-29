# Review A (scientific), Round 1

Reviewer A. Scope: research logic, methodology, literature positioning, unsupported claims,
novelty, interpretation of N2/N3, threats to validity, internal consistency, length.
Read: BRIEF.md, 00_outline.md, main.tex, sections 00 to 29 and A to G; checked against
`research/n2/*`, `research/n3/*`, `gapmap/src/gapmap/*`, `reconstruct/runs/*/sidecar.json`,
`docs/architecture/decisions/0008*`, the bibliography, arXiv, OpenAlex and Crossref.

**Counts:** 2 CRITICAL, 14 MAJOR, 24 MINOR.

**Overall.** The report is careful with evidence labels, and it is honest about the negative
N3 result. The chain from problem to RQ-B to H1/H2/H3 to PoC to validation is coherent. Four
kinds of problem remain:

1. In several places the report states that the absence check found the missing element
   "stated nowhere". That is exactly the claim it says it cannot make.
2. The central negative result is described with more precision, and a firmer mechanism, than
   the control supports.
3. As designed, the deciding gate (MS3) will very probably read "inconclusive". The lean
   program is sold as the investment that "reads" that gate.
4. The same facts are repeated in up to 10 sections. The report can lose about 30 to 35 pages
   without losing substance.

**Reviewer replay (new evidence).** I replayed the fair control offline from the committed judge
caches (`research/n3/*/closure_judgements.json`) with the package's own functions (`semantic.retrieve`,
`checks._nearest_other`, `semantic.judge_retrieval`, `CachedJudge(live=False)`). No network call and
no live model call was made. The replay reproduces the committed own rates exactly (PLC 48/54 =
0.889). The script is `scratchpad/ctrl_pair.py`, not committed. Findings M1 and C1 use it. If the
owner wants these numbers in the report, the paired statistics should first be added to
`checks.py` output and committed, so that they cite a repository artifact.

---

## CRITICAL

### C1. The report says the absence check found the element "stated nowhere", but the records say otherwise

**Locations:**
- `04_approach.tex:131-133`
- `01_problem.tex:142-147`
- `20_organizations.tex:22-26`
- `11_demonstrations.tex:13-15, 37-43`
- `10_n3.tex:250-252` (softer)

**Problem.** Section 4 defines a gap candidate as "at least two independent sources discuss the
attested side and **none states the missing element**". Section 1 and Section 20 say of the PLC
GUARD record that "no source in the corpus says how a troubleshooter is supposed to notice the
drift". Trace 1 calls its `open` state "the strongest of the three states" and says the judge
"found none stating a discriminating sign".

All three statements treat the absence check as a working instrument. Every one of them is
contradicted by the committed records.

**Evidence** (`research/n3/*/gapmap.json`, `map[*].inferred_gap`):
- (a) HYP is assigned by `record.categorize` whenever the state is `partial` or `open` and
  `k_topic ≥ 2`. A partial state means the judge found part of the element. 13 of the 16 HYP
  records are `partial`.
- (b) The GUARD record (PLC rank 9) is `partial` with 1 partial hit.
- (c) The two PLC DIAG records reported as `open` carry 5 and 6 `partial_hits`. Trace 1's own
  `judge_reason` says "Sentences 1 and 4 partially address the distinction".
  `semantic._judge_diag` counts a rival as unsigned whenever its state is not `closed`
  (`unsigned = [r ... if per_rival[r].state != "closed"]`). A DIAG group is therefore `open`
  even when every rival is partially signed.
- (d) Only 1 of the 16 HYP records has zero partial hits: PLC rank 7, WHY, `k_topic` 3.

The report's "3 open" candidates are really 1 open and 2 DIAG groups built from partial rivals.
The report also says, correctly, that the absence check is uninformative. Even so, none of these
"stated nowhere" sentences is licensed.

**Fix:**
- `04_approach.tex:131-133`: replace with "A **gap candidate** means at least two independent
  sources discuss the attested side, and the absence check did not mark the missing element as
  fully stated (its state is open or partial; in the PoC, 13 of 16 candidates are partial, that
  is, the judge found part of the element)."
- `01_problem.tex:145-147`: replace with "the sources name the failure mode; the absence check
  found at most a partial statement of how a troubleshooter notices the drift (state:
  \code{partial})."
- `20_organizations.tex:23-24`: make the same change.
- Trace 1 (`11:39-41`): replace with "Of 34 verified sentences retrieved, the judge found none
  that fully states a discriminating sign for any of the 5 rival causes; it marked 5 claims as
  partial. DIAG treats a partially signed rival as unsigned, so the group reads \code{open}."
- Delete "the strongest of the three states a candidate can reach" (`11:14-15`).
- `10_n3.tex:191`: add a row or note: "of the 3 open records, the 2 DIAG groups rest on partial
  rivals; 1 record (WHY) has no partial hit."

### C2. As designed, the deciding gate (MS3) cannot reach "stop" and will very probably read "inconclusive"

**Locations:**
- `00_executive_summary.tex:88-106`
- `02_question.tex:96-108`
- `17_validation.tex:83-115, 207-209, 232-236, 256`
- `22_roadmap.tex:54-58, 189-196`
- `23_workpackages.tex:138-144`
- `25_resources.tex:214-217`
- `29_conclusion.tex:36-40`

**Problem.** The report's own power arithmetic makes the falsifier practically unreachable in
the lean program:
- V2 (one CTA gold, 15 to 25 areas) is "inconclusive by design" (`17:112-113`).
- V3's effective n is the number of departures, and V3 becomes "descriptive" if too few exist
  (`17:232-236`).
- With δ = 0.05, a stop needs about 150 areas per class (`17:103`).

So MS3 most likely reads inconclusive. The report does not say this where it sells the lean
program ("reads the deciding gate", Exec summary, 25:214-217, 29:38-40).

Further, the gate logic has three open ends:
- (i) `17:87-88`: "inconclusive: one pre-registered fallback runs, and the same rule applies
  again". No terminal rule exists for a second inconclusive reading.
- (ii) V5, the expensive human study, starts on "inconclusive with a positive point estimate"
  (`17:256`, `29:36`). That lets a null result proceed.
- (iii) "MS3 reads V2 and V3 together" (`22:189-190`, `23:139`), but the rule for combining
  them (V2 inconclusive plus V3 continue? disagreement?) is not stated.

`02_question.tex:96-99` also claims the test "is powered to detect the absence of that margin".
That contradicts `17:107-108`: "It cannot show that a small gain is absent."

**Evidence:** the report's own numbers at `17:99-115` and `17:232-236`. I re-checked the
Hanley–McNeil arithmetic: the ±0.14 / ±0.10 / ±0.06 / ±0.05 figures are correct for AUROC
0.70 vs 0.62 and r = 0.5.

**Fix:**
- (1) In the Exec summary and §17, state plainly: "With one CTA gold and δ = 0.05, V2 cannot
  stop H2. MS3 can reach a stop only through V3, and only if the 5-departure pilot shows that
  enough departures exist. The most likely MS3 reading in the lean program is inconclusive."
- (2) Add a terminal rule. Proposed: "A second inconclusive reading at MS3 ends H2 as a funded
  claim; the program then takes the interview-only pivot."
- (3) Make V5 start only on Continue, or on a pre-registered minimum lower bound (for example
  lower 90% bound > −δ/2 and point ≥ δ). Do not start it on any positive point estimate.
- (4) Pre-register the MS3 combination rule: V3 primary, V2 secondary; or a pooled
  random-effects ΔAUROC with a stated weight.
- (5) Delete "powered to detect the absence of that margin" from `02:98-99`. Replace with "and
  it can show that margin is absent only when enough areas exist (about 150 per class for
  δ = 0.05); a single CTA gold cannot."
- (6) Make the lean program's value claim match this. It buys the closure verdict (MS2), the V3
  power decision and a V3 reading if one is feasible. It does not buy a guaranteed H2 decision.

---

## MAJOR

### M1. The headline control result is described more precisely than the control allows

**Locations:**
- `10_n3.tex:87-111` and the fig. 8 caption at `10:101-104`
- `14_interpretation.tex:21-27`
- `A_claims.tex:125` (E36)
- `08_evolution.tex:57-61`

**Problem.** Four problems:
- (a) The report says the judge's closures "track the seed's own text". The same JSON shows
  that the other-source-only arm (seed and same-source sentences removed) still closes or
  partially closes 0.667, 0.725 and 0.708 of candidates. The mechanism is not established. The
  pattern equally fits a lenient judge that says closed or partial for almost any topical text:
  a ceiling effect, since own rate is 1.0 on 10 of 13 lens-ledger cells.
- (b) In 32 of 153 control pairs (PLC 8, GDPR v1 11, GDPR v2 13), the own and control prompts
  were byte-identical (reviewer replay). Either the candidate had no other-source sentences, or
  the neighbor's other-source sentences were the same. For these pairs, equality holds by
  construction.
- (c) The control statistic counts `partial` as closed (`checks._closed_or_partial`). Triage
  keeps `partial` as HYP. The control therefore tests a different decision from the one that
  builds the map.
- (d) Equal marginal rates are weak evidence. The paired decision is what matters.

**Evidence (reviewer replay, from committed caches):**
- Paired closed-or-partial agreement between arms: 48/54 (PLC), 51/51 (GDPR v1), 48/48 (GDPR v2).
- Closed-only own vs control rates:
  - PLC: 16/54 = 0.30 vs 18/54 = 0.33
  - GDPR v1: 33/51 = 0.65 vs 31/51 = 0.61
  - GDPR v2: 28/48 = 0.58 vs 25/48 = 0.52

The conclusion "uninformative" survives: every difference is far below the 0.20 bar. The
framing "exact equality on every lens" and the seed-text mechanism do not.

**Fix.** After `10:96`, add:
"Three qualifications. First, in 32 of the 153 pairs the two arms gave the judge the same
prompt, so equality there holds by construction. Second, the rate counts partial as closed,
while triage keeps partial candidates; counted on closed alone, own versus control is 0.30/0.33,
0.65/0.61 and 0.58/0.52, still far below the 0.20 difference the check requires. Third, the
judge's own rate sits at 1.0 on most lenses, so the test has little room to separate the arms."

Then:
- Fig. 8 caption and `14:25-27`: replace "tracks the seed's own text" with "does not depend on
  which candidate's other-source evidence is shown."
- Relabel the fig. 8 x-axis "closed-or-partial rate".
- E36: replace "whether or not the evidence is on-topic" with "whether it is shown this
  candidate's or the topically nearest candidate's other-source evidence".

Before any of these numbers enter the report, commit the paired statistics to `checks.py`
(outside `report/`, so this is an owner action).

### M2. Spin: "the PoC found this for itself"

**Locations:**
- `12_demonstrates.tex:20-28`
- `10_n3.tex:250-251` ("its own checks caught its own central failure")
- `27_contributions.tex:75-76`
- `29_conclusion.tex:22-23` ("The PoC's own built-in control found this")

**Problem.** The fair control was built after an external adversarial review (Opus) found the
failure. The first built-in control was a straw man that "passed" at 41% against 2%. The
judge-parsing defect was also found by review, not by the tests. The report says as much itself
at `15_threats.tex:68-77`, which contradicts the sections listed above.

**Evidence:**
- `research/n3/README.md` status paragraph: "An Opus adversarial review found two problems:
  its absence-detection step … does not beat a fair control".
- `gapmap/src/gapmap/checks.py:157-160` docstring: "the first version was a straw man …
  rewritten after the second adversarial review".
- `D_defects.tex` L6 and L7.

**Fix.** Replace each claim with: "An adversarial review found the weakness; the fair control
now built into every map confirms it and is re-run on every replay." In §12, change "The most
useful result is a negative one that the PoC found for itself" to "The most useful result is a
negative one, found by adversarial review and now carried as a built-in check."

### M3. H3 is stated so that a null result counts as support, and it mixes up two selection methods

**Locations:**
- `02_question.tex:58-62`
- `17_validation.tex:325, 342-347`
- `22_roadmap.tex:192-194`

**Problem.**
- H3 reads "recovers the same amount … per expert hour … **or more**". That is a
  non-inferiority claim. A null result would satisfy it. The test in V6, however, is a
  superiority test with a smallest effect of interest of 1.25. The hypothesis and its test
  disagree.
- H3 is about "prioritized questions", which in the PoC means breadth ranking. V6 and the pivot
  test selection by expected information gain (EIG), which is not built. Under the pivot, EIG
  runs "without any reconstruction prior". The report does not define the hypothesis space or
  prior that EIG would then use.

**Fix:**
- `02:58-62`: replace with "**H3 — Prioritized questions reduce expert time.** Questions chosen
  from the gap map recover at least 1.25 times as many validated, previously unwritten items per
  expert hour as an untargeted interview of equal length (smallest effect of interest fixed
  before data)."
- In V6, state which selector is tested: breadth ranking, EIG over the gap map, or both.
- For the pivot, state what EIG conditions on: for example, a type prior from other golds plus
  the expert's own earlier answers.

### M4. The report gives three different, incompatible readings of the N2 verdict

**Locations:**
- `08_evolution.tex:50-56`: "a **genuine negative result**, not an unfinished task"
- `09_n2.tex:170-171`: "Neither floor failure is a finding about reconstruction quality"
- `09_n2.tex:210-211`: "N2 closed inconclusive **for a budget reason, not on evidence**"
- `17_validation.tex:146`, `18_platform.tex:381-383`, `25_resources.tex:66-67`: "a provider
  limit, not a result, stopped N2"

**Problem.** The registered reading is INCONCLUSIVE. E-PLANT's Continue branch was closed by the
validity floor (5 < 8). That is a result about the test's sensitivity, not a finding about
gating, and not a budget event. The budget only stopped the gated arms and E-LIVE v3.

**Evidence.**
- `research/n2/closeout.md`: "the registered INCONCLUSIVE readings stand"; "Continue closed" by
  the floor.
- `e_plant_eabst_report.md:128`: the baselines "resisted the failure each gate was built to catch".

**Fix.** Use one sentence everywhere: "N2 reads INCONCLUSIVE. The E-PLANT baseline adopted too
few plants (5 of 24, floor 8) for the test to detect a gating benefit, which closes Continue by
the registered rule; the budget limit then stopped the gated arms and the post-fix live check."
- In `08:50`, delete "a genuine negative result".
- In `09:210-211`, replace "for a budget reason, not on evidence" with "partly for a budget
  reason: the floor failure closed Continue, and the budget stopped the remaining arms".

### M5. The ClashEval ">60%" expectation was carried over to a condition it does not cover

**Locations:** `09_n2.tex:136-140`; `D_defects.tex:84` (R1)

**Problem.** The report presents the registered ">60%" adoption expectation as borrowed from
planted-evidence work (`wu2024clasheval`), and never says that ClashEval's condition differs.

**Evidence.** I verified the ClashEval abstract (arXiv 2404.10198). "LLMs are susceptible to
adopting incorrect retrieved content, overriding their own correct prior knowledge over 60% of
the time" holds for six 2024 LLMs, over 1,200+ QA items. In that setting the perturbed document
is the model's retrieved context and no competing correct document is present. The same
abstract also reports that adoption falls as the edit becomes less realistic and as the model's
prior confidence rises.

E-PLANT placed each plant among about 12 real pages per domain that state the truth
(`docs/n2-eplant-eabst-protocol.md` §1). The 5/24 result is therefore not surprising, and the
validity floor (⌈n/3⌉, "about half the >60% expectation") was derived from a condition that did
not apply.

**Fix.** After `09:140`, add: "ClashEval's figure comes from a setting where the modified
document is the model's only retrieved context; E-PLANT shows each plant among about 12 real
pages that state the true value, a condition ClashEval did not test. The floor derived from
that figure was therefore miscalibrated." Also move this point into the "What N2 taught us"
lesson at `09:221-228`.

### M6. The gap map produces claim-level candidates, but the program scores areas, and the step between them is not defined

**Locations:** `17_validation.tex:75-81, 185-211, 297`; `16_residual.tex:45-52`

**Problem.** The PoC emits 9, 1 and 6 claim-level gap candidates per ledger, ranked by a
breadth rubric. Every validation test is an area-level AUROC. The report never defines how a
gap-map score per area is computed: maximum breadth, number of candidates, share of lens
firings, or something else.

With 1 to 9 candidates spread over 15 to 25 areas, most areas would score 0. AUROC would then
be dominated by ties, and a GDPR-v1-like ledger (1 candidate) could not rank anything. This is
also a researcher degree of freedom that must be fixed before any gold is seen.

**Fix.** Add to "Rules common to every study":
"Area score: pre-registered as [function], computed from all lens firings, not only HYP
records, with ties broken by [rule]; the share of zero-score areas is reported. A map in which
more than X% of areas tie at zero is registered as uninformative for that gold."
Also add "area-scoring function" to the MS1 freeze list.

### M7. E-CTA measures reconstruction misses, not the Human Knowledge Residual

**Locations:** `17_validation.tex:185-193`; `16_residual.tex:54-59`

**Problem.** Section 16 correctly splits H \ R into H \ E (the residual) and (H ∩ E) \ R
(reconstruction misses). V2, however, defines an area as "missed if it holds at least one
important gold item the reconstruction lacks", which is relative to R, not E. A gap map
computed from R that predicts where R is incomplete is partly circular: thin retrieval produces
both retrieval gaps and gold misses. So V2, as written, does not test H2 as the report defines
it.

V5, by contrast, correctly requires "absent from the frozen reconstruction and the dated
corpus".

**Fix.** In V2's design, add: "Each gold item the reconstruction lacks is checked against the
dated corpus E under the V1 codebook. An area is *residual-present* only if it holds an
important item absent from E; items present in E but missed by R are scored separately as
reconstruction misses. The primary outcome is residual-present."
State that this needs the V1 absence judgment to have passed. If it did not, V2 can test only
"predicts reconstruction misses", and it must be registered as that narrower test.

### M8. V1 sizes its sample for κ as if "not stated" were as common as "stated", but the PoC shows 0.89–0.96 stated; its binary split also differs from triage

**Location:** `17_validation.tex:153-181`

**Problem.** Three problems:
- (a) V1 plans for κ ≈ 0.70 with chance agreement 0.50 (±0.10 at 200 units). The PoC's own
  prevalence of "closed or partial" is 0.89 to 0.96. With chance agreement around 0.8, κ = 0.70
  needs observed agreement of about 0.94. The 95% half-width at 200 units is then about ±0.17,
  not ±0.10. V1 is underpowered by roughly a factor of three. The report mentions the prevalence
  paradox (`17:93-94`) but does not use it.
- (b) The primary split, "not stated" vs "partly or fully stated", matches the control statistic
  but not triage, which keeps "partial" as HYP (see C1 and M1). A judge that passes V1 can still
  mis-triage every partial.
- (c) There are 155 PoC firings. "About 200 units per arm" therefore needs about 45 or more
  new-domain units. The report also requires the judge to pass on the new domain separately
  ("a judge that passes only on the PoC ledgers is not adopted"). At about 50 units, κ has a
  half-width of about ±0.20, which cannot establish ≥ 0.70.

**Fix:**
- Replan the sample size using the observed prevalence.
- Score all three states (weighted κ or Krippendorff's α, ordinal).
- Make the gating split match triage (closed vs not closed).
- Stratify sampling to enrich "not stated" units.
- Give the new domain its own sample size (about 150 units, or state that new-domain results
  are descriptive).

### M9. The configuration is frozen at MS1 (M5), before the judge is chosen at MS2 (M10)

**Locations:**
- `23_workpackages.tex:36-39, 57-59, 78-81`
- `17_validation.tex:61-65, 179-181`
- `29_conclusion.tex:32-33`

**Problem.** WP2 freezes the gap-map configuration by M4, and MS1 (M5) requires "configuration
hash-frozen". V1 then adopts a judge, or drops closure, at M10. Changing the closure judge
changes the configuration, so the MS1 freeze either blocks V1's outcome or is broken by it. The
conclusion puts "hash-freeze" after the closure decision (`29:31-33`), which contradicts the WP
schedule.

**Fix.** Split the freeze into two:
- MS1 (M5) freezes lexicons, lenses, thresholds and the area-scoring rule.
- MS2 (M10) re-freezes with the adopted judge, or with closure dropped, before any V2/V3
  reconstruction runs (WP4 M11).

State that both freezes precede gold acquisition.

### M10. E-OSS is not a test of the current gap map

**Locations:** `17_validation.tex:213-238`; `20_organizations.tex:146-158`; `21_domains.tex:51-55`

**Problem.** V3 is called "the best-powered retrospective test" of H2. The lenses, however,
were built for expert procedural prose: judgment terms, rival causes, hedged rules. V3's unit is
a code unit, and its evidence is commits, blame, issues and reviews. It is not specified how the
seven lenses fire on code or commit text, and a new World B Git adapter is required. What V3
would test is a new instrument ("artifact coverage"), not the frozen PoC gap map.

The outcome, "rationale-seeking issues and defect-fix commits", is a proxy for knowledge loss.
Its link to the HKR (knowledge practitioners hold and use that E lacks) is not argued.

**Fix.** Add to V3:
- a statement of which lenses apply to code artifacts and how (for example WHY on commits
  without a linked rationale; RESULT on tests without documented expectations);
- that lens adaptation is part of the MS1 freeze;
- that V3 tests "artifact-coverage gaps predict realized knowledge loss", a construct adjacent
  to the HKR.

Reword "best-powered test of H2" as "best-powered test of the organizational analogue of H2".

### M11. Rigby et al. 2016 is misquoted in three sections

**Locations:** `01_problem.tex:165-167`; `20_organizations.tex:125-127`; `28_impact.tex:52-53`

**Problem.** The report says "turnover-related knowledge losses run at more than three times the
expected level".

**Evidence.** The abstract (DOI 10.1145/2884781.2884851, verified via OpenAlex) says "projects
are susceptible to losses that are more than three times larger than the expected loss". That is
a tail-risk (value-at-risk style) statement about the historical loss distribution, in two
projects (Chrome, and one project at Avaya). It is not a statement about the typical loss level.

**Fix.** Replace with: "in two large projects, worst-case turnover losses reached more than three
times the expected loss \parencite{rigby2016quantifying}, and a replication found more severe
extremes \parencite{nassif2017revisiting}."

### M12. The expert blind spot is overgeneralized as "grows with expertise"

**Locations:** `01_problem.tex:117-120`; `19_education.tex:30-34`; `03_foundations.tex:140-147`

**Problem.** "More expertise makes the misjudgment worse, not better" (§1) and "The blind spot is
general, and grows with expertise" (§19) are stated as established literature. The evidence does
not support that:
- Nathan & Petrosino (2003) is about preservice teachers, and the variable is advanced
  mathematics coursework (N = 48).
- Maries & Singh (2016) report instructors *no better* than TAs, not worse. Its abstract (DOI
  10.1103/physrevphyseducres.12.010131) concerns graduate TAs only, and says TAs "are more
  accurate … than random guessing". §19 calls 65% versus 40% "only slightly above" chance.
- Hinds (1999) finds intermediates best on one prediction task.

**Fix:**
- §1: replace with "Experts do not just omit their own principle-selection step; in these
  studies they also misjudged which steps novices find hard, and more expertise did not help."
- §19 heading: replace with "The blind spot recurs across settings."
- Delete "only slightly".
- Check in the full text of Maries & Singh 2016 that instructors were part of that study. If
  not, cite the instructor comparison's own source.

### M13. A directly relevant tradition is missing: automated incompleteness and tacit-knowledge detection in requirements engineering

**Locations:** `04_approach.tex:13-69` (traditions), `04:202-224` (closest work),
`tab:novelty` row "Methodology lenses as absence detectors"

**Problem.** Requirements engineering has more than ten years of work on detecting, from text,
where a document is incomplete or where tacit knowledge hides. This is the closest analogue to
"lenses as absence detectors". The report cites Gervasi et al. 2013 only as a taxonomy.

`luitel2024improving` is in `bibliography.bib`, and `notes/03_novelty.md` rates it "Medium"
closeness, but the report text never cites it. Ferrari, Spoletini & Gnesi 2016 (ambiguity as a
cue to tacit knowledge in elicitation interviews; DOI 10.1007/s00766-016-0249-3, verified via
OpenAlex) is absent.

**Fix:**
- Add a paragraph to §4.1: "Requirements engineering already detects incompleteness in text:
  masked-language-model predictions flag likely omissions in requirements documents
  \parencite{luitel2024improving}, and ambiguity in interview answers has been used as a cue to
  tacit knowledge \parencite{ferrari2016ambiguity}. These work on one document or one interview,
  at the level of terms, and do not type the missing knowledge or route it to an elicitation
  channel."
- Add Luitel to the closest-work list.
- Add Luitel and Ferrari as precedents in the lens row of `tab:novelty`.

### M14. Several threats to validity are missing

**Location:** `15_threats.tex:12-52` (table) and §15 prose.

**Problem.** The following threats are absent:
- (a) **Judge leniency / ceiling**: own rate is 1.0 on most lenses, so no control can separate
  the arms. This is a construct threat to the absence check itself, distinct from "7B judge".
- (b) **Selection of demonstration traces**: §11 traces were chosen by the author, and nothing
  says how.
- (c) **Area-partition researcher degrees of freedom** (M6).
- (d) **Corpus quality**: in PLC, 42 promotional seeds were excluded against 56 retained lens
  candidates, a sign that much of the corpus is vendor marketing. The denylist was tuned
  in-sample.
- (e) **Non-reproducible retrieval inputs**: the OpenRouter web plugin is an opaque search
  engine, web pages drift, and hosted model versions (`claude-haiku-4.5`, `gpt-5.4-mini`) will
  be retired. The ledgers are replayable, but the reconstruction step is not reproducible.
- (f) **Owner incentive**: the single operator is also the grant applicant. The single-operator
  row covers blinding, not incentive.
- (g) **GDPR v2 inadmissibility**: it enters the headline closure numbers and Trace 2
  (see m6).

**Fix.** Add rows (a), (b), (d) and (e) to the table, each with "Now" and "Program" mitigations:
- (a): report closed-only and paired statistics; enrich "not stated" units in V1.
- (b): a stated selection rule, for example "top-ranked record of each lens".
- (d): the source-kind mix reported per ledger.
- (e): snapshot archives and model-ID pinning; claim only ledger-level reproducibility.

Add (f) to the single-operator row.

---

## MINOR

### m1. The Sullivan 2014 prompting result is paraphrased wrongly

**Locations:** `01_problem.tex:39-41`; `16_residual.tex:12-13`

**Problem.** The report says "the share of steps any surgeon described". The abstract (verified,
OpenAlex W1984195792) reports "the average number of steps that were described increased from
44% (20/46) when unprompted to 66% (31/46) when prompted". That is a per-expert average in the
CTA interview, not a union across surgeons.

**Fix.** Replace with "the average share of steps each surgeon described in the CTA interview".

### m2. Section 21 calls all 46 Sullivan steps "decision steps"

**Location:** `21_domains.tex:81`

**Problem.** "46 decision steps" is wrong. The 46 steps are 14 clinical-knowledge, 27 action and
5 decision steps.

**Fix.** Replace with "46 steps (14 clinical-knowledge, 27 action, 5 decision)".

### m3. Kestin et al. 2025 is misdescribed

**Location:** `19_education.tex:117-118`

**Problem.** The report calls it "an argumentation tutor". The paper is an RCT of a physics AI
tutor against in-class active learning (DOI 10.1038/s41598-025-97652-6).

**Fix.** Replace with "an RCT in which an AI physics tutor outperformed in-class active learning
\parencite{kestin2025aitutoring}".

### m4. The lexical-null statement is false for GDPR v2

**Locations:** `10_n3.tex:78-80, 214-215`

**Problem.** The report says observed counts "sit at or below the null mean on every ledger".
GDPR v2 observed 11 against a null mean of 8.08 (range 5–12). It is within the range but above
the mean. PLC (22 against [26, 41]) is *below* the null range.

**Fix.** Replace with "within or below the null range on every ledger (PLC below it)".

### m5. "Open candidates" in the stability check silently includes retrieval gaps

**Locations:**
- `10_n3.tex:162, 236-238`
- `13_not_demonstrated.tex:73-74`
- `14_interpretation.tex:96`
- `15_threats.tex:95`
- `16_residual.tex:101`
- `26_risks.tex:141`

**Problem.** "13 open candidates" (GDPR v1) is 1 HYP plus 12 RG-SINGLE (`__main__.py`:
`open_a = [r for r in pool if r.category in ("HYP","RG-SINGLE")]`). This breaks the terminology
ruling ("gap candidate" means HYP only) and clashes with the closure state "open".

**Fix.** Replace with "13 unclosed lens records (1 gap candidate, 12 single-source retrieval
gaps)", and use the same wording everywhere.

### m6. The inadmissible GDPR v2 run is used without a caveat in two places

**Locations:** `06_architecture.tex:116-120`; `11_demonstrations.tex:74-112` (Trace 2)

**Problem.** §6 presents the v2 run as "a real completed run". In that run, 305 of 523 claims
are `synthetic_extrapolation` and 140 verdicts are pending. Trace 2 (v2) omits the "not
N3-admissible" note. Trace 2's anchor, "relevant controller", is a drafting phrase from statute
text, not a judgment term. It is arguably a DISC false positive, and its question is
ungrammatical ("whether something was relevant controller").

**Fix:**
- Choose a v1 or PLC run for §6.
- Add "(GDPR v2: not N3-admissible)" to the Trace 2 caption.
- List "the anchor is a legal drafting phrase, not a judgment term" among Trace 2's weaknesses.

### m7. Trace 1 gives the wrong number of rival causes

**Location:** `11_demonstrations.tex:37-38`

**Problem.** "The sources attest 7 rival causes" misreads `k_topic` = 7, the number of
independent sources. The record lists 5 rivals (the table's own row 39-41 says 5).

**Fix.** Replace with "7 independent sources discuss the topic; the lens found 5 rival causes".

### m8. The claim that the template defect leaves the closure judgment unaffected is unsupported

**Location:** `11_demonstrations.tex:201-203`

**Problem.** The report says "the underlying evidence and the closure judgment are
unaffected". The DIAG judge prompt contains the question
`_QUESTIONS["DIAG"].format(rival=text.trim(split[r][0]))`, built from the same fragmentary cause
strings ("Aliasing in data can be a", visible in the record). The judge was asked fragmentary
questions.

**Fix.** Replace with "the evidence is unaffected; the judge's DIAG prompts carry the same
fragmentary cause strings, so the closure judgment may be affected."

### m9. The appendix documents the DIAG template differently from the code

**Location:** `B_lenses.tex:75-79`

**Problem.** The documented template uses `{effect}`. The code (`semantic.py:273`) uses
`cand.anchor`, the full sentence fragment. That difference is the root of the defect.

**Fix.** Document the template as coded and name the substitution as the defect.

### m10. Decision 0008 is described as enforced, but its status is "proposed"

**Locations:** `18_platform.tex:264-265, 294-297`; `06_architecture.tex:139-141`;
`24_team.tex:220`

**Problem.** `docs/architecture/decisions/0008-…md` front matter says `status: proposed`. §18
says "the first four are already enforced in the PoC's code", including the three-family rule.
§6 itself says that rule is "checked by code review rather than by a test".

**Fix.** Write "decision 0008 (proposed)" at first mention. In §18, replace "enforced" with
"implemented; the three-family rule is not test-enforced".

### m11. Section 2 cross-references the report's own validation section as using "H1"

**Location:** `02_question.tex:66-68`

**Problem.** "…the program notes it points to (for example §22 and \cref{sec:validation}) call
this same claim H1". The report's own validation section calls it H2.

**Fix.** Replace `\cref{sec:validation}` with `\repo{report/notes/07_validation.md}`, or delete it.

### m12. The hypothesis tested at L0 is not H1

**Location:** `17_validation.tex:13-14, 24-26`

**Problem.** The report says L0 "concerns H1 (feasible and checkable)". L0's hypothesis is
instead "gated reconstruction adopts fewer planted falsehoods …", a superiority claim about
gating.

**Fix.** Either add a gating sub-hypothesis to H1 (for example "H1b"), or say "L0 tests the
adversarial part of H1".

### m13. The problem statement says experts have "nothing left to report", which the report's own CTA evidence contradicts

**Location:** `01_problem.tex:21-23`

**Problem.** "Because there is nothing left to report" conflicts with the CTA evidence the report
cites: prompting recovers 44% to 66% of steps.

**Fix.** Replace with "because the steps no longer come to mind unprompted".

### m14. The 70% figure's provenance is ambiguous

**Location:** `01_problem.tex:65-68`

**Problem.** The report says the 70% figure "traces to a review chapter citing two other review
chapters" and cites Clark 2008, which is itself a review chapter. The reader cannot tell which
chapter is meant.

**Fix.** Replace with "Clark et al. (2008, p. 589) state it citing two earlier review chapters,
not a new measurement."

### m15. Artifact corroboration conflicts with "E does not contain" in the HKR definition

**Location:** `16_residual.tex:28-31`

**Problem.** An item "corroborated by … an artifact" is, if the artifact states it, written
somewhere. If E includes World B, this conflicts with "E does not contain".

**Fix.** Add "(an artifact outside E, such as a log or trace that shows the item in use without
stating it)".

### m16. The report says "every claim" is tied to a span; that holds for every evidence item, not every claim

**Locations:** `00_executive_summary.tex:23`; `05_scope.tex:8-10`; `09_n2.tex:17`

**Problem.** Unknown claims have no evidence. Synthetic claims have no verified span.

**Fix.** Replace with "every evidence item is an exact span…".

### m17. The report describes the fair control too broadly in two places

**Locations:** `08_evolution.tex:57-61`; `12_demonstrates.tex:24`

**Problem.**
- "Every lens in every domain tried" overstates the coverage. Lenses with fewer than 2
  candidates were not tested (PLC GUARD and DISC).
- "Off-topic match": the control uses the *topically nearest* candidate, so its evidence is not
  off-topic.

**Fix.** Replace with "every lens tested (lenses with fewer than two candidates are skipped)" and
"a topically nearest neighbor's evidence".

### m18. One word in §10 says the opposite of what is meant

**Location:** `10_n3.tex:217-219`

**Problem.** "…sit in a state the map's own control would call **informative**" is wrong. The
control counts partial as closed.

**Fix.** Replace "informative" with "closed".

### m19. §14 uses pre-final lexical numbers where §10 uses the final ones

**Location:** `14_interpretation.tex:17-20`

**Problem.** §14 uses the pre-final lexical figures (PLC 42 vs [33, 47]); §10 uses the final ones
(22 vs [26, 41]).

**Fix.** Use the final figures, with the pre-final ones in a footnote at most.

### m20. Two drift rates and two "located" counts are given for the same runs

**Locations:**
- `09_n2.tex:92` and `D_defects.tex:54`
- `09_n2.tex:118` (table row 5, "≈20% PLC")
- `09_n2.tex:72` (GDPR v2 "Located 366")

**Problem.**
- Drift: the §9 text says 30% (6 of 20, final inspection), while table row 5 says "≈20% PLC"
  (v1 review). Both appear without explanation.
- Located count: the run's `sidecar.json` stat `n_located` is 351. The 366 comes from counting
  `located: true` in the extractions list. The footnote says the figures were "recomputed from
  sidecar.json".

**Fix.** Label the drift figures "v1 review ≈20%; closeout inspection 30%". Footnote the
366/351 difference.

### m21. E-PLANT's domains are never introduced

**Location:** `09_n2.tex:136-144`

**Problem.** E-PLANT and E-ABST ran on food safety and concreting, not on PLC or GDPR
(`docs/n2-eplant-eabst-protocol.md` §1). This is first mentioned in passing at `09:225`.

**Fix.** Add one sentence at 136: "Both ran on two other domains, food safety and concreting."

### m22. The V5 blinding involves deception, and the report does not say so

**Location:** `17_validation.tex:293`

**Problem.** "Experts are not told that a model chose areas" is partial disclosure (deception).
The ethics plan should say so.

**Fix.** Add "…(partial disclosure, with debriefing, approved by the ethics board)".

### m23. The education pilot has no sample-size reasoning

**Location:** `19_education.tex:164-173`

**Problem.** One course section, two arms, delayed transfer, with typical education effects of
0.1–0.2 SD (`kraft2020interpreting`, cited in §28). The pilot can test feasibility only.

**Fix.** Add "a feasibility pilot; not powered for an effect".

### m24. Staffing, FTE and method-appendix details are inconsistent or premature

- **Lean team roles** (`24_team.tex:91-94` vs `23_workpackages.tex:131-132`): the lean team's
  coders cover WP3 and WP4 only. V3 (WP5) needs ≥200 double-coded issues and a
  mining-software-repositories researcher. **Fix:** add WP5 to the coders' line and name the
  MSR skill.
- **Grant-scale FTE** (`24:122` vs `25:54`): 3.5–5.0 vs 3.2–5.0. **Fix:** use one figure.
- **Method appendix** (`G_method.tex:34-48`): it describes two review rounds and a final audit
  in the past tense. **Fix:** make sure it is true at publication, and list the reviewers'
  unresolved objections, if any.

---

## Cuts (target: main body ≈ 85–95 pages; now pp. 1–127 ≈ 121 pages of text)

The main source of length is repetition. Each of the following appears in many sections:

| Repeated item | Occurrences |
|---|---|
| Closure numbers 0.889/0.961/0.958 | 10 sections (00, 04, 08, 10, 12, 13, 14, 17, 26, 29) |
| Omission studies (Sullivan, Chao, Crandall) | 7 to 9 sections |
| Rigby / Avelino | 8 sections |
| Blind-spot studies (Nathan, Maries) | 6 sections |
| Precision "3 of 19" | 8 files |
| Spearman 0.91 | 7 files |
| The $5 / $21 budget story | 06, 09, 17, 18, 25, 26 |
| Szulanski | 4 sections |
| Orr and the GUARD example | 2 sections |

**Rule for the edit:** state each number once, in its home section (§10 for closure; §1 for
omission; §9 for budget). Elsewhere cite the section without the number, except in the
Executive summary and the Conclusion.

| # | Section (current pages) | Action | Saves |
|---|---|---|---|
| 1 | §3 Foundations (11 pp, pp. 9–19) | Delete the six "Key findings: this is a conceptual framework" stubs. Delete the omission numbers repeated from §1 (lines 56–58). Merge Expert blind spot + PCK + Threshold concepts + Conceptual change into one subsection, "What experts misjudge about learners" (keep Table 1). Cut "Investigated but not central" to one paragraph; move knowledge tracing, ITS, KST and decision-based learning to one sentence each. | ~5 pp |
| 2 | §4 Approach (7 pp) | Delete the third restatement of the omission numbers (`04:21-26`). Shorten steps 1–7 of the central model to one line each, pointing to §6 and §10 (they restate §6, §9 and §10). Merge the "Novelty statement" paragraph (`04:244-258`) with the paragraph above it; it repeats the Executive summary and tab:novelty. Keep the figure and the novelty table. | ~2.5 pp |
| 3 | §5–§8 Scope, Architecture, Evidence model, Evolution (11 pp) | Merge §5 and §8 into one "Scope and N0–N3 verdicts" section: one table (merge tab:now-items and tab:now-verdicts). Move the module inventories (`06:52-64`), the determinism and budget paragraphs (`06:146-172`) and residual accounting / frozen schema (`07:141-166`) to Appendix E. The pipeline stage list appears in §4, §6 and §9: keep it only in §6. | ~4 pp |
| 4 | §11 Demonstrations (5 pp) | Keep Trace 1 (corrected per C1) and the failure trace. Move Traces 2 and 3 to Appendix C. | ~2 pp |
| 5 | §12 + §13 + App. A (5 pp main + 7 pp app.) | Replace tab:demonstrates (a longtable of 14 rows that duplicates App. A) with a half-page summary of 6 bullets or a 6-row table pointing to App. A row IDs. Merge §12 and §13 into one section, "What the PoC shows and does not show". | ~2 pp |
| 6 | §14 + §15 Interpretation, Threats (7 pp) | §15's prose subsections restate the table and §10 (the parsing defect appears in §10, §15 and App. D). Keep the table (with M14's rows added) and one paragraph on AI-assisted development. §14.2–§14.5 (thinness, density, stability, tuning) each restate §10: compress to one subsection. | ~2.5 pp |
| 7 | §16 Residual (4 pp) | "What makes it hard" partly duplicates §17's threats: merge it into §17's threats. | ~1 pp |
| 8 | §17 Validation (11 pp) | Cut V7 and V8 to a paragraph each (their detail repeats in §19, §20 and §21). Cut the "Threats to the program" paragraphs that repeat §15 (contamination, in-sample tuning). Keep V0–V5 in full, since they are the grant core. Note that C2, M6, M7 and M8 add about 0.5 page. | ~1.5 pp |
| 9 | §18 Platform (10 pp) | Move the Weft subsection (`18:389-454`, ~1.5 pp) to a new appendix, "Weft assessment". Compress the NFR subsection (`18:320-387`, ~2 pp) to half a page; its privacy, GDPR and works-council text repeats §20.7 almost verbatim. Keep the three worlds, tab:components and the decisions. | ~3.5 pp |
| 10 | §19 + §20 Education, Organizations (9 pp) | Delete the third and fourth restatements of Chi, Maries and Nathan (`19:13-34`) and of Orr and Szulanski (`20:14-33`); point to §1 instead. Merge the §20.7 ethics text with §18's NFR (keep one copy, in §20). Move the "Software as the reproducible test domain" subsection into §21 (D2), which says the same. | ~3.5 pp |
| 11 | §21–§23 Domains, Roadmap, Work packages (14 pp) | The same S/V/WP/MS information appears three times: roadmap stage tables, WP tables, and tab:validation plus the milestones table. Replace the seven roadmap stage tables with one table (stage × hypothesis × gate × duration) plus fig. 14. Compress each WP table to 5 lines (drop the "Expertise" rows; §24 covers them). Keep the milestones table. | ~4.5 pp |
| 12 | §24 + §25 Team, Resources (7 pp) | Move the product-team table and the funding-instrument table to an appendix. Cut the "why interdisciplinary" paragraph, which repeats citations from §3 and §17. | ~2 pp |
| 13 | §26–§29 Risks, Contributions, Impact, Conclusion (8 pp) | Merge §27 and §28 into one "Expected contributions and impact" section; the "even if it fails" column repeats §17's closing box and §26's pivots. Remove the repeated numbers from §26's risk table (point to §10). | ~2 pp |

**Total: about 35 pages, giving a main body of about 86–90 pages.** Appendices grow by about 6
pages, which is acceptable.

**Priority order if only part can be done:** 9, 11, 1, 3, 10. These are the largest and involve
the most mechanical repetition.
