import pytest
from pydantic import BaseModel, Field

from residual.freeze import _sha, _structure, fingerprint, frozen


def test_the_schema_matches_its_freeze():
    assert fingerprint() == frozen()


def test_fingerprint_has_the_three_hashes():
    assert set(fingerprint()) == {"schema_sha256", "features_sha256", "semantics_sha256"}


def test_structure_strips_prose_at_every_depth():
    schema = {"title": "T", "description": "D", "type": "object",
              "properties": {"x": {"title": "X", "description": "d", "type": "integer"}},
              "anyOf": [{"description": "d", "type": "null"}]}
    assert _structure(schema) == {"type": "object", "properties": {"x": {"type": "integer"}},
                                  "anyOf": [{"type": "null"}]}


class Plain(BaseModel):
    x: int
    y: str | None = None


class Reworded(BaseModel):
    """Prose that says something new."""

    x: int = Field(description="an integer", title="The X")
    y: str | None = Field(None, description="an optional string")


class Retyped(BaseModel):
    x: float
    y: str | None = None


def schema_sha(model):
    return _sha(_structure(model.model_json_schema()))


def test_prose_edits_do_not_change_the_schema_hash():
    assert schema_sha(Plain) == schema_sha(Reworded)


def test_structural_edits_do_change_the_schema_hash():
    assert schema_sha(Plain) != schema_sha(Retyped)


class WithTitleField(BaseModel):
    x: int
    y: str | None = None
    title: str | None = None


def test_a_field_named_title_is_a_structural_change():
    assert schema_sha(Plain) != schema_sha(WithTitleField)
