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
