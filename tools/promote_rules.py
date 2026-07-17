# tools/promote_rules.py
# Called by promote.yml
# Detects changed staging rules and copies to prod/enabled or prod/disabled

import os
import shutil
import subprocess
import sys
from rule_utils import load_rule, print_separator


def get_changed_staging_files():
    """Get staging .yml files changed in last commit."""
    result = subprocess.run(
        [
            "git", "diff", "--name-only",
            "HEAD~1", "HEAD",
            "--", "rules/staging/*.yml"
        ],
        capture_output=True, text=True
    )
    return [
        f.strip() for f in
        result.stdout.strip().split("\n")
        if f.strip().endswith(".yml")
        and ".gitkeep" not in f
    ]


def promote_rule(src):
    """
    Copy rule from staging to prod/enabled or prod/disabled
    based on the enabled: field.
    Returns destination path or None if skipped.
    """
    if not os.path.exists(src):
        print(f"SKIP: {src} — file not found")
        return None

    rule    = load_rule(src)
    enabled = rule.get("enabled", False)
    fname   = os.path.basename(src)
    dest    = (
        f"rules/prod/enabled/{fname}"
        if enabled
        else f"rules/prod/disabled/{fname}"
    )

    shutil.copy2(src, dest)
    folder = "enabled" if enabled else "disabled"
    print(f"PROMOTED: {fname}")
    print(f"  From:    {src}")
    print(f"  To:      {dest}")
    print(f"  Folder:  {folder}")
    return dest


def git_commit_promoted(promoted_files):
    """Commit and push promoted rules back to main."""
    subprocess.run([
        "git", "config", "user.name",
        "elastic-dac-pipeline[bot]"
    ])
    subprocess.run([
        "git", "config", "user.email",
        "elastic-dac-pipeline[bot]@users.noreply.github.com"
    ])
    subprocess.run(["git", "add", "rules/prod/"])
    subprocess.run([
        "git", "commit", "-m",
        f"chore: promote {len(promoted_files)} rule(s) to prod"
    ])
    subprocess.run(["git", "push", "origin", "main"])


def main():
    print_separator("PROMOTE RULES")

    changed = get_changed_staging_files()
    print(f"Changed staging files: {changed}")

    if not changed:
        print("Nothing to promote")
        sys.exit(0)

    promoted = []
    for src in changed:
        dest = promote_rule(src)
        if dest:
            promoted.append(dest)

    print()
    print(f"Promoted: {len(promoted)} rule(s)")

    if promoted:
        git_commit_promoted(promoted)
        print("Committed and pushed to main")


if __name__ == "__main__":
    main()

