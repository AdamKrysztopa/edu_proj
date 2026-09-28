from datetime import date

import pytest
from conftest import CODER, GENERATOR, SCOPE, VERIFIER, claim, evidence, generation, search, source
from hypothesis import given
from hypothesis import strategies as st
from pydantic import ValidationError

from residual.claims import Scope
from residual.provenance import Agent, Derivation, Verdict
from residual.vocab import (
    CRITERION_LABELS,
    WORLD_C_KINDS,
    Certainty,
    EpistemicLabel,
    Practice,
    Question,
    SourceKind,
    Voice,
    World,
)

L = EpistemicLabel
K = SourceKind
ORG = Scope(domain="test-domain", organisation="org-1")


@pytest.mark.parametrize(("kind", "world", "scope", "label"), [
    *[(k, World.C, SCOPE, L.OBSERVED_HUMAN_EVIDENCE) for k in sorted(WORLD_C_KINDS)],
    (K.LEARNER_RESPONSE, World.A, SCOPE, L.OBSERVED_HUMAN_EVIDENCE),
    (K.ELICITATION_RECORD, World.A, SCOPE, L.LITERATURE_SUPPORTED),
    (K.STUDY, World.A, SCOPE, L.LITERATURE_SUPPORTED),
    (K.DOCUMENTATION, World.B, ORG, L.ORGANISATIONAL_ARTEFACT_SUPPORTED),
    (K.COMMIT, World.B, ORG, L.ORGANISATIONAL_ARTEFACT_SUPPORTED),
])
def test_label_table(kind, world, scope, label):
    assert claim(scope=scope, evidence=(evidence(source(kind=kind, world=world)),)).label is label


def test_out_of_scope_organisational_evidence_is_excluded_with_its_reason():
    c = claim(evidence=(evidence(source(kind=K.DOCUMENTATION, world=World.B)),))
    assert c.label is L.UNKNOWN
    assert c.supporting == ()
    [(_, why)] = c.excluded
    assert "organisation" in why
    other = Scope(domain="test-domain", organisation="org-2")
    assert claim(scope=other, evidence=c.evidence).label is L.UNKNOWN


def test_a_derivation_is_inferred():
    c = claim(derivation=Derivation(premises=("c-x",), method="m", agent=CODER))
    assert c.label is L.INFERRED


def test_model_generated_unverified_is_synthetic():
    assert claim(generation=generation()).label is L.SYNTHETIC_EXTRAPOLATION
    pending = evidence(verdict=Verdict.PENDING)
    assert claim(generation=generation(), evidence=(pending,)).label is L.SYNTHETIC_EXTRAPOLATION


def test_machine_voiced_support_is_synthetic_and_excluded():
    c = claim(evidence=(evidence(source(voice=Voice.MACHINE)),))
    assert c.label is L.SYNTHETIC_EXTRAPOLATION
    assert c.excluded[0][1] == "machine-voiced source"


@pytest.mark.parametrize("verdict", [Verdict.INSUFFICIENT, Verdict.UNRESOLVABLE, Verdict.REFUTES,
                                     Verdict.PENDING])
def test_failed_evidence_not_model_made_is_unknown(verdict):
    assert claim(evidence=(evidence(verdict=verdict),)).label is L.UNKNOWN
    assert claim(evidence=(evidence(verdict=verdict),),
                 generation=generation(CODER, "coding")).label is L.UNKNOWN


def test_a_search_alone_is_unknown():
    assert claim(searches=(search(),)).label is L.UNKNOWN


@pytest.mark.parametrize("gen", [None, generation(CODER, "coding"),
                                 generation(Agent(kind="software", id="s"))])
def test_a_claim_with_nothing_to_account_for_it_is_invalid(gen):
    with pytest.raises(ValidationError, match="account"):
        claim(generation=gen)


def test_the_generators_own_family_verifying_does_not_count():
    same = Agent(kind="model", id="another-model", family=GENERATOR.family)
    c = claim(generation=generation(), evidence=(evidence(verifier=same),))
    assert c.label is L.SYNTHETIC_EXTRAPOLATION
    assert c.excluded[0][1] == "verified by the generating model's family"


@pytest.mark.parametrize("verifier", [VERIFIER, CODER])
def test_another_family_or_a_human_verifying_counts(verifier):
    c = claim(generation=generation(), evidence=(evidence(verifier=verifier),))
    assert c.label is L.LITERATURE_SUPPORTED
    assert c.excluded == ()


def test_a_model_verifier_counts_against_a_human_generator():
    same = Agent(kind="model", id="m", family=GENERATOR.family)
    coded = generation(CODER, "coding")
    assert claim(evidence=(evidence(verifier=same),), generation=coded).label is L.LITERATURE_SUPPORTED


def test_a_model_verifier_needs_a_recorded_generator():
    same = Agent(kind="model", id="m", family=GENERATOR.family)
    c = claim(evidence=(evidence(verifier=same),))
    assert c.label is L.UNKNOWN
    assert c.excluded[0][1] == "a model's verdict counts only against a recorded generator"


def test_a_software_verifier_does_not_count():
    c = claim(evidence=(evidence(verifier=Agent(kind="software", id="string-match")),))
    assert c.label not in CRITERION_LABELS


@pytest.mark.parametrize(("kind", "voice", "counts"), [
    (K.LEARNER_RESPONSE, Voice.NOVICE, True),
    (K.LOG, Voice.NOVICE, True),
    (K.STUDY, Voice.NOVICE, True),
    (K.STUDY, Voice.EXPERT, False),
    (K.LEARNER_RESPONSE, Voice.MIXED, False),
    (K.TEXTBOOK, Voice.NOVICE, False),
    (K.FORUM_POST, Voice.NOVICE, True),
    (K.ISSUE, Voice.NOVICE, True),
    (K.ISSUE, Voice.EXPERT, False),
    (K.INTERVIEW, Voice.NOVICE, False),
])
def test_difficulty_counts_only_novice_learner_data(kind, voice, counts):
    c = claim(question=Question.DIFFICULTY, evidence=(evidence(source(kind=kind, voice=voice)),))
    assert (c.label in CRITERION_LABELS) is counts
    if not counts:
        assert c.excluded[0][1] == "difficulty is answered only by learner data"


@pytest.mark.parametrize(("kind", "world", "voice", "counts"), [
    (K.LEARNER_RESPONSE, World.C, Voice.NOVICE, True),
    (K.LEARNER_RESPONSE, World.A, Voice.NOVICE, False),
    (K.LEARNER_RESPONSE, World.C, Voice.EXPERT, False),
    (K.THINK_ALOUD, World.C, Voice.NOVICE, False),
    (K.LOG, World.A, Voice.NOVICE, False),
])
def test_learner_state_counts_only_world_c_novice_responses(kind, world, voice, counts):
    c = claim(question=Question.LEARNER_STATE,
              evidence=(evidence(source(kind=kind, world=world, voice=voice)),))
    assert (c.label is L.OBSERVED_HUMAN_EVIDENCE) is counts
    if not counts:
        assert "learner state" in c.excluded[0][1]


def test_pending_and_refuting():
    ok, bad, wait = (evidence(source(f"id-{v}"), verdict=v)
                     for v in (Verdict.SUPPORTS, Verdict.REFUTES, Verdict.PENDING))
    c = claim(evidence=(ok, bad, wait))
    assert c.pending
    assert c.refuting == (bad,)
    assert not claim(evidence=(ok, bad)).pending
    assert claim(evidence=(ok,)).refuting == ()


def test_corroboration_counts_independence_keys_once():
    a, b, c = (source(i, independence_key=k) for i, k in (("a", "k1"), ("b", "k1"), ("c", "k2")))
    assert claim(evidence=(evidence(a), evidence(b))).corroboration == 1
    assert claim(evidence=(evidence(a), evidence(b), evidence(c))).corroboration == 2
    machine = source("d", voice=Voice.MACHINE)
    assert claim(evidence=(evidence(a), evidence(machine))).corroboration == 1


def test_practices_come_from_supporting_evidence_only():
    book = evidence(source("book", kind=K.TEXTBOOK))
    log = evidence(source("log", kind=K.LOG))
    assert claim(evidence=(book,)).practices == {Practice.IMAGINED}
    assert claim(evidence=(book, log)).practices == {Practice.IMAGINED, Practice.DONE}
    failed = evidence(source("log", kind=K.LOG), verdict=Verdict.INSUFFICIENT)
    assert claim(evidence=(book, failed)).practices == {Practice.IMAGINED}


def test_certainty_only_on_criterion_claims():
    assert claim(evidence=(evidence(),), certainty=Certainty.LOW).certainty is Certainty.LOW
    with pytest.raises(ValidationError, match="certainty"):
        claim(generation=generation(), certainty=Certainty.HIGH)
    with pytest.raises(ValidationError, match="certainty"):
        claim(searches=(search(),), certainty=Certainty.HIGH)


def test_validity_window():
    with pytest.raises(ValidationError, match="valid_from"):
        claim(searches=(search(),), valid_from=date(2021, 1, 1), valid_until=date(2020, 1, 1))
    c = claim(searches=(search(),), valid_from=date(2020, 1, 1), valid_until=date(2021, 1, 1))
    assert c.in_force(date(2020, 1, 1)) and c.in_force(date(2021, 1, 1))
    assert not c.in_force(date(2019, 12, 31)) and not c.in_force(date(2021, 1, 2))
    assert claim(searches=(search(),)).in_force(date(1, 1, 1))


def test_claim_id():
    base = claim("An  Assertion. ", searches=(search(),))
    assert base.claim_id == claim("an assertion.", evidence=(evidence(),)).claim_id
    assert base.claim_id == claim("AN\tASSERTION.\n", generation=generation()).claim_id
    assert base.claim_id.startswith("c-")
    assert base.claim_id != claim("An assertion", searches=(search(),)).claim_id
    assert base.claim_id != claim("An assertion.", question=Question.DOMAIN,
                                  searches=(search(),)).claim_id
    for scope in (Scope(domain="other"), Scope(domain="test-domain", task="t"),
                  Scope(domain="test-domain", organisation="org-1")):
        assert base.claim_id != claim("An assertion.", scope=scope, searches=(search(),)).claim_id


def test_evidence_is_held_in_canonical_order():
    a, b = evidence(source("a")), evidence(source("b"))
    assert claim(evidence=(a, b)) == claim(evidence=(b, a))


FAMILIES = ("family-a", "family-b")


@st.composite
def agents(draw, kinds):
    kind = draw(st.sampled_from(kinds))
    return Agent(kind=kind, id=draw(st.sampled_from(("x", "y"))),
                 family=draw(st.sampled_from(FAMILIES)) if kind == "model" else None)


@st.composite
def evidences(draw, verifier_kinds):
    world = draw(st.sampled_from(list(World)))
    kinds = sorted(WORLD_C_KINDS) if world is World.C else list(SourceKind)
    src = source(draw(st.sampled_from(("s1", "s2", "s3"))), kind=draw(st.sampled_from(kinds)),
                 world=world, voice=draw(st.sampled_from(list(Voice))),
                 organisation=draw(st.sampled_from(("org-1", "org-2"))) if world is World.B else None)
    return evidence(src, verdict=draw(st.sampled_from(list(Verdict))),
                    verifier=draw(agents(verifier_kinds)))


@st.composite
def claims(draw, verifier_kinds=("human", "model", "software")):
    gen = draw(st.one_of(st.none(), agents(("human", "model", "software"))))
    ev = draw(st.lists(evidences(verifier_kinds), max_size=3,
                       unique_by=lambda e: e.source.identifier))
    return claim(
        question=draw(st.sampled_from(list(Question))),
        scope=Scope(domain="d", organisation=draw(st.sampled_from((None, "org-1", "org-2")))),
        evidence=tuple(ev),
        generation=None if gen is None else generation(gen, "extraction"),
        searches=(search(),) if draw(st.booleans()) or not ev else (),
    )


def _verified_by_other_than_generator(c):
    gen = c.generation.agent if c.generation else None
    for e in c.evidence:
        v = e.verification.verifier
        if e.verification.verdict is not Verdict.SUPPORTS or e.source.voice is Voice.MACHINE:
            continue
        if v.kind == "human" or (v.kind == "model" and not (
                gen is not None and gen.kind == "model" and gen.family == v.family)):
            return True
    return False


@given(claims(verifier_kinds=("human", "model")))
def test_a_criterion_label_needs_support_verified_by_a_human_or_another_family(c):
    if c.label in CRITERION_LABELS:
        assert _verified_by_other_than_generator(c)


@given(claims())
def test_a_criterion_label_needs_support_verified_by_a_human_or_another_family_any_verifier(c):
    if c.label in CRITERION_LABELS:
        assert _verified_by_other_than_generator(c)


@given(claims())
def test_model_generated_claims_without_counting_support_are_never_criteria(c):
    gen = c.generation
    if gen is None or gen.agent.kind != "model":
        return
    counting = [e for e in c.evidence
                if e.verification.verdict is Verdict.SUPPORTS and e.source.voice is not Voice.MACHINE
                and not (e.verification.verifier.kind == "model"
                         and e.verification.verifier.family == gen.agent.family)]
    if not counting:
        assert c.label is L.SYNTHETIC_EXTRAPOLATION
