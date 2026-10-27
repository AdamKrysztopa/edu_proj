"""Topic selection (plan §1.3): seeded, one pair per seed cluster, lens quotas, no judge state."""
from types import SimpleNamespace

import select_topics as sel


def _spec(lens, seed, k=8):
    return SimpleNamespace(lens=lens, seeds=(seed,), k=k)


def test_one_pair_per_cluster_lens_quotas_and_a_reserve_in_shuffle_order():
    specs = [_spec("WHY", f"w{i}") for i in range(5)] + [_spec("SEL", "s0"), _spec("SEL", "s0"), _spec("SEL", "s1")]
    chosen, reserve = sel.pick(specs, {"WHY": 2, "SEL": 2}, seed=1)
    assert [s.lens for s in chosen].count("WHY") == 2 and [s.lens for s in chosen].count("SEL") == 2
    assert len({s.seeds[0] for s in chosen}) == len(chosen)
    assert {s.seeds[0] for s in reserve["WHY"]}.isdisjoint({s.seeds[0] for s in chosen})
    assert sel.pick(specs, {"WHY": 2, "SEL": 2}, seed=1) == (chosen, reserve)


def test_pairs_without_sentences_are_never_chosen():
    chosen, _ = sel.pick([_spec("WHY", "a", k=0), _spec("WHY", "b")], {"WHY": 2}, seed=1)
    assert [s.seeds[0] for s in chosen] == ["b"]
