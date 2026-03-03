# Plan: Beneficiary UX Improvements

> **Plan ID**: beneficiary-ux-260301-001
> **Created**: 2026-03-01
> **Status**: ✅ Implemented

---

## Problem Statement

Current beneficiary flow has several UX issues:
1. **Duplicate navigation**: QR scan shows "Add Beneficiary" even when beneficiary already exists
2. **No post-add navigation**: After adding beneficiary, user is left on previous screen instead of transfer
3. **Raw error display**: Server errors show full JSON instead of readable `MifosError.message`
4. **Low visibility**: "Scan QR Code" option is not prominent enough to indicate form skip

---

## Tasks

### Task 1: Skip Add Beneficiary if Exists → Navigate to Intra-Bank Transfer
**Priority**: P0 | **Effort**: M

**Current Behavior**:
- `FastMpayProcessor.processIntraBankQr()` checks if beneficiary exists
- If exists → `NavigateToMakeTransfer` (this is correct)
- BUT: `NavigateToMakeTransfer` may not be wired correctly in navigation

**Analysis Required**:
1. Check `FastMpayScreen.kt` handling of `NavigateToMakeTransfer`
2. Verify navigation to intra-bank transfer with pre-filled beneficiary

**Files to Modify**:
- `feature/fast-mpay/src/commonMain/kotlin/.../FastMpayScreen.kt`
- `cmp-shared/src/commonMain/kotlin/.../MifosNavHost.kt`

**Implementation**:
```kotlin
// FastMpayScreen.kt - Verify this navigation handler exists
is QrProcessResult.NavigateToMakeTransfer -> {
    // Navigate to intra-bank transfer with beneficiary pre-selected
    navigateToIntraBankTransfer(
        beneficiaryId = findBeneficiaryId(result.qrData.accountNo),
        amount = result.qrData.amount
    )
}
```

---

### Task 2: After Successful Add Beneficiary → Auto-Navigate to Transfer
**Priority**: P0 | **Effort**: M

**Current Behavior**:
- `AddEditBeneficiaryViewModel.handleBeneficiaryAddEditResult()` on success:
  ```kotlin
  sendEvent(AEBEvent.ShowToast(action.result.data))
  sendEvent(AEBEvent.NavigateBack)  // ← Goes back, not to transfer
  ```

**Solution**:
1. Add new event `AEBEvent.NavigateToTransfer(transferType, beneficiaryData)`
2. Modify success handler to check if came from QR scan
3. If from QR → Navigate to appropriate transfer screen

**Files to Modify**:
- `feature/beneficiary/src/commonMain/kotlin/.../AddEditBeneficiaryViewModel.kt`
- `feature/beneficiary/src/commonMain/kotlin/.../AddEditBeneficiaryScreen.kt`
- `feature/beneficiary/src/commonMain/kotlin/.../BeneficiaryNavigation.kt`
- `cmp-shared/src/commonMain/kotlin/.../MifosNavHost.kt`

**Implementation**:
```kotlin
// AddEditBeneficiaryViewModel.kt - Track source
@Serializable
internal data class AEBState(
    // ... existing fields
    val sourceQrType: QrCodeType? = null,  // NEW: Track if from QR scan
)

// On success
is DataState.Success -> {
    if (state.sourceQrType != null) {
        // Navigate to transfer based on QR type
        when (state.sourceQrType) {
            QrCodeType.INTRA_BANK -> sendEvent(AEBEvent.NavigateToIntraBankTransfer(beneficiaryData))
            QrCodeType.INTER_BANK -> sendEvent(AEBEvent.NavigateToInterbankTransfer(beneficiaryData))
            else -> sendEvent(AEBEvent.NavigateBack)
        }
    } else {
        sendEvent(AEBEvent.NavigateBack)
    }
}
```

---

### Task 3: Show MifosError Message Instead of Full JSON
**Priority**: P1 | **Effort**: S

**Current Behavior**:
- `handleBeneficiaryAddEditResult()` shows raw exception message:
  ```kotlin
  val message = action.result.exception.message.toString()
  it.copy(dialogState = Error.StringMessage(message))
  ```

**Solution**:
Parse MifosError structure from exception message.

**Files to Modify**:
- `feature/beneficiary/src/commonMain/kotlin/.../AddEditBeneficiaryViewModel.kt`

**Implementation**:
```kotlin
// AddEditBeneficiaryViewModel.kt
is DataState.Error -> {
    val errorMessage = extractMifosErrorMessage(action.result.exception)
    mutableStateFlow.update {
        it.copy(dialogState = Error.StringMessage(errorMessage))
    }
}

private fun extractMifosErrorMessage(exception: Throwable): String {
    val rawMessage = exception.message ?: return "Unknown error"

    // Try to parse MifosError JSON structure
    return try {
        // Pattern: {"defaultUserMessage":"...", "userMessageGlobalisationCode":"..."}
        val regex = """"defaultUserMessage"\s*:\s*"([^"]+)"""".toRegex()
        regex.find(rawMessage)?.groupValues?.get(1) ?: rawMessage
    } catch (e: Exception) {
        rawMessage
    }
}
```

---

### Task 4: Highlight "Scan QR Code" Button for Better Visibility
**Priority**: P1 | **Effort**: S

**Current Behavior**:
```kotlin
Row(horizontalArrangement = Arrangement.spacedBy(KptTheme.spacing.sm)) {
    Text(text = stringResource(Res.string.skip_the_form))
    Text(
        text = stringResource(Res.string.scan_qr_code),
        modifier = Modifier.clickable { onAction(AEBAction.OnQrScanClicked) },
    )
}
```
- Plain text, no visual distinction
- Users may not notice it's clickable

**Solution**:
Convert to prominent button with icon.

**Files to Modify**:
- `feature/beneficiary/src/commonMain/kotlin/.../AddEditBeneficiaryScreen.kt`

**Implementation**:
```kotlin
// Replace current Row with:
OutlinedCard(
    onClick = { onAction(AEBAction.OnQrScanClicked) },
    modifier = Modifier.fillMaxWidth(),
    colors = CardDefaults.outlinedCardColors(
        containerColor = KptTheme.colors.surfaceVariant,
    ),
    border = BorderStroke(1.dp, KptTheme.colors.primary),
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(KptTheme.spacing.md),
        horizontalArrangement = Arrangement.Center,
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Icon(
            imageVector = MifosIcons.QrCodeScanner,
            contentDescription = null,
            tint = KptTheme.colors.primary,
        )
        Spacer(modifier = Modifier.width(KptTheme.spacing.sm))
        Column {
            Text(
                text = stringResource(Res.string.scan_qr_code),
                style = KptTheme.typography.titleMedium,
                color = KptTheme.colors.primary,
            )
            Text(
                text = stringResource(Res.string.skip_the_form),
                style = KptTheme.typography.bodySmall,
                color = KptTheme.colors.onSurfaceVariant,
            )
        }
    }
}
```

---

## Execution Order

| Order | Task | Priority | Effort | Dependencies |
|:-----:|------|:--------:|:------:|--------------|
| 1 | Task 1: Verify existing transfer navigation | P0 | M | None |
| 2 | Task 3: Show MifosError message | P1 | S | None |
| 3 | Task 4: Highlight Scan QR button | P1 | S | None |
| 4 | Task 2: Auto-navigate to transfer after add | P0 | M | Task 1 |

---

## Verification Checklist

After implementation:
- [ ] QR scan with existing beneficiary → Goes directly to intra-bank transfer
- [ ] QR scan with new beneficiary → Add form → Success → Goes to transfer
- [ ] Server error shows readable message (not JSON)
- [ ] "Scan QR Code" is visually prominent and recognizable as clickable

---

## Files Summary

| Action | File |
|--------|------|
| VERIFY | `feature/fast-mpay/.../FastMpayScreen.kt` |
| MODIFY | `feature/fast-mpay/.../FastMpayViewModel.kt` |
| MODIFY | `feature/beneficiary/.../AddEditBeneficiaryViewModel.kt` |
| MODIFY | `feature/beneficiary/.../AddEditBeneficiaryScreen.kt` |
| MODIFY | `feature/beneficiary/.../BeneficiaryNavigation.kt` |
| MODIFY | `cmp-shared/.../MifosNavHost.kt` |

---

## Notes

- Task 2 requires passing `sourceQrType` through navigation args from QR scan → Add Beneficiary
- Consider adding `BeneficiaryAddEditType.AddItem(beneficiary, qrType)` variant
- Test inter-bank and intra-bank flows separately
