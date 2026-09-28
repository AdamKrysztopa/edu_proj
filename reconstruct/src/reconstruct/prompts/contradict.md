You are given two claims, each with its supporting quoted span and source date. Classify their
relationship conservatively, choosing exactly one kind:
- `genuine`: both claims cannot be true in the same scope and at the same time — a real
  contradiction.
- `scope`: they apply to different scopes, conditions or populations.
- `temporal`: one statement has been superseded by the other over time.
- `terminology`: they use different words for compatible ideas.
- `insufficient`: there is not enough here to judge.
- `compatible`: both can be true together.

Only choose `genuine` when you are confident that no scope, time or terminology difference
explains the apparent difference.

Return: `kind`, and one verbatim quote copied from each span (`quote_a`, `quote_b`) that shows
the disagreement.
