# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mobile-wallet/design-spec-layer/features/pocket/API.md"
# last_modified: "2026-03-20"

# API Spec: Pocket

> Fineract Self-Service Pocket API Integration

---

## API Overview

| Attribute | Value |
|-----------|-------|
| Base URL | `{fineract_url}/fineract-provider/api/v1` |
| Auth | Bearer Token |
| Content-Type | `application/json` |

---

## Endpoints

### GET /self/pockets

Retrieve all accounts linked to the user's pocket.

**Request:**
```http
GET /self/pockets HTTP/1.1
Authorization: Bearer {token}
Fineract-Platform-TenantId: {tenant}
```

**Response (200 OK):**
```json
{
  "savingsAccounts": [
    {
      "id": 1,
      "accountNo": "000000001",
      "productName": "Savings Account",
      "accountBalance": 25000.00,
      "currency": {
        "code": "INR",
        "name": "Indian Rupee",
        "decimalPlaces": 2,
        "displaySymbol": "₹"
      }
    }
  ],
  "loanAccounts": [
    {
      "id": 10,
      "accountNo": "000000010",
      "productName": "Personal Loan",
      "outstandingBalance": 50000.00,
      "currency": {
        "code": "INR",
        "name": "Indian Rupee",
        "decimalPlaces": 2,
        "displaySymbol": "₹"
      }
    }
  ],
  "shareAccounts": []
}
```

**Response (404):**
```json
{
  "errors": [
    {
      "developerMessage": "Pocket does not exist for current user",
      "defaultUserMessage": "No pocket found"
    }
  ]
}
```

---

### POST /self/pockets?command=linkAccounts

Link accounts to the user's pocket.

**Request:**
```http
POST /self/pockets?command=linkAccounts HTTP/1.1
Authorization: Bearer {token}
Fineract-Platform-TenantId: {tenant}
Content-Type: application/json

{
  "savingsAccounts": [123, 456],
  "loanAccounts": [789],
  "shareAccounts": [101]
}
```

**Response (200 OK):**
```json
{
  "pocketId": 1,
  "changes": {
    "savingsAccounts": [123, 456],
    "loanAccounts": [789],
    "shareAccounts": [101]
  }
}
```

**Response (400 Bad Request):**
```json
{
  "errors": [
    {
      "developerMessage": "Account 123 is already linked to pocket",
      "defaultUserMessage": "Some accounts are already linked"
    }
  ]
}
```

---

### POST /self/pockets?command=delinkAccounts

Remove accounts from the user's pocket.

**Request:**
```http
POST /self/pockets?command=delinkAccounts HTTP/1.1
Authorization: Bearer {token}
Fineract-Platform-TenantId: {tenant}
Content-Type: application/json

{
  "savingsAccounts": [123],
  "loanAccounts": [],
  "shareAccounts": []
}
```

**Response (200 OK):**
```json
{
  "pocketId": 1,
  "changes": {
    "savingsAccounts": [123]
  }
}
```

---

## Data Models

### Kotlin Models

```kotlin
// Request/Response models for Pocket API

package org.mifospay.core.network.model.entity.pocket

import kotlinx.serialization.Serializable
import org.mifospay.core.model.savingsaccount.Currency

/**
 * Response from GET /self/pockets
 */
@Serializable
data class PocketAccountsEntity(
    val savingsAccounts: List<PocketSavingsAccount> = emptyList(),
    val loanAccounts: List<PocketLoanAccount> = emptyList(),
    val shareAccounts: List<PocketShareAccount> = emptyList()
)

@Serializable
data class PocketSavingsAccount(
    val id: Long,
    val accountNo: String,
    val productName: String,
    val accountBalance: Double,
    val currency: Currency
)

@Serializable
data class PocketLoanAccount(
    val id: Long,
    val accountNo: String,
    val productName: String,
    val outstandingBalance: Double,
    val currency: Currency
)

@Serializable
data class PocketShareAccount(
    val id: Long,
    val accountNo: String,
    val productName: String,
    val totalShares: Int,
    val currentValue: Double,
    val currency: Currency
)

/**
 * Request body for link/delink operations
 */
@Serializable
data class PocketLinkRequest(
    val savingsAccounts: List<Long> = emptyList(),
    val loanAccounts: List<Long> = emptyList(),
    val shareAccounts: List<Long> = emptyList()
)

/**
 * Response from link/delink operations
 */
@Serializable
data class PocketCommandResponse(
    val pocketId: Long,
    val changes: PocketChanges
)

@Serializable
data class PocketChanges(
    val savingsAccounts: List<Long> = emptyList(),
    val loanAccounts: List<Long> = emptyList(),
    val shareAccounts: List<Long> = emptyList()
)
```

### Domain Models

```kotlin
// Domain models in core:model

package org.mifospay.core.model.pocket

import org.mifospay.core.model.savingsaccount.Currency

/**
 * Unified pocket account model for UI consumption
 */
data class PocketAccount(
    val id: Long,
    val accountNo: String,
    val productName: String,
    val balance: Double,
    val currency: Currency,
    val accountType: PocketAccountType
)

enum class PocketAccountType {
    SAVINGS,
    LOAN,
    SHARE
}

/**
 * Pocket state with all linked accounts
 */
data class Pocket(
    val accounts: List<PocketAccount>,
    val totalBalance: Double,
    val currency: Currency
)
```

---

## API Service Interface

```kotlin
// In core:network

package org.mifospay.core.network.services

import de.jensklingenberg.ktorfit.http.Body
import de.jensklingenberg.ktorfit.http.GET
import de.jensklingenberg.ktorfit.http.POST
import de.jensklingenberg.ktorfit.http.Query
import kotlinx.coroutines.flow.Flow
import org.mifospay.core.network.model.entity.pocket.PocketAccountsEntity
import org.mifospay.core.network.model.entity.pocket.PocketCommandResponse
import org.mifospay.core.network.model.entity.pocket.PocketLinkRequest

interface PocketService {

    @GET("self/pockets")
    fun getPocketAccounts(): Flow<PocketAccountsEntity>

    @POST("self/pockets")
    suspend fun linkAccounts(
        @Query("command") command: String = "linkAccounts",
        @Body request: PocketLinkRequest
    ): PocketCommandResponse

    @POST("self/pockets")
    suspend fun delinkAccounts(
        @Query("command") command: String = "delinkAccounts",
        @Body request: PocketLinkRequest
    ): PocketCommandResponse
}
```

---

## Repository Interface

```kotlin
// In core:data

package org.mifospay.core.data.repository

import kotlinx.coroutines.flow.Flow
import org.mifospay.core.common.DataState
import org.mifospay.core.model.pocket.Pocket
import org.mifospay.core.model.pocket.PocketAccount

interface PocketRepository {

    /**
     * Get all accounts linked to user's pocket
     */
    fun getPocket(): Flow<DataState<Pocket>>

    /**
     * Link accounts to pocket
     * @param savingsIds List of savings account IDs to link
     * @param loanIds List of loan account IDs to link
     * @param shareIds List of share account IDs to link
     */
    suspend fun linkAccounts(
        savingsIds: List<Long> = emptyList(),
        loanIds: List<Long> = emptyList(),
        shareIds: List<Long> = emptyList()
    ): DataState<Unit>

    /**
     * Remove accounts from pocket
     * @param savingsIds List of savings account IDs to remove
     * @param loanIds List of loan account IDs to remove
     * @param shareIds List of share account IDs to remove
     */
    suspend fun delinkAccounts(
        savingsIds: List<Long> = emptyList(),
        loanIds: List<Long> = emptyList(),
        shareIds: List<Long> = emptyList()
    ): DataState<Unit>
}
```

---

## Error Handling

| HTTP Status | Error Code | Description | UI Action |
|-------------|------------|-------------|-----------|
| 401 | `UNAUTHORIZED` | Token expired | Navigate to login |
| 403 | `FORBIDDEN` | No permission | Show error message |
| 404 | `POCKET_NOT_FOUND` | No pocket exists | Show empty state |
| 400 | `ALREADY_LINKED` | Account already in pocket | Show info toast |
| 400 | `NOT_LINKED` | Account not in pocket | Refresh list |
| 500 | `SERVER_ERROR` | Server error | Show retry option |

---

## Caching Strategy

| Data | Cache Duration | Strategy |
|------|----------------|----------|
| Pocket accounts | 5 minutes | Memory cache with stale-while-revalidate |
| Account balances | No cache | Always fetch fresh |

---

## Rate Limiting

| Endpoint | Limit |
|----------|-------|
| GET /self/pockets | 60/min |
| POST link/delink | 30/min |

---

## Testing

### Mock Data

```json
// mock_pocket_accounts.json
{
  "savingsAccounts": [
    {
      "id": 1,
      "accountNo": "MW0000001",
      "productName": "Savings Account",
      "accountBalance": 25000.00,
      "currency": {
        "code": "INR",
        "name": "Indian Rupee",
        "decimalPlaces": 2,
        "displaySymbol": "₹"
      }
    }
  ],
  "loanAccounts": [],
  "shareAccounts": []
}
```

### Test Scenarios

| Scenario | Expected |
|----------|----------|
| Empty pocket | Return empty lists |
| Single account | Return account in correct type list |
| Mixed accounts | Return accounts grouped by type |
| Link success | Return pocketId and changes |
| Link duplicate | Return 400 error |
| Delink success | Return pocketId and changes |
| Network error | Return error state |

---

## Related

- **Swagger:** https://sandbox.mifos.community/fineract-provider/swagger-ui/index.html#/Pocket
- **API Docs:** https://demo.mifos.io/api-docs/apiLive.htm#linkaccountstopocket
- **Feature Spec:** `SPEC.md`
