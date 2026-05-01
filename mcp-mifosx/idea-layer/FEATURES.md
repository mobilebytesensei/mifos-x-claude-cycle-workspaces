# Mifos MCP — Features

## Feature Summary

| # | Feature | Priority | Go | Python | Rust | Java | Status |
|---|---------|:--------:|:--:|:------:|:----:|:----:|--------|
| 1 | client-management | must | 11 | 16 | 23 | 25 | implemented |
| 2 | group-management | must | 12 | 6 | 8 | 15 | implemented |
| 3 | loan-management | must | 15 | 14 | 18 | 28 | implemented |
| 4 | savings-management | must | 11 | 9 | 11 | 18 | implemented |
| 5 | staff-organization | should | 4 | 4 | 4 | 8 | implemented |
| 6 | accounting | should | 3 | 3 | 3 | 6 | implemented |
| 7 | document-management | should | 14 | 0 | 0 | 8 | partial |
| 8 | reporting | could | 8 | 5 | 0 | 8 | partial |
| 9 | bulk-operations | could | 16 | 0 | 0 | 0 | partial |
| 10 | composite-operations | could | 3 | 0 | 0 | 0 | partial |
| 11 | diagnostics | could | 2 | 0 | 0 | 0 | partial |
| 12 | product-management | should | 0 | 4 | 0 | 0 | partial |
| 13 | charge-management | should | 0 | 4 | 4 | 8 | partial |
| 14 | code-tables | could | 0 | 3 | 0 | 0 | partial |
| 15 | collateral-management | could | 0 | 0 | 4 | 8 | partial |

## Parity Analysis

**Full parity (all 4 languages):** client-management, group-management, loan-management, savings-management, staff-organization, accounting

**Partial parity:** document-management (Go+Java), reporting (Go+Python+Java), charge-management (Python+Rust+Java), collateral-management (Rust+Java)

**Go-only:** bulk-operations, composite-operations, diagnostics

**Python-only:** product-management, code-tables

## Requirements (FR-001 to FR-025)

See `idea-plan.yaml` §requirements for full list.
