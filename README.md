# Elastic Detection as Code — Rules Repository

Detection rules managed as code using the DaC methodology.

## Structure
rules/
├── staging/ ← ALL new rules enter here
└── prod/
├── enabled/ ← Auto-promoted, deployed as ENABLED
└── disabled/ ← Auto-promoted, deployed as DISABLED

schemas/ ← Rule validation schema
tools/ ← Deployment scripts
docs/ ← Templates and guides
.github/workflows/ ← CI/CD pipeline

## Workflow

1. Write rule → `rules/staging/`
2. Open Pull Request
3. Pipeline validates automatically
4. Get approval and merge
5. Rule auto-promoted to `rules/prod/`
6. Rule auto-deployed to Elastic!

## Author
HRISHIKESH YALAVARTHI
