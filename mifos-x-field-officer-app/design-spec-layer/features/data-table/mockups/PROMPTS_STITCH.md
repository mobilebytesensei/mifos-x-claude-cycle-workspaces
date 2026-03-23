# template_meta
# template_version: "2.86.5"
# template_path: "workspaces/mifos-x/mifos-x-field-officer-app/design-spec-layer/features/data-table/mockups/PROMPTS_STITCH.md"
# last_modified: "2026-03-20"

# DynamicDataTableForm - Stitch Mockup Prompts

**Feature**: data-table (Dynamic Form Building Block)
**Type**: Reusable Compose Component
**Screens**: 5 (Component Previews)
**Generated**: 2026-03-05
**Updated**: 2026-03-05 (Added multi-table scenario)

---

## Design System

**Colors (Material Design 3 Default):**
- Primary: #1976D2 (Blue - Mifos brand)
- On Primary: #FFFFFF
- Surface: #FAFAFA
- On Surface: #1C1B1F
- Surface Variant: #E7E0EC
- Error: #B3261E
- Outline: #79747E

**Typography:**
- Font Family: Roboto
- Title Medium: 16sp / 500 weight
- Body Large: 16sp / 400 weight
- Body Medium: 14sp / 400 weight
- Label Large: 14sp / 500 weight

**Spacing:**
- Field gap: 12dp
- Grid gap: 16dp
- Card padding: 16dp

---

## Screen 1: DynamicDataTableForm - 2 Column Grid

Create a mobile component preview showing a dynamic form building block:

**Design Intent**: Show a reusable form component that renders fields from a DataTable schema. This is a building block that can be embedded in any screen.

**Header Card:**
- Surface variant background (#E7E0EC)
- Edit icon (✎) on left, blue color (#1976D2)
- Title: "DATOS_DE_LA_PERSONA" in Title Medium, semibold
- Rounded top corners (8dp)

**Form Grid (2 columns, LazyVerticalGrid):**
- 16dp horizontal gap between columns
- 12dp vertical gap between rows

**Row 1:**
- Left: Date field "FECHA_DE_NACIMIENTO"
  - Calendar icon trailing
  - Placeholder: "Select date"
  - OutlinedTextField style
- Right: Dropdown "ESTADO_CIVIL"
  - Trailing dropdown arrow
  - Text: "Select option"
  - ExposedDropdownMenu style

**Row 2:**
- Left: Text field "MUNICIPIO"
  - Empty OutlinedTextField
  - Label at top
- Right: Text field "TIPO_DE_IDENTIFICACION"
  - Empty OutlinedTextField
  - Label at top

**Row 3:**
- Left: Dropdown "MARITAL STATUS"
  - Trailing dropdown arrow
  - Text: "Select option"
- Right: Dropdown "SEXO"
  - Trailing dropdown arrow
  - Text: "Select option"

**Row 4:**
- Left: Number field "EDAD"
  - Empty OutlinedTextField
  - Number keyboard hint
- Right: Number field "NUMERO_DE_DEPENDIENTES"
  - Empty OutlinedTextField
  - Number keyboard hint

**Style:**
- Background: #FAFAFA (surface)
- All fields have outlined style
- Labels above fields (M3 style)
- Touch targets: 48dp minimum

**Dimensions:** 393x600 (component, not full screen)

---

## Screen 2: DynamicDataTableForm - Single Column (Phone)

Create a mobile component preview showing the same form in single column layout:

**Design Intent**: Show responsive layout for narrow screens (phones in portrait).

**Header Card:**
- Same as Screen 1
- "CONDICION" as title

**Form Fields (single column, stacked):**
Each field takes full width with 12dp vertical spacing:

1. "MONTO_SOLICITADO" - Decimal field
   - OutlinedTextField
   - Decimal keyboard hint
   - Full width

2. "SI" - Dropdown field
   - ExposedDropdownMenu
   - "Select option" placeholder
   - Full width

3. "LUGAR" - Multiline text field
   - OutlinedTextField with minLines=3
   - Expandable
   - Full width

4. "ACTIVO" - Switch toggle
   - Label on left, Switch on right
   - Row layout
   - Full width

**Style:**
- Same colors as Screen 1
- Single column layout (columns = 1)
- 16dp horizontal padding
- 12dp between fields

**Dimensions:** 393x500 (component, not full screen)

---

## Screen 3: Field Type Showcase

Create a component preview showing all 8 field types supported:

**Design Intent**: Document all field variations for implementation reference.

**Title:** "Field Types" - Title Large, bold

**Field Grid (2 columns):**

**Row 1:**
- BooleanField: Switch with label "Active"
- IntegerField: "Age" with 42 value

**Row 2:**
- DecimalField: "Amount" with 1234.56 value
- StringField: "Name" with "John Doe" value

**Row 3:**
- MultilineTextField: "Notes" with 3 lines visible, sample text
- DateField: "Birth Date" with calendar icon, "05 Mar 2026"

**Row 4:**
- DateTimeField: "Created At" with datetime picker, "05 Mar 2026 14:30"
- DropdownField: "Country" with expanded state showing 3 options

**Each field shows:**
- Label above (Material 3 style)
- Value/placeholder
- Appropriate input indicator (keyboard type icon, dropdown arrow, calendar icon)
- Error state variant where applicable

**Style:**
- Card wrapper with 16dp padding
- Surface background
- 16dp gap between field rows
- Clear visual distinction between field types

**Dimensions:** 393x650 (component showcase)

---

## Screen 4: Embedded Usage Example

Create a preview showing DynamicDataTableForm embedded in a parent screen:

**Design Intent**: Show how the building block integrates with a real screen.

**Top App Bar:**
- Title: "Client Details"
- Back arrow
- Blue background (#1976D2)

**Content (LazyColumn):**

**Section 1: Client Info Card**
- Avatar placeholder (circle, 64dp)
- Name: "Maria Garcia"
- ID: "CLI-2026-0042"
- Card with surface background

**Section 2: DynamicDataTableForm (embedded)**
- Header: "DATOS_PERSONALES"
- 4 fields in 2-column grid
- Surface variant header
- No parent padding (component handles it)

**Section 3: Another DynamicDataTableForm**
- Header: "DATOS_LABORALES"
- 3 fields in 2-column grid
- Collapsed accordion style

**Bottom:**
- "Save All Data" - Primary button, full width
- 16dp bottom padding

**Style:**
- Shows real integration context
- Multiple data tables on one screen
- Accordion/expandable pattern
- Blue top bar, white content area

**Dimensions:** 393x852 (full screen)

---

## Screen 5: Data-Driven Multi-Table Form

Create a full-screen preview showing multiple DynamicDataTableForm components rendered from API data:

**Design Intent**: Show data-driven rendering where the number of forms, form titles, and fields all come from API response. Nothing is hardcoded.

**Top App Bar:**
- Title: "Client Data Tables"
- Subtitle: "Maria Garcia - CLI-2026-0042"
- Back arrow
- Blue background (#1976D2)

**Key Visual Message:** Show that this is DYNAMIC:
- Small info banner at top: "Showing {N} data tables from API"
- Forms are rendered in a loop, not hardcoded

**Content (LazyColumn - renders items(dataTables)):**

**Dynamic Form 1 (Expanded):**
- Header: Edit icon, dynamic title from API (e.g., "Datos Personales")
- Surface variant background
- Fields in 2-column grid - all from columnHeaderData:
  - Date field, Dropdown field, Text field, Integer field
  - Show 4-6 sample fields

**Dynamic Form 2 (Expanded):**
- Header: Edit icon, different title from API
- Different number of fields (3 fields shown)
- Shows variety: Decimal, Dropdown, Multiline text

**Dynamic Form 3 (Collapsed):**
- Shows accordion pattern
- Header only with chevron
- Badge: "{N} fields" (number from API)

**Dynamic Form 4 (Collapsed):**
- Another collapsed section
- Different field count badge

**Visual Indicators:**
- Small "API" badge on each header to show data source
- Field count comes from columnHeaderData.size
- Form title comes from registeredTableName

**Bottom Bar (Fixed):**
- "Save All ({N} tables)" - Primary button
- Button text shows dynamic count

**Visual Design:**
- Each section is a Card
- 16dp spacing between cards
- Expanded sections show DynamicDataTableForm
- Collapsed sections show header + field count
- All text/counts are dynamic placeholders

**Dimensions:** 393x852 (full screen, scrollable)

---

## After Generation Checklist

- [ ] All field types visible and correctly styled
- [ ] 2-column and 1-column layouts shown
- [ ] Header card with edit icon
- [ ] Dropdown fields show arrow indicator
- [ ] Date fields show calendar icon
- [ ] Switch toggle for boolean
- [ ] Touch targets ≥ 48dp
- [ ] Labels above fields (M3 style)
- [ ] Consistent 12dp/16dp spacing

---

## Tips for Stitch

1. This is a COMPONENT, not a full screen - focus on the form building block
2. Use Material Design 3 outlined text field style
3. Show variety of field types (date, dropdown, text, number, switch)
4. Grid layout should clearly show 2-column arrangement
5. Header card is distinctive with surface variant color
6. All fields should look interactive (not disabled)

---

## After-Generation Workflow

1. Export generated screens from Stitch
2. Save to: `mockups/prod/stitch/0{N}-data-table-{screen}/`
3. Run: `/implement data-table` to generate Compose code
