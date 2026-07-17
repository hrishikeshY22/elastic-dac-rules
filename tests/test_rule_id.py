import yaml
import glob
import sys
import re

UUID_PATTERN = (
    r'^[0-9a-f]{8}-[0-9a-f]{4}-'
    r'[0-9a-f]{4}-[0-9a-f]{4}-'
    r'[0-9a-f]{12}$'
)

def main():
    rules = sorted([
        f for f in glob.glob("rules/staging/*.yml")
        if ".gitkeep" not in f
    ])

    if not rules:
        print("No rules in staging — skipping")
        sys.exit(0)

    failed = 0
    for filepath in rules:
        rule    = yaml.safe_load(open(filepath))
        name    = rule.get("name", filepath)
        rule_id = str(rule.get("rule_id", "")).strip()

        if not rule_id or rule_id == "":
            print(f"FAIL: {name}")
            print(f"  rule_id is empty — uuid-inject may still be running")
            failed += 1
        elif not re.match(UUID_PATTERN, rule_id):
            print(f"FAIL: {name}")
            print(f"  '{rule_id}' is not a valid UUID4")
            failed += 1
        else:
            print(f"PASS: {name}")
            print(f"  rule_id: {rule_id}")

    print(f"\nFailed: {failed}")
    sys.exit(1 if failed > 0 else 0)

if __name__ == "__main__":
    main()
