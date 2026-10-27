# Canary brief

You write two short answers used to check two blind judges. Each judge compares an expert's
answer with passages from a software project's documentation and labels it "new" (it adds
knowledge the passages lack) or "already written". You never see any real question or answer.

Source passage, from the project's own documentation (id 5983b51b770f, "Lagged-Exogenous Triage"):

> > [!IMPORTANT] > A `selected_for_tensor=True` flag at $k = 0$ is impossible by default. > It requires an explicit `known_future_drivers` opt-in at the use-case layer. > This is not a library limitation — it is an intentional chronological-causality > guard.

Write one JSON object with these keys:

- `source_id`: "5983b51b770f".
- `paraphrase_question`: a question a newcomer to the project could ask that the passage answers,
  naming its topic in the documentation's own terms (the judges are shown the passages retrieved
  for the question and the answer together, so the source must still be found).
- `paraphrase`: an expert's answer to it that says what the passage says in new words. Keep every
  claim, add none, never reuse a run of more than 6 words from the passage, and keep
  its length between half and twice the passage's.
- `planted_question`: a question on the passage's topic.
- `planted_new`: an expert's answer to it, 50 to 90 words, on the same topic, that states two or
  three concrete facts the documentation does not contain: a number with its unit, a threshold, a
  named case, a failure seen in practice. Invent them; keep them plausible.
- `planted_terms`: the exact short strings in `planted_new` that carry the invented facts (for
  example "a 3-day cutoff"). Each must occur nowhere in the documentation.
- `owner_confirmed`: false.

Two trivial labellers must each get one of your two answers wrong: "new iff it contains a digit"
(so if the planted answer has digits, the paraphrase must carry one too, for example a number the
passage states) and "the longer answer is new" (so the planted answer may be at most
20% longer than the paraphrase).

Paths are relative to the repository root. Save it as `research/d1c/dryrun-dependence-forecastability/fixtures/canaries.json`. The documentation is the HTML
under `research/d1_demonstrator/corpus`; you may search it. Then run `uv run --directory gapmap python ../research/d1b_rerun/canaries.py check --codebase ../research/d1c/dryrun-dependence-forecastability/codebase.json` from the repository root and revise until it prints `"ready": false` with only the owner's confirmation
missing. The owner confirms both labels before use.
