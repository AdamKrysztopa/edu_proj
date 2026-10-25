# I7: Freeze manifest and historical-admission fixtures

**Branch:** `i7-freeze-manifest`, from `plans-2026-10-24` (I1 and I1c are merged there: donor pairing is decoupled from the config hash, and `control2.json` carries `pairs_sha256`).
**Outputs:**
- code: `gapmap/src/gapmap/manifest.py` with its tests, and an admission-fixture module in `reconstruct/` with its tests;
- note: `research/freeze_manifest/RESULT.md`.

**Cost:** $0.

## Context
- Read `docs/plans/implement-queue.md` § I7 and `docs/plans/coverage-audit.md` findings 7, 13 and 15.
- Read `REORIENTATION.md` §14.3 (anti-circularity: freeze the feature set, weights, scope decomposition and area partition before any gold).
- Precedent: `residual/src/residual/freeze.py` and `residual/frozen/n1.json`.
- Precedent: Track A's `FrozenConfig`. Read it only; never edit `instrument/`.
- `gapmap/src/gapmap/config.py:135-166` hashes parameter values only.
- `reconstruct/src/reconstruct/run.py:657-658` hard-codes corpus mode as not N3-admissible.

## Steps
1. Build `manifest.py`. It computes one SHA over:
   - the predictor source files: lenses, link, text, semantic, judge, rank, record, checks, `control2`, area (I12 replaces the predictor inside `area.py` in parallel: hash the file set, not a function list, so its change is caught);
   - the judge prompts, the model IDs and reasoning effort of both closure arms (ADR 0009: sol and the guard judge I2 settles);
   - `config._canonical()`;
   - `residual/src/residual/features.py`, I5's `auroc.py` and `baselines.py`, `research/n3_control_v3/compare.py` (it computes the ADR 0009 direction), `l73.py` and `gapmap/tests/l73_fixtures.py`;
   - the area partition file;
   - the eligible-gold list file.

   Write `research/freeze_manifest/manifest.json` with the per-file hashes. The CLI gets a `--require-manifest <sha>` that refuses to run on any mismatch.
   Tests hash a temporary copy of the files, never a literal SHA, because I2, I5 and I12 change hashed files in parallel; the committed `manifest.json` is regenerated after they merge.
2. **Mutation tests (L7.3).** Change one character in each hashed file, in turn; every change must be refused. Changing a comment-only file outside the set must not be refused.
3. **Historical-admission fixtures** in `reconstruct/`. Build a pure function `admit(document, gold_date, blocklist)` that rejects:
   - documents dated after the gold;
   - undated documents;
   - documents dated only by `Last-Modified`;
   - documents matching the blocklist by DOI, normalised title or landing-page URL.

   Test it on planted documents: every one that should be rejected is rejected, and a properly dated scholarly record is admitted.
4. Do **not** freeze any values. Freezing the values waits for MS1 and I6. This item builds and proves the mechanism only.

## Done when
The tests pass, and `RESULT.md` reports the mutation-detection results and the fixture results.

## Decision it feeds
Whether the machinery can hold a pre-registration boundary. The MS2 freeze uses it, and so does the out-of-sample domain run that I4 needs.
