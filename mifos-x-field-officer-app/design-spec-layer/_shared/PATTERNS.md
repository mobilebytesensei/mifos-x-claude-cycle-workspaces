# template_meta
# template_version: "2.84.0"
# template_path: "templates/blueprints/workspace-project/design-spec-layer/_shared/PATTERNS.md"
# last_modified: "2026-03-20"

# Implementation Patterns

> **Purpose**: Shared implementation patterns used across all KMP projects.
> **Last Updated**: 2026-03-19
> **Sources**: mifos-mobile, mood-movies, byte-wallpaper, reels-downloader

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [MVI Pattern](#mvi-pattern)
3. [Service Pattern](#service-pattern)
4. [Repository Pattern](#repository-pattern)
5. [DataState Pattern](#datastate-pattern)
6. [Pagination Pattern](#pagination-pattern)
7. [Navigation Pattern](#navigation-pattern)
8. [Dialog Pattern](#dialog-pattern)
9. [Mapper Pattern](#mapper-pattern)
10. [DI Module Pattern](#di-module-pattern)
11. [Logging Pattern](#logging-pattern)
12. [Preview Pattern](#preview-pattern)
13. [Testing Pattern](#testing-pattern)

---

## Architecture Overview

### 2-Layer Architecture (DataManager Pattern)

```
┌─────────────────────────────────────────────────────────────────────┐
│  Feature Modules (UI + ViewModel)                                    │
│  MVI: State, Event, Action                                           │
└─────────────────────────────────────────────────────────────────────┘
                    ↓ Uses
┌─────────────────────────────────────────────────────────────────────┐
│  core/data - Repository Implementations                              │
│  Uses DataManager to access services, returns DataState<T>           │
└─────────────────────────────────────────────────────────────────────┘
                    ↓ Uses
┌─────────────────────────────────────────────────────────────────────┐
│  core/network - Services + DTOs (via DataManager)                    │
│  Ktorfit interfaces, Flow-based APIs                                 │
└─────────────────────────────────────────────────────────────────────┘
```

### 3-Layer Architecture (UseCase Pattern)

```
┌─────────────────────────────────────────────────────────────────────┐
│  Feature Modules (UI + ViewModel)                                    │
│  MVI: State, Event, Action                                           │
└─────────────────────────────────────────────────────────────────────┘
                    ↓ Uses
┌─────────────────────────────────────────────────────────────────────┐
│  core/domain - Use Cases                                             │
│  Single responsibility, invoke() operator, Paging support            │
└─────────────────────────────────────────────────────────────────────┘
                    ↓ Uses
┌─────────────────────────────────────────────────────────────────────┐
│  core/data - Repository Implementations                              │
│  Combines network + database, DTO→Domain mapping                     │
└─────────────────────────────────────────────────────────────────────┘
                    ↓ Uses
┌─────────────────────────────────────────────────────────────────────┐
│  core/network - Services + DTOs                                      │
│  Flow-based APIs, RPC calls                                          │
└─────────────────────────────────────────────────────────────────────┘
```

---

## MVI Pattern

### ViewModel Structure

```kotlin
internal class [Feature]ViewModel(
    private val repository: [Feature]Repository,
) : BaseViewModel<[Feature]State, [Feature]Event, [Feature]Action>(
    initialState = [Feature]State(),
) {
    init {
        loadData()
    }

    override fun handleAction(action: [Feature]Action) {
        when (action) {
            is [Feature]Action.OnItemClick -> {
                sendEvent([Feature]Event.NavigateToDetail(action.id))
            }
            is [Feature]Action.OnRefresh -> loadData()
        }
    }

    private fun loadData() {
        viewModelScope.launch {
            mutableStateFlow.update { it.copy(isLoading = true) }
            repository.getData().collect { result ->
                when (result) {
                    is DataState.Success -> {
                        mutableStateFlow.update {
                            it.copy(isLoading = false, items = result.data)
                        }
                    }
                    is DataState.Error -> {
                        mutableStateFlow.update {
                            it.copy(isLoading = false, error = result.error.message)
                        }
                    }
                    is DataState.Loading -> {
                        mutableStateFlow.update { it.copy(isLoading = true) }
                    }
                }
            }
        }
    }
}
```

### State, Event, Action

```kotlin
// State - UI state, collected via collectAsStateWithLifecycle()
@Immutable
data class [Feature]State(
    val items: List<Item> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null,
    val dialogState: DialogState? = null,
    val uiState: [Feature]ScreenState = [Feature]ScreenState.Loading,
)

// ScreenState - Loading/Success/Error states
sealed interface [Feature]ScreenState {
    data object Loading : [Feature]ScreenState
    data object Success : [Feature]ScreenState
    data object Empty : [Feature]ScreenState
    data class Error(val message: StringResource) : [Feature]ScreenState
}

// Event - One-shot navigation/effects, handled via EventsEffect()
sealed interface [Feature]Event {
    data class NavigateToDetail(val id: Long) : [Feature]Event
    data object NavigateBack : [Feature]Event
    data class ShowToast(val message: String) : [Feature]Event
}

// Action - User interactions, sent via viewModel.trySendAction()
sealed interface [Feature]Action {
    data class OnItemClick(val id: Long) : [Feature]Action
    data object OnRefresh : [Feature]Action
    data object OnRetry : [Feature]Action
    data object OnDismissDialog : [Feature]Action

    // Internal actions for async results
    sealed interface Internal : [Feature]Action {
        data class ReceiveData(val result: DataState<List<Item>>) : Internal
    }
}
```

### Screen Pattern (Container + Content)

```kotlin
@Composable
internal fun [Feature]Screen(
    onNavigateBack: () -> Unit,
    onNavigateToDetail: (Long) -> Unit,
    modifier: Modifier = Modifier,
    viewModel: [Feature]ViewModel = koinViewModel(),
) {
    val state by viewModel.stateFlow.collectAsStateWithLifecycle()

    EventsEffect(viewModel.eventFlow) { event ->
        when (event) {
            is [Feature]Event.NavigateToDetail -> onNavigateToDetail(event.id)
            is [Feature]Event.NavigateBack -> onNavigateBack()
        }
    }

    [Feature]ScreenContent(
        state = state,
        onAction = remember(viewModel) { { viewModel.trySendAction(it) } },
        modifier = modifier,
    )
}

@Composable
private fun [Feature]ScreenContent(
    state: [Feature]State,
    onAction: ([Feature]Action) -> Unit,
    modifier: Modifier = Modifier,
) {
    // Stateless, preview-able composable
}
```

---

## Service Pattern

### Ktorfit Interface Definition

```kotlin
@KtorfitApi
interface {{Feature}}Api {

    /**
     * Get list of items with pagination
     * @param limit Number of items per page
     * @param offset Starting position
     * @return Flow of paginated items
     */
    @GET("{{endpoint}}")
    fun get{{Feature}}List(
        @Query("limit") limit: Int = 20,
        @Query("offset") offset: Int = 0,
    ): Flow<List<{{Feature}}Dto>>

    /**
     * Get single item by ID
     * @param id Item identifier
     * @return Single item details
     */
    @GET("{{endpoint}}/{id}")
    suspend fun get{{Feature}}ById(
        @Path("id") id: Long,
    ): {{Feature}}Dto

    /**
     * Create new item
     * @param request Request payload
     * @return Created item or response
     */
    @POST("{{endpoint}}")
    suspend fun create{{Feature}}(
        @Body request: Create{{Feature}}Request,
    ): HttpResponse

    /**
     * Update existing item
     * @param id Item identifier
     * @param request Update payload
     * @return Updated item or response
     */
    @PUT("{{endpoint}}/{id}")
    suspend fun update{{Feature}}(
        @Path("id") id: Long,
        @Body request: Update{{Feature}}Request,
    ): HttpResponse

    /**
     * Delete item
     * @param id Item identifier
     * @return Response status
     */
    @DELETE("{{endpoint}}/{id}")
    suspend fun delete{{Feature}}(
        @Path("id") id: Long,
    ): HttpResponse
}
```

### DataManager Integration

```kotlin
class DataManager(
    private val preferenceManager: PreferenceManager,
    private val retrofitClient: RetrofitClient,
) {
    val {{feature}}Api: {{Feature}}Api by lazy {
        retrofitClient.{{feature}}Api
    }
}
```

---

## Repository Pattern

### Interface Definition

```kotlin
/**
 * Repository interface for {{Feature}} data operations.
 * Abstraction layer between data sources and domain layer.
 */
interface {{Feature}}Repository {

    /**
     * Get paginated list as Flow (for real-time updates)
     */
    fun get{{Feature}}List(): Flow<DataState<List<{{Feature}}>>>

    /**
     * Get single item by ID
     */
    suspend fun get{{Feature}}ById(id: Long): DataState<{{Feature}}>

    /**
     * Create new item
     */
    suspend fun create{{Feature}}(request: Create{{Feature}}Request): DataState<String>

    /**
     * Update existing item
     */
    suspend fun update{{Feature}}(id: Long, request: Update{{Feature}}Request): DataState<String>

    /**
     * Delete item
     */
    suspend fun delete{{Feature}}(id: Long): DataState<String>

    /**
     * Get paging source for Paging3 integration
     */
    fun get{{Feature}}PagingSource(): PagingSource<Int, {{Feature}}>
}
```

### Implementation

```kotlin
class {{Feature}}RepositoryImpl(
    private val dataManager: DataManager,
    private val ioDispatcher: CoroutineDispatcher,
) : {{Feature}}Repository {

    override fun get{{Feature}}List(): Flow<DataState<List<{{Feature}}>>> {
        return dataManager.{{feature}}Api.get{{Feature}}List()
            .map { dtoList ->
                DataState.Success(dtoList.map { it.toDomainModel() })
            }
            .catch { e ->
                emit(DataState.Error(e, e.message))
            }
            .flowOn(ioDispatcher)
    }

    override suspend fun get{{Feature}}ById(id: Long): DataState<{{Feature}}> {
        return withContext(ioDispatcher) {
            try {
                val dto = dataManager.{{feature}}Api.get{{Feature}}ById(id)
                DataState.Success(dto.toDomainModel())
            } catch (e: Exception) {
                DataState.Error(e, e.message)
            }
        }
    }

    override suspend fun create{{Feature}}(request: Create{{Feature}}Request): DataState<String> {
        return withContext(ioDispatcher) {
            try {
                val response = dataManager.{{feature}}Api.create{{Feature}}(request)
                if (response.status.isSuccess()) {
                    DataState.Success(response.bodyAsText())
                } else {
                    DataState.Error(
                        Exception("HTTP ${response.status.value}"),
                        extractErrorMessage(response)
                    )
                }
            } catch (e: ClientRequestException) {
                DataState.Error(e, extractErrorMessage(e.response))
            } catch (e: IOException) {
                DataState.Error(e, "Network error. Please check your connection.")
            }
        }
    }

    override suspend fun update{{Feature}}(id: Long, request: Update{{Feature}}Request): DataState<String> {
        return withContext(ioDispatcher) {
            try {
                val response = dataManager.{{feature}}Api.update{{Feature}}(id, request)
                if (response.status.isSuccess()) {
                    DataState.Success(response.bodyAsText())
                } else {
                    DataState.Error(
                        Exception("HTTP ${response.status.value}"),
                        extractErrorMessage(response)
                    )
                }
            } catch (e: Exception) {
                DataState.Error(e, e.message)
            }
        }
    }

    override suspend fun delete{{Feature}}(id: Long): DataState<String> {
        return withContext(ioDispatcher) {
            try {
                val response = dataManager.{{feature}}Api.delete{{Feature}}(id)
                if (response.status.isSuccess()) {
                    DataState.Success("Deleted successfully")
                } else {
                    DataState.Error(
                        Exception("HTTP ${response.status.value}"),
                        extractErrorMessage(response)
                    )
                }
            } catch (e: Exception) {
                DataState.Error(e, e.message)
            }
        }
    }

    private suspend fun extractErrorMessage(response: HttpResponse): String {
        return try {
            val errorBody = response.body<ErrorResponse>()
            errorBody.message ?: "Unknown error"
        } catch (e: Exception) {
            "Error ${response.status.value}: ${response.status.description}"
        }
    }
}
```

---

## Pagination Pattern

Two approaches exist depending on whether AndroidX Paging is a dependency:

| Approach | Library | Best For | Source |
|----------|---------|----------|--------|
| **Pager + PagingSource** | AndroidX Paging 3 | Large lists, infinite scroll | reels-downloader |
| **Manual PaginatedResult** | None (custom) | Simple APIs, no library dependency | byte-wallpaper |

### Approach A: Pager + PagingSource (AndroidX Paging)

**Critical Rule**:
```
UseCase: Creates Pager, returns Flow
ViewModel: Exposes Flow directly (NO stateIn!)
Screen: Collects as LazyPagingItems
```

#### PagingSource Implementation

```kotlin
class [Feature]PagingSource(
    private val repository: [Feature]Repository,
) : PagingSource<Int, [Feature]>() {

    override suspend fun load(params: LoadParams<Int>): LoadResult<Int, [Feature]> {
        return try {
            val page = params.key ?: INITIAL_PAGE
            val pageSize = params.loadSize
            val offset = page * pageSize

            when (val result = repository.getItems(limit = pageSize, offset = offset)) {
                is DataState.Success -> {
                    val items = result.data
                    LoadResult.Page(
                        data = items,
                        prevKey = if (page == INITIAL_PAGE) null else page - 1,
                        nextKey = if (items.size < pageSize) null else page + 1,
                    )
                }
                is DataState.Error -> LoadResult.Error(result.error)
                else -> LoadResult.Error(Exception("Unexpected state"))
            }
        } catch (e: Exception) {
            LoadResult.Error(e)
        }
    }

    override fun getRefreshKey(state: PagingState<Int, [Feature]>): Int? {
        return state.anchorPosition?.let { anchorPosition ->
            val anchorPage = state.closestPageToPosition(anchorPosition)
            anchorPage?.prevKey?.plus(1) ?: anchorPage?.nextKey?.minus(1)
        }
    }

    companion object {
        private const val INITIAL_PAGE = 0
    }
}
```

#### UseCase with Pager

```kotlin
class Get[Feature]FlowUseCase(
    private val repository: [Feature]Repository,
) {
    operator fun invoke(): Flow<PagingData<[Feature]>> {
        return Pager(
            config = PagingConfig(
                pageSize = PAGE_SIZE,
                prefetchDistance = PREFETCH_DISTANCE,
                enablePlaceholders = false,
                initialLoadSize = INITIAL_LOAD_SIZE,
            ),
            pagingSourceFactory = { [Feature]PagingSource(repository) },
        ).flow
    }

    companion object {
        private const val PAGE_SIZE = 20
        private const val PREFETCH_DISTANCE = 5
        private const val INITIAL_LOAD_SIZE = 20
    }
}
```

#### ViewModel with Paging

```kotlin
internal class [Feature]ViewModel(
    private val getItemsUseCase: Get[Feature]FlowUseCase,
) : BaseViewModel<[Feature]State, [Feature]Event, [Feature]Action>(...) {

    // Direct flow exposure - NO stateIn!
    val items: Flow<PagingData<[Feature]>> = getItemsUseCase()
}
```

#### Screen with Paging

```kotlin
@Composable
fun [Feature]Screen(viewModel: [Feature]ViewModel = koinViewModel()) {
    val items = viewModel.items.collectAsLazyPagingItems()

    LazyColumn {
        items(
            count = items.itemCount,
            key = items.itemKey { it.id },
        ) { index ->
            items[index]?.let { item ->
                ItemCard(item = item)
            }
        }

        // Handle loading states
        when (items.loadState.refresh) {
            is LoadState.Loading -> item { LoadingIndicator() }
            is LoadState.Error -> item { ErrorMessage() }
            else -> {}
        }
    }
}
```

### Approach B: Manual PaginatedResult (No Library)

For simpler use cases or when AndroidX Paging is not a dependency.

#### Data Models

```kotlin
data class PaginatedResult<T>(
    val data: List<T>,
    val currentPage: Int,
    val hasMore: Boolean,
    val totalLoaded: Int,
)

data class PaginationState(
    val currentPage: Int = 0,
    val pageSize: Int = DEFAULT_PAGE_SIZE,
    val isLoading: Boolean = false,
    val hasMore: Boolean = true,
    val error: String? = null,
) {
    val nextOffset: Int get() = currentPage * pageSize

    companion object {
        const val DEFAULT_PAGE_SIZE = 30
    }
}
```

#### UseCase with Manual Pagination

```kotlin
class GetPaginated[Feature]UseCase(
    private val repository: [Feature]Repository,
) {
    suspend fun loadPage(
        paginationState: PaginationState,
    ): PaginatedResult<[Feature]> {
        val items = repository.getItems(
            offset = paginationState.nextOffset,
            limit = paginationState.pageSize,
        )

        return PaginatedResult(
            data = items,
            currentPage = paginationState.currentPage,
            hasMore = items.size >= paginationState.pageSize,
            totalLoaded = paginationState.nextOffset + items.size,
        )
    }
}
```

#### ViewModel with Manual Pagination

```kotlin
internal class [Feature]ViewModel(
    private val getPaginatedUseCase: GetPaginated[Feature]UseCase,
) : BaseViewModel<[Feature]State, [Feature]Event, [Feature]Action>(...) {

    override fun handleAction(action: [Feature]Action) {
        when (action) {
            is [Feature]Action.OnLoadMore -> loadNextPage()
            // ...
        }
    }

    private fun loadNextPage() {
        val pagination = state.paginationState
        if (pagination.isLoading || !pagination.hasMore) return

        viewModelScope.launch {
            mutableStateFlow.update {
                it.copy(paginationState = pagination.copy(isLoading = true))
            }
            try {
                val result = getPaginatedUseCase.loadPage(pagination)
                mutableStateFlow.update {
                    it.copy(
                        items = it.items + result.data,
                        paginationState = pagination.copy(
                            currentPage = pagination.currentPage + 1,
                            isLoading = false,
                            hasMore = result.hasMore,
                        ),
                    )
                }
            } catch (e: Exception) {
                mutableStateFlow.update {
                    it.copy(
                        paginationState = pagination.copy(
                            isLoading = false,
                            error = e.message,
                        ),
                    )
                }
            }
        }
    }
}
```

---

## DataState Pattern

### Definition

```kotlin
sealed class DataState<out T> {
    data class Success<T>(val data: T) : DataState<T>()
    data class Error(val error: Throwable, val message: String?) : DataState<Nothing>()
    data object Loading : DataState<Nothing>()
}
```

> **Variant note**: The canonical template defines 5 states (`Loading`, `Success`, `Pending`,
> `Error`, `NoNetwork`) for maximum flexibility. Some production apps simplify to the 3 states
> shown above when `Pending` and `NoNetwork` are not needed. The `Error` variant uses a field
> named `error` (not `exception`) to hold the `Throwable` -- this is the canonical name across
> all reference projects. Templates use the full 5-state model; projects may reduce as appropriate.

### Usage in Repository

```kotlin
// Flow-based GET
override fun get[Feature]List(): Flow<DataState<List<Entity>>> {
    return dataManager.[feature]Api.get[Feature]List()
        .map { DataState.Success(it) }
        .catch { emit(DataState.Error(it, null)) }
        .flowOn(ioDispatcher)
}

// Suspend-based POST/PUT/DELETE
override suspend fun create[Feature](payload: Payload?): DataState<String> {
    return withContext(ioDispatcher) {
        try {
            val response = dataManager.[feature]Api.create[Feature](payload)
            DataState.Success(response.bodyAsText())
        } catch (e: ClientRequestException) {
            DataState.Error(e, extractErrorMessage(e.response))
        } catch (e: IOException) {
            DataState.Error(e, "Network error")
        }
    }
}
```

### NetworkResult -> DataState Bridge

The bridge between the network layer (`NetworkResult`) and the UI layer (`DataState`).
Located in `core/data/util/ResultExtensions.kt`.

#### RemoteException (Error Wrapper)

```kotlin
/** Custom exception class that wraps a NetworkError with user-friendly messages */
class RemoteException(
    val networkError: NetworkError,
    message: String = networkError.name,
) : Exception(message)

fun NetworkError.toThrowable(): Throwable = when (this) {
    NetworkError.BAD_REQUEST -> RemoteException(this, "Something went wrong with your request. Please try again.")
    NetworkError.NOT_FOUND -> RemoteException(this, "The information you're looking for couldn't be found.")
    NetworkError.UNAUTHORIZED -> RemoteException(this, "You need to sign in to access this content.")
    NetworkError.REQUEST_TIMEOUT -> RemoteException(this, "The request is taking too long. Please check your connection and try again.")
    NetworkError.TOO_MANY_REQUESTS -> RemoteException(this, "You're doing that too often. Please wait a moment and try again.")
    NetworkError.SERVER -> RemoteException(this, "We're experiencing technical difficulties. Please try again later.")
    NetworkError.SERIALIZATION -> RemoteException(this, "We received unexpected data. Please try refreshing the app.")
    NetworkError.UNKNOWN -> RemoteException(this, "Something unexpected happened. Please try again.")
}
```

#### Single Result Conversion

```kotlin
/** Simple conversion: Success -> Success, Error -> Error */
fun <D> NetworkResult<D, *>.toDataState(): DataState<D> = when (this) {
    is NetworkResult.Success -> DataState.Success(data)
    is NetworkResult.Error -> DataState.Error(error.toThrowable(), null)
}

/** Conversion with existing data preserved (show stale data on error) */
fun <D> NetworkResult<D, *>.toDataState(existingData: D?): DataState<D> = when (this) {
    is NetworkResult.Success -> DataState.Success(data)
    is NetworkResult.Error -> DataState.Error(error.toThrowable(), existingData)
}

/** Smart conversion that maps certain errors to specific DataState types */
fun <D> NetworkResult<D, *>.toDataStateWithMapping(): DataState<D> = when (this) {
    is NetworkResult.Success -> DataState.Success(data)
    is NetworkResult.Error -> when (error) {
        NetworkError.REQUEST_TIMEOUT -> DataState.NoNetwork(null)
        else -> DataState.Error(error.toThrowable(), null)
    }
}
```

#### Flow Conversion (NetworkResult Flows)

**Important**: This is distinct from `Flow<T>.asDataStateFlow()` (which wraps raw data flows).
This overload converts `Flow<NetworkResult<D, *>>` to `Flow<DataState<D>>`.

```kotlin
/** Convert Flow<NetworkResult> to Flow<DataState> with automatic Loading emission */
fun <D> Flow<NetworkResult<D, *>>.asDataStateFlow(): Flow<DataState<D>> =
    map { it.toDataState() }
        .onStart { emit(DataState.Loading) }

/** Convert Flow<NetworkResult> with existing data preservation on error */
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

#### Utility Extensions

```kotlin
/** Check if DataState represents a successful state */
val <T> DataState<T>.isSuccess: Boolean
    get() = this is DataState.Success

/** Check if DataState represents an error state */
val <T> DataState<T>.isError: Boolean
    get() = this is DataState.Error

/** Get the error if DataState is in error state */
val <T> DataState<T>.errorOrNull: Throwable?
    get() = (this as? DataState.Error)?.error

/** Get the original NetworkError if the error is a RemoteException */
val <T> DataState<T>.networkErrorOrNull: NetworkError?
    get() = (this as? DataState.Error)?.error?.let { error ->
        (error as? RemoteException)?.networkError
    }
```

> **Extension naming note**: The canonical names are `takeUntilSuccess()` and
> `combineDataStates()`. Some production apps rename these (e.g., `takeUntilResultSuccess()`,
> `combineResults()`). Templates use the canonical names for consistency across projects.

---

## Logging Pattern

```kotlin
import co.touchlab.kermit.Logger

private val logger = Logger.withTag("[Feature]ViewModel")

// Usage
logger.d { "Loading data with id: $id" }
logger.i { "Data loaded successfully: ${items.size} items" }
logger.w { "Cache miss, fetching from network" }
logger.e(exception) { "Failed to load data" }
```

---

## Preview Pattern

### All Components Must Have Previews

```kotlin
@Preview
@Composable
private fun [Feature]ScreenContentPreview() {
    AppTheme {
        [Feature]ScreenContent(
            state = [Feature]State(
                items = listOf(
                    Item(1, "Item 1"),
                    Item(2, "Item 2"),
                ),
                uiState = [Feature]ScreenState.Success,
            ),
            onAction = {},
        )
    }
}

@Preview
@Composable
private fun [Feature]LoadingPreview() {
    AppTheme {
        [Feature]LoadingContent()
    }
}

@Preview
@Composable
private fun [Feature]ErrorPreview() {
    AppTheme {
        MifosErrorComponent(
            message = "Failed to load data",
            onRetry = {},
        )
    }
}
```

---

## Navigation Pattern

> **Two valid navigation trigger patterns exist:**
>
> - **Pattern A: Callbacks** -- Navigation lambdas passed through composable parameters
>   (e.g., `onNavigateBack: () -> Unit`). Best for simple, direct navigation like "go back".
> - **Pattern B: Events via sealed interface** -- ViewModel emits events consumed by `EventsEffect`
>   (e.g., `sendEvent(NavigateToDetail(id))`). Best for navigation that involves business logic
>   (e.g., "save data, then navigate on success").
>
> Both are valid and commonly used together in the same screen. Callbacks wire the nav graph;
> events handle navigation triggered by ViewModel logic.

### Navigation Graph Structure

```kotlin
@Composable
fun {{Feature}}NavHost(
    navController: NavHostController,
    startDestination: String = {{Feature}}Route.List.route,
) {
    NavHost(
        navController = navController,
        startDestination = startDestination,
    ) {
        {{feature}}ListScreen(
            onNavigateToDetail = { id ->
                navController.navigate({{Feature}}Route.Detail(id))
            },
            onNavigateToCreate = {
                navController.navigate({{Feature}}Route.Create)
            },
        )

        {{feature}}DetailScreen(
            onNavigateBack = { navController.popBackStack() },
            onNavigateToEdit = { id ->
                navController.navigate({{Feature}}Route.Edit(id))
            },
        )

        {{feature}}CreateScreen(
            onNavigateBack = { navController.popBackStack() },
            onSuccess = { id ->
                navController.navigate({{Feature}}Route.Detail(id)) {
                    popUpTo({{Feature}}Route.List.route)
                }
            },
        )

        {{feature}}EditScreen(
            onNavigateBack = { navController.popBackStack() },
            onSuccess = { navController.popBackStack() },
        )
    }
}
```

### Type-Safe Route Definition

```kotlin
sealed class {{Feature}}Route(val route: String) {
    data object List : {{Feature}}Route("{{feature}}_list")
    data class Detail(val id: Long) : {{Feature}}Route("{{feature}}_detail/{id}") {
        companion object {
            const val ROUTE = "{{feature}}_detail/{id}"
            const val ARG_ID = "id"
        }
    }
    data object Create : {{Feature}}Route("{{feature}}_create")
    data class Edit(val id: Long) : {{Feature}}Route("{{feature}}_edit/{id}") {
        companion object {
            const val ROUTE = "{{feature}}_edit/{id}"
            const val ARG_ID = "id"
        }
    }
}
```

### Deep Link Support

```kotlin
fun NavGraphBuilder.{{feature}}DetailScreen(
    onNavigateBack: () -> Unit,
    onNavigateToEdit: (Long) -> Unit,
) {
    composable(
        route = {{Feature}}Route.Detail.ROUTE,
        arguments = listOf(
            navArgument({{Feature}}Route.Detail.ARG_ID) {
                type = NavType.LongType
            }
        ),
        deepLinks = listOf(
            navDeepLink {
                uriPattern = "{{app_scheme}}://{{feature}}/{id}"
            }
        ),
    ) { backStackEntry ->
        val id = backStackEntry.arguments?.getLong({{Feature}}Route.Detail.ARG_ID) ?: return@composable

        {{Feature}}DetailScreen(
            id = id,
            onNavigateBack = onNavigateBack,
            onNavigateToEdit = onNavigateToEdit,
        )
    }
}
```

### Conditional Navigation (ADD/UPDATE Mode)

```kotlin
sealed interface {{Feature}}Mode {
    data object Add : {{Feature}}Mode
    data class Update(val id: Long) : {{Feature}}Mode
}

@Composable
fun {{Feature}}FormScreen(
    mode: {{Feature}}Mode,
    onNavigateBack: () -> Unit,
    onSuccess: () -> Unit,
    viewModel: {{Feature}}FormViewModel = koinViewModel { parametersOf(mode) },
) {
    val state by viewModel.stateFlow.collectAsStateWithLifecycle()

    // Form handles both modes based on viewModel state
    {{Feature}}FormContent(
        state = state,
        isEditMode = mode is {{Feature}}Mode.Update,
        onAction = viewModel::trySendAction,
    )
}
```

---

## Dialog Pattern

### Dialog State in Screen State

```kotlin
@Immutable
data class {{Feature}}State(
    val items: List<Item> = emptyList(),
    val isLoading: Boolean = false,
    val dialogState: {{Feature}}DialogState? = null,
)

sealed interface {{Feature}}DialogState {
    data class DeleteConfirmation(val item: Item) : {{Feature}}DialogState
    data class Error(val message: StringResource) : {{Feature}}DialogState
    data object Success : {{Feature}}DialogState
}
```

### Dialog Actions

```kotlin
sealed interface {{Feature}}Action {
    // ... other actions ...

    // Dialog actions
    data class OnDeleteClick(val item: Item) : {{Feature}}Action
    data object OnDismissDialog : {{Feature}}Action
    data object OnConfirmDelete : {{Feature}}Action
}
```

### Dialog Rendering in Screen

```kotlin
@Composable
private fun {{Feature}}ScreenContent(
    state: {{Feature}}State,
    onAction: ({{Feature}}Action) -> Unit,
) {
    // Main content...

    // Dialog handling
    state.dialogState?.let { dialogState ->
        when (dialogState) {
            is {{Feature}}DialogState.DeleteConfirmation -> {
                DeleteConfirmationDialog(
                    itemName = dialogState.item.name,
                    onConfirm = { onAction({{Feature}}Action.OnConfirmDelete) },
                    onDismiss = { onAction({{Feature}}Action.OnDismissDialog) },
                )
            }
            is {{Feature}}DialogState.Error -> {
                ErrorDialog(
                    message = stringResource(dialogState.message),
                    onDismiss = { onAction({{Feature}}Action.OnDismissDialog) },
                )
            }
            is {{Feature}}DialogState.Success -> {
                SuccessDialog(
                    onDismiss = { onAction({{Feature}}Action.OnDismissDialog) },
                )
            }
        }
    }
}
```

### Delete Confirmation Dialog Component

```kotlin
@Composable
fun DeleteConfirmationDialog(
    itemName: String,
    onConfirm: () -> Unit,
    onDismiss: () -> Unit,
) {
    AlertDialog(
        onDismissRequest = onDismiss,
        icon = {
            Icon(
                imageVector = Icons.Default.Delete,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.error,
            )
        },
        title = {
            Text("Delete Item?")
        },
        text = {
            Text("Are you sure you want to delete \"$itemName\"? This action cannot be undone.")
        },
        confirmButton = {
            TextButton(
                onClick = onConfirm,
                colors = ButtonDefaults.textButtonColors(
                    contentColor = MaterialTheme.colorScheme.error,
                ),
            ) {
                Text("Delete")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Cancel")
            }
        },
    )
}
```

---

## Mapper Pattern

### DTO to Domain Model

```kotlin
/**
 * Data Transfer Object from API
 */
@Serializable
data class {{Feature}}Dto(
    @SerialName("id") val id: Long,
    @SerialName("name") val name: String,
    @SerialName("description") val description: String?,
    @SerialName("created_at") val createdAt: String,
    @SerialName("updated_at") val updatedAt: String?,
    @SerialName("is_active") val isActive: Boolean = true,
    @SerialName("metadata") val metadata: MetadataDto? = null,
)

/**
 * Domain model used in business logic
 */
data class {{Feature}}(
    val id: Long,
    val name: String,
    val description: String?,
    val createdAt: LocalDateTime,
    val updatedAt: LocalDateTime?,
    val isActive: Boolean,
    val metadata: Metadata?,
)

/**
 * Extension function for DTO → Domain mapping
 */
fun {{Feature}}Dto.toDomainModel(): {{Feature}} = {{Feature}}(
    id = id,
    name = name,
    description = description,
    createdAt = createdAt.toLocalDateTime(),
    updatedAt = updatedAt?.toLocalDateTime(),
    isActive = isActive,
    metadata = metadata?.toDomainModel(),
)

/**
 * Extension function for Domain → DTO mapping (for POST/PUT)
 */
fun {{Feature}}.toDto(): {{Feature}}Dto = {{Feature}}Dto(
    id = id,
    name = name,
    description = description,
    createdAt = createdAt.toIsoString(),
    updatedAt = updatedAt?.toIsoString(),
    isActive = isActive,
    metadata = metadata?.toDto(),
)
```

### Alternative: AbstractMapper Pattern

For projects that prefer class-based mappers with bidirectional mapping enforced at the type
level (e.g., byte-wallpaper). Useful when mapping between Entity (database) and Domain models.

```kotlin
interface EntityMapper<Entity, DomainModel> {
    fun mapFromEntity(entity: Entity): DomainModel
    fun mapToEntity(domainModel: DomainModel): Entity
    fun mapFromEntityList(entities: List<Entity>): List<DomainModel>
    fun mapToEntityList(domainModels: List<DomainModel>): List<Entity>
}

abstract class AbstractMapper<Entity, DomainModel> : EntityMapper<Entity, DomainModel> {
    override fun mapFromEntityList(entities: List<Entity>): List<DomainModel> =
        entities.map { mapFromEntity(it) }

    override fun mapToEntityList(domainModels: List<DomainModel>): List<Entity> =
        domainModels.map { mapToEntity(it) }
}

// Usage: singleton mapper object
object {{Feature}}Mapper : AbstractMapper<{{Feature}}Entity, {{Feature}}>() {
    override fun mapFromEntity(entity: {{Feature}}Entity): {{Feature}} = {{Feature}}(
        id = entity.id,
        name = entity.name,
        // ...
    )

    override fun mapToEntity(domainModel: {{Feature}}): {{Feature}}Entity = {{Feature}}Entity(
        id = domainModel.id,
        name = domainModel.name,
        // ...
    )
}
```

**When to use which**:
- **Extension functions** (preferred): Simple, idiomatic Kotlin, no boilerplate. Best for DTO-to-Domain mapping.
- **AbstractMapper**: Enforces bidirectional mapping contract. Best for Entity-to-Domain when both directions are always needed (e.g., database caching).

### Request/Response Models

```kotlin
/**
 * Request model for creating new item
 */
@Serializable
data class Create{{Feature}}Request(
    @SerialName("name") val name: String,
    @SerialName("description") val description: String? = null,
    @SerialName("metadata") val metadata: MetadataDto? = null,
)

/**
 * Request model for updating item
 */
@Serializable
data class Update{{Feature}}Request(
    @SerialName("name") val name: String? = null,
    @SerialName("description") val description: String? = null,
    @SerialName("is_active") val isActive: Boolean? = null,
)

/**
 * Standard error response
 */
@Serializable
data class ErrorResponse(
    @SerialName("error") val error: String? = null,
    @SerialName("message") val message: String? = null,
    @SerialName("code") val code: Int? = null,
)
```

### DateTime Utilities

```kotlin
/**
 * Parse ISO 8601 string to LocalDateTime
 */
fun String.toLocalDateTime(): LocalDateTime {
    return try {
        LocalDateTime.parse(this)
    } catch (e: Exception) {
        // Fallback for different formats
        Instant.parse(this).toLocalDateTime(TimeZone.currentSystemDefault())
    }
}

/**
 * Convert LocalDateTime to ISO 8601 string
 */
fun LocalDateTime.toIsoString(): String {
    return this.toInstant(TimeZone.currentSystemDefault()).toString()
}
```

---

## DI Module Pattern

### Feature Module with Koin

```kotlin
val {{feature}}Module = module {
    // Services (if not in DataManager)
    single<{{Feature}}Api> { get<RetrofitClient>().{{feature}}Api }

    // Repository
    single<{{Feature}}Repository> {
        {{Feature}}RepositoryImpl(
            dataManager = get(),
            ioDispatcher = get(named("IoDispatcher")),
        )
    }

    // Use Cases (if 3-layer architecture)
    factory { Get{{Feature}}ListUseCase(repository = get()) }
    factory { Get{{Feature}}ByIdUseCase(repository = get()) }
    factory { Create{{Feature}}UseCase(repository = get()) }
    factory { Update{{Feature}}UseCase(repository = get()) }
    factory { Delete{{Feature}}UseCase(repository = get()) }

    // ViewModels
    viewModel { {{Feature}}ListViewModel(repository = get()) }
    viewModel { parameters ->
        {{Feature}}DetailViewModel(
            id = parameters.get(),
            repository = get(),
        )
    }
    viewModel { parameters ->
        {{Feature}}FormViewModel(
            mode = parameters.get(),
            repository = get(),
        )
    }
}
```

### Registering Module in Application

```kotlin
// In KoinConfiguration.kt or similar
val appModules = listOf(
    coreModule,
    networkModule,
    databaseModule,
    // Feature modules
    homeModule,
    {{feature}}Module,
    profileModule,
    settingsModule,
)

// In Application.kt
startKoin {
    androidContext(this@MainApplication)
    modules(appModules)
}
```

### ViewModel with Parameters

```kotlin
internal class {{Feature}}DetailViewModel(
    private val id: Long,
    private val repository: {{Feature}}Repository,
) : BaseViewModel<{{Feature}}DetailState, {{Feature}}DetailEvent, {{Feature}}DetailAction>(
    initialState = {{Feature}}DetailState(),
) {
    init {
        loadItem(id)
    }
}

// In NavGraph
composable(...) { backStackEntry ->
    val id = backStackEntry.arguments?.getLong("id") ?: return@composable
    val viewModel: {{Feature}}DetailViewModel = koinViewModel { parametersOf(id) }
    // ...
}
```

---

## Testing Pattern

### Fake Repository

```kotlin
class Fake{{Feature}}Repository : {{Feature}}Repository {

    private val items = mutableListOf<{{Feature}}>()
    private val itemsFlow = MutableStateFlow<List<{{Feature}}>>(emptyList())

    var shouldReturnError = false
    var errorMessage = "Test error"

    fun setItems(newItems: List<{{Feature}}>) {
        items.clear()
        items.addAll(newItems)
        itemsFlow.value = newItems.toList()
    }

    override fun get{{Feature}}List(): Flow<DataState<List<{{Feature}}>>> = flow {
        if (shouldReturnError) {
            emit(DataState.Error(Exception(errorMessage), errorMessage))
        } else {
            emit(DataState.Success(items.toList()))
        }
    }

    override suspend fun get{{Feature}}ById(id: Long): DataState<{{Feature}}> {
        if (shouldReturnError) {
            return DataState.Error(Exception(errorMessage), errorMessage)
        }
        val item = items.find { it.id == id }
        return if (item != null) {
            DataState.Success(item)
        } else {
            DataState.Error(Exception("Item not found"), "Item not found")
        }
    }

    override suspend fun create{{Feature}}(request: Create{{Feature}}Request): DataState<String> {
        if (shouldReturnError) {
            return DataState.Error(Exception(errorMessage), errorMessage)
        }
        val newId = (items.maxOfOrNull { it.id } ?: 0) + 1
        items.add(/* create item from request */)
        return DataState.Success(newId.toString())
    }

    // ... other implementations
}
```

### ViewModel Test

```kotlin
class {{Feature}}ViewModelTest {

    private lateinit var viewModel: {{Feature}}ViewModel
    private val fakeRepository = Fake{{Feature}}Repository()

    @BeforeTest
    fun setup() {
        viewModel = {{Feature}}ViewModel(repository = fakeRepository)
    }

    @Test
    fun `initial state shows loading then success`() = runTest {
        // Given
        val testItems = listOf(
            {{Feature}}(id = 1, name = "Item 1"),
            {{Feature}}(id = 2, name = "Item 2"),
        )
        fakeRepository.setItems(testItems)

        // When
        viewModel = {{Feature}}ViewModel(repository = fakeRepository)

        // Then
        viewModel.stateFlow.test {
            val loadingState = awaitItem()
            assertTrue(loadingState.isLoading)

            val successState = awaitItem()
            assertFalse(successState.isLoading)
            assertEquals(2, successState.items.size)
        }
    }

    @Test
    fun `error state when repository fails`() = runTest {
        // Given
        fakeRepository.shouldReturnError = true
        fakeRepository.errorMessage = "Network error"

        // When
        viewModel = {{Feature}}ViewModel(repository = fakeRepository)

        // Then
        viewModel.stateFlow.test {
            skipItems(1) // Skip loading
            val errorState = awaitItem()
            assertNotNull(errorState.error)
            assertEquals("Network error", errorState.error)
        }
    }

    @Test
    fun `item click sends navigation event`() = runTest {
        // Given
        fakeRepository.setItems(listOf({{Feature}}(id = 42, name = "Test")))
        viewModel = {{Feature}}ViewModel(repository = fakeRepository)

        // When
        viewModel.trySendAction({{Feature}}Action.OnItemClick(42))

        // Then
        viewModel.eventFlow.test {
            val event = awaitItem()
            assertIs<{{Feature}}Event.NavigateToDetail>(event)
            assertEquals(42, event.id)
        }
    }
}
```

### TestTags Pattern

```kotlin
object {{Feature}}TestTags {
    private const val PREFIX = "{{feature}}"

    // Screen
    const val SCREEN = "${PREFIX}_screen"

    // List
    const val LIST = "${PREFIX}_list"
    const val LIST_ITEM = "${PREFIX}_list_item"

    // Empty state
    const val EMPTY_STATE = "${PREFIX}_empty_state"
    const val EMPTY_STATE_TITLE = "${PREFIX}_empty_state_title"
    const val EMPTY_STATE_BUTTON = "${PREFIX}_empty_state_button"

    // Loading
    const val LOADING_INDICATOR = "${PREFIX}_loading_indicator"
    const val LOADING_SKELETON = "${PREFIX}_loading_skeleton"

    // Error
    const val ERROR_STATE = "${PREFIX}_error_state"
    const val RETRY_BUTTON = "${PREFIX}_retry_button"

    // Actions
    const val FAB = "${PREFIX}_fab"
    const val DELETE_BUTTON = "${PREFIX}_delete_button"
    const val EDIT_BUTTON = "${PREFIX}_edit_button"

    // Form
    const val NAME_INPUT = "${PREFIX}_name_input"
    const val DESCRIPTION_INPUT = "${PREFIX}_description_input"
    const val SUBMIT_BUTTON = "${PREFIX}_submit_button"
}
```

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| `instructions/feature-layer/VIEWMODEL.md` | Detailed ViewModel patterns |
| `instructions/feature-layer/COMPOSE.md` | Compose UI patterns |
| `instructions/feature-layer/NAVIGATION.md` | Navigation patterns |
| `instructions/feature-layer/DI.md` | Koin DI patterns |
| `instructions/client-layer/CLIENT_PATTERNS.md` | Service/Repository patterns |
| `instructions/testing-layer/*.md` | Testing patterns |
| `_shared/COMPONENTS.md` | UI component specifications |
| `_shared/USER_FLOWS.md` | App navigation flows |

---

## Version History

| Date | Change |
|------|--------|
| 2026-03-19 | Added dual pagination (Pager + PaginatedResult), full NetworkResult->DataState bridge, AbstractMapper alternative |
| 2026-03-19 | Added Service, Repository, Navigation, Dialog, Mapper, DI, Testing patterns |
