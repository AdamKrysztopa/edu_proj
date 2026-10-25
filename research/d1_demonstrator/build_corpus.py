"""Build the D1 local corpus: 16 public, user-facing docs of dependence-forecastability at a
pinned commit, plus 10 outside pages on the same methods (owner, 2026-10-25: one repository is one
independence key, so without them no gap can reach k_topic >= 2). Everything is wrapped as HTML
(reconstruct.web.fetch accepts HTML only), content-addressed, in reconstruct.corpus manifest shape.
Outside pages are reduced to their article text, since navigation would fill --max-doc-chars."""
from __future__ import annotations

import hashlib
import html
import urllib.parse
import urllib.request
from html.parser import HTMLParser
import json
import re
import subprocess
import sys
import time
import urllib.error
from pathlib import Path

HERE = Path(__file__).parent
SOURCE = HERE / "source"
REPO = "https://github.com/AdamKrysztopa/dependence-forecastability"

DOCS = [
    "README.md",
    "llms.txt",
    "docs/quickstart.md",
    "docs/why_use_this.md",
    "docs/how-to/golden_path.md",
    "docs/theory/foundations.md",
    "docs/theory/forecastability_profile.md",
    "docs/theory/pami_residual_backends.md",
    "docs/theory/lagged_exogenous_triage.md",
    "docs/explanation/architecture.md",
    "docs/explanation/limitations.md",
    "docs/explanation/results_summary.md",
    "docs/explanation/surface_guide.md",
    "docs/reference/diagnostics_matrix.md",
    "docs/code/module_map.md",
    "docs/medium/forecastability-triage-for-practitioners.md",
]

WIKIPEDIA = ["Mutual_information", "Autocorrelation", "Partial_autocorrelation_function",
             "Transfer_entropy", "Surrogate_data_testing", "Forecasting"]
SPHINX = [
    "https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.mutual_info_regression.html",
    "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html",
    "https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.ccf.html",
    "https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html",
]
UA = {"User-Agent": "edu-proj-d1/0.1 (research corpus)"}


def _get(url: str) -> bytes:
    for attempt in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 4:
                raise
            time.sleep(10 * (attempt + 1))


def wikipedia_markdown(title: str) -> tuple[str, bytes]:
    api = ("https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&explaintext=1"
           "&redirects=1&titles=" + urllib.parse.quote(title))
    raw = _get(api)
    page = next(iter(json.loads(raw)["query"]["pages"].values()))
    text = re.sub(r"^(=+)\s*(.*?)\s*=+$", lambda m: "#" * len(m.group(1)) + " " + m.group(2),
                  page["extract"], flags=re.M)
    return f"# {page['title']}\n\n{text}", raw


class _Article(HTMLParser):
    """Text of block elements inside the first <article>, as markdown-ish lines."""
    BLOCKS = {"p", "h1", "h2", "h3", "h4", "li", "dt", "dd", "pre"}
    SKIP = {"script", "style", "nav", "button"}

    def __init__(self) -> None:
        super().__init__()
        self.depth, self.skip, self.block, self.buf, self.lines = 0, 0, None, [], []

    def handle_starttag(self, tag, attrs):
        if tag == "article":
            self.depth += 1
        elif self.depth and tag in self.SKIP:
            self.skip += 1
        elif self.depth and tag in self.BLOCKS and self.block is None:
            self.block, self.buf = tag, []

    def handle_endtag(self, tag):
        if tag == "article" and self.depth:
            self.depth -= 1
        elif self.depth and tag in self.SKIP and self.skip:
            self.skip -= 1
        elif tag == self.block:
            text = " ".join("".join(self.buf).split())
            if text:
                prefix = "#" * int(tag[1]) + " " if tag[0] == "h" and tag[1:].isdigit() else ""
                self.lines.append(prefix + text.replace("¶", "").rstrip("#").strip())
            self.block = None

    def handle_data(self, data):
        if self.depth and self.block and not self.skip:
            self.buf.append(data)


def sphinx_markdown(url: str) -> tuple[str, bytes]:
    raw = _get(url)
    parser = _Article()
    parser.feed(raw.decode("utf-8", "replace"))
    return "\n\n".join(parser.lines), raw


def md_to_html(text: str, title: str) -> str:
    out, para, in_code = [], [], False

    def flush() -> None:
        if para:
            out.append("<p>" + html.escape(" ".join(para)) + "</p>")
            para.clear()

    for line in text.splitlines():
        if line.strip().startswith("```"):
            flush()
            out.append("</pre>" if in_code else "<pre>")
            in_code = not in_code
            continue
        if in_code:
            out.append(html.escape(line))
            continue
        stripped = line.strip()
        if stripped.startswith("#"):
            flush()
            level = min(len(stripped) - len(stripped.lstrip("#")), 6)
            out.append(f"<h{level}>{html.escape(stripped.lstrip('#').strip())}</h{level}>")
        elif not stripped:
            flush()
        else:
            para.append(stripped)
    flush()
    if in_code:
        out.append("</pre>")
    body = "\n".join(out)
    return (f"<!doctype html><html><head><meta charset='utf-8'><title>{html.escape(title)}</title>"
            f"</head><body>\n{body}\n</body></html>\n")


def main() -> int:
    commit = subprocess.run(["git", "-C", str(SOURCE), "rev-parse", "HEAD"],
                            capture_output=True, text=True, check=True).stdout.strip()
    files_dir = HERE / "corpus" / "files"
    files_dir.mkdir(parents=True, exist_ok=True)
    documents, inventory = [], []
    for rel in DOCS:
        text = (SOURCE / rel).read_text(encoding="utf-8")
        title = next((ln.lstrip("#").strip() for ln in text.splitlines() if ln.startswith("#")), rel)
        page = md_to_html(text, title).encode("utf-8")
        digest = hashlib.sha256(page).hexdigest()
        (files_dir / f"{digest}.html").write_bytes(page)
        documents.append({"url": f"{REPO}/blob/{commit}/{rel}", "content_type": "text/html; charset=utf-8",
                          "file": f"files/{digest}.html", "title": title})
        inventory.append({"path": rel, "source_bytes": len(text.encode("utf-8")), "html_sha256": digest})
    outside = [(f"https://en.wikipedia.org/wiki/{t}", *wikipedia_markdown(t)) for t in WIKIPEDIA]
    outside += [(u, *sphinx_markdown(u)) for u in SPHINX]
    for url, text, raw in outside:
        title = next((ln.lstrip("#").strip() for ln in text.splitlines() if ln.startswith("#")), url)
        page = md_to_html(text, title).encode("utf-8")
        digest = hashlib.sha256(page).hexdigest()
        (files_dir / f"{digest}.html").write_bytes(page)
        documents.append({"url": url, "content_type": "text/html; charset=utf-8",
                          "file": f"files/{digest}.html", "title": title})
        inventory.append({"url": url, "outside": True, "raw_sha256": hashlib.sha256(raw).hexdigest(),
                          "source_bytes": len(text.encode("utf-8")), "html_sha256": digest})
    (HERE / "corpus" / "manifest.json").write_text(
        json.dumps({"commit": commit, "repo": REPO, "documents": documents}, indent=1) + "\n")
    (HERE / "corpus" / "inventory.json").write_text(
        json.dumps({"commit": commit, "documents": inventory,
                    "total_source_bytes": sum(d["source_bytes"] for d in inventory)}, indent=1) + "\n")
    print(commit, len(documents), sum(d["source_bytes"] for d in inventory))
    return 0


if __name__ == "__main__":
    sys.exit(main())
