# Mature representations of domain knowledge and expertise (beyond knowledge graphs)

Verification note (2026-09-28): every DOI below was resolved against OpenAlex in this session and matched the cited title, authors and year, unless marked "identifier not verified". Fetched and read this session: Liu & Koedinger 2017 (full text), Mislevy & Riconscente ECD layers paper (full text), KCluster abstract, RDF 1.2 status pages, ESCO/competency-framework pages. For the other works, the content claims come from well-known summaries of those papers. The identifiers were checked, but the full texts were not re-read, so a citation-verifier pass is still needed before these claims go into `research/`. Tags: ESTABLISHED (replicated or standard, widely used), PROMISING (some empirical support, limited replication), SPECULATIVE (argument or inference only).

## 1. Learning-science models: what they already represent

### Takeaway
Learning science already has well-developed formal units for the performance side of expertise. KLI knowledge components carry explicit application conditions. ACT-R productions and constraint-based models encode "when to apply" and "when a solution is wrong". Bug libraries and malrules encode failure modes. Q-matrix/CDM and Knowledge Space Theory encode prerequisites and diagnosis. LFA/DataShop gives a validation route that needs no participants. The concepts are not missing. What is missing is shared glue between these models, plus a way to represent misconceptions that does not treat them as fixed, stable units.

### Cited Findings
- **KLI framework.** A knowledge component (KC) is an acquired unit of cognitive function or structure that is inferred from performance on a set of related tasks. KCs are classified by whether their application conditions and responses are constant or variable, whether they are verbal or non-verbal, and whether they come with a rationale. Three families of learning process (memory and fluency; induction and refinement; understanding and sense-making) are linked to instructional principles. ESTABLISHED. [Koedinger, Corbett & Perfetti 2012, Cognitive Science](https://doi.org/10.1111/j.1551-6709.2012.01245.x)
- **KCs have a built-in "condition" part.** A KC is written as a condition-response pair, so "when (not) to apply" is part of the unit rather than an extra attached later. ESTABLISHED. [Koedinger et al. 2012](https://doi.org/10.1111/j.1551-6709.2012.01245.x)
- **Cognitive Tutors (ACT-R).** Skill is represented as if-then production rules. "Model tracing" matches each student step against correct and buggy productions to give step-level feedback. The tutor lessons were drawn from about a decade of deployments. ESTABLISHED. [Anderson, Corbett, Koedinger & Pelletier 1995, JLS](https://doi.org/10.1207/s15327809jls0402_2)
- **Bayesian Knowledge Tracing.** BKT estimates per-KC mastery from four parameters: initial knowledge, learning rate, guess and slip. It is the standard learner layer over a KC model. ESTABLISHED. [Corbett & Anderson 1995, UMUAI](https://doi.org/10.1007/bf01099821)
- **Constraint-based modelling.** CBM represents domain knowledge as constraints, each a pair of a *relevance condition* and a *satisfaction condition*. A solution is wrong when a relevant constraint is not satisfied. CBM does not model the problem-solving process, which makes it cheaper to author than production-rule tutors. ESTABLISHED. [Ohlsson 1994](https://doi.org/10.1007/978-3-662-03037-0_7); [Mitrovic & Ohlsson 1999, IJAIED](https://openalex.org/W2156086800); [Mitrovic 2012, "Fifteen years of constraint-based tutors", UMUAI](https://doi.org/10.1007/s11257-011-9105-9)
- **Bug libraries.** BUGGY represented subtraction errors as perturbed ("buggy") versions of the correct procedure, which allowed a student's systematic errors to be diagnosed. ESTABLISHED. [Brown & Burton 1978, Cognitive Science](https://doi.org/10.1016/s0364-0213(78)80004-4)
- **Repair theory.** Bugs are generated rather than just listed. A learner reaches an *impasse* when the known procedure does not apply and applies a local *repair*. This is a generative model of failure modes. ESTABLISHED (for procedural arithmetic). [Brown & VanLehn 1980, Cognitive Science](https://doi.org/10.1016/s0364-0213(80)80010-3); [VanLehn 1990, *Mind Bugs*](https://openalex.org/W1564397683)
- **Rule space.** This was the first psychometric treatment of misconceptions as diagnosable states, using item response theory to classify examinees into "bug" or knowledge states. ESTABLISHED. [Tatsuoka 1983, JEM](https://doi.org/10.1111/j.1745-3984.1983.tb00212.x)
- **Q-matrix and CDMs.** A Q-matrix maps items to the attributes they need. DINA models conjunctive attribute requirements with item-level slip and guess. G-DINA generalises DINA, DINO and additive models. The Q-matrix can be checked against data empirically. ESTABLISHED. [Junker & Sijtsma 2001, APM](https://doi.org/10.1177/01466210122032064); [de la Torre 2011, Psychometrika](https://doi.org/10.1007/s11336-011-9207-7); [de la Torre & Chiu 2016, Psychometrika](https://doi.org/10.1007/s11336-015-9467-8)
- **Knowledge Space Theory.** A domain is a set of items. A learner's *knowledge state* is the subset of items they have mastered, and a *knowledge space* is the family of feasible states, closed under union. Prerequisites appear as surmise relations, and the "outer fringe" of a state says what the learner is ready to learn next. The later "learning space" axioms underpin ALEKS. ESTABLISHED. [Doignon & Falmagne 1985, IJMMS](https://doi.org/10.1016/s0020-7373(85)80031-6)
- **CDMs and KST are formally linked.** Competence-based KST and CDMs are shown to be two notations for closely related structures, so one representation can serve both communities. ESTABLISHED. [Heller, Stefanutti, Anselmi & Robusto 2015, Psychometrika](https://doi.org/10.1007/s11336-015-9457-x)
- **Learning progressions.** These are ordered levels of increasingly sophisticated understanding. The levels explicitly include intermediate, partly incorrect ideas. The force-and-motion progression was assessed with ordered multiple-choice items whose options map to levels, which is directly relevant to physics. ESTABLISHED as a construct; the empirical ordering is only PROMISING. [Corcoran, Mosher & Rogat 2009, CPRE report](https://doi.org/10.1037/e557172009-001); [Alonzo & Steedle 2009, Science Education](https://doi.org/10.1002/sce.20303)
- **Misconception inventories.** The Force Concept Inventory builds its distractors from a taxonomy of non-Newtonian common-sense beliefs, so each wrong answer carries diagnostic meaning. ESTABLISHED. [Hestenes, Wells & Swackhamer 1992, The Physics Teacher](https://doi.org/10.1119/1.2343497)
- **Critique: misconceptions are not stable units.** The "misconceptions" view is challenged by the knowledge-in-pieces argument. Novice ideas are context-sensitive, productive resources that get refined, not stable wrong beliefs to be replaced. ESTABLISHED as a live theoretical dispute. [Smith, diSessa & Roschelle 1994, JLS](https://doi.org/10.1207/s15327809jls0302_1)
- **Expert–novice differences.** Experts sort physics problems by deep principle (for example, conservation of energy), while novices sort by surface features (for example, inclined planes). This is the classic evidence that expert knowledge is organised by principle and applicability. ESTABLISHED. [Chi, Feltovich & Glaser 1981, Cognitive Science](https://doi.org/10.1207/s15516709cog0502_2)
- **Learning Factors Analysis.** LFA searches combinatorially over hypothesised difficulty factors to split or merge KCs, scores each KC model by fit to a learning-curve model (the Additive Factors Model), and returns the best model in symbolic form. ESTABLISHED. [Cen, Koedinger & Junker 2006](https://doi.org/10.1007/11774303_17)
- **DataShop.** Human-machine KC model refinement works from public learning-curve visualisations and gave significantly better prediction on a Geometry dataset (DataShop #76). ESTABLISHED. [Stamper & Koedinger 2011](https://doi.org/10.1007/978-3-642-21869-9_46)
- **Automated KC models beat human ones across many datasets.** Applied to 11 public DataShop datasets across several domains, LFA improved KC-model fit beyond the best human-generated model in every one. ESTABLISHED (as reported by the originating group). [Liu & Koedinger 2017, JEDM](https://jedm.educationaldatamining.org/index.php/JEDM/article/view/212), citing Koedinger et al. 2012
- **Closing the loop, with numbers.** An LFA-discovered KC split in Geometry (a hidden "backward area" difficulty) was confirmed on a new dataset (72,404 problem steps), using AIC, BIC and item- and student-stratified 10-fold CV RMSE. It was then used to redesign the tutor. In the classroom RCT, 115 students were randomised (57 control, 58 redesign) and 91 completed. Post-test was higher for the redesign, F(1,89)=5.04, p=0.027, Cohen's d=0.47, and the effect held after controlling for pre-test. ESTABLISHED (single study). [Liu & Koedinger 2017, JEDM](https://files.eric.ed.gov/fulltext/EJ1155896.pdf); related: [Koedinger, Stamper, McLaughlin & Nixon 2013, AIED](https://doi.org/10.1007/978-3-642-39112-5_43)
- **LLM-discovered KC models.** KCluster clusters items using LLM-generated similarity to discover KC models. The authors report that the models predict student performance better than the best expert-designed KC models on three datasets. PROMISING: one group, a conference paper, and effect sizes not checked this session. [Wei, Carvalho & Stamper 2025, EDM 2025 (arXiv:2505.06469)](https://arxiv.org/abs/2505.06469)

### Inferences
- KLI plus a Q-matrix is the natural core unit for "what an expert knows that a learner lacks". A KC's condition side is where tacit "conditions of applicability" should go, so the project does not need its own "applicability" construct. SPECULATIVE (design inference).
- Physics principle selection, which is what K0 counts, is exactly the "variable condition, variable response" KC class in KLI. Chi et al. is the empirical anchor for it. SPECULATIVE.
- Constraints (relevance → satisfaction) are the cleanest existing formalism for "when NOT to apply a rule". For example, "if external impulse is non-negligible during the interval, then momentum conservation must not be applied". SPECULATIVE (mapping).
- LFA/AFM on public DataShop data gives a zero-participant check. If expert-elicited operations are coded as KCs and tagged onto the steps of an existing public physics dataset, one can test whether the expert-derived KC model fits learning curves better than the dataset's default KC model. This is PROMISING because the method is established. Whether a suitable public physics dataset with step-level data exists was not verified this session.
- Misconceptions should be stored as *hypotheses with evidence and confidence*, not as fixed entities. That keeps the representation neutral between the misconception view and the knowledge-in-pieces view. SPECULATIVE.

### Gaps
- Whether DataShop currently hosts physics datasets (for example, from the Andes tutor) with KC-labelled steps that suit an LFA comparison was not checked.
- KCluster's actual fit metrics and its dataset domains were not read.
- No source was found that combines bug libraries with KC models into one shared standard format.

## 2. Assessment design: Evidence-Centered Design as the claim→evidence→task bridge

### Takeaway
ECD is the most mature framework for "what competent performance looks like → observable evidence → diagnostic tasks". Its design-pattern attributes line up almost one-to-one with the project's needs. "Additional KSAs" formalise alternative explanations for a failure, which the project needs for bottleneck diagnosis. ESTABLISHED.

### Cited Findings
- **ECD's core structure.** ECD structures an assessment as an evidentiary argument, with three linked models in its Conceptual Assessment Framework. The *student model* holds what we want to claim. The *evidence model* holds evidence rules plus a measurement model that update the student model. The *task model* holds the situations that elicit evidence. ESTABLISHED. [Mislevy, Steinberg & Almond 2003, Measurement](https://doi.org/10.1207/s15366359mea0101_02); [Mislevy & Haertel 2006, EM:IP](https://doi.org/10.1111/j.1745-3992.2006.00075.x)
- **Layered design.** ECD is organised in layers, starting with *Domain Analysis* and then *Domain Modeling*, before the CAF, implementation and delivery. Domain Analysis gathers substantive information, including "cognitive analyses of how people use their knowledge". Domain Modeling casts it as assessment arguments built on Toulmin's claim–data–warrant structure, with multiple data sources and warrants. ESTABLISHED. [Mislevy & Riconscente 2005, "Evidence-Centered Assessment Design: Layers, Structures, and Terminology", PADI/SRI](https://padi.sri.com/downloads/aera/2005/symposium2/papers/MislevyRicLayers.pdf)
- **Design-pattern attributes.** The paper names these slots: *Rationale*, which gives the underlying warrant; *Focal KSAs*, the primary target; *Additional KSAs*, other knowledge a task demands that "draw our attention to explanations for poor responses"; *Potential Work Products*, what students say, do or make; *Potential Observations*, the qualities of work products that carry evidence; *Characteristic Features*, which must be present to evoke evidence about the focal KSA; and *Variable Features*, which change difficulty and the degree of confounding. ESTABLISHED. [Mislevy & Riconscente 2005](https://padi.sri.com/downloads/aera/2005/symposium2/papers/MislevyRicLayers.pdf)
- **Design patterns are deliberately informal.** They are broad, narrative and non-technical, centred on one KSA, and allow many task designs. A template series then forces the student, evidence and task models to be made explicit. ESTABLISHED. [ETS/ERIC design patterns paper](https://files.eric.ed.gov/fulltext/EJ1111295.pdf); [ETS 2012 ECD+UDL paper](https://www.ets.org/Media/Research/pdf/session1-cameto-cheng-haertel-paper-tea2012.pdf)
- **ECD in physics.** ECD has been applied to paper-based physics assessments of scientific practices. PROMISING (not read in full). [arXiv:2106.13028](https://arxiv.org/pdf/2106.13028)

### Inferences
- ECD Domain Analysis is the formal slot for CTA output, and Domain Modeling design patterns are the slot for "expert operation → diagnostic task". Using ECD vocabulary for the diagnostic layer instead of inventing one is justified. SPECULATIVE (design recommendation, strongly supported by fit).
- "Additional KSAs" are the ECD name for construct-irrelevant or alternative causes of an error. A "bottleneck hypothesis" is then a focal KSA claimed to be missing, contrasted with named additional KSAs that could also explain the same observation. ECD gives the slots but no standard for ranking such competing hypotheses. SPECULATIVE.
- "Variable features" give the principled way to generate item families, for example with an LLM, while holding the focal KC constant. SPECULATIVE.

### Gaps
- A Bayesian-network implementation of ECD (Almond et al. 2015, *Bayesian Networks in Educational Assessment*, Springer) was not verified this session; the identifier is not verified.
- No machine-readable, widely adopted serialisation of ECD design patterns was found. PADI had an object model, but its current maintenance status is unknown.

## 3. Instructional design built on CTA: 4C/ID and component display theory

### Takeaway
4C/ID already separates the two kinds of expert knowledge the project cares about. *Supportive information* covers mental models and systematic approaches to problem solving (SAPs, meaning phases plus heuristics) for non-recurrent skills. *Procedural information* covers rules and just-in-time how-to for recurrent skills. It also has a skill hierarchy and explicit analysis of intuitive strategies, typical errors and misconceptions. ESTABLISHED.

### Cited Findings
- **The four components.** 4C/ID prescribes (1) whole learning tasks, (2) supportive information, (3) procedural information and (4) part-task practice. It distinguishes non-recurrent constituent skills, which vary across problems and need schema construction, from recurrent ones, which stay consistent and need rule automation. It organises them into a skill hierarchy. ESTABLISHED. [van Merriënboer, Clark & de Croock 2002, ETR&D](https://doi.org/10.1007/bf02504993)
- **Content of supportive and procedural information.** Supportive information contains mental models (conceptual, causal and structural domain knowledge) and cognitive strategies, expressed as SAPs: phases, goals and rules of thumb. Procedural information contains how-to rules plus their prerequisite knowledge. ESTABLISHED. [van Merriënboer et al. 2002](https://doi.org/10.1007/bf02504993)
- **Error and intuition analysis steps in the Ten Steps.** The "Ten Steps" operationalisation adds explicit analysis steps for *intuitive* cognitive strategies and mental models, and for typical errors, malrules and misconceptions tied to rules and prerequisite knowledge. ESTABLISHED in the ID literature. Source: van Merriënboer & Kirschner, *Ten Steps to Complex Learning* (Routledge; 3rd ed. 2018); identifier not verified, content from the book's standard summary.
- **Component Display Theory.** CDT crosses content types (fact, concept, procedure, principle) with performance levels (remember, use, find). ESTABLISHED as a classic taxonomy. Source: Merrill 1983, "Component Display Theory", in Reigeluth (ed.), *Instructional-Design Theories and Models*; identifier not verified (OpenAlex match only to a secondary comparison, [Twitchell 1990](https://openalex.org/W99204744)).

### Inferences
- 4C/ID's supportive/procedural split and recurrent/non-recurrent split give the project a ready-made typing for "strategies/heuristics" (SAPs) versus "procedures" (rules). SAPs are the only mainstream ID construct that holds expert heuristics as ordered phases with rules of thumb. SPECULATIVE (mapping).
- CDT's "find" level (generating new concepts or procedures) roughly corresponds to KLI's variable-condition KCs. It is not needed as a separate layer. SPECULATIVE.

### Gaps
- No machine-readable 4C/ID schema or standard was found. 4C/ID is a design method, not a data format.

## 4. Cognitive engineering representations: decisions, cues, goals, troubleshooting

### Takeaway
Cognitive engineering has the most mature representations of *decisions, cues, expectancies, goals and common errors*, which are the tacit side of expertise. The CDM/ACTA decision-requirements or cognitive-demands table is the de-facto standard. GOMS "selection rules" and HTA "plans" formalise conditions for choosing a method. The CWA abstraction hierarchy formalises means–ends and causal structure, and PARI formalises troubleshooting. None of them is a learner model.

### Cited Findings
- **Critical Decision Method.** CDM elicits non-routine incidents through multiple retrospective sweeps. Probes cover cues, knowledge, goals, options, the basis for a choice, analogues and hypotheticals, all aimed at decision points. ESTABLISHED. [Klein, Calderwood & MacGregor 1989, IEEE SMC](https://doi.org/10.1109/21.31053); [Hoffman, Crandall & Shadbolt 1998, Human Factors](https://doi.org/10.1518/001872098779480442)
- **ACTA.** ACTA's knowledge audit probes past and future, big picture, noticing, job smarts, improvising, self-monitoring and anomalies. Its output *cognitive demands table* has four columns: difficult cognitive element, why it is difficult, common errors, and cues and strategies used. ESTABLISHED. [Militello & Hutton 1998, Ergonomics](https://doi.org/10.1080/001401398186108)
- **Practitioner synthesis.** *Working Minds* summarises CDM and related methods and the decision-requirements table as the standard output. ESTABLISHED. [Crandall, Klein & Hoffman 2006, *Working Minds*](https://openalex.org/W1664374833)
- **HTA.** HTA decomposes goals into subgoals and uses *plans* to state the conditions and ordering under which subgoals are carried out. ESTABLISHED. [Stanton 2006, Applied Ergonomics](https://doi.org/10.1016/j.apergo.2005.06.003)
- **GOMS.** GOMS represents skilled procedural knowledge as Goals, Operators, Methods and *Selection rules*. A selection rule chooses between methods by context, which formalises conditional method choice. The Keystroke-Level Model gives quantitative time predictions. ESTABLISHED. [John & Kieras 1996, ACM TOCHI](https://doi.org/10.1145/235833.236054); [Card, Moran & Newell 1980, CACM](https://doi.org/10.1145/358886.358895)
- **Cognitive Work Analysis.** CWA covers work domain analysis via Rasmussen's abstraction hierarchy (functional purpose → abstract function, such as mass and energy balances → generalised function → physical function → physical form), then control-task, strategies, social-organisation and worker-competency (skills-rules-knowledge) analyses. ESTABLISHED. [Vicente 1999, *Cognitive Work Analysis*](https://openalex.org/W1550840327). Rasmussen 1985 original: identifier not verified; the DOI tried resolved to an unrelated paper.
- **PARI.** PARI structures troubleshooting knowledge as Precursor (why this action), Action, Result and Interpretation (what the result means for the fault hypothesis). It was developed for Air Force avionics troubleshooting. ESTABLISHED. [Hall, Gott & Pokorny 1995, AFHRL report](https://doi.org/10.21236/ada303654)
- **Goal-Directed Task Analysis.** GDTA builds goal → subgoal → decision (phrased as a question) → situation-awareness requirements at three levels: perception, comprehension and projection. ESTABLISHED in human factors. Source: Endsley, Bolté & Jones 2003, *Designing for Situation Awareness* (Taylor & Francis); identifier not verified (OpenAlex holds only a [book review](https://doi.org/10.1177/106480460401200310)).

### Inferences
- The ACTA/CDM table is already the right row format for "decisions + cues + strategies + common errors". The project's elicitation output should emit these columns rather than a new schema. SPECULATIVE (design recommendation).
- The abstraction hierarchy fits physics unusually well. Its "abstract function" level is literally conservation laws and balances, which is the principle-selection layer K0 targets. SPECULATIVE.
- PARI's Interpretation step, which updates the fault hypothesis, is the same structure as the tutor's diagnosis loop (observation → updated bottleneck hypothesis). Fault trees and FMEA are the engineering counterparts for failure modes. SPECULATIVE; FMEA/FTA standards were not checked this session.

### Gaps
- No standard machine-readable format for CDM/ACTA tables was found. They are tables in reports.
- No study was found that links CDM-derived cues directly to KC models or Q-matrices. This is a genuine integration gap.

## 5. Knowledge engineering: problem-solving methods, ontologies, terminology, competency frameworks

### Takeaway
CommonKADS and Chandrasekaran's generic tasks provide reusable *inference structures* for diagnosis, assessment and design, which is exactly the shape of the project's diagnose→instruct loop. SKOS covers terminology. Ontology design patterns cover modelling idioms. Occupational competency frameworks (O*NET, ESCO, SFIA) are descriptive label systems and are too coarse to act as an expertise model.

### Cited Findings
- **CommonKADS.** CommonKADS separates the knowledge model into domain knowledge, inference knowledge and task knowledge. It provides task templates (for example diagnosis, assessment and design) with reusable inference structures built from primitive inferences such as cover, select, predict and compare. ESTABLISHED. [Schreiber et al. 1994, IEEE Expert](https://doi.org/10.1109/64.363263)
- **Generic tasks.** Knowledge-based reasoning is decomposed into generic tasks such as hierarchical classification, hypothesis matching, knowledge-directed data retrieval and abductive assembly. Each comes with its own knowledge form and control regime. ESTABLISHED. [Chandrasekaran 1986, IEEE Expert](https://doi.org/10.1109/mex.1986.4306977)
- **SKOS.** SKOS is a W3C Recommendation (2009) for concept schemes, with preferred, alternative and hidden labels, broader, narrower and related relations, and cross-scheme mapping such as exactMatch and closeMatch. ESTABLISHED. [Miles & Bechhofer 2009, SKOS Reference](https://www.w3.org/TR/skos-reference/) ([OpenAlex](https://openalex.org/W2259172389))
- **Competency frameworks are descriptive only.** Large taxonomies such as O*NET and ESCO "remain primarily descriptive and do not necessarily provide a psychologically integrated account of how internal resources combine to produce competence". Practitioners fall back on tacit "folk" interpretations of competency labels. PROMISING (single 2026 validation paper). [ATHENA framework, J. Intelligence 2026](https://doi.org/10.3390/jintelligence14020023)
- **ESCO–O*NET crosswalk.** An official crosswalk exists between ESCO and O*NET. The frameworks interoperate at the occupation/skill-label level. ESTABLISHED. [ESCO crosswalk](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/crosswalk-between-onet-and-esco)
- **Granularity mismatch.** Public taxonomies do not match the granularity employers need. The source here is weak: a commercial explainer. SPECULATIVE. [AIEH](https://aieh.com/skills-taxonomy-frameworks/)

### Inferences
- The CommonKADS diagnosis template (complaint → cover → hypotheses → select a test → predict → compare) is a ready-made spec for the cohort-level diagnosis step. The "hypothesis" objects are bottleneck hypotheses and the "tests" are ECD tasks. SPECULATIVE.
- Competency frameworks are useful only as a top-level anchor for organisational transfer (mapping a KC cluster to an ESCO skill URI via SKOS mapping). They cannot hold cues, conditions or errors. SPECULATIVE.

### Gaps
- Ontology design patterns (Gangemi & Presutti 2009, *Handbook on Ontologies*) are identifier not verified; the catalogue is at ontologydesignpatterns.org, which was not fetched.
- SFIA and IEEE 1484.20.x competency-definition standards were not examined this session.

## 6. Provenance, uncertainty and argument

### Takeaway
Mature standards exist for every epistemic element the project needs. PROV-O covers where a claim came from. Nanopublications and micropublications give claim-level units with evidence and support/challenge. Dung, AIF and IBIS cover contradictions and open issues. GRADE covers graded certainty. Wikidata qualifiers and RDF 1.2 triple terms cover statement-level metadata. The gap is not the vocabulary. It is an agreed certainty scale for *pedagogical and expertise* claims, since GRADE is clinical.

### Cited Findings
- **PROV-O.** PROV-O is a W3C Recommendation (2013) built on Entity, Activity and Agent, with relations such as wasGeneratedBy, wasDerivedFrom and wasAttributedTo. ESTABLISHED. [W3C PROV-O](https://www.w3.org/TR/prov-o/)
- **Nanopublications.** A nanopublication is the smallest publishable unit: one assertion plus its provenance, so single claims can be cited and attributed. ESTABLISHED. [Groth, Gibson & Velterop 2010, Information Services & Use](https://doi.org/10.3233/isu-2010-0613)
- **Micropublications.** Micropublications model a claim together with its supporting evidence, arguments, and *support* and *challenge* relations. They can express disagreement and contradicting evidence explicitly. ESTABLISHED. [Clark, Ciccarese & Goble 2014, J Biomed Semantics](https://doi.org/10.1186/2041-1480-5-28)
- **Dung's argumentation frameworks.** These are pairs of (arguments, attack relation), with semantics (grounded, preferred, stable) that compute which arguments are acceptable. This is the formal core for managing contradictory claims. ESTABLISHED. [Dung 1995, Artificial Intelligence](https://doi.org/10.1016/0004-3702(94)00041-x)
- **Argument Interchange Format.** AIF is an interchange ontology for argument structures across tools. ESTABLISHED. [Chesñevar et al. 2006, Knowledge Engineering Review](https://doi.org/10.1017/s0269888906001044)
- **Toulmin's model.** Toulmin's claim, data, warrant, backing, qualifier and rebuttal structure is the base of ECD's assessment argument, shown in Section 2. ESTABLISHED. [Toulmin, *The Uses of Argument*, CUP (updated ed. 2003)](https://doi.org/10.1017/cbo9780511840005)
- **GRADE.** GRADE rates certainty of evidence as high, moderate, low or very low. Ratings are downgraded for risk of bias, inconsistency, indirectness, imprecision and publication bias, and certainty is kept separate from the strength of a recommendation. ESTABLISHED. [Guyatt et al. 2008, BMJ](https://doi.org/10.1136/bmj.39489.470347.ad)
- **Wikidata.** Wikidata statements carry qualifiers, references and ranks (preferred, normal, deprecated). The same property can hold several conflicting sourced values. ESTABLISHED. [Vrandečić & Krötzsch 2014, CACM](https://doi.org/10.1145/2629489)
- **RDF 1.2.** RDF 1.2 adds *triple terms*, so a triple can be the object of another triple and statements about statements become native. As of April 2026 RDF 1.2 Concepts is a Candidate Recommendation, not yet a Recommendation. ESTABLISHED (status as of the fetched pages). [RDF 1.2 Concepts](https://www.w3.org/TR/rdf12-concepts/); [RDF 1.2 Semantics CR 2026-04-07](https://www.w3.org/TR/2026/CR-rdf12-semantics-20260407/)
- **IBIS and ADRs.** IBIS (Kunz & Rittel 1970) structures deliberation as Issues, Positions and Arguments, and Architecture Decision Records are its lightweight engineering descendant. ESTABLISHED as practice. Identifier not verified: the 1970 working paper has no DOI, and OpenAlex had no convincing match.

### Inferences
- An "unresolved question" is an IBIS Issue with no accepted Position. A "contradiction" is a mutual attack in a Dung framework, or a micropublication challenge. Neither needs a new construct. SPECULATIVE.
- GRADE's downgrading domains carry over to expertise claims reasonably well. For example: one expert versus several (inconsistency), a physics claim applied to another domain (indirectness), or a small elicitation sample (imprecision). The adaptation is untested. SPECULATIVE.
- Until RDF 1.2 is final, a property graph or named graphs (the nanopublication style) are the safe way to attach confidence and provenance to individual edges. SPECULATIVE.

### Gaps
- No certainty scale validated for elicited expert *procedural or tacit* claims was found. GRADE and similar scales cover clinical and intervention evidence.
- Whether any education platform has adopted nanopublications or micropublications was not found.

## 7. Is a knowledge graph sufficient?

### Takeaway
No. A plain triple KG represents entities and relations well. It does not natively represent condition→action rules with their applicability, ordered procedures, perceptual cues, probabilistic learner states, or argumentative status. Those are exactly what Sections 1–6 supply. Current LLM+KG tutoring work mostly uses KGs for concepts and prerequisites plus LLM generation, and does not model expertise as condition-bound performance. ESTABLISHED for the structural point; PROMISING or SPECULATIVE for the LLM+KG tutoring claims.

### Cited Findings
- **KG survey scope.** The comprehensive KG survey treats deductive knowledge (ontologies, rules) and contextual or annotated knowledge (qualifiers, reification, fuzzy or probabilistic annotations) as *extensions* layered on the basic graph data model, not as part of it. ESTABLISHED. [Hogan et al. 2021, ACM Computing Surveys](https://doi.org/10.1145/3447772)
- **LLM–KG combinations.** The LLM–KG roadmap distinguishes KG-enhanced LLMs, LLM-augmented KGs and synergised LLM+KG, with KGs as the structured, interpretable and factual complement to LLMs. ESTABLISHED as a framing. [Pan et al. 2024, IEEE TKDE](https://doi.org/10.1109/tkde.2024.3352100)
- **Educational LLM+KG survey.** A 2025 survey of educational LLM+KG integration covers intelligent tutoring, learning companions and evaluation systems. It names hallucination, lack of explainable reasoning and misfit to curriculum standards as open problems. PROMISING (abstract only). [Neurocomputing 2025](https://doi.org/10.1016/j.neucom.2025.131230)
- **LLM curriculum KGs.** LLMs are being used to extract concepts and *prerequisite* relations from syllabi into curriculum KGs. PROMISING (abstract only). [Gacek & Adrian 2025, SAGE](https://journals.sagepub.com/doi/10.1177/17248035251360196)
- **Recursive prerequisite tracing.** Recursive prerequisite knowledge tracing has been proposed for conversational tutors. PROMISING or SPECULATIVE (arXiv, not read). [RPKT, arXiv:2508.11892](https://arxiv.org/pdf/2508.11892)
- **Behaviour-level models are argued to miss something.** An argument holds that behaviour- and outcome-level models of expertise miss internal "tension and value structures". SPECULATIVE (single-author 2026 preprint, not peer reviewed). [Yuan 2026, arXiv:2605.11393](https://arxiv.org/abs/2605.11393)
- **Mature tutors use rules and constraints, not graphs.** The strongest empirical ITS results come from production-rule and constraint representations with statistical learner models layered on top, not from graph-only models. ESTABLISHED. [Anderson et al. 1995](https://doi.org/10.1207/s15327809jls0402_2); [Mitrovic 2012](https://doi.org/10.1007/s11257-011-9105-9); [Liu & Koedinger 2017](https://jedm.educationaldatamining.org/index.php/JEDM/article/view/212)

### Inferences
What a KG misses, and what fills each gap:
- **Conditionality.** Filled by KLI conditions, production rules, CBM relevance conditions and GOMS selection rules.
- **Procedure and ordering.** Filled by HTA plans, GOMS methods and 4C/ID SAP phases.
- **Perceptual cues.** Filled only by CDM/ACTA text descriptors plus examples; nothing is formal.
- **Probabilistic learner state.** Filled by BKT, AFM and CDMs.
- **Epistemic status.** Filled by PROV, micropublications and Dung.

A KG is best used as the *index and glue* layer linking these objects, not as the expertise model itself. SPECULATIVE (synthesis).

A "hypothesis graph", in which bottleneck hypotheses are nodes carrying evidence, confidence and attack/support edges, can be assembled from micropublications plus the CommonKADS diagnosis template. No off-the-shelf education implementation was found. SPECULATIVE.

### Gaps
- No controlled study was found comparing a KG-only domain model against a KC/production model on learning outcomes.
- The "correct-answer trap" paper on LLM tutor blind spots ([arXiv:2605.23925](https://arxiv.org/pdf/2605.23925)) was surfaced but not read.

## 8. Implications: a composite layered representation

### Takeaway
Reuse, do not invent. The recommended composite has seven layers:
- **L0 Terminology:** SKOS.
- **L1 Domain structure:** an RDF/OWL KG as the index, with a CWA abstraction hierarchy for principles and causal means–ends.
- **L2 Performance/expertise:** KLI KCs as the unit, typed by 4C/ID (recurrent rules versus non-recurrent SAPs and mental models), with CBM constraints for applicability and violations, and CDM/ACTA tables for decisions, cues and errors.
- **L3 Learner/difficulty:** a Q-matrix with G-DINA or KST, BKT/AFM, and bug libraries or malrules plus learning-progression levels. Validate with LFA on public DataShop data.
- **L4 Diagnosis/assessment:** ECD design patterns and the CAF, with the CommonKADS diagnosis template for hypothesis testing.
- **L5 Instruction:** 4C/ID components and KLI principles.
- **L6 Epistemics:** PROV-O and nanopublications, micropublication support/challenge, Dung/AIF, IBIS issues, and GRADE-style certainty adapted, carried by RDF 1.2 triple terms or named graphs.

Four gaps are genuinely unaddressed: formal perceptual-cue representation, a standard "bottleneck hypothesis" object, a validated certainty scale for elicited expertise, and a cross-framework ID crosswalk (KC ↔ ECD KSA ↔ CDM decision ↔ 4C/ID constituent skill).

### Cited Findings
Element-by-element mapping. Each row lists the existing framework (source) and the gap status.
- **Concepts.** SKOS concepts plus an OWL class hierarchy ([SKOS](https://www.w3.org/TR/skos-reference/); [Hogan 2021](https://doi.org/10.1145/3447772)). Covered.
- **Terminology.** SKOS pref/alt/hidden labels, with SKOS mapping to ESCO for organisational transfer ([SKOS](https://www.w3.org/TR/skos-reference/); [ESCO crosswalk](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/crosswalk-between-onet-and-esco)). Covered.
- **Facts.** KG triples; KLI "constant condition, constant response" KCs ([Koedinger 2012](https://doi.org/10.1111/j.1551-6709.2012.01245.x)). Covered.
- **Principles.** CDT "principle" content type; CWA abstract-function level; KLI variable-condition KCs ([Vicente 1999](https://openalex.org/W1550840327); [Koedinger 2012](https://doi.org/10.1111/j.1551-6709.2012.01245.x)). Covered.
- **Causal relations.** 4C/ID causal mental models; CWA means–ends links ([van Merriënboer 2002](https://doi.org/10.1007/bf02504993); [Vicente 1999](https://openalex.org/W1550840327)). Partly covered: no standard causal-edge semantics for education.
- **Procedures.** ACT-R productions, GOMS methods, HTA goals and plans, 4C/ID recurrent-skill rules ([Anderson 1995](https://doi.org/10.1207/s15327809jls0402_2); [John & Kieras 1996](https://doi.org/10.1145/235833.236054); [Stanton 2006](https://doi.org/10.1016/j.apergo.2005.06.003)). Covered.
- **Strategies.** 4C/ID SAPs (phases plus rules of thumb); CWA strategies analysis ([van Merriënboer 2002](https://doi.org/10.1007/bf02504993)). Covered.
- **Decisions.** CDM decision points; GDTA decisions-as-questions; ACTA "difficult cognitive element" ([Klein 1989](https://doi.org/10.1109/21.31053); [Militello & Hutton 1998](https://doi.org/10.1080/001401398186108)). Covered.
- **Cues.** CDM/ACTA "cues and strategies" column; GDTA SA level-1 requirements ([Militello & Hutton 1998](https://doi.org/10.1080/001401398186108)). **Gap:** cues are free text. There is no formal representation of perceptual or pattern cues, and no link from a cue to its evidence.
- **Representations.** Chi et al. deep versus surface problem representation; ECD potential work products (diagrams, equations) ([Chi 1981](https://doi.org/10.1207/s15516709cog0502_2); [Mislevy & Riconscente 2005](https://padi.sri.com/downloads/aera/2005/symposium2/papers/MislevyRicLayers.pdf)). Partly covered: no standard vocabulary for external representations such as a free-body diagram or an energy bar chart.
- **Heuristics.** 4C/ID SAP rules of thumb; ACTA "job smarts" ([Militello & Hutton 1998](https://doi.org/10.1080/001401398186108)). Covered, as text.
- **Conditions of applicability ("when NOT to apply").** KLI KC conditions; CBM relevance conditions; GOMS selection rules; HTA plans ([Ohlsson 1994](https://doi.org/10.1007/978-3-662-03037-0_7); [John & Kieras 1996](https://doi.org/10.1145/235833.236054)). Covered.
- **Exceptions.** CBM constraints (relevant but not satisfied); defeasible attack in Dung frameworks ([Dung 1995](https://doi.org/10.1016/0004-3702(94)00041-x)). Partly covered: no education standard for defeasible rule exceptions.
- **Counterexamples.** Dung attacks and micropublication "challenge" ([Clark 2014](https://doi.org/10.1186/2041-1480-5-28)). Partly covered as argument objects; there is no standard link to specific task instances.
- **Failure modes.** Bug libraries, repair theory, ACTA "common errors", PARI interpretation ([Brown & Burton 1978](https://doi.org/10.1016/s0364-0213(78)80004-4); [Brown & VanLehn 1980](https://doi.org/10.1016/s0364-0213(80)80010-3); [Hall et al. 1995](https://doi.org/10.21236/ada303654)). Covered.
- **Misconceptions.** FCI-style distractor taxonomies, learning-progression levels, rule space. They must be held as hypotheses given the knowledge-in-pieces critique ([Hestenes 1992](https://doi.org/10.1119/1.2343497); [Alonzo & Steedle 2009](https://doi.org/10.1002/sce.20303); [Tatsuoka 1983](https://doi.org/10.1111/j.1745-3984.1983.tb00212.x); [Smith et al. 1994](https://doi.org/10.1207/s15327809jls0302_1)). Covered, but the theory is contested.
- **Prerequisites.** KST surmise relations and learning spaces; Q-matrix attribute hierarchies; 4C/ID skill hierarchy ([Doignon & Falmagne 1985](https://doi.org/10.1016/s0020-7373(85)80031-6); [Heller 2015](https://doi.org/10.1007/s11336-015-9457-x)). Covered.
- **Expert–novice differences.** Chi et al. categorisation; learning-progression level contrasts; KC model differences discovered via LFA ([Chi 1981](https://doi.org/10.1207/s15516709cog0502_2); [Cen 2006](https://doi.org/10.1007/11774303_17)). **Gap:** there is no standard relation type such as "expert-has / novice-lacks / novice-substitutes". It must be modelled as paired KCs or malrules.
- **Bottleneck hypotheses.** ECD focal KSA versus additional KSAs; CommonKADS diagnosis hypotheses; LFA difficulty factors ([Mislevy & Riconscente 2005](https://padi.sri.com/downloads/aera/2005/symposium2/papers/MislevyRicLayers.pdf); [Schreiber 1994](https://doi.org/10.1109/64.363263); [Liu & Koedinger 2017](https://jedm.educationaldatamining.org/index.php/JEDM/article/view/212)). **Gap:** the pieces exist, but there is no standard first-class object linking an expert operation to a learner failure, its evidence, and its competing explanations.
- **Diagnostic candidates.** ECD task models with characteristic and variable features; the Q-matrix row for each item; CommonKADS "select test" ([Mislevy et al. 2003](https://doi.org/10.1207/s15366359mea0101_02); [de la Torre 2011](https://doi.org/10.1007/s11336-011-9207-7)). Covered.
- **Instructional candidates.** The 4C/ID four components; KLI instructional principles tied to learning processes ([van Merriënboer 2002](https://doi.org/10.1007/bf02504993); [Koedinger 2012](https://doi.org/10.1111/j.1551-6709.2012.01245.x)). Covered at the design level; no machine-readable standard.
- **Provenance.** PROV-O; nanopublication provenance graph; Wikidata references ([PROV-O](https://www.w3.org/TR/prov-o/); [Groth 2010](https://doi.org/10.3233/isu-2010-0613)). Covered.
- **Confidence.** GRADE certainty levels; Wikidata ranks; CDM and BKT posteriors for learner-side confidence ([Guyatt 2008](https://doi.org/10.1136/bmj.39489.470347.ad); [Corbett & Anderson 1995](https://doi.org/10.1007/bf01099821)). **Gap:** no validated certainty scale for elicited expertise claims; GRADE's adaptation is untested.
- **Contradictions.** Dung frameworks, AIF, micropublication challenge, Wikidata multi-valued statements with ranks ([Dung 1995](https://doi.org/10.1016/0004-3702(94)00041-x); [Chesñevar 2006](https://doi.org/10.1017/s0269888906001044); [Vrandečić 2014](https://doi.org/10.1145/2629489)). Covered.
- **Unresolved questions.** IBIS Issues with no accepted Position; ADR "proposed" status (Kunz & Rittel 1970, identifier not verified). Covered as practice; no W3C-level standard.

### Inferences
- **Suggested minimal build order for the static first version.** SPECULATIVE throughout.
  1. SKOS terms plus KLI KCs with condition fields.
  2. ACTA-column decision rows attached to KCs.
  3. Q-matrix over the K0/pilot items.
  4. ECD design-pattern record per diagnostic item.
  5. PROV-O/nanopub-style provenance and a GRADE-like confidence per claim.

  Everything else (G-DINA, KST, Dung semantics) can wait for data.
- **Codebook alignment.** The Stage A codebook's "operations" should map one-to-one onto KCs with condition parts. The K0 error categories (principle selection, representation) should map onto KC types or malrules. That keeps the codebook and the representation aligned without changing any registered rule. SPECULATIVE.
- **Zero-participant check of expert-elicited KCs.** Tag the steps of a public DataShop dataset with the expert-elicited KCs and compare AFM fit (BIC and CV RMSE) against the dataset's default KC model, following the method in Liu & Koedinger 2017. PROMISING method; data availability for physics is unverified.
- **Genuinely new work, where no mature framework exists.**
  - Formal cue representation.
  - The bottleneck-hypothesis object, including its expert–novice contrast relation.
  - A cross-framework identifier crosswalk.
  - A certainty scale for elicited tacit claims.

  Everything else should reuse existing vocabularies. SPECULATIVE (synthesis).

### Gaps
- No existing ontology was found that already integrates KLI, ECD and CTA outputs. A targeted search for "ECD ontology", "PADI object model OWL" and "KC ontology" is still needed before declaring the integration layer novel.
- The FMEA and fault-tree standards (IEC) and SFIA were not verified this session.
