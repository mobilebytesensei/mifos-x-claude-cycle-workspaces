# template_meta
# template_version: "2.86.5"
# template_path: "workspaces/mifos-x/mifos-x-field-officer-app/plan-layer/plans/PLAN-implement-data-table-260316-001.md"
# last_modified: "2026-03-20"

# Implementation Plan: Data Table Building Block

**Plan ID**: `PLAN-implement-data-table-260316-001`
**Feature**: data-table (Dynamic Data Table Form Building Block)
**Created**: 2026-03-16
**Status**: Phase 1-4 Complete (14/14 files)
**Type**: E2E Feature Implementation
**Priority**: High
**Estimated Files**: 14 new files
**Based On**: GAP_PLAN_DATA_TABLE_FORM.md (2026-03-05)

---

## Summary

Implement a **100% data-driven, reusable Compose building block** (`DynamicDataTableForm`) that dynamically generates form UI from Fineract DataTable JSON schema. 14 new files across 4 phases.

---

## Prerequisites

| Prerequisite | Status |
|-------------|:------:|
| Design Spec (SPEC.md) | ✅ Complete |
| Mockups | ✅ Complete (5 screens) |
| API Design (API.md) | ✅ Complete |
| Gap Plan | ✅ Complete |
| Flow Diagram | ✅ Complete |
| Existing Source Code | ✅ 4 screens, models, repos exist |

---

## Task Breakdown

### Phase 1: Extension Functions (Foundation)
**Effort**: S | **Files**: 1

| # | Task | File | Status | Priority |
|:-:|------|------|:------:|:--------:|
| 1 | ColumnHeader extensions (displayName, isRequired, isSystemColumn) | `feature/data-table/.../util/ColumnHeaderExt.kt` | ✅ | P0 |

### Phase 2: Field Components (Parallelizable)
**Effort**: M | **Files**: 8

| # | Task | File | Status | Priority |
|:-:|------|------|:------:|:--------:|
| 2 | BooleanField (Switch for BOOLEAN) | `.../components/fields/BooleanField.kt` | ✅ | P0 |
| 3 | IntegerField (Number input for INTEGER) | `.../components/fields/IntegerField.kt` | ✅ | P0 |
| 4 | DecimalField (Decimal input for DECIMAL) | `.../components/fields/DecimalField.kt` | ✅ | P0 |
| 5 | StringField (Text input for STRING) | `.../components/fields/StringField.kt` | ✅ | P0 |
| 6 | MultilineTextField (Multiline for TEXT) | `.../components/fields/MultilineTextField.kt` | ✅ | P0 |
| 7 | DateField (Date picker for DATE) | `.../components/fields/DateField.kt` | ✅ | P0 |
| 8 | DateTimeField (DateTime picker for DATETIME) | `.../components/fields/DateTimeField.kt` | ✅ | P0 |
| 9 | DropdownField (Dropdown for CODELOOKUP) | `.../components/fields/DropdownField.kt` | ✅ | P0 |

### Phase 3: Core Components (Depends on Phase 1+2)
**Effort**: M | **Files**: 3

| # | Task | File | Status | Priority |
|:-:|------|------|:------:|:--------:|
| 10 | DynamicField router (routes by columnDisplayType) | `.../components/DynamicField.kt` | ✅ | P0 |
| 11 | DataTableHeader (optional header card) | `.../components/DataTableHeader.kt` | ✅ | P1 |
| 12 | DynamicDataTableForm (main building block) | `.../components/DynamicDataTableForm.kt` | ✅ | P0 |

### Phase 4: Multi-Table State Management (Depends on Phase 3)
**Effort**: S | **Files**: 2

| # | Task | File | Status | Priority |
|:-:|------|------|:------:|:--------:|
| 13 | MultiDataTableState data class | `.../state/MultiDataTableState.kt` | ✅ | P0 |
| 14 | DynamicDataTableList wrapper (renders N tables) | `.../components/DynamicDataTableList.kt` | ✅ | P0 |

---

## Dependency Graph

```
Phase 1: ColumnHeaderExt ─────────────────────────────────┐
                                                           │
Phase 2: BooleanField ─┐                                  │
         IntegerField ─┤                                   │
         DecimalField ─┤                                   │
         StringField  ─┤─── All parallel ──────────────────┤
         MultilineField┤                                   │
         DateField    ─┤                                   ▼
         DateTimeField─┤                          Phase 3: DynamicField
         DropdownField─┘                                   │
                                                  DataTableHeader
                                                           │
                                                  DynamicDataTableForm
                                                           │
                                                           ▼
                                                  Phase 4: MultiDataTableState
                                                           │
                                                  DynamicDataTableList
```

---

## File Paths (All in source repo)

**Base**: `feature/data-table/src/commonMain/kotlin/com/mifos/feature/dataTable/`

| File | Full Path |
|------|-----------|
| ColumnHeaderExt.kt | `util/ColumnHeaderExt.kt` |
| BooleanField.kt | `components/fields/BooleanField.kt` |
| IntegerField.kt | `components/fields/IntegerField.kt` |
| DecimalField.kt | `components/fields/DecimalField.kt` |
| StringField.kt | `components/fields/StringField.kt` |
| MultilineTextField.kt | `components/fields/MultilineTextField.kt` |
| DateField.kt | `components/fields/DateField.kt` |
| DateTimeField.kt | `components/fields/DateTimeField.kt` |
| DropdownField.kt | `components/fields/DropdownField.kt` |
| DynamicField.kt | `components/DynamicField.kt` |
| DataTableHeader.kt | `components/DataTableHeader.kt` |
| DynamicDataTableForm.kt | `components/DynamicDataTableForm.kt` |
| MultiDataTableState.kt | `state/MultiDataTableState.kt` |
| DynamicDataTableList.kt | `components/DynamicDataTableList.kt` |

---

## Implementation Commands

```bash
# Full implementation (all phases)
/implement data-table

# Phase-by-phase
/implement data-table --phase 1    # Extensions only
/implement data-table --phase 2    # Field components
/implement data-table --phase 3    # Core components
/implement data-table --phase 4    # Multi-table state

# Verify
/verify data-table
/test data-table
```

---

## Design References

| Document | Path |
|----------|------|
| Feature Spec | `design-spec-layer/features/data-table/SPEC.md` |
| API Design | `design-spec-layer/features/data-table/API.md` |
| Gap Plan | `plan-layer/GAP_PLAN_DATA_TABLE_FORM.md` |
| Status | `design-spec-layer/features/data-table/STATUS.md` |
| Mockups | `design-spec-layer/features/data-table/mockups/` |
| Flow | `design-spec-layer/user-flows/flows/data-table-form-flow.mmd` |

---

## Existing Code to Consult

| Component | Path | Purpose |
|-----------|------|---------|
| DataTableEntity | `core/database/.../entities/noncore/DataTable.kt` | Data model |
| ColumnHeader | `core/database/.../entities/noncore/ColumnHeader.kt` | Field metadata |
| ColumnValue | `core/database/.../entities/noncore/ColumnValue.kt` | Dropdown options |
| DataTableListScreen | `feature/data-table/.../dataTableList/` | Existing form (reference) |
| MifosDatePickerTextField | `core/designsystem/` | Date picker to reuse |
| MifosOutlinedTextField | `core/designsystem/` | Text field to reuse |
| MifosTextFieldDropdown | `core/designsystem/` | Dropdown to reuse |
