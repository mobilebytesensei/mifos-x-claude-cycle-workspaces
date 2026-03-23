# template_meta
# template_version: "2.86.5"
# template_path: "workspaces/mifos-x/mifos-x-field-officer-app/plan-layer/versions/VERSION_INDEX.md"
# last_modified: "2026-03-20"

# Version Index - ${PROJECT_NAME}

> **Purpose**: Track release versions and roadmap

**Last Updated**: ${DATE}

---

## Active Versions

| Version | Status | Focus | Release Target |
|---------|:------:|-------|----------------|
| v1.0.0 | Current | Core features | - |

---

## Version Structure

Each version has a planning folder:

```
plan-layer/versions/
├── v1.0.0/
│   ├── SCOPE.md        # Feature scope definition
│   ├── PLAN.md         # Milestone breakdown
│   ├── STATUS.md       # Implementation status
│   └── CHANGELOG.md    # Changes in this version
├── v1.1.0/
│   └── ...
└── backlog/
    └── FEATURES.md     # Future features not yet scheduled
```

---

## Version Stages

| Stage | Description | Branch |
|-------|-------------|--------|
| Development | Active development | `development` |
| Staging | Pre-release testing | `staging` |
| Production | Released version | `main` |

---

## Version Naming

Format: `vMAJOR.MINOR.PATCH`

| Component | When to Increment |
|-----------|-------------------|
| MAJOR | Breaking changes, major redesign |
| MINOR | New features, significant updates |
| PATCH | Bug fixes, minor improvements |

---

## Version History

| Version | Status | Key Changes |
|---------|:------:|-------------|
| v1.0.0 | Current | Initial release |

---

## Commands

```bash
# Plan version work
/gap-planning --version v1.1.0

# Check version status
/gap-analysis --version v1.0.0

# Feature planning for version
/gap-planning feature auth --version v1.1.0
```

---

## Creating New Version

1. Create version directory: `plan-layer/versions/vX.X.X/`
2. Create SCOPE.md with feature list
3. Create PLAN.md with milestones
4. Create STATUS.md (initially empty)
5. Update this VERSION_INDEX.md
