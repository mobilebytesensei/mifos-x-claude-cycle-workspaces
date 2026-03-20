# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mifos-x-field-officer-app/client-layer/instructions/SERVICE_TEMPLATE.kt.md"
# last_modified: "2026-03-20"

# Service Template (Ktorfit Api Interface)

> **Layer**: core/network
> **Pattern**: Ktorfit HTTP Client Interface with NetworkResult
> **Confidence**: 95%

---

## Overview

Ktorfit Api interfaces define type-safe HTTP endpoints for REST communication. Every method
returns `NetworkResult<T, NetworkError>` -- a sealed type that encapsulates either a successful
response or a classified error. The `ResultSuspendConverterFactory` registered in the Ktorfit
builder performs this wrapping automatically, so individual endpoint methods never throw
exceptions and never contain try-catch logic.

### Why NetworkResult Instead of Raw Types

| Old (Wrong) | New (Correct) | Reason |
|-------------|---------------|--------|
| `Flow<List<Dto>>` | `suspend fun ...(): NetworkResult<List<Dto>, NetworkError>` | Ktorfit GET is a one-shot request, not a stream |
| `suspend fun ...(): HttpResponse` | `suspend fun ...(): NetworkResult<Dto, NetworkError>` | Raw HttpResponse forces manual status checking |
| `suspend fun ...(): Dto?` | `suspend fun ...(): NetworkResult<Dto, NetworkError>` | Nullable hides error details (was it 404? 500? timeout?) |

With `NetworkResult`, the repository layer calls `toDataState()` to convert into a UI-friendly
`DataState<T>` -- no manual error mapping needed anywhere in the chain.

### Naming Convention: Api vs Service

| Suffix | Used For | Example |
|--------|----------|---------|
| `{Feature}Api` | Ktorfit interface (REST endpoints, auto-generated impl) | `MovieApi`, `UserApi` |
| `{Feature}Service` | Supabase service interface (manual impl wrapping SupabaseClient) | `MovieService`, `UserService` |

The `Api` suffix distinguishes Ktorfit-generated implementations (where Ktorfit creates the
class at compile time via KSP) from Supabase service classes (where you write
`{Feature}ServiceImpl` manually). Repositories accept either type through their interface
-- they are interchangeable at the DI level.

---

## File Location

```
core/network/src/commonMain/kotlin/{package}/core/network/service/{feature}/{Feature}Api.kt
```

---

## Template

```kotlin
package {appPackage}.core.network.service.{feature}

import de.jensklingenberg.ktorfit.http.Body
import de.jensklingenberg.ktorfit.http.DELETE
import de.jensklingenberg.ktorfit.http.GET
import de.jensklingenberg.ktorfit.http.Header
import de.jensklingenberg.ktorfit.http.Headers
import de.jensklingenberg.ktorfit.http.PATCH
import de.jensklingenberg.ktorfit.http.POST
import de.jensklingenberg.ktorfit.http.PUT
import de.jensklingenberg.ktorfit.http.Path
import de.jensklingenberg.ktorfit.http.Query
import {appPackage}.core.network.model.{Feature}Dto
import {appPackage}.core.network.model.Create{Feature}Request
import {appPackage}.core.network.model.Update{Feature}Request
import {appPackage}.core.network.model.Patch{Feature}Request
import {appPackage}.core.network.model.{Feature}PageResponse
import template.core.base.network.NetworkError
import template.core.base.network.NetworkResult

/**
 * {Feature} API
 *
 * Defines all REST endpoints for {feature} functionality.
 * Uses Ktorfit for compile-time HTTP client generation.
 *
 * Return type convention:
 * - All methods return `NetworkResult<T, NetworkError>`
 * - The `ResultSuspendConverterFactory` auto-wraps HTTP responses
 * - Services never throw exceptions -- errors arrive as `NetworkResult.Error`
 */
interface {Feature}Api {

    // =========================================================================
    // GET Endpoints
    // =========================================================================

    /**
     * Get all {feature} items.
     *
     * @return List of items wrapped in NetworkResult.
     */
    @GET("{endpoint}")
    suspend fun get{Feature}s(): NetworkResult<List<{Feature}Dto>, NetworkError>

    /**
     * Get a single {feature} item by ID.
     *
     * @param id Item identifier.
     * @return Single item wrapped in NetworkResult.
     *         Returns NetworkResult.Error with NetworkError.NOT_FOUND if the item does not exist.
     */
    @GET("{endpoint}/{id}")
    suspend fun get{Feature}ById(
        @Path("id") id: String,
    ): NetworkResult<{Feature}Dto, NetworkError>

    /**
     * Get {feature} items with pagination.
     *
     * @param limit Maximum number of items to return.
     * @param offset Number of items to skip (for offset-based pagination).
     * @return Paginated response wrapped in NetworkResult.
     */
    @GET("{endpoint}")
    suspend fun get{Feature}sPaginated(
        @Query("limit") limit: Int = 20,
        @Query("offset") offset: Int = 0,
    ): NetworkResult<{Feature}PageResponse, NetworkError>

    /**
     * Search {feature} items by query.
     *
     * @param query Search term.
     * @param limit Maximum number of results.
     * @return Matching items wrapped in NetworkResult.
     */
    @GET("{endpoint}/search")
    suspend fun search{Feature}s(
        @Query("q") query: String,
        @Query("limit") limit: Int = 20,
    ): NetworkResult<List<{Feature}Dto>, NetworkError>

    // =========================================================================
    // POST Endpoints
    // =========================================================================

    /**
     * Create a new {feature} item.
     *
     * @param request Creation request body.
     * @return The created item wrapped in NetworkResult.
     */
    @POST("{endpoint}")
    suspend fun create{Feature}(
        @Body request: Create{Feature}Request,
    ): NetworkResult<{Feature}Dto, NetworkError>

    // =========================================================================
    // PUT / PATCH Endpoints
    // =========================================================================

    /**
     * Full update of an existing {feature} item.
     *
     * @param id Item identifier.
     * @param request Full update request body.
     * @return The updated item wrapped in NetworkResult.
     */
    @PUT("{endpoint}/{id}")
    suspend fun update{Feature}(
        @Path("id") id: String,
        @Body request: Update{Feature}Request,
    ): NetworkResult<{Feature}Dto, NetworkError>

    /**
     * Partial update of an existing {feature} item.
     *
     * @param id Item identifier.
     * @param request Partial update fields.
     * @return The updated item wrapped in NetworkResult.
     */
    @PATCH("{endpoint}/{id}")
    suspend fun patch{Feature}(
        @Path("id") id: String,
        @Body request: Patch{Feature}Request,
    ): NetworkResult<{Feature}Dto, NetworkError>

    // =========================================================================
    // DELETE Endpoints
    // =========================================================================

    /**
     * Delete a {feature} item.
     *
     * @param id Item identifier.
     * @return Unit wrapped in NetworkResult (success = deleted, error = reason).
     */
    @DELETE("{endpoint}/{id}")
    suspend fun delete{Feature}(
        @Path("id") id: String,
    ): NetworkResult<Unit, NetworkError>
}
```

---

## Annotations Reference

| Annotation | Purpose | Example |
|------------|---------|---------|
| `@GET` | HTTP GET request | `@GET("movies")` |
| `@POST` | HTTP POST request | `@POST("movies")` |
| `@PUT` | HTTP PUT (full replace) | `@PUT("movies/{id}")` |
| `@PATCH` | HTTP PATCH (partial update) | `@PATCH("movies/{id}")` |
| `@DELETE` | HTTP DELETE request | `@DELETE("movies/{id}")` |
| `@Path` | URL path parameter | `@Path("id") id: String` |
| `@Query` | URL query parameter | `@Query("limit") limit: Int` |
| `@Body` | Request body (serialized to JSON) | `@Body request: CreateMovieRequest` |
| `@Header` | Dynamic request header | `@Header("Authorization") token: String` |
| `@Headers` | Static headers on method | `@Headers("Accept: application/json")` |

---

## Return Types

All methods use the same return type pattern. The only thing that changes is the
success type `T`:

| Success Type | Use Case | Signature |
|--------------|----------|-----------|
| `List<Dto>` | Fetching collections | `suspend fun getAll(): NetworkResult<List<Dto>, NetworkError>` |
| `Dto` | Fetching / creating / updating single item | `suspend fun getById(...): NetworkResult<Dto, NetworkError>` |
| `PageResponse` | Paginated results | `suspend fun getPaginated(...): NetworkResult<PageResponse, NetworkError>` |
| `Unit` | Delete or fire-and-forget | `suspend fun delete(...): NetworkResult<Unit, NetworkError>` |

Never use `Flow<T>` as a return type on a Ktorfit Api interface when using the
`NetworkResult` return type pattern. Ktorfit endpoints are one-shot HTTP calls. If you
need reactive streams (e.g., Supabase Realtime), use a `{Feature}Service` interface
with Flow return types instead.

> **Exemplar note**: The mobile-wallet exemplar uses an older Ktorfit pattern where
> service methods return raw types (`suspend fun ...(): T` or `fun ...(): Flow<T>`)
> without `NetworkResult` wrapping. In that pattern, repositories use manual `try-catch`
> and `withContext(ioDispatcher)`. The `NetworkResult` pattern described here is the
> **recommended approach** for new projects, as it eliminates try-catch in repositories
> and provides typed error classification via `ResultSuspendConverterFactory`.

---

## Alternative: Raw Return Types (Legacy / Migration)

When migrating an existing codebase or integrating with services that do not use
`ResultSuspendConverterFactory`, service interfaces can return raw types instead of
`NetworkResult`. In this pattern, **repositories** handle error wrapping manually
with `try-catch` and `withContext(ioDispatcher)`.

### When to Use Each Pattern

| Pattern | Use When | Error Handling |
|---------|----------|----------------|
| **NetworkResult (Primary)** | New projects, kmp-project-template foundation | Automatic via `ResultSuspendConverterFactory` -- no try-catch in repositories |
| **Raw Return Types (Alternative)** | Legacy migration, third-party APIs without converter factory, Retrofit-style codebases | Manual `try-catch` in repositories with `withContext(ioDispatcher)` |

### Alternative Service Interface Template

```kotlin
package {appPackage}.core.network.service.{feature}

import de.jensklingenberg.ktorfit.http.*
import {appPackage}.core.network.model.{Feature}Dto
import {appPackage}.core.network.model.Create{Feature}Request

/**
 * {Feature} Service -- Raw return type pattern.
 *
 * Return type convention:
 * - Methods return raw deserialized types (Dto, List<Dto>, Unit)
 * - Methods throw exceptions on HTTP errors
 * - Repositories wrap calls in try-catch to produce DataState
 *
 * Use this pattern when ResultSuspendConverterFactory is not available.
 */
interface {Feature}Service {

    @POST("{endpoint}")
    suspend fun authenticate(
        @Body payload: AuthenticationPayload,
    ): {Feature}Dto

    @GET("{endpoint}")
    suspend fun get{Feature}s(): List<{Feature}Dto>

    @GET("{endpoint}/{id}")
    suspend fun get{Feature}ById(
        @Path("id") id: String,
    ): {Feature}Dto

    @POST("{endpoint}")
    suspend fun create{Feature}(
        @Body request: Create{Feature}Request,
    ): {Feature}Dto

    @DELETE("{endpoint}/{id}")
    suspend fun delete{Feature}(
        @Path("id") id: String,
    )
}
```

### Alternative Concrete Example: AuthenticationService

From the mobile-wallet exemplar:

```kotlin
interface AuthenticationService {

    @POST(ApiEndPoints.AUTHENTICATION)
    suspend fun authenticate(
        @Body authPayload: AuthenticationPayload,
    ): User

    @POST(ApiEndPoints.CLIENTS)
    suspend fun getClients(): Page<Client>

    @GET(ApiEndPoints.SAVINGS_ACCOUNTS + "/{accountId}")
    suspend fun getSavingsAccount(
        @Path("accountId") accountId: Long,
    ): SavingsAccount
}
```

### How Repositories Handle Raw Types

When services return raw types, the repository is responsible for error handling:

```kotlin
class {Feature}RepositoryImpl(
    private val service: {Feature}Service,
    private val ioDispatcher: CoroutineDispatcher,
) : {Feature}Repository {

    override suspend fun get{Feature}ById(id: String): DataState<{Feature}> {
        return withContext(ioDispatcher) {
            try {
                val dto = service.get{Feature}ById(id)
                DataState.Success(dto.to{Feature}())
            } catch (e: Exception) {
                DataState.Error(e)
            }
        }
    }
}
```

See [REPOSITORY_TEMPLATE.kt.md](REPOSITORY_TEMPLATE.kt.md) for the full alternative
repository pattern.

---

## ResultSuspendConverterFactory

The `ResultSuspendConverterFactory` is what makes the `NetworkResult` return type work.
It intercepts every HTTP response before it reaches your code and wraps it:

```
HTTP 2xx  -->  NetworkResult.Success(deserializedBody)
HTTP 400  -->  NetworkResult.Error(NetworkError.BAD_REQUEST)
HTTP 401  -->  NetworkResult.Error(NetworkError.UNAUTHORIZED)
HTTP 404  -->  NetworkResult.Error(NetworkError.NOT_FOUND)
HTTP 408  -->  NetworkResult.Error(NetworkError.REQUEST_TIMEOUT)
HTTP 429  -->  NetworkResult.Error(NetworkError.TOO_MANY_REQUESTS)
HTTP 5xx  -->  NetworkResult.Error(NetworkError.SERVER)
Deserialization failure  -->  NetworkResult.Error(NetworkError.SERIALIZATION)
Unknown failure          -->  NetworkResult.Error(NetworkError.UNKNOWN)
```

### Registration (Required)

The factory MUST be registered when building the Ktorfit instance. Without it,
Ktorfit will not know how to produce `NetworkResult` and compilation will fail.

```kotlin
val ktorfit = Ktorfit.Builder()
    .baseUrl(baseUrl)
    .httpClient(httpClient)
    .converterFactories(
        ResultSuspendConverterFactory(),
    )
    .build()
```

This is a one-time setup in `NetworkModule.kt`. Individual Api interfaces do not need
any special configuration -- they just declare `NetworkResult` as their return type and
the factory handles the rest.

### Source Location

The factory lives in the `core-base/network` module (part of the template project
foundation, never regenerated):

```
core-base/network/src/commonMain/kotlin/template/core/base/network/factory/ResultSuspendConverterFactory.kt
```

---

## @Header and @Headers Usage

### Dynamic Headers (Per-Request)

Use `@Header` when the value changes per call (e.g., tokens, API keys):

```kotlin
@GET("{endpoint}")
suspend fun get{Feature}sWithAuth(
    @Header("Authorization") token: String,
): NetworkResult<List<{Feature}Dto>, NetworkError>
```

### Static Headers (Per-Method)

Use `@Headers` when every call to this method needs the same headers:

```kotlin
@Headers("Accept: application/json", "X-Api-Version: 2")
@POST("{endpoint}")
suspend fun create{Feature}(
    @Body request: Create{Feature}Request,
): NetworkResult<{Feature}Dto, NetworkError>
```

Note: Prefer setting common headers (Content-Type, Authorization) in the HttpClient
configuration rather than on every method. Use `@Header`/`@Headers` only for
endpoint-specific headers.

---

## Example: MovieApi

```kotlin
package com.example.app.core.network.service.movie

import de.jensklingenberg.ktorfit.http.Body
import de.jensklingenberg.ktorfit.http.DELETE
import de.jensklingenberg.ktorfit.http.GET
import de.jensklingenberg.ktorfit.http.POST
import de.jensklingenberg.ktorfit.http.PUT
import de.jensklingenberg.ktorfit.http.Path
import de.jensklingenberg.ktorfit.http.Query
import com.example.app.core.network.model.CreateMovieRequest
import com.example.app.core.network.model.MovieDto
import com.example.app.core.network.model.MoviePageResponse
import com.example.app.core.network.model.UpdateMovieRequest
import template.core.base.network.NetworkError
import template.core.base.network.NetworkResult

interface MovieApi {

    @GET("movies")
    suspend fun getMovies(): NetworkResult<List<MovieDto>, NetworkError>

    @GET("movies/{id}")
    suspend fun getMovieById(
        @Path("id") id: String,
    ): NetworkResult<MovieDto, NetworkError>

    @GET("movies")
    suspend fun getMoviesPaginated(
        @Query("limit") limit: Int = 20,
        @Query("offset") offset: Int = 0,
    ): NetworkResult<MoviePageResponse, NetworkError>

    @GET("movies/search")
    suspend fun searchMovies(
        @Query("q") query: String,
        @Query("limit") limit: Int = 20,
    ): NetworkResult<List<MovieDto>, NetworkError>

    @POST("movies")
    suspend fun createMovie(
        @Body request: CreateMovieRequest,
    ): NetworkResult<MovieDto, NetworkError>

    @PUT("movies/{id}")
    suspend fun updateMovie(
        @Path("id") id: String,
        @Body request: UpdateMovieRequest,
    ): NetworkResult<MovieDto, NetworkError>

    @DELETE("movies/{id}")
    suspend fun deleteMovie(
        @Path("id") id: String,
    ): NetworkResult<Unit, NetworkError>
}
```

---

## Supabase RPC Pattern

For backends using Supabase RPC (Remote Procedure Calls), use a `{Feature}Service`
interface instead of `{Feature}Api`. The service wraps Supabase SDK calls in
`NetworkResult` manually:

```kotlin
// Interface (in core/network/service/{feature}/)
interface MovieService {
    suspend fun getMoviesByMood(
        moodId: String,
        limit: Int,
        offset: Int,
    ): NetworkResult<List<MovieDto>, NetworkError>
}

// Implementation (in core/network/service/{feature}/)
class MovieServiceImpl(
    private val client: SupabaseClient,
) : MovieService {
    override suspend fun getMoviesByMood(
        moodId: String,
        limit: Int,
        offset: Int,
    ): NetworkResult<List<MovieDto>, NetworkError> {
        return try {
            val params = buildJsonObject {
                put("p_mood_id", moodId)
                put("p_limit", limit)
                put("p_offset", offset)
            }
            val result = client.postgrest
                .rpc("get_cached_movies_by_mood", params)
                .decodeList<MovieDto>()
            NetworkResult.Success(result)
        } catch (e: Exception) {
            NetworkResult.Error(e.toNetworkError())
        }
    }
}
```

The repository layer does not care whether it receives data from a Ktorfit `Api`
or a Supabase `Service` -- both return `NetworkResult<T, NetworkError>`, so the
repository uses the same `toDataState()` conversion in either case.

---

## DI Registration

### REST (Ktorfit Api)

```kotlin
// In NetworkModule.kt
val networkModule = module {
    // Ktorfit instance (configured once with ResultSuspendConverterFactory)
    single {
        Ktorfit.Builder()
            .baseUrl(BuildConfig.BASE_URL)
            .httpClient(get<HttpClient>())
            .converterFactories(ResultSuspendConverterFactory())
            .build()
    }

    // Api interfaces (Ktorfit generates implementations at compile time)
    single<{Feature}Api> { get<Ktorfit>().create<{Feature}Api>() }
}
```

### Supabase (Service + ServiceImpl)

```kotlin
// In NetworkModule.kt
val networkModule = module {
    single<{Feature}Service> { {Feature}ServiceImpl(get()) }
}
```

---

## Related Templates

| Template | Purpose |
|----------|---------|
| `DTO_TEMPLATE.kt.md` | Request/Response DTOs used by this Api |
| `MAPPER_TEMPLATE.kt.md` | DTO-to-Domain mappers used by repository |
| `REPOSITORY_TEMPLATE.kt.md` | Repository that consumes this Api via `toDataState()` |
| `ERROR_HANDLING.md` | Full NetworkError/NetworkResult/DataState pipeline |
