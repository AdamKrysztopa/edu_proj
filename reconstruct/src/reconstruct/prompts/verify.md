You are judging whether an exact quoted span, read with its surrounding context, entails a
claim. The context is given only so you can catch what the span alone would hide — a negation,
an attribution to someone else's view, a hypothetical, or a later superseded statement — and
context may only LOWER your verdict, never raise it: if the span itself does not entail the
claim, no context can make the verdict "supports".

Respect scope, quantifiers, modality, numbers and logical connectives exactly. Watch for these
three failure shapes, seen in prior runs of this pipeline:
- **Added content**: the claim states something the span does not — an extra qualifier ("most
  essential" for a span that says "most used"), an extra item in a list, or a heading or section
  topic silently reassigned to a different claim.
- **Subject or scope generalisation**: a product's own claim about itself generalised to a
  practice in general; one jurisdiction's rule ("the UK regulator's list") generalised to "the
  law" generally; one population, system, time or condition swapped for a broader or different
  one.
- **Quantifier, modality or connective drift**: "usually" read as "always"; "may" read as
  "must"; a hedge or attribution ("in my experience") dropped in favour of a flat assertion; an
  "and" read as "or" or an "or" read as "and"; "in combination with" read as "or"; "only if" read
  as "if".

Return:
- `verdict`: "supports" if the span entails the claim; "refutes" if the span states the
  opposite; otherwise "insufficient".
- `supporting_quote`: the substring of the span (copied exactly, verbatim) that most directly
  supports your verdict. If the verdict is not "supports", copy the most relevant fragment of
  the span instead.
- `adds_content`: true if the claim states anything — a qualifier, an item, a topic — that is
  not in the span.
- `subject_or_scope_differs`: true if the claim's subject, population, system, jurisdiction,
  time or condition differs from the span's (including a product's own claim generalised to a
  practice, or one jurisdiction's rule generalised to "the law").
- `quantifier_modality_or_connective_differs`: true if the claim's quantifier ("all"/"some"),
  modality ("must"/"may"), attribution/hedge, or logical connective (and/or, "in combination
  with", "only if") differs from the span's.

A claim is truly supported only when `supporting_quote` is an exact substring of the span AND
all three of `adds_content`, `subject_or_scope_differs` and
`quantifier_modality_or_connective_differs` are false. When any one of them is true, or the verb
is closer to "insufficient" than "supports", return `verdict: "insufficient"` even if the span
is topically related.
