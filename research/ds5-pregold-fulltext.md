# DS5: pre-gold full text and memorisation controls

- **Question:** For each DS1 gold, how much legally obtainable full text predates it, how must it be blocked, how are memorisation probes run, and which models have documented cutoffs?
- **Answer:** Free-to-read pre-gold works range from 4 (Phillips 1998, 4% of 96) to 5,457 (Canopy ERCP, 22% of 24,480) per domain query. Three of the 17 provisional golds fall below a proposed screen of 100. Only Russ-Jara and Ede (December 2023) postdate a documented cutoff, and that cutoff is Mistral Small 3's system-prompt date (2023-10-01).
- **Changed:** I10 now has a proposed screen and floor and a stricter blocklist. The blocklist moves 5 golds' cut-offs to an earlier same-team precursor and also blocks citing works. Probes are calibrated on decoys run through each model, and on OLMo 2's public training data. The paywalled TDM route is guaranteed only with institutional access, which the owner assumes the project lacks (2026-10-24, §7), so it is closed for I10.

**Result (2026-10-24).**
- **Full text.** Pre-gold full text is ample for every clinical gold and scarce for the old non-clinical ones. Measured by OpenAlex metadata only, the free-to-read share of pre-gold works per domain query is 18–51% for the 13 clinical provisional golds and Okoli. It is 4–12% for the 1990s golds: Phillips 1998 and 2001, Seamster 1993, and the U candidates Crandall and Chao.
- **Paywalled text.** By default, publisher TDM terms (Elsevier, Springer Nature) open it only to researchers at subscribing institutions. Both consider non-subscriber requests case by case. EU DSM Art. 4 needs lawful access. So without institutional access, the guaranteed TDM share beyond open access is 0.
- **Finding 21 holds.** The binding constraint is full text, not Wayback (`docs/plans/coverage-audit.md:113`). It now binds on Phillips 1998, Phillips 2001 and Grover TAR rather than on the 1993–94 golds, which DS1 moved to U or rank 17.
- **The gold's date alone is not a valid cut-off.** In 3 of 17 golds, OpenAlex dates a citing work on or before the cut-off. In 5 golds, a same-team task analysis predates the gold, and that precursor plausibly published part of the same list (*inferred* from titles).
- **Memorisation probes.**
  - Current practice is guided-versus-general completion with an exact or near-exact judge [151]. Its published validation reports agreement with human labels, not a false-positive rate on known-clean items.
  - Per-item membership inference on matched data is close to chance [Duan 2024].
  - So probe-positive must be calibrated on decoys, and on a model whose training data can be searched: OLMo 2, Dec 2023 cutoff, public data with an infini-gram index.

**Decision it feeds.**
- **I10's design and floor.** This note proposes them in §6; I10 measures the binding numbers.
- **The owner's primary set** (DS1 decision: Okoli, Madani, Logishetty; `docs/plans/deep-search-queue.md:14`).
  - All three pass the screen, with 1,166, 4,534 and 263 free works.
  - Okoli's effective cut-off moves from 2020 to 2015 because of its own precursors (§3), so I10 must recount it first.
  - Madani needs citation blocking for one mis-dated citing work.
  - Logishetty shows neither leak.
- **Dropping golds below the floor.** Proposed: Phillips 1998 and Phillips 2001 (fallback ranks 15–16), with Grover TAR (rank 5) borderline. Dropping waits for I10's task-level count.
- **The §22 "primary model and baseline" blank.** This note supplies the shortlist in §5. The pick waits for I5 and I12.

**Method.**
- **What was used.** OpenAlex aggregates only (`group_bys`), with no work's text read; the Wayback CDX index (capture lines, no archived page fetched); primary policy and statute pages; model cards; the OpenRouter models API.
- **The gold side.** No gold paper, supplement or list was opened, and no work that restates one. DS1's blocklist (DOI, title) was applied.
- **Scripts and outputs.** Each script sits next to its JSON in `research/ds5-pregold-fulltext/`:
  - `openalex_counts.py` → `openalex_counts.json`;
  - `cdx_counts.py` → `cdx_counts.json`;
  - `openrouter_snapshot.py` → `openrouter_snapshot.json`.
- **Blocking.** The blocking queries in `blocking.json` ran through the OpenAlex MCP, because the keyless API's shared daily budget ran out. The API's own response notice on 2026-10-24 gave that budget as $0.10 per IP. Each entry carries its OQL.
- **Retrieved:** 2026-10-24.
- **Verification.** `citation-verifier` passed on 2026-10-24 after two rounds of fixes. The first round fixed 15 findings: one wrong range, ten overstatements, three unrecorded figures and one unlabelled inference. The second fixed three.
- **Delegation.** Q4 (probe practice) and Q5 (model cutoffs) were read by a delegated agent from the primary sources cited. The OLMo cutoffs, the Ollama tags, the infini-gram index name and all OpenRouter prices were re-checked here.

## 1. Pre-gold full text per gold domain

**Domain queries.**
- Each query is a title-and-abstract search for the gold's procedure or task, in `openalex_counts.py:GOLDS`.
- Cut-off is the day before the gold's OpenAlex `publication_date`. For Phillips 1998, that date is year-only, so the cut-off is 1997-12-31.
- A five-title random sample per query (printed by `openalex_counts.py --sample`; the sample was not recorded) showed precision is uneven: high for named procedures, low for Okoli, Dias and Russ-Jara, whose topics are broad. So the counts are an upper bound on relevant text. They are a screen, not the floor; I10 measures task-level precision.

**What the columns count.**
- *Free* is every OpenAlex status except closed: gold, green, hybrid, bronze and diamond. All of these are lawfully readable now.
- *Open licence* means the best OA copy carries a CC or public-domain licence.
- *OpenAlex PDF* means OpenAlex holds a cached PDF (`has_content.pdf`).
- *Closed: Elsevier + Springer* is the closed works whose host is "Elsevier BV" or a host name beginning "Springer", derived from `closed_by_publisher`. Imprints and Nature Portfolio are not included. These works are reachable by default only under those publishers' subscriber TDM terms (§1.1).

| Gold (DS1 rank, verdict) | Cut-off | Pre-gold works | Free | Free % | Open licence | OpenAlex PDF | Closed: Elsevier + Springer |
|---|---|---|---|---|---|---|---|
| Sullivan 2014, cricothyrotomy (1, P) | 2014-03-24 | 1,578 | 370 | 23% | 91 | 252 | 410 |
| Okoli 2020, fireground command (2, P) | 2020-08-20 | 3,361 | 1,166 | 35% | 415 | 780 | 266 |
| Madani 2015, lap. cholecystectomy (3, P) | 2015-08-05 | 20,283 | 4,534 | 22% | 1,996 | 2,882 | 3,675 |
| Logishetty 2019, anterior THA (4, P) | 2019-09-19 | 830 | 263 | 32% | 136 | 172 | 224 |
| Grover 2022, TAR (5, P) | 2022-11-16 | 258 | 95 | 37% | 58 | 62 | 103 |
| Grover 2023, RYGB (6, P) | 2023-09-12 | 15,686 | 5,421 | 35% | 2,863 | 3,419 | 6,911 |
| Smink 2012, lap. appendectomy (7, P) | 2012-02-09 | 1,900 | 340 | 18% | 178 | 189 | 442 |
| Sullivan 2007, colonoscopy (8, P) | 2007-12-12 | 17,828 | 3,487 | 20% | 622 | 2,718 | 4,164 |
| Dias 2019, cardiac surgery team (9, P) | 2019-07-23 | 3,268 | 1,377 | 42% | 434 | 993 | 525 |
| Karamchandani 2021, meniscal repair (10, P) | 2021-06-23 | 2,648 | 879 | 33% | 497 | 518 | 817 |
| Russ-Jara 2023, DDI management (11, P) | 2023-11-30 | 5,453 | 2,795 | 51% | 1,479 | 1,841 | 749 |
| Ede 2023, nursing escalation (12, P) | 2023-12-08 | 3,091 | 1,487 | 48% | 811 | 1,002 | 360 |
| Canopy 2015, ERCP (13, P) | 2015-06-29 | 24,480 | 5,457 | 22% | 1,991 | 4,125 | 6,089 |
| Plumptre 2017, pelvic exam (14, P) | 2017-07-11 | 6,110 | 1,705 | 28% | 604 | 1,086 | 1,246 |
| Phillips 1998, MOUT leaders (15, P) | 1997-12-31 | 96 | **4** | 4% | 1 | 3 | 3 |
| Phillips 2001, MOUT training (16, P) | 2001-07-31 | 212 | **14** | 7% | 2 | 10 | 4 |
| Seamster 1993, en route ATC (17, P) | 1993-09-30 | 3,282 | 395 | 12% | 73 | 327 | 311 |
| Crandall 1993, NICU sepsis (U) | 1993-08-31 | 200 | 24 | 12% | 5 | 20 | 52 |
| Chao 1994, troubleshooting (U) | 1994-06-30 | 1,022 | 107 | 10% | 9 | 76 | 322 |

Source: `research/ds5-pregold-fulltext/openalex_counts.json`, fields `n_pregold`, `n_free_to_read`, `n_open_licence`, `n_openalex_pdf` and `closed_by_publisher`. The API charge was $0.038.

**Readings.**
- **Routes for the clinical golds.** Every clinical provisional gold has at least 263 free pre-gold works, except Grover TAR with 95. TAR is a procedure first described about 2012 (*inferred* from the domain's recent literature), so its pre-gold window is short.
- **The military golds.** Phillips 1998 and 2001 have almost no free scholarly pre-gold text. Their natural corpus is US Army and DTIC field manuals and reports. OpenAlex indexes few of these (18 and 50 reports). Of all pre-gold works in these two queries, 96% and 93% are closed. Whether DTIC "approved for public release" copies raise the count is *unverified* and is I10's to measure.
- **Seamster 1993.** Its domain is text-rich (3,282 works), but only 12% are free. A 1993 cut-off also leaves no Wayback material (§2).
- **Not counted.** Pre-gold abstracts of closed works are also lawfully readable through OpenAlex and PubMed, but they are not counted here. Closed works hosted under "National Institutes of Health" (PubMed records) are abstract-only.

### 1.1 Legal routes, strongest first

1. **Open licence (CC or public domain).** Reading, mining and keeping copies are all clean.
2. **Free to read (bronze, green, hybrid, diamond, gold).** This content is lawfully accessible. EU DSM Directive 2019/790 Art. 4(1) excepts "reproductions and extractions of lawfully accessible works … for the purposes of text and data mining". Art. 4(3) makes that conditional on the use "not [having] been expressly reserved by their rightholders … such as machine-readable means" ([Art. 4](https://www.legislation.gov.uk/eudr/2019/790/article/4)). So the pipeline must honour machine-readable reservations, for example robots.txt or TDM-reservation headers, at fetch time. Art. 3 gives research organisations a TDM exception that rightholders cannot opt out of. The Art. 4(3) reservation does not apply to it, and contrary contract terms are unenforceable ([Art. 7(1)](https://www.legislation.gov.uk/eudr/2019/790/article/7)). It still requires "lawful access" ([Art. 3](https://www.legislation.gov.uk/eudr/2019/790/article/3)). This is a reading of the statute, not legal advice.
3. **Publisher TDM terms for paywalled content.**
   - [Elsevier](https://www.elsevier.com/about/policies-and-standards/text-and-data-mining) lets "researchers at subscribing academic institutions" text-mine ScienceDirect for non-commercial research. It considers non-subscriber requests "on a case-by-case basis".
   - [Springer Nature](https://www.springernature.com/gp/researchers/text-and-data-mining) grants TDM rights for subscribed content "via their institutions" for non-commercial research. Non-subscribers are offered TDM tools for its open-access resources. Non-subscriber requests for paywalled content are treated case by case.
   - Wiley's TDM page refused the fetch (HTTP 403). Lippincott, Taylor & Francis, SAGE and OUP terms were not checked.
   - **Share reachable this way:** a guaranteed 0 without an institutional subscription; non-subscriber requests are decided case by case. With one, it is up to the "Closed: Elsevier + Springer" column, 2–44% of each domain's pre-gold works, depending on the subscription's coverage.
4. **Purchase per article.** This is lawful access for reading. Whether it licenses mining is publisher-specific and was not checked.

## 2. Wayback before each gold (post-1996 golds)

Source: `research/ds5-pregold-fulltext/cdx_counts.json`. It counts status-200 captures with a timestamp on or before the cut-off, capped at 20,000 per query. A capped row is a lower bound, so only "capped" and the first-capture date are informative there.

**Wikipedia article on the gold's procedure** (exact URL; captures before the cut-off, first capture):

| Gold | Article | Captures | First |
|---|---|---|---|
| Sullivan 2014 | Cricothyrotomy | 19 | 2007 |
| Okoli 2020 | Incident Command System | 123 | 2004 |
| Madani 2015 | Cholecystectomy | 49 | 2004 |
| Logishetty 2019 | Hip replacement | 78 | 2004 |
| Grover TAR 2022 | Incisional hernia | 71 | 2006 |
| Grover RYGB 2023 | Gastric bypass surgery | 167 | 2005 |
| Smink 2012 | Appendectomy | 48 | 2004 |
| Sullivan 2007 | Colonoscopy | 28 | 2004 |
| Dias 2019 | Cardiac surgery | 195 | 2004 |
| Karamchandani 2021 | Tear of meniscus | 48 | 2008 |
| Russ-Jara 2023 | Drug interaction | 119 | 2005 |
| Ede 2023 | Early warning score | 15 | 2015 |
| Canopy 2015 | Endoscopic retrograde cholangiopancreatography | 32 | 2004 |
| Plumptre 2017 | Pelvic examination | 25 | 2007 |
| Phillips 1998 | Urban warfare | 0 | none before the cut-off |

**Specialist sites.**
- **Clinical golds:** every one except Russ-Jara has at least one specialist or society site with ≥ 20,000 pre-gold captures (the cap). Their first captures run from 1996 to 2009, including emedicine.medscape.com, trauma.org, sages.org, websurg.com, orthobullets.com, orthoinfo.aaos.org, asmbs.org, gi.org, sts.org, ctsnet.org, sportsmed.org, rcplondon.ac.uk, nice.org.uk, asge.org and acog.org.
- **Below the cap:**
  - americasherniasociety.org (Grover TAR) has 1,544 captures, the first in 2020.
  - asge.org before Sullivan 2007 has 16,337.
  - drugs.com/drug_interactions, the only specialist site measured for Russ-Jara, has 2,911 captures over 253 URLs, the first in 2004.
- **Fireground (Okoli):** firehouse.com, fireengineering.com and usfa.fema.gov all reach the cap, with first captures in 1997–2007.

**Military golds.** For Phillips 1998 and 2001, whole-domain queries on fas.org and army.mil returned HTTP 504 after retries. globalsecurity.org and the Phillips 2001 targets were therefore not measured (`provenance` in the JSON). Wikipedia has no pre-1998 capture.

**Pre-1996 golds.** Seamster 1993, Crandall 1993 and Chao 1994 predate the Wayback Machine's first captures in this sample (1996), so they have no web route at all.

**Reading.**
- For every post-1996 clinical gold, archived web material exists before the gold, so Wayback does not bind. This is consistent with finding 21.
- What binds the web route is quality and relevance, not existence. Capture counts measure archive density, not relevance; I10 measures relevance with the pipeline's own queries.
- Wikipedia's own revision history is a dated source finer than its Wayback captures (*inferred*; not measured here).

## 3. Blocking per gold

A cut-off on publication date blocks the gold and nearly all its citing works. Two measurements show it is not enough on its own.

**1. Citing works dated on or before the cut-off.**
- These occur in 3 of 17 provisional golds: Madani 2015 (one citing work dated 2000), Karamchandani 2021 (one dated 2021, before 23 June) and Seamster 1993 (one dated 1993).
- Madani's (dated 2000) is a metadata error. Karamchandani's and Seamster's fall in the gold's own year and may reflect online-first or year-only dates. Either way, the date filter admits them.
- Source: `blocking.json` → `citing_dated_on_or_before_cutoff`. Across all 17 golds there are 458 citing works, of which 40 are book chapters and 2 are books (`citing_all_p_golds_by_type`).

**2. Same-team precursors.** A task analysis of the same procedure by the gold's own group predates the gold in five cases:

| Gold | Precursor | Relation |
|---|---|---|
| Sullivan 2014 | Campbell et al. 2011 (doi:10.1016/j.jsurg.2011.05.007); Yates, Sullivan & Clark 2011 online (doi:10.1016/j.amjsurg.2011.07.011) | Same USC group. Both are CTA studies of open cricothyrotomy. |
| Okoli 2020 | Okoli, Weller & Watt 2015 (doi:10.1007/s10111-015-0348-9); Okoli, Watt & Weller 2016, fireground cue classification (doi:10.1111/1468-5973.12129) | Same first author and domain. The 2016 paper classifies fireground cues. |
| Russ-Jara 2023 | Russ et al. 2017 (doi:10.1097/pts.0000000000000324); Russ et al. 2021 (doi:10.1007/s11606-020-06386-w) | Same first author. CTA of medication-safety incidents. |
| Seamster 1993 | Redding 1992, two CTA reports on en route ATC; Redding et al. 1991 (doi:10.1177/154193129103501914) | Redding is Seamster 1993's second author. |
| Phillips 2001 | Phillips et al. 1998 (DS1 rank 15) | Same team (Phillips, McCloskey, McDermott) and the same population. |

- Source: `blocking.json` → `prior_task_analysis_same_procedure`.
- Whether each precursor prints part of the gold's list is *inferred* from titles only. Checking it means reading them, which waits for the pre-registration.
- If precursors are admitted, the reconstruction can retrieve the experts' own earlier disclosure. Then §18.2's "was this written before experts revealed it?" is answered wrongly.
- **Adjacent CTAs by other groups** (Ede ← Marshall 2022; Karamchandani ← Bhattacharyya 2017) are legitimate pre-gold evidence and stay in.

**Blocklist spec (proposed for I10).** For each gold *g*:
1. **Effective cut-off** = min(*g*'s earliest online date, the earliest date of any same-team precursor on the same procedure or population). A same-team precursor shares an author with *g* and matches the task-analysis query.
2. **Exclude by DOI and OpenAlex id:** *g* itself; every work that cites *g* or a precursor, whatever its date; and every precursor.
3. **Exclude by normalised title:** *g*'s title, for undated web copies and repository versions.
4. **Exclude web pages** whose text contains *g*'s DOI, its title, or "<first author> et al." with *g*'s year. This check runs on the captured text at fetch time.
5. **Restatements.** Textbooks and guidelines that restate *g* without citing it cannot be found by metadata. Date-blocking handles them, because a restatement postdates *g*. The remaining risk is re-editions whose OpenAlex date is the first edition's. Rule: a book or book-chapter is admitted only if its edition date precedes the cut-off.
6. **Memorisation.** Residual leakage through the models is handled by §4, not by the blocklist.

## 3a. Model cutoffs against gold dates

- 15 of the 17 provisional golds predate every documented cutoff in §5. The latest provisional gold dates are December 2023: Russ-Jara on 2023-12-01 and Ede on 2023-12-09.
- Those two postdate only Mistral Small 3.x's stated date, 2023-10-01. That date is weak evidence: it comes from a system prompt, not a model card.
- The same two fall inside the cutoff month of OLMo 2 ("Dec. 2023") and Llama 3.1/3.3 ("December 2023"). By date alone, whether they are in training data is undetermined. For OLMo 2 it can be checked directly (§4).
- So DS1's hope that the 2023–2025 golds postdate some cutoffs holds for two provisional golds, against one weakly documented model. It holds cleanly only for U candidates, such as Mansur 2025.

## 4. Memorisation probes

**Current practice.**
- **Golchin & Surdeanu** [151] (ICLR 2024; [arXiv:2308.08493](https://arxiv.org/abs/2308.08493)).
  - *Guided instruction:* dataset name, partition and an initial segment of the instance.
  - *General instruction:* the same, without the dataset or partition name.
  - *Completion overlap:* ROUGE-L and BLEURT, or a GPT-4 few-shot judge that labels exact, near-exact or inexact.
  - *Partition-level contamination, Algorithm 1:* a significant guided-over-general ROUGE-L or BLEURT gap on 10 instances (bootstrap, p ≤ 0.05).
  - *Partition-level contamination, Algorithm 2 (the best performer):* a GPT-4 few-shot judge flags ≥1 exact or ≥2 near-exact matches among 10. The authors set this threshold "intuitively".
  - *Validation:* 92.86–100% agreement with two human experts who applied the same rule. Controlled contamination produced exact matches. It used continued training of GPT-3.5 on 100 training instances from each of AG News, RTE and XSum, one model per dataset. No false-positive rate on known-clean items is reported.
- **Sainz et al.** [151] ([doi:10.18653/v1/2023.findings-emnlp.722](https://doi.org/10.18653/v1/2023.findings-emnlp.722)) defines contamination as extractability and leaves non-verbatim cases to auditor judgement. They leave open whether an absence of memorisation shows the model was not trained on the benchmark.
- **Membership inference does not settle it.**
  - On same-distribution members and non-members, membership-inference attacks "barely outperform random guessing for most settings" ([Duan et al. 2024, arXiv:2402.07841](https://arxiv.org/abs/2402.07841)).
  - "Blind" attacks that never query the model beat published ones on 8 MI datasets ([Das et al. 2024, arXiv:2406.16201](https://arxiv.org/abs/2406.16201)).
  - The Data Contamination Quiz asks the model to pick the original instance from word-level perturbed variants, correcting for positional bias ([Golchin & Surdeanu, arXiv:2311.06233](https://arxiv.org/abs/2311.06233)).
  - Dataset-level aggregation reaches significance at p < 0.1 without false positives on Pile splits ([Maini et al. 2024, arXiv:2406.06443](https://arxiv.org/abs/2406.06443)).
- **Consequence:** a single item's probe verdict is weak evidence either way. False-positive control has to come from decoys run through the identical pipeline.

**Probe protocol (proposed; everything below is *inferred* from the sources above).** It runs only after the pre-registration is hash-committed and the gold is acquired.

1. **Prefix.** Each gold item is cut after the first 40% of its words, with at least 3 words.
2. **Two arms.**
   - *Guided:* gold title, year and procedure, plus "item N of the cognitive task analysis list", plus the prefix.
   - *General:* procedure plus the prefix.
   - Greedy decoding, plus 5 samples at temperature 0.7.
3. **Score.** The primary score is deterministic: token-level longest-common-subsequence F1 of the generated tail against the true tail. An LLM judge (exact, near-exact or inexact) is secondary, with a top-tier parallel arm per CLAUDE.md.
4. **Controls through the identical pipeline.**
   - **Decoys:** plausible items for the same procedure, written from the pre-gold corpus before the gold is unsealed. Any decoy that matches a gold item after unsealing is dropped.
   - **Paraphrases:** one paraphrase per gold item; the score is the match to the original minus the match to the paraphrase.
5. **Probe-positive.** An item is probe-positive when its guided score is ≥ τ, it beats the general arm, and it beats its paraphrase.
   - τ is the smallest value that keeps the decoy false-positive rate ≤ 5%, with the one-sided 95% Clopper–Pearson upper bound reported.
   - With zero decoy hits, the bound falls below 5% only at ≥ 59 decoys per model. The exact bound is 1 − 0.05^(1/n); the rule of three, 3/n, needs ≥ 61. The set is therefore ≥ 61 decoys per model, which meets both.
6. **False-negative estimate on OLMo 2.**
   - Count each gold item's exact n-grams in the infini-gram index of the exact checkpoint probed. For OLMo-2-1124-13B-Instruct, that is `v4_olmo-2-1124-13b-instruct_llama` ([API docs](https://infini-gram.readthedocs.io/en/latest/api.html)).
   - `v4_olmo-mix-1124_llama` covers stage-1 pretraining only, so a miss there is not a known non-member.
   - Items with hits are known members; the probe's recall on them is its sensitivity.
   - This is the only model in the shortlist where membership can be checked rather than inferred.
7. **Scope.** The probe runs on every model in the chain: planner, extractor, verifier and judge (`report/sections/17_validation.tex:111-114`). Probe-positive items leave the primary analysis. A negative probe is never evidence of absence, so recall stays an upper bound (§18.2).
8. **Discrimination check before use (L7.3).** The probe is used only after it shows it can discriminate:
   - it must fire on a planted positive, an item from a list known to be in OLMo-mix;
   - it must not pass on a stand-in of random procedure-shaped sentences.

## 5. Model shortlist (cutoffs as documented by the publisher)

Prices are OpenRouter's, in $ per million input / output tokens: `openrouter_snapshot.json`, retrieved 2026-10-24.

| Model | Documented cutoff (source) | Training data public | OpenRouter id, $ in/out | Ollama |
|---|---|---|---|---|
| **OLMo 2** (7B, 13B, 32B) | "Date cutoff: Dec. 2023" ([HF card](https://huggingface.co/allenai/OLMo-2-1124-13B)) | **Yes**: OLMo-mix-1124 (`v4_olmo-mix-1124_llama`), plus infini-gram indexes for the 13B-Instruct (1124) and 32B-Instruct (0325) checkpoints; none for 7B | not listed | `olmo2:7b`, `olmo2:13b` |
| OLMo 3 (7B, 32B) | "Date cutoff: Dec 2024" ([HF card](https://huggingface.co/allenai/Olmo-3-1125-32B)) | Yes: Dolma 3; no infini-gram index listed | not listed | `olmo-3:7b`, `olmo-3:32b` |
| Llama 3.1 (8B, 70B) | December 2023 ([model card](https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md)) | No | `meta-llama/llama-3.1-8b-instruct` 0.05/0.08; 70B 0.40/0.40 | `llama3.1` |
| Llama 3.3 70B | December 2023 ([model card](https://github.com/meta-llama/llama-models/blob/main/models/llama3_3/MODEL_CARD.md)) | No | `meta-llama/llama-3.3-70b-instruct` 0.10/0.32 | `llama3.3:70b` |
| Llama 4 Scout / Maverick | August 2024 ([model card](https://github.com/meta-llama/llama-models/blob/main/models/llama4/MODEL_CARD.md)) | No | scout 0.10/0.30; maverick 0.1875/0.6525 | `llama4` |
| Gemma 3 27B | August 2024 ([model card](https://ai.google.dev/gemma/docs/core/model_card_3)) | No | `google/gemma-3-27b-it` 0.08/0.35 | `gemma3` |
| Gemma 4 31B | January 2025 ([HF card](https://huggingface.co/google/gemma-4-31B-it)) | No | `google/gemma-4-31b-it` 0.20/0.40 | `gemma4:31b` |
| Phi-4 14B | "June 2024 and earlier" for public data ([HF card](https://huggingface.co/microsoft/phi-4)) | No | `microsoft/phi-4` 0.07/0.14 | `phi4:14b` |
| gpt-oss 20B / 120B | June 2024 (OpenAI model card, [arXiv:2508.10925](https://arxiv.org/abs/2508.10925)) | No | 20b 0.018/0.09; 120b 0.15/0.60 | `gpt-oss` |
| Mistral Small 3.x 24B | 2023-10-01, stated only in the system prompt ([SYSTEM_PROMPT.txt](https://huggingface.co/mistralai/Mistral-Small-3.2-24B-Instruct-2506/blob/main/SYSTEM_PROMPT.txt)) (weak) | No | 3.2: 0.075/0.20 | `mistral-small3.2` |

**Excluded for having no publisher-stated cutoff:** Qwen 2.5, Qwen 3 and later, DeepSeek V3, R1 and V4, Kimi K2, GLM-4.5 and 4.6. This includes the project's local judge family, qwen2.5. OpenRouter's `knowledge_cutoff` field gives dates for some of them, but it is aggregator metadata, not a publisher statement.

**Constraints from the project's rules.**
- gpt-oss is OpenAI-family, the family of the N2 verifier. ADR 0009 covers closure judges only. Applying its parallel-arm rule to gpt-oss as a primary model or baseline is proposed here and needs its own decision.
- Each small model needs a top-tier parallel arm.

**Proposed roles.**
- **OLMo 2 13B (local, Ollama)** is the probe-calibration anchor, because it is the only model whose training data can be searched for a gold item.
- **Llama 3.3 70B** (Dec 2023) and **Gemma 3 27B** (Aug 2024) are low-cost documented-cutoff candidates of 27B or more, outside the OpenAI family, for the E-CTA primary model and the plain-LLM baseline. **Llama 4 Scout** (0.10/0.30, Aug 2024) is a cost-equivalent alternative.
- The pick waits for I5's and I12's discrimination results.

## 6. Proposed corpus floor

**Screen (metadata, now): ≥ 100 free-to-read pre-gold works on the gold's domain query.**
- The N2 reconstructions consumed 20–35 fetched sources for 5 areas (`research/n2/e_live_report.md:47,62,134`), so the pipeline needs about 25 usable documents (*inferred*: E-LIVE was a sanity gate and measured no minimum).
- Domain-query precision is unmeasured. Assuming at least 25% (*inferred*) gives 25 / 0.25 = 100.
- **Disclosure:** this screen was proposed after the counts were seen. methods-critic must review it before it is registered, and I10's measured precision replaces the 25%.

**Floor (binding, measured by I10).** At least 25 dated, admissible, full-text documents reachable by the pipeline's own queries for the gold's task, with at least 3 per planned area. "Admissible" means:
- dated by OpenAlex `publication_date` or a CDX timestamp before the effective cut-off (§3);
- free to read, or covered by a TDM licence the project actually holds;
- not blocklisted;
- not reserved under Art. 4(3).

**Golds below the screen.**

| Gold | Free pre-gold works | Status against the screen of 100 |
|---|---|---|
| Phillips 1998 | 4 | fails |
| Phillips 2001 | 14 | fails; also its precursor moves its cut-off to 1997 |
| Grover TAR | 95 | borderline |
| Crandall | 24 | fails (U, so not on the list anyway) |

Seamster passes the screen with 395. Its precursors move the effective cut-off to 1991, so it must be recounted at that date.

**Golds that pass.** Every other clinical gold and Okoli pass the screen. For Sullivan 2014, Okoli and Russ-Jara, that holds at the gold's own date; the earlier effective cut-offs (2011, 2015 and 2017) still need a recount, which is I10's first step.

## 7. Owner input (decided 2026-10-24)

- The owner assumes no institutional subscription access through an EU research organisation (`docs/plans/implement-queue.md`, I10 entry). Route 3 (§1.1) is closed for I10 and later work until such access is obtained, so the floor is computed on free-to-read text only. The §3 blocklist (cut-off at the earliest same-team disclosure, citing works blocked whatever their date) is adopted.

## Deviations

- Gold-adjacent exposure is limited to titles of pre-gold same-team works (§3). They are recorded as titles and DOIs only.
- The keyless OpenAlex API hit its shared daily budget mid-run. The blocking queries were rerun through the OpenAlex MCP and recorded with their OQL in `blocking.json`.
- **Breaches of §14.3:** none known.

## References

- [151] Golchin S, Surdeanu M 2023, arXiv:2308.08493; Sainz O et al. 2023, doi:10.18653/v1/2023.findings-emnlp.722 (`REORIENTATION.md:884`).
- Other sources are linked inline: statute, publisher policies, model cards, the infini-gram docs, and Duan, Das, Maini and Golchin on arXiv.
- Gold DOIs and dates come from `research/ds1-gold-availability.md` and `openalex_counts.json`.
