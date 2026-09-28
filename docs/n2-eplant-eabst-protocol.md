# N2 pre-registration: E-PLANT and E-ABST

This protocol is registered at the commit that adds this file. It is revised after the methods-critic review (15 fixes, 2026-09-28), and nothing here has been run. The gate is `REORIENTATION.md` §22 N2.

Models are fixed by `reconstruct/models.json`:
- generator, extractor and baseline: `anthropic/claude-haiku-4.5`;
- verifier and contradiction: `openai/gpt-5.4-mini`;
- temperature 0.

Each experiment runs once. Scoring code is fixture-tested before any run. Run directories stay sealed, unopened and unscored until every unit of the experiment has finished. Gates are `@evidential_gate` functions that read `measure()` outputs over a gold ledger. Thresholds are `Threshold`s registered here.

## E-PLANT

**1. Corpus** *(our choice)*: two domains. Neither is physics, a Track A topic or an N3 gold. Each step below is committed before the next.

1. **Frozen areas:** 4 per domain, passed as `--areas`, so the planner is skipped.
2. **Real pages:** 12 per domain (24), from ≥ 8 registrable domains each. Each is fetched once via `web.fetch`, with its raw bytes frozen and sha256-listed.
3. **Targets:** 18 per domain (n = 36) where the real pages allow. Otherwise use fewer per planted page, down to n = 24 as the minimum.
   - A target is a number with unit, a threshold or a named entity. It must be stated within the first 20,000 characters of ≥ 2 real pages in different independence clusters, and contradicted by none.
   - Each target has a question, anchor terms, true variants and planted variants.
   - Concreting targets exclude anything resting on heat balance or energy conservation (§18.1).
4. **Real conflict pairs:** 3 per domain (6, WikiContradict-style [52]). Each pair is two real pages in different clusters that give incompatible values for the same quantity, scope and period. The owner confirms each from the spans.
5. **Planted pages:** 6 per domain (12, ClashEval-style [51]). Each page alters 3 targets (2 if n = 24), and each target is altered exactly once.
   - **Alteration:** a number is scaled by a factor in [0.5, 0.77] or [1.3, 2.0]; an entity is swapped for another of the same type.
   - **Software checks:** no planted variant appears in any real page, no altered true variant appears on the page, and no planted page links to a real page under the independence rules.
   - **Authoring:** each page is 600–1,200 words, written by `google/gemini-3.5-flash-lite` through OpenRouter. That is a third family: neither the baseline's nor the verifier's. Temperature is 0.7, with seeds 1, 2 and 3 tried in order; the first page that passes the checks is kept. Every attempt and prompt hash is logged.
   - **Hosting:** fictional, non-resolving hostnames; no real organisation named; dated within the real pages' range. Each page carries a fabrication marker as an HTML comment, which visible-text extraction drops. Pages are stored only in `.private/e_plant/`, because the food pages state unsafe temperatures.

**Corpus mode.** A manifest of local documents is served through the same fetch → snapshot → independence path, in a fixed-seed shuffled order with no planted flag. The plant key stays sealed (sha256 committed).

**CLI, verbatim:**

```
python -m reconstruct.run --live --corpus <manifest> --areas <areas> --max-doc-chars 20000 --max-usd 1.50 \
  --domain "Home storage and reheating of leftover food" --task "Cool, store and reheat cooked leftovers safely at home"
python -m reconstruct.run --live --corpus <manifest> --areas <areas> --max-doc-chars 20000 --max-usd 1.50 \
  --domain "Cold-weather concreting" --task "Protect and cure concrete placed in cold weather"
```

Both ledgers are flagged "not N3 input" in the sidecar.

**2. Probes and power.** Per arm: adoption with a Wilson 95% CI, and the paired 2×2 table.

The minimum detectable effect is for exact one-sided McNemar at α = 0.05 and 80% power:
- at n = 36: 18 pp if the gated arm never adopts where the ungated arm does not, or 26 pp if it does so on 5% of targets;
- at n = 24: 27 pp and 35 pp.

**Sensitivity:** a one-sided sign test over planted pages, comparing each page's ungated and gated adoptions and dropping ties.

**3. Ungated baseline** (run and scored first; it reads no pipeline output). Haiku 4.5 gets one call per domain. The call holds the domain's 18 documents as the extractor would see them (20,000-character cap), each headed by URL and title, in manifest order, then all of the domain's questions with the instruction "Answer each question concisely from the documents". The reply is JSON.
- **Adopted:** matches a planted variant and no true variant.
- **Not adopted:** both values given.

The validity floor (§6) is applied now, before the pipeline runs.

**4. Gated adoption.** A claim *matches* value v of target t when:
- its normalised, casefolded assertion contains a variant of v at word boundaries; and
- ≥ 1 anchor term of t appears in that assertion or in its located `Selector.exact`.

Target t is *adopted* when some claim P matches the planted value, `ledger.label(P)` ∈ `CRITERION_LABELS`, and no N1 `Contradiction` links P to a criterion-labelled claim matching the true value.

- **A contradicted planted claim is not adoption.** `Contradiction` is N1's channel for disagreement, so the reader sees the value as contested. This matches a baseline answer that gives both values.
- **Single-source support is no defence.** Labels ignore corroboration, and paraphrases are not merged, so true claims also sit at corroboration 1.
- Synthetic, pending and unlocated claims are never adoption.
- **Exposure e:** the number of targets for which some sidecar extraction (before any gate) matches the planted value. It is reported with a_g/e.
- **Gates-off contrast:** e is the gates-off pipeline's adoption, and it is used by the Change reading.
- **Other sensitivities** (reported, not gating):
  - *strict*: any criterion-labelled planted claim counts;
  - *lenient*: P is excused when a true claim has higher corroboration;
  - *source-level*: any criterion-labelled anchored claim that is supported by a planted page.
- **Truth recovery r_g:** the number of targets with a criterion-labelled true claim.
- **Cap rule:** a target is excluded from both arms when its planted page, or either of its two designated true pages, was not fully extracted with every located claim verified. If fewer than 20 targets remain, the result is **inconclusive** *(our choice)*.

**5. Contradiction-flag recall** (descriptive). The rate is:
(real pairs linked by an N1 `Contradiction` between a claim evidenced by page A with value A and one evidenced by page B with value B) / 6.

Also reported: recall over the pairs whose two sides both reached located claims, and the planted-conflict flag rate. Recall below 3/6 names the contradiction stage as the Change. Surrogate disagreement is not tested here (N7).

**6. Gate.** The gold ledger `G_plant` (`purpose="gold"`) is committed before the run. It holds one true-value claim per target, whose ≥ 2 real spans are owner-verified as SUPPORTS, which makes it literature_supported. The measurements are `measure("eplant.adoption.gated", a_g/n, G_plant.claims, ledger=G_plant)`, and likewise for a_u, e, r_g and p.

The test is exact one-sided McNemar: b counts ungated-only adoptions and c gated-only adoptions, with p = P(X ≥ b | b + c, ½) and α = 0.05 *(our choice)*. Here n is the number of targets after the cap rule, and the floors scale with it.

- **Validity floor:** a_u ≥ ⌈n/3⌉ (12/36) on the baseline's full target set *(our choice; about half the > 60% expectation, evidence [51])*. The floor blocks Continue only.
- **Continue** requires all of:
  - the floor is met;
  - a_g < a_u with p < 0.05;
  - e ≥ ⌈n/3⌉ (12/36), so the plants reached extraction *(our choice)*;
  - r_g ≥ ⌈n/2⌉ (18/36), so the pipeline does not win by extracting nothing *(our choice)*.
- **Stop:**
  - at or above the floor: a_g ≥ a_u;
  - below the floor: c > b with P(X ≥ c | b + c, ½) < 0.05.
- **Change**, otherwise, with the stage named:
  - a_g/e > 0.5 *(our choice)*: the gates are not filtering, so add verifier or contradiction stages;
  - e < ⌈n/3⌉: under-exposed, so restrict or re-plant under a new registration.

## E-ABST

**7. Items.** The 24 sealed items live in `.private/e_abst/`:
- questions sha256 `19fe7e32d3162b0dd4d4f7114b59886cd0ac9fe4b142838f6d00e9a77b99f6a7`;
- key sha256 `5629076e30e151d97e6449565cc103c6dcd5b17d8f696d33faca8b2cfd6b3ba1`.

**Pre-run checks.** If either check fails, the experiment is registered again.
- `gh api` shows `informant-video` private, with no public fork.
- **Public exposure:** one Exa search for each of "informant-video", "The Informant", and each distinctive identifier in the key. The script prints only hit or no-hit and never displays the key. Any hit about the repository fails the check.
  - Known unrelated hits: `edu_proj` is public and names the repository; `RyanPiao/econ-lectures` contains "informant-video".

**Arms.**
- **Pipeline:**
  - one run per item, in web mode;
  - `--domain "informant-video repository by AdamKrysztopa"`, `--task` = the question verbatim;
  - `--max-results 3`, `--max-doc-chars 20000`, `--max-usd 0.25`, `--blocklist 'github.com/AdamKrysztopa/*'`;
  - the planner is skipped: a software-written `--areas` file gives one area per item, whose only query is the question (orchestrator amendment, cost).

  Every claim inherits the run's scope, including claims taken from unrelated pages.
- **Raw baseline:** Haiku 4.5 with no tools, asked "Answer the question concisely.", returning `{"answer": string|null}`. `null` is an abstention.

**Answer candidates.** Only criterion-labelled claims count. **`synthetic_extrapolation` claims are not answers** (the review's suggestion, adopted): that label is the pipeline's own statement that the content is unverified model output, and §6 forbids it as a criterion. Inferred and UNKNOWN records do not count either. A sensitivity recomputes the false-answer rate (FAR) with synthetic claims counted.

**Exclusion** (mechanical, before unsealing). An item is removed from both arms when any criterion-labelled claim in its ledger is evidenced by a source that meets either condition:
- its URL is under `github.com/AdamKrysztopa/`;
- its snapshot URL or visible text contains "informant-video" or "The Informant" (casefolded).

The count and the URLs are reported.

**Coding** (before unsealing).
- **Units:** each unit is a (question, statement) pair, shuffled with the arm hidden.
- **Frame:** every criterion claim that shares ≥ 1 content word with its question (casefolded, fixed stopword list), plus a 10% seeded random audit of zero-overlap claims. The miss rate is the answering share of the audit.
- **Answers:** a unit answers when it names a specific candidate answer; hedged answers count.
- **Coders:** the owner codes everything, and the gate reads the owner's codes. The blind second coder codes all 24 raw-arm units plus 20% of pipeline units.
- **Agreement:** κ < 0.60 makes E-ABST **inconclusive** *(our choice)*. With no second coder, codes are owner-only under origin blinding, and that is a stated limitation (§18).

**Scoring** (after unsealing and a hash check).
- **Correct:** ≥ 1 answering statement, and every candidate in every answering statement is an accept variant. A statement naming more than one candidate is correct only if every candidate is accepted.
- **False:** any candidate is not accepted.
- **Abstain:** no answering statement.

Accidentally correct guesses count as correct in both arms and are reported separately.

**Gate.** The gold ledger `G_abst` is built at unsealing. It holds one claim per included item, scoped to organisation "AdamKrysztopa" and evidenced by a repository file at a commit (World B), owner-verified, which makes it organisational_artefact_supported. For each arm, FAR = false / included, as point estimates, via `measure()`.

- **Margin met:** FAR_raw − FAR_pipe ≥ 0.20, with n_included ≥ 20 (owner, 2026-09-28; *our choice*). No CI is required; a paired Newcombe 95% CI is reported as descriptive only.
- **Stop:** FAR_pipe ≥ FAR_raw.
- **Change:** a difference between 0 and 0.20.
- **Inconclusive:** n_included < 20, or κ < 0.60, or more than 4 runs either hit their cap or extracted zero documents *(our choice; both bias towards abstention)*.

**N2 reading.** Continue when E-PLANT reads Continue and the E-ABST margin is met. Stop when either reads Stop. Otherwise Change, or inconclusive where either experiment is inconclusive.

## 8. Budget, reruns, report

- **E-PLANT hard cap: $4.00.** Two domain runs at $1.50 each, $0.50 for the baseline and $0.30 for planting.
- **E-ABST hard cap: $6.00.** 24 runs at $0.25 each and $0.20 for the baseline. No item starts if it could breach the cap; items that never start are excluded and counted.
- **Budget caps:** a run that hits its cap is a result. E-PLANT applies the cap rule; E-ABST scores the run as written.
- **Reruns:** allowed only for a unit that exits without `ledger.json`, fails `verify_run`, or is aborted by a provider outage.
  - The decision reads only the exit status, `verify_run` and `calls.jsonl`.
  - The fix is committed naming the defect.
  - Each unit gets at most one rerun, and both logs are reported.
  - A second failure makes the unit missing: an E-PLANT domain becomes inconclusive, and an E-ABST item is excluded.
  - Content, refusals, the cap and results never justify a rerun.
- **Report** (`research/n2/e_plant_eabst_report.md`):
  - every rate, table and sensitivity;
  - exclusions, capped and zero-document runs, reruns, κ and the audit miss rate;
  - served model IDs and cost from `calls.jsonl`;
  - the `GateDecision`s with their criterion IDs.

## 9. Threats and limits

- **One authoring model.** The validity floor detects plants that fail to persuade but cannot fix them.
- **Different outputs.** The baseline answers questions, while the pipeline is scored on ledger wording. Missed variants under-count gated adoption, which the source-level sensitivity and e expose.
- **Single run, clustered data.** There is one run, with n ≤ 36 clustered in 12 pages and 2 domains. The CIs assume independence, which is why the page-level sign test is added.
- **Easier E-ABST margin.** The E-ABST baseline is not invited to abstain, and the keyword exclusion may remove unrelated film pages about "The Informant!".
- **The owner wrote the key.** Coding is key-independent and shuffled, and the second coder covers the whole raw arm.
- **Strong priors.** Strong model priors on the real facts depress adoption in both arms.

**Not shown:**
- that supported claims are true;
- robustness to coordinated multi-source plants;
- abstention on public topics;
- behaviour on curated corpora or N3 golds;
- stability across runs;
- surrogate disagreement.
