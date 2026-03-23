# template_meta
# template_version: "2.86.5"
# template_path: "templates/blueprints/workspace-project/design-spec-layer/STATUS.md"
# last_modified: "2026-03-19"

# STATUS.md - Single Source of Truth for Implementation Status

> **Purpose**: ONE file to check and update all implementation status
> **Rule**: Update THIS file after any implementation work
> **Last Verified**: ${DATE}

---

## Quick Overview

| Phase | Features | Done | In Progress | Planned |
|-------|----------|------|-------------|---------|
| Core MVP | ${phase1_count} | 0 | 0 | ${phase1_count} |

**Next Priority**: ${first_feature}

---

## Phase 1: Core MVP

| Feature | Status | Server | Client | UI | Gaps |
|---------|--------|--------|--------|-----|------|
| ${feature_1} | Planned | - | - | - | All |
| ${feature_2} | Planned | - | - | - | All |

---

## Status Legend

| Status | Meaning |
|--------|---------|
| Done | Feature complete, all working |
| Needs Update | Has gaps, spec changed, or incomplete |
| In Progress | Currently being implemented |
| Planned | Spec exists, not started |
| Not Started | No work done |

---

## Code Verification Summary

### Feature Layer (feature/*)
| Module | Screen | ViewModel | Components | DI |
|--------|--------|-----------|------------|-----|
| ${feature_1} | - | - | - | - |

### Network Layer (core/network)
- ${service_count} services registered

### Data Layer (core/data)
- ${repository_count} repositories registered

---

## Layer Checklist Template

When implementing a feature, track layers here:

```
Feature: [Name]
- [ ] SPEC.md created
- [ ] API.md created
- [ ] Backend: RPCs deployed
- [ ] Network: DTO + Service
- [ ] Data: Mapper + Repository
- [ ] Domain: UseCase(s)
- [ ] Feature: ViewModel + Screen
- [ ] Navigation: Route registered
- [ ] STATUS.md updated
```

---

## Recent Updates

| Date | Feature | Change |
|------|---------|--------|
| ${DATE} | Project | Initial STATUS.md created |

---

## How to Update This File

1. **After implementing code**: Check off layers in feature section
2. **After completing feature**: Change status from In Progress to Done
3. **After spec change**: Change status to Needs Update and list gaps
4. **Add recent update**: Add row to Recent Updates table
5. **IMPORTANT**: Run `/gap-analysis-project` periodically to detect staleness
