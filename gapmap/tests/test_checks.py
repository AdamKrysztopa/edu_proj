"""checks.py: J10, hand-rolled Spearman with ties, terciles, the S2 lexical donor null,
mismatched-evidence control and sibling matching."""
import pytest
from conftest import FakeJudge, a_claim, fillers, ledger, mk_record
from residual.vocab import KnowledgeType

from gapmap import checks, lenses, link, semantic


def test_j10_full_overlap_and_no_overlap():
    assert checks.j10(["a", "b", "c"], ["a", "b", "c"]) == 1.0
    assert checks.j10(["a", "b"], ["c", "d"]) == 0.0
    assert checks.j10(["a", "b", "c"], ["b", "c", "d"]) == pytest.approx(2 / 4)


def test_spearman_hand_example_no_ties():
    # Textbook example: x = 1..5, y = [2, 1, 4, 3, 5] -> rho = 0.8.
    pairs = list(zip([1, 2, 3, 4, 5], [2, 1, 4, 3, 5]))
    assert checks.spearman([(float(a), float(b)) for a, b in pairs]) == pytest.approx(0.8)


def test_spearman_hand_example_with_ties():
    # x has a tie (ranks 1, 2.5, 2.5, 4); worked by hand: rho = 4.5 / sqrt(4.5 * 5.0).
    pairs = [(1.0, 1.0), (2.0, 2.0), (2.0, 3.0), (3.0, 4.0)]
    expected = 4.5 / (4.5 * 5.0) ** 0.5
    assert checks.spearman(pairs) == pytest.approx(expected)


def test_spearman_perfect_and_constant():
    assert checks.spearman([(1.0, 1.0), (2.0, 2.0), (3.0, 3.0)]) == pytest.approx(1.0)
    assert checks.spearman([(1.0, 1.0), (1.0, 1.0)]) == 0.0  # zero variance: defined as 0


def test_terciles_split_ascending_by_density_and_count_closed_and_hyp():
    stats = [checks.CandidateStat(lens="DISC", anchor=f"a{i}", dens=i, state=s, category=c)
            for i, (s, c) in enumerate([
                ("closed", None), ("closed", None), ("open", "RG-SINGLE"),
                ("open", "HYP"), ("partial", "HYP"), ("open", "HYP"),
            ])]
    out = checks.anti_renaming(map_records=[], pool=[], stats=stats)
    terciles = {row["tercile"]: row for row in out["terciles"]}
    assert terciles["low"]["n"] == 2 and terciles["low"]["closed"] == 2
    assert terciles["high"]["n"] == 2 and terciles["high"]["hyp"] == 2


def test_anti_renaming_flags_density_in_disguise():
    # The map is exactly the low-density half of the pool: J10(map, D_low) = 1.0 >= 0.5.
    pool = [mk_record(f"g-{i}", "DISC", "HYP" if i < 2 else "RG-SINGLE", seeds=[f"c{i}"],
                      score=2 - i if i < 2 else 1, k_topic=2) for i in range(4)]
    map_records = sorted(pool, key=lambda r: checks.dens(r))[:2]
    out = checks.anti_renaming(map_records, pool, stats=[])
    assert "density-in-disguise" in out["flags"]


def test_match_candidate_disc_matches_by_anchor_only():
    a = mk_record("g-a", "DISC", "HYP", seeds=["c1"])
    b = mk_record("g-b", "DISC", "HYP", seeds=["c2"])  # same default anchor="anchor"
    assert checks.match_candidate(a, [b]).gap_id == "g-b"


def test_apply_sibling_reroutes_to_rg_sibling_when_the_match_is_closed():
    rec = mk_record("g-a", "DISC", "RG-SINGLE", seeds=["c1"])
    sibling_stats = [checks.CandidateStat(lens="DISC", anchor="anchor", dens=3, state="closed", category=None)]
    out = checks.apply_sibling(rec, sibling_stats)
    assert out.category == "RG-SIBLING"
    assert out.inferred_gap.sibling.state == "closed"


def test_apply_sibling_downgrades_open_to_partial_when_the_match_is_partial():
    rec = mk_record("g-a", "DISC", "HYP", seeds=["c1"])
    assert rec.inferred_gap.closure_state == "open"
    sibling_stats = [checks.CandidateStat(lens="DISC", anchor="anchor", dens=3, state="partial",
                                          category="HYP")]
    out = checks.apply_sibling(rec, sibling_stats)
    assert out.category == "HYP"
    assert out.inferred_gap.closure_state == "partial"
    assert out.inferred_gap.sibling.state == "partial"


def test_apply_sibling_leaves_record_alone_with_no_match():
    rec = mk_record("g-a", "SEL", "HYP", seeds=["c1"])
    out = checks.apply_sibling(rec, [])
    assert out == rec


# --------------------------------------------------------------- S2 lexical donor null (checks.py)

def _fake_candidate(lens_name, seed_stems, pattern_names, extra=None, seed_id="c-seed"):
    return lenses.Candidate(
        lens=lens_name, anchor="a", seeds=frozenset({seed_id}), x_a=frozenset(), rivals=frozenset(),
        lexical_state="open", lexical_partial_hits=(), lexical_synthetic_hits=(),
        s_scope_n=0, test_id="t", missing="m", hypothesis_text="h",
        predicted_knowledge_type=(), predicted_tacitness=(), channel="c", weak_channel=False,
        question_text="q", question_targets=(), alternatives=(),
        closure_seed_stems=seed_stems, closure_pattern_names=pattern_names, extra=extra or {})


def test_lexical_donor_null_excludes_disc():
    seed = a_claim("Systems must inspect the widget.", source_id="c1")
    lg = ledger([seed])
    idx = link.build_index(lg)
    cands = [_fake_candidate("DISC", frozenset({"widget"}), ("QUANT",), seed_id=seed.claim_id)]
    out = checks.lexical_donor_null(lg, idx, cands)
    assert out["by_lens"] == {}
    assert out["total"]["observed"] == 0


def test_lexical_donor_null_is_deterministic():
    claims = [a_claim(f"Systems must inspect the widgetword{i} during commissioning.", source_id=f"c{i}")
             for i in range(20)]
    lg = ledger(claims)
    idx = link.build_index(lg)
    lg2 = ledger(list(claims))
    idx2 = link.build_index(lg2)
    cand = _fake_candidate("SEL", frozenset({"widgetword0"}), ("MODAL",), seed_id=claims[0].claim_id)
    out1 = checks.lexical_donor_null(lg, idx, [cand])
    out2 = checks.lexical_donor_null(lg2, idx2, [cand])
    assert out1 == out2


def test_lexical_donor_null_flags_a_never_closing_candidate():
    # A candidate whose real seed stems never appear (with the required pattern) anywhere else
    # in the ledger closes 0/1 for real; the fix means a check only "passes" when observed is
    # STRICTLY ABOVE the null's high end, so a flat zero is always flagged (never silently
    # "informative" merely because it also falls inside [lo, hi]).
    claims = [a_claim(f"Component code {i:03d} was logged without incident.", source_id=f"c{i}")
             for i in range(30)]
    lg = ledger(claims)
    idx = link.build_index(lg)
    cand = _fake_candidate("SEL", frozenset({"neverseenanywhere"}), ("MODAL",), seed_id=claims[0].claim_id)
    out = checks.lexical_donor_null(lg, idx, [cand])
    assert out["by_lens"]["SEL"]["observed"] == 0
    assert out["by_lens"]["SEL"]["flag"] is True


def test_lexical_donor_null_does_not_flag_a_genuinely_discriminating_closure():
    # required = min(2, |seed_stems|) = 2 here: a donor drawn from an unrelated claim shares at
    # most one of the two seed stems by chance, so the null rarely closes while the real,
    # specifically-corroborated pair reliably does. `_donor_pool` needs each donor to carry >= 2
    # non-common stems of its own, so the filler pool here (unlike `conftest.fillers`, whose
    # shared template words all become common) gives each claim 2 unique per-claim words.
    seed = a_claim("Systems must inspect the coil resistance during commissioning.", source_id="seed-1")
    closer = a_claim("Coil resistance inspection is documented.",
                     exact="Systems must inspect the coil resistance thoroughly.", source_id="closer-1")
    fillers_ = [a_claim(f"Systems observe the sensor{i} value{i} periodically.", source_id=f"f{i}")
               for i in range(40)]
    lg = ledger([seed, closer, *fillers_])
    idx = link.build_index(lg)
    cand = _fake_candidate("SEL", frozenset({"coil", "resistance"}), ("MODAL",), seed_id=seed.claim_id)
    out = checks.lexical_donor_null(lg, idx, [cand])
    assert out["by_lens"]["SEL"]["observed"] == 1
    assert out["by_lens"]["SEL"]["null_mean"] < 0.3
    assert out["by_lens"]["SEL"]["flag"] is False


def test_lexical_donor_null_handles_diag_via_its_own_rival_closure_unit():
    # DIAG's closure unit is one rival's sign test, not a group-level candidate; the null must
    # draw donors per rival, using each rival's own (cause | effect) stems -- not the group.
    race = a_claim("Race conditions indicate timing conflicts.", source_id="c1",
                   knowledge_type=KnowledgeType.FAILURE_MODE)
    ground = a_claim("Ground loops indicate interference.", source_id="c2",
                     knowledge_type=KnowledgeType.FAILURE_MODE)
    lg = ledger([race, ground])
    idx = link.build_index(lg)
    extra = {"diag_rival_stems": {
        race.claim_id: (frozenset({"racecondit"}), frozenset()),
        ground.claim_id: (frozenset({"groundloop"}), frozenset()),
    }}
    cand = _fake_candidate("DIAG", frozenset(), (), extra=extra, seed_id=race.claim_id)
    out = checks.lexical_donor_null(lg, idx, [cand])
    assert "DIAG" in out["by_lens"]
    assert out["by_lens"]["DIAG"]["n_candidates"] == 2  # one per rival, not one per group


def test_judge_lexical_confusion_counts_pairs():
    stats = [checks.CandidateStat(lens="SEL", anchor="a", dens=1, state="open", category="RG-SINGLE",
                                  lexical_state="closed"),
            checks.CandidateStat(lens="SEL", anchor="b", dens=1, state="open", category="RG-SINGLE",
                                 lexical_state="closed"),
            checks.CandidateStat(lens="SEL", anchor="c", dens=1, state="closed", category=None,
                                 lexical_state="open")]
    out = checks.judge_lexical_confusion(stats)
    assert out == {"closed->open": 2, "open->closed": 1}


# ------------------------------------------------------------------- S2 fair mismatched-evidence control

def test_mismatched_evidence_control_skips_lenses_with_fewer_than_2_candidates():
    seed = a_claim("Diagnostic tests should be selected based on failure likelihood.", source_id="s1")
    lg = ledger([seed])
    idx = link.build_index(lg)
    cands = lenses.run_all(lg, idx, link.SETTING_1)
    out = checks.mismatched_evidence_control(lg, "ledgersha", idx, FakeJudge(), cands)
    assert "SEL" not in out["by_lens"]


def test_mismatched_evidence_control_reports_own_control_and_other_source_only():
    seed1 = a_claim("Diagnostic tests should be selected based on failure likelihood.", source_id="s1")
    seed2 = a_claim("Sampling rate should be selected based on the suspected event.", source_id="s2")
    lg = ledger([seed1, seed2])
    idx = link.build_index(lg)
    cands = [c for c in lenses.run_all(lg, idx, link.SETTING_1) if c.lens == "SEL"]
    out = checks.mismatched_evidence_control(lg, "ledgersha", idx, FakeJudge(), cands)
    row = out["by_lens"]["SEL"]
    assert {"n", "own_rate", "control_rate", "other_source_only_rate", "flag"} <= row.keys()
    assert "mismatched_rate" not in row  # the old straw-man field name is gone


def test_mismatched_evidence_control_flags_a_judge_that_closes_on_anything():
    # Both arms now ALWAYS carry the seed's own sentence (the fix itself), so a judge that closes
    # on whatever is offered first closes BOTH arms every time: own_rate == control_rate == 1.0,
    # own - control == 0, never >= 0.20 -- correctly flagged uninformative regardless of content.
    class _AlwaysCloses:
        model_id = "always"

        def ask(self, prompt):
            import re
            ids = re.findall(r"^(\d+):", prompt, re.MULTILINE)
            return {"states": ids[:1], "partially": [], "reason": "always"} if ids else {
                "states": [], "partially": [], "reason": "nothing offered"}

    seed1 = a_claim("Diagnostic tests should be selected based on failure likelihood.", source_id="s1")
    seed2 = a_claim("Sampling rate should be selected based on the suspected event.", source_id="s2")
    lg = ledger([seed1, seed2])
    idx = link.build_index(lg)
    cands = [c for c in lenses.run_all(lg, idx, link.SETTING_1) if c.lens == "SEL"]
    assert len(cands) == 2
    out = checks.mismatched_evidence_control(lg, "ledgersha", idx, _AlwaysCloses(), cands)
    assert out["by_lens"]["SEL"]["own_rate"] == 1.0
    assert out["by_lens"]["SEL"]["control_rate"] == 1.0
    assert out["by_lens"]["SEL"]["flag"] is True


def test_other_source_only_excludes_a_marked_sentence_from_the_seeds_own_source():
    # The straw-man bug this replaces (task 2): 17/22 of PLC's old closures cited only the seed or
    # its own source. A CLOSES_HERE-marked sentence from the SAME source as the seed must never
    # count toward "other-source" evidence, even though it is a different claim.
    seed = a_claim("Diagnostic tests should be selected based on failure likelihood.",
                   source_id="src-shared", independence_key="k1")
    same_source_other = a_claim(
        "A related note from the same source.",
        exact="CLOSES_HERE: choose the test whose failure likelihood is highest.",
        source_id="src-shared", independence_key="k1")  # same source identifier as `seed`
    other_candidate = a_claim("Sampling rate should be selected based on the suspected event.",
                              source_id="src-2")
    lg = ledger([seed, same_source_other, other_candidate, *fillers(40)])
    idx = link.build_index(lg)
    cands = [c for c in lenses.run_all(lg, idx, link.SETTING_1) if c.lens == "SEL"]
    seed_cand = next(c for c in cands if c.seeds == frozenset({seed.claim_id}))
    stems, ids, _q, _t = semantic.primary_probe(lg, seed_cand)
    ret = semantic.retrieve(idx, ids, stems)
    # Confirm the same-source claim is actually retrieved (scores >= 1 on the seed's stems) --
    # otherwise the assertions below would pass for the wrong reason (nothing retrieved at all).
    assert same_source_other.claim_id in {cid for _id, cid, _s in ret.a_items}
    out = checks.mismatched_evidence_control(lg, "ledgersha", idx, FakeJudge(), cands)
    # own_rate would be 1.0 if the same-source marked sentence leaked into "other"; it must not.
    assert out["by_lens"]["SEL"]["own_rate"] < 1.0
    assert out["by_lens"]["SEL"]["other_source_only_rate"] < 1.0


def test_nearest_other_picks_the_max_seed_stem_jaccard_candidate():
    stems = [frozenset({"a", "b"}), frozenset({"a"}), frozenset({"a", "b", "c"})]
    gap_ids = ["g-2", "g-0", "g-1"]
    # 0 vs 1: jaccard({a,b},{a}) = 0.5; 0 vs 2: jaccard({a,b},{a,b,c}) = 2/3 -> 2 wins.
    assert checks._nearest_other(0, stems, gap_ids) == 2


def test_nearest_other_ties_broken_by_the_smaller_gap_id():
    stems = [frozenset({"a"}), frozenset({"a"}), frozenset({"a"})]
    gap_ids = ["g-z", "g-a", "g-m"]
    # Every pair ties at jaccard 1.0; among {g-a (index 1), g-m (index 2)}, g-a sorts first.
    assert checks._nearest_other(0, stems, gap_ids) == 1


def test_own_minus_control_at_least_020_is_informative_not_flagged():
    # A 3-candidate construction where only ONE candidate's own foreign evidence is marked, and
    # the other two are each other's nearest neighbour (so neither donates the marked evidence
    # into any control arm): own_rate = 1/3, control_rate = 0, own - control = 1/3 >= 0.20.
    seed_i = a_claim("Diagnostic tests should be selected based on failure likelihood.",
                     source_id="s-i", independence_key="k-i")
    foreign_i = a_claim("Selection practice for failure likelihood is documented.",
                        exact="CLOSES_HERE: choose the test whose failure likelihood is highest.",
                        source_id="s-i-f", independence_key="k-i-f")
    seed_j = a_claim("Sampling rate should be selected based on the suspected event.",
                     source_id="s-j", independence_key="k-j")
    foreign_j = a_claim("Sampling rate selection practice is documented for the suspected event.",
                        source_id="s-j-f", independence_key="k-j-f")
    seed_k = a_claim("Sampling interval should be selected based on the suspected event.",
                     source_id="s-k", independence_key="k-k")
    foreign_k = a_claim("Sampling interval selection guidance is documented for the suspected event.",
                        source_id="s-k-f", independence_key="k-k-f")
    # Fillers dilute the common-stem cut (spec §1.3): with too few claims, virtually every content
    # word clears the 5% "common" threshold and `closure_seed_stems` ends up empty for everyone.
    lg = ledger([seed_i, foreign_i, seed_j, foreign_j, seed_k, foreign_k, *fillers(40)])
    idx = link.build_index(lg)
    cands = [c for c in lenses.run_all(lg, idx, link.SETTING_1) if c.lens == "SEL"]
    assert len(cands) == 3
    out = checks.mismatched_evidence_control(lg, "ledgersha", idx, FakeJudge(), cands)
    row = out["by_lens"]["SEL"]
    assert row["own_rate"] - row["control_rate"] >= 0.20
    assert row["flag"] is False
