# Elastic Detection as Code — Rules Repository

Detection rules managed as code using the **Detection as Code (DaC)** methodology.
Every rule is a YAML file stored in Git, validated automatically, and deployed to
Elastic SIEM via a GitHub Actions CI/CD pipeline. No manual Kibana UI edits.
No direct API calls. Pure code-driven detection engineering.

---

## Environment

| Component | Details |
|---|---|
| Elastic Version | 9.4.3 |
| Rule Type | ES\|QL only |
| Runner | Self-hosted (Kali Linux) |
| Validated Against | Live Elastic 9.4.3 API |
| Author | HRISHIKESH YALAVARTHI |

---

## Repository Structure

```
elastic-dac-rules/
│
├── .github/
│   └── workflows/
│       ├── uuid-inject.yml      ← auto-fills rule_id on push to branch
│       ├── validate.yml         ← validates rules on PR to main
│       ├── promote.yml          ← copies staging → prod on merge
│       ├── deploy-prod.yml      ← deploys to Elastic PROD on merge
│       └── deploy-staging.yml   ← manual deploy to staging
│
├── tests/
│   ├── test_yaml_syntax.py      ← YAML can be parsed
│   ├── test_rule_id.py          ← UUID is valid and not empty
│   ├── test_schema.py           ← validates against rule.schema.json
│   ├── test_severity_risk.py    ← severity and risk_score alignment
│   ├── test_no_duplicates.py    ← no duplicate rule_ids
│   └── test_no_prod_edits.py    ← blocks direct edits to rules/prod/
│
├── tools/
│   ├── rule_utils.py            ← shared: load, strip, build payload
│   ├── inject_uuid.py           ← UUID injection logic
│   ├── promote_rules.py         ← staging to prod copy logic
│   └── deploy_rules.py          ← YAML to Elastic API logic
│
├── docs/
│   ├── rule-standard-v1.yaml    ← master rule template
│   ├── lifecycle.md             ← rule lifecycle documentation
│   └── runbook.md               ← operations runbook
│
├── schemas/
│   └── rule.schema.json         ← jsonschema validation file
│
└── rules/
    ├── staging/                 ← ALL new rules enter here ONLY
    └── prod/
        ├── enabled/             ← auto-promoted, deployed as ENABLED
        └── disabled/            ← auto-promoted, deployed as DISABLED
```

---

## Pipeline Flow

```
Developer writes rule → leaves rule_id: "" → git push branch
         ↓
uuid-inject.yml     auto-fills rule_id UUID → commits back to branch
         ↓
Developer opens PR to main
         ↓
validate.yml        6 checks: YAML syntax · UUID · schema ·
                    severity/risk · no duplicates · no prod edits
         ↓
Developer merges PR
         ↓
promote.yml         copies staging → prod/enabled/ or prod/disabled/
                    based on enabled: field
         ↓
deploy-prod.yml     GET rule_id → exists? PUT (update) : POST (create)
                    rule live in Elastic SIEM
```

---

## Workflow Triggers

| Workflow | Trigger | Runner | Purpose |
|---|---|---|---|
| `uuid-inject.yml` | push to any branch (not main) | ubuntu-latest | auto-fill `rule_id: ""` |
| `validate.yml` | pull_request to main | ubuntu-latest | 6 quality checks |
| `promote.yml` | push to main · `rules/staging/*.yml` | ubuntu-latest | copy to prod folder |
| `deploy-prod.yml` | push to main · `rules/prod/**/*.yml` | self-hosted | deploy to Elastic |
| `deploy-staging.yml` | manual trigger only | self-hosted | optional staging deploy |
