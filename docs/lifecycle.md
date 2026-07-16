# Detection Rule Lifecycle

## New Rule
1. Create YAML in `rules/staging/`
2. Open PR to main
3. Pipeline validates
4. Get approval → Merge
5. Auto-promoted to `rules/prod/`
6. Auto-deployed to Elastic

## Update Existing Rule
1. Copy from `rules/prod/` to `rules/staging/`
2. Edit staging copy ONLY
3. Open PR → same flow

## Golden Rules
- staging/ is the ONLY entry point
- NEVER edit rules/prod/ directly
- rule_id NEVER changes
- enabled: true → prod/enabled/
- enabled: false → prod/disabled/
