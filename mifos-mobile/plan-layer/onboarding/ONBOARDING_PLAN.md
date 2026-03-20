# template_meta
# template_version: "2.84.0"
# template_path: "templates/blueprints/workspace-project/plan-layer/onboarding/ONBOARDING_PLAN.md"
# last_modified: "2026-03-20"

# Project Onboarding Plan

> Comprehensive plan for integrating existing project into claude-product-cycle framework

---

## Project Info

| Field | Value |
|-------|-------|
| Project | ${PROJECT_NAME} |
| Workspace | ${WORKSPACE_NAME} |
| Type | ${PROJECT_TYPE} |
| Created | ${DATE} |
| Status | ${STATUS} |

---

## Source Analysis Summary

### Detected Structure

| Item | Count | Details |
|------|:-----:|---------|
| Features | ${FEATURE_COUNT} | ${FEATURE_LIST} |
| Screens | ${SCREEN_COUNT} | Detected from UI packages |
| ViewModels | ${VM_COUNT} | Detected from viewmodel packages |
| API Endpoints | ${ENDPOINT_COUNT} | Detected from service/api packages |
| Repositories | ${REPO_COUNT} | Detected from data packages |

### Server Type Detection

| Check | Result |
|-------|--------|
| Supabase Client | ${SUPABASE_DETECTED} |
| Retrofit/Ktor | ${REST_DETECTED} |
| GraphQL | ${GRAPHQL_DETECTED} |
| Firebase | ${FIREBASE_DETECTED} |

**Confirmed Server Type**: ${SERVER_TYPE}

---

## Onboarding Phases

```
Phase 1: Design Layer     ░░░░░░░░░░  0%
Phase 2: Server Layer     ░░░░░░░░░░  0%
Phase 3: Client Layer     ░░░░░░░░░░  0%
Phase 4: Feature Layer    ░░░░░░░░░░  0%
Phase 5: Testing Layer    ░░░░░░░░░░  0%
────────────────────────────────────────
OVERALL                   ░░░░░░░░░░  0%
```

---

## Phase 1: Design Layer

**Goal**: Create comprehensive design specifications for all detected features

**Status**: ${PHASE_1_STATUS}

### Tasks

| # | Task | Status | Output |
|:-:|------|:------:|--------|
| 1.1 | Analyze feature: ${FEATURE_1} | ⬜ | design-spec-layer/features/${FEATURE_1}/ |
| 1.2 | Create SPEC.md from source | ⬜ | Extract screens, VMs, user stories |
| 1.3 | Create API.md from endpoints | ⬜ | Document API requirements |
| 1.4 | Create STATUS.md | ⬜ | Track implementation status |
| 1.5 | Setup mockups/dummy/ | ⬜ | Placeholder PNGs |
| 1.6 | Setup mockups/prod/ | ⬜ | Production mockup placeholders |
| 1.7 | Repeat for all features | ⬜ | ${FEATURE_COUNT} features total |

### Source Analysis for Design Layer

```
Analyze these source paths:
├── feature/           → Extract feature names
├── ui/screens/        → Extract screen names
├── viewmodel/         → Extract ViewModel names
├── navigation/        → Extract navigation flow
└── components/        → Extract reusable components
```

### Deliverables

- [ ] FEATURES_INDEX.md updated
- [ ] SPEC.md for each feature (from source analysis)
- [ ] API.md for each feature (from endpoint analysis)
- [ ] STATUS.md for each feature
- [ ] mockups/dummy/ with placeholders
- [ ] mockups/prod/ with placeholders

---

## Phase 2: Server Layer

**Goal**: Setup server layer based on detected server type

**Status**: ${PHASE_2_STATUS}

### Server Type: ${SERVER_TYPE}

#### If Supabase:

| # | Task | Status | Output |
|:-:|------|:------:|--------|
| 2.1 | Create supabase/ directory structure | ⬜ | server-layer/supabase/ |
| 2.2 | Document existing tables | ⬜ | TABLES_INDEX.md |
| 2.3 | Document RPC functions | ⬜ | RPC_INDEX.md |
| 2.4 | Document Edge Functions | ⬜ | EDGE_FUNCTIONS_INDEX.md |
| 2.5 | Document RLS policies | ⬜ | POLICIES_INDEX.md |
| 2.6 | Create migration scripts | ⬜ | migrations/ |

#### If REST API:

| # | Task | Status | Output |
|:-:|------|:------:|--------|
| 2.1 | Create endpoints/ directory | ⬜ | server-layer/endpoints/ |
| 2.2 | Document each endpoint | ⬜ | {feature}.md per feature |
| 2.3 | Create API_INDEX.md | ⬜ | Endpoint lookup table |
| 2.4 | Document auth flow | ⬜ | AUTH.md |
| 2.5 | Document error codes | ⬜ | ERRORS.md |

### Source Analysis for Server Layer

```
Analyze these source paths:
├── network/api/       → Extract API interfaces
├── network/dto/       → Extract DTOs/models
├── data/remote/       → Extract remote data sources
└── supabase/          → Extract Supabase client usage
```

### Deliverables

- [ ] Server layer structure created
- [ ] All endpoints documented
- [ ] Auth flow documented
- [ ] Error handling documented

---

## Phase 3: Client Layer

**Goal**: Document client-side network and data layer

**Status**: ${PHASE_3_STATUS}

### Tasks

| # | Task | Status | Output |
|:-:|------|:------:|--------|
| 3.1 | Document existing services | ⬜ | client-layer/services/ |
| 3.2 | Document repositories | ⬜ | client-layer/repositories/ |
| 3.3 | Document DTOs | ⬜ | client-layer/models/ |
| 3.4 | Create CLIENT_INDEX.md | ⬜ | O(1) lookup |
| 3.5 | Document DI setup | ⬜ | DEPENDENCY_INJECTION.md |

### Source Analysis for Client Layer

```
Analyze these source paths:
├── core/network/      → Extract services
├── core/data/         → Extract repositories
├── core/model/        → Extract domain models
├── core/common/       → Extract shared utilities
└── di/                → Extract DI modules
```

### Deliverables

- [ ] All services documented
- [ ] All repositories documented
- [ ] DTOs mapped to API
- [ ] DI structure documented

---

## Phase 4: Feature Layer

**Goal**: Document UI layer implementation

**Status**: ${PHASE_4_STATUS}

### Tasks

| # | Task | Status | Output |
|:-:|------|:------:|--------|
| 4.1 | Document ViewModels | ⬜ | feature-layer/viewmodels/ |
| 4.2 | Document Screens | ⬜ | feature-layer/screens/ |
| 4.3 | Document Navigation | ⬜ | feature-layer/navigation/ |
| 4.4 | Document UI State | ⬜ | feature-layer/state/ |
| 4.5 | Create FEATURE_INDEX.md | ⬜ | O(1) lookup |

### Source Analysis for Feature Layer

```
Analyze these source paths:
├── feature/{name}/    → Extract feature modules
├── ui/screens/        → Extract screen composables
├── viewmodel/         → Extract ViewModels
├── state/             → Extract UI state classes
└── navigation/        → Extract nav graphs
```

### Deliverables

- [ ] All ViewModels documented
- [ ] All Screens documented
- [ ] Navigation flow documented
- [ ] UI state patterns documented

---

## Phase 5: Testing Layer

**Goal**: Document and setup testing infrastructure

**Status**: ${PHASE_5_STATUS}

### Tasks

| # | Task | Status | Output |
|:-:|------|:------:|--------|
| 5.1 | Audit existing tests | ⬜ | testing-layer/AUDIT.md |
| 5.2 | Document test patterns | ⬜ | testing-layer/PATTERNS.md |
| 5.3 | Create fake repositories | ⬜ | testing-layer/fakes/ |
| 5.4 | Create test fixtures | ⬜ | testing-layer/fixtures/ |
| 5.5 | Create TESTING_INDEX.md | ⬜ | O(1) lookup |

### Deliverables

- [ ] Test coverage report
- [ ] Test patterns documented
- [ ] Fake implementations ready
- [ ] Test fixtures created

---

## User Decisions Required

### Server Configuration

```
Question: Confirm server type?
Detected: ${DETECTED_SERVER_TYPE}

Options:
[ ] Supabase (detected)
[ ] REST API
[ ] GraphQL
[ ] Firebase
[ ] Other: ___________
```

### Feature Priority

```
Question: Which features to onboard first?

Detected features:
${FEATURE_LIST_WITH_CHECKBOXES}

Priority order: ___________
```

### Mockup Generation

```
Question: Generate mockups during onboarding?

Options:
[ ] Yes - Generate dummy mockups for all features
[ ] No - Skip mockup generation
[ ] Partial - Only for priority features
```

---

## Execution Commands

```bash
# Execute full onboarding
/project-add --execute-plan

# Execute specific phase
/project-add --phase 1    # Design Layer only
/project-add --phase 2    # Server Layer only

# Skip to next phase
/project-add --next-phase

# Check onboarding status
/project-add --status
```

---

## Progress Tracking

| Phase | Started | Completed | Duration |
|:-----:|:-------:|:---------:|:--------:|
| 1 | - | - | - |
| 2 | - | - | - |
| 3 | - | - | - |
| 4 | - | - | - |
| 5 | - | - | - |

**Total Onboarding Time**: -

---

## Notes

${NOTES}

---

## Related Files

| File | Purpose |
|------|---------|
| PROJECT.md | Project configuration |
| CURRENT_WORK.md | Active work tracking |
| plan-layer/PLANS_INDEX.md | Plan lookup |
