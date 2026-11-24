"""Tests for the auto-merge policy helpers in .github/scripts/pr_policy.py."""

import importlib.util
import json
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / ".github" / "scripts" / "pr_policy.py"
spec = importlib.util.spec_from_file_location("pr_policy", SCRIPT)
pr_policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pr_policy)

OWNER = "kelvinn"


def commit(login=OWNER, headline="Add post", body=""):
    return {
        "authors": [{"login": login}, {"login": "claude"}],  # co-author trailer
        "messageHeadline": headline,
        "messageBody": body,
    }


def pr(**overrides):
    base = {
        "author": {"login": OWNER},
        "baseRefName": "main",
        "headRefName": "claude/new-post",
        "headRefOid": "abc123",
        "isCrossRepository": False,
        "isDraft": False,
        "state": "OPEN",
        "mergeable": "MERGEABLE",
        "reviewDecision": "",
        "labels": [],
        "commits": [commit()],
    }
    base.update(overrides)
    return base


# --- inspect -----------------------------------------------------------------


def test_owner_pr_is_eligible():
    info = pr_policy.inspect(pr(), OWNER)
    assert info["actor"] == "owner"
    assert info["eligible"] is True
    assert info["reasons"] == []


def test_other_authors_are_ignored():
    assert pr_policy.inspect(pr(author={"login": "mybuddyassistant"}), OWNER)["actor"] == "ignore"


def test_fork_pr_is_ignored_even_with_owner_name():
    assert pr_policy.inspect(pr(isCrossRepository=True), OWNER)["actor"] == "ignore"


def test_foreign_commit_on_owner_pr_is_ignored():
    commits = [commit(), commit(login="someone-else")]
    assert pr_policy.inspect(pr(commits=commits), OWNER)["actor"] == "ignore"


def test_owner_pr_without_commits_is_ignored():
    assert pr_policy.inspect(pr(commits=[]), OWNER)["actor"] == "ignore"


def test_factory_branch_is_flagged():
    for head in ("claude/issue-12", "claude/issue-12-2"):
        info = pr_policy.inspect(pr(headRefName=head), OWNER)
        assert info["actor"] == "owner"
        assert info["reasons"], head


def test_non_factory_claude_branch_is_not_flagged():
    for head in ("claude/issue-build", "claude/issue-12-fix", "claude/factory-issue-build"):
        assert pr_policy.inspect(pr(headRefName=head), OWNER)["reasons"] == []


def test_blockers():
    info = pr_policy.inspect(
        pr(isDraft=True, state="CLOSED", baseRefName="dev", mergeable="CONFLICTING"), OWNER
    )
    assert info["eligible"] is False
    assert set(info["blockers"]) == {"draft", "not open", "does not target main", "merge conflicts"}


def dependabot(update_type="minor", **overrides):
    body = f"updated-dependencies:\n- dependency-name: x\n  update-type: version-update:semver-{update_type}"
    return pr(
        author={"login": "app/dependabot"},
        headRefName="dependabot/pip/x",
        commits=[{"authors": [{"login": "dependabot[bot]"}], "messageHeadline": "bump", "messageBody": body}],
        **overrides,
    )


def test_dependabot_minor_is_clean():
    info = pr_policy.inspect(dependabot("patch"), OWNER)
    assert info["actor"] == "dependabot"
    assert info["reasons"] == []


def test_dependabot_major_and_unknown_are_flagged():
    assert pr_policy.inspect(dependabot("major"), OWNER)["reasons"]
    unknown = dependabot()
    unknown["commits"][0]["messageBody"] = ""
    assert pr_policy.inspect(unknown, OWNER)["reasons"]


def test_dependabot_repair_commit_is_flagged():
    p = dependabot()
    p["commits"].append(commit(login="repair-bot", headline=pr_policy.REPAIR_HEADLINE))
    assert pr_policy.inspect(p, OWNER)["reasons"]


def test_branch_name_alone_does_not_make_dependabot():
    p = pr(author={"login": "stranger"}, headRefName="dependabot/pip/x")
    assert pr_policy.inspect(p, OWNER)["actor"] == "ignore"


# --- diff --------------------------------------------------------------------

DIFF = """\
diff --git a/content/posts/a/index.md b/content/posts/a/index.md
index 111..222 100644
--- a/content/posts/a/index.md
+++ b/content/posts/a/index.md
@@ -1,3 +1,4 @@
 # Title
-old line
+new line
+++ not a header
 tail
diff --git a/content/posts/a/chart.png b/content/posts/a/chart.png
new file mode 100644
Binary files /dev/null and b/content/posts/a/chart.png differ
diff --git a/content/posts/a/data/x.csv b/content/posts/a/data/x.csv
new file mode 100644
--- /dev/null
+++ b/content/posts/a/data/x.csv
@@ -0,0 +1,2 @@
+a,b
+1,2
diff --git a/package-lock.json b/package-lock.json
--- a/package-lock.json
+++ b/package-lock.json
@@ -1 +1 @@
-x
+y
"""


def test_scan_contains_only_added_text_with_line_numbers():
    result = pr_policy.analyse_diff(DIFF)
    scan = result["scan"]
    assert "=== FILE: content/posts/a/index.md" in scan
    assert "L2: new line" in scan
    assert "L3: ++ not a header" in scan
    assert "old line" not in scan
    assert "x.csv" not in scan and "package-lock" not in scan and "chart.png" not in scan
    assert result["reasons"] == []


def test_protected_paths_are_flagged():
    for path in (".github/workflows/x.yml", "CLAUDE.md", "AGENTS.md", "hugo.toml", "requirements.txt"):
        diff = f"diff --git a/{path} b/{path}\n--- a/{path}\n+++ b/{path}\n@@ -1 +1 @@\n-a\n+b\n"
        assert pr_policy.analyse_diff(diff)["reasons"], path


def test_content_paths_are_not_protected():
    assert pr_policy.analyse_diff(DIFF)["reasons"] == []


def test_oversized_scan_is_flagged():
    big = "x" * (pr_policy.MAX_SCAN_CHARS + 1)
    diff = f"diff --git a/a.md b/a.md\n--- a/a.md\n+++ b/a.md\n@@ -0,0 +1 @@\n+{big}\n"
    assert pr_policy.analyse_diff(diff)["reasons"]


def test_image_only_change_needs_no_scan():
    diff = "diff --git a/i.png b/i.png\nBinary files a/i.png and b/i.png differ\n"
    result = pr_policy.analyse_diff(diff)
    assert result["scan"] == "" and result["reasons"] == []


# --- verdict -----------------------------------------------------------------

SCAN = "=== FILE: content/a.md\nL4: text"


def verdict(outcome="success", **data):
    return pr_policy.evaluate_verdict(outcome, json.dumps(data), SCAN)


def test_pass_verdict():
    assert verdict(verdict="pass", findings=[]) == []


def test_flag_verdict_reports_location_and_category_only():
    out = verdict(
        verdict="flag",
        findings=[{"file": "content/a.md", "line": 4, "category": "spam", "note": "BAD WORDS"}],
    )
    assert out == ["the content scan flagged possible spam text at content/a.md:4"]


def test_unknown_category_and_file_are_neutralised():
    out = verdict(
        verdict="flag", findings=[{"file": "../../etc/passwd", "line": 1, "category": "<script>"}]
    )
    assert out == ["the content scan flagged possible other text"]


def test_pass_with_findings_is_a_flag():
    assert verdict(verdict="pass", findings=[{"file": "content/a.md", "line": 4, "category": "hate"}])


def test_scan_fails_closed():
    assert pr_policy.evaluate_verdict("failure", "", SCAN)
    assert pr_policy.evaluate_verdict("success", "", SCAN)
    assert pr_policy.evaluate_verdict("success", "not json", SCAN)
    assert pr_policy.evaluate_verdict("success", "{}", SCAN)
    assert verdict(verdict="maybe")
    assert pr_policy.evaluate_verdict("success", "[1]", SCAN)
