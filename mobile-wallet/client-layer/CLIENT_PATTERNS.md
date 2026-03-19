# template_meta
# template_version: "2.81.0"
# template_path: "templates/blueprints/workspace-project/client-layer/CLIENT_PATTERNS.md"
# last_modified: "2026-03-19"

# Client Layer Patterns - mobile-wallet

> Client layer patterns for mobile-wallet. See framework templates for detailed documentation.

---

## Architecture

```
HTTP Response
    ↓ (ResultSuspendConverterFactory — automatic for REST)
NetworkResult<T, NetworkError>          ← Network boundary
    ↓ (ResultExtensions.toDataState() — in repository)
DataState<T>                            ← UI boundary
    ↓ (ViewModel StateFlow)
Compose UI
```

---

## Service Pattern

### REST (Ktorfit)

```kotlin
interface {Feature}Api {
    @GET("{endpoint}")
    suspend fun get{Feature}s(): NetworkResult<List<{Feature}Dto>, NetworkError>
}
```

### Supabase

```kotlin
interface {Feature}Service {
    suspend fun get{Feature}s(): NetworkResult<List<{Feature}Dto>, NetworkError>
}

class {Feature}ServiceImpl(private val client: SupabaseClient) : {Feature}Service {
    override suspend fun get{Feature}s(): NetworkResult<List<{Feature}Dto>, NetworkError> =
        try {
            NetworkResult.Success(client.postgrest.from("{table}").select().decodeList())
        } catch (e: Exception) {
            NetworkResult.Error(e.toNetworkError())
        }
}
```

---

## Repository Pattern

```kotlin
class {Feature}RepositoryImpl(
    private val api: {Feature}Api,
) : {Feature}Repository {
    override suspend fun get{Feature}s(): DataState<List<{Feature}>> =
        api.get{Feature}s().toDataState().map { dtos -> dtos.to{Feature}List() }
}
```

---

## DataState (5 States)

| State | When Used | Has Data? |
|-------|-----------|:---------:|
| `Loading` | Initial fetch | No |
| `Success<T>` | Fetched successfully | Yes |
| `Pending<T>` | Refreshing with stale data | Yes (stale) |
| `Error<T>` | Request failed | Optional |
| `NoNetwork<T>` | Device offline | Optional |

---

## DI Modules

| Module | Contains |
|--------|----------|
| `NetworkModule` | Service/Api bindings |
| `DataModule` / `RepositoryModule` | Repository bindings |

---

## Directory Structure

```
core/network/service/{feature}/     # Services (feature-grouped)
core/network/model/                  # DTOs (@Serializable)
core/data/mapper/                    # DTO ↔ Domain mapping
core/model/                          # Domain models
core/data/repository/                # Repository interfaces
core/data/repositoryImpl/            # Repository implementations
```

---

## Reference

For detailed patterns, see framework templates:
- `templates/instructions/client-layer/CLIENT_PATTERNS.md`
- `templates/instructions/client-layer/SERVICE_TEMPLATE.kt.md`
- `templates/instructions/client-layer/REPOSITORY_TEMPLATE.kt.md`
- `templates/instructions/client-layer/ERROR_HANDLING.md`
