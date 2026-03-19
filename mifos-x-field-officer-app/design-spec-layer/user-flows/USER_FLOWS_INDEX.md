# User Flows Index

> **Project**: mifos-x-field-officer-app
> **Purpose**: Single source of truth for all user journeys
> **Last Updated**: 2026-03-19

---

## Quick Reference

| Flow | File | Screens | Coverage | Status |
|------|------|:-------:|:--------:|:------:|
| - | - | - | - | - |

**Total Flows**: 0
**Average Coverage**: N/A

---

## Available Flows

No flows created yet. Use one of the following to create your first flow:

```bash
# Create flow manually (wizard)
/flow-create [name]

# Generate flow with AI
/flow-generate [name] "description"

# Use a template
/flow-create --from-template
```

---

## Commands

| Command | Purpose |
|---------|---------|
| `/flow` | Visualize flows (ASCII + Mermaid) |
| `/flow-create` | Create flow with wizard |
| `/flow-generate` | AI generates flow |
| `/flow-update` | Update existing flow |
| `/flow-validate` | Validate design coverage |
| `/flow-to-design` | Generate feature from flow |

---

## Flow → Feature Mapping

| Flow | Feature Folder | Status |
|------|----------------|:------:|
| - | - | - |

---

## Getting Started

1. **Create your first flow**:
   ```bash
   /flow-create authentication
   # OR
   /flow-generate authentication "User login with email, password, forgot password, and OTP verification"
   ```

2. **Generate feature from flow**:
   ```bash
   /flow-to-design authentication
   ```

3. **Validate coverage**:
   ```bash
   /flow-validate --coverage
   ```

---

## Related Files

| File | Purpose |
|------|---------|
| `flows/*.mmd` | Mermaid flow definitions |
| `FLOW_COVERAGE.md` | Coverage tracking report |
| `FEATURES_INDEX.md` | Feature registry with flow coverage |
