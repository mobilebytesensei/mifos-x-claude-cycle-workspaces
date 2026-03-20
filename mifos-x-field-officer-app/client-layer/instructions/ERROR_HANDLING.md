# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mifos-x-field-officer-app/client-layer/instructions/ERROR_HANDLING.md"
# last_modified: "2026-03-20"

# Error Handling Reference

> **Purpose**: Type-safe error pipeline from HTTP response to UI display
> **Derived from**: KMP template project (`core-base/network`, `core/data`)
> **Used by**: Client layer services, repositories, and ViewModels

---

## Table of Contents
1. [Pipeline Overview](#pipeline-overview)
2. [NetworkError Enum](#networkerror-enum)
3. [NetworkResult Sealed Interface](#networkresult-sealed-interface)
4. [ResultSuspendConverterFactory](#resultsuspendconverterfactory)
5. [RemoteException Wrapper](#remoteexception-wrapper)
6. [NetworkError.toThrowable() Messages](#networkerrortothrowable-messages)
7. [toDataState() Conversions](#todatastate-conversions)
8. [NetworkResult-to-DataState Bridge (Complete Reference)](#networkresult-to-datastate-bridge-complete-reference)
9. [Supabase Exception Mapping](#supabase-exception-mapping)
10. [ViewModel Error Handling](#viewmodel-error-handling)
11. [DataState Utility Extensions](#datastate-utility-extensions)
12. [Testing Error Handling](#testing-error-handling)

---

## Pipeline Overview

The KMP template project handles errors through a type-safe sealed pipeline. Raw exceptions never propagate past the service boundary. Every HTTP failure is classified into a `NetworkError` enum value, wrapped into a `RemoteException` with a user-friendly message, and delivered to the UI as a `DataState.Error` or `DataState.NoNetwork`.

```
HTTP Response
    |
    v  ResultSuspendConverterFactory (Ktorfit) or try-catch (Supabase)
NetworkResult.Error(NetworkError)          <-- 8 typed error values
    |
    v  NetworkError.toThrowable()
RemoteException(networkError, userMessage) <-- user-friendly message attached
    |
    v  Repository toDataState() or toDataStateWithMapping()
DataState.Error(throwable, existingData?)  <-- generic errors
DataState.NoNetwork(existingData?)         <-- timeout/connectivity errors
    |
    v  ViewModel StateFlow
Compose UI                                 <-- displays error or offline state
```

### Key Principles

- **No try-catch in repositories.** The `ResultSuspendConverterFactory` converts HTTP errors automatically for Ktorfit APIs. Supabase services use a local try-catch that produces `NetworkResult.Error`, never raw exceptions.
- **No manual status code matching in repositories.** Status codes are classified once in the converter factory (Ktorfit) or service (Supabase), then flow as typed `NetworkError` values.
- **User-friendly messages are defined once.** The `NetworkError.toThrowable()` extension maps each error to a `RemoteException` with a consistent user-facing message.

---

## NetworkError Enum

Located in `core-base/network/src/commonMain/kotlin/.../NetworkError.kt`.

This enum classifies every network failure into one of 8 categories:

```kotlin
enum class NetworkError {
    BAD_REQUEST,       // HTTP 400
    NOT_FOUND,         // HTTP 404
    UNAUTHORIZED,      // HTTP 401
    REQUEST_TIMEOUT,   // HTTP 408 or socket timeout
    TOO_MANY_REQUESTS, // HTTP 429
    SERVER,            // HTTP 5xx
    SERIALIZATION,     // JSON deserialization failures
    UNKNOWN,           // Fallback for unclassified errors
}
```

### HTTP Status Code Mapping

| NetworkError | HTTP Status | When Triggered |
|---|:---:|---|
| `BAD_REQUEST` | 400 | Malformed request or missing required parameters |
| `UNAUTHORIZED` | 401 | Invalid or expired authentication token |
| `NOT_FOUND` | 404 | Requested resource does not exist |
| `REQUEST_TIMEOUT` | 408 / socket timeout | Slow or unresponsive network |
| `TOO_MANY_REQUESTS` | 429 | Rate limit exceeded |
| `SERVER` | 500-599 | Server-side failure |
| `SERIALIZATION` | N/A | `SerializationException` or `NoTransformationFoundException` during body parsing |
| `UNKNOWN` | Any other | Fallback for `KtorfitResult.Failure` or unrecognized status codes |

---

## NetworkResult Sealed Interface

Located in `core-base/network/src/commonMain/kotlin/.../NetworkResult.kt`.

This is the network boundary type. Services return `NetworkResult`, repositories consume it.

```kotlin
sealed interface NetworkResult<out D, out E : NetworkError> {
    data class Success<out D>(val data: D) : NetworkResult<D, Nothing>
    data class Error<out E : NetworkError>(val error: E) : NetworkResult<Nothing, E>
}
```

### Usage in Service Interfaces (Ktorfit)

```kotlin
interface MovieApi {
    @GET("movies/{id}")
    suspend fun getMovie(@Path("id") id: Int): NetworkResult<MovieDto, NetworkError>

    @GET("movies")
    suspend fun getMovies(): NetworkResult<List<MovieDto>, NetworkError>
}
```

### Usage in Service Interfaces (Supabase)

```kotlin
interface MovieService {
    suspend fun getMovie(id: Int): NetworkResult<MovieDto, NetworkError>
    suspend fun getMovies(): NetworkResult<List<MovieDto>, NetworkError>
}
```

---

## ResultSuspendConverterFactory

Located in `core-base/network/src/commonMain/kotlin/.../factory/ResultSuspendConverterFactory.kt`.

This Ktorfit converter factory automatically intercepts every HTTP response and produces a `NetworkResult`. It is registered once during Ktorfit setup and applies to all API methods that return `NetworkResult`.

```kotlin
class ResultSuspendConverterFactory : Converter.Factory {

    override fun suspendResponseConverter(
        typeData: TypeData,
        ktorfit: Ktorfit,
    ): Converter.SuspendResponseConverter<HttpResponse, *>? {
        if (typeData.typeInfo.type == NetworkResult::class) {
            val successType = typeData.typeArgs.first().typeInfo
            return object :
                Converter.SuspendResponseConverter<HttpResponse, NetworkResult<Any, NetworkError>> {

                override suspend fun convert(
                    result: KtorfitResult,
                ): NetworkResult<Any, NetworkError> {
                    return when (result) {
                        is KtorfitResult.Failure -> {
                            NetworkResult.Error(NetworkError.UNKNOWN)
                        }

                        is KtorfitResult.Success -> {
                            val status = result.response.status.value

                            when (status) {
                                in 200..209 -> {
                                    try {
                                        val data = result.response.body(successType) as Any
                                        NetworkResult.Success(data)
                                    } catch (e: NoTransformationFoundException) {
                                        NetworkResult.Error(NetworkError.SERIALIZATION)
                                    } catch (e: SerializationException) {
                                        NetworkResult.Error(NetworkError.SERIALIZATION)
                                    }
                                }

                                400 -> NetworkResult.Error(NetworkError.BAD_REQUEST)
                                401 -> NetworkResult.Error(NetworkError.UNAUTHORIZED)
                                404 -> NetworkResult.Error(NetworkError.NOT_FOUND)
                                408 -> NetworkResult.Error(NetworkError.REQUEST_TIMEOUT)
                                429 -> NetworkResult.Error(NetworkError.TOO_MANY_REQUESTS)
                                in 500..599 -> NetworkResult.Error(NetworkError.SERVER)
                                else -> NetworkResult.Error(NetworkError.UNKNOWN)
                            }
                        }
                    }
                }
            }
        }
        return null
    }
}
```

### Registering the Factory

```kotlin
val ktorfit = ktorfit {
    baseUrl(BASE_URL)
    httpClient(httpClient)
    converterFactories(ResultSuspendConverterFactory())
}
```

---

## RemoteException Wrapper

Located in `core/data/src/commonMain/kotlin/.../core/data/util/ResultExtensions.kt`.

`RemoteException` wraps a `NetworkError` with a user-friendly message string. It bridges the typed network error into the `Throwable` hierarchy that `DataState.Error` expects.

```kotlin
class RemoteException(
    val networkError: NetworkError,
    message: String = networkError.name,
) : Exception(message)
```

### Why RemoteException Exists

- `DataState.Error` holds a `Throwable`. The `RemoteException` carries both the typed `NetworkError` (for programmatic branching) and a display-ready `message` (for the UI).
- ViewModels can check `(error as? RemoteException)?.networkError` when they need to handle specific error types (e.g., redirect to login on `UNAUTHORIZED`).

---

## NetworkError.toThrowable() Messages

Located in `core/data/src/commonMain/kotlin/.../core/data/util/ResultExtensions.kt`.

This extension maps each `NetworkError` to a `RemoteException` with a consistent, user-facing message:

```kotlin
fun NetworkError.toThrowable(): Throwable = when (this) {
    NetworkError.BAD_REQUEST -> RemoteException(
        networkError = this,
        message = "Something went wrong with your request. Please try again.",
    )

    NetworkError.NOT_FOUND -> RemoteException(
        networkError = this,
        message = "The information you're looking for couldn't be found.",
    )

    NetworkError.UNAUTHORIZED -> RemoteException(
        networkError = this,
        message = "You need to sign in to access this content.",
    )

    NetworkError.REQUEST_TIMEOUT -> RemoteException(
        networkError = this,
        message = "The request is taking too long. Please check your connection and try again.",
    )

    NetworkError.TOO_MANY_REQUESTS -> RemoteException(
        networkError = this,
        message = "You're doing that too often. Please wait a moment and try again.",
    )

    NetworkError.SERVER -> RemoteException(
        networkError = this,
        message = "We're experiencing technical difficulties. Please try again later.",
    )

    NetworkError.SERIALIZATION -> RemoteException(
        networkError = this,
        message = "We received unexpected data. Please try refreshing the app.",
    )

    NetworkError.UNKNOWN -> RemoteException(
        networkError = this,
        message = "Something unexpected happened. Please try again.",
    )
}
```

### Quick Reference Table

| NetworkError | User-Friendly Message |
|---|---|
| `BAD_REQUEST` | "Something went wrong with your request. Please try again." |
| `NOT_FOUND` | "The information you're looking for couldn't be found." |
| `UNAUTHORIZED` | "You need to sign in to access this content." |
| `REQUEST_TIMEOUT` | "The request is taking too long. Please check your connection and try again." |
| `TOO_MANY_REQUESTS` | "You're doing that too often. Please wait a moment and try again." |
| `SERVER` | "We're experiencing technical difficulties. Please try again later." |
| `SERIALIZATION` | "We received unexpected data. Please try refreshing the app." |
| `UNKNOWN` | "Something unexpected happened. Please try again." |

---

## toDataState() Conversions

Located in `core/data/src/commonMain/kotlin/.../core/data/util/ResultExtensions.kt`.

These extensions convert `NetworkResult` into `DataState` at the repository boundary. Repositories call one of these -- no manual error mapping required.

### toDataState() -- Simple Conversion

Maps every `NetworkResult.Error` to `DataState.Error`:

```kotlin
fun <D> NetworkResult<D, *>.toDataState(): DataState<D> = when (this) {
    is NetworkResult.Success -> DataState.Success(data)
    is NetworkResult.Error -> DataState.Error(error.toThrowable(), null)
}
```

With existing data preserved on error:

```kotlin
fun <D> NetworkResult<D, *>.toDataState(existingData: D?): DataState<D> =
    when (this) {
        is NetworkResult.Success -> DataState.Success(data)
        is NetworkResult.Error -> DataState.Error(error.toThrowable(), existingData)
    }
```

### toDataStateWithMapping() -- Smart Conversion

Maps `REQUEST_TIMEOUT` to `DataState.NoNetwork` instead of `DataState.Error`. Use this when the UI should show an offline indicator for timeout errors:

```kotlin
fun <D> NetworkResult<D, *>.toDataStateWithMapping(): DataState<D> =
    when (this) {
        is NetworkResult.Success -> DataState.Success(data)
        is NetworkResult.Error -> when (error) {
            NetworkError.REQUEST_TIMEOUT -> DataState.NoNetwork(null)
            else -> DataState.Error(error.toThrowable(), null)
        }
    }
```

With existing data preserved:

```kotlin
fun <D> NetworkResult<D, *>.toDataStateWithMapping(existingData: D?): DataState<D> =
    when (this) {
        is NetworkResult.Success -> DataState.Success(data)
        is NetworkResult.Error -> when (error) {
            NetworkError.REQUEST_TIMEOUT -> DataState.NoNetwork(existingData)
            else -> DataState.Error(error.toThrowable(), existingData)
        }
    }
```

### Which to Use

| Scenario | Function | Result on Timeout |
|---|---|---|
| Standard API call | `toDataState()` | `DataState.Error` with timeout message |
| Data screen with offline support | `toDataStateWithMapping()` | `DataState.NoNetwork` |
| Refreshing with cached data visible | `toDataState(currentData)` | `DataState.Error` keeping existing data |
| Refreshing with offline banner | `toDataStateWithMapping(currentData)` | `DataState.NoNetwork` keeping existing data |

### Repository Usage Example (Ktorfit)

```kotlin
class MovieRepositoryImpl(
    private val movieApi: MovieApi,
) : MovieRepository {

    override suspend fun getMovie(id: Int): DataState<Movie> {
        return movieApi.getMovie(id)
            .toDataState()
            .map { it.toDomain() }
    }

    override suspend fun getMovies(): DataState<List<Movie>> {
        return movieApi.getMovies()
            .toDataStateWithMapping()
            .map { dtos -> dtos.map { it.toDomain() } }
    }
}
```

### Repository Usage Example (Supabase)

```kotlin
class MovieRepositoryImpl(
    private val movieService: MovieService,
) : MovieRepository {

    override suspend fun getMovie(id: Int): DataState<Movie> {
        return movieService.getMovie(id)
            .toDataState()
            .map { it.toDomain() }
    }
}
```

### Flow Extensions

There are two `asDataStateFlow()` functions in the foundation. Be careful to use the correct one:

**1. ResultExtensions.kt (core/data)** -- for `Flow<NetworkResult>`:

```kotlin
fun <D> Flow<NetworkResult<D, *>>.asDataStateFlow(): Flow<DataState<D>> =
    map { it.toDataState() }
        .onStart { emit(DataState.Loading) }
```

**2. DataState.kt (core-base/common)** -- for any `Flow<T>`:

```kotlin
fun <T> Flow<T>.asDataStateFlow(): Flow<DataState<T>> =
    map<T, DataState<T>> { DataState.Success(it) }
        .onStart { emit(DataState.Loading) }
        .catch { emit(DataState.Error(it, null)) }
```

The mobile-wallet exemplar uses version 2 (from `DataState.kt`) because its services return raw `Flow<T>` types. When using the `toDataState()` pipeline with `NetworkResult`, use version 1 from `ResultExtensions.kt`.

With existing data preservation:

```kotlin
fun <D> Flow<NetworkResult<D, *>>.asDataStateFlow(
    preserveDataOnError: Boolean = false,
    getCurrentData: () -> D? = { null },
): Flow<DataState<D>> = flow {
    emit(DataState.Loading)
    collect { result ->
        val dataState = if (preserveDataOnError) {
            result.toDataState(getCurrentData())
        } else {
            result.toDataState()
        }
        emit(dataState)
    }
}
```

---

## NetworkResult-to-DataState Bridge (Complete Reference)

This section consolidates all bridge functions from `ResultExtensions.kt` into a single
reference. These are the functions that connect the network boundary (`NetworkResult`)
to the UI boundary (`DataState`).

### Compact Bridge (Code-Oriented)

When using `RemoteException` with HTTP status codes for programmatic handling:

```kotlin
fun NetworkError.toThrowable(): Throwable = when (this) {
    NetworkError.BAD_REQUEST -> RemoteException("Bad Request", 400)
    NetworkError.UNAUTHORIZED -> RemoteException("Unauthorized", 401)
    NetworkError.NOT_FOUND -> RemoteException("Not Found", 404)
    NetworkError.REQUEST_TIMEOUT -> RemoteException("Request Timeout", 408)
    NetworkError.TOO_MANY_REQUESTS -> RemoteException("Too Many Requests", 429)
    NetworkError.SERVER -> RemoteException("Server Error", 500)
    NetworkError.SERIALIZATION -> RemoteException("Serialization Error", 0)
    NetworkError.UNKNOWN -> RemoteException("Unknown Error", -1)
}

fun <D> NetworkResult<D, *>.toDataState(): DataState<D> = when (this) {
    is NetworkResult.Success -> DataState.Success(data)
    is NetworkResult.Error -> DataState.Error(error.toThrowable())
}

fun <D> Flow<NetworkResult<D, *>>.asDataStateFlow(): Flow<DataState<D>> =
    map { it.toDataState() }
        .onStart { emit(DataState.Loading) }
        .catch { emit(DataState.Error(it)) }
```

> **Note**: The compact bridge uses HTTP status codes in `RemoteException` for
> programmatic branching (e.g., `if (statusCode == 401) navigateToLogin()`).
> The user-friendly messages in the [section above](#networkerrortothrowable-messages)
> are for UI display. Both approaches are valid -- choose based on your error
> presentation strategy.

### Quick Reference: All Bridge Functions

| Function | Input | Output | Use When |
|----------|-------|--------|----------|
| `toThrowable()` | `NetworkError` | `Throwable` | Converting typed error to exception hierarchy |
| `toDataState()` | `NetworkResult<D, *>` | `DataState<D>` | Standard one-shot conversion |
| `toDataState(existingData)` | `NetworkResult<D, *>` + `D?` | `DataState<D>` | Preserving cached data on error |
| `toDataStateWithMapping()` | `NetworkResult<D, *>` | `DataState<D>` | Mapping `REQUEST_TIMEOUT` to `NoNetwork` |
| `asDataStateFlow()` | `Flow<NetworkResult<D, *>>` | `Flow<DataState<D>>` | Flow-based sources (Realtime, WebSocket) |

---

## Supabase Exception Mapping

Supabase SDK does not use Ktorfit, so the `ResultSuspendConverterFactory` does not apply. Instead, each `{Feature}ServiceImpl` wraps Supabase calls in a try-catch and converts exceptions to `NetworkResult` using a local `Exception.toNetworkError()` extension.

### Exception.toNetworkError()

```kotlin
import template.core.base.network.NetworkError

private fun Exception.toNetworkError(): NetworkError = when {
    message?.contains("400") == true -> NetworkError.BAD_REQUEST
    message?.contains("401") == true -> NetworkError.UNAUTHORIZED
    message?.contains("404") == true -> NetworkError.NOT_FOUND
    message?.contains("timeout", ignoreCase = true) == true -> NetworkError.REQUEST_TIMEOUT
    message?.contains("429") == true -> NetworkError.TOO_MANY_REQUESTS
    message?.contains("500") == true || message?.contains("502") == true
        || message?.contains("503") == true -> NetworkError.SERVER
    this is kotlinx.serialization.SerializationException -> NetworkError.SERIALIZATION
    message?.contains("Unable to resolve host") == true
        || message?.contains("No address associated") == true -> NetworkError.REQUEST_TIMEOUT
    else -> NetworkError.UNKNOWN
}
```

### Supabase Service Pattern

```kotlin
class MovieServiceImpl(
    private val supabaseClient: SupabaseClient,
) : MovieService {

    override suspend fun getMovies(): NetworkResult<List<MovieDto>, NetworkError> {
        return try {
            val result = supabaseClient
                .from("movies")
                .select()
                .decodeList<MovieDto>()
            NetworkResult.Success(result)
        } catch (e: Exception) {
            NetworkResult.Error(e.toNetworkError())
        }
    }
}
```

This keeps the repository layer identical for both backends -- it always receives `NetworkResult` and calls `toDataState()`.

---

## ViewModel Error Handling

ViewModels observe `DataState` via `StateFlow` and render the appropriate UI state. They never see `NetworkError` or `NetworkResult` directly.

### Basic Pattern

```kotlin
@Composable
fun MovieScreen(viewModel: MovieViewModel) {
    val state by viewModel.movieState.collectAsStateWithLifecycle()

    when (val currentState = state) {
        is DataState.Loading -> LoadingIndicator()
        is DataState.Success -> MovieContent(currentState.data)
        is DataState.Error -> ErrorContent(
            message = currentState.error.message ?: "Something went wrong",
            onRetry = { viewModel.retry() },
        )
        is DataState.NoNetwork -> OfflineBanner(
            cachedData = currentState.data,
            onRetry = { viewModel.retry() },
        )
        is DataState.Pending -> {
            // Show existing data with a refresh indicator
            MovieContent(currentState.data)
            RefreshIndicator()
        }
    }
}
```

### Extracting NetworkError for Specific Handling

When the ViewModel needs to take action based on the error type (e.g., redirect to login):

```kotlin
class MovieViewModel(
    private val repository: MovieRepository,
) : ViewModel() {

    private val _movieState = MutableStateFlow<DataState<Movie>>(DataState.Loading)
    val movieState: StateFlow<DataState<Movie>> = _movieState.asStateFlow()

    fun loadMovie(id: Int) {
        viewModelScope.launch {
            _movieState.value = DataState.Loading
            val result = repository.getMovie(id)
            _movieState.value = result

            // Handle specific error types
            if (result is DataState.Error) {
                val networkError = (result.error as? RemoteException)?.networkError
                when (networkError) {
                    NetworkError.UNAUTHORIZED -> navigateToLogin()
                    NetworkError.NOT_FOUND -> showNotFoundScreen()
                    else -> { /* default error display handled by UI */ }
                }
            }
        }
    }
}
```

### Using Utility Extensions

The `ResultExtensions` file provides convenience properties for checking DataState:

```kotlin
// Check state type
if (movieState.value.isSuccess) { /* ... */ }
if (movieState.value.isError) { /* ... */ }

// Extract error details
val error: Throwable? = movieState.value.errorOrNull
val networkError: NetworkError? = movieState.value.networkErrorOrNull
```

---

## DataState Utility Extensions

Located in `core/data/src/commonMain/kotlin/.../core/data/util/ResultExtensions.kt`.

These extensions simplify working with `DataState` in ViewModels and UI code:

```kotlin
// =========================================================================
// State checking extensions
// =========================================================================

/** Check if DataState is a successful state */
val <T> DataState<T>.isSuccess: Boolean
    get() = this is DataState.Success

/** Check if DataState is an error state */
val <T> DataState<T>.isError: Boolean
    get() = this is DataState.Error

/** Check if DataState is in loading state */
val <T> DataState<T>.isLoading: Boolean
    get() = this is DataState.Loading

// =========================================================================
// Data extraction extensions
// =========================================================================

/** Get the Throwable if DataState is in error state */
val <T> DataState<T>.errorOrNull: Throwable?
    get() = (this as? DataState.Error)?.error

/** Get the NetworkError if the error is a RemoteException */
val <T> DataState<T>.networkErrorOrNull: NetworkError?
    get() = (this as? DataState.Error)?.error?.let { error ->
        (error as? RemoteException)?.networkError
    }

/** Get the success data or null (shorthand for .data on Success) */
val <T> DataState<T>.dataOrNull: T?
    get() = (this as? DataState.Success)?.data
```

### Usage in ViewModel

```kotlin
// Concise state checks
if (state.isSuccess) updateUI(state.dataOrNull!!)
if (state.isError) showError(state.errorOrNull?.message)

// Programmatic error branching
val networkError = state.networkErrorOrNull
if (networkError == NetworkError.UNAUTHORIZED) navigateToLogin()
```

---

## Testing Error Handling

### Testing Repository with NetworkResult.Error

```kotlin
@Test
fun `getMovie returns error state on NOT_FOUND`() = runTest {
    // Given
    coEvery {
        mockApi.getMovie(99)
    } returns NetworkResult.Error(NetworkError.NOT_FOUND)

    // When
    val result = repository.getMovie(99)

    // Then
    assertIs<DataState.Error<Movie>>(result)
    val remoteException = result.error as RemoteException
    assertEquals(NetworkError.NOT_FOUND, remoteException.networkError)
    assertEquals(
        "The information you're looking for couldn't be found.",
        remoteException.message,
    )
}
```

### Testing Repository with toDataStateWithMapping

```kotlin
@Test
fun `getMovies returns NoNetwork on REQUEST_TIMEOUT`() = runTest {
    // Given
    coEvery {
        mockApi.getMovies()
    } returns NetworkResult.Error(NetworkError.REQUEST_TIMEOUT)

    // When -- repository uses toDataStateWithMapping()
    val result = repository.getMovies()

    // Then
    assertIs<DataState.NoNetwork<List<Movie>>>(result)
    assertNull(result.data)
}
```

### Testing Supabase Service Exception Mapping

```kotlin
@Test
fun `getMovies maps timeout exception to REQUEST_TIMEOUT`() = runTest {
    // Given
    coEvery {
        mockSupabaseClient.from("movies").select().decodeList<MovieDto>()
    } throws Exception("Request timeout")

    // When
    val result = service.getMovies()

    // Then
    assertIs<NetworkResult.Error<NetworkError>>(result)
    assertEquals(NetworkError.REQUEST_TIMEOUT, result.error)
}
```

### Testing ViewModel Error State

```kotlin
@Test
fun `loadMovie emits error state with user-friendly message`() = runTest {
    // Given
    coEvery {
        mockRepository.getMovie(1)
    } returns DataState.Error(
        RemoteException(NetworkError.SERVER, "We're experiencing technical difficulties. Please try again later."),
    )

    // When
    viewModel.loadMovie(1)

    // Then
    val state = viewModel.movieState.value
    assertIs<DataState.Error<Movie>>(state)
    assertEquals(
        "We're experiencing technical difficulties. Please try again later.",
        state.error.message,
    )
}
```

---

## Related Files

- Client Patterns: [CLIENT_PATTERNS.md](CLIENT_PATTERNS.md)
- Supabase Patterns: [kotlin/SUPABASE_CLIENT_PATTERNS.md](kotlin/SUPABASE_CLIENT_PATTERNS.md)
- Repository Template: [REPOSITORY_TEMPLATE.kt.md](REPOSITORY_TEMPLATE.kt.md)
- Service Template: [SERVICE_TEMPLATE.kt.md](SERVICE_TEMPLATE.kt.md)

---

## Changelog

| Date | Change |
|------|--------|
| 2025-01-05 | Created with error patterns from codebase analysis |
| 2026-02-26 | Rewritten for NetworkResult pipeline (NetworkError enum, RemoteException, toDataState/toDataStateWithMapping, Supabase mapping, ViewModel patterns) |
