# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mifos-x-field-officer-app/design-spec-layer/features/data-table/mockups/prod/stitch/04-data-table-embedded-usage/README.md"
# last_modified: "2026-03-20"

# Client Details - Embedded Form Usage

**Generated**: 2026-03-05
**Source**: Stitch MCP
**Project ID**: 13047846909194906272
**Screen ID**: 0c33b35aae6d4b6f96c04fe5dfb3f69c

## Description

Full screen example showing DynamicDataTableForm embedded in a real Client Details screen. Demonstrates integration pattern with multiple data table sections.

## Files

- `code.html` - HTML/Tailwind implementation
- `screen.png` - Visual screenshot

## Screen Sections

1. **Top App Bar** - Blue with back arrow, "Client Details" title
2. **Client Info Card** - Avatar, name "Maria Garcia", ID "CLI-2026-0042"
3. **DATOS_PERSONALES** - Expanded data table form (4 fields in 2-column grid)
4. **DATOS_LABORALES** - Collapsed accordion (3 fields badge)
5. **Save All Data** - Primary action button

## Integration Pattern

Shows how DynamicDataTableForm can be:
- Embedded in LazyColumn
- Used multiple times on same screen
- Combined with accordion/expandable pattern

## Stitch Project

View in Stitch: https://stitch.withgoogle.com/
