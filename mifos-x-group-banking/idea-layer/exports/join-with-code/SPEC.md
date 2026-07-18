# Join With Code — Feature Spec

## Overview

Member-onboarding screen that accepts a group invite code (manually entered or auto-filled
from a deep-link) and walks the user through validation → group preview → join confirmation.
Handles the unauthenticated deep-link case by redirecting to `login-signup` with the
pending invite code preserved as a nav param for auto-resume after login.

**Acceptance Criteria:**

- AC1: If a `inviteCode` nav param is present (from deep link), auto-trigger `OnValidateCode`
       on mount — skip the manual-entry `initial` state.
- AC2: Validation calls COMP-DT-002 (datatable read) + COMP-GRP-001 (group preview read);
       on success, show `preview` state with `GroupPreview` card.
- AC3: `OnConfirmJoin` calls COMP-GRP-003 (associateClients); on success, marks invitation
       accepted via COMP-DT-004. COMP-DT-004 failure is **non-fatal** — navigate to
       group-dashboard regardless.
- AC4: If user is not authenticated when deep-link arrives, redirect to `login-signup` with
       `pendingInviteCode` param. Post-login, `login-signup` must restore this screen with
       the code pre-filled.
- AC5: No offline fallback — joining requires connectivity.

## Screens

| Screen | Composable | Layout | Description |
|---|---|---|---|
| join-with-code | `JoinWithCodeScreen` | Single column, center card | Invite code entry → group preview → join confirmation |

## State Model

### JoinWithCodeViewModel

**State — `JoinWithCodeState`**

| Field | Type | Default | Description |
|---|---|---|---|
| inviteCode | String | `""` | User-entered or deep-link-supplied code |
| inviteStatus | InviteStatus | `INITIAL` | See InviteStatus enum below |
| groupPreview | GroupPreview? | `null` | Group metadata after code validation |
| isJoining | Boolean | `false` | In-flight COMP-GRP-003 call |
| error | String? | `null` | Error message for banner |

**InviteStatus enum:** `INITIAL`, `VALIDATING`, `PREVIEW`, `JOINING`, `SUCCESS`,
`ERROR_INVALID_CODE`, `ERROR_EXPIRED`, `ERROR_ALREADY_MEMBER`, `ERROR_NETWORK`

**Screen States**

| State | Components |
|---|---|
| `initial` | code_input_field, validate_button |
| `validating` | code_input_field (read-only), circular_progress |
| `preview` | group_preview_card (name, type, member count), confirm_join_button, back_button |
| `joining` | group_preview_card, linear_progress |
| `success` | success_icon, group name, navigates in 1s |
| `error_invalid_code` | error_banner ("Invalid code"), code_input_field, retry |
| `error_expired` | error_banner ("Code expired"), code_input_field, retry |
| `error_already_member` | error_banner ("Already a member"), navigate_to_group_cta |
| `error_network` | error_banner, retry |

**Actions — `JoinWithCodeAction`**

| Action | Trigger |
|---|---|
| `OnCodeChange(code)` | Text input change |
| `OnValidateCode` | Tap Validate, or auto on mount if deep-link code present |
| `OnConfirmJoin` | Tap Confirm Join in preview state |
| `OnBack` | Tap back arrow |
| `OnRetry` | Tap retry in error state |

**Events — `JoinWithCodeEvent`**

| Event | Payload | Trigger |
|---|---|---|
| `NavigateToGroupDashboard` | groupId: String | Join success |
| `NavigateToLoginSignup` | pendingInviteCode: String | Unauthenticated deep-link redirect |
| `NavigateBack` | — | `OnBack` |
| `ShowSnackbar` | message: String | Non-fatal errors / success messages |

**DI Dependencies**

- `InvitationRepository` — COMP-DT-002/003/005 (datatable read/validate/accept)
- `GroupRepository` — COMP-GRP-001 (group preview read)
- `AuthRepository` — checks session before joining
- `NetworkMonitor` — connectivity gate

## Navigation

| Condition | Destination | Params |
|---|---|---|
| Deep-link, unauthenticated | `login-signup` | `pendingInviteCode` |
| Join success | `group-dashboard` | `groupId` |
| `OnBack` | Back stack | — |

## API Endpoints

| ID | Method | Endpoint | Companion Tool | Writable |
|---|---|---|---|---|
| `validate_invite_token` | GET | `/companion/datatables/invitations/{entityId}` | COMP-DT-002 read | no |
| `get_group_preview` | GET | `/companion/groups/{groupId}` | COMP-GRP-001 | no |
| `associate_client_to_group` | POST | `/companion/groups/{groupId}/associate-clients` | COMP-GRP-003 | yes |
| `mark_invitation_accepted` | PUT | `/companion/datatables/invitations/{entityId}/{rowId}` | COMP-DT-004 | yes |

**Note:** `mark_invitation_accepted` failure is non-fatal — navigation to group-dashboard
proceeds even if this call fails.

## Data-Flow

**Tables**

| Table | PK | Mutation | Strategy |
|---|---|---|---|
| `pending_invite_cache` | token | upsert | session_only (cleared on success/error) |
| `group_memberships_cache` | groupId | upsert | sqldelight_entity — serve_stale 300 s |

**Sync Queue:** none (join requires connectivity).

## DTOs

See `exports/join-with-code/API.md` for full DTO schemas.

Key types: `InvitationRow` (token, groupId, invitedEmailPhone, expiresAt, acceptedAt?),
`GroupPreview` (groupId, groupName, groupType, memberCount),
`AssociateClientsRequest` (clientIds: List<String>),
`AssociateClientsResponse` (groupId, associatedClientId, role),
`MarkAcceptedRequest` (acceptedAt: String),
`MarkAcceptedResponse` (rowId: Long, status: String).

## Designed UX Reference

- **Stitch mockups:** `idea-layer/screens/join-with-code/prompts/`
- **Preview HTML:** `idea-layer/screens/join-with-code/preview/`
- **Design conformance:** Large outlined code entry field (OTP-style or single text field);
  preview card shows group name in titleLarge, group type chip, member count badge. Confirm
  Join button is `filled` style. Error states render inline below the input field, not as
  dialogs. Deep-link auto-validation suppresses the manual input field and jumps directly
  to the validating spinner.
