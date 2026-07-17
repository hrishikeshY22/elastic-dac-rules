import uuid
import re
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from rule_utils import load_rule, load_rule_raw, get_staging_rules

def inject_uuid(filepath):
    content = load_rule_raw(filepath)
    rule    = load_rule(filepath)
    rule_id = str(rule.get("rule_id", "")).strip()

    if rule_id and rule_id != "":
        return False, rule_id

    new_uuid = str(uuid.uuid4())

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
    rules    = get_staging_rules()
    injected = []

    for filepath in rules:
        rule = load_rule(filepath)
        name = rule.get("name", filepath)
        did_inject, new_uuid = inject_uuid(filepath)

        if did_inject:
            print(f"INJECTED: {name}")
            print(f"  UUID: {new_uuid}")
            print(f"  File: {filepath}")
            injected.append(filepath)
        else:
            print(f"SKIP: {name} — UUID already present")

    print(f"\nTotal injected: {len(injected)}")
    sys.exit(0)

if __name__ == "__main__":
    main()
