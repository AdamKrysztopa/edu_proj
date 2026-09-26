---
name: branch
description: Investigate one branch of the AI-education research map — explore a method, compare two, try to falsify one, or design the first experiment — and update the map only where evidence justifies it.
argument-hint: explore|compare|falsify|experiment <METHOD> [METHOD B]
disable-model-invocation: true
---

# /branch

The map is `ai_education_research_map.md`, the project's single source of state. Arguments: `$ARGUMENTS`.

## Modes

| Mode | Question to answer | Verdict required |
|---|---|---|
| `explore <M>` | Empirical evidence, criticisms, domain fit, operational method, how M plugs into the §6 architecture | Change to M's priority/evidence rating, or none |
| `compare <A> <B>` | Overlap, differences, evidence quality, implementation cost, for eliciting hidden expert reasoning in university physics | A minimal experiment that discriminates them |
| `falsify <M>` | Critiques, null findings, validity problems, better alternatives | **keep / narrow / park / reject** |
| `experiment` | Smallest defensible study that AI-assisted DtD/CTA elicits expert knowledge that improves novice transfer in one physics topic | A design, then hand it to the `methods-critic` agent |

If the mode or method is missing or not in §4, ask once and stop.

## Procedure

1. Read the map. Quote the current card for M (§5.x), its §4 row, and any §9 phase / §10 RQ it serves. That is the baseline you are allowed to move.
2. Check the Zotero library first (`zotero` MCP) for what the user has already read; cite those notes where relevant.
3. Search the literature with the `openalex` MCP: forward citations of the card's anchor papers, systematic reviews and meta-analyses, then critiques. Fall back to WebSearch only if OpenAlex is unavailable, and say so.
4. Grade each source you rely on: design (meta-analysis / RCT / quasi-experiment / qualitative / theory), N, domain, and whether the outcome is transfer, retention or immediate performance. Evidence from outside physics or university level must be labelled as such.
5. Hold every conclusion against §11 "What not to assume". A finding that only shows fluency, immediate correctness or plausible-sounding LLM output does not count as support.
6. Write `research/<mode>-<method-slug>.md`:
   - **Question** (one line) and **verdict** (one line)
   - **Evidence** — claims, each with DOI and its grade from step 4
   - **Against** — strongest counter-evidence found; "none found" only after a targeted search for it
   - **Implications for the map** — the exact edits proposed, section by section
   - **Open questions** — only ones that would change the verdict
7. Launch the `citation-verifier` agent on the new file. Fix or drop anything it flags before going on.
8. Edit the map with only the proposed changes that survived verification. Never touch branches unrelated to M. Commit with the verdict as the subject line.
9. Before closing the branch, record each mistake caught during it (a citation the verifier flagged, a claim a source falsified) with the `lessons` skill. The branch isn't done while one is uncaptured.

## Stop conditions

- No source at or above quasi-experimental design supports a change → leave the rating as it is and say the evidence is insufficient.
- A kill criterion from §9 is met → state it at the top of the research note, not in the map's body text.
