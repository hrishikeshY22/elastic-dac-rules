# tests/test_severity_risk.py
# Warn if severity and risk_score don't match recommended mapping

import yaml
import glob
import sys

RECOMMENDED = {
    "low":      21,
    "medium":   47,
    "high":     73,
    "critical": 99,
}


def test_severity_risk():
    rules = sorted([
        f for f in glob.glob("rules/staging/*.yml")
        if ".gitkeep" not in f
    ])

    if not rules:
        print("No rules in staging — skipping")
        sys.exit(0)

    for filepath in rules:
        rule = yaml.safe_load(open(filepath))
        name = rule.get("name", filepath)
        sev  = rule.get("severity", "")
        risk = rule.get("risk_score", 0)

        if sev in RECOMMENDED and risk != RECOMMENDED[sev]:
            print(f"WARN: {name}")
            print(f"  severity={sev} → "
                  f"recommended risk_score={RECOMMENDED[sev]}, "
                  f"got {risk}")
        else:
            print(f"PASS: {name} [{sev}/{risk}]")

    # Warning only — never block the pipeline
    sys.exit(0)


if __name__ == "__main__":
    test_severity_risk()

