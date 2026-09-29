# N3 PoC: methodology lenses for a structural gap map (spec)

**Status: built (revised three times); final outcome: the pipeline works, but its closure step does not beat a fair control, so the output is gap *candidates*. See `research/n3/README.md`.** A proof of concept (PoC) of the NOW pipeline *evidence ledger → methodology-guided analysis → hidden-knowledge hypotheses → ranked gap map → questions for humans*. It is **not** the N3 gate of `docs/plans/n3-gap-map-plan.md`. It uses no gold, no experts and no paid calls, and it touches nothing under `instrument/`. It does not change `gapmap.py`, `AreaFeatures` or `residual/frozen/n1.json`. It adds new modules only. **Since a second adversarial review (2026-09-29, "S1-S3 changes" below), closure is decided by a local, $0 semantic judge (Ollama, `qwen2.5:7b-instruct`) over stdlib `urllib` -- the package therefore now makes one kind of network call (to `localhost:11434`), never a paid one, and replay mode (the CLI default) makes none at all.** Results (current): `research/n3/README.md` and `research/n3/{plc,gdpr_v1,gdpr_v2}/`. §8 and §9's numbers are the **pre-review prototype's** (measured before the first adversarial review found the defects §25 "Post-review changes" fixes); §7.1's pre-review table is likewise superseded. They are kept for the historical record and are no longer what the code in `gapmap/` produces.

**In-sample warning.** The lexicons and thresholds were iterated on these three ledgers (§8 lists every change and the case that forced it). The PoC's output on them is therefore in-sample. Before any gold is acquired, the config is hash-frozen (§0), and any evaluation uses fresh ledgers (`REORIENTATION.md` §14.3). The code never reads `research_notes/`.

## 0. Contract

- **Input:** one `Ledger` (`Ledger.from_json`), optionally a *sibling* ledger of the same domain (§7.2), and optionally the run's `sidecar.json` (`slots`) for §3.
- **Output:** `gapmap.json` (records, §4) and `gapmap.md` (the rendered map plus the §7 checks), written to `--out`. Run directories are never modified. Hypotheses are never written back into a ledger as claims.
- **Code:** the sibling package `gapmap/` (`src/gapmap/`: `text.py`, `link.py`, `lenses.py`, `judge.py`, `semantic.py`, `record.py`, `rank.py`, `checks.py`, `config.py`, `render.py`, `__main__.py`), with tests in `gapmap/tests/`, so `residual/` and its freeze are untouched. Like `residual/`, it imports only stdlib, pydantic and `residual` (an architecture test enforces it), so Spearman, the stemmer and the Ollama HTTP call (`judge.py`, stdlib `urllib` only) are hand-written. Invocation: `uv run --directory gapmap python -m gapmap --ledger L.json [--sibling S.json] [--sidecar sc.json] --domain NAME --out DIR [--judge ollama]`.
- **Determinism:** the same inputs give byte-identical output. Iterate claims sorted by `claim_id` and emit JSON with `sort_keys=True`. `config.py` holds every lexicon, threshold and cap. Its canonical JSON is hashed (`config_sha256`) into every output. Changing it is a re-freeze.
- **Pipeline:** §1 shared machinery → §2 six lenses (*analysis*) → §4 records with three tiers (*hypotheses*) → §6 ranking (*gap map*) → question templates in §2 (*questions*). §3 retrieval gaps travel in a separate section and never enter the map.

## 1. Shared machinery

### 1.1 Pools, labels and what each may do

Take `lab = ledger.label(claim_id)`.
- **A (attested):** `lab ∈ CRITERION_LABELS`. On this data that is only `literature_supported`: 321 / 193 / 203 claims in PLC / GDPR v1 / GDPR v2. Only A **attests** an explicit part, and only A **closes** a gap.
- **S (synthetic):** `lab == synthetic_extrapolation`: 49 / 64 / 305. On this data this means extracted but not verified (verdict `insufficient`, `pending`, or no located span). S never attests and never closes. If S alone contains the missing element, the candidate is rerouted to **RG-UNVER** (§3). S claims may appear in a record's evidence list, flagged.
- **U (unknown):** `lab == unknown`: 5 / 14 / 15. These are N2's templated slot questions. They feed only **RG-UNK**.

### 1.2 Text: fire narrow, close wide

`T(c) = assertion + " " + " ".join(e.selector.exact for e in c.evidence if e.selector.exact)`. Lenses **fire on `assertion`**, the extractor's paraphrase of what the claim is. Closure tests run on **`T(c)`**, which adds the verbatim source text. This asymmetry is conservative: a gap needs the explicit part stated, but anything the source says can close it. The measured case: the span of `c-111d883494ccf58b` states the ordering ("the field device and wiring are far more likely to fail than the card"), which its assertion drops.

### 1.3 Tokens and stems

- `tokens(s)`: `re.findall(r"[a-z][a-z0-9]+", s.lower())`. Drop tokens of length ≤ 2 and tokens in STOP.
- STOP: a an the and or but if then else when while of in on at to for from by with without into onto over under about as is are was were be been being this that these those it its it's their there they them we you your our can could may might must should shall will would do does did done not no nor any all each every some such more most less least other than also only very just both either neither which who whom whose what where why how per via using use used uses make makes made one two three first new e.g i.e etc within between before after during across through because since so up out off down whether common commonly typically typical often usually among issue issues most many several various.
- `stem(t)`: try suffixes in the order `ies→y`, `ing`, `ed`, `es`, `s`. Strip the first that leaves at least 4 characters, never stripping from a word ending in `ss`.
- `cw(s)` = the set of stems.
- **Ledger-common stems** are those in more than 5% of A's assertions: 30 / 44 / 52 stems here, for example `fault, plc, intermittent`, `dpia, process, data, risk`. They are excluded from linking.

### 1.4 Linking and breadth

- **Neighbourhood** `N(c)`: the A claims `d ≠ c` with `|cw(c) ∩ cw(d) ∖ common| ≥ 2` (assertions only). Measured median degree is 4 / 2 / 3. Isolated A claims: 27/321, 41/193, 35/203. The share of links crossing independence keys is 0.65 / 0.08 / 0.43. Areas are not used for linking. They are 5 topical planner buckets per ledger, and a third or more of links cross them.
- **Seeds:** the A claims on which a lens fires, restated for one record.
- **Explicit part** `X`: the seeds plus their neighbourhoods, A only.
- **Breadth:** `k_step` = distinct `independence_key` over the supporting evidence of the seeds, and `k_topic` = the same over X. Per-claim `corroboration` cannot carry breadth on this data: every claim has at most 1 counted supporting source. Distinct supporting keys per ledger are 19 / 3 / 5. GDPR v1 has 13 source identifiers but only 3 keys.
- **Robustness settings:** the common-stem cut is 5% or 8%, and the shared-stem threshold is 2 or 3. Setting 1 is (5%, 2). A record's robustness `r ∈ 0..4` counts the settings that reproduce it: same lens and category, and the same anchor or an X Jaccard of at least 0.5.

### 1.5 Closure states (F1: whole-pool, not neighbourhood-only)

**Post-review (F1).** For SEL, HEDGE, GUARD, WHY, DIAG's per-rival sign test and RESULT, the
closure test below is no longer scoped to the lexical neighbourhood: it runs over **every**
attested (A) claim in the ledger (S for synthetic-closed), because scoping it to the
neighbourhood made "closed vs open" track neighbour count rather than genuine textual support. A
claim `c` closes a candidate iff one sentence of `T(c)` (split per §1.2) contains the lens's
closure-lexicon hit **and** contains at least `min(2, |seed content stems|)` of the seed's
non-common content stems (for DIAG: of that rival's cause stems; HEDGE still excludes the seed
itself). The neighbourhood (§1.4) still defines `X` and breadth (`k_step`, `k_topic`) only --
never closure. DISC is unaffected: its closure was already ledger-wide and anchor-regex-driven,
not neighbourhood- or stem-overlap-based.

A lens's missing-element test over the lens's **closure scope** gives one of four states:
- **open:** no hit.
- **partial:** a weaker hit that the lens defines.
- **closed:** a hit in an A claim.
- **synthetic-closed:** a hit only in S.

Only open and partial can become hypotheses.

## 2. Lenses

Each lens is an analytical construct, not a named method. For each one: what it fires on, its explicit part, the missing element, the hypothesis template, alternative explanations specific to the lens, the knowledge type and tacitness it predicts (`KnowledgeType` / `Tacitness`, recorded as predictions labelled `inferred`, never written to claims), the matched channel (§10.3), and a question template. The lexicons are in §2.7.

**Question rules (all lenses).** The CDM style is retrospective and incident-anchored, and never asks during a task (`research/explore-cognitive-task-analysis.md`, "Which method? Validity constraints": Klein et al. 1989; Hoffman et al. 1998; reactivity per Fox et al. 2011).
- Quote at most 2 verbatim spans (`selector.exact`) from different keys.
- Never name a candidate answer.
- No yes/no questions.
- Ask for a contrast between cases.
- One construct per question.

The DtD element used is bottleneck framing only. The decoding interview is not evidential (`research/falsify-decoding-the-disciplines.md`, Verdict).

### 2.1 DISC: undefined discrimination (cue as discrimination)

- **Construct.** A cue is a discrimination: contrasting cases plus the feature that separates them (`REORIENTATION.md` §10.2 item 1). CDM probes for cues, discriminations and typicality (`explore-cognitive-task-analysis.md`, "Which method? Validity constraints"). The residual is predicted to be cue and expectancy knowledge, and *which* cue triggered a choice is behaviour-only (`tacit_knowledge_foundations.md` §4 and §7, Inferences).
- **Fires on:** a JUDGE term in an A assertion. The anchor is the term plus the stem of the next non-STOP token. `high risk` and `large scale` are fixed anchors. **Termhood:** an anchor needs at least 2 distinct A claims, otherwise it is dropped. This removes one-off bigrams such as "appropriate tank".
- **Explicit part:** the anchor claims (the seeds) plus their neighbourhoods.
- **Missing element:** a boundary for the anchor. The closure scope is every claim whose `T` contains the anchor, matched as `\b<term>[- ]<head>\w*`. Check the states in this order:
  1. **closed:** QUANT in the anchor's sentence (sentences are split on `(?<=[.;])\s`) in an A claim.
  2. **synthetic-closed:** the same, in an S claim only.
  3. **partial:** CASE in the anchor's sentence (A), **or** DEFN anywhere in an A anchor claim, **or** an A sentence defines the bare term (`\b<term>\b[^.;]{0,60}\b(means|defined as|refers? to|is when|occurs when|covers)\b` or `\bis <term> (when|if)\b`).
  4. **open:** none of these.
  One-sided examples ("such as children") are partial, not closed: they do not give the separating feature.
- **Hypothesis:** "Practitioners discriminate *<anchor>* from its neighbours by features no attested source states. The sources name the category (and, if partial, list factors or example cases) but give no boundary."
- **Alternatives:**
  - The boundary is stated in paraphrase without the anchor string.
  - The term is **institutionally indeterminate**, so experts disagree and there is nothing to recover. This is live when at least 50% of the anchor claims are `norm` or `concept`.
  - The boundary is in unfetched sources.
- **Predicts:** `cue` (`expectancy` for `normal`, `expected`, `baseline`). Tacitness: `perceptual` if at least 50% of X is typed failure_mode, cue, check, procedure_step or interpretation, otherwise `collective`.
- **Channel:** contrasting-case classification (perceptual), or expert-rated written vignettes (collective or relational; `tacit_knowledge_foundations.md` §5, Inferences). Not interviews alone.
- **Question template:** "Two sources write: “{s1}” and “{s2}”. Think of a recent case where you had to judge whether something was {anchor}. Describe one case that clearly was, one that clearly was not, and one that was hard to call. What differed between them, and what did you check first?"

### 2.2 DIAG: rival causes without discriminating signs (interpretation)

- **Construct.** PARI's Interpretation step updates the fault hypothesis. ECD "additional KSAs" formalise rival explanations of one observation (`expertise_representation.md` §4 and §2, Inferences). The rival-cause coverage rates quoted in the notes are held-out gold material and are not used.
- **Fires on:** A claims typed `failure_mode`, `cue`, `interpretation`, `misconception` or `expert_novice_contrast` whose assertion matches CAUSE. Split the assertion at the marker. If the marker matches `caused|due|result(s|ing)? from|stem|traceable|relate`, the text after the marker is the cause and the text before it is the effect; otherwise the reverse. Two cause claims are **rivals** if their effect stems share at least 2 stems (common stems allowed) and their cause stems share at most 1 non-common stem. A seed plus its rivals is a group, and a group needs at least 2 rivals.
- **Explicit part:** the group, with each rival cause attested by its own claim.
- **Missing element:** a sign per rival. Rival `r` is **signed** if some A claim (r itself included, using its span) shares at least min(2, |cause stems of r|) of r's non-common cause stems and matches DISCR in `T`. The group is **open** if at least 2 rivals are unsigned, otherwise **closed**.
- **Hypothesis:** "Practitioners tell {unsigned causes} apart by signs no attested source states. Sources attest signs only for {signed causes}."
- **Alternatives:**
  - The sign exists but is phrased without the cause's stems. Measured: the movement-correlation cue in `c-23aba084f2e63ad1` is not linked to "loose".
  - The causes co-occur, and experts test rather than discriminate.
  - The sign is instrument output, not tacit knowledge.
- **Predicts:** `interpretation` (+`cue`). Tacitness: `relational`, with `perceptual` added if any seed is typed `cue`.
- **Channel:** CDM probes on a recalled case, then contrasting cases.
- **Question template:** "Sources list several causes of {effect}: “{s_a}”, “{s_b}”. Think of the last {effect} you diagnosed. Which cause did you suspect first, and what did you see, hear or measure that let you rule the others out?"

### 2.3 SEL: selection criterion named, mapping absent (decision rule)

- **Construct.** Conditions for choosing a method: GOMS selection rules, HTA plans and the KC condition part (`expertise_representation.md` §4 Takeaway, §1 Inferences). "When (not) to apply" is the L2 row of `REORIENTATION.md` §10.
- **Fires on:** an A assertion that matches SEL **and** is prescriptive (MODAL, or typed `decision`).
- **Explicit part:** the seed plus its neighbourhood.
- **Missing element:** a mapping from situation to option. It is **closed** if COND matches `T` of the seed or of any A neighbour, **synthetic-closed** if it matches only an S neighbour, and **open** otherwise.
- **Hypothesis:** "Practitioners map situations to the choice ‘{seed}’ by conditions no attested source states."
- **Alternatives:**
  - The mapping is stated as an example or a comparative that COND does not match.
  - The choice is not a real decision point in practice.
- **Predicts:** `decision`, `relational`.
- **Channel:** CDM probes for options considered and the basis of choice.
- **Question template:** "“{s1}”. Think of the last time you made this choice. Which options did you consider, which did you take, and what about that situation decided it? When did you last choose differently?"

### 2.4 HEDGE: hedged rule, exception condition absent (conditional knowledge)

- **Construct.** "When NOT to apply" a rule: CBM relevance conditions and KLI condition parts (`expertise_representation.md` §1 and §7, Inferences). A quasi-universal hedge admits exceptions without stating them.
- **Fires on:** an A assertion that is prescriptive (MODAL, or typed decision, norm, strategy, procedure_step or check) and has HEDGE **before** any RAT marker, because a hedge inside a "because" clause qualifies the reason, not the rule.
- **Explicit part:** the seed plus its neighbourhood.
- **Missing element:** an exception condition. It is **closed** if EXC matches `T` of any A neighbour (not the seed itself), **synthetic-closed** if it matches only in S, and **open** otherwise.
- **Hypothesis:** "Practitioners know the cases in which ‘{seed}’ does not hold, and no attested source states them."
- **Alternatives:**
  - The exception is circular: it restates the judgement. Measured in the span of `c-04425373cd3694c7`: "if you are confident that the processing is nonetheless unlikely to result in a high risk".
  - The hedge is statutory boilerplate with no practice behind it.
  - A trigger is stated inside the seed itself in a form EXC does not match ("at least when").
- **Predicts:** `decision`. Tacitness: `relational`, or `collective` if at least 50% of X is `norm`.
- **Channel:** CDM hypotheticals and boundary-case vignettes.
- **Question template:** "“{s1}”. Describe a case where this did not hold, or where you decided against it. What about that case told you it was an exception?"

### 2.5 GUARD: named error without a detection cue (automated self-check)

- **Construct.** Automated error-monitoring and self-check habits are behaviour-only (`tacit_knowledge_foundations.md` §7, Inferences). Omission comes partly from automated procedure (§1, Inferences). The bottleneck-hypothesis object (`REORIENTATION.md` §10.2 item 2) needs a *learner* observation, but these ledgers hold only expert-voiced text. Experts hold only part of what learners get wrong (`explore-pedagogical-content-knowledge.md`, "Do content experts know what students get wrong?"), and a misconception is a context-bound hypothesis (`explore-conceptual-change.md`, "Theory: what is a misconception?"). **GUARD therefore never asserts a learner difficulty.** It hypothesises the expert's guard against an error that an expert reported.
- **Fires on:** A claims typed `misconception`, or whose assertion matches ERR.
- **Explicit part:** the seed plus its neighbourhood.
- **Missing element:** a detection cue. It is **closed** if DETECT matches the seed's `T`, or if an A neighbour is typed check or cue or matches DETECT in `T`. It is **synthetic-closed** if this happens only in S, and **open** otherwise.
- **Hypothesis:** "Practitioners notice {error} before or as it happens by a check no attested source states. This is an expert-reported error, not an observed learner difficulty."
- **Alternatives:**
  - The cue is stated in paraphrase.
  - The error is a vendor framing, not a practitioner error.
  - The guard is organisational (a checklist or procedure), not cognitive.
- **Predicts:** `check` or `metacognition`, `automated`.
- **Channel:** observation or process tracing first. A retrospective probe over a recorded trace comes second, because think-aloud is weak for automated checks (§10.3).
- **Question template:** "“{s1}”. Think of the last time you or a colleague nearly did this or just had. What made you notice? What did you look at?" Flag the answer as a weak channel for this type.

### 2.6 WHY: prohibitive or contrastive prescription without rationale

- **Construct.** The rationale gap, from Szulanski's causal ambiguity (`REORIENTATION.md` §14.2; `AreaFeatures.rationale_present`). "This works because…" rationales are text-visible (`tacit_knowledge_foundations.md` §7, Inferences), so their absence where many sources prescribe carries information. The channel for rationale is targeted confirmation questions (§10.3). This is restricted to prohibitions and contrasts, where the "why" is least obvious.
- **Fires on:** an A assertion with MODAL and CONTRA.
  - It is excluded as `authority` (logged, not emitted) if AUTH matches `T`, because the reason is the rule itself.
  - It is **closed** if RAT matches the seed's `T`.
- **Explicit part:** the seed plus its neighbourhood.
- **Missing element:** a reason. It is **closed** if an A neighbour is typed rationale or failure_mode (the failure the prescription guards against) or matches RAT. It is **synthetic-closed** if this happens only in S, and **open** otherwise.
- **Hypothesis:** "Practitioners know why ‘{seed}’, and no attested source states it."
- **Alternatives:**
  - The rationale is a purpose clause ("to identify…") that RAT does not match.
  - The source is promotional.
  - The reason is trivial safety knowledge.
- **Predicts:** `rationale`, `relational`.
- **Channel:** a targeted confirmation question.
- **Question template (revised, F9):** "Sources say: “{s1}”. What would happen if someone did it differently, and in what situations, if any, is doing it differently acceptable?"

### 2.7 Lexicons (case-insensitive; frozen in `config.py`)

```
MODAL  \b(must|should|shall|required?|need(?:s)? to|mandatory|necessary to)\b
JUDGE  \b(appropriate|adequate|sufficient(?:ly)?|reasonable|significant(?:ly)?|large[- ]scale|high[- ]risk|systematic(?:ally)?|relevant|suitable|proper(?:ly)?|excessive|abnormal|unusual|normal|acceptable|minor|serious|severe|substantial|stable|loose|marginal|poor|vulnerable|extensive|innovative|sensitive|expected|baseline)\b
QUANT  \b(?:more than|less than|fewer than|at least|at most|over|under|above|below|between|up to|exceed\w*|within)\s+\d
       |\d+(?:\.\d+)?\s?(?:%|percent|vdc|vac|v|ms|s|seconds?|minutes?|hours?|days?|weeks?|months?|years?|ohms?|mm|hz|khz|mhz|ma|a)\b
CASE   \b(whereas|rather than|unlike|versus|vs\.?|as opposed to|but not|not (?:a|an|on|be)\b)
DEFN   \b(means|defined as|refers? to|covers|is when|occurs when|consider\w*|factors?|criteria|criterion|includ\w+|such as|for example|e\.g\.|examples?)\b
CAUSE  \b(caus(?:e|ed|es)|due to|result(?:s|ing)? (?:from|in)|lead(?:s)? to|stem(?:s)? from|produce[sd]?|traceable to|relate[sd]? to|source of|create[sd]?)\b
DISCR  \b(indicat\w*|signs?\b|distinguish\w*|rather than|whereas|correlat\w*|only after|appear\w* only|symptom\w*|characteristic|signature|points? to|pattern)\b
SEL    \b(based on|according to|depending on|most likely|most probable|prioriti[sz]\w*|choos\w*|chosen|select\w*|decid\w*|determin\w* (?:which|whether))\b
COND   \b(if|when|whenever|for (?:a|an)\b.*\buse)\b|\b(?:more|less) likely\b[^.;]{0,40}\bthan\b
HEDGE  \b(in most cases|generally|typically|usually|normally|in general|as a rule|not (?:a|an) (?:strict|absolute|hard) rule|where appropriate|where necessary|if necessary|as needed|case[- ]by[- ]case|in (?:some|certain) cases|depend(?:s|ing)? on)\b
EXC    \b(unless|except\w*\b(?![^.;]{0,25}\b(?:article|art\.|section|recital)\b)|only (?:if|when|where)|does not apply|do not apply|not required|exempt\w*|even (?:if|when)|provided that|as long as)\b
ERR    \b(mistake\w*|pitfall\w*|overlook\w*|false (?:positive|negative|reading|result|state)\w*|wrongly|mistaken\w*|tempting|common error\w*|misinterpret\w*|misread\w*)\b
DETECT \b(check\w*|verif\w*|confirm\w*|notic\w*|detect\w*|recogni\w*|tell\w*|warning sign\w*|indicat\w*)\b
CONTRA \b(not|never|avoid\w*|instead|rather than|only|before|first)\b|QUANT
RAT    ,\s*as\s|\bwill (?:destroy|damage|kill|overwrite|lose|corrupt|cause)\b|\b(because|since|so that|in order to|to ensure|to avoid|to prevent|prevent\w*|otherwise|reason|why|as this|this (?:helps|allows|ensures)|to (?:preserve|protect|reduce|keep|save|stop))\b
AUTH   \b(article|regulation|gdpr|law|legal\w*|statut\w*|directive|act|authorit\w*|supervisory|dpa|ico|regulator\w*|edpb|wp29|guideline\w*)\b
TEST   \b(measur\w*|check\w*|test\w*|inspect\w*|verif\w*|monitor\w*|observ\w*|compar\w*|captur\w*|trend\w*|assess\w*|evaluat\w*|review\w*)\b
INTERP \b(indicat\w*|means|suggest\w*|points? to|impl(y|ies)|reveal\w*|shows? that|confirm\w*|rules? out|should (read|be|show)|expected|normal(ly)?|typical(ly)?|reading of|then)\b
PROMO  \b(our|we offer|request a demo|book a demo|pricing|platform|solution|appliance|hub|dashboard|live data|no cloud)\b|™|®
GUARD_AGENT \b(technician|engineer|operator|practitioner|troubleshoot\w*|you|people|staff|team|someone|organi[sz]ation\w*|controller\w*|mistake)\b
WHY_DISJUNCTION require(?:s)? or (?:do|does) not require
```
(F6, F7: added post-review; AUTH's additions and WHY_DISJUNCTION are new WHY guards, TEST/INTERP feed §2.8 RESULT, PROMO and GUARD_AGENT feed WHY/GUARD's promotional-source and human-agent guards.)

### 2.8 RESULT: PARI result interpretation (added post-review, F7)

- **Construct.** PARI's Precursor-Action-Result-Interpretation (`research_notes/Tacit knowledge reorientation/expertise_representation.md`, PARI [106]; `REORIENTATION.md` §10 L2 "troubleshooting steps"); CDM "what did you notice / what would have made you act differently". Sources prescribe a test; the expert's reading of the result and the branch it selects is the predicted residual -- the "A → B → C, but what decides B vs D" gap.
- **Fires on:** an A claim typed `procedure_step`, `check`, `strategy` or `decision` whose assertion matches TEST, followed within 6 tokens by >= 1 non-common content stem (the object). Anchor = the verbatim verb + object phrase, trimmed to <= 60 chars.
- **Explicit part:** the seed plus its neighbourhood (§1.4, unchanged by F1 -- only the closure test moved to the whole pool).
- **Missing element:** a result-to-interpretation mapping for the test. Closed by the shared F1 rule (§1's closure test, below) against INTERP or QUANT.
- **Hypothesis:** "Hypothesis (inferred): practitioners are predicted to read the result of &lt;anchor&gt; against expected values and map it to the next action; no verified claim in this ledger matched test &lt;test_id&gt;."
- **Alternatives:** the interpretation is stated in paraphrase without the seed's stems; the test is a formality with a binary outcome; the interpretation is instrument-given.
- **Predicts:** `interpretation` + `expectancy`. Tacitness: `relational`, plus `perceptual` if the verb is `inspect`/`observe`.
- **Channel:** CDM probes on a recalled case; process tracing.
- **Question template:** "Sources prescribe: “{s1}”. Think of the last time you did this. What result did you get, what had you expected, what did that result make you do next — and what result would have sent you down a different path?"
- Same 3-per-lens cap as every other lens (§6); included in the render, summary and robustness settings identically to DISC/DIAG/SEL/HEDGE/GUARD/WHY.

## 3. Retrieval gaps: a separate category, never hypotheses

Each retrieval gap is rendered in its own section of `gapmap.md` with an action of the form *search or verify*, never *ask an expert*:
- **RG-UNK:** ledger U claims, which are N2 slot probes with nothing found (5 / 14 / 15 here, for example "What observable features of a situation signal that <area> applies…?"), plus sidecar `slots` with status `unknown`, `thin` or `unverified` when a sidecar is given. The GDPR v2 sidecar has 15 unknown, 9 thin and 5 unverified.
- **RG-SINGLE:** a lens fired open or partial, but `k_topic ≤ 1`. One voice not saying X is weak evidence that X is unsaid.
- **RG-UNVER:** the state is synthetic-closed. The element may be stated, but the statement is unverified.
- **RG-SIBLING:** the sibling run's matching candidate is closed (§7.2). If the sibling's candidate is only partial while this one is open, this record becomes partial (−1) instead.

## 4. Gap record schema (`record.py`, pydantic `Record`)

```
gap_id              "g-" + sha256(config_sha256 | ledger_sha256 | lens | sorted seed claim_ids)[:12]
lens, category      DISC|DIAG|SEL|HEDGE|GUARD|WHY ; HYP|RG-UNK|RG-SINGLE|RG-UNVER|RG-SIBLING
anchor              anchor string or seed assertion (display)
observed_evidence   [ {claim_id, epistemic_label, knowledge_type, area_id, source_identifier,
                       independence_key, source_kind, verdict, span (verbatim selector.exact),
                       role: seed|topic|rival|closure_near, counts_as_attestation: bool,
                       flag: null|"unverified-synthetic"} ]            # A → true; S → false + flag
inferred_gap        { statement:  "No attested claim in ledger <sha[:8]> matches <test_id> within
                                   scope <n> claims (A: <n_a>, S searched: <n_s>)",
                      test_id, closure_state: open|partial,
                      partial_hits: [claim_id], synthetic_hits: [claim_id],
                      sibling: {matched_gap_id|null, state|null} }  # checkable by re-running the test
hypothesis          { text, label: "inferred", predicted_knowledge_type, predicted_tacitness,
                      channel }                                      # HYP only; null for RG-*
reasoning           template: "{k_step} key(s) state {explicit}; {k_topic} key(s) discuss the topic;
                               none states {missing element}"
missing             lens-specific description of the element sought
confidence          { score, A, B, P, level: high|moderate|low, robustness: r/4, k_step, k_topic }
alternatives        [ {text, live: bool, why} ]                     # live flags computed, §2
question            { text, target_claim_ids, channel, weak_channel: bool }   # HYP only
rank, merged_from   int|null ; [gap_id]
```

The three tiers never mix:
- `observed_evidence` holds verbatim spans only.
- `inferred_gap` is a statement about the ledger that anyone can re-run.
- `hypothesis` is a prediction and always carries `label: "inferred"`.

The renderer prints them under separate headings and never prints a hypothesis in the indicative mood.

## 5. Confidence rubric and uncertainty

`score = A + B − P − Q`, where:
- `A` = 0 / 1 / 2 / 3 for `k_topic` ≤ 1 / 2 / 3–4 / ≥ 5.
- `B` = 1 if `k_step ≥ 2`, otherwise 0.
- `P` = 1 if the state is partial, otherwise 0.
- `Q` = 1 if the PROMO lexicon (§2.7) is live on the span, otherwise 0 (F6, added post-review).

A record is HYP only if `k_topic ≥ 2`; otherwise it is RG-SINGLE.

**Post-review (F3): the level is renamed `breadth` and is never "high".** `breadth` is `broad` iff `k_topic ≥ 5` **and** `k_step ≥ 2` (decided directly from breadth, not from `score`, since a partial or promo-penalised record can still be broadly attested); `moderate` if not broad but `score ≥ 3`; `narrow` otherwise. Rendered as "breadth (uncalibrated; no gold)". Ranking among open gaps is deliberately by breadth of the attested explicit side — the opposite of low density, on purpose: WHICH candidates are gaps at all is decided entirely by the lens's firing rule plus its closure test (§1.5), and whether that closure test is itself informative is what the §7.1 closure null checks, not this rubric.

Confidence therefore **rises** with the number of independent voices that state or discuss the step while none states the element, and **falls** when the explicit side is thin. Density enters only through independent keys, never through claim counts.

**Uncertainty** is shown, not folded into the score:
- the robustness `r/4`;
- the live alternatives.

The rubric is ordinal and uncalibrated. It has no gold. The only "high" (pre-review) record in these data was a false positive (§9) -- one motivation for F3's rename.

A near-miss count (A claims outside X sharing exactly 1 stem and matching the closure lexicon) was tried and rejected: it ran 0–17 per record and was mostly irrelevant on inspection.

## 6. Ranking, dedup and caps (`rank.py`)

- **Merge:** records with the same lens and category whose X sets have a Jaccard of at least 0.5 merge into the higher-ranked one (`merged_from`). Example: GDPR v2's "Where necessary, the controller shall…" and "…must…" merge.
- **Co-location:** records from different lenses that share a seed are kept, and the map shows the lower one indented under the higher one, using one slot. Example: PLC `c-…dafc04ec`, "Diagnostic tests should be selected based on…", is both SEL and WHY.
- **Order:** by `(−score, −r, −k_topic, −|X|, gap_id)`.
- **Map:** the top 12 HYP per ledger, at most 3 per lens and at most 4 per area (the seed's area).
- **Control slot:** one extra slot for the §14.2 unknown-unknowns guard. It goes to the area with no HYP and the highest A share (ties broken by `area_id`), with a generic CDM walk-through question marked `control`. The fraction is a PoC choice and must be pre-registered for N3.

## 7. Built-in checks, printed in `gapmap.md`

### 7.1 Anti-renaming: is the map density in disguise?

**Post-review (F2): computed over lens candidates only.** Take the pool P = all non-closed AND
closed lens candidates (HYP ∪ RG-SINGLE ∪ RG-UNVER ∪ RG-SIBLING, plus closed) -- RG-UNK and
CONTROL are excluded, since their density cannot vary and would dilute the check. For a record,
`dens` = |X|, the number of verified supporting evidence items, since each A claim carries exactly
one here.
- `D_low` ranks P by ascending `dens` (ties by `gap_id`), and `D_high` ranks it by descending `dens`.
- Report:
  - `J10(map, D_low)`;
  - `J10(map, D_high)`;
  - Spearman ρ(score, dens) over P, with RG records scored −1;
  - a **matched-density table**: for each `dens` tercile of all lens candidates, the counts of closed and HYP;
  - a **closure-rate-by-`k_topic`-band table** (bands 0–1, 2, 3–4, ≥5), over all lens candidates (F2).
- **Flags:**
  - *density-in-disguise* if `J10(map, D_low) ≥ 0.5` or `ρ ≤ −0.5`;
  - *salience-in-disguise* if `J10(map, D_high) ≥ 0.7` **and** the lens closes fewer than 20% of the top tercile. This is the case where the map just ranks the most-discussed topics and its missing-element test decides nothing;
  - *closure-uninformative* (F2, new): from the closure null below.

**Post-review addition (F2): the stem-scramble closure null.** For each lens candidate other than
DISC (whose closure is anchor-regex-driven, not a seed-stem-overlap test, and so is not subject to
the vacuity the null checks for), replace the seed's content stems with an equally sized random
draw from the ledger's non-common stem vocabulary (`random.Random(0)`, 200 draws, deterministic),
and rerun that candidate's closure test (§1.5). Report per lens and total: observed closed count,
null mean, null 5–95% interval, and flag `closure-uninformative` if the observed count falls
inside the null interval -- i.e. random stems would close about as many candidates as the real
seed stems do, meaning the closure test is not discriminating on content. Measured numbers for the
current code are in `research/n3/README.md` and each `gapmap.md`, not reproduced here (they will
drift with every lexicon change and would otherwise go stale the way §8/§9's did).

**Pre-review measured table (PLC / GDPR v1 / GDPR v2), throwaway prototype, kept for history:**

| | PLC | GDPR v1 | GDPR v2 |
|---|---|---|---|
| `J10(map, D_low)` | 0.00 | 0.00 | 0.07 |
| ρ(score, dens) | +0.84 | +0.39 | +0.65 |
| `J10(map, D_high)` | 0.73 | 0.27 | 0.45 |
| Top-tercile candidates closed | 7/12 | 3/5 | 1/9 |

**Reading (pre-review).** The map is not low density in disguise, by construction. It does lean
toward salient topics. In PLC the missing-element test still closes most of the salient
candidates. In GDPR v2 it closes 1 of 9, so there the map is mostly "big DISC anchors" and needs
the §9 caveats. No flag fired -- but this is exactly the table the adversarial review showed was
computed over the wrong pool and without any null, i.e. it could not have detected a vacuous
closure test even if one were present. The closure null above is the fix.

### 7.2 Cross-run stability (GDPR v1 vs v2, which are independent reconstructions)

- **Match:** same lens; for DISC, same term and either the same head stem or the other run's
  anchor head appearing in this run's own anchor claims (F4, revised -- an exact-anchor match was
  too strict, since the same discrimination is often anchored by a different head word across
  independent reconstructions). For the other lenses, a seed-stem Jaccard of at least 0.3, keeping
  the best match.
- **Report:** for each direction, the counterpart category of each open candidate (HYP ∪ RG-SINGLE). Apply RG-SIBLING (§3).
- **Measured (pre-review prototype, kept for history):** v1→v2: of 25 candidates, 16 have no counterpart, 3 are HYP, 3 RG-SINGLE, 1 RG-UNVER and 2 closed. v2→v1: of 21, 14 have no counterpart, 1 is HYP, 5 RG-SINGLE and 1 closed.
- **Stable in both runs (pre-review):** only DISC `innovative technology`, which is partial in both.
- **Reading.** Stability is low. One cause is that each run has one dominant independence key (v1 has 13 identifiers in 3 keys), so most v1 candidates are RG-SINGLE. Another is that the planner retrieved different documents. The check pays for itself: it moves GDPR v2's #2 record (`systematic extensive`, open) to partial, because v1 attests "Processing is systematic when it occurs according to a system…" (`c-2294f81bcee5f2d1`).

## 8. Measured feasibility on the three ledgers

**Pre-review prototype numbers.** Everything in this section was measured with the throwaway
prototype that predated the adversarial review (§25 "Post-review changes"). It is not what the
current `gapmap/` code produces; current counts are in `research/n3/README.md` and the three
`gapmap.md` files.

- **Claims:** 375 / 271 / 523. A: 321 / 193 / 203; S: 49 / 64 / 305; U: 5 / 14 / 15.
- **Layers and questions:** only L1 and L2, and only the questions domain and performance. There are no difficulty or learner claims.
- **Sources:** 100% expert voice. Kinds: PLC documentation only; GDPR v1 documentation; GDPR v2 procedure_document 154, standard 28, documentation 25.
- **Other fields:** contradictions 0 / 1 / 0; tacitness all `unassessed`. The span coverage for evidence (`selector.exact`) is 337/337, 206/206 and 366/366.
- **Knowledge types** are extractor-assigned. Types the lenses read, as A/total: PLC failure_mode 44/48, cue 20/23, decision 14/15, interpretation 11/11, misconception 6/6, rationale 19/21. GDPR v2 cue 9/54, failure_mode 1/5 (4 are U slots). So DIAG and GUARD are PLC-only by construction.
- **Marker hits on A assertions (PLC / v1 / v2), from broader probe lexicons:** modal 78 / 117 / 106; cause marker 48 / 14 / 26; judgement term 62 / 72 / 97; error marker 11 / 4 / 4. `high risk` is in 31 claims across 3 keys in v1, and 44 claims across 5 keys in v2. After termhood and merging, the DISC records are 2 / 8 / 12, and none is closed by QUANT. The HEDGE records are 0 / 4 / 3.
- **Lens output** (HYP / RG-SINGLE / RG-UNVER / closed):
  - PLC: 9 / 12 / 1 / 32 (DISC 2, DIAG 1, GUARD 3, WHY 3 HYP).
  - GDPR v1: 4 / 21 / 1 / 13 (DISC 2, WHY 2).
  - GDPR v2: 12 / 9 / 3 / 18 (DISC 9, SEL 1, HEDGE 2).
- **Levels of HYP:** PLC 3 moderate and 6 low; v1 4 low; v2 1 high, 1 moderate and 10 low.
- **Robust at all 4 settings (r = 4):** 2/9, 1/4 and 7/12. DISC is anchor-linked, so it is robust. The neighbourhood lenses are not.
- **Rule changes forced by the data (all in-sample, all before any gold):**
  - DIAG was restricted to diagnostic types. Without this, v2 gave 22 spurious DIAG records from additive DPIA criteria that "result in high risk".
  - DISC termhood (at least 2 claims), and QUANT narrowed from "any digit". Article numbers had closed `high risk` and `large scale`.
  - DISCR no longer matches "signal", and "common/typically/issue" were added to STOP. Before this, DIAG signed rivals via "signal" and "common cause".
  - RAT gained `, as` and consequence verbs. "…without first verifying the load coil resistance, as a shorted coil will destroy the replacement card" had been open.
  - "assum*", "avoid", "never" and "do not" were dropped from ERR. They fired on procedures and legal negations.
  - SEL requires a prescription, and its COND closure gained comparatives.
  - EXC ignores "exception in Article …". That legal cross-reference had falsely closed the WP248 two-criteria rule.

## 9. Worked examples (the author's judgement, not validation)

**Pre-review prototype numbers.** As §8: these examples (record IDs, states, `r`/`k` values) were
drawn from the pre-review throwaway prototype's output and are not re-verified against the current
`gapmap/` code's output. They still illustrate the constructs; see §25 for what changed and why.

**DISC, GOOD, PLC #1 (moderate, r = 4): `loose terminal`.** `k_step` = 3 and `k_topic` = 6.
- The anchor claims:
  - `c-d7bce12d16755797`: "Loose terminal connections are a common cause of intermittent PLC faults and should be checked during troubleshooting."
  - `c-aed289a57231c28c`: "Loose or damaged ferrules and failed push-in spring terminals account for a large proportion of intermittent input faults…"
  - `c-210c933978127214`: "Loose terminals and oxidized connections create jitter…"
- No attested sentence gives a boundary for "loose". The state is partial only because a list mention matched DEFN, a small false partial.
- A span sharpens the hypothesis: "Push-in spring terminals … can release their grip on a ferrule without looking damaged". Visual inspection is insufficient, so the discrimination is predicted to be tactile or perceptual.
- Question: contrasting cases of loose, sound and hard-to-call terminals.

**DISC, GOOD with a live alternative, GDPR v2 #3 (low, partial): `large scale`.**
- Cases are attested: `c-1db99980d97460c0`, "A hospital, but not an individual doctor, is an example of large-scale processing", and `c-387239d700df0972`.
- Factors are attested: `c-47e588c2eec6cdfb`, "you should consider the number of individuals concerned, the volume of data…".
- No boundary is attested.
- The live alternative is institutional indeterminacy, and the span says so: "the UK GDPR does not contain a definition of large-scale processing". If experts disagree on the boundary cases, the finding is `collective` and contested, and that is still worth knowing. The same shape appears in GDPR v1's #1, `high risk` (partial, `k` = 3).

**DISC, FALSE POSITIVE, GDPR v2 #1 (the only "high"): `appropriate time`.**
- The anchors are `c-4a696a73a28e2228`, "…carried out when required, at the appropriate time…", and `c-c84a6bfd3edc53fd`.
- The boundary is attested in paraphrase: `c-a3c8bac7f585866d`, "The DPIA should be conducted before the processing begins". The anchor-string closure cannot see it. This is the main limitation of DISC.

**DIAG, GOOD, PLC #2 (moderate, r = 4): rival causes of intermittent faults**, across 4 keys.
- Rivals include `c-ec36686ad589464b` (race conditions), `c-0ae2bfae93f15f20` (ground loops), `c-d7bce12d16755797` (loose terminals), loose or contaminated connectors, aliasing, and installation problems. At least 5 are unsigned.
- Signed: electrical noise, and environmental factors, whose own span says "problems appearing only in summer heat or winter cold often trace to marginal components".
- Other discriminators the ledger does hold: `c-8ae8e6a8b21edca0`, "Fault timing correlation with facility-wide events … indicates power quality issues rather than bad sensors", and `c-23aba084f2e63ad1`, "If a fault follows a cable-carrier position … inspect that physical region".
- Hypothesis: experts hold a sign-to-cause map of which the text states 2 or 3 entries.
- Caveat: the movement cue probably signs "loose connector", but lexical linking missed it.
- DIAG is silent on GDPR by design.

**SEL, FALSE POSITIVE caught by span closure, PLC.** `c-111d883494ccf58b`, "Testing should proceed from the most likely failure location toward the least likely", was open until COND gained comparatives. Its span says "the field device and wiring are far more likely to fail than the card".

**SEL, correct category for the wrong reason.** `c-5a47287dab362e5a`, "Sampling rate should be chosen according to the suspected event", is RG-SINGLE. The ledger does hold a contrast from another key: `c-e745cab599279124`, "A 1 second trend is appropriate for a tank level that drifts over an hour but inappropriate for a bit that is low for one update". It is unlinked, because "sampling" and "trend" share no stems.

**HEDGE, GOOD but lost twice.**
- GDPR v1 `c-04425373cd3694c7`, "In most cases, a combination of two factors … indicates the need for a DPIA, though this is not a strict rule", is RG-SINGLE (one key). Its span's exception is circular: "if you are confident … unlikely to result in a high risk".
- In GDPR v2 the same rule comes from WP248 (`c-4e53c658695920f0`), together with `c-36c7a706651b79fc`: "In some cases … a processing meeting only one of these criteria requires a DPIA". Which cases is never stated. This was falsely closed by "the exception in Article 35(10)" until the EXC fix. It is now HYP (low, r = 3).
- **Weak HYP:** `c-82aecb61fdbe2614`, "Where necessary, the controller shall carry out a review … at least when there is a change of the risk". The seed itself states one trigger, which EXC misses.

**GUARD, FALSE POSITIVE, PLC #3 (moderate, r = 1).**
- The seed is `c-1a4dbea5c8f1f4fe`: "Standard MOV-based surge protective devices … remain dormant during low-level transients that actually disrupt logic."
- The detection cue exists in paraphrase in the same source: `c-409133c961713218`, "Random resets leaving no trace in the fault log are classic signs of power quality degradation". It is unlinked.
- r = 1 flags the record correctly as fragile.

**GUARD, GOOD, low (r = 3).** "A common mistake in troubleshooting intermittent faults is panicking and abandoning systematic approaches in favor of quick fixes" (`k_topic` = 2). No attested claim says how a troubleshooter notices the drift. The prediction is metacognition, automated, and the channel is observation.

**WHY, FALSE POSITIVES (PLC, low).**
- `c-3217e2ac…`, "Real-time PLC data updates should occur at sub-second latency through WebSocket technology rather than polling". The span is feature copy ("Sub-second updates - WebSocket-driven live data, not polling"), so the "why" is a product claim. The ledger fields cannot detect this: kind is documentation and voice is expert.
- `c-47a2a29c52f7d738`: the rationale is the purpose clause "to identify when a repair has not resolved the underlying issue".
- **GOOD but RG-SINGLE:** `c-999231909ad2e610`, "Do not mask a power problem by increasing software delays until the electrical cause is understood". It has one key, so under the rules it is correctly not a hypothesis.

**Tally at the top of the map (the author's judgement).**
- PLC top-3: 2 GOOD and 1 FP.
- GDPR v2 top-3: 1 GOOD, 1 FP and 1 downgraded to partial by the sibling run.
- GDPR v1: its one moderate-shaped record (`high risk`) is plausible.

Precision is roughly one half. It is in-sample and unmeasured against any criterion.

## 10. Known limitations on this data

- **Lexical linking is the binding constraint.** Four of the eight examined failures are paraphrases: the element is present but unlinked. Every open state means "not found by these regexes", which is exactly what the `inferred_gap` statement says.
- **The knowledge types are extractor-assigned** and drive DIAG and GUARD eligibility, including the misconception type. GDPR v2 cue is 42 of 54 synthetic.
- **Independence keys are coarse:** 3 in GDPR v1 and 5 in v2. That caps `k_topic`, and the design then correctly returns RG-SINGLE, so GDPR yields few hypotheses. Pooling sibling runs for breadth is future work.
- **All sources are expert-voiced World A text** of kind documentation, procedure_document or standard. There is no work-as-done, no learner data, and no difficulty claims. GUARD cannot claim a learner bottleneck, and no lens can reach the L3 learner layer.
- **Some remnants are promotional.** PLC sources include vendor blogs, and no ledger field marks promotional voice.
- **The GDPR v2 run is not N3-admissible** (140 pending verdicts). The PoC runs on it anyway and says so in `gapmap.md`.
- **Areas are planner buckets** (5 per ledger), so the area cap is coarse and no area-level AUROC is possible (§14.3).
- **The lexicons are English and in-sample.** The tacitness predictions are rule-of-thumb mappings and are never criteria.

## 11. TDD build order (fixture ledgers built in tests; no real run is read by the unit tests)

1. `text.py`: tokenise, stem and STOP. Spans are included in `T` and assertions are used for firing.
2. `link.py`: common stems at 5%, the neighbourhood at 2 shared stems, and breadth by independence key. A test shows two claims with 1 evidence each from the same key give `k` = 1.
3. One test file per lens, each with 5 cases:
   - fires, stays open and becomes HYP at `k_topic` ≥ 2;
   - closed by an A neighbour's **span**;
   - synthetic-closed becomes RG-UNVER;
   - `k_topic` = 1 becomes RG-SINGLE;
   - one regression case from §8. For example: "exception in Article 35(10)" does not close HEDGE; DISC ignores "Article 35(3)"; DIAG ignores "signal".
4. `record.py`: the tier separation (an S claim has `counts_as_attestation` = false), `hypothesis.label == "inferred"`, and `gap_id` stable under claim reordering.
5. `rank.py`: merge, co-location, the caps and the control slot.
6. `checks.py`: J10, a hand-rolled Spearman with ties (checked against a hand example), the terciles and sibling matching.
7. `__main__`: two runs give byte-identical output, and `socket.socket` is patched to raise, proving there is no network.
8. A smoke test over the three real ledgers, skipped if they are missing, asserts the §8 counts.

## Implementation notes

Added after the `gapmap/` PoC package was built test-first per §11. These are places the spec
left ambiguous or, in one case, a rule that would misfire on the modal reading of its own words;
each was resolved by re-reading the surrounding construct and is recorded here rather than
silently decided in code.

- **§2.2 DIAG cause/effect split, "caused".** Read completely literally, the splitting lexicon
  `caused|due|result(s|ing)? from|stem|traceable|relate` does not match the bare present-tense
  "causes"/"cause" that actually appears in most extracted assertions ("X causes Y"), only the
  passive participle "caused" ("Y is caused by X"). This is intentional, not an omission: the
  "after = cause" branch is exactly the set of markers whose natural argument order is
  effect-then-cause (passive "caused by", "due to", "stems from", "traceable to", "relates to"),
  while active-voice "causes"/"leads to"/"produces" correctly falls to the "otherwise" branch
  (cause-then-effect), where `_split_cause_effect` puts it. An earlier draft of this
  implementation broadened "caused" to `caus\w*`, which would have flipped every active-voice "X
  causes Y" claim's cause and effect; that draft was wrong and was reverted before any lens test
  was written against it (see `lenses._CAUSE_AFTER`'s docstring).
- **§2.2 DIAG grouping (revised).** An earlier revision of this implementation read "a group is a
  seed plus its rivals" as "take connected components of the rivalry graph": any claim reachable
  from a seed through a chain of pairwise-rival edges joined that seed's group, with every member
  playing an undifferentiated "rival" role. On PLC this chained unrelated causes together through
  a shared neighbour into one large, low-precision group (e.g. one component mixing "array
  subscript out of range", aliasing, race conditions and loose terminals, none of which is a
  direct rival of more than one or two of the others) — the construct is meant to test whether
  *directly* competing causes are told apart, not whether the whole rivalry graph is connected.
  This is now read literally: a group is exactly one seed plus that seed's DIRECT rivals
  (`edge(seed, r)` true, not merely reachable), and every claim eligible for DIAG is tried as a
  seed in turn, each yielding its own (possibly overlapping) candidate group, deduplicated
  downstream by the existing `rank.merge` X-Jaccard >= 0.5 rule the spec names for exactly this
  ("overlapping groups are then deduplicated by the existing merge rule") — `diag()` itself does
  no deduplication. `seeds`/`rivals` on `Candidate` are correspondingly no longer set to the same
  set: `seeds` is the one claim that defines the group, `rivals` are its direct rivals, and
  `observed_evidence` roles are `seed`/`rival` accordingly (previously every member was "rival").
  Fixing this required two follow-on corrections: `rank._x_a`/`checks.dens` (which define `|X|`
  and the merge/ranking Jaccard from `observed_evidence` roles) had to start counting the `rival`
  role, which they did not need to before this fix since DIAG's old seed/rival split was a no-op;
  and the tacitness prediction ("perceptual added if any seed is typed cue", §2.2) now reads the
  one true seed's type directly rather than `any(... for r in group)`, which was a workaround for
  not having a distinguished seed. On the three measured ledgers the final *surfaced* HYP count by
  lens is unchanged (PLC DIAG 2, matching §8 raw run's post-merge total both before and after this
  fix) because both readings' merges collapse to the same number of representative clusters here;
  what changed is the composition of each surviving record's evidence (far fewer, tightly-related
  claims per group) and, via defect 2 below, its readability.
- **§2.2 DIAG anchor and hypothesis readability.** With a single true seed (previous note), the
  anchor is the seed's effect-clause substring exactly as spec'd ("the seed's effect clause as it
  appears in the seed assertion", trimmed to <= 80 characters at a word boundary via the new
  `text.trim`), replacing the earlier `"rival causes of " + " ".join(stems[:3])` label, which
  concatenated raw stems into fragments like "rival causes of check code controller". The
  hypothesis text lists each rival's verbatim (trimmed) cause-clause substring as one bullet,
  annotated "(attested sign)"/"(no attested sign)", replacing the earlier single run-on sentence
  that joined every rival's raw cause text with "; " (the "Practitioners tell Aliasing in data can
  be a; Ground loops..." shape). The question template's closing clause was reworded from "Think
  of the last {effect} you diagnosed" (grammatically awkward once `{effect}` is a full clause
  rather than a noun phrase) to "Think of the last time you diagnosed {effect}".
- **§4 `observed_evidence` readability cap (render-only).** A record's evidence list can run to
  dozens of `topic`-role spans (every A claim in the linking neighbourhood), which made
  `gapmap.md` unreadable without shortening the underlying data. `render.py` now shows every
  `seed`/`rival`/`closure_near` item, then at most 5 `topic` items (preferring distinct
  `independence_key`s, to keep the shown set breadth-representative rather than an arbitrary
  prefix), then a "+ N more topic claims across K keys (full list in gapmap.json)" line.
  `gapmap.json`'s `observed_evidence` is untouched — this is a Markdown rendering choice only,
  mirrored in the §7.1 checks table caveat below.
- **§3 RG-UNK rendering (render-only).** Sidecar-slot RG-UNK anchors were the raw
  `f"{probe} ({area_id})"` (e.g. "cue (a-8c10790bb9b3111b)"), and every RG-UNK record — ledger U
  claim or sidecar slot — got its own full Markdown section. `record.unk_gaps` now builds a
  readable anchor, `"<probe> slot searched, <finding> — area: <name>"` for a sidecar slot (`<probe>`
  reads as a knowledge-type label since that is literally what the sidecar's `probe` field names;
  `<finding>` is "nothing found" for `status: unknown` as the task's literal example gives, and
  "only thin coverage found" / "found but unverified" for `thin`/`unverified`, which the task's
  single example did not cover but the sidecar's own status vocabulary distinguishes) or the U
  claim's own (already-readable) assertion, both suffixed with the resolved area name rather than
  a raw `area_id`. `render.py` renders all RG-UNK records as one compact table (area, slot/
  question, source) instead of one section per slot, splitting the anchor back into columns on
  the same `" — area: "` separator it was built with. `gapmap.json` keeps the full per-record
  `Record` objects (including the readable anchor) unchanged; only the Markdown layout collapses.
- **§3/§6 retrieval-gap co-location collapse (render-only).** Two lenses firing on the same seed
  claim (§6's co-location, e.g. SEL and WHY both firing on one prescriptive assertion) previously
  produced two separate, near-identical `### [RG-SINGLE] <same anchor text>` sections in the
  retrieval-gaps listing, with no lens named in either heading. `render.py` now groups retrieval-
  gap records (excluding RG-UNK, handled separately above) by `(seed/rival claim-id set,
  category)` and renders one heading naming every lens involved (`### [SEL/WHY] <anchor> —
  RG-SINGLE`), with the shared evidence shown once and each lens's own inferred-gap/missing/
  reasoning under its own `**[LENS]**` subheading. This is a Markdown grouping only: the
  underlying `Record`s (and `gapmap.json`) are unchanged and still one per lens, so nothing here
  touches the merge/cap logic that governs the ranked map itself (§6's co-location cap-accounting
  simplification, noted further below, is unaffected and unrelated).
- **§4/§6/§7 summary block and map index table (render-only).** `gapmap.md` now opens (after the
  header) with a "## Summary" block: HYP counts by lens and confidence level, retrieval-gap counts
  by category, the control-slot count, and the §7.1 J10/Spearman numbers with their flags — all
  values already computed elsewhere and simply surfaced earlier. The "## Ranked gap map" section
  now opens with a compact index table (rank, lens, anchor trimmed to <= 60 characters, level,
  robustness, k_topic) before the existing per-record detail blocks, so a reader can scan the
  whole map before descending into any one record. Neither addition changes `gapmap.json`.
- **§4 `inferred_gap.statement`'s `n`/`n_a`/`n_s`.** The spec gives the statement's shape but not
  what exactly "scope" counts. This implementation reports `n_a = |X|` (the linking-based
  explicit part already defined in §1.4) and `n_s` = the synthetic-side scope actually searched
  by that lens's closure test (for DISC, every S claim whose `T` matches the anchor regex,
  ledger-wide as the construct requires; for SEL/HEDGE/GUARD/WHY, the S-neighbourhood computed
  the same way as the A-neighbourhood; DIAG has no S-side test, so `n_s = 0`). DIAG's own
  signing test is ledger-wide over all A claims (§2.2: "some A claim... using its span", with no
  neighbourhood restriction stated), but reporting that raw ledger-wide count as `n_a` would make
  every DIAG record cite the same large number and add no information, so DIAG reports `|X|`
  like every other lens; the signing test itself still scans the whole A pool.
- **§4 `inferred_gap.statement` wording (revised).** The original sentence
  (`"No attested claim in ledger <sha> matches <test_id> within scope <n> claims (A: <n_a>, S
  searched: <n_s>)"`) named the closure test but never the *missing element* it was testing for,
  which made every statement across every lens read identically apart from numbers and an opaque
  `test_id`. The sentence is now `"Of <n_a> verified claim(s) on this topic (<k_topic> independent
  source(s)), none states <cand.missing>. (Test <test_id>, re-runnable; <n_s> unverified claim(s)
  searched.)"` — `cand.missing` is each lens's own human-readable description of the sought
  element (already used elsewhere, e.g. render's "Missing element" line), so a reader no longer
  has to cross-reference the lens to know what was searched for. `n_a`/`n_s` keep the exact
  meaning the note above already fixed; only the surrounding prose and the now-redundant
  `ledger_sha` prefix (the ledger is already named once, in `gapmap.md`'s header) were dropped.
- **§4 `inferred_gap.closure_state` for a synthetic-closed candidate.** The field is typed
  `open|partial` only, but a synthetic-closed candidate (→ RG-UNVER) has an A-side state too.
  This implementation reports the A-only state (open or partial) in `closure_state`, and carries
  the fact that S closes it separately via a non-empty `synthetic_hits` plus `category:
  "RG-UNVER"` — the two fields are never in tension because `synthetic_hits` is only non-empty
  when `category == "RG-UNVER"`.
- **§6 control slot `category`.** The spec's schema enum for `category` is `HYP |
  RG-UNK | RG-SINGLE | RG-UNVER | RG-SIBLING`, but §6 separately describes "one extra slot... with
  a generic CDM walk-through question marked `control`" rendered in its own section, distinct
  from both the ranked map and retrieval gaps. This implementation adds `category: "CONTROL"` as
  a sixth value (not part of the map's `HYP` count, not a retrieval gap) and gives it `lens:
  null` and `hypothesis: null`, since it is not itself a missing-element test result.
- **§6 co-location "one slot".** The cap accounting (12 total, 3 per lens, 4 per area) is applied
  per record, not per co-located slot: two records from different lenses sharing a seed each
  still consume their own slot against the caps, rather than sharing one slot as §6's example
  implies. They are still detected and annotated at render time (`render._co_location_note`) so
  the map reads as co-located, but the saving in the cap accounting was not implemented. This is
  a real simplification, not a spec-error fix, called out separately from the other notes above.
- **§7.2 cross-run stability's counterpart pool.** `checks.cross_run_stability`'s
  `counterpart_category` table matches each open candidate against the sibling's own *records*
  (non-closed candidates only), so a sibling candidate that is closed shows as "no match" in that
  table. The §3 RG-SIBLING reroute itself is unaffected by this: `checks.apply_sibling` matches
  against the richer `CandidateStat` list (candidate stats include closed candidates), which is
  the mechanism that actually needs to see a closed sibling counterpart.
- **Renderer never prints a hypothesis in the indicative (§4).** *(Pre-review; superseded by F5,
  see "Post-review changes" below.)* `hypothesis.text` was originally generated from the §2
  templates verbatim, which were themselves written in the indicative ("Practitioners
  discriminate..."), so the JSON field carried indicative text under `label: "inferred"`, and
  `render.py` prefixed every printed hypothesis with "Predicted, not observed: " on the way to
  Markdown rather than rewriting the stored text. F5 (adversarial review) found this a tier leak
  in the stored JSON itself, not only a rendering concern: every lens's `hypothesis_text` now
  starts "Hypothesis (inferred):" and uses predictive modality ("practitioners are predicted
  to...") at the source, and no longer asserts what sources do or do not state (that assertion
  moved to `inferred_gap`/`reasoning`, phrased as "no verified claim in this ledger matched test
  &lt;test_id&gt;"). `render.py`'s "Predicted, not observed: " prefix is kept as a second, redundant
  visual cue in the Markdown, on top of the now-predictive stored text.

## Post-review changes (F1–F9, and the new RESULT lens)

An adversarial review of this PoC (2026-09-29) found that the gap-determination mechanism did not
beat a null: closure was decided over a tiny lexical neighbourhood, so "closed vs open" tracked
neighbour count rather than genuine textual support; §7.1's anti-renaming check was vacuous
(computed over the wrong pool, with no null); and the confidence rubric's "high" level read as
calibrated confidence when it was, in fact, breadth. The fixes below were implemented test-first,
per §11's build order, and are what the current `gapmap/` code and `research/n3/` outputs reflect;
§8 and §9's numbers are the pre-review prototype's and are marked as such above.

- **F1 (blocking): whole-pool, stem-disciplined closure.** SEL, HEDGE, GUARD, WHY and DIAG's
  per-rival sign test (and the new RESULT lens) now search their closure lexicon over **every**
  attested claim in the ledger (S for synthetic-closed), not only the lexical neighbourhood, and
  require the closing sentence to share `min(2, |seed stems|)` of the seed's own content stems --
  never a bare type-based closure (the old "neighbour typed rationale/failure_mode closes WHY" /
  "neighbour typed check/cue closes GUARD" rules are gone). §1.5 documents the rule; the
  neighbourhood still defines `X`/breadth only. DISC was already immune (ledger-wide, anchor-regex
  closure) and is unchanged by F1.
- **F2 (blocking): §7.1 made real, plus a closure null.** §7.1 now runs over lens candidates only
  (RG-UNK and CONTROL excluded, since their density cannot vary), and a new stem-scramble closure
  null (`checks.closure_null`, `random.Random(0)`, 200 draws) reports, per lens and total, whether
  the observed closed count is distinguishable from what random stems would close --
  `closure-uninformative` if not. A closure-rate-by-`k_topic`-band table is also reported. See §7.1.
- **F3 (major): confidence renamed `breadth`, never "high".** `Confidence.level` is now
  `Confidence.breadth` ∈ {`broad`, `moderate`, `narrow`}, decided by `k_topic`/`k_step` directly
  for `broad`, rendered "breadth (uncalibrated; no gold)". See §5 and the "How to read" note in
  `gapmap.md`.
- **F4 (major): DISC's bare-term definer and sibling matching.** The bare-term definer (§2.1) now
  runs over the whole A/S pool, not only claims containing the anchor bigram; a stated contrast
  (CASE) in the anchor's sentence now closes, not merely partials; DISC's sibling match (§7.2) is
  now "same term and (same head stem or the other run's head appears in this run's own anchor
  claims)", not an exact-anchor match.
- **F5 (major): tier leak in hypothesis/reasoning text.** See the Implementation-notes entry just
  above: every lens's `hypothesis_text` now starts "Hypothesis (inferred):", uses predictive
  modality, and never asserts what sources do or do not state; `reasoning` uses the same
  "no verified claim in this ledger matched test &lt;test_id&gt;" wording as `inferred_gap`. DIAG's
  per-rival annotations read "(sign test matched)" / "(sign test not matched)", not "(attested
  sign)" / "(no attested sign)".
- **F6 (major): lens guards.** WHY now requires the seed be typed `procedure_step`, `strategy`,
  `check`, `decision` or `norm`; excludes sources of kind `standard`; AUTH gained
  `authorit\w*|supervisory|dpa|ico|regulator\w*|edpb|wp29|guideline\w*`; and excludes the
  descriptive disjunction "require(s)? or (do|does) not require". GUARD now fires only when the
  assertion matches ERR **and** names a human agent or action (GUARD_AGENT, §2.7) -- misconception
  type alone no longer fires. DIAG's rivals now need 0 shared non-common cause stems **and** a
  full cause-stem Jaccard below 0.5 (catches near-duplicate causes the non-common-only check
  alone missed). A PROMO lexicon (§2.7) makes WHY/GUARD's "promotional source" alternative live
  and applies a −1 (`Q`) penalty to the confidence score (§5).
- **F7 (major, methodological): new lens RESULT.** §2.8, above -- PARI result interpretation, the
  "A → B → C, but what decides B vs D" gap.
- **F8: determinism.** Every iteration over a set/frozenset that reaches output is sorted;
  verified by running the CLI under `PYTHONHASHSEED` 0, 1 and 2 and asserting byte-identical
  output (`test_main.py`).
- **F9: questions.** Never renders an empty quote (the second quote is omitted if absent, with a
  reworded lead sentence for DISC/DIAG's two-quote templates); prefers a quote sentence containing
  the anchor/seed stems, prepending the preceding sentence when the chosen one opens with a bare
  referent ("This/These/It/They/Such"). WHY's question template is reworded (§2.6). GUARD's is
  unchanged.

## S1-S3 changes (second adversarial review, 2026-09-29)

A second adversarial review found that F1-F9's fix did not itself beat a fair null: excluding the
seed and same-source claims in both arms and drawing real stems from a random other-source
attested claim of the same knowledge type as donor, observed lexical closure was statistically
indistinguishable from the null (PLC 42 vs 40.6 [33,47]; GDPR v1 13 vs 14.1 [10,19]; GDPR v2 11 vs
8.2 [5,12]), and 13 of 15 sampled other-source lexical closures were wrong on inspection. The
reviewer's script is `fairnull.py` (kept as run evidence alongside this delivery's outputs). Lens
**FIRING** -- which seeds, anchors and rival-groups exist as candidates at all -- is unchanged by
any of S1-S3: every firing rule in §2 still applies exactly as written. What changed is **closure**
(open/partial/closed/synthetic-closed): it is no longer decided by lexical stem-overlap at all.

### S1: the semantic closure judge (`judge.py`, `semantic.py`)

- **Judge protocol.** `Judge` is anything answerable with one JSON-in/JSON-out call (`model_id`
  attribute, `ask(prompt) -> dict`). `OllamaJudge` calls `http://localhost:11434/api/chat` with
  `qwen2.5:7b-instruct` over stdlib `urllib` (`format: "json"`, `options: {temperature: 0, seed:
  0}`) -- a different model family from the extractor (anthropic) and verifier (openai).
  `CachedJudge` wraps any judge with a JSON cache file keyed by `sha256(model_id, prompt)`.
  **Replay mode** (the CLI default, no `--judge` flag) is cache-only and never opens a socket -- a
  cache miss raises `JudgeCacheMiss` naming `--judge ollama`. `--judge ollama` fills the cache from
  a live local call. The cache file is `<out>/closure_judgements.json`, committed alongside a run's
  `gapmap.json`/`gapmap.md` so anyone can replay it byte-identically. Tests use a `FakeJudge`
  (`conftest.py`): it never touches the network and closes/partials a retrieved sentence containing
  the literal marker `CLOSES_HERE`/`PARTIAL_HERE`, the judge-era equivalent of a lexical fixture
  spelling out a regex-triggering phrase.
- **Retrieval per candidate** (`semantic.retrieve`), independent of the four link-parameter
  settings so a robustness rerun's prompts -- and cache hits -- match the primary run's: every
  sentence of `T(c)` over the whole A and S pools, scored by overlap with the candidate's scoring
  stems (the seed's non-common content stems for SEL/HEDGE/GUARD/WHY/RESULT; the anchor term+head
  for DISC; one rival's own cause+effect stems for DIAG, judged per rival, see below), ties by
  claim_id then sentence index. The top 8 A and top 4 S sentences scoring >= 1 are kept, **plus**
  the seed's own evidence-span sentences unconditionally (a source stating the element in the
  seed's own span legitimately closes, per §2.2's original "r itself, using its span" rule,
  generalised here to every lens). Each retrieved sentence gets an id, `A1..`/`S1..`.
- **Prompt and state rule** (`semantic.judge_retrieval`). A short, lens-specific question (the
  literal templates in `semantic._QUESTIONS`, one per lens, DIAG's parameterised by the rival's
  cause phrase) plus the seed assertion and the numbered sentences; the judge returns
  `{"states": [ids], "partially": [ids], "reason": "<=25 words"}`. Ids outside the offered set are
  dropped and counted (`JudgeOutcome.dropped_ids`). State: any A id in `states` -> `closed`; else an
  A id in `partially` -> `partial`; else an S id in `states`/`partially` -> `synthetic-closed`; else
  `open`. Only `open`/`partial`/`synthetic-closed` ever reach a `Record` -- exactly as the old
  lexical `closed` short-circuit worked, now decided by the judge instead.
- **DIAG is judged per rival, not per group** (`semantic._judge_diag`). `diag()` (`lenses.py`) no
  longer decides "signed"/"unsigned" at all: it fires a candidate for every seed with >= 2 direct
  rivals (after S3 defect 3's pairwise dedup) and stores each rival's own non-common cause/effect
  stems (`Candidate.extra["diag_rival_stems"]`). `semantic._judge_diag` then asks one judge call per
  rival ("does any sentence state an observable sign that distinguishes ‹rival cause› from the
  other listed causes?", scored on that rival's own stems, its own span always included); a rival
  is "signed" only if its own outcome is `closed` -- `partial` and `synthetic-closed` both still
  count as unsigned, matching the old signing test's A-only, binary "signed" concept, now decided
  by the judge instead of DISCR-regex overlap. The group survives (state `open`) only if >= 2
  rivals stay unsigned, exactly reproducing the old `len(unsigned) < 2: continue` gate, but
  evaluated after judging rather than before it. `hypothesis_text`/`question_text`/`missing` are
  therefore finalised post-judge too (`lenses.diag()` leaves them blank; `_judge_diag` fills them
  from the real per-rival outcomes, `dataclasses.replace`-ing the candidate).
- **`inferred_gap.statement`, rewritten** (defect 4, revised again): "Of `<n>` verified sentence(s)
  retrieved on this topic, the closure judge (`qwen2.5:7b-instruct, local`) found none stating
  `<missing>`. Re-runnable: prompt sha `<sha>`." -- `<n>` is `outcome.retrieved_n_a`, the count of
  retrieved SENTENCES, not `|X|` claims as before S1 (S1's own instruction: the closure decision now
  comes from retrieval, so the statement should say what was actually searched). A `partial` state
  reads "found only a partial statement of `<missing>`"; a `synthetic-closed` one names the
  unverified-sentence count searched. `InferredGap` also carries `lexical_state` (the old test's
  result, comparison only), `judge_model`, `judge_reason`, `judge_prompt_sha256` and the retrieved/
  dropped counts, all re-runnable and re-checkable independent of this code.
- **`Candidate.closure_state`/`partial_hits`/`synthetic_hits` are renamed** `lexical_state`/
  `lexical_partial_hits`/`lexical_synthetic_hits` throughout `lenses.py` -- the lexical test
  (`_lexical_state`, formerly `_closure_state`; `_disc_lexical`, formerly `_disc_closure`) is
  unchanged in its own logic and is still computed and stored, but purely for comparison (S2's
  judge-vs-lexical confusion table) and the S2 lexical donor null below; it decides nothing.
  `include_closed` is gone from every lens function: firing and closure are now fully separate
  stages, so a lens always emits one `Candidate` per fired construct and the judge (downstream)
  decides whether a `Record` gets built from it at all.
- **Robustness (§1.4) is measured lexically, not re-judged.** The 4 robustness settings' candidates
  are categorised by `lexical_state` (`__main__._lexical_category`), not judged: retrieval/prompts
  are independent of `common_cut`/`shared_threshold` by design (this section, "Retrieval per
  candidate"), so a judged robustness rerun would just re-ask the SAME SETTING_1 question with a
  different `x_a` membership underneath it -- lexical reproducibility of the underlying construct
  is what `r/4` always measured, and re-judging 4x would roughly quadruple the live-call cost for a
  number that would not, by construction, differ from a judged version. This is a scope trade-off,
  not a hidden default -- recorded here rather than silently decided in code, per this file's own
  convention.

### S2: built-in informativeness checks (§7.1)

Both checks below replace the F2 stem-scramble closure null entirely (`checks.closure_null` no
longer exists); §7.1's `gapmap.md` section is retitled accordingly. Numbers for the three ledgers
are in `research/n3/README.md` and each `gapmap.md`, not reproduced here (S2's own instruction:
they drift with every lexicon or model change and would otherwise go stale the way §8/§9's did).

- **Mismatched-evidence control** (`checks.mismatched_evidence_control`). For every lens candidate,
  the same judge is asked the same question with the retrieved evidence of a DIFFERENT same-lens
  candidate (`semantic.primary_probe` gives one representative probe per candidate -- for DIAG, its
  first rival by claim_id stands in for the group; deterministic pairing by `gap_id`, cyclic;
  lenses with < 2 candidates are skipped). `closure-uninformative` unless the own-evidence closure
  rate exceeds the mismatched rate by >= 0.20 absolute AND the mismatched rate is <= 0.30.
- **Lexical baseline** (`checks.lexical_donor_null`), the reviewer's fair donor null reimplemented
  for the (now-comparison-only) lexical closure test: self and same-source claims excluded from
  both the observed and the null arm; donor = the real non-common content stems of a random
  other-source A claim of the same knowledge type as the seed; one `random.Random(0)` per run,
  `CLOSURE_NULL_DRAWS` (200) draws per candidate. This is what documents why the lexical test was
  replaced -- it is reported, not used for anything downstream. DISC is excluded (anchor-regex, not
  stem-overlap); **DIAG is handled per its own closure unit**, one rival's sign test (its
  `cause_stems`, DISCR pattern) rather than a group-level candidate, matching S1's per-rival design
  above.
- **Fixed flag logic.** A check now "passes" (is informative, not `closure-uninformative`) only if
  the observed count is STRICTLY ABOVE the null's 5-95% interval. The earlier F2 logic flagged only
  `lo <= observed <= hi`, which never caught an observed count BELOW the null (worse than chance) --
  fixed to `observed <= null_hi`, i.e. "at or below" fails, in both `anti_renaming`'s (removed) null
  and this one.
- **Judge-vs-lexical agreement** (`checks.judge_lexical_confusion`): confusion counts,
  `<lexical_state>-><judge_state>`, over every judged candidate (`CandidateStat.lexical_state`),
  rendered in `gapmap.md` and reported in the delivery.

### S3: other genuine defects from the review

1. **PROMO is an exclusion for every lens** (`lenses.promo_blocked`), not only a WHY/GUARD
   alternative/penalty (F6, kept unchanged and now largely dead in practice -- see the note below).
   A seed whose `T` matches the expanded PROMO lexicon (adds `we replaced|with \w+ we|our
   (customers|team)|the agent (selects|decides)|ai agent`), or whose evidence source's bare domain
   (`text.domain`, `urllib.parse`) is in `config.PROMO_DOMAINS`, does not fire; the exclusion count
   is logged (`lenses.promo_excluded_count`, rendered in `gapmap.md`'s Summary). `PROMO_DOMAINS` =
   `plclogs.com` (the testimonial: "We replaced three separate monitoring tools with PlcLogs..."),
   `capafy.ai`, `peakboard.com`, `csintegrators.com` (the "Edge" appliance copy) -- the exact PLC
   ledger identifiers the reviewer named, found by grepping the PLC ledger's source identifiers.
   Because a candidate whose `T` matches PROMO is now excluded before it can become a `Candidate` at
   all, F6's WHY/GUARD "promotional source" alternative/`Q` penalty (§5, §2.5, §2.6) almost never
   fires on a surviving candidate any more (the same regex, checked at the same scope, already
   excluded it) -- kept rather than removed, since the spec does not ask for its removal and a
   domain-only exclusion (T-regex silent, domain listed) is still theoretically distinguishable.
2. **RESULT fires only on a prescriptive test** (`lenses._result_prescriptive`): MODAL, or an
   imperative sentence opening with the TEST verb -- never descriptive or precondition text. A new
   exclusion, `only (be )?performed when|before using`, is checked first and wins over MODAL (so
   "should only be performed when a circuit is de-energized" never fires, MODAL notwithstanding).
3. **DIAG dedupes rivals pairwise** (`lenses._dedupe_rivals`), after `_direct_rivals`: a rival whose
   cause-stem Jaccard with an already-kept rival is >= `DIAG_CAUSE_JACCARD_MAX`, or which shares a
   non-common cause stem with one, is dropped, using the exact same test `rival_edge` already
   applies between seed and candidate (harmonic/harmonics-type plurals are already folded by the
   existing suffix stemmer, §1.3, so no separate normalisation was needed here). The anchor is now
   the seed's full effect clause, never `text.trim`-truncated (a group's anchor can now run past 80
   characters; `test_anchor_is_the_full_effect_clause_never_trimmed` covers this).
4. **Stems: `failure`/`failures` fold to `fail`** (`config.IRREGULAR_STEMS`, checked first in
   `text.stem`), so a claim's "fail" and a corroborating span's "failure" share a stem. This is
   deliberately a small hardcoded pair, not a general `-ure -> base` rule: a blanket suffix (e.g.
   `pressure -> press`) risks conflating unrelated words exactly the way this whole review is about
   (a "press the reset button" claim would share a stem with an unrelated "check the pressure gauge"
   claim) -- the general rule the spec sketches ("where the base is a known stem in the ledger")
   would need ledger-wide vocabulary threaded through every `text.stem`/`text.cw` call site, which
   was judged not worth the blast radius for the one concrete case asked for.
5. **DISC: `DEFN` gains `concerns?`; a small stop-list of non-discriminations.**
   `config.DISC_STOP_ANCHORS` = exactly `{"appropriate time", "sensitive control"}` -- an anchor in
   this set never fires. **This list is in-sample**, chosen by inspecting these three ledgers' DISC
   output (the same in-sample status every lexicon/threshold in this PoC already carries, §0's
   warning); it is not a general "temporal frame" or "adjective+generic-noun" detector.
6. **Questions never use a testimonial; bare-referent fix crosses span boundaries**
   (`lenses._pick_quotes`, `lenses._best_sentence`). A claim sourced from a `PROMO_DOMAINS` domain
   is skipped when picking a quote, regardless of whether PROMO-exclusion already kept it from
   firing as a seed (this covers DIAG's rivals, which are never seed-firing-gated themselves).
   `_best_sentence` now flattens ALL of a claim's evidence spans (in evidence order) before picking
   the best-scoring sentence, so a bare-referent sentence ("This/These/It/They/Such...") that opens
   its OWN span can still be prepended with the end of a PRECEDING span, not only a preceding
   sentence within the same span; if there is no earlier sentence anywhere, it falls back to the
   claim's assertion (previously: no fallback at all when the bare-referent sentence was a span's
   first).
7. **Records are presented as "gap candidates."** The rendered heading is "## Ranked gap map
   (candidates)"; `gapmap.md`'s "How to read this map" note adds: precision against a human
   criterion is unmeasured (there is no gold yet), and the judge's own informativeness is what §7.1
   measures instead (S2, above). The hypothesis tier's `label` stays `"inferred"` (§4): no schema
   change, a rendering and prose change only.

### Implementation notes (S1-S3)

Resolutions of ambiguities this round's spec left open, in the same spirit as the notes above.

- **DIAG's `lexical_state` field is a fixed placeholder, not a real per-group lexical result.**
  Because DIAG's real closure unit moved to "one rival's sign test" even before S1 (§1.5's F1), the
  group-level `Candidate.lexical_state` was already a non-informative `"open"` constant, unused by
  anything except the categorisation short-circuit it no longer performs. It is left as `"open"` for
  schema uniformity (every `Candidate` has the field); DIAG's real lexical comparison lives in the
  S2 lexical donor null, which reads `Candidate.extra["diag_rival_stems"]` directly rather than
  `lexical_state`.
- **The mismatched-evidence control's DIAG probe is one rival, not the whole group.** S2 asks for
  "the retrieved sentences of a different candidate of the same lens"; DIAG's per-candidate unit is
  a *group* of judge calls (one per rival), which has no single "retrieved sentences" set. Rather
  than inventing a group-level aggregate retrieval with no natural question to pair it with,
  `semantic.primary_probe` picks the group's first rival (by claim_id) as a stable, deterministic
  stand-in probe for the whole candidate, on both the "own" and "mismatched" side of the pairing.
  This under-tests DIAG's control relative to the other six lenses (only one of possibly several
  rivals per group is checked), a real limitation recorded here rather than silently narrowed.
- **`--judge` has exactly one live value, `ollama`.** The spec's CLI sketch (`[--judge ollama]`)
  reads as a flag with one meaningful setting rather than a general judge-selector; `argparse`
  enforces `choices=["ollama"]` rather than accepting an arbitrary string, so a typo fails fast
  instead of silently falling back to replay mode.
- **`CachedJudge`'s `save()` is called once, at the end of `__main__.run`,** not after every
  candidate: a crash mid-run loses that run's new cache entries (they are recomputed on retry, at
  the cost of re-asking the model), trading crash-safety for not repeatedly rewriting a cache file
  that can grow to hundreds of entries per ledger.

## Final fix round (narrow, 2026-09-29b)

A third, narrow pass fixed five specific defects the second adversarial review's own follow-up
scratch scripts surfaced (`audit.py`'s fair own/mismatched-arm construction, `intids.py`'s
int-id probe -- kept as run evidence alongside that review, not committed here) -- test-first, no
prompt tuning, no lexicon tuning, and no attempt to make any check pass. Lens **firing** is
unchanged by any of these five; what changed is closure parsing (fix 1), one check's construction
(fix 2), and three display-only details (fixes 3-5).

- **Fix 1 (blocking): the silent id-drop bug.** The judge often cited bare integers (`[3, 8]`)
  against the old `A3`/`S1`-prefixed ids `semantic.judge_retrieval` offered, which dropped every
  such citation as unrecognised and fell through to `open` -- a real answer silently misread as no
  answer. `semantic._assign_ids`/`build_retrieval` now number every offered sentence with one
  single bare-integer scheme, 1..N across BOTH the A and S pool (never `A<n>`/`S<n>`); the model is
  shown only the numbers, and `judge_retrieval` resolves a cited entry as an int or a numeric
  string. If the JSON is unparseable (`judge.ask` returns `None`, `OllamaJudge`'s own sentinel for
  a model reply that did not parse as JSON, or raises) or any cited id cannot be resolved to one of
  the offered numbers, the state is `undecided` -- never `open`. A `JudgeCacheMiss` is re-raised,
  not swallowed, so replay mode's cache-miss error still surfaces. `record.categorize` routes
  `undecided` to a new category, `RG-UNDECIDED` (`record.py`'s `Category`/`InferredGap.closure_state`
  literals gain the value), rendered with action "re-judge or inspect", never "ask an expert"
  (`render._RG_ACTION`). DIAG's per-rival judging (`semantic._judge_diag`) propagates an undecided
  rival up to the group: the aggregate state is `undecided`, not silently `open`, if any rival
  counted toward "unsigned" was itself undecided. Because the prompt text changed (the new
  numbering), every cache key changed; all three ledgers were re-run live (`--judge ollama`,
  Ollama `qwen2.5:7b-instruct`) and replayed byte-identical before being committed. Measured: 0 of
  the 662 live judge calls across the three ledgers came back with a non-integer citation or an
  unresolvable id (every citation was a bare int, never a numeric string, confirming the bug
  report's own diagnosis); a further, narrower case was found live and fixed alongside this one
  (below) rather than left to surface as `undecided` in the committed output. Tests:
  `gapmap/tests/test_semantic.py` (an integer-id response, a string-integer response, an unknown
  id, malformed JSON, a raising judge, a `JudgeCacheMiss` that must still propagate, `categorize`
  routing), plus DIAG-, record- and render-level integration tests for the `RG-UNDECIDED` path.
  - **A second, related defect found live, fixed in the same commit.** The S2 fair control's
    "other-source-only" arm (fix 2, below) can legitimately retrieve nothing at all (no
    non-seed-source sentence scored) -- and, live, asking the judge a question with zero offered
    sentences produced a hallucinated citation against an empty offered set on 10 (GDPR v1) and 8
    (GDPR v2) of these calls, which fix 1's own rule correctly turned into `undecided` rather than
    a wrong `open`. Since an empty retrieval is unambiguously `open` by construction (there is
    nothing it could state), `semantic.judge_retrieval` now short-circuits to `open` without
    calling the judge at all when both pools are empty, rather than asking an unanswerable
    question and risking (and, live, getting) a hallucinated citation. This changes no committed
    `gapmap.json`/`gapmap.md` byte (`_closed_or_partial`, the only consumer of these particular
    outcomes, already treated `undecided` and `open` identically), only which cache entries exist;
    the 18 now-unreachable entries (10 + 8) were pruned from `research/n3/{gdpr_v1,gdpr_v2}`'s
    committed caches. Test: `test_empty_retrieval_is_open_without_calling_the_judge_at_all`
    (a judge that asserts if asked at all).
- **Fix 2 (blocking): the fair mismatched-evidence control.** The first S2 control (a prior
  revision of this file) was itself a straw man: the own-evidence arm always carried the seed's
  own sentences while the mismatched arm never did (17 of PLC's 22 old closures cited only the
  seed or its own source), and the mismatched sentences were topically off-topic (cyclic gap_id
  pairing). `checks.mismatched_evidence_control` is rewritten: in BOTH arms the seed's own
  sentences are kept; the OWN arm adds this candidate's own retrieved non-seed-source sentences;
  the CONTROL arm replaces those with the non-seed-source sentences retrieved for the topically
  nearest OTHER candidate of the same lens (max seed-stem Jaccard over each candidate's
  `semantic.primary_probe` scoring stems, ties by gap_id -- `checks._nearest_other`). A third
  figure, "other-source-only", is the OWN arm with the seed and same-source sentences excluded
  entirely (`checks._rows`/`semantic.build_retrieval` splice retrievals together for all three
  arms) -- how often an independent source alone closes it. `closure-uninformative` now fires
  unless `own_rate - control_rate >= 0.20` (the old, additional `mismatched_rate <= 0.30` clause is
  gone with the straw-man arm it protected). Rendered per lens and total
  (`render._mismatched_evidence_control_lines`); the old "mismatched rate" wording and field name
  are gone everywhere. **Measured result, all three ledgers, every lens: `own_rate` equals
  `control_rate` exactly** -- PLC total 0.89 = 0.89 (by lens: DIAG 1.00=1.00, RESULT 1.00=1.00, SEL
  1.00=1.00, WHY 0.75=0.75); GDPR v1 total 0.96 = 0.96; GDPR v2 total 0.96 = 0.96 -- so every lens
  and both totals are flagged `closure-uninformative`, and `own - control` is 0 in every single
  row, not merely under the 0.20 bar. The "other-source-only" figure is consistently lower than
  the own/control rate wherever the two are not both 1.00 (e.g. PLC WHY 0.38 vs 0.75; GDPR v1 DISC
  0.31 vs 1.00; GDPR v2 DISC 0.36 vs 1.00, HEDGE 0.80 vs 0.60 the one case it is higher). Read
  plainly, not charitably: the judge does not beat this fair control anywhere in these three
  ledgers -- closure tracks the seed's own stated text (present in both arms, by the fix's own
  design) far more than it tracks which independent evidence is spliced in alongside it, own or
  borrowed. This is a materially different, more specific finding than the straw-man control could
  have shown, and it survives the fix that was supposed to give the judge a fair chance to
  disprove it. Tests: `checks._nearest_other`'s max-Jaccard/tie-break rule in isolation, same-source
  exclusion from the "other-source-only" arm even when marked, a judge that closes on anything
  (own = control = 1.0 always, by construction, since both arms always carry the seed), and a
  3-candidate construction proving the flag CAN read informative (own - control >= 0.20) when the
  pairing structure allows it -- the universal tie above is a property of this data, not of the
  check being unable to discriminate.
- **Fix 3 (minor): lexical robustness.** `r/4` (§1.4) is measured across the 4 link-parameter
  settings on the LEXICAL construct, never re-judged -- so a record the judge closes, or leaves
  open, can show a low or `0/4` robustness with no tension between the two numbers. Every rendered
  occurrence (`render._confidence_lines`'s per-record line, `render._map_index_table`'s column
  header) now reads "lexical robustness", and a new "How to read this map" paragraph says plainly
  that it is not re-judged and the two numbers answer different questions.
- **Fix 4 (minor): DIAG anchor.** The anchor was the raw effect-side substring `_split_cause_effect`
  returns, which starts exactly at the CAUSE marker's boundary and so can open mid-sentence on a
  bare preposition when an independent clause precedes the marker (measured: "Loose terminal
  connections are a common cause of intermittent PLC faults and should be checked during
  troubleshooting" split into the fragment "of intermittent PLC faults and should be checked
  during troubleshooting", no subject). `lenses._diag_anchor` (new) anchors on the FULL sentence
  containing the marker instead (`text.sentence_containing`, new), trimmed at a word boundary to
  <= 80 characters (`text.trim`); if the effect side itself has < 3 content words, it falls back to
  the whole (trimmed) seed assertion. This reintroduces the trim that an earlier revision (S3
  defect 3) deliberately removed for the OLD, narrower "just the effect substring" anchor;
  `test_lens_diag.py`'s regression test for that removal is rewritten
  (`test_anchor_is_the_full_sentence_trimmed_to_80_chars_at_a_word_boundary`) to assert the new
  <= 80-character, full-sentence behaviour, and a new regression test reproduces the exact
  motivating fragment above and asserts the anchor no longer opens with "of ".
- **Fix 5 (minor): fragment quote fallback.** `lenses._best_sentence` could return a genuine
  sentence-fragment quote (e.g. "retention periods;") when that fragment scored highest against
  the question's relevance stems. It now falls back to the claim's own (always full-sentence)
  assertion whenever the chosen quote, after the existing bare-referent fix, is under 5 words
  (`_WORD.findall`, already used for DISC's anchor tokenisation). Test: `gapmap/tests/test_quotes.py`.

**Live-run accounting.** All three ledgers were re-run live end to end for this round (fix 1 changed
every judge prompt's text): PLC 6m41s (193 judge calls), GDPR v1 8m49s (240 calls, 11 pruned after
fix 1's empty-retrieval short-circuit made them unreachable), GDPR v2 8m34s (229 calls, 10 pruned) --
about 24 minutes and 662 live calls total. Each domain was then replayed in the default (no
`--judge`) cache-only mode and diffed byte-for-byte against the live run's own output, both before
and after the cache pruning; all six files (`gapmap.json`/`gapmap.md` x3) were identical both times.
`research/n3/{plc,gdpr_v1,gdpr_v2}/gapmap.json`, `gapmap.md` and the pruned `closure_judgements.json`
are the committed result of this round; `research/n3/README.md` is unchanged (out of this round's
scope) and its numbers should be read as pre-dating fix 1-5, same caveat as §8/§9 above.
