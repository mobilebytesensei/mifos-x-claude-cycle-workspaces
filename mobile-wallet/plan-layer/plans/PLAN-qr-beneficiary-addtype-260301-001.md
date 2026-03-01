# Plan: QR Scan - Navigate to Add Beneficiary (Not Update)

> **Plan ID**: qr-beneficiary-addtype-260301-001
> **Created**: 2026-03-01
> **Status**: ✅ Implemented
> **Priority**: P0 (Bug Fix)
> **Codename**: Add Type Fix

---

## Problem Statement

When scanning a QR code and the beneficiary doesn't exist, the system navigates to "Update Beneficiary" instead of "Add Beneficiary".

### Root Cause

The navigation code uses `BeneficiaryAddEditType.EditItem(beneficiaryData)` instead of a proper "Add with pre-filled data" type.

**Bug Location** (`MifosNavHost.kt:300-308`):
```kotlin
onNavigateToAddBeneficiary = { beneficiaryData ->
    navController.navigateToBeneficiaryAddEdit(
        BeneficiaryAddEditType.EditItem(beneficiaryData),  // ← BUG: Using EditItem
        ...
    )
}
```

### Current Behavior

| QR Scan Result | Expected Screen | Actual Screen |
|---------------|-----------------|---------------|
| New beneficiary | **Add Beneficiary** | ❌ Update Beneficiary |
| Title shown | "Add Beneficiary" | ❌ "Update Beneficiary" |
| Button shown | "Save" | ❌ "Update" |
| API called | POST `/beneficiaries/tpt` | ❌ PUT `/beneficiaries/tpt/{id}` (fails - no ID) |

### Expected Behavior

| QR Scan Result | Screen | Title | Button | API |
|---------------|--------|-------|--------|-----|
| New beneficiary | Add Beneficiary | "Add Beneficiary" | "Save" | POST |
| Pre-filled fields | Yes | - | - | - |

---

## Solution Design (Implemented + Refactored)

### Final Implementation: Renamed Types for Clarity

```kotlin
@Serializable
sealed class BeneficiaryAddEditType {

    abstract val beneficiary: String?

    // Manual add (empty form)
    @Serializable
    data object AddManualItem : BeneficiaryAddEditType() {
        override val beneficiary: String?
            get() = null
    }

    // Add from QR scan (pre-filled form)
    @Serializable
    data class AddScannedItem(
        override val beneficiary: String,
    ) : BeneficiaryAddEditType()

    // Edit existing beneficiary
    @Serializable
    data class EditItem(
        override val beneficiary: String,
    ) : BeneficiaryAddEditType()
}
```

**Route Types:**
- `ADD_TYPE = "add_beneficiary"` → `AddManualItem`
- `SCAN_TYPE = "scan_beneficiary"` → `AddScannedItem`
- `EDIT_TYPE = "edit_beneficiary"` → `EditItem`

**Benefits:**
- Clear semantic distinction: Manual vs Scanned vs Edit
- Each type has its own route constant (no ambiguity)
- Pre-filled data for QR scan flow
- Correct API call (POST vs PUT)
- Correct title/button text

---

## Implementation Tasks

### Task 1: Add `AddItemWithData` to `BeneficiaryAddEditType`
**File**: `feature/accounts/src/commonMain/kotlin/.../BeneficiaryAddEditType.kt`

```kotlin
@Serializable
data class AddItemWithData(
    override val beneficiary: String,
) : BeneficiaryAddEditType()
```

### Task 2: Update `AddEditBeneficiaryViewModel` to handle `AddItemWithData`
**File**: `feature/accounts/src/commonMain/kotlin/.../AddEditBeneficiaryViewModel.kt`

Change initialState logic:
```kotlin
when (val addEditType = BeneficiaryAddEditArgs(savedStateHandle).addEditType) {
    is BeneficiaryAddEditType.AddItem -> {
        AEBState(name = "", accountNumber = "", ...)
    }

    // NEW: Handle AddItemWithData - pre-fill form but use Add mode
    is BeneficiaryAddEditType.AddItemWithData -> {
        val beneficiary = json.decodeFromString(...)
        AEBState(
            name = beneficiary.name,
            accountNumber = beneficiary.accountNumber,
            transferLimit = beneficiary.transferLimit,
            officeName = beneficiary.officeName,
            // NOTE: beneficiaryId is NULL - this is Add mode
            beneficiaryId = null,
            addEditType = addEditType,
        )
    }

    is BeneficiaryAddEditType.EditItem -> {
        // Existing logic for Edit
    }
}
```

### Task 3: Update `AEBState.isAddItemMode` check
**File**: `feature/accounts/src/commonMain/kotlin/.../AddEditBeneficiaryViewModel.kt`

```kotlin
private val isAddItemMode: Boolean
    get() = addEditType is BeneficiaryAddEditType.AddItem ||
            addEditType is BeneficiaryAddEditType.AddItemWithData
```

### Task 4: Update navigation in `MifosNavHost.kt`
**File**: `cmp-shared/src/commonMain/kotlin/.../MifosNavHost.kt`

Change line 300-308:
```kotlin
onNavigateToAddBeneficiary = { beneficiaryData ->
    navController.navigateToBeneficiaryAddEdit(
        BeneficiaryAddEditType.AddItemWithData(beneficiaryData),  // FIXED
        navOptions = navOptions {
            popUpTo(FAST_MPAY_ROUTE) {
                inclusive = true
            }
        },
    )
},
```

Also fix line 481-489 (`scanQrScreen` callback):
```kotlin
navigateToAddBeneficiaryScreen = {
    navController.navigateToBeneficiaryAddEdit(
        BeneficiaryAddEditType.AddItemWithData(it),  // FIXED
        navOptions = navOptions {
            popUpTo(SCAN_QR_ROUTE) {
                inclusive = true
            }
        },
    )
},
```

### Task 5: Update tests
**File**: `feature/accounts/src/commonTest/kotlin/.../AddEditBeneficiaryViewModelTest.kt`

Add test for `AddItemWithData`:
- Should pre-fill form fields
- Should show "Add Beneficiary" title
- Should show "Save" button
- Should call POST API (createBeneficiary)

---

## Files to Modify

| Action | File | Description |
|--------|------|-------------|
| UPDATE | `feature/accounts/.../BeneficiaryAddEditType.kt` | Add `AddItemWithData` type |
| UPDATE | `feature/accounts/.../AddEditBeneficiaryViewModel.kt` | Handle new type + fix isAddItemMode |
| UPDATE | `cmp-shared/.../MifosNavHost.kt` | Fix both navigation callbacks |
| UPDATE | `feature/accounts/.../BeneficiaryNavigation.kt` | Fix Args parsing to distinguish AddItem vs AddItemWithData |
| UPDATE | `feature/accounts/.../AddEditBeneficiaryViewModelTest.kt` | Add test for new type |

---

## Verification Checklist

After implementation:
- [ ] Scan QR for new beneficiary → Shows "Add Beneficiary" title
- [ ] Scan QR for new beneficiary → Shows "Save" button
- [ ] Scan QR for new beneficiary → Form pre-filled with QR data
- [ ] Scan QR for new beneficiary → POST API called on save
- [ ] Scan QR for existing beneficiary → Navigate to Make Transfer (unchanged)
- [ ] Manual add beneficiary → Still works (AddItem)
- [ ] Manual edit beneficiary → Still works (EditItem)
- [ ] Unit tests pass

---

## Task Summary

| # | Task | Priority | Effort | Status |
|---|------|:--------:|:------:|:------:|
| 1 | Add `AddItemWithData` to `BeneficiaryAddEditType` | P0 | S | ✅ |
| 2 | Handle `AddItemWithData` in ViewModel initialState | P0 | S | ✅ |
| 3 | Fix `isAddItemMode` check | P0 | S | ✅ |
| 4 | Fix navigation in `MifosNavHost.kt` (2 locations) | P0 | S | ✅ |
| 5 | Add tests for `AddItemWithData` | P1 | M | ⬜ |

**Total**: 5 tasks
**Effort**: Small-Medium

---

## Notes

### Why not just change EditItem to AddItem?

`AddItem` has `beneficiary = null`, so pre-filling wouldn't work. We need a distinct type that:
1. Pre-fills form data (like EditItem)
2. Uses Add mode for API/UI (like AddItem)

### Alternative: Remove beneficiaryId check

Could check `beneficiaryId == null` instead of type, but type-based approach is cleaner and more explicit.

---

## Flow Diagram (After Fix)

```
┌─────────────────────────────────────────────────────────────────────┐
│                     QR SCAN → ADD BENEFICIARY FLOW                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐                                                   │
│  │  Scan QR     │                                                   │
│  │  (INTRA_BANK)│                                                   │
│  └──────┬───────┘                                                   │
│         │                                                           │
│         ▼                                                           │
│  ┌──────────────┐                                                   │
│  │ Check if     │                                                   │
│  │ beneficiary  │                                                   │
│  │ exists?      │                                                   │
│  └──────┬───────┘                                                   │
│         │                                                           │
│     ┌───┴───┐                                                       │
│     │       │                                                       │
│     ▼ YES   ▼ NO                                                    │
│  ┌──────────────┐    ┌──────────────────────────────────────────┐   │
│  │ Navigate to  │    │ Navigate to Add Beneficiary              │   │
│  │ Make Transfer│    │ ┌──────────────────────────────────────┐ │   │
│  │ (Send Money) │    │ │ Type: AddItemWithData(beneficiary)   │ │   │
│  └──────────────┘    │ │ Title: "Add Beneficiary"  ✅         │ │   │
│                      │ │ Button: "Save"  ✅                   │ │   │
│                      │ │ Pre-filled: Yes  ✅                  │ │   │
│                      │ │ API: POST  ✅                        │ │   │
│                      │ └──────────────────────────────────────┘ │   │
│                      └──────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```
