#!/usr/bin/env python3
"""PostToolUse on Write|Edit: every DOI in an edited markdown file must resolve, and resolve to
the work its line cites (first author's surname or two title words on the line).

Any form counts: doi.org links, `doi:10.…`, or a bare 10.xxxx/… identifier. A DOI that could not
be looked up is reported as unverified, never passed silently."""
from __future__ import annotations

import json
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

DOI = re.compile(r'(?:(?<=doi\.org/)|(?<![\w./]))(10\.\d{4,9}/[^\s\]\[<>"`\']+)')
CACHE = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")) / ".claude/hooks/.doi-verified"
STOP = {"about", "after", "their", "there", "these", "those", "which", "while", "within", "without",
        "between", "through", "under", "using", "study", "studies", "effects", "effect", "review"}


def fold(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def lookup(doi: str) -> dict | int | None:
    """CSL metadata, an HTTP status for an unregistered DOI, or None when the network is unavailable."""
    req = urllib.request.Request(f"https://doi.org/{doi}",
                                 headers={"Accept": "application/vnd.citationstyles.csl+json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code if e.code == 404 else None
    except (urllib.error.URLError, TimeoutError, ValueError):
        return None


def cites(csl: dict, context: str) -> bool:
    people = csl.get("author") or csl.get("editor") or []
    # Some registrars put "Surname, Given" in `family`.
    names = [fold(p.get("family") or p.get("literal") or "").split(",")[0].strip() for p in people[:3]]
    title = csl.get("title") or ""
    title = fold(title[0] if isinstance(title, list) and title else str(title))
    words = {w for w in re.findall(r"[a-z]{5,}", title) if w not in STOP}
    if not any(names) and not words:
        return True
    ctx = fold(context)
    # ...and some put the whole name there, so the last word counts too.
    return (any(n and (n in ctx or n.split()[-1] in ctx) for n in names)
            or sum(w in ctx for w in words) >= 2)


def describe(csl: dict) -> str:
    people = csl.get("author") or csl.get("editor") or []
    who = people[0].get("family") or people[0].get("literal") if people else "no author"
    title = csl.get("title") or ""
    title = title[0] if isinstance(title, list) and title else title
    year = (csl.get("issued", {}).get("date-parts") or [[None]])[0][0]
    return f"'{title}' ({who}, {year})"


def clean(doi: str) -> str:
    doi = doi.rstrip(".,;:*_")
    while doi.endswith(")") and doi.count(")") > doi.count("("):
        doi = doi[:-1].rstrip(".,;:*_")
    return doi


def check(path: Path) -> tuple[list[str], list[str]]:
    ok = set(CACHE.read_text().split()) if CACHE.exists() else set()
    lines = path.read_text().splitlines()
    bad, unchecked, seen = [], [], set()
    for i, line in enumerate(lines):
        for m in DOI.finditer(line):
            doi = clean(m.group(1))
            if doi in seen or doi in ok:
                continue
            seen.add(doi)
            csl = lookup(doi)
            if csl is None:
                unchecked.append(doi)
                continue
            if isinstance(csl, int):
                bad.append(f"{doi} does not resolve ({csl})")
            elif cites(csl, " ".join(lines[max(0, i - 1):i + 1])):
                ok.add(doi)
            else:
                bad.append(f"{doi} resolves to {describe(csl)}, which line {i + 1} does not name")
    CACHE.write_text("\n".join(sorted(ok)) + "\n")
    return bad, unchecked


def main() -> None:
    event = json.load(sys.stdin)
    file = event.get("tool_input", {}).get("file_path") or event.get("tool_response", {}).get("filePath") or ""
    path = Path(file)
    if path.suffix != ".md" or not path.is_file():
        return
    bad, unchecked = check(path)
    if bad:
        print(json.dumps({"decision": "block", "reason": f"DOI check in {path.name}: " + "; ".join(bad)
                          + ". Verify each against OpenAlex or the publisher, then fix or remove it."}))
    elif unchecked:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext":
              f"DOI check in {path.name} could not reach doi.org for {len(unchecked)} DOI(s): "
              + ", ".join(unchecked[:10]) + ". They are unverified, not clean."}}))


if __name__ == "__main__":
    main()
