# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mobile-wallet/plan-layer/plans/PLAN-qr-external-id-260228-001.md"
# last_modified: "2026-03-20"

# Plan: QR Code Generation - Handle Missing External ID

> **Plan ID**: qr-external-id-260228-001
> **Created**: 2026-02-28
> **Status**: Implemented
> **Feature**: mpay-qr (Receive Money / Generate QR)

---

## Problem Statement

When `accountExternalId` is null or empty, the current implementation throws an error **for both QR types** with the generic message "Unable to Generate QR Code". This is incorrect because:

1. **Intra-Bank QR** does NOT require `accountExternalId` - it uses internal IDs (`clientId`, `accountId`)
2. **Inter-Bank QR** REQUIRES `accountExternalId` - this is correct validation

**Current Behavior:**
- Both QR tabs show "Unable to Generate QR Code" error
- User cannot generate ANY QR code even though Intra-Bank should work

**Expected Behavior:**
1. **Intra-Bank QR**: Generate successfully (uses internal IDs)
2. **Inter-Bank QR**: Show humanized placeholder explaining external ID is needed

---

## Root Cause Analysis

### File: `MpayQrCodeProcessor.kt` (lines 226-229)

```kotlin
QrCodeType.INTER_BANK -> {
    require(!data.accountExternalId.isNullOrBlank()) {
        "Account external ID is required for inter-bank QR"
    }
}
```

The validation is correct for INTER_BANK type, but the error propagates and blocks BOTH QR codes.

### File: `MpayQrViewModel.kt` (lines 218-242)

```kotlin
try {
    val (intraBankData, interBankData) = withContext(ioDispatcher) {
        Pair(
            MpayQrCodeProcessor.encodeMpayString(state.qrData),        // Intra-bank
            MpayQrCodeProcessor.encodeMpayString(state.interBankQrData), // Inter-bank - FAILS HERE
        )
    }
    // ...
} catch (e: IllegalArgumentException) {
    // Shows error for BOTH - even though only inter-bank failed
    mutableStateFlow.update {
        it.copy(viewState = MpayQrState.ViewState.Error(e.message ?: "Failed to generate QR code"))
    }
}
```

**Problem**: The code generates both QR codes in a single try-catch. When inter-bank fails (no external ID), it catches the error and shows error state for the entire screen.

---

## Solution Design

### Approach: Independent QR Generation with Placeholder

1. **Generate QR codes independently** - don't let one failure block the other
2. **Intra-Bank**: Always generate (has internal IDs)
3. **Inter-Bank**: Either generate OR show placeholder with humanized message

### New ViewState Model

```kotlin
data class Content(
    val intraBankData: String,                    // Always populated
    val interBankData: String?,                   // null if external ID missing
    val interBankUnavailableReason: String? = null, // Humanized message
)
```

### Humanized Messages

For Inter-Bank QR placeholder:

```
Title: "Inter-Bank QR Not Available"

Message: "Your account doesn't have an external ID configured yet.
External IDs are required for cross-bank transfers.

Please contact your bank to set up an external ID for this account."
```

Or shorter version:
```
"External ID not configured. Contact your bank to enable inter-bank transfers."
```

---

## Implementation Tasks

### Task 1: Update ViewState Content Model
**File**: `feature/mpay-qr/.../MpayQrViewModel.kt`
**Priority**: P0 (Critical)
**Effort**: S

Add nullable inter-bank data and reason:
```kotlin
data class Content(
    val intraBankData: String,
    val interBankData: String?,                   // NEW: nullable
    val interBankUnavailableReason: String? = null, // NEW
    // ... rest of properties
)
```

### Task 2: Update generateQr() Logic
**File**: `feature/mpay-qr/.../MpayQrViewModel.kt`
**Priority**: P0 (Critical)
**Effort**: M

Separate QR generation:
```kotlin
private fun generateQr() {
    viewModelScope.launch {
        // Check default account
        if (state.defaultAccount.accountNo.isBlank()) {
            // ... existing error
            return@launch
        }

        // Generate Intra-Bank QR (always works with internal IDs)
        val intraBankData = withContext(ioDispatcher) {
            MpayQrCodeProcessor.encodeMpayString(state.qrData)
        }

        // Try to generate Inter-Bank QR
        val (interBankData, interBankReason) = withContext(ioDispatcher) {
            if (state.accountExternalId.isBlank()) {
                // No external ID - return null with reason
                null to Res.string.feature_mpay_qr_external_id_required
            } else {
                try {
                    MpayQrCodeProcessor.encodeMpayString(state.interBankQrData) to null
                } catch (e: IllegalArgumentException) {
                    null to e.message
                }
            }
        }

        mutableStateFlow.update {
            it.copy(
                viewState = MpayQrState.ViewState.Content(
                    intraBankData = intraBankData,
                    interBankData = interBankData,
                    interBankUnavailableReason = interBankReason,
                ),
            )
        }
    }
}
```

### Task 3: Update initiateSetAmount() Logic
**File**: `feature/mpay-qr/.../MpayQrViewModel.kt`
**Priority**: P0 (Critical)
**Effort**: S

Apply same logic when updating amount:
```kotlin
private fun initiateSetAmount() {
    viewModelScope.launch {
        val intraBankData = withContext(ioDispatcher) {
            MpayQrCodeProcessor.encodeMpayString(state.qrData)
        }

        val interBankData = if (state.accountExternalId.isNotBlank()) {
            withContext(ioDispatcher) {
                MpayQrCodeProcessor.encodeMpayString(state.interBankQrData)
            }
        } else {
            null
        }

        updateContent {
            it.copy(
                intraBankData = intraBankData,
                interBankData = interBankData,
            )
        }
        // ... dismiss dialog
    }
}
```

### Task 4: Add String Resources
**File**: `feature/mpay-qr/src/commonMain/composeResources/values/strings.xml`
**Priority**: P0 (Critical)
**Effort**: S

Add humanized error messages:
```xml
<string name="feature_mpay_qr_inter_bank_unavailable">Inter-Bank QR Not Available</string>
<string name="feature_mpay_qr_external_id_required">Your account doesn\'t have an external ID configured. Contact your bank to enable inter-bank transfers.</string>
```

### Task 5: Create InterBankPlaceholder Composable
**File**: `feature/mpay-qr/.../components/InterBankPlaceholder.kt` (NEW)
**Priority**: P0 (Critical)
**Effort**: M

```kotlin
@Composable
fun InterBankPlaceholder(
    reason: String,
    modifier: Modifier = Modifier,
) {
    Card(
        modifier = modifier
            .fillMaxWidth()
            .aspectRatio(1f),
        colors = CardDefaults.cardColors(
            containerColor = KptTheme.colorScheme.surfaceVariant,
        ),
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(KptTheme.spacing.lg),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally,
        ) {
            Icon(
                imageVector = Icons.Default.Info,
                contentDescription = null,
                modifier = Modifier.size(48.dp),
                tint = KptTheme.colorScheme.onSurfaceVariant,
            )

            Spacer(modifier = Modifier.height(KptTheme.spacing.md))

            Text(
                text = stringResource(Res.string.feature_mpay_qr_inter_bank_unavailable),
                style = KptTheme.typography.titleMedium,
                color = KptTheme.colorScheme.onSurfaceVariant,
                textAlign = TextAlign.Center,
            )

            Spacer(modifier = Modifier.height(KptTheme.spacing.sm))

            Text(
                text = reason,
                style = KptTheme.typography.bodyMedium,
                color = KptTheme.colorScheme.onSurfaceVariant,
                textAlign = TextAlign.Center,
            )
        }
    }
}
```

### Task 6: Update MpayQrScreen to Show Placeholder
**File**: `feature/mpay-qr/.../MpayQrScreen.kt`
**Priority**: P0 (Critical)
**Effort**: M

Update the HorizontalPager content:
```kotlin
HorizontalPager(
    state = pagerState,
    modifier = Modifier.fillMaxWidth(),
    key = { it },
) { page ->
    Box(
        modifier = Modifier.fillMaxWidth(),
        contentAlignment = Alignment.Center,
    ) {
        when (page) {
            0 -> {
                // Intra-Bank - always show QR
                QrCodeCard(
                    data = contentState.intraBankData,
                    options = contentState.options,
                    qrType = QrType.INTRA_BANK,
                )
            }
            1 -> {
                // Inter-Bank - show QR or placeholder
                if (contentState.interBankData != null) {
                    QrCodeCard(
                        data = contentState.interBankData,
                        options = contentState.options,
                        qrType = QrType.INTER_BANK,
                    )
                } else {
                    InterBankPlaceholder(
                        reason = contentState.interBankUnavailableReason
                            ?: stringResource(Res.string.feature_mpay_qr_external_id_required),
                    )
                }
            }
        }
    }
}
```

### Task 7: Update Share/Download to Handle Null Inter-Bank
**File**: `feature/mpay-qr/.../MpayQrScreen.kt`
**Priority**: P1 (High)
**Effort**: S

Disable share/download when on inter-bank page with no data:
```kotlin
val currentData = when {
    pagerState.currentPage == 0 -> contentState.intraBankData
    contentState.interBankData != null -> contentState.interBankData
    else -> null
}

QrActionButtons(
    enabled = currentData != null,
    onShareClick = {
        currentData?.let { data ->
            val bytes = rememberQrCodePainter(data, contentState.options)
                .toByteArray(1024, 1024, ImageFormat.PNG)
            onAction(MpayQrAction.ShareQrCode(bytes))
        }
    },
    // ... similar for download
)
```

### Task 8: Add Localization for All Languages
**Files**: `values-{lang}/strings.xml` for ar, bn, es, fr, hi, id, pt, sw
**Priority**: P1 (High)
**Effort**: S

Add translations for:
- `feature_mpay_qr_inter_bank_unavailable`
- `feature_mpay_qr_external_id_required`

### Task 9: Update Tests
**File**: `feature/mpay-qr/src/commonTest/.../MpayQrViewModelTest.kt`
**Priority**: P1 (High)
**Effort**: M

Add test cases:
- `generateQr_withNoExternalId_generatesIntraBankOnly`
- `generateQr_withExternalId_generatesBothQrCodes`
- `setAmount_withNoExternalId_updatesOnlyIntraBank`

---

## Verification Checklist

After implementation:
- [x] No external ID → Intra-bank QR generates successfully
- [x] No external ID → Inter-bank tab shows placeholder with humanized message
- [x] With external ID → Both QR codes generate
- [x] Share/Download hidden on inter-bank page when no external ID
- [x] Amount changes work correctly
- [ ] All language strings added (mpay-qr doesn't have localized folders yet - P1)
- [ ] Tests pass (P1 - can be added in follow-up)

---

## Files to Create/Modify

| Action | File |
|--------|------|
| UPDATE | `feature/mpay-qr/.../MpayQrViewModel.kt` |
| UPDATE | `feature/mpay-qr/.../MpayQrScreen.kt` |
| CREATE | `feature/mpay-qr/.../components/InterBankPlaceholder.kt` |
| UPDATE | `feature/mpay-qr/.../composeResources/values/strings.xml` |
| UPDATE | `feature/mpay-qr/.../composeResources/values-{lang}/strings.xml` (8 files) |
| UPDATE | `feature/mpay-qr/.../MpayQrViewModelTest.kt` |

---

## Estimated Scope

- **New files**: 1 (InterBankPlaceholder.kt)
- **Modified files**: 11
- **Priority**: P0 (Bug Fix - Blocking QR generation)
- **Effort**: M (Medium - ~2-3 hours)

---

## Related

- **QR_PAYMENT_ROUTING_APPROACH.md**: Existing documentation for QR routing
- **MpayQrCodeProcessor.kt**: Validation logic (correct, no changes needed)
- **PR #3110**: Recent LocalizedDateFormatter changes (same feature area)
