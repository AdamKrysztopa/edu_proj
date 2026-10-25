# Fire plan: prompts for the implement and deep-search queues (2026-10-24)

Every item's result note opens with a Question / Answer / Changed card and ships a `report.json` with one figure's rows (`_common.md` § Finish), so each wave's report is built from them directly.

Each item in [implement-queue.md](../implement-queue.md) and [deep-search-queue.md](../deep-search-queue.md) has one prompt file here. To fire one, start a fresh session (`/clear`) in the repo root and paste:

```
Read docs/plans/prompts/_common.md, then execute docs/plans/prompts/<FILE>.md exactly.
```

Each prompt states its own context, branch, outputs, owner decisions, done-criterion and the decision its result feeds. [`_common.md`](_common.md) holds the rules every prompt shares. Prompts in the same wave can run at the same time in separate sessions. Each works on its own branch, so they don't collide.

## Waves

| Wave | Fire | Needs first | Cost |
|---|---|---|---|
| **1: now, in parallel** | [I1](I1-closure-control.md) (recommended first), [DS1](DS1-gold-availability.md) (recommended first), [I3](I3-residual-identifiability.md), [DS3](DS3-decisive-delta.md), [DS4](DS4-identifiability.md), [I6](I6-area-features.md), [I9](I9-provenance-fixes.md), [I11](I11-cost-ledger.md) | — | $0 |
| **2** (revised 2026-10-24 after wave 1; launcher [WAVE2.md](WAVE2.md)) | [I2](I2-jev-control.md): an eligible guard judge for the closure control (qwen2.5-coder 32b first), Jev as a cheap substitute. Done: coder32 dropped (not runnable locally), Jev far from sol | I1c merged | ≤ $0.10 |
| | [I5](I5-gate-simulation.md): gate reachability at the set rules and the 16/4 split | DS3 package set | $0 |
| | [I12](I12-predictor-replacement.md): replace the predictor that is source count in disguise | I6 | $0 |
| | [I7](I7-freeze-manifest.md) | I1, I1c merged | $0 |
| | [DS2](DS2-closure-codebook.md), [DS6](DS6-verifier-validity.md), [DS7](DS7-boundary-sources.md) | — | $0 |
| | [DS5](DS5-pregold-fulltext.md) | DS1 register | $0 |
| | [DS8](DS8-oss-departures.md): moved up, since E-OSS now decides when E-CTA cannot | — | $0 |
| **3** | Re-judge the gap map's own closure with sol plus an eligible guard arm (today it rests on qwen 7b, which failed L7.3); OpenAI spend, cap set by the owner | a guard arm chosen and passing L7.3 (none yet: coder32 dropped) | owner cap |
| | Threshold-table blanks (primary model and baseline, minimums per gold and class, unmappable floor) | I5, I12, DS5 | $0 |
| | [I4](I4-v1-kit.md) | I1, I2 and DS2 merged; owner decisions (the prompt asks for them); I7 and I9 merged before its domain run | ≈ $0.5–1 |
| | [I10](I10-pregold-corpus.md) | DS1 and DS5 notes | ≤ $1 |
| | [I8](I8-admissibility.md) | — (Phase 1, V0; run before the MS2 freeze) | $0 |
| **Any time, lower priority** | [DS9](DS9-learner-licences.md), [DS10](DS10-eig.md), [DS11](DS11-sop-log.md), [DS12](DS12-surrogate-t2.md) | — | $0 |

The Tier 3 deep searches (DS13–DS17) have no prompt. They stay deferred until their trigger in the deep-search queue occurs.

## What changes the order

- **I1 shows the control already discriminates.** I2 shrinks to a confirmation run, and DS1 becomes the only critical-path item.
- **The owner adopts `REORIENTATION.md` §22 instead of the report's MS1.** I3 leads, because R4 is fatal-class.
- **DS1 finds fewer than three itemised golds.** Stop before I4. The MS3 route is dead, and the owner chooses a pivot (report §26).

## Budget

Waves 1–3 together cap at about $2. On 2026-10-24 the key had $14.99 of $15/week left. The deferred N2 reruns (≈ $19.40 in caps) have no prompt here, because I5 must first show they can reach a reading worth the spend.
