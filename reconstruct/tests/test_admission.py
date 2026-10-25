from datetime import date

import pytest
from admission_fixtures import BLOCKLIST, GOLD_DATE, PLANTED

from reconstruct.admission import Blocklist, Document, admit, normalise_doi, normalise_title, normalise_url


@pytest.mark.parametrize("name,doc,reason", PLANTED, ids=[p[0] for p in PLANTED])
def test_planted_documents(name, doc, reason):
    result = admit(doc, GOLD_DATE, BLOCKLIST)
    if reason is None:
        assert result.admitted and result.reasons == ()
    else:
        assert not result.admitted and reason in result.reasons


def test_every_rejection_class_is_planted():
    reasons = {r for _, _, r in PLANTED}
    assert reasons >= {"on_or_after_gold", "undated", "last_modified_only",
                       "blocklist_doi", "blocklist_title", "blocklist_url", None}


def test_blocklisted_plants_are_rejected_by_the_blocklist_alone():
    for name, doc, reason in PLANTED:
        if reason and reason.startswith("blocklist_"):
            assert admit(doc, GOLD_DATE, Blocklist.of()).admitted, name


def test_admit_is_pure():
    _, doc, _ = PLANTED[0]
    assert admit(doc, GOLD_DATE, BLOCKLIST) == admit(doc, GOLD_DATE, BLOCKLIST)


def test_an_empty_blocklist_rejects_on_dates_only():
    doc = Document(url="https://a.example/x", published=date(1990, 1, 1), published_field="dc.date")
    assert admit(doc, GOLD_DATE, Blocklist.of()).admitted


@pytest.mark.parametrize("raw,norm", [
    ("doi:10.1000/ABC.1", "10.1000/abc.1"),
    ("https://dx.doi.org/10.1000/abc.1.", "10.1000/abc.1"),
    ("https://doi.org/10.1000%2Fabc.1", "10.1000/abc.1"),
    ("not a doi", None),
])
def test_normalise_doi(raw, norm):
    assert normalise_doi(raw) == norm


def test_normalise_title_and_url():
    assert normalise_title("  Fault–Diagnosis:\tA  Study. ") == "fault diagnosis a study"
    assert normalise_url("HTTPS://WWW.Example.org/a/b/?q=1#frag") == "example.org/a/b?q=1"
