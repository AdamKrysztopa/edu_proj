# Lessons — queue

A **queue, not an archive**. Empty is the healthy state. An entry's job is to survive the hours
between the mistake and the next drain — not to be permanent.

Write an entry **at the moment the mistake is caught**, not at the end of the session. By the end
the bug is fixed, the diff looks clean, and the only trace is a correction nobody can reconstruct
into a rule.

**Nothing is carried across two drains.** An entry that survives one drain is an entry nobody
intends to implement, and a queue with permanent residents stops being read. Either implement it,
or decline it in the archive with the reason.

Entries are drained by the `implement-ll` skill and land in `LESSONS-ARCHIVE.md`. Ids (`L<drain>.<n>`)
are assigned at drain time — don't number entries here.

## Entry format

```markdown
### <short title>

- **What happened:** the specific fact, with `path:line` or a quotation. Include *how it was
  caught* — that is frequently the real finding.
- **Generalises to:** one sentence, stated as a rule someone could follow.
- **Candidate home:** a suggestion, explicitly not a decision.
```

`Generalises to` is the filter. If the entry cannot be written as a rule someone could follow, it
is an anecdote and does not belong in the queue.

There is no status field. Presence in this queue is the status.

## What is not a lesson

- A typo.
- A one-off misreading with no general shape.
- A decision that was correctly argued and went the other way.

A queue padded with those is a queue nobody drains.

---

## Open

### A required nuisance check was impossible on the population being screened

- **What happened:** I12's phase-1 rules in commit `14cbdab` require defined, discriminating correlations against every covariate, including `k_step`. Phase-2 replay (`research/area_score/predictors/plc.json`, each predictor's `a.checks.k_step`) found no variation in `k_step` across the 24 uncapped PLC HYPs: its correlation is undefined for every possible predictor. Both replacements pass the lens/length check, but cannot pass the full screen; the independently failed noise calibration is another blocker. This was caught by replaying all required checks on the real pool, not by the balanced synthetic positive, whose nuisance covariates vary.
- **Generalises to:** Before committing a conjunctive screening rule, audit every required covariate's variation on the intended population and distinguish an undefined check from evidence that confounding is absent.
- **Candidate home:** `docs/plans/prompts/_common.md` § Gates and controls (L7.3 reachability), or a pre-registration checklist; the committed I12 rules remain unchanged.

<!-- Append entries below. After a drain this section is empty again. -->

### A judge reply missing its keys still reads as "open"

- **What happened:** In `gapmap/src/gapmap/semantic.py:177-199`, a JSON object with no `states` and no `partially` key (e.g. `{}`) becomes two empty lists and falls through to `state="open"`, which is a positive gap finding, instead of `_undecided`. The earlier fix for the same class ("judge answers given as integer ids, silently dropped as open", `PROGRESS.md` N3 defects) covered unresolved ids only. No test caught it: an independent read-only Codex audit found it by static reading on 2026-10-24.
- **Generalises to:** A parser for a judge's reply defaults to "undecided" unless every required key is present and well-typed. A fix for one malformed-answer shape comes with a test enumerating the other shapes (missing key, wrong type, empty object), not only the one that was seen.
- **Candidate home:** a regression test in `gapmap/tests/` for the missing-key and empty-object cases. **Recurs L7.8** (`docs/LESSONS-ARCHIVE.md:79`), whose bound test covers only unknown ids; ADR 0008's `undecided-never-a-finding` is verified by that same test.

### A proposed fix rule was queued without replaying it on committed data

- **What happened:** The first `docs/plans/implement-queue.md` (2026-10-24) proposed that a judge reply is undecided "unless both keys are present", and that admissibility requires cross-verify and decoys. A round-2 reviewer replayed both rules on the committed caches and ledgers. The parser rule would flip 16 valid closures that carry only `states` (5 GDPR v1, 11 GDPR v2). The admissibility rule would refuse every committed ledger, including the 107 firings the V1 study plans to code. The defect it targeted hit 0 of 641 cached answers. It was caught by an adversarial reviewer counting, not by the auditor.
- **Generalises to:** Before a fix to a parser, filter or admissibility rule is queued or specified, replay it on the committed artefacts and report how many records it flips and which downstream samples it empties.
- **Candidate home:** the `methods-critic` checklist (plan review), or the `implement-ll` routing for plan documents.

### "Args as committed" omitted the one argument that breaks byte-identity

- **What happened:** `research/spikes/jev/judge_swap.py:24` labels its `DOMAINS` table "args as
  committed for research/n3/<domain>", but `:58` passes `domain=domain` (`plc`, `gdpr_v1`,
  `gdpr_v2`), while the committed maps were built with the display names "PLC intermittent-fault
  diagnosis", "GDPR DPIA (run v1)", "GDPR DPIA (run v2)". The I1 prompt pointed at that table for
  regenerating inputs. Caught when I1's byte-identical replay of the three maps reported
  `gapmap.json`/`gapmap.md` DIFFERS; the diff was line 1 only (the title). Prompts were unaffected,
  so the spike's cache hits never revealed it.
- **Generalises to:** a "byte-identical replay" claim needs one checked-in replay command naming
  every argument, display-only ones included, and anything that claims to copy those arguments
  must call it rather than restate them.
- **Candidate home:** a `scripts/replay_n3.py` (or a test) that rebuilds `research/n3/*` and
  diffs it, referenced from `research/n3/README.md`; fix the comment at `judge_swap.py:24`.

### A planted positive proven only on a marker-reading fake judge is not proven

- **What happened:** I1's L7.3 planted positive for control2 (`gapmap/tests/test_control2.py::test_planted_positive_fires`) passes on `FakeJudge`, which closes only sentences carrying the `CLOSES_HERE` marker. Run through gpt-5.6-luna (I1b, `research/n3_control_luna/l73.py`), the same fixture with the marker removed does not fire: the donor arm is built from the donor candidate's own seed sentences first (`control2.py:123`, `(*seed_rows[j], *ranked[j])`), a donor seed is by construction a same-lens rule ("Sampling rate should be selected based on the suspected event."), and the SEL question is topic-free, so a literal judge closes the control arm as well. The same real-judge run through qwen2.5:7b-instruct fires the planted positive but also fires the random-letter stand-in on all three RNG seeds. Caught only by running the check through real judges; the fake cannot see either failure, because it ignores what the sentences say.
- **Generalises to:** A discrimination check (planted positive, stand-in) for an LLM-judged gate must also be run through the real judge on a fixture without fake-judge markers, because a fake that reads markers proves the plumbing, not that the control arm lacks the element.
- **Candidate home:** `docs/plans/prompts/_common.md` "Gates and controls (L7.3)" step 2, or a check in the control2 runner that refuses a verdict without a real-judge L7.3 file.

### A fired prompt lived on a branch its agent did not start from

- **What happened:** DS1 was fired into a worktree created at `4db3c4d`. `docs/plans/prompts/_common.md` and `DS1-gold-availability.md` exist only on the unmerged branch `plans-2026-10-24` (`e41b54f`), and `_common.md` itself says "Start from an up-to-date `main`". The prompt's own files were absent, and `cat` failed on the first step. Caught by running the first read, not by any check at fire time. The branch was then created from `plans-2026-10-24` so that the queue file the item must update exists.
- **Generalises to:** Fire a prompt only once the commit holding it, and every file it tells the agent to update, is reachable from the base the agent starts from; otherwise the prompt names its base commit.
- **Candidate home:** `docs/plans/prompts/README.md` (fire procedure), or a check in the wave launcher that `git cat-file -e <base>:<prompt path>` succeeds.

### Abstracts read whole leaked gold content under a metadata-only rule

- **What happened:** DS1's hard rule allowed abstracts but forbade reading the gold lists. Six abstracts that search agents read whole named content beyond counts: example decisions (Craig 2012), cue categories (Cioffi 2010, Harris-Thompson 2006), strategy classes (Mumaw 2000), process areas (Kancler 2005) and a category name (Canopy 2015). These are recorded as deviations in `research/ds1-gold-availability.md`. The medical pass, which screened 276 PubMed records with a script that printed only count phrases, exposed least. Caught by the agents' own deviation logs.
- **Generalises to:** Under a metadata-only rule, abstracts are screened by a script that prints only counts and location words, never the abstract text whole, because an abstract can itself enumerate gold items.
- **Candidate home:** the §14.3 anti-circularity procedure in `REORIENTATION.md`, or a shared screening helper that DS5 and later gold checks reuse.

### A gate statistic proposed without a planted-positive run over-stops

- **What happened:** `report/sections/17_validation.tex:127-129` proposes choosing the strongest baseline "inside each bootstrap resample" (min_k ΔAUROC_k). It was written as a statistics proposal and never simulated. DS3's planning simulation (40 areas per class, K = 8 baselines, δ = 0.10; `research/ds3-decisive-delta.md` §4) found that it falsely stops 55% of maps that truly beat every baseline by δ when the baselines are close together. The bootstrap of a non-differentiable minimum is inconsistent (Fang & Santos 2019). An intersection–union Continue with a Bonferroni Stop held both errors at or below 0.05. This was caught only because DS3 ran the planted positive (true gain = δ) on the rule, not by any review of the report.
- **Generalises to:** Every gate statistic or interval method in a design text, including one only "proposed", gets its L7.3 planted-positive and best-reachable-outcome run before it is written down as the recommended rule, because an intuitive resampling rule can be badly miscalibrated with nothing in the prose to show it.
- **Candidate home:** the `methods-critic` checklist (require a planted-positive operating characteristic for every proposed gate statistic), or the L7.3 rule text in `_common.md`.

### A registered continue/stop rule compared two estimates of different estimands

- **What happened:** The N5 row of `REORIENTATION.md` §22 ("Continue if the text-occasion estimate of unseen items matches the gold-as-occasion count within the pre-set tolerance") and R4's trigger (§16) compare a text estimate, which can target at most the unseen *written* items, with a gold count that targets the unseen written items plus the never-written ones. Even with perfect estimators the rule passes only if the never-written share of all unseen items is at most τ. So it stops the residual objective exactly when the residual is large. I3 step 4 (`docs/plans/prompts/I3-residual-identifiability.md`) compares with the raw gold-uncaught count, which equals g × unseen. In a seeded SYNTHETIC cell this let a jackknife that was 26% low "pass τ = 10%" through offsetting errors (`research/ds4-identifiability.md` §3.3, appendix row A′). It was caught by writing down what each side of the comparison estimates while doing the DS4 literature work, not by any check on the rule.
- **Generalises to:** Before a gate compares two quantities, write down the estimand each side targets and compute the gate's best reachable outcome under perfect estimators; if the estimands differ, the gate measures their difference, not the estimator.
- **Candidate home:** the `methods-critic` checklist for pre-registrations, beside the L7.3 discrimination steps in `docs/plans/prompts/_common.md`.

### A fired-prompt worktree was cut from a commit that lacked the prompts

- **What happened:** The DS4 agent worktree started at `4db3c4d`. The fired prompt, `docs/plans/prompts/_common.md`, the queues and `scripts/key_headroom.py` exist only on `plans-2026-10-24` (`e41b54f`, one commit past `main` at `f8139c9`). `cat docs/plans/prompts/_common.md` failed in the worktree. The item had to be rebased onto `plans-2026-10-24` before its status line could be written.
- **Generalises to:** A worktree for a fired prompt starts from the commit that contains the prompt and its queue, and the first step checks that the prompt file exists in the worktree before any branch is created.
- **Candidate home:** `docs/plans/prompts/_common.md` § Git, or the wave launcher in `docs/plans/prompts/WAVE1.md`.

### The large-t estimator forms were taken as lower bounds at two to five occasions

- **What happened:** The first build of `residual/src/residual/estimators.py` used the large-t forms. One was classic Chao1, S + f1²/(2 f2), which `REORIENTATION.md` §14.1 calls the "lower bound". The other was Lee & Chao's coverage, 1 − f1/n. Both passed their worked-example tests, which use t = 18 (cottontail) and t = 4 (hares). The first I3 simulation run then showed both overstating the unseen count under homogeneous, independent capture: at k = 2, Chao1 was +96% and Mh +333%. Under homogeneity, f1²/(2 f2) has expectation f0·t/(t−1). The (t−1)/t factor (EstimateS 9.1, iNEXT `Chat.Sam`) and the Chao–Jost coverage bring both within 8%. It was caught by the planted-truth simulation, not by the worked examples.
- **Generalises to:** Test an estimator on planted truth at the occasion counts the study will actually have, not only on published worked examples, which are usually large-sample. Before calling an estimator a "lower bound" in a plan, check that the claim holds at that sample size.
- **Candidate home:** `methods-critic`, as a check on any estimator named in a NOW pre-registration. Or the N5 row of the threshold table in `REORIENTATION.md` §22.

### A done-check names a command that cannot report drift

- **What happened:** `docs/plans/prompts/I3-residual-identifiability.md` makes "Done when" require that `uv run --directory residual python -m residual.freeze` "shows no drift". Without `--write`, that module does nothing: it prints nothing and exits 0 whatever the hashes are (`residual/src/residual/freeze.py`, the last two lines). The real check is `tests/test_freeze.py`, or comparing `fingerprint()` with `frozen()` directly, which is what I3 did. It was caught by reading the CLI after it stayed silent.
- **Generalises to:** A "done when" condition names a command that exits non-zero on failure. Before a fired prompt is written, run the command once in its failing state.
- **Candidate home:** give `residual.freeze` a `--check` mode that exits 1 on drift, and point the fire-prompt template (`docs/plans/prompts/_common.md`) at it.

### The N5 tolerance rule passes the singleton count as often as the estimators

- **What happened:** The I3 known-truth rule, |f0 − gold-uncaught| ≤ τ·gold-uncaught, was run on the trivial stand-in f0 = f1, the number of singletons. In the 18 cells where I3's stop rule applies (ρ = 0, never-written share 0), f1 passed τ = 50% at least as often as the best estimator in 16 cells (`research/n5_sim/RESULT.md`). The stop rule in the I3 prompt ("no estimator meets even τ = 50%") has no stand-in clause, so f1 alone would also have cleared it. It was caught by the L7.3 stand-in step. The entry "A spike's pre-registered 'beyond density' rule was passable by word length" covers the same failure and did not reach the plan that wrote this stop rule.
- **Generalises to:** A decision rule in a plan or fire prompt states its stand-in comparison next to its threshold, and passes only when the real statistic meets the threshold and the stand-in does not.
- **Candidate home:** `_common.md` "Gates and controls", for rules that prompts write as well as rules that items build. Merge at drain time with the word-length entry.

### A draft result counted (cell, estimator) pairs as cells

- **What happened:** The first `research/n5_sim/RESULT.md` draft said "some estimator meets τ = 50% in 10 of the 18 stop-rule cells". The 10 came from reading a printed list of (cell, estimator) hits by eye. The scripted count over distinct cells is 6. The DS4-requested rerun recomputed it, and the stream change did not explain the difference.
- **Generalises to:** Every count in a result note comes from a script that counts the stated unit, never from eyeballing a listing of a finer unit.
- **Candidate home:** the `/branch` or result-note template ("each number cites the script line that computed it"), or `citation-verifier`, extended to recompute numbers from committed artefacts.

### A web-search summary supplied a test's external anchor

- **What happened:** `residual/tests/test_estimators.py` anchors the cottontail tests to a known enclosure size of 135 rabbits (Edwards & Eberhardt 1967). The 135 came only from a web-search result summary. The page it pointed to refused the fetch, and no opened source (the abstract, SPECIES, Krebs, EstimateS) contains the number. The same pass credited Krebs eq. 2.35 to Chao (1987), but Krebs credits Chao (1988). `citation-verifier` caught both. The docstrings and `research/n5_sim/RESULT.md` now say "secondhand, unverified".
- **Generalises to:** A number used as a test anchor or a cited fact comes from a source that was actually fetched and read. A search-engine summary of a page is a lead to follow, not a source.
- **Candidate home:** the `research` skill or the `citation-verifier` brief ("flag any figure whose only provenance is a search summary"), and the TDD guidance for worked-example tests.

### A predictor check measured on the displayed map passes where the uncapped pool trips

- **What happened:** Over the 9 PLC HYPs that `gapmap.md` shows, Spearman(score, `k_topic`) is 0.79, under I6's pre-stated 0.8 threshold. Over all 24 merged HYPs before the caps it is 0.96 (`research/area_score/RESULT.md` §2–3). The caps (`gapmap/src/gapmap/rank.py:48-62`) select on the ranked score and hide mostly candidates with `k_topic` 2–3 (15 of 24), which restricts the range. `docs/plans/coverage-audit.md` finding 19 judged "ranking is a monotone function of `k_topic`" from ρ values computed within the displayed records only (≈ 0.83, against density). Caught by I6, the first check computed on an uncapped export.
- **Generalises to:** Compute a predictor-health or confound statistic on the population before any display cap or top-N truncation, never on the shown subset.
- **Candidate home:** the `gapmap` anti-renaming check (`checks.anti_renaming` takes the capped map), or the L7.3 gate-discrimination rule in `_common.md`.

### A script's tests ran on a different Python from the one that runs it

- **What happened:** `scripts/cost_ledger.py` (I11) imported `from datetime import UTC` (Python 3.11+). Its tests passed under `uv run --directory reconstruct pytest` (CPython 3.14), but the documented invocation `python3 scripts/cost_ledger.py` runs the system `python3` (3.9, Command Line Tools) and failed with `ImportError`. It was caught by running the script, not by its tests. `scripts/key_headroom.py` is invoked the same bare-`python3` way.
- **Generalises to:** A script under `scripts/` that is documented as `python3 scripts/x.py` is tested under the interpreter that command resolves to (or pins it with a `uv run --python` / shebang), because a package venv's newer Python hides version-only failures.
- **Candidate home:** a smoke test that runs each `scripts/*.py --help` with the system `python3`, or a `requires-python` shebang convention for `scripts/`.

### A model was called top-tier on the owner's word, without checking its tier

- **What happened:** The owner asked for a top-tier parallel arm and named "GPT 5.6 Luna" as much better than qwen. The coordinating session fired I1b on it and described it to the owner as the top-tier comparison. I1b then read OpenAI's own model page: `gpt-5.6-luna` "roughly corresponds to the nano model tier" ($0.20 / $1.20 per 1M tokens; `research/n3_control_luna/RESULT.md`). Caught by the subagent's price lookup, after the run, not before launch.
- **Generalises to:** Before a run is described or registered as a "top-tier" or "strongest-model" arm, the model's tier is read from the provider's own model list or pricing page and written into the prompt, and the claim is made only once that check is done.
- **Candidate home:** the parallel-arm rule in `CLAUDE.md`, or `docs/plans/prompts/_common.md` (a model-tier check before a live run).

### A judge swap was fired without checking the judge-family rule

- **What happened:** I1b swapped the closure judge to an OpenAI model. ADR 0008 (proposed) has the rule `closure-judge-other-family`: the judge's family must differ from the families that generated (anthropic) and verified (openai) the N2 ledgers. Neither the I1b prompt nor the launch checked it. The conflict was found only afterwards, while the owner's decisions were being written up. The proposed next arm, `gpt-5.6-terra`, has the same conflict.
- **Generalises to:** A prompt that changes which model plays a role (judge, verifier, generator) first lists every recorded rule naming that role or its model family, proposed ADRs included, and states how the change meets each one.
- **Candidate home:** `docs/plans/prompts/_common.md`, or a check in the `OpenAIJudge` constructor against the ledger's generator and verifier families.

### A fixable gap was reported as a blocker instead of asked about

- **What happened:** The closing summary of the 2026-10-24 decision write-up said "The `gpt-6.1-sol` run also can't start yet". The causes were two small code gaps the session could fix itself: no price for the model in `OPENAI_PRICES_PER_MTOK` (`gapmap/src/gapmap/judge.py:67`) and no reasoning-effort flag in control2. The summary neither said that plainly nor asked whether to fix them now. The owner read it as "the API key is missing" and replied: "if you have doubts aks me, not assume! NEVER". Caught by the owner, not by the session.
- **Generalises to:** When work the owner asked for cannot proceed, the reply names the exact cause and whether the session can fix it, and asks with AskUserQuestion whether to fix it now; it never reports a fixable gap as a blocker, or leaves the owner to guess the cause.
- **Candidate home:** the global `CLAUDE.md` "If you need something only I can decide, ask" section, or this project's `CLAUDE.md` definition of done.

### A scripted verifier parsed the prompt's own delimiter example as the span

- **What happened:** While writing `reconstruct/tests/test_provenance_fixes.py` (I9), a scripted verifier took the span under judgement as `text.split(">>>")[1]`. `run._verify_user` puts the instruction "marked >>>like this<<<" ahead of the context, so the fake answered with the quote "like this". `_verdict_from_result` then downgraded that answer to INSUFFICIENT, and the merge test failed on `corroboration == 0` for a reason in the fixture, not in the code. It was caught by dumping the sidecar's `verify_supporting_quote`, not by the assertion message.
- **Generalises to:** A fake that pulls a delimited region out of a prompt anchors on the last or unique delimiter (`rsplit`), or on the full expected text, because prompts often quote their own delimiters as examples.
- **Candidate home:** a shared `marked_span()` helper in `reconstruct/tests/e2e_support.py` beside `ScriptedBackend`.

### A result note called all withheld pairs statute copies from a four-item sample

- **What happened:** The first draft of `research/n2/provenance_fixes.md` said that the 242 pairs the R3 copy test withheld on GDPR v2 were "all Article 35 text quoted verbatim". It also cited "every source pair in the top ten". Both claims rested on 4 random samples and a most-common list. The `citation-verifier` recomputed all 242 pairs: they fall in only 6 source pairs, and 121 of them withhold the regulator's own prose, not statute text. The verifier caught it, not the replay.
- **Generalises to:** When a result note characterises the items a rule fired on and the population is small enough to enumerate, the characterisation is computed over every item (with a count per kind), not inferred from a sample.
- **Candidate home:** `docs/plans/prompts/_common.md` "Before changing a rule" (report what the flipped records are, by kind, not only how many), or the replay script itself.

### A guard arm was named in a decision rule after it had already failed its discrimination check

- **What happened:** ADR 0009 (`docs/architecture/decisions/0009-same-family-judge-as-parallel-arm.md`) lets a same-family judge count only where it agrees in direction with the other-family arm, local `qwen2.5:7b-instruct`. I1b had already shown qwen closing the own arm on the random-letter stand-in (`research/n3_control_luna/RESULT.md`, "Qwen closes the own arm on random letters"). After the donor fix, I1c's pre-stated L7.3 rule makes qwen ineligible again: 7 of 9 random-letter and 1 of 3 length-matched stand-ins close its own seed-free arm (`research/n3_control_v3/qwen/l73/l73.json`). So the ADR's agreement condition needs an arm that cannot count, and no reading can pass it. Caught by applying the eligibility rule to every arm before reading any domain result, not by the ADR review.
- **Generalises to:** A decision rule that makes one judge or arm the guard for another names only an arm that has already passed the real-judge L7.3 check on the same control, and the rule records which check it passed.
- **Candidate home:** ADR 0009's Consequences, or the parallel-arm rule in `docs/plans/prompts/_common.md`.

### A control fix removed a leak from one arm and left its mirror in the other

- **What happened:** I1c's first donor fix (commit `dca3b0b`) dropped both candidates' seed sources from the donor arm only. The own arm still dropped only *i*'s seed sources, so it could carry the donor *j*'s seed. The code docstring and the draft note both said "both arms are seed-free" and cited `_common.md` L7.3 rule 4 ("the same exclusions to both arms"). On the committed ledgers, own arms carried a donor seed-source sentence in 69 of 142 judged pairs. The run cost $2.545 on three judges before this was found. The `citation-verifier` caught it by reading `control2.py:124-133` against the rule-4 claim. Neither the tests nor the L7.3 fixtures caught it, because no fixture puts *j*'s seed inside *i*'s retrieval.
- **Generalises to:** When a fix removes a leak from one arm of a control, the same exclusion is applied to every arm, and a test on a fixture where the leak can reach each arm is written before any paid run.
- **Candidate home:** `docs/plans/prompts/_common.md` L7.3 rule 4 (require a per-arm exclusion test), or `gapmap/tests/test_control2.py`.

### A "same pairs" check compared pair keys, not what the arms contain

- **What happened:** The first ADR 0009 parallel-arm check in `gapmap/src/gapmap/control2.py` (commit 5e1f0cd) matched arms on (lens, seeds, donor seeds, k). In PLC, k never drops, so I1's legacy pairs and run 1's asymmetric pairs have the same keys as the fixed pairs, while 34 of 54 control arms differ. A qwen arm from the stale design would have passed as "the same pairs". The test only truncated the pair list, so it could not catch this. The `citation-verifier` caught it by checking the ADR's "same pairs" claim against the code, not the tests.
- **Generalises to:** A check that two runs saw "the same inputs" compares a hash of the content each arm was shown, and its test uses a variant with equal keys and different content (here, the legacy pool).
- **Candidate home:** `docs/plans/prompts/_common.md` L7.3 rule 4, or a test pattern in `gapmap/tests/test_control2.py`.

### Wave 2 prompts were written with checks that noise or the baseline itself passes

- **What happened:** The first revision of the wave 2 prompts (commit 68a00e8) had I12 accept any predictor that avoids |ρ| ≥ 0.8 and varies within strata, which a random score does. I5 put "strongest baseline inside each bootstrap resample" back in, although DS3 had rejected it, and used "predictor = area size" as a stand-in that scores ΔAUROC = 0 by construction. I2's agreement reading counted 0/0 as agreement. `methods-critic` caught all of these before firing; the author did not.
- **Generalises to:** A prompt that tells an agent to pre-state a rule must itself name the rule's stand-ins and pass mark, and each one must fail by a margin, not by construction. It must also be checked against the latest settled note, here DS3, before review.
- **Candidate home:** `docs/plans/prompts/_common.md` § Gates and controls (L7.3: "a prompt's own rules meet L7.3 before it is fired"); a recurrence of L7.3.

### Worktree isolation cut wave 2's agents from `main` although the launcher stayed on the plans branch

- **What happened:** I2's worktree (Agent `isolation: "worktree"`) started at `4db3c4d`, `main`'s HEAD, not at `plans-2026-10-24` (`aacc86f`). `docs/plans/prompts/WAVE2.md` step 0 says "Stay on `plans-2026-10-24`; the worktrees start from it, not from `main`", and the agent prompt says "You are in an isolated git worktree cut from plans-2026-10-24". Both are prose: the launcher's checked-out branch did not set the worktree base. Caught when `ls docs/plans/prompts/` failed in the worktree; the item branch was then created with `git switch -c i2-guard-judge plans-2026-10-24`. This recurs the wave-1 DS1 and DS4 entries above after their prose fix.
- **Generalises to:** When an agent's worktree must start from a branch other than the default, the agent's first command creates its branch from that named branch explicitly (`git switch -c <item> <base>`), because worktree isolation cuts from the default branch whatever the launcher has checked out.
- **Candidate home:** `docs/plans/prompts/_common.md` § Git (spell the command with the base), and merge with the DS1/DS4 entries at the next drain.

### A timed-out foreground wait kept running, and sixteen waiters stacked on one run

- **What happened:** I2 waited for the 32b L7.3 run (pid 29278) with a foreground `until grep … coder32_l73_r1.log; do sleep 30; done` and a 600 s timeout. Each timeout moved that shell to the background, and still running, and the agent started a new one, so 16 identical waiters were watching one log. The orchestrator caught it and killed 15. The agent never checked for an existing waiter before starting the next.
- **Generalises to:** Wait on a long run with one background waiter tied to its pid (`while kill -0 <pid>; do sleep 30; done`). Before starting any further wait, check that no waiter is already running, because a foreground command that times out keeps running in the background.
- **Candidate home:** `docs/plans/prompts/_common.md` (a "Long runs" line beside § Paid calls), or the wave launcher's agent prompt.

### A cache-hit count was explained by guessing its source, and the guess was wrong

- **What happened:** I2's Jev domain runs reported `cache_hits: 2` in GDPR v1 and GDPR v2. `GUARD.md` first explained them as "4 prompts repeated across domains, answered from this run's own cache", inferred from 532 prompts against 528 raw files. `citation-verifier` rebuilt the prompts and found that no prompt recurs across domains. The 4 were prompts the old control had issued, answered from the spike cache: the cache rule working as designed, and the opposite of the note's claim. `JevJudge.spend()` counts hits without saying which cache served them.
- **Generalises to:** A runner that reads several caches records which cache answered each hit, and a note explains a hit count only from that record, never from arithmetic on file counts.
- **Candidate home:** `gapmap/src/gapmap/jev.py` (`cache_hits` per directory) and the same for `CachedJudge`; or `_common.md` § Judges.
### A fired agent's worktree was cut from `main`, not from the wave branch

- **What happened:** I5 was launched in an isolated worktree whose HEAD was `main` (`4db3c4d`), while `_common.md` § Git says to start from `plans-2026-10-24`. `git switch -c i5-gate-simulation` branched from `main`, and the item's own context files (`docs/plans/prompts/_common.md`, `docs/plans/implement-queue.md`) were missing. It was caught only because `cat` of the prompt file failed. Fixed with `git reset --hard plans-2026-10-24` on the new, still empty branch.
- **Generalises to:** A fired prompt names its base branch as a commit check (`git merge-base --is-ancestor <wave-branch> HEAD` must hold before any work), not as prose the agent is trusted to follow, because a worktree launcher picks its own base.
- **Candidate home:** `docs/plans/prompts/_common.md` § Git, or the wave launcher (`WAVE2.md`) that creates the worktrees.

### A clustered variance silently dropped a component when one class sat in one cluster

- **What happened:** `residual/src/residual/auroc.py` `auroc_covariance` (I5) set the negative-side factor I0/((I0-1)N0) to 0 when every negative sat in one cluster (I0 = 1), so a 16/4 gold whose four negatives shared a cluster got too small a standard error and an anticonservative gate. The first 1000-replicate grid ran with it. The tests passed: they covered the singleton reduction to DeLong and duplicated clusters, not a class confined to one cluster. It was caught by asking why false Stop at a gain of δ ran above nominal in small designs.
- **Generalises to:** A variance estimator that divides by (count − 1) of some grouping states what it returns when that count is below 2, and has a test for that case, because the silent 0 makes every downstream bound too narrow.
- **Candidate home:** `residual/tests/test_auroc.py` pattern, or `_common.md` § Gates and controls (an estimator's degenerate cases are part of L7.3's "can discriminate").

### A proposed threshold was paired with a design that does not meet it

- **What happened:** The first draft of `research/gate_sim/RESULT.md` (I5) proposed "a pooled minority class of 30, which in practice means 5 golds of 20 areas, or 3 of 30, at 16/4". But pooled minority is k × min(n1, n0) (`simulate.py` `make_cell`), so those designs give 20 and 18, and under the note's own "below 30 is inconclusive by design" the recommended design could never read. The floor came from the r = 0.6 slice and the designs from the P(Continue) ≥ 0.8 column, and they were merged from memory. `methods-critic` and `citation-verifier` both caught it; the author did not.
- **Generalises to:** When a note proposes both a threshold and a design that should meet it, the design's value of the threshold quantity is computed by the same code that defined the quantity and printed next to it, never asserted in prose.
- **Candidate home:** `docs/plans/prompts/_common.md` § Finish (every number in a recommendation is read from a committed file), or the `analyse.py` pattern of generating recommendation rows.
### A fired item's worktree was cut from main, not from the wave's base branch

- **What happened:** The DS2 launcher said "you are in an isolated git worktree cut from plans-2026-10-24", but the worktree's HEAD was `main` (`4db3c4d`). `docs/plans/prompts/` did not exist there, and neither did the DS1, DS3 or DS4 notes. A plain `git switch -c ds2-closure-codebook`, which `_common.md` § Git prescribes, would have based the item on `main` without wave 2's prompts and settled notes. It was caught only because `ls docs/plans/prompts` failed. The fix was `git switch -c ds2-closure-codebook plans-2026-10-24`.
- **Generalises to:** A fired item names its base explicitly (`git switch -c <branch> <base>`) and checks that the base holds its own prompt file before doing any work, rather than trusting the worktree's starting HEAD.
- **Candidate home:** `docs/plans/prompts/_common.md` § Git, or the wave launcher's worktree creation.

### A phrase lifted from a source was paraphrased as the opposite finding

- **What happened:** The DS2 draft (`research/ds2-closure-codebook.md` §5, item 3) said that pre-annotation moves human labels towards the tool's, "whether it be good or bad" (Fort & Sagot 2010). The phrase came from a keyword hit. In context (§4.2), it says the *weaker* annotator's accuracy *improved* under both good and bad pre-annotation. The bias finding is a different one: the strongest annotator fell from 98.1% to 95.8% with the weak tagger, through lapses of concentration. It was caught by rereading the paragraph before handing the note to `citation-verifier`, not by the keyword search that found it.
- **Generalises to:** A quoted phrase enters a note only after its whole paragraph has been read, because a keyword-window hit gives the words without the subject or direction they qualify.
- **Candidate home:** the `research` skill's method step, or the `citation-verifier` brief ("check that a quotation's sense survives its paragraph").
### The gold's publication date was taken as the date experts revealed the list

- **What happened:** `REORIENTATION.md` §18.2 says that freezing the corpus at the gold's own publication date "directly measures 'was this written before experts revealed it?'". `report/sections/17_validation.tex:107-110` builds the dated corpus on the same rule.
  - **First measurement.** DS5 queried OpenAlex metadata (`research/ds5-pregold-fulltext/blocking.json`). In 5 of 17 provisional golds, a same-team task analysis of the same procedure predates the gold:
    - Sullivan 2014 ← Campbell 2011 and Yates 2011;
    - Okoli 2020 ← Okoli 2015 and 2016;
    - Russ-Jara 2023 ← Russ 2017 and 2021;
    - Seamster 1993 ← Redding 1991 and 1992;
    - Phillips 2001 ← Phillips 1998.

    The date rule admits each of them.
  - **Second measurement.** In 3 of 17, a work that cites the gold is dated on or before the cut-off, which is metadata error.
  - **How it was caught:** by running the blocklist queries, not by reasoning. The rule had been written and reviewed as self-evident.
- **Generalises to:** A cut-off meant to mark when information became public is set at the earliest disclosure by the same source, found by searching for precursors, not at the canonical paper's date. Citation exclusion is applied whatever the date, because publication dates in metadata are wrong often enough to leak.
- **Candidate home:** I10's `admit()` rules and its fixtures (a precursor fixture and a mis-dated citing-work fixture), with a one-line correction to §18.2.
### A registered floor took a literature headline, not the source's matching table

- **What happened:** The E-PLANT validity floor (`docs/n2-eplant-eabst-protocol.md` §6: a_u ≥ ⌈n/3⌉, "about half the > 60% expectation, evidence [51]") came from ClashEval's discussion headline: GPT-4o overrides a correct prior over 60% of the time (Table 2: 60.8%).
  - In the same one-document, prior-correct setting, Table 2 gives 31.3% and 40.1% for the Claude models. A ⌈n/3⌉ ≈ 33% floor therefore sat at the Claude single-document rate.
  - Its §4.2 says extra documents lower that rate (Opus: 28.7% at k = 1, 23.7% at k = 5).
  - E-PLANT ran Haiku with 18 documents and at least 2 true pages per target. The observed rate was 5/24 = 20.8%, and the floor closed Continue before any gated arm ran.
  - **How it was caught:** only when DS6 read the source's full text. Neither the methods-critic review of the protocol nor the citation check had compared the number with the per-model rows.
  - **Recurrence inside DS6.** DS6's own first draft then cited the paper's appendix Table 4, which reports half of each Table 2 value without explanation, as "the matching table", and drew too strong a conclusion from it. The `citation-verifier` caught that.
- **Generalises to:** A threshold taken from a literature figure cites the source's row that matches our model, setting and conditioning (or says that none matches). The citation check reads that row, and every other table reporting the same quantity, not the abstract or discussion.
- **Candidate home:** `docs/plans/prompts/_common.md` § Gates and controls (L7.3 step 1, best reachable outcome), or the `citation-verifier` agent's instructions for threshold-bearing citations.
### The wrong-base worktree recurred a third time while its lesson sat in the queue

- **What happened:** The DS7 agent worktree started at `4db3c4d` (`main`), not `plans-2026-10-24` (`aacc86f`). `cat docs/plans/prompts/_common.md` failed on the first read, exactly as for DS1 and DS4, whose entries are already in this queue ("A fired-prompt worktree was cut from a commit that lacked the prompts"). The branch was then created with `git switch -c ds7-boundary-sources plans-2026-10-24`. Caught by the first read failing, the third time in one wave; the queued rule had not reached the launcher.
- **Generalises to:** When a queued lesson about how items are fired recurs within the same wave, the launcher is fixed before the next item fires, instead of waiting for the checkpoint drain.
- **Candidate home:** `implement-ll`'s trigger list (a recurrence inside a wave is a checkpoint), or `docs/plans/prompts/WAVE2.md`'s launch step (assert the prompt file exists in the worktree before firing).
### A wave-2 worktree said "cut from plans-2026-10-24" but sat on main

- **What happened:** The DS8 launcher prompt (`docs/plans/prompts/WAVE2.md:20`) told the agent its isolated worktree was "cut from plans-2026-10-24", but the worktree's HEAD was `main` at `4db3c4d`, which has no `docs/plans/prompts/`. Caught only because `cat docs/plans/prompts/_common.md` failed; fixed by checking out `plans-2026-10-24` (`aacc86f`) detached before `git switch -c ds8-oss-departures`. An item whose files also exist on `main` would have branched from the wrong base silently.
- **Generalises to:** A fired prompt that names a base branch verifies it first (`git merge-base --is-ancestor <base> HEAD`, or compare `git rev-parse HEAD` with the base) and stops on a mismatch, instead of trusting the launcher's description of the worktree.
- **Candidate home:** a first step in `docs/plans/prompts/_common.md` § Git, or a check in the wave launcher before agents are spawned.

### A dataset's row count was reported in the wrong unit, and a table cell was retyped from the wrong grid cell

- **What happened:** The DS8 note (`research/ds8-oss-departures.md`, first draft) called the 315 rows of Avelino 2019's `tfprojects_commits_new.csv` "315 departures"; they are 315 projects with one dated TFDD each, while `measures.csv` holds 388 TFDD events in 344 repositories. In the same note, two power-table cells ("P ≤ 0.31", "P ≤ 0.02") were retyped from a printout of neighbouring cells (floor 20; ≥ 20 departures) rather than read from `power.json`. Both were caught by `citation-verifier` recomputing the aggregates and the cells, not by the author.
- **Generalises to:** A count quoted from a dataset names the unit of the file's rows (project, event, person) and is cross-checked against any other file that counts the same thing; a number in a note's table is generated from the committed output by script, like `report.json` rows, never retyped.
- **Candidate home:** `docs/plans/prompts/_common.md` § Finish (extend the "read from a committed file" rule from `report.json` to note tables), and the `citation-verifier` checklist (unit of count).
### A value hash imported its source and read a stale bytecode cache

- **What happened:** I7's `gapmap/src/gapmap/manifest.py` first hashed `config._canonical()` by loading `config.py` with `importlib.util.spec_from_file_location`. A one-value edit (`TERMHOOD_MIN_CLAIMS = 2` → `3`) kept the file's size and mtime second, so the loader used the stale `__pycache__` entry and the changed value was **accepted**. The manifest's own mutation audit (the L7.3 planted positive) caught it under pytest; the same audit run standalone passed, so one clean run would have hidden it. Fixed by compiling the source bytes into a fresh module.
- **Generalises to:** Code that hashes or fingerprints what a source file *computes* must compile the file's current bytes, never import it, because Python's bytecode cache validates on size and whole-second mtime and a same-length edit inside one second is silently served stale.
- **Candidate home:** `residual/src/residual/freeze.py` and any future fingerprint helper; `docs/plans/prompts/_common.md` § Gates and controls (a mutation probe that keeps size constant).

### Passing `--help` to a prompt-taking subcommand ran a real model task

- **What happened:** To read the Codex companion's flags, the wave 2 launcher ran `codex-companion.mjs task --help`. `task` treats its free-text arguments as the prompt, so it started a real Codex thread with "--help" as the task (it answered "Tell me what you'd like to do…"), which also counted against the Codex usage limit that later cut I12 phase 2 short. Caught only by reading that command's backgrounded output; the flags were then read from the script source (`grep` on its option parser).
- **Generalises to:** Learn a wrapper's flags from its source or a documented help command, never by passing `--help` to a subcommand whose positional arguments are a prompt or a payload.
- **Candidate home:** the `codex:codex-cli-runtime` usage notes, or the wave launcher's preflight.

### A sandboxed agent in a linked worktree could not commit

- **What happened:** I12 was handed to Codex with `--write` in a linked worktree (`.claude/worktrees/i12-codex`). Its `git switch -c i12-predictor` failed with "Unable to create '…/edu_proj/.git/refs/heads/i12-predictor.lock': Operation not permitted": a linked worktree keeps its refs, index and objects in the main repo's `.git`, outside the sandbox's writable roots. The run produced only a blocker note. Caught by the run's own report. Fixed by having the orchestrator create the branch and commit between phases (rules commit `14cbdab`, then `b518774`).
- **Generalises to:** Before giving a sandboxed agent work that must branch or commit, either put the repository's `.git` inside its writable roots (a standalone clone) or plan for the orchestrator to commit at each pre-registered boundary.
- **Candidate home:** the wave launcher template (`docs/plans/prompts/WAVE*.md`) or `_common.md`.

### The `--help` lesson recurred one day after capture: queue text did not stop it

- **What happened:** Building the wave 3 report on 2026-10-25, the orchestrator again ran `codex-companion.mjs task --help` to read its flags, and a real Codex thread answered with `codex --help` output. This is the same mistake as the queued entry "Passing `--help` to a prompt-taking subcommand ran a real model task" (commit `4bdb488`), which was in `docs/lessons.md` § Open but not yet drained to any mechanism. Caught by reading the command's output.
- **Generalises to:** A lesson about a command an agent runs by reflex needs a mechanical guard (a PreToolUse hook that denies `codex-companion.mjs task --help`), because a queued entry is not read before the command runs.
- **Candidate home:** a PreToolUse Bash hook under `.claude/hooks/`, paired with the earlier entry at drain time.

### A synthesis restated wave-report headlines and got four registered facts wrong

- **What happened:** The SYNTH waves 1–4 page (2026-10-25) said MS1 and the first N3 reading wait on "an eligible second judge". The registered `research/v1_closure/PREREG.md` §6 and §9 (branch `i4-v1-kit`) make Jev eligible and adoptable on its own: only sol needs an agreeing guard, and MS1 needs only a registered guard-screening result. The same draft called DS9's "14 reviewed sources" "14 learner datasets", listed the two-week cap split as an open owner decision although PREREG §14 (D2) already registers it, and called provisional golds "not confirmed itemised" when DS1's open criterion is that the list can be obtained. A Codex review against the source files caught all four before the page was final; my own pass over the wave reports did not.
- **Generalises to:** A summary of a gate, a count or an owner decision is checked against the file that registers it (the pre-registration, the result note, the queue line), never only against a report that already summarises it, because each summary layer drops the qualifier that changes the meaning.
- **Candidate home:** `docs/plans/prompts/_common.md` § Wave report and the SYNTH prompt's Method (a source-file check per stated gate and count), or citation-verifier's checklist.

### Codex translated "conservation content" as nature conservation in the Polish report

- **What happened:** Translating the D1 implementation plan for the Polish synthesis (2026-10-25), gpt-5.6-sol rendered "reconstructed conservation content" (physics conservation laws, Track A §18.1) as "treściami dotyczącymi ochrony przyrody". The prompt's terminology list fixed "gate", "gap map" and others but not this term. I caught it reading the output before inserting it, not through any check. In the same pass the docs connector silently dropped the in-page link `[Plan wdrożenia](#plan-wdrożenia)` (non-ASCII slug); only the ack, which showed no `<link>`, revealed it.
- **Generalises to:** A translation prompt lists every domain term that also has an everyday meaning, with its fixed rendering, and the translated text is read against that list before it is published; after any insert with in-page links, the ack is checked for `<link>` elements.
- **Candidate home:** the Polish-translation step of the SYNTH prompt (a terminology table that includes ambiguous domain terms), and the docs-editing notes for in-page links.

### A budget stop was tested at one stage only, and a later stage lost the whole run

- **What happened:** `test_budget_exceeded_mid_run_still_writes_an_incomplete_run_dir` stops the budget after 3 calls, before any claim exists. On the D1 26-doc corpus (2026-10-25) the cheap arm hit its cap inside cross-verification; `ledger_areas` was set only after that stage (`reconstruct/src/reconstruct/run.py`, slot stage), so the Ledger refused assignments naming absent areas and the run died with no ledger.json, losing $1.50 of calls. Found by running live, not by a test. The 16-doc corpus never reached cross-verification (one independence key), so earlier live runs could not show it.
- **Generalises to:** A "a stop still writes a valid output" guarantee is tested with the stop placed in every stage that follows a state change, not only in the first stage, because each stage leaves a different partial state for the final assembly to accept.
- **Candidate home:** `reconstruct/tests/test_e2e_resilience.py` (a parametrised stop per stage), and the MUST 5 note in run.py's except clause.

### Multiple-choice elicitation, with "Skip" marked Recommended, collected stances and no knowledge

- **What happened:** In D1 step 5 (2026-10-25) the owner asked for the 15 questions as options. I put them through AskUserQuestion with stance options ("Serious risk, never OK", "Done it; as expected") and, to meet the always-recommend rule, marked "Type my answer" and later "Skip, no detail" as Recommended. The notes box did not carry text back, and the owner followed the recommendation: after 10 questions there was no sentence of content, so every answer would be judged "no content" and the rule would read Change for a reason unrelated to the gap map. I noticed it from the empty answers, not from any check.
- **Generalises to:** When the measured quantity is what a person knows beyond the written material, the collection form must require their own words (free text or speech), the options may only route, and the recommended option is the one that yields their words, never one that skips content.
- **Candidate home:** `docs/plans/prompts/D1-demonstrator.md` step 5 and the POC protocol in `research/wut_pilot/`; a content floor in `rule.py` that returns "no reading" when too few answers carry content.

### The Polish synthesis read as a stiff translation, and I wrote Polish fixes myself

- **What happened:** The owner asked (2026-10-25) for the Polish version to be translated by gpt-5.6-sol because it writes better Polish. The doc used "fala" for "wave" where the owner expects "etap", and several later fixes (mistranslations, widget labels, the conservation term) were written in Polish by me rather than sent back through gpt-5.6-sol. The owner judged the result "terrible"; no check of mine looked at Polish fluency or at the owner's own terms.
- **Generalises to:** When the owner names a model for a language, every sentence in that language goes through that model, including fixes, and the term list is asked of the owner or taken from their own writing before the first pass, with a native-editor review pass by the same model before publishing.
- **Candidate home:** the SYNTH prompt's Polish step and `docs/plans/prompts/_common.md` (a translation rule: named model for every edit, owner's glossary, a review pass).

### Translating sentence by sentence produced translated Polish, whatever the model

- **What happened:** The outside report's Polish version (2026-10-25) was made by gpt-5.6-sol from English units, with a native-editor review pass; the owner still called it "terrible Polish". It kept English sentence shapes ("Doświadczeni ludzie wiedzą znacznie więcej, niż kiedykolwiek zapisują"). A from-scratch Polish rewrite from a brief, five critique rounds by four OpenAI models plus Fable, and above all one sentence written by the owner as a voice model, fixed it; the critics alone plateaued at 8/10.
- **Generalises to:** A text for native readers in another language is written in that language from a brief, not translated unit by unit, and the owner's own example sentence is asked for before the first draft, since model critics converge on fluency but not on the owner's voice.
- **Candidate home:** the translation rule proposed in the previous entry (`docs/plans/prompts/_common.md`).

### The key-headroom check passed while the account had no credit

- **What happened:** On 2026-10-26 `scripts/key_headroom.py --need 0.01` printed `limit=15 remaining=14.99998 reset=weekly`, while the OpenRouter account credit was exhausted ($80 of $80; D1's judge calls got HTTP 402 on 2026-10-25, `research/d1_demonstrator/judgements_openrouter_402.json`). The script reads the key's weekly `limit_remaining`, not the account balance, so L7.1's guard would let a paid run start that fails at its first call. Caught by reading the script's output against the 402 record while planning the gap-map fix and D1 rerun budget, not by any check.
- **Generalises to:** A pre-run spending check reads every limit that can refuse the call (the account balance as well as the per-key cap) and passes only on the smallest, because a cap is not money.
- **Candidate home:** `scripts/key_headroom.py` (also read the account credits endpoint) and L7.1's wording; `.claude/hooks/guard-key-headroom.sh`.

### control2's own-versus-donor contrast is topicality, and a word counter beats the judge it certified

- **What happened:** control2 ranks the own arm by candidate i's probe and the donor arm by j's probe (`gapmap/src/gapmap/control2.py:120,128-132`), so the own arm is more on-topic by construction. A lexical-overlap stand-in (close an arm iff its overlap with the question and seed reaches the median) gives +0.78 [0.67, 0.87] and +0.78 [0.65, 0.89] on the D1 ledgers, and +0.68 (PLC) and +0.46 (GDPR v1) on N3, against sol's +0.13 and +0.23. Only 6 and 1 D1 pairs are overlap-matched within 25%. I1c guarded against length and random letters, never against topical overlap; my draft plan then cited sol's GDPR v1 pass as prior evidence. Caught by `methods-critic` on the plan (2026-10-26), reproduced offline.
- **Generalises to:** A control whose arms are retrieved by different queries must include a stand-in that scores each arm's topical overlap with the judged question, and a judge passes only by beating it on overlap-matched arms, because "on topic" is the cheapest way to look like "states the element".
- **Candidate home:** `control2.verdict` (an overlap stand-in row) and L7.3's list of trivial stand-ins; the I1c MS1-candidate reading in `docs/plans/implement-queue.md` § I1 needs re-reading.

### Local-model screening crashed the owner's Mac although the RAM limit was already on record

- **What happened:** The D1b plan (§2.1, 2026-10-26) chose local Ollama models (gemma3:12b, mistral-nemo:12b, llama3.1:8b, about 25 GB of downloads) as the cheap judge arm, although `docs/plans/implement-queue.md` § I1c already recorded that coder32 was "not runnable on this laptop (24 GB RAM, 76 s per trivial reply, first L7.3 run hung about 4 h)". The gemma3 screening run, started while the other downloads filled the disk (31 GB free), took the machine down; the owner stopped local models and asked for hosted cheap judges instead. Caught by the owner, not by any check; two methods-critic rounds reviewed the plan without raising it.
- **Generalises to:** A plan that runs local models states the machine's free RAM and disk against each model's size and runs one model at a time, and a recorded hardware failure on this machine counts as evidence against any local run, not only against that model.
- **Candidate home:** `methods-critic` checklist (compute budget beside money budget); L7.2's plan record.

### Provider errors and truncated replies were scored as a judge failing its check

- **What happened:** In D1b's C1 screening (2026-10-26), mistral-small-2603 was rate-limited upstream (HTTP 429) on every G2 call: 0 billed calls, 30 "undecided" states, printed as "fails". deepseek-v4.1-flash and qwen3.8-flash reason by default (mean 661 and 973 reasoning tokens) and hit `OpenRouterJudge`'s 2,000-token cap on 12 and 14 calls (`finish_reason: length`), so 9 G2 replies each were unparseable, became "undecided" and counted as not closing. `semantic.judge_retrieval` degrades any judge exception to "undecided" by design, and `g2.evaluate` gave a pass/fail verdict over undecided arms. Caught by reading per-arm states after the arm-0 rates looked wrong, not by any check.
- **Generalises to:** A screening or gate verdict over judge replies is "incomplete", never pass or fail, while any reply is an error, truncated or unparseable; a hosted judge retries transient errors and records every finish reason, and its token cap is set from a measured reply of that model.
- **Candidate home:** `gapmap.judge.OpenRouterJudge` (retry, truncation flag); `research/d1b_rerun/g2.py` verdict; the same rule for `l73.py` when it is next re-frozen.

### A confirmed "the seed does not state the element" was wrong for four of six selection seeds

- **What happened:** G2's fixture writer and the owner both confirmed that every seed leaves its lens question open (`research/d1b_rerun/fixtures/confirmations.json`). In C1 (2026-10-26), every hosted judge, and qwen 7b, closed the no-insert arm of t06, t12, t03 and t19 by citing the seed itself. t03's seed carries its own reason and result ("…because lags outside it carry no detectable predictive signal"), and t12's and t19's carry a "when deciding…" condition. With those seeds in a 4- to 6-topic split, arm 0 ≤ 0.25 was out of reach for any judge that reads them that way, so the selection split could not select. Caught from the per-arm citations after every candidate failed, not by a check before the run.
- **Generalises to:** Before a known-truth fixture is used as ground truth, its "absent" labels are checked by several independent readers (the no-insert arm through more than one model, or a second human), a label they dispute is treated as ambiguous and dropped, and the reachability of every limit is recomputed after the drops.
- **Candidate home:** L7.3's best-case clause (recompute after fixture drops); the G2 spec in the D1b plan.

### G2's random-letter limit was stricter than the no-insert limit it contains, so it counted a seed closure twice

- **What happened:** The G2 rule (plan §2.2, `research/d1b_rerun/g2.py:passes`) required close(R) ≤ 0.10 and close(0) ≤ 0.25. But every R arm is the no-insert arm plus one random-letter sentence, so any judge that closes a seed also closes that topic's R arm. gemma-4-31b-it on the gate split (2026-10-26, two identical runs) closed exactly t07 and t21 under both 0 and R and no other R arm: P − N +0.92, lower bound +0.75, N 0.08, N+ 0.08, arm 0 0.15, R 0.15, so it failed on R alone. The offline tests passed because the oracle fake never closes a seed. Caught by comparing per-topic states after the run.
- **Generalises to:** When a check's arms nest (one arm is another plus an insert), each limit is stated on what the insert adds (closures where the containing arm was open), or the limits are made consistent; and the L7.3 fixtures include a judge that closes the shared base, so a double count shows up before any real run.
- **Candidate home:** L7.3's stand-in clause (a "base-closing" fake); G2's rule if it is amended.

### Paid runs started in parallel with the free gate that should have stopped them

- **What happened:** To save wall time, I started sol's paid OpenAI R1 runs (G1, then the G2 gate) while C3 was still running, before the $0 Stop A matched-pool count. `docs/plans/gapmap-fix-and-d1-rerun.md` §3.2 and §5 say "Feasibility before any OpenAI spend … stop here, with no OpenAI spend". Stop A then failed (gemma: 7 all-open topics, 3 matched pairs, floor 10), so $0.29 of OpenAI spend went to runs the plan said must not start. It was caught only when `build_sheet.py count` returned `stop_at_A: true`. The ordering lived in prose; no code refuses a paid run while the free gate before it is pending.
- **Generalises to:** A paid run that a plan places after a free feasibility gate starts only once that gate's recorded output says to continue; running stages in parallel for speed must never reorder a gate ahead of the spend it guards.
- **Candidate home:** a check in the paid-run wrappers (g1.py, g2.py, the gapmap CLI under `--judge openai`) that refuses when the plan's preceding gate record is missing or says stop; or the guard-key-headroom hook.

### `codex exec` launched from a script waited silently on stdin

- **What happened:** The Polish brief for the D1b artifact updates went to `codex exec -m gpt-5.6-sol -s read-only -o out.json "<prompt>"` from a backgrounded Bash call. Twice it ran for 10+ minutes and produced no output. `codex.log` read only "Reading additional input from stdin...": with stdin open, codex-cli 0.154 waits for more input after the prompt argument. It was caught by reading the log on a status check, not by any timeout or error. The fix was `< /dev/null`.
- **Generalises to:** Any non-interactive CLI call from an agent closes stdin (`< /dev/null`), and a long-running background call is checked by its log early, not only when it exits.
- **Candidate home:** the codex-companion skill or a wrapper script for `codex exec`; a PreToolUse hint on `codex exec` without a stdin redirect.

### Artifact updates declared done after patching sentences, not the diagrams or conclusions

- **What happened:** After D1b, I updated the four Claude Docs pages by find-and-replace on the sentences I found with a text search for "D1" and "rerun", then reported "all artifacts updated" twice. The text search does not reach diagram widgets or table cells phrased differently. In the synthesis (EN and PL), the "Implementation plan" timeline still showed "Fix the gap map's ranking: Nov 2026" and "Rerun D1: Nov–Dec 2026" as future work, and the status diagrams and plan table were stale. No section drew conclusions from the two studies. The owner caught both from a screenshot.
- **Generalises to:** An artifact is updated after a result only when every embedded widget, table and status chip has been read against the new state (outline, then each embed's code), and when the page states what the result concludes and changes in the plan, not only that the result exists.
- **Candidate home:** the docs-update step of the result workflow (a checklist that lists every embed and table on each artifact page); `docs/artifacts.md` could record which widgets carry plan dates.

### A sealed artefact sat on disk in clear text between write and encrypt

- **What happened:** D1b's `seal()` (`research/d1b_rerun/build_sheet.py`) writes the sealed key and sheet into a `secret/` directory, then tars, encrypts and deletes it, so the content exists unencrypted on disk for a while (and in any backup or snapshot taken meanwhile). D1b's tests checked that the ciphertext decrypts, not that no plaintext was ever written. Caught by the N8 E-SEAL agent when it reused the scheme; N8's version pipes plaintext to openssl on stdin and a canary test scans every written file.
- **Generalises to:** Sealed or blind material is encrypted from memory and never written in clear, and its test plants a canary in the content and asserts it appears in no file, log or output stream.
- **Candidate home:** a shared `seal` helper used by D1b and N8, with the canary test; fix D1b's `seal()` before it is reused for D1c.

### A coverage measure was compared with baselines of unequal length

- **What happened:** N8's first scoring design (`docs/plans/n8-e-seal.md`, branch `n8-e-seal`) compared each arm's coverage of the reference operation list against baselines up to three times longer, which biases the reading toward the longer list. `methods-critic` caught it before anything ran.
- **Generalises to:** A coverage or recall measure compared across arms or against a baseline uses size-matched lists (or a length-adjusted score), because coverage rises with list length alone.
- **Candidate home:** the `methods-critic` checklist, next to L7.3's trivial stand-ins (list length as a stand-in).

### Provider-side logging is a display path that code cannot see

- **What happened:** While designing N8's preconditions, the agent found that OpenRouter's account-level prompt and response logging would keep sealed model output readable in the provider's activity view, and no client-side check can confirm it is off. N8 now refuses to run without an explicit `--provider-logging-off` attestation and records it.
- **Generalises to:** Any sealed or blind paid run requires provider-side logging to be confirmed off by the account owner and the confirmation recorded in the run's manifest, because the client cannot verify it.
- **Candidate home:** the sealing rules in `CLAUDE.md` beside L7.1; the `/preflight` checklist.
