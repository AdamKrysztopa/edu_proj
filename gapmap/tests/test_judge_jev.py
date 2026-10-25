"""jev.py JevJudge (I2): Jev answers one three-way question per sentence through OpenRouter's
Decisions API; the judge turns its top choices into control2's JSON-reply contract. Cache first
(the spike's raw cache, then this run's), live only for misses, a miss on a prompt the old
control issued is a bug, and a hard USD cap is checked before every call. No test opens a socket."""
import hashlib
import json

import pytest

from gapmap import jev, judge as judge_mod, semantic

PROMPT = semantic.build_prompt(
    "Cables should be selected based on noise.", "Does any sentence state a condition?",
    semantic.Retrieval(a_items=(("1", "c1", "Choose a shielded cable near a drive."),
                                ("2", "c2", "Noise was logged."),
                                ("3", "c3", "Cables are long.")), s_items=()))


class FakePost:
    def __init__(self, choices=("states", "no", "partially"), cost=7e-05, drop=()):
        self.choices, self.cost, self.drop = choices, cost, drop
        self.bodies = []

    def __call__(self, url, body, headers):
        self.bodies.append(body)
        answers = {f"s{n}": {"type": "choice", "choice": c, "probabilities": {c: 0.6}}
                   for n, c in enumerate(self.choices, start=1) if f"s{n}" not in self.drop}
        return {"model": "typesafe/jev-1.13-20260917", "answers": answers,
                "usage": {"input_tokens": 1000, "output_tokens": 300, "cost": self.cost}}


def _judge(tmp_path, post, max_usd=0.10, **kw):
    return jev.JevJudge(max_usd=max_usd, post=post, cache_dir=tmp_path / "raw",
                        spend_ledger=tmp_path / "spend.jsonl", **kw)


def test_the_request_is_the_spike_body_one_choice_question_per_sentence():
    body = jev.request_body(PROMPT)
    assert body["model"] == "typesafe/jev-1.13"
    assert body["state"] == {"seed_assertion": "Cables should be selected based on noise.",
                             "sentences": {"1": "Choose a shielded cable near a drive.", "2": "Noise was logged.",
                                           "3": "Cables are long."}}
    assert sorted(body["questions"]) == ["s1", "s2", "s3"]
    q = body["questions"]["s2"]
    assert q["type"] == "choice" and q["criteria"] == jev.LEVELS
    assert q["instructions"] == ("Question about the seed assertion: Does any sentence state a condition? "
                                 'Does sentences["2"] state the element this question asks for?')


def test_the_cache_key_is_the_spikes():
    body = jev.request_body(PROMPT)
    assert jev.body_key(body) == hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()


def test_top_choices_become_the_states_and_partially_lists():
    reply = _judge_reply(("states", "no", "partially"))
    assert reply == {"states": ["1"], "partially": ["3"], "reason": "jev top choices"}


def _judge_reply(choices):
    return jev.to_reply({"answers": {f"s{n}": {"choice": c} for n, c in enumerate(choices, start=1)}},
                        jev.request_body(PROMPT))


@pytest.mark.parametrize("choices,state", [(("states", "no", "no"), "closed"),
                                           (("partially", "states", "no"), "closed"),
                                           (("no", "partially", "no"), "partial"),
                                           (("no", "no", "no"), "open")])
def test_arm_state_closed_iff_a_states_top_choice_partial_iff_none_and_a_partially(tmp_path, choices, state):
    j = _judge(tmp_path, FakePost(choices=choices))
    retrieval = semantic.Retrieval(a_items=tuple((str(n), f"c{n}", f"sentence {n}") for n in (1, 2, 3)),
                                   s_items=())
    out = semantic.judge_retrieval(j, retrieval, "seed", "q?")
    assert out.state == state


def test_a_missing_choice_is_unparseable_and_degrades_to_undecided(tmp_path):
    assert _judge(tmp_path, FakePost(drop=("s2",))).ask(PROMPT) is None


def test_a_spike_cache_hit_never_dispatches(tmp_path):
    prior = tmp_path / "spike"
    prior.mkdir()
    body = jev.request_body(PROMPT)
    resp = FakePost(choices=("no", "states", "no"))(None, body, None)
    (prior / f"{jev.body_key(body)}.json").write_text(json.dumps({"request": body, "response": resp}))
    post = FakePost()
    j = _judge(tmp_path, post, prior_cache_dirs=(prior,))
    assert j.ask(PROMPT)["states"] == ["2"]
    assert post.bodies == [] and j.calls == [] and j.cache_hits == 1


def test_a_miss_on_a_prompt_the_old_control_issued_is_a_bug_and_never_dispatches(tmp_path):
    post = FakePost()
    j = _judge(tmp_path, post, issued_prompt_sha256s={hashlib.sha256(PROMPT.encode()).hexdigest()})
    with pytest.raises(jev.IssuedPromptMiss):
        j.ask(PROMPT)
    assert post.bodies == []
    assert issubclass(jev.IssuedPromptMiss, judge_mod.JudgeCacheMiss)


def test_a_live_call_is_cached_raw_and_charged_to_the_ledger(tmp_path):
    post = FakePost(cost=8e-05)
    j = _judge(tmp_path, post)
    j.ask(PROMPT)
    key = jev.body_key(jev.request_body(PROMPT))
    raw = json.loads((tmp_path / "raw" / f"{key}.json").read_text())
    assert raw["request"] == post.bodies[0] and raw["response"]["usage"]["cost"] == 8e-05
    line = json.loads((tmp_path / "spend.jsonl").read_text())
    assert line["usd"] == 8e-05 and line["body_sha256"] == key
    assert j.spend()["usd"] == pytest.approx(8e-05) and j.spend()["calls"] == 1
    _judge(tmp_path, post).ask(PROMPT)
    assert len(post.bodies) == 1


def test_the_cap_is_checked_before_the_call_and_counts_the_ledgers_prior_spend(tmp_path):
    (tmp_path / "spend.jsonl").write_text(json.dumps({"usd": 0.09999}) + "\n")
    post = FakePost()
    j = _judge(tmp_path, post)
    with pytest.raises(judge_mod.BudgetExceeded):
        j.ask(PROMPT)
    assert post.bodies == []


def test_a_response_without_a_cost_stops_the_run(tmp_path):
    class NoCost(FakePost):
        def __call__(self, url, body, headers):
            r = super().__call__(url, body, headers)
            del r["usage"]["cost"]
            return r
    with pytest.raises(jev.UnaccountedCall):
        _judge(tmp_path, NoCost()).ask(PROMPT)


def test_a_sentence_holding_a_newline_stays_one_sentence():
    prompt = semantic.build_prompt("s", "q?", semantic.Retrieval(
        a_items=(("1", "c1", "line one\nline two"), ("2", "c2", "other")), s_items=()))
    assert jev.request_body(prompt)["state"]["sentences"] == {"1": "line one\nline two", "2": "other"}
