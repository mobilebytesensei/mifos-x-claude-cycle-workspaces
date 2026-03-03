# Feature Spec: Pocket

> Unified view and management of linked financial accounts

---

## Feature Metadata

| Attribute | Value |
|-----------|-------|
| Feature ID | `pocket` |
| Module | `feature:pocket` |
| Priority | P1 |
| Status | Design |
| Created | 2026-03-03 |
| Flow | `FLOW-pocket.md` |

---

## Overview

The Pocket feature enables users to organize their financial accounts (savings, loans, shares) into a unified pocket view. Users can link multiple accounts to their pocket for consolidated balance tracking and quick access.

### Problem Statement

Users with multiple accounts (savings, loans, shares) currently need to navigate to each account separately to view balances and perform actions. There's no way to get a consolidated view of their financial position across account types.

### Solution

Implement the Fineract Pocket API to allow users to:
1. View all linked accounts in a single dashboard
2. See aggregated balance across account types
3. Link/delink accounts to their pocket
4. Quick access to individual account details

---

## User Stories

### US-1: View Pocket Dashboard
**As a** user
**I want to** see all my linked accounts in one place
**So that** I can quickly understand my total financial position

**Acceptance Criteria:**
- [ ] Display total aggregated balance from all linked accounts
- [ ] List all linked accounts grouped by type
- [ ] Show account name, masked number, and balance for each
- [ ] Support pull-to-refresh
- [ ] Handle empty state when no accounts are linked

### US-2: Link Accounts to Pocket
**As a** user
**I want to** link my savings, loan, or share accounts to my pocket
**So that** I can track them all in one place

**Acceptance Criteria:**
- [ ] Show list of available accounts not yet linked
- [ ] Group available accounts by type (savings, loans, shares)
- [ ] Allow multi-select for batch linking
- [ ] Show confirmation on successful linking
- [ ] Refresh pocket dashboard after linking

### US-3: Delink Account from Pocket
**As a** user
**I want to** remove an account from my pocket
**So that** I can organize which accounts I want to track

**Acceptance Criteria:**
- [ ] Show remove option for each linked account
- [ ] Display confirmation dialog before removing
- [ ] Account remains accessible from main accounts list
- [ ] Refresh pocket dashboard after delinking

### US-4: Access Account Details
**As a** user
**I want to** tap on a linked account to see its full details
**So that** I can view transactions and perform actions

**Acceptance Criteria:**
- [ ] Navigate to existing account details screen
- [ ] Support all account types (savings, loan, share)
- [ ] Maintain back navigation to pocket dashboard

---

## Functional Requirements

### FR-1: Pocket Dashboard

| ID | Requirement | Priority |
|----|-------------|:--------:|
| FR-1.1 | Fetch linked accounts on screen load | P0 |
| FR-1.2 | Calculate total balance from all linked accounts | P0 |
| FR-1.3 | Display accounts in a scrollable list | P0 |
| FR-1.4 | Show loading state while fetching | P0 |
| FR-1.5 | Show empty state with CTA to link accounts | P0 |
| FR-1.6 | Support pull-to-refresh | P1 |
| FR-1.7 | Cache pocket data locally | P2 |

### FR-2: Link Accounts

| ID | Requirement | Priority |
|----|-------------|:--------:|
| FR-2.1 | Fetch all client accounts | P0 |
| FR-2.2 | Filter out already-linked accounts | P0 |
| FR-2.3 | Group accounts by type | P0 |
| FR-2.4 | Support multi-select | P0 |
| FR-2.5 | Call linkAccounts API with selected IDs | P0 |
| FR-2.6 | Show success/error feedback | P0 |
| FR-2.7 | Search/filter available accounts | P1 |

### FR-3: Delink Accounts

| ID | Requirement | Priority |
|----|-------------|:--------:|
| FR-3.1 | Show remove button for each linked account | P0 |
| FR-3.2 | Display confirmation dialog | P0 |
| FR-3.3 | Call delinkAccounts API | P0 |
| FR-3.4 | Update UI optimistically | P1 |
| FR-3.5 | Rollback on API failure | P1 |

---

## Non-Functional Requirements

### Performance

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | Initial load time | < 2 seconds |
| NFR-2 | Link/delink operation | < 3 seconds |
| NFR-3 | Smooth scrolling | 60 FPS |

### Accessibility

| ID | Requirement |
|----|-------------|
| NFR-4 | All interactive elements have content descriptions |
| NFR-5 | Minimum touch target 48dp |
| NFR-6 | Announce balance changes to screen readers |
| NFR-7 | Support high contrast mode |

### Security

| ID | Requirement |
|----|-------------|
| NFR-8 | Mask account numbers (show last 4 digits) |
| NFR-9 | Require authentication for session |
| NFR-10 | Clear pocket data on logout |

---

## UI Components

### New Components

| Component | Description |
|-----------|-------------|
| `PocketDashboardScreen` | Main pocket view with aggregated balance and accounts list |
| `ManagePocketScreen` | Link/delink accounts management screen |
| `LinkAccountsBottomSheet` | Multi-select account linking UI |
| `PocketAccountCard` | Card displaying account info in pocket |
| `EmptyPocketView` | Empty state when no accounts linked |

### Reused Components

| Component | From Module |
|-----------|-------------|
| `AccountDetailsScreen` | `feature:accounts` |
| `LoadingIndicator` | `core:designsystem` |
| `ErrorView` | `core:designsystem` |
| `ConfirmationDialog` | `core:designsystem` |

---

## Data Flow

```
┌──────────────────────────────────────────────────────────────────────┐
│                          DATA FLOW                                    │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐            │
│  │  UI Layer   │     │ Domain Layer│     │ Data Layer  │            │
│  │             │     │             │     │             │            │
│  │ PocketScreen│────▶│PocketUseCase│────▶│PocketRepo   │            │
│  │             │     │             │     │             │            │
│  │ ViewModel   │◀────│  Models     │◀────│ ApiService  │            │
│  └─────────────┘     └─────────────┘     └─────────────┘            │
│         │                                       │                    │
│         ▼                                       ▼                    │
│  ┌─────────────┐                         ┌─────────────┐            │
│  │  UiState    │                         │ Fineract API│            │
│  │  Loading    │                         │ self/pockets│            │
│  │  Success    │                         └─────────────┘            │
│  │  Error      │                                                     │
│  │  Empty      │                                                     │
│  └─────────────┘                                                     │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Module Structure

```
feature/pocket/
├── build.gradle.kts
└── src/commonMain/kotlin/org/mifospay/feature/pocket/
    ├── PocketNavigation.kt
    ├── PocketRoute.kt
    ├── PocketScreen.kt
    ├── PocketViewModel.kt
    ├── ManagePocketScreen.kt
    ├── ManagePocketViewModel.kt
    ├── LinkAccountsBottomSheet.kt
    └── components/
        ├── PocketAccountCard.kt
        └── EmptyPocketView.kt
```

---

## Dependencies

### Required Modules

| Module | Purpose |
|--------|---------|
| `core:network` | API client for pocket endpoints |
| `core:data` | Repository implementation |
| `core:model` | Pocket data models |
| `core:designsystem` | UI components |
| `core:common` | Shared utilities |

### New Dependencies

None required - uses existing Ktorfit/Ktor stack.

---

## Testing Strategy

### Unit Tests

| Test | Description |
|------|-------------|
| `PocketViewModelTest` | State management and use case calls |
| `PocketRepositoryTest` | API interaction and mapping |
| `PocketUseCaseTest` | Business logic validation |

### UI Tests

| Test | Description |
|------|-------------|
| `PocketScreenTest` | Screen rendering and interactions |
| `LinkAccountsTest` | Multi-select and submission |
| `DelinkAccountTest` | Confirmation and removal |

### Integration Tests

| Test | Description |
|------|-------------|
| `PocketApiIntegrationTest` | End-to-end API calls |

---

## Migration/Rollout

### Phase 1: Core Implementation
- [ ] Implement pocket API service
- [ ] Create pocket repository
- [ ] Build pocket dashboard screen
- [ ] Add navigation to pocket

### Phase 2: Management Features
- [ ] Implement link accounts flow
- [ ] Implement delink accounts flow
- [ ] Add confirmation dialogs

### Phase 3: Polish
- [ ] Add analytics events
- [ ] Implement caching
- [ ] Add empty states and error handling
- [ ] Accessibility testing

---

## Related Documents

- **Flow:** `user-flows/flows/FLOW-pocket.md`
- **API:** `features/pocket/API.md`
- **Status:** `features/pocket/STATUS.md`

---

## Open Questions

1. **Q:** Should loan accounts show negative balance or outstanding amount?
   **A:** TBD - Check API response format

2. **Q:** Can a user have multiple pockets?
   **A:** No - Fineract API supports single pocket per user

3. **Q:** Should we show account health indicators (active/dormant)?
   **A:** P2 - Consider for future enhancement
