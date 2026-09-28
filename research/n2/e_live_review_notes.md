# E-LIVE review and post-N2a architecture review

Reviewer: E-LIVE Research Reviewer (read-only on code). Date: 2026-09-28. Branch `n2`.
Inputs: run (a) `reconstruct/runs/20260928T133336Z-59ec876b3d7e/` (PLC intermittent faults) and run (b) `reconstruct/runs/20260928T135354Z-eb840a85b7d1/` (GDPR DPIA; complete, `verify_run` ok, $0.50). Run (b) is reviewed in its own section below.
Sampling used my own seeds:
- (a), `random.Random("e-live-reviewer-2026")`: 4 supported claims per area = 20; all 49 synthetic claims; all 20 decoys; all 50 disagreements; all 35 sources.
- (b), `random.Random("e-live-reviewer-b")`: 10 supported claims; all non-compatible disagreements; all scope and false-accept decoys; all 20 sources and 18 fetch failures; all 55 unlocated quotes.

## Verdict

**N2a accepted with fixes. Neither E-LIVE run is valid N3 input.** The provenance core works as designed in both domains: every `Selector.exact` re-slices from its snapshot, and spans, verdicts and labels can be inspected. What sits on top of that core does not yet produce a signal N3 can use:
- HTTP error pages are counted as sources in both runs.
- Corroboration is structurally zero in (a), and independence is wrongly collapsed in (b).
- The verifier passes scope drift in (a) at about 1 in 5, and and/or swaps in (b).
- The single ledger contradiction in (b) is a false positive.
- 9 of the 19 frozen AreaFeatures come out constant.

## Headline findings (run a)

| Finding | Evidence |
| --- | --- |
| 11 of 35 "sources" are HTTP 403/429 error pages; 3 more are empty 200s and 5 are bot walls or app shells | sidecar `status`: 403 ×10, 429 ×1. Snapshots: MDPI ×3 "Access Denied", ScienceDirect "There was a problem providing the content", Vercel "We're verifying your browser", studylib ×2 login shell, exa.ai ×2 marketing shell; industrialmonitordirect ×4, atecentral and dl.acm.org have 0 characters. **14 of 35 sources yielded 0 extractions.** |
| The supported corpus is vendor and blog content | Among the 321 supporting evidence items: practitioner blogs 127, vendor 80, SaaS maintenance-log vendors (recurrr, dovient, assetcenter, machdatum) 71, trade-association expert Q&A (automate.org) 30, an AI-agent product page (capafy.ai) 9, academic 4 (1.2%). |
| The 12 PDF rejections removed the curated tier | They include the ISA *Troubleshooting: A Technician's Guide*, de Kleer's intermittent-fault paper (IJCAI), NASA NTRS 20110014231, the NECA and IPS electrical standards, the TPC *Systematic Troubleshooting Approach*, and two Uni Stuttgart test papers. These are the §11 curated and boundary sources. The open web kept the SEO pages. |
| Corroboration is dead, not "undercounted" | 370 extractions produced 370 claims: 0 merges. Every supported claim has corroboration 1. Decision 0007's "paraphrases stay separate, undercount accepted" has been falsified in practice: undercount = total. |
| Verifier false-support on natural claims is about 20% | 4 of 20 sampled supported claims are wrong on scope (below); Wilson 95% CI roughly 8–42%. One more wrong support turned up among the decoy base claims (`c-08d943f885942281`). |
| Decoy false-accept of 35% is not a valid measurement for scope | 3 of the 5 "scope" decoys *weaken* the claim by dropping a conjunct, so the span still entails them (below). The decoy verifier also runs without the ±300-char context that real verification gets (run.py:430-433), so decoys are not measured in the production condition. |
| The coverage rule is lenient, and slots ignore the task's core knowledge | 5 of the 10 slots covered by ≤ 2 supported claims are covered only by off-topic or mistagged claims. 136 of 370 claims are `procedure_step` or `strategy`, types that no probe slot looks at. |
| The disagreement sweep is mostly a paraphrase finder | Kinds: 47 compatible, 2 insufficient, 1 scope, 0 genuine. Several "compatible" pairs are the same fact from different clusters, i.e. missed corroboration. |

## 1. Is the Evidence Ledger useful, to a human and to N3?

**Human: yes for audit, poor for reading.** Each supported claim can be traced to an exact span in an exact snapshot. `report.md` is 1,265 lines and 175 KB for one task, and its supported-claim lines carry no `claim_id`, `knowledge_type` or verdict, so a reader cannot cross-reference `sidecar.json` without grep. Claims the verifier rejected are rendered as "(no located evidence)" (report.py:55) even though they have a located span with an `insufficient` verdict. Example: `c-970e29651ce716ce` ("A quality multimeter is the **most essential** tool…"; the span says "most **used**") is shown as unlocated at report.md:466. That misreports a correct verifier catch as a fabrication.

**N3: not yet.** Deriving `AreaFeatures` from run (a) gives constant or dead values for:
- `source_kinds`: all `documentation`, because the `default-documentation` rule matched all 35 sources.
- `n_boundary_sources`: 0, with no forum host.
- `n_contradictions`: 0.
- `tacitness`: all UNASSESSED.
- `has_done_support` and `imagined_only`: there is no done/imagined classification.
- `n_inferred`: 0.
- `n_single_source_claims`: equals the number of supported claims, so it is collinear with `evidence_density`.
- `n_independent_sources`: inflated by error pages.
- The date features: only 11 of 35 sources are dated.

That leaves roughly `n_claims`, `evidence_density`, `knowledge_types`, `n_synthetic`, `n_unknown` and `rationale_present`. Planner areas are also topical search buckets ("Data Logging and Monitoring"), not the §14.2 partition (task step, decision point, KC, SOP section), and five areas per task gives area-level AUROC no power. N3 must supply the partition through `--areas` (A11). That is an N3 prerequisite, not an N2a defect.

## 2. Are claims atomic?

Mostly. In my 20-claim sample, 4 are compound:
- `c-6c4d3550369ac002`: a definition plus two consequences.
- `c-918a646916acb85c`: "vulnerable to loss" plus "cannot prove not edited".
- `c-2271e1237b9ecb46`: displayed live plus recorded for analysis.
- `c-a8bd7cbc95e28ca3`: a norm plus its rationale.

Among the 20 decoy base claims, 3 more are compound (`c-03221fc648c50847`, `c-05ffecbae90b2aa5`, `c-0854575ba0113ca4`). That makes about 7 of 40 (18%). Compoundness is what makes "drop a conjunct" scope decoys invalid. I found no harmful over-fragmentation.

## 3. Can you see exactly WHY a supported claim is supported?

**Only half.** You get the span (`Selector.exact`) and the locator, and the ±300-char context can be rebuilt from the snapshot. The verifier's `supporting_quote` is **discarded** (run.py:334-338 keeps only the verdict), and `calls.jsonl` stores only a hash of the prompt. So a human cannot see which part of the span the verifier relied on, or whether it leaned on context outside the span. That matters: `c-aed289a57231c28c` is supported only through an antecedent ("These" = loose ferrule, push-in terminal) that lies *outside* the span, against the verify prompt's own rule that the span alone must entail.

Sample verdicts (20 supported claims). Right: 12. Right with a caveat (qualifier or antecedent outside the span, or vendor rhetoric): 4 (`c-2ec7925ad29b0ba4`, `c-7f19c8dd5a3ca919`, `c-aed289a57231c28c`, `c-54099e84c666855c`). **Wrong: 4.**
- `c-d4ac349735a8502c`: the span "Confirm whether communication loss triggered the stop…" is in the *network* section; the claim reassigns it to "intermittent **software** faults" (taken from the next heading).
- `c-d008e8f1da0cb01c`: "teams that stay out of firefighting mode **usually**…" becomes "The **most effective** maintenance teams…". The hedge is dropped and the subject is reframed.
- `c-33bf55b7567f1546`: the span describes a product ("The Agent prioritizes…" on capafy.ai); the claim generalises it to "troubleshooting procedures".
- `c-894231e165c5777c`: the span says "In my experience… follow-through, not technical skill. **The reminder failed**…"; the claim says "…rather than **scheduling**". It inverts the contrast and drops the attribution.

## 4. Evidence collection or RAG answers?

**Evidence collection at the claim level; model-mediated at the retrieval level.** Claims are harvested from documents with verbatim, re-sliceable spans, and no answer is generated. Two caveats:
- Search hits are only the `url_citation` annotations that the planner model chose to cite (llm.py `search`). What a model decides to cite is the retrieval filter.
- Extraction answers "what does this page say", not the probe questions. 39% of claims fall outside the probe types, and areas are single-assigned by the extractor. The equipment-maintenance-log SEO pages leak into "Systematic Troubleshooting" and "Data Logging" (`c-d008e8f1da0cb01c`, `c-3b2e378a345df8d8`, `c-a8bd7cbc95e28ca3`).

## 5. Are unsupported claims clearly visible?

**In the sidecar, yes. In the report, blurred.** All 49 synthetic claims appear in the report. The 16 `insufficient` ones are mislabelled "no located evidence" (report.py:55), and neither the span nor the verdict is shown.

The 16 rejections were mostly correct catches of added content: "most essential" vs "most used" (`c-970e29651ce716ce`), "alarm history, program changes" not in the span (`c-cefe3a6de33365fc`), added escalation targets (`c-1df2033df671081a`). So the verifier catches **additions** well and misses **generalisation and scope shift**.

The 33 unlocated extractions break down as follows:
- about 12 quotes stitched from non-contiguous sentences: correct rejections;
- 10 lost to `|` table-cell separators in the page text, which the extractor drops. These are mostly the academic/table pages: exa.ai library, 10 extractions, 0 located;
- 3 quotes trimmed mid-sentence with a period added;
- 5 over or under the 6–80 word limits;
- 1 case difference, 1 ellipsis, 1 paraphrase.

The report calls this the "fabrication rate". It is not one. Rename it "unlocated rate".

## 6. Does UNKNOWN occur naturally, or is the coverage rule too lenient?

**Too lenient, and partly a product of the area partition.** All 5 UNKNOWN slots have 0 tagged claims, so the rule behaves as coded. But "covered" needs only **one** supported claim carrying the extractor's type tag, in the extractor's chosen area. Of the 10 covered slots with ≤ 2 supported claims, 5 are covered by an off-topic or mistagged claim:
- Systematic Troubleshooting / concept ← "Reactive maintenance is significantly more expensive than preventive" (`c-230f741640d97da5`).
- Systematic Troubleshooting / failure_mode ← "If the Trend_Idx reaches 600 while a MOV runs, the controller takes a major fault type 4 code 20" (`c-dde847bfa2cea027`): one code example.
- Systematic Troubleshooting / rationale ← Peakboard marketing "Machine monitoring is lean… complements an existing MES" (`c-81a0afa878acb787`).
- Electrical / decision ← two cue or interpretation claims (`c-458f4d99523f4ac1`, `c-933e695c5b497d18`).
- Documentation / check ← two claims about log-entry content (norm, not check) (`c-186e4bb7f806fcdf`, `c-54099e84c666855c`).

Conversely, "PLC Fault Diagnosis Methods / norm = UNKNOWN" is an artefact. Norm claims about exactly that topic (`c-999231909ad2e610`, "Do not mask a power problem…") were single-assigned to the near-duplicate area "Systematic Troubleshooting Frameworks". So UNKNOWN under-counts true thinness and over-counts partition noise. The core of a "how does a technician diagnose" task, `procedure_step` (71) and `strategy` (65), is never probed. That matters because §14.3's naive baseline is "every procedural or decision area is a gap".

**Minimal fix:** a slot is `covered` only with supported claims from **≥ 2 independence clusters**. A slot with support from a single cluster becomes a new sidecar status `thin`, which is a feature and never an UNKNOWN record. Add `procedure_step` to the probe set (this changes the probe hash, so do it before E-PLANT freezes the config).

## 7. Corroboration

**The problem is the opposite of false corroboration: corroboration is dead.** Merging on identical casefolded assertions never fires, because each document is extracted separately and the extractor paraphrases. The contradiction sweep shows that real cross-cluster corroboration exists and is being thrown away. Its candidate pairs are cross-cluster and same-area by construction, and several "compatible" pairs are the same fact:
- "An open or infinite resistance reading… coil may have failed" and "An open circuit reading (OL)… indicates a burnt… coil";
- two claims that continuity testing belongs only on de-energised circuits;
- two claims on verifying a fix under the conditions that correlated with failure.

**Minimal fix (a cross-cluster re-verification pass, which also replaces A10's merge):**
1. After verification, for each supported claim *c* in area *a*, rank the located spans of other supported claims in *a* from **other** independence clusters by content-word Jaccard against *c*'s assertion. Reuse `evidence.content_words`/`jaccard`; this is `contradiction_candidates` with the claim as the query.
2. Take the top k = 2 and call the existing verifier on (c.assertion, that span with its ±300 context).
3. If the verdict is SUPPORTS and `quote_in_span` holds, append that span as another `Evidence` on *c*, built through `evidence.build_evidence`, so there is still one constructor. Record `{claim_id, span_locator, verdict, supporting_quote, pass: "cross-cluster"}` in the sidecar.

Record a REFUTES verdict as refuting `Evidence`. It feeds `n_contradictions` directly, and that is why the separate contradiction stage can go (see REMOVE). Cost: at k = 2, about 640 verify calls, about $0.36 at run (a)'s measured $0.00056 per verify call. Corroboration then feeds `corroboration`, `n_single_source_claims` and `n_independent_sources` with no schema change.

**Preconditions:**
- The pass must come **after** the verifier fix (Q10). Otherwise a 20% false-support verifier manufactures corroboration.
- Its false-corroboration rate must be measured with cross-cluster decoy pairs: a mutated claim against a real cross-cluster span.
- Independence has blind spots that this pass will expose:
  - **Over-merge:** the registrable-domain rule collapses distinct works on publishers and hosts (3 different MDPI papers, 3 exa.ai library publications, 2 different NETA standards on studylib), and would collapse every Springer/ScienceDirect/arXiv paper in a curated corpus into one cluster.
  - **Under-merge:** SEO "equipment-maintenance-log" pages (recurrr, dovient, assetcenter, machdatum) share one outline but no verbatim text. In run (b), regulator guidance from ICO, EDPB, CNIL and CNPD all derives from WP248, and shingles will not see it.
  - Fix the over-merge with a publisher/host list where independence falls back to canonical URL or DOI. Record the under-merge as a known limitation in the N3 pre-registration.

## 8. Same architecture across both domains?

**The architecture is the same; the failure modes differ by domain.** Both runs use the same code and the same `models.json` (planner, extractor and baseline are anthropic/claude-haiku-4.5; verifier and contradiction are openai/gpt-5.4-mini), and the planner produced 5 areas × 2 queries for each. The run-(b) section below has the details. In short:

| | (a) PLC | (b) GDPR DPIA |
| --- | --- | --- |
| Corpus | Junk-heavy: vendor and SEO pages | Authoritative: regulators and statute |
| Independence | Many clusters (27, largest 11%) | Over-merged (4, largest 55%) |
| Verifier on natural claims | Passes generalisation (about 20%) | Near-verbatim legal restatement, about 9/10 right |
| Verifier on decoys | Scope decoys invalid | Passes and/or swaps (2/7) |
| Unlocated | 9%, stitched sentences and table pipes | 21%, list and checklist stitching, >80-word paragraphs |
| UNKNOWN | 5/35 | 14/35, sparse `cue`/`failure_mode`/`check` in regulator text, which looks natural |

In both runs, error pages become sources, the curated tier arrives as PDFs and is rejected, and `source_kinds` is constant (`documentation`, because there are no host rules for legislation or regulators).

## Run (b): GDPR DPIA

Task: "When must a controller carry out a DPIA under the GDPR, and what must it contain?", domain "EU data protection law".
Stats: 20 sources, 18 fetch failures, 4 clusters (largest 0.55), 259 extracted, 21% unlocated, 195 supports; labels 193 `literature_supported` / 64 synthetic / 14 unknown; 1 ledger contradiction and 39 other disagreements; decoy false-accept 15%.

**Fetch: 18 of 18 failures are PDFs, but only about 10 are unique URLs.** Failed fetches are not cached, so the same URL is refetched every time a search returns it. WP248 rev.01 was attempted 4 times, as `cnil.fr` and `www.cnil.fr` × 2, and the IE DPC list 3 times (run.py:230-236 caches successes only). The rejected PDFs are WP248 (the EDPB-endorsed DPIA guideline), the EDPB DPIA template explainer 2026, and the national Art. 35(4) lists (GR, SI, IE, BE, IS, UK). That is exactly the pan-EU and cross-jurisdiction material where scope differences and contradictions would live. Separately, 5 of the 20 "sources" are HTTP 404 ×3 or 403 ×2 pages (EDPB file links, EDPS, commission.europa.eu, gra.gi), accepted as Sources by the same missing status check as in (a).

**The corpus is UK-centred in an "EU data protection law" run.** Supports by host: ico.org.uk 131, cnpd.public.lu 28, legislation.gov.uk 25, edpb.europa.eu 6, dataprotection.ie 5. So 80% of supports come from the UK regulator or the UK copy of the text. Only 34 claims name the ICO or the UK. ICO-list claims are stated as general GDPR rules; for example, `c-c3aa083e28775828` says "Processing involving innovative technologies requires a DPIA when combined with any criteria from the European guidelines", which is the ICO's Art. 35(4) list and not EU-wide. `Scope` has no jurisdiction field, so this drift is invisible to the ledger. Add jurisdiction to the extraction prompt now, and to Scope at the next N1 re-freeze.

**Independence over-merge (the runner's finding 2): confirmed, by two mechanisms.**
1. **The ≥25-word shared-run rule unions whole documents, transitively.** legislation.gov.uk (Art. 35 text) is linked to ico.org.uk (6 pages) and to cnpd.public.lu because both quote Art. 35 verbatim, so all 11 documents become one cluster. That is right for the quoted Art. 35 spans and wrong for everything else. CNPD's 28 supports are its own checklist, which is independent of the ICO's guidance, yet it can never corroborate an ICO claim.
2. **Registrable domain `europa.eu` merges EDPB, EDPS and the Commission,** which are different institutions.

The fix is span-level derivation. Evidence spans that overlap a shared run take the independence key of the run's other document; every other span keeps its own document's key. `independence_key` lives on the `Source` embedded in each `Evidence`, so no schema change is needed. Also use host-level keys for multi-institution registrable domains (europa.eu, and publishers or document hosts, see Q7). Until this is fixed, the corroboration pass (Q7) would find almost no "other cluster" in (b).

**The ledger contradiction (the runner's finding 1): confirmed false positive.** `c-592a2fadc6f4283c` (DPC: consult the SA when a DPIA indicates high risk absent mitigation, Art. 36) and `c-a8d67e2f019b7cce` (ICO: do a DPIA where processing is likely to be high risk, Art. 35(1)) are sequential obligations, not contradictory ones. The guard only checks that the quotes are verbatim (run.py:468-470), not that the kind is correct, so a mis-kinded pair reaches the ledger.

Other disagreements:
- Of the 4 "scope" disagreements, 1 is informative: `c-107ffd1f52495e14`/`c-dcb6e18a5bd4c866`, where DPC answers within 8 weeks and the ICO within 8 weeks extendable to 14, a real jurisdiction difference. Two pair unrelated claims (`c-27af33c5674fc109`/`c-2fa57f35f4df9222`, `c-38cfa9c10f9c0da1`/`c-6154d9c9cb8eb883`).
- The "terminology" pair (`c-6154d9c9cb8eb883` EDPB / `c-d2de2485aa413a04` CNPD: consult the DPA when risks cannot be mitigated) is a missed corroboration.

So across both runs the contradiction stage returned 1 false positive, 1 useful scope pair and a set of missed corroborations out of 90 calls.

**Atomicity (the runner's finding 3): partly confirmed; the rate is overstated.** A crude heuristic (≥ 3 commas, ≥ 2 semicolons, or "N key steps") flags 13% of (b) claims and 12% of (a) claims, so (b) is not worse than (a). Many flagged (b) claims are disjunctive legal triggers that should stay one claim. `c-16af9326fa272d7d` "Automated decision-making about an individual's access to products, services, opportunities, or benefits requires a DPIA" is one norm, and splitting its "or" list would change its meaning. Genuine bundles are conjunctive content lists: `c-1d5f876623c86b1a` "A DPIA process should include seven key steps…" and "A DPIA submission to the ICO must include descriptions of roles…, purposes…, measures…, DPO contact…". Extract-prompt fix: split conjunctive "must include A, B, C" lists into one claim per element; keep disjunctive condition lists whole.

**Unlocated 21% (the runner's finding 5): cause disputed.** Of 55 unlocated quotes:
- about 38 are stitched or paraphrased, mostly list or checklist items joined across `☐` and "(a)/(b)" boundaries;
- 8 exceed 80 words (legal paragraphs);
- 4 differ only by glyph or quote style (`'` vs `"`, `☐`);
- 2 contain an ellipsis;
- only **1** involves a bracketed or nested citation.

Most of these are correct rejections of non-contiguous quotes. The fixable part is the glyph/quote-style tolerance (SHOULD 5), plus a limit raise or a split for single legal sentences over 80 words.

**Verifier on (b).** 10 sampled supported claims are about 9/10 right; they are mostly near-verbatim restatements, as legal text invites. The caveats are the jurisdiction-scope drift above and `c-592a2fadc6f4283c`, which paraphrases "in the absence of mitigating measures" as "mitigating measures cannot eliminate the residual risks", borrowing the next sentence's gloss. The decoys are **valid** here and expose the connective weakness:
- `c-0403ebb7fb067639` "extensive" (**or → and**) was accepted.
- `c-08c2a454d91ee0bd` ICO innovative technology ("in combination with" → **or**) was accepted.
- `c-138d82fe861101fe` negation "more than remote" → "more than certain" was accepted.

In law, and/or is the decision.

**Combined decoys (the runner's finding 6).** Scope 7/12, negation 2/20, number 1/8 are arithmetically right. But 3 of (a)'s 5 scope false accepts are invalid decoys (Q10), so valid scope evidence is about 2 (ambiguous, a) + 2/7 (b). The and/or failure is confirmed, and the verifier fix's `quantifier_or_modality_differs` flag must name **logical connectives** (and/or, "in combination with", "only if") explicitly.

**UNKNOWN in (b): 14/35, and it looks natural.** `failure_mode` is UNKNOWN in 5/5 areas and `cue` in 4/5; regulator text states obligations, not how DPIAs go wrong in practice. That is the tacit side the gap map exists to predict, so (b)'s UNKNOWNs are signal. The leniency from Q6 still applies: several slots are covered by a single claim (Legal triggers/check 1, Processor/concept 1, Processor/decision 1, Exemptions/decision 1, Exemptions/rationale 1).

## 9. Abstractions with one implementation, and anything unnecessary for N3 (REMOVE)

- `evidence._majority` and the tie/`conflict` machinery in `merge_extractions` (evidence.py:400-429): fired 0 times in 370. Replace with the corroboration pass; keep at most an exact-duplicate collapse.
- `slot_status(area_lost_to_truncation=…)`: the argument is hard-coded `False` (run.py:385). A stub parameter implies a check that does not exist. Remove it, or implement it from `truncated_fraction`.
- Sidecar `modified: None` (run.py:311): never populated, although A9 says published = the later of published and modified. Either implement it in `web._extract_metadata` or drop the field. `tier: "open"` (run.py:316) is constant but required by A9 and decision 0007; keep it until a curated tier exists.
- The report's per-area "N1 exclusions" section: always "none" for World A, which cannot trigger an exclusion. Remove it from the N2a report.
- The report's full summary-statistics dump (19 rows, float noise such as 0.11428571428571428): replace it with the headline plus labels.

- **The separate contradiction stage** (`contradict.md`, `CONTRADICT_SCHEMA`, the `contradiction` role, run.py:441-477). Across both runs, 90 calls produced 0 correct genuine contradictions, 1 false positive in the ledger (run b), and mostly "compatible" pairs that were really missed corroborations. The cross-cluster re-verification pass (Q7) asks the same pairs a sharper question, whether span B supports claim A. Its REFUTES verdicts already feed `n_contradictions`, which is defined as "claims in a detected contradiction **or with refuting evidence**". One pass then yields both corroboration and contradiction.

Keep the `Backend` Protocol (the fakes and `CorpusSearchBackend` justify it) and the one-line `build_*` wrappers (they enforce the single-constructor rule cheaply).

## 10. Decoys, and whether the verifier is fit to label `literature_supported`

**Not yet fit.** It rejects added content well (16 correct `insufficient` verdicts) but passes scope and subject generalisation: 4 of 20 on natural claims, plus `c-08d943f885942281` ("enables decision-making based on current information rather than historical data" ← span "Summit streams live KPIs to dashboards.").

The E-LIVE decoy numbers:
- **Negation 1/13:** a genuine miss. `c-0ae2bfae93f15f20` "common" → "rare" was accepted; the span "Next are unwanted interactions…" depends on list context the decoy verifier never sees.
- **Number 1/2:** a genuine miss (`c-099467b81e3870ec` "multiple parts" → "a single part"). n = 2 carries no information.
- **Scope 5/5 is mostly an invalid measurement:**
  - `c-0750488ddafc04ec` drops "or eliminate", `c-0b0bdd3ff65e2dd0` drops "follow-up" and `c-03221fc648c50847` drops a conjunct. Each mutated claim is *weaker* and still entailed.
  - `c-037aaebe7854868f` ("weeks and months" → "days and weeks") and `c-0cc23648971b50f9` ("multiple channels" → "a single channel" against "via Email, SMS, or push") are ambiguous.

So 35% is a noisy pre-fix baseline, not an estimate of the scope false-accept rate. Scope drift in the verifier is real, but it is shown by the natural sample, not by the decoys.

**Minimal verifier fix (same call count):**
1. Extend `VERIFY_SCHEMA` with three booleans the model must commit to: `adds_content_not_in_span`, `subject_or_scope_differs` (a different population, system, condition, or a product's claim generalised to practice), and `quantifier_or_modality_differs` (usually→always, may→does, "in my experience"→general). In code, keep SUPPORTS only if all three are false **and** `quote_in_span` holds. Otherwise record INSUFFICIENT.
2. In the verify prompt, name the three failure shapes from this run: section or heading reassignment, product-to-practice generalisation, dropped hedge or attribution.
3. Persist `supporting_quote` and the three flags per extraction in the sidecar.
4. In the extract prompt, require the assertion to keep the quote's subject, quantifier, modality and attribution.

**How to re-measure honestly:**
- Build decoys in the production condition (claim + annotated ±300 context, the same `_verify_user` call as real verification).
- Scope mutations must be **strictly stronger or different**: universalise a quantifier, drop a hedge, broaden the subject, add an unstated condition. **Never** drop a conjunct.
- Stratify to 10 per mutation type (cap 30, not 20) and report a Wilson CI per type in the headline.
- A decoy is valid only if a third-family model or the owner confirms the span does not entail it; invalid decoys are excluded and counted.
- Report a **natural** false-support rate as well: the owner blind-labels 40 randomly drawn supported claims, since decoys only measure synthetic drift.
- The E-LIVE numbers (negation 1/13, number 1/2, scope 5/5 invalid) and my natural 4/20 are the pre-fix baseline. Re-verifying E-LIVE's stored spans offline (snapshots exist, no search or extraction, about $0.2) is a cheap check that the fix does not simply reject everything. The retention-vs-rejection trade-off must be read from E-PLANT, the pre-registered re-measure, not tuned on the claims named in this note.

## Implementation defects

1. **web.py:221-243: `fetch` never checks the HTTP status.** 403/429 bodies become Fetched, then Sources and clusters (11 of 35 in run a). Nothing rejects bot-wall or near-empty text (0-char, 107-char Vercel checkpoint, 209-char Access Denied). Fix: non-2xx is a `FetchFailure`, and text under a minimum length (for example 150 words) is a `FetchFailure("too little text")`.
2. **llm.py:131: `json.loads` can raise `JSONDecodeError`, which is not `LLMUnavailable`.** The run then dies, and `reconstruct()` catches only `BudgetExceeded` (run.py:479), so nothing is written: no ledger, sidecar or report.
3. **llm.py:160-167: billed calls that end in refusal, `length` truncation or malformed JSON raise before `log.append`.** Their cost never reaches `total_cost` (the budget undercounts) and they never appear in `calls.jsonl` (silent). Log every response with an `outcome` field.
4. **run.py:632-636: extraction failure is silent.** `_extract_document` returns `([], False)` with no sidecar record, so a document lost to truncation or refusal looks the same as a document with nothing to say. An area counts as "extracted" if any one of its docs extracted, including an error page that legitimately yields nothing. Record `extract_ok` and `n_claims` per source.
5. **run.py:669: `--out` defaults to the relative `reconstruct/runs`**, resolved against the cwd. `models_path` is anchored to `__file__` (run.py:679), but `out` is not, which explains the reported crash. Anchor it the same way, or `.resolve()` it and require it to exist.
6. **run.py:430-433: decoys are verified on `selector.exact` only**, while real claims are verified with the annotated context (run.py:327-331). The decoy false-accept rate therefore does not measure the production verifier.
7. **run.py:334-338: `supporting_quote` is discarded.** Keep it in the sidecar (Q3).
8. **report.py:55: `insufficient` and `refutes` claims render as "(no located evidence)".**
9. **report.py:44-47: supported claims print no `claim_id`, `knowledge_type` or verdict,** so the report cannot be cross-referenced with the sidecar.
10. **A5 is not fully implemented:** "nearest preceding heading if detectable" is absent, and normalisation flattens headings. `c-d4ac349735a8502c` is exactly a heading-scope error.
11. **A9 is not fully implemented:** `modified` is never read, and published is the first meta field found, not the later of published and modified.
12. **Stats mix units:** `n_located` counts claims while `n_extracted` counts extractions, including rejected ones (run.py:488-508). This is harmless only while merges are 0.
13. **run.py:230-236: failed fetches are not cached.** The same failing URL is refetched on every hit (WP248 ×4 in run b), which inflates `n_fetch_failures` (18 reported, about 10 unique).
14. **run.py:468-471: the contradiction guard checks only that the quotes are verbatim**, not the classification, so one mis-kinded pair became the only ledger contradiction (run b).
15. **evidence.py:283-284: the shared-run rule unions whole documents transitively,** where it should mark only the overlapping spans as derived (run b: an 11-document cluster).

## Silent-failure risks

- **The corpus bias from PDF exclusion is real and one-directional.** The rejected PDFs are the standards, the technician's guide and the research; what survives is HTML marketing and SEO. Add PDF text extraction (pypdf/pdfminer, page-aware) before any N3 corpus, or restrict World A to a curated manifest (corpus mode already exists).
- **Host tier "open" and voice "expert/default-unassessed" on all 35 sources.** The ledger asserts `voice=expert` for vendor marketing and an AI-agent product page. Nothing downstream reads voice for World A today, but it is a false fact in a criterion record. SourceKind has no vendor/commercial value, so record a `commercial` flag in the sidecar at least.
- **Undated sources: 24 of 35.** §14.3's anti-contamination rule (freeze the corpus at each gold's publication date) cannot run on an undated open-web corpus.
- **The table-separator loss** silently removes table-formatted academic pages (10 of 33 unlocated).
- **The planner's near-duplicate areas** ("PLC Fault Diagnosis Methods" vs "Systematic Troubleshooting Frameworks") plus single assignment create UNKNOWNs that are partition noise.
- **Budget accounting undercounts** (defect 3). With a $1.50 cap and $0.68 spent, it has not bitten yet.

## MUST-FIX before E-PLANT / E-ABST

Every prompt edit belongs here, because the pipeline freezes before E-PLANT and a later prompt change invalidates E-PLANT.

1. Reject non-2xx and near-empty or bot-wall pages in `fetch` (defect 1; 11/35 in a, 5/20 in b).
2. **The verifier fix.** Schema flags `adds_content_not_in_span`, `subject_or_scope_differs` (including jurisdiction) and `quantifier_or_modality_differs` (naming **logical connectives**: and/or, "in combination with", "only if"), plus a code rule that keeps SUPPORTS only if all three are false. Persist `supporting_quote` and the flags (Q10; defect 7; runner (b) finding 6: and/or flips confirmed).
3. **The extract-prompt edits, made in the same freeze:**
   - keep the quote's subject, quantifier, modality, attribution and **jurisdiction**;
   - split conjunctive "must include A, B, C" lists into one claim per element;
   - keep disjunctive condition lists whole (runner finding 3: partly confirmed, 13% flagged in b vs 12% in a).
4. **A valid decoy protocol:** the production condition (defect 6), strengthening-only scope mutations including and↔or swaps, 10 per type with a Wilson CI, and a validity check.
5. JSON parse errors become `LLMUnavailable`; every billed call is logged and counted against the budget; extraction failures are recorded per source (defects 2–4).
6. Anchor `--out` (defect 5).
7. Fix the report's mislabel of verifier-rejected claims and add `claim_id`/`knowledge_type`/verdict per line (defects 8–9).
8. Freeze the pipeline (prompt and probe hashes, including `procedure_step`, see SHOULD 3) after 1–7 and before E-PLANT runs.

## SHOULD-FIX (each blocks N3 input, not E-PLANT)

1. **Span-level independence** (runner (b) finding 2: confirmed). The shared-run rule marks only the overlapping spans as derived and never unions whole documents (defect 15). Use host-level keys for multi-institution or publisher domains (europa.eu, mdpi.com, springer.com, sciencedirect.com, acm.org, arxiv.org, studylib.net, exa.ai).
2. **The cross-cluster re-verification pass** (Q7), run after MUST 2 and SHOULD 1. It yields corroboration (SUPPORTS) and contradiction (REFUTES) together; measure its false-corroboration rate with cross-cluster decoys.
3. **Coverage** needs ≥ 2 independence clusters, plus a `thin` slot status. Add `procedure_step` to the probe set *before* the MUST 8 freeze (Q6).
4. **PDF text extraction,** or a curated corpus manifest, for World A (runner finding 4: confirmed, and worse in b, where WP248 and every national Art. 35(4) list were lost). Cache fetch failures (defect 13).
5. **Glyph-, quote-style- and separator-insensitive `locate`** through an offset-mapped index (`|`, `☐`, `•`, `'`/`"`) (runner finding 5: cause disputed; only 1/55 is a nested citation, and most are correct rejections of stitched list items).
6. **Host rules** for academic publishers (→ `study`) and for legislation or regulators (→ `standard`/`procedure_document`), so `source_kinds` is not constant. Add jurisdiction to Scope at the next N1 re-freeze.
7. A5 heading capture and A9 `modified`.
8. N3 must supply a frozen `--areas` partition at §14.2 grain; planner topical areas are not N3 areas.

## REMOVE

- **The contradiction stage** (`contradict.md`, `CONTRADICT_SCHEMA`, the `contradiction` role, run.py:441-477), replaced by REFUTES from SHOULD 2. Runner (b) finding 1 is confirmed: the only ledger contradiction is Art. 36 vs Art. 35(1), sequential obligations, a false positive.
- `_majority` and the tie/`conflict` logic in `merge_extractions` (2 merges in 629 extractions across both runs: 0 in a, 2 in b).
- The hard-coded `area_lost_to_truncation=False` stub (run.py:385), unless it is implemented.
- The sidecar `modified` field, unless it is implemented.
- The report's "N1 exclusions" section and its raw 19-row stats dump.
