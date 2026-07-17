# tests/test_no_prod_edits.py
# Block PRs that directly edit rules/prod/
# rules/prod/ is managed by promote.yml only

import subprocess
import sys


def test_no_prod_edits():
    result = subprocess.run(
        ["git", "diff", "--name-only", "origin/main...HEAD"],
        capture_output=True, text=True
    )
    changed = [
        f.strip() for f in
        result.stdout.strip().split("\n")
        if f.strip()
    ]

    print("Files changed in this PR:")
    for f in changed:
        print(f"  {f}")
    print()

    prod_edits = [
        f for f in changed
        if f.startswith("rules/prod/")
        and f.endswith(".yml")
        and ".gitkeep" not in f
    ]

    if prod_edits:
        print("=" * 55)
        print("BLOCKED: Direct edits to rules/prod/ detected")
        print("=" * 55)
        for f in prod_edits:
            print(f"  FAIL: {f}")
        print()
        print("rules/prod/ is managed by promote.yml only")
        print("Edit rules/staging/ instead")
        print("See docs/lifecycle.md")
        sys.exit(1)

    print("PASS: No direct prod edits detected")
    sys.exit(0)


if __name__ == "__main__":
    test_no_prod_edits()

