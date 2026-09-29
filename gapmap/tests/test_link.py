from conftest import a_claim, ledger

from gapmap import link


def test_common_stems_over_5_percent_of_a_assertions():
    # "fault" appears in 3/4 A assertions (75% > 5%), "widget" in 1/4 (25%, also > 5%: cut is strict).
    claims = [
        a_claim("Intermittent fault in the field wiring.", source_id="s1"),
        a_claim("A fault in the relay causes chatter.", source_id="s2"),
        a_claim("Ground fault detection uses a sensor.", source_id="s3"),
        a_claim("The widget housing cracked under vibration.", source_id="s4"),
    ]
    idx = link.build_index(ledger(claims))
    common = link.common_stems(idx, cut=0.05)
    assert "fault" in common


def _fillers(n: int) -> list:
    # Distinct filler A claims, disjoint vocabulary from a/b/c below, so with enough of them the
    # stems shared only between a and b stay under the 5% common-stem cut (spec §1.3).
    return [a_claim(f"Component code zz{i:03d} was inspected without incident.", source_id=f"filler-{i}")
            for i in range(n)]


def test_neighbourhood_needs_at_least_threshold_shared_non_common_stems():
    a = a_claim("Loose terminal connections cause intermittent faults.", source_id="s1")
    b = a_claim("Loose terminals and oxidized connections create jitter.", source_id="s2")
    c = a_claim("Ground loops interfere with the analog signal.", source_id="s3")
    idx = link.build_index(ledger([a, b, c, *_fillers(40)]))
    common = link.common_stems(idx, cut=0.05)
    assert not {"loos", "terminal", "connect", "connection"} & common
    nb = link.neighbourhood(idx, a.claim_id, common, threshold=2)
    assert b.claim_id in nb
    assert c.claim_id not in nb


def test_explicit_part_is_seeds_plus_their_neighbourhoods():
    a = a_claim("Loose terminal connections cause intermittent faults.", source_id="s1")
    b = a_claim("Loose terminals and oxidized connections create jitter.", source_id="s2")
    idx = link.build_index(ledger([a, b, *_fillers(40)]))
    common = link.common_stems(idx, cut=0.05)
    x = link.explicit_part(idx, frozenset({a.claim_id}), common, threshold=2)
    assert x == frozenset({a.claim_id, b.claim_id})


def test_breadth_counts_distinct_independence_keys():
    a = a_claim("First claim from key one.", source_id="s1", independence_key="key-1")
    b = a_claim("Second claim also from key one.", source_id="s2", independence_key="key-1")
    lg = ledger([a, b])
    # two claims with 1 evidence each from the same key give k = 1 (spec §1.4).
    assert link.breadth(lg, frozenset({a.claim_id, b.claim_id})) == frozenset({"key-1"})


def test_breadth_two_distinct_keys():
    a = a_claim("First claim from key one.", source_id="s1", independence_key="key-1")
    b = a_claim("Second claim from key two.", source_id="s2", independence_key="key-2")
    lg = ledger([a, b])
    assert link.breadth(lg, frozenset({a.claim_id, b.claim_id})) == frozenset({"key-1", "key-2"})
