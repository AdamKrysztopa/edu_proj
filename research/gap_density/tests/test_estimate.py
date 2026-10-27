"""The survey's $0 cost estimate: the corpus rule, unit costs read from D1's spend records, and how
many codebases a cap covers. No model, no network."""
import pytest

import estimate as est


def test_corpus_rule_keeps_user_facing_prose_and_drops_process_files():
    tree = [("README.md", 6000), ("docs/guide.md", 9000), ("docs/api.rst", 500), ("llms.txt", 1600),
            ("docs/plan/v1_plan.md", 90000), ("docs/archive/done/old.md", 5000), ("CHANGELOG.md", 8000),
            ("docs/changelog.rst", 4000), (".github/pull_request_template.md", 2500),
            (".claude/skills/x/SKILL.md", 3000), ("notebooks/demo.ipynb", 400000),
            ("tests/fixtures/expected/README.md", 2600), ("docs/superpowers/plans/p.md", 7000),
            ("CONTRIBUTING.md", 3000), ("docs/contributing.rst", 7000), ("notes.txt", 700),
            ("data/lorenz.txt", 19000), ("docs/html/_sources/index.rst.txt", 1100)]
    assert sorted(p for p, _ in est.user_docs(tree)) == ["README.md", "docs/api.rst", "docs/guide.md", "llms.txt"]


def test_corpus_takes_at_most_d1s_owner_count_largest_truncated_first():
    tree = [(f"docs/p{i:02d}.md", 1000 * i) for i in range(1, 21)]
    chosen = est.choose_owner_docs(tree)
    assert len(chosen) == est.OWNER_DOCS_MAX == 16
    assert min(s for _, s in chosen) == 5000


def test_truncated_chars_cap_each_document():
    assert est.truncated([("a", 30000), ("b", 500)]) == est.MAX_DOC_CHARS + 500


def test_unit_costs_read_from_d1_records():
    u = est.unit_costs()
    assert u["toptier_ledger_observed_usd"] == pytest.approx(3.955, abs=0.01)
    # 761 of its 802 cross-verifications, 32 verifications and all 30 decoys ended in api_error.
    assert u["toptier_ledger_usd"] > 6.0
    assert u["cheap_ledger_observed_usd"] == pytest.approx(1.501, abs=0.01)
    assert u["cheap_ledger_full_usd"] > u["cheap_ledger_observed_usd"]
    assert u["gemma_two_maps_usd"] == pytest.approx(0.234, abs=0.01)
    assert u["d1_docs"] == 26
    assert u["d1_truncated_chars"] > 0


def test_per_codebase_estimate_reproduces_d1_at_d1s_size():
    u = est.unit_costs()
    full = est.codebase_usd(u["d1_truncated_chars"], u, variant="d1")
    assert full == pytest.approx(u["toptier_ledger_usd"] + u["cheap_ledger_full_usd"]
                                 + u["gemma_two_maps_usd"] + u["sol_two_maps_usd"])
    assert est.codebase_usd(u["d1_truncated_chars"], u, variant="toptier-ledger-only") < full


def test_fit_counts_cheapest_first_under_the_cap():
    assert est.fit({"a": 1.5, "b": 3.0, "c": 1.0}, cap=2.6) == ["c", "a"]
    assert est.fit({"a": 5.0}, cap=4.0) == []
