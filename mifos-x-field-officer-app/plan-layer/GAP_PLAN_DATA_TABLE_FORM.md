# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mifos-x-field-officer-app/plan-layer/GAP_PLAN_DATA_TABLE_FORM.md"
# last_modified: "2026-03-20"

# Gap Planning: Data-Driven Dynamic Data Table Form Building Block

**Plan ID**: `gap-plan-datatable-form-260305-001`
**Feature**: data-table (Data-Driven Reusable Building Block)
**Created**: 2026-03-05
**Updated**: 2026-03-05
**Status**: Ready for Implementation

---

## Executive Summary

Implement a **100% data-driven, reusable Compose building block** (`DynamicDataTableForm`) that dynamically generates form UI from Fineract DataTable JSON schema. This is NOT a screen or wizard - it's a composable component that can be embedded anywhere.

### Core Principle: Everything from API

```
API Response: List<DataTableEntity>
├── dataTables.size        → Number of form sections (dynamic)
├── registeredTableName    → Section title (dynamic)
├── columnHeaderData.size  → Number of fields per section (dynamic)
├── columnDisplayType      → Field component type (dynamic)
└── columnValues           → Dropdown options (dynamic)
```

**Key Design Decisions**:
- **100% Data-Driven** - No hardcoded tables, fields, or types
- **No navigation** - Parent screen controls navigation
- **No Previous/Next** - Building block is stateless
- **Drop-in ready** - Works in screens, bottom sheets, accordions, tabs
- **Schema-driven** - UI generated entirely from `columnHeaderData`
- **Multi-table support** - Render N data tables from single API response

**Estimated Scope**: ~14 files, low-medium complexity

---

## Gap Analysis

### Current State
| Component | Status | Notes |
|-----------|--------|-------|
| `DataTableListScreen` | Exists | Renders single table form, but tightly coupled |
| `FormWidget` base class | Exists | Abstract form widget with type constants |
| Field type handling | Partial | Basic types, no grid layout, hardcoded |
| Reusable form component | Missing | No standalone building block |
| Two-column grid | Missing | Single column only |

### Target State
- New `DynamicDataTableForm` composable - reusable anywhere
- New `DynamicField` router for all 8 field types
- Individual field components (Boolean, Integer, Decimal, String, Text, Date, DateTime, Dropdown)
- ColumnHeader extension functions
- Two-column responsive grid layout

---

## Implementation Plan

### Phase 1: Extension Functions (Foundation)

#### Task 1.1: Create ColumnHeader Extensions
**File**: `feature/data-table/src/commonMain/kotlin/com/mifos/feature/dataTable/util/ColumnHeaderExt.kt`

```kotlin
// ColumnHeader extensions
val ColumnHeader.displayName: String
    get() = columnName
        ?.replace("_cd_", " - ")
        ?.replace("_", " ")
        ?.split(" ")
        ?.joinToString(" ") { word ->
            word.replaceFirstChar { it.uppercase() }
        } ?: "Field"

val ColumnHeader.isRequired: Boolean
    get() = columnNullable == false

fun ColumnHeader.isSystemColumn(): Boolean {
    val name = columnName ?: return false
    return columnPrimaryKey == true ||
           name == "id" ||
           name == "created_at" ||
           name == "updated_at" ||
           (isColumnIndexed == true && name.endsWith("_id"))
}

// String extension
fun String.toDisplayName(): String =
    replace("_", " ")
        .split(" ")
        .joinToString(" ") { it.replaceFirstChar { c -> c.uppercase() } }
```

**Acceptance Criteria**:
- [ ] `displayName` converts snake_case to Title Case
- [ ] `isSystemColumn` detects id, *_id, timestamps
- [ ] `isRequired` checks `columnNullable == false`

---

### Phase 2: Field Components (UI Building Blocks)

#### Task 2.1: BooleanField Component
**File**: `feature/data-table/src/commonMain/kotlin/com/mifos/feature/dataTable/components/fields/BooleanField.kt`

```kotlin
@Composable
fun BooleanField(
    label: String,
    value: Boolean,
    onValueChange: (Boolean) -> Unit,
    readOnly: Boolean = false,
    modifier: Modifier = Modifier
)
```

**UI Spec**:
- Row layout with label on left, Switch on right
- Padding: vertical 8dp
- Label: `bodyMedium` typography

---

#### Task 2.2: IntegerField Component
**File**: `feature/data-table/src/commonMain/kotlin/com/mifos/feature/dataTable/components/fields/IntegerField.kt`

```kotlin
@Composable
fun IntegerField(
    label: String,
    value: Int?,
    onValueChange: (Int) -> Unit,
    isError: Boolean = false,
    errorMessage: String? = null,
    readOnly: Boolean = false,
    modifier: Modifier = Modifier
)
```

**UI Spec**:
- OutlinedTextField with `KeyboardType.Number`
- Error state with red border
- Supporting text for error message

---

#### Task 2.3: DecimalField Component
**File**: `feature/data-table/src/commonMain/kotlin/com/mifos/feature/dataTable/components/fields/DecimalField.kt`

```kotlin
@Composable
fun DecimalField(
    label: String,
    value: Double?,
    onValueChange: (Double) -> Unit,
    isError: Boolean = false,
    errorMessage: String? = null,
    readOnly: Boolean = false,
    modifier: Modifier = Modifier
)
```

**UI Spec**:
- OutlinedTextField with `KeyboardType.Decimal`
- Error state with red border

---

#### Task 2.4: StringField Component
**File**: `feature/data-table/src/commonMain/kotlin/com/mifos/feature/dataTable/components/fields/StringField.kt`

```kotlin
@Composable
fun StringField(
    label: String,
    value: String?,
    onValueChange: (String) -> Unit,
    maxLength: Int? = null,
    isError: Boolean = false,
    errorMessage: String? = null,
    readOnly: Boolean = false,
    modifier: Modifier = Modifier
)
```

**UI Spec**:
- Single-line OutlinedTextField
- Character counter if maxLength set
- Error state with red border

---

#### Task 2.5: MultilineTextField Component
**File**: `feature/data-table/src/commonMain/kotlin/com/mifos/feature/dataTable/components/fields/MultilineTextField.kt`

```kotlin
@Composable
fun MultilineTextField(
    label: String,
    value: String?,
    onValueChange: (String) -> Unit,
    minLines: Int = 3,
    maxLines: Int = 5,
    isError: Boolean = false,
    errorMessage: String? = null,
    readOnly: Boolean = false,
    modifier: Modifier = Modifier
)
```

**UI Spec**:
- Multiline (3-5 lines default), expandable
- Error state with red border

---

#### Task 2.6: DateField Component
**File**: `feature/data-table/src/commonMain/kotlin/com/mifos/feature/dataTable/components/fields/DateField.kt`

```kotlin
@Composable
fun DateField(
    label: String,
    value: String?,  // ISO date string or display format
    onValueChange: (String) -> Unit,
    isError: Boolean = false,
    errorMessage: String? = null,
    readOnly: Boolean = false,
    modifier: Modifier = Modifier
)
```

**UI Spec**:
- OutlinedTextField (read-only) with calendar icon
- Tap opens `DatePickerDialog`
- Display format: "dd MMMM yyyy" (e.g., "05 March 2026")
- Use existing `MifosDatePickerTextField` from designsystem if available

---

#### Task 2.7: DateTimeField Component
**File**: `feature/data-table/src/commonMain/kotlin/com/mifos/feature/dataTable/components/fields/DateTimeField.kt`

```kotlin
@Composable
fun DateTimeField(
    label: String,
    value: String?,  // ISO datetime string
    onValueChange: (String) -> Unit,
    isError: Boolean = false,
    errorMessage: String? = null,
    readOnly: Boolean = false,
    modifier: Modifier = Modifier
)
```

**UI Spec**:
- Two-step picker: Date first, then Time
- Display format: "dd MMMM yyyy HH:mm"
- Calendar + clock icons

---

#### Task 2.8: DropdownField Component (CODELOOKUP)
**File**: `feature/data-table/src/commonMain/kotlin/com/mifos/feature/dataTable/components/fields/DropdownField.kt`

```kotlin
@Composable
fun DropdownField(
    label: String,
    options: List<ColumnValue>,  // From columnValues array
    selectedId: Int?,
    onValueChange: (Int) -> Unit,
    isError: Boolean = false,
    errorMessage: String? = null,
    readOnly: Boolean = false,
    modifier: Modifier = Modifier
)
```

**UI Spec**:
- ExposedDropdownMenuBox with OutlinedTextField
- Trailing icon: dropdown arrow (rotates on open)
- Options from `columnValues` array
- Display `value` text, return `id` on select

---

### Phase 3: Core Components

#### Task 3.1: DynamicField Router
**File**: `feature/data-table/src/commonMain/kotlin/com/mifos/feature/dataTable/components/DynamicField.kt`

```kotlin
@Composable
fun DynamicField(
    column: ColumnHeader,
    value: Any?,
    onValueChange: (Any) -> Unit,
    isError: Boolean = false,
    errorMessage: String? = null,
    readOnly: Boolean = false,
    modifier: Modifier = Modifier
)
```

**Logic**:
- Routes to correct field composable based on `columnDisplayType`
- Handles type casting
- Passes through error state

---

#### Task 3.2: DataTableHeader Component
**File**: `feature/data-table/src/commonMain/kotlin/com/mifos/feature/dataTable/components/DataTableHeader.kt`

```kotlin
@Composable
fun DataTableHeader(
    tableName: String,
    modifier: Modifier = Modifier
)
```

**UI Spec**:
- Surface with `surfaceVariant` background
- Edit icon + table name (formatted with toDisplayName())
- Rounded corners (top only: 8dp)

---

#### Task 3.3: DynamicDataTableForm Main Component
**File**: `feature/data-table/src/commonMain/kotlin/com/mifos/feature/dataTable/components/DynamicDataTableForm.kt`

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

**Implementation**:
1. Filter visible columns (exclude system columns)
2. Validate fields and call `onValidationChange`
3. Render optional header
4. Render grid with DynamicField for each column
5. Handle value changes via `onValuesChange`

**Grid Layout**:
```kotlin
LazyVerticalGrid(
    columns = GridCells.Fixed(columns),
    horizontalArrangement = Arrangement.spacedBy(16.dp),
    verticalArrangement = Arrangement.spacedBy(12.dp)
)
```

---

### Phase 4: Multi-Table State Management (NEW)

#### Task 4.1: MultiDataTableState Data Class
**File**: `feature/data-table/src/commonMain/kotlin/com/mifos/feature/dataTable/state/MultiDataTableState.kt`

```kotlin
/**
 * Centralized state for managing multiple data tables.
 * All keys are dynamic - determined by API response at runtime.
 */
data class MultiDataTableState(
    // Dynamic: Keys = table names from API (e.g., "CONDICION", "DOMICILIO_PARTICULAR")
    // Values = field values map (e.g., "MONTO_SOLICITADO" to 25000.0)
    val tableValues: Map<String, Map<String, Any>> = emptyMap(),

    // Dynamic: Tracks validation per table
    val tableValidation: Map<String, Boolean> = emptyMap(),

    val isLoading: Boolean = false,
    val error: String? = null
)
```

**Acceptance Criteria**:
- [ ] Holds values for N data tables (dynamic)
- [ ] Tracks validation state per table
- [ ] All keys come from API response

---

#### Task 4.2: DynamicDataTableList Wrapper Component
**File**: `feature/data-table/src/commonMain/kotlin/com/mifos/feature/dataTable/components/DynamicDataTableList.kt`

```kotlin
/**
 * Renders a list of data tables as form sections.
 * Number of sections is dynamic - determined by dataTables.size from API.
 */
@Composable
fun DynamicDataTableList(
    dataTables: List<DataTableEntity>,  // From API - could be 1, 6, or 20 tables
    allValues: Map<String, Map<String, Any>>,
    onValuesChange: (tableName: String, values: Map<String, Any>) -> Unit,
    onValidationChange: ((tableName: String, isValid: Boolean) -> Unit)? = null,
    readOnly: Boolean = false,
    columns: Int = 2,
    modifier: Modifier = Modifier
)
```

**Implementation**:
```kotlin
Column(
    modifier = modifier,
    verticalArrangement = Arrangement.spacedBy(16.dp)
) {
    // DYNAMIC: Iterates over whatever tables come from API
    dataTables.forEach { dataTable ->
        val tableName = dataTable.registeredTableName ?: return@forEach

        DynamicDataTableForm(
            dataTable = dataTable,
            values = allValues[tableName] ?: emptyMap(),
            onValuesChange = { values -> onValuesChange(tableName, values) },
            onValidationChange = { isValid ->
                onValidationChange?.invoke(tableName, isValid)
            },
            readOnly = readOnly,
            showHeader = true,
            columns = columns,
            modifier = Modifier.fillMaxWidth()
        )
    }
}
```

**Acceptance Criteria**:
- [ ] Renders N forms based on `dataTables.size`
- [ ] Each form title from `registeredTableName`
- [ ] Passes values/callbacks per table

---

#### Task 4.3: ViewModel Integration Pattern
**File**: Example integration (not a new file)

```kotlin
class ClientDataTablesViewModel(
    private val dataTableRepository: DataTableRepository
) : ViewModel() {

    private val _state = MutableStateFlow(MultiDataTableState())
    val state: StateFlow<MultiDataTableState> = _state.asStateFlow()

    private val _dataTables = MutableStateFlow<List<DataTableEntity>>(emptyList())
    val dataTables: StateFlow<List<DataTableEntity>> = _dataTables.asStateFlow()

    fun loadDataTables(clientId: Long) {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true) }
            try {
                // API returns dynamic list - could be any number of tables
                val tables = dataTableRepository.getDataTablesForClient(clientId)
                _dataTables.value = tables

                // Initialize values from existing data (dynamic keys)
                val initialValues = tables.associate { table ->
                    val tableName = table.registeredTableName ?: ""
                    tableName to extractExistingValues(table)
                }
                _state.update { it.copy(tableValues = initialValues, isLoading = false) }
            } catch (e: Exception) {
                _state.update { it.copy(error = e.message, isLoading = false) }
            }
        }
    }

    fun updateTableValues(tableName: String, values: Map<String, Any>) {
        _state.update { current ->
            current.copy(
                tableValues = current.tableValues + (tableName to values)
            )
        }
    }

    fun collectAllFormData(): Map<String, Map<String, Any>> {
        return _state.value.tableValues
    }
}
```

---

### Phase 5: Integration Examples

#### Task 5.1: Example Usage in Existing Screens
- Show how to embed in `ClientDetailsScreen`
- Show how to embed in `DataTableDataScreen`
- Example bottom sheet usage
- Example accordion usage

---

## File Summary

### New Files (14)
| # | File | Layer | Purpose |
|:-:|------|-------|---------|
| 1 | `util/ColumnHeaderExt.kt` | feature | Extension functions |
| 2 | `components/fields/BooleanField.kt` | feature | Switch for BOOLEAN |
| 3 | `components/fields/IntegerField.kt` | feature | Number input for INTEGER |
| 4 | `components/fields/DecimalField.kt` | feature | Decimal input for DECIMAL |
| 5 | `components/fields/StringField.kt` | feature | Text input for STRING |
| 6 | `components/fields/MultilineTextField.kt` | feature | Multiline for TEXT |
| 7 | `components/fields/DateField.kt` | feature | Date picker for DATE |
| 8 | `components/fields/DateTimeField.kt` | feature | DateTime picker for DATETIME |
| 9 | `components/fields/DropdownField.kt` | feature | Dropdown for CODELOOKUP |
| 10 | `components/DynamicField.kt` | feature | Field type router |
| 11 | `components/DataTableHeader.kt` | feature | Optional header card |
| 12 | `components/DynamicDataTableForm.kt` | feature | Main building block |
| 13 | `components/DynamicDataTableList.kt` | feature | Multi-table wrapper |
| 14 | `state/MultiDataTableState.kt` | feature | State data class |

### Modified Files (0)
No modifications to existing files required - this is a purely additive building block.

---

## Success Criteria

1. **100% Data-Driven** - No hardcoded tables, fields, or types
2. **All 8 field types** render correctly based on `columnDisplayType`
3. **Two-column grid** with configurable column count
4. **System columns auto-filtered** (id, *_id, timestamps)
5. **Validation callback** works correctly for required fields
6. **CODELOOKUP dropdowns** populated from `columnValues`
7. **Stateless design** - accepts values and callbacks, no internal state
8. **Drop-in ready** - works in any parent composable
9. **No navigation** - parent controls all navigation
10. **Multi-table support** - Render N tables from `List<DataTableEntity>`
11. **Centralized state** - `MultiDataTableState` holds all table values
12. **Dynamic keys** - All state keys come from API response

---

## Usage Examples

### Embedded in Screen
```kotlin
DynamicDataTableForm(
    dataTable = dataTable,
    values = formValues,
    onValuesChange = { viewModel.updateValues(it) },
    showHeader = true,
    columns = 2
)
```

### In Bottom Sheet
```kotlin
DynamicDataTableForm(
    dataTable = dataTable,
    values = values,
    onValuesChange = { values = it },
    onValidationChange = { isValid = it },
    showHeader = false,
    columns = 1
)
```

### In Accordion
```kotlin
AnimatedVisibility(visible = isExpanded) {
    DynamicDataTableForm(
        dataTable = dataTable,
        values = allValues[tableName] ?: emptyMap(),
        onValuesChange = { allValues[tableName] = it },
        showHeader = false
    )
}
```

---

## Next Steps

1. **Approve this plan** to begin implementation
2. Start with **Phase 1: Extension Functions**
3. Implement **Phase 2: Field Components** (can be parallelized)
4. Complete **Phase 3: Core Components**
5. Run `/implement data-table` when ready

---

## Commands

```bash
# Start implementation
/implement data-table

# Run tests after implementation
/test data-table

# Verify implementation
/verify data-table
```
