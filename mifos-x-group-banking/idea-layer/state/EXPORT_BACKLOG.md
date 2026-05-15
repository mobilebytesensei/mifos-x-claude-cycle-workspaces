# Export Backlog — mifos-x-group-banking

> Screens that need export re-generation or have pending changes since last export.

Last updated: 2026-05-09

## Pending Re-export

| Screen | Export Folder | Reason | Priority |
|--------|--------------|--------|----------|
| personal-dashboard | end-user-dashboard | demo-data.yaml added post-export | P1 |
| personal-loans | end-user-dashboard | demo-data.yaml added post-export | P1 |
| personal-savings | end-user-dashboard | demo-data.yaml added post-export | P1 |
| loan-request | loan-management | demo-data.yaml added post-export | P1 |
| savings-dashboard | savings-collection | demo-data.yaml added post-export | P2 |

## Completed Exports (current)

| Export Folder | Screens | Last Export | Status |
|--------------|---------|-------------|--------|
| authentication | login, client-type-selector | 2026-05-08 | ✅ Current |
| group-management | group-list, group-create, group-dashboard | 2026-05-08 | ✅ Current |
| meeting-lifecycle | meeting-calendar, meeting-conduct, meeting-summary, previous-meeting-review | 2026-05-08 | ✅ Current |
| loan-management | loan-list, loan-apply, loan-detail, loan-repayment-dialog, loan-mark-defaulted-dialog | 2026-05-08 | ✅ Current |
| member-onboarding | member-list, member-add, member-profile, member-savings-detail | 2026-05-08 | ✅ Current |
| share-out | share-out-preview, share-out-execute | 2026-05-08 | ✅ Current |
| offline-sync | sync-status | 2026-05-08 | ✅ Current |
| multi-language | settings | 2026-05-08 | ✅ Current |
| field-officer-view | field-officer-dashboard | 2026-05-08 | ✅ Current |

## How to Re-export

```
/idea export {screen-id}         # Re-export single screen
/idea export --flow {flow-id}    # Re-export all screens in a flow
/idea export --all --force       # Full re-export (slow)
```
