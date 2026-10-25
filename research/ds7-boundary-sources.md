# DS7: public boundary sources that would revive dead features

- **Question:** For each candidate gold domain, which public texts record practice at the novice–expert boundary, and could they revive the frozen features that are constant today (`n_boundary_sources`, `has_done_support`, `imagined_only`, `latest_source`)?
- **Answer:** Public boundary texts that predate the gold exist for all three primary golds: near-miss and fatality reports for Okoli 2020, and M&M cases with expert commentary, device-event reports and trainee forums for Madani 2015 and Logishetty 2019. But the features are dead because of retrieval, not vocabulary: 0 of the 108 URLs recorded by the three N2 runs whose ledgers N3 reads is a forum, incident or other proposed boundary host (`research/ds7/replay.json`). No public source in these domains is a record of work as done, so `has_done_support` stays dead for all three.
- **Changed:** The E-CTA pre-registration should state that its primary test covers size, density, type and the lens signal only. `n_boundary_sources` and `imagined_only` can enter as secondary features only after a gold-blind retrieval probe shows they vary across areas (§6). Owner decision 2026-10-24: option 1 adopted.

**Result (2026-10-24).** The boundary sources exist, and most of them predate their gold. The existing vocabulary can hold all of them without a new field: `INCIDENT_REPORT` or `FORUM_POST`, with `boundary=True` where the text records an error and an expert's account of it. That is the class of boundary text `REORIENTATION.md` §11 step 2 lists. Three facts limit what follows from that:
1. **Retrieval, not vocabulary, keeps `n_boundary_sources` at 0.** The forum rule already sets `boundary=True` (`reconstruct/src/reconstruct/evidence.py`, `classify_source`). The three N2 ledgers N3 reads never reached a forum or incident host: 0 of 50 cited sources and 0 of 108 recorded URLs. Across all six committed runs, one URL out of 134 is a forum host. It sits in the failed PLC run `20260928T145115Z-518f99363336`, and it is a `plctalk.net/technical-articles/` page: an article that the host-level rule would mislabel as a forum post. Adding host rules alone flips nothing on the N3 ledgers (replay, §4).
2. **`has_done_support` has no honest World A source in fire command or surgery.** Incident, near-miss and M&M texts are accounts of work, so they map to `Practice.REPORTED`, not `DONE`. The only public "work as done" text found is aviation transcripts in NTSB dockets (`LOG`), which fits only DS1 rank 17 (Seamster 1993, air traffic control).
3. **No study measures the reporting-bias claim in these domains.** The mechanism is literature-supported [25], and one software study shows Q&A topics that documentation omits [S1]. No study shows that surgical or fire-command boundary texts hold the "obvious" steps expert-to-expert text omits (§5). The feature's direction is a hypothesis, and in-sample it has zero variance, so its weight cannot be set before gold.

**Decision it feeds:** whether the E-CTA pre-registration revives the dead features, or states that it tests size, density, type and the lens signal only (I6, `research/area_score/RESULT.md`). The owner adopted option 1 on 2026-10-24 (§6).

**Method.** Web search and fetch of the sources' own pages, retrieved 2026-10-24. Volume was measured with Wayback CDX counts and openFDA `meta.results.total` queries; OpenAlex was used for the evidence in §5. All six committed N2 runs under `reconstruct/runs/` were replayed offline (`research/ds7/replay.py`, output `replay.json`; a second run is byte-identical). `citation-verifier` passed on 2026-10-24, after one round of fixes: the replay was widened to all six runs, and nine wording and source corrections were made. Every claim is tagged with its source; *inferred* marks a judgement the source does not state. Cost: $0 in model calls.

**Gold blocklist (DS1).** DS1 has no blocklist file, so this pass applied one built from DS1's register:
- all 29 register DOIs;
- Logishetty 2019's open-access web training tool, which DS1 records as "built from the CTA";
- any material by a gold's authors on the same procedure after the gold date (*inferred* to be a derivative).

No search targeted a gold procedure's steps, decisions or cues. Searches named source types (near-miss systems, M&M series, forums), never procedure content. The only procedure words used were the device generic names in four openFDA count queries ("laparoscopic", "hip", "duodenoscope", "colonoscope"), and those returned counts only. No gold content was seen.

## 1. Why the features are dead (mechanism)

`area_features` (`residual/src/residual/features.py`) computes the features as follows:
- `n_boundary_sources` = `sum(s.boundary)` over an area's sources.
- `has_done_support` = `Practice.DONE in practices`, where `PRACTICE[kind]` (`residual/src/residual/vocab.py`) maps `ISSUE`, `COMMIT`, `REVIEW_THREAD`, `LOG`, `LEARNER_RESPONSE`, `THINK_ALOUD` and `OBSERVATION` to `DONE`.
- `imagined_only` = every source is `IMAGINED`: `TEXTBOOK`, `STANDARD`, `PROCEDURE_DOCUMENT`, `DOCUMENTATION` or `DESIGN_RECORD`.
- `earliest_source` and `latest_source` use only dates that came from a document field. `_date` drops a date the sidecar shows came from `Last-Modified` alone.

`Source.kind` and `boundary` are set by host rules in `classify_source`:
- forum hosts (`reddit.com`, the Stack Exchange sites, `plctalk.net`, any `forums.*` host) → `FORUM_POST`, voice `MIXED`, `boundary=True`;
- academic publishers → `STUDY`;
- regulators → `PROCEDURE_DOCUMENT`;
- legislation and standards bodies → `STANDARD`;
- everything else → `DOCUMENTATION`.

No rule yields `INCIDENT_REPORT`, `ISSUE` or `LOG`. Date fields come from `citation_publication_date`, `article:published_time`, `dc.date`, JSON-LD `datePublished` or the PDF `CreationDate` (`reconstruct/src/reconstruct/web.py`).

## 2. Source tables per domain

**Columns:**
- **Pre-gold?** asks whether the source has items dated before the gold's first-online date (DS1 register).
- **Volume** is what was measured on 2026-10-24.
- **Wayback counts** are distinct archived URLs returning HTTP 200 before the gold date (CDX, `collapse=urlkey`). They are an upper bound on pages, not a report count.
- **Kind / boundary / voice** is the proposed mapping onto the existing `SourceKind`, `boundary` and `Voice`, with no new field.
- **Dated by** is the field the current `web.py` would read, or "adapter" where an API record carries no HTML date meta.

### 2.1 Incident command: Okoli 2020 (first online 2020-08; author at Coventry, UK [G1])

| Source | Access route | Licence / terms | Coverage; pre-gold? | Volume | Kind / boundary / voice | Dated by |
|---|---|---|---|---|---|---|
| NIOSH Fire Fighter Fatality Investigation and Prevention Program reports [F1][F2] | cdc.gov for 2017 onward; CDC Stacks for 2016 and earlier [F1] | US federal work, public domain (*inferred*; the page states no licence) | Reports on Stacks run back many years before 2020 [F1][F2]; start year not verified from a primary page; **yes** | 680 archived `cdc.gov/niosh/fire/reports/face*` URLs before 2020-08 | `INCIDENT_REPORT` / `True` / `EXPERT` (investigators' account of a death or serious injury) | PDF `CreationDate`. *Inferred* risk: re-hosted PDFs carry a re-render date |
| National Fire Fighter Near-Miss Reporting System (IAFC) [F3][F4] | `firefighternearmiss.com` now returns 301 to `firefighterclosecalls.com` (checked 2026-10-24); pre-gold pages via Wayback only | IAFC; no terms found | Launched 2005-08-12; more than 3,100 reports by late 2009 [F3]; **yes** | 1,994 archived URLs before 2020-08 | `INCIDENT_REPORT` / `True` / `MIXED` (de-identified self-reports by the crews involved [F4]) | Wayback snapshot timestamp (dated-corpus mode); the page meta is unknown |
| Wildland Fire Lessons Learned Center incident reviews: facilitated learning analyses, rapid lesson sharing [F5] | `lessons.wildfire.gov` (returned 403 to a scripted fetch); `wildfirelessons.net` via Wayback | US interagency; terms not checked | Center founded 2002 [F5]; **yes** | 7,817 archived `wildfirelessons.net` URLs before 2020-08 | `INCIDENT_REPORT` / `True` / `MIXED` | Unknown |
| Coroners' Prevention of Future Deaths reports, England and Wales [F6] | judiciary.uk listings (405 to a scripted fetch) | Terms not checked | Under the Coroners (Investigations) Regulations 2013, reg 28; 5,891 reports by 2025-09 [F6]; no fire-service category found; **yes** for 2013–2020 | Fire subset not counted; 2,034 archived `judiciary.uk/publications/*` URLs (all topics) before 2020-08 | `INCIDENT_REPORT` / `False` / `EXPERT` (a coroner, not a domain expert) | Unknown |
| Reddit r/Firefighting [P1] | Reddit Data API: research use non-commercial, no redistribution [P1]; Pushshift access cut in 2023 [P1] | Reddit terms | **yes** | 1,795 archived thread URLs before 2020-08 | `FORUM_POST` / `True` / `MIXED`: **existing rule, no change** | Unknown |
| UK NFCC National Operational Learning action notes [F7] | Sector-internal; public release unconfirmed [F7] | — | — | — | World B (organisational), not World A | — |

**Domain-fit caveat (*inferred*).** Okoli's gold is UK structural firefighting. Every high-volume public source above is US, and one is wildland. A US near-miss narrative is boundary text for incident command in general, not for UK procedure.

### 2.2 Surgery: Madani 2015 (laparoscopic cholecystectomy, 2015-08) and Logishetty 2019 (anterior total hip arthroplasty, 2019-09)

| Source | Access route | Licence / terms | Coverage; pre-gold? | Volume | Kind / boundary / voice | Dated by |
|---|---|---|---|---|---|---|
| AHRQ PSNet WebM&M: anonymously submitted error cases, each with an expert commentary [M1][M2] | psnet.ahrq.gov (405 to a scripted fetch); earlier `webmm.ahrq.gov` | AHRQ, federal; reuse terms not checked | Launched February 2003 [M2]; 668 case studies listed in a search extract of [M1] (the page refuses scripted fetches); **yes** for both golds | 5,009 archived `webmm.ahrq.gov` URLs before 2015-08; 22,499 `psnet.ahrq.gov/webmm*` URL variants before 2019-09. Procedure-specific counts are unknown and *inferred* to be small | `INCIDENT_REPORT` / `True` / `MIXED`: the textbook boundary form, where an error is followed by expert articulation | Unknown |
| FDA MAUDE device-event reports, via openFDA `device/event` [M3] | JSON API | openFDA terms and licence (`meta` of every response) | About 1992 to the present [M3]; **yes** | 2,797 reports with generic name matching "laparoscopic", received by 2015-07-31; 229,413 matching "hip", received by 2019-08-31 (openFDA `meta.results.total`) | `INCIDENT_REPORT` / `False` / `EXPERT` (manufacturers' and facilities' device narratives in `mdr_text`) | `date_received`, via an **adapter**: an API record has no HTML date meta |
| Surgical case reports: Journal of Surgical Case Reports [M4]; BMJ Case Reports [M5] | JSCR open access; BMJ Case Reports by fellowship or subscription [M5] | JSCR: CC BY or CC BY-NC (DOAJ) [M4]; BMJ: publisher © | JSCR from 2010 [M4]; BMJ Case Reports from 2008 [M5]; **yes** for both golds | Not counted | `STUDY` / `False` / `EXPERT` (expert-to-expert text, the very genre [25] concerns) | `citation_publication_date`: reliable. But `academic.oup.com` is not in the academic host list today, so it would fall to `DOCUMENTATION` |
| Student Doctor Network forums, surgery section [M6] | forums.studentdoctor.net (403 to a scripted fetch); Wayback | SDN ToS; © 1999–2026 [M6]; reuse of member posts not stated | **yes** | 136,882 archived thread URLs, all sections, before 2015-08; the surgery subset is unknown | `FORUM_POST` / `True` / `MIXED`: **existing `forums.*` rule, no change** | Unknown (XenForo JSON-LD not checked) |
| Reddit r/surgery [P1] | as in §2.1 | Reddit terms | **thin** before Madani | 25 archived thread URLs before 2015-08 | `FORUM_POST` / `True` / `MIXED`: existing rule | Unknown |
| Coroners' PFD reports [F6] | as in §2.1 | — | 2013 onward: **yes** for Logishetty; 2 years for Madani | Surgical subset not counted | `INCIDENT_REPORT` / `False` / `EXPERT` | Unknown |
| **Blocklisted:** Logishetty's open-access web training tool built from the CTA (DS1 register) | — | — | — | — | Excluded: a derivative of the gold | — |

Not checked: OrthoBullets and VuMedi (both behind logins); surgical-college examiner reports (an instance of the 'examiner reports' class §11 step 2 lists) [notes].

### 2.3 DS1 fallback domains (ranks 5–17)

| DS1 rank: gold (first online) | Best boundary sources (from §2.1–2.2 unless stated) | Pre-gold coverage |
|---|---|---|
| 5 Grover TAR (2022-11), 6 Grover RYGB (2023-09), 10 Karamchandani (2021-06), 9 Dias cardiac team (2019-07), 14 Plumptre (2017-07) | WebM&M, MAUDE, JSCR, BMJ Case Reports, SDN, PFD | All yes |
| 7 Smink appendectomy (2012-02) | WebM&M, MAUDE, SDN, BMJ Case Reports, JSCR (from 2010) | Yes; PFD no (2013) |
| 8 Sullivan colonoscopy (2007-12) | WebM&M, MAUDE (426 "colonoscope" reports by 2007-11), SDN | JSCR no (2010); BMJ Case Reports no (2008 launch [M5]); PFD no |
| 13 Canopy ERCP (2015-06) | WebM&M, MAUDE (59 "duodenoscope" reports by 2015-05) | Yes; MAUDE thin |
| 11 Russ-Jara drug–drug interactions (2023-12) | WebM&M medication cases. ISMP *Medication Safety Alert!* is subscription-based [D1], so it has no open route. FAERS quarterly files are raw structured extracts [D2]; whether they include narratives was not verified | Yes (WebM&M) |
| 12 Ede nursing escalation (2023-12) | PFD reports (deterioration deaths), WebM&M; allnurses forum (403 to a scripted fetch; terms not checked) | Yes |
| 15–16 Phillips MOUT (1998; 2001-08) | Center for Army Lessons Learned: some handbooks are limited to service members, DoD civilians and validated contractors [D3]; which ones are public release was not verified | Online availability before 1998 or 2001 unknown: **weak** |
| 17 Seamster en route ATC (1993-10) | NASA ASRS Database Online: de-identified narratives from 1988, more than 1,000,000 reports submitted, prevalence not inferable [A1]. NTSB CAROL: aviation investigations from 1962 [A2]. FAA SDR yearly files are maintenance records, not ATC [A3] | ASRS 1988–1993 only; NTSB yes. Docket transcripts before 1993 online: not checked |

## 3. Proposed `Source.kind` mappings (no new field)

These are host-rule additions to `classify_source` in `reconstruct/src/reconstruct/evidence.py`. That file is outside both the N1 semantics hash and the I7 freeze manifest, which hashes only `admission.py` from `reconstruct/`. `evidence.py` must be added to the manifest's file set, and the rules fixed, before gold (coverage-audit finding 15).

| Host(s) | `kind` | `boundary` | `voice` | Practice (fixed by `vocab.py`) |
|---|---|---|---|---|
| `firefighternearmiss.com`, `wildfirelessons.net`, `lessons.wildfire.gov`, `psnet.ahrq.gov`, `webmm.ahrq.gov`, `asrs.arc.nasa.gov` | `INCIDENT_REPORT` | `True` | `MIXED` | `REPORTED` |
| `cdc.gov/niosh/fire/*` (path-scoped, since `cdc.gov` is broad) | `INCIDENT_REPORT` | `True` | `EXPERT` | `REPORTED` |
| `judiciary.uk` PFD pages, `api.fda.gov` / `accessdata.fda.gov` (MAUDE), `ntsb.gov` reports | `INCIDENT_REPORT` | `False` | `EXPERT` | `REPORTED` |
| NTSB docket CVR and ATC transcripts | `LOG` | `False` | `EXPERT` | `DONE` (the only `DONE` route found) |
| `allnurses.com`; Reddit and `forums.*` (already covered) | `FORUM_POST` | `True` | `MIXED` | `REPORTED` |
| `academic.oup.com`, `casereports.bmj.com` | `STUDY` | `False` | `EXPERT` | `REPORTED` |

`boundary=True` for incident texts reads the `Source.boundary` docstring ("a novice's error forces an expert to articulate") in the wider sense §11 step 2 uses. That section lists incident reports as boundary texts, but the person who erred in a fatality report is not always a novice. `methods-critic` should rule on this before the rules are frozen.

Mapping MAUDE or NIOSH reports to `LOG` to make `has_done_support` fire would mislabel an account of work as a record of it, which is the Safety-II distinction the vocabulary encodes [19]. It is rejected.

## 4. Which dead features each source could revive

**Replay (L7 "before changing a rule").** Run on all six N2 runs under `reconstruct/runs/` (`research/ds7/replay.json`; §3's hosts, with `cdc.gov` path-scoped to `/niosh/fire`):
- **The three N3 ledgers** (PLC, GDPR v1, GDPR v2):
  - cited sources: 19, 13 and 18, with 0 boundary under the current rules and 0 under the proposed rules;
  - every URL the sidecars record (47, 31 and 30, including search hits and fetch failures): 0 boundary under either rule set, and 0 hits on any proposed host.
- **The three failed runs:** 0 cited sources. Their sidecars record 26 URLs, one of which is boundary under the current rule: `plctalk.net/technical-articles/…` in `20260928T145115Z-518f99363336`.

So the proposed rules flip **0 records** and shrink no downstream sample on the N3 ledgers. They change something only if retrieval reaches these hosts. That is untested in the gold domains, and measuring it needs a paid, search-only probe. The plctalk page shows one more risk: a host-level rule marks an article on a forum host as a forum post. Boundary rules should therefore be path-scoped to thread URLs (`/threads/`, `/comments/`, `/questions/`) (*inferred*).

| Feature | What revives it | Okoli | Madani | Logishetty | Fallbacks |
|---|---|---|---|---|---|
| `n_boundary_sources` | A boundary host retrieved into an area. Needs site-scoped queries or a dated-corpus adapter as well as host rules. To leave I6's "dead" class it must also take ≥ 2 values within a ledger | **Possible**: NIOSH, near-miss (Wayback), r/Firefighting; US sources only | **Possible**: WebM&M, SDN; procedure-specific volume unknown | **Possible**: WebM&M, SDN, PFD | Surgical ranks as Madani; ATC via ASRS; military weak |
| `imagined_only` | Any `REPORTED` or `DONE` source in an area. It becomes live together with `n_boundary_sources`, and also through case reports (`STUDY`) | Possible | Possible | Possible | As left |
| `has_done_support` | A `DONE` source. None of the World A text found qualifies outside aviation | **Dead** | **Dead** | **Dead** | Rank 17 only (NTSB transcripts as `LOG`), if dockets before 1993 are online (unchecked) |
| `latest_source` (dead; `earliest_source` is already live in PLC and GDPR v2 per I6) | A document-field date in more than one source per area. Case reports carry `citation_publication_date`; MAUDE `date_received` and ASRS dates need an adapter; Wayback timestamps serve in dated-corpus mode; forum and NIOSH pages are untested | Partial (Wayback, PDF dates) | Partial (case reports) | Partial (case reports, MAUDE adapter) | As left |

## 5. Is there evidence that boundary texts hold the "obvious" steps expert text omits?

**Mechanism: literature-supported.** Text frequency does not track world frequency; people under-report what is obvious [25]. Experts asked to describe a procedure omit much of it unprompted [1]. `REORIENTATION.md` §8 records 25 of 70 NICU cues absent from the training literature [4], as reported in [3].

**Direct, but outside the gold domains.** Topic analysis of Stack Overflow questions against the PHP and Python documentation found topics the documentation did not cover [S1]. That is novice-asks-expert-answers text holding what the expert documentation omits, but in software.

**In-domain: the material exists, but its content is unmeasured.**
- In 232 surgical M&M presentations at 4 US academic hospitals, 72% included adverse events and 42% included errors causing an adverse event. 77% of those errors were discussed as errors, and 79% of surgical errors were attributed to a cause. Leaders rarely used explicit error language [S2]. Surgical M&M does put errors on the table, but those were live conferences, not published text.
- Near-miss narratives from the fire service are long free text; the better of two Bayesian autocoders (Fuzzy) reached a sensitivity of 0.74 (Naïve 0.678), with injury records coded more sensitively than near misses [S3]. The corpus is analysable, but nobody has measured whether it holds steps that expert text omits.

**Counter-evidence.** Incident systems have their own reporting bias. ASRS states that its reports are voluntary, are subject to self-reporting bias and cannot be used to infer prevalence [A1]. An incident text records an "obvious" step only when that step failed (*inferred*).

**No study was found** that compares boundary texts with expert-to-expert texts in surgery or fire command for omitted steps. The sign of `n_boundary_sources` can be pre-registered from [25] (more boundary text, fewer missed items). Its size cannot, because it has zero variance in every in-sample ledger.

## 6. Decision (owner, 2026-10-24: option 1)

**Question:** Should the E-CTA pre-registration revive the dead features, or state that it tests size, density, type and the lens signal only?

1. **Primary test on size, density, type and the lens signal only. Declare `has_done_support` dead for World A text. Register `n_boundary_sources` and `imagined_only` as secondary features, which enter only if a gold-blind, search-only retrieval probe in the gold's domain, run before freeze, shows them taking ≥ 2 values across areas (threshold fixed before the probe) (Recommended).**
   - *For it:* on the N3 ledgers the replay finds 0 boundary sources of 50 cited, and 0 of 108 recorded URLs, under either rule set, so host rules alone revive nothing. No `DONE` source exists for any primary gold. The in-domain evidence for the feature's effect is indirect (§5). The PLC and GDPR ledgers give the feature zero variance, so no weight can be set in-sample, and an uncalibrated primary feature would make the headline depend on an untested retrieval change.
   - *What would change it:* a probe showing boundary hosts in most areas of a gold domain with real spread. The feature could then be promoted to primary in the same pre-registration, before gold.
2. **Revive `n_boundary_sources` and `imagined_only` as primary features now.** Add the §3 host rules and site-scoped retrieval before the freeze. This is the more direct test of §14.2's hypothesis. But it puts an unmeasured retrieval change on the critical path, and it fixes a feature direction and weight with no in-sample variance.
3. **Revive every dead feature, mapping incident reports to `LOG` so that `has_done_support` fires.** This is the weakest option: it mislabels reported work as done work [19], and the feature would then measure the mapping, not the evidence.

## Deviations

- The `research` skill asks for a background agent. This item ran directly in the fired agent, with no subagent.
- Several sites refused scripted fetches (psnet 405, judiciary.uk 405, SDN 403, allnurses 403, lessons.wildfire.gov 403). Their facts come from search-engine extracts of their own pages, or from Wayback counts.
- Wayback counts measure archived URLs, not reports, and include URL variants (psnet).
- No paid call was made. The retrieval probe in §6 is not run here.

## References

Numbered references [1], [3], [4], [19] and [25] are `REORIENTATION.md` §26.

- [G1] Okoli J. 2020. Expert knowledge elicitation in the firefighting domain and the implications for training novices. *IJDRBE*. doi:10.1108/IJDRBE-09-2020-086. Metadata only (OpenAlex W2805342423).
- [F1] NIOSH. Fire Fighter Fatality Investigation and Prevention Program. https://www.cdc.gov/niosh/firefighters/fffipp/index.html
- [F2] NIOSH. FFFIPP reports and programme history. https://www.cdc.gov/niosh/fire/ ; https://stacks.cdc.gov/view/cdc/5991
- [F3] National Fire Fighter Near-Miss Reporting System. https://en.wikipedia.org/wiki/National_Fire_Fighter_Near-Miss_Reporting_System ; https://ohsonline.com/articles/2009/12/17/reporting-system-reaches-reports-goal.aspx
- [F4] IAFC launches near-miss reporting system. https://www.ehstoday.com/archive/article/21906766/iafc-launches-near-miss-reporting-system-for-the-fire-service
- [F5] Wildland Fire Lessons Learned Center. https://lessons.wildfire.gov/blog/2021-03-15/where-are-the-lessons ; https://www.frames.gov/catalog/88
- [F6] Prevention of future deaths report. https://en.wikipedia.org/wiki/Prevention_of_future_deaths_report
- [F7] Fire Standards Board, Operational learning. https://www.firestandards.org/?p=676
- [P1] Reddit, "API update: continued access to our API for moderators" (r/modnews, 2023-05-31), https://www.reddit.com/r/modnews/comments/13wshdp/ (403 to scripted fetches; read from search extracts of mirrors, so unverified at source)
- [M1] AHRQ PSNet, WebM&M case studies. https://psnet.ahrq.gov/webmm-case-studies (405 to scripted fetches; read from a search extract).
- [M2] UCSF News, 2003-02. New web-based medical journal will draw patient safety lessons from actual cases. https://ucsf.edu/news/2003/02/97244/new-web-based-medical-journal-will-draw-patient-safety-lessons-actual-cases
- [M3] openFDA, Device adverse event API. https://open.fda.gov/apis/device/event/
- [M4] DOAJ, Journal of Surgical Case Reports. https://doaj.org/toc/2042-8812
- [M5] Becker Library, BMJ Case Reports now available. https://becker.wustl.edu/news/bmj-case-reports-now-available/
- [M6] Student Doctor Network Terms of Service. https://forums.studentdoctor.net/help/tos
- [D1] ECRI, ISMP Medication Safety Alert! Acute Care. https://home.ecri.org/products/ismp-medication-safety-alert-%C2%AE-acute-care
- [D2] FDA, FAERS latest quarterly data files. https://www.fda.gov/drugs/fdas-adverse-event-reporting-system-faers/fda-adverse-event-reporting-system-faers-latest-quarterly-data-files
- [D3] Army.mil, The Center for Army Lessons Learned publishes Operations Officer Handbook. https://www.army.mil/article/40590/the_center_for_army_lessons_learned_publishes_operations_officer_handbook
- [A1] NASA ASRS, About ASRS data. https://asrs.arc.nasa.gov/search/dbol/aboutdata.html
- [A2] NTSB, CAROL help. https://www.ntsb.gov/Pages/carol.aspx
- [A3] FAA, Download Service Difficulty Reports by year. https://www.faa.gov/av-info/download_SDR (403 to scripted fetches; read from a search extract).
- [S1] Campbell JC, Zhang C, Xu Z, Hindle A, Miller J. 2013. Deficient documentation detection. *MSR 2013*. doi:10.1109/MSR.2013.6624005
- [S2] Pierluissi E et al. 2003. Discussion of medical errors in morbidity and mortality conferences. *JAMA* 290(21). doi:10.1001/jama.290.21.2838
- [S3] Taylor JA, Lacovara AV, Smith GS, Pandian R, Lehto M. 2013 (online; vol. 62, 2014). Near-miss narratives from the fire service: a Bayesian analysis. *Accid Anal Prev* 62:119–129. doi:10.1016/j.aap.2013.09.012
