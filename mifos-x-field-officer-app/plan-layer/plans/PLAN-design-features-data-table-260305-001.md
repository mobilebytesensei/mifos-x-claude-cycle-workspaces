# Feature Generation Plan: data-table

**Plan ID:** design-features-data-table-260305-001
**Created:** 2026-03-05
**Status:** Ready for Implementation
**Flow:** data-table-form-flow.mmd

---

## Overview

Generate feature components from the `data-table-form-flow.mmd` building block design.

**Note:** This flow describes a **reusable building block component** (not a traditional multi-screen user flow). The components are designed to be embedded in parent screens.

---

## Design Layer Status

| Artifact | Status | Path |
|----------|:------:|------|
| SPEC.md | Completed | `features/data-table/SPEC.md` |
| STATUS.md | Completed | `features/data-table/STATUS.md` |
| Flow Diagram | Completed | `user-flows/flows/data-table-form-flow.mmd` |
| GAP_PLAN | Completed | `plan-layer/GAP_PLAN_DATA_TABLE_FORM.md` |
| API.md | N/A | Building block - no dedicated API |
| MOCKUP.md | N/A | Uses existing web screenshots as reference |

---

## Components to Generate

### Core Components (Phase 3)

| # | Component | Type | Description | Priority |
|:-:|-----------|------|-------------|:--------:|
| 1 | DynamicDataTableForm | Composable | Main building block - schema-driven form | P0 |
| 2 | DynamicField | Composable | Field type router (8 types) | P0 |
| 3 | DataTableHeader | Composable | Optional header card with table name | P1 |

### Field Components (Phase 2)

| # | Component | Type | Field Type | Priority |
|:-:|-----------|------|------------|:--------:|
| 4 | BooleanField | Composable | BOOLEAN | P0 |
| 5 | IntegerField | Composable | INTEGER | P0 |
| 6 | DecimalField | Composable | DECIMAL | P0 |
| 7 | StringField | Composable | STRING | P0 |
| 8 | MultilineTextField | Composable | TEXT | P0 |
| 9 | DateField | Composable | DATE | P0 |
| 10 | DateTimeField | Composable | DATETIME | P0 |
| 11 | DropdownField | Composable | CODELOOKUP | P0 |

### Extensions (Phase 1)

| # | Component | Type | Description | Priority |
|:-:|-----------|------|-------------|:--------:|
| 12 | ColumnHeaderExt | Extension | displayName, isRequired, isSystemColumn | P0 |

---

## Implementation Order

Based on dependencies, implement in this order:

```
Phase 1: Extensions (Foundation)
├── ColumnHeaderExt.kt          # Required by all field components
│
Phase 2: Field Components (Parallel)
├── BooleanField.kt             │
├── IntegerField.kt             │
├── DecimalField.kt             │ Can be implemented
├── StringField.kt              │ in parallel
├── MultilineTextField.kt       │
├── DateField.kt                │
├── DateTimeField.kt            │
└── DropdownField.kt            │
│
Phase 3: Core Components (Sequential)
├── DynamicField.kt             # Routes to field components
├── DataTableHeader.kt          # Optional header
└── DynamicDataTableForm.kt     # Main building block (depends on all above)
```

---

## File Paths

```
feature/data-table/src/commonMain/kotlin/com/mifos/feature/dataTable/
├── components/
│   ├── DynamicDataTableForm.kt    ← Main building block
│   ├── DynamicField.kt            ← Field router
│   ├── DataTableHeader.kt         ← Optional header
│   └── fields/
│       ├── BooleanField.kt
│       ├── IntegerField.kt
│       ├── DecimalField.kt
│       ├── StringField.kt
│       ├── MultilineTextField.kt
│       ├── DateField.kt
│       ├── DateTimeField.kt
│       └── DropdownField.kt
└── util/
    └── ColumnHeaderExt.kt         ← Extensions
```

---

## Estimated Effort

| Phase | Components | Effort |
|-------|:----------:|:------:|
| Phase 1: Extensions | 1 | S |
| Phase 2: Field Components | 8 | M (parallelizable) |
| Phase 3: Core Components | 3 | M |
| **Total** | **12** | **M-L** |

---

## Success Criteria

- [ ] All 8 field types render correctly based on `columnDisplayType`
- [ ] Two-column grid layout with configurable column count
- [ ] System columns auto-filtered (id, *_id, timestamps)
- [ ] Validation callback works for required fields
- [ ] CODELOOKUP dropdowns populated from `columnValues`
- [ ] Stateless design - accepts values and callbacks
- [ ] Drop-in ready - works in any parent composable
- [ ] No regressions in existing DataTable screens

---

## Execution Commands

```bash
# Implement all components
/implement data-table

# Or implement phase by phase
/implement data-table --phase 1    # Extensions only
/implement data-table --phase 2    # Field components
/implement data-table --phase 3    # Core components

# Verify implementation
/verify data-table

# Run tests
/test data-table
```

---

## Related Documents

| Document | Path |
|----------|------|
| Feature Spec | `design-spec-layer/features/data-table/SPEC.md` |
| Status | `design-spec-layer/features/data-table/STATUS.md` |
| Gap Plan | `plan-layer/GAP_PLAN_DATA_TABLE_FORM.md` |
| Flow Diagram | `design-spec-layer/user-flows/flows/data-table-form-flow.mmd` |
