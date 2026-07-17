# Share-Out Execute — Feature Spec

## Overview

Execution screen for the cycle's share-out. Requires a double-confirmation guard before
dispatching (either type "SHARE OUT" in a text field OR use biometric auth). Calls
COMP-DIST-001 for ACCUMULATING groups and COMP-DIST-002 for ROTATING_PAYOUT groups.
Back navigation is disabled during and after execution. Partial failures (some member
payouts fail) show per-member status badges with retry capability.
Offline execution is queued at HIGH priority.

**Acceptance Criteria:**

- AC1: Double-confirmation required: either type the phrase "SHARE OUT" in a text
       input OR authenticate with biometrics.
- AC2: `OnExecute` uses:
  - `poolModel == ACCUMULATING` → COMP-DIST-001 (`/companion/groups/{groupId}/shareout/execute`)
  - `poolModel == ROTATING_PAYOUT` → COMP-DIST-002 (`/companion/groups/{groupId}/rotation/execute`)
- AC3: Back navigation disabled once `isExecuting == true` OR `isCompleted == true`.
- AC4: Per-member status badges: `PENDING` → `PROCESSING` → `PAID` \| `FAILED`.
       Failed members show individual retry buttons.
- AC5: On partial failure (≥1 member failed), screen stays on Execute with failed
       rows highlighted. User can retry individual rows.
- AC6: Offline → enqueue `EXECUTE_SHAREOUT` to sync_queue at HIGH priority.
       `isCompleted == true` and show "Will complete when online" banner.
- AC7: idempotency_key prevents double-execution on sync retry:
       `groupId:{groupId}:cycle:{cycleNumber}`.

## Screens

| Screen | Composable | Layout | Description |
|---|---|---|---|
| share-out-execute | `ShareOutExecuteScreen` | Scrollable with sticky footer | Double-confirm guard; per-member progress list; completion CTA |

## State Model

### ShareOutExecuteViewModel

**State — `ShareOutExecuteState`**

| Field | Type | Default | Description |
|---|---|---|---|
| groupId | String | `""` | From nav params |
| cycleNumber | Int | `0` | From nav params |
| poolModel | String | `""` | ACCUMULATING \| ROTATING_PAYOUT |
| totalAmount | Long | `0L` | From nav params |
| confirmationText | String | `""` | Typed phrase for double-confirm |
| isBiometricConfirmed | Boolean | `false` | Biometric path |
| isConfirmed | Boolean | `false` | true when either path passes |
| isExecuting | Boolean | `false` | Execution in progress |
| isCompleted | Boolean | `false` | All done (success or partial with retries exhausted) |
| isOfflineQueued | Boolean | `false` | Queued to sync |
| memberStatuses | List<MemberExecutionStatus> | `emptyList()` | Per-member execution state |
| error | String? | `null` | Top-level error banner |

**Screen States**

| State | Components |
|---|---|
| `AwaitingConfirmation` | confirmation_text_input OR biometric_button, execute_button (disabled until confirmed) |
| `Executing` | linear_progress, per-member status list (live-updating), back disabled |
| `PartialFailure` | per-member list with FAILED rows in error color + individual retry buttons |
| `Complete` | success_animation, total_distributed amount, "Back to Dashboard" CTA |
| `OfflineQueued` | "Will complete when online" banner, back to group-list |
| `Error` | error_banner + retry_button |

**Actions — `ShareOutExecuteAction`**

| Action | Trigger |
|---|---|
| `OnConfirmationTextChange(text)` | Type in text input |
| `OnBiometricConfirm` | Biometric success callback |
| `OnExecute` | Tap "Execute Share-Out" (enabled only when isConfirmed) |
| `OnRetryMember(memberId)` | Individual member retry |
| `OnBackToDashboard` | Completion CTA |

**Events — `ShareOutExecuteEvent`**

| Event | Payload | Trigger |
|---|---|---|
| `NavigateToGroupDashboard` | groupId: String | Completion CTA |
| `DisableBack` | — | On `isExecuting` or `isCompleted` set |
| `ShowBiometricPrompt` | — | Tap biometric button |
| `ShowOfflineBanner` | — | On offline queue |

**DI Dependencies**

- `ShareOutRepository` — COMP-DIST-001 (accumulating), COMP-DIST-002 (rotation)
- `SyncQueueRepository` — offline enqueue
- `BiometricManager` — expect/actual
- `NetworkMonitor`
- `SessionManager`

## Navigation

| Condition | Destination | Params |
|---|---|---|
| Completion (online success) | `group-dashboard` | groupId |
| Offline queued | `group-list` | — |
| Back (during/after execution) | DISABLED | — |

Entry from: `share-out-preview` → Confirm.

## API Endpoints

| ID | Method | Endpoint | Companion Tool | Writable |
|---|---|---|---|---|
| `execute_accumulating_shareout` | POST | `/companion/groups/{groupId}/shareout/execute` | COMP-DIST-001 | yes |
| `execute_rotation_payout` | POST | `/companion/groups/{groupId}/rotation/execute` | COMP-DIST-002 | yes |

## Data-Flow

**Tables**

| Table | PK | Mutation | Strategy |
|---|---|---|---|
| `sync_queue` | id | write | drain_on_connect (HIGH priority) |
| `shareout_execution_log` | groupId:cycleNumber | write | audit log; non-queryable |

**Sync Queue Entry:**

```
entity_type: EXECUTE_SHAREOUT
priority: HIGH
idempotency_key: "groupId:{groupId}:cycle:{cycleNumber}"
```

**No local read cache** — this is a pure write screen. Preview data comes via nav args.

## DTOs

See `exports/share-out-execute/API.md` for full DTO schemas.

Key types:
- `ExecuteShareOutRequest` (cycleNumber, idempotencyKey, memberDistributions[])
- `ExecuteShareOutResponse` (executionId, status, memberResults[])
- `MemberExecutionStatus` (memberId, memberName, amount, status: PENDING/PROCESSING/PAID/FAILED, failureReason?)
- `ExecuteRotationPayoutRequest` (cycleNumber, idempotencyKey)
- `ExecuteRotationPayoutResponse` (executionId, recipientMemberId, amount, status)

## Designed UX Reference

- **Stitch mockups:** `idea-layer/screens/share-out-execute/prompts/`
- **Preview HTML:** `idea-layer/screens/share-out-execute/preview/`
- **Design conformance:** Confirmation section has a red-tinted warning card: "This
  action cannot be undone. Type SHARE OUT below or use biometrics." The text input
  shows the placeholder "SHARE OUT" and the Execute button stays disabled until the
  phrase matches exactly (case-insensitive) OR biometric resolves. Per-member status
  badges use colored chips: PENDING=neutral, PROCESSING=blue pulse, PAID=green,
  FAILED=red. Back button in top app bar is hidden (not just disabled) once execution
  starts. Success state: confetti animation + total KES in displayLarge.
