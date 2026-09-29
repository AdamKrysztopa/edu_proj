# 03 Novelty: adjacent work, closest prior work, and a graded novelty ledger

Author role: adjacent-work / novelty researcher. Brief: `report/notes/BRIEF.md`.
Goal: try to falsify the novelty of the chain
(1) reconstruct explicit knowledge from documents with provenance →
(2) find where that reconstruction is insufficient →
(3) use expertise methods (CTA/CDM, expert–novice, DtD, PARI) to hypothesize what is missing and its type →
(4) prioritize questions for human experts (ideally by expected information gain, EIG).

Labels used below follow the brief: ESTABLISHED LITERATURE, OBSERVED IN THE PoC, INTERPRETATION, HYPOTHESIS, FUTURE WORK.
Every cited work was checked in Crossref, OpenAlex or the arXiv API (see the verification log). Items I could not verify are marked UNVERIFIED and are not in `03_novelty.bib`.

---

## 0. Bottom line

1. **No step is new on its own.** Each of the four steps has direct prior work (ESTABLISHED LITERATURE). Step 1 is a known combination (atomic claims, attribution checks, W3C selectors). Step 4 is a known method (EIG / expected value of information for question selection), and the PoC does not implement it: gap records are ranked by a rubric score (`gapmap/src/gapmap/rank.py`, `order_key`; `record.py`, `score = A + B - P - Q`), not by EIG (OBSERVED IN THE PoC).
2. **The whole chain has close neighbours but no match found.** The closest systems either (a) guide expert interviews with an ontology or RAG context but do not first predict, from a provenance ledger, where and what type of knowledge is missing (OntoAgent, PKAI, Walther et al.), or (b) map absences in documents but never route them to experts by knowledge type (UQS, GAPMAP), or (c) simulate the organisation instead of reading real documents (Zuin et al.). INTERPRETATION.
3. **The most defensible novel element** is the use of named expertise-research constructs (CDM cues, PARI result→interpretation, selection rules, automated checks, rationale) as *absence detectors* over a provenance-typed ledger, with a predicted knowledge type and a human elicitation channel per gap, and with retrieval gaps routed to search rather than to experts. Status: potentially novel, uncertain, and **not validated**. The PoC shows its closure step is no better than a fair control (OBSERVED IN THE PoC, `research/n3/README.md`).
4. **The evaluation design is a stronger novelty candidate than the system.** I found no study that scores an LLM reconstruction or gap map against a published CTA gold standard (for example, the steps experts omitted in Sullivan et al. 2014). The E-OSS departure design adapts known turnover work (Rigby et al. 2016; Nassif & Robillard 2017). Both are HYPOTHESIS / FUTURE WORK until run.
5. **Two corrections for the report.**
   - (a) The name "GAPMAP" is already taken by a 2025 LLM paper on implicit knowledge gaps in biomedical literature (Salem et al. 2025). The report should say so and not imply the name or the "implicit gap" idea is ours.
   - (b) `REORIENTATION.md` cites van den Bent et al. as a Semantic Web Journal paper. The journal page lists it as **Rejected** (submitted 1 May 2025). Cite it only as an unpublished manuscript, or drop it.
   - (c) `REORIENTATION.md` §1 says no product computes "what documents cover versus what only experts know". Interloom's press coverage claims it checks operational records against internal documentation and measured a documented-vs-actual gap (grey source, no paper). The claim should be narrowed; see §4.

---

## 1. Closest prior work per step

Closeness scale: **High** = same task and same kind of input/output; **Medium** = same task, different input or target; **Low** = shares a component only.

### Step 1: reconstruct available explicit knowledge from documents, with provenance

| Work | What it does | Closeness | Difference from the PoC |
|---|---|---|---|
| STORM (Shao et al. 2024, NAACL) | Perspective-guided question asking over web sources to write cited, Wikipedia-like articles | High | Output is prose with citations, not an atomic-claim ledger with verbatim selectors, evidence labels and UNKNOWN slots |
| PaperQA2 (Skarlinski et al. 2024); OpenScholar (Asai et al. 2024) | Retrieval agents that write cited syntheses of scientific literature | High | Same: cited synthesis, no typed ledger; literature only |
| mimeo (Kassis 2026, preprint) | Compiles a named expert's public work into an agent file; checks every extracted quotation against cached source text (rejects 13.2%) | High (provenance mechanism) | Per-person corpus; goal is persona/knowledge transfer, not gap finding |
| FActScore (Min et al. 2023); AIS (Rashkin et al. 2023); ALCE (Gao et al. 2023); AttributionBench (Li et al. 2024); RAGAS (Es et al. 2024); FEVER (Thorne et al. 2018) | Atomic-fact decomposition, attribution to sources, claim verification, and their evaluation | High (components) | These are methods and benchmarks; the PoC composes them |
| W3C PROV-O (2013); W3C Web Annotation Data Model (2017) | Standards for provenance and for text-quote / text-position selectors | High (component) | The PoC's `Selector.exact` re-slice from a hashed snapshot is an application of the TextQuoteSelector idea |
| Audits: Liu et al. 2023; DeepTRACE (Venkit et al. 2025); SourceCheckup (Wu et al. 2025); Onweller et al. 2026; Rao et al. 2026 | Measure unsupported or unverifiable citations in generative search and deep-research agents | Medium (motivation) | They motivate span-level verification; they do not build a ledger |
| LLMs4OL (Babaei Giglou et al. 2023) | LLMs for ontology learning from text | Medium | Ontology terms and relations; no provenance per claim |

Verdict: **known combination** (ESTABLISHED LITERATURE for each part). The PoC's engineering choices (cross-family verifier, UNKNOWN only after a searched slot, independence clustering) are engineering contributions, not research novelty.

### Step 2: identify where the reconstruction is insufficient

| Work | What it does | Closeness | Difference |
|---|---|---|---|
| UQS (Ono, Yoshioka & Taketsugu 2026, ChemRxiv preprint) | LLM pipeline that turns papers into "structured absence records with evidence chains", an evidence-need dictionary and a filling-status map over later literature | High | Absences are about the *research record* (what later papers must supply), not about expert-held knowledge; one case study; expert validation left to future work |
| GAPMAP (Salem et al. 2025, arXiv) | LLMs detect explicit and *implicit* (context-inferred) knowledge gaps in biomedical papers; Toulmin-style inference (TABI) | High | Gaps are research unknowns, not knowledge experts hold but did not write; no routing to experts; **name collision with the project's `gapmap`** |
| Razniewski et al. 2024 (ACM CSUR) | Survey of completeness, recall and negation in open-world knowledge bases, including recall estimation from text | High (conceptual) | KB-level completeness of facts; no expertise typing |
| Luitel, Hassani & Sabetzadeh 2024 (Requirements Engineering) | Uses BERT masked-LM predictions to flag likely incompleteness in natural-language requirements | Medium | Lexical/term omissions in one requirements document; no expert-knowledge types |
| Feng et al. 2024 (ACL); Kadavath et al. 2022; Yin et al. 2023; Wen et al. 2025; AbstentionBench (Kirichenko et al. 2025) | Detect gaps in the *model's* knowledge; abstain | Medium | Gap is in the model, not in the document corpus relative to expert practice |
| Lakkaraju et al. 2017 (AAAI) | Find a model's "unknown unknowns" by guided, budgeted queries to an oracle | Medium (conceptually close to steps 2+4) | Classifier blind spots, not knowledge content |
| Interloom (grey: Fortune, 23 Mar 2026) | Builds a "context graph" from tickets, emails and transcripts; checked support emails against internal documentation; claims the documented-vs-actual gap fell from about 50% to 5% | High (organisational setting) | Uses behavioural trace data, not public text; no published method or evaluation; no mention of expertise methods or expert questions |
| Reporting bias: Gordon & Van Durme 2013; Paik et al. 2021; Collins & Thorne 2026 (preprint) | Text under-reports the obvious; LMs inherit it; LLMs lack access to spoken expert discourse | Medium (theory for *where* gaps are) | Explains why gaps exist; does not detect them |

Verdict: **known method** at the level of "LLM finds gaps in a corpus" (UQS, GAPMAP, Razniewski). Finding gaps *relative to expert practice* rather than relative to the research record is less covered; see step 3.

### Step 3: use expertise/learning methodology to hypothesize what is missing and its type

| Work | What it does | Closeness | Difference |
|---|---|---|---|
| OntoAgent (Jin et al. 2026, RE 2026 per arXiv journal-ref) | Builds an "experience ontology" of requirement concerns from domain descriptions and uses it to pick the next interview concern, to avoid omitting implicit requirements | High | Requirements engineering; concern ontology from analyst experience, not CTA constructs; operates *during* the interview, not as a pre-interview absence prediction with evidence status |
| Shen, Singhal & Breaux 2025 (RE 2025) | GPT-4o follow-up questions guided by a framework of interviewer mistake types; guided questions beat human-authored ones | Medium | Methodology guides *question wording*, not the prediction of missing content |
| Bridge (Wang et al. 2024, NAACL) | Uses CTA to turn expert tutors' latent decisions into a decision model that improves LLM remediation | Medium | CTA is done with humans; no document reconstruction or gap prediction |
| Cho et al. 2026 (preprint) | LLMs externalize tacit knowledge from expert behaviour (tutoring conversations); novices trained on it approach expert performance | Medium | Input is expert behaviour data, not documents; no gap map |
| Gervasi et al. 2013; Klein et al. 1989 (CDM); Chi et al. 1981; Middendorf & Pace 2004 (DtD); Sullivan et al. 2014; Chao & Salvendy 1994; Crandall & Getchell-Reiter 1993 | Taxonomies of tacit knowledge ("unknown knowns"), probes for cues and decisions, evidence that experts omit decision steps and cues | High (source constructs) | Human methods; nobody I found runs these constructs as automatic absence detectors over a document ledger |
| Data-driven KC discovery: Cen et al. 2006 (LFA); Stamper & Koedinger 2011; Koedinger et al. 2013 | Learner data reveal difficulty factors the expert model missed | Medium | Needs learner performance data; finds missing *knowledge components*, not missing expert steps in text |

Verdict: **adaptation, possibly novel in combination** (INTERPRETATION). The constructs are ESTABLISHED; using them as typed absence detectors on a provenance ledger has no match in my search. This is the element to claim, carefully.

### Step 4: prioritize questions for human experts

| Work | What it does | Closeness | Difference |
|---|---|---|---|
| BED-LLM (Choudhury et al. 2025); OPEN (Handa et al. 2024); GATE (Li et al. 2023); Uncertainty of Thoughts (Hu et al. 2024); Piriyakulkij et al. 2023 | LLM question selection by expected information gain or Bayesian optimal design | High (method) | Targets preferences, 20-questions, diagnosis; not expert knowledge elicitation over a domain model |
| Rao & Daumé 2018 (ACL) | Ranks clarification questions by neural expected value of perfect information | High (method) | Clarifying questions on StackExchange posts |
| Lindley 1956; Rainforth et al. 2024 | EIG and modern Bayesian experimental design | ESTABLISHED foundation | — |
| InfoGatherer (Taranukhin et al. 2026, preprint) | Gathers missing information from two sources, retrieved documents and targeted questions to the user, with Dempster–Shafer uncertainty over hypotheses | High (structure) | Goal is to decide a legal/medical case, not to elicit expert knowledge; the "ask a human" source is a lay client |
| Chen et al. 2018 (KDD, Learning-to-Ask); Aliannejadi et al. 2019 (SIGIR) | Learn question strategies for knowledge acquisition / clarifying questions | Medium | Crowd/user facts, not expert tacit knowledge |
| OntoChat (Zhang et al. 2025, ESWC 2024 satellite); Walther et al. 2026 (HCII, LNCS); PKAI (Schinckus et al. 2025, BISE); Data Therapist (Shin et al. 2025, preprint) | LLM-supported expert elicitation: competency questions, RAG-enriched interviews, multi-agent process-knowledge acquisition, targeted Q&A about datasets | High (task) | Questions come from requirements templates, RAG context or dataset analysis, not from a ranked, typed absence map; no EIG |

Verdict: **known method** (EIG, EVPI). FUTURE WORK in the PoC, which does not implement EIG.

---

## 2. Closest work to the whole chain (top 5)

Ranked by how many of the four steps each covers, and how directly.

1. **OntoAgent — Jin et al. 2026, "From Chat to Interview: Agentic Requirements Elicitation with an Experience Ontology" (arXiv:2605.05828; RE 2026 per journal-ref).** It covers steps 1, 3 and 4 in requirements engineering. It builds an ontology of concerns from domain requirement descriptions, scores and re-ranks concerns, and generates the next question to avoid omitting implicit requirements. **Differences:**
   - It has no evidence ledger with provenance.
   - It makes no pre-interview prediction of *where* written sources are silent.
   - Its concerns come from requirements experience, not from CTA/CDM constructs.
   - It uses no knowledge-type prediction and no separation between search gaps and expert gaps.
   - It is evaluated on interview effectiveness, not on whether predicted gaps match what experts later add.
2. **PKAI — Schinckus, Simonofski & Bono Rosselló 2025, "Large Language Models for Process Knowledge Acquisition", BISE 68:7–33.** A multi-agent system that runs the preparation, socialization and externalization stages of process discovery with LLM agents. It was evaluated with analysts, in a quasi-experiment and in a case study. **Differences:**
   - It targets process models.
   - Grounding is in knowledge-acquisition theory (SECI-style stages), not in expertise constructs.
   - I read only the abstract. I could not confirm whether the preparation stage analyses documents for gaps. Closeness is **uncertain**.
3. **Walther et al. 2026, "GenAI-Supported Expert Interviews for Knowledge Acquisition", HCII 2026, LNCS pp. 416–428.** It automates expert interviews from content preparation to follow-up. RAG enriches the interview with domain-specific prior knowledge. **Differences:**
   - As far as the abstract shows, RAG serves relevance. No explicit map of what the documents lack drives the questions.
   - No typed hypotheses and no information-gain ranking.
   - The full text was not accessible (Springer paywall redirect). Closeness is **uncertain**.
4. **Zuin, Mastelini, Loures & Veloso 2025, "Leveraging LLMs for Tacit Knowledge Discovery in Organizational Contexts", IJCNN 2025.** An LLM agent iteratively reconstructs dataset descriptions by asking employees. It decides whom to ask and what to ask. Across 864 simulations of synthetic companies it reaches 94.9% full-knowledge recall. **Differences:**
   - The organisation, the employees and the hidden knowledge are all simulated. There is no real-document reconstruction with provenance.
   - The knowledge to recover is pre-seeded, so there is no residual to predict.
   - No expertise methodology, no knowledge types.
5. **UQS — Ono, Yoshioka & Taketsugu 2026, "Mapping Structured Absences in Scientific Papers: An Auditable LLM-Assisted Workflow…" (ChemRxiv preprint).** It covers steps 1–2 with strong provenance: structured absence records with evidence chains, pre-locked filling criteria and configuration-pinned reruns. It ends in research-question briefs. **Differences:**
   - Its absences concern the published record, not expert-held knowledge.
   - There are no human-expert questions and no knowledge-type prediction.
   - It is one case study, and its authors defer expert validation.

**Runners-up.**
- InfoGatherer (documents + targeted questions + formal uncertainty; wrong target population).
- GAPMAP (implicit gaps; research unknowns).
- Co-STORM (Jiang et al. 2024, EMNLP: grounded multi-agent discourse that surfaces a *learner's* "unknown unknowns").
- Cho et al. 2026 (tacit knowledge from behaviour, not documents).
- van den Bent et al. (LLM interviews for ontology building; rejected manuscript).
- Industrial: Interloom (documented vs actual practice from tickets), eGain (claims question-mining across tickets and chats plus "structured elicitation … derived from cognitive science"; blog, 9 Apr 2025), KNOA (AI interviews that flag divergence between interviewees). None publishes a method or evaluation.

---

## 3. Graded novelty ledger

Each project element sits in exactly one category.

| # | Project element | Category | Justification |
|---|---|---|---|
| L1 | Evidence labels per claim (observed human, literature-supported, organisational-artefact-supported, inferred, synthetic, unknown) | Known method | Graded evidence status is standard (GRADE, Guyatt et al. 2008; provenance typing, PROV-O). The label set is ours; the idea is not |
| L2 | Claim ledger: atomic claims, verbatim `Selector.exact` re-sliced from a hashed snapshot, verifier from a different model family | Known combination | FActScore + AIS/ALCE attribution + W3C TextQuoteSelector. mimeo (2026) does the same quote re-check on cached sources |
| L3 | UNKNOWN written only for a searched, uncovered slot; abstention | Adaptation | Abstention and KB completeness are ESTABLISHED (Wen et al. 2025; Razniewski et al. 2024); applying them per (area × probe) slot is a small adaptation |
| L4 | Source independence clustering, contradiction handling, drift veto | Engineering contribution | Useful hygiene; no research claim |
| L5 | E-PLANT (planted-falsehood adoption) and E-ABST (abstention on private objectives) harnesses | Adaptation | Follows ClashEval-style evidence-conflict tests and abstention benchmarks. N2 closed INCONCLUSIVE (`research/n2/closeout.md`) |
| L6 | Methodology lenses: seven CTA/CDM/PARI/GOMS/KLI/causal-ambiguity constructs as absence detectors that fire when a construct is attested but its content is missing (`gapmap/src/gapmap/lenses.py`, `LENSES`) | **Potentially novel contribution (uncertain)** | No match found. Closest are OntoAgent (ontology-guided concerns), Shen et al. 2025 (mistake-type-guided follow-ups) and GAPMAP/TABI (implicit-gap inference). Uncertain because (a) search limits and paywalled 2025–26 papers, (b) the PoC closure judge equals its control. The totals are PLC 0.89 = 0.89, GDPR v1 0.96 = 0.96 and GDPR v2 0.96 = 0.96, checked in each `research/n3/*/gapmap.md` §7 table. Adversarial precision was 3/19 strict; this figure comes from `research/n3/README.md` only and was not re-tallied on the final maps. The mechanism exists; its validity is unshown |
| L7 | Predicted knowledge type per gap (cue, decision, check, rationale, interpretation; Collins's relational/somatic/collective) | Adaptation | Taxonomies are ESTABLISHED (Collins 2010; Gervasi et al. 2013; Klein et al. 1989). Attaching a predicted type to an automatically found absence is an adaptation that depends on L6 |
| L8 | Human channel per gap (CDM on a recalled case, contrasting cases, boundary vignettes, observation first) | Known method | CDM and CTA probe selection by knowledge type are ESTABLISHED (Klein et al. 1989; Gervasi et al. 2013; Burton et al. 1990) |
| L9 | Retrieval gaps (RG-UNK, RG-SINGLE, RG-UNVER, RG-SIBLING, RG-UNDECIDED) routed to *search/verify*, never to experts | Adaptation | InfoGatherer (2026) already splits "retrieve documents" vs "ask the user". Using this split to stop wasting expert time on search failures is a sensible adaptation |
| L10 | Three-tier gap records, anti-renaming check, closure null controls, cross-run stability check | Engineering contribution | Good methodological hygiene that exposed the closure failure. Not a research finding by itself |
| L11 | Ranking and question priority by EIG | Known method (FUTURE WORK) | Lindley 1956; Rao & Daumé 2018; BED-LLM. **Not implemented**: the PoC ranks by rubric score, robustness and breadth |
| L12 | "Human knowledge residual" as a measurable quantity; unseen-item estimation (Chao 1987; Chao & Jost 2012) | Adaptation | Species-richness estimators are ESTABLISHED and have been used for qualitative themes (Tran et al. 2017, per `REORIENTATION.md` [157]; not re-verified here). Naming the residual is framing, not a method |
| L13 | RQ-B: a reconstruction + gap map predicts where the human residual lies (ΔAUROC over the strongest baseline) | Research hypothesis | Untested. N3 PoC: "hidden-knowledge prediction not demonstrated" |
| L14 | E-CTA: score the gap map against published CTA gold (steps experts omitted, cues missing from training literature) | **Potentially novel contribution (evaluation design)** | No study found that scores LLM reconstruction or gap prediction against a CTA gold standard (my searches; repo note `llm_domain_reconstruction.md` agrees). Gold sets are small (n = 3–17 experts, one domain each) |
| L15 | E-OSS: developer-departure natural experiment as ground truth for predicted residual | Adaptation | Knowledge-at-risk and truck-factor work is ESTABLISHED (Rigby et al. 2016; Avelino et al. 2016, 2019; Nassif & Robillard 2017; Robillard 2021; Jabrayilzade et al. 2022). Using it to validate a text-based gap predictor is new use of known data |
| L16 | Synthetic learners/experts allowed as predictors only, never as criteria | Known method | Follows ESTABLISHED cautions: Argyle et al. 2023; Bisbee et al. 2024; Cui et al. 2025 (LLM replications give larger effects than human studies) |
| L17 | Rationale that the residual sits in obvious-to-expert steps (reporting bias + expert omission) | Known combination | Gordon & Van Durme 2013; Paik et al. 2021; Sullivan et al. 2014; Chao & Salvendy 1994; Crandall & Getchell-Reiter 1993. Combining them to predict *where* to ask is HYPOTHESIS |
| L18 | Whole chain (1→4) as one pipeline, domain-neutral, with evidence status carried end to end | **Potentially novel contribution (uncertain)** | No single system found that does all four with expertise-typed absence prediction. Neighbours (§2) each miss at least two parts. Uncertain because industrial products (Interloom, eGain, KNOA) do not publish methods, and 2026 preprints appear monthly |

---

## 4. Recommended novelty statement (for the report)

> Each part of our pipeline has precedent. LLM systems already write cited syntheses from documents, verify claims against sources, detect gaps in literature, and choose questions by expected information gain. LLM interview agents already help experts externalize knowledge. What we did not find is one method that does all of this in order. It builds a provenance-typed ledger of what public sources state, then uses constructs from cognitive task analysis and expertise research as detectors for what those sources leave unsaid. It labels each suspected gap with a likely knowledge type and a suitable human elicitation method, and it sends search failures back to search instead of to experts. We present this combination as a proof of concept, not as a validated method. In our two demonstration domains, the step that decides whether content is truly absent did no better than a control. Whether the gap map predicts what experts would add is an open hypothesis. We have designed tests for it against published cognitive-task-analysis results and against developer departures in open-source projects. Our search covered peer-reviewed venues, arXiv and public product material up to September 2026. Commercial tools that do not publish their methods may overlap with parts of this design.

Plain rule for the report: say "combination we did not find in prior work", never "first" or "novel method"; never "identifies tacit knowledge"; say "flags candidate gaps".

Narrowed replacement for `REORIENTATION.md` §1's product claim: "We found no product or paper that, before asking anyone, predicts from written evidence where expert-only knowledge is likely to be and of what type, and publishes an evaluation of that prediction. One product reports comparing operational records with documentation (Interloom, press source)."

---

## 5. Limits of this search

- Sources: Crossref API, OpenAlex API/MCP (keyword and semantic), arXiv API (title/abstract field queries), web search, publisher and product pages. English only. No Scopus/Web of Science. No patents beyond incidental hits.
- The full text of Walther et al. 2026 and Schinckus et al. 2025 was not read (Springer redirect). Their closeness is judged from abstracts.
- Products (Interloom, eGain, KNOA, Glean) are described from press or vendor pages. Their claims are unverified. Absence of a published method is not absence of the method.
- 2026 preprints (OntoAgent, InfoGatherer, UQS, mimeo, Cho et al.) are not peer reviewed, except that OntoAgent lists RE 2026 as its venue.
- The search found no EIG-for-CTA work and no LLM-vs-CTA-gold comparison. This is weak evidence of absence.
- Collisions and status issues worth fixing elsewhere in the repo: the GAPMAP name; the van den Bent status; the Interloom claim.

---

## 6. Verification log (one line per .bib key)

- `shao2024assisting`: Crossref DOI 10.18653/v1/2024.naacl-long.347 resolves (NAACL 2024, pp. 6252–6278); arXiv 2402.14207 abstract read.
- `jiang2024unknown`: Crossref DOI 10.18653/v1/2024.emnlp-main.554 (EMNLP 2024, pp. 9917–9955); OpenAlex W4404782796; abstract read.
- `skarlinski2024language`: arXiv 2409.13740 via arXiv API; abstract read.
- `asai2024openscholar`: arXiv 2411.14199 via arXiv API; abstract read. (A Nature version is listed in `REORIENTATION.md` [40]; not re-verified, so not used.)
- `kassis2026mimeo`: arXiv 2609.00453 via arXiv API; abstract read (13.2% quotation rejection).
- `min2023factscore`: Crossref DOI 10.18653/v1/2023.emnlp-main.741.
- `rashkin2023measuring`: Crossref DOI 10.1162/coli_a_00486 (CL 49:777–840).
- `gao2023enabling`: Crossref DOI 10.18653/v1/2023.emnlp-main.398 (ALCE).
- `li2024attributionbench`: Crossref DOI 10.18653/v1/2024.findings-acl.886.
- `es2024ragas`: Crossref DOI 10.18653/v1/2024.eacl-demo.16.
- `thorne2018fever`: Crossref DOI 10.18653/v1/N18-1074.
- `lebo2013provo`: W3C page fetched; W3C Recommendation, 30 April 2013; editors Lebo, Sahoo, McGuinness.
- `sanderson2017web`: W3C page fetched; W3C Recommendation, 23 February 2017; defines TextQuoteSelector and TextPositionSelector.
- `guyatt2008grade`: Crossref DOI 10.1136/bmj.39489.470347.ad (BMJ 336:924–926).
- `liu2023evaluating`: Crossref DOI 10.18653/v1/2023.findings-emnlp.467.
- `venkit2025deeptrace`: arXiv 2509.04499 via arXiv API; abstract read.
- `wu2025automated`: Crossref DOI 10.1038/s41467-025-58551-6 (Nat Commun 16; SourceCheckup).
- `onweller2026cited`: arXiv 2605.06635 via arXiv API; abstract read.
- `rao2026detecting`: arXiv 2604.03173 via arXiv API; abstract read.
- `babaeigiglou2023llms4ol`: arXiv 2307.16648 via arXiv API (ISWC 2023 per comment).
- `ono2026mapping`: OpenAlex W7204537243, DOI 10.26434/chemrxiv.15007996/v1; abstract read via OpenAlex (publisher page 403).
- `salem2025gapmap`: arXiv 2510.25055 via arXiv API; abstract read; a NeurIPS 2025 virtual page exists (track not verified, so cited as arXiv).
- `razniewski2024completeness`: Crossref DOI 10.1145/3639563 (ACM CSUR 56(6), pp. 1–42).
- `luitel2024improving`: Crossref DOI 10.1007/s00766-024-00416-3 (Req. Eng. 29:73–95).
- `feng2024dont`: Crossref DOI 10.18653/v1/2024.acl-long.786.
- `kadavath2022language`: arXiv 2207.05221 via arXiv API; OpenAlex W4285429195.
- `yin2023large`: Crossref DOI 10.18653/v1/2023.findings-acl.551.
- `wen2025know`: Crossref DOI 10.1162/tacl_a_00754 (TACL 13:529–556).
- `kirichenko2025abstentionbench`: arXiv 2506.09038 via arXiv API.
- `wu2024clasheval`: arXiv 2404.10198 via arXiv API.
- `lakkaraju2017identifying`: Crossref DOI 10.1609/aaai.v31i1.10821; abstract read.
- `gordon2013reporting`: Crossref DOI 10.1145/2509558.2509563 (AKBC 2013, pp. 25–30).
- `paik2021world`: Crossref DOI 10.18653/v1/2021.emnlp-main.63.
- `collins2026large`: arXiv 2603.23543 via arXiv API; abstract read.
- `jin2026chat`: arXiv 2605.05828 via arXiv API; journal-ref "RE 2026"; abstract read.
- `shen2025requirements`: arXiv 2507.02858 via arXiv API; comment "accepted at the 33rd IEEE RE 2025"; abstract read.
- `wang2024bridging`: Crossref DOI 10.18653/v1/2024.naacl-long.120; abstract read.
- `cho2026large`: arXiv 2608.07488 via arXiv API; abstract read.
- `shin2025data`: arXiv 2505.00455 via arXiv API; abstract read.
- `zhang2025ontochat`: Crossref DOI 10.1007/978-3-031-78952-6_10 (LNCS, ESWC 2024 Satellite Events, pp. 102–121); arXiv 2403.05921 abstract read.
- `walther2026genai`: Crossref DOI 10.1007/978-3-032-29178-3_28 (LNCS, pp. 416–428); OpenAlex W7167599692; abstract only via search snippet, full text not read.
- `schinckus2025large`: Crossref DOI 10.1007/s12599-025-00976-w (BISE 68:7–33); abstract read via OpenAlex W4417319448.
- `zuin2025leveraging`: Crossref DOI 10.1109/ijcnn64981.2025.11227259; arXiv 2507.03811 abstract read.
- `vandenbent2025investigating`: Semantic Web Journal submission page fetched; status "Rejected", submitted 1 May 2025; authors van den Bent, Pernisch, Schlobach. Real manuscript, not a publication.
- `taranukhin2026infogatherer`: arXiv 2603.05909 via arXiv API; abstract read ("Under review").
- `benderoth2025socially`: arXiv 2508.19942 via arXiv API; abstract read.
- `allen2023knowledge`: arXiv 2310.00637 via arXiv API.
- `allen2026elenchus`: arXiv 2603.06974 abstract page fetched (single author Bradley P. Allen, 7 Mar 2026).
- `leu2016multi`: Crossref DOI 10.1016/j.knosys.2016.02.012 (KBS 105:1–22).
- `choudhury2025bedllm`: arXiv 2508.21184 via arXiv API.
- `handa2024bayesian`: arXiv 2403.05534 via arXiv API.
- `li2023eliciting`: arXiv 2310.11589 via arXiv API; OpenAlex W4387800384.
- `hu2024uncertainty`: Crossref DOI 10.52202/079017-0762 (NeurIPS 37, pp. 24181–24215).
- `piriyakulkij2023active`: arXiv 2312.12009 via arXiv API.
- `rao2018learning`: Crossref DOI 10.18653/v1/P18-1255 (ACL 2018, pp. 2737–2746).
- `aliannejadi2019asking`: Crossref DOI 10.1145/3331184.3331265.
- `chen2018learning`: Crossref DOI 10.1145/3219819.3220047 (KDD 2018, pp. 1216–1225).
- `lindley1956measure`: Crossref DOI 10.1214/aoms/1177728069.
- `rainforth2024modern`: Crossref DOI 10.1214/23-sts915 (Stat Sci 39).
- `klein1989critical`: Crossref DOI 10.1109/21.31053 (IEEE TSMC 19:462–472).
- `gervasi2013unpacking`: Crossref DOI 10.1007/978-3-642-34419-0_2.
- `burton1990efficacy`: Crossref DOI 10.1016/s1042-8143(05)80010-x.
- `middendorf2004decoding`: Crossref DOI 10.1002/tl.142.
- `chi1981categorization`: Crossref DOI 10.1207/s15516709cog0502_2.
- `sullivan2014use`: Crossref DOI 10.1097/ACM.0000000000000224 (Acad Med 89(5):811–816).
- `chao1994percentage`: Crossref DOI 10.1080/10447319409526093 (IJHCI 6(3):221–233).
- `crandall1993critical`: Crossref DOI 10.1097/00012272-199309000-00006 (Adv Nurs Sci 16(1):42–51; Crossref title "Critical decision method").
- `collins2010tacit`: Crossref DOI 10.7208/chicago/9780226113821.001.0001 (University of Chicago Press, 2010).
- `forsythe1993engineering`: Crossref DOI 10.1177/0306312793023003002.
- `cen2006learning`: Crossref DOI 10.1007/11774303_17.
- `stamper2011human`: Crossref DOI 10.1007/978-3-642-21869-9_46.
- `koedinger2013new`: Crossref DOI 10.1609/aimag.v34i3.2484.
- `chao1987estimating`: Crossref DOI 10.2307/2531532.
- `chao2012coverage`: Crossref DOI 10.1890/11-1952.1.
- `avelino2016novel`: Crossref DOI 10.1109/icpc.2016.7503718.
- `avelino2019abandonment`: Crossref DOI 10.1109/esem.2019.8870181.
- `rigby2016quantifying`: Crossref DOI 10.1145/2884781.2884851.
- `nassif2017revisiting`: Crossref DOI 10.1109/icsme.2017.64.
- `robillard2021turnover`: Crossref DOI 10.1145/3468264.3473923.
- `jabrayilzade2022bus`: Crossref DOI 10.1109/icse-seip55303.2022.9793985.
- `argyle2023out`: Crossref DOI 10.1017/pan.2023.2.
- `bisbee2024synthetic`: Crossref DOI 10.1017/pan.2024.5.
- `cui2025large`: Crossref DOI 10.1038/s43588-025-00840-7 (Nat Comput Sci 5:627–634). The "larger effect sizes" claim comes from the PubMed/Nature abstract via search; publisher page redirected.
- `watanabe2026can`: arXiv 2605.22971 via arXiv API; abstract read (LLM expertise estimation from Slack logs; expertise-locator analogue).

Not in .bib (grey or unverified):
- Interloom (Fortune 23 Mar 2026, fetched).
- eGain blog (9 Apr 2025, fetched).
- KNOA product page (fetched).
- AHFE 2025 review "LLMs for Tacit Knowledge Elicitation in Industry 5.0" (found, venue page not checked).
- "Collaborative Construction of Domain Ontologies Supported by Evidence-Grounded LLMs" (OpenAlex W7162422579, no abstract; content unknown).
- Tran et al. 2017 (not re-verified here).
