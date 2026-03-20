# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mifos-x-field-officer-app/client-layer/instructions/MAPPER_TEMPLATE.kt.md"
# last_modified: "2026-03-20"

# Mapper Template (DTO <-> Domain)

> **Layer**: core/data
> **Pattern**: Extension Function Mappers
> **Confidence**: 95%

---

## File Location

```
Mapper: core/data/src/commonMain/kotlin/{package}/core/data/mapper/{Feature}Mapper.kt
Test:   core/data/src/commonTest/kotlin/{package}/core/data/mapper/{Feature}MapperTest.kt
```

> **Note**: Mappers live in `core/data/mapper/`, NOT `core/network/mapper/`. This matches the mobile-wallet exemplar where all mapper files (e.g., `ClientDetailsMapper.kt`, `AccountMapper.kt`, `UserMapper.kt`, `TransactionMapper.kt`) reside in `core/data/src/commonMain/kotlin/.../core/data/mapper/`.

---

## Mapper Template

```kotlin
// File: core/data/src/commonMain/kotlin/{pkg}/core/data/mapper/{Feature}Mapper.kt
package {package}.core.data.mapper

import {package}.core.model.{Feature}
import {package}.core.model.{Feature}Metadata
import {package}.core.network.model.{Feature}Dto
import {package}.core.network.model.{Feature}MetadataDto
import {package}.core.network.model.Create{Feature}Request
import {package}.core.network.model.Update{Feature}Request

// =============================================================================
// DTO -> Domain Model
// =============================================================================

/**
 * Convert {Feature}Dto to {Feature} domain model
 */
fun {Feature}Dto.to{Feature}(): {Feature} {
    return {Feature}(
        id = id,
        name = name,
        description = description,
        createdAt = createdAt,
        metadata = metadata?.to{Feature}Metadata(),
        tags = tags,
    )
}

/**
 * Convert list of {Feature}Dto to list of {Feature} domain models
 */
fun List<{Feature}Dto>.to{Feature}List(): List<{Feature}> {
    return map { it.to{Feature}() }
}

// =============================================================================
// Domain Model -> DTO
// =============================================================================

/**
 * Convert {Feature} domain model back to {Feature}Dto
 */
fun {Feature}.to{Feature}Dto(): {Feature}Dto {
    return {Feature}Dto(
        id = id,
        name = name,
        description = description,
        createdAt = createdAt,
        metadata = metadata?.to{Feature}MetadataDto(),
        tags = tags,
    )
}

// =============================================================================
// Domain Model -> Request DTOs
// =============================================================================

/**
 * Convert {Feature} to CreateRequest DTO
 */
fun {Feature}.toCreate{Feature}Request(): Create{Feature}Request {
    return Create{Feature}Request(
        name = name,
        description = description.takeIf { it.isNotBlank() },
        tags = tags,
    )
}

/**
 * Convert {Feature} to UpdateRequest DTO
 */
fun {Feature}.toUpdate{Feature}Request(): Update{Feature}Request {
    return Update{Feature}Request(
        name = name,
        description = description.takeIf { it.isNotBlank() },
        tags = tags,
    )
}

// =============================================================================
// Nested Object Mappers
// =============================================================================

/**
 * Convert metadata DTO to domain model
 */
fun {Feature}MetadataDto.to{Feature}Metadata(): {Feature}Metadata {
    return {Feature}Metadata(
        key = key,
        value = value,
    )
}

/**
 * Convert domain metadata to DTO
 */
fun {Feature}Metadata.to{Feature}MetadataDto(): {Feature}MetadataDto {
    return {Feature}MetadataDto(
        key = key,
        value = value,
    )
}
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

## Mapper Test Template

```kotlin
// File: core/data/src/commonTest/kotlin/{pkg}/core/data/mapper/{Feature}MapperTest.kt
package {package}.core.data.mapper

import {package}.core.model.{Feature}
import {package}.core.model.{Feature}Metadata
import {package}.core.network.model.{Feature}Dto
import {package}.core.network.model.{Feature}MetadataDto
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertNull

class {Feature}MapperTest {

    // =========================================================================
    // DTO -> Domain
    // =========================================================================

    @Test
    fun `map DTO to domain model`() {
        val dto = {Feature}Dto(
            id = "1",
            name = "Test",
            description = "A test feature",
            createdAt = "2024-01-01T00:00:00Z",
        )
        val model = dto.to{Feature}()

        assertEquals("1", model.id)
        assertEquals("Test", model.name)
        assertEquals("A test feature", model.description)
        assertEquals("2024-01-01T00:00:00Z", model.createdAt)
    }

    @Test
    fun `map DTO with metadata to domain model`() {
        val dto = {Feature}Dto(
            id = "1",
            name = "Test",
            metadata = {Feature}MetadataDto(key = "color", value = "blue"),
        )
        val model = dto.to{Feature}()

        assertEquals("color", model.metadata?.key)
        assertEquals("blue", model.metadata?.value)
    }

    @Test
    fun `map DTO with null metadata to domain model`() {
        val dto = {Feature}Dto(id = "1", name = "Test", metadata = null)
        val model = dto.to{Feature}()

        assertNull(model.metadata)
    }

    @Test
    fun `map list of DTOs to domain models`() {
        val dtos = listOf(
            {Feature}Dto(id = "1", name = "First"),
            {Feature}Dto(id = "2", name = "Second"),
        )
        val models = dtos.to{Feature}List()

        assertEquals(2, models.size)
        assertEquals("1", models[0].id)
        assertEquals("2", models[1].id)
    }

    @Test
    fun `map empty list of DTOs returns empty list`() {
        val dtos = emptyList<{Feature}Dto>()
        val models = dtos.to{Feature}List()

        assertEquals(0, models.size)
    }

    // =========================================================================
    // Domain -> DTO
    // =========================================================================

    @Test
    fun `map domain model to DTO`() {
        val model = {Feature}(
            id = "1",
            name = "Test",
            description = "A test feature",
            createdAt = "2024-01-01T00:00:00Z",
            metadata = null,
            tags = emptyList(),
        )
        val dto = model.to{Feature}Dto()

        assertEquals("1", dto.id)
        assertEquals("Test", dto.name)
        assertEquals("A test feature", dto.description)
    }

    @Test
    fun `round-trip DTO to domain and back preserves data`() {
        val original = {Feature}Dto(
            id = "1",
            name = "Test",
            description = "Description",
            createdAt = "2024-01-01T00:00:00Z",
            tags = listOf("tag1", "tag2"),
        )
        val roundTripped = original.to{Feature}().to{Feature}Dto()

        assertEquals(original.id, roundTripped.id)
        assertEquals(original.name, roundTripped.name)
        assertEquals(original.description, roundTripped.description)
        assertEquals(original.tags, roundTripped.tags)
    }

    // =========================================================================
    // Domain -> Request DTOs
    // =========================================================================

    @Test
    fun `map domain model to create request`() {
        val model = {Feature}(
            id = "1",
            name = "Test",
            description = "Description",
            createdAt = "",
            metadata = null,
            tags = listOf("tag1"),
        )
        val request = model.toCreate{Feature}Request()

        assertEquals("Test", request.name)
        assertEquals("Description", request.description)
        assertEquals(listOf("tag1"), request.tags)
    }

    @Test
    fun `map domain model with blank description to create request omits description`() {
        val model = {Feature}(
            id = "1",
            name = "Test",
            description = "",
            createdAt = "",
            metadata = null,
            tags = emptyList(),
        )
        val request = model.toCreate{Feature}Request()

        assertNull(request.description)
    }
}
```

---

## Example: MovieMapper

```kotlin
// File: core/data/src/commonMain/kotlin/com/moodmovies/core/data/mapper/MovieMapper.kt
package com.moodmovies.core.data.mapper

import com.moodmovies.core.model.Movie
import com.moodmovies.core.model.Genre
import com.moodmovies.core.network.model.MovieDto
import com.moodmovies.core.network.model.GenreDto
import kotlinx.datetime.LocalDate

/**
 * MovieDto -> Movie domain model
 */
fun MovieDto.toMovie(): Movie {
    return Movie(
        id = id,
        title = title,
        overview = overview,
        posterUrl = posterPath.takeIf { it.isNotBlank() }?.let { "https://image.tmdb.org/t/p/w500$it" },
        backdropUrl = backdropPath.takeIf { it.isNotBlank() }?.let { "https://image.tmdb.org/t/p/original$it" },
        releaseDate = releaseDate.takeIf { it.isNotBlank() }?.let { parseDate(it) },
        rating = voteAverage,
        voteCount = voteCount,
        genres = genres.toGenreList(),
        moodTags = moodTags,
    )
}

fun List<MovieDto>.toMovieList(): List<Movie> = map { it.toMovie() }

/**
 * GenreDto -> Genre domain model
 */
fun GenreDto.toGenre(): Genre {
    return Genre(
        id = id,
        name = name,
    )
}

fun List<GenreDto>.toGenreList(): List<Genre> = map { it.toGenre() }

private fun parseDate(dateString: String): LocalDate? {
    return try {
        LocalDate.parse(dateString)
    } catch (e: Exception) {
        null
    }
}
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

## Mapping Patterns

### 1. Nullable Handling

```kotlin
// Safe handling with takeIf
description = dto.description.takeIf { it.isNotBlank() }

// Default value for nullable
rating = dto.rating ?: 0.0

// orEmpty for nullable strings
description = dto.description.orEmpty()
```

### 2. List Mapping

```kotlin
// Extension function for lists (preferred pattern)
fun List<GenreDto>.toGenreList() = map { it.toGenre() }

// Usage in parent mapper
genres = dto.genres.toGenreList()
```

### 3. URL Construction

```kotlin
// Construct full URL from path (check non-blank first)
posterUrl = dto.posterPath.takeIf { it.isNotBlank() }?.let { path ->
    "${BuildConfig.IMAGE_BASE_URL}$path"
}
```

### 4. Date/Time Parsing

```kotlin
// ISO timestamp to Instant
createdAt = Instant.parse(dto.createdAt)

// Date string to LocalDate
releaseDate = LocalDate.parse(dto.releaseDate)

// Safe parsing with fallback
releaseDate = try {
    LocalDate.parse(dto.releaseDate)
} catch (e: Exception) {
    null
}
```

### 5. Enum Mapping

```kotlin
// String to enum
status = Status.valueOf(dto.status.uppercase())

// Safe enum mapping
status = Status.entries.find { it.name == dto.status }
    ?: Status.UNKNOWN
```

### 6. Computed Properties

```kotlin
// In domain model (not in mapper)
data class Movie(...) {
    val isHighRated: Boolean
        get() = rating >= 7.0

    val displayTitle: String
        get() = "$title (${releaseYear ?: "TBA"})"
}
```

---

## Bidirectional Mapping

### When to Use

| Direction | Use Case |
|-----------|----------|
| DTO -> Domain | API response to UI |
| Domain -> DTO | Caching or reverse mapping |
| Domain -> Request DTO | Creating/updating via API |
| Domain -> Entity | Local database storage |
| Entity -> Domain | Local database to UI |

### Full Round-Trip Example

```kotlin
// DTO -> Domain (from API)
fun UserDto.toUser(): User

// Domain -> DTO (reverse)
fun User.toUserDto(): UserDto

// Domain -> CreateRequest (to API)
fun User.toCreateUserRequest(): CreateUserRequest

// Domain -> UpdateRequest (to API)
fun User.toUpdateUserRequest(): UpdateUserRequest

// Domain -> Entity (to database)
fun User.toUserEntity(): UserEntity

// Entity -> Domain (from database)
fun UserEntity.toUser(): User
```

---

## File Organization

```
core/data/src/commonMain/kotlin/{package}/core/data/
├── mapper/                         # Mappers live in core/data, not core/network
│   ├── MovieMapper.kt
│   ├── UserMapper.kt
│   └── GenreMapper.kt
├── repository/
│   └── MovieRepository.kt         # Interface
└── repositoryImpl/
    └── MovieRepositoryImpl.kt     # Implementation

core/network/src/commonMain/kotlin/{package}/core/network/
├── model/                          # DTOs stay in core/network
│   ├── MovieDto.kt
│   ├── UserDto.kt
│   ├── CreateMovieRequest.kt
│   └── MoviePageResponse.kt
└── service/
    └── MovieService.kt             # Uses DTOs

core/data/src/commonTest/kotlin/{package}/core/data/
└── mapper/
    ├── MovieMapperTest.kt
    └── UserMapperTest.kt

core/model/src/commonMain/kotlin/{package}/core/model/
├── Movie.kt
├── User.kt
└── Genre.kt
```

---

## Best Practices

### 1. One Mapper File Per Feature

```kotlin
// MovieMapper.kt - contains all movie-related mappings
fun MovieDto.toMovie(): Movie
fun GenreDto.toGenre(): Genre
fun List<MovieDto>.toMovieList(): List<Movie>
fun Movie.toMovieDto(): MovieDto
```

### 2. Extension Functions Over Utility Classes

```kotlin
// GOOD: Extension function
fun MovieDto.toMovie(): Movie { ... }

// BAD: Utility class with static methods
object MovieMapper {
    fun mapToDomain(dto: MovieDto): Movie { ... }
}
```

### 3. Naming Convention

Two naming patterns are acceptable. Choose one and be consistent within a project:

```kotlin
// Pattern A (recommended for new projects): to{DomainType}
fun MovieDto.toMovie(): Movie
fun GenreDto.toGenre(): Genre
fun List<MovieDto>.toMovieList(): List<Movie>

// Pattern B (used in mobile-wallet exemplar): toModel/toEntity
fun ClientEntity.toModel(): Client         // Entity/DTO -> Domain
fun NewClient.toEntity(): NewClientEntity  // Domain -> Entity/DTO
fun List<ClientEntity>.toModel(): List<Client>
fun UpdatedClient.toEntity(): UpdateClientEntity

// Also acceptable from exemplar: domain-specific names
fun ClientAccountsEntity.toAccount(): List<Account>
fun User.toUserInfo(): UserInfo

// BAD: Generic/unclear names
fun MovieDto.toDomainModel(): Movie
fun MovieDto.map(): Movie
```

> **Exemplar note**: The mobile-wallet exemplar uses `.toModel()` for Entity/DTO-to-Domain
> and `.toEntity()` for Domain-to-Entity/DTO conversions. It also uses domain-specific
> names like `.toAccount()`, `.toUserInfo()`, `.toRoleInfo()` when the mapping crosses
> domain boundaries.

### 4. Keep Domain Models Clean

```kotlin
// Domain model should NOT have:
// - @SerialName annotations
// - @Serializable annotation
// - Default values matching API defaults

// Domain model SHOULD have:
// - Computed properties
// - Business logic methods
// - Companion object with EMPTY/DEFAULT
```

### 5. Handle All Edge Cases in Mapper

```kotlin
// All null handling, defaults, and transformations
// happen in the mapper, not in repository or ViewModel
fun MovieDto.toMovie(): Movie {
    return Movie(
        title = title.trim(),
        rating = voteAverage.coerceIn(0.0, 10.0),
        posterUrl = posterPath.takeIf { it.isNotBlank() }?.toFullUrl(),
    )
}
```

### 6. Always Write Mapper Tests

```kotlin
// Every mapper should have corresponding tests
// Test: DTO -> Domain, Domain -> DTO, list mapping, edge cases
class MovieMapperTest {
    @Test fun `map DTO to domain model`() { ... }
    @Test fun `map domain model to DTO`() { ... }
    @Test fun `map list of DTOs to domain models`() { ... }
    @Test fun `round-trip preserves data`() { ... }
}
```

---

## Related Templates

| Template | Purpose |
|----------|---------|
| `DTO_TEMPLATE.kt.md` | DTOs being mapped |
| `REPOSITORY_TEMPLATE.kt.md` | Repository using mappers |
| `USECASE_TEMPLATE.kt.md` | Use cases with domain models |
