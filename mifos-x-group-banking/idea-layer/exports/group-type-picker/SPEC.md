# Group Type Picker — Feature Spec

## Overview

Selection screen that bridges the "Create a Group" intent with the correctly configured
wizard in `group-create`. Fetches the full `GroupTypeConfig[]` catalog from the companion
datatable API and renders one card per supported group type. Selection passes the chosen
`GroupTypeConfig` as a nav arg to `group-create`, which uses it to adapt the wizard steps.

**Acceptance Criteria:**

- AC1: On mount, fetches `GET /companion/datatables/group_type_config/{entityId}` (entityId=0)
       — returns all available group type configurations.
- AC2: Each card shows: `displayName`, `tagline`, `savingsMechanism` chip, `maxMembers` label.
- AC3: Tapping a card sets `selectedType` and emits `NavigateToGroupCreate(typeConfig)`.
- AC4: Config is cached for 86400 s (stale-while-revalidate); serves offline.
- AC5: Retry on error refetches the same endpoint.

## Screens

| Screen | Composable | Layout | Description |
|---|---|---|---|
| group-type-picker | `GroupTypePickerScreen` | Vertical scroll list | Catalog of group type cards — select one to proceed to group-create |

## State Model

### GroupTypePickerViewModel

**State — `GroupTypePickerState`**

| Field | Type | Default | Description |
|---|---|---|---|
| typeConfigs | List<GroupTypeConfig> | `emptyList()` | All supported group types from datatable |
| selectedType | GroupTypeConfig? | `null` | User's current selection (tap-to-navigate) |
| isLoading | Boolean | `true` | In-flight fetch |
| error | String? | `null` | Error banner message |

**Screen States**

| State | Components |
|---|---|
| `Loading` | shimmer skeleton (3 cards) |
| `Content` | type_card × N, back_button |
| `Error` | error_banner with Retry |

**Actions — `GroupTypePickerAction`**

| Action | Trigger |
|---|---|
| `OnTypeCardTap(typeSlug)` | Tap a group type card |
| `OnBack` | Tap back arrow |
| `OnRetry` | Tap retry in error state |

**Events — `GroupTypePickerEvent`**

| Event | Payload | Trigger |
|---|---|---|
| `NavigateToGroupCreate` | typeConfig: GroupTypeConfig | After `OnTypeCardTap` |
| `NavigateBack` | — | `OnBack` |

**DI Dependencies**

- `GroupTypeConfigRepository` — fetches + caches `/companion/datatables/group_type_config/{entityId}`

## Navigation

| Action | Destination | Params |
|---|---|---|
| `OnTypeCardTap` | `group-create` | `typeConfig: GroupTypeConfig` |
| `OnBack` | Back stack | — |

Entry point: from `group-list` FAB or `login-signup` zero_groups CTA.

## API Endpoints

| ID | Method | Endpoint | Companion Tool | Writable |
|---|---|---|---|---|
| `get_group_type_configs` | GET | `/companion/datatables/group_type_config/{entityId}` | COMP-DT-002 (datatable read) | no |

entityId = 0 (global catalog row). Cache TTL 86400 s.

## Data-Flow

**Tables**

| Table | PK | Mutation | Strategy |
|---|---|---|---|
| `group_type_config_cache` | typeSlug | upsert | sqldelight_entity — stale_while_revalidate 86400 s |

**Sync Queue:** none (read-only screen).

## DTOs

See `exports/group-type-picker/API.md` for full DTO schemas.

Key type: `GroupTypeConfig` — typeSlug, displayName, tagline, savingsMechanism,
contributionMode, lendingEnabled, hasSocialFund, hasBankLinkage, welfareOnlyMode,
formallyRegistered, defaultLoanMultiplier, defaultInterestRatePct,
defaultCycleLengthMonths, maxMembers, minMembers.

## Designed UX Reference

- **Stitch mockups:** `idea-layer/screens/group-type-picker/prompts/`
- **Preview HTML:** `idea-layer/screens/group-type-picker/preview/`
- **Design conformance:** Vertically stacked cards. Each card: displayName (titleLarge),
  tagline (bodyMedium, onSurfaceVariant), `savingsMechanism` chip (primaryContainer),
  `maxMembers` trailing label. No horizontal carousel — full-width tap targets.
