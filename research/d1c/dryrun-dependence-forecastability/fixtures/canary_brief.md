# Canary brief

You write two short answers used to check two blind judges. Each judge compares an expert's
answer with passages from a software project's documentation and labels it "new" (it adds
knowledge the passages lack) or "already written". You never see a question the expert was asked,
or any expert answer.

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

Three trivial labellers must each get one of your two answers wrong: "new iff it contains a digit"
(so if the planted answer has digits, the paraphrase must carry one too, for example a number the
passage states), "the longer answer is new" (so the planted answer may be at most
20% longer than the paraphrase) and "the answer with less word overlap with the
documentation is new" (so the planted answer should reuse at least as much of the documentation's
own vocabulary as the paraphrase does).

Write `paraphrase_question` and `planted_question` in the same style as these candidate questions. They were generated for this project but are not on the expert's sheet, so no expert answer to them exists:

> Sources say: "When you suspect that longer lags add noise rather than signal (the curve never plateauing is also informative).". What would happen if someone did it differently, and in what situations, if any, is doing it differently acceptable?
> Sources say: "require cross-backend agreement before acting on lag recommendations". What would happen if someone did it differently, and in what situations, if any, is doing it differently acceptable?
> "Selection of a method should be based on your objectives and your conditions (data etc.).". Think of the last time you made this choice. Which options did you consider, which did you take, and what about that situation decided it? When did you last choose differently?

Paths are relative to the repository root. Save it as `research/d1c/dryrun-dependence-forecastability/fixtures/canaries.json`. The documentation is the HTML
under `research/d1_demonstrator/corpus`; you may search it. Then run `uv run --directory gapmap python ../research/d1b_rerun/canaries.py check --codebase ../research/d1c/dryrun-dependence-forecastability/codebase.json` from the repository root and revise until it prints `"ready": false` with only the owner's confirmation
missing. The owner confirms both labels before use.
