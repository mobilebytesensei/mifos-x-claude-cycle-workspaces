# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mifos-x-field-officer-app/design-spec-layer/features/data-table/mockups/.backup/20260305-194744/04-data-table-embedded-usage/README.md"
# last_modified: "2026-03-20"

# Data-Driven Multi-Table Form View

**Generated**: 2026-03-05
**Source**: Stitch MCP
**Project ID**: 7303051831053368728
**Screen ID**: ad1847ca8670418bb6c317042f4df658

## Description

Full screen example showing **data-driven** DynamicDataTableForm embedded in a real Client Details screen. The number of forms, form titles, and fields all come from API response - nothing is hardcoded.

## Key Concept: 100% Data-Driven

| Aspect | Source |
|--------|--------|
| Number of form sections | `dataTables.size` from API |
| Section titles | `dataTable.registeredTableName` from API |
| Fields per section | `dataTable.columnHeaderData` from API |
| Field types | `column.columnDisplayType` from API |
| Dropdown options | `column.columnValues` from API |

## Files

- `code.html` - HTML/Tailwind implementation
- `screen.png` - Visual screenshot

## Screen Sections (All Dynamic)

1. **Top App Bar** - Blue with back arrow, title
2. **Client Info Card** - Avatar, name, ID
3. **Data Table Forms** - N sections from API (e.g., 2, 6, or 10)
4. **Save All Data** - Primary action button

## Integration Pattern

```kotlin
// Dynamic rendering - no hardcoded sections
items(dataTables) { dataTable ->
    DynamicDataTableForm(
        dataTable = dataTable,  // Schema from API
        values = state.tableValues[dataTable.registeredTableName],
        onValuesChange = { ... }
    )
}
```

## Stitch Project

View in Stitch: https://stitch.withgoogle.com/
