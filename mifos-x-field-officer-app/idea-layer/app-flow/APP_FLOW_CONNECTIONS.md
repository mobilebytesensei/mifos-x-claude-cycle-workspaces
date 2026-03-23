# App Flow Connections Matrix

> **Project**: mifos-x-field-officer-app
> **Generated**: 2026-03-22
> **Generator**: app-flow-generate.sh
> **Framework**: 2.86.5
> **Flows**: 6 | **Connections**: 6

---

## Flow Overview

| # | Flow | Entry Screen | Screens | Connects To |
|:-:|------|-------------|:-------:|-------------|
| 1 | admin-utilities |         AboutScreen | 5 | authentication |
| 2 | authentication |         EntityList | 3 | client-management |
| 3 | client-management |         ClientList | 1 | data-table-form-flow |
| 4 | data-table-form-flow |         EntityScreen | 1 | field-operations |
| 5 | field-operations |         CenterList | 4 | financial-operations |
| 6 | financial-operations |         GroupLoan | 5 | admin-utilities |

---

## Connection Details

| From | → | To | Type | Screen |
|------|:-:|-----|------|--------|
| admin-utilities | → | authentication | sequential |  |
| authentication | → | client-management | sequential |  |
| client-management | → | data-table-form-flow | sequential |  |
| data-table-form-flow | → | field-operations | sequential |  |
| field-operations | → | financial-operations | sequential |  |
| financial-operations | → | admin-utilities | sequential |  |

---

*Auto-generated. Regenerate with `/flow-full --refresh` or `app-flow-generate.sh`.*
*Used by `/flow-to-design` for cross-flow navigation in SPEC.md.*
