import json
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Literal

type Outcome = Literal["passed", "failed", "cantTell"]


@dataclass(frozen=True)
class ClerkResult:
    test_file: str
    test_case: str
    outcome: Outcome
    messages: list[str]


class MissingReport(Exception):
    pass


def read_clerk_report(stdout: str, repository_root: PurePosixPath) -> list[ClerkResult]:
    """Read the report that `clerk test --json` prints after the build output."""
    lines = [line for line in stdout.splitlines() if line.startswith("{")]
    if not lines:
        raise MissingReport("clerk printed no test report")
    report = json.loads(lines[-1])
    results = []
    for test_file in report["test-results"]:
        path = PurePosixPath(test_file["file"]).relative_to(repository_root).as_posix()
        for scope in test_file["tests"]["scopes"]:
            results.append(ClerkResult(
                test_file=path,
                test_case=scope["scope_name"],
                outcome="passed" if scope["success"] else "failed",
                messages=[error["message"] for error in scope["errors"]],
            ))
        # clerk gives no name to an inline test, only the command that runs it
        for index, inline_test in enumerate(test_file["tests"]["inline-tests"], start=1):
            results.append(ClerkResult(
                test_file=path,
                test_case=f"inline test {index}",
                outcome="passed" if inline_test["success"] else "failed",
                messages=[],
            ))
    return results
