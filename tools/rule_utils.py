import yaml
import glob
import os

STRIP_FIELDS = [
    "schema_version",
    "metadata",
]

def load_rule(filepath):
    with open(filepath, "r") as f:
        return yaml.safe_load(f)

def load_rule_raw(filepath):
    with open(filepath, "r") as f:
        return f.read()

def build_payload(rule, enabled_override=None):
    payload = {
        k: v for k, v in rule.items()
        if k not in STRIP_FIELDS
    }
    if enabled_override is not None:
        payload["enabled"] = enabled_override
    payload["actions"] = []
    return payload

def get_staging_rules():
    return sorted([
        f for f in glob.glob("rules/staging/*.yml")
        if ".gitkeep" not in f
    ])

def get_prod_rules(folder):
    return sorted([
        f for f in glob.glob(f"{folder}/*.yml")
        if ".gitkeep" not in f
    ])
