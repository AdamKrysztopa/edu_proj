# I7: Freeze manifest and historical-admission fixtures

- **Question:** Can the freeze manifest and the historical-admission rule hold a pre-registration boundary?
- **Answer:** Yes, as a mechanism. The manifest refused 40 of 40 planted mutations and accepted 2 of 2 comment-only edits outside the set. `admit` classified 17 of 17 planted documents as planted. No value is frozen yet.
- **Changed:** The MS2 freeze becomes: write three files into `research/freeze_manifest/`, regenerate `manifest.json`, register its SHA, and run `python -m gapmap` and `python -m gapmap.control2` with `--require-manifest <sha>`. The check is added to the other scored commands before MS2 names them. None of the 80 sources in the committed PLC and GDPR runs passes a 1994 gold date.

## Result

**Decision it feeds:** whether the machinery can hold a pre-registration boundary (MS2 freeze, and the out-of-sample domain run I4 needs). **Continue**: the mechanism holds on every planted case. The freeze itself waits for MS1 and I6 (values), a guard arm not yet chosen (I2 found none eligible: coder32 was dropped on 2026-10-24) and DS1 (the eligible golds).

### The manifest (`gapmap/src/gapmap/manifest.py`)
One SHA over 37 files and the config values (`research/freeze_manifest/manifest.json`, field `roles`):

| Role | Files | What it covers |
|---|---|---|
| `gapmap` | 14 | every `*.py` in `gapmap/src/gapmap/` except `config.py` and `render.py` |
| `residual` | 15 | every `*.py` in `residual/src/residual/`, including `features.py` and I5's `auroc.py`, `baselines.py` and `reach.py` |
| `controls` | 4 | `research/n3_control_v3/compare.py`, `l73.py`, `gapmap/tests/l73_fixtures.py`, `gapmap/tests/conftest.py` |
| `admission` | 1 | `reconstruct/src/reconstruct/admission.py` |
| `partition`, `eligible_gold`, `closure_arms` | 3 | `research/freeze_manifest/{area_partition,eligible_gold,closure_arms}.json` |
| config | — | `config._canonical()`, hashed by value; equal to `CONFIG_SHA256` |

- **Additions beyond the item's list.** Each one is something whose change would move a scored result:
  - Both packages are hashed as file sets, so a new module (I2's `jev.py`, I5's `reach.py`) is caught without being named.
  - The set therefore also holds `__main__.py`, which decides which records reach the map, and `manifest.py` itself.
  - `conftest.py` builds the ledgers that `l73_fixtures.py` plants into.
  - `admission.py` is the temporal rule.
- **Judge prompts.** The judge prompts live in `semantic.py` (`_QUESTIONS`, `build_prompt`), so its file hash covers them.
- **Closure arms.** The model ID and reasoning effort of both closure arms are read from `closure_arms.json`. `--require-manifest` also refuses unless the run's judge model is one of those two arms. `python -m gapmap` checks `config.JUDGE_MODEL`; `control2` checks `--model` and `--reasoning-effort`. An arm registered with no effort matches any effort.
- **Byte-level hashing.** Files are hashed byte for byte, so a comment added to a hashed file is refused. That covers more than `residual/frozen/n1.json`, which byte-hashes six residual modules but hashes the schema only by structure.
- **The CLI flag.** `--require-manifest <sha>` is on `python -m gapmap` and `python -m gapmap.control2`. It refuses before the ledger is read when any of these holds:
  - a file is missing;
  - the SHA differs (it names the changed files when the recorded `manifest.json` carries the required SHA);
  - the judge is not a registered arm.

  `control2.json` and `gapmap.json` record the SHA they ran under.

**Mutation test (L7.3)**, on a scratch copy (`research/freeze_manifest/mutation.json`):

| Probe | Expected | Correct |
|---|---|---|
| one character changed in each hashed file, in turn | refused | 37 / 37 |
| a config value (`TERMHOOD_MIN_CLAIMS` 2 → 3), a new module in the package, `area.py` deleted | refused | 3 / 3 |
| comment appended to `config.py` and to `render.py` (outside the set) | accepted | 2 / 2 |

The copy was restored after every probe, and after the last probe its SHA equals the base (`base_restored: true`). The three freeze files not yet written have placeholders in the copy (`placeholders`), so every role is probed.

**Defect caught by the planted positive.** The first build loaded `config.py` with `importlib` to hash its values. The config-value probe was accepted under pytest, because a same-size edit within one second was served from the stale `__pycache__` entry. It passed when run standalone. The values are now compiled from the source bytes. The lesson is queued in `docs/lessons.md`.

**Committed `manifest.json` is incomplete by design:** SHA `d38a1720…`, `complete: false`, with three files missing:
- the partition, the eligible-gold list and the closure arms, not frozen yet.

`check` refuses any incomplete manifest, so nothing can run under this one. It was regenerated after I2, I5 and I12 merged and again after `compare.py` changed (`264cb43`): 37 files, 40/40 mutations refused; it stays incomplete until the three freeze files exist.

### Historical admission (`reconstruct/src/reconstruct/admission.py`)
`admit(document, gold_date, blocklist)` is pure. It returns every reason a document is refused:
- **Undated:** the document has no page-stated publication date. A page modification date alone does not date it.
- **Last-Modified only:** the only date is the HTTP `Last-Modified` header. The header is server file time, so it neither dates nor rejects a document. A post-gold header beside a pre-gold publication date is admitted.
- **On or after the gold:** the later of the publication date and any page-stated modification date falls on or after the gold date. The same day is refused, because a day's precision cannot order two documents.
- **Blocklisted:** the DOI matches after normalisation (case, `doi:` or resolver prefix, percent-encoding, a DOI inside a landing-page URL), or the title matches after normalisation (NFKC, case, punctuation, spacing), or the landing-page URL matches after normalisation (scheme, `www.`, trailing slash, fragment). The URL check covers the requested and the final URL. A blocklist match rejects the document whatever its date.

**Fixtures** (`reconstruct/tests/admission_fixtures.py`, `research/freeze_manifest/admission.json`): 17 of 17 classified as planted.
- **Rejected, 13 of 13:**
  - 3 dated after or on the gold, and 1 revised after it;
  - 2 undated;
  - 2 dated only by `Last-Modified`;
  - 2 by DOI, 1 by title and 2 by URL.

  Each blocklisted plant is pre-gold, and each is admitted with an empty blocklist, so the blocklist alone rejects it.
- **Admitted, 4 of 4:** the properly dated scholarly record, plus three near-miss stand-ins:
  - a longer title containing the gold's;
  - a DOI that is the gold's DOI plus one character;
  - a post-gold `Last-Modified` beside a pre-gold date.

**Replay on committed artefacts.** No rule was changed, and `admit` is not wired into `run.py`. Still, at the fixtures' gold date (1994-06-01, the era of the 1993–94 CTA golds), with no blocklist, **0 of 80** sources are admitted. The sources come from the three committed E-LIVE sidecars that hold any; the other three are incomplete runs with none:
- 52 are undated;
- 20 are dated in or after 2017;
- 8 are dated only by `Last-Modified`.

This is consistent with coverage-audit finding 21. These are PLC-maintenance and GDPR sources, and most fail for lack of any page-stated date. A live search on a gold-era task has not been tried. (Finding 21's `run.py:657-658` is now `run.py:697-698`.)

## Limits
- The manifest guards the two CLIs above. `l73.py`, `compare.py`, `area.py`'s CLI and `reconstruct.run` do not check it yet. The MS2 registration must name the commands that run under it.
- `admit` is not wired into reconstruction. Corpus mode (`run.py:697-698`) still marks every run as not N3-admissible, and its manifest documents carry no dates. Wiring both is the out-of-sample run's work.
- A year-only date (for example "1994") does not parse in `reconstruct.web`. It reads as undated and is rejected, which is conservative and costs coverage.
- Sidecars written before `modified_field` existed leave a modification date's origin unknown. The replay treats such a date as page-stated, which is conservative.

## Reproduce
```
uv run --directory gapmap python -m gapmap.manifest --write --audit ../research/freeze_manifest/mutation.json
uv run --directory reconstruct python ../research/freeze_manifest/admission_report.py
uv run --directory gapmap pytest -q tests/test_manifest.py
uv run --directory reconstruct pytest -q tests/test_admission.py
```
