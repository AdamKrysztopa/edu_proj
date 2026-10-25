"""I1c: plain-text L7.3 fixtures for running control2 through a real judge. Three SEL fixtures on
different topics, each with one planted pair: candidate i's other-source evidence states the
element in plain text (no FakeJudge marker), and its two donors j and k only describe the topic.
Each plant has two stand-ins that state no element: random letters with the plant's word lengths
(the retrieval words kept), and a plain-English sentence of the plant's exact length."""
from __future__ import annotations

import random
from dataclasses import dataclass

from conftest import a_claim, fillers, ledger

from gapmap import lenses, link


@dataclass(frozen=True)
class Topic:
    name: str
    seed_i: str
    basis: str
    planted: str
    length_matched: str
    donor_j: str
    donor_k: str
    donor_basis: str


TOPICS = (
    Topic(name="plc_test_order",
          seed_i="Diagnostic tests should be selected based on failure likelihood.",
          basis="failure likelihood",
          planted="When an intermittent fault appears, choose first the test whose failure likelihood is highest.",
          length_matched="The failure likelihood of each test was logged by the maintenance team after the spring audit.",
          donor_j="Sampling rate", donor_k="Sampling interval", donor_basis="the suspected event"),
    Topic(name="cable_shielding",
          seed_i="Cable types should be selected based on noise exposure.",
          basis="noise exposure",
          planted="Where a cable runs beside a frequency drive, choose a shielded cable, since its noise exposure is high.",
          length_matched="The noise exposure of every cable was measured by the site team and logged in the yearly plant reports.",
          donor_j="Fuse ratings", donor_k="Breaker ratings", donor_basis="the load current"),
    Topic(name="gdpr_retention",
          seed_i="Retention periods should be selected based on the processing purpose.",
          basis="processing purpose",
          planted="If the processing purpose is a single delivery, choose the shortest retention period and then delete.",
          length_matched="The processing purpose of the dataset was written down by the team in the register during the review.",
          donor_j="Encryption methods", donor_k="Access levels", donor_basis="the data sensitivity"),
)

RANDOM_SEEDS = (7, 8, 9)


def random_letters(topic: Topic, seed: int) -> str:
    keep = set(topic.basis.split())
    rng = random.Random(seed)
    letters = "abcdefghijklmnopqrstuvwxyz"
    return " ".join(w if w.strip(".,:").lower() in keep else "".join(rng.choice(letters) for _ in w)
                    for w in topic.planted.split())


def variants(topic: Topic) -> list[tuple[str, str]]:
    """(variant name, the sentence in i's other-source evidence): the plant, then its stand-ins."""
    return [("planted", topic.planted),
            *((f"random_letters_{s}", random_letters(topic, s)) for s in RANDOM_SEEDS),
            ("length_matched", topic.length_matched)]


def fixture(topic: Topic, sentence: str):
    """Ledger, index, the three SEL candidates, and candidate i's seed claim id."""
    tag = topic.name
    seed_i = a_claim(topic.seed_i, source_id=f"{tag}-s-i", independence_key=f"{tag}-k-i")
    foreign_i = a_claim(f"Selection practice for {topic.basis} is documented.", exact=sentence,
                        source_id=f"{tag}-s-i-f", independence_key=f"{tag}-k-i-f")
    claims = [seed_i, foreign_i]
    for side, head, noun in (("j", topic.donor_j, "practice"), ("k", topic.donor_k, "guidance")):
        claims.append(a_claim(f"{head} should be selected based on {topic.donor_basis}.",
                              source_id=f"{tag}-s-{side}", independence_key=f"{tag}-k-{side}"))
        claims.append(a_claim(f"{head} selection {noun} is documented for {topic.donor_basis}.",
                              source_id=f"{tag}-s-{side}-f", independence_key=f"{tag}-k-{side}-f"))
    lg = ledger([*claims, *fillers(40)])
    idx = link.build_index(lg)
    cands = [c for c in lenses.run_all(lg, idx, link.SETTING_1) if c.lens == "SEL"]
    return lg, idx, cands, seed_i.claim_id
