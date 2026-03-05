# Dynamic Data Table Form - Feature Specification

**Feature**: data-table (Data-Driven Dynamic Form Building Block)
**Status**: Planning
**Priority**: High
**Created**: 2026-03-05
**Updated**: 2026-03-05

---

## Overview

Design a **standalone, reusable Compose building block** that dynamically generates form UI from Fineract DataTable JSON schema. This is NOT a screen - it's a composable component that can be embedded anywhere in the app where data tables need to be rendered.

### Key Concept: 100% Data-Driven

**Everything comes from the API** - no hardcoded form sections, field names, or field types:
- Number of data tables: Dynamic (1, 6, 20, etc.)
- Table names: Dynamic (from `registeredTableName`)
- Number of fields: Dynamic (from `columnHeaderData.size`)
- Field types: Dynamic (from `columnDisplayType`)
- Dropdown options: Dynamic (from `columnValues`)

### Design Philosophy
- **Data-Driven**: UI generated entirely from API response
- **Building Block**: A composable function, not a screen
- **Zero Navigation**: No Previous/Next buttons, no wizard flow
- **Self-Contained**: Handles its own state or accepts external state
- **Drop-In Ready**: Can be placed in any parent composable
- **Schema-Driven**: UI generated entirely from `columnHeaderData`

### Use Cases
1. **Embedded in Client Details**: Show client data tables inline
2. **Part of Loan Application**: Include as a section in loan form
3. **Inside Bottom Sheets**: Quick data entry dialogs
4. **Accordion Sections**: Expandable data table sections
5. **Tab Content**: Each tab shows a different data table

---

## Core Concept

```
┌─────────────────────────────────────────────────────────────────────┐
│  ANY PARENT SCREEN (ClientDetails, LoanApplication, etc.)          │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  DynamicDataTableForm(                                        │ │
│  │      dataTable = dataTableEntity,                             │ │
│  │      values = mapOf("FIELD_1" to "value1", ...),              │ │
│  │      onValuesChange = { newValues -> updateState(newValues) },│ │
│  │      onValidationChange = { isValid -> ... },                 │ │
│  │      modifier = Modifier.fillMaxWidth()                       │ │
│  │  )                                                            │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  [ Parent's Own Buttons / Actions ]                                │
└─────────────────────────────────────────────────────────────────────┘
```

---

## API Design

### Primary Composable

```kotlin
/**
 * A standalone, reusable composable that renders a dynamic form
 * based on Fineract DataTable schema.
 *
 * Usage:
 * ```
 * DynamicDataTableForm(
 *     dataTable = myDataTable,
 *     values = formState.values,
 *     onValuesChange = { viewModel.updateValues(it) },
 *     modifier = Modifier.fillMaxWidth()
 * )
 * ```
 */
@Composable
fun DynamicDataTableForm(
    dataTable: DataTableEntity,
    values: Map<String, Any> = emptyMap(),
    onValuesChange: (Map<String, Any>) -> Unit,
    onValidationChange: ((Boolean) -> Unit)? = null,
    readOnly: Boolean = false,
    showHeader: Boolean = true,
    columns: Int = 2,  // 1 for phone, 2 for tablet
    modifier: Modifier = Modifier
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dataTable` | `DataTableEntity` | required | Schema from Fineract API |
| `values` | `Map<String, Any>` | `emptyMap()` | Current field values |
| `onValuesChange` | `(Map<String, Any>) -> Unit` | required | Callback when any value changes |
| `onValidationChange` | `((Boolean) -> Unit)?` | `null` | Optional callback for validation state |
| `readOnly` | `Boolean` | `false` | Disable all inputs |
| `showHeader` | `Boolean` | `true` | Show table name header card |
| `columns` | `Int` | `2` | Grid columns (adaptive by default) |
| `modifier` | `Modifier` | `Modifier` | Standard Compose modifier |

---

## Component Architecture

```
DynamicDataTableForm
├── DataTableHeader (optional)
│   └── Card with tableName + edit icon
│
└── DynamicFormGrid
    ├── LazyVerticalGrid (or Column for single column)
    │
    └── For each visible column in columnHeaderData:
        └── DynamicField
            ├── BooleanField (BOOLEAN)
            ├── IntegerField (INTEGER)
            ├── DecimalField (DECIMAL)
            ├── StringField (STRING)
            ├── MultilineTextField (TEXT)
            ├── DateField (DATE)
            ├── DateTimeField (DATETIME)
            └── DropdownField (CODELOOKUP)
```

---

## Column Type Mapping

| columnDisplayType | UI Component | Keyboard | Example |
|-------------------|--------------|----------|---------|
| `BOOLEAN` | `Switch` | N/A | Toggle on/off |
| `INTEGER` | `OutlinedTextField` | Number | 42 |
| `DECIMAL` | `OutlinedTextField` | Decimal | 1234.56 |
| `STRING` | `OutlinedTextField` | Text | "John Doe" |
| `TEXT` | `OutlinedTextField` (multiline) | Text | Long description |
| `DATE` | `DatePickerTextField` | Date picker | 05 March 2026 |
| `DATETIME` | `DateTimePickerTextField` | DateTime picker | 05 March 2026 14:30 |
| `CODELOOKUP` | `ExposedDropdownMenu` | N/A | Select from options |

### Hidden Columns (Auto-Filtered)
- `id` (primary key)
- `client_id`, `loan_id`, `group_id` (foreign keys)
- `created_at`, `updated_at` (timestamps)
- Any column where `isColumnPrimaryKey == true`
- Any column where `isColumnIndexed == true` AND ends with `_id`

---

## Visual Layout

### With Header (showHeader = true)
```
┌─────────────────────────────────────────────────────────────────┐
│ [✎] DATOS_DE_LA_PERSONA_SOLICITANTE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────┐  ┌─────────────────────┐              │
│  │ FECHA_DE_NACIMIENTO │  │ STATE            ▼ │              │
│  │ [📅] ______________ │  │ [Select option]    │              │
│  └─────────────────────┘  └─────────────────────┘              │
│                                                                 │
│  ┌─────────────────────┐  ┌─────────────────────┐              │
│  │ MUNICIPIO           │  │ TIPO_DE_IDENT...   │              │
│  │ ___________________ │  │ ___________________ │              │
│  └─────────────────────┘  └─────────────────────┘              │
│                                                                 │
│  ┌─────────────────────┐  ┌─────────────────────┐              │
│  │ MARITAL STATUS   ▼  │  │ SEXO             ▼ │              │
│  │ [Select option]     │  │ [Select option]    │              │
│  └─────────────────────┘  └─────────────────────┘              │
│                                                                 │
│  ┌─────────────────────┐  ┌─────────────────────┐              │
│  │ EDAD                │  │ NUMERO_DE_DEP...   │              │
│  │ ___________________ │  │ ___________________ │              │
│  └─────────────────────┘  └─────────────────────┘              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Without Header (showHeader = false)
```
┌─────────────────────────────────────────────────────────────────┐
│  ┌─────────────────────┐  ┌─────────────────────┐              │
│  │ FECHA_DE_NACIMIENTO │  │ STATE            ▼ │              │
│  │ [📅] ______________ │  │ [Select option]    │              │
│  └─────────────────────┘  └─────────────────────┘              │
│                                                                 │
│  ┌─────────────────────┐  ┌─────────────────────┐              │
│  │ MUNICIPIO           │  │ TIPO_DE_IDENT...   │              │
│  │ ___________________ │  │ ___________________ │              │
│  └─────────────────────┘  └─────────────────────┘              │
│                                                                 │
│  ... more fields ...                                            │
└─────────────────────────────────────────────────────────────────┘
```

### Single Column (columns = 1, for phones)
```
┌─────────────────────────────┐
│ [✎] CONDICION               │
├─────────────────────────────┤
│  ┌─────────────────────────┐│
│  │ MONTO_SOLICITADO        ││
│  │ _______________________ ││
│  └─────────────────────────┘│
│                             │
│  ┌─────────────────────────┐│
│  │ SI                    ▼ ││
│  │ [Select option]         ││
│  └─────────────────────────┘│
│                             │
│  ┌─────────────────────────┐│
│  │ LUGAR                   ││
│  │ _______________________ ││
│  │ _______________________/││
│  └─────────────────────────┘│
└─────────────────────────────┘
```

---

## Usage Examples

### Example 1: Embedded in Client Details Screen

```kotlin
@Composable
fun ClientDetailsScreen(viewModel: ClientDetailsViewModel) {
    val clientDataTables by viewModel.dataTables.collectAsState()
    val formValues by viewModel.dataTableValues.collectAsState()

    LazyColumn {
        // Client basic info
        item { ClientInfoCard(viewModel.client) }

        // Data tables as sections
        items(clientDataTables) { dataTable ->
            DynamicDataTableForm(
                dataTable = dataTable,
                values = formValues[dataTable.registeredTableName] ?: emptyMap(),
                onValuesChange = { values ->
                    viewModel.updateDataTableValues(dataTable.registeredTableName!!, values)
                },
                showHeader = true,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp)
            )
        }

        // Save button
        item {
            Button(onClick = { viewModel.saveAllDataTables() }) {
                Text("Save All Data")
            }
        }
    }
}
```

### Example 2: Inside a Bottom Sheet

```kotlin
@Composable
fun DataTableBottomSheet(
    dataTable: DataTableEntity,
    onSave: (Map<String, Any>) -> Unit,
    onDismiss: () -> Unit
) {
    var values by remember { mutableStateOf(emptyMap<String, Any>()) }
    var isValid by remember { mutableStateOf(false) }

    ModalBottomSheet(onDismissRequest = onDismiss) {
        Column(modifier = Modifier.padding(16.dp)) {
            DynamicDataTableForm(
                dataTable = dataTable,
                values = values,
                onValuesChange = { values = it },
                onValidationChange = { isValid = it },
                showHeader = false,  // Bottom sheet has its own title
                columns = 1,         // Single column for bottom sheet
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(modifier = Modifier.height(16.dp))

            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                OutlinedButton(onClick = onDismiss, modifier = Modifier.weight(1f)) {
                    Text("Cancel")
                }
                Button(
                    onClick = { onSave(values) },
                    enabled = isValid,
                    modifier = Modifier.weight(1f)
                ) {
                    Text("Save")
                }
            }
        }
    }
}
```

### Example 3: Expandable Accordion

```kotlin
@Composable
fun DataTableAccordion(dataTables: List<DataTableEntity>) {
    var expandedIndex by remember { mutableStateOf<Int?>(null) }
    val allValues = remember { mutableStateMapOf<String, Map<String, Any>>() }

    Column {
        dataTables.forEachIndexed { index, dataTable ->
            val tableName = dataTable.registeredTableName ?: ""
            val isExpanded = expandedIndex == index

            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 4.dp)
            ) {
                Column {
                    // Header (clickable)
                    ListItem(
                        headlineContent = { Text(tableName.toDisplayName()) },
                        trailingContent = {
                            Icon(
                                if (isExpanded) Icons.Default.ExpandLess
                                else Icons.Default.ExpandMore,
                                contentDescription = null
                            )
                        },
                        modifier = Modifier.clickable {
                            expandedIndex = if (isExpanded) null else index
                        }
                    )

                    // Content (animated)
                    AnimatedVisibility(visible = isExpanded) {
                        DynamicDataTableForm(
                            dataTable = dataTable,
                            values = allValues[tableName] ?: emptyMap(),
                            onValuesChange = { allValues[tableName] = it },
                            showHeader = false,
                            modifier = Modifier.padding(16.dp)
                        )
                    }
                }
            }
        }
    }
}
```

### Example 4: Tab Content

```kotlin
@Composable
fun DataTableTabs(dataTables: List<DataTableEntity>) {
    var selectedTabIndex by remember { mutableStateOf(0) }
    val allValues = remember { mutableStateMapOf<String, Map<String, Any>>() }

    Column {
        ScrollableTabRow(selectedTabIndex = selectedTabIndex) {
            dataTables.forEachIndexed { index, table ->
                Tab(
                    selected = selectedTabIndex == index,
                    onClick = { selectedTabIndex = index },
                    text = { Text(table.registeredTableName?.toDisplayName() ?: "Table $index") }
                )
            }
        }

        val currentTable = dataTables[selectedTabIndex]
        val tableName = currentTable.registeredTableName ?: ""

        DynamicDataTableForm(
            dataTable = currentTable,
            values = allValues[tableName] ?: emptyMap(),
            onValuesChange = { allValues[tableName] = it },
            showHeader = false,  // Tabs serve as header
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        )
    }
}
```

---

## Component Implementation

### DynamicDataTableForm.kt

```kotlin
@Composable
fun DynamicDataTableForm(
    dataTable: DataTableEntity,
    values: Map<String, Any>,
    onValuesChange: (Map<String, Any>) -> Unit,
    onValidationChange: ((Boolean) -> Unit)? = null,
    readOnly: Boolean = false,
    showHeader: Boolean = true,
    columns: Int = 2,
    modifier: Modifier = Modifier
) {
    // Filter visible columns
    val visibleColumns = remember(dataTable) {
        dataTable.columnHeaderData.filter { !it.isSystemColumn() }
    }

    // Track validation
    val validationState = remember(values, visibleColumns) {
        validateFields(visibleColumns, values)
    }

    LaunchedEffect(validationState) {
        onValidationChange?.invoke(validationState.all { it.value == null })
    }

    Column(modifier = modifier) {
        // Optional header
        if (showHeader) {
            DataTableHeader(
                tableName = dataTable.registeredTableName ?: "Data Table",
                modifier = Modifier.fillMaxWidth()
            )
            Spacer(modifier = Modifier.height(16.dp))
        }

        // Form grid
        DynamicFormGrid(
            columns = visibleColumns,
            values = values,
            validationErrors = validationState,
            onValueChange = { fieldName, value ->
                onValuesChange(values + (fieldName to value))
            },
            readOnly = readOnly,
            gridColumns = columns
        )
    }
}

@Composable
private fun DataTableHeader(
    tableName: String,
    modifier: Modifier = Modifier
) {
    Surface(
        color = MaterialTheme.colorScheme.surfaceVariant,
        shape = RoundedCornerShape(topStart = 8.dp, topEnd = 8.dp),
        modifier = modifier
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                imageVector = Icons.Default.Edit,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.primary
            )
            Spacer(modifier = Modifier.width(12.dp))
            Text(
                text = tableName.toDisplayName(),
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.SemiBold
            )
        }
    }
}

@Composable
private fun DynamicFormGrid(
    columns: List<ColumnHeader>,
    values: Map<String, Any>,
    validationErrors: Map<String, String?>,
    onValueChange: (String, Any) -> Unit,
    readOnly: Boolean,
    gridColumns: Int
) {
    LazyVerticalGrid(
        columns = GridCells.Fixed(gridColumns),
        horizontalArrangement = Arrangement.spacedBy(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
        modifier = Modifier.heightIn(max = 600.dp)  // Prevent infinite height
    ) {
        items(columns, key = { it.columnName ?: it.hashCode() }) { column ->
            val fieldName = column.columnName ?: return@items
            DynamicField(
                column = column,
                value = values[fieldName],
                onValueChange = { onValueChange(fieldName, it) },
                isError = validationErrors[fieldName] != null,
                errorMessage = validationErrors[fieldName],
                readOnly = readOnly,
                modifier = Modifier.fillMaxWidth()
            )
        }
    }
}

private fun validateFields(
    columns: List<ColumnHeader>,
    values: Map<String, Any>
): Map<String, String?> {
    return columns.associate { column ->
        val fieldName = column.columnName ?: ""
        val value = values[fieldName]
        val error = when {
            column.isRequired && (value == null || value.toString().isBlank()) ->
                "${column.displayName} is required"
            column.columnLength != null && column.columnLength > 0 &&
                value?.toString()?.length ?: 0 > column.columnLength ->
                "Maximum ${column.columnLength} characters"
            else -> null
        }
        fieldName to error
    }
}
```

### DynamicField.kt

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
) {
    when (column.columnDisplayType) {
        "BOOLEAN" -> BooleanField(
            label = column.displayName,
            value = value as? Boolean ?: false,
            onValueChange = onValueChange,
            readOnly = readOnly,
            modifier = modifier
        )
        "INTEGER" -> IntegerField(
            label = column.displayName,
            value = value as? Int,
            onValueChange = onValueChange,
            isError = isError,
            errorMessage = errorMessage,
            readOnly = readOnly,
            modifier = modifier
        )
        "DECIMAL" -> DecimalField(
            label = column.displayName,
            value = value as? Double,
            onValueChange = onValueChange,
            isError = isError,
            errorMessage = errorMessage,
            readOnly = readOnly,
            modifier = modifier
        )
        "STRING" -> StringField(
            label = column.displayName,
            value = value as? String,
            onValueChange = onValueChange,
            maxLength = column.columnLength,
            isError = isError,
            errorMessage = errorMessage,
            readOnly = readOnly,
            modifier = modifier
        )
        "TEXT" -> MultilineTextField(
            label = column.displayName,
            value = value as? String,
            onValueChange = onValueChange,
            isError = isError,
            errorMessage = errorMessage,
            readOnly = readOnly,
            modifier = modifier
        )
        "DATE" -> DateField(
            label = column.displayName,
            value = value as? String,
            onValueChange = onValueChange,
            isError = isError,
            errorMessage = errorMessage,
            readOnly = readOnly,
            modifier = modifier
        )
        "DATETIME" -> DateTimeField(
            label = column.displayName,
            value = value as? String,
            onValueChange = onValueChange,
            isError = isError,
            errorMessage = errorMessage,
            readOnly = readOnly,
            modifier = modifier
        )
        "CODELOOKUP" -> DropdownField(
            label = column.displayName,
            options = column.columnValues,
            selectedId = value as? Int,
            onValueChange = { onValueChange(it) },
            isError = isError,
            errorMessage = errorMessage,
            readOnly = readOnly,
            modifier = modifier
        )
        else -> StringField(
            label = column.displayName,
            value = value?.toString(),
            onValueChange = onValueChange,
            isError = isError,
            errorMessage = errorMessage,
            readOnly = readOnly,
            modifier = modifier
        )
    }
}
```

---

## Extension Functions

```kotlin
// ColumnHeader extensions
val ColumnHeader.displayName: String
    get() = columnName
        ?.replace("_cd_", " - ")  // Handle code lookup naming
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

// String extensions
fun String.toDisplayName(): String =
    replace("_", " ")
        .split(" ")
        .joinToString(" ") { it.replaceFirstChar { c -> c.uppercase() } }
```

---

## Files to Create

| # | File | Purpose |
|:-:|------|---------|
| 1 | `components/DynamicDataTableForm.kt` | Main building block composable |
| 2 | `components/DynamicField.kt` | Field type router |
| 3 | `components/DataTableHeader.kt` | Optional header card |
| 4 | `components/fields/BooleanField.kt` | Switch for BOOLEAN |
| 5 | `components/fields/IntegerField.kt` | Number input for INTEGER |
| 6 | `components/fields/DecimalField.kt` | Decimal input for DECIMAL |
| 7 | `components/fields/StringField.kt` | Text input for STRING |
| 8 | `components/fields/MultilineTextField.kt` | Multiline for TEXT |
| 9 | `components/fields/DateField.kt` | Date picker for DATE |
| 10 | `components/fields/DateTimeField.kt` | DateTime picker for DATETIME |
| 11 | `components/fields/DropdownField.kt` | Dropdown for CODELOOKUP |
| 12 | `util/ColumnHeaderExt.kt` | Extension functions |

---

## Testing

```kotlin
@Preview
@Composable
fun DynamicDataTableFormPreview() {
    val sampleTable = DataTableEntity(
        registeredTableName = "DATOS_PERSONA",
        columnHeaderData = listOf(
            ColumnHeader(columnName = "NOMBRE", columnDisplayType = "STRING"),
            ColumnHeader(columnName = "EDAD", columnDisplayType = "INTEGER"),
            ColumnHeader(columnName = "ESTADO_CIVIL", columnDisplayType = "CODELOOKUP",
                columnValues = listOf(
                    ColumnValue(id = 1, value = "SOLTERO"),
                    ColumnValue(id = 2, value = "CASADO")
                )),
            ColumnHeader(columnName = "FECHA_NACIMIENTO", columnDisplayType = "DATE"),
            ColumnHeader(columnName = "ACTIVO", columnDisplayType = "BOOLEAN")
        )
    )

    var values by remember { mutableStateOf(emptyMap<String, Any>()) }

    DynamicDataTableForm(
        dataTable = sampleTable,
        values = values,
        onValuesChange = { values = it },
        showHeader = true,
        columns = 2
    )
}
```

---

## Multi-Table State Management

When rendering multiple data tables on a single screen, the state management follows a centralized ViewModel pattern. **Everything is 100% dynamic** - the number of tables, table names, fields, and field types are all determined by the API response at runtime.

### Key Principle: Fully Data-Driven

```
┌─────────────────────────────────────────────────────────────────────────┐
│  API Response: List<DataTableEntity>                                    │
│  - Could be 1 table, 6 tables, or any number                           │
│  - Table names are dynamic (CONDICION, CUSTOM_TABLE_XYZ, etc.)         │
│  - Fields per table are dynamic (3 fields, 15 fields, etc.)            │
│  - Field types are dynamic (STRING, DATE, CODELOOKUP, etc.)            │
│                                                                         │
│  ↓ Renders dynamically ↓                                                │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  DynamicDataTableList(dataTables = apiResponse)                 │   │
│  │    → Iterates over List<DataTableEntity>                        │   │
│  │    → Renders N forms based on list size                         │   │
│  │    → Each form renders M fields based on columnHeaderData       │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

### No Hardcoding - Everything from API

| Aspect | Source | Example |
|--------|--------|---------|
| Number of forms | `dataTables.size` | Could be 1, 3, 6, or 20 |
| Form title | `dataTable.registeredTableName` | "CONDICION", "DATOS_PERSONALES" |
| Number of fields | `dataTable.columnHeaderData.size` | Could be 3, 8, or 25 fields |
| Field name | `column.columnName` | "FECHA_DE_NACIMIENTO" |
| Field type | `column.columnDisplayType` | "DATE", "STRING", "CODELOOKUP" |
| Dropdown options | `column.columnValues` | List of id/value pairs |
| Required/Optional | `column.columnNullable` | true/false |

### State Structure (Fully Dynamic)

```kotlin
// Centralized state: tableName → fieldName → value
// Keys are dynamic - determined by API response at runtime
data class MultiDataTableState(
    // Dynamic: Keys = table names from API (e.g., "CONDICION", "DOMICILIO_PARTICULAR")
    // Values = field values map (e.g., "MONTO_SOLICITADO" to 25000.0)
    val tableValues: Map<String, Map<String, Any>> = emptyMap(),

    // Dynamic: Tracks validation per table
    val tableValidation: Map<String, Boolean> = emptyMap(),

    val isLoading: Boolean = false,
    val error: String? = null
)

// Example at runtime (all keys from API):
// tableValues = {
//     "CONDICION" to { "MONTO_SOLICITADO" to 25000.0, "SI_cd_SI" to 53 },
//     "DATOS_PERSONALES" to { "FECHA_DE_NACIMIENTO" to "1985-06-15", "EDAD" to 38 },
//     "CUSTOM_TABLE_ABC" to { "FIELD_X" to "value", "FIELD_Y" to true }
// }
```

### ViewModel Implementation

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
                val tables = dataTableRepository.getDataTablesForClient(clientId)
                _dataTables.value = tables

                // Initialize values from existing data
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

    /**
     * Update values for a specific table
     */
    fun updateTableValues(tableName: String, values: Map<String, Any>) {
        _state.update { current ->
            current.copy(
                tableValues = current.tableValues + (tableName to values)
            )
        }
    }

    /**
     * Update validation state for a specific table
     */
    fun updateTableValidation(tableName: String, isValid: Boolean) {
        _state.update { current ->
            current.copy(
                tableValidation = current.tableValidation + (tableName to isValid)
            )
        }
    }

    /**
     * Check if all tables are valid
     */
    val isAllValid: StateFlow<Boolean> = _state.map { state ->
        state.tableValidation.values.all { it }
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(), false)

    /**
     * Collect all form data for submission
     */
    fun collectAllFormData(): Map<String, Map<String, Any>> {
        return _state.value.tableValues
    }

    /**
     * Save all data tables
     */
    fun saveAllDataTables(clientId: Long) {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true) }
            try {
                val allData = collectAllFormData()
                allData.forEach { (tableName, values) ->
                    dataTableRepository.saveDataTable(clientId, tableName, values)
                }
                _state.update { it.copy(isLoading = false) }
            } catch (e: Exception) {
                _state.update { it.copy(error = e.message, isLoading = false) }
            }
        }
    }

    private fun extractExistingValues(table: DataTableEntity): Map<String, Any> {
        // Extract existing values from table data if available
        return table.data?.firstOrNull()?.row?.mapIndexed { index, value ->
            val columnName = table.columnHeaderData.getOrNull(index)?.columnName ?: ""
            columnName to (value ?: "")
        }?.toMap() ?: emptyMap()
    }
}
```

### UI Integration Pattern (Data-Driven)

```kotlin
@Composable
fun ClientDataTablesScreen(
    viewModel: ClientDataTablesViewModel,
    clientId: Long
) {
    // dataTables comes from API - could be any number of tables
    val dataTables by viewModel.dataTables.collectAsState()
    val state by viewModel.state.collectAsState()
    val isAllValid by viewModel.isAllValid.collectAsState()

    LaunchedEffect(clientId) {
        viewModel.loadDataTables(clientId)
    }

    Scaffold(
        topBar = {
            TopAppBar(title = { Text("Client Details") })
        },
        bottomBar = {
            Surface(
                tonalElevation = 3.dp,
                modifier = Modifier.fillMaxWidth()
            ) {
                Button(
                    onClick = { viewModel.saveAllDataTables(clientId) },
                    enabled = isAllValid && !state.isLoading,
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp)
                ) {
                    if (state.isLoading) {
                        CircularProgressIndicator(
                            modifier = Modifier.size(20.dp),
                            strokeWidth = 2.dp
                        )
                    } else {
                        Text("Save All Data")
                    }
                }
            }
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // Client info header
            item {
                ClientInfoCard(client = viewModel.client)
            }

            // DYNAMIC: Renders N forms based on dataTables.size from API
            // Each form renders M fields based on dataTable.columnHeaderData
            items(dataTables, key = { it.registeredTableName ?: it.hashCode() }) { dataTable ->
                val tableName = dataTable.registeredTableName ?: ""

                // Each DynamicDataTableForm renders fields dynamically
                // based on columnHeaderData from API
                DynamicDataTableForm(
                    dataTable = dataTable,  // Schema from API
                    values = state.tableValues[tableName] ?: emptyMap(),
                    onValuesChange = { values ->
                        viewModel.updateTableValues(tableName, values)
                    },
                    onValidationChange = { isValid ->
                        viewModel.updateTableValidation(tableName, isValid)
                    },
                    showHeader = true,
                    columns = 2,
                    modifier = Modifier.fillMaxWidth()
                )
            }
        }
    }
}
```

### Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│  Fineract API                                                            │
│  GET /datatables?apptable=m_client&clientId=123                          │
└───────────────────────────────────┬──────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│  Response: List<DataTableEntity>                                         │
│  [                                                                       │
│    { registeredTableName: "TABLE_A", columnHeaderData: [...] },          │
│    { registeredTableName: "TABLE_B", columnHeaderData: [...] },          │
│    { registeredTableName: "TABLE_C", columnHeaderData: [...] },          │
│    ... (any number of tables)                                            │
│  ]                                                                       │
└───────────────────────────────────┬──────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│  ViewModel                                                               │
│  - Stores dataTables: List<DataTableEntity>                              │
│  - Stores tableValues: Map<String, Map<String, Any>>                     │
│  - All keys are dynamic (from API)                                       │
└───────────────────────────────────┬──────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│  UI: LazyColumn                                                          │
│  items(dataTables) { dataTable ->                                        │
│      DynamicDataTableForm(dataTable)  // Renders fields dynamically      │
│  }                                                                       │
│  - Number of forms = dataTables.size (dynamic)                           │
│  - Fields per form = dataTable.columnHeaderData.size (dynamic)           │
└──────────────────────────────────────────────────────────────────────────┘
```

### Helper Component: DynamicDataTableList

For convenience, a wrapper component can render multiple data tables:

```kotlin
/**
 * Renders a list of data tables as form sections.
 * State is managed externally via callbacks.
 */
@Composable
fun DynamicDataTableList(
    dataTables: List<DataTableEntity>,
    allValues: Map<String, Map<String, Any>>,
    onValuesChange: (tableName: String, values: Map<String, Any>) -> Unit,
    onValidationChange: ((tableName: String, isValid: Boolean) -> Unit)? = null,
    readOnly: Boolean = false,
    columns: Int = 2,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier,
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
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
}
```

### Usage with DynamicDataTableList

```kotlin
@Composable
fun ClientDataTablesContent(
    viewModel: ClientDataTablesViewModel
) {
    val dataTables by viewModel.dataTables.collectAsState()
    val state by viewModel.state.collectAsState()

    Column {
        // Some header content
        Text("Complete all sections below")

        // Data tables in the middle
        DynamicDataTableList(
            dataTables = dataTables,
            allValues = state.tableValues,
            onValuesChange = { tableName, values ->
                viewModel.updateTableValues(tableName, values)
            },
            onValidationChange = { tableName, isValid ->
                viewModel.updateTableValidation(tableName, isValid)
            },
            columns = 2
        )

        // Footer content
        Text("All data will be saved together")
    }
}
```

### Fineract DataTable Schema Examples

Below are real Fineract DataTable JSON schemas that this component handles:

#### 1. CONDICION (Loan Conditions)
```json
{
  "registeredTableName": "CONDICION",
  "columnHeaderData": [
    {"columnName": "id", "columnDisplayType": "INTEGER", "isColumnPrimaryKey": true},
    {"columnName": "loan_id", "columnDisplayType": "INTEGER"},
    {"columnName": "MONTO_SOLICITADO", "columnDisplayType": "DECIMAL"},
    {"columnName": "SI_cd_SI", "columnDisplayType": "CODELOOKUP",
     "columnValues": [{"id": 53, "value": "SI"}, {"id": 54, "value": "NO"}]},
    {"columnName": "LUGAR", "columnDisplayType": "TEXT"}
  ]
}
```

#### 2. DATOS_DE_LA_PERSONA_SOLICITANTE (Applicant Data)
```json
{
  "registeredTableName": "DATOS_DE_LA_PERSONA_SOLICITANTE",
  "columnHeaderData": [
    {"columnName": "FECHA_DE_NACIMIENTO", "columnDisplayType": "DATE"},
    {"columnName": "STATE_cd_STATE", "columnDisplayType": "CODELOOKUP"},
    {"columnName": "MUNICIPIO", "columnDisplayType": "STRING"},
    {"columnName": "TIPO_DE_IDENTIFICACION", "columnDisplayType": "STRING"},
    {"columnName": "MARITAL STATUS_cd_MARITAL STATUS", "columnDisplayType": "CODELOOKUP"},
    {"columnName": "SEXO_cd_SEXO", "columnDisplayType": "CODELOOKUP"},
    {"columnName": "EDAD", "columnDisplayType": "INTEGER"},
    {"columnName": "NUMERO_DE_DEPENDIENTES", "columnDisplayType": "INTEGER"}
  ]
}
```

#### 3. DOMICILIO_PARTICULAR (Home Address)
```json
{
  "registeredTableName": "DOMICILIO_PARTICULAR",
  "columnHeaderData": [
    {"columnName": "CALLE", "columnDisplayType": "STRING"},
    {"columnName": "NUMERO_EXTERIOR", "columnDisplayType": "STRING"},
    {"columnName": "NUMERO_INTERIOR", "columnDisplayType": "STRING"},
    {"columnName": "COLONIA", "columnDisplayType": "STRING"},
    {"columnName": "CODIGO_POSTAL", "columnDisplayType": "STRING"},
    {"columnName": "MUNICIPIO", "columnDisplayType": "STRING"},
    {"columnName": "CIUDAD", "columnDisplayType": "STRING"},
    {"columnName": "STATE_cd_STATE", "columnDisplayType": "CODELOOKUP"},
    {"columnName": "TIEMPO_DE_RESIDENCIA", "columnDisplayType": "INTEGER"},
    {"columnName": "TIPO_DE_VIVIENDA_cd_TIPO_DE_VIVIENDA", "columnDisplayType": "CODELOOKUP"}
  ]
}
```

#### 4. DOMICILIO_NEGOCIO (Business Address)
```json
{
  "registeredTableName": "DOMICILIO_NEGOCIO",
  "columnHeaderData": [
    {"columnName": "CALLE", "columnDisplayType": "STRING"},
    {"columnName": "NUMERO_EXTERIOR", "columnDisplayType": "STRING"},
    {"columnName": "NUMERO_INTERIOR", "columnDisplayType": "STRING"},
    {"columnName": "COLONIA", "columnDisplayType": "STRING"},
    {"columnName": "CODIGO_POSTAL", "columnDisplayType": "STRING"},
    {"columnName": "MUNICIPIO", "columnDisplayType": "STRING"},
    {"columnName": "CIUDAD", "columnDisplayType": "STRING"},
    {"columnName": "STATE_cd_STATE", "columnDisplayType": "CODELOOKUP"},
    {"columnName": "TELEFONO_DEL_NEGOCIO", "columnDisplayType": "STRING"}
  ]
}
```

#### 5. INFORMACION_DEL_NEGOCIO_O_ACTIVIDAD_PRODUCTIVA (Business Info)
```json
{
  "registeredTableName": "INFORMACION_DEL_NEGOCIO_O_ACTIVIDAD_PRODUCTIVA",
  "columnHeaderData": [
    {"columnName": "GIRO_DEL_NEGOCIO_cd_GIRO_DEL_NEGOCIO", "columnDisplayType": "CODELOOKUP"},
    {"columnName": "ANTIGUEDAD_DEL_NEGOCIO", "columnDisplayType": "INTEGER"},
    {"columnName": "NUMERO_DE_EMPLEADOS", "columnDisplayType": "INTEGER"},
    {"columnName": "VENTAS_SEMANALES", "columnDisplayType": "DECIMAL"},
    {"columnName": "COSTO_DE_VENTAS_SEMANAL", "columnDisplayType": "DECIMAL"},
    {"columnName": "GASTOS_FIJOS_SEMANALES", "columnDisplayType": "DECIMAL"},
    {"columnName": "DESCRIPCION_DE_ACTIVIDAD", "columnDisplayType": "TEXT"}
  ]
}
```

#### 6. CREDITO_INSTITUCIO_FINANCIERA (Financial Credit)
```json
{
  "registeredTableName": "CREDITO_INSTITUCIO_FINANCIERA",
  "columnHeaderData": [
    {"columnName": "NOMBRE_DE_LA_INSTITUCION", "columnDisplayType": "STRING"},
    {"columnName": "MONTO_OTORGADO", "columnDisplayType": "DECIMAL"},
    {"columnName": "SALDO_ACTUAL", "columnDisplayType": "DECIMAL"},
    {"columnName": "PAGO_SEMANAL", "columnDisplayType": "DECIMAL"},
    {"columnName": "DESTINO_DEL_CREDITO_cd_DESTINO_DEL_CREDITO", "columnDisplayType": "CODELOOKUP"},
    {"columnName": "FECHA_DE_VENCIMIENTO", "columnDisplayType": "DATE"}
  ]
}
```

### Column Naming Convention

Fineract uses a specific naming pattern for CODELOOKUP fields:
- Pattern: `{FIELD_NAME}_cd_{CODE_NAME}`
- Example: `SEXO_cd_SEXO`, `STATE_cd_STATE`, `MARITAL STATUS_cd_MARITAL STATUS`

The `displayName` extension handles this:
```kotlin
val ColumnHeader.displayName: String
    get() = columnName
        ?.substringBefore("_cd_")  // Remove code suffix
        ?.replace("_", " ")
        ?.split(" ")
        ?.joinToString(" ") { it.replaceFirstChar { c -> c.uppercase() } }
        ?: "Field"
```

---

## Files to Create (Updated)

| # | File | Purpose |
|:-:|------|---------|
| 1 | `components/DynamicDataTableForm.kt` | Main building block composable |
| 2 | `components/DynamicDataTableList.kt` | Multi-table wrapper component |
| 3 | `components/DynamicField.kt` | Field type router |
| 4 | `components/DataTableHeader.kt` | Optional header card |
| 5 | `components/fields/BooleanField.kt` | Switch for BOOLEAN |
| 6 | `components/fields/IntegerField.kt` | Number input for INTEGER |
| 7 | `components/fields/DecimalField.kt` | Decimal input for DECIMAL |
| 8 | `components/fields/StringField.kt` | Text input for STRING |
| 9 | `components/fields/MultilineTextField.kt` | Multiline for TEXT |
| 10 | `components/fields/DateField.kt` | Date picker for DATE |
| 11 | `components/fields/DateTimeField.kt` | DateTime picker for DATETIME |
| 12 | `components/fields/DropdownField.kt` | Dropdown for CODELOOKUP |
| 13 | `util/ColumnHeaderExt.kt` | Extension functions |
| 14 | `state/MultiDataTableState.kt` | State data class |

---

## Related Documents

- [GAP_PLAN_DATA_TABLE_FORM.md](../../plan-layer/GAP_PLAN_DATA_TABLE_FORM.md) - Implementation plan
- [data-table-form-flow.mmd](../user-flows/flows/data-table-form-flow.mmd) - Component flow diagram
