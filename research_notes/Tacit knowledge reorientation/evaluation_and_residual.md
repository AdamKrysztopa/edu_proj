# Evaluating autonomous domain reconstruction without new participants; the human knowledge residual; choosing expert questions by information gain

Scope: how to test, with zero new participants and without relying on LLM-as-judge alone, whether AI-reconstructed domain models are correct and useful. The models cover concepts/KCs, prerequisites, misconceptions, expert–novice differences and diagnostic items. Also covered: how to measure the knowledge that only humans add, and how to pick the expert questions that reduce it fastest.

Evidence tags: **ESTABLISHED** means replicated or standard method. **PROMISING** means one or a few peer-reviewed or preprint results. **SPECULATIVE** means my inference with no direct test. Licence flags: **NC** means non-commercial only; **?** means licence not verified in this pass.

Identifiers were checked on 2026-09-28. DOIs and titles were resolved through OpenAlex/Crossref. arXiv abstracts were read from arxiv.org. Quantitative claims were read from the abstract or full text unless marked otherwise.

---

## 1. Public ground truth: which resources can serve as held-out gold, per artefact type

### Takeaway
Public gold exists for every artefact type in education, and it is richest in mathematics and science misconceptions. The Eedi Misconception Graph (8,000+ misconceptions, CC BY 4.0), the Eedi NeurIPS 2020 diagnostic-question responses, AAAS item-level misconception data, DataShop logs with expert KC models, and the BEA 2024 USMLE item statistics are the strongest anchors. Organisational and professional domains have task and competency lists (O*NET CC BY 4.0, ESCO, AAMC EPAs, CS2023) but almost no public learner-response data. Many interaction datasets are non-commercial (EdNet, Junyi), and the Stack Exchange dump now carries anti-LLM-training terms.

### Cited Findings

**Misconception / distractor gold (the most direct "catalogued misconceptions")**
- ESTABLISHED. The Force Concept Inventory (Hestenes, Wells & Swackhamer 1992, *Phys. Teach.* 30:141) is the canonical physics inventory whose distractors encode Newtonian misconceptions. It is still "the most commonly used concept inventory" in physics-education research — [Crossref DOI 10.1119/1.2343497](https://doi.org/10.1119/1.2343497); [Küchemann et al. 2024, Front. Psychol.](https://doi.org/10.3389/fpsyg.2024.1426209). It is distributed through PhysPort ([page resolves](https://www.physport.org/assessments/assessment.cfm?A=FCI)). Access terms are **?**.
- ESTABLISHED. Distractor-driven instruments are the recognised bridge between qualitative misconception research and psychometrics. Sadler (1998) modelled how distractor choice varies with ability (IRT on misconception-based distractors) — [Sadler 1998, JRST, doi 10.1002/(SICI)1098-2736(199803)35:3<265::AID-TEA3>3.0.CO;2-P](https://doi.org/10.1002/(sici)1098-2736(199803)35:3%3C265::aid-tea3%3E3.0.co;2-p).
- ESTABLISHED. AAAS Project 2061 assessment items show, for each item, the misconceptions embedded in the answer choices. They also give the national field-test distribution of responses and percent correct by grade, gender and language. More than 150,000 students were involved since 2004 — [AAAS news](https://www.aaas.org/news/new-testing-feature-aaas-web-site-helps-teachers-find-gaps-students-science-knowledge); [AAAS assessment "About"](http://assessment.aaas.org/pages/about). The original host did not respond in my check. A mirror resolves at [assess.bscs.org](http://assess.bscs.org/science/pages/about). Licence **?**.
- ESTABLISHED (resource). **Eedi Misconception Graph**: "a mapping of more than 8,000 common maths misconceptions, informed by 200 million real student responses", released open-source under **CC BY 4.0** through Learning Commons — [Eedi news](https://www.eedi.com/news/from-wrong-answers-to-real-insights-how-we-used-a-kaggle-challenge-to-map-student-misconceptions); [Learning Commons announcement](https://learningcommons.org/news/ai-platform-launch/).
- ESTABLISHED (resource). **Eedi NeurIPS 2020 Education Challenge**: 20M+ student answers to 4-option diagnostic MCQs "whose distractors embody misconceptions" (Sept 2018 – May 2020). There were four tasks, including predicting which option a student picks. Nearly 400 teams made about 4,000 submissions — [Wang et al. 2020, arXiv:2007.12061](https://arxiv.org/abs/2007.12061); [Wang et al. 2021 results, arXiv:2104.04034](https://arxiv.org/abs/2104.04034). Licence **?** (not stated in the guide PDF). The dataset won best dataset at EDM 2021 — [Eedi news](https://www.eedi.com/news/from-wrong-answers-to-real-insights-how-we-used-a-kaggle-challenge-to-map-student-misconceptions).
- ESTABLISHED (resource). **Kaggle "Eedi – Mining Misconceptions in Mathematics"** (2024): predict the misconception behind each distractor, scored by MAP@25 — [Kaggle](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics). Competition-data terms **?**. The CC BY 4.0 graph above is the safer reuse route.
- PROMISING (synthetic gold). **MalAlgoPy** builds algebra misconception datasets from a graph representation of solution steps. Instruction-tuning LLMs on misconception examples replicates the errors but lowers correct solving where the misconception does not apply — [Sonkar et al. 2024, arXiv:2410.12294](https://arxiv.org/abs/2410.12294). Caveat: the gold here is written by the library's authors, not observed in students. Repo licence **?**.

**Learner-log gold (lets you test a KC or prerequisite model against behaviour, not against opinion)**
- ESTABLISHED. **PSLC DataShop** offers public datasets (login required). Its tools include Learning Curve, AFM parameter values and KC-model export/import, so alternative KC models can be uploaded and scored on the same logs — [DataShop](https://pslcdatashop.web.cmu.edu/); [Stamper & Koedinger 2011](https://learnlab.org/wp-content/uploads/2016/06/Stamper-Koedinger-2011.pdf). As of Dec 2011 it held more than 300 datasets and more than 70M student actions — [Koedinger, McLaughlin & Stamper 2012, ERIC ED537201](https://files.eric.ed.gov/fulltext/ED537201.pdf). "Nearly 60% of the 4,639 datasets available in DataShop" have no KC model beyond the default Single-KC and Unique-step baselines — [Wei, Carvalho & Stamper 2025, KCluster, arXiv:2505.06469](https://arxiv.org/abs/2505.06469). Terms of use **?** (the terms page returned HTTP 500).
- ESTABLISHED. **EdNet**: 131M interactions from 784k students (Santa tutoring service, Korea). Licence reported as **CC BY-NC 4.0 (NC)**, per the search-engine summary of the paper, not opened directly — [Choi et al. 2020, arXiv:1912.03072 / doi 10.1007/978-3-030-52240-7_13](https://arxiv.org/abs/1912.03072).
- ESTABLISHED. **Junyi Academy** problem logs with exercise-related metadata (whether it includes a usable prerequisite map was not verified here). Licence **CC BY-NC-SA 4.0 (NC)** — [Kaggle dataset page](https://www.kaggle.com/datasets/junyiacademy/learning-activity-public-dataset-by-junyi-academy).
- ASSISTments datasets (2009, 2013, etc.) are widely used for knowledge tracing. Licence **?** — [IEEE DataPort listing](https://ieee-dataport.org/documents/assistments-dataset-2009-2010).
- ESTABLISHED. **BEA 2024 shared task**: 667 retired USMLE MCQs with empirical difficulty (p-value) and mean response time; 17 teams — [Yaneva et al. 2024, BEA findings](https://aclanthology.org/2024.bea-1.39/).

**Curricula, standards, competency and task gold (for concept and prerequisite coverage, and for organisational domains)**
- ESTABLISHED. The **O*NET 31.0** database (occupational tasks, knowledge, skills) is **CC BY 4.0** — [O*NET licence](https://www.onetcenter.org/license_db.html).
- **ESCO** (EU skills/occupations taxonomy). Reuse is governed by Commission reuse policy (Decision 2011/833/EU, per search summary). Exact terms **?** — [ESCO "Use ESCO"](https://esco.ec.europa.eu/en/use-esco).
- These pages resolve (HTTP 200 on 2026-09-28); licence terms **?**: ACM/IEEE-CS/AAAI **CS2023** ([csed.acm.org](https://csed.acm.org/)); **AAMC Core EPAs** ([aamc.org](https://www.aamc.org/about-us/mission-areas/medical-education/cbme/core-epas)); **USMLE Content Outline** ([PDF](https://www.usmle.org/sites/default/files/2021-08/USMLE_Content_Outline.pdf)); **NGSS** ([nextgenscience.org](https://www.nextgenscience.org/)). The Learning Commons Knowledge Graph also bundles state standards, "granular learning components" and learning progressions — [Learning Commons](https://learningcommons.org/news/ai-platform-launch/).

**Expert–novice and CTA gold**
- ESTABLISHED. Chi, Feltovich & Glaser (1981): experts categorise physics problems by deep principle, novices by surface features. It is a canonical, replicable expert–novice contrast — [doi 10.1207/s15516709cog0502_2](https://doi.org/10.1207/s15516709cog0502_2).
- ESTABLISHED (design template). Sullivan et al. (2014) built a "gold standard" cricothyrotomy task list from CTA with 6 surgeons, then scored each expert's teaching and free recall against it — [Acad. Med., doi 10.1097/ACM.0000000000000224](https://doi.org/10.1097/acm.0000000000000224). Published CTA task lists like this are ready-made held-out gold.

**Expert-only knowledge benchmarks**
- ESTABLISHED. **GPQA**: 448 expert-written biology, physics and chemistry MCQs. PhD experts score 65% (74% after discounting clear mistakes). Skilled non-experts with the web score 34% after more than 30 minutes. The GPT-4 baseline scored 39% — [Rein et al. 2023, arXiv:2311.12022](https://arxiv.org/abs/2311.12022).
- ESTABLISHED. **Humanity's Last Exam**: 2,500 expert-written questions "that cannot be quickly answered via internet retrieval"; state-of-the-art LLMs showed low accuracy and calibration — [Phan et al. 2025, arXiv:2501.14249](https://arxiv.org/abs/2501.14249).

**Novice-difficulty corpora**
- ESTABLISHED (licence risk). The Stack Exchange data dump is CC BY-SA content. Since July 2024 it is downloadable only after login and agreement to terms excluding "projects that … include training a large language model". Critics argue this conflicts with CC BY-SA — [devclass 2024](https://devclass.com/2024/07/30/stack-exchange-restricts-access-to-dump-of-user-contributed-data-as-critics-complain-license-permits-reuse-for-any-purpose/); [ArchiveTeam wiki](https://wiki.archiveteam.org/index.php/Stack_Exchange). Using it for evaluation (not training) appears to be within the stated terms. This is my reading, not legal advice.

### Inferences
- SPECULATIVE. The Eedi graph plus the NeurIPS 2020 responses is the best single testbed. It links misconception labels, the distractors that embody them, and real selection frequencies. A reconstruction can then be scored on recall (did it find the misconception?) and on usefulness (does it predict which distractor students pick?).
- SPECULATIVE. For physics, the combination is FCI/AAAS distractors (catalogue), AAAS response distributions (prevalence) and DataShop physics/statics logs (learning curves). It covers all three test types, though at small scale.
- SPECULATIVE. Organisational domains (IT ops, maintenance) have task lists (O*NET/ESCO) but no public "misconception" or learner-log gold. For them only coverage-type tests are possible. Usefulness tests would need proxy data, for example incident post-mortems, which I did not verify here.

### Gaps
- Not verified in this pass: licences for DataShop, ASSISTments, the Eedi NeurIPS 2020 data, the Kaggle Eedi data, MalAlgoPy, CS2023, NGSS, USMLE outline and AAMC EPAs; FCI access terms on PhysPort.
- Not located or verified: the Pfundt & Duit / Duit STCSE misconception bibliography (IPN Kiel); the Calculus Concept Inventory; thermodynamics inventories; Physics Forums or Reddit as corpora; textbook "common mistakes" sections as structured data; public gold for law, OSS projects, industrial maintenance and IT ops.
- No public dataset found that pairs a published CTA with learner-log data in the same domain.

---

## 2. Evaluation designs that avoid LLM-as-judge circularity

### Takeaway
Three evaluation families score AI-built domain models against real human behaviour, not a model's opinion:
1. **Learning-curve fit** of a generated KC model on real logs (AFM/LFA in DataShop).
2. **Prediction of real response statistics**: distractor choice, item difficulty, discrimination.
3. **Held-out-source and temporal-holdout recall** against published expert artefacts.

Machine-discovered KC models already beat expert models on fit (ESTABLISHED for LFA, PROMISING for LLMs). Predicting item difficulty from text barely beats a constant baseline. LLM judges agree with humans on easy, high-agreement tasks but show self-preference, leniency and task-dependent validity. So any judge must be calibrated against human labels first, and should be a panel, not the model being evaluated.

### Cited Findings

**Learning-curve fit (behavioural validity of KC or prerequisite structure)**
- ESTABLISHED. Learning Factors Analysis searches over splits and merges of a KC (Q-matrix) model, scored by the Additive Factors Model — [Cen, Koedinger & Junker 2006, doi 10.1007/11774303_17](https://doi.org/10.1007/11774303_17).
- ESTABLISHED. Human–machine discovery example: splitting a geometry KC lowered BIC from 5,677 to 5,628 and 3-fold CV RMSE from 0.4064 to 0.4021, and the improvement transferred to a second dataset — [Stamper & Koedinger 2011, doi 10.1007/978-3-642-21869-9_46](https://learnlab.org/wp-content/uploads/2016/06/Stamper-Koedinger-2011.pdf).
- ESTABLISHED. Across 11 DataShop datasets in 4–5 domains (geometry, algebra, fractions, English articles, statistics), "a machine-generated model is the best predictor of student performance across all eleven datasets" (10-fold item-stratified CV). RMSE gains are small overall, for example geometry 0.4129 (original) → 0.4033 (best by hand) → 0.4011 (best LFA). The discovered models also had steeper learning slopes — [Koedinger, McLaughlin & Stamper 2012, EDM](https://files.eric.ed.gov/fulltext/ED537201.pdf). The authors note that overall RMSE hides large local changes to a few KCs.
- ESTABLISHED (closing the loop). A tutor redesigned from data-discovered KC changes produced learning gains, per the title and abstract. Effect sizes were not re-verified here — [Koedinger et al. 2013, AIED, doi 10.1007/978-3-642-39112-5_43](https://link.springer.com/chapter/10.1007/978-3-642-39112-5_43); [JEDM, "Closing the Loop: Automated Data-Driven Cognitive Model Discoveries Lead to Improved Instruction and Learning Gains" (authors not re-verified)](https://jedm.educationaldatamining.org/index.php/JEDM/article/view/212).
- PROMISING. **KCluster** clusters questions with an LLM-induced similarity metric. It "discovers KC models that predict student performance better than the best expert-designed models available" on E-learning datasets — [Wei, Carvalho & Stamper 2025, arXiv:2505.06469](https://arxiv.org/abs/2505.06469). A small language model (Phi-2) was also effective for KC discovery — [Wei et al. 2025, arXiv:2505.08588](https://arxiv.org/abs/2505.08588).
- PROMISING. GPT-4 KC generation matched human KCs for 56% of Chemistry and 35% of E-learning MCQs. Expert evaluators preferred the LLM KC about two-thirds of the time when the two disagreed — [Moore, Schmucker, Mitchell & Stamper 2024, arXiv:2405.20526](https://arxiv.org/abs/2405.20526). Note: the preference result is itself a human-judgement measure, not a behavioural one.

**Predicting real response statistics**
- PROMISING. LLM generation likelihoods correlate only moderately with how often students select each distractor. When LLMs err, they tend to pick the same wrong option most students pick — [Liu, Sonkar & Baraniuk 2025, arXiv:2502.15140](https://arxiv.org/abs/2502.15140).
- PROMISING. On real math MCQ data (Eedi), LLMs "can generate some mathematically valid distractors" but "are less adept at anticipating common errors or misconceptions among real students" — [Feng et al. 2024, arXiv:2404.02124](https://arxiv.org/abs/2404.02124). The MISTAKE method (cycle consistency between wrong answers and latent misconceptions) improves alignment with expert-written distractors and misconception inference — [arXiv:2510.11502](https://arxiv.org/abs/2510.11502).
- ESTABLISHED (negative result). BEA 2024: on 667 USMLE items the best difficulty system reached RMSE 0.299 against a dummy-regressor baseline of 0.311. The top 15 were nearly tied, "consistent with the prior literature" (e.g., 0.225 vs 0.237 on 12,038 items). Response time was more predictable: 23.9 vs a baseline of 31.7 — [Yaneva et al. 2024](https://aclanthology.org/2024.bea-1.39/). Survey of text-based difficulty estimation: [Benedetto et al. 2023, ACM CSUR, doi 10.1145/3556538](https://doi.org/10.1145/3556538).
- PROMISING. LLM "respondents" as synthetic calibration samples: item parameters calibrated from LLM responses correlate above 0.8 with human-calibrated ones (GPT-3.5). No single LLM matches the human ability spread, but ensembles do better. Resampling augmentation raised Spearman from 0.89 to 0.93 — [Liu, Bhandari & Pardos 2024, arXiv:2407.10899](https://arxiv.org/abs/2407.10899). Fine-tuned ability-conditioned LLMs reconstruct item characteristic curves "competitive with or outperform[ing]" baselines on Grade 6 ELA and BEA 2024 items — [arXiv:2601.02580](https://arxiv.org/abs/2601.02580).
- PROMISING (negative). Across 42 LLMs, predicting item *discrimination* in reading comprehension is weak: rank correlation at most 0.231. The signal comes from differences between models, not from ability-prompted simulated students — [arXiv:2606.18709](https://arxiv.org/abs/2606.18709).
- PROMISING. "Generative Students": 45 GPT-4 personas defined by mastered, confused and unknown KCs, answering 20 MCQs. Their answers correlated highly with real students' and flagged overlapping hard items — [Lu & Wang 2024, arXiv:2405.11591](https://arxiv.org/abs/2405.11591).

**Temporal holdout and forward-looking benchmarks**
- PROMISING. BrainBench is a forward-looking benchmark: predict neuroscience results from real abstracts. LLMs surpassed human experts, and confidence tracked correctness — [Luo et al. 2024, arXiv:2403.03230](https://arxiv.org/abs/2403.03230).
- ESTABLISHED (design). ForecastBench asks only questions with no known answer at submission time, "to avoid any possibility of data leakage". Expert forecasters beat the top LLM (p < 0.001) — [Karger et al. 2024, arXiv:2409.19839](https://arxiv.org/abs/2409.19839).
- ESTABLISHED (design). LiveBench uses frequently updated questions from recent sources with objective ground truth, specifically to avoid both contamination and LLM-judge pitfalls — [White et al. 2024, arXiv:2406.19314](https://arxiv.org/abs/2406.19314).

**LLM-as-judge: what it can and cannot carry**
- ESTABLISHED. GPT-4 judges reach over 80% agreement with human preferences, the same level as human–human agreement, on MT-bench and Chatbot Arena. The paper documents position, verbosity and self-enhancement biases — [Zheng et al. 2023, arXiv:2306.05685](https://arxiv.org/abs/2306.05685).
- PROMISING. Self-preference: LLM evaluators recognise their own outputs, and self-recognition strength correlates linearly with self-preference bias — [Panickssery, Bowman & Feng 2024, arXiv:2404.13076](https://arxiv.org/abs/2404.13076).
- PROMISING. With 13 judge models in a clean, high-agreement setting, "only the best (and largest) models achieve reasonable alignment with humans". Even they remain "far behind inter-human agreement", deviate by up to 5 points, and are lenient. For ranking systems, even small models or lexical metrics gave usable signal — [Thakur et al. 2024, arXiv:2406.12624](https://arxiv.org/abs/2406.12624).
- PROMISING. JUDGE-BENCH (20 datasets, 11 LLMs) found substantial variance by property, by expertise of the human judges, and by whether the text is human- or model-generated. Its conclusion: validate against human judgments before use — [Bavaresco et al. 2024, arXiv:2406.18403](https://arxiv.org/abs/2406.18403).
- PROMISING. A panel of smaller judges from disjoint model families beat a single large judge, reduced intra-model bias, and cost over 7× less — [Verga et al. 2024, arXiv:2404.18796](https://arxiv.org/abs/2404.18796).
- PROMISING (pattern). PaperBench grades with an LLM judge against author co-developed rubrics (8,316 gradable sub-tasks), and first validates that judge on a separate judge benchmark — [Starace et al. 2025, arXiv:2504.01848](https://arxiv.org/abs/2504.01848).

**Contamination**
- ESTABLISHED. Benchmark contamination must be measured per benchmark — [Sainz et al. 2023, doi 10.18653/v1/2023.findings-emnlp.722](https://doi.org/10.18653/v1/2023.findings-emnlp.722). Guided-completion prompts can detect whether test instances were memorised — [Golchin & Surdeanu 2023, arXiv:2308.08493](https://arxiv.org/abs/2308.08493).

### Inferences
- SPECULATIVE but strongly implied. A "held-out source" test on the FCI, a well-known misconception review, or GPQA-era material is confounded. The source is almost certainly in pretraining data, so recall measures memory, not reconstruction. Held-out tests need (a) sources published after the model's training cutoff, or (b) contamination probes (Golchin & Surdeanu) reported next to recall.
- SPECULATIVE. Recall against a gold list still needs a *matching* step (is generated item X the same as gold item Y?). That step is where an LLM judge sneaks back in. The non-circular version is: a fixed codebook, blind double human coding on a sample, and an LLM matcher used only after its agreement with human coders (κ) is reported, using a model family different from the generator.
- ESTABLISHED + inference. Behavioural tests (AFM fit, distractor-choice prediction) need no matching judgement, so they are the least circular. The BEA result warns that text-only difficulty prediction is a weak discriminator between systems. Distractor-choice and KC-fit tests are likely more sensitive.

### Gaps
- I found no published study that runs a *held-out-source recall* test of LLM-reconstructed misconception catalogues against a post-cutoff misconception review. This appears novel.
- No "agreement with published expert rankings" study for domain models was verified. Delphi-type ranking studies exist in education, but none were checked here.

---

## 3. Diagnosticity of generated questions: psychometric evidence with real students

### Takeaway
When LLM-generated items are administered to real students, their **difficulty and discrimination are often comparable** to expert items, once experts have filtered them. But **distractors are not reliably aligned with real misconceptions** unless generation is conditioned on real student responses. Expert ratings of item quality are unreliable (ICC 0.07–0.18) and failed to separate item sets that IRT did separate. Item statistics from real responses, not judges, must be the criterion.

### Cited Findings
- PROMISING (preregistered, blinded, within-subject). 24 GPT-4o items versus 24 topic-matched human items in imaging specialties, taken by 82 medical students and 46 physicians. Difficulty was 0.65 (SD 0.22) for human items vs 0.67 (0.20) for LLM items; discrimination 0.27 (0.12) vs 0.29 (0.12); neither difference significant. Participants could not identify item origin above chance. **Expert ratings of appropriateness showed ICC = 0.07–0.18.** Workflow was human-in-the-loop — [npj Digital Medicine, doi 10.1038/s41746-025-02313-7](https://www.nature.com/articles/s41746-025-02313-7).
- PROMISING (physics). 30 ChatGPT kinematics items were created; the 15 top-rated by two experts were given with the FCI to 172 first-year students. The ChatGPT items had medium difficulty and discrimination, slightly below FCI items. CFA recovered a 3-factor structure close to an expert model. But "human oversight or student interviews are necessary when creating … distractors that are closely aligned with students' difficulties" — [Küchemann et al. 2024, Front. Psychol., doi 10.3389/fpsyg.2024.1426209](https://doi.org/10.3389/fpsyg.2024.1426209).
- PROMISING. AnaQuest generates MCQ foils from students' own free-text answers. Instructors rated both AnaQuest and plain-ChatGPT items as valid as human items. **IRT showed only the AnaQuest items (especially foils) resembled human items in difficulty and discrimination** — [arXiv:2505.05815](https://arxiv.org/abs/2505.05815). Experts could not see a difference that response data exposed.
- PROMISING (negative). LLMs cannot yet predict item discrimination from content (max rank correlation 0.231 across 42 LLMs) — [arXiv:2606.18709](https://arxiv.org/abs/2606.18709).
- ESTABLISHED (identifier). IRT comparison of ChatGPT-generated and textbook college-algebra items — [Bhandari, Liu, Kwak & Pardos 2024, Computers & Education: AI, doi 10.1016/j.caeai.2024.100284](https://doi.org/10.1016/j.caeai.2024.100284). Detailed results not re-verified in this pass.
- ESTABLISHED (framework). The KLI framework defines knowledge components as the unit that items should diagnose — [Koedinger, Corbett & Perfetti 2012, doi 10.1111/j.1551-6709.2012.01245.x](https://doi.org/10.1111/j.1551-6709.2012.01245.x).

### Inferences
- SPECULATIVE. With zero new participants, diagnosticity can only be tested on items that already have response data: Eedi, AAAS, BEA/USMLE, DataShop steps. The feasible test is **retrodiction**. Give the system the item stems only, withhold the response data, and score predicted distractor-selection shares, predicted difficulty rank and predicted misconception labels against the real data.
- SPECULATIVE. Newly generated items cannot be validated without respondents. LLM respondents (Liu et al. 2024) are a pre-screen, not a validator, especially for discrimination (arXiv:2606.18709).

### Gaps
- No verified study was found of LLM-generated items evaluated with cognitive diagnostic models (DINA/G-DINA Q-matrix fit) on real students. This is an open gap.

---

## 4. Active knowledge acquisition: choosing the most informative questions to ask humans

### Takeaway
The principled criterion is **expected information gain** (EIG; Lindley 1956) under a Bayesian experimental design framing. Several 2023–2025 systems compute EIG from LLM predictive distributions and beat prompting-only question generation on 20-questions, diagnosis and preference tasks. Knowledge-gap detection supplies the prior over *where* the model is ignorant. Methods include P(IK) self-evaluation, semantic entropy, multi-LLM probing, and a Good-Turing bound for once-seen facts. No study was found applying EIG to *expert CTA interviews*.

### Cited Findings
- ESTABLISHED. EIG as the value of an experiment — [Lindley 1956, doi 10.1214/aoms/1177728069](https://doi.org/10.1214/aoms/1177728069). Modern review of Bayesian experimental design, including sequential and amortised EIG estimation — [Rainforth, Foster, Ivanova & Bickford Smith 2024, Stat. Sci., doi 10.1214/23-STS915](https://doi.org/10.1214/23-sts915).
- PROMISING (preregistered user studies). GATE: LMs that elicit by open-ended questions or synthesised edge cases obtain responses "often more informative than user-written prompts or labels". Users report lower effort, and elicitation "surfaces novel considerations not initially anticipated by users" — [Li, Tamkin, Goodman & Andreas 2023, arXiv:2310.11589](https://arxiv.org/abs/2310.11589).
- PROMISING. OPEN uses Bayesian optimal experimental design to choose the query and an LM to turn it into natural language. In user studies it outperformed both LM-only and BOED-only elicitation — [Handa, Gal, Pavlick & Goodman 2024, arXiv:2403.05534](https://arxiv.org/abs/2403.05534).
- PROMISING. An LLM-defined probabilistic model selects questions by expected entropy reduction and expected model change. It beat same-LLM baselines while using fewer user interactions — [Piriyakulkij, Kuleshov & Ellis 2023, arXiv:2312.12009](https://arxiv.org/abs/2312.12009).
- PROMISING. Uncertainty of Thoughts (information-gain rewards over simulated futures) gave +38.1% average task success across medical diagnosis, troubleshooting and 20 Questions, and needed fewer questions — [Hu et al. 2024, arXiv:2402.03271](https://arxiv.org/abs/2402.03271).
- PROMISING. BED-LLM chooses questions that maximise EIG estimated from the LLM's predictive distributions, with substantial gains on 20 Questions and preference inference over prompting-based and other adaptive designs — [Choudhury et al. 2025, arXiv:2508.21184](https://arxiv.org/abs/2508.21184). Active task disambiguation (EIG-selected clarifying questions) beats reasoning only in question space — [Kobalczyk et al. 2025, arXiv:2502.04485](https://arxiv.org/abs/2502.04485).
- ESTABLISHED. Models can predict P(IK) ("I know") and P(True) reasonably well, but P(IK) calibration degrades on new tasks — [Kadavath et al. 2022, arXiv:2207.05221](https://arxiv.org/abs/2207.05221).
- ESTABLISHED. Semantic entropy (entropy over meaning clusters of samples) predicts QA accuracy better than comparable baselines — [Kuhn, Gal & Farquhar 2023, arXiv:2302.09664](https://arxiv.org/abs/2302.09664).
- PROMISING. Multi-LLM cooperative or competitive probing detects knowledge gaps better than self-reflection, with up to 19.3% improvement in abstain accuracy — [Feng et al. 2024, arXiv:2402.00367](https://arxiv.org/abs/2402.00367).
- ESTABLISHED (theory). For "arbitrary" facts, calibrated LMs must hallucinate at a rate close to the fraction of facts seen exactly once in training (a Good-Turing estimate). There is no such statistical pressure for facts seen repeatedly or systematic facts — [Kalai & Vempala 2024, arXiv:2311.14648](https://arxiv.org/abs/2311.14648).
- ESTABLISHED. "Unknown unknowns" are high-confidence model errors that uncertainty sampling cannot find. They can be discovered by partitioning the input space and running a budgeted exploration policy that queries an oracle — [Lakkaraju, Kamar, Caruana & Horvitz 2017, AAAI, doi 10.1609/aaai.v31i1.10821](https://doi.org/10.1609/aaai.v31i1.10821). The method summary is from the paper's framing; the abstract was not re-read.

### Inferences
- SPECULATIVE. For expert elicitation, the "variable of interest" should be the *reconstructed domain model* itself: which misconception or KC edges exist, which cues experts use. A question's EIG is then the expected reduction in entropy over contested model elements. Contested elements are where independent reconstructions disagree, or where semantic entropy is high. The Kalai & Vempala result suggests the residual concentrates in *rare, once-documented* knowledge, which is exactly where an LLM's confidence is least trustworthy.
- SPECULATIVE. Lakkaraju's point applies directly: EIG computed from the model's own uncertainty will miss confidently wrong elements. A fraction of expert questions should go to "confident-but-unverified" elements, sampled by partition, not by uncertainty.
- SPECULATIVE. Zero-participant validation of the question selector is possible by *simulating* experts from a held-out gold. Replay a published CTA or misconception review as the answer oracle, then compare learning curves (gold items recovered per question) for EIG-selected versus random versus LLM-prompted questions.

### Gaps
- No study found that applies EIG or BED to expert knowledge elicitation or cognitive task analysis interviews specifically.
- Active learning for ontology or knowledge-graph completion: the search surfaced only e-commerce product-type ontology work ([arXiv:2009.09143](https://arxiv.org/html/2009.09143)) and general crowdsourcing reviews. No education-specific evidence was verified.

---

## 5. The "human knowledge residual": related concepts and how to operationalise it

### Takeaway
"Human knowledge residual" is not an established term. The closest established measurements are:
- **CTA omission rates.** Experts omit about half to three-quarters of the steps in a union-of-experts gold list.
- **Saturation and species-richness estimation.** These estimate how many themes remain unseen.
- **Capture–recapture in software inspection.** Multiple independent "trappers" estimate total defect content.

Combining these gives a defensible operationalisation: the residual is the importance-weighted share of *validated* domain items that experts supply and the reconstruction does not, with the unseen remainder estimated by capture–recapture across independent sources. The central pitfalls are dependence between sources (literature is written by experts), unequal catchability, and the matching judgement.

### Cited Findings
- ESTABLISHED. The CTA omission effect: "experts omitted an average of 71% (10/14) of clinical knowledge steps, 51% (14/27) of action steps, and 73% (3.6/5) of decision steps" when teaching. CTA probing raised articulated steps from 44% (unprompted) to 66% (prompted) of the gold list. The gold list was built from CTA with 3 + 3 surgeons — [Sullivan et al. 2014, doi 10.1097/ACM.0000000000000224](https://doi.org/10.1097/acm.0000000000000224). Automaticity as the cause of omission, reviewed — [Feldon 2006/7, Educ. Psychol. Rev., doi 10.1007/s10648-006-9009-0](https://doi.org/10.1007/s10648-006-9009-0).
- ESTABLISHED. Knowledge-elicitation methods differ in efficiency, which can be measured as yield per unit time — [Hoffman, Shadbolt, Burton & Klein 1995, OBHDP, doi 10.1006/obhd.1995.1039](https://doi.org/10.1006/obhd.1995.1039). A meta-analysis of CTA-based training exists — [Tofel-Grehl & Feldon 2013, JCEDM, doi 10.1177/1555343412474821](https://doi.org/10.1177/1555343412474821). Its effect size was not re-verified here.
- PROMISING (directly relevant, June 2026 preprint). LLMs "externalize tacit knowledge from experts' behaviors". Across two studies, LLM-externalised knowledge "improves decision quality and enables novices to approach expert-level performance, often outperforming knowledge articulated by human experts" — [arXiv:2608.07488](https://arxiv.org/abs/2608.07488). This bears on the reconstruct-first hypothesis. Note the input is *expert behaviour records*, not literature.
- ESTABLISHED. Saturation: 60 interviews gave 114 codes; ~70% of themes appeared within 6 interviews and 92% within 12 — [Guest, Bunce & Johnson 2006, Field Methods, doi 10.1177/1525822X05279903](https://doi.org/10.1177/1525822x05279903), as summarised in [Guest, Namey & Chen 2020, PLOS ONE](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7200005/). The 2020 bootstrap method (base size, run length, ≤5% or 0% new-information threshold) indicated saturation at 6–16 interviews, corresponding to a median "degree of saturation" of 62–89% of the eventual theme count. Saturation declared by stopping rules leaves a measurable unseen remainder.
- ESTABLISHED. Ecology models (a mixture of zero-truncated binomials over theme elicitation probabilities) predicted the number of themes found when the sample doubles, with 1–3% mean error, on a 1,053-participant open-ended survey — [Tran et al. 2017, J. Clin. Epidemiol., doi 10.1016/j.jclinepi.2016.10.001](https://doi.org/10.1016/j.jclinepi.2016.10.001).
- PROMISING. Capture–recapture applied to interview codes: saturation "may occur more than once in a sequence of interviews". The equal-catchability assumption fails when interview questions adapt to earlier answers — [Barker 2023, arXiv:2301.04760](https://arxiv.org/abs/2301.04760).
- ESTABLISHED. Species-richness estimators: Chao1 lower bound from singletons and doubletons — [Chao 1984, Scand. J. Stat.](https://openalex.org/W1558982506). Capture–recapture with unequal catchability — [Chao 1987, Biometrics, doi 10.2307/2531532](https://doi.org/10.2307/2531532). Extrapolation overview — [Colwell & Coddington 1994, doi 10.1098/rstb.1994.0091](https://doi.org/10.1098/rstb.1994.0091). Sample coverage (Good-Turing) to standardise by completeness — [Chao & Jost 2012, Ecology, doi 10.1890/11-1952.1](https://doi.org/10.1890/11-1952.1). Rarefaction/extrapolation with Hill numbers (iNEXT) — [Chao et al. 2014, Ecol. Monogr., doi 10.1890/13-0133.1](https://doi.org/10.1890/13-0133.1).
- ESTABLISHED. Software inspection uses independent inspectors as capture occasions to estimate total defect content — [Eick et al. 1992, ICSE, doi 10.1145/143062.143090](https://doi.org/10.1145/143062.143090). Comprehensive evaluation of which CRC models work with few inspectors — [Briand et al. 2000, IEEE TSE, doi 10.1109/32.852741](https://doi.org/10.1109/32.852741).
- ESTABLISHED. The LLM–expert gap depends on the task. On GPQA, experts (65–74%) beat GPT-4 (39%) — [arXiv:2311.12022](https://arxiv.org/abs/2311.12022). On ForecastBench, expert forecasters beat LLMs — [arXiv:2409.19839](https://arxiv.org/abs/2409.19839). On BrainBench, LLMs beat neuroscience experts at predicting results — [arXiv:2403.03230](https://arxiv.org/abs/2403.03230).

### Inferences
- SPECULATIVE. The Sullivan design *is* a residual measurement with the roles swapped. Replace "expert's unprompted teaching" with "autonomous reconstruction" and keep "union of CTA-elicited experts" as gold. The same percent-omitted statistics then apply per knowledge type (clinical/conceptual, action, decision), and decision steps are where omission is highest.
- SPECULATIVE. The main measurement hazard is **positive dependence** between the reconstruction's sources and the experts. Literature is written by experts, and experts learned from the same textbooks. Lincoln–Petersen-type estimates are biased low under positive dependence, so the unseen count is *under*-estimated. Mitigations: use more than two capture sources (different expert cohorts, different source families such as textbooks, forums, logs and CTA papers) and heterogeneity models (Chao 1987; Mh/jackknife in Briand et al.). Report Chao1 as a *lower bound*.
- SPECULATIVE. Catchability also differs by knowledge type. Tacit decision cues are rarely written down (Sullivan: 73% omitted), so aggregate estimates should be stratified by type.

### Gaps
- No established literature was found using the terms "human knowledge residual", "added value of expert elicitation" (in this sense) or "knowledge audit gap" as a measured quantity. The SHELF structured-elicitation literature concerns probability judgements, not knowledge content ([NCBI Bookshelf NBK571048](https://www.ncbi.nlm.nih.gov/books/NBK571048/)).
- No verified primary source for the often-quoted "3–4 experts are optimal for CTA" claim.
- No verified "tacit knowledge benchmark" for LLMs beyond GPQA and HLE (expert-only, not tacit) and arXiv:2608.07488.

---

## 6. Cross-domain benchmark design and contamination

### Takeaway
A domain panel should be chosen by **which of the three test families (coverage, behavioural fit, response retrodiction) have public gold**, not by topical breadth. Only mathematics has all three at scale (Eedi graph + NeurIPS 2020 responses + DataShop/ASSISTments logs). Physics and science have catalogue and response distributions (FCI, AAAS) plus limited logs. Medicine has item statistics (BEA/USMLE) and competency lists. CS and organisational domains mostly have coverage gold. Every well-known source is probably in pretraining data, so a temporal split is required.

### Cited Findings
- Maths: catalogue + prevalence + choice data — [Eedi graph](https://learningcommons.org/news/ai-platform-launch/), [NeurIPS 2020](https://arxiv.org/abs/2104.04034); KC-fit logs — [DataShop](https://pslcdatashop.web.cmu.edu/), [Koedinger et al. 2012](https://files.eric.ed.gov/fulltext/ED537201.pdf).
- Physics and science: [FCI](https://doi.org/10.1119/1.2343497), [AAAS items](https://www.aaas.org/news/new-testing-feature-aaas-web-site-helps-teachers-find-gaps-students-science-knowledge), expert–novice categorisation [Chi et al. 1981](https://doi.org/10.1207/s15516709cog0502_2), LLM–FCI item comparison [Küchemann et al. 2024](https://doi.org/10.3389/fpsyg.2024.1426209).
- Medicine: [BEA 2024 USMLE items](https://aclanthology.org/2024.bea-1.39/), [GPT-4o vs human items with student responses](https://www.nature.com/articles/s41746-025-02313-7), [CTA gold task list](https://doi.org/10.1097/acm.0000000000000224), [AAMC EPAs](https://www.aamc.org/about-us/mission-areas/medical-education/cbme/core-epas).
- Chemistry and E-learning KC gold: [Moore et al. 2024](https://arxiv.org/abs/2405.20526); [KCluster](https://arxiv.org/abs/2505.06469).
- Occupational task and skill coverage: [O*NET CC BY 4.0](https://www.onetcenter.org/license_db.html), [ESCO](https://esco.ec.europa.eu/en/use-esco).
- Contamination: [Sainz et al. 2023](https://doi.org/10.18653/v1/2023.findings-emnlp.722); [Golchin & Surdeanu 2023](https://arxiv.org/abs/2308.08493); temporal or dynamic designs [LiveBench](https://arxiv.org/abs/2406.19314), [ForecastBench](https://arxiv.org/abs/2409.19839).

### Inferences
- SPECULATIVE. A minimal panel with genuine falsifiability: **Maths** (all three tests), **Physics mechanics** (catalogue + distribution + small logs; the project's home domain), **Clinical medicine** (item statistics + CTA task list), and one **organisational** domain limited to coverage (O*NET/ESCO task lists), reported as coverage only. Law, OSS and IT ops should be added only once public gold is identified.
- SPECULATIVE. Temporal split: freeze the reconstruction corpus at date T, before the model's training cutoff where possible. Gold is then drawn from misconception papers, CTA papers and concept-inventory validations published after T. The data cutoff of the model used limits how late T can be, which argues for open-weight models with documented cutoffs.

### Gaps
- No verified public gold for law, OSS project onboarding, industrial maintenance or IT operations (e.g., incident post-mortem corpora as a misconception analogue).

---

## 7. Cost measurement for autonomous research

### Takeaway
Report cost jointly with accuracy (a Pareto frontier), not accuracy alone, and hold the budget fixed when comparing to human elicitation.

### Cited Findings
- PROMISING. Agent benchmarks focus narrowly on accuracy, which makes state-of-the-art agents "needlessly complex and costly". The paper proposes jointly optimising cost and accuracy — [Kapoor et al. 2024, arXiv:2407.01502](https://arxiv.org/abs/2407.01502).
- PROMISING. A panel of small judges is over 7× cheaper than a single large judge — [Verga et al. 2024](https://arxiv.org/abs/2404.18796).
- PROMISING. End-to-end autonomous research pipelines report per-paper cost — [Lu et al. 2024, The AI Scientist, arXiv:2408.06292](https://arxiv.org/abs/2408.06292) (figure not re-verified here). The best agent on PaperBench replicated 21.0% of rubric items, below an ML-PhD baseline — [arXiv:2504.01848](https://arxiv.org/abs/2504.01848).

### Inferences
- SPECULATIVE. The comparable unit is **cost per validated domain item**. For the reconstruction: tokens, compute and wall-clock. For human elicitation: expert-hours at a stated rate, plus coding hours. The residual (Section 5) should be reported alongside the cost of closing it.

### Gaps
- No verified study compares the cost per knowledge item of LLM reconstruction against that of CTA.

---

## Implications

### A. Zero-participant evaluation suite

Every experiment uses only existing public data. None uses an LLM judge as the criterion. Where matching is needed, it uses a fixed codebook, blind double human coding on a sample of at least 20%, and an LLM matcher from a *different* model family, used only after reporting κ against the human coders.

"Reconstruct-first hypothesis" (RFH) here means: an autonomous system working from existing evidence recovers most of the important domain knowledge, and what it recovers is behaviourally valid.

1. **E1 KC-model learning-curve fit.** Gold: DataShop datasets with expert KC models (math, geometry, physics/statics where available), plus the ~60% with no KC model. Metric: AFM item-stratified CV RMSE, AIC/BIC and median learning slope. Compare the reconstructed Q-matrix (built from item text + literature only) with the expert model, the best LFA model and Single-KC. *Falsifies RFH if* the reconstructed model does not beat Single-KC/Unique-step, or loses to the expert model on most datasets. KCluster and LFA prior results say it should at least tie (ESTABLISHED/PROMISING).
2. **E2 Misconception catalogue recall (held-out source).** Gold: Eedi Misconception Graph (CC BY 4.0) for a sampled set of topics, withheld; FCI and AAAS distractor misconceptions for mechanics. Metric: recall and precision at matched granularity, and **prevalence-weighted recall**, weighting each misconception by its real selection rate from the NeurIPS 2020 / Eedi response data. *Falsifies RFH if* prevalence-weighted recall is below a threshold set in advance (e.g., 0.6), or if recall collapses on the post-cutoff subset versus the pre-cutoff subset (which would show memorisation, not reconstruction). Report contamination probes.
3. **E3 Distractor-choice retrodiction.** Gold: NeurIPS 2020 / Eedi option-level responses; AAAS national response distributions. Metric: rank correlation and KL divergence between the predicted and observed distribution over wrong options; top-1 "most popular distractor" accuracy. Baselines: uniform and LLM-likelihood (Liu et al. 2025 found moderate correlations). *Falsifies RFH if* the reconstructed misconception model does not beat raw LLM likelihood. If it does not, the "model" adds nothing over the LM prior.
4. **E4 Item difficulty and discrimination retrodiction.** Gold: BEA 2024 USMLE items (difficulty 0.311 dummy baseline, 0.299 best); AAAS percent-correct by grade; DataShop step error rates. Metric: RMSE vs the dummy baseline; Spearman on discrimination. *Falsifies* only weakly, since the task is near-floor for all known systems. Use it as a sanity check, not a gate.
5. **E5 Temporal-holdout reconstruction.** Freeze sources at date T. Gold: misconception, CTA and concept-inventory papers published after T in the panel domains (PRPER, JRST, Acad. Med., EDM/LAK proceedings). Metric: recall of their reported items; novel-item rate. *Falsifies RFH if* post-T recall is far below pre-T recall on matched topics. That would mean earlier "reconstruction" was retrieval of already-published syntheses.
6. **E6 CTA gold replay (residual proxy).** Gold: published CTA task lists (e.g., Sullivan et al. 2014 cricothyrotomy; others to be collected). Metric: percent of clinical, action and decision steps recovered, compared directly with the published human-expert unprompted rates (e.g., 44% unprompted, 66% prompted; decision-step omission 73%). *Falsifies RFH if* the reconstruction recovers fewer steps than a single unprompted expert. It *supports* RFH if it matches or exceeds the prompted-CTA level.
7. **E7 Expert–novice contrast recovery.** Gold: Chi et al. (1981) categorisation contrasts and published expert/novice problem-sorting data. Metric: does the reconstructed model predict which problem pairs experts versus novices group together? *Falsifies RFH if* predictions are at the surface-feature (novice) level.
8. **E8 EIG question-selection simulation.** Oracle: a held-out gold (E2 or E6 gold) answering yes/no or short questions. Compare EIG-selected (BED-LLM style), uncertainty-plus-partition sampling (Lakkaraju style), plain LLM-generated and random questions. Metric: gold items recovered per question (area under the curve); number of questions to reach 90% of the recoverable gold. *Falsifies the active-acquisition claim if* EIG does not beat random or plain-LLM question selection.
9. **E9 Judge calibration (auxiliary, not a criterion).** Wherever an LLM matcher or judge is used, report its κ against the human double-coded sample and its self-preference gap (same family vs different family), per Panickssery et al. 2024. Use a panel of judges (PoLL). *Invalidates* E2, E5 and E6 scores if κ with humans is below the human–human κ.
10. **E10 Cost ledger.** Record tokens, dollars and wall-clock per validated item for every experiment, and plot a cost–accuracy frontier (Kapoor et al. 2024).

Order of value: E1, E3 and E2 are behavioural or large-scale and the least circular. E6 is the closest proxy for the residual. E5 is the contamination control. E4 is a sanity check.

### B. Operational definition of the human knowledge residual (proposal)

For a task scope *D* (e.g., "energy-conservation problem solving, first-year"):

- **U(D)**: the set of *important* domain items. Items are typed as concept/KC, prerequisite edge, misconception, decision cue/rule, or expert–novice contrast. Each has an importance weight *wᵢ* grounded in *behavioural* data where possible: misconception prevalence, KC error rate or learning-curve slope, or the step's decision criticality in a CTA task list. Otherwise the weight is an expert-panel rating recorded before comparison.
- **R**: items produced by autonomous reconstruction from existing evidence (World A: literature + public data; World B: A + project-internal artefacts).
- **H**: items elicited from humans (CTA, think-aloud, probes) and **validated**. Validation means corroboration by a second expert, or by trace or log evidence, as the prepared study already requires for Stage A operations.
- **Observed residual:** Res_obs = Σ_{i ∈ H \ R} wᵢ / Σ_{i ∈ H ∪ R_valid} wᵢ. This is the importance-weighted share of validated knowledge that only humans supplied. Report it stratified by item type, and report its converse (R \ H: reconstruction items experts did not state, following Sullivan's finding that experts omit much).
- **Estimated total residual (unseen-corrected):** treat each independent source as a capture occasion: each expert, each source family, each reconstruction run with a different model family. Estimate |U| with heterogeneity-robust capture–recapture (Chao 1987 Mh; jackknife as in Briand et al. 2000). Report Chao1 as a lower bound and sample coverage Ĉ = 1 − f₁/n (Chao & Jost 2012). Then the estimated residual = (Σ weights of H \ R + estimated unseen mass attributable to humans-only) / estimated weighted |U|.
- **Pitfalls to pre-register:**
  1. *Source dependence.* Literature is authored by experts, which biases capture–recapture low. Use at least 3 occasions and log-linear dependence terms.
  2. *Unequal catchability by type.* Stratify by type.
  3. *Adaptive questioning* breaks equal-catchability (Barker 2023). Estimate from the non-adaptive portion only.
  4. *Granularity mismatch.* Fix the codebook grain before matching.
  5. *Matching by LLM judge.* Apply the E9 rules.
  6. *Expert recall is incomplete.* H is not gold; the union of experts plus trace corroboration is.
  7. *Multiple saturation plateaus* (Barker 2023). Never declare the residual zero from a stopping rule alone.
- **Decision use (SPECULATIVE):** the reconstruct-first hypothesis holds for *D* if Res_obs (weighted) is small, with the threshold pre-registered, *and* R passes E1/E3 behaviourally. Expert time is then justified only for the item types and regions with the highest estimated residual. Those are chosen by the E8 EIG procedure, which turns the residual from a post-hoc number into the objective that expert questions minimise.
