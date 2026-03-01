# Plan: QR Code Generation - Multi-Wallet Account Support

> **Plan ID**: qr-multi-account-260228-001
> **Created**: 2026-02-28
> **Status**: Implemented
> **Feature**: mpay-qr (Receive Money / Generate QR)

---

## Problem Statement

Currently, the QR code generation (Receive Money) feature uses only the **default account** from `UserPreferencesRepository`. Users with multiple wallet accounts cannot:

1. Select which account to generate QR for
2. See all their accounts when receiving money
3. Generate QR for non-default accounts

**Current Behavior:**
- MpayQrScreen always uses `repository.defaultAccount.value`
- AccountSelectorCard shows only the default account
- No option to switch accounts within the QR screen

**Expected Behavior:**
1. Show all user accounts with ability to select
2. Generate Intra-Bank QR for any selected account
3. Generate Inter-Bank QR for accounts with external ID
4. Remember last selected account for convenience

---

## Root Cause Analysis

### File: `MpayQrViewModel.kt` (Lines 64-102)

```kotlin
val initialState = run {
    val client = repository.client.value
    val defaultAccount = repository.defaultAccount.value ?: DefaultAccount.DEFAULT  // ONLY default
    val accountExternalId = repository.getAccountExternalId(defaultAccount.accountId)

    MpayQrState(
        client = client,
        defaultAccount = defaultAccount,
        accountExternalId = accountExternalId ?: "",
    )
}
```

**Problem**: The ViewModel only fetches the default account, not all available accounts.

### File: `MpayQrScreen.kt` (Lines 239-245)

```kotlin
AccountSelectorCard(
    client = state.client,
    account = state.defaultAccount,
    isPrimary = true,  // Always primary
)
```

**Problem**: The UI shows only the default account with no selection capability.

---

## Solution Design

### Approach: Add Account Dropdown/Selector with Clickable Card

1. **Fetch all accounts** from repository (like HomeViewModel does)
2. **Make AccountSelectorCard clickable** to show account picker
3. **Update QR codes** when account changes
4. **Handle external ID availability** per account

### New State Model

```kotlin
data class MpayQrState(
    val client: Client,
    val accounts: List<Account> = emptyList(),      // NEW: All accounts
    val selectedAccount: Account? = null,            // NEW: Currently selected
    val defaultAccount: DefaultAccount,              // Keep for backwards compat
    val fspId: String = "",
    val accountExternalId: String = "",              // From selected account
    // ... rest of state
)
```

### UI Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  MpayQrScreen                                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  AccountSelectorCard (CLICKABLE)                          │  │
│  │  ┌─────┐  John Doe                                    ▼   │  │
│  │  │Logo │  Mifos Head Office                               │  │
│  │  └─────┘  ●●●● ●●●● 7890                   [Primary]      │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  [Tab: Intra-Bank QR] [Tab: Inter-Bank QR]                      │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    QR CODE / PLACEHOLDER                  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  [Set Amount]                                                    │
│  [Share] [Download]                                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

When AccountSelectorCard clicked:
┌───────────────────────────────────────────────────────────────┐
│  Select Account                                               │
├───────────────────────────────────────────────────────────────┤
│  ○ Savings Account - ****7890          ✓ Has External ID      │
│  ● Current Account - ****1234 (Selected)                      │
│  ○ Business Account - ****5678         ⚠ No External ID       │
└───────────────────────────────────────────────────────────────┘
```

---

## Implementation Tasks

### Task 1: Add Account Model Import and State Update
**File**: `feature/mpay-qr/.../MpayQrViewModel.kt`
**Priority**: P0 (Critical)
**Effort**: S

Add Account import and update state:
```kotlin
import org.mifospay.core.model.account.Account

data class MpayQrState(
    // ... existing fields
    val accounts: List<Account> = emptyList(),
    val selectedAccount: Account? = null,
    val isAccountPickerVisible: Boolean = false,
)
```

### Task 2: Fetch All Accounts in ViewModel
**File**: `feature/mpay-qr/.../MpayQrViewModel.kt`
**Priority**: P0 (Critical)
**Effort**: M

Add account fetching in init:
```kotlin
class MpayQrViewModel(
    private val accountRepository: SelfServiceAccountRepository,  // NEW dependency
    // ... other deps
) {
    init {
        loadAccounts()
        generateQr()
    }

    private fun loadAccounts() {
        viewModelScope.launch {
            when (val result = accountRepository.getActiveAccounts(state.client.id)) {
                is DataState.Success -> {
                    val accounts = result.data
                    val defaultAcc = accounts.find { it.id == state.defaultAccount.accountId }
                        ?: accounts.firstOrNull()

                    mutableStateFlow.update {
                        it.copy(
                            accounts = accounts,
                            selectedAccount = defaultAcc,
                            accountExternalId = defaultAcc?.externalId ?: "",
                        )
                    }
                    generateQr()  // Regenerate with selected account
                }
                is DataState.Error -> { /* Handle error */ }
            }
        }
    }
}
```

### Task 3: Add Account Selection Action
**File**: `feature/mpay-qr/.../MpayQrViewModel.kt`
**Priority**: P0 (Critical)
**Effort**: S

Add new actions:
```kotlin
sealed interface MpayQrAction {
    // ... existing actions
    data object ShowAccountPicker : MpayQrAction
    data object DismissAccountPicker : MpayQrAction
    data class SelectAccount(val account: Account) : MpayQrAction
}
```

Handle in ViewModel:
```kotlin
is MpayQrAction.ShowAccountPicker -> {
    mutableStateFlow.update { it.copy(isAccountPickerVisible = true) }
}

is MpayQrAction.DismissAccountPicker -> {
    mutableStateFlow.update { it.copy(isAccountPickerVisible = false) }
}

is MpayQrAction.SelectAccount -> {
    mutableStateFlow.update {
        it.copy(
            selectedAccount = action.account,
            accountExternalId = action.account.externalId ?: "",
            isAccountPickerVisible = false,
        )
    }
    generateQr()  // Regenerate QR for new account
}
```

### Task 4: Update QR Data Generation to Use Selected Account
**File**: `feature/mpay-qr/.../MpayQrViewModel.kt`
**Priority**: P0 (Critical)
**Effort**: M

Update `qrData` computed property:
```kotlin
val qrData: QrCodeData
    get() {
        val account = state.selectedAccount
        return QrCodeData(
            fspId = fspId,
            clientId = client.id,
            clientName = client.displayName,
            accountNo = account?.number ?: defaultAccount.accountNo,
            accountId = account?.id ?: defaultAccount.accountId,
            officeId = account?.officeId ?: client.officeId,
            accountTypeId = QrCodeData.ACCOUNT_TYPE_ID,
            accountExternalId = account?.externalId ?: "",
            currency = state.currency,
            amount = state.amount,
        )
    }
```

### Task 5: Create AccountPickerBottomSheet Component
**File**: `feature/mpay-qr/.../components/AccountPickerBottomSheet.kt` (NEW)
**Priority**: P0 (Critical)
**Effort**: M

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
internal fun AccountPickerBottomSheet(
    accounts: List<Account>,
    selectedAccount: Account?,
    onAccountSelected: (Account) -> Unit,
    onDismiss: () -> Unit,
    modifier: Modifier = Modifier,
) {
    ModalBottomSheet(
        onDismissRequest = onDismiss,
        sheetState = rememberModalBottomSheetState(),
    ) {
        Column(
            modifier = modifier
                .fillMaxWidth()
                .padding(KptTheme.spacing.md),
        ) {
            Text(
                text = stringResource(Res.string.feature_mpay_qr_select_account),
                style = KptTheme.typography.titleMedium,
            )

            Spacer(modifier = Modifier.height(KptTheme.spacing.md))

            accounts.forEach { account ->
                AccountPickerItem(
                    account = account,
                    isSelected = account.id == selectedAccount?.id,
                    hasExternalId = !account.externalId.isNullOrBlank(),
                    onClick = { onAccountSelected(account) },
                )
            }

            Spacer(modifier = Modifier.height(KptTheme.spacing.lg))
        }
    }
}

@Composable
private fun AccountPickerItem(
    account: Account,
    isSelected: Boolean,
    hasExternalId: Boolean,
    onClick: () -> Unit,
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() }
            .padding(KptTheme.spacing.md),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        RadioButton(
            selected = isSelected,
            onClick = onClick,
        )

        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = account.productName ?: account.name,
                style = KptTheme.typography.bodyMedium,
            )
            Text(
                text = formatAccountDisplay(account.number),
                style = KptTheme.typography.bodySmall,
                color = KptTheme.colorScheme.onSurfaceVariant,
            )
        }

        // External ID indicator
        if (hasExternalId) {
            Icon(
                imageVector = MifosIcons.Check,
                contentDescription = "Has external ID",
                tint = KptTheme.colorScheme.primary,
            )
        } else {
            Icon(
                imageVector = MifosIcons.Info,
                contentDescription = "No external ID",
                tint = KptTheme.colorScheme.error,
            )
        }
    }
}
```

### Task 6: Make AccountSelectorCard Clickable
**File**: `feature/mpay-qr/.../components/AccountSelectorCard.kt`
**Priority**: P0 (Critical)
**Effort**: S

Add click handler and dropdown indicator:
```kotlin
@Composable
internal fun AccountSelectorCard(
    client: Client,
    account: Account,              // Changed from DefaultAccount
    isPrimary: Boolean,
    hasMultipleAccounts: Boolean,  // NEW
    onClick: (() -> Unit)? = null, // NEW
    modifier: Modifier = Modifier,
) {
    Card(
        modifier = modifier
            .fillMaxWidth()
            .then(
                if (onClick != null && hasMultipleAccounts) {
                    Modifier.clickable { onClick() }
                } else Modifier
            ),
        // ... rest of card
    ) {
        Row(...) {
            // ... existing content

            // Add dropdown indicator if multiple accounts
            if (hasMultipleAccounts) {
                Icon(
                    imageVector = MifosIcons.DropDown,
                    contentDescription = "Select account",
                    tint = KptTheme.colorScheme.onSurfaceVariant,
                )
            }

            // Primary badge
            if (isPrimary) {
                PrimaryBadge()
            }
        }
    }
}
```

### Task 7: Update MpayQrScreen to Show Account Picker
**File**: `feature/mpay-qr/.../MpayQrScreen.kt`
**Priority**: P0 (Critical)
**Effort**: M

Add account picker integration:
```kotlin
@Composable
internal fun MpayQrScreenContent(...) {
    // ... existing code

    // Account Picker Bottom Sheet
    if (state.isAccountPickerVisible) {
        AccountPickerBottomSheet(
            accounts = state.accounts,
            selectedAccount = state.selectedAccount,
            onAccountSelected = { account ->
                onAction(MpayQrAction.SelectAccount(account))
            },
            onDismiss = {
                onAction(MpayQrAction.DismissAccountPicker)
            },
        )
    }

    // Update AccountSelectorCard
    item {
        AccountSelectorCard(
            client = state.client,
            account = state.selectedAccount ?: state.defaultAccount.toAccount(),
            isPrimary = state.selectedAccount?.id == state.defaultAccount.accountId,
            hasMultipleAccounts = state.accounts.size > 1,
            onClick = {
                onAction(MpayQrAction.ShowAccountPicker)
            },
        )
    }
}
```

### Task 8: Add DI for Account Repository
**File**: `feature/mpay-qr/.../di/MpayQrModule.kt`
**Priority**: P0 (Critical)
**Effort**: S

Add repository dependency:
```kotlin
val mpayQrModule = module {
    viewModelOf(::MpayQrViewModel)
}

// Ensure SelfServiceAccountRepository is injected
class MpayQrViewModel(
    private val accountRepository: SelfServiceAccountRepository,  // From core:data
    localRepository: LocalAssetRepository,
    repository: UserPreferencesRepository,
    // ... other deps
)
```

### Task 9: Add String Resources
**File**: `feature/mpay-qr/.../composeResources/values/strings.xml`
**Priority**: P1 (High)
**Effort**: S

Add new strings:
```xml
<string name="feature_mpay_qr_select_account">Select Account</string>
<string name="feature_mpay_qr_has_external_id">Inter-bank enabled</string>
<string name="feature_mpay_qr_no_external_id">Inter-bank not available</string>
<string name="feature_mpay_qr_account_selected">Account selected</string>
```

### Task 10: Update Tests
**File**: `feature/mpay-qr/src/commonTest/.../MpayQrViewModelTest.kt`
**Priority**: P1 (High)
**Effort**: M

Add test cases:
- `loadAccounts_success_setsAccountsList`
- `selectAccount_updatesSelectedAccountAndRegeneratesQr`
- `selectAccount_withNoExternalId_showsInterBankPlaceholder`
- `selectAccount_withExternalId_generatesBothQrCodes`

---

## Verification Checklist

After implementation:
- [x] All accounts loaded and displayed in picker
- [x] Default account pre-selected on screen open
- [x] Account selection updates both QR codes
- [x] Inter-bank placeholder shown for accounts without external ID
- [x] Primary badge shows for default account
- [x] Share/Download works for selected account's QR
- [x] Amount changes apply to selected account's QR
- [x] Build compiles successfully
- [ ] Tests pass (P1 - can be added in follow-up)

---

## Files to Create/Modify

| Action | File |
|--------|------|
| UPDATE | `feature/mpay-qr/.../MpayQrViewModel.kt` |
| UPDATE | `feature/mpay-qr/.../MpayQrScreen.kt` |
| UPDATE | `feature/mpay-qr/.../components/AccountSelectorCard.kt` |
| CREATE | `feature/mpay-qr/.../components/AccountPickerBottomSheet.kt` |
| UPDATE | `feature/mpay-qr/.../di/MpayQrModule.kt` |
| UPDATE | `feature/mpay-qr/.../composeResources/values/strings.xml` |
| UPDATE | `feature/mpay-qr/src/commonTest/.../MpayQrViewModelTest.kt` |

---

## Dependencies

### Required from core:data
- `SelfServiceAccountRepository.getActiveAccounts(clientId)`

### Required from core:model
- `Account` data class (already has `externalId` field)

---

## Estimated Scope

- **New files**: 1 (AccountPickerBottomSheet.kt)
- **Modified files**: 6
- **Priority**: P1 (Feature Enhancement)
- **Effort**: M (Medium - ~3-4 hours)

---

## Related

- **PLAN-qr-external-id-260228-001**: Previous fix for inter-bank QR placeholder (IMPLEMENTED)
- **HomeViewModel.kt**: Reference for account loading pattern (Lines 50-114)
- **TransactionFilterBottomSheet**: Reference for bottom sheet pattern

---

## UI Mockup (ASCII)

### Initial State (Default Account Selected)
```
┌─────────────────────────────────────────────────────────────────┐
│  Receive Money                                            [←]  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Scan to pay me using any payment app                           │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  [Logo]  John Doe                                     ▼   │  │
│  │          Mifos Head Office                                │  │
│  │          ●●●● ●●●● 7890               [✓ Primary]         │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│        [Intra-Bank QR]        [Inter-Bank QR]                   │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                                                           │  │
│  │                       ████████████                        │  │
│  │                       ██        ██                        │  │
│  │                       ██  QR    ██                        │  │
│  │                       ██        ██                        │  │
│  │                       ████████████                        │  │
│  │                                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                     [Set Amount]                          │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│          [Share]                    [Download]                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Account Picker Bottom Sheet
```
┌─────────────────────────────────────────────────────────────────┐
│  Select Account                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ◉ Savings Account                                         ✓   │
│    ●●●● ●●●● 7890                        (Inter-bank enabled)  │
│                                                                 │
│  ────────────────────────────────────────────────────────────   │
│                                                                 │
│  ○ Current Account                                         ✓   │
│    ●●●● ●●●● 1234                        (Inter-bank enabled)  │
│                                                                 │
│  ────────────────────────────────────────────────────────────   │
│                                                                 │
│  ○ Business Account                                        ⚠   │
│    ●●●● ●●●● 5678                        (No external ID)      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```
