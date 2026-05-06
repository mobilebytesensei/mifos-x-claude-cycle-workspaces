# Flows — CommonPurse

> 9 flows generated · 2026-05-05 · source: idea-plan.yaml §flows + /idea sync

| Flow | Type | Client | Screens |
|------|------|--------|---------|
| admin-auth-flow | happy | admin | client-type-selector → login → group-list |
| end-user-auth-flow | happy | end_user | client-type-selector → login → personal-dashboard |
| group-creation-flow | happy | admin | group-list → group-create → group-dashboard |
| meeting-flow | happy | admin | group-dashboard → previous-meeting-review → meeting-conduct → meeting-summary |
| loan-lifecycle-flow | happy | admin | member-profile → loan-apply → meeting-conduct → loan-detail |
| share-out-flow | happy | admin | group-dashboard → share-out-preview → share-out-execute |
| end-user-loan-request-flow | happy | end_user | personal-dashboard → loan-request → personal-loans |
| corpus-outflow-blocked-flow | error | admin | meeting-conduct (inline) |
| offline-sync-flow | happy | both | sync-status |

Run `/flow {name}` to view a specific flow's Mermaid diagram.
