#!/usr/bin/env python3
"""Deterministic policy helpers for .github/workflows/auto-merge.yml.

The workflow runs the trusted default-branch copy of this file and never checks
out PR code. Subcommands print `key=value` lines meant for $GITHUB_OUTPUT, and
append human-readable reasons for withholding a merge to the file named by the
REASONS_FILE environment variable (default /tmp/reasons.txt).

    inspect              PR JSON on stdin (gh pr view --json ...)
    diff DIFF SCAN_OUT   PR diff -> protected-path check + text for the content scan
    verdict SCAN_FILE    model result in $RESULT, $OUTCOME -> pass/flag
"""

from __future__ import annotations

import json
import os
import re
import sys

BASE_BRANCH = "main"
DEPENDABOT_LOGINS = {"dependabot[bot]", "app/dependabot"}
# `claude/issue-N` PRs come from the issue factory and always get a human review.
FACTORY_BRANCH = re.compile(r"^claude/issue-\d+(-\d+)?$")
REPAIR_HEADLINE = "fix: repair Dependabot PR checks"

# Owner PRs touching these are not auto-merged: a merge deploys the site, and
# these paths control CI, agent behaviour, dependencies and the domain.
PROTECTED = re.compile(
    r"^(\.github/|\.claude/|\.well-known/|CLAUDE\.md$|AGENTS\.md$|hugo\.toml$|"
    r"requirements\.txt$|CNAME$)"
)

MAX_SCAN_CHARS = 200_000

LOCKFILES = {
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "poetry.lock",
    "Pipfile.lock",
    "go.sum",
    "Cargo.lock",
}
SKIP_DIRS = ("public/", "resources/")
BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".ico", ".bmp", ".tiff",
    ".pdf", ".zip", ".gz", ".tar", ".woff", ".woff2", ".ttf", ".otf", ".eot",
    ".mp3", ".mp4", ".mov", ".webm", ".parquet", ".db", ".sqlite",
}  # fmt: skip

CATEGORIES = {"spam", "sexual", "hate", "harassment", "profanity", "other"}


def reasons_file() -> str:
    return os.environ.get("REASONS_FILE", "/tmp/reasons.txt")


def add_reason(reason: str) -> None:
    with open(reasons_file(), "a", encoding="utf-8") as fh:
        fh.write(reason.strip() + "\n")


def safe(text: str) -> str:
    """Keep only characters that are harmless in a comment or output line."""
    return re.sub(r"[^\w./@+-]", "?", text)[:200]


# --- inspect -----------------------------------------------------------------


def _commit_author(commit: dict) -> str:
    authors = commit.get("authors") or []
    return (authors[0].get("login") or "") if authors else ""


def is_major_or_unknown(commits: list[dict]) -> bool:
    """Dependabot records each bump as `update-type: version-update:semver-X`."""
    body = "\n".join(c.get("messageBody") or "" for c in commits)
    types = set(re.findall(r"update-type: version-update:semver-([a-z]+)", body))
    return not types or "major" in types


def inspect(pr: dict, owner: str) -> dict:
    """Decide who the PR is from, whether it can merge now, and what needs a human."""
    author = (pr.get("author") or {}).get("login") or ""
    head = pr.get("headRefName") or ""
    commits = pr.get("commits") or []
    same_repo = pr.get("isCrossRepository") is False

    actor = "ignore"
    if same_repo and author in DEPENDABOT_LOGINS:
        actor = "dependabot"
    elif (
        same_repo
        and author.lower() == owner.lower()
        and commits
        and all(_commit_author(c).lower() == owner.lower() for c in commits)
    ):
        actor = "owner"

    blockers = []
    if pr.get("isDraft"):
        blockers.append("draft")
    if pr.get("state") != "OPEN":
        blockers.append("not open")
    if pr.get("baseRefName") != BASE_BRANCH:
        blockers.append("does not target main")
    if pr.get("mergeable") == "CONFLICTING":
        blockers.append("merge conflicts")
    if pr.get("reviewDecision") == "CHANGES_REQUESTED":
        blockers.append("changes requested")

    reasons = []
    if actor == "owner" and FACTORY_BRANCH.match(head):
        reasons.append("it was opened by the issue factory, which always gets a human review")
    if actor == "dependabot":
        if is_major_or_unknown(commits):
            reasons.append("it is a major version bump (or has no recognisable update metadata)")
        if any(c.get("messageHeadline") == REPAIR_HEADLINE for c in commits):
            reasons.append("it was modified by the automated Dependabot repair bot")

    return {
        "actor": actor,
        "eligible": actor != "ignore" and not blockers,
        "blockers": blockers,
        "reasons": reasons,
        "head_sha": pr.get("headRefOid") or "",
        "labelled": any(
            (label or {}).get("name") == "needs-review" for label in pr.get("labels") or []
        ),
    }


# --- diff --------------------------------------------------------------------

_HUNK = re.compile(r"^@@ -\d+(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def _unquote(path: str) -> str:
    path = path.split("\t")[0].strip()
    if path.startswith('"') and path.endswith('"'):
        path = path[1:-1]
    return path


def parse_diff(diff: str) -> tuple[set[str], dict[str, list[tuple[int, str]]]]:
    """Return (all touched paths, added lines per path as (line number, text))."""
    paths: set[str] = set()
    added: dict[str, list[tuple[int, str]]] = {}
    current: str | None = None
    old_left = new_left = 0
    new_line = 0

    for raw in diff.split("\n"):
        if old_left > 0 or new_left > 0:  # inside a hunk; counts say where it ends
            if raw.startswith("+"):
                if current is not None:
                    added.setdefault(current, []).append((new_line, raw[1:]))
                new_line += 1
                new_left -= 1
            elif raw.startswith("-"):
                old_left -= 1
            elif raw.startswith("\\"):
                pass
            else:
                new_line += 1
                old_left -= 1
                new_left -= 1
            continue

        if raw.startswith("diff --git "):
            current = None
            m = re.match(r"^diff --git a/(.+) b/(.+)$", raw)
            if m:
                paths.update({_unquote(m.group(1)), _unquote(m.group(2))})
        elif raw.startswith(("rename from ", "rename to ")):
            paths.add(_unquote(raw.split(" ", 2)[2]))
        elif raw.startswith("--- a/"):
            paths.add(_unquote(raw[6:]))
        elif raw.startswith("+++ b/"):
            current = _unquote(raw[6:])
            paths.add(current)
        elif raw.startswith("+++ "):  # /dev/null: deleted file
            current = None
        elif (m := _HUNK.match(raw)) is not None:
            old_left = int(m.group(1)) if m.group(1) is not None else 1
            new_left = int(m.group(3)) if m.group(3) is not None else 1
            new_line = int(m.group(2))
    return paths, added


def scannable(path: str) -> bool:
    name = path.rsplit("/", 1)[-1]
    if name in LOCKFILES or path.startswith(SKIP_DIRS):
        return False
    ext = os.path.splitext(name)[1].lower()
    if ext in BINARY_EXTENSIONS:
        return False
    return not (ext == ".csv" and "data" in path.split("/")[:-1])


def build_scan(added: dict[str, list[tuple[int, str]]]) -> str:
    chunks = []
    for path in sorted(added):
        if not scannable(path):
            continue
        lines = [
            f"L{n}: {text}"
            for n, text in added[path]
            if text.strip() and not text.startswith("Subproject commit")
        ]
        if lines:
            chunks.append(f"=== FILE: {path}\n" + "\n".join(lines))
    return "\n\n".join(chunks)


def analyse_diff(diff: str) -> dict:
    paths, added = parse_diff(diff)
    protected = sorted(p for p in paths if PROTECTED.match(p))
    scan = build_scan(added)
    reasons = []
    if protected:
        shown = ", ".join(safe(p) for p in protected[:5])
        more = f" (+{len(protected) - 5} more)" if len(protected) > 5 else ""
        reasons.append(f"it touches protected paths: {shown}{more}")
    if len(scan) > MAX_SCAN_CHARS:
        reasons.append(
            f"its added text ({len(scan)} characters) is too large to scan completely"
        )
    return {"reasons": reasons, "scan": scan}


# --- verdict -----------------------------------------------------------------


def scanned_files(scan_text: str) -> set[str]:
    return set(re.findall(r"^=== FILE: (.+)$", scan_text, flags=re.MULTILINE))


def evaluate_verdict(outcome: str, result: str, scan_text: str) -> list[str]:
    """Return the reasons to withhold the merge; an empty list means the scan passed.

    Anything other than a well-formed `pass` is a flag, so the scan fails closed.
    Only enum values and file:line locations from the scanned diff are echoed back,
    never free text from the model.
    """
    if outcome != "success":
        return ["the content scan did not complete, so the text could not be checked"]
    try:
        data = json.loads(result)
        verdict = data["verdict"]
        findings = data.get("findings") or []
    except (TypeError, ValueError, KeyError):
        return ["the content scan returned an unreadable result"]
    if verdict == "pass" and not findings:
        return []
    if verdict != "flag" and verdict != "pass":
        return ["the content scan returned an unreadable result"]

    files = scanned_files(scan_text)
    out = []
    for item in findings[:10] if isinstance(findings, list) else []:
        if not isinstance(item, dict):
            continue
        category = item.get("category")
        category = category if category in CATEGORIES else "other"
        path = item.get("file")
        line = item.get("line")
        where = ""
        if isinstance(path, str) and path in files and isinstance(line, int):
            where = f" at {safe(path)}:{line}"
        out.append(f"the content scan flagged possible {category} text{where}")
    return out or ["the content scan flagged text that may not suit a personal blog"]


# --- CLI ---------------------------------------------------------------------


def _emit(**kwargs: object) -> None:
    for key, value in kwargs.items():
        if isinstance(value, bool):
            value = "true" if value else "false"
        print(f"{key}={value}")


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else ""
    if cmd == "inspect":
        owner = os.environ["OWNER_LOGIN"]
        info = inspect(json.load(sys.stdin), owner)
        for reason in info["reasons"]:
            add_reason(reason)
        _emit(
            actor=info["actor"],
            eligible=info["eligible"],
            flagged=bool(info["reasons"]),
            blockers=",".join(info["blockers"]),
            head_sha=info["head_sha"],
            already_flagged=info["labelled"],
        )
    elif cmd == "diff":
        with open(argv[2], encoding="utf-8", errors="replace") as fh:
            result = analyse_diff(fh.read())
        for reason in result["reasons"]:
            add_reason(reason)
        with open(argv[3], "w", encoding="utf-8") as fh:
            fh.write(result["scan"])
        _emit(scan=bool(result["scan"]) and not result["reasons"])
    elif cmd == "verdict":
        with open(argv[2], encoding="utf-8") as fh:
            scan_text = fh.read()
        reasons = evaluate_verdict(
            os.environ.get("OUTCOME", ""), os.environ.get("RESULT", ""), scan_text
        )
        for reason in reasons:
            add_reason(reason)
        _emit(passed=not reasons)
    else:
        print(__doc__, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
