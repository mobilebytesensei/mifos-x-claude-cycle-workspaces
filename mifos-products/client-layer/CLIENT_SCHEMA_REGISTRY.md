<!--
  template_meta:
    version: "2.87.0"
    last_modified: "2026-03-28"
    type: blueprint
    layer: client-layer
-->

# CLIENT_SCHEMA_REGISTRY.md

> Track DTO field definitions for staleness detection.

**Purpose**: Single source of truth for every DTO class and its `@SerialName` fields. Used by staleness and contract rules to detect schema drift between API.md response models and generated Kotlin DTOs.

**Updated by**: `/kmp-client`, `/client test dto`
**Consumed by**: `RULE-CLIENT-STALE-001`, `RULE-CLIENT-CONTRACT-001`

---

## DTO Field Registry

| DTO Class | @SerialName Fields | Source API.md | Last Verified | Match Status |
|-----------|-------------------|---------------|:-------------:|:------------:|
| `AuthTokenDto` | `access_token: String`, `refresh_token: String`, `expires_in: Long`, `token_type: String` | `auth/API.md` | {ISO-8601} | MATCH |
| `MovieDto` | `id: String`, `title: String`, `overview: String`, `poster_path: String`, `release_date: String`, `vote_average: Double`, `genre_ids: List<Int>` | `movies/API.md` | {ISO-8601} | MATCH |
| `MoodDto` | `id: String`, `name: String`, `emoji: String`, `color: String` | `mood/API.md` | {ISO-8601} | MATCH |
| `SignUpRequest` | `email: String`, `password: String`, `display_name: String` | `auth/API.md` | {ISO-8601} | MATCH |
| `MovieDetailDto` | `id: String`, `title: String`, `overview: String`, `poster_path: String`, `backdrop_path: String`, `release_date: String`, `runtime: Int`, `vote_average: Double`, `genres: List<GenreDto>`, `cast: List<CastDto>` | `movie-detail/API.md` | {ISO-8601} | MATCH |

### Match Status Values

| Status | Meaning |
|--------|---------|
| `MATCH` | All `@SerialName` fields match API.md response schema exactly |
| `DRIFT` | Fields differ between DTO class and API.md (added, removed, or type changed) |
| `STALE` | API.md updated after last verification -- re-check needed |
| `PARTIAL` | Some fields match, others missing or extra |
| `UNKNOWN` | No API.md found for this DTO (orphan or shared model) |

---

## Drift Detection

### Field-Level Comparison

For each DTO class, compare:
1. **@SerialName fields in .kt file** vs **response fields in API.md**
2. **Kotlin types** vs **JSON types** (String, Int, Double, Boolean, List, nested objects)
3. **Default values** -- DTOs must have safe defaults for optional fields
4. **Nullability** -- nullable in API.md must be nullable in Kotlin (`?`)

### Drift Categories

| Category | Description | Severity |
|----------|-------------|:--------:|
| Missing Field | API.md has field, DTO does not | HIGH |
| Extra Field | DTO has field, API.md does not | LOW |
| Type Mismatch | Field exists in both, type differs | HIGH |
| Nullability Mismatch | API.md says nullable, DTO says non-null (or vice versa) | MEDIUM |
| Name Mismatch | @SerialName does not match API.md field name | HIGH |
| Default Value Missing | Optional field lacks default value | MEDIUM |

### Detection Algorithm

```
for each DTO class in registry:
  1. Parse .kt file -> kotlin_fields[] (name, type, nullable, default)
  2. Parse API.md response model -> api_fields[] (name, type, nullable)
  3. MISSING  = api_fields - kotlin_fields (by @SerialName)
  4. EXTRA    = kotlin_fields - api_fields (by @SerialName)
  5. TYPE_MISMATCH = intersection where type mapping differs
  6. NULL_MISMATCH = intersection where nullability differs
  7. If any HIGH severity -> status = DRIFT
  8. If only LOW/MEDIUM -> status = PARTIAL
  9. If none -> status = MATCH
```

---

## Auto-Update Rules

### After `/kmp-client`
1. Parse all generated `@Serializable` data classes
2. Extract `@SerialName` field names, Kotlin types, nullability, and defaults
3. Map each DTO to its source API.md file
4. Add/update rows in this registry
5. Set `Match Status` = `MATCH`, `Last Verified` = now

### After `/client test dto`
1. Re-parse API.md response models for current field definitions
2. Compare against this registry field-by-field
3. Update `Match Status` for each DTO
4. Report any `DRIFT` or `PARTIAL` entries with details
5. Update `Last Verified` = now for all `MATCH` entries
