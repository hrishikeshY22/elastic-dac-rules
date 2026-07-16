# DaC Operations Runbook

## Generate UUID
python3 -c "import uuid; print(uuid.uuid4())"

## Create New Rule
1. python3 -c "import uuid; print(uuid.uuid4())"
2. cp docs/rule-standard-v1.yaml rules/staging/your-rule-name.yml
3. Fill all required fields
4. git add rules/staging/your-rule-name.yml
5. git commit -m "Add: your rule description"
6. git push origin your-branch-name
7. Open PR on GitHub

## Required GitHub Secrets
- ELASTIC_PROD_URL
- ELASTIC_PROD_API_KEY
