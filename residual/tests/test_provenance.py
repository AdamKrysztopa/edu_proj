from datetime import date

import pytest
from conftest import CODER, DAY, GENERATOR, evidence, generation, source
from pydantic import ValidationError

from residual.provenance import (
    Agent,
    Derivation,
    Evidence,
    Generation,
    Selector,
    Source,
    Verdict,
    Verification,
)
from residual.vocab import QUOTABLE_KINDS, WORLD_C_KINDS, SourceKind, Voice, World


@pytest.mark.parametrize("kind", sorted(set(SourceKind) - WORLD_C_KINDS))
def test_world_c_refuses_text_kinds(kind):
    with pytest.raises(ValidationError, match="World C"):
        source(kind=kind, world=World.C)


@pytest.mark.parametrize("kind", sorted(WORLD_C_KINDS))
def test_world_c_accepts_human_records(kind):
    assert source(kind=kind, world=World.C).world is World.C


def test_world_b_requires_an_organisation():
    with pytest.raises(ValidationError, match="organisation"):
        Source(identifier="x", kind=SourceKind.ISSUE, world=World.B, voice=Voice.EXPERT,
               independence_key="x", published=None)


@pytest.mark.parametrize("world", [World.A, World.C])
def test_only_world_b_names_an_organisation(world):
    with pytest.raises(ValidationError, match="organisation"):
        Source(identifier="x", kind=SourceKind.INTERVIEW, world=world, voice=Voice.EXPERT,
               independence_key="x", published=None, organisation="org-1")


@pytest.mark.parametrize("field", ["identifier", "independence_key"])
def test_source_keys_must_not_be_blank(field):
    kw = dict(identifier="x", kind=SourceKind.STUDY, world=World.A, voice=Voice.EXPERT,
              independence_key="x", published=None) | {field: "  "}
    with pytest.raises(ValidationError):
        Source(**kw)


@pytest.mark.parametrize("kind", sorted(QUOTABLE_KINDS))
def test_prose_kinds_require_an_exact_quote(kind):
    src = source(kind=kind, world=World.C if kind in WORLD_C_KINDS else World.A)
    with pytest.raises(ValidationError, match="exact"):
        Evidence(source=src, selector=Selector(locator="p. 1"), retrieved=DAY)


@pytest.mark.parametrize("kind", sorted(set(SourceKind) - QUOTABLE_KINDS))
def test_record_kinds_accept_a_locator_alone(kind):
    Evidence(source=source(kind=kind), selector=Selector(locator="row 7"), retrieved=DAY)


def test_a_selector_needs_a_quote_or_a_locator():
    with pytest.raises(ValidationError):
        Selector()


def test_pending_verification_has_no_verifier_or_date():
    assert Verification(verdict=Verdict.PENDING).verifier is None
    for kw in ({"verifier": CODER}, {"on": DAY}, {"verifier": CODER, "on": DAY}):
        with pytest.raises(ValidationError, match="pending"):
            Verification(verdict=Verdict.PENDING, **kw)


@pytest.mark.parametrize("verdict", sorted(set(Verdict) - {Verdict.PENDING}))
def test_a_settled_verification_needs_verifier_and_date(verdict):
    Verification(verdict=verdict, verifier=CODER, on=DAY)
    with pytest.raises(ValidationError):
        Verification(verdict=verdict)


@pytest.mark.parametrize("kw", [{"verifier": CODER}, {"on": DAY}])
def test_a_settled_verification_with_only_one_of_verifier_and_date_is_refused(kw):
    with pytest.raises(ValidationError):
        Verification(verdict=Verdict.SUPPORTS, **kw)


def test_model_agents_need_a_family():
    with pytest.raises(ValidationError, match="family"):
        Agent(kind="model", id="m")


@pytest.mark.parametrize("kind", ["human", "software"])
def test_only_model_agents_have_a_family(kind):
    Agent(kind=kind, id="a")
    with pytest.raises(ValidationError, match="family"):
        Agent(kind=kind, id="a", family="family-a")


def test_model_generation_needs_a_spec_hash():
    with pytest.raises(ValidationError, match="spec"):
        Generation(agent=GENERATOR, activity="extraction", on=DAY)
    Generation(agent=CODER, activity="coding", on=DAY)


def test_simulation_needs_a_tier():
    with pytest.raises(ValidationError, match="tier"):
        generation(activity="simulation")
    assert generation(activity="simulation", tier="T1").tier == "T1"


@pytest.mark.parametrize("agent", [CODER, Agent(kind="software", id="sim")])
def test_simulation_is_run_by_a_model(agent):
    with pytest.raises(ValidationError, match="model"):
        generation(agent, "simulation", tier="none")


@pytest.mark.parametrize("activity", ["extraction", "parametric_recall", "coding"])
def test_only_simulation_has_a_tier(activity):
    with pytest.raises(ValidationError, match="tier"):
        generation(activity=activity, tier="T2")


def test_a_derivation_needs_a_premise():
    with pytest.raises(ValidationError, match="premise"):
        Derivation(premises=(), method="m", agent=CODER)
    assert Derivation(premises=("b", "a", "b"), method="m", agent=CODER).premises == ("a", "b")


def test_source_id_is_deterministic_and_depends_only_on_identifier():
    a = source("doi:10.1/x")
    b = source("doi:10.1/x", kind=SourceKind.TEXTBOOK, voice=Voice.NOVICE, independence_key="k",
               published=date(1999, 1, 1), world=World.B)
    assert a.source_id == source("doi:10.1/x").source_id == b.source_id
    assert a.source_id != source("doi:10.1/y").source_id
    assert a.source_id.startswith("s-")


def test_records_are_frozen_and_closed():
    e = evidence()
    with pytest.raises(ValidationError):
        e.retrieved = DAY
    with pytest.raises(ValidationError):
        Selector(exact="q", colour="red")
