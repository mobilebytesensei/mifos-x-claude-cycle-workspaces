# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mobile-wallet/plan-layer/plans/PLAN-qr-beneficiary-office-260301-001.md"
# last_modified: "2026-03-20"

# Plan: QR Scan Beneficiary - Office Name Lookup

> **Plan ID**: qr-beneficiary-office-260301-001
> **Created**: 2026-03-01
> **Status**: ✅ Implemented
> **Completed**: 2026-03-01
> **Priority**: P2 (Enhancement)
> **Codename**: Office Resolver

---

## Problem Statement

When scanning an INTRA_BANK QR code and the beneficiary doesn't exist, the system navigates to Add Beneficiary with pre-filled data. However, the `officeName` is hardcoded to "Head Office" instead of being resolved from the `officeId` in the QR code.

### Current State

```
QR Code Data:
├── officeId: 5 (Long)
└── (no officeName)

FastMpayProcessor.convertToBeneficiaryJson():
└── officeName = "Head Office"  ← HARDCODED ❌
```

### Expected State

```
QR Code Data:
├── officeId: 5 (Long)
└── (no officeName)

FastMpayProcessor.processIntraBankQr():
├── 1. Fetch office list from API
├── 2. Find office where id == qrData.officeId
├── 3. Use office.name for beneficiary
└── officeName = "Lagos Branch"  ← RESOLVED ✅
```

---

## Existing Infrastructure

### Already Available

| Component | Location | Status |
|-----------|----------|:------:|
| OfficeService | `core/network/services/OfficeService.kt` | ✅ |
| Office model | `core/model/office/Office.kt` | ✅ |
| OfficeRepository | `core/data/repository/OfficeRepository.kt` | ✅ |
| getOffices() | Returns `List<Office>` | ✅ |

### QR Code Data Fields

| Field | Type | Available | Used For |
|-------|------|:---------:|----------|
| officeId | Long | ✅ | Office lookup |
| clientName | String | ✅ | Beneficiary name |
| accountNo | String | ✅ | Account number |
| accountTypeId | Long | ✅ | Account type |

---

## Solution Design

### Approach: Fetch offices and find by ID

```kotlin
// In FastMpayProcessor
private suspend fun resolveOfficeName(officeId: Long): String {
    return try {
        val result = officeRepository.getOffices().first()
        when (result) {
            is DataState.Success -> {
                result.data.find { it.id == officeId }?.name
                    ?: DEFAULT_OFFICE_NAME
            }
            else -> DEFAULT_OFFICE_NAME
        }
    } catch (e: Exception) {
        DEFAULT_OFFICE_NAME
    }
}

companion object {
    const val DEFAULT_OFFICE_NAME = "Head Office"
}
```

---

## Implementation Tasks

### Task 1: Add OfficeRepository to FastMpayProcessor
**File**: `feature/fast-mpay/src/commonMain/kotlin/.../FastMpayProcessor.kt`

```kotlin
class FastMpayProcessor(
    private val beneficiaryRepository: BeneficiaryRepository,
    private val userPreferencesRepository: UserPreferencesRepository,
    private val officeRepository: OfficeRepository,  // ADD
) {
```

### Task 2: Add resolveOfficeName() function
**File**: `feature/fast-mpay/src/commonMain/kotlin/.../FastMpayProcessor.kt`

```kotlin
private suspend fun resolveOfficeName(officeId: Long): String {
    return try {
        val result = officeRepository.getOffices().first()
        when (result) {
            is DataState.Success -> {
                result.data.find { it.id == officeId }?.name
                    ?: DEFAULT_OFFICE_NAME
            }
            else -> DEFAULT_OFFICE_NAME
        }
    } catch (e: Exception) {
        DEFAULT_OFFICE_NAME
    }
}

companion object {
    const val DEFAULT_OFFICE_NAME = "Head Office"
}
```

### Task 3: Update convertToBeneficiaryJson() to use resolved name
**File**: `feature/fast-mpay/src/commonMain/kotlin/.../FastMpayProcessor.kt`

Change from:
```kotlin
private fun convertToBeneficiaryJson(qrData: QrCodeData): String {
    val beneficiary = Beneficiary(
        ...
        officeName = "Head Office",  // HARDCODED
        ...
    )
}
```

To:
```kotlin
private suspend fun convertToBeneficiaryJson(
    qrData: QrCodeData,
    officeName: String,
): String {
    val beneficiary = Beneficiary(
        ...
        officeName = officeName,  // RESOLVED
        ...
    )
}
```

### Task 4: Update processIntraBankQr() to resolve office first
**File**: `feature/fast-mpay/src/commonMain/kotlin/.../FastMpayProcessor.kt`

```kotlin
private suspend fun processIntraBankQr(qrData: QrCodeData): QrProcessResult {
    // ... bank mismatch check ...

    // Resolve office name early
    val officeName = resolveOfficeName(qrData.officeId)

    return try {
        val beneficiaryResult = beneficiaryRepository.getBeneficiaryList().first()
        when (beneficiaryResult) {
            is DataState.Success -> {
                val existingBeneficiary = beneficiaryResult.data.find {
                    it.accountNumber == qrData.accountNo
                }
                if (existingBeneficiary != null) {
                    QrProcessResult.NavigateToMakeTransfer(...)
                } else {
                    val beneficiaryJson = convertToBeneficiaryJson(qrData, officeName)
                    QrProcessResult.NavigateToAddBeneficiary(beneficiaryJson)
                }
            }
            // ... error handling uses officeName ...
        }
    }
}
```

### Task 5: Update DI Module
**File**: `feature/fast-mpay/src/commonMain/kotlin/.../FastMpayModule.kt` (or similar)

Add OfficeRepository to the FastMpayProcessor factory.

### Task 6: Update Tests
**File**: `feature/fast-mpay/src/commonTest/kotlin/.../FastMpayProcessorTest.kt`

- Mock OfficeRepository
- Test office name resolution success
- Test fallback to "Head Office" on error

---

## Files to Modify

| Action | File | Description |
|--------|------|-------------|
| UPDATE | `feature/fast-mpay/.../FastMpayProcessor.kt` | Add office lookup |
| UPDATE | `feature/fast-mpay/.../FastMpayModule.kt` | Add OfficeRepository to DI |
| UPDATE | `feature/fast-mpay/.../FastMpayProcessorTest.kt` | Add office tests |

---

## API Reference

### GET /offices
Returns list of all offices.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Head Office",
    "nameDecorated": "Head Office",
    "externalId": "HO001",
    "hierarchy": ".1."
  },
  {
    "id": 5,
    "name": "Lagos Branch",
    "nameDecorated": "..Lagos Branch",
    "externalId": "LB005",
    "hierarchy": ".1.5."
  }
]
```

### Add Beneficiary Request (for reference)

**POST /beneficiaries/tpt**
```json
{
  "locale": "en_GB",
  "name": "John Doe",
  "accountNumber": "ACC001",
  "accountType": 2,
  "transferLimit": 0,
  "officeName": "Lagos Branch"  // ← This is what we're fixing
}
```

---

## Verification Checklist

After implementation:
- [ ] Scan QR with officeId=1 → "Head Office" in Add Beneficiary
- [ ] Scan QR with officeId=5 → Resolved office name (e.g., "Lagos Branch")
- [ ] Office API error → Falls back to "Head Office"
- [ ] Existing beneficiary → Navigates to Make Transfer (unchanged)
- [ ] Unit tests pass

---

## Task Summary

| # | Task | Priority | Effort | Status |
|---|------|:--------:|:------:|:------:|
| 1 | Add OfficeRepository to FastMpayProcessor | P0 | S | ✅ |
| 2 | Add resolveOfficeName() function | P0 | S | ✅ |
| 3 | Update convertToBeneficiaryJson() signature | P0 | S | ✅ |
| 4 | Update processIntraBankQr() flow | P0 | M | ✅ |
| 5 | Update DI Module | P0 | S | ✅ |
| 6 | Update Tests | P1 | M | ✅ |

**Total**: 6 tasks
**Effort**: Small

---

## Notes

### Why not add GET /offices/{id}?

The Fineract API doesn't have a single-office endpoint by default. Adding one would require backend changes. Using the existing `getOffices()` and filtering client-side is simpler.

### Performance Consideration

Offices are typically a small list (<100 items). The overhead of fetching all and filtering is negligible. For optimization, offices could be cached in UserPreferences on login.

### Fallback Strategy

If office resolution fails for any reason, the system falls back to "Head Office" to ensure the user can still add the beneficiary. The user can manually change the office if needed.

---

## Flow Diagram (Updated)

```
┌─────────────────────────────────────────────────────────────────────┐
│                     QR SCAN INTRA-BANK FLOW                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐                                                   │
│  │  Scan QR     │                                                   │
│  │  (INTRA_BANK)│                                                   │
│  └──────┬───────┘                                                   │
│         │                                                           │
│         ▼                                                           │
│  ┌──────────────┐     ┌──────────────┐                              │
│  │ Check FSP ID │────▶│ Bank Mismatch│──▶ Show error/option         │
│  └──────┬───────┘     └──────────────┘                              │
│         │ Same FSP                                                  │
│         ▼                                                           │
│  ┌──────────────────┐                                               │
│  │ Resolve Office   │  GET /offices → find(id == officeId)         │
│  │ Name from ID     │                                               │
│  └──────┬───────────┘                                               │
│         │                                                           │
│         ▼                                                           │
│  ┌──────────────┐                                                   │
│  │ Fetch        │  GET /beneficiaries/tpt                          │
│  │ Beneficiaries│                                                   │
│  └──────┬───────┘                                                   │
│         │                                                           │
│         ▼                                                           │
│  ┌──────────────────────────────────────┐                           │
│  │ Match by accountNumber?              │                           │
│  └──────────────┬───────────────────────┘                           │
│                 │                                                   │
│     ┌───────────┴───────────┐                                       │
│     │                       │                                       │
│     ▼ YES                   ▼ NO                                    │
│  ┌──────────────┐    ┌──────────────────┐                           │
│  │ Navigate to  │    │ Navigate to      │                           │
│  │ Make Transfer│    │ Add Beneficiary  │                           │
│  │ (Send Money) │    │ (Pre-filled with │                           │
│  │              │    │  resolved office)│                           │
│  └──────────────┘    └──────────────────┘                           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```
