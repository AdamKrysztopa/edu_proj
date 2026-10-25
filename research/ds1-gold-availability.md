# DS1: which CTA golds are itemised and obtainable?

**Result (2026-10-24): fewer than 3 golds are confirmed eligible. None is.** No candidate's metadata confirms that its full list is printed, or supplied, in a document we can obtain (condition C4). That is the only condition still open for 17 candidates, which pass C1–C3 on their abstracts and have a legal access route. They are **provisionally eligible**, and 16 of them are new to the project. V2's minimum of 3 golds, and the type-prior baseline's 2, are therefore *reachable but unconfirmed*. Author and publisher enquiries settle C4 without exposure, and drafts are in `research/ds1-author-contact/`.

**Decision it feeds:** the MS2 eligible-gold list and the type-prior baseline (`report/sections/17_validation.tex:233-246`, `26_risks.tex:51-59`). Under the item's rule, "fewer than 3" means the MS3 route is dead unless the owner decides otherwise. This note **does not** declare it dead: the open condition can be answered by author contact, which the eligibility rule permits. That decision belongs to the owner and is put to them in §6.

**RQ-I (text-poor test):** not possible NOW. No text-poor candidate passes C1 and C2 at metadata level. The leads are PARI [106], Schaafstal 2000, Dadashi 2020 and Kancler 2005; all need an enquiry.

**Method.** OpenAlex (`resolve_references`, `get_work`, `list_citations`), PubMed abstracts and publisher landing pages were read for access, licence and supplement labels only, retrieved 2026-10-24. One search pass covered the five named candidates. Two more searched for CTA studies with published multi-expert outputs, 1990–2025: one in medicine and nursing, one in maintenance, process control, military and aviation. The medical pass screened 276 PubMed records with a script that printed only count phrases and words near location terms. No PDF, full text, results table or supplementary file was opened. Every fact below comes from an abstract or metadata record unless marked *inferred*. The dated-corpus floor (`17_validation.tex:236-237`) is DS5's job and is not assessed here. `citation-verifier` passed on 2026-10-24, after two rounds of fixes: two missed type splits (Madani, Dias), one unsupported count (Mumaw) and stale ranks.

## 1. Eligibility conditions

From `17_validation.tex:235-238`, recorded per candidate as y / n / ?:

- **C1 itemised:** the abstract or metadata states a list of steps, decisions or cues, with a count.
- **C2 multi-expert CTA:** built by CTA from more than one expert.
- **C3 domain:** not PLC, GDPR or Track A physics. Every candidate here passes.
- **C4 obtainable:** a legal access route exists *and* the list sits in a document on that route. The access route is known for every candidate. Whether the list is actually printed there is "?" for all of them, because metadata never says.

**Verdicts:** **P** = provisionally eligible (C1, C2 and C3 are y; only C4's location is ?). **U** = C1 or C2 is ?. **R** = a review, not a gold. **X** = excluded.

## 2. Register

"Date" is the first-online date. "Location" is what the abstract or landing page names, never what was seen. Licence "publisher ©" means OpenAlex records no licence for a closed article (*inferred* to be publisher copyright).

| # | Gold | DOI / ID | Date | Itemised | Location | Item count (stated) | Experts | Access | Licence | C1/C2/C3/C4 | Verdict | Rank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Sullivan et al., cricothyrotomy [1] | 10.1097/ACM.0000000000000224 | 2014-03 | y | ? (generic "Supplementary Data" tab, no named files) | 46: 14 knowledge, 27 action, 5 decision | 6 (3 + 3) | OUP, paywalled, purchasable | publisher © (AAMC) | y/y/y/? | P | 1 |
| 2 | Okoli, firefighting incident command | 10.1108/IJDRBE-09-2020-086 | 2020-08 | y | in article (form not stated); OpenAlex pages 577–578 look too short | 134 decision points; 42 cues in 5 types | 31 | Emerald, free to read (bronze) | publisher © | y/y/y/? | P | 2 |
| 3 | Logishetty et al., anterior total hip arthroplasty | 10.2106/JBJS.19.00121 | 2019-09 | y | an open-access web training tool built from the CTA; place in the article not stated | 11 phases, 46 steps, 36 decisions, 42 errors | 4 | Wolters Kluwer, paywalled; web tool not checked | publisher © | y/y/y/? | P | 4 |
| 4 | Grover et al., open transversus abdominis release (TAR) | 10.1097/SLA.0000000000005756 | 2022-11 | y | ? | 10 steps, 80 subtasks, 17 decisions | 4 | LWW, paywalled | publisher © | y/y/y/? | P | 5 |
| 5 | Grover et al., robotic Roux-en-Y gastric bypass (RYGB) | 10.1007/s00464-023-10354-w | 2023-09 | y | 2 supplementary files listed (contents unknown) | 8 steps, 83 subtasks, 15 decisions | 4 | Springer, paywalled | publisher © | y/y/y/? | P | 6 |
| 6 | Smink et al., laparoscopic appendectomy | 10.1016/j.amjsurg.2011.11.002 | 2012-02 | y | a "master cognitive demands table" (form only) | 24 steps, 27 decisions | 3 | Elsevier, paywalled | publisher © | y/y/y/? | P | 7 |
| 7 | Sullivan et al., colonoscopy | 10.1016/j.amjsurg.2007.08.051 | 2007-12 | y | ? | 26-step checklist, 16-step cognitive demands table | 3 | Elsevier, paywalled | publisher © | y/y/y/? | P | 8 |
| 8 | Karamchandani et al., meniscal repair | 10.1177/03635465211021652 | 2021-06 | y | ? | 55 steps in 9 phases | 3 | OA (PMC8283189) | CC BY-NC-ND | y/y/y/? | P | 10 |
| 9 | Russ-Jara et al., drug–drug interaction management | 10.1136/bmjopen-2023-075512 | 2023-12 | y | ? | 4-step model, 19 cues | clinicians, number not stated | OA | CC BY-NC | y/y/y/? | P | 11 |
| 10 | Ede et al., nursing escalation of deteriorating patients | 10.1016/j.ijnurstu.2023.104671 | 2023-12 | y | ? | 8 prescribed + 24 additional tasks | 30 interviews | OA | CC BY-NC | y/y/y/? | P | 12 |
| 11 | Canopy et al., endoscopic retrograde cholangiopancreatography (ERCP) | 10.1016/j.amjsurg.2015.05.006 | 2015-06 | y | "protocol" (form only) | 180 steps (decisions not counted) | 11, refined by 5 | Elsevier, paywalled | publisher © | y/y/y/? | P | 13 |
| 12 | Plumptre et al., bimanual vaginal examination | 10.1002/ijgo.12260 | 2017-07 | y | ? | 88 steps reduced to 30 | 10 and 5 (roles unresolved) | Wiley, paywalled | publisher © | y/y/y/? | P | 14 |
| 13 | Dias et al., cardiac surgery team | 10.1097/SLA.0000000000003489 | 2019-07 | y | ? | 137 cognitive elements in 4 stated types, of which only decision points (33) is a step, decision or cue type | 9 | green OA (PMC7241253) | author manuscript; VoR publisher © | y/y/y/? | P | 9 |
| 14 | Seamster et al., en route air traffic control | 10.1207/s15327108ijap0304_2 | 1993-10 | y | ? | 13 primary tasks, 3 strategy categories | controllers, number not stated | T&F, paywalled | publisher © | y/y/y/? | P | 17 |
| 15 | Madani et al., laparoscopic cholecystectomy | 10.1016/j.jamcollsurg.2015.07.450 | 2015-08 | y | ? (pages to 940.e8 suggest an online appendix, *inferred*) | 14 tasks; 108 cognitive elements in 3 stated types (35 / 47 / 26) | 10 | LWW (current DOI target), paywalled | publisher © | y/y/y/? | P | 3 |
| 16 | Phillips et al., urban-operations (MOUT) small-unit leaders | 10.1037/e444522005-001 | 1998 | y | decision requirement tables | not stated | 7 | PsycEXTRA, closed | ARI contractor report | y/y/y/? | P | 15 |
| 17 | Phillips et al., decision-centred MOUT training | 10.21236/ADA395934 | 2001-08 | y | ? | 11 decision requirements | Army personnel, number not stated | free (HathiTrust, DTIC) | ARI contractor report; distribution statement unverified | y/y/y/? | P | 16 |
| 18 | Crandall & Getchell-Reiter, NICU sepsis cues [4] | 10.1097/00012272-199309000-00006 | 1993-09 | ? | probably a separate Klein Associates guide (Crandall & Gamblian 1991), not found online | not stated ("70 cues" unverified) | not stated | LWW, paywalled | publisher © | ?/?/y/? | U | — |
| 19 | Chao & Salvendy, troubleshooting knowledge vs number of experts [2] | 10.1080/10447319409526093 | 1994-07 | ? | no list mentioned | not stated | 1–6 per condition | T&F, paywalled | publisher © | ?/y/y/? | U | — |
| 20 | Hall, Gott & Pokorny, PARI guide [106] | 10.21236/ada303654 | 1995-10 | ? | worked analyses not mentioned | not stated | methods drawn from >200 technicians | DTIC, approved for public release (from a search extract) | US government work, *inferred* public domain | ?/?/y/? | U | — |
| 21 | Schaafstal, Schraagen & van Berlo, naval radar troubleshooting | 10.1518/001872000779656570 | 2000-03 | ? (a strategy, not counted) | ? | not stated | 2 observational studies, n not stated | SAGE, paywalled | publisher © | ?/?/y/? | U | — |
| 22 | Dadashi, Golightly & Sharples, rail maintenance control | 10.1007/s10111-020-00636-x | 2020-06 | ? (decision-ladder model) | ? | not stated | operators in 3 types of centre | OA | CC BY | ?/?/y/? | U | — |
| 23 | Kancler et al., USAF aircraft maintenance troubleshooting | 10.1177/154193120504902310 | 2005-09 | ? | ? | not stated | n not stated | SAGE, paywalled | publisher © | ?/?/y/? | U | — |
| 24 | Al-Halabi et al., breast augmentation | 10.1016/j.jsurg.2023.03.003 | 2023-04 | ? (competencies, not steps, decisions or cues) | ? | 208 competencies, 41 pitfalls | 8 | Elsevier, paywalled | publisher © | ?/y/y/? | U | — |
| 25 | Kim et al., robotic thyroidectomy | 10.21037/gs-23-467 | 2024-03 | ? (skills and strategies) | ? | 89 items | 12 interviews, then Delphi panels | OA | CC BY-NC-ND | ?/y/y/? | U | — |
| 26 | Mansur et al., robotic right lower lobectomy | 10.21037/jtd-2025-118 | 2025-11 | y | ? | 32 steps | 7 | OA | CC BY-NC-ND | y/?/y/? (procedural map; whether it is CTA is unclear) | U | — |
| 27 | Craig et al., laparoscopic critical decisions | 10.1177/0018720812448393 | 2012-06 | y (decision requirement tables) | ? | not stated | 8 | SAGE, paywalled | publisher © | ?/y/y/? | U | — |
| 28 | Velmahos et al., central venous catheterisation | 10.1016/j.amjsurg.2002.12.005 | 2003-12 | ? | ? | not stated | not stated | Elsevier, paywalled | publisher © | ?/?/y/? | U | — |
| 29 | Clark et al., CTA review chapter [3] | book 10.4324/9780203880869 (the chapter DOI is unregistered) | 2008-09 | — | — | — | — | Routledge, closed | publisher © | — | R | — |

**Checked but not in the table.**
Years in this list are print years.
- *Itemised, but with no count in the abstract:*
  - Yates, Sullivan & Clark 2012, CVC and cricothyrotomy (doi:10.1016/j.amjsurg.2011.07.011);
  - Campbell et al. 2011, cricothyrotomy (doi:10.1016/j.jsurg.2011.05.007);
  - Lee et al. 2023, escharotomy, 5 experts (doi:10.1093/milmed/usad104);
  - Hegde et al. 2020, endoscopic submucosal dissection (doi:10.1007/s00464-019-06822-x);
  - Bhattacharyya et al. 2017 and 2018 (doi:10.2106/JBJS.17.00190; doi:10.1080/17453674.2018.1517442);
  - Yeung et al. 2017, plastic surgery skills (doi:10.1016/j.jsurg.2017.01.008).
- *Unclear whether CTA, or no step list:*
  - Pfandler et al. 2018, a task analysis, CC BY (doi:10.1186/s41077-018-0077-2);
  - Leedom et al. 2007, 11 skill areas (doi:10.1037/e587402011-001);
  - Lercel & Andrews 2021, uncrewed-aircraft (UAS) pilots, 16 experts, 6 task diagrams (doi:10.1080/24721840.2021.1895797);
  - Zupanc et al. 2015, a 27-element competency framework (doi:10.1186/s12909-015-0494-z);
  - Mumaw et al. 2000, nuclear operators, monitoring strategies (count not stated in the abstract; doi:10.1518/001872000779656651).
- *Open-access USC dissertations:* multi-expert gold-standard protocols, but no counts in their abstracts (Tirapelle doi:10.25549/usctheses-m3006; Bartholio doi:10.25549/usctheses-m3424; Canillas doi:10.25549/usctheses-m2953).
- *Excluded:*
  - Klein, Calderwood & Clinton-Cirocco 1988, fireground (doi:10.21236/ADA199492): before 1990.
  - Nauert & Gillan 2019, chainsaw troubleshooting (doi:10.1177/1071181319631536): a single expert.

## 3. Ranked eligible list (the MS2 candidates)

**Ranking rule.** It was written before any candidate was ranked and uses only the register's stated fields. Score = 2 × (the abstract gives a type split across steps, decisions or cues) + 1 × (3 or more experts stated) + 1 × (40 or more items stated) + 1 × (free or OA access to the article).
- Ties break by expert count, then by item count.
- Sullivan 2014 stays first because the report fixes the named candidates' order (`17_validation.tex:238-243`). It is also the only one with published comparator figures (44% unprompted, 66% prompted [1]).
- The 40-item cut is *inferred*. Area-level AUROC needs about 20 areas, split near 10 missed and 10 not missed, for a ±0.20 half-width (`docs/plans/n3-gap-map-plan.md:21`). The report's risk row flags golds covering under 15 missed areas (`26_risks.tex:51-54`).

| Rank | Gold | Score | Domain | Text-richness (*inferred*) |
|---|---|---|---|---|
| 1 | Sullivan 2014 | 4 | surgery | medium |
| 2 | Okoli 2020 | 5 | firefighting command | rich |
| 3 | Madani 2015 | 4 | general surgery | medium |
| 4 | Logishetty 2019 | 4 | orthopaedics | medium |
| 5 | Grover 2022 (TAR) | 4 | hernia surgery | medium |
| 6 | Grover 2023 (RYGB) | 4 | bariatric surgery | medium |
| 7 | Smink 2012 | 4 | general surgery | medium |
| 8 | Sullivan 2007 | 4 | colonoscopy | medium |
| 9 | Dias 2019 (only one of its 4 types is a step, decision or cue type, so no split) | 3 | cardiac surgery team | medium |
| 10 | Karamchandani 2021 | 3 | orthopaedics | medium |
| 11 | Russ-Jara 2023 | 3 | prescribing | medium |
| 12–14 | Ede 2023, Canopy 2015, Plumptre 2017 | 2 | nursing, endoscopy, gynaecology | medium |
| 15–16 | Phillips 1998, Phillips 2001 | 1 | military | rich |
| 17 | Seamster 1993 (tasks plus strategy categories are not counted as a type split) | 0 | air traffic control | rich |

Years here are the register's first-online dates, which differ from print years for Dias (2021), Logishetty (2020), Grover TAR (2023), Sullivan colonoscopy (2008) and Ede (2024).

**Caveats that bear on the pre-registration, for `methods-critic` and not decided here:**
- **Golds already known to the project.** Sullivan's and Crandall's structures are in the notes, and the type feature was derived from them (`REORIENTATION.md:441`). Leave-one-gold-out lets neither be a test gold for a feature drawn from it. The 16 new provisional golds carry no such exposure.
- **Diversity.** Ranks 1–11 are all clinical except Okoli, so a pooled V2 on the top three would test one non-clinical domain.
- **Okoli 2020's grain.** Its 134 decision points come from 31 incident accounts, so they are episode-level, not a canonical task list. The cue inventory may be the usable gold; this is *inferred*.
- **Dating.** The newer golds (2019–2025) fall inside the Wayback era, which helps the dated-corpus floor (`17_validation.tex:107-108`; DS5). The 2023–2025 golds may also postdate some open-weight models' cutoffs; this is *inferred*, and DS5 checks it.

**Count.**
- Confirmed eligible: **0**.
- Provisionally eligible: **17**. Pending only C4, that is ≥3 for V2 and ≥2 for the type prior.
- Unknown: **11**. Of the four non-Sullivan candidates the report names, three (Crandall, Chao & Salvendy, PARI) are U. The fourth, Clark et al. [3], is a review.

## 4. RQ-I: does a text-poor test become possible?

Only if an enquiry confirms an itemised, multi-expert list for one of these: PARI [106] (aircraft maintenance), Schaafstal 2000 (naval radar), Dadashi 2020 (rail maintenance, CC BY) or Kancler 2005 (USAF maintenance). Every one of them is U on C1. Every provisional gold is text-medium or text-rich (*inferred*; corpus size was not measured). So `REORIENTATION.md` §19's reading stands: RQ-I cannot be tested NOW.

## 5. Enquiries drafted (not sent)

`research/ds1-author-contact/enquiries.md` holds one paragraph per target. Each asks only whether the itemised list is published or can be supplied, and in what format and under what licence. Targets:
- the top 10 provisional golds (their C4 is ?);
- the 4 text-poor U candidates;
- Crandall & Gamblian 1991, through the Klein Associates successor.

Only the owner sends them.

## 6. Owner decision now due (`26_risks.tex:51-59`)

**Question.** With 0 golds confirmed and 17 provisional, pending only the list's location, should the MS3 route stay open?

1. **Keep MS3 open; send the top-10 enquiries now; fix the MS2 list when 3 or more replies confirm a printed or supplied list (Recommended).**
   - *For it:* 17 candidates pass C1–C3 and have a legal access route. The one open condition is exactly what the eligibility rule allows author contact to settle (`17_validation.tex:238`).
   - *Inferred:* the top 10 come from at least 6 independent groups, so 3 confirmations is plausible.
   - *What would change it:* replies showing that the lists are unpublished and will not be supplied for all but two.
2. **Fix a provisional MS2 list now; let the fallback ranks absorb any gold whose list proves missing when the sealed gold is acquired.** It is faster. But each miss wastes that domain's "first and only" reconstruction (`17_validation.tex:248`), and counts against V2.
3. **Treat "fewer than 3 confirmed" as final and take the interview-only pivot (`26_risks.tex:48`).** This is the weakest option: it discards 17 candidates on a condition nobody has yet tried to resolve.

## Deviations

- **Abstract-level exposure.** No list document was opened, but some abstracts read during screening named content beyond counts:
  - Craig 2012 named example key decisions.
  - Cioffi 2010 (midwifery, online 2008, doi:10.1016/j.midw.2008.05.004) named cue categories.
  - Canopy 2015 showed one category name.
  - Harris-Thompson 2006 (DTIC ADA521919) named its four cue categories.
  - Mumaw 2000 described its strategy classes.
  - Kancler 2005 named its process areas.

  None of this is recorded here or anywhere in the repo. The search contexts that saw it had no other role and are gone. If Canopy (rank 13) or Craig, Cioffi, Mumaw or Kancler becomes a gold, log this exposure in its pre-registration. Craig and Kancler are U; Cioffi, Mumaw and Harris-Thompson are not in the register.
- **Verifier exposure.** The citation check reported the names of Dias 2019's four element types to the coordinating context. These are category headings, not items. Nothing is recorded here beyond the fact that only one of them is a step, decision or cue type.
- **Search-engine extracts.** For two DTIC PDFs that were never fetched (ADA303654, ADA303597), a search engine returned cover matter and table-of-contents headings. No task, step or cue items appeared.
- **Landing pages.** The Springer pages for Grover 2023 (RYGB), Hegde 2020 and Nayar 2019 were indexed. Only their supplementary-file lists and an abstract methods snippet were displayed.
- **Breaches of §14.3:** none known. No gold is made ineligible by this pass.

## References

Numbered references are `REORIENTATION.md` §26: [1] Sullivan 2014, [2] Chao & Salvendy 1994, [3] Clark et al. 2008, [4] Crandall & Getchell-Reiter 1993, [106] Hall, Gott & Pokorny 1995. Every other source is identified by its DOI in the register; all DOIs were resolved with OpenAlex `resolve_references` or `get_work` on 2026-10-24.
