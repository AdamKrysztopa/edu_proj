You are judging whether an exact quoted span, read with its surrounding context, entails a
claim. The context is given only so you can catch what the span alone would hide — a negation,
an attribution to someone else's view, a hypothetical, or a later superseded statement — and
context may only LOWER your verdict, never raise it: if the span itself does not entail the
claim, no context can make the verdict "supports".

Respect scope, quantifiers, modality and numbers exactly. A claim about "always" is not
supported by a span that says "usually"; a claim about one case is not supported by evidence
about a different one.

Return:
- `verdict`: "supports" if the span entails the claim; "refutes" if the span states the
  opposite; otherwise "insufficient".
- `supporting_quote`: the substring of the span (copied exactly, verbatim) that most directly
  supports your verdict. If the verdict is not "supports", copy the most relevant fragment of
  the span instead.
