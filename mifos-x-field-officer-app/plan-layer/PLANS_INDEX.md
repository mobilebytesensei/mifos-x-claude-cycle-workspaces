# Plans Index

> **Purpose**: Registry of all saved implementation plans.
> **Auto-updated**: Plans are added/updated by `/gap-planning-project` commands.

---

## Active Plans

| ID | Status | Scope | Tasks | Created | Path |
|:---|:------:|-------|:-----:|---------|------|
| design-features-data-table-260305-001 | Ready | data-table | 12 | 2026-03-05 | plans/PLAN-design-features-data-table-260305-001.md |

---

## Plan ID Convention

```
{scope}-{YYMMDD}-{SEQ}

Scopes:
- full           → Full project plan
- {feature}      → Feature-specific plan
- {layer}        → Layer-specific plan
- design-features-{flow} → Feature generation from flow
- impl-{flow}    → Source implementation for flow
- impl-{feature} → Source implementation for feature
- user-flows     → User flow alignment plan
```

---

## Commands

```bash
# List all plans
/gap-planning-project list

# View current/latest plan
/gap-planning-project plan current

# View specific plan
/gap-planning-project plan {ID}

# Implement a plan
/gap-implement-project plan {ID}

# Check plan progress
/gap-analysis-project plan {ID}
```
