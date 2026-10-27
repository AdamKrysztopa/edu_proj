import json

import g1_retest


def test_counts_only_when_both_pass_with_identical_results():
    first = json.loads(g1_retest.FIRST.read_text())
    assert g1_retest.compare(first, first)["counts"]
    other = dict(first, topics={**first["topics"], "x": 1})
    assert not g1_retest.compare(first, other)["counts"]
    assert not g1_retest.compare(first, dict(first, eligible=False))["counts"]
