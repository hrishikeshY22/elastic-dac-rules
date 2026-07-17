# tests/test_schema.py
# Validate all staging rules against rule.schema.json

import yaml
import json
import glob
import sys
import jsonschema


def test_schema():
    schema = json.load(open("schemas/rule.schema.json"))
    rules  = sorted([
        f for f in glob.glob("rules/staging/*.yml")
        if ".gitkeep" not in f
    ])

    if not rules:
        print("No rules in staging — skipping")
        sys.exit(0)

    passed = failed = 0
    for filepath in rules:
        rule = yaml.safe_load(open(filepath))
        name = rule.get("name", filepath)
        try:
            jsonschema.validate(rule, schema)
            print(f"PASS: {name}")
            passed += 1
        except jsonschema.ValidationError as e:
            print(f"FAIL: {name}")
            print(f"  {e.message}")
            failed += 1

    print(f"\nPassed: {passed} | Failed: {failed}")
    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    test_schema()

