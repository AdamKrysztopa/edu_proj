# Autonomous LLM reconstruction of an evidence-grounded domain model: state of the art and failure modes

Scope: how reliably LLMs and agentic research systems, started from only a domain/role/objective, can build a provenance-tracked model of concepts, prerequisites, procedures, misconceptions and expert–novice differences from public sources. Compiled 2026-09-28.

Tags: **ESTABLISHED** = replicated or large-n and consistent across studies; **PROMISING** = one or a few credible studies, positive but narrow; **SPECULATIVE** = single small study, simulation only, or my extrapolation.

Verification: every arXiv ID below was resolved against arxiv.org on 2026-09-28 and its title and first author checked. DOIs were resolved through OpenAlex. Numbers come from the abstract or full text of the cited work unless marked "secondary".

---

## 1. Agentic deep-research systems: factual accuracy, citation accuracy, hallucinated references, coverage, cost

### Takeaway
The best systems now put citation *links* at 80–90%+ validity, but claim-level *support* is much weaker. Across independent audits, 20–60% of statements are unsupported by the sources the system itself cites, and coverage of what experts consider essential tops out around 75% on rubric benchmarks. More retrieval does not fix this: one 2026 study found factual support fell as tool calls rose. The narrow, literature-grounded systems (PaperQA2, OpenScholar) are the reliable exception, and only inside their scientific-paper corpora.

### Cited Findings
**Foundational audits (ESTABLISHED; the pattern replicates through 2026)**
- Generative search engines (Bing Chat, NeevaAI, perplexity.ai, YouChat): only 51.5% of generated sentences were fully supported by their citations, and only 74.5% of citations supported their associated sentence. The answers read as fluent and informative anyway. — [Liu, Zhang & Liang 2023, arXiv:2304.09848](https://arxiv.org/abs/2304.09848)
- ALCE benchmark: even the best models lacked complete citation support 50% of the time on ELI5. — [Gao et al. 2023, arXiv:2305.14627](https://arxiv.org/abs/2305.14627)
- Fabricated bibliographic references: 55% of GPT-3.5 and 18% of GPT-4 citations were fabricated in literature-review prompts, and many "real" ones had substantive errors. — [Walters & Wilder 2023, Sci Rep, doi:10.1038/s41598-023-41032-5](https://doi.org/10.1038/s41598-023-41032-5) (DOI verified; percentages from the abstract as I recall it and not re-read this session, so treat them as approximate).

**Deep-research agents, 2025–2026 (ESTABLISHED as a direction; exact numbers vary by judge)**
- DeepResearch Bench (100 PhD-level tasks, 22 fields; citation support judged by an LLM that agreed with humans in 96% of "support" and 92% of "not support" cases on 100 pairs). Citation accuracy / effective citations per report:
  - Gemini-2.5-Pro Deep Research: 81.44% / 111.21
  - OpenAI Deep Research: 77.96% / 40.79
  - Perplexity Deep Research: 90.24% / 31.26
  - Grok Deeper Search: 83.59% / 8.15

  The trade-off is volume versus precision. — [Du et al. 2025, arXiv:2506.11763](https://arxiv.org/abs/2506.11763)
- DeepTRACE (ICLR 2026) audited GPT-4.5/5, You.com, Perplexity, Copilot/Bing and Gemini in search and deep-research modes. Deep-research modes "reduce overconfidence" but "remain highly one-sided on debate queries and still exhibit large fractions of unsupported statements, with citation accuracy ranging from 40–80% across systems." — [Venkit et al. 2025, arXiv:2509.04499](https://arxiv.org/abs/2509.04499)
- **Unreliability signal:** across 14 LLMs generating cited reports, link validity was above 94% and relevance above 80%, but factual accuracy against source content was only **39–77%**. Fact-check accuracy **dropped about 42%** as tool calls scaled from 2 to 150, so "more retrieval does not produce more accurate citations." Fewer than half of the open-source models could produce a cited report in one shot. — [Onweller et al. 2026, arXiv:2605.06635](https://arxiv.org/abs/2605.06635) (PROMISING: a single study with an LLM judge calibrated by human review)
- **Unreliability signal:** across 10 models/agents on DRBench (53,090 URLs) and 3 models on ExpertQA (168,021 URLs, 32 fields), **3–13% of citation URLs were hallucinated** (never existed per the Wayback Machine) and 5–18% did not resolve. Deep-research agents cite more but "hallucinate URLs at higher rates." Non-resolving rates vary by domain, from 5.4% in Business to 11.4% in Theology. — [Rao et al. 2026, arXiv:2604.03173](https://arxiv.org/abs/2604.03173)
- FINDER/DEFT: about 1,000 reports from mainstream deep-research agents were coded into 14 failure modes. Agents "struggle not with task comprehension but with evidence integration, verification, and reasoning-resilient planning." — [Zhang et al. 2025, arXiv:2512.01948](https://arxiv.org/abs/2512.01948)
- ReportBench uses published arXiv surveys as gold references. Commercial deep-research agents beat search-augmented LLMs but show "substantial room for improvement" in breadth, depth and factual consistency. — [Li et al. 2025, arXiv:2508.15804](https://arxiv.org/abs/2508.15804)

**Coverage against expert-written reviews (ESTABLISHED that coverage is incomplete)**
- ResearchQA distilled surveys from 75 fields into 21K queries and 160K rubric items; 31 PhD annotators judged 90% of queries to reflect PhD needs. No system exceeded 75% rubric coverage. The top system fully addressed **<11% of citation items, 48% of limitation items and 49% of comparison items.** — [Yifei et al. 2025, arXiv:2509.00496](https://arxiv.org/abs/2509.00496)
- DeepScholar-Bench, a live benchmark of generative research synthesis: "no system surpasses a geometric mean of 31% across all metrics." — [Patel et al. 2025, arXiv:2508.20033](https://arxiv.org/abs/2508.20033)
- LitSearch (597 ML/NLP literature queries): commercial search engines and research tools, Google Search included, trail the best dense retriever by up to 32 recall points. — [Ajith et al. 2024, arXiv:2407.18940](https://arxiv.org/abs/2407.18940)
- STORM (Wikipedia-style articles from scratch): +25% absolute on organization and +10% on coverage versus an outline-RAG baseline, with citation recall 84.83% and precision 85.18%. Experienced Wikipedia editors reported **source-bias transfer** (7/10 found articles "emotional"/"unneutral") and **"improper inferential links"** between facts, the most common citation error, beyond simple hallucination. — [Shao et al. 2024 (NAACL), arXiv:2402.14207](https://arxiv.org/abs/2402.14207)
- Co-STORM, a human-in-the-loop variant: 70% of participants preferred it over a search engine and 78% over a RAG chatbot. — [Jiang et al. 2024, arXiv:2408.15232](https://arxiv.org/abs/2408.15232)
- AutoSurvey, 64k-token surveys: citation recall 82.25% and precision 77.41%, versus human-written 86.33% and 77.78%, and naive RAG 68.79% and 61.97%. Its evaluation is itself LLM-judged. — [Wang et al. 2024 (NeurIPS), arXiv:2406.10252](https://arxiv.org/abs/2406.10252)

**Domain-specialised scientific agents (PROMISING; strong within scope)**
- PaperQA2 on LitQA2: precision 85.2% ± 1.1 and accuracy 66.0% ± 1.2, against human experts (n=9) at 73.8% ± 9.6 and 67.7% ± 11.9. That is "superhuman precision," with accuracy no different from the experts.
  - WikiCrow articles: 13.5% cited-and-unsupported statements versus 24.9% for human Wikipedia, over 375 statements.
  - Contradiction detection (ContraCrow): 2.34 ± 1.99 contradictions per biology paper, 70% validated by experts. Human–human agreement (75.5%) exceeded human–ContraCrow agreement (60.4%).
  - — [Skarlinski et al. 2024, arXiv:2409.13740](https://arxiv.org/abs/2409.13740)
- OpenScholar, a retrieval-augmented LM over 45M open-access papers, with ScholarQABench (2,967 expert queries, 208 long-form answers across CS, physics, neuroscience and biomedicine). **GPT-4o hallucinated citations 78–90% of the time**, while OpenScholar matched human-expert citation accuracy. Experts preferred OpenScholar-8B / OpenScholar-GPT4o answers over expert-written ones 51% / 70% of the time, versus 32% for GPT-4o. — [Asai et al. 2024, arXiv:2411.14199](https://arxiv.org/abs/2411.14199); published as [Asai et al. 2026, Nature 650:857–863, "Synthesizing scientific literature with retrieval-augmented language models"](https://www.nature.com/articles/s41586-025-10072-4)
- An independent evaluation of the AI Scientist found:
  - 42% of experiments failed on coding errors;
  - literature reviews misjudged novelty, calling established concepts such as micro-batching for SGD novel;
  - manuscripts had a median of 5 citations, and only 5 of 34 dated from 2020 or later;
  - some papers contained hallucinated numerical results.
  - — [Beel et al. 2025, arXiv:2502.14297](https://arxiv.org/abs/2502.14297); original system: [Lu et al. 2024, arXiv:2408.06292](https://arxiv.org/abs/2408.06292)

**Medical and news domains (ESTABLISHED as a pattern)**
- SourceCheckup tested 7 LLMs on 800 medical questions and 58,000 statement–source pairs. **50–90% of responses were not fully supported** (sometimes contradicted) by their cited sources. Even for GPT-4o with Web Search, about 30% of statements were unsupported and nearly half of responses not fully supported. The automated judge agreed 89% with a consensus of 3 physicians. — [Wu et al. 2025, Nat Commun, doi:10.1038/s41467-025-58551-6](https://doi.org/10.1038/s41467-025-58551-6)
- Tow Center test of 8 AI search engines on 1,600 queries: they identified the correct article or citation less than 40% of the time, with error rates from 37% (Perplexity) to 94% (worst performer). — [Columbia Journalism Review, Mar 2025](https://www.cjr.org/tow_center/we-compared-eight-ai-search-engines-theyre-all-bad-at-citing-news.php) (grey literature)

**Hallucinated references in the peer-reviewed record (ESTABLISHED as happening)**
- GPTZero found 100+ hallucinated citations across 51 of 4,841 NeurIPS 2025 accepted papers — [GPTZero](https://gptzero.me/news/neurips/) (vendor report). RefChecker, under a strict identity-level definition, found about 1 in 20 NeurIPS 2025 and USENIX Security papers with ≥2 likely hallucinated references. — [Russinovich et al. 2026, arXiv:2607.00738](https://arxiv.org/abs/2607.00738)

**Cost (PROMISING; prices change fast)**
- The o3-deep-research API lists $10 per million input tokens and $40 per million output tokens — [OpenRouter listing](https://openrouter.ai/openai/o3-deep-research-2025-06-26). Artificial Analysis reported spending about $100 over 10 o3 deep-research queries (up to ~$30 a call) and $9.18 with o4-mini — [Artificial Analysis on X](https://x.com/ArtificialAnlys/status/1940896348364210647) (secondary).
- PaperQA2 costs $1–3 per query, and WikiCrow $4.48 ± 1.02 per article at about 8 minutes each — [arXiv:2409.13740](https://arxiv.org/abs/2409.13740). AutoSurvey costs $0.89 per 32k-token survey with Claude-3-Haiku — [arXiv:2406.10252](https://arxiv.org/abs/2406.10252). The AI Scientist costs under $15 per paper — [arXiv:2408.06292](https://arxiv.org/abs/2408.06292).

### Inferences
- A domain-model builder can count on real, resolving links (after a URL-liveness filter), but not on the claim a link is attached to. Claim-level support around 60–85% means one in six to one in three extracted "facts" will lack support in any auto-built domain model unless every claim is checked.
- The best-evidenced accuracy comes from systems restricted to a curated corpus of full-text scientific papers (PaperQA2, OpenScholar). An open-web agent working on "centrifugal pump troubleshooting" or "onboarding a backend engineer" lacks both the corpus and the benchmark evidence.
- Most headline numbers rest on LLM judges. Where the judges were validated (DeepResearch Bench, SourceCheckup), they agree with humans about 89–96% of the time, so a 5–10% judge-error floor should be budgeted.

### Gaps
- I found no benchmark measuring deep-research agents on industrial, organisational or vocational domains; all coverage benchmarks use academic surveys or PhD-style questions.
- No peer-reviewed per-report cost figures for commercial deep-research products; the published figures are API list prices and anecdotes.
- Anthropic's and Google's own published deep-research accuracy figures were not located in this pass.

---

## 2. LLM-based knowledge-graph and ontology construction: precision/recall against gold, typical errors

### Takeaway
Zero-shot LLMs do lexical typing well in generic domains but poorly in specialised ones, and non-taxonomic relations poorly everywhere; the best F1 was about 0.5 in 2023. Fine-tuning, schemas and canonicalisation help substantially. GraphRAG improves LLM-judged "comprehensiveness" but has no gold-standard validation, and independent benchmarks find it often underperforms plain RAG.

### Cited Findings
- LLMs4OL (zero-shot, nine model families) (ESTABLISHED as a baseline):
  - term typing MAP@1 was 91.7% on WordNet (GPT-3.5), 43.3% on GeoNames (GPT-4) and 16.1–37.7% on UMLS sub-ontologies;
  - taxonomy discovery F1 was 67.8% on GeoNames, 78.1% on UMLS and 74.4% on schema.org;
  - **non-taxonomic relation extraction F1 was 49.5% on UMLS.**

  The authors conclude foundational LLMs "are not sufficiently suitable for ontology construction that entails a high degree of reasoning skills and domain expertise"; fine-tuning added about 25% on typing and about 18% on taxonomy. — [Babaei Giglou et al. 2023 (ISWC), arXiv:2307.16648](https://arxiv.org/abs/2307.16648). Follow-up shared task: [LLMs4OL 2024 Overview, arXiv:2409.10146](https://arxiv.org/abs/2409.10146)
- GPT-4 is "more suited as an inference assistant rather than few-shot information extractor" for KG construction, and it underperforms fine-tuned extractors. — [Zhu et al. 2023, arXiv:2305.13168](https://arxiv.org/abs/2305.13168) (ESTABLISHED for 2023-era models)
- Text2KGBench (Wikidata-TekGen: 10 ontologies, 13,474 sentences; DBpedia-WebNLG: 19 ontologies, 4,860 sentences) defines metrics for fact precision/recall, ontology conformance and **hallucination** by LLMs. — [Mihindukulasooriya et al. 2023, arXiv:2308.02357](https://arxiv.org/abs/2308.02357)
- A schema has to fit in the prompt, which breaks at scale. Extract–Define–Canonicalize (open IE, then schema definition, then canonicalisation) produces a self-generated schema without parameter tuning. — [Zhang et al. 2024, arXiv:2404.03868](https://arxiv.org/abs/2404.03868) (PROMISING)
- A contrast case: on semi-structured cloud logs with a hand-built reference KG, few-shot Llama reached 99.35% triple F1. — [Martin et al. 2026, arXiv:2603.29878](https://arxiv.org/abs/2603.29878). High scores are attainable when the input is structured and the schema fixed. Neither holds for "reconstruct a domain from public prose."
- **Expert-elicitation ontologies (unreliability signal, SPECULATIVE given the small n):** ChatGPT-4 was compared with human-expert interviews, with the extracted knowledge turned into RDF ontologies and scored against a base-truth ontology. **19–32% of classes in AI-generated ontologies were hallucinated**, and there were type/instance confusions (individuals modelled as subclasses). The authors recommend LLMs for fast interviewing but humans for ontology creation. — [van den Bent, Pernisch & Schlobach, "Investigating Knowledge Elicitation Automation with Large Language Models," Semantic Web Journal submission swj3868](https://www.semantic-web-journal.net/system/files/swj3868.pdf) (preprint under review; two human experts)
- GraphRAG: "all Graph RAG conditions outperformed naive RAG on comprehensiveness and diversity" for global sense-making questions over corpora of about 1M tokens. Root-level community summaries need 9–43× fewer tokens per query than source-text summarisation. **Every quality score came from an LLM judge in head-to-head comparisons; there was no gold graph or fact-level accuracy.** — [Edge et al. 2024, arXiv:2404.16130](https://arxiv.org/abs/2404.16130)
- GraphRAG-Bench: "recent studies report that GraphRAG frequently underperforms vanilla RAG on many real-world tasks" — [Xiang et al. 2025, arXiv:2506.05690](https://arxiv.org/abs/2506.05690). A systematic RAG vs GraphRAG study found task-dependent strengths and evaluation biases — [Han et al. 2025, arXiv:2502.11371](https://arxiv.org/abs/2502.11371) (ESTABLISHED that GraphRAG is not a uniform win)
- LLM knowledge materialisation at scale: GPTKB v1.5 is a 100M-triple KB built from GPT-4.1 for $14,000, a KB of what the model *believes* rather than what sources say. — [Hu et al. 2025, arXiv:2507.05740](https://arxiv.org/abs/2507.05740)

### Inferences
- The concept inventory (terms, taxonomy) is the part an autonomous pipeline can draft most reliably. Relations beyond is-a, including prerequisite, causes, used-for and misconception-of, are the weakest link, and they are exactly what a domain model for instruction needs.
- A graph index (GraphRAG) is a retrieval and summarisation convenience, not a validated domain model. Its entities and relations inherit the same extraction errors, and the quality evidence is LLM-judged preference.

### Gaps
- No gold-standard evaluation was found of an end-to-end autonomous domain-ontology build, from topic string through web search to ontology, against an expert ontology in a technical or vocational domain.
- The 2025–2026 LLMs4OL challenge scores were not extracted.

---

## 3. Prerequisite relations, concept maps, knowledge components and learning objectives

### Takeaway
Evidence is thin and evaluation is weak. Studies score LLM prerequisite and concept output by semantic similarity (BERTScore) or by expert preference rather than edge-level precision/recall. Where exact matching was used, LLMs matched expert knowledge-component labels for only 35–56% of items.

### Cited Findings
- LectureBank: 1,352 lecture files and 208 manually labelled prerequisite topics in NLP. It is the standard gold set, and it is small. — [Li et al. 2019 (AAAI), arXiv:1811.12181](https://arxiv.org/abs/1811.12181)
- ESCO-PrereqSkill: 3,196 skills with expert-defined prerequisite links, and 13 LLMs tested zero-shot. The best BERTScore F1 was 0.835 (LLaMA4-Maverick). **The metric is semantic similarity of generated text to expert prerequisites, not precision/recall over edges.** — [Le et al. 2025, arXiv:2507.18479](https://arxiv.org/abs/2507.18479) (PROMISING at best; metric validity is weak)
- Concept generation and extraction plus relation identification with GPT-3.5, GPT-4o-mini and GPT-4o: GPT-3.5 scored highest on P/R/F1 against ground truth, but experts judged GPT-4o output more "educationally meaningful despite lexical divergence." **Automatic metrics and expert judgement disagree**, a warning about metric choice. — [Yang et al. 2025, MAKE 7(3):103, doi:10.3390/make7030103](https://doi.org/10.3390/make7030103)
- Knowledge components: GPT-4-generated KCs matched human KCs for **56% of chemistry and 35% of e-learning MCQs**, better with top-5 suggestions. — [Moore et al. 2024 (L@S), arXiv:2405.20526](https://arxiv.org/abs/2405.20526) (PROMISING)
- Skill decomposition against ESCO/ROME ontologies: zero-shot gives a strong baseline, and few-shot stabilises granularity. A hierarchy-aware F1 is introduced, which shows granularity mismatch is a core error. — [Le et al. 2025, arXiv:2510.11313](https://arxiv.org/abs/2510.11313)
- Learning objectives: GPT-4 generated 127 LOs for a university AI course and they were rated against LO quality guidelines. — [Sridhar et al. 2023, arXiv:2306.17459](https://arxiv.org/abs/2306.17459) (result figures not extracted)

### Inferences
- An autonomous pipeline can propose a plausible prerequisite graph, but nothing published shows it recovers the expert graph's edges at a known precision/recall. BERTScore-style results are compatible with many wrong or missing edges.
- Granularity (how fine a concept or KC is) is a recurrent mismatch, and it will matter for any cohort-level diagnosis that relies on KC tagging.

### Gaps
- No 2024–2026 study found reporting edge-level precision/recall of frontier LLMs on LectureBank or AL-CPL. The AL-CPL reference (Liang et al. 2018) was not verified in this pass.
- No study found comparing LLM concept maps with expert concept maps in physics specifically.

---

## 4. Misconceptions, distractors, diagnostic items and prediction of student errors

### Takeaway
LLMs can generate valid distractors and can role-play documented misconceptions when told which one. They are poor at anticipating which errors real students actually make and how often: correlations with student distractor choices are only moderate, LLM errors cluster on one distractor while students spread out, and direct difficulty prediction is weak. Simulation-plus-IRT approaches are more promising. Physics-specific evidence exists (the FCI) but relies on inventories that are in the training data.

### Cited Findings
- Distractor generation for math MCQs: LLMs "can generate some mathematically valid distractors" but "are less adept at anticipating common errors or misconceptions among real students." — [Feng et al. 2024 (NAACL Findings), arXiv:2404.02124](https://arxiv.org/abs/2404.02124) (ESTABLISHED; replicated by the next two items)
- LLM token probabilities over distractors show only **moderate correlation** with real student selection rates. When LLMs err, they tend to pick the most common student distractor, but a "gap between LLM's underlying reasoning process and human cognitive processes" remains. — [Liu, Sonkar & Baraniuk 2025, arXiv:2502.15140](https://arxiv.org/abs/2502.15140)
- DiVERT (1,434 real math MCQs answered by hundreds of thousands of students): a 7B model with learned error representations beat GPT-4o on distractor generation, and its error labels were comparable to human-authored ones. Learning from real response data beats prompting a frontier model. — [Fernandez et al. 2024, arXiv:2406.19356](https://arxiv.org/abs/2406.19356) (PROMISING)
- Eedi "Mining Misconceptions in Mathematics" (Kaggle 2024) required ranking the top 25 of 2,500+ catalogued misconceptions per distractor, scored by MAP@25. The winning approach distilled Claude 3.5 Sonnet reasoning into retrievers and rerankers. — [Kaggle competition](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics); [Eedi blog](https://www.eedi.com/news/from-wrong-answers-to-real-insights-how-we-used-a-kaggle-challenge-to-map-student-misconceptions). This is *matching to an existing expert catalogue*, not discovering misconceptions.
- MalAlgoPy (16 algebra problem types, 20 misconceptions): LLMs fine-tuned on misconception examples learn to replicate errors but lose the ability to solve problems where the misconception does not apply, unless correct examples are mixed in (ratio as low as 0.25). — [Sonkar et al. 2024, arXiv:2410.12294](https://arxiv.org/abs/2410.12294). Follow-up: a single misconception is "overapplied across problems," and "intermediate reasoning steps are the bottleneck." — [Liu et al. 2026, arXiv:2604.00818](https://arxiv.org/abs/2604.00818)
- **Physics, FCI:** ChatGPT (GPT-4) averaged 83% on the FCI. Prompting it to answer as a student from a different cohort produced **no variance**; prompting a specific preconception produced variance that "approximate[s] real human responses on the FCI in some regards." — [Kieser et al. 2023, Phys Rev PER 19:020150, doi:10.1103/PhysRevPhysEducRes.19.020150](https://doi.org/10.1103/PhysRevPhysEducRes.19.020150) (PROMISING; inventory contamination likely)
- **Physics, uncontaminated inventory (unreliability signal):** on the Classical Relativity Concept Inventory, unpublished at test time (21 items × 30 runs × 3 models = 1,890 responses), accuracy was 97% (Gemini 3 Flash), 89% (Gemini 3 Pro) and 73% (GPT-5.2), against 62% for 267 students. All models failed completely on a few items, mostly through visual misinterpretation. **When models err they converge on a single distractor, whereas student errors are broadly distributed.** — [Tufino et al. 2026, arXiv:2605.09602](https://arxiv.org/abs/2605.09602)
- Item difficulty (unreliability signal, ESTABLISHED across studies):
  - Across 20+ models, human–AI difficulty alignment is systematically poor. Models "converge toward a shared machine consensus," "struggle to simulate the capability limitations of students even when explicitly prompted," and "fail to predict their own limitations." — [Li et al. 2025, arXiv:2512.18880](https://arxiv.org/abs/2512.18880)
  - Direct judgement is poor, but simulated classrooms fitted with IRT correlated 0.75/0.76/0.82 with NAEP item correctness for grades 4/8/12. Weaker-at-math models predicted better. — [Acquaye et al. 2026, arXiv:2601.09953](https://arxiv.org/abs/2601.09953)
  - Item discrimination across 42 LLMs: direct prediction is weak, and the best proxy rank correlation was 0.231. — [Chen et al. 2026, arXiv:2606.18709](https://arxiv.org/abs/2606.18709)
  - Pairwise LLM difficulty judgements on primary math correlated moderately to strongly with empirical difficulty. — [Kolesnikova et al. 2026, arXiv:2605.18562](https://arxiv.org/abs/2605.18562)

### Inferences
- A pipeline can reproduce catalogued misconceptions from public literature, for example physics PER inventories, and turn them into distractors. It cannot tell which misconceptions dominate in a given cohort, or how often, without real response data. That makes an early cohort-level error audit like K0 necessary rather than a redundant check.
- LLM "errors" are not a proxy for student errors: they are too concentrated (Tufino) and too tied to the model's own competence (Li et al. 2025; Acquaye et al. 2026).

### Gaps
- No study found that measures how well autonomously *discovered* misconceptions (with no catalogue given) recall a documented catalogue such as the FCI taxonomy or Eedi's, with precision and recall.
- The final Eedi Kaggle MAP@25 leaderboard scores were not verified.

---

## 5. Expert–novice differences and cognitive task analysis (CTA) outputs

### Takeaway
No study was found in which an LLM, working only from public sources, produced a CTA, task analysis or SOP that was scored against an expert-produced CTA. The few positive results all need *expert behaviour data*: transcripts, conversations or interviews. The honest status is **untested for public-source-only reconstruction**.

### Cited Findings
- Math tutoring study. LLMs *externalising tacit knowledge from 320 real expert tutoring conversations* produced guidance that scored about 7.2/10 in response quality, above both expert-articulated knowledge from CTA-style interviews (about 7.0) and expert responses (about 6.8). Novices trained on it (85–99 per condition) narrowed the expert–novice gap. **The effect depended on having expert conversation data and a capable model; a weak LLM gave no benefit.** — [Cho et al. 2026, "Large Language Models Explain Experts Better Than Experts Themselves," arXiv:2608.07488](https://arxiv.org/abs/2608.07488) (PROMISING; one domain, preprint)
- An agent reconstructing organisational dataset knowledge by interviewing simulated employees reached 94.9% full-knowledge recall, **in 864 simulations of synthetic companies only.** — [Zuin et al. 2025, arXiv:2507.03811](https://arxiv.org/abs/2507.03811) (SPECULATIVE for real organisations)
- LLM estimates of individual domain knowledge from Slack logs (27,188 messages, 43 users): the best MAE against self-ratings was 21.1% (Gemini 2.5 Flash), and more text did not reliably help. — [Watanabe et al. 2026, arXiv:2605.22971](https://arxiv.org/abs/2605.22971)
- LLM interviews versus expert interviews for knowledge elicitation: AI interviews were faster and more structured, but the ontologies built from them contained 19–32% hallucinated classes. — [van den Bent et al., swj3868](https://www.semantic-web-journal.net/system/files/swj3868.pdf) (SPECULATIVE)
- On complex business SOPs (SOP-Maze: 397 instances, 3,422 subtasks), "nearly all state-of-the-art models struggle" to *follow* the procedures. — [SOP-Maze, arXiv:2510.08942](https://arxiv.org/abs/2510.08942) (execution, not authoring; not ID-checked beyond search result)
- LLMs' failure to model learners' limits (Section 4: Li et al. 2025, Acquaye et al. 2026) is itself evidence of an "expert blind spot" in LLMs. Strong problem-solvers are worse at predicting what novices find hard. — [arXiv:2512.18880](https://arxiv.org/abs/2512.18880); [arXiv:2601.09953](https://arxiv.org/abs/2601.09953) (PROMISING)

### Inferences
- What an autonomous pipeline can extract from public sources is *explicit, published* procedural knowledge: textbooks, manuals and SOPs. By definition the CTA target is what experts leave out of such sources. So public-source reconstruction should be expected to miss decision cues, heuristics and the "why" behind steps, and the expert-conversation route (Cho et al.) is a different pipeline.
- The expert–novice gap an LLM can describe is the one written about in the expertise literature, such as Chi-style deep versus surface features, not the domain-specific differences a CTA would elicit.

### Gaps
- No study was found comparing LLM-generated CTA, hierarchical task analysis or SOP outputs against expert CTA for completeness (omitted steps, decisions, cues). The oft-quoted claim that experts omit about 70% of decision steps when explaining (Clark, Feldon et al.) was not re-verified here.
- No evidence on industrial or vocational domains (pump troubleshooting and similar).

---

## 6. Provenance and claim-level attribution; contradiction detection; source quality; temporal change

### Takeaway
The machinery exists and is mature: atomic-claim decomposition, retrieval-based verification, AIS-style attribution, and PROV-O, nanopublications and micropublications for representation. Its automatic verifiers agree with humans only 72–96% of the time. LLMs are poor at surfacing contradictions between sources, adopt wrong retrieved content over their correct priors more than 60% of the time, and rate source credibility only moderately well (ρ ≈ 0.5 with experts).

### Cited Findings
- FActScore, atomic-fact precision: ChatGPT reached 58% on biographies, and the automated estimator's error was under 2%. — [Min et al. 2023 (EMNLP), arXiv:2305.14251](https://arxiv.org/abs/2305.14251) (ESTABLISHED)
- SAFE, a search-augmented factuality evaluator: it agreed with crowd annotators 72% of the time on about 16k facts, won 76% of 100 disagreements, and cost more than 20× less than humans. — [Wei et al. 2024, arXiv:2403.18802](https://arxiv.org/abs/2403.18802) (ESTABLISHED; note that "wins disagreements" was judged by the authors)
- RARR retrofits attribution by researching and revising outputs — [Gao et al. 2023 (ACL), arXiv:2210.08726](https://arxiv.org/abs/2210.08726). AIS is the "Attributable to Identified Sources" evaluation framework — [Rashkin et al. 2023 (Comput Linguist), arXiv:2112.12870](https://arxiv.org/abs/2112.12870). Both are ESTABLISHED as methods.
- Representation standards: W3C PROV-O (2013 Recommendation) — [w3.org/TR/prov-o](https://www.w3.org/TR/prov-o/); nanopublications (assertion plus provenance plus publication info) — [Groth, Gibson & Velterop 2010, doi:10.3233/ISU-2010-0613](https://doi.org/10.3233/ISU-2010-0613); micropublications (claims, evidence, arguments and challenges) — [Clark, Ciccarese & Goble 2014, J Biomed Semantics, doi:10.1186/2041-1480-5-28](https://doi.org/10.1186/2041-1480-5-28). All ESTABLISHED. The micropublication model directly represents a claim together with its supporting and challenging evidence.
- **Contradictions (unreliability signal):** WikiContradict (253 human-annotated real conflicts, 3,500+ human judgements): given two contradictory passages, "all models struggle to generate answers that accurately reflect the conflicting nature of the context," especially for implicit conflicts. — [Hou et al. 2024 (NeurIPS D&B), arXiv:2406.13805](https://arxiv.org/abs/2406.13805). ContraCrow's contradiction flags were only 70% expert-validated — [arXiv:2409.13740](https://arxiv.org/abs/2409.13740).
- **Susceptibility to bad sources (unreliability signal):** ClashEval (1,200+ questions, 6 domains): six top LLMs, GPT-4o included, adopted incorrect retrieved content, **overriding their own correct prior knowledge over 60% of the time.** — [Wu et al. 2024, arXiv:2404.10198](https://arxiv.org/abs/2404.10198) (ESTABLISHED)
- Source credibility: across 9 LLMs, ratings agreed with each other (ρ = 0.79) but only moderately with human experts (ρ = 0.50), with a systematic political-lean bias. Larger models refuse more; smaller ones err more. — [Yang & Menczer 2023, arXiv:2304.00228](https://arxiv.org/abs/2304.00228)
- STORM's editors reported source-bias transfer and improper inferential links — [arXiv:2402.14207](https://arxiv.org/abs/2402.14207). DeepTRACE found one-sidedness on debate queries — [arXiv:2509.04499](https://arxiv.org/abs/2509.04499).
- Temporal: FreshQA shows "all models (regardless of model size) struggle on questions that involve fast-changing knowledge and false premises." Search augmentation (FreshPrompt) helps. — [Vu et al. 2023, arXiv:2310.03214](https://arxiv.org/abs/2310.03214). AbstentionBench includes outdated-information questions (Section 7).

### Inferences
- Provenance *format* is a solved engineering problem: PROV-O or nanopub-style assertion, source, span, retrieval time and verifier verdict. Provenance *truth*, meaning that the span actually supports the claim, has an automatic-verifier error of roughly 4–28% depending on the tool, so a sample must be human-audited.
- A pipeline will under-report disagreement in a field. Contradiction and "contested" status should be computed separately (claim clustering plus NLI across sources) rather than left to the synthesiser.

### Gaps
- Argument-mining pipelines applied to domain-model building were not evaluated in this pass.
- No study found measuring knowledge-freshness errors specifically in technical or procedural domains, such as superseded standards.

---

## 7. Calibration and abstention: can the system say "insufficient evidence"?

### Takeaway
Not reliably. Verbalised confidence is overconfident. Strong models answer wrongly rather than abstain when retrieved context is insufficient, and reasoning-tuning makes abstention worse. Conformal factuality offers statistical guarantees (80–90%) at the cost of dropping claims, but it needs a labelled calibration set from the target distribution.

### Cited Findings
- Models "mostly know what they know" (P(IK) predicts correctness in-distribution) but "struggle with calibration of P(IK) on new tasks." — [Kadavath et al. 2022, arXiv:2207.05221](https://arxiv.org/abs/2207.05221) (ESTABLISHED)
- Verbalised confidence is overconfident, "potentially imitating human patterns." Consistency across samples mitigates this. — [Xiong et al. 2024 (ICLR), arXiv:2306.13063](https://arxiv.org/abs/2306.13063) (ESTABLISHED)
- AbstentionBench (20 datasets, 20 frontier LLMs; unknown answers, underspecification, false premises, outdated info): abstention is "an unsolved problem," scaling does little, and **reasoning fine-tuning degrades abstention by 24% on average.** — [Kirichenko et al. 2025, arXiv:2506.09038](https://arxiv.org/abs/2506.09038)
- Sufficient context in RAG: Gemini 1.5 Pro, GPT-4o and Claude 3.5 "often output incorrect answers instead of abstaining when the context is not [sufficient]." Guided abstention improved accuracy-when-answering by 2–10%. — [Joren et al. 2025 (ICLR), arXiv:2411.06037](https://arxiv.org/abs/2411.06037)
- Conformal factuality: back off claims until a guarantee holds. It gives 80–90% correctness guarantees "while retaining the majority" of output on FActScore/NQ/MATH and needs "very few human-annotated samples." — [Mohri & Hashimoto 2024 (ICML), arXiv:2402.10978](https://arxiv.org/abs/2402.10978) (PROMISING; exchangeability with calibration data is required)
- Hallucination persists because training and evaluation "reward guessing over acknowledging uncertainty." — [Kalai et al. 2025, arXiv:2509.04664](https://arxiv.org/abs/2509.04664) (theory plus argument)
- Short-form factuality benchmark adversarially collected against GPT-4. — [Wei et al. 2024 (SimpleQA), arXiv:2411.04368](https://arxiv.org/abs/2411.04368)
- Surveys: [Wen et al. 2024, arXiv:2407.18418](https://arxiv.org/abs/2407.18418)

### Inferences
- "Insufficient evidence" has to be an *architectural* output, not a model self-report: a claim with no verifying span gets status *unsupported*, whatever the model's stated confidence.
- A conformal layer is feasible, but only after someone labels a calibration set *in the target domain*. That is exactly the human input the "before asking any human" constraint wants to avoid, so the guarantee cannot be had fully autonomously.

### Gaps
- No calibration study found for domain-model-building outputs (concept/relation-level confidence).

---

## 8. Long-tail knowledge: implications for niche industrial and organisational domains

### Takeaway
Accuracy rises with how often a fact appears in pre-training data, and scaling does not close the tail. Niche industrial and organisational knowledge sits in that tail, and much of it is not public at all. Retrieval helps for tail facts but brings in the source-quality and contradiction failures of Section 6.

### Cited Findings
- There are strong correlational *and* causal relationships between QA accuracy and the count of relevant pre-training documents. — [Kandpal et al. 2023 (ICML), arXiv:2211.08411](https://arxiv.org/abs/2211.08411) (ESTABLISHED)
- PopQA (14k questions, 10 models): LMs "struggle with less popular factual knowledge," and "scaling fails to appreciably improve memorization of factual knowledge in the long tail." Adaptive retrieval helps. — [Mallen et al. 2023 (ACL), arXiv:2212.10511](https://arxiv.org/abs/2212.10511) (ESTABLISHED)
- Head-to-Tail (18K QA pairs, 16 LLMs): LLMs are "far from perfect… especially for facts of torso-to-tail entities." — [Sun et al. 2024 (NAACL), arXiv:2308.10168](https://arxiv.org/abs/2308.10168) (ESTABLISHED)
- Citation-URL failures vary by domain, from 5.4% to 11.4% non-resolving. — [Rao et al. 2026, arXiv:2604.03173](https://arxiv.org/abs/2604.03173)

### Inferences
- In "introductory thermodynamics" or intro mechanics the public corpus is huge and well covered, so reconstruction is at its best. In "centrifugal pump troubleshooting at plant X" or "onboarding a backend engineer at company Y," the decisive knowledge (site equipment quirks, internal conventions) is absent from public sources. An autonomous pipeline will either leave it out or fill it with generic content presented as specific (SPECULATIVE, but follows directly from the cited long-tail results).

### Gaps
- No benchmark found measuring LLM accuracy on vocational or industrial maintenance knowledge by popularity stratum.

---

## Implications

### What an autonomous reconstruction pipeline can do reliably now
1. **Draft a broad concept inventory and taxonomy** for well-documented academic domains such as intro thermodynamics and mechanics. Evidence: LLMs4OL taxonomy F1 of 0.68–0.78, and good lexical typing in general domains ([arXiv:2307.16648](https://arxiv.org/abs/2307.16648)). Treat it as a high-recall draft.
2. **Retrieve and cite real sources** once a URL-liveness and bibliographic-resolution filter is in place, which cuts the 3–13% fabricated URLs ([arXiv:2604.03173](https://arxiv.org/abs/2604.03173)). Restricting to a curated full-text corpus (the PaperQA2/OpenScholar pattern) gives the best measured claim support: 86% precision and 13.5% cited-and-unsupported.
3. **Assemble catalogued misconceptions** from the published literature (for physics, PER inventories) and turn them into candidate distractors ([Kieser et al. 2023](https://doi.org/10.1103/PhysRevPhysEducRes.19.020150); [Feng et al. 2024](https://arxiv.org/abs/2404.02124)).
4. **Represent provenance** at claim level with PROV-O or nanopublication/micropublication structures, and **run automatic claim verification** (FActScore/SAFE-style) as a filter, while accepting a verifier error of roughly 5–25%.

### What it cannot do reliably now
1. **Guarantee that cited claims are supported.** 20–60% unsupported statements is typical in open-web deep research ([arXiv:2509.04499](https://arxiv.org/abs/2509.04499); [arXiv:2605.06635](https://arxiv.org/abs/2605.06635); [doi:10.1038/s41467-025-58551-6](https://doi.org/10.1038/s41467-025-58551-6)), and it gets *worse* with more tool calls.
2. **Recover non-taxonomic relations**: prerequisites, causal and procedural dependencies. The best zero-shot F1 was about 0.5 in 2023, and newer evaluation uses soft metrics.
3. **Represent disagreement.** Models flatten contradictions ([arXiv:2406.13805](https://arxiv.org/abs/2406.13805)), adopt wrong sources over correct priors more than 60% of the time ([arXiv:2404.10198](https://arxiv.org/abs/2404.10198)), and produce one-sided syntheses.
4. **Know what real learners get wrong, and how often.** Distractor preferences correlate only moderately with student data, LLM errors are over-concentrated, and difficulty prediction is poorly aligned ([arXiv:2502.15140](https://arxiv.org/abs/2502.15140); [arXiv:2605.09602](https://arxiv.org/abs/2605.09602); [arXiv:2512.18880](https://arxiv.org/abs/2512.18880)).
5. **Produce CTA-grade procedural and tacit knowledge from public sources.** There is no evidence it can, and the positive evidence needs expert behaviour data ([arXiv:2608.07488](https://arxiv.org/abs/2608.07488)).
6. **Abstain reliably** when evidence is missing ([arXiv:2506.09038](https://arxiv.org/abs/2506.09038); [arXiv:2411.06037](https://arxiv.org/abs/2411.06037)).
7. **Cover niche, organisational or industrial knowledge.** This follows from the long-tail results and from that knowledge not being public.

### Evaluation design that would detect these failures
- **A held-out expert gold model per domain.** Build it independently and blind to the pipeline, by expert CTA or a published inventory/ontology, for at least one academic domain and one industrial or organisational one. Score edge-level precision/recall separately for each relation type (is-a, prerequisite, procedure-step, misconception-of), not BERTScore. Report metrics stratified by concept "popularity" (search hit count or corpus frequency) to expose long-tail decay.
- **A claim-level audit on a random sample**, not cherry-picked items. For each claim, humans judge (a) whether the source exists, (b) whether the cited span supports it (AIS-style), and (c) whether it is correct. Compare against the pipeline's own verifier to estimate the verifier's false-accept rate, and report unsupported-claim rate with confidence intervals. The Onweller et al. result means sampling has to cover runs at different research depths.
- **Planted-error and planted-contradiction tests.** Inject a known-false but plausible source (ClashEval-style) and a known real controversy (WikiContradict-style). Measure whether the model adopts the error and whether it flags the contradiction.
- **Abstention probes.** Include objectives whose required knowledge is demonstrably not public, such as a fictional plant's pump model or a private codebase convention. The correct output is "insufficient evidence." Score false-answer rate (AbstentionBench / sufficient-context logic).
- **Learner-data validation for the diagnostic layer.** Compare generated misconceptions and distractors against real response distributions, via a pretest or early quiz. Report recall of the documented catalogue, the rank correlation of predicted versus observed error frequencies, and the dispersion of simulated versus real errors (Tufino et al.'s concentration finding). For physics, use items that are *not* public, to rule out contamination.
- **An expert-omission test for CTA claims.** Have the pipeline produce a task analysis before expert interviews, then count the decision points and cues the experts add that the pipeline lacked. This directly measures the tacit-knowledge gap the pipeline cannot close from public sources.
- **Reproducibility and cost logging.** Run each domain several times, report the stability of the concept and edge sets across runs, and log tokens, $ and tool calls per run. Accuracy has to be reported jointly with depth, because more tool calls reduced accuracy.
