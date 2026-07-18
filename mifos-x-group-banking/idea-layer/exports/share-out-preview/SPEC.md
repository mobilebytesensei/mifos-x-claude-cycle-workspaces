# Share-Out Preview — Feature Spec

## Overview

Read-only pre-execution screen that shows the full distribution breakdown for the current
cycle's share-out. Fetches preview data from COMP-DIST-001 (accumulating) and presents
a per-member distribution table or rotation card depending on `pool_model`. The `Confirm`
button passes key parameters as nav args to `share-out-execute` — no state is mutated here.

**Acceptance Criteria:**

- AC1: Fetch `get_shareout_preview` via COMP-DIST-001 on mount. Cache 60 s, network_first.
- AC2: Display adapts by `pool_model`:
  - `ACCUMULATING` → per-member distribution table sorted by shareout amount desc,
    `distribution_formula_chip` shows formula label
  - `ROTATING_PAYOUT` → rotation card: next recipient name, amount, rotation #
- AC3: `distribution_formula_chip` label derived from
       `GroupTypeConfig.shareout_formula`:
       PRORATA_SHARES → "By Shares", PRORATA_SAVINGS → "By Savings",
       EQUAL → "Equal Split", LOTTERY → "Lottery", AUCTION → "Auction".
- AC4: `OnConfirm` navigates to `share-out-execute` passing
       `groupId`, `cycleNumber`, `poolModel`, `totalAmount`.
- AC5: Back navigation returns to `group-dashboard`.

## Screens

| Screen | Composable | Layout | Description |
|---|---|---|---|
| share-out-preview | `ShareOutPreviewScreen` | Scrollable column | Distribution breakdown; Confirm CTA |

## State Model

### ShareOutPreviewViewModel

**State — `ShareOutPreviewState`**

| Field | Type | Default | Description |
|---|---|---|---|
| groupId | String | `""` | From nav params |
| cycleNumber | Int | `0` | From nav params |
| poolModel | String | `""` | ACCUMULATING \| ROTATING_PAYOUT |
| shareoutFormula | String | `""` | PRORATA_SHARES \| PRORATA_SAVINGS \| EQUAL \| FIXED_ORDER \| LOTTERY \| AUCTION |
| formulaLabel | String | `""` | Human-readable formula label |
| totalAmount | Long | `0L` | Total pool to distribute (KES) |
| memberDistributions | List<MemberDistribution> | `emptyList()` | ACCUMULATING: per-member amounts |
| nextRecipient | RotationRecipient? | `null` | ROTATING_PAYOUT: next payout info |
| isLoading | Boolean | `true` | Fetch in progress |
| error | String? | `null` | Error banner |

**Screen States**

| State | Components |
|---|---|
| `Loading` | Skeleton for distribution table |
| `Content` | summary_header, distribution_formula_chip, distribution_table OR rotation_card, confirm_button |
| `Error` | error_banner + retry_button |

**Actions — `ShareOutPreviewAction`**

| Action | Trigger |
|---|---|
| `OnConfirm` | Tap Confirm button |
| `OnBack` | Tap back arrow |
| `OnRetry` | Tap retry on error |

**Events — `ShareOutPreviewEvent`**

| Event | Payload | Trigger |
|---|---|---|
| `NavigateToShareOutExecute` | groupId: String, cycleNumber: Int, poolModel: String, totalAmount: Long | `OnConfirm` |
| `NavigateBack` | — | `OnBack` |

**DI Dependencies**

- `ShareOutRepository` — COMP-DIST-001 preview call
- `SessionManager`

## Navigation

| Action | Destination | Params |
|---|---|---|
| `OnConfirm` | `share-out-execute` | groupId, cycleNumber, poolModel, totalAmount |
| `OnBack` | `group-dashboard` | groupId |

Entry from: `group-dashboard` → Share Out button.

## API Endpoints

| ID | Method | Endpoint | Companion Tool | Writable |
|---|---|---|---|---|
| `get_shareout_preview` | GET | `/companion/groups/{groupId}/shareout/preview?cycle={cycleNumber}` | COMP-DIST-001 | no |

## Data-Flow

**Tables**

| Table | PK | Mutation | Strategy |
|---|---|---|---|
| `shareout_preview_cache` | groupId:cycleNumber | upsert | network_first, TTL 60 s |

**Sync Queue:** none (read-only screen — execution happens in share-out-execute).

## DTOs

See `exports/share-out-preview/API.md` for full DTO schemas.

Key types: `ShareOutPreviewResponse` (cycleNumber, poolModel, shareoutFormula,
totalAmount, memberDistributions[], nextRecipient?),
`MemberDistribution` (memberId, memberName, sharesHeld?, shareAmount, percentOfTotal),
`RotationRecipient` (memberId, memberName, rotationNumber, payoutAmount).

## Designed UX Reference

- **Stitch mockups:** `idea-layer/screens/share-out-preview/prompts/`
- **Preview HTML:** `idea-layer/screens/share-out-preview/preview/`
- **Design conformance:** A `distribution_formula_chip` is a tinted chip with the
  formula label (e.g. "By Shares"). For ACCUMULATING, the distribution table rows show
  member avatar initials, name, shares held (if SHARE_BASED_VARIABLE), and amount in
  bold. Total row at bottom of table. For ROTATING_PAYOUT, a prominent card shows the
  next recipient's name in displayLarge and amount in headlineMedium. Confirm button
  is full-width primary-filled and labeled "Confirm Share-Out".
