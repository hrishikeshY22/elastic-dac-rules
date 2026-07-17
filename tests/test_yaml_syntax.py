import yaml
import glob
import sys

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
        try:
            yaml.safe_load(open(filepath))
            print(f"PASS: {filepath}")
        except yaml.YAMLError as e:
            print(f"FAIL: {filepath}")
            print(f"  {e}")
            failed += 1

    print(f"\nPassed: {len(rules) - failed} | Failed: {failed}")
    sys.exit(1 if failed > 0 else 0)

if __name__ == "__main__":
    main()
