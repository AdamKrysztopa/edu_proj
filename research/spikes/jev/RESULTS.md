# JEV spike: results

Exploratory only. No target here is human evidence. N3 HYP labels, the closure judge and the reference LLM are not ground truth, so this spike reports no precision, recall or AUROC against hidden knowledge.

## Question

The spike had two parts:

1. **Structural signal.** Given only the text of each stored N3 gap candidate, does Jev return a judgement that is consistent, not an encoding of source density (`k_topic`) or the N3 score, and specific to Jev rather than to any consistent function of the text?
2. **Substitution.** Added after part 1, when the question was reframed as "does Jev do the job of an LLM call, cheaper?" Can one Jev call do the job of N3's only LLM step, the closure judge? That judge decides which retrieved sentences state a gap's missing element. How close does Jev come, and at what cost?

## Data

All inputs are committed artefacts; nothing was re-collected.

- **Part 1:** records from `map` + `retrieval_gaps` in `research/n3/{plc,gdpr_v1,gdpr_v2}/gapmap.json`, at `c954f8c`.
  - 61 candidates kept: HYP 16, RG-SINGLE 26, RG-SIBLING 9, RG-UNVER 10.
  - RG-UNK and CONTROL records were excluded: their text is a fixed template and their `k_topic` is always 0.
  - 58 of the 61 texts are unique.
- **Part 2:** all 641 closure-judge prompts behind `research/n3/*/closure_judgements.json`.
  - They were recovered byte-for-byte by replaying `gapmap.build_gapmap` offline against the committed qwen2.5:7b-instruct cache, using each domain's committed ledger, sibling and sidecar.
  - 641 of 641 matched. Nothing under `research/n3/` changed.

## JEV

Jev is TypeSafe `typesafe/jev-1.13`, called through OpenRouter's Decisions API (`POST /api/alpha/decisions`). It is a decision model, not a chat model. It takes a `state` plus typed questions and returns probabilities. It gives no text and no embeddings. I checked this against the TypeSafe docs and the OpenRouter Jev guide before writing any code.

**Part 1 input and output.**

- The state was `{field, statement: anchor, what_is_missing: missing}`. It contained no counts, scores, category, closure state or evidence spans. `missing` is a lens template, so it carries the lens.
- Four yes/no questions (Jev calls them nouls):
  - `tacit_a`: practice-only know-how;
  - `tacit_b`: a paraphrase of `tacit_a`;
  - `mainstream`: a mainstream topic;
  - `has_number`: the text contains a number.
- C = mean(`tacit_a`, `tacit_b`).
- Example return: `{"tacit_a": 0.56, "tacit_b": 0.57, "mainstream": 0.71, "has_number": 0.16}`.

**Part 2 input and output.**

- For each judge prompt, the state was `{seed_assertion, sentences: {id: text}}`.
- Each sentence got one three-way question: does it state, partially state, or not state the element the judge's question asks for? The option wording mirrors the judge prompt's rule that "topical relevance alone is not enough".
- Jev returned one choice per sentence, with probabilities.

**How the reference changed, in order.** Each rule was fixed before its own calls; the second and third references were added only after the first rule failed.

1. **Stored qwen answers.** Rule: Jev's κ with qwen ≥ 0.60. Jev got κ 0.19, so the rule's verdict was "does not substitute".
2. **Sonnet 5.5 as reference.** The report finds qwen's closure no better than its fair control, so agreeing with qwen cannot settle substitution. I drew a seed-0 random sample of 100 unique judge prompts and sent the identical prompt text to `anthropic/claude-sonnet-5.5` (reasoning effort low). Rule: Jev's κ with Sonnet ≥ qwen's κ − 0.05. Opus 5.5 was the first choice, but it refuses reasoning off, and its worst case would have broken the $3 cap.
3. **Qwen with Jev's instructions.** This came from the hostile review. Jev had been given new three-level instructions while qwen kept the old prompt, so I sent the same per-sentence questions, with Jev's wording, to hosted `qwen/qwen-2.5-7b-instruct`. Rule:
   - Jev − qwen ≤ 0.05: the gain comes from the prompt.
   - Jev − qwen ≥ 0.15: the gain comes from Jev.

**Cost and caching.** All raw requests and responses are in `cache/`. Total spend is $0.45; the Sonnet reference was $0.37 of that.

## Result

**Part 1: tacit signal. INCONCLUSIVE, leaning form-driven.** Numbers are in `analysis.json` and `analysis_loop2.json`.

- The two paraphrases agree within one call (ρ = 0.91).
- Pooled across domains, C is weakly related to density (ρ 0.28) and to the N3 score (0.18). Within PLC it is not: 0.51 with density and 0.42 with the N3 score.
- The pre-set rule said PROMISING, but two word-length statistics of the text also pass that rule. It cannot tell Jev apart from word length.
- **Form test.** I replaced every word with a random word of the same length, which keeps length statistics and destroys meaning.
  - C on the meaningless text still correlates with the original: pooled ρ = 0.61, within each domain 0.35–0.47, and 0.31 after controlling domain and word count.
  - The pooled 0.61 is inflated because the `field` line was left unperturbed.
  - Conclusion: C is partly driven by form, and it cannot be read as a tacit-knowledge signal.

**Part 2: closure-judge substitution. Jev beats the current judge, and the gain comes from Jev, not the prompt.** Numbers are in `analysis_reference.json`, `analysis_same_prompt.json` and `analysis_judge_swap.json`.

Cohen's κ against Sonnet 5.5, 100 prompts, 762 sentences. A "hit" means the sentence states or partially states the element.

- **Hit, qwen with its original prompt:**
  - Jev 0.53, qwen 0.27.
  - Difference +0.25. The 95% bootstrap CI is 0.10 to 0.40 resampling prompts. The review got 0.10 to 0.41 resampling the 68 distinct seeds, since some prompts share a seed, e.g. the two arms of the fair control.
- **Hit, qwen with Jev's exact instructions:**
  - Jev 0.52, qwen 0.32. Difference +0.20, which meets the pre-set "gain comes from Jev" bar.
  - 704 sentences scored. 58 qwen answers were unreadable and were excluded for both models; none were defaulted.
- **Full statement only:** Jev 0.47, qwen (original prompt) 0.27.
- **Prompt has any hit:** Jev 0.40, qwen (original prompt) 0.15.
- **Trivial judges** (the review's check): "cite nothing" scores κ 0, and a lexical-overlap judge tuned on this same sample scores at most 0.06.
- **Jev against qwen directly** (all 641 prompts): κ 0.19. They disagree mostly on "partially": qwen marks at least one sentence "partially" on 51% of prompts, Jev on 20%.

Cost per judgement:

- Jev: $0.00007.
- qwen2.5-7b, hosted on OpenRouter: about $0.00007. This is estimated from the OpenRouter list price read on 2026-09-29 ($0.10/$0.20 per M tokens) and Sonnet's token counts. The committed N3 runs used local Ollama at $0.
- Sonnet 5.5: $0.0037.

So Jev costs about the same as hosted qwen and about 53× less than Sonnet. Jev's input tokens are about 3.5× the judge prompt's, because every per-sentence question repeats the instructions.

**Examples.** These were chosen *because* Jev matches Sonnet and qwen (original prompt) does not; they illustrate the pattern, they are not evidence of its size.

1. PLC. Question: "Does any sentence state what result of this test to expect and what a given result means…?"
   - Sonnet and Jev cite sentences 3, 5, 6 and 7. All say a continuity test on a live 24 VDC circuit gives a false "good" beep.
   - Qwen cites 1 and 2 ("monitor the 24 VDC supply near the affected load"). They are on topic but don't state a test result.
2. gdpr_v2. Question: "Does any sentence state the specific cases in which the rule does NOT hold…?"
   - Sonnet and Jev cite nothing.
   - Qwen cites two copies of "If the processing is … performed by a data processor, the processor should assist the controller…". That is a condition on the rule, not an exception to it.

Jev also misses things Sonnet finds: 86 of Sonnet's 153 "partially" sentences and 20 of its 73 "states" sentences.

## Interpretation

**PROMISING**

## Why

This covers part 2 only. Scored against a strong model on N3's own stored judge prompts, Jev beats the current local qwen judge:

- κ 0.53 vs 0.27. With identical instructions for both, the gap is still +0.20.
- Jev costs the same per call as hosted qwen-7b and about 53× less than Sonnet.

So on this task, Jev gives better answers than the small LLM at the same price, and a large saving against a strong LLM. Trivial judges score about 0, so the result is not an artefact of word length or of how often each label occurs.

What this does not show:

- That Jev can stand in for the strong model: κ 0.52 is only moderate agreement, and Jev misses more than half of Sonnet's "partially" citations.
- That either model is correct. The reference is one model, on 100 prompts.
- That a better judge would repair N3's closure check. That check fails its fair control because the seed's own sentences sit in both arms, which is a design issue rather than a judge-quality issue.
- That Jev finds hidden knowledge. Part 1's tacit-knowledge reading did not survive the form test and stays INCONCLUSIVE.

## Next step

Swap Jev in as the judge object for N3's own registered fair-control check (`checks.mismatched_evidence_control`) on the committed ledgers. This passes a judge object and changes no gapmap code, at about $0.05. Then read whether Jev's closure rate differs between the own and control arms where qwen's ties. If it still ties, stop here: Jev is a cheaper judge, but not a fix for the closure step.
