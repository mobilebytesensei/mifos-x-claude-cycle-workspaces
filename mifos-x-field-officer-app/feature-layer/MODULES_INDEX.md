# Modules Index - O(1) Lookup

> **Purpose**: Instant lookup for all feature modules in the feature-layer.
> **Source**: Discovered from `source/mifos-x-field-officer-app/feature/`

---

## Quick Reference

| # | Module | Screens | VMs | Keywords | Source Path |
|:-:|--------|:-------:|:---:|----------|-------------|
| 1 | about | 1 | 0 | about, info | feature/about/ |
| 2 | activate | 1 | 1 | activate, activation | feature/activate/ |
| 3 | auth | 1 | 1 | login, authentication | feature/auth/ |
| 4 | center | 5 | 5 | center, hub | feature/center/ |
| 5 | checker-inbox-task | 2 | 2 | checker, approval | feature/checker-inbox-task/ |
| 6 | client | 38 | 31 | client, customer | feature/client/ |
| 7 | collectionSheet | 5 | 5 | collection, payments | feature/collectionSheet/ |
| 8 | data-table | 4 | 4 | datatable, custom-fields | feature/data-table/ |
| 9 | document | 2 | 2 | document, file | feature/document/ |
| 10 | groups | 4 | 4 | group, team | feature/groups/ |
| 11 | loan | 11 | 12 | loan, lending | feature/loan/ |
| 12 | note | 2 | 2 | note, comment | feature/note/ |
| 13 | offline | 5 | 6 | offline, sync | feature/offline/ |
| 14 | path-tracking | 1 | 1 | tracking, gps | feature/path-tracking/ |
| 15 | recurringDeposit | 1 | 1 | recurring, rd | feature/recurringDeposit/ |
| 16 | report | 3 | 2 | report, analytics | feature/report/ |
| 17 | savings | 7 | 7 | savings, deposit | feature/savings/ |
| 18 | search | 1 | 1 | search, find | feature/search/ |
| 19 | search-record | 1 | 1 | search-record | feature/search-record/ |
| 20 | settings | 2 | 3 | settings, preferences | feature/settings/ |

**Total**: 20 modules, 97 screens, 91 ViewModels

---

## Category Index

### Authentication & Security
| Module | Screens | VMs | Path |
|--------|:-------:|:---:|------|
| auth | 1 | 1 | feature/auth/ |
| checker-inbox-task | 2 | 2 | feature/checker-inbox-task/ |

### Client Management
| Module | Screens | VMs | Path |
|--------|:-------:|:---:|------|
| client | 38 | 31 | feature/client/ |
| activate | 1 | 1 | feature/activate/ |
| document | 2 | 2 | feature/document/ |
| note | 2 | 2 | feature/note/ |

### Financial Products
| Module | Screens | VMs | Path |
|--------|:-------:|:---:|------|
| loan | 11 | 12 | feature/loan/ |
| savings | 7 | 7 | feature/savings/ |
| recurringDeposit | 1 | 1 | feature/recurringDeposit/ |

### Group & Center Management
| Module | Screens | VMs | Path |
|--------|:-------:|:---:|------|
| center | 5 | 5 | feature/center/ |
| groups | 4 | 4 | feature/groups/ |
| collectionSheet | 5 | 5 | feature/collectionSheet/ |

### Data & Reports
| Module | Screens | VMs | Path |
|--------|:-------:|:---:|------|
| data-table | 4 | 4 | feature/data-table/ |
| report | 3 | 2 | feature/report/ |
| search | 1 | 1 | feature/search/ |
| search-record | 1 | 1 | feature/search-record/ |

### Utilities
| Module | Screens | VMs | Path |
|--------|:-------:|:---:|------|
| about | 1 | 0 | feature/about/ |
| settings | 2 | 3 | feature/settings/ |
| offline | 5 | 6 | feature/offline/ |
| path-tracking | 1 | 1 | feature/path-tracking/ |

---

## Keyword → Module Mapping

```yaml
# Authentication
login: auth
authentication: auth
checker: checker-inbox-task
approval: checker-inbox-task

# Client
client: client
customer: client
member: client
activate: activate
activation: activate

# Financial Products
loan: loan
lending: loan
credit: loan
savings: savings
deposit: savings
recurring: recurringDeposit

# Groups/Centers
center: center
group: groups
collection: collectionSheet

# Data
datatable: data-table
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

## Module → Service Mapping

| Module | Primary Services |
|--------|------------------|
| auth | (AuthService - inferred) |
| client | ClientApi, ClientService, ClientAccountsService |
| loan | LoanService |
| savings | SavingsAccountService |
| groups | GroupsApi, GroupService |
| center | CentersApi, CenterService |
| collectionSheet | CollectionSheetService |
| data-table | DataTableService, DataTablesApi |
| document | DocumentService |
| note | NoteService |
| search | SearchService |
| report | RunReportsService |
| checker-inbox-task | CheckerInboxService |
| recurringDeposit | RecurringAccountService |
| offline | (Local DB sync) |
| path-tracking | (Location services) |
| settings | (Local preferences) |
| about | (Static content) |

---

## Commands

```bash
/enforce-index modules     # Validate this index
/feature [module]          # Document feature (auto-indexes)
/gap-analysis feature      # Check feature layer gaps
```
