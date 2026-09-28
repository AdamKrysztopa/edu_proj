You are constructing a decoy for a named mutation type, given a real claim and its supporting
quote. Produce a claim the SAME quote should no longer support, mutated ONLY in the way named:

- `number`: change exactly one number or quantity.
- `negation`: negate the claim (state the opposite).
- `scope`: make the claim STRONGER or otherwise different from what the quote actually supports
  — broaden a population, system, jurisdiction, time or condition beyond what the quote states;
  add an unstated "all"/"always"/"every"; drop a hedge or attribution ("in my experience") in
  favour of a flat assertion; or swap a connective (and -> or, or -> and, "in combination with"
  -> "or", "only if" -> "if") in the direction that makes the claim stronger or broader. Never
  narrow the claim and never drop a conjunct from a list — a weaker claim can still be true of
  the same quote, which makes it an invalid decoy.

Keep the sentence otherwise as close to the original as possible, so the mutation is the only
difference that matters.

Return:
- `mutated_claim`: the mutated claim. It must be a real change from the original claim.
- `mutation`: the mutation type you were given ("number", "negation", or "scope").
- `rationale`: one line explaining specifically why the quote no longer entails the mutated
  claim (e.g. "the quote says 'usually', the mutated claim says 'always'").
