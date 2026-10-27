import sim


def test_a_perfect_reader_always_passes_and_a_coin_never_does():
    assert sim.pass_rate(13, 1.0, 0.0, 0.0, reps=20) == 1.0
    assert sim.pass_rate(13, 0.5, 0.5, reps=50) == 0.0
