# template_meta
# template_version: "2.86.5"
# template_path: "workspaces/mifos-x/mifos-x-field-officer-app/plan-layer/onboarding/ONBOARDING_PLAN.md"
# last_modified: "2026-03-20"

# Onboarding Plan: mifos-x-field-officer-app

**Created**: 2026-03-04
**Status**: Completed
**Workspace**: mifos-x

---

## Project Summary

| Attribute | Value |
|-----------|-------|
| Project Name | mifos-x-field-officer-app |
| Project Type | kmp (kmp-app) |
| Targets | Android, iOS, Desktop, Web |
| Backend | Fineract REST API |
| Features Discovered | 20 |
| Total Screens | 97 |
| Total ViewModels | 91 |
| Services | 27 |
| Repositories | 64 |

---

## Discovery Results

### Features Discovered

| # | Feature | Screens | VMs | Category |
|:-:|---------|:-------:|:---:|----------|
| 1 | about | 1 | 0 | Utilities |
| 2 | activate | 1 | 1 | Client Management |
| 3 | auth | 1 | 1 | Authentication |
| 4 | center | 5 | 5 | Group/Center |
| 5 | checker-inbox-task | 2 | 2 | Authentication |
| 6 | client | 38 | 31 | Client Management |
| 7 | collectionSheet | 5 | 5 | Group/Center |
| 8 | data-table | 4 | 4 | Data/Reports |
| 9 | document | 2 | 2 | Client Management |
| 10 | groups | 4 | 4 | Group/Center |
| 11 | loan | 11 | 12 | Financial |
| 12 | note | 2 | 2 | Client Management |
| 13 | offline | 5 | 6 | Utilities |
| 14 | path-tracking | 1 | 1 | Utilities |
| 15 | recurringDeposit | 1 | 1 | Financial |
| 16 | report | 3 | 2 | Data/Reports |
| 17 | savings | 7 | 7 | Financial |
| 18 | search | 1 | 1 | Data/Reports |
| 19 | search-record | 1 | 1 | Data/Reports |
| 20 | settings | 2 | 3 | Utilities |

### Backend Detection

| Provider | Detected |
|----------|:--------:|
| Supabase | ❌ |
| Firebase | ✅ (analytics only) |
| Retrofit | ✅ |
| Ktor Client | ✅ |
| Fineract | ✅ (Primary) |

**Selected Backend**: Fineract REST API

---

## Phases Completed

### Phase 1: Layer Structure ✅
- Created all 8 layer directories
- Created PROJECT.md with configuration

### Phase 2: Design Layer ✅
- Created FEATURES_INDEX.md with 20 features
- Created user-flows directory structure
- Created USER_FLOWS_INDEX.md with suggested flows

### Phase 3: Server Layer ✅
- Created API_INDEX.md with Fineract endpoints

### Phase 4: Client Layer ✅
- Created SERVICES_INDEX.md with 27 services

### Phase 5: Feature Layer ✅
- Created MODULES_INDEX.md with 20 modules

### Phase 6: Testing Layer ⏳
- Directory created
- Patterns pending

### Phase 7: Platform Layer ⏳
- Directory created
- Platform-specific config pending

### Phase 8: Infrastructure Layer ⏳
- Directory created
- Navigation/DI config pending

---

## Next Steps

1. **Generate Feature Specs**: Run `/design [feature]` for each feature to create SPEC.md
2. **Create User Flows**: Run `/flow-create` to define user journeys
3. **Document APIs**: Run `/server [endpoint]` for Fineract API documentation
4. **Generate Mockups**: Run `/mockup [feature] --auto` for UI mockups

---

## Recommended Order

### Priority 1: Core Features
1. `auth` - Authentication (login/logout)
2. `client` - Client management (38 screens)
3. `loan` - Loan management (11 screens)
4. `savings` - Savings management (7 screens)

### Priority 2: Operations
5. `groups` - Group management
6. `center` - Center management
7. `collectionSheet` - Collections
8. `offline` - Offline sync

### Priority 3: Utilities
9. `search` - Search functionality
10. `report` - Reports
11. `settings` - App settings
12. Other features...

---

## Commands for Onboarding

```bash
# Generate specs for all features
/design auth
/design client
/design loan
/design savings

# Create user flows
/flow-create

# Run gap analysis
/gap-analysis design
/gap-analysis client
/gap-analysis feature

# Generate mockups
/mockup auth --auto
/mockup client --auto
```
