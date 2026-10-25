"""DS5 snapshot of OpenRouter list prices for open-weight shortlist candidates.
    python3 -I openrouter_snapshot.py   # writes openrouter_snapshot.json
"""
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

PATTERN = re.compile(r"^(allenai/|meta-llama/llama-(3\.1|3\.3|4)|google/gemma-(3|4)|microsoft/phi-4|"
                     r"openai/gpt-oss|mistralai/mistral-small|qwen/qwen(-2\.5|3)|deepseek/)")


def main():
    req = urllib.request.Request("https://openrouter.ai/api/v1/models", headers={"User-Agent": "ds5"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)["data"]
    rows = []
    for m in data:
        if not PATTERN.match(m["id"]) or m["id"].endswith(":free"):
            continue
        p = m.get("pricing", {})
        rows.append({"id": m["id"], "usd_per_mtok_in": round(float(p.get("prompt", 0)) * 1e6, 4),
                     "usd_per_mtok_out": round(float(p.get("completion", 0)) * 1e6, 4),
                     "context_length": m.get("context_length"),
                     "openrouter_knowledge_cutoff": m.get("knowledge_cutoff")})
    rows.sort(key=lambda r: r["id"])
    doc = {"retrieved": datetime.now(timezone.utc).isoformat(timespec="minutes"),
           "source": "https://openrouter.ai/api/v1/models",
           "note": "openrouter_knowledge_cutoff is aggregator metadata, not a publisher statement",
           "models": rows}
    Path(__file__).with_suffix(".json").write_text(json.dumps(doc, indent=1) + "\n")
    print(len(rows))
    for r in rows:
        print(r["id"], r["usd_per_mtok_in"], r["usd_per_mtok_out"], r["openrouter_knowledge_cutoff"])


if __name__ == "__main__":
    main()
