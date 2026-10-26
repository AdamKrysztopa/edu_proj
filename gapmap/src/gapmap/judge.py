"""S1: the semantic closure judge (local, $0). `Judge` is anything answerable with one JSON-in,
JSON-out call; `OllamaJudge` talks to a local Ollama server over stdlib `urllib` only (`gapmap`
imports no HTTP library, per the architecture test); `CachedJudge` wraps any judge with a JSON
cache file keyed by sha256(model id, prompt), so a run is replayable byte-identically without the
network. Different family from the extractor (anthropic) and verifier (openai) per the spec."""
from __future__ import annotations

import hashlib
import json
import os
import urllib.request
from pathlib import Path
from typing import Protocol

from gapmap import config


class Judge(Protocol):
    model_id: str

    def ask(self, prompt: str) -> dict: ...


class JudgeCacheMiss(RuntimeError):
    """Replay mode (the default) never opens the network; a live flag (--judge ollama, or
    --judge openai in control2) fills the cache."""


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


OPENAI_URL = "https://api.openai.com/v1/chat/completions"
# USD per 1M (input, output) tokens; reasoning tokens bill as output. Spend charges every prompt
# token at the full input price, an upper bound when part of the prompt is cached.
# platform.openai.com/docs/models/gpt-5.6-luna, read 2026-10-24;
# platform.openai.com/docs/models/gpt-6.1-sol (served at developers.openai.com/api/docs/models/), read 2026-10-24.
OPENAI_PRICES_PER_MTOK = {"gpt-5.6-luna": (0.20, 1.20), "gpt-6.1-sol": (2.0, 10.0)}
OPENAI_CACHED_INPUT_PER_MTOK = {"gpt-6.1-sol": 0.10}


def family(model_id: str) -> str:
    """Vendor family, comparable with a sidecar's `config.models.*.family`."""
    if model_id in OPENAI_PRICES_PER_MTOK or model_id.startswith(("gpt-", "openai/")):
        return "openai"
    if model_id.startswith(("claude", "anthropic/")):
        return "anthropic"
    return "other"


class BudgetExceeded(JudgeCacheMiss):
    """A JudgeCacheMiss so that `semantic.judge_retrieval` re-raises it: every other exception there
    degrades to `undecided`, and a refused call must stop the run, not become a judgement."""


def _http_post(url: str, body: dict, headers: dict) -> dict:
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=300) as resp:
        return json.loads(resp.read())


class OpenAIJudge:
    """OpenAI Chat Completions in JSON mode. Before every call the cap is checked against the
    spend so far plus the call's worst case (prompt at 2 chars/token, a full `max_completion_tokens`
    reply), so the reported spend can never pass `max_usd`. With `spend_ledger`, a JSONL of every
    call shared by several runs, the cap covers the ledger's prior spend too, and each call is
    appended to it as soon as it returns."""

    PRICES = OPENAI_PRICES_PER_MTOK
    URL = OPENAI_URL
    KEY_ENV = "OPENAI_API_KEY"

    def __init__(self, model: str, *, max_usd: float, reasoning_effort: str = "medium",
                 max_completion_tokens: int = 6000, post=None, spend_ledger: Path | str | None = None):
        if model not in self.PRICES:
            raise ValueError(f"no recorded price for {model!r}")
        self.model_id = model
        self.max_usd = max_usd
        self.spend_ledger = Path(spend_ledger) if spend_ledger else None
        self.prior_usd = (sum(json.loads(line)["usd"] for line in self.spend_ledger.read_text().splitlines()
                              if line.strip())
                          if self.spend_ledger and self.spend_ledger.exists() else 0.0)
        self.max_completion_tokens = max_completion_tokens
        self.settings = self._settings(reasoning_effort, max_completion_tokens)
        self._post = post
        self.spent_usd = 0.0
        self.calls: list[dict] = []
        self.incomplete = False

    def _settings(self, reasoning_effort: str | None, max_completion_tokens: int) -> dict:
        return {"api": self.URL, "reasoning_effort": reasoning_effort,
                "max_completion_tokens": max_completion_tokens,
                "response_format": "json_object", "temperature": "not sent",
                "price_usd_per_mtok": list(self.PRICES[self.model_id])}

    def _body(self, prompt: str) -> dict:
        return {"model": self.model_id, "messages": [{"role": "user", "content": prompt}],
                "response_format": {"type": "json_object"},
                "reasoning_effort": self.settings["reasoning_effort"],
                "max_completion_tokens": self.settings["max_completion_tokens"]}

    def _billed(self, usage: dict, prompt_tokens: int, completion_tokens: int) -> float:
        return self._cost(prompt_tokens, completion_tokens)

    def _cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        pin, pout = self.PRICES[self.model_id]
        return (prompt_tokens * pin + completion_tokens * pout) / 1e6

    def ask(self, prompt: str) -> dict | None:
        worst = self._cost(len(prompt) // 2 + 50, self.max_completion_tokens)
        if self.prior_usd + self.spent_usd + worst > self.max_usd:
            self.incomplete = True
            raise BudgetExceeded(f"spent ${self.prior_usd + self.spent_usd:.4f}; the next call could cost ${worst:.4f} "
                                 f"against a ${self.max_usd:.4f} cap; refusing it")
        post = self._post or _http_post
        payload = post(self.URL, self._body(prompt), {"Content-Type": "application/json",
                                                      "Authorization": "Bearer " + os.environ[self.KEY_ENV]})
        usage = payload.get("usage") or {}
        p_tok, c_tok = usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0)
        cost = self._billed(usage, p_tok, c_tok)
        self.spent_usd += cost
        choice = (payload.get("choices") or [{}])[0]
        call = {"prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                "served_model": payload.get("model"), "finish_reason": choice.get("finish_reason"),
                "prompt_tokens": p_tok, "completion_tokens": c_tok,
                "cached_tokens": (usage.get("prompt_tokens_details") or {}).get("cached_tokens", 0),
                "reasoning_tokens": (usage.get("completion_tokens_details") or {}).get("reasoning_tokens", 0),
                "usd": cost}
        self.calls.append(call)
        if self.spend_ledger:
            with self.spend_ledger.open("a") as f:
                f.write(json.dumps({"model": self.model_id, **call}, sort_keys=True) + "\n")
        content = (choice.get("message") or {}).get("content")
        try:
            parsed = json.loads(content) if content else None
        except json.JSONDecodeError:
            return None
        return parsed if isinstance(parsed, dict) else None

    def spend(self) -> dict:
        return {"usd": self.spent_usd, "max_usd": self.max_usd, "prior_usd": self.prior_usd,
                "calls": len(self.calls),
                "cached_tokens": sum(c["cached_tokens"] for c in self.calls),
                "prompt_tokens": sum(c["prompt_tokens"] for c in self.calls),
                "completion_tokens": sum(c["completion_tokens"] for c in self.calls),
                "reasoning_tokens": sum(c["reasoning_tokens"] for c in self.calls),
                "served_models": sorted({str(c["served_model"]) for c in self.calls}),
                "finish_reasons": {r: sum(c["finish_reason"] == r for c in self.calls)
                                   for r in sorted({str(c["finish_reason"]) for c in self.calls})}}


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
# USD per 1M (input, output) tokens, from https://openrouter.ai/api/v1/models, read 2026-10-26. The
# cap's worst case uses these; the spend uses the cost OpenRouter reports for the call when present.
OPENROUTER_PRICES_PER_MTOK = {
    "google/gemini-3.5-flash-lite": (0.30, 2.50),
    "deepseek/deepseek-v4.1-flash": (0.02, 1.00),
    "qwen/qwen3.8-flash": (0.15, 0.47),
    "mistralai/mistral-small-2603": (0.15, 0.60),
}


class OpenRouterJudge(OpenAIJudge):
    """A non-OpenAI judge through OpenRouter's chat completions, with `OpenAIJudge`'s cap, ledger and
    reply contract; temperature 0, no reasoning setting."""

    PRICES = OPENROUTER_PRICES_PER_MTOK
    URL = OPENROUTER_URL
    KEY_ENV = "OPENROUTER_API_KEY"

    def __init__(self, model: str, *, max_usd: float, max_completion_tokens: int = 2000, post=None,
                 spend_ledger: Path | str | None = None):
        super().__init__(model, max_usd=max_usd, reasoning_effort=None,
                         max_completion_tokens=max_completion_tokens, post=post, spend_ledger=spend_ledger)

    def _settings(self, reasoning_effort: str | None, max_completion_tokens: int) -> dict:
        return {"api": self.URL, "max_tokens": max_completion_tokens, "response_format": "json_object",
                "temperature": 0, "price_usd_per_mtok": list(self.PRICES[self.model_id])}

    def _body(self, prompt: str) -> dict:
        return {"model": self.model_id, "messages": [{"role": "user", "content": prompt}],
                "response_format": {"type": "json_object"}, "temperature": 0,
                "max_tokens": self.settings["max_tokens"], "usage": {"include": True}}

    def _billed(self, usage: dict, prompt_tokens: int, completion_tokens: int) -> float:
        cost = usage.get("cost")
        return float(cost) if cost is not None else self._cost(prompt_tokens, completion_tokens)


class CachedJudge:
    """Replay mode (`live=False`, the default): cache-only, never touches the network -- a miss
    raises `JudgeCacheMiss` naming `live_flag`, the flag that would fill it. Live mode (`live=True`): fills the cache.
    Cache file: `<out>/closure_judgements.json`, committed with a run's outputs so anyone can
    replay it byte-identically. `meta` (the judge's settings) is stored under `_meta`, and a cache
    filled under other settings is refused."""

    def __init__(self, judge: Judge, cache_path: Path | str, *, live: bool = False,
                 meta: dict | None = None, live_flag: str = "--judge ollama"):
        self.judge = judge
        self.live_flag = live_flag
        self.model_id = judge.model_id
        self.cache_path = Path(cache_path)
        self.live = live
        self._cache: dict[str, dict] = (json.loads(self.cache_path.read_text())
                                        if self.cache_path.exists() else {})
        self._dirty = False
        if meta is not None:
            if self._cache.setdefault("_meta", meta) != meta:
                raise ValueError(f"{self.cache_path} was filled under {self._cache['_meta']}, not {meta}")

    def ask(self, prompt: str) -> dict:
        key = cache_key(self.model_id, prompt)
        if key in self._cache:
            return self._cache[key]
        if not self.live:
            raise JudgeCacheMiss(
                f"no cached judgement for prompt {key[:12]}... in {self.cache_path}; "
                f"pass {self.live_flag} to fill the cache.")
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
