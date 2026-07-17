# tools/rule_utils.py
# Shared utilities for DaC pipeline tools

import yaml
import json
import os

# Fields stripped before sending to Elastic API
STRIP_FIELDS = [
    "schema_version",
    "metadata",
]

def load_rule(filepath):
    """Load and parse a YAML rule file."""
    with open(filepath, "r") as f:
        return yaml.safe_load(f)

def load_rule_raw(filepath):
    """Load raw text content of a rule file."""
    with open(filepath, "r") as f:
        return f.read()

def build_payload(rule, enabled=None):
    """
    Strip DaC-internal fields and build
    the payload to send to Elastic API.
    enabled parameter overrides the rule's enabled field.
    """
    payload = {
        k: v for k, v in rule.items()
        if k not in STRIP_FIELDS
    }
    if enabled is not None:
        payload["enabled"] = enabled
    payload["actions"] = []
    return payload

def get_rule_files(folder, recursive=False):
    """
    Return all .yml rule files in a folder.
    Excludes .gitkeep files.
    """
    import glob
    pattern = (
        f"{folder}/**/*.yml"
        if recursive
        else f"{folder}/*.yml"
    )
    return sorted([
        f for f in glob.glob(pattern, recursive=recursive)
        if ".gitkeep" not in f
    ])

def print_separator(title=""):
    """Print a section separator."""
    print("=" * 55)
    if title:
        print(title)
        print("=" * 55)

