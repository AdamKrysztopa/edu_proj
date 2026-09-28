from residual.vocab import (
    CRITERION_LABELS,
    HUMAN_RECORD_KINDS,
    PRACTICE,
    EpistemicLabel,
    Question,
    SourceKind,
    World,
)


def test_exactly_the_six_labels_of_section_6():
    assert {label.value for label in EpistemicLabel} == {
        "observed_human_evidence", "literature_supported", "organisational_artefact_supported",
        "inferred", "synthetic_extrapolation", "unknown",
    }


def test_only_supported_labels_can_be_criteria():
    assert EpistemicLabel.SYNTHETIC_EXTRAPOLATION not in CRITERION_LABELS
    assert EpistemicLabel.INFERRED not in CRITERION_LABELS
    assert EpistemicLabel.UNKNOWN not in CRITERION_LABELS
    assert len(CRITERION_LABELS) == 3


def test_three_worlds_and_six_questions():
    assert len(World) == 3
    assert len(Question) == 6


def test_every_source_kind_has_a_practice():
    assert set(PRACTICE) == set(SourceKind)
    assert HUMAN_RECORD_KINDS < set(SourceKind)
