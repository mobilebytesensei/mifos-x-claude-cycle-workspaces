# API-Driven Multi-Table Form View

**Generated**: 2026-03-05
**Source**: Stitch MCP
**Project ID**: 13047846909194906272
**Screen ID**: 62cefa327a2b4b279d1b096150d6ecaf

## Description

Full-screen mobile interface demonstrating **100% data-driven rendering** of multiple form sections from API response. Shows how `DynamicDataTableList` renders N tables dynamically.

## Key Concept: Data-Driven

| Aspect | Source |
|--------|--------|
| Number of form sections | `dataTables.size` from API (4 shown) |
| Section titles | `dataTable.registeredTableName` from API |
| Fields per section | `dataTable.columnHeaderData` from API |
| Field types | `column.columnDisplayType` from API |
| Dropdown options | `column.columnValues` from API |

## Files

- `code.html` - HTML/Tailwind implementation
- `screen.png` - Visual screenshot

## Screen Sections (All Dynamic)

1. **Top App Bar** - "Client Data Tables", subtitle "Maria Garcia - CLI-2026-0042"
2. **Info Banner** - "Showing 4 data tables from API"
3. **Form 1: Datos Personales** (Expanded) - 4 fields in 2-column grid
4. **Form 2: Condicion** (Expanded) - 3 fields including multiline
5. **Form 3: Domicilio Particular** (Collapsed) - "8 fields" badge
6. **Form 4: Domicilio Negocio** (Collapsed) - "9 fields" badge
7. **Bottom Bar** - "Save All (4 tables)" button

## Integration Pattern

```kotlin
// Dynamic rendering - no hardcoded sections
DynamicDataTableList(
    dataTables = dataTables,  // List from API
    allValues = state.tableValues,
    onValuesChange = { tableName, values ->
        viewModel.updateTableValues(tableName, values)
    }
)
```

## Stitch Project

View in Stitch: https://stitch.withgoogle.com/
