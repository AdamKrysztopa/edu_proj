# Topic review prompt (D1c plan §3.4, registered before use)

You review a list of candidate topics for a question sheet. Each line is `- T<id>: <question text>`.
The questions are generated from a software project's documentation, and several may ask about
the same underlying point in different words.

Flag every pair of topics that ask about **the same underlying point**: an answer to one would
substantially answer the other. Different wording, lens or question template does not make two
topics different. A shared word or a shared broad area does not make them the same.

For each group of topics on one point, keep the lowest ID and drop every other ID in the group.

Read only the file named below. Do not open any other file, run no code beyond reading it, and
make no network call. Write one JSON object to the output path:

```json
{"drop": ["T…", …], "reasons": {"T…": "same as T…: <the shared point in a few words>"}}
```
