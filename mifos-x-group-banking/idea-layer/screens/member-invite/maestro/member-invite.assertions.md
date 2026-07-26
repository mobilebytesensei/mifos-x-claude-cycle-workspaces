# Behavior-assertion map — member-invite Maestro flow

Flow: `idea-layer/screens/member-invite/maestro/member-invite.yaml`
appId: `org.mifos.groupbanking` · TestTags: `MemberInviteTestTags.kt` (CU-5)

## Reachability
login(ORGANIZER) → organizer-dashboard → group-list → group card → group-dashboard → `group_dashboard_view_members_button` → member-list → `member_list_invite_action` → member-invite (NavHost §11c, member-list `onInviteMember`).

## State → success_signal → tag mapping
| State | success_signal | Selector | Encoded? |
|---|---|---|---|
| Loading | pending-invites fetch (COMP-DT-003) | `id: member_invite_pending_loading_indicator` | waited-through via `extendedWaitUntil` on screen |
| Content | create-invite form + pending list | `id: member_invite_field_email_phone` (+ `generate_button`) | yes — asserted |
| Generating | spinner while COMP-DT-002 in flight | `id: member_invite_generating_indicator` | transient — waited-through into Generated |
| Generated | code card + copy/share actions | `id: member_invite_generated_card` (+ `copy_code_button`, `share_button`) | yes — asserted |
| Error | inline error banner + retry | `id: member_invite_error_banner` / `error_retry_button` | NOT asserted — induced network/server failure only |

## on_click exercised
- `member_invite_field_email_phone` inputText `+254712345678` + `member_invite_generate_button` (OnGenerateInvite) → Generated state asserted.

## Backend seed prerequisites
- ORGANIZER account + group + ≥1 member (so member-list renders and Invite is reachable).
- Connectivity + companion backend for COMP-DT-002 (invite generation has no offline queue).

## Notes / gaps
- Pending-invites Empty state (`member_invite_pending_empty_state`) and Error are induced-only; not faked.
- Revoke on_click (`member_invite_revoke_button`) needs a pre-existing pending invite row (seed-specific) — not exercised.
- No tag ids invented.
