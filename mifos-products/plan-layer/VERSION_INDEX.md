# Version Index

**Current Version:** v{{LATEST}}
**Next Planned:** v{{NEXT}}

---

## Version Timeline

| Version | Date | Status | Milestone |
|:-------:|:----:|:------:|-----------|
| v0.1.0 | 2026-08-15 | ✅ Complete | Initial features |
| v0.2.0 | 2026-08-15 | 🔄 In Progress | Enhancements |
| v1.0.0 | 2026-08-15 | 📝 Planned | Production release |

---

## Semantic Versioning

- **Major (1.0.0)**: Breaking changes, new architecture
- **Minor (0.1.0)**: New features, backward compatible
- **Patch (0.0.1)**: Bug fixes, minor improvements

---

## Status Legend

| Symbol | Status |
|:------:|--------|
| ✅ | Complete - Implemented and deployed |
| 🔄 | In Progress - Currently being implemented |
| 📝 | Planned - Design approved, pending implementation |
| ⚠️ | Blocked - Waiting on dependencies |
| ❌ | Cancelled - No longer needed |

---

## Commands

```bash
# View current version
cat VERSION_INDEX.md | grep "Current Version"

# Create new version plan
/plan create v{NEXT_VERSION}

# Check plan status
/gap-analysis plan
```
