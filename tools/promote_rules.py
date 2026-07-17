import os
import shutil
import subprocess
import sys
sys.path.insert(0, os.path.dirname(__file__))
from rule_utils import load_rule

def get_changed_staging_files():
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD",
         "--", "rules/staging/*.yml"],
        capture_output=True, text=True
    )
    return [
        f.strip() for f in
        result.stdout.strip().split("\n")
        if f.strip().endswith(".yml")
        and ".gitkeep" not in f
    ]

def promote_rule(src):
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
    print(f"PROMOTED: {fname} → prod/{folder}/")
    return dest

def git_commit_promoted(promoted_files):
    subprocess.run(["git", "config", "user.name",
        "elastic-dac-pipeline[bot]"])
    subprocess.run(["git", "config", "user.email",
        "elastic-dac-pipeline[bot]@users.noreply.github.com"])
    subprocess.run(["git", "add", "rules/prod/"])
    subprocess.run(["git", "commit", "-m",
        f"chore: promote {len(promoted_files)} rule(s) to prod"])
    subprocess.run(["git", "push", "origin", "main"])

def main():
    print("=" * 50)
    print("PROMOTE RULES")
    print("=" * 50)

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

    print(f"\nPromoted: {len(promoted)} rule(s)")

    if promoted:
        git_commit_promoted(promoted)
        print("Committed and pushed")

if __name__ == "__main__":
    main()
