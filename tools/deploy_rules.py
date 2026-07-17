import os
import sys
import glob
import requests
sys.path.insert(0, os.path.dirname(__file__))
from rule_utils import load_rule, build_payload

def get_headers(api_key):
    return {
        "Authorization": f"ApiKey {api_key}",
        "kbn-xsrf":      "true",
        "Content-Type":  "application/json",
    }

def rule_exists(kibana_url, headers, rule_id):
    resp = requests.get(
        f"{kibana_url}/api/detection_engine/rules"
        f"?rule_id={rule_id}",
        headers=headers,
    )
    return resp.status_code == 200

def deploy_rule(kibana_url, headers, payload, rule_name):
    rule_id = payload.get("rule_id", "")

    if rule_exists(kibana_url, headers, rule_id):
        resp   = requests.put(
            f"{kibana_url}/api/detection_engine/rules",
            headers=headers,
            json=payload,
        )
        action = "UPDATED"
    else:
        resp   = requests.post(
            f"{kibana_url}/api/detection_engine/rules",
            headers=headers,
            json=payload,
        )
        action = "CREATED"

    if resp.status_code in [200, 201]:
        print(f"{action}: {rule_name}")
        return True
    else:
        print(f"FAILED: {rule_name}")
        print(f"  Status:   {resp.status_code}")
        print(f"  Response: {resp.text[:300]}")
        return False

def deploy_folder(kibana_url, headers, folder, enabled_override):
    files = sorted([
        f for f in glob.glob(f"{folder}/*.yml")
        if ".gitkeep" not in f
    ])

    if not files:
        print(f"No rules found in {folder}")
        return 0, 0

    deployed = failed = 0
    for filepath in files:
        rule      = load_rule(filepath)
        rule_id   = rule.get("rule_id", "")
        rule_name = rule.get("name", filepath)

        if not rule_id:
            print(f"SKIP: {rule_name} — missing rule_id")
            continue

        payload = build_payload(rule, enabled_override=enabled_override)
        success = deploy_rule(kibana_url, headers, payload, rule_name)
        if success:
            deployed += 1
        else:
            failed += 1

    return deployed, failed

def main():
    print("=" * 50)
    print("DEPLOY RULES TO ELASTIC")
    print("=" * 50)

    kibana_url = os.environ.get("ELASTIC_PROD_URL", "")
    api_key    = os.environ.get("ELASTIC_PROD_API_KEY", "")

    if not kibana_url or not api_key:
        print("ERROR: Missing ELASTIC_PROD_URL or ELASTIC_PROD_API_KEY")
        sys.exit(1)

    print(f"Target: {kibana_url}\n")

    headers = get_headers(api_key)
    total_deployed = total_failed = 0

    print("--- rules/prod/enabled/ ---")
    d, f = deploy_folder(
        kibana_url, headers,
        "rules/prod/enabled",
        enabled_override=True
    )
    total_deployed += d
    total_failed   += f

    print("\n--- rules/prod/disabled/ ---")
    d, f = deploy_folder(
        kibana_url, headers,
        "rules/prod/disabled",
        enabled_override=False
    )
    total_deployed += d
    total_failed   += f

    print("\n" + "=" * 50)
    print(f"Deployed: {total_deployed}")
    print(f"Failed:   {total_failed}")
    print("=" * 50)

    if total_failed > 0:
        sys.exit(1)

    print("All rules deployed successfully")

if __name__ == "__main__":
    main()
