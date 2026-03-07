# Repository Template (Data Layer)

> **Layer**: core/data
> **Pattern**: Repository Pattern with toDataState() conversion
> **Confidence**: 95%

---

## Overview

Repositories sit at the boundary between `NetworkResult` (network layer) and `DataState` (UI layer). Their only job is to call `toDataState()` on the `NetworkResult` returned by the service/API, then `.map {}` the DTO to a domain model. No try-catch. No manual error mapping. No dispatcher injection.

```
NetworkResult<T, NetworkError>   <-- from {Feature}Api / {Feature}Service
        |
        v  toDataState()         <-- ResultExtensions (one-liner)
DataState<T>                     <-- returned to ViewModel
        |
        v  .map { dto -> dto.to{Feature}() }
DataState<DomainModel>           <-- final result with domain types
```

---

## File Locations

Interface and implementation live in separate directories with separate packages:

```
core/data/src/commonMain/kotlin/{package}/core/data/repository/{Feature}Repository.kt
core/data/src/commonMain/kotlin/{package}/core/data/repositoryImpl/{Feature}RepositoryImpl.kt
```

| Artifact | Package | Directory |
|----------|---------|-----------|
| `{Feature}Repository` (interface) | `{appPackage}.core.data.repository` | `repository/` |
| `{Feature}RepositoryImpl` (class) | `{appPackage}.core.data.repositoryImpl` | `repositoryImpl/` |

---

## Repository Interface Template

```kotlin
package {appPackage}.core.data.repository

import {appPackage}.core.model.{Feature}
import template.core.base.common.DataState
import kotlinx.coroutines.flow.Flow

/**
 * {Feature} Repository Interface
 *
 * Abstraction layer between data sources and domain/feature layers.
 * Returns DataState<T> for consistent error handling across the app.
 *
 * Convention:
 * - Use suspend for one-shot operations (CRUD, search, paging)
 * - Use Flow for real-time streams (Supabase Realtime, Room observation)
 */
interface {Feature}Repository {

    // =========================================================================
    // Suspend (One-shot operations) -- DEFAULT for most methods
    // =========================================================================

    /**
     * Get all {feature} items.
     * @return DataState with list of items or error.
     */
    suspend fun get{Feature}s(): DataState<List<{Feature}>>

    /**
     * Get a single {feature} item by ID.
     * @param id Item identifier.
     * @return DataState with item or error.
     */
    suspend fun get{Feature}ById(id: String): DataState<{Feature}>

    /**
     * Create a new {feature} item.
     * @param request Creation data.
     * @return DataState with created item or error.
     */
    suspend fun create{Feature}(request: Create{Feature}Request): DataState<{Feature}>

    /**
     * Update an existing {feature} item.
     * @param id Item identifier.
     * @param request Update data.
     * @return DataState with updated item or error.
     */
    suspend fun update{Feature}(id: String, request: Update{Feature}Request): DataState<{Feature}>

    /**
     * Delete a {feature} item.
     * @param id Item identifier.
     * @return DataState with Unit on success or error.
     */
    suspend fun delete{Feature}(id: String): DataState<Unit>

    // =========================================================================
    // Flow (Real-time / observation) -- ONLY when streaming is needed
    // =========================================================================

    /**
     * Observe {feature} items in real time.
     * Emits Loading, then continuous updates as DataState.
     *
     * Use when: Supabase Realtime, Room @Query Flow, or combined cache+network.
     * @return Flow emitting DataState with list updates.
     */
    fun observe{Feature}s(): Flow<DataState<List<{Feature}>>>
}
```

---

## Repository Implementation Template

### REST (Ktorfit Api)

```kotlin
package {appPackage}.core.data.repositoryImpl

import {appPackage}.core.data.repository.{Feature}Repository
import {appPackage}.core.data.util.toDataState
import {appPackage}.core.data.mapper.to{Feature}
import {appPackage}.core.data.mapper.to{Feature}List
import {appPackage}.core.model.{Feature}
import {appPackage}.core.network.service.{feature}.{Feature}Api
import template.core.base.common.DataState

/**
 * {Feature} Repository Implementation
 *
 * Bridges NetworkResult (from Api) to DataState (for UI) using toDataState().
 * No try-catch, no manual error mapping, no dispatcher injection.
 * Ktor handles threading internally -- no ioDispatcher needed.
 */
class {Feature}RepositoryImpl(
    private val api: {Feature}Api,
) : {Feature}Repository {

    override suspend fun get{Feature}s(): DataState<List<{Feature}>> =
        api.get{Feature}s().toDataState().map { dtos -> dtos.to{Feature}List() }

    override suspend fun get{Feature}ById(id: String): DataState<{Feature}> =
        api.get{Feature}ById(id).toDataState().map { dto -> dto.to{Feature}() }

    override suspend fun create{Feature}(
        request: Create{Feature}Request,
    ): DataState<{Feature}> =
        api.create{Feature}(request).toDataState().map { dto -> dto.to{Feature}() }

    override suspend fun update{Feature}(
        id: String,
        request: Update{Feature}Request,
    ): DataState<{Feature}> =
        api.update{Feature}(id, request).toDataState().map { dto -> dto.to{Feature}() }

    override suspend fun delete{Feature}(id: String): DataState<Unit> =
        api.delete{Feature}(id).toDataState()
}
```

### Supabase (Service)

The pattern is identical because both `{Feature}Api` and `{Feature}Service` return `NetworkResult<T, NetworkError>`:

```kotlin
package {appPackage}.core.data.repositoryImpl

import {appPackage}.core.data.repository.{Feature}Repository
import {appPackage}.core.data.util.toDataState
import {appPackage}.core.data.mapper.to{Feature}
import {appPackage}.core.data.mapper.to{Feature}List
import {appPackage}.core.model.{Feature}
import {appPackage}.core.network.service.{feature}.{Feature}Service
import template.core.base.common.DataState

class {Feature}RepositoryImpl(
    private val service: {Feature}Service,
) : {Feature}Repository {

    override suspend fun get{Feature}s(): DataState<List<{Feature}>> =
        service.get{Feature}s().toDataState().map { dtos -> dtos.to{Feature}List() }

    override suspend fun get{Feature}ById(id: String): DataState<{Feature}> =
        service.get{Feature}ById(id).toDataState().map { dto -> dto.to{Feature}() }

    override suspend fun create{Feature}(
        request: Create{Feature}Request,
    ): DataState<{Feature}> =
        service.create{Feature}(request).toDataState().map { dto -> dto.to{Feature}() }

    override suspend fun update{Feature}(
        id: String,
        request: Update{Feature}Request,
    ): DataState<{Feature}> =
        service.update{Feature}(id, request).toDataState().map { dto -> dto.to{Feature}() }

    override suspend fun delete{Feature}(id: String): DataState<Unit> =
        service.delete{Feature}(id).toDataState()
}
```

---

## Alternative: Raw Return Types with try-catch

When services return raw types (no `NetworkResult` wrapping), the repository handles
error conversion manually with `try-catch` and `withContext(ioDispatcher)`. This pattern
is used in the mobile-wallet exemplar and is appropriate for legacy codebases or
third-party APIs that do not use `ResultSuspendConverterFactory`.

### When to Use Each Pattern

| Pattern | Use When | Repository Complexity |
|---------|----------|----------------------|
| **NetworkResult + toDataState() (Primary)** | New projects, kmp-project-template | Minimal -- one-liner per method, no try-catch |
| **Raw types + try-catch (Alternative)** | Legacy migration, Retrofit-style services | Higher -- try-catch + withContext per method |

### Alternative Repository Interface

The interface is **identical** regardless of pattern -- it always returns `DataState<T>`:

```kotlin
interface {Feature}Repository {
    suspend fun get{Feature}s(): DataState<List<{Feature}>>
    suspend fun get{Feature}ById(id: String): DataState<{Feature}>
    suspend fun authenticate(username: String, password: String): DataState<User>
}
```

### Alternative Repository Implementation (try-catch Pattern)

```kotlin
package {appPackage}.core.data.repositoryImpl

import {appPackage}.core.data.repository.{Feature}Repository
import {appPackage}.core.data.mapper.to{Feature}
import {appPackage}.core.data.mapper.to{Feature}List
import {appPackage}.core.model.{Feature}
import {appPackage}.core.network.service.{feature}.{Feature}Service
import template.core.base.common.DataState
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.withContext

/**
 * {Feature} Repository Implementation -- Raw return type pattern.
 *
 * Services return raw types (Dto, List<Dto>) and throw on errors.
 * Repository wraps each call in try-catch to produce DataState.
 * Uses withContext(ioDispatcher) because raw Ktorfit/Retrofit calls
 * may not handle threading internally.
 */
class {Feature}RepositoryImpl(
    private val service: {Feature}Service,
    private val ioDispatcher: CoroutineDispatcher,
) : {Feature}Repository {

    override suspend fun get{Feature}s(): DataState<List<{Feature}>> {
        return withContext(ioDispatcher) {
            try {
                val dtos = service.get{Feature}s()
                DataState.Success(dtos.to{Feature}List())
            } catch (e: Exception) {
                DataState.Error(e)
            }
        }
    }

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

### Concrete Example: AuthenticationRepositoryImpl (from mobile-wallet)

```kotlin
class AuthenticationRepositoryImpl(
    private val authService: AuthenticationService,
    private val ioDispatcher: CoroutineDispatcher,
) : AuthenticationRepository {

    override suspend fun authenticate(
        username: String,
        password: String,
    ): DataState<User> {
        return withContext(ioDispatcher) {
            try {
                val user = authService.authenticate(
                    AuthenticationPayload(username, password),
                )
                DataState.Success(user)
            } catch (e: Exception) {
                DataState.Error(e)
            }
        }
    }

    override fun observeClients(): Flow<DataState<List<Client>>> {
        return flow {
            emit(DataState.Loading)
            try {
                val clients = authService.getClients()
                emit(DataState.Success(clients.pageItems))
            } catch (e: Exception) {
                emit(DataState.Error(e))
            }
        }.flowOn(ioDispatcher)
    }
}
```

### Comparison: Same Method, Both Patterns

```kotlin
// PRIMARY: NetworkResult pattern (no try-catch, no dispatcher)
override suspend fun getMovies(): DataState<List<Movie>> =
    api.getMovies().toDataState().map { dtos -> dtos.toMovieList() }

// ALTERNATIVE: Raw type pattern (try-catch + dispatcher)
override suspend fun getMovies(): DataState<List<Movie>> {
    return withContext(ioDispatcher) {
        try {
            val dtos = service.getMovies()
            DataState.Success(dtos.toMovieList())
        } catch (e: Exception) {
            DataState.Error(e)
        }
    }
}
```

The primary pattern is 1 line. The alternative is 8 lines. Both produce identical
`DataState<List<Movie>>` output. Prefer the primary pattern for new projects.

### DI for Alternative Pattern

When using the try-catch pattern, the repository needs an `ioDispatcher`:

```kotlin
// core/data/di/RepositoryModule.kt
val dataModule = module {
    single<CoroutineDispatcher>(named("io")) { Dispatchers.IO }

    single<{Feature}Repository> {
        {Feature}RepositoryImpl(
            service = get(),
            ioDispatcher = get(named("io")),
        )
    }
}
```

---

## ResultExtensions Reference

The bridge utilities live in `core/data/src/commonMain/kotlin/{package}/core/data/util/ResultExtensions.kt`. These are part of the foundation and are never regenerated.

### Available Functions

| Function | Signature | Use When |
|----------|-----------|----------|
| `toDataState()` | `NetworkResult<T, NetworkError>.toDataState(): DataState<T>` | Standard one-shot conversion (most common) |
| `toDataState(existingData)` | `NetworkResult<T, NetworkError>.toDataState(existingData: T?): DataState<T>` | Preserving cached data on error (refresh scenarios) |
| `toDataStateWithMapping()` | `NetworkResult<T, NetworkError>.toDataStateWithMapping(transform: (T) -> R): DataState<R>` | Combining conversion and DTO mapping in one call |
| `asDataStateFlow()` | `Flow<NetworkResult<T, NetworkError>>.asDataStateFlow(): Flow<DataState<T>>` | Flow wrapper -- emits Loading first, then converts each emission |

### Conversion Rules

| NetworkResult | DataState |
|---------------|-----------|
| `NetworkResult.Success(data)` | `DataState.Success(data)` |
| `NetworkResult.Error(NetworkError.REQUEST_TIMEOUT)` | `DataState.NoNetwork(existingData)` (via `toDataStateWithMapping()`) |
| `NetworkResult.Error(anyOtherError)` | `DataState.Error(throwable, existingData)` |

### toDataStateWithMapping Variant

The `toDataStateWithMapping()` variant maps `REQUEST_TIMEOUT` to `DataState.NoNetwork` instead of `DataState.Error`. Use this when the UI should show an offline indicator for timeout errors:

```kotlin
override suspend fun get{Feature}s(): DataState<List<{Feature}>> =
    api.get{Feature}s().toDataStateWithMapping { dtos -> dtos.to{Feature}List() }
```

### Preserving Cached Data on Refresh

Use the `toDataState(existingData)` overload to keep stale data visible when a refresh fails:

```kotlin
override suspend fun refresh{Feature}s(
    currentData: List<{Feature}>?,
): DataState<List<{Feature}>> =
    api.get{Feature}s().toDataState(currentData).map { dtos -> dtos.to{Feature}List() }
```

On success, the cached data is ignored and fresh data is returned. On error or no network, the error state carries the `existingData` so the UI can still display stale content with an error banner.

---

## DataState.map() for DTO-to-Domain Transformation

The `map()` extension on `DataState` transforms the success data without changing the state type. It is defined in the foundation:

```kotlin
fun <T, R> DataState<T>.map(transform: (T) -> R): DataState<R>
```

Behavior by state:

| Input State | Output After `.map { transform }` |
|-------------|----------------------------------|
| `Success(data)` | `Success(transform(data))` |
| `Error(error, data)` | `Error(error, data?.let(transform))` |
| `NoNetwork(data)` | `NoNetwork(data?.let(transform))` |
| `Pending(data)` | `Pending(transform(data))` |
| `Loading` | `Loading` |

This is why repositories can chain `.toDataState().map { dto -> dto.to{Feature}() }` -- the mapping only runs when there is data to transform.

---

## Suspend vs Flow Guidelines

### Use Suspend (Default for Most Methods)

| Scenario | Signature |
|----------|-----------|
| Fetch a list | `suspend fun get{Feature}s(): DataState<List<{Feature}>>` |
| Fetch by ID | `suspend fun get{Feature}ById(id: String): DataState<{Feature}>` |
| Create item | `suspend fun create{Feature}(request): DataState<{Feature}>` |
| Update item | `suspend fun update{Feature}(id, request): DataState<{Feature}>` |
| Delete item | `suspend fun delete{Feature}(id: String): DataState<Unit>` |
| Search | `suspend fun search{Feature}s(query: String): DataState<List<{Feature}>>` |
| Paginated fetch | `suspend fun get{Feature}sPaginated(limit, offset): DataState<{Feature}PageResponse>` |

**Why**: Ktorfit endpoints and Supabase SDK calls are one-shot HTTP requests. Wrapping them in a Flow adds unnecessary complexity.

### Use Flow (Only for Streaming / Observation)

| Scenario | Signature |
|----------|-----------|
| Supabase Realtime | `fun observe{Feature}s(): Flow<DataState<List<{Feature}>>>` |
| Room database observation | `fun observe{Feature}ById(id: String): Flow<DataState<{Feature}>>` |
| Combined cache + remote | `fun get{Feature}sStream(): Flow<DataState<List<{Feature}>>>` |
| WebSocket streams | `fun observe{Feature}Changes(): Flow<DataState<{Feature}Change>>` |

**Why**: These sources emit multiple values over time. A single suspend call cannot represent continuous updates.

### Flow Implementation in Repository

When a Flow-based method is needed, use `asDataStateFlow()` from ResultExtensions:

```kotlin
override fun observe{Feature}s(): Flow<DataState<List<{Feature}>>> =
    service.observe{Feature}s()           // Flow<NetworkResult<List<Dto>, NetworkError>>
        .asDataStateFlow()                // Flow<DataState<List<Dto>>> (emits Loading first)
        .map { state ->                   // Transform DTO to domain inside DataState
            state.map { dtos -> dtos.to{Feature}List() }
        }
```

For combined cache + remote patterns:

```kotlin
override fun get{Feature}sStream(): Flow<DataState<List<{Feature}>>> = flow {
    emit(DataState.Loading)

    // Emit from local cache first (if available)
    val cached = localDao.getAll()
    if (cached.isNotEmpty()) {
        emit(DataState.Pending(cached.toDomainList()))
    }

    // Then fetch fresh from network
    val result = api.get{Feature}s().toDataState().map { it.to{Feature}List() }
    emit(result)
}
```

---

## Example: MovieRepository

### Interface

```kotlin
package com.moodmovies.core.data.repository

import com.moodmovies.core.model.Movie
import template.core.base.common.DataState
import kotlinx.coroutines.flow.Flow

interface MovieRepository {
    suspend fun getMovies(): DataState<List<Movie>>
    suspend fun getMovieById(id: String): DataState<Movie>
    suspend fun getMoviesByMood(moodId: String, limit: Int, offset: Int): DataState<List<Movie>>
    suspend fun createMovie(request: CreateMovieRequest): DataState<Movie>
    suspend fun updateMovie(id: String, request: UpdateMovieRequest): DataState<Movie>
    suspend fun deleteMovie(id: String): DataState<Unit>

    // Flow only for real-time observation
    fun observeMovies(): Flow<DataState<List<Movie>>>
}
```

### Implementation (Ktorfit)

```kotlin
package com.moodmovies.core.data.repositoryImpl

import com.moodmovies.core.data.repository.MovieRepository
import com.moodmovies.core.data.util.toDataState
import com.moodmovies.core.data.mapper.toMovie
import com.moodmovies.core.data.mapper.toMovieList
import com.moodmovies.core.model.Movie
import com.moodmovies.core.network.service.movie.MovieApi
import template.core.base.common.DataState

class MovieRepositoryImpl(
    private val api: MovieApi,
) : MovieRepository {

    override suspend fun getMovies(): DataState<List<Movie>> =
        api.getMovies().toDataState().map { dtos -> dtos.toMovieList() }

    override suspend fun getMovieById(id: String): DataState<Movie> =
        api.getMovieById(id).toDataState().map { dto -> dto.toMovie() }

    override suspend fun getMoviesByMood(
        moodId: String,
        limit: Int,
        offset: Int,
    ): DataState<List<Movie>> =
        api.getMoviesByMood(moodId, limit, offset).toDataState().map { dtos ->
            dtos.toMovieList()
        }

    override suspend fun createMovie(request: CreateMovieRequest): DataState<Movie> =
        api.createMovie(request).toDataState().map { dto -> dto.toMovie() }

    override suspend fun updateMovie(
        id: String,
        request: UpdateMovieRequest,
    ): DataState<Movie> =
        api.updateMovie(id, request).toDataState().map { dto -> dto.toMovie() }

    override suspend fun deleteMovie(id: String): DataState<Unit> =
        api.deleteMovie(id).toDataState()
}
```

### Implementation (Supabase)

```kotlin
package com.moodmovies.core.data.repositoryImpl

import com.moodmovies.core.data.repository.MovieRepository
import com.moodmovies.core.data.util.toDataState
import com.moodmovies.core.data.mapper.toMovie
import com.moodmovies.core.data.mapper.toMovieList
import com.moodmovies.core.model.Movie
import com.moodmovies.core.network.service.movie.MovieService
import template.core.base.common.DataState

class MovieRepositoryImpl(
    private val service: MovieService,
) : MovieRepository {

    override suspend fun getMovies(): DataState<List<Movie>> =
        service.getMovies().toDataState().map { dtos -> dtos.toMovieList() }

    override suspend fun getMovieById(id: String): DataState<Movie> =
        service.getMovieById(id).toDataState().map { dto -> dto.toMovie() }

    override suspend fun getMoviesByMood(
        moodId: String,
        limit: Int,
        offset: Int,
    ): DataState<List<Movie>> =
        service.getMoviesByMood(moodId, limit, offset).toDataState().map { dtos ->
            dtos.toMovieList()
        }

    override suspend fun createMovie(request: CreateMovieRequest): DataState<Movie> =
        service.createMovie(request).toDataState().map { dto -> dto.toMovie() }

    override suspend fun updateMovie(
        id: String,
        request: UpdateMovieRequest,
    ): DataState<Movie> =
        service.updateMovie(id, request).toDataState().map { dto -> dto.toMovie() }

    override suspend fun deleteMovie(id: String): DataState<Unit> =
        service.deleteMovie(id).toDataState()
}
```

---

## DI Registration

### Using singleOf with bind (Recommended)

```kotlin
// In core/data/di/RepositoryModule.kt
val dataModule = module {
    singleOf(::{Feature}RepositoryImpl) bind {Feature}Repository::class
}
```

This pattern auto-resolves constructor parameters from Koin. The `bind` clause tells Koin to serve `{Feature}RepositoryImpl` when `{Feature}Repository` is requested.

### Full Example with Multiple Repositories

```kotlin
// core/data/di/RepositoryModule.kt
package {appPackage}.core.data.di

import org.koin.core.module.dsl.bind
import org.koin.core.module.dsl.singleOf
import org.koin.dsl.module
import {appPackage}.core.data.repository.*
import {appPackage}.core.data.repositoryImpl.*

val dataModule = module {
    singleOf(::MovieRepositoryImpl) bind MovieRepository::class
    singleOf(::UserRepositoryImpl) bind UserRepository::class
    singleOf(::MoodRepositoryImpl) bind MoodRepository::class
    singleOf(::GenreRepositoryImpl) bind GenreRepository::class
}
```

### Why No ioDispatcher

Ktor's HTTP client handles threading internally. Network calls are already performed on appropriate dispatchers inside Ktor. Injecting an `ioDispatcher` and wrapping calls in `withContext(ioDispatcher)` is unnecessary overhead. The repository stays clean with zero threading concerns.

---

## Paging Source Template

For paginated lists, use a PagingSource that also leverages `toDataState()` internally:

```kotlin
package {appPackage}.core.data.paging

import androidx.paging.PagingSource
import androidx.paging.PagingState
import {appPackage}.core.data.mapper.to{Feature}
import {appPackage}.core.model.{Feature}
import {appPackage}.core.network.service.{feature}.{Feature}Api
import template.core.base.network.NetworkResult

class {Feature}PagingSource(
    private val api: {Feature}Api,
) : PagingSource<Int, {Feature}>() {

    override fun getRefreshKey(state: PagingState<Int, {Feature}>): Int? {
        return state.anchorPosition?.let { anchorPosition ->
            state.closestPageToPosition(anchorPosition)?.prevKey?.plus(1)
                ?: state.closestPageToPosition(anchorPosition)?.nextKey?.minus(1)
        }
    }

    override suspend fun load(params: LoadParams<Int>): LoadResult<Int, {Feature}> {
        val page = params.key ?: 0

        return when (val result = api.get{Feature}sPaginated(limit = params.loadSize, offset = page * params.loadSize)) {
            is NetworkResult.Success -> {
                val items = result.data.items.map { it.to{Feature}() }
                LoadResult.Page(
                    data = items,
                    prevKey = if (page == 0) null else page - 1,
                    nextKey = if (items.isEmpty()) null else page + 1,
                )
            }
            is NetworkResult.Error -> {
                LoadResult.Error(Exception(result.error.name))
            }
        }
    }
}
```

Paging integration in the repository interface:

```kotlin
// In {Feature}Repository interface
fun get{Feature}PagingSource(): PagingSource<Int, {Feature}>

// In {Feature}RepositoryImpl
override fun get{Feature}PagingSource(): PagingSource<Int, {Feature}> =
    {Feature}PagingSource(api)
```

---

## Anti-Patterns (What NOT to Do)

### 1. Manual DataState Construction

```kotlin
// WRONG: Manual try-catch with DataState construction
override suspend fun get{Feature}ById(id: String): DataState<{Feature}> {
    return withContext(ioDispatcher) {
        try {
            val dto = service.get{Feature}ById(id)
            DataState.Success(dto.toDomainModel())
        } catch (e: Exception) {
            DataState.Error(e, e.message)
        }
    }
}

// CORRECT: One-liner with toDataState()
override suspend fun get{Feature}ById(id: String): DataState<{Feature}> =
    api.get{Feature}ById(id).toDataState().map { dto -> dto.to{Feature}() }
```

### 2. Flow Wrapping One-Shot Calls

```kotlin
// WRONG: Wrapping a one-shot HTTP call in Flow
override fun get{Feature}List(): Flow<DataState<List<{Feature}>>> {
    return flow {
        emit(DataState.Loading)
        val result = api.get{Feature}s()
        emit(result.toDataState().map { it.to{Feature}List() })
    }
}

// CORRECT: Use suspend for one-shot
override suspend fun get{Feature}s(): DataState<List<{Feature}>> =
    api.get{Feature}s().toDataState().map { dtos -> dtos.to{Feature}List() }
```

### 3. Injecting ioDispatcher (When Using NetworkResult Pipeline)

```kotlin
// WRONG (with NetworkResult pipeline): Unnecessary dispatcher injection
class {Feature}RepositoryImpl(
    private val api: {Feature}Api,
    private val ioDispatcher: CoroutineDispatcher,  // Not needed with NetworkResult
) : {Feature}Repository {
    override suspend fun get{Feature}s(): DataState<List<{Feature}>> {
        return withContext(ioDispatcher) {  // Ktor handles this
            api.get{Feature}s().toDataState().map { it.to{Feature}List() }
        }
    }
}

// CORRECT (with NetworkResult pipeline): No dispatcher, no withContext
class {Feature}RepositoryImpl(
    private val api: {Feature}Api,
) : {Feature}Repository {
    override suspend fun get{Feature}s(): DataState<List<{Feature}>> =
        api.get{Feature}s().toDataState().map { dtos -> dtos.to{Feature}List() }
}
```

> **Exemplar note**: The mobile-wallet exemplar injects `ioDispatcher` and uses
> `withContext(ioDispatcher)` / `flowOn(ioDispatcher)` because its services return raw
> types (not `NetworkResult`). When using the `toDataState()` pipeline with Ktorfit,
> Ktor handles threading internally and no dispatcher injection is needed.

### 4. Catch-Map-OnStart Flow Pattern

```kotlin
// WRONG: Verbose Flow operators for error handling
override fun get{Feature}List(): Flow<DataState<List<{Feature}>>> {
    return service.get{Feature}List()
        .map { DataState.Success(it.map { dto -> dto.toDomainModel() }) }
        .catch { emit(DataState.Error(it, it.message)) }
        .onStart { emit(DataState.Loading) }
        .flowOn(ioDispatcher)
}

// CORRECT: Use asDataStateFlow() for Flow-based sources
override fun observe{Feature}s(): Flow<DataState<List<{Feature}>>> =
    service.observe{Feature}s()
        .asDataStateFlow()
        .map { state -> state.map { dtos -> dtos.to{Feature}List() } }
```

---

## File Organization

```
core/data/src/commonMain/kotlin/{package}/core/data/
+-- di/
|   +-- RepositoryModule.kt          # Koin DI registration
+-- mapper/
|   +-- {Feature}Mapper.kt           # DTO-to-Domain extension functions (e.g., toModel(), toEntity())
+-- repository/
|   +-- {Feature}Repository.kt       # Interface (package: .repository)
+-- repositoryImpl/
|   +-- {Feature}RepositoryImpl.kt   # Implementation (package: .repositoryImpl)
+-- util/
    +-- ResultExtensions.kt           # toDataState() bridge (foundation, never regenerated)
```

> **Note**: Mappers live in `core/data/mapper/`, NOT `core/network/mapper/`. This matches the mobile-wallet exemplar where all mappers (e.g., `ClientDetailsMapper.kt`, `AccountMapper.kt`, `UserMapper.kt`) are in `core/data/src/commonMain/kotlin/.../core/data/mapper/`.

---

## Related Templates

| Template | Purpose |
|----------|---------|
| `SERVICE_TEMPLATE.kt.md` | Api/Service interface returning NetworkResult |
| `DTO_TEMPLATE.kt.md` | Data Transfer Objects |
| `MAPPER_TEMPLATE.kt.md` | DTO-to-Domain mapping extensions |
| `CLIENT_PATTERNS.md` | Full client layer architecture reference |
| `ERROR_HANDLING.md` | Comprehensive error handling pipeline |
