# Share-Out — Feature Specification
**Project**: MifosSave (mifos-x-group-banking)
**Feature ID**: share-out
**Requirements**: FR-007
**Version**: 1.0.0
**Status**: enriched

---

## Overview

Share-out is the end-of-cycle distribution of accumulated savings and profit to all group members. The total distribution pool equals `totalCorpus + totalProfit (interest earned)`. Each member's payout is calculated pro-rata by their total savings contribution: `memberShare% = memberTotalSavings / totalGroupSavings`, then `memberPayout = sharePercent × totalPool`. Computation is performed client-side after fetching corpus and account data. The chairperson executes the share-out with a double-confirmation gate (type "SHARE OUT" or biometric), triggering sequential withdrawal transactions per member. Offline support queues all operations to SyncQueue.

---

## Acceptance Criteria

- **FR-007**: The share-out pool = corpus balance + total interest earned across all loan accounts. Each member receives a pro-rata share based on their total savings contributions over the cycle. The chairperson must confirm execution with "SHARE OUT" text entry or biometric authentication. Execution posts a withdrawal transaction to each member's savings account. Partial failures are shown with per-member retry. Offline operations are queued to SyncQueue with HIGH priority.

---

## Screens Table

| Screen ID | Route | Type | Role Required |
|-----------|-------|------|---------------|
| share-out-preview | /groups/{groupId}/share-out/preview | detail | Chairperson |
| share-out-execute | /groups/{groupId}/share-out/execute | form | Chairperson |

---

## State Model

### ShareOutPreviewViewModel
| Field | Type | Default |
|-------|------|---------|
| isLoading | Boolean | true |
| totalCorpus | Double | 0.0 |
| totalProfit | Double | 0.0 |
| totalPool | Double | 0.0 |
| memberPayouts | List<MemberPayout> | emptyList() |
| error | ShareOutPreviewError? | null |
| cycleNumber | Int | 0 |

**Actions**: OnConfirm, OnBack, Retry, OnRefresh
**Events**: NavigateToShareOutExecute(groupId, centerId, totalPool, memberPayouts), NavigateBack, ShowSnackbar
**DI**: ShareOutRepository, SavingsRepository, NetworkMonitor, SessionManager

### ShareOutExecuteViewModel
| Field | Type | Default |
|-------|------|---------|
| confirmationText | String | "" |
| isConfirmed | Boolean | false |
| isExecuting | Boolean | false |
| executedCount | Int | 0 |
| totalCount | Int | 0 |
| memberExecutionStatus | Map<Long, MemberExecutionStatus> | emptyMap() |
| totalPool | Double | 0.0 |
| isOnline | Boolean | true |
| isCompleted | Boolean | false |
| queuedOffline | Boolean | false |
| failedPayouts | List<MemberPayout> | emptyList() |
| succeededCount | Int | 0 |

**Actions**: OnConfirmationTextChanged, OnBiometricSelected, OnExecute, OnRetryFailed, OnBack, OnDone
**Events**: NavigateToGroupDashboard(groupId), NavigateBack, ShowBiometricPrompt, ShowSnackbar
**DI**: ShareOutRepository, SyncQueueRepository, BiometricManager, NetworkMonitor, SessionManager

---

## Navigation Table

| From | Action | To | Params |
|------|--------|----|--------|
| group-dashboard | Tap Share-Out (isCycleEnd=true) | share-out-preview | groupId, centerId |
| share-out-preview | Tap Confirm & Proceed | share-out-execute | groupId, centerId, cycleNumber, totalPool, memberPayouts |
| share-out-execute | Tap Done (success or queued) | group-dashboard | groupId |
| share-out-execute | Tap back (before execution) | share-out-preview | groupId, centerId |

---

## API Endpoints Table

| Method | Path | Description |
|--------|------|-------------|
| GET | /centers/{centerId}/accounts | Get all savings+loan accounts for corpus+profit computation |
| GET | /datatables/dt_share_out/{centerId} | Check if share-out record already exists for cycle |
| POST | /datatables/dt_share_out/{centerId} | Create share-out record in datatable |
| POST | /savingsaccounts/{savingsAccountId}/transactions | Post withdrawal per member (payout) |

---

## Design Tokens Used

| Token | Value | Usage |
|-------|-------|-------|
| primary | #2E7D32 | Completion banner, done button, pro-rata label |
| primaryContainer | #A6F1A6 | Summary card background, completion banner bg |
| error | #D32F2F | Execute button (irreversible action signal) |
| errorContainer | #FFDAD6 | Error snackbar, failed payout indicator |
| warningContainer | #FFF9C4 | Offline warning banner, partial failure banner |
| secondaryContainer | #FFDDB3 | Member avatar backgrounds, queued payout indicator |
| tertiaryContainer | #D2E4FF | Distribution formula chip |
| surface | #FAFAFA | Summary card, payout list background |
| shape.medium | 12dp | All cards corner radius |
| min_touch_target | 48dp | Confirmation field, biometric button; 56dp execute button |
