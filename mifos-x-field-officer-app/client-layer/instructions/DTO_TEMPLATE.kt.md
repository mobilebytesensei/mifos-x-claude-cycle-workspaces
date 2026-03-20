# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mifos-x-field-officer-app/client-layer/instructions/DTO_TEMPLATE.kt.md"
# last_modified: "2026-03-20"

# DTO Template (Data Transfer Objects)

> **Layer**: core/network
> **Pattern**: Kotlinx Serialization DTOs with Default Values
> **Confidence**: 95%

---

## File Locations

```
DTO:    core/network/src/commonMain/kotlin/{package}/core/network/model/{Feature}Dto.kt
Domain: core/model/src/commonMain/kotlin/{package}/core/model/{Feature}.kt
```

---

## DTO Template

```kotlin
// File: core/network/src/commonMain/kotlin/{pkg}/core/network/model/{Feature}Dto.kt
package {package}.core.network.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/**
 * {Feature} Data Transfer Object
 *
 * Represents the API response structure for {feature} entity.
 * Maps directly to JSON response from backend.
 *
 * NOTE: All fields have default values for safe deserialization in KMP.
 * Do NOT use @Parcelize -- it is Android-only and not compatible with KMP.
 */
@Serializable
data class {Feature}Dto(
    @SerialName("id")
    val id: String = "",

    @SerialName("name")
    val name: String = "",

    @SerialName("description")
    val description: String = "",

    @SerialName("created_at")
    val createdAt: String = "",

    @SerialName("updated_at")
    val updatedAt: String = "",

    // Nested objects
    @SerialName("metadata")
    val metadata: {Feature}MetadataDto? = null,

    // Lists
    @SerialName("tags")
    val tags: List<String> = emptyList(),
)

/**
 * Nested metadata DTO
 */
@Serializable
data class {Feature}MetadataDto(
    @SerialName("key")
    val key: String = "",

    @SerialName("value")
    val value: String = "",
)
```

---

## Domain Model Template

```kotlin
// File: core/model/src/commonMain/kotlin/{pkg}/core/model/{Feature}.kt
package {package}.core.model

/**
 * {Feature} Domain Model
 *
 * Clean domain representation used throughout the app.
 * Independent of network/database structure.
 * No serialization annotations -- this is a pure domain object.
 */
data class {Feature}(
    val id: String,
    val name: String,
    val description: String,
    val createdAt: String,
    val metadata: {Feature}Metadata?,
    val tags: List<String>,
) {
    companion object {
        val EMPTY = {Feature}(
            id = "",
            name = "",
            description = "",
            createdAt = "",
            metadata = null,
            tags = emptyList(),
        )
    }
}

/**
 * {Feature} Metadata domain model
 */
data class {Feature}Metadata(
    val key: String,
    val value: String,
)
```

---

## Request DTOs

### Create Request

```kotlin
// File: core/network/src/commonMain/kotlin/{pkg}/core/network/model/Create{Feature}Request.kt
package {package}.core.network.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/**
 * Request body for creating a new {feature}
 */
@Serializable
data class Create{Feature}Request(
    @SerialName("name")
    val name: String,

    @SerialName("description")
    val description: String? = null,

    @SerialName("tags")
    val tags: List<String> = emptyList(),
)
```

### Update Request

```kotlin
// File: core/network/src/commonMain/kotlin/{pkg}/core/network/model/Update{Feature}Request.kt
package {package}.core.network.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/**
 * Request body for updating an existing {feature}
 */
@Serializable
data class Update{Feature}Request(
    @SerialName("name")
    val name: String? = null,

    @SerialName("description")
    val description: String? = null,

    @SerialName("tags")
    val tags: List<String>? = null,
)
```

### Patch Request (Partial Update)

```kotlin
// File: core/network/src/commonMain/kotlin/{pkg}/core/network/model/Patch{Feature}Request.kt
package {package}.core.network.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/**
 * Request body for partial {feature} update
 * Only non-null fields will be updated
 */
@Serializable
data class Patch{Feature}Request(
    @SerialName("name")
    val name: String? = null,

    @SerialName("description")
    val description: String? = null,
)
```

---

## Response DTOs

### Paginated Response

```kotlin
// File: core/network/src/commonMain/kotlin/{pkg}/core/network/model/{Feature}PageResponse.kt
package {package}.core.network.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/**
 * Paginated response wrapper for {feature} list
 */
@Serializable
data class {Feature}PageResponse(
    @SerialName("items")
    val items: List<{Feature}Dto> = emptyList(),

    @SerialName("total")
    val total: Int = 0,

    @SerialName("page")
    val page: Int = 0,

    @SerialName("limit")
    val limit: Int = 0,

    @SerialName("has_more")
    val hasMore: Boolean = false,
)
```

### Single Item Response

```kotlin
/**
 * Single item response wrapper (if API wraps data)
 */
@Serializable
data class {Feature}Response(
    @SerialName("data")
    val data: {Feature}Dto = {Feature}Dto(),

    @SerialName("message")
    val message: String = "",
)
```

### Error Response

```kotlin
/**
 * Standard error response from API
 */
@Serializable
data class ErrorResponse(
    @SerialName("error")
    val error: String = "",

    @SerialName("message")
    val message: String = "",

    @SerialName("code")
    val code: String = "",

    @SerialName("details")
    val details: Map<String, String> = emptyMap(),
)
```

---

## Supabase-Specific DTOs

### RPC Request

```kotlin
/**
 * Request for Supabase RPC function call
 */
@Serializable
data class {Function}Request(
    @SerialName("param1")
    val param1: String,

    @SerialName("param2")
    val param2: Int? = null,
)
```

### RPC Response

```kotlin
/**
 * Response from Supabase RPC function
 */
@Serializable
data class {Function}Response(
    @SerialName("result")
    val result: String = "",

    @SerialName("count")
    val count: Int = 0,
)
```

---

## Serialization Annotations Reference

| Annotation | Purpose | Example |
|------------|---------|---------|
| `@Serializable` | Mark class as serializable | `@Serializable data class Dto(...)` |
| `@SerialName` | Map JSON key to property | `@SerialName("user_id") val userId` |
| `@Transient` | Exclude from serialization | `@Transient val temp: String = ""` |
| `@EncodeDefault` | Include default values | `@EncodeDefault val flag: Boolean = true` |
| `@Required` | Field must be present | `@Required val id: String` |

---

## Type Mapping

| JSON Type | Kotlin Type | Notes |
|-----------|-------------|-------|
| `string` | `String` | Default to `""` |
| `string?` | `String?` | Optional field, default `null` |
| `number` | `Int`, `Long`, `Double` | Default to `0` / `0.0` |
| `boolean` | `Boolean` | Default to `false` |
| `array` | `List<T>` | Default to `emptyList()` |
| `object` | Nested `@Serializable` | Nullable, default `null` |
| `null` | `T?` | Nullable type |
| `timestamp` | `String` | Default to `""`, parse in mapper |
| `uuid` | `String` | Default to `""` |

---

## Example: MovieDto

```kotlin
// File: core/network/src/commonMain/kotlin/com/moodmovies/core/network/model/MovieDto.kt
package com.moodmovies.core.network.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class MovieDto(
    @SerialName("id")
    val id: String = "",

    @SerialName("title")
    val title: String = "",

    @SerialName("overview")
    val overview: String = "",

    @SerialName("poster_path")
    val posterPath: String = "",

    @SerialName("backdrop_path")
    val backdropPath: String = "",

    @SerialName("release_date")
    val releaseDate: String = "",

    @SerialName("vote_average")
    val voteAverage: Double = 0.0,

    @SerialName("vote_count")
    val voteCount: Int = 0,

    @SerialName("genres")
    val genres: List<GenreDto> = emptyList(),

    @SerialName("mood_tags")
    val moodTags: List<String> = emptyList(),
)

@Serializable
data class GenreDto(
    @SerialName("id")
    val id: Int = 0,

    @SerialName("name")
    val name: String = "",
)

// Request DTOs
@Serializable
data class MoodRequest(
    @SerialName("mood")
    val mood: String,

    @SerialName("limit")
    val limit: Int = 20,
)

// Response DTOs
@Serializable
data class MoviePageResponse(
    @SerialName("results")
    val items: List<MovieDto> = emptyList(),

    @SerialName("page")
    val page: Int = 0,

    @SerialName("total_pages")
    val totalPages: Int = 0,

    @SerialName("total_results")
    val totalResults: Int = 0,
)
```

```kotlin
// File: core/model/src/commonMain/kotlin/com/moodmovies/core/model/Movie.kt
package com.moodmovies.core.model

import kotlinx.datetime.LocalDate

data class Movie(
    val id: String,
    val title: String,
    val overview: String,
    val posterUrl: String?,
    val backdropUrl: String?,
    val releaseDate: LocalDate?,
    val rating: Double,
    val voteCount: Int,
    val genres: List<Genre>,
    val moodTags: List<String>,
) {
    val formattedRating: String
        get() = "%.1f".format(rating)

    val releaseYear: Int?
        get() = releaseDate?.year
}

data class Genre(
    val id: Int,
    val name: String,
)
```

---

## Best Practices

### 1. Use @SerialName When JSON Key Differs from Property Name

```kotlin
// REQUIRED: When JSON key uses snake_case but property uses camelCase
@SerialName("user_id")
val userId: String = ""

@SerialName("created_at")
val createdAt: String = ""

// NOT NEEDED: When property name already matches JSON key
val id: Long? = null          // JSON key is "id" -- matches, @SerialName optional
val active: Boolean = false   // JSON key is "active" -- matches, @SerialName optional
val displayName: String? = null  // JSON key is "displayName" -- matches

// BAD: Using snake_case property name to match JSON (violates Kotlin conventions)
val user_id: String = ""  // Works but violates Kotlin naming conventions
```

> **Exemplar note**: The mobile-wallet exemplar uses `@Serializable` without `@SerialName`
> on fields where the property name already matches the JSON key. Only add `@SerialName`
> when the JSON key uses a different format (typically snake_case).

### 2. Always Provide Default Values for DTO Fields

Both non-null with defaults and nullable with `null` default are valid:

```kotlin
// GOOD (Pattern A - non-null with defaults): Used for guaranteed fields
val id: String = ""
val count: Int = 0
val tags: List<String> = emptyList()
val active: Boolean = false

// GOOD (Pattern B - nullable with null default): Used in exemplar for optional fields
val id: Long? = null
val accountNo: String? = null
val displayName: String? = null
val isStaff: Boolean? = null

// BAD: No default - deserialization fails if field is missing from JSON
val id: String
```

> **Exemplar note**: The mobile-wallet exemplar uses Pattern B (nullable with `null`)
> for most fields, which is more resilient when APIs may omit fields. Mappers then
> handle null-to-default conversion (e.g., `id ?: 0`, `name.orEmpty()`).

### 3. Nullable vs Default for Optional API Fields

```kotlin
// Use nullable when absence has semantic meaning
@SerialName("deleted_at")
val deletedAt: String? = null  // null = not deleted

// Use default when a fallback is appropriate
@SerialName("description")
val description: String = ""  // empty = no description yet
```

### 4. Separate DTOs from Domain Models

```kotlin
// DTO in core/network/model/ - matches API exactly
data class UserDto(@SerialName("user_name") val userName: String = "")

// Domain Model in core/model/ - clean for app use
data class User(val name: String)

// Mapper in core/data/mapper/ - converts DTO to Domain
fun UserDto.toUser() = User(name = userName)
```

### 5. Never Use Android-Only Annotations in KMP DTOs

```kotlin
// BAD: @Parcelize is Android-only, breaks iOS/Desktop/Web
@Parcelize
data class UserDto(...) : Parcelable

// GOOD: Use @Serializable only (KMP-compatible)
@Serializable
data class UserDto(...)
```

---

## Related Templates

| Template | Purpose |
|----------|---------|
| `SERVICE_TEMPLATE.kt.md` | Service using these DTOs |
| `MAPPER_TEMPLATE.kt.md` | DTO to Domain mapping |
| `REPOSITORY_TEMPLATE.kt.md` | Repository using services |
