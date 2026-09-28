from datetime import date

import pytest
from conftest import CODER, DAY, SCOPE, claim, evidence, generation, search, source
from hypothesis import given
from hypothesis import strategies as st
from pydantic import ValidationError

from residual.claims import Scope
from residual.ledger import Area, Contradiction, Ledger
from residual.provenance import Derivation, Search, Verdict
from residual.vocab import EpistemicLabel, SourceKind, World

L = EpistemicLabel


def supported(assertion="Supported.", src=None):
    return claim(assertion, evidence=(evidence(src or source()),))


def derived(assertion, *premises):
    return claim(assertion, derivation=Derivation(premises=tuple(p.claim_id for p in premises),
                                                  method="m", agent=CODER))


def contradiction(a, b):
    return Contradiction(claims=(a.claim_id, b.claim_id), detected_by=CODER, method="nli")


def area(area_id="a1"):
    return Area(area_id=area_id, scope=SCOPE, name=area_id)


def test_duplicate_claim_ids_refused():
    with pytest.raises(ValidationError, match="duplicate claims"):
        Ledger(purpose="reconstruction", claims=(supported("X."), claim("x.", searches=(search(),))))


def test_the_same_source_described_two_ways_refused():
    a = supported("A.", source("doi:1", published=date(2020, 1, 1)))
    b = supported("B.", source("doi:1", published=date(2021, 1, 1)))
    with pytest.raises(ValidationError, match="described two ways"):
        Ledger(purpose="reconstruction", claims=(a, b))
    Ledger(purpose="reconstruction", claims=(a, supported("B.", source("doi:1"))))


def test_absent_premises_refused():
    with pytest.raises(ValidationError, match="absent claims"):
        Ledger(purpose="reconstruction", claims=(derived("D.", supported()),))


def test_cycles_refused():
    a = claim("A.", derivation=Derivation(premises=(claim("B.", searches=(search(),)).claim_id,),
                                          method="m", agent=CODER))
    b = derived("B.", a)
    with pytest.raises(ValidationError, match="cycle"):
        Ledger(purpose="reconstruction", claims=(a, b))
    selfish = claim("S.", derivation=Derivation(premises=(claim("S.", searches=(search(),)).claim_id,),
                                                method="m", agent=CODER))
    with pytest.raises(ValidationError, match="cycle"):
        Ledger(purpose="reconstruction", claims=(selfish,))


def test_contradictions_must_name_present_claims():
    a, b = supported("A."), supported("B.")
    with pytest.raises(ValidationError, match="absent claims"):
        Ledger(purpose="reconstruction", claims=(a,), contradictions=(contradiction(a, b),))


def test_a_claim_does_not_contradict_itself():
    a = supported("A.")
    with pytest.raises(ValidationError, match="itself"):
        contradiction(a, a)


@pytest.mark.parametrize(("areas", "assignments", "match"), [
    (("a1",), (("c", "a1"),), "absent claim or area"),
    (("a1",), (("A", "a2"),), "absent claim or area"),
    (("a1", "a2"), (("A", "a1"), ("A", "a2")), "more than one area"),
    (("a1", "a1"), (), "duplicate area"),
])
def test_bad_or_duplicate_assignments_refused(areas, assignments, match):
    a = supported("A.")
    assignments = tuple((a.claim_id if cid == "A" else cid, aid) for cid, aid in assignments)
    with pytest.raises(ValidationError, match=match):
        Ledger(purpose="reconstruction", claims=(a,), areas=tuple(area(x) for x in areas),
               assignments=assignments)


@pytest.mark.parametrize(("premise", "label"), [
    (claim("P.", generation=generation()), L.SYNTHETIC_EXTRAPOLATION),
    (claim("P.", searches=(search(),)), L.UNKNOWN),
    (supported("P."), L.INFERRED),
])
def test_derivation_takes_the_weakest_premise(premise, label):
    d = derived("D.", premise)
    ledger = Ledger(purpose="reconstruction", claims=(premise, d))
    assert d.label is L.INFERRED
    assert ledger.label(d.claim_id) is label


def test_taint_follows_chains_and_synthetic_wins():
    syn, unk, ok = (claim("S.", generation=generation()), claim("U.", searches=(search(),)),
                    supported("O."))
    d1 = derived("D1.", syn, ok)
    d2 = derived("D2.", d1, unk)
    d3 = derived("D3.", ok)
    d4 = derived("D4.", d3)
    ledger = Ledger(purpose="reconstruction", claims=(syn, unk, ok, d1, d2, d3, d4))
    assert ledger.label(d1.claim_id) is L.SYNTHETIC_EXTRAPOLATION
    assert ledger.label(d2.claim_id) is L.SYNTHETIC_EXTRAPOLATION
    assert ledger.label(d4.claim_id) is L.INFERRED
    assert ledger.label(unk.claim_id) is L.UNKNOWN


def simulated(assertion="Sim."):
    return claim(assertion, generation=generation(activity="simulation", tier="T1"))


def test_a_surrogate_ledger_holds_only_simulation():
    Ledger(purpose="surrogate", claims=(simulated(),))
    with pytest.raises(ValidationError, match="only simulation"):
        Ledger(purpose="surrogate", claims=(simulated(), claim("Gen.", generation=generation())))


@pytest.mark.parametrize("purpose", ["reconstruction", "gold"])
def test_simulation_refused_outside_a_surrogate_ledger(purpose):
    with pytest.raises(ValidationError, match="surrogate"):
        Ledger(purpose=purpose, claims=(simulated(),))


def test_gold_holds_only_criterion_labels():
    Ledger(purpose="gold", claims=(supported(),))
    for weak in (claim("G.", generation=generation()), claim("U.", searches=(search(),))):
        with pytest.raises(ValidationError, match="gold holds only supported"):
            Ledger(purpose="gold", claims=(supported(), weak))
    with pytest.raises(ValidationError, match="gold holds only supported"):
        Ledger(purpose="gold", claims=(supported(), derived("D.", supported())))


def test_as_of_drops_undated_and_later_sources_and_reports_the_dropped():
    old = supported("Old.", source("old", published=date(2019, 1, 1)))
    new = supported("New.", source("new", published=date(2022, 1, 1)))
    undated = supported("Undated.", source("undated", published=None))
    mixed = claim("Mixed.", evidence=(evidence(source("old", published=date(2019, 1, 1))),
                                      evidence(source("new", published=date(2022, 1, 1)))))
    ledger = Ledger(purpose="reconstruction", claims=(old, new, undated, mixed))
    dated, dropped = ledger.as_of(date(2020, 1, 1))
    assert set(dated.by_id) == {old.claim_id, mixed.claim_id}
    assert dropped == tuple(sorted((new.claim_id, undated.claim_id)))
    assert len(dated.by_id[mixed.claim_id].evidence) == 1


def test_as_of_keeps_a_claim_with_an_earlier_search_as_unknown():
    c = claim("C.", evidence=(evidence(source("new", published=date(2022, 1, 1))),),
              searches=(Search(corpus="c", query="q", on=date(2019, 1, 1), agent=CODER),))
    late = claim("Late.", evidence=(evidence(source("new", published=date(2022, 1, 1))),),
                 searches=(search(),))
    dated, dropped = Ledger(purpose="reconstruction", claims=(c, late)).as_of(date(2020, 1, 1))
    assert dated.label(c.claim_id) is L.UNKNOWN
    assert dropped == (late.claim_id,)


def test_as_of_drops_contradictions_assignments_and_dependent_derivations():
    new = supported("New.", source("new", published=date(2022, 1, 1)))
    old = supported("Old.", source("old", published=date(2019, 1, 1)))
    d = derived("D.", new)
    dd = derived("DD.", d)
    ledger = Ledger(purpose="reconstruction", claims=(new, old, d, dd),
                    contradictions=(contradiction(new, old),), areas=(area(),),
                    assignments=((new.claim_id, "a1"), (old.claim_id, "a1")))
    dated, dropped = ledger.as_of(date(2020, 1, 1))
    assert set(dropped) == {new.claim_id, d.claim_id, dd.claim_id}
    assert dated.contradictions == ()
    assert dated.assignments == ((old.claim_id, "a1"),)
    assert dated.areas == ledger.areas


def test_as_of_keeps_a_gold_ledger_gold():
    old = supported("Old.", source("old", published=date(2019, 1, 1)))
    gold_both = claim("Both.", evidence=(evidence(source("new", published=date(2022, 1, 1))),))
    dated, dropped = Ledger(purpose="gold", claims=(old, gold_both)).as_of(date(2020, 1, 1))
    assert dated.purpose == "gold" and dropped == (gold_both.claim_id,)


def test_within_separates_worlds():
    a = supported("A.", source("pub", world=World.A))
    b = claim("B.", scope=Scope(domain="test-domain", organisation="org-1"),
              evidence=(evidence(source("org", kind=SourceKind.DOCUMENTATION, world=World.B)),))
    c = supported("C.", source("human", kind=SourceKind.INTERVIEW, world=World.C))
    ledger = Ledger(purpose="reconstruction", claims=(a, b, c))
    for world, kept in ((World.A, a), (World.B, b), (World.C, c)):
        restricted, dropped = ledger.within({world})
        assert set(restricted.by_id) == {kept.claim_id}
        assert len(dropped) == 2
    assert ledger.within(set(World))[1] == ()


def test_within_keeps_only_the_matching_label():
    scope = Scope(domain="test-domain", organisation="org-1")
    ab = claim("AB.", scope=scope, evidence=(
        evidence(source("pub", world=World.A)),
        evidence(source("org", kind=SourceKind.DOCUMENTATION, world=World.B))))
    ledger = Ledger(purpose="reconstruction", claims=(ab,))
    assert ledger.label(ab.claim_id) is L.ORGANISATIONAL_ARTEFACT_SUPPORTED
    assert ledger.within({World.A})[0].label(ab.claim_id) is L.LITERATURE_SUPPORTED
    assert ledger.within({World.B})[0].label(ab.claim_id) is L.ORGANISATIONAL_ARTEFACT_SUPPORTED
    assert ledger.within({World.A})[0].by_id[ab.claim_id].worlds == {World.A}


def rich_ledger_parts():
    a, b, c = supported("A.", source("sa")), supported("B.", source("sb")), supported("C.", source("sc"))
    d = derived("D.", a, b)
    s = claim("S.", generation=generation(), evidence=(evidence(source("sd"), verdict=Verdict.PENDING),))
    claims = [a, b, c, d, s]
    areas = [area("a1"), area("a2"), area("a3")]
    assignments = [(a.claim_id, "a1"), (b.claim_id, "a2"), (d.claim_id, "a1"), (s.claim_id, "a3")]
    contradictions = [contradiction(a, c), contradiction(b, s), contradiction(c, d)]
    return claims, areas, assignments, contradictions


def test_json_round_trip():
    claims, areas, assignments, contradictions = rich_ledger_parts()
    ledger = Ledger(purpose="reconstruction", claims=tuple(claims), areas=tuple(areas),
                    assignments=tuple(assignments), contradictions=tuple(contradictions))
    back = Ledger.from_json(ledger.to_json())
    assert back == ledger
    assert back.to_json() == ledger.to_json()
    assert {cid: back.label(cid) for cid in back.by_id} == {cid: ledger.label(cid)
                                                           for cid in ledger.by_id}


PARTS = rich_ledger_parts()
BASELINE = Ledger(purpose="reconstruction", claims=tuple(PARTS[0]), areas=tuple(PARTS[1]),
                  assignments=tuple(PARTS[2]), contradictions=tuple(PARTS[3])).to_json()


@given(st.permutations(PARTS[0]), st.permutations(PARTS[1]), st.permutations(PARTS[2]),
       st.permutations(PARTS[3]), st.lists(st.booleans(), min_size=3, max_size=3))
def test_to_json_is_independent_of_input_order(claims, areas, assignments, contradictions, flips):
    contradictions = [Contradiction(claims=x.claims[::-1] if f else x.claims,
                                    detected_by=x.detected_by, method=x.method)
                      for x, f in zip(contradictions, flips, strict=True)]
    ledger = Ledger(purpose="reconstruction", claims=tuple(claims), areas=tuple(areas),
                    assignments=tuple(assignments), contradictions=tuple(contradictions))
    assert ledger.to_json() == BASELINE


def test_to_json_is_stable_under_evidence_and_premise_order():
    a, b = supported("A.", source("sa")), supported("B.", source("sb"))
    x, y = evidence(source("x")), evidence(source("y"))
    one = Ledger(purpose="reconstruction", claims=(a, b, claim("E.", evidence=(x, y)),
                                                   derived("D.", a, b)))
    two = Ledger(purpose="reconstruction", claims=(b, a, claim("E.", evidence=(y, x)),
                                                   derived("D.", b, a)))
    assert one.to_json() == two.to_json()
    assert one.to_json().endswith("\n")


def test_as_of_counts_sources_published_on_the_day():
    c = supported("C.", source("s", published=DAY))
    assert Ledger(purpose="reconstruction", claims=(c,)).as_of(DAY)[1] == ()
