"""Question-quote picking (spec §2 question rules; S3 defect 6; fix 5 "fragment quote fallback").
`lenses._best_sentence`/`_pick_quotes` narrow a claim's evidence span(s) to the most relevant
sentence for a question quote; fix 5 covers the case where that sentence is itself a fragment too
short to quote on its own (e.g. "retention periods;")."""
from conftest import a_claim, ledger

from gapmap import lenses, text


def test_short_quote_sentence_falls_back_to_assertion():
    claim = a_claim("Records must be kept for the required retention periods.",
                    exact="Some longer lead-in sentence about scope. retention periods; more text follows here.",
                    source_id="s1")
    lg = ledger([claim])
    sent = lenses._best_sentence(lg, claim.claim_id, text.cw("retention periods"))
    assert sent == claim.assertion


def test_long_enough_quote_sentence_is_kept_verbatim():
    claim = a_claim("Records must be kept for the required retention periods.",
                    exact="The controller must document all applicable retention periods in the "
                         "register for audit purposes.",
                    source_id="s1")
    lg = ledger([claim])
    sent = lenses._best_sentence(lg, claim.claim_id, text.cw("retention periods"))
    assert "retention periods" in sent
    assert sent != claim.assertion
