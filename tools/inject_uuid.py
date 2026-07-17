# tools/inject_uuid.py
# Called by uuid-inject.yml
# Finds staging rules with empty rule_id and injects UUID4

import uuid
import re
import sys
from rule_utils import load_rule, load_rule_raw, get_rule_files


def inject_uuid(filepath):
    """
    Inject UUID4 into rule_id: "" field.
    Preserves all file formatting and comments.
    Returns (injected: bool, new_uuid: str)
    """
    content = load_rule_raw(filepath)
    rule    = load_rule(filepath)

    rule_id = rule.get("rule_id", "")

    # Skip if rule_id already has a value
    if rule_id and str(rule_id).strip() != "":
        return False, rule_id

    new_uuid = str(uuid.uuid4())

    # Replace rule_id: "" preserving formatting
    updated = re.sub(
        r'^(rule_id:\s*)"[^"]*"',
        f'\\1"{new_uuid}"',
        content,
        flags=re.MULTILINE
    )

    if updated == content:
        print(f"WARN: rule_id line not found in {filepath}")
        return False, ""

    with open(filepath, "w") as f:
        f.write(updated)

    return True, new_uuid


def main():
    rules     = get_rule_files("rules/staging")
    injected  = []

    for filepath in rules:
        rule      = load_rule(filepath)
        name      = rule.get("name", filepath)
        did_inject, new_uuid = inject_uuid(filepath)

        if did_inject:
            print(f"INJECTED: {name}")
            print(f"  UUID:  {new_uuid}")
            print(f"  File:  {filepath}")
            injected.append(filepath)
        else:
            print(f"SKIP:     {name} (UUID already present)")

    print()
    print(f"Total injected: {len(injected)}")

    if not injected:
        sys.exit(0)

    # Signal to workflow that files were changed
    sys.exit(0)


if __name__ == "__main__":
    main()

