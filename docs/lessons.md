# Lessons — queue

A **queue, not an archive**. Empty is the healthy state. An entry's job is to survive the hours
between the mistake and the next drain — not to be permanent.

Write an entry **at the moment the mistake is caught**, not at the end of the session. By the end
the bug is fixed, the diff looks clean, and the only trace is a correction nobody can reconstruct
into a rule.

**Nothing is carried across two drains.** An entry that survives one drain is an entry nobody
intends to implement, and a queue with permanent residents stops being read. Either implement it,
or decline it in the archive with the reason.

Entries are drained by the `implement-ll` skill and land in `LESSONS-ARCHIVE.md`. Ids (`L<drain>.<n>`)
are assigned at drain time — don't number entries here.

## Entry format

```markdown
### <short title>

- **What happened:** the specific fact, with `path:line` or a quotation. Include *how it was
  caught* — that is frequently the real finding.
- **Generalises to:** one sentence, stated as a rule someone could follow.
- **Candidate home:** a suggestion, explicitly not a decision.
```

`Generalises to` is the filter. If the entry cannot be written as a rule someone could follow, it
is an anecdote and does not belong in the queue.

There is no status field. Presence in this queue is the status.

## What is not a lesson

- A typo.
- A one-off misreading with no general shape.
- A decision that was correctly argued and went the other way.

A queue padded with those is a queue nobody drains.

---

## Open

<!-- Append entries below. After a drain this section is empty again. -->

### Route-surface test filtered to the route type it expected

- **What happened:** `test_every_route_is_either_expert_or_loopback_only` (`instrument/tests/test_server.py`) keeps only `APIRoute` entries of `app.routes`, so it passed while FastAPI's `/openapi.json`, `/docs`, `/docs/oauth2-redirect`, `/redoc` and the `/static` mount (`console.html`, `js/console.js`) answer a non-loopback client with 200. That contradicts decision 0005's "only the expert routes are reachable from the network". It was caught while binding the rule: a strict test that requested every `Route`, `Mount` file and `APIRoute` from a tablet `TestClient` listed exactly those six URLs.
- **Generalises to:** A test that claims to cover a whole surface must enumerate it without filtering by type, and must fail on any entry it cannot classify, because a filter silently narrows the claim to what the author expected to exist.
- **Candidate home:** `arch-crew` binding practice for decision 0005, or a test-writing rule in `CLAUDE.md`.

### Hook registration pointed at a script its own commit deleted

- **What happened:** `.claude/settings.json:9` registers `.claude/hooks/check-dois.sh` as the PostToolUse DOI check, but `4e790e2` replaced that script with `check-dois.py` and deleted the `.sh`, so the L1.1 DOI check has not run on any edit since. No check caught it; a read-only repository audit during the reorientation found it by reading the settings file against `ls .claude/hooks`.
- **Generalises to:** Every hook registered in settings must resolve to an existing executable, checked by a test, because a missing hook script fails silently and looks like a clean pass.
- **Candidate home:** a test in `instrument/tests/test_gates.py` (or a repo-level test) that resolves every `command` path in `.claude/settings.json`.

### A fetch tool's summary invented a figure for the paper it summarised

- **What happened:** during the reorientation research, a WebFetch summary of Acquaye et al. (arXiv:2601.09953) reported a "63% distractor match rate vs 25% chance" that does not occur in the paper; the researcher agent caught it only by reading the PDF text before writing the note (`research_notes/Tacit knowledge reorientation/adjacent_fields_and_falsification.md`).
- **Generalises to:** A number enters a research note only after it is found verbatim in the source's own text, never from a summarising tool's paraphrase, because the summariser can fabricate figures that look like the paper's.
- **Candidate home:** `citation-verifier` agent (check quoted numbers against source text), and the researcher brief used for deep-research subagents.

### A plan whose only admissible evidence needed absent people defaulted to tooling

- **What happened:** between `6f228c2` and `4e790e2` every open milestone (M1–M8, assumptions A1–A10) required experts, a cohort or a course, none of which existed; with nowhere else to go, the work became ever more careful instrument-building (session app, tablet audio, freeze machinery), and `PROGRESS.md` ended with "both now wait on people". Caught by the reorientation audit (`REORIENTATION.md` §3), not by any gate; L1.11 had named the symptom but not the cause.
- **Generalises to:** Every research plan must name at least one route to evidence that is available now; if its only admissible evidence needs people or data the project does not have, the plan is revised before anything else is built.
- **Candidate home:** `/branch` skill's experiment mode and `methods-critic` checklist (reject a plan with no currently available evidence route), or the phase-gate rule in `REORIENTATION.md` §22.

### Condensing notes into a synthesis reintroduced grain errors L2.1 was meant to stop

- **What happened:** `REORIENTATION.md` was written from the eight research notes under an explicit L2.1 instruction, yet `citation-verifier`, checking against the primary sources, found about 45 content defects: an inverted figure ("64–69% not mentioned by experts" for Zhou et al., where the source says 64–69% of *unmentioned* arguments were helpful), a certification rate reported as an agreement rate (RankCert 3.75%), novice conversations described as expert ones (Cho et al.), a within-expert test–retest r described as between-expert agreement (an error already present in `tacit_knowledge_foundations.md`), and ranges that exist only in the notes. The error was caught by verifying against sources, not against the notes.
- **Generalises to:** A synthesis built from intermediate notes is verified against the primary sources, never against the notes, because the notes carry their own errors and condensing adds new ones even under an explicit grain rule.
- **Candidate home:** `citation-verifier` agent brief (verify syntheses against the source text, list note-only figures), and the L2.1 archive entry, which did not prevent this.

### The DOI hook checks only one citation form, and the new documents use the other

- **What happened:** after `.claude/settings.json` was repointed to `check-dois.py`, the hook passed `REORIENTATION.md` silently: its pattern (`check-dois.py:15`) matches only `https://doi.org/…` URLs, and the document cites its 105 DOIs as `doi:10.…`. It demonstrably blocks a bad `doi.org` link. Caught by counting both forms in the document after a suspiciously quiet pass.
- **Generalises to:** A citation check must match every identifier form the repository's documents use (and fail on an identifier it cannot parse), because a check scoped to one form reports a clean pass on documents written in another.
- **Candidate home:** `check-dois.py` pattern plus a test with one citation in each form; or a style rule fixing one DOI form for all research documents.
