"""S1: the semantic closure judge (local, $0). `Judge` is anything answerable with one JSON-in,
JSON-out call; `OllamaJudge` talks to a local Ollama server over stdlib `urllib` only (`gapmap`
imports no HTTP library, per the architecture test); `CachedJudge` wraps any judge with a JSON
cache file keyed by sha256(model id, prompt), so a run is replayable byte-identically without the
network. Different family from the extractor (anthropic) and verifier (openai) per the spec."""
from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path
from typing import Protocol

from gapmap import config


class Judge(Protocol):
    model_id: str

    def ask(self, prompt: str) -> dict: ...


class JudgeCacheMiss(RuntimeError):
    """Replay mode (the default) never opens the network; pass --judge ollama to fill the cache."""


def cache_key(model_id: str, prompt: str) -> str:
    return hashlib.sha256(f"{model_id}\x1f{prompt}".encode()).hexdigest()


class OllamaJudge:
    """`format: "json"`, `options: {temperature: 0, seed: 0}` (spec S1)."""

    def __init__(self, url: str = config.JUDGE_URL, model: str = config.JUDGE_MODEL):
        self.url = url
        self.model_id = model

    def ask(self, prompt: str) -> dict | None:
        """Fix 1: a network or transport failure (bad URL, timeout, non-2xx, an unparseable HTTP
        envelope) still raises -- that is a real infrastructure failure, not a judge answer. But
        the MODEL's own reply, `payload["message"]["content"]`, is free text the model was asked
        to shape as JSON; when it fails to (or returns something that parses but isn't a JSON
        object), that is exactly the "malformed JSON" case `semantic.judge_retrieval` must turn
        into `undecided` rather than crash on -- so this returns `None` (cacheable, unlike an
        exception) instead of letting `json.JSONDecodeError` propagate."""
        body = json.dumps({
            "model": self.model_id,
            "messages": [{"role": "user", "content": prompt}],
            "format": "json",
            "stream": False,
            "options": {"temperature": 0, "seed": 0},
        }).encode()
        req = urllib.request.Request(self.url, data=body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=180) as resp:
            payload = json.loads(resp.read())
        try:
            parsed = json.loads(payload["message"]["content"])
        except json.JSONDecodeError:
            return None
        return parsed if isinstance(parsed, dict) else None


class CachedJudge:
    """Replay mode (`live=False`, the default): cache-only, never touches the network -- a miss
    raises `JudgeCacheMiss` naming `--judge ollama`. Live mode (`live=True`): fills the cache.
    Cache file: `<out>/closure_judgements.json`, committed with a run's outputs so anyone can
    replay it byte-identically."""

    def __init__(self, judge: Judge, cache_path: Path | str, *, live: bool = False):
        self.judge = judge
        self.model_id = judge.model_id
        self.cache_path = Path(cache_path)
        self.live = live
        self._cache: dict[str, dict] = (json.loads(self.cache_path.read_text())
                                        if self.cache_path.exists() else {})
        self._dirty = False

    def ask(self, prompt: str) -> dict:
        key = cache_key(self.model_id, prompt)
        if key in self._cache:
            return self._cache[key]
        if not self.live:
            raise JudgeCacheMiss(
                f"no cached judgement for prompt {key[:12]}... in {self.cache_path}; "
                f"pass --judge ollama to fill the cache.")
        result = self.judge.ask(prompt)
        self._cache[key] = result
        self._dirty = True
        return result

    def save(self) -> None:
        if not self._dirty:
            return
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.write_text(json.dumps(self._cache, sort_keys=True, indent=1) + "\n")
        self._dirty = False
