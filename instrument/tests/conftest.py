import pytest

from fakes import TEST_MODELS
from probe_app import config


@pytest.fixture(autouse=True)
def test_models_file(tmp_path, monkeypatch):
    path = tmp_path / "models.json"
    path.write_text(TEST_MODELS.model_dump_json(exclude_none=True))
    monkeypatch.setattr(config, "MODELS_PATH", path)
    return path
