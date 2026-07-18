# Member Invite — Feature Spec

## Overview

Organizer/treasurer tool for generating invite codes and links to bring new members into
a group. Creates invitation rows in the `dt_companion_invitations` datatable via the
companion API, displays a list of pending (not yet accepted) invitations, and supports
revocation. The generated invite link is a deep-link that routes to `join-with-code`.

**Acceptance Criteria:**

- AC1: On mount, fetch pending invites via COMP-DT-003 (paginated, offset 20, cache 60 s).
- AC2: `OnGenerateInvite` calls COMP-DT-002 (create invitation); returns `token` +
       `inviteLink`. Link is a deep-link pointing to `join-with-code?code={token}`.
- AC3: `OnCopyCode` / `OnCopyLink` write to `ClipboardManager`. `OnShareLink` triggers
       system share sheet with `ShowShareSheet(link, code)`.
- AC4: `OnRevokeInvite(inviteId)` calls COMP-DT-005 (DELETE); applies optimistic delete
       from `pendingInvites` list before response.
- AC5: Invite generation requires connectivity; pending list serves stale cache offline.

## Screens

| Screen | Composable | Layout | Description |
|---|---|---|---|
| member-invite | `MemberInviteScreen` | Single column scroll | Email/phone + role input → generate; pending invites list below |

## State Model

### MemberInviteViewModel

**State — `MemberInviteState`**

| Field | Type | Default | Description |
|---|---|---|---|
| groupId | String | `""` | From nav params |
| emailPhone | String | `""` | Intended recipient (optional — leave blank for generic code) |
| selectedRole | String | `"MEMBER"` | Role to assign on join |
| pendingInvites | List<PendingInvite> | `emptyList()` | Loaded from COMP-DT-003 |
| isGenerating | Boolean | `false` | In-flight COMP-DT-002 call |
| generatedCode | String? | `null` | Returned token after generation |
| generatedLink | String? | `null` | Deep-link URL |
| isLoadingPending | Boolean | `true` | Initial pending list fetch |
| error | String? | `null` | Error banner message |

**Screen States**

| State | Components |
|---|---|
| `loading` | shimmer for pending list |
| `content` | emailPhone input, role selector, generate button, pending_invites list |
| `generating` | content + circular progress on button |
| `generated` | generated_code_card (code + link + copy/share actions), pending_invites list |
| `error` | error_banner + content |

**Actions — `MemberInviteAction`**

| Action | Trigger |
|---|---|
| `OnEmailPhoneChange(value)` | Text input |
| `OnRoleSelect(role)` | Role chip selection |
| `OnGenerateInvite` | Tap Generate Invite |
| `OnCopyCode` | Tap Copy Code |
| `OnCopyLink` | Tap Copy Link |
| `OnShareLink` | Tap Share Link |
| `OnRevokeInvite(inviteId)` | Tap revoke on pending row |
| `OnBack` | Tap back arrow |
| `OnRetry` | Tap retry in error state |

**Events — `MemberInviteEvent`**

| Event | Payload | Trigger |
|---|---|---|
| `NavigateBack` | — | `OnBack` |
| `ShowSnackbar` | message: String | Copy/revoke confirmations |
| `ShowShareSheet` | link: String, code: String | `OnShareLink` |

**DI Dependencies**

- `InvitationRepository` — COMP-DT-002 (create), COMP-DT-003 (list), COMP-DT-005 (revoke)
- `ClipboardManager` — platform expect/actual

## Navigation

| Action | Destination | Params |
|---|---|---|
| `OnBack` | Back stack | — |
| (invite link) | `join-with-code` | `inviteCode={token}` (deep-link, not in-app nav) |

Entry from: `group-dashboard` via Members action → member-invite.

## API Endpoints

| ID | Method | Endpoint | Companion Tool | Writable |
|---|---|---|---|---|
| `create_invite` | POST | `/companion/datatables/invitations/{groupId}` | COMP-DT-002 | yes |
| `list_pending_invites` | GET | `/companion/datatables/invitations/{groupId}` | COMP-DT-003 | no |
| `revoke_invite` | DELETE | `/companion/datatables/invitations/{groupId}/{rowId}` | COMP-DT-005 | yes |

## Data-Flow

**Tables**

| Table | PK | Mutation | Strategy |
|---|---|---|---|
| `pending_invites_cache` | rowId | upsert | stale_while_revalidate 60 s; optimistic delete on revoke |

**Sync Queue:** none (invite generation requires connectivity; revoke is best-effort live).

## DTOs

See `exports/member-invite/API.md` for full DTO schemas.

Key types: `CreateInviteRequest` (emailPhone?: String, roleToAssign: String),
`GeneratedInvite` (token, inviteLink, rowId),
`PendingInvite` (rowId, token, invitedEmailPhone, roleToAssign, expiresAt, acceptedAt?).

## Designed UX Reference

- **Stitch mockups:** `idea-layer/screens/member-invite/prompts/`
- **Preview HTML:** `idea-layer/screens/member-invite/preview/`
- **Design conformance:** Email/phone input is optional — placeholder says "Leave blank for
  generic code". Role selector is a horizontal chip row (Member / Treasurer / Secretary).
  Generated code shown in a tinted card with large monospace text + Copy Code and Share
  buttons. Pending list below uses trailing icon-button for revoke with a confirmation
  snackbar (no dialog — optimistic delete).
