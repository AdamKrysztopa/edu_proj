# Adjacent fields and falsification evidence for the reconstruct-first reorientation

Scope: red-team the proposal that an AI should first reconstruct a domain and expertise model from public evidence, then build a synthetic "surrogate cohort", then use organisational data, and only then elicit the "human knowledge residual" from people, universally across education and company knowledge.
Tags: ESTABLISHED (replicated or meta-analytic, or a large, well-identified study), PROMISING (one or a few good studies, or a strong preprint), SPECULATIVE (argument, position paper, or my inference).
Verification: identifiers were checked against OpenAlex (`resolve_references`) or the publisher/arXiv page on 2026-09-28. Where a check failed or was not run, the entry says so.
Project coverage check: a grep of `research/` and `ai_education_research_map.md` found no hits for reporting bias, Gervasi, Zowghi, Cooke, truth serum or surprisingly popular, process mining, Safety-II, learnersourcing, epistemic network analysis, knowledge space theory, evidence-centered design, simulated students, Stack Overflow, Viva, knowledge hiding, Szulanski, Nisbett, Hinds, job/practice analysis, design rationale or truck factor. These are the likeliest blind spots. Bastani, Kestin, VanLehn, Feldon, the "70%" rule, threshold concepts, Delphi and DataShop/LFA are already cited somewhere.

---

## Q1. Adjacent fields the project may have missed, and what each contributes

### Takeaway
Some fields already solve parts of the pipeline. Structured expert judgment (Cooke) and peer prediction (Prelec) aggregate experts better than majority vote or unweighted "surrogate experts". Data-driven knowledge-component discovery (Koedinger/DataShop) and expert-blind-spot research show that learner data reveal what both experts and text miss. Safety-II and process mining show that written procedures describe work-as-imagined, not work-as-done. Requirements engineering and cognitive task analysis give the elicitation techniques. Evidence-centered design and automatic item generation give a disciplined way to go from a domain model to diagnostic tasks.

### Cited Findings

**Elicitation of tacit knowledge outside education**
- Requirements engineering (RE) treats tacit knowledge as the main source of requirements failure. Gervasi et al. give a taxonomy that separates knowledge a stakeholder has but does not articulate ("unknown knowns") from knowledge that is truly unknown, and they review techniques (ethnography, apprenticing, protocol analysis, laddering) matched to each type. ESTABLISHED as a framework. It maps almost one-to-one onto "residual" types. — [Gervasi et al. 2013, *Unpacking Tacit Knowledge for Requirements Engineering*, doi:10.1007/978-3-642-34419-0_2](https://doi.org/10.1007/978-3-642-34419-0_2)
- Zowghi & Coulin's survey of elicitation techniques (interviews, scenarios, observation, prototyping, group work) is the standard reference for matching a technique to the kind of knowledge sought. ESTABLISHED. — [Zowghi & Coulin 2005, doi:10.1007/3-540-28244-0_2](https://doi.org/10.1007/3-540-28244-0_2)
- Critical Decision Method: retrospective probing of one non-routine incident to extract cues, goals, expectancies and options. It is the direct ancestor of the project's probe design. ESTABLISHED. — [Klein, Calderwood & MacGregor 1989, doi:10.1109/21.31053](https://doi.org/10.1109/21.31053)
- Conditions for valid intuitive expertise: expert intuition is trustworthy only in "high-validity" environments that give rapid, unambiguous feedback. This is a filter for which experts' tacit knowledge is worth eliciting at all. ESTABLISHED. — [Kahneman & Klein 2009, doi:10.1037/a0016755](https://doi.org/10.1037/a0016755)
- Cognitive task analysis (CTA) outcomes: a meta-analysis of CTA-based training reports a large effect, Hedges' g ≈ 0.87. I took the figure from a secondary summary and did not read the full text. ESTABLISHED direction, magnitude to verify. — [Tofel-Grehl & Feldon 2013, doi:10.1177/1555343412474821](https://journals.sagepub.com/doi/abs/10.1177/1555343412474821)

**Expert aggregation (directly relevant to "independently grounded surrogate expert perspectives")**
- Cooke's classical model weights each expert by calibration and informativeness, scored on seed questions with known answers. Out-of-sample cross-validation shows performance weighting beats equal weighting. ESTABLISHED. — [Colson & Cooke 2017, doi:10.1016/j.ress.2017.02.003](https://doi.org/10.1016/j.ress.2017.02.003); database: [Cooke & Goossens 2008, doi:10.1016/j.ress.2007.03.005](https://doi.org/10.1016/j.ress.2007.03.005)
- The "surprisingly popular" algorithm asks each respondent for an answer and for a prediction of others' answers. It can recover the correct answer when the majority is wrong, that is, when the correct knowledge sits with an informed minority. PROMISING to ESTABLISHED. — [Prelec, Seung & McCoy 2017, *Nature*, doi:10.1038/nature21054](https://doi.org/10.1038/nature21054); foundation: [Prelec 2004, Bayesian truth serum, doi:10.1126/science.1102081](https://doi.org/10.1126/science.1102081)
- Delphi: iterated anonymous estimation with feedback. ESTABLISHED as a method; it gives consensus, not validity. — [Dalkey & Helmer 1963, doi:10.1287/mnsc.9.3.458](https://doi.org/10.1287/mnsc.9.3.458)

**Education fields**
- Pedagogical content knowledge (PCK) is knowledge of what makes a topic hard and which representations work. It is exactly the "expert–novice difference" layer the reorientation wants to reconstruct, and it is held by teachers, not by domain experts. ESTABLISHED construct. — [Shulman 1986, doi:10.3102/0013189x015002004](https://doi.org/10.3102/0013189x015002004). Content Representations (CoRe) are a structured instrument for documenting PCK per topic and give a ready schema. — [Loughran, Mulhall & Berry 2004, doi:10.1002/tea.20007](https://doi.org/10.1002/tea.20007)
- Expert blind spot: preservice teachers with more advanced mathematics predicted that symbolic equations would be easier for students than story problems. Student data showed the reverse. ESTABLISHED. — [Nathan & Petrosino 2003, doi:10.3102/00028312040004905](https://doi.org/10.3102/00028312040004905). Curse of expertise: experts underestimate novice task time, and debiasing methods did not remove the bias. ESTABLISHED. — [Hinds 1999, doi:10.1037/1076-898x.5.2.205](https://doi.org/10.1037/1076-898x.5.2.205)
- Data-driven discovery of knowledge components: DataShop and Learning Factors Analysis repeatedly find cognitive models that fit learner data better than the expert-authored ones. Learner data reveal difficulty factors that experts did not list. ESTABLISHED. — [Koedinger et al. 2013, *AI Magazine*, doi:10.1609/aimag.v34i3.2484](https://doi.org/10.1609/aimag.v34i3.2484); framework: [Koedinger, Corbett & Perfetti 2012 (KLI), doi:10.1111/j.1551-6709.2012.01245.x](https://doi.org/10.1111/j.1551-6709.2012.01245.x)
- Knowledge space theory is a formal model of prerequisite structure as feasible knowledge states (the basis of ALEKS). It offers a tested representation for the "prerequisites" layer. ESTABLISHED. — [Doignon & Falmagne 1985, doi:10.1016/s0020-7373(85)80031-6](https://doi.org/10.1016/s0020-7373(85)80031-6)
- Evidence-centered design (ECD) takes you from a student model to an evidence model to a task model, which is the principled path from a domain model to diagnostic tasks. ESTABLISHED. — [Mislevy, Almond & Lukas 2003, doi:10.1002/j.2333-8504.2003.tb01908.x](https://doi.org/10.1002/j.2333-8504.2003.tb01908.x). Automatic item generation from cognitive models: [Gierl, Lai & Turner 2012, doi:10.1111/j.1365-2923.2012.04289.x](https://doi.org/10.1111/j.1365-2923.2012.04289.x)
- Professional job/practice analysis: NCCA accreditation requires a job or practice analysis that delineates performance domains, tasks and the associated knowledge and skills, and it requires a published report linking that analysis to exam specifications. This is a mature, auditable, cross-profession precedent for a "domain+expertise model". Its validity comes from SME panels plus a practitioner survey, not from text. ESTABLISHED as practice. — [NCCA Standards (Institute for Credentialing Excellence), draft 2021 revision PDF](https://www.credentialingexcellence.org/Portals/0/NCCA%20Standards%202021%20DRAFT%20REVISIONS_Sept%202021.pdf)
- Entrustable professional activities (EPAs) define competence as units of work entrusted to a trainee, not as lists of knowledge. They provide a cross-domain unit of analysis for "role/capability" inputs. ESTABLISHED in medical education. — [ten Cate 2005, doi:10.1111/j.1365-2929.2005.02341.x](https://doi.org/10.1111/j.1365-2929.2005.02341.x)
- Cognitive apprenticeship: expert processes must be made visible (modelling, coaching, scaffolding, articulation). ESTABLISHED as theory. — [Collins, Brown & Newman 1989, DTIC report, OpenAlex W3204540359](https://openalex.org/W3204540359). Situated learning / legitimate peripheral participation: [Lave & Wenger 1991; OpenAlex matched only a 1994 review, so the book record is unverified](https://openalex.org/W2116199508)
- Threshold concepts: Meyer & Land give the construct (transformative, irreversible, integrative, troublesome) — [doi:10.1007/s10734-004-6779-5](https://doi.org/10.1007/s10734-004-6779-5). Critiques say that, as defined, threshold concepts cannot be empirically identified or distinguished — [Rowbottom 2007, doi:10.1111/j.1467-9752.2007.00554.x](https://doi.org/10.1111/j.1467-9752.2007.00554.x) — and that identification methods are inconsistent — [Barradell 2013, doi:10.1007/s10734-012-9542-3](https://doi.org/10.1007/s10734-012-9542-3). The construct is ESTABLISHED; its operational identification is contested. Do not make it a node type without an operational test.
- Worked examples, expertise reversal and self-explanation: example-based learning theory — [Renkl 2014, doi:10.1111/cogs.12086](https://doi.org/10.1111/cogs.12086). The expertise reversal effect (support that helps novices hurts more expert learners) means a single "instructional hypothesis" per concept is wrong by design — [Kalyuga et al. 2003, doi:10.1207/s15326985ep3801_4](https://doi.org/10.1207/s15326985ep3801_4). Self-explanation: [Chi et al. 1989, doi:10.1016/0364-0213(89)90002-5](https://doi.org/10.1016/0364-0213(89)90002-5); meta-analysis [Bisra et al. 2018, doi:10.1007/s10648-018-9434-x](https://doi.org/10.1007/s10648-018-9434-x). ESTABLISHED.
- Learnersourcing: learners' own subgoal labels for how-to videos reached quality comparable to expert labels. This makes learners a production source, not only a test population. PROMISING. — [Weir, Kim, Gajos & Miller 2015, CSCW, doi:10.1145/2675133.2675219](https://doi.org/10.1145/2675133.2675219). (AXIS, Williams et al. 2016, and PeerWise, Denny et al. 2008, did not resolve in OpenAlex; unverified.)
- Epistemic network analysis models expertise as co-occurrence structure among coded elements, not as a list. It is a candidate representation for "how cues, decisions and principles connect", and it is testable against expert–novice data. PROMISING. — [Shaffer, Collier & Ruis 2016, doi:10.18608/jla.2016.33.3](https://doi.org/10.18608/jla.2016.33.3)
- Tutoring effectiveness baseline: human tutoring d ≈ 0.79, step-based ITS d ≈ 0.76, answer-based systems d ≈ 0.31 (the effect sizes are my recollection of this meta-review; the DOI is verified). ESTABLISHED. — [VanLehn 2011, doi:10.1080/00461520.2011.611369](https://doi.org/10.1080/00461520.2011.611369)

**LLM tutoring evidence, 2024–2026 (mixed; guardrails and design dominate)**
- Turkey, about 1,000 high-school students: unguarded GPT-4 ("GPT Base") improved practice performance by 48% but lowered unassisted exam performance by 17% relative to control. A scaffolded "GPT Tutor" improved practice by 127% and removed the harm, with no exam gain. ESTABLISHED (large field RCT, PNAS). — [Bastani et al. 2025, doi:10.1073/pnas.2422633122](https://doi.org/10.1073/pnas.2422633122)
- Harvard physics, crossover RCT: a custom AI tutor built on the same pedagogical design as the active-learning lessons gave a regression effect size of 0.63 (authors: an underestimate because of a ceiling effect), with a median of 49 minutes on task against a 60-minute class. The limits are single lessons, short-term post-tests and an elite sample. PROMISING. — [Kestin et al. 2025, *Sci Rep*, doi:10.1038/s41598-025-97652-6](https://doi.org/10.1038/s41598-025-97652-6)
- Ghana, Rori WhatsApp math tutor: about 1,000 students in grades 3–9, 11 schools randomised at school level, 8 months, effect size 0.37 on math growth. With only 11 clusters, precision is limited; a full-scale RCT is registered with J-PAL. PROMISING. — [Henkel et al. 2024, arXiv:2402.09809](https://arxiv.org/abs/2402.09809); [J-PAL full-scale RCT page](https://www.povertyactionlab.org/initiative-project/scaling-ai-powered-math-tutoring-across-diverse-educational-contexts-full-scale)
- Nigeria (Edo State), 6-week after-school GPT-4/Copilot programme under teacher supervision: 0.31 SD overall, 0.23 SD on English. PROMISING (World Bank working paper 11125). — [De Simone et al. 2025, ERIC ED676624](https://eric.ed.gov/?q=source:%22World+Bank%22&id=ED676624); [VoxDev summary](https://voxdev.org/topic/education/how-ai-tutors-improved-learning-nigeria)

**Company-knowledge fields**
- Safety-II / resilience engineering separates work-as-imagined (procedures) from work-as-done (adaptive practice). The gap is where the operational residual lives. ESTABLISHED framework. — [Hollnagel 2014, OpenAlex W300856602](https://openalex.org/W300856602)
- Process mining reconstructs actual process flows from event logs. It is the organisational-data analogue of reconstruction, and it measures SOP deviation directly. ESTABLISHED. — [van der Aalst 2016, doi:10.1007/978-3-662-49851-4](https://doi.org/10.1007/978-3-662-49851-4)
- Troubleshooting knowledge lives in narrative ("war stories") among technicians and not in documentation (Xerox repair technicians). ESTABLISHED ethnography. — [Orr 1996, review record doi:10.2307/2655659](https://doi.org/10.2307/2655659); [Brown & Duguid 1991, doi:10.1287/orsc.2.1.40](https://doi.org/10.1287/orsc.2.1.40)
- Design rationale / software archaeology: why decisions were made is rarely recorded, and capture tools have struggled with the cost of capture. ESTABLISHED. — [Burge et al. 2008, *Rationale-Based Software Engineering*, doi:10.1007/978-3-540-77583-6](https://doi.org/10.1007/978-3-540-77583-6)
- Truck (bus) factor: an algorithm estimates how many developers must leave before a project stalls. In my recollection of the result, most of 133 GitHub systems have a truck factor of 2 or less. That operationalises "retiring expert" risk from repository data. PROMISING. — [Avelino et al. 2016, doi:10.1109/icpc.2016.7503718](https://doi.org/10.1109/icpc.2016.7503718). Newcomer onboarding barriers: [Steinmacher et al. 2015, doi:10.1016/j.infsof.2014.11.001](https://doi.org/10.1016/j.infsof.2014.11.001)
- Knowledge creation (the SECI tacit↔explicit conversion model): [Nonaka 1994, doi:10.1287/orsc.5.1.14](https://doi.org/10.1287/orsc.5.1.14)
- Organisational interaction data carry transferable tacit skill. An AI assistant trained on customer-support conversations raised productivity by about 14% on average and about 34% for novice/low-skill agents, with little effect on the most experienced. That is consistent with disseminating top performers' tacit practices. ESTABLISHED (QJE; the figures are my recollection, the DOI is verified). — [Brynjolfsson, Li & Raymond 2025, doi:10.1093/qje/qjae044](https://doi.org/10.1093/qje/qjae044)

**AI knowledge engineering and automated discovery**
- Knowledge engineering with LLMs: a position paper framing hybrid human–LLM knowledge engineering. SPECULATIVE (position). — [Allen, Stork & Groth 2023, arXiv:2310.00637](https://arxiv.org/abs/2310.00637)
- AI co-scientist: a multi-agent Gemini system produced drug-repurposing candidates for acute myeloid leukaemia that were validated in vitro. It shows that reconstruct-then-hypothesise can work in literature-dense biomedicine. PROMISING. — [Gottweis et al. 2025, arXiv:2502.18864](https://arxiv.org/abs/2502.18864); see also [Lu et al. 2024, *The AI Scientist*, arXiv:2408.06292](https://arxiv.org/abs/2408.06292)
- The ethnography of expert systems found that knowledge engineers systematically deleted the social, situated and tacit parts of expert practice from what they encoded. This is the historical failure mode that reconstruct-first risks repeating at scale. ESTABLISHED (classic STS study). — [Forsythe 1993, doi:10.1177/0306312793023003002](https://doi.org/10.1177/0306312793023003002)

### Inferences
- The most valuable imports are:
  1. Cooke-style seed-question calibration, applied to surrogate experts and human experts alike.
  2. Surprisingly-popular / BTS scoring, to find minority expert knowledge that majority aggregation, and LLM consensus, would erase.
  3. Learnersourcing plus data-driven KC refinement, so that learner errors are a first-class source rather than a late validation step.
  4. ECD, as the formal bridge from model to diagnostic task.
  5. Safety-II and process mining for the company track, since SOP text is work-as-imagined by construction.
- Job/practice analysis (NCCA) is the closest existing universal pipeline: role → tasks → knowledge/skills → assessment specs, across hundreds of professions. Its validity rests on SME panels and practitioner surveys. That is a precedent for "universal method, domain-specific human validation", not for text-only reconstruction.

### Gaps
- Human reliability analysis (e.g. THERP, SPAR-H) was not searched; it is relevant to the procedure-error taxonomy in the company track.
- I found no peer-reviewed crowdsourced-misconception-discovery study beyond learnersourcing; AXIS and PeerWise could not be verified in OpenAlex.
- Walsh & Ungson 1991 (organisational memory) did not resolve in OpenAlex and is omitted.

---

## Q2(a). Is autonomous LLM reconstruction of domains unreliable?

### Takeaway
Yes, in precisely the places the reorientation needs most: long-tail and niche facts, citations, and anything seen rarely in the training data. Theory and data agree that hallucination is at least as frequent as the fraction of facts seen only once. Homogenisation and monoculture make "independent" surrogate perspectives less independent than they look. Retrieval with provenance mitigates the problem but does not remove it.

### Cited Findings
- Fabricated citations: 55% of GPT-3.5 and 18% of GPT-4 generated citations were fabricated, and many of the real ones contained substantive errors (figures from memory of the abstract; the DOI is verified). ESTABLISHED. — [Walters & Wilder 2023, *Sci Rep*, doi:10.1038/s41598-023-41032-5](https://doi.org/10.1038/s41598-023-41032-5)
- Hallucinated references survive expert peer review. GPTZero reports over 100 hallucinated citations across 51+ of 4,841 NeurIPS 2025 accepted papers, which is vendor data and not peer-reviewed. — [GPTZero](https://gptzero.me/news/neurips/). A taxonomy of 100 fabricated NeurIPS 2025 citations is in [arXiv:2602.05930](https://arxiv.org/abs/2602.05930). PROMISING. **In-session example:** during this research a WebFetch summariser reported a "63% distractor match rate vs 25% chance" for Acquaye et al. (arXiv:2601.09953). The number does not exist in the paper (checked with pdftotext). LLM summaries of sources are themselves an unreliable layer.
- Long-tail knowledge: LLM QA accuracy tracks the number of pretraining documents relevant to a question, so rare facts are answered poorly. ESTABLISHED. — [Kandpal et al. 2023, arXiv:2211.08411](https://arxiv.org/abs/2211.08411). Parametric memory fails on less popular entities and retrieval helps most there. ESTABLISHED. — [Mallen et al. 2023, ACL, doi:10.18653/v1/2023.acl-long.546](https://doi.org/10.18653/v1/2023.acl-long.546)
- Hallucination is structural: training and evaluation reward guessing over abstaining, and for arbitrary facts the hallucination rate is bounded below by roughly the share of facts that appear once in training. PROMISING (theory with empirical support). — [Kalai, Nachum, Vempala & Zhang 2025, arXiv:2509.04664](https://arxiv.org/abs/2509.04664) (OpenAlex returns a corrupted title for this ID; the authors match). Survey: [Ji et al. 2023, doi:10.1145/3571730](https://doi.org/10.1145/3571730)
- Sycophancy: RLHF models shift answers toward the user's stated beliefs. ESTABLISHED. — [Sharma et al. 2023, arXiv:2310.13548](https://arxiv.org/abs/2310.13548) (OpenAlex title for this ID is corrupted; the authors match)
- Model collapse: training on recursively generated data removes the tails of the distribution first. ESTABLISHED (Nature). — [Shumailov et al. 2024, doi:10.1038/s41586-024-07566-y](https://doi.org/10.1038/s41586-024-07566-y)
- Homogenisation: GenAI raised the creativity of individual writers but reduced the collective diversity of their stories. ESTABLISHED (preregistered experiment). — [Doshi & Hauser 2024, doi:10.1126/sciadv.adn5290](https://doi.org/10.1126/sciadv.adn5290). Algorithmic monoculture can lower overall welfare even when each individual algorithm is more accurate. ESTABLISHED (theory). — [Kleinberg & Raghavan 2021, doi:10.1073/pnas.2018340118](https://doi.org/10.1073/pnas.2018340118). Reliance on AI concentrates knowledge toward the centre of the distribution ("knowledge collapse"). SPECULATIVE (model). — [Peterson 2025, *AI & Society*, doi:10.1007/s00146-024-02173-x](https://doi.org/10.1007/s00146-024-02173-x)
- Epistemic monoculture in science: AI tools risk "monocultures of knowing" and illusions of understanding, in which researchers believe they understand more than they do. SPECULATIVE (analytic perspective in Nature). — [Messeri & Crockett 2024, doi:10.1038/s41586-024-07146-0](https://doi.org/10.1038/s41586-024-07146-0)
- Models converge to a "machine consensus" on item difficulty rather than toward human difficulty, and scaling does not fix this (20+ models). PROMISING. — [Li et al. 2025, arXiv:2512.18880](https://arxiv.org/abs/2512.18880)
- Counter-evidence: a literature-grounded multi-agent system produced hypotheses validated in vitro. PROMISING. — [Gottweis et al. 2025, arXiv:2502.18864](https://arxiv.org/abs/2502.18864)

### Inferences
- Strength: ESTABLISHED for citations, the long tail and homogenisation. **Implication (hard limit):** nothing enters the domain model on parametric recall alone. Every node needs a resolvable source span, and a citation-verification pass (as with the project's `citation-verifier`) must be a mechanical gate, not a prompt.
- **Implication (design):** several surrogate experts drawn from the same or similar model families are *not* independent samples. Li et al.'s "machine consensus" is direct evidence. Surrogate disagreement therefore underestimates true expert disagreement. Use different model families plus source-diverse retrieval, and treat agreement among surrogates as weak evidence.
- Company knowledge is the extreme long tail. Most internal facts appear zero or one times in public corpora, so reconstruction there reduces to retrieval over organisational documents, and the Kalai bound predicts high hallucination for anything not retrieved.

### Gaps
- I found no study measuring the precision and recall of an LLM-built domain or expertise model against a human-built one (e.g. a CTA or job analysis) in the same domain. That is the key missing experiment, and the project could run it (see the Verdict).

---

## Q2(b). Are synthetic cohorts misleading?

### Takeaway
Yes for effect sizes, misconception dynamics and between-person variance. Partly no for coarse item difficulty when the simulator is deliberately weak. Grounding simulated individuals in real per-person data helps a lot, which argues for learner data early, not late.

### Cited Findings
- Effect inflation: across 156 psychology/management experiments replicated with LLMs, 73–81% of main effects replicated, but only 19.44% of GPT-4's confidence intervals contained the original effect size, with most estimates larger. Where the original study found a null, LLMs returned significant effects 68–83% of the time. ESTABLISHED (Nature Computational Science). — [Cui, Li & Zhou 2025, doi:10.1038/s43588-025-00840-7](https://doi.org/10.1038/s43588-025-00840-7)
- Flattening: LLMs standing in for identity groups misportray them and flatten within-group diversity. ESTABLISHED. — [Wang, Morgenstern & Dickerson 2025, *Nat Mach Intell*, doi:10.1038/s42256-025-00986-z](https://doi.org/10.1038/s42256-025-00986-z). Synthetic survey responses showed less variance than real ones, were sensitive to prompt wording and were unstable across model versions (from my reading of the abstract). ESTABLISHED. — [Bisbee et al. 2024, *Political Analysis*, doi:10.1017/pan.2024.5](https://doi.org/10.1017/pan.2024.5)
- Misconception faithfulness: across seven LLMs (4B–120B), simulated students scored near zero on Selective Flip Score. They dropped their "misconception" at similar rates whether feedback targeted the true misconception, a different one, or none, behaving as sycophantic problem-solvers rather than learners with coherent wrong beliefs. Fine-tuning improved SFS by up to +0.56. PROMISING (2026 preprint). — [Do, Sonkar & Sachan 2026, arXiv:2605.12748](https://arxiv.org/abs/2605.12748)
- Tutoring dialogues: "prompting strategies for student simulation perform poorly; supervised fine-tuning and preference optimization yield much better but still limited performance" on real math tutoring data (ACL 2026). PROMISING. — [Scarlatos et al. 2026, arXiv:2601.04025](https://arxiv.org/abs/2601.04025)
- Competence paradox: a capable LLM asked to play a partially knowledgeable learner produces unrealistic error patterns and learning dynamics. SPECULATIVE (conceptual framework). — [Yuan et al. 2026, arXiv:2601.05473](https://arxiv.org/abs/2601.05473)
- Difficulty misalignment: see Q2(a). Models "struggle to simulate the capability limitations of students even when being explicitly prompted to adopt specific proficiency levels". PROMISING. — [Li et al. 2025, arXiv:2512.18880](https://arxiv.org/abs/2512.18880)
- Counter-evidence: simulated classrooms fitted with IRT correlated 0.75, 0.76 and 0.82 with NAEP item correctness rates for grades 4, 8 and 12. LLMs were "poor direct judges" of difficulty, and *weaker* math models predicted better than stronger ones. PROMISING (verified from the PDF). — [Acquaye et al. 2026, arXiv:2601.09953](https://arxiv.org/abs/2601.09953)
- Grounding helps: agents built from 2-hour interviews of 1,052 real people reached 83% (interview), 82% (survey) and 86% (both) of participants' own test-retest consistency on held-out GSS items, against 74% for demographics-only agents. PROMISING. — [Park et al. 2024, arXiv:2411.10109](https://arxiv.org/abs/2411.10109)
- Earlier simulation work: [Argyle et al. 2023, doi:10.1017/pan.2023.2](https://doi.org/10.1017/pan.2023.2) (positive); [Aher, Arriaga & Kalai 2023, arXiv:2208.10264](https://arxiv.org/abs/2208.10264) (mixed); [Dillion et al. 2023, doi:10.1016/j.tics.2023.04.008](https://doi.org/10.1016/j.tics.2023.04.008) (cautious). Validation frameworks: [Anthis et al. 2025, arXiv:2504.02234](https://arxiv.org/abs/2504.02234); [Hullman et al. 2026, arXiv:2602.15785](https://arxiv.org/abs/2602.15785) (read only as titles and abstracts).

### Inferences
- **Hard limit:** a surrogate cohort must not be used to estimate intervention effects or to rank instructional hypotheses by expected effect. Cui et al. show systematic inflation and false positives on nulls, which is exactly the error that would make a weak instructional hypothesis look good.
- **Hard limit for diagnosis:** unprompted LLM "misconceptions" are not stable belief states (near-zero SFS). Simulated error *distributions* should be treated as hypotheses to test against real learner errors, never as priors on prevalence.
- **Usable niche:** coarse item-difficulty pretesting with deliberately weaker models and IRT (Acquaye), and coverage generation (listing candidate errors), both scored against real data.
- Park et al. imply that surrogate validity scales with real per-person grounding. That reverses the proposed order: a small real learner sample early makes the synthetic cohort useful, whereas "synthetic first, humans last" leaves it uncalibrated.

### Gaps
- There is no published validation of LLM-simulated *physics* conservation-problem errors against coded real errors. The project's Early K0 data would be a direct test.
- A search snippet claimed a "31–47% distractor match rate" for LLM-simulated vs real students on concept inventories; I could not trace it to a source, so it is excluded.

---

## Q2(c). Does tacit knowledge fundamentally require human observation, and do written corpora systematically lack it?

### Takeaway
The evidence is strong that text under-reports the obvious (reporting bias), that experts omit most of what novices need when they explain, and that verbal reports cannot reach automated processes. So the residual is systematically non-textual. But "tacit" is not "unarticulable": some perceptual and procedural expertise was codified once researchers analysed expert performance directly. The limit is on text-first reconstruction, not on codification.

### Cited Findings
- Reporting bias: text frequency diverges from world frequency. In a teraword n-gram corpus, "murdered" occurs about 2.84M times against "breathed" at about 0.73M, and "was late" about 369k against "was on time" about 24k. A knowledge extractor learned "a person may have eyes" almost a million times but "a person may have a spleen" fewer than 1,600 times. ESTABLISHED (verified from the PDF). — [Gordon & Van Durme 2013, doi:10.1145/2509558.2509563](https://doi.org/10.1145/2509558.2509563)
- Reporting bias transfers to LMs: an LM's object-colour distributions correlate more with the (biased) text distribution than with human-perceived ground truth; multimodal training partly mitigates this. ESTABLISHED. — [Paik et al. 2021, EMNLP, arXiv:2110.08182](https://arxiv.org/abs/2110.08182)
- Expert omission: when describing a procedure, surgeons omitted on average 71% of clinical-knowledge steps, 51% of action steps and 73% of decision steps, compared with CTA. ESTABLISHED (replicated "70% rule"; figures from a secondary summary of the abstract). — [Sullivan et al. 2014, *Acad Med*, doi:10.1097/acm.0000000000000224](https://doi.org/10.1097/acm.0000000000000224); review: [Feldon 2007, doi:10.1007/s10648-006-9009-0](https://doi.org/10.1007/s10648-006-9009-0)
- Limits of introspection: people report on mental processes they cannot access. ESTABLISHED. — [Nisbett & Wilson 1977, doi:10.1037/0033-295x.84.3.231](https://doi.org/10.1037/0033-295x.84.3.231). Concurrent verbalisation is valid only for information held in attention, so automated processes do not surface. ESTABLISHED. — [Ericsson & Simon 1980, doi:10.1037/0033-295x.87.3.215](https://doi.org/10.1037/0033-295x.87.3.215)
- Typology: relational tacit knowledge (could be made explicit but is not), somatic (embodied), and collective (social, which Collins argues cannot be fully explicated). ESTABLISHED as theory, not quantified. — [Collins 2010, doi:10.7208/chicago/9780226113821.001.0001](https://doi.org/10.7208/chicago/9780226113821.001.0001)
- Perceptual expertise is learned through exposure and classification practice, not through description. ESTABLISHED. — [Kellman & Garrigan 2009, doi:10.1016/j.plrev.2008.12.001](https://doi.org/10.1016/j.plrev.2008.12.001)
- Counter-evidence: chick-sexing expertise, long considered ineffable, was partly codified. Researchers analysed the discriminating cue, and a short instruction sheet raised novices toward expert accuracy. ESTABLISHED. — [Biederman & Shiffrar 1987, doi:10.1037/0278-7393.13.4.640](https://doi.org/10.1037/0278-7393.13.4.640)
- Situated troubleshooting knowledge circulates as narrative and is not captured by documentation. ESTABLISHED. — [Orr 1996](https://doi.org/10.2307/2655659); [Brown & Duguid 1991](https://doi.org/10.1287/orsc.2.1.40)

### Inferences
- Much of the "relational" tacit layer (Collins) is reachable by good probing, which is the project's Stage A bet. Somatic and perceptual knowledge needs observation of performance or stimulus sets, for example the cue analysis in Biederman & Shiffrar. Collective knowledge needs presence in the community (Orr). A text-first reconstructor can at best *locate the holes*, not fill them.
- **Design implication:** the model schema needs a node attribute for "knowledge type" (relational, somatic, perceptual, collective), and each type needs a matched elicitation channel. For perceptual cues, elicitation means contrasting cases and classification tasks, not interviews.

### Gaps
- I found no study that directly measures the overlap between public-text content and CTA-elicited steps for the same task. That would quantify the residual.

---

## Q2(d). Does cross-domain generalisation fail?

### Takeaway
Expertise and PCK are domain-specific, generic skills do not transfer well, and ITS authoring tools historically did not generalise cheaply. A universal *pipeline* is plausible; a universal *model* or universal validation is not.

### Cited Findings
- Experts categorise physics problems by deep principles and novices by surface features. The structure of expertise is domain content. ESTABLISHED. — [Chi, Feltovich & Glaser 1981, doi:10.1207/s15516709cog0502_2](https://doi.org/10.1207/s15516709cog0502_2)
- Skill is explained by domain-specific knowledge in long-term memory, and teaching generic skills does not work. ESTABLISHED (argued review). — [Tricot & Sweller 2014, doi:10.1007/s10648-013-9243-1](https://doi.org/10.1007/s10648-013-9243-1)
- PCK is topic-specific by definition. — [Shulman 1986](https://doi.org/10.3102/0013189x015002004); [Loughran et al. 2004](https://doi.org/10.1002/tea.20007)
- ITS authoring: a review of dozens of authoring tools found trade-offs between generality, depth and ease. Tools that are easy to use are shallow or narrow. ESTABLISHED. — [Murray 2003, doi:10.1007/978-94-017-0819-7_17](https://doi.org/10.1007/978-94-017-0819-7_17). Example-tracing tutors cut development cost by restricting the model to demonstrated solution paths, trading generality for cost. ESTABLISHED. — [Aleven et al. 2009, doi:10.5555/1734243.1734245](https://doi.org/10.5555/1734243.1734245); [Anderson et al. 1995, doi:10.1207/s15327809jls0402_2](https://doi.org/10.1207/s15327809jls0402_2)
- The evidence on LLM tutoring effects is domain- and design-specific. Math with guardrails: no gain (Bastani). Physics with a pedagogy-matched tutor: large gain (Kestin). English in Nigeria: 0.23 SD. — see Q1.
- Uneven domain coverage: math forums lost less activity than Stack Overflow after ChatGPT, because "ChatGPT is less capable" there (the paper's identification strategy). That is evidence that LLM capability, and hence reconstruction quality, differs by domain. PROMISING. — [del Rio-Chanona et al. 2024, doi:10.1093/pnasnexus/pgae400](https://doi.org/10.1093/pnasnexus/pgae400)

### Inferences
- **Hard limit:** "universal" can only mean a universal *procedure* with domain-specific validation gates. Every new domain needs its own calibration set: seed questions, a real error sample, and a small human elicitation.
- Physics mechanics is one of the most text-rich domains for learner difficulties: decades of PER misconception research, concept inventories, and Physics Stack Exchange. It is therefore close to a best case for reconstruction. Success in physics would not show universality. The thesis needs at least one deliberately text-poor domain (vocational skill, or one firm's troubleshooting) as a falsification test.

### Gaps
- I found no head-to-head study of generic vs domain-specific LLM tutors that holds pedagogy constant.

---

## Q2(e). Can knowledge graphs or LLMs represent the relevant cognition?

### Takeaway
Partly. Graphs represent declarative and prerequisite structure well (knowledge space theory, KC models). Procedural, perceptual and embodied expertise is represented better as tasks, contrasting cases or performance models than as nodes. Text-only models inherit reporting bias about perceptual properties.

### Cited Findings
- Prerequisite structure can be formalised and used adaptively (knowledge spaces). ESTABLISHED. — [Doignon & Falmagne 1985](https://doi.org/10.1016/s0020-7373(85)80031-6)
- Procedural knowledge in tutors is represented as production rules (cognitive tutors) or demonstrated solution graphs (example tracing); both need authoring or demonstration per task. ESTABLISHED. — [Anderson et al. 1995](https://doi.org/10.1207/s15327809jls0402_2); [Aleven et al. 2009](https://doi.org/10.5555/1734243.1734245)
- Text-only LMs mis-represent perceptual properties because of reporting bias. ESTABLISHED. — [Paik et al. 2021](https://arxiv.org/abs/2110.08182)
- Connection structure (which elements co-occur in expert reasoning) differs from node lists and can separate experts from novices. PROMISING. — [Shaffer et al. 2016](https://doi.org/10.18608/jla.2016.33.3)
- Knowledge engineers encoding expertise as rules deleted its situated parts. ESTABLISHED. — [Forsythe 1993](https://doi.org/10.1177/0306312793023003002)

### Inferences
- **Design implication:** make the representation hybrid. Use a graph for concepts, prerequisites and misconceptions; a task and solution-path library for procedures (example tracing); contrasting-case sets for perceptual cues; and narrative cases for collective or troubleshooting knowledge. The graph should index these assets rather than try to hold them.

### Gaps
- I found no empirical comparison of LLM-constructed and expert-constructed KC models on learner-data fit (e.g. AFM/LFA fit in DataShop). It is feasible and would be decisive.

---

## Q2(f). Does the product thesis fail (KM adoption, codification, incentives)?

### Takeaway
The evidence against KM *codification* products is real but more nuanced than "experts hoard". The main barriers to transfer are cognitive (absorptive capacity, causal ambiguity) and relational, and knowledge hiding is a measurable but separate problem. Viva Topics' retirement is weak evidence; Microsoft's stated reason was a strategic shift to Copilot, not adoption failure. A new risk: LLMs are drying up the very public Q&A sources that reconstruction depends on.

### Cited Findings
- Knowledge "stickiness": the main barriers to internal best-practice transfer were knowledge-related (the recipient's lack of absorptive capacity, causal ambiguity, an arduous source–recipient relationship), not motivation. ESTABLISHED (highly cited empirical study). — [Szulanski 1996, doi:10.1002/smj.4250171105](https://doi.org/10.1002/smj.4250171105)
- Knowledge hiding (evasive hiding, playing dumb, rationalised hiding) is a distinct, measurable behaviour, separate from lack of sharing. ESTABLISHED. — [Connelly et al. 2012, doi:10.1002/job.737](https://doi.org/10.1002/job.737)
- Codification vs personalisation strategy: firms should lean predominantly one way, and codification suits reusable, standardised knowledge. ESTABLISHED as practitioner framework (HBR; not verified in OpenAlex). — [Hansen, Nohria & Tierney 1999, HBR](https://hbr.org/1999/03/whats-your-strategy-for-managing-knowledge)
- Viva Topics (AI-built topic pages from M365 content): feature development stopped on 22 Feb 2024 and the product retired on 22 Feb 2025. Microsoft attributed this to refocusing on Copilot-based knowledge experiences. I found no primary adoption figures. WEAK evidence for "KM tools fail from non-adoption". — [Microsoft Learn: Changes coming to Topics](https://learn.microsoft.com/en-us/microsoft-365/topics/changes-coming-to-topics?view=o365-worldwide); [Office365ITPros](https://office365itpros.com/2024/02/23/viva-topics-retirement/)
- Source erosion: Stack Overflow activity fell about 25% within 6 months of ChatGPT's release relative to counterfactual platforms, with no significant change in post quality, among both more and less experienced users. ESTABLISHED (PNAS Nexus, difference-in-differences). — [del Rio-Chanona et al. 2024](https://doi.org/10.1093/pnasnexus/pgae400). Possible counterpoint (not read beyond the title): [arXiv:2609.12447, "Informational help-seeking on Reddit did not decline after ChatGPT"](https://arxiv.org/pdf/2609.12447)
- Positive signal: organisational conversation data used as AI assistance transferred top-performer practice to novices in a firm. ESTABLISHED. — [Brynjolfsson et al. 2025](https://doi.org/10.1093/qje/qjae044)

### Inferences
- Reconstruct-first *helps* the product thesis on Szulanski's barriers: a pre-built model reduces the arduous source–recipient relationship and lowers the cost of expert time, because experts correct rather than dictate. That is a genuine argument for the reorientation. SPECULATIVE until measured.
- Motivation and incentives still matter for the "retiring expert" case (knowledge hiding, job security). Design for low expert burden and credit attribution. Provenance tracking can double as attribution.
- Reconstruction from public Q&A has a shrinking base. The exception sources in Q3 are being displaced by private LLM chats, so the method becomes relatively more dependent on organisational and human data over time.

### Gaps
- There is no rigorous published adoption study of Viva Topics or comparable AI-KM products. Enterprise KM failure-rate figures that circulate (e.g. "50–70%") had no traceable primary source and were not used.

---

## Q3. Given reporting bias, is the "human knowledge residual" concentrated in the obvious-to-experts steps? Which public texts are exceptions?

### Takeaway
Yes. Three independent mechanisms point to the same place:
1. Text under-reports what is obvious to its writers (reporting bias).
2. Experts omit about 70% of the steps novices need, and cannot verbalise automated processes.
3. LLMs trained on that text fail to simulate learners' limitations (difficulty misalignment, the competence paradox).

The residual should therefore be densest in the compiled, "obvious" expert steps and the novice difficulties they cause, which is the knowledge the project cares about most. The exceptions are texts produced *at the expert–novice boundary*, where a novice's question or error forces articulation.

### Cited Findings
- Text omits the obvious. — [Gordon & Van Durme 2013](https://doi.org/10.1145/2509558.2509563); LMs inherit this. — [Paik et al. 2021](https://arxiv.org/abs/2110.08182)
- Expert explanations omit about 70% of the steps novices need. — [Sullivan et al. 2014](https://doi.org/10.1097/acm.0000000000000224)
- Experts misjudge what is hard for novices. — [Nathan & Petrosino 2003](https://doi.org/10.3102/00028312040004905); [Hinds 1999](https://doi.org/10.1037/1076-898x.5.2.205)
- LLMs misjudge what is hard for learners and converge to machine consensus. — [Li et al. 2025](https://arxiv.org/abs/2512.18880)
- Learner data correct expert cognitive models. — [Koedinger et al. 2013](https://doi.org/10.1609/aimag.v34i3.2484)
- A boundary source is shrinking: Stack Overflow activity fell about 25% after ChatGPT. — [del Rio-Chanona et al. 2024](https://doi.org/10.1093/pnasnexus/pgae400)

### Inferences
- Two different "obviousness" relations need to be kept apart:
  1. Obvious to everyone (commonsense). This is classic reporting bias, largely irrelevant to domain instruction.
  2. Obvious to experts but not to novices (expert blind spot). This is the target. Expert-to-expert text (papers, standards, SOPs) omits it almost entirely. Expert-to-novice text (textbooks, SOPs for trainees) contains it only partly: the 70% rule applies to instruction as well.
- Public text sources that break the pattern, ranked by expected yield for the target layer. These are my inferences unless cited.
  1. **Expert–novice and CTA research itself.** Published think-aloud protocols, CTA-derived procedures and expert–novice contrasts (e.g. [Chi et al. 1981](https://doi.org/10.1207/s15516709cog0502_2); [Sullivan et al. 2014](https://doi.org/10.1097/acm.0000000000000224)). This is the highest-yield source, but it covers few tasks.
  2. **Discipline-based education research on learner errors.** Misconception catalogues, concept inventories and their distractor rationales (e.g. [FCI, Hestenes et al. 1992](https://doi.org/10.1119/1.2343497)), and error-analysis studies. Dense in physics, math, chemistry and intro CS; sparse in vocational and company domains.
  3. **Novice-asks, expert-answers forums.** Physics/Math Stack Exchange, r/AskPhysics, vendor community forums, GitHub issues. The novice question exposes the gap and the accepted answer forces articulation. The base is shrinking (del Rio-Chanona 2024).
  4. **Examiner and marker reports.** Some exam boards publish reports on common candidate errors per question. This is high-signal learner-error text, and near-free.
  5. **Worked solutions with commentary, instructor guides and PCK documents** (CoRes; [Loughran et al. 2004](https://doi.org/10.1002/tea.20007)). Teacher-facing text is where "what makes this hard" gets written down.
  6. **Incident reports, postmortems and case reviews** (aviation safety reporting, morbidity-and-mortality reviews, software postmortems). They record work-as-done and cue failures ([Hollnagel 2014](https://openalex.org/W300856602)).
  7. **Video and live demonstrations with narration** (repair videos, live coding). These are partial carriers of perceptual and procedural cues. Transcripts lose the visual channel.
  8. **Design rationale artefacts** (ADRs, code-review threads, commit messages) for software platforms ([Burge et al. 2008](https://doi.org/10.1007/978-3-540-77583-6)).
- Corollary: the residual is not a fixed quantity. It depends on the domain's boundary-text density. It will look small in introductory mechanics and large in one firm's troubleshooting, so any residual estimate from physics will overstate reconstructability elsewhere.

### Gaps
- There is no quantitative estimate of how much of a CTA-elicited procedure appears anywhere in public text. This is measurable and should be measured.

---

## Q4. Verdict: does the evidence support, qualify, or contradict the reconstruct-first reorientation?

### Takeaway
**It qualifies it.** The evidence supports reconstruct-first as a way to *locate* gaps, *reduce expert burden* and *generate candidate tasks and hypotheses*, with provenance. It contradicts three parts of the proposal:
- that a synthetic cohort can stand in for learners before any real learner data exist;
- that surrogate expert perspectives are independent;
- that the method's validity transfers across domains without per-domain human calibration.

Because of reporting bias, the residual is concentrated in the obvious-to-experts steps. The step that matters most is therefore the one reconstruction is structurally worst at.

### Cited Findings
- Synthetic effects are inflated and give false positives on nulls. — [Cui et al. 2025](https://doi.org/10.1038/s43588-025-00840-7)
- Simulated misconceptions are unstable. — [Do et al. 2026](https://arxiv.org/abs/2605.12748)
- Simulators match learners poorly unless fine-tuned. — [Scarlatos et al. 2026](https://arxiv.org/abs/2601.04025)
- Grounding in real individuals improves fidelity from 74% to 86% of the test-retest ceiling. — [Park et al. 2024](https://arxiv.org/abs/2411.10109)
- Models converge to machine consensus. — [Li et al. 2025](https://arxiv.org/abs/2512.18880)
- Long-tail hallucination. — [Kandpal et al. 2023](https://arxiv.org/abs/2211.08411); [Kalai et al. 2025](https://arxiv.org/abs/2509.04664)
- Expert omission. — [Sullivan et al. 2014](https://doi.org/10.1097/acm.0000000000000224)
- Learner data reveal missed components. — [Koedinger et al. 2013](https://doi.org/10.1609/aimag.v34i3.2484)
- Organisational data transfer tacit practice. — [Brynjolfsson et al. 2025](https://doi.org/10.1093/qje/qjae044)
- Tutoring gains depend on guardrails and design. — [Bastani et al. 2025](https://doi.org/10.1073/pnas.2422633122); [Kestin et al. 2025](https://doi.org/10.1038/s41598-025-97652-6)

### Inferences — specific design changes
1. **Reorder: real learner errors early, not last.** Move a small real-error sample ahead of the synthetic cohort and use it to calibrate the cohort (Park; Koedinger). In this project, Early K0 already supplies it. Keep the reconstruct-first model, but let learner errors be the second input, not the fourth.
2. **Demote the surrogate cohort to a hypothesis generator.** It may propose candidate errors and pretest coarse item difficulty (weak models plus IRT, as in Acquaye). It must never estimate effect sizes, prevalence or rank interventions (Cui; Do). Any surrogate-derived claim carries a `synthetic` provenance tag, and gates may not consume it.
3. **Provenance as a hard gate.** Every model node needs a resolvable source span. Parametric-only content is flagged and excluded from gates. Automated citation resolution is required (Walters & Wilder; the NeurIPS evidence; the summariser hallucination caught in this session).
4. **Do not assume surrogate independence.** Use multiple model families, source-diverse retrieval, and Cooke-style calibration on seed questions with known answers for surrogate *and* human experts. Treat surrogate agreement as weak evidence (Li; Kleinberg & Raghavan).
5. **Measure the residual; do not define it by subtraction.** Keep a *blind* human-elicitation arm, run before experts see the reconstruction, so that anchoring on the AI model does not shrink the apparent residual. This is SPECULATIVE on anchoring size but cheap to guard against. Score minority expert contributions with surprisingly-popular or BTS-style prompts, so that unique human knowledge is not averaged away (Prelec et al. 2017).
6. **A cheap test inside the current study (no change to registered rules).** Before Stage A, have the reconstructor produce its operation list for the Stage A problems from public sources only. After coding, report as a *secondary, non-gating* measure what fraction of K1's new shared operations were reconstructable. Similarly, have an LLM predict the Early K0 error-category distribution before coding, and compare. Together these test the residual thesis and the synthetic-cohort thesis on the project's own data.
7. **Typed knowledge, typed channels.** Tag nodes as relational, perceptual, somatic or collective (Collins) and route each to a matched channel: probes or CTA for relational; contrasting-case classification for perceptual (Biederman & Shiffrar; Kellman); observation or narrative capture for collective and troubleshooting (Orr).
8. **Universality as a falsification target, not a premise.** Add a deliberately text-poor second domain (vocational or one firm's troubleshooting) before claiming generality. Physics is near a best case for boundary-text density.
9. **Company track: organisational event data before public text.** Compare SOPs (work-as-imagined) with process-mined logs and ticket or chat histories (work-as-done). The divergence *is* the residual map there (Hollnagel; van der Aalst; Brynjolfsson). Use truck-factor analysis to prioritise which experts to elicit (Avelino).
10. **Hybrid representation.** Use a graph for concepts, prerequisites and misconceptions (knowledge spaces, KCs); solution-path libraries for procedures (example tracing); contrasting-case sets for perception; and ECD to derive diagnostic tasks from the model.
11. **Learner-facing guardrails, if tutoring is later added.** Scaffold, and withhold answers (Bastani). This is outside the static first version but constrains any later live-LLM milestone.

### Gaps
- The decisive missing study is a same-domain comparison of an LLM-reconstructed expertise model with a CTA- or job-analysis-derived one, scored on real learner data (KC-model fit, error-category recall). The project's Stage A plus Early K0 can approximate it with change 6 above.
