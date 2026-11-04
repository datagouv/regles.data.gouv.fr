import json

from engine_catala import Finding, cited_commits, summarize, verify

COMMIT = "478b3cc2ab28299c73b94fdd192b0559ae5873b8"
PRESTAGRI = "https://github.com/betagouv/prestagri"


def test_records_that_cite_the_same_commit_are_verified_once(tmp_path):
    (tmp_path / "prestagri").mkdir()
    (tmp_path / "prestagri" / "a.json").write_text(json.dumps([
        {"source_repository": PRESTAGRI, "source_commit": COMMIT},
        {"source_repository": None, "source_commit": None},
    ]))
    (tmp_path / "prestagri" / "b.json").write_text(json.dumps([
        {"source_repository": PRESTAGRI, "source_commit": COMMIT},
    ]))

    assert cited_commits(tmp_path) == [(PRESTAGRI, COMMIT)]


def test_a_repository_that_is_not_an_https_url_is_not_fetched(tmp_path):
    findings = verify("ext::sh -c touch% /tmp/pwned", COMMIT, tmp_path)

    assert [finding.outcome for finding in findings] == ["cantTell"]
    assert not (tmp_path / ".git").exists()


def test_the_summary_lists_the_cases_that_did_not_pass():
    findings = [
        Finding(PRESTAGRI, COMMIT, "catala/tests/a.catala_fr", "TestA", "passed", []),
        Finding(PRESTAGRI, COMMIT, "catala/tests/a.catala_fr", "TestB", "failed", ["Assertion failed: 434,67 € ≠ 434,66 €"]),
    ]

    assert summarize(findings) == (
        "## Tests natifs Catala\n\n"
        f"- {PRESTAGRI} au commit `478b3cc`. Réussis : 1, en échec : 1, non exécutés : 0.\n"
        "  - `catala/tests/a.catala_fr` `TestB` : Assertion failed: 434,67 € ≠ 434,66 €\n"
    )
