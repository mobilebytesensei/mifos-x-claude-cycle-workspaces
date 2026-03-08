# Services Index - O(1) Lookup

> **Purpose**: Instant lookup for all network services in the client-layer.
> **Source**: Discovered from `source/mifos-x-field-officer-app/core/network/`

---

## Quick Reference

| # | Service | Type | Keywords | Source Path |
|:-:|---------|:----:|----------|-------------|
| 1 | OfficesApi | API | office, branch | core/network/src/.../OfficesApi.kt |
| 2 | StaffApi | API | staff, employee | core/network/src/.../StaffApi.kt |
| 3 | DataTablesApi | API | datatable, custom-field | core/network/src/.../DataTablesApi.kt |
| 4 | CentersApi | API | center, hub | core/network/src/.../CentersApi.kt |
| 5 | GroupsApi | API | group, team | core/network/src/.../GroupsApi.kt |
| 6 | ClientApi | API | client, customer | core/network/src/.../ClientApi.kt |
| 7 | ClientIdentifierApi | API | identifier, id | core/network/src/.../ClientIdentifierApi.kt |
| 8 | DataTableService | Service | datatable | core/network/src/.../DataTableService.kt |
| 9 | DocumentService | Service | document, file | core/network/src/.../DocumentService.kt |
| 10 | FixedDepositService | Service | fixed-deposit, fd | core/network/src/.../FixedDepositService.kt |
| 11 | ClientAccountsService | Service | client-account | core/network/src/.../ClientAccountsService.kt |
| 12 | GroupService | Service | group | core/network/src/.../GroupService.kt |
| 13 | RunReportsService | Service | report, analytics | core/network/src/.../RunReportsService.kt |
| 14 | NoteService | Service | note, comment | core/network/src/.../NoteService.kt |
| 15 | SavingsAccountService | Service | savings | core/network/src/.../SavingsAccountService.kt |
| 16 | SearchService | Service | search, find | core/network/src/.../SearchService.kt |
| 17 | LoanService | Service | loan, lending | core/network/src/.../LoanService.kt |
| 18 | ShareAccountService | Service | share | core/network/src/.../ShareAccountService.kt |
| 19 | CheckerInboxService | Service | checker, inbox | core/network/src/.../CheckerInboxService.kt |
| 20 | CenterService | Service | center | core/network/src/.../CenterService.kt |
| 21 | StaffService | Service | staff | core/network/src/.../StaffService.kt |
| 22 | OfficeService | Service | office | core/network/src/.../OfficeService.kt |
| 23 | SurveyService | Service | survey | core/network/src/.../SurveyService.kt |
| 24 | CollectionSheetService | Service | collection | core/network/src/.../CollectionSheetService.kt |
| 25 | ClientService | Service | client | core/network/src/.../ClientService.kt |
| 26 | RecurringAccountService | Service | recurring, rd | core/network/src/.../RecurringAccountService.kt |
| 27 | ChargeService | Service | charge, fee | core/network/src/.../ChargeService.kt |

---

## Category Index

### Client Services
| Service | Keywords | Path |
|---------|----------|------|
| ClientApi | client, customer | ClientApi.kt |
| ClientService | client | ClientService.kt |
| ClientAccountsService | client-account | ClientAccountsService.kt |
| ClientIdentifierApi | identifier | ClientIdentifierApi.kt |

### Financial Product Services
| Service | Keywords | Path |
|---------|----------|------|
| LoanService | loan, lending | LoanService.kt |
| SavingsAccountService | savings | SavingsAccountService.kt |
| FixedDepositService | fixed-deposit | FixedDepositService.kt |
| RecurringAccountService | recurring | RecurringAccountService.kt |
| ShareAccountService | share | ShareAccountService.kt |
| ChargeService | charge, fee | ChargeService.kt |

### Group & Center Services
| Service | Keywords | Path |
|---------|----------|------|
| GroupsApi | group | GroupsApi.kt |
| GroupService | group | GroupService.kt |
| CentersApi | center | CentersApi.kt |
| CenterService | center | CenterService.kt |
| CollectionSheetService | collection | CollectionSheetService.kt |

### Organization Services
| Service | Keywords | Path |
|---------|----------|------|
| OfficesApi | office, branch | OfficesApi.kt |
| OfficeService | office | OfficeService.kt |
| StaffApi | staff | StaffApi.kt |
| StaffService | staff | StaffService.kt |

### Data & Reporting Services
| Service | Keywords | Path |
|---------|----------|------|
| DataTablesApi | datatable | DataTablesApi.kt |
| DataTableService | datatable | DataTableService.kt |
| RunReportsService | report | RunReportsService.kt |
| SearchService | search | SearchService.kt |

### Utility Services
| Service | Keywords | Path |
|---------|----------|------|
| DocumentService | document | DocumentService.kt |
| NoteService | note | NoteService.kt |
| SurveyService | survey | SurveyService.kt |
| CheckerInboxService | checker | CheckerInboxService.kt |

---

## Service → Feature Mapping

| Service | Primary Feature |
|---------|-----------------|
| ClientApi, ClientService | client |
| LoanService | loan |
| SavingsAccountService | savings |
| GroupsApi, GroupService | groups |
| CentersApi, CenterService | center |
| CollectionSheetService | collectionSheet |
| DataTableService, DataTablesApi | data-table |
| DocumentService | document |
| NoteService | note |
| SearchService | search |
| RunReportsService | report |
| CheckerInboxService | checker-inbox-task |
| RecurringAccountService | recurringDeposit |

---

## Commands

```bash
/enforce-index services    # Validate this index
/client [service]          # Document service (auto-indexes)
/gap-analysis client       # Check client layer gaps
```
