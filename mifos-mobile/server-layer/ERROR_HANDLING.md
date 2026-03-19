# template_meta
# template_version: "2.81.0"
# template_path: "templates/blueprints/workspace-project/server-layer/ERROR_HANDLING.md"
# last_modified: "2026-03-19"

# Error Handling - ${PROJECT_NAME}

> **Purpose**: Exception handling conventions for API integration.
> **Auto-generated**: ${DATE} by /project-verify

---

## Overview

This document defines error handling patterns for the ${BACKEND_PROVIDER} backend.

---

## HTTP Status Codes

| Status | Description | Handling |
|:------:|-------------|----------|
| 200 | Success | Process response |
| 201 | Created | Process created resource |
| 400 | Bad Request | Show validation errors |
| 401 | Unauthorized | Redirect to login |
| 403 | Forbidden | Show permission error |
| 404 | Not Found | Show "not found" message |
| 409 | Conflict | Show conflict resolution |
| 422 | Unprocessable | Show validation errors |
| 500 | Server Error | Show retry option |
| 503 | Service Unavailable | Show maintenance message |

---

## Error Response Format

### Standard Error Response

```json
{
    "developerMessage": "Detailed error for debugging",
    "httpStatusCode": "401",
    "defaultUserMessage": "User-friendly error message",
    "userMessageGlobalisationCode": "error.msg.authentication.failed",
    "errors": [
        {
            "developerMessage": "Field-specific error",
            "defaultUserMessage": "Username is required",
            "userMessageGlobalisationCode": "error.msg.username.required",
            "parameterName": "username"
        }
    ]
}
```

### Parsing Error Response

```kotlin
@Serializable
data class ApiError(
    val developerMessage: String?,
    val httpStatusCode: String?,
    val defaultUserMessage: String?,
    val userMessageGlobalisationCode: String?,
    val errors: List<FieldError>?
)

@Serializable
data class FieldError(
    val developerMessage: String?,
    val defaultUserMessage: String?,
    val userMessageGlobalisationCode: String?,
    val parameterName: String?
)
```

---

## Exception Types

### Network Exceptions

```kotlin
sealed class NetworkException : Exception() {
    data object NoConnection : NetworkException()
    data object Timeout : NetworkException()
    data class ServerError(val code: Int, val message: String) : NetworkException()
}
```

### API Exceptions

```kotlin
sealed class ApiException : Exception() {
    data class Unauthorized(val message: String) : ApiException()
    data class Forbidden(val message: String) : ApiException()
    data class NotFound(val resource: String) : ApiException()
    data class ValidationError(val errors: List<FieldError>) : ApiException()
    data class ServerError(val message: String) : ApiException()
}
```

---

## Error Handling in Repository

```kotlin
suspend fun <T> safeApiCall(
    apiCall: suspend () -> T
): Result<T> {
    return try {
        Result.success(apiCall())
    } catch (e: HttpException) {
        val error = parseErrorResponse(e.response()?.errorBody())
        Result.failure(mapToApiException(e.code(), error))
    } catch (e: IOException) {
        Result.failure(NetworkException.NoConnection)
    } catch (e: SocketTimeoutException) {
        Result.failure(NetworkException.Timeout)
    }
}

private fun mapToApiException(code: Int, error: ApiError?): ApiException {
    return when (code) {
        401 -> ApiException.Unauthorized(error?.defaultUserMessage ?: "Unauthorized")
        403 -> ApiException.Forbidden(error?.defaultUserMessage ?: "Forbidden")
        404 -> ApiException.NotFound(error?.defaultUserMessage ?: "Not found")
        422 -> ApiException.ValidationError(error?.errors ?: emptyList())
        else -> ApiException.ServerError(error?.defaultUserMessage ?: "Server error")
    }
}
```

---

## Error Handling in ViewModel

```kotlin
class ${FEATURE}ViewModel : ViewModel() {
    private val _uiState = MutableStateFlow<UiState>(UiState.Idle)
    val uiState = _uiState.asStateFlow()

    fun loadData() {
        viewModelScope.launch {
            _uiState.value = UiState.Loading

            repository.getData()
                .onSuccess { data ->
                    _uiState.value = UiState.Success(data)
                }
                .onFailure { error ->
                    _uiState.value = when (error) {
                        is ApiException.Unauthorized -> UiState.Error.Unauthorized
                        is ApiException.NotFound -> UiState.Error.NotFound
                        is NetworkException.NoConnection -> UiState.Error.NoConnection
                        else -> UiState.Error.Generic(error.message)
                    }
                }
        }
    }
}
```

---

## UI Error Display

### Error UI State

```kotlin
sealed interface UiState {
    data object Idle : UiState
    data object Loading : UiState
    data class Success<T>(val data: T) : UiState

    sealed interface Error : UiState {
        data object Unauthorized : Error
        data object NotFound : Error
        data object NoConnection : Error
        data class Generic(val message: String?) : Error
    }
}
```

### Error Messages

| Error Type | User Message | Action |
|------------|--------------|--------|
| Unauthorized | "Session expired. Please login again." | Navigate to login |
| Forbidden | "You don't have permission for this action." | Show info dialog |
| NotFound | "The requested item was not found." | Navigate back |
| NoConnection | "No internet connection. Please check your network." | Show retry |
| Generic | "Something went wrong. Please try again." | Show retry |

---

## Retry Pattern

```kotlin
suspend fun <T> withRetry(
    times: Int = 3,
    initialDelay: Long = 100,
    factor: Double = 2.0,
    block: suspend () -> T
): T {
    var currentDelay = initialDelay
    repeat(times - 1) {
        try {
            return block()
        } catch (e: Exception) {
            if (e is ApiException.Unauthorized) throw e // Don't retry auth errors
        }
        delay(currentDelay)
        currentDelay = (currentDelay * factor).toLong()
    }
    return block() // Last attempt
}
```

---

## Backend-Specific Errors

### ${BACKEND_PROVIDER} Errors

| Error Code | Meaning | Handling |
|------------|---------|----------|
| `error.msg.authentication.failed` | Invalid credentials | Show login error |
| `error.msg.client.not.found` | Client doesn't exist | Show not found |
| `error.msg.insufficient.balance` | Not enough funds | Show balance error |

---

## Related Files

| File | Purpose |
|------|---------|
| `API_INDEX.md` | Endpoint documentation |
| `CLIENT_PATTERNS.md` | Service/Repository patterns |
| `endpoints/*.md` | Per-endpoint error details |

---

**Generated by**: /project-verify (FIX-SERVER-ERROR_HANDLING)
