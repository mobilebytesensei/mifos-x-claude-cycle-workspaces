# Plans Index - O(1) Lookup

**Project:** mifos-x-group-banking
**Total Plans:** {{COUNT}}

---

## Quick Reference

| Version | Status | Features | Created | Implemented |
|:-------:|:------:|:--------:|:-------:|:-----------:|
| v0.1.0 | ✅ Implemented | {{FEATURE_COUNT}} | {{DATE}} | {{DATE}} |
| v0.2.0 | 🔄 In Progress | {{FEATURE_COUNT}} | {{DATE}} | - |
| v0.3.0 | 📝 Draft | {{FEATURE_COUNT}} | {{DATE}} | - |

---

## Plan → Design Flow

```
1. Create plan in plan-layer/versions/v{VERSION}/PLAN.md
2. Define features, APIs, mockup states
3. Get approval (status: Approved)
4. Run /design from-plan v{VERSION}
5. Design layer auto-generates 8 files per feature
6. Server CRUD engine auto-syncs (Supabase only)
7. Implementation begins with /gap-implement
```

---

## Commands

| Command | Purpose |
|---------|---------|
| /plan create v{VERSION} | Create new plan |
| /plan approve v{VERSION} | Mark plan as approved |
| /design from-plan v{VERSION} | Generate design layer |
| /gap-analysis plan | Check plan coverage |
