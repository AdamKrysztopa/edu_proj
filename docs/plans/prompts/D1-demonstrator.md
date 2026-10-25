# D1: End-to-end demonstrator on dependence-forecastability

**Branch:** `d1-demonstrator`, from `plans-2026-10-24`.
**Outputs:** `research/d1_demonstrator/` (corpus manifest, runs, gap map, question sheet, answers, novelty check, onboarding notes, `RESULT.md`, `report.json`).
**Cost:** all paid calls together capped at `--max-usd` totals of **$11** (owner, 2026-10-25; first $8, raised when outside sources were added), split across the arms below. Run `python3 scripts/key_headroom.py` before each live command.
**Purpose (owner, 2026-10-25):** show how the tool is meant to be used: demonstrator, then a POC at Warsaw University of Technology, then funding and partners. In step 4 the pre-registration document, `methods-critic` and hash commit are dropped. The rule is still written down, and its synthetic checks still run, before the owner answers.
**Label:** exploratory demonstrator. It is not N3, feeds no N3 gate or threshold, and its result is never cited as evidence for RQ-B.

## Why
The owner wants the five-step tool shown end to end on a real example, by the owner and Claude alone, with no hired people (owner, 2026-10-25). N3 stays paused with its registered rules unchanged until independent coders exist.

The tool's steps:
1. Read what is written.
2. Find where it is thin (the gap map).
3. Ask the expert only those questions.
4. Turn the answers into learning material.
5. See where newcomers still struggle.

The domain is the owner's own public project, https://github.com/AdamKrysztopa/dependence-forecastability (MIT; a Python toolkit for horizon-wise forecastability analysis with AMI/pAMI, rolling-origin benchmarking and reporting). The owner wrote its docs and is its expert, so "missing from the docs" means "the owner knows it but never wrote it down". That is the residual the tool hunts.

## Context
- `docs/plans/implement-queue.md` § D1 and the synthesis doc https://claude.ai/artifact/XwWjHGbKjDuBgyKX4BEME9 ("What we are building, and why").
- `reconstruct/src/reconstruct/corpus.py` (local-corpus mode, manifest shape), `reconstruct/models.json`, `gapmap/` (lenses, ranked map, CDM-style questions).
- `docs/plans/prompts/_common.md` applies, except where this file says otherwise.

## Steps

1. **Corpus (step 1 input, $0).**
   - Shallow-clone the repo at a pinned commit into `research/d1_demonstrator/source/` (git-ignored) and record the commit SHA.
   - Build a `corpus/manifest.json` in `reconstruct.corpus` shape from the public text only: `README.md`, `docs/**`, `examples/**` (markdown and docstrings), `llms.txt`, `CHANGELOG.md`, and module docstrings under `src/`. Each document gets its GitHub URL at the pinned commit.
   - Exclude `.env*`, `.claude/`, `AGENTS.md`, `CLAUDE.md` and anything not in the public repo.
   - Add outside pages on the same methods (owner, 2026-10-25): one repository is one independence key, and the gap map needs at least two sources on a topic to call an open gap a hypothesis.
   - Record the file list and byte counts in `corpus/inventory.json`.

2. **Reconstruction (step 1).**
   - Choose the task with the owner in one line, for example "How does a new contributor run, extend and interpret a horizon-wise forecastability analysis in this toolkit?"
   - Run `python -m reconstruct.run --live --corpus <manifest> --domain "forecastability toolkit" --task "<task>"` on the cheap models (`models.json`).
   - **Top-tier parallel arm** (CLAUDE.md): add a `--models <path>` option to `reconstruct.run`, test-first, so the same corpus and task run on a top-tier planner and extractor. Choose the verifier per ADR 0009 (other family from the generator). Write that config to `research/d1_demonstrator/models_toptier.json`.
   - Caps: cheap arm `--max-usd 1.5`, top-tier arm `--max-usd 5`. Report both arms.
   - Apply the I8 admissibility rule (if merged) and report its status. Admissibility does not gate the demonstrator.

3. **Gap map (step 2, $0).**
   - Run `gapmap` on each arm's ledger. Use the cached or local qwen judge.
   - Report where the two arms agree on the thin areas.

4. **Question sheet (step 3), written before the owner answers.**
   - Take 10 questions from the top-ranked gap areas (union of both arms, ties by top-tier rank).
   - Take 5 questions from areas the map rates best covered.
   - Phrase all 15 in the same CDM-style form and length band.
   - Shuffle with a fixed seed. Write the arm key to `sealed/key.json`, hash it into `PREREG.md` and never show it to the owner.
   - Write `PREREG.md` with the question sheet hash, the key hash, the novelty rule below and the decision rule.
   - Run `methods-critic` on `PREREG.md` and fix what it finds.
   - Run the rule's L7.3 checks on SYNTHETIC answers before committing it:
     - a planted positive (gap answers novel, covered answers not) must give Continue;
     - all-novel and all-copied stand-ins must not;
     - length-matched filler must not.
   - Then commit the hash.

5. **Owner answers (about 45 minutes).**
   - Give the owner the shuffled sheet only, in `questions.md`.
   - The owner answers in `answers.md`, in plain prose, without the docs open.
   - Nothing about the arm key is said until all 15 are locked (`answers.lock.json` with its sha256).

6. **Novelty check.**
   - For each answer, a top-tier judge sees the answer and the retrieved corpus passages for that area, not the arm. It states whether the answer adds a fact, check, rationale or step that the corpus does not contain: `new` / `partly` / `already written`.
   - Run a second, other-family judge on the same pairs (ADR 0009). A reading counts only where both agree.
   - The owner also rates each of their own answers, as a secondary measure.
   - Cap the judges at `--max-usd 1.5` together.

7. **Decision rule** (fixed in step 4).
   - Novelty rate = share of `new` answers among answers where both judges agree.
   - **Continue** (the idea survives a first real test) if the gap-question rate minus the covered-question rate is at least **0.30**, and at least 5 of the 10 gap answers are `new`.
   - **Change** (fix the gap map's ranking before anything else) otherwise.
   - Report the difference, its exact permutation p-value over the 15 labels, and the owner's self-ratings beside the judges'.
   - State plainly that this is one expert, the system's owner, on one codebase.

8. **Onboarding notes (step 4).**
   - From the owner's answers, write `onboarding.md` for a new contributor.
   - Mark each paragraph with its evidence label: `observed human evidence` (the owner's answer) or `organisational-artefact-supported` (the docs).
   - Link it beside the existing docs, and list which answers are not in the docs today, as candidate doc additions the owner may accept.

9. **Step 5 is design only.**
   - One paragraph says how newcomer struggle would be measured later (for example, issues and questions from first-time contributors), and that no learner was involved.

## Never
- Never present the result as N3, as evidence for RQ-B, or as a validated product.
- Never run a live call inside a test. Never exceed the caps. Never edit the owner's repository.

## Done when
- The pipeline tests pass.
- `RESULT.md` opens with the Question / Answer / Changed card and gives the decision, both arms' figures and the costs.
- `report.json` is written.
- `onboarding.md` exists.
- The owner has seen the arm key revealed after locking.

## Decision it feeds
Continue or Change for the gap map's ranking, read on one real expert. It also decides whether D1 grows into a demonstrator the owner can show (owner decision at the end).
