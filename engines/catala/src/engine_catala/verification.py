import argparse
import json
import re
import subprocess
import tempfile
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath

from engine_catala.report import MissingReport, Outcome, read_clerk_report

COMMIT = re.compile(r"[0-9a-f]{40}")
IMAGE = "engine-catala"
CONTAINER_REPOSITORY = PurePosixPath("/home/opam/repository")
CLERK_TIMEOUT_SECONDS = 1800
TIMEOUT_EXIT_CODE = 124
CLERK_TEST = f'mkdir {CONTAINER_REPOSITORY} && tar -x -C {CONTAINER_REPOSITORY} && cd {CONTAINER_REPOSITORY}/"$1" && timeout {CLERK_TIMEOUT_SECONDS} clerk test --json'


@dataclass(frozen=True)
class Finding:
    source_repository: str
    source_commit: str
    test_file: str | None
    test_case: str | None
    outcome: Outcome
    messages: list[str]


def cited_commits(data: Path) -> list[tuple[str, str]]:
    """List the distinct repositories and commits that the records of `data` cite."""
    cited = set()
    for path in data.rglob("*.json"):
        for record in json.loads(path.read_text()):
            repository, commit = record.get("source_repository"), record.get("source_commit")
            if repository and commit:
                cited.add((repository, commit))
    return sorted(cited)


def git(*args: str, cwd: Path) -> bytes:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True).stdout


def cant_tell(repository: str, commit: str, message: str) -> list[Finding]:
    return [Finding(repository, commit, None, None, "cantTell", [message])]


def verify(repository: str, commit: str, workdir: Path) -> list[Finding]:
    # git runs a command for some URL schemes, such as ext::
    if not repository.startswith("https://") or not COMMIT.fullmatch(commit):
        return cant_tell(repository, commit, "the record cites a repository that is not an https URL, or a commit that is not a full hash")
    git("init", "--quiet", cwd=workdir)
    try:
        git("fetch", "--quiet", "--depth", "1", "--filter", "blob:none", repository, commit, cwd=workdir)
    except subprocess.CalledProcessError as error:
        return cant_tell(repository, commit, f"git could not fetch the commit: {error.stderr.decode().strip()}")
    files = git("ls-tree", "-r", "--name-only", "FETCH_HEAD", cwd=workdir).decode().splitlines()
    projects = [Path(file).parent.as_posix() for file in files if Path(file).name == "clerk.toml"]
    if not projects:
        return []
    archive = git("archive", "FETCH_HEAD", cwd=workdir)

    findings = []
    for project in projects:
        # the tests run the code of the cited repository: the container has no network and receives the code on stdin
        run = subprocess.run(
            ["docker", "run", "--rm", "--interactive", "--network", "none", IMAGE, "sh", "-c", CLERK_TEST, "sh", project],
            input=archive, capture_output=True,
        )
        if run.returncode == TIMEOUT_EXIT_CODE:
            findings += cant_tell(repository, commit, f"clerk test ran for more than {CLERK_TIMEOUT_SECONDS} seconds in {project}")
            continue
        output = (run.stdout + run.stderr).decode(errors="replace")
        try:
            results = read_clerk_report(run.stdout.decode(errors="replace"), CONTAINER_REPOSITORY)
        except MissingReport:
            findings += cant_tell(repository, commit, f"clerk test printed no report in {project}: {output.strip()[-2000:]}")
            continue
        findings += [Finding(repository, commit, **asdict(result)) for result in results]
    return findings


def summarize(findings: list[Finding]) -> str:
    lines = ["## Tests natifs Catala", ""]
    for repository, commit in sorted({(f.source_repository, f.source_commit) for f in findings}):
        own = [f for f in findings if (f.source_repository, f.source_commit) == (repository, commit)]
        counts = {outcome: sum(f.outcome == outcome for f in own) for outcome in ("passed", "failed", "cantTell")}
        lines.append(f"- {repository} au commit `{commit[:7]}`. Réussis : {counts['passed']}, "
                     f"en échec : {counts['failed']}, non exécutés : {counts['cantTell']}.")
        for finding in own:
            if finding.outcome != "passed":
                case = f"`{finding.test_file}` `{finding.test_case}` : " if finding.test_case else ""
                lines.append(f"  - {case}{' '.join(finding.messages)}")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the native Catala tests of the repositories cited by the records")
    parser.add_argument("data", type=Path, help="folder of the record files")
    parser.add_argument("--output", type=Path, required=True, help="JSON file to write the findings to")
    parser.add_argument("--summary", type=Path, help="Markdown file to append a summary of the findings to")
    args = parser.parse_args()

    engine_version = subprocess.run(
        ["docker", "run", "--rm", IMAGE, "catala", "--version"], check=True, capture_output=True, text=True,
    ).stdout.strip()
    findings = []
    for repository, commit in cited_commits(args.data):
        with tempfile.TemporaryDirectory() as workdir:
            try:
                findings += verify(repository, commit, Path(workdir))
            # the findings of the other repositories are kept
            except Exception as error:
                findings += cant_tell(repository, commit, f"the adapter failed: {error!r}")
    args.output.write_text(json.dumps({
        "engine": "catala",
        "engine_version": engine_version,
        "verified_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "findings": [asdict(finding) for finding in findings],
    }, ensure_ascii=False, indent=2) + "\n")
    if args.summary:
        with args.summary.open("a") as summary:
            summary.write(summarize(findings))
