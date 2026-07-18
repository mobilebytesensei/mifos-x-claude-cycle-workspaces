# Flows — CommonPurse

> 13 flows · regenerated 2026-07-17 · source: idea-plan.yaml §flows (global self-signup pivot) + /idea sync
> Identity is UNIFIED — one login/signup for everyone; capabilities resolve per-group after login (no admin/end_user client_type).

| Flow | Type | Tier | Screens |
|------|------|------|---------|
| unified-auth-flow | happy | v1.0 | login-signup → organizer-dashboard / personal-dashboard / group-list · zero-groups → group-type-picker / join-with-code |
| self-signup-organizer-flow | happy | v1.0 (primary) | login-signup → group-type-picker → group-create → organizer-dashboard → member-invite |
| group-creation-flow | happy | v1.0 | group-list → group-type-picker → group-create → organizer-dashboard |
| member-onboarding-flow | happy | v1.0 | member-list → member-add / (invite) member-invite → join-with-code → login-signup |
| member-invitation-flow | happy | v1.0 | member-invite → join-with-code → login-signup → personal-dashboard |
| meeting-flow | happy | v1.0 | meeting-calendar → group-dashboard → previous-meeting-review → meeting-conduct → meeting-summary |
| loan-lifecycle-flow | happy | v1.0 | loan-list → member-profile → loan-apply → meeting-conduct → loan-detail |
| share-out-flow | happy | v1.0 | organizer-dashboard → share-out-preview → share-out-execute (pro-rata / rotation / auction branch) |
| end-user-loan-request-flow | happy | v1.0 | personal-dashboard → loan-request → personal-loans |
| corpus-outflow-blocked-flow | error | v1.0 | meeting-conduct (inline corpus gate) |
| offline-sync-flow | happy | v1.0 | sync-status |
| multi-language-flow | happy | v1.0 | settings → settings-logout-dialog |
| field-officer-view-flow | happy | v1.1 (optional supervisory tier) | field-officer-dashboard → group-dashboard (read-only) |

**Roles** are resolved per group after unified login: **organizer** (creates + runs the group, loan-officer capabilities), **chairperson** (approve loans + run meetings), **treasurer** (record transactions), **secretary** (notes), **member** (own data + request loans + vote). The **field officer** is an optional, back-office-provisioned, read-only cross-group tier (1.1.0) — not a first-class v1 flow.

**Distribution** (share-out-flow) is pluggable per GroupTypeConfig: PRO_RATA (VSLA/SILC/ASCA), ROTATION (ROSCA family), AUCTION/BID (chit/hui).

Run `/flow {name}` to view a specific flow's Mermaid diagram.
