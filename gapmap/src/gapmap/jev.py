"""I2: Jev (`typesafe/jev-1.13`, OpenRouter's Decisions API) as a closure judge for control2.

Jev answers one three-way choice per sentence; it cannot share control2's prompt and parser, so
it is never ADR 0009's guard arm, only a substitute candidate. `request_body` rebuilds the JEV
spike's body (`research/spikes/jev/judge_swap.py`) from a control2 prompt, byte for byte, so the
spike's raw cache answers every prompt it already sent. `to_reply` maps Jev's top choices onto
the `{"states", "partially"}` contract, so an arm is closed iff a sentence's top choice is
'states', partial iff none is and one is 'partially', else open."""
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

from gapmap.judge import BudgetExceeded, JudgeCacheMiss, _http_post

MODEL = "typesafe/jev-1.13"
URL = "https://openrouter.ai/api/alpha/decisions"
# Every spike call cost input_tokens x $0.042/M with input_tokens <= 0.55 x body chars, so one
# token per body character bounds a call's cost.
PRICE_PER_M_INPUT = 0.042
LEVELS = {
    "states": "The sentence explicitly states the element the question asks for.",
    "partially": "The sentence states part of the element, or states it only implicitly.",
    "no": "The sentence does not state the element; being on the same topic is not enough.",
}


class IssuedPromptMiss(JudgeCacheMiss):
    """The spike's cache holds every prompt the old control issued; missing one means the body
    changed, and a live call would silently re-judge it."""


class UnaccountedCall(RuntimeError):
    """A response without `usage.cost` cannot be charged against the cap."""


def parse_prompt(prompt: str) -> tuple[str, str, dict[str, str]]:
    seed = re.search(r'^Seed assertion: "(.*)"$', prompt, re.M).group(1)
    question = re.search(r"^Question: (.*)$", prompt, re.M).group(1)
    body = prompt.split("\nSentences:\n", 1)[1].split("\n\nRespond as JSON only", 1)[0]
    sents: dict[str, str] = {}
    for line in body.split("\n"):
        m = re.match(r"^(\d+): (.*)$", line)
        if m:
            sents[m.group(1)] = m.group(2)
        elif sents:
            last = next(reversed(sents))
            sents[last] += "\n" + line
    return seed, question, sents


def request_body(prompt: str) -> dict:
    seed, question, sents = parse_prompt(prompt)
    questions = {f"s{i}": {"type": "choice",
                           "instructions": (f"Question about the seed assertion: {question} "
                                            f"Does sentences[\"{i}\"] state the element this question asks for?"),
                           "criteria": LEVELS}
                 for i in sents}
    return {"model": MODEL, "state": {"seed_assertion": seed, "sentences": sents}, "questions": questions}


def body_key(body: dict) -> str:
    return hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()


def to_reply(response: dict, body: dict) -> dict | None:
    answers = response.get("answers") or {}
    choices = {qid[1:]: (answers.get(qid) or {}).get("choice") for qid in body["questions"]}
    if any(c not in LEVELS for c in choices.values()):
        return None
    pick = lambda level: sorted((i for i, c in choices.items() if c == level), key=int)  # noqa: E731
    return {"states": pick("states"), "partially": pick("partially"), "reason": "jev top choices"}


class JevJudge:
    """Cache first: `prior_cache_dirs`, then `cache_dir` (raw `{request, response}` files keyed by
    `body_key`); live only for a miss, after checking the cap against the ledger's prior spend,
    this judge's spend and the call's worst case."""

    model_id = MODEL

    def __init__(self, *, max_usd: float, cache_dir: Path | str, spend_ledger: Path | str,
                 prior_cache_dirs=(), issued_prompt_sha256s=frozenset(), live: bool = True, post=None):
        self.max_usd = max_usd
        self.cache_dir = Path(cache_dir)
        self.prior_cache_dirs = tuple(Path(d) for d in prior_cache_dirs)
        self.issued = frozenset(issued_prompt_sha256s)
        self.live = live
        self.spend_ledger = Path(spend_ledger)
        self.prior_usd = (sum(json.loads(line)["usd"] for line in self.spend_ledger.read_text().splitlines()
                              if line.strip()) if self.spend_ledger.exists() else 0.0)
        self._post = post
        self.spent_usd = 0.0
        self.calls: list[dict] = []
        self.cache_hits = 0

    def _cached(self, key: str) -> dict | None:
        for d in (*self.prior_cache_dirs, self.cache_dir):
            f = d / f"{key}.json"
            if f.exists():
                return json.loads(f.read_text())["response"]
        return None

    def ask(self, prompt: str) -> dict | None:
        body = request_body(prompt)
        key = body_key(body)
        response = self._cached(key)
        if response is not None:
            self.cache_hits += 1
            return to_reply(response, body)
        if hashlib.sha256(prompt.encode()).hexdigest() in self.issued:
            raise IssuedPromptMiss(f"the old control issued this prompt, but no cache holds Jev body {key[:12]}...")
        if not self.live:
            raise JudgeCacheMiss(f"no cached Jev response for body {key[:12]}...")
        worst = len(json.dumps(body)) * PRICE_PER_M_INPUT / 1e6
        if self.prior_usd + self.spent_usd + worst > self.max_usd:
            raise BudgetExceeded(f"spent ${self.prior_usd + self.spent_usd:.5f}; the next call could cost "
                                 f"${worst:.5f} against a ${self.max_usd:.4f} cap; refusing it")
        post = self._post or _http_post
        response = post(URL, body, {"Content-Type": "application/json",
                                    "Authorization": "Bearer " + os.environ.get("OPENROUTER_API_KEY", "")})
        cost = (response.get("usage") or {}).get("cost")
        if not isinstance(cost, (int, float)):
            raise UnaccountedCall(f"Jev response for body {key[:12]}... carries no usage.cost")
        self.spent_usd += cost
        call = {"body_sha256": key, "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                "served_model": response.get("model"), "usd": cost,
                "input_tokens": response["usage"].get("input_tokens", 0)}
        self.calls.append(call)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        (self.cache_dir / f"{key}.json").write_text(json.dumps({"request": body, "response": response},
                                                               indent=1, sort_keys=True) + "\n")
        with self.spend_ledger.open("a") as f:
            f.write(json.dumps(call, sort_keys=True) + "\n")
        return to_reply(response, body)

    def spend(self) -> dict:
        return {"usd": self.spent_usd, "max_usd": self.max_usd, "prior_usd": self.prior_usd,
                "calls": len(self.calls), "cache_hits": self.cache_hits,
                "input_tokens": sum(c["input_tokens"] for c in self.calls),
                "served_models": sorted({str(c["served_model"]) for c in self.calls})}
