# DS8: OSS departure corpora, outcomes and a first E-OSS power estimate

- **Question:** Can E-OSS get enough dated, pre-agent truck-factor departures with outcomes that measure knowledge loss, and how many does it need?
- **Answer:** The corpus exists: 315 projects with a dated truck-factor departure (2008–2016), under CC-BY-4.0. A null map is stopped with P ≥ 0.8 from about 600 leaver-owned units (30 departures × 20 units, Bonferroni over 6 baselines; P(Stop | null) = 0.87–0.95 at 30 × 20 across the activity and noise cells). A real gain is read as Continue only if per-unit outcome counts vary from period to period no more than Poisson (P(Continue) ≤ 0.90 at 30 × 20 with ≥ 10 events per unit, one baseline). With negative-binomial period noise (size 10), it stays ≤ 0.34 in every cell up to 120 departures [SYNTHETIC].
- **Changed:** E-OSS gets a pre-*t* dispersion check as its go/no-go before any outcome is read. It also gets an activity floor of 10 outcome events per unit per window and defect-fix commits as the primary label. Option (a) needs a new low-visibility scan, because every departure in the obtainable corpus is in a popular repository.

**Result.** Departures are obtainable, and the count needed is in the tens, as `REORIENTATION.md` §18 assumed. The binding constraint is the outcome's noise, not the number of departures.
- **The corpus.** The 1,932-project corpus of Avelino et al. 2019 [112] is public, CC-BY-4.0. Its `data.rar` lists all 315 projects with a truck-factor-developer detachment (TFDD), one dated TFDD per project, with status and departing developers; `measures.csv` holds 388 TFDD events across 344 repositories. All 315 dates fall in 2008–2016, so all predate agentic coding.
- **Visibility.** These are the top-starred repositories of six languages. At departure their median was 1,195 stars, and only 6 of 314 had ≤ 100. They therefore cannot serve contamination option (a) without screening, and the low-visibility pool needs a new scan.
- **Chromium plus 7** [111] has a live 464 MB replication package (no licence stated). It records generic leavers with per-period file ownership, not truck-factor departures.
- **Base rates.** About 22% of commits are corrective in 7,557 GitHub projects. No verified base rate exists for question or rationale-seeking issues. No file-level dispersion is published. Rationale-seeking issues are too rare to label single units, so they become a secondary, component-level outcome.
- **The simulation's warning.** If per-unit counts are heavily over-dispersed between periods (NB size 2), even an oracle map's mean observed ΔAUROC is 0.065–0.075 at 40 × 20, below δ = 0.10. It continues in only 11–16% of runs and stops in 15–26%. Because its expected ΔAUROC is below δ, more departures push it towards Stop [inferred], so the gate would tend to stop a perfect map; L7.3's "best reachable outcome" fails.
- **Consequence for the pre-registration.** It must measure that dispersion on two pre-*t* windows before any post-*t* outcome is read.

**Decision it feeds.** The §22 threshold rows "E-OSS departures and minimum post-departure activity" and "'Dominate' for a change to H2", and the World B Git adapter (§7). These are proposals: nothing here is registered, and the owner sets the rows through `methods-critic`.

**Method.** The `anthropic-skills:deep-research` workflow was used, with four parallel searches over OpenAlex, arXiv, Zenodo, GitHub and publisher pages on 2026-10-24.
- **Data checked directly.** The Avelino 2019 `data.rar` (1.3 MB) was downloaded and aggregated. Its aggregate counts are reproducible from `tfprojects_commits_new.csv`, `tfprojects_stars.csv` and `measures.csv` (388 events, 344 repositories) in Zenodo record 2546008. The CSVs hold developer names and e-mails, and none was printed or stored here. Every other package was checked by metadata, README and file listing only.
- **The power figures** are SYNTHETIC. They come from `research/ds8-oss-departures/power.py` (spec and generator sha256 in `power.json`) and size the design. They never feed a gate.
- **Reproduce:** `uv run --with numpy python research/ds8-oss-departures/power.py` (about 10 minutes).
- **Cost:** no model was called and nothing was spent.
- **Review.** `citation-verifier` ran four times; the first three runs' findings were fixed, and the fourth returned PASS.
- **Marking.** "[inferred]" marks this note's own reasoning. "Abstract" means only the abstract or a secondary summary was read.

## 1. Dataset register

| Dataset | Hosting, licence (checked 2026-10-24) | Fields relevant to E-OSS | Events and dates | Pre-2023 | Fit |
|---|---|---|---|---|---|
| **Avelino, Constantinou, Valente & Serebrenik 2019**, 1,932 projects [112] ([doi:10.1109/esem.2019.8870181](https://doi.org/10.1109/esem.2019.8870181)) | Zenodo [10.5281/zenodo.2546008](https://doi.org/10.5281/zenodo.2546008), **CC-BY-4.0**, resolves. Files: `data.rar` 1.3 MB, `raw_data.rar` 980 MB, R scripts | `tfprojects_commits_new.csv`: project, status, `tf_date`, commits before and after. `tfdevelopers.csv`, `leavers.csv`: name, e-mail, first and last commit date. `measures.csv`: yearly truck-factor snapshots with commit SHA, TF developers and DOA coverage, TFDD and survival flags | **315 projects with a TFDD**, one date each (128 surviving, 187 not); `measures.csv` has 388 TFDD events in 344 repositories (303 with one, 38 with two, 3 with three). Dates by year: 2008: 2, 2009: 2, 2010: 7, 2011: 20, 2012: 30, 2013: 53, 2014: 76, 2015: 92, 2016: 33. The repository snapshot ends in late 2017 | All 315 | The only verified, licensed register of truck-factor departures with dates. Per-file authorship at *t* must be rebuilt from `raw_data.rar` or a re-clone. The 29 extra repositories in `measures.csv` are presumably filtered later (unverified) |
| **Nassif & Robillard 2017**, Chromium plus 7 [111] ([doi:10.1109/icsme.2017.64](https://doi.org/10.1109/icsme.2017.64)) | [cs.mcgill.ca/~swevo/knowledgeloss](https://www.cs.mcgill.ca/~swevo/knowledgeloss/), `replication_package.zip` 464 MB, last modified 2017-08-03, resolves. **No licence stated** | Per project: commit–author and commit–file lists, leavers and newcomers per 2-week and 3-month period, per-period file ownership (git-blame). Projects: Chromium, GIMP, Assimp, TrinityCore, GitLab CE, Linux (raspberrypi fork), Kodi, Apereo CAS ([author PDF](https://www.cs.mcgill.ca/~martin/papers/icsme2017.pdf)) | Generic leavers (last commit at least one year before the clone), not TF departures; counts not extracted | All, by construction | Gives ownership at period boundaries; TF developers would have to be derived. Ask the authors before redistributing anything |
| **Avelino et al. 2016**, 133 projects [109] ([arXiv:1604.06766](https://arxiv.org/abs/1604.06766)) | The paper's data URL (aserg.labsoft.dcc.ufmg.br/truckfactor) returns **404**. The TF tool, [aserg-ufmg/Truck-Factor](https://github.com/aserg-ufmg/Truck-Factor), is **MIT** | Truck-factor estimates, not departures | — | — | Tool only. Use it to compute TF at *t* |
| **Mirsaeedi & Rigby 2020** ([doi:10.1145/3377811.3380335](https://doi.org/10.1145/3377811.3380335)) | Zenodo [10.5281/zenodo.3678551](https://doi.org/10.5281/zenodo.3678551), **CC-BY-4.0**: SQL Server backups for Rust, CoreCLR, Roslyn, Kubernetes and CoreFX (about 8 GB). Code: [CESEL/RelationalGit](https://github.com/CESEL/RelationalGit), MIT | Review-aware knowledge and files at risk | Departure counts not verified | Not verified | The practical source of a **review-weighted baseline** (§4) |
| **Nourry et al. 2025**, over 36,000 projects ([doi:10.1587/transinf.2025edl8005](https://doi.org/10.1587/transinf.2025edl8005); preprint [arXiv:2412.00313](https://arxiv.org/abs/2412.00313)) | No data package found | — | 89.65% of 36,464 projects had at least one TFDD, and 70% of projects with a TFDD had it within their first three years. The preprint is titled "Myth: The loss of core developers is a critical issue for OSS communities" | Not stated | Shows departures are common in broad samples. No register to download |
| **Calefato et al. 2022** ([doi:10.1007/s10664-021-10012-6](https://doi.org/10.1007/s10664-021-10012-6)) | Scripts only (Zenodo record 4590208 says MIT, GitHub says GPL-3.0) | Breaks and returns of core developers in 18 organisations | Re-run needed | — | Departure-definition evidence (§3), not a register |
| **Fan et al. 2025**, 36,991 Rust packages ([doi:10.1145/3729392](https://doi.org/10.1145/3729392)) | No verified package | Core-developer turnover | — | — | Not usable yet |
| **Rigby et al. 2016** [110] | No public package found; the second case is an Avaya project | — | — | — | Not usable |

**Pre-agent count (question 3).** **315 projects have a dated TF departure before 2023**, all in 2008–2016 (388 TFDD events in `measures.csv`). Nassif & Robillard's leavers all predate August 2017. No other verified register was found.

**Personal data.** The Avelino CSVs carry developer names and e-mail addresses. Pseudonymise them on ingest (§7).

## 2. Outcome codebook outline

**Knowledge loss versus ordinary churn.**
- **Abandoned or leaver-owned files** are the literature's knowledge-loss proxy (Rigby et al. 2016 [110]; Nassif & Robillard 2017 [111]).
- **Ownership predicts defects even without a departure** (Bird et al. 2011, [doi:10.1145/2025113.2025119](https://doi.org/10.1145/2025113.2025119), abstract). A post-*t* rise counts as loss only against a within-project contrast that shares the project's churn.
- **No published study** estimates a file-level DiD of a departure on defect or question outcomes with intervals. Mockus 2010 ([doi:10.1145/1882291.1882311](https://doi.org/10.1145/1882291.1882311)) and Foucault et al. 2015 ([doi:10.1145/2786805.2786870](https://doi.org/10.1145/2786805.2786870)) are associational (both read only as quoted in [Robillard 2021](https://www.cs.mcgill.ca/~martin/papers/esecfse2021.pdf)).
- **The one DiD found** measures the productivity of the developers who remain, not quality (Russo Latona et al. 2024, [doi:10.1145/3589335.3651559](https://doi.org/10.1145/3589335.3651559), abstract).
- **So no effect size can be borrowed.** §5 posits one [inferred].

| Element | Definition (proposal) | Evidence and reliability |
|---|---|---|
| **Unit** | A directory existing at *t* (blame at *t*) in which the leaver holds a pre-*t* ownership share above a registered threshold. Directories, not files, so that units reach the activity floor | Most files have 0–1 fix commits per month, so file-level labels are noise [inferred from the base rates below] |
| **Control units** | Directories in the same project the leaver never touched. They carry the project's activity drop, newcomers, releases and platform changes | Within-project contrast [inferred] |
| **Primary outcome** | Corrective (defect-fix) commits touching the unit, classified from the commit message, with a log-commit offset | About 22% of commits are corrective (22.7% in 2018, 22.3% in 2019; 7,557 projects). The median project's corrective-commit probability is 0.20; the worst decile is ≥ 0.39 and the best ≤ 0.06. Human κ ≥ 0.9. The classifier has accuracy 93.0%, recall 84.1% and FPR 4.2%, with an ML correction for known recall and FPR (Amit & Feitelson 2021, [doi:10.1007/s11219-021-09564-z](https://doi.org/10.1007/s11219-021-09564-z); numbers read in [arXiv:2007.10912](https://arxiv.org/abs/2007.10912)) |
| **Secondary outcome** | Rationale-seeking issues (why is it so, how does it work, who knows it) mentioning the unit's component. Read at component level, not per unit | No verified base rate. The NLBSE'22 benchmark labels over 800k issues as bug, enhancement or question ([organisers' page](https://nlbse2022.github.io/tools/)), but its question share is unverified and is a benchmark's label mix, not a base rate. Rationale-seeking issues are a subset of questions, with no verified rate and no published κ. The blind second coder sets the floor |
| **Not used** | Issue-tracker "bug" labels | 33.8% of reports filed as bugs were not bugs, in a manual check of over 7,000 issue reports from five projects (Herzig, Just & Zeller 2013, [doi:10.1109/icse.2013.6606585](https://doi.org/10.1109/icse.2013.6606585)) |
| **Negative-control outcome** | Feature or enhancement commits on the same units | Knowledge loss should not raise them [inferred] |
| **Label** | Per departure, the unit's post/pre corrective rate ratio divided by the control units' ratio, above a registered threshold | §5 simulates this label |
| **Covariate only** | Abandoned files | Defined by authorship (`REORIENTATION.md` §18) |
| **Coding** | Both outcomes blind to the gap map, the arm and the departure date. Owner plus one blind second coder on at least 20% (§18 common rules) | — |

**Published variance.** The only published stability figure is project-level and annual. A project's corrective-commit probability correlates 0.86 between successive years (projects with ≥ 200 commits in each), with a mean absolute change of 5.5 points. Across projects it is higher in older ones, 0.18 at year 1 against 0.23 at year 10, a cross-sectional figure the authors note carries survival bias (Amit & Feitelson 2021). Nothing is published on how a directory's count varies between periods, and §5 shows that this is the number that decides E-OSS.

## 3. Confounders

| Confounder | Mechanism | Handling (proposal) | Source |
|---|---|---|---|
| Activity level | The departure lowers activity, so raw counts fall | Log-activity offset; control units in the same project | [inferred] |
| Regression to the mean | A one-year-inactivity rule means the leaver's activity falls before *t* by construction | Set *t* at the last commit and drop a 3–6-month buffer before *t* from the pre-period | Departure rule: Avelino 2019 [112] |
| False departures | From the gone state (a break of a year or more), average transition probabilities were 26% back to coding, 21% to non-coding work and 54% remaining gone (538 core developers, 18 organisations) | Require confirmed absence from *t* to *t* + 12 months; a sensitivity analysis drops returners | Calefato et al. 2022 |
| Newcomer influx | New TF developers had touched a median 41% of files in surviving projects; external newcomers were associated with lower quality | Time-varying newcomer count; survival status as a stratum | Avelino 2019 [112]; Foucault 2015 (as quoted in Robillard 2021) |
| Project age | Older projects show a higher corrective share (cross-sectional, survival-biased) | Age at *t* as a covariate | Amit & Feitelson 2021 |
| Release cycles and seasonality | Fix bursts around releases | Month fixed effects; release dates as covariates. No precedent found in turnover studies | [inferred] |
| GitHub Discussions | Opened to all projects in December 2020. In 92 early-adopter projects, 12% of 9,234 discussions had been converted from issues | Adoption date as a covariate, or windows wholly before 2020-12. Pre-2017 departures avoid it | Hata et al. 2022, [doi:10.1007/s10664-021-10058-6](https://doi.org/10.1007/s10664-021-10058-6) |
| Bots | Bot comments and commits inflate counts | Exclude bots with a ground-truth classifier for issue and PR comments; commit bots need a separate rule | Golzadeh et al. 2021, [doi:10.1016/j.jss.2021.110911](https://doi.org/10.1016/j.jss.2021.110911) |
| Internal transfer, partial disengagement | Leavers can remain partly reachable ("partial departure"), and an internal transfer can amount to a departure (interviews with 27 practitioners in three companies) | Limitation; not separable in public data | Robillard 2021 |
| Post-*t* edits leaking into pre-*t* text | GitHub's live API returns current, edited text | Take pre-*t* text from GH Archive event payloads or Software Heritage snapshots | [GH Archive](https://www.gharchive.org/) [inferred] |
| Staggered departure dates | Two-way fixed effects pooled across departures at different dates is biased when effects vary over time after treatment (already-treated units act as controls) | Estimate each departure against its own control units and pool the per-departure contrasts; no cross-departure TWFE | Goodman-Bacon 2021, [doi:10.1016/j.jeconom.2021.03.014](https://doi.org/10.1016/j.jeconom.2021.03.014) |

## 4. Review-weighted concentration and the R8 cut-off

**Measures that weight review** (question 3). None has been validated against what happened after a real departure.
- **Jabrayilzade et al. 2022 [114]** ([arXiv:2202.01523](https://arxiv.org/abs/2202.01523), abstract) combine version control, code review and meetings. They were tested on 13 JetBrains projects against engineers' survey answers and did "slightly better" than Avelino's tool. No code was found, and meeting data does not exist in OSS, so the measure cannot be reproduced as published.
- **Thongtanunam et al. 2016** ([doi:10.1145/2884781.2884852](https://doi.org/10.1145/2884781.2884852), abstract) add review activity to ownership on Qt and OpenStack, validated against post-release defects.
- **Mirsaeedi & Rigby 2020** compute review-based knowledge and files at risk. Their code and data are open (§1). The follow-up reports −28% files at risk under turnover-aware review recommendation (Hajari et al., [arXiv:2312.17236](https://arxiv.org/abs/2312.17236), abstract).
- **Proposal** [inferred]. Add **review-aware files at risk** (Thongtanunam-style author ∪ reviewer ownership fed into a Rigby-style KaR) to the E-OSS baselines under both contamination options, not only under option (b). Name Fritz's degree-of-knowledge as DOA when it is computed from Git alone: its interaction component is not in public data.

**Cut-off for R8** [115].
- **Agent launches.** The earliest agent launch dated here is Devin, announced on 2024-03-12 ([Cognition](https://cognition.ai/blog/introducing-devin)). Copilot agent mode followed in VS Code Insiders on 2025-02-06 ([GitHub blog](https://github.blog/news-insights/product-news/github-copilot-the-agent-awakens/); general rollout 2025-04-04, [GitHub blog](https://github.blog/news-insights/product-news/github-copilot-agent-mode-activated/)), and the Claude Code research preview on 2025-02-24 ([Anthropic](https://www.anthropic.com/news/claude-3-7-sonnet)).
- **Earlier assistance.** Code-completion assistants predate the agents and leave no trace in commits, so no recent window is guaranteed free of AI [inferred].
- **Proposal** [inferred]. The primary sample uses pre-*t* windows ending before 2023-01-01, which every Avelino departure satisfies by six years. A sensitivity sample ends before 2024-03-12 and still runs the screen below. Flag any repository whose pre-*t* window carries agent trailers or agent bot accounts. The AIDev dataset (932,791 agent-authored PRs; [arXiv:2602.09185](https://arxiv.org/abs/2602.09185), abstract) can screen for these.
- **Wheeler's claim** [115] (single author, no data) predicts that authorship metrics fail in agent-era histories. E-OSS on pre-agent histories tests those baselines where they should work best.

## 5. First power estimate [SYNTHETIC]

**Model** (`power.json` → `spec.model`).
- **Units.** Per departure, *m* leaver-owned units. Latent loss *z* has prevalence about 0.3 (Beta across departures), and loss doubles the outcome rate.
- **Activity.** Every unit has at least `floor` expected outcome events per window, pre and post.
- **Noise.** Between-unit heterogeneity cancels in the unit's own post/pre ratio, so only period-to-period noise is simulated: negative binomial with size 2 or 10, or Poisson. The observed label is post/pre > √2.
- **Scores.** The map and the strongest baseline both have latent AUROC 0.62 under the null; under the alternative the map has 0.82 against 0.62. Their noise correlation is 0.5.
- **Gate.** The statistic is the pooled within-departure Mann–Whitney ΔAUROC with a departure-cluster variance. The N3 rule applies at c = 1.85. Stop uses either one baseline (z = 1.85) or Bonferroni over 6 baselines at the same level (z = 2.55, this note's reading of "Bonferroni at c").
- **Not modelled.** The settings are assumptions, not estimates: no published file- or directory-level effect or dispersion exists (§2).
- **Upper bound.** Continue is simulated against one baseline in one look. The registered rule is intersection–union across baselines with a pooled fallback look (`REORIENTATION.md` §22), so each P(Continue) here is an upper bound. The noise correlation is fixed at 0.5; I5 finds r decisive.

**Departures for P(Stop | null map) ≥ 0.8** (`power.json` → `minimum_departures`). This depends almost only on the number of labelled units:

| Units per departure | 1 baseline (z = 1.85) | Bonferroni, 6 baselines (z = 2.55) |
|---|---|---|
| 20 | 15–20 | **30** |
| 10 | 40 | **60** |

That is about 300–400 units for one baseline and about 600 under Bonferroni, in every activity and noise cell.

**Continue under a latent gain of 0.20** (one baseline; an upper bound). This depends on the label noise:

| Activity floor (events per unit per window) | Period noise | Oracle map's observed ΔAUROC (40 × 20) | Departures for P(Continue) ≥ 0.8 (20 units) |
|---|---|---|---|
| 10 | Poisson | 0.237 | 20 |
| 20 | Poisson | 0.303 | 10 |
| 10 | NB size 10 | 0.142 | not reached by 120 (P ≤ 0.26) |
| 10 | NB size 2 | 0.072 | not reached (P ≤ 0.09) |
| 2–20 | NB size 2 | 0.065–0.075 | not reached |

**The rule fails L7.3 under heavy period noise.**
- **Best reachable outcome.** With size-2 noise an oracle map (it knows *z*) reaches a mean observed ΔAUROC of only about 0.07, below δ, so P(Continue) ≥ 0.8 is unreachable at any count [inferred] (oracle P(Continue) = 0.11–0.16 at 40 × 20; one baseline, an upper bound).
- **Planted positive.** An oracle under Poisson noise at a floor of 20 continues with P = 1.00 (`selfcheck`; one baseline, an upper bound).
- **Trivial stand-in.** A score equal to unit activity never continues and stops with P = 1.00 (`selfcheck`). The rule discriminates only where the labels are reliable.
- **Stopping a real gain.** With size-2 noise the gate stops a real latent gain of 0.20 with P = 0.71 at 30 × 20 and 0.85 at 40 × 20 (floor 10; one baseline, z = 1.85; `p_stop_gain`; not simulated under Bonferroni). There, a Stop would read label noise as a falsification of H1. Under Poisson noise the same cells stop it with P = 0.003.
- **False Continue.** A null map continues with P ≤ 0.053 in every cell (`p_continue_null`).

**Proposed threshold row** [inferred, SYNTHETIC basis].
- **Departures.** At least 30 departures with at least 20 eligible units each, or more departures to reach about 600 eligible units in total.
- **Activity floor.** At least 10 primary-outcome events per unit in each of the pre- and post-*t* windows (corrective commits, for example over 12 months either side).
- **Go/no-go on dispersion.** Before any post-*t* outcome is read, estimate the period-to-period dispersion of each eligible unit's corrective count on two consecutive pre-*t* windows. If it is materially above Poisson, E-OSS cannot reach P(Continue) ≥ 0.8 for a latent gain of 0.20 (≤ 0.34 at NB size 10, ≤ 0.13 at size 2), and it is registered as unable to read rather than run.

**Feasibility** [inferred].
- **Activity in the corpus.** 229 of the 315 Avelino TFDD projects had at least 100 commits after their TFDD by late 2017, and 86 had at least 500. These are project-level figures; how many directories per departure reach 10 corrective commits per window must be measured on pre-*t* data.
- **Where the shortfall lands.** If fewer than 20 units qualify, the departure count scales as about 600 / *m*.

## 6. Contamination option (a): low-visibility repositories

**No named repository qualifies today.** This is not settled by a repository list; the deliverable is a rule plus a scan.
- **The Avelino corpus is high-visibility.** At departure the median was 1,195 stars, only 6 of 314 had ≤ 100, and every one of the 314 projects with star data had at least 882 (`today_stars`, collection date not stated).
- **Membership checks.** The Stack v2 includes GitHub pull requests as well as code. Its released SWHIDs cover the source code, so code membership can be checked by content hash; PR membership needs a separate check, for example by repository and PR number ([arXiv:2402.19173](https://arxiv.org/abs/2402.19173), abstract).
- **What drives memorisation.** It grows log-linearly with duplication (Carlini et al., [arXiv:2202.07646](https://arxiv.org/abs/2202.07646)). No star threshold for "not memorised" was found.
- **Probe.** The best guided-completion variant matched human experts on 92–100% of partition-level contamination verdicts over seven datasets; instance-level agreement is not reported (Golchin & Surdeanu, [arXiv:2308.08493](https://arxiv.org/abs/2308.08493)). The per-item probe proposed below therefore has no published accuracy.

**Rule (proposal)** [inferred].
1. **Pre-screen.** Low stars and forks (for example ≤ 100 stars, ≤ 20 forks at the scan date) no SWHID match for the code in The Stack v2, and the repository's PRs absent from its PR subset.
2. **Criterion.** A pre-registered guided-completion probe on post-*t* issue titles and commit messages, excluding hits (`REORIENTATION.md` §18). The pre-screen only filters; the probe decides.
3. **Candidate pool.** A broad sample in the style of Nourry et al., where most projects have a TFDD, mostly in years 1–3, intersected with the activity floor.

**The tension.** Young, low-star projects rarely reach 10 outcome events per directory per window. The scan must report the yield; a rough guess of 500–1,000 candidates for 30–40 usable departures is unmeasured.

**Option (b)**, outcome windows after every model's cutoff, needs departures from 2026 onward. Those are agent-era, so option (b) relies wholly on review-weighted baselines (R8). Under option (b) the 315 pre-agent departures are unusable.

**Recommendation** [inferred]. Option (a) is the only route consistent with pre-agent histories. Its yield is unknown until the scan runs, so the scan is the next E-OSS step.

## 7. Text arm against trace arm for H2, and the World B adapter

**Prior evidence.**
- Process metrics beat code metrics for defect prediction (Rahman & Devanbu 2013, [doi:10.1109/icse.2013.6606589](https://doi.org/10.1109/icse.2013.6606589); Moser et al. 2008, [doi:10.1145/1368088.1368114](https://doi.org/10.1145/1368088.1368114); both abstracts).
- Over 700 GitHub projects the best process-metric learner reached a median AUC of 0.95 against 0.54 for the best product-metric learner (Majumder, Mody & Menzies, [arXiv:2008.09569](https://arxiv.org/abs/2008.09569); EMSE 2022, [doi:10.1007/s10664-021-10068-4](https://doi.org/10.1007/s10664-021-10068-4)).
- No study was found that compares process or trace inputs against documentation or text inputs as nested predictor sets. H2's contrast is open.
- E-OSS's label is a *change* in rate, not a level. A trace baseline that predicts defect level well (prior trouble) need not predict the post-*t* rise, and regression to the mean can make it predict a fall [inferred].

**Design** [inferred]. One gap map is built three times from inputs dated ≤ *t*:
- **T (text).** READMEs and docs, ADRs, code comments, commit messages, and issue and PR text.
- **R (trace).** Blame at *t*, co-change, review participation and approvals, CI outcomes and who-touches-what.
- **T+R.** Both.

The three maps are scored on the same units, labels, exclusions and departures, so the arms differ only in input set and the conclusion names only that (L7.4). The E-OSS baselines are themselves trace measures (prior trouble, churn, TF, KaR, review-aware files at risk), so H1 compares T+R against them. H2 compares the arms with each other.

**"Dominate" (proposal for the §22 row).** Change to H2 if both hold at boundary c:
1. AUROC(R) − AUROC(T) has a lower bound above 0 and a point estimate ≥ δ. Traces beat text.
2. AUROC(T+R) − AUROC(R) has an upper bound below δ. Text adds less than δ once traces exist.
- **Sample size.** Both comparisons are paired on the same units; their power is not simulated here [inferred], so the ~600-unit figure is a floor to check, not a size.
- **Multiplicity.** The two conditions form an intersection, so no adjustment applies within H2. They add one family to the N3 readings, and the pre-registration states how.
- **Ceiling.** If R's AUROC sits near the ceiling, condition 2 is easy to meet. Report AUROC(R) beside it.

**E-DVP.**
- **No norm-enforcement dataset.** No public, openly licensed dataset labels review comments as norm or convention enforcement. Mäntylä & Lassenius ([doi:10.1109/tse.2008.71](https://doi.org/10.1109/tse.2008.71)) found 75% of review-found defects are evolvability, not functional. Beller et al. found 10–22% of review-induced changes had no explicit comment ([doi:10.1145/2597073.2597082](https://doi.org/10.1145/2597073.2597082)), so comment text undercounts enforcement, and the revision diff (a trace) catches some of the rest.
- **Codebook seed.** Aghajani et al. 2019 [116] (878 artefacts; [doi:10.1109/icse.2019.00122](https://doi.org/10.1109/icse.2019.00122)) can seed the codebook. Its public replication package ([GitHub](https://github.com/anonymouspaperauthors-ICSE19/replicationpackage)) lists 183 final Issue tags and has no licence file. Read and cite it; do not redistribute it.
- **Rejections.** Gousios et al. 2014 ([doi:10.1145/2568225.2568260](https://doi.org/10.1145/2568225.2568260)) found that technical reasons are only a small minority of PR rejections. E-DVP should count only rejections where a maintainer cites a rule [inferred].

**DeepWiki** [126]. The pages are generated from a repository's current or last-indexed state ([Devin docs](https://docs.devin.ai/work-with-devin/deepwiki)), so they post-date *t*. DeepWiki is admissible only as a SYNTHETIC predictor, with its indexed commit captured at retrieval, and never as a pre-*t* input [inferred].

**World B adapter requirements** (`docs/plans/n3-gap-map-plan.md` § "E-OSS needs").
1. **Pre-*t* text** comes from GH Archive payloads or Software Heritage snapshots, never the live API.
2. **The freeze commit** is the last commit at or before *t*. Avelino's `measures.csv` SHAs sit on a yearly grid and do not mark *t*.
3. **Mapping.** Commits, issues, PRs, review threads and ADRs map to `COMMIT`, `ISSUE`, `REVIEW_THREAD` and `DESIGN_RECORD`, with author-keyed independence.
4. **Concentration.** DOA truck factor via the MIT tool; review-aware files at risk via RelationalGit's approach.
5. **Units** are directories with a per-unit activity count for the floor.
6. **Pseudonymisation.** Identities pass through a keyed hash held outside the repository before anything is stored. Outputs stay at unit and project level only; anonymisation is "almost impossible" because code changes re-identify developers (Gold & Krinke 2022, [doi:10.1007/s10664-021-10057-7](https://doi.org/10.1007/s10664-021-10057-7)).
7. **Legal and access conditions.** A legitimate-interest record (`REORIENTATION.md` §21). Open-access publication: GitHub's Acceptable Use Policies allow research use of public, non-personal information only if the publications are open access ([AUP §7](https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies)). No contact with developers.

## 8. What would change this

- **The dispersion check.** If it finds near-Poisson period noise for directories at 10 or more events, Continue is reachable with 10–20 departures of 20 units each (one baseline; an upper bound), and the Stop count (about 600 units) binds. If it finds negative-binomial size ≤ 10, E-OSS cannot reach P(Continue) ≥ 0.8 for a latent gain of 0.20 (≤ 0.34), and N3's "E-OSS decides" branch reads inconclusive, so H1 is not shown and the owner rule pivots to H3.
- **Pooled count model.** Labelling by a pooled count model instead of per-unit thresholds (an NB GLMM with a unit random effect) may recover power. This note did not simulate it.
- **Too few eligible units.** If fewer than about 30 departures with 20 eligible units survive the low-visibility probe, option (a) fails on count, and only option (b), which is agent-era, remains.

## Open checks

- Reconcile the 29 repositories flagged in `measures.csv` but absent from the 315-project list. Over the 315 the one/two/three-TFDD split is 276 / 36 / 3, matching the paper's 88% / 11%; over all 344 it is 303 / 38 / 3, which rounds the same way. The paper's 315 base is the one to use.
- Check how many of the 315 repositories still resolve on GitHub.
- Extract the per-project leaver counts from the Nassif & Robillard package.
- The Turzo & Bosu review-comment categories and the licences of their data were not read.
- No κ is published for coding rationale-seeking issues.
