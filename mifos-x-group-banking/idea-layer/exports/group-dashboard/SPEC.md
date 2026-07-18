# Group Dashboard — Feature Spec

## Overview

Primary hub for a specific group. Makes 4 parallel API calls on mount (group details,
viewer role, group corpus/financial summary, group accounts). Surfaces pool_model-aware
corpus display (ACCUMULATING: total corpus + projected shareout; ROTATING_PAYOUT: rotation
queue card). Role-gates quick-action buttons (ORGANIZER/TREASURER vs MEMBER).
Share-Out button only visible when `isCycleEnd && (role == ORGANIZER || role == TREASURER)`.

**Acceptance Criteria:**

- AC1: 4 parallel calls on mount: get_group, get_viewer_role, get_group_corpus,
       get_group_accounts. Screen shows skeleton until all resolve.
- AC2: `corpus_card` adapts by pool_model:
  - `ACCUMULATING` → total_corpus + projected_shareout_amount
  - `ROTATING_PAYOUT` → current_rotation_number + next_recipient_name + next_recipient_eta
- AC3: Quick actions role-gated: `Share Out` only visible when
       `isCycleEnd && role ∈ {ORGANIZER, TREASURER}`.
- AC4: `Members` and `Savings` tiles always visible to all roles.
- AC5: Health indicator chip derived client-side from `overdueRate`
       (GREEN <5%, AMBER <20%, RED ≥20%).

## Screens

| Screen | Composable | Layout | Description |
|---|---|---|---|
| group-dashboard | `GroupDashboardScreen` | Scrollable column with sections | Group hub: corpus card, quick actions, members summary, health indicator |

## State Model

### GroupDashboardViewModel

**State — `GroupDashboardState`**

| Field | Type | Default | Description |
|---|---|---|---|
| groupId | String | `""` | From nav params |
| groupName | String | `""` | Display name |
| groupType | String | `""` | typeSlug |
| poolModel | String | `""` | ACCUMULATING \| ROTATING_PAYOUT \| NONE |
| contributionModel | String | `""` | From typeConfig |
| viewerRole | String | `""` | ORGANIZER \| TREASURER \| SECRETARY \| MEMBER |
| isCycleEnd | Boolean | `false` | Whether shareout period is active |
| memberCount | Int | `0` | Total members |
| overdueRate | Double | `0.0` | % members with overdue contributions |
| healthIndicator | String | `"GREEN"` | GREEN \| AMBER \| RED (client-derived) |
| totalCorpus | Long | `0L` | ACCUMULATING: total pooled funds (KES) |
| projectedShareout | Long | `0L` | ACCUMULATING: expected per-member payout |
| currentRotationNumber | Int | `0` | ROTATING_PAYOUT: current payout turn |
| totalRotations | Int | `0` | ROTATING_PAYOUT: total member count |
| nextRecipientName | String | `""` | ROTATING_PAYOUT: next payout recipient |
| nextRecipientEta | String | `""` | ROTATING_PAYOUT: date string |
| savingsAccountId | String? | `null` | Active savings account ID |
| loanAccountId | String? | `null` | Active loan account ID (may be null) |
| isLoading | Boolean | `true` | Initial parallel load |
| error | String? | `null` | Error banner |

**Screen States**

| State | Components |
|---|---|
| `Loading` | Skeleton for corpus_card, quick_actions, members row |
| `Content` | corpus_card, quick_action_buttons, members_row, health_chip |
| `Error` | error_banner + retry_button |
| `PartialError` | Content with non-fatal warning banner for failed sub-calls |

**Actions — `GroupDashboardAction`**

| Action | Trigger |
|---|---|
| `OnShareOut` | Tap Share Out button |
| `OnViewMembers` | Tap Members tile |
| `OnViewSavings` | Tap Savings tile |
| `OnInviteMember` | Tap Invite tile |
| `OnViewLoans` | Tap Loans tile (if loanAccountId present) |
| `OnRefresh` | Pull-to-refresh |
| `OnBack` | Tap back arrow |
| `OnRetry` | Tap retry on error |

**Events — `GroupDashboardEvent`**

| Event | Payload | Trigger |
|---|---|---|
| `NavigateToShareOutPreview` | groupId: String, cycleNumber: Int | `OnShareOut` |
| `NavigateToMemberList` | groupId: String | `OnViewMembers` |
| `NavigateToSavingsDashboard` | groupId: String | `OnViewSavings` |
| `NavigateToMemberInvite` | groupId: String | `OnInviteMember` |
| `NavigateBack` | — | `OnBack` |

**DI Dependencies**

- `GroupRepository` — get_group, get_group_corpus, get_group_accounts
- `MemberRoleRepository` — get_viewer_role (dt_member_role)
- `SessionManager`

## Navigation

| Action | Destination | Params |
|---|---|---|
| `OnShareOut` | `share-out-preview` | `groupId`, `cycleNumber` |
| `OnViewMembers` | `group-member-list` (v1.1) | `groupId` |
| `OnViewSavings` | `savings-dashboard` | `groupId` |
| `OnInviteMember` | `member-invite` | `groupId` |
| `OnBack` | `group-list` | — |

## API Endpoints

| ID | Method | Endpoint | Companion Tool | Writable |
|---|---|---|---|---|
| `get_group` | GET | `/companion/groups/{groupId}` | COMP-GRP-001 | no |
| `get_viewer_role` | GET | `/companion/datatables/dt_member_role/{groupId}` | COMP-DT-002 (read) | no |
| `get_group_corpus` | GET | `/companion/groups/{groupId}/corpus` | — | no |
| `get_group_accounts` | GET | `/companion/groups/{groupId}/accounts` | — | no |

All 4 calls executed in parallel via `async { }` blocks. Cache strategies per table.

## Data-Flow

**Tables**

| Table | PK | Mutation | Strategy |
|---|---|---|---|
| `group_cache` | groupId | upsert | stale_while_revalidate 300 s |
| `group_type_config_cache` | groupId | upsert | stale_while_revalidate 86400 s |
| `viewer_role_cache` | groupId | upsert | stale_while_revalidate 300 s |
| `group_corpus_cache` | groupId | upsert | stale_while_revalidate 60 s (financial freshness) |
| `group_accounts_cache` | groupId | upsert | stale_while_revalidate 300 s |

**Sync Queue:** none (read-only screen).

## DTOs

See `exports/group-dashboard/API.md` for full DTO schemas.

Key types: `GroupDetail` (groupId, groupName, groupType, poolModel, memberCount, isCycleEnd,
overdueRate), `ViewerRoleRow` (groupId, memberId, role), `GroupCorpus`
(accumulating variant: totalCorpus, projectedShareout; rotating variant: rotationNumber,
totalRotations, nextRecipientName, nextRecipientEta), `GroupAccounts`
(savingsAccountId, loanAccountId?).

## Designed UX Reference

- **Stitch mockups:** `idea-layer/screens/group-dashboard/prompts/`
- **Preview HTML:** `idea-layer/screens/group-dashboard/preview/`
- **Design conformance:** Corpus card background is a group-type accent color. Health chip
  is color-coded (GREEN/AMBER/RED) and shown below member count. Quick-action buttons are
  a 2×2 grid; Share Out is full-width when visible and styled in primary color. Share Out
  button is entirely absent (not disabled) for MEMBER role. The rotation queue card
  (ROTATING_PAYOUT) shows a horizontal progress indicator (#current / #total with payout
  queue chips below).
