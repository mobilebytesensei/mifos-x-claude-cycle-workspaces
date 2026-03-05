# Data Table Feature - Implementation Status

**Feature**: data-table (Data-Driven Dynamic Form Building Block)
**Last Updated**: 2026-03-05

---

## Overview

| Attribute | Value |
|-----------|-------|
| Status | Design Complete |
| Priority | High |
| Complexity | Low-Medium |
| Estimated Files | 14 (all new) |
| Design Type | Reusable Building Block |
| Mockups | ✅ Regenerated (2026-03-05) - 5 screens |
| Stitch Project | 13047846909194906272 (v2) |
| Flow Diagram | ✅ Updated (2026-03-05) |
| GAP Plan | ✅ Updated (2026-03-05) |

---

## Design Philosophy

This feature implements a **100% data-driven, reusable Compose building block** - NOT a screen or wizard.

| Principle | Description |
|-----------|-------------|
| **Data-Driven** | Everything from API - tables, fields, types, options |
| **Building Block** | A composable function, not a screen |
| **Zero Navigation** | No Previous/Next buttons, no wizard flow |
| **Self-Contained** | Accepts state and callbacks from parent |
| **Drop-In Ready** | Can be placed in any parent composable |
| **Schema-Driven** | UI generated entirely from `columnHeaderData` |
| **No Hardcoding** | Number of tables, fields, names all dynamic |

---

## Current Implementation

### Existing Screens (4)

| Screen | Status | Description |
|--------|:------:|-------------|
| DataTableListScreen | Existing | Renders single table form during create flows |
| DataTableScreen | Existing | Lists data tables for an entity |
| DataTableDataScreen | Existing | Shows/edits existing table data |
| DataTableRowDialogScreen | Existing | Dialog for adding entries |

### New Building Block Components

| Component | Status | Description |
|-----------|:------:|-------------|
| DynamicDataTableForm | Planned | Main reusable building block |
| DynamicDataTableList | Planned | Multi-table wrapper component |
| DynamicField | Planned | Field type router composable |
| DataTableHeader | Planned | Optional header card |
| BooleanField | Planned | Switch component for BOOLEAN |
| IntegerField | Planned | Number input for INTEGER |
| DecimalField | Planned | Decimal input for DECIMAL |
| StringField | Planned | Text input for STRING |
| MultilineTextField | Planned | Multiline for TEXT |
| DateField | Planned | Date picker for DATE |
| DateTimeField | Planned | DateTime picker for DATETIME |
| DropdownField | Planned | Dropdown for CODELOOKUP |
| ColumnHeaderExt | Planned | Extension functions |
| MultiDataTableState | Planned | State data class for multi-table forms |

---

## Field Type Support

| columnDisplayType | Existing | Building Block |
|-------------------|:--------:|:--------------:|
| BOOLEAN | Existing | Planned |
| INTEGER | Existing | Planned |
| DECIMAL | Existing | Planned |
| STRING | Existing | Planned |
| TEXT | Existing | Planned |
| DATE | Existing | Planned |
| DATETIME | Missing | Planned |
| CODELOOKUP | Existing | Planned |

---

## Implementation Progress

### Phase 1: Extension Functions
- [ ] ColumnHeader.displayName extension
- [ ] ColumnHeader.isRequired extension
- [ ] ColumnHeader.isSystemColumn() function
- [ ] String.toDisplayName() extension

### Phase 2: Field Components
- [ ] BooleanField
- [ ] IntegerField
- [ ] DecimalField
- [ ] StringField
- [ ] MultilineTextField
- [ ] DateField
- [ ] DateTimeField
- [ ] DropdownField

### Phase 3: Core Components
- [ ] DynamicField router
- [ ] DataTableHeader
- [ ] DynamicDataTableForm (main building block)

### Phase 4: Multi-Table State Management
- [ ] MultiDataTableState data class
- [ ] ViewModel integration pattern
- [ ] DynamicDataTableList wrapper
- [ ] collectAllFormData() helper

### Phase 5: Integration Examples
- [ ] ClientDetailsScreen example (6 data tables)
- [ ] Bottom sheet example
- [ ] Accordion example
- [ ] Tab content example

---

## API Design

```kotlin
@Composable
fun DynamicDataTableForm(
    dataTable: DataTableEntity,
    values: Map<String, Any> = emptyMap(),
    onValuesChange: (Map<String, Any>) -> Unit,
    onValidationChange: ((Boolean) -> Unit)? = null,
    readOnly: Boolean = false,
    showHeader: Boolean = true,
    columns: Int = 2,
    modifier: Modifier = Modifier
)
```

---

## Related Documents

| Document | Path |
|----------|------|
| Feature Spec | [SPEC.md](./SPEC.md) |
| Gap Plan | [GAP_PLAN_DATA_TABLE_FORM.md](../../../plan-layer/GAP_PLAN_DATA_TABLE_FORM.md) |
| Component Flow | [data-table-form-flow.mmd](../../user-flows/flows/data-table-form-flow.mmd) |

---

## Commands

```bash
# Implement feature
/implement data-table

# Run feature tests
/test data-table

# Verify implementation
/verify data-table
```
