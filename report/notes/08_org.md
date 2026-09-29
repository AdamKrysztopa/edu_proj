# World B: organisational and industrial knowledge

Evidence labels follow the report's hard rule: ESTABLISHED LITERATURE, OBSERVED IN THE PoC,
INTERPRETATION, HYPOTHESIS, FUTURE WORK. "PoC" below means the N3 methodology-guided gap map
(`gapmap/`, `research/n3/`), run on two demo domains built from **public** text (PLC
troubleshooting forum/manual material, and the Article 29 Working Party's WP248 guidance on
DPIAs). Its own closeout says the closure step is not informative against a fair control and
precision was 3 of 19 strict by adversarial judgement. Nothing below claims the PoC has run on
real organisational data, and nothing below claims it identifies real tacit knowledge.

## 1. Three concrete organisational blind spots

**A maintenance technician's diagnostic cue.** Orr's ethnography of photocopier repair
technicians found that diagnosis proceeds through a *narrative process*: technicians build a
coherent story of the failing machine, and that story, not the service manual, is what
circulates and keeps the group's diagnostic knowledge current. The manual describes the machine
as designed; the war story describes the machine as it actually fails (Orr 1996). Brown &
Duguid's reading of the same fieldwork frames this as knowledge held by a *community of
practice*, not by individuals or documents (Brown & Duguid 1991). ESTABLISHED LITERATURE. The
PLC demo in `research/n3/plc/gapmap.md` produced a candidate of the same shape: a GUARD-lens
record built on the span "a common mistake … is panicking and abandoning systematic approaches",
where no source says how a troubleshooter notices the drift. OBSERVED IN THE PoC (candidate, not
validated) that a lens can flag this *kind* of gap in text; whether the flagged item is real
tacit knowledge is untested.

**A senior engineer's review heuristics and design rationale.** Szulanski's study of 122
practice transfers in 8 firms found that the largest barriers to transfer were the recipient's
absorptive capacity and **causal ambiguity** — not knowing *why* a practice works — while
source motivation mattered less than folk theory suggests (Szulanski 1996). In software, this
shows up as commits and configuration changes with no issue, PR or ADR explaining the reasoning;
LLM extraction of that rationale from commits and issues has high recall but low precision (about
0.27 precision, 0.7 recall in one 100-problem study; 64–69% of extracted arguments were not
mentioned by the human experts) (Zhou, Li & Liang 2025, cited via the repo's organisational
note; not independently re-verified in this pass). ESTABLISHED LITERATURE for the barrier;
INTERPRETATION for the software framing.

**A compliance officer's exception judgement.** Regulatory guidance is written in hedges: WP248
says a DPIA is needed "in most cases" when two screening criteria are met, and "in some cases"
when only one is met, without saying which cases. Hollnagel's work-as-imagined vs. work-as-done
distinction is the general frame: the written rule is the imagined process, and the officer's
case-by-case judgement of which single-criterion cases still warrant a DPIA is the work actually
done (Hollnagel 2018). ESTABLISHED LITERATURE. The GDPR v2 demo's best-rated HEDGE record is
built on exactly this WP248 sentence. OBSERVED IN THE PoC (candidate, not validated) — the run
is flagged not N3-admissible (140 pending verdicts) and the closure check that would confirm the
boundary is genuinely unstated is uninformative against a fair control.

## 2. World B evidence vs. World A

World A (Track A physics, and the public text N3 used) is expert-voiced explanation: textbooks,
papers, curated guidance documents — work-as-imagined, written to be read. World B is
organisational trace: SOPs and runbooks (imagined), but also tickets, incident reports, commit
history, code review threads, chat, work orders and postmortems (done). Doc-vs-practice
divergence is the World-B-specific signal that World A public text cannot show at all, because
public text has no paired execution log (Hollnagel 2018; no public SOP-plus-execution-log
corpus was found in the repo's organisational note). ESTABLISHED LITERATURE for the concept;
FUTURE WORK for a benchmark.

World B evidence differs from World A in three practical ways this pipeline must handle
differently:
- **Access control.** World A text is public by construction. World B artefacts are internally
  scoped — retrieval must enforce per-user ACLs, and every reconstructed claim needs provenance
  a reader can check against their own access (HYPOTHESIS: no existing enterprise RAG evaluation
  was found that scores ACL-respecting retrieval against a held-out knowledge criterion; Gao et
  al. 2023's survey and the RAGAS evaluation framework (Es et al. 2024) evaluate retrieval and
  answer quality, not access-scoped provenance).
- **Confidentiality and IP.** Company artefacts are the firm's property; ingesting them for a
  third-party tool, or sending them to an external API, is a data-handling decision the org
  itself must control (see §5).
- **Personal-data exposure.** Git blame, review participation and chat authorship are the raw
  material for *concentration* scoring (who is the only person who understands this), and that
  is simultaneously personal-data processing about identifiable employees (§5, §6).

## 3. How the pipeline would apply

The N2/N3 pipeline (reconstruction → explicit-knowledge extraction → methodology lenses →
closure judge → ranked gap map → prioritised questions) is domain-neutral by construction
(decision 0006 moved reusable components into `residual/`). Applying it to World B is FUTURE
WORK requiring three changes, none built or tested:

1. **Retrieval over a private corpus, not the open web.** N2's reconstruction step currently
   retrieves public sources; a World B run needs an indexed, access-scoped corpus (SOPs, tickets,
   Git history, ADRs, incident reports) with per-document ACLs carried through to every claim's
   provenance. Enterprise RAG survey literature describes the retrieval architecture (Gao et al.
   2023); RAGAS-style automated evaluation (Es et al. 2024) is a candidate harness for grading
   whether retrieved context actually supports generated claims, but neither addresses
   permission-aware retrieval directly. HYPOTHESIS.
2. **On-prem or contractually isolated LLMs.** The confidentiality of World B artefacts likely
   forecloses sending them to a third-party API by default; the gap map's own closure judge
   already runs against a local Ollama model for this reason (`gapmap/src/gapmap/semantic.py`),
   which is a precedent for the pattern, not evidence it works on organisational text (OBSERVED
   IN THE PoC that a local judge is technically viable; its closure judgements were not
   informative against a fair control on the two demo domains).
3. **Gap map → question prioritisation → residual capture**, unchanged in shape from N3: lenses
   fire on constructs whose content is attested but missing, a judge assesses whether the gap is
   genuinely unclosed elsewhere in the corpus, and the ranked output becomes a short list of
   targeted questions for a named or pseudonymised expert. What is untested for World B
   specifically: whether the lenses (built against CTA/PARI/GOMS-style methodological
   constructs) fire usefully on ticket and commit text rather than expert prose, and whether
   closure against a private corpus is any more informative than the public-text closure step
   that failed its control. FUTURE WORK.

## 4. Value propositions for an industrial partner (stated soberly)

| Proposition | Literature grounding | Evidence status of *our system solving it* |
|---|---|---|
| Onboarding acceleration | Newcomer barriers in OSS include documentation problems, from a review of 878 artefacts (Steinmacher et al. 2015) | HYPOTHESIS — untested that a gap map shortens onboarding |
| Retiring-expert knowledge capture | Retention frameworks (DeLong 2004) and nuclear-industry practice (TVA/IAEA attrition × position-criticality scoring) treat this as a real, prioritised risk; both rest on case studies and practitioner argument, not effect sizes | HYPOTHESIS — no validated method converts an artefact gap map into capture priority; DeLong's own framework is solution-oriented, not measured |
| Turnover-induced knowledge loss (quantified) | Established at scale only in software: 65% of 133 popular GitHub projects have a truck factor ≤ 2 (Avelino et al. 2016); losses over 3× expected by Knowledge-at-Risk / Expected Shortfall, replicated with more severe extremes (Rigby et al. 2016; Nassif & Robillard 2017); 315 of 1,932 projects (16%) abandoned after truck-factor developers left (Avelino et al. 2019) | ESTABLISHED LITERATURE that the risk is real and measurable in software specifically. HYPOTHESIS that an artefact-coverage score adds predictive value beyond authorship-only concentration — this is exactly what E-OSS (REORIENTATION.md §22) is designed to test, and it has not run |
| Troubleshooting / diagnostic support | Diagnostic knowledge circulates as narrative among practitioners, not in manuals (Orr 1996) | HYPOTHESIS — untested whether a reconstruction-plus-gap-map surfaces the missing cue rather than just the documented procedure |
| Audit and regulatory defensibility | Doc-vs-practice divergence has a mature theoretical frame (Hollnagel 2018) and a mature computational one in process-mining conformance checking for event logs, but nobody has joined that to prose SOPs, and no public SOP-plus-execution-log corpus was found | FUTURE WORK — no benchmark exists to validate an SOP-vs-record divergence detector against |

No credible, peer-reviewed dollar figure for the cost of knowledge loss was found in the repo's
prior research pass, and none is asserted here.

## 5. Candidate organisational pilot design

**Partner type (Recommended).** A software engineering organisation of moderate size (tens of
engineers) with an internal Git repository, issue tracker, code review history and some ADRs —
closest in kind to the already-registered E-OSS design (REORIENTATION.md §22), which lets the
pilot reuse a pre-specified analysis rather than inventing one. An industrial-maintenance
partner (PLC/SCADA fault diagnosis, matching the N3 PLC demo domain) is the stronger long-run
target for the diagnostic-cue value proposition, but has no natural-experiment structure as
clean as developer departure, and MaintIE/MaintNet-style text is terse and jargon-heavy, which
the repo's own notes flag as a low-support domain for reconstruction. Start with the software
partner; treat the maintenance partner as a second-wave target once the method is shown to work
at all.

**Domain and data.** Git history, code review comments, the issue tracker, and ADRs where they
exist, all dated. No private chat or personal messages without separate, explicit consent.

**What is measured.** Freeze the corpus at a date *t* shortly before a known or planned
departure or internal transfer of a senior contributor. Compute the gap map and a concentration
score per component from artefacts dated ≤ *t* only. After departure, blind-code post-*t*
"why is this like this" issues and defect-fix commits per component. Compare the gap map's
ranking against the strongest available baseline (raw truck factor, churn, doc-link density) —
the same comparison structure as E-OSS.

**Success / failure.** Success: the gap map's ranking predicts post-departure trouble
better than the strongest baseline, by a pre-registered margin, matching E-OSS's stop rule
logic. Failure: it does not beat the baseline, in which case the artefact-coverage axis adds
nothing beyond what authorship-based concentration already captures — this would be informative
even though negative, and mirrors N3's own honest failure on closure.

**Ethics and data protection.** A DPIA under GDPR Art. 35 is required because per-person
concentration scoring is systematic processing of identifiable employees' work; the legal basis
is legitimate interest under Art. 6(1)(f) with a documented balancing test, not consent, which
is generally invalid in an employment relationship (WP29 Opinion 2/2017). If the pilot involves
a German entity, a works council agreement is required before deployment, because a system
*objectively capable* of assessing performance is co-determined under § 87(1) no. 6 BetrVG
regardless of stated intent. The pilot must not feed task allocation, promotion, or performance
evaluation, to stay on the safer side of AI Act Annex III(4)(b) and within the Art. 6(3)
derogation for systems that merely detect patterns without replacing human assessment; those
Annex III obligations apply from 2 December 2027 under the Digital Omnibus deferral. Outputs
should default to aggregate or pseudonymised concentration scores, with named attribution only
by the individual's own consent. Company artefacts remain the firm's IP; a written agreement
must specify that ingested text is not used to train any model outside the engagement, and that
processing is on-prem or under a data-processing agreement equivalent to it.

## 6. Risks specific to organisations

**Goodhart on documentation.** If a coverage or residual score becomes a target metric — for a
team, a promotion case, or an audit — the response most available to people is to write
documentation that raises the score, not documentation that conveys the missing knowledge. This
is the software-engineering-scale evidence problem already visible in the literature: a
162-type taxonomy of documentation issues found outdated, incomplete and inconsistent
information to be the dominant failure modes even without any scoring pressure at all
(Aghajani et al. 2019). Turning coverage into a KPI would very plausibly increase the rate of
by-the-letter-but-hollow documentation, which is Goodhart's law applied to knowledge management
rather than a citable empirical study of it. INTERPRETATION.

**Expert resistance and ownership of knowledge.** The intuitive story is that experts withhold
knowledge because it is their leverage. Szulanski's evidence runs against the strong form of
that story: motivation was a smaller barrier to transfer than absorptive capacity and causal
ambiguity (Szulanski 1996). The more defensible risk is not hoarding but **surveillance
framing**: a system that infers "only Ana understands the flare system" from her Git and review
history is doing exactly the processing that GDPR's legitimate-interest test and Germany's
co-determination law were built to check, whether or not that was the intent. If deployed
without the safeguards in §5, it will read to staff as a covert performance-monitoring tool, and
that framing risk is itself sufficient to block adoption or trigger a works-council veto, apart
from any technical result. INTERPRETATION.

**Confidentiality and injection exposure.** Every ingested internal document a retrieval system
serves back to a user is also a channel an attacker or a careless internal author can use to
plant instructions; indirect prompt injection through retrieved content is a demonstrated attack
class against real LLM-integrated applications (Greshake et al. 2023). A World B deployment
that retrieves from tickets, chat exports and commit messages has a much larger and less curated
attack surface than a World A pipeline reading public papers. ESTABLISHED LITERATURE for the
attack class; INTERPRETATION for its severity in this specific pipeline shape.

**Misuse of concentration scores.** A per-person concentration or "irreplaceability" score is a
short step from a redundancy-targeting or performance tool, which is precisely the AI Act
Annex III(4)(b) and German co-determination trigger the pilot design in §5 is built to avoid.
The mitigation is a governance decision (aggregate by default, consent for naming, no evaluation
use), not a technical one, and it has to be enforced by contract, not by the pipeline's own good
intentions. INTERPRETATION.
