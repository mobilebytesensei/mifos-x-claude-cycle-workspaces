# User Flows Index

> **Purpose**: Registry of all user flows for the mifos-x-field-officer-app.
> **Status**: Initial discovery - flows need to be created

---

## Quick Reference

| # | Flow | Screens | Status | Path |
|:-:|------|:-------:|:------:|------|
| 1 | auth-flow | TBD | ❌ | flows/auth-flow.mmd |
| 2 | client-management-flow | TBD | ❌ | flows/client-management-flow.mmd |
| 3 | loan-flow | TBD | ❌ | flows/loan-flow.mmd |
| 4 | savings-flow | TBD | ❌ | flows/savings-flow.mmd |
| 5 | group-center-flow | TBD | ❌ | flows/group-center-flow.mmd |
| 6 | collection-flow | TBD | ❌ | flows/collection-flow.mmd |
| 7 | offline-sync-flow | TBD | ❌ | flows/offline-sync-flow.mmd |
| 8 | data-table-form-flow | Component | ✅ | flows/data-table-form-flow.mmd |

**Status Legend:**
- ✅ Complete (documented with all screens)
- 🔄 In progress
- ❌ Not started

---

## Suggested Flows

Based on discovered features, these flows should be created:

### Core Flows
| Flow | Features Involved | Priority |
|------|-------------------|:--------:|
| auth-flow | auth, settings | High |
| client-management-flow | client, activate, document, note | High |
| loan-flow | loan, data-table, document | High |
| savings-flow | savings, recurringDeposit | High |

### Group Operations
| Flow | Features Involved | Priority |
|------|-------------------|:--------:|
| group-center-flow | groups, center | Medium |
| collection-flow | collectionSheet, groups, center | Medium |

### Utility Flows
| Flow | Features Involved | Priority |
|------|-------------------|:--------:|
| offline-sync-flow | offline, path-tracking | Medium |
| search-report-flow | search, search-record, report | Low |
| checker-approval-flow | checker-inbox-task | Low |

---

## Commands

```bash
/flow                      # Visualize all flows
/flow-create               # Create new flow interactively
/flow-validate             # Validate all flows
/flow-to-tickets           # Create tickets from flows
```

---

## Related Files

| File | Purpose |
|------|---------|
| `flows/*.mmd` | Individual flow definitions (Mermaid) |
| `../FEATURES_INDEX.md` | Feature registry |
| `../FLOW_COVERAGE.md` | Flow coverage tracking |
