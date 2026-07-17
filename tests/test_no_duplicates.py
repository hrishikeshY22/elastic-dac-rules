import yaml
import glob
import sys

def main():
    failed = 0

    staging = sorted([
        f for f in glob.glob("rules/staging/*.yml")
        if ".gitkeep" not in f
    ])

    seen = {}
    for filepath in staging:
        rule = yaml.safe_load(open(filepath))
        rid  = rule.get("rule_id", "")
        name = rule.get("name", filepath)
        if rid in seen:
            print(f"DUPLICATE in staging: {name}")
            print(f"  rule_id also in: {seen[rid]}")
            failed += 1
        else:
            seen[rid] = filepath
            print(f"UNIQUE: {name}")

    prod_seen = {}
    for folder in ["rules/prod/enabled", "rules/prod/disabled"]:
        for filepath in glob.glob(f"{folder}/*.yml"):
            if ".gitkeep" in filepath:
                continue
            rule = yaml.safe_load(open(filepath))
            rid  = rule.get("rule_id", "")
            name = rule.get("name", filepath)
            if rid in prod_seen:
                print(f"DUPLICATE in prod: {name}")
                print(f"  rule_id also in: {prod_seen[rid]}")
                failed += 1
            else:
                prod_seen[rid] = filepath

    print(f"\nDuplicates found: {failed}")
    sys.exit(1 if failed > 0 else 0)

if __name__ == "__main__":
    main()
