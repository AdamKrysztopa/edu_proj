# Plan: a topicality-controlled closure check on real ledgers (2026-10-27)

Branch `closure-topicality-check`. Directory `research/closure_topicality/` (new). Nothing under
`gapmap/src/`, `instrument/`, `residual/frozen/`, `research/n3/<domain>/` or
`research/results_manifest.json` changes; every committed output of I1c, I2 and D1b stays as it is.

Status: revision 3. `methods-critic` round 1: "would not run as designed" (B1–B5 blocking,
S1–S8, minors), all applied (§8). Round 2: one blocking finding (no L7.3 checks on the §3(b)
recount), applied. Round 3: **no blocking findings**, "would run it as revised".

## 0. Why

D1b (`research/d1b_rerun/RESULT.md`, plan `docs/plans/gapmap-fix-and-d1-rerun.md` §1.5, §2.2 G4)
showed that the two real-data closure nulls cannot certify a closure judge:

- **control2** (`gapmap/src/gapmap/control2.py`): a lexical-overlap stand-in (close an arm iff its
  summed content-word overlap with the seed and question reaches the median) gives +0.78 on both D1
  ledgers, +0.68 on PLC and +0.46 on GDPR v1, against sol's +0.13 and +0.23.
- **MEC**, the gap map's mismatched-evidence control (`gapmap/src/gapmap/checks.py:156`): the same
  stand-in gives +0.208 (cheap ledger) and +0.200 (top-tier), at the +0.20 pass line
  (`research/d1b_rerun/g4_standins.json`).
- Only G2, a constructed check with off-topic background, separates judges. gemma-4-31b-it passed it
  twice (under a disclosed amendment); gpt-6.1-sol passed its first gate run, and its second
  (P − N 1.00) since, which makes it eligible under D1b's rule. That run is the coordinator's
  report of 2026-10-27 and is not in this worktree (which holds only
  `research/d1b_rerun/g2/sol-gate1`); nothing here depends on it.

**Undecided arms.** `OpenAIJudge` has no retry: an exception in a call becomes a silent
`undecided` with no cache entry and no ledger line (`semantic.judge_retrieval`), which once
happened in sol's D1b G1 run. A rule that read undecided as "not closed" would favour stand-ins.
So in every run here (RT, gemma's control2, gemma's G1 retest) any undecided arm makes the run
**incomplete**: its verdict is not read, and it is reported as such. A call that fails after a
billed response is not in the ledger either, so the caps below leave $1.00 of the $3.00 line unused
as margin.

Measured on 2026-10-27 at $0 (to be committed as `nulls_t.py`): in control2's pairs the own arm's
summed overlap exceeds the donor's in 72/72 (D1 cheap), 44/45 (D1 top), 52/54 (PLC), 41/44
(GDPR v1) and 40/42 (GDPR v2) discriminable pairs. The retriever's scoring stems are a subset of
the prompt's seed-and-question words in every candidate of all five ledgers.

Three jobs, in this order: (1) a judge check on real ledgers that the overlap stand-in fails;
(2) redesigned control2 and MEC, or a demonstration that they cannot be repaired; (3) a re-read of
sol's I1c GDPR v1 reading, +0.23 [+0.07, +0.39] (noise-inflated [+0.05, +0.38],
`research/n3_control_v3/GUARD.md`).

**The binding constraint.** Every label that says a real ledger sentence does or does not state an
element must come from the owner (`CLAUDE.md`: synthetic output never feeds a gate; G2's
`require_confirmed`, `research/d1b_rerun/g2.py:95`). This work cannot reach the owner. So it runs
paid calls only where the labels that decide the verdict are already the owner's (the D1 split's
inserts), and builds a blind owner pack for everything else. No verdict that depends on a label the
owner has not given is read or reported.

## 1. The new check: RT (real-background topicality plants)

### 1.1 Design

RT is G2 moved onto real retrievals. Per topic, every arm shares the lens question, the seed (in
the prompt header only, as in control2's seed-free primary) and a **real background**: the first
`min(k, 7)` sentences of the topic candidate's own seed-free control2 arm (`PairSpec.own_other`).
Seven at most, so one insert fits under `JUDGE_A_CAP = 8`. For the 13 of GDPR v1's 44 pairs with
k < 7 (all 8 DISC pairs among them) the background is shorter; its length is reported per topic.
Where k = 8 the background lacks the 8th sentence sol judged in I1c. The insert has claim id
`insert` (as G2's `INSERT`), so `judge_retrieval`'s `a_hits` show whether it was cited
(`gapmap/src/gapmap/semantic.py:204`). Its position is drawn once per topic
(`random.Random(sha256(topic_id))`, over `len(background) + 1` slots) and is the same in every arm.

| Arm | Sentences |
|---|---|
| 0 | background only |
| P | background + a sentence that states the lens element |
| N | background + an on-topic concrete sentence that is not the element |
| R | background + random letters with P's word lengths |

G2's N+ arm is dropped; part II below tests real on-topic non-answers directly.

**Scoring by citation.** The reply lists the sentence numbers that state the element.
`hit(X)` = the arm is `closed` and `insert` is among its `a_hits`. Arm-level closure is reported as
secondary. Citation scoring removes D1b's R-arm problem (no `R_excess` amendment is needed).

### 1.2 Two parts of the verdict

- **Part I, inserts.** Decided by the insert labels.
- **Part II, real background.** A judge could reject authored N sentences yet still cite real
  on-topic sentences that do not state the element, which is the topicality explanation itself
  (finding B1). After both runs of every judge on a split, every background sentence cited by any
  judge in any arm, plus an equal number of uncited background sentences from the same topics
  (seeded draw), go into the owner pack, shuffled, with no judge, arm or cited mark, each under its
  topic's seed, question and element definition. Per judge and split, the share of its cited
  background sentences that the owner labels as not stating the element must be **≤ 0.25**. A judge
  that cites fewer than 5 background sentences on a split meets part II trivially; that is
  reported.
- Background sentences that already state the element can only lower hit(P) for a judge that cites
  one sentence; that biases RT against good judges, not for bad ones, and is reported (topics where
  the owner labels a cited background sentence as stating the element, hit(P) apart).

### 1.3 Two splits

- **D1 split (13 topics).** G2's 13 gate topics, with their P and N exactly as the owner confirmed
  them (`research/d1b_rerun/fixtures/`; part I labels are the owner's). Background: each topic's
  control2 spec on its D1 ledger; all 13 map to exactly one spec with the same seed text and
  question, k = 8. Cluster: G2's D1 anchor cluster (10 clusters).
- **GDPR v1 split (16 topics).** From control2's 44 discriminable GDPR v1 pairs (`pairs_sha256`
  equal to sol's I1c `129beef55ad6…`). One pair per seed cluster (`seeds[0]`), lens quotas DISC 3,
  WHY 3, HEDGE 3, SEL 2, RESULT 5, filled in the order of a seeded shuffle (seed 20261027), before
  any judge sees them and without reading any judge state. Clusters are all singletons, so its
  bootstrap is an ordinary one; background sentences shared between topics are counted and
  reported. **No paid call on this split before the owner confirms its pack**
  (`require_confirmed`, as G2).

### 1.4 GDPR inserts (built now, $0; marked SYNTHETIC with the spec's sha256)

- **Author:** a fresh subagent, from a fixed spec (`fixtures/insert_spec.md`), never the session
  that builds the arms. It sees the seed, the lens question, a one-line element definition and the
  background.
- **P** states the lens element for the seed. **N** is an on-topic concrete fact that is not the
  element (a date, a document or section reference, a role, a default, a format), on the same topic
  words as P and with about as many new words. About half of each carries a closing-lexicon word.
- **Checked in code, per topic** (`insert_problem`):
  - len(P) ≤ len(N) ≤ 1.10·len(P);
  - seed-and-question overlap: ov(P) ≤ ov(N) ≤ ov(P) + 1;
  - probe overlap (`semantic.primary_probe` stems: the anchor for DISC, the seed's stems
    otherwise): probe(N) ≥ probe(P);
  - novel content words (outside the seed and question): |novel(N) − novel(P)| ≤ 1;
  - specificity(N) ≥ specificity(P).
- **Per split:** P and N hits differ by at most 1 for the closing lexicons
  (`standins.CLOSING_LEXICONS`) and, separately, for every lexicon in `config.PATTERNS` (DEFN,
  CASE, SEL, HEDGE, CAUSE and DISCR among them, the cue words of the DISC, SEL and HEDGE questions).
- **Blind labeller:** a second fresh subagent sees, per topic, the inserts mixed with that topic's
  background sentences in random order, not told how many are inserts, and marks each sentence
  "states the element: yes / no". A topic stays if P is yes and N is no. A mismatch gets one
  rewrite and relabel; a second mismatch drops the topic, replaced from the shuffle order of the same
  lens. One round only. Under 12 kept topics: the GDPR split cannot be read.
- These labels are synthetic and only choose and rewrite fixtures. The owner pack holds the same
  mixed lists (about 16 × 8 sentences); the owner's labels decide parts I and II for GDPR, and
  background sentences the owner labels as stating the element mark those topics for the hit(P)
  report. Topics the owner rejects are replaced before any call.

### 1.5 Pass rule (fixed here, before any paid call)

Per judge, per split, per run, only `closed` counting:
- **Part I:** hit(P) − hit(N) **≥ 0.50**; cluster-bootstrap lower bound (5th percentile of 2,000
  resamples of whole clusters, seed 20261027) **≥ 0.30**; hit(N) **≤ 0.25**; hit(R) **≤ 0.10**;
  no arm undecided (an undecided arm makes the run **incomplete**, never a fail; no rescue re-ask).
- **Part II:** §1.2.

A judge **passes a split** iff part I holds in two cold-cache runs and part II holds. A judge
**passes RT** iff it passes every split that cleared §1.6. Until the owner's part II labels exist,
the verdict reads "part I: pass/fail; part II: pending", and nothing is called a pass.

### 1.6 L7.3 for RT ($0, before any paid call)

1. **Best reachable case:** 1.0 (cite P only), lower bound 1.0.
2. **Planted positive:** an oracle fake that cites the insert iff it is P passes. Plumbing only
   (lesson "A planted positive proven only on a marker-reading fake judge is not proven"); the real
   judges' P hits are the real plant.
3. **Stand-ins, on the real fixtures.** Each per-sentence statistic is used four ways: cite every
   sentence at or above the median over all sentences offered in the split's prompts; at or below
   it; the argmax; the argmin. Statistics: length; seed-and-question overlap (D1b's overlap stand-in
   per sentence); overlap fraction; probe overlap; idf-weighted overlap (idf over the split's
   sentences); novel content words; novel content words in sentences carrying an English function
   word (so random letters do not count); specificity; any closing lexicon; the lens-matched
   lexicon; coin flip (three seeds). Plus D1b's arm-level stand-ins (`gapmap.standins`) scored on
   arm closure P − N. **Every threshold, not only the median,** is swept for each statistic in the
   ≥ and ≤ directions, and the best is reported. A split is usable only if no stand-in passes part I
   at the median **and** none passes at its best threshold. Measured on the D1 split
   (2026-10-27, scratch): the best of all sweeps is novel content words at ≥ 9, P − N +0.46, lower
   bound +0.27, which fails; every median form fails. GDPR inserts that let a stand-in pass get the
   one rewrite round of §1.4.
4. **Same exclusions in both arms:** P, N and R share topic, background, position and header.

**Operating characteristics (SYNTHETIC simulation, independent topics, R hit 0.02):** probability
one run passes part I on one split. 13 topics: P/N hit 0.9/0.1 → 0.92; 0.8/0.1 → 0.85;
0.8/0.2 → 0.56; 0.7/0.2 → 0.38; 0.5/0.5 → 0.00. 16 topics: 0.93, 0.90, 0.63, 0.37, 0.00. Sol's I2
retest agreement was 0.92–0.94, so the second run mostly re-measures judge noise; the binding
uncertainty is which topics were sampled, which two runs do not address.

## 2. control2 and MEC with a topicality-matched donor ($0 only)

### 2.1 The argument

control2's own arm is the top k of the candidate's ranked pool by the retriever's score,
Σ|probe ∩ cw(s)|, and the probe words are visible in the prompt. Any donor set disjoint from the own
top k scores at most the own arm's, with equality only through ties at the rank-k boundary. So no
donor keeps own = top k and makes a stand-in on the retriever's exact score fail. The prompt-side
stand-ins use a superset of the probe words, so their dominance is measured, not proved. The
deeper reason (critic, round 1): these nulls have no labels. Matching topicality removes the
stand-in's advantage and a good judge's expected advantage alike, and without element labels no
planted positive exists for them.

### 2.2 What is measured

`nulls_t.py`, beside the originals, importing `gapmap` unchanged, $0:
- **control2-T:** control2's pairs and exclusions; the donor rebuilt only from j's ranked pool
  (minus i's own top k and both seed sources) by exact per-sentence match on seed-and-question
  overlap, ties broken by closest length; a pair with an unmatched own sentence is dropped from
  both arms. **control2-TT:** matched on probe overlap as well.
- **MEC-T, MEC-TT:** the MEC arms with donor rows rebuilt the same two ways, the own rows excluded
  from the donor pool.
- The stand-ins of §1.6 in arm-level form, plus D1b's source-count stand-in, on all five ledgers.
  For each: matched pairs, the best reachable difference (matched share), and each stand-in's own −
  control with its 95% cluster CI.

### 2.3 Rule

control2 and MEC are **declared unrepairable as judge certificates** on these ledgers, whatever
the stand-ins do, because no planted positive can be built for a real-data null without element
labels (§2.1). The measurement shows how far matching goes: it is expected to make D1b's overlap
stand-in fail and leave the probe-overlap stand-in passing (control2-T), and to leave too few pairs
to read (control2-TT). There is **no paid call on any null.**

## 3. Re-reading sol's I1c GDPR v1 reading

I1c's reading: on GDPR v1, sol closes the seed-free own arm more often than the mismatched arm,
+0.23 [+0.07, +0.39]. The overlap stand-in gives +0.46 on the same pairs. Net +10 of 44 pairs:
DISC +3, HEDGE +3, WHY +2, RESULT +2 (4 for, 2 against), SEL 0.

Three readings; the reading **survives** only if all three hold:
- **(a) RT's GDPR split:** sol passes it (parts I and II). Outcomes: passes; **does not survive**
  if sol fails with hit(N) > 0.25 or part II fails; **no reading** if sol fails on hit(P) or the
  difference alone with hit(N) ≤ 0.25, if fewer than 12 topics are kept, or if a run is incomplete.
- **(b) Sol's own citations:** sol's committed I1c cache holds the cited sentence numbers of its 19
  closed own arms and 9 closed control arms (`research/n3_control_v3/sol/gdpr_v1/`). Each cited
  sentence, mixed with an equal number of uncited sentences from the same arms (seeded), goes into
  the owner pack, blind to arm and to whether it was cited. Recomputed: own − control counting only
  closures with at least one cited sentence the owner labels as stating the element, with
  control2's bootstrap (B = 2000, seed 20261024, clusters by seed claim). Citation precision in
  each arm is reported. Judge cost $0. L7.3 for this recount (round-2 finding):
  - best reachable: recounting only drops closures, so at most 19/44 − 0 = +0.43;
  - **stand-in:** the overlap stand-in's citations go into the same pack, unmarked: for each arm the
    stand-in closes on these pairs (D1b's arm-level overlap stand-in, +0.46 here), its argmax-overlap
    sentence. Its recounted own − control must have a 95% CI lower bound **≤ 0**;
  - **planted positive:** a fake that closes an arm iff it holds a pack sentence the owner labels as
    stating the element must have a recounted lower bound **above 0**.
  If either check fails, (b) is **no reading**. Otherwise (b) holds iff sol's recounted lower bound
  is above 0.
- **(c) ADR 0009:** gemma, the other-family arm, judged on the same pairs, prompt and parser
  (control2 on GDPR v1, equal `pairs_sha256`), must agree in direction (95% CI above 0), and gemma
  counts only after its G1 (`research/n3_control_v3/l73.py`) passes in two identical runs
  (`docs/plans/prompts/_common.md:34-35`); it has one (`research/d1b_rerun/g1/google_gemma-4-31b-it-r3`).
  This session runs gemma's control2 on GDPR v1 and its G1 retest.

(a) and (b) wait for the owner's labels, so this session reports (c) and builds the packs for (a)
and (b). L7.4: what survives would be only "sol's own-versus-mismatched difference on GDPR v1 is
not explained by sol citing on-topic sentences that do not state the element"; nothing about
whether the gap map's open and closed labels are right.

## 4. Costs and caps

Prices: sol $2.00 / $10.00 per 1M tokens (in / out), gemma $0.10 / $0.34
(`gapmap/src/gapmap/judge.py`). Measured per call: sol $0.0040 on control2 prompts (I1c GDPR v1,
$0.70 / 176) and $0.0020 on G2 prompts (D1b, $0.29 / 149); gemma about $0.0002.

| Run (this session unless marked) | Prompts | Estimate | Cumulative `--max-usd` (ledger) |
|---|---|---|---|
| gemma G1 retest | 76 | $0.02 | 0.10 (OpenRouter) |
| gemma control2, GDPR v1 | 176 | $0.04 | 0.20 (OpenRouter) |
| gemma RT D1 split, runs 1 and 2 | 2 × 52 | $0.02 | 0.30 (OpenRouter) |
| sol RT D1 split, runs 1 and 2 | 2 × 52 | $0.42 | 0.80 (OpenAI) |
| later, after the owner's pack: gemma RT GDPR, 2 runs | 2 × 64 | $0.03 | 0.40 (OpenRouter) |
| later: sol RT GDPR, 2 runs | 2 × 64 | $0.52 | 1.60 (OpenAI) |

One spend ledger per provider under `research/closure_topicality/` (`openrouter_spend.jsonl`,
`openai_spend.jsonl`); each judge counts its ledger's prior spend against `--max-usd`, so the caps
are cumulative. **Sum of caps: $1.60 (OpenAI) + $0.40 (OpenRouter) = $2.00, under the $3.00 line
cap**; this session's caps sum to $1.10, expected spend about $0.50. Before each OpenRouter run,
`uv run --directory gapmap python ../scripts/key_headroom.py`; stop if it shows less than $10
remaining (read by the critic on 2026-10-27: limit $30, remaining $29.37). The OpenAI balance cannot
be read by script; the owner's last statement (2026-10-26) was $5 or more.

ADR 0009 order: every gemma run on a split precedes sol's on it. The D1 ledgers' verifier family is
OpenAI, so sol runs only beside gemma's arm on the same prompts.

## 5. Order and stop points

1. This plan; `methods-critic` until no blocking finding.
2. **Build, test first ($0):** `rt.py`, `standins_t.py`, `nulls_t.py`, `select.py`, `sim.py`,
   `pack.py`, `reread.py`; tests under `research/closure_topicality/tests/`, fake judges, no network.
3. GDPR topics selected; author subagent; code checks; blind labeller subagent; one rewrite round.
4. **All $0 checks:** RT's L7.3 on both splits; the nulls' measurement. **Stop R0:** a split on
   which a stand-in passes is not run.
5. **Paid, in order:** headroom read; gemma G1 retest; gemma control2 GDPR v1; gemma RT D1 runs 1
   and 2; sol RT D1 runs 1 and 2. **Stop R1:** a run that hits its cap stops the line.
6. Owner pack written (`fixtures/owner_pack.md`): GDPR insert-and-background lists; D1 part II
   cited-plus-decoy sentences; sol's I1c citations plus decoys. Shuffled, blind.
7. `RESULT.md` in D1's shape; `citation-verifier`; fixes.
8. All four suites and this directory's tests; commit on the branch. No push, merge or PR.

## 6. Files

`research/closure_topicality/`: `rt.py`, `standins_t.py`, `nulls_t.py` (→ `nulls_t.json`),
`select.py` (→ `fixtures/topics.json`), `sim.py` (→ `sim.json`, SYNTHETIC), `pack.py`
(→ `fixtures/owner_pack.md`, `fixtures/owner_pack_key.json`), `reread.py` (item 3 (b), runs once
the owner's labels exist), `fixtures/` (`insert_spec.md`, `inserts.json`, `labels_llm.json`,
`owner_labels.json`, empty until the owner fills it), `rt/<split>/<judge>-run<n>/` (cache, `rt.json`),
`rt/standins_<split>.json`, `g1/`, `control2_gemma/gdpr_v1/`, spend ledgers, `tests/`, `RESULT.md`.

## 7. Limits, stated now

- RT controls lexical topicality by construction and the measured stand-ins; it does not rule out a
  semantic shortcut, in particular an embedding-similarity-to-the-question stand-in, which was not
  run (no local models, owner decision 2026-10-26).
- The D1 split's inserts were seen by gemma and sol in G2 (with other backgrounds); the judges keep
  no state between calls, but D1's topics also chose gemma.
- Splits are small (13, 16). A failed part I on hit(P) alone does not separate "topicality reader"
  from "borderline element reader".
- Nothing here feeds an N3 gate or RQ-B.

## 8. Round-1 findings and where they are applied

B1 → §1.2 part II, §1.5. B2 → §1.4 checks, §1.6 item 3 (sweep, novelty, overlap fraction, reversed
and argmin forms, lens-matched lexicon). B3 → §3 (c), §4. B4 → §0 binding constraint, §1.3, §1.5,
§3. B5 → §2.2 (donors from j only, own rows excluded), §2.3 (declared unrepairable, no paid branch).
S1 → §3 (b). S2 → §3 (a). S3 → §1.1. S4 → §1.4. S5 → §2.2 (CI reported; no repair rule left to
weaken). S6 → §1.4 labeller. S7 → §1.4 (one round), §1.5 (passes every split that cleared §1.6).
S8 → §7. Minors: headroom §4; SYNTHETIC mark §1.4; insert id §1.1; clusters §1.3; background vs I1c
§1.1.
