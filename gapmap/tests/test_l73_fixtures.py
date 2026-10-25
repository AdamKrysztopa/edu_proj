"""The I1c real-judge L7.3 fixtures are well formed before any judge sees them: each planted pair can
discriminate, the plant reaches only the own seed-free arm, no seed sentence of either candidate is
in a seed-free arm, the stand-ins carry no plant, and they match the plant's length."""
import pytest
from conftest import FakeJudge
from l73_fixtures import TOPICS, fixture, random_letters, variants

from gapmap import control2


def _target(topic, sentence):
    lg, idx, cands, target = fixture(topic, sentence)
    assert len(cands) == 3
    specs = control2.build_pairs(lg, idx, cands)
    return lg, next(s for s in specs if target in s.seeds)


@pytest.mark.parametrize("topic", TOPICS, ids=lambda t: t.name)
def test_the_plant_is_in_the_own_seed_free_arm_only(topic):
    lg, spec = _target(topic, topic.planted)
    assert spec.k >= 1
    own = [s for _n, _c, s in spec.arm("own_sf").a_items]
    ctrl = [s for _n, _c, s in spec.arm("ctrl_sf").a_items]
    assert topic.planted in own and topic.planted not in ctrl
    seeds = {lg.by_id[c].assertion for c in (*spec.seeds, *spec.donor_seeds)}
    assert not seeds & set(own + ctrl)


@pytest.mark.parametrize("topic", TOPICS, ids=lambda t: t.name)
def test_every_stand_in_takes_the_plants_place_with_its_length(topic):
    _lg, planted = _target(topic, topic.planted)
    for name, sentence in variants(topic)[1:]:
        assert len(sentence) == len(topic.planted), name
        _lg, spec = _target(topic, sentence)
        assert sentence in [s for _n, _c, s in spec.arm("own_sf").a_items], name
        assert spec.k == planted.k
        assert [s for _c, _i, s in spec.donor_other] == [s for _c, _i, s in planted.donor_other]


@pytest.mark.parametrize("topic", TOPICS, ids=lambda t: t.name)
def test_the_plants_carry_no_fake_judge_marker(topic):
    lg, idx, cands, target = fixture(topic, topic.planted)
    pairs = control2.run(lg, idx, FakeJudge(), cands)
    assert next(p for p in pairs if target in p.seeds).states["own_sf"] == "open"
    assert "CLOSES_HERE" not in topic.planted and "PARTIAL_HERE" not in topic.planted


def test_the_random_letter_stand_ins_differ_by_seed_and_keep_the_retrieval_words():
    topic = TOPICS[0]
    outs = {random_letters(topic, s) for s in (7, 8, 9)}
    assert len(outs) == 3
    assert all(set(topic.basis.split()) <= set(o.rstrip(".").split()) for o in outs)
