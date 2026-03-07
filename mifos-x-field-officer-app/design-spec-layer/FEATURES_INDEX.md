# Features Index - O(1) Lookup

> **Purpose**: Instant lookup for all features in the design-spec-layer.
> **Flow Coverage**: User flows are the single source of truth for design completeness.

---

## Quick Reference

| # | Feature | Status | Screens | VMs | Keywords | Path |
|:-:|---------|:------:|:-------:|:---:|----------|------|
| 1 | about | ⚠️ | 1 | 0 | about, info, app-info | features/about/ |
| 2 | activate | ⚠️ | 1 | 1 | activate, activation | features/activate/ |
| 3 | auth | ⚠️ | 1 | 1 | login, logout, authentication | features/auth/ |
| 4 | center | ⚠️ | 5 | 5 | center, centers, hub | features/center/ |
| 5 | checker-inbox-task | ⚠️ | 2 | 2 | checker, inbox, task, approval | features/checker-inbox-task/ |
| 6 | client | ⚠️ | 38 | 31 | client, customer, member | features/client/ |
| 7 | collectionSheet | ⚠️ | 5 | 5 | collection, sheet, payments | features/collectionSheet/ |
| 8 | data-table | ✅ | 4 | 4 | data, table, custom-fields, dynamic-form | features/data-table/ |
| 9 | document | ⚠️ | 2 | 2 | document, file, attachment | features/document/ |
| 10 | groups | ⚠️ | 4 | 4 | group, groups, team | features/groups/ |
| 11 | loan | ⚠️ | 11 | 12 | loan, lending, credit | features/loan/ |
| 12 | note | ⚠️ | 2 | 2 | note, notes, comment | features/note/ |
| 13 | offline | ⚠️ | 5 | 6 | offline, sync, cache | features/offline/ |
| 14 | path-tracking | ⚠️ | 1 | 1 | path, tracking, location, gps | features/path-tracking/ |
| 15 | recurringDeposit | ⚠️ | 1 | 1 | recurring, deposit, rd | features/recurringDeposit/ |
| 16 | report | ⚠️ | 3 | 2 | report, reports, analytics | features/report/ |
| 17 | savings | ⚠️ | 7 | 7 | savings, account, deposit | features/savings/ |
| 18 | search | ⚠️ | 1 | 1 | search, find, query | features/search/ |
| 19 | search-record | ⚠️ | 1 | 1 | search-record, history | features/search-record/ |
| 20 | settings | ⚠️ | 2 | 3 | settings, preferences, config | features/settings/ |

**Status Legend:**
- ✅ Complete (SPEC + MOCKUP + API + STATUS)
- ⚠️ Partial (discovered, needs spec generation)
- ❌ Not started
- 🔄 In progress

---

## Category Index

### Authentication & Security
| Feature | Path |
|---------|------|
| auth | features/auth/ |
| checker-inbox-task | features/checker-inbox-task/ |

### Client Management
| Feature | Path |
|---------|------|
| client | features/client/ |
| activate | features/activate/ |
| document | features/document/ |
| note | features/note/ |

### Financial Products
| Feature | Path |
|---------|------|
| loan | features/loan/ |
| savings | features/savings/ |
| recurringDeposit | features/recurringDeposit/ |

### Group & Center Management
| Feature | Path |
|---------|------|
| center | features/center/ |
| groups | features/groups/ |
| collectionSheet | features/collectionSheet/ |

### Data & Reports
| Feature | Path |
|---------|------|
| data-table | features/data-table/ |
| report | features/report/ |
| search | features/search/ |
| search-record | features/search-record/ |

### Utilities
| Feature | Path |
|---------|------|
| about | features/about/ |
| settings | features/settings/ |
| offline | features/offline/ |
| path-tracking | features/path-tracking/ |

---

## Keyword → Feature Mapping

```yaml
# Authentication
login: auth
logout: auth
authentication: auth
checker: checker-inbox-task
inbox: checker-inbox-task
approval: checker-inbox-task

# Client
client: client
customer: client
member: client
activate: activate
activation: activate

# Financial
loan: loan
lending: loan
credit: loan
savings: savings
deposit: savings
recurring: recurringDeposit

# Group/Center
center: center
group: groups
collection: collectionSheet
sheet: collectionSheet

# Data
data-table: data-table
custom-fields: data-table
report: report
analytics: report
search: search

# Utilities
settings: settings
preferences: settings
offline: offline
sync: offline
tracking: path-tracking
gps: path-tracking
document: document
note: note
about: about
```

---

## Commands

```bash
# Flow-Driven Design
/flow                      # Visualize user flows
/flow-validate             # Validate ALL design artifacts
/flow-validate --feature   # Validate specific feature
/design verify             # Alias for /flow-validate --coverage

# Feature Management
/enforce-index features    # Validate this index
/design [feature]          # Create/update feature spec (auto-indexes)
/gap-analysis design       # Check design layer gaps
```

---

## Related Files

| File | Purpose |
|------|---------|
| `FLOW_COVERAGE.md` | Per-project flow coverage tracking |
| `user-flows/flows/*.mmd` | User flow definitions (Mermaid) |
| `user-flows/USER_FLOWS_INDEX.md` | Flow registry |
