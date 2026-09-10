# template_meta
# template_version: "2.86.0"
# template_path: "templates/blueprints/workspace-project/server-layer/CLIENT_PATTERNS.md"
# last_modified: "2026-03-19"

# Client Layer Patterns - ${PROJECT_NAME}

> **Purpose**: Service and Repository implementation patterns for API integration.
> **Auto-generated**: ${DATE} by /project-verify

---

## Overview

This document defines the patterns for implementing API clients in the client layer.

```
┌─────────────────────────────────────────────────────────────────┐
│  Server Layer: API_INDEX.md, endpoints/*.md                     │
│  └─→ Defines: Endpoints, Request/Response JSON, DTOs           │
├─────────────────────────────────────────────────────────────────┤
│  Client Layer: (Implementation)                                 │
│  ├─→ services/*.kt - API service interfaces                    │
│  ├─→ repository/*.kt - Repository implementations              │
│  └─→ models/*.kt - Data classes (DTOs)                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Service Interface Pattern

### KMP (Ktor)

```kotlin
interface ${SERVICE_NAME}Service {
    /**
     * ${ENDPOINT_PURPOSE}
     * @see endpoints/${CATEGORY}.md
     */
    @${METHOD}("${PATH}")
    suspend fun ${METHOD_NAME}(
        ${IF_HAS_PATH_PARAM}@Path("${PARAM}") ${PARAM}: ${TYPE},${END_IF}
        ${IF_HAS_QUERY_PARAM}@Query("${PARAM}") ${PARAM}: ${TYPE},${END_IF}
        ${IF_HAS_BODY}@Body request: ${REQUEST_TYPE}${END_IF}
    ): ${RESPONSE_TYPE}
}
```

### Example: AuthenticationService

```kotlin
interface AuthenticationService {
    /**
     * Authenticate user with username and password
     * @see endpoints/AUTH.md
     */
    @POST("authentication")
    suspend fun authenticate(
        @Body request: LoginRequest
    ): User

    /**
     * Register new client
     * @see endpoints/AUTH.md
     */
    @POST("registration")
    suspend fun register(
        @Body request: RegisterPayload
    ): RegistrationResponse
}
```

---

## Repository Pattern

### Base Pattern

```kotlin
class ${REPOSITORY_NAME}Repository(
    private val service: ${SERVICE_NAME}Service
) {
    /**
     * ${METHOD_PURPOSE}
     * Wraps service call with error handling
     */
    suspend fun ${METHOD_NAME}(${PARAMS}): Result<${TYPE}> {
        return runCatching {
            service.${METHOD_NAME}(${ARGS})
        }
    }
}
```

### Example: AuthRepository

```kotlin
class AuthRepository(
    private val authService: AuthenticationService
) {
    suspend fun login(username: String, password: String): Result<User> {
        return runCatching {
            authService.authenticate(LoginRequest(username, password))
        }
    }

    suspend fun register(payload: RegisterPayload): Result<RegistrationResponse> {
        return runCatching {
            authService.register(payload)
        }
    }
}
```

---

## DTO Patterns

### Request DTO

```kotlin
@Serializable
data class ${REQUEST_NAME}(
    ${FOR_EACH_FIELD}
    val ${FIELD_NAME}: ${FIELD_TYPE}${IF_NULLABLE}? = null${END_IF},
    ${END_FOR_EACH}
)
```

### Response DTO

```kotlin
@Serializable
data class ${RESPONSE_NAME}(
    ${FOR_EACH_FIELD}
    val ${FIELD_NAME}: ${FIELD_TYPE}${IF_NULLABLE}?${END_IF},
    ${END_FOR_EACH}
)
```

### Example: User DTO

```kotlin
@Serializable
data class User(
    val userId: Long,
    val username: String?,
    val clients: List<Long>,
    val isAuthenticated: Boolean,
    val base64EncodedAuthenticationKey: String?,
    val officeName: String?,
)
```

---

## Error Handling Pattern

### Result Wrapper

```kotlin
sealed class ApiResult<out T> {
    data class Success<T>(val data: T) : ApiResult<T>()
    data class Error(val code: Int, val message: String) : ApiResult<Nothing>()
    data object Loading : ApiResult<Nothing>()
}
```

### Usage in Repository

```kotlin
suspend fun <T> safeApiCall(
    apiCall: suspend () -> T
): ApiResult<T> {
    return try {
        ApiResult.Success(apiCall())
    } catch (e: HttpException) {
        ApiResult.Error(e.code(), e.message())
    } catch (e: Exception) {
        ApiResult.Error(-1, e.localizedMessage ?: "Unknown error")
    }
}
```

---

## Service Method Naming Conventions

| HTTP Method | Naming Pattern | Example |
|-------------|----------------|---------|
| GET (list) | `get${Resource}s()` | `getClients()` |
| GET (single) | `get${Resource}()` | `getClient(id)` |
| GET (detail) | `get${Resource}Details()` | `getClientDetails(id)` |
| POST (create) | `create${Resource}()` | `createClient(payload)` |
| POST (action) | `${action}${Resource}()` | `authenticate(credentials)` |
| PUT | `update${Resource}()` | `updateClient(id, payload)` |
| DELETE | `delete${Resource}()` | `deleteClient(id)` |

---

## File Structure

```
client-layer/
├── services/
│   ├── AuthenticationService.kt
│   ├── ClientService.kt
│   └── ${FEATURE}Service.kt
├── repository/
│   ├── AuthRepository.kt
│   ├── ClientRepository.kt
│   └── ${FEATURE}Repository.kt
└── models/
    ├── User.kt
    ├── Client.kt
    └── ${DTO}.kt
```

---

## Related Files

| File | Purpose |
|------|---------|
| `API_INDEX.md` | Endpoint quick lookup |
| `endpoints/*.md` | Detailed endpoint docs |
| `ERROR_HANDLING.md` | Error handling patterns |

---

**Generated by**: /project-verify (FIX-SERVER-CLIENT_PATTERNS)
