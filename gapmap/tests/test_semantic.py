"""semantic.py: retrieval numbering, prompt building and the judge/parse/state rules (S1, fix 1
"the silent id-drop bug"). The judge often cites bare integers or numeric strings, which the
pre-fix code silently dropped as invalid, turning a real (unparsed) answer into `open` -- see
`docs/plans/n3-poc-lens-spec.md`'s Implementation notes for the incident counts this fixes."""
import pytest
from conftest import a_claim, ledger

from gapmap import link, record, semantic
from gapmap.judge import JudgeCacheMiss


def _retrieval():
    seed = a_claim("Systems must inspect the widget.", source_id="s1")
    other = a_claim("The widget inspection interval is documented.",
                    exact="A widget check finds a crack before failure.", source_id="s2")
    lg = ledger([seed, other])
    idx = link.build_index(lg)
    return semantic.retrieve(idx, frozenset({seed.claim_id}), frozenset({"widget", "check"}))


class _FixedJudge:
    model_id = "fixed"

    def __init__(self, response):
        self._response = response

    def ask(self, prompt):
        return self._response


def test_ids_are_a_single_bare_integer_scheme_not_a_or_s_prefixed():
    ret = _retrieval()
    ids = [i for i, _c, _s in (*ret.a_items, *ret.s_items)]
    assert ids == [str(i) for i in range(1, len(ids) + 1)]
    prompt = semantic.build_prompt("seed", "question?", ret)
    assert "A1:" not in prompt and "S1:" not in prompt
    assert f"{ids[0]}:" in prompt


def test_integer_id_response_closes():
    ret = _retrieval()
    first_id_str, first_cid, _sent = ret.a_items[0]
    judge = _FixedJudge({"states": [int(first_id_str)], "partially": [], "reason": "int id"})
    out = semantic.judge_retrieval(judge, ret, "seed", "question?")
    assert out.state == "closed"
    assert out.a_hits == (first_cid,)


def test_string_integer_id_response_closes():
    ret = _retrieval()
    first_id_str, first_cid, _sent = ret.a_items[0]
    judge = _FixedJudge({"states": [first_id_str], "partially": [], "reason": "string id"})
    out = semantic.judge_retrieval(judge, ret, "seed", "question?")
    assert out.state == "closed"
    assert out.a_hits == (first_cid,)


def test_unknown_id_is_undecided_never_open():
    ret = _retrieval()
    out_of_range = max(int(i) for i, _c, _s in (*ret.a_items, *ret.s_items)) + 50
    judge = _FixedJudge({"states": [out_of_range], "partially": [], "reason": "hallucinated id"})
    out = semantic.judge_retrieval(judge, ret, "seed", "question?")
    assert out.state == "undecided"
    assert out.state != "open"
    assert out.dropped_ids == 1


def test_malformed_json_is_undecided_never_open():
    # e.g. OllamaJudge's own sentinel (`None`) for a model reply that did not parse as JSON.
    ret = _retrieval()
    out = semantic.judge_retrieval(_FixedJudge(None), ret, "seed", "question?")
    assert out.state == "undecided"


def test_a_judge_that_raises_also_degrades_to_undecided_not_a_crash():
    class _RaisingJudge:
        model_id = "raises"

        def ask(self, prompt):
            raise ValueError("boom")

    ret = _retrieval()
    out = semantic.judge_retrieval(_RaisingJudge(), ret, "seed", "question?")
    assert out.state == "undecided"


def test_no_citations_at_all_is_a_genuine_open_not_undecided():
    ret = _retrieval()
    judge = _FixedJudge({"states": [], "partially": [], "reason": "nothing found"})
    out = semantic.judge_retrieval(judge, ret, "seed", "question?")
    assert out.state == "open"


def test_empty_retrieval_is_open_without_calling_the_judge_at_all():
    # Observed live in the S2 fair control's "other-source-only" arm: when nothing at all is
    # retrieved, the answer is unambiguously open -- asking anyway risked (and, live, produced) a
    # hallucinated citation against zero offered sentences, which would otherwise read as
    # `undecided` for a question that was never answerable any other way.
    empty = semantic.Retrieval(a_items=(), s_items=())

    class _ExplodingJudge:
        model_id = "should-not-be-called"

        def ask(self, prompt):
            raise AssertionError("the judge must not be asked about an empty retrieval")

    out = semantic.judge_retrieval(_ExplodingJudge(), empty, "seed", "question?")
    assert out.state == "open"


def test_judge_cache_miss_propagates_not_swallowed_as_undecided():
    class _MissJudge:
        model_id = "miss"

        def ask(self, prompt):
            raise JudgeCacheMiss("no cache")

    ret = _retrieval()
    with pytest.raises(JudgeCacheMiss):
        semantic.judge_retrieval(_MissJudge(), ret, "seed", "question?")


def test_categorize_routes_undecided_to_rg_undecided_not_a_hypothesis():
    assert record.categorize("undecided", k_topic=5) == "RG-UNDECIDED"
