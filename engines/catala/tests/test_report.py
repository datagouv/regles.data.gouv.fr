import json
from pathlib import Path, PurePosixPath

import pytest

from engine_catala.report import ClerkResult, MissingReport, read_clerk_report

ROOT = PurePosixPath("/home/opam/prestagri")
# stdout of `clerk test --json` in the catala/ folder of Prest'Agri at commit 478b3cc, checked out in /home/opam/prestagri
STDOUT = (Path(__file__).parent / "fixtures" / "clerk-test-478b3cc.log").read_text()


def test_each_test_scope_gives_a_result_with_its_file_in_the_repository():
    results = read_clerk_report(STDOUT, ROOT)

    assert len(results) == 27
    assert [result for result in results if result.outcome == "failed"] == [
        ClerkResult(
            test_file="catala/tests/commun/tests_quotient_familial.catala_fr",
            test_case="TestQuotientFamilial4",
            outcome="failed",
            messages=["Assertion failed: 434,67 € ≠ 434,66 €"],
        ),
    ]


def test_an_inline_test_is_named_by_its_rank_in_its_file():
    report = {"test-results": [{
        "file": "/home/opam/prestagri/catala/tests/inline.catala_fr",
        "tests": {"scopes": [], "inline-tests": [{"cmd": "catala interpret", "success": True}, {"cmd": "catala interpret", "success": False}]},
    }]}

    assert read_clerk_report(json.dumps(report), ROOT)[1] == ClerkResult(
        test_file="catala/tests/inline.catala_fr", test_case="inline test 2", outcome="failed", messages=[],
    )


def test_an_output_without_report_is_refused():
    with pytest.raises(MissingReport):
        read_clerk_report("ninja: build stopped: subcommand failed.\n", ROOT)
