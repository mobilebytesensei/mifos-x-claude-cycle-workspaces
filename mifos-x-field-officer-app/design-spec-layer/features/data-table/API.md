# template_meta
# template_version: "2.86.5"
# template_path: "workspaces/mifos-x/mifos-x-field-officer-app/design-spec-layer/features/data-table/API.md"
# last_modified: "2026-03-20"

# Data Table API Documentation

> **Auto-generated from SPEC.md analysis**
> **Generated:** 2026-03-08

---

## Overview

| Attribute | Value |
|-----------|-------|
| Feature | data-table |
| Backend | fineract |
| Endpoints | 8 |
| Purpose | Dynamic form generation from Fineract DataTable schemas |

---

## Endpoints

### Data Table Schema

#### GET /datatables
**Purpose:** List all available data tables

**Query Parameters:**
| Param | Type | Required | Description |
|-------|------|:--------:|-------------|
| apptable | string | No | Filter by application table (m_client, m_loan, m_group, m_savings_account) |

**Response:** `List<DataTableEntity>`

---

#### GET /datatables/{tableName}
**Purpose:** Get data table schema (column definitions)

**Path Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| tableName | string | Registered table name (e.g., "CONDICION", "DATOS_DE_LA_PERSONA_SOLICITANTE") |

**Response:**
```json
{
  "applicationTableName": "m_client",
  "registeredTableName": "CONDICION",
  "columnHeaderData": [
    {
      "columnName": "MONTO_SOLICITADO",
      "columnType": "Decimal",
      "columnDisplayType": "DECIMAL",
      "isColumnNullable": true,
      "isColumnPrimaryKey": false
    },
    {
      "columnName": "STATE_cd_STATE",
      "columnType": "Integer",
      "columnDisplayType": "CODELOOKUP",
      "columnValues": [
        {"id": 1, "value": "Active"},
        {"id": 2, "value": "Inactive"}
      ]
    }
  ]
}
```

---

### Data Table Data Operations

#### GET /datatables/{tableName}/{entityId}
**Purpose:** Get data table entries for a specific entity

**Path Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| tableName | string | Registered table name |
| entityId | long | Entity ID (clientId, loanId, groupId, etc.) |

**Query Parameters:**
| Param | Type | Required | Description |
|-------|------|:--------:|-------------|
| order | string | No | Sort order (id ASC, id DESC) |

**Response:** `List<Map<String, Any>>`

---

#### POST /datatables/{tableName}/{entityId}
**Purpose:** Create new data table entry

**Path Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| tableName | string | Registered table name |
| entityId | long | Entity ID |

**Request Body:**
```json
{
  "MONTO_SOLICITADO": 25000.00,
  "STATE_cd_STATE": 1,
  "FECHA_DE_NACIMIENTO": "1985-06-15",
  "ACTIVO": true,
  "DESCRIPCION": "Sample description text"
}
```

**Response:**
```json
{
  "resourceId": 123
}
```

---

#### PUT /datatables/{tableName}/{entityId}/{entryId}
**Purpose:** Update existing data table entry

**Path Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| tableName | string | Registered table name |
| entityId | long | Entity ID |
| entryId | long | Data entry ID |

**Request Body:** Same as POST

**Response:**
```json
{
  "resourceId": 123,
  "changes": {
    "MONTO_SOLICITADO": 30000.00
  }
}
```

---

#### DELETE /datatables/{tableName}/{entityId}/{entryId}
**Purpose:** Delete data table entry

**Path Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| tableName | string | Registered table name |
| entityId | long | Entity ID |
| entryId | long | Data entry ID |

**Response:**
```json
{
  "resourceId": 123
}
```

---

### Multi-Table Operations

#### GET /clients/{clientId}/datatables
**Purpose:** Get all data tables associated with a client (with data)

**Path Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| clientId | long | Client ID |

**Response:** `List<DataTableEntity>` (includes schema + data)

---

#### GET /loans/{loanId}/datatables
**Purpose:** Get all data tables associated with a loan (with data)

**Path Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| loanId | long | Loan ID |

**Response:** `List<DataTableEntity>` (includes schema + data)

---

## Column Display Types

| Type | Description | UI Component |
|------|-------------|--------------|
| `BOOLEAN` | True/False value | Switch |
| `INTEGER` | Whole number | Number TextField |
| `DECIMAL` | Decimal number | Decimal TextField |
| `STRING` | Short text (≤255 chars) | TextField |
| `TEXT` | Long text | Multiline TextField |
| `DATE` | Date only | DatePicker |
| `DATETIME` | Date and time | DateTimePicker |
| `CODELOOKUP` | Dropdown from code values | ExposedDropdownMenu |

---

## Application Tables

| apptable | Entity | Description |
|----------|--------|-------------|
| m_client | Client | Client-attached data tables |
| m_loan | Loan | Loan-attached data tables |
| m_group | Group | Group-attached data tables |
| m_savings_account | Savings | Savings account-attached data tables |
| m_center | Center | Center-attached data tables |

---

## Usage in App

The data-table feature is a **building block component** used across multiple screens:

| Screen | Usage |
|--------|-------|
| ClientDetailsScreen | Display/edit client data tables |
| LoanApplicationScreen | Collect loan-related data |
| GroupDetailsScreen | Display/edit group data tables |
| SavingsAccountScreen | Display/edit savings data tables |

---

**Generated by:** /project-verify (FIX-CONTENT-002)
