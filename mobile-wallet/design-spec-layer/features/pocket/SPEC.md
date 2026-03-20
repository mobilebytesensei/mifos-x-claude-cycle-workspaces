# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mobile-wallet/design-spec-layer/features/pocket/SPEC.md"
# last_modified: "2026-03-20"

# Feature Spec: Pocket

> Favorite accounts for quick access on Home screen

---

## Feature Metadata

| Attribute | Value |
|-----------|-------|
| Feature ID | `pocket` |
| Module | `feature:home` (integrated) + `feature:pocket` (management) |
| Priority | P1 |
| Status | Design |
| Created | 2026-03-03 |
| Updated | 2026-03-03 |
| Flow | `FLOW-pocket.md` |

---

## Overview

Pocket acts as **"Favorites"** for accounts. Users can link their Savings, Loan, and Share accounts to Pocket for faster access directly on the Home screen's account pager.

### Problem Statement

Users with multiple accounts see all accounts in the Home screen pager, making it slow to access their most-used accounts. There's no way to prioritize or favorite specific accounts.

### Solution

Integrate the Fineract Pocket API with the Home screen to:
1. **Empty Pocket:** Show all accounts (first-time user experience)
2. **Pocket has accounts:** Show only pocket (favorite) accounts by default
3. **Toggle View:** Allow switching between Pocket and All Accounts views
4. **Quick Actions:** Long press to add/remove from pocket

### Key Behavior

| Pocket State | Home Screen Display | Rationale |
|--------------|---------------------|-----------|
| **Empty** | All accounts shown | First-time users see everything |
| **Has accounts** | Pocket accounts shown (default) | Quick access to favorites |
| **Toggle to All** | All accounts shown | Full access when needed |

---

## User Stories

### US-1: View Accounts on Home (Smart Default)
**As a** user
**I want** the Home screen to show my favorite accounts by default
**So that** I can quickly access the accounts I use most

**Acceptance Criteria:**
- [ ] If pocket is empty → show all accounts in pager
- [ ] If pocket has accounts → show pocket accounts by default
- [ ] Show aggregated balance for displayed accounts
- [ ] Display star indicator (⭐) for accounts in pocket

### US-2: Toggle Between Pocket and All Accounts
**As a** user
**I want** to switch between Pocket view and All Accounts view
**So that** I can access any account when needed

**Acceptance Criteria:**
- [ ] Dropdown at top shows current view (Pocket/All)
- [ ] Tapping dropdown shows view options
- [ ] Selection persists during session
- [ ] Show account count in each view option

### US-3: Add Account to Pocket (Quick Action)
**As a** user
**I want to** long-press an account to add it to my pocket
**So that** I can quickly favorite accounts

**Acceptance Criteria:**
- [ ] Long press account card shows context menu
- [ ] "Add to Pocket" option for non-pocket accounts
- [ ] API call to link account
- [ ] Star indicator appears on success
- [ ] Show toast confirmation

### US-4: Remove Account from Pocket (Quick Action)
**As a** user
**I want to** long-press an account to remove it from my pocket
**So that** I can manage my favorites

**Acceptance Criteria:**
- [ ] "Remove from Pocket" option for pocket accounts
- [ ] Confirmation dialog before removing
- [ ] API call to delink account
- [ ] Star indicator disappears on success
- [ ] Account remains accessible in All Accounts view

### US-5: Manage Pocket (Full Management)
**As a** user
**I want to** access a dedicated screen to manage all pocket accounts
**So that** I can see and organize all favorites at once

**Acceptance Criteria:**
- [ ] "Manage Pocket" option in view dropdown
- [ ] Shows two sections: In Pocket / Not in Pocket
- [ ] Tap star to toggle pocket membership
- [ ] Swipe-to-remove gesture support

---

## Functional Requirements

### FR-1: Home Screen Pocket Integration

| ID | Requirement | Priority |
|----|-------------|:--------:|
| FR-1.1 | Fetch pocket accounts on Home screen load | P0 |
| FR-1.2 | Determine display mode based on pocket state | P0 |
| FR-1.3 | Show all accounts if pocket is empty | P0 |
| FR-1.4 | Show pocket accounts if pocket has linked accounts | P0 |
| FR-1.5 | Calculate and display aggregated balance | P0 |
| FR-1.6 | Show star indicator (⭐) for pocket accounts | P0 |
| FR-1.7 | Persist view selection during session | P1 |

### FR-2: View Toggle

| ID | Requirement | Priority |
|----|-------------|:--------:|
| FR-2.1 | Dropdown shows current view with account count | P0 |
| FR-2.2 | Options: Pocket (N), All Accounts (M) | P0 |
| FR-2.3 | "Manage Pocket" link in dropdown | P0 |
| FR-2.4 | Switching view updates pager immediately | P0 |

### FR-3: Quick Link/Delink (Context Menu)

| ID | Requirement | Priority |
|----|-------------|:--------:|
| FR-3.1 | Long press account shows context menu | P0 |
| FR-3.2 | "Add to Pocket" for non-pocket accounts | P0 |
| FR-3.3 | "Remove from Pocket" for pocket accounts | P0 |
| FR-3.4 | "Set as Default" option | P0 |
| FR-3.5 | "View Details" option | P0 |
| FR-3.6 | Haptic feedback on long press | P1 |

### FR-4: Manage Pocket Screen

| ID | Requirement | Priority |
|----|-------------|:--------:|
| FR-4.1 | List pocket accounts with filled star | P0 |
| FR-4.2 | List non-pocket accounts with empty star | P0 |
| FR-4.3 | Tap star to toggle pocket membership | P0 |
| FR-4.4 | Confirmation dialog for delink | P0 |
| FR-4.5 | Swipe-to-remove gesture | P1 |

---

## Non-Functional Requirements

### Performance

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | Pocket API fetch | < 1 second |
| NFR-2 | Link/delink operation | < 2 seconds |
| NFR-3 | View toggle | < 100ms (local) |
| NFR-4 | Context menu appearance | < 200ms |

### Accessibility

| ID | Requirement |
|----|-------------|
| NFR-5 | Star icon: "In Pocket" / "Not in Pocket" content description |
| NFR-6 | Long press announces "Actions available" |
| NFR-7 | View dropdown announces current selection |
| NFR-8 | Minimum touch target 48dp |

---

## UI Components

### Modified Components (Home Module)

| Component | Changes |
|-----------|---------|
| `HomeScreen.kt` | Add view dropdown, pocket state handling |
| `HomeViewModel.kt` | Add pocket fetch, display mode logic |
| `AccountCard.kt` | Add star indicator, long press handler |

### New Components

| Component | Description |
|-----------|-------------|
| `ViewDropdownMenu.kt` | Pocket/All accounts switcher |
| `AccountContextMenu.kt` | Long press actions bottom sheet |
| `ManagePocketScreen.kt` | Full pocket management screen |
| `ManagePocketViewModel.kt` | Manage pocket state |
| `DelinkConfirmationDialog.kt` | Confirm removal from pocket |

---

## State Management

### HomeState (Extended)

```kotlin
data class HomeState(
    // Existing
    val accounts: List<Account> = emptyList(),
    val selectedAccount: Account? = null,

    // NEW: Pocket
    val pocketAccounts: List<PocketAccount> = emptyList(),
    val isPocketEmpty: Boolean = true,
    val showPocketView: Boolean = true,
    val pocketTotalBalance: Double = 0.0,

    // Context menu
    val showContextMenu: Boolean = false,
    val contextMenuAccount: Account? = null,

    // Computed
    val displayedAccounts: List<Account>
        get() = when {
            isPocketEmpty -> accounts           // Empty pocket = all
            showPocketView -> pocketAsAccounts  // Pocket view
            else -> accounts                    // All view
        }
)
```

### HomeAction (Extended)

```kotlin
sealed interface HomeAction {
    // Existing...

    // Pocket Actions
    data object TogglePocketView : HomeAction
    data object ShowViewDropdown : HomeAction
    data object DismissViewDropdown : HomeAction
    data class ShowContextMenu(val account: Account) : HomeAction
    data object DismissContextMenu : HomeAction
    data class AddToPocket(val accountId: Long, val type: AccountType) : HomeAction
    data class RemoveFromPocket(val accountId: Long, val type: AccountType) : HomeAction
    data object NavigateToManagePocket : HomeAction
}
```

---

## Data Flow

```
┌────────────────────────────────────────────────────────────────────────┐
│                    HOME SCREEN WITH POCKET                              │
├────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  INIT:                                                                  │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐                        │
│  │  Home    │────▶│ Fetch    │────▶│ Pocket   │                        │
│  │  Screen  │     │ Accounts │     │ API      │                        │
│  └──────────┘     │ + Pocket │     └──────────┘                        │
│                   └────┬─────┘                                          │
│                        │                                                │
│                        ▼                                                │
│  DISPLAY LOGIC:                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  if (pocketAccounts.isEmpty())                                   │   │
│  │      displayedAccounts = allAccounts    // Show all              │   │
│  │      showPocketView = false                                      │   │
│  │  else                                                            │   │
│  │      displayedAccounts = pocketAccounts // Show pocket (default) │   │
│  │      showPocketView = true                                       │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  USER ACTIONS:                                                          │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐            │
│  │ Toggle View    │  │ Long Press     │  │ Manage Pocket  │            │
│  │ (Dropdown)     │  │ (Context Menu) │  │ (Full Screen)  │            │
│  └───────┬────────┘  └───────┬────────┘  └───────┬────────┘            │
│          │                   │                   │                      │
│          ▼                   ▼                   ▼                      │
│  Update displayMode    Show Add/Remove    Navigate to                  │
│  Refresh pager         API call           ManagePocketScreen           │
│                        Refresh pager                                    │
│                                                                         │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Module Structure

```
feature/home/ (MODIFIED)
└── src/commonMain/kotlin/org/mifospay/feature/home/
    ├── HomeScreen.kt              # Add dropdown, star indicators
    ├── HomeViewModel.kt           # Add pocket state, display logic
    ├── components/
    │   ├── AccountCard.kt         # Add star, long press
    │   ├── ViewDropdownMenu.kt    # NEW: View switcher
    │   └── AccountContextMenu.kt  # NEW: Long press menu

feature/pocket/ (NEW)
└── src/commonMain/kotlin/org/mifospay/feature/pocket/
    ├── PocketNavigation.kt
    ├── ManagePocketScreen.kt
    ├── ManagePocketViewModel.kt
    └── components/
        └── DelinkConfirmationDialog.kt
```

---

## Dependencies

### Home Module Changes

```kotlin
// feature/home/build.gradle.kts
dependencies {
    implementation(projects.core.data)  // Add PocketRepository
}
```

### New Pocket Module

```kotlin
// feature/pocket/build.gradle.kts
dependencies {
    implementation(projects.core.network)
    implementation(projects.core.data)
    implementation(projects.core.model)
    implementation(projects.core.designsystem)
}
```

---

## Testing Strategy

### Unit Tests

| Test | Description |
|------|-------------|
| `HomeViewModelPocketTest` | Display mode logic, toggle behavior |
| `ManagePocketViewModelTest` | Link/delink operations |
| `PocketRepositoryTest` | API calls and mapping |

### UI Tests

| Test | Description |
|------|-------------|
| `HomeScreenPocketTest` | Star indicators, dropdown, context menu |
| `ManagePocketScreenTest` | List interactions, star toggle |

---

## Implementation Phases

### Phase 1: Core Integration (P0)
- [ ] Add `PocketRepository` to HomeViewModel
- [ ] Implement display mode logic (empty → all, has accounts → pocket)
- [ ] Add star indicator to AccountCard
- [ ] Fetch pocket on Home screen init

### Phase 2: View Toggle (P0)
- [ ] Create ViewDropdownMenu component
- [ ] Implement view switching
- [ ] Update pager on toggle

### Phase 3: Quick Actions (P0)
- [ ] Add long press handler to AccountCard
- [ ] Create AccountContextMenu
- [ ] Implement Add/Remove from Pocket actions
- [ ] Add confirmation dialog for delink

### Phase 4: Full Management (P1)
- [ ] Create ManagePocketScreen
- [ ] Implement ManagePocketViewModel
- [ ] Add navigation from dropdown

---

## Related Documents

- **Flow:** `user-flows/flows/FLOW-pocket.md`
- **API:** `features/pocket/API.md`
- **Status:** `features/pocket/STATUS.md`
- **Jira:** MR-16 (Roadmap), MW-378 (Epic), MW-379-387 (Stories)

---

## Open Questions

1. **Q:** Should we persist view preference across sessions?
   **A:** P2 - Start with session-only, consider DataStore later

2. **Q:** What happens when last pocket account is delinked?
   **A:** Switch to All Accounts view automatically

3. **Q:** Should long press show different options based on account type?
   **A:** No - keep consistent for now, consider P2 enhancement
