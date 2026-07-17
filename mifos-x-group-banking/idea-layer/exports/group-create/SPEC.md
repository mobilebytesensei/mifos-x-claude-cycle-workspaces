# Group Create — Feature Spec

## Overview

4-step wizard for creating a new savings group. Receives a `GroupTypeConfig` from
`group-type-picker` and adapts the wizard's Step 2 fields to the contribution model.
Submits a single companion orchestration call (COMP-GRP-001) that handles center creation,
activation, member association, role assignment, and datatable provisioning server-side.
Supports offline creation via sync queue.

**Acceptance Criteria:**

- AC1: Step 2 fields adapt to `typeConfig.contribution_model`:
  - `SHARE_BASED_VARIABLE` → share_value, shareMin, shareMax
  - `FIXED_AMOUNT` → contributionAmount (per meeting)
  - `ROTATING_PAYOUT` → payoutOrderMethod (FIXED_ORDER / LOTTERY / AUCTION)
- AC2: Office list fetched from `/offices` on mount (cache 3600 s).
- AC3: `OnSubmit` calls COMP-GRP-001 single orchestration endpoint — no sequential calls.
- AC4: On success → navigate to `group-dashboard` with returned `groupId`.
- AC5: Offline → enqueue `CREATE_GROUP_ORCHESTRATE` to sync_queue (NORMAL priority,
       idempotency_key: `name:{name}:officeId:{officeId}:userId:{userId}`).
- AC6: Show `ShowOfflineSyncDialog` if user submits offline explaining deferred creation.

## Screens

| Screen | Composable | Layout | Description |
|---|---|---|---|
| group-create | `GroupCreateScreen` | Step-wizard, vertical scroll per step | 4-step group creation wizard; steps adapt to typeConfig |

## State Model

### GroupCreateViewModel

**State — `GroupCreateState`**

| Field | Type | Default | Description |
|---|---|---|---|
| currentStep | Int | `1` | Active wizard step (1–4) |
| totalSteps | Int | `4` | Total steps |
| typeConfig | GroupTypeConfig? | `null` | From nav params |
| groupTypeName | String | `""` | Display name for type |
| groupName | String | `""` | Step 1 — group display name |
| officeId | String | `""` | Step 1 — selected Fineract office |
| officeName | String | `""` | Display name of selected office |
| currency | String | `"KES"` | Default currency |
| meetingDay | String | `""` | Step 1 — day of week |
| meetingTime | String | `""` | Step 1 — meeting time |
| shareValue | Long | `0L` | SHARE_BASED_VARIABLE — per-share KES value |
| shareMin | Int | `1` | SHARE_BASED_VARIABLE — min shares per meeting |
| shareMax | Int | `5` | SHARE_BASED_VARIABLE — max shares per meeting |
| contributionAmount | Long | `0L` | FIXED_AMOUNT — KES per meeting |
| payoutOrderMethod | String | `"FIXED_ORDER"` | ROTATING_PAYOUT — FIXED_ORDER/LOTTERY/AUCTION |
| loanMultiplier | Double | `3.0` | Step 3 — loan limit = shares × multiplier |
| interestRate | Double | `10.0` | Step 3 — interest rate % |
| cycleLengthMonths | Int | `12` | Step 3 — cycle duration |
| fineAmount | Long | `0L` | Step 3 — per-meeting late-payment fine |
| socialFundEnabled | Boolean | `false` | Step 3 — social fund toggle |
| socialFundPercent | Double | `5.0` | Step 3 — % of shares to social fund |
| maxMembers | Int | `30` | Step 3 — max members |
| inviteCode | String? | `null` | Returned by COMP-GRP-001 on success |
| isSubmitting | Boolean | `false` | In-flight orchestration call |
| isSubmitSuccess | Boolean | `false` | Navigate trigger |
| officeList | List<Office> | `emptyList()` | From `/offices` endpoint |
| validationErrors | Map<String,String> | `emptyMap()` | Per-field errors |
| error | String? | `null` | Top-level banner error |
| isOffline | Boolean | `false` | Drives sync dialog |

**Screen States**

| State | Components |
|---|---|
| `Content` | step_indicator, step_N_fields, next_button, back_button |
| `Submitting` | step_4_fields (read-only), linear_progress |
| `Success` | success_illustration, group_name, invite_code_chip, navigate CTA |
| `Error` | error_banner + content |

**Actions — `GroupCreateAction`** (20+, key subset)

| Action | Trigger |
|---|---|
| `OnNameChange(name)` | Step 1 name input |
| `OnOfficeSelect(officeId, name)` | Step 1 office picker |
| `OnShareValueChange(value)` | Step 2 share value input (SHARE_BASED_VARIABLE) |
| `OnContributionAmountChange(amount)` | Step 2 contribution input (FIXED_AMOUNT) |
| `OnPayoutOrderChange(method)` | Step 2 payout method (ROTATING_PAYOUT) |
| `OnSocialFundToggle` | Step 3 toggle |
| `OnNextStep` | Next button |
| `OnPreviousStep` | Back within wizard |
| `OnSubmit` | Final step Submit button |
| `OnBack` | Tap back from Step 1 |

**Events — `GroupCreateEvent`**

| Event | Payload | Trigger |
|---|---|---|
| `NavigateToGroupDashboard` | groupId: String | On success |
| `NavigateBack` | — | `OnBack` from Step 1 |
| `ShowOfflineSyncDialog` | — | Submit while offline |
| `ShowSnackbar` | message: String | Errors |

**DI Dependencies**

- `GroupRepository` — COMP-GRP-001 orchestration
- `OfficeRepository` — GET /offices
- `SyncQueueRepository` — offline queue
- `NetworkMonitor`
- `SessionManager`

## Navigation

| Condition | Destination | Params |
|---|---|---|
| Create success (online) | `group-dashboard` | `groupId` |
| Create queued (offline) | `group-list` | with offline sync banner |
| `OnBack` from Step 1 | `group-type-picker` | — |

## API Endpoints

| ID | Method | Endpoint | Companion Tool | Writable |
|---|---|---|---|---|
| `get_offices` | GET | `/offices` | — | no (cache 3600 s) |
| `create_group_orchestrate` | POST | `/companion/groups` | COMP-GRP-001 | yes |

COMP-GRP-001 orchestrates server-side: createCenter → activate → associateClients → assignRole(ORGANIZER) → provision dt_group_type_config.

## Data-Flow

**Tables**

| Table | PK | Mutation | Strategy |
|---|---|---|---|
| `offices_cache` | id | upsert | stale_while_revalidate 3600 s |
| `groups_cache` | groupId | write | serve_stale after creation |
| `group_type_config_cache` | groupId | write | serve_stale — from nav_arg post-create |
| `sync_queue` | id | write | drain_on_connect (NORMAL priority) |

**Sync Queue Entry:**

```
entity_type: CREATE_GROUP_ORCHESTRATE
priority: NORMAL
idempotency_key: "name:{name}:officeId:{officeId}:userId:{userId}"
```

## DTOs

See `exports/group-create/API.md` for full DTO schemas.

Key types: `GroupTypeConfig` (pool_model, contribution_model, shareout_formula,
payout_order_method, share_value, contribution_amount, social_fund_enabled,
social_fund_percent, cycle_length_months, loan_multiplier, interest_rate, fine_amount,
max_members), `CreateGroupOrchestrationRequest`, `CreateGroupOrchestrationResponse`
(groupId, fineractCenterId, inviteCode), `Office`.

## Designed UX Reference

- **Stitch mockups:** `idea-layer/screens/group-create/prompts/`
- **Preview HTML:** `idea-layer/screens/group-create/preview/`
- **Design conformance:** 4-step horizontal step indicator at top. Step 2 fields are
  dynamically shown/hidden based on `contribution_model` — NOT separate step pages.
  Social fund toggle (Step 3) reveals `socialFundPercent` input only when enabled.
  Success state shows a trophy/check illustration, the group name in headlineLarge,
  and the invite code in a copy-able chip. Submit button is error-styled to signal
  irreversibility.
