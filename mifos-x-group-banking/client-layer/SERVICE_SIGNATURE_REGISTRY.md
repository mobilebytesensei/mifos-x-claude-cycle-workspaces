<!--
  template_meta:
    version: "2.87.0"
    last_modified: "2026-03-28"
    type: blueprint
    layer: client-layer
-->

# SERVICE_SIGNATURE_REGISTRY.md

> Track all service method signatures for delta detection and contract validation.

**Purpose**: Single source of truth for every service method the client layer exposes. Used by staleness and contract rules to detect drift between API.md specs and generated Kotlin/TypeScript code.

**Updated by**: `/kmp-client`, `/client test contract`, `/client evolve`
**Consumed by**: `RULE-CLIENT-CONTRACT-001`, `RULE-CLIENT-STALE-001`

---

## Service Method Signatures

| Service | Method | Parameters | Return DTO | API.md Endpoint | Contract Status | Last Verified |
|---------|--------|-----------|------------|-----------------|:--------------:|:-------------:|
| `AuthApi` | `signIn` | `email: String, password: String` | `AuthTokenDto` | `POST /auth/signin` | VALID | {ISO-8601} |
| `AuthApi` | `signUp` | `request: SignUpRequest` | `AuthTokenDto` | `POST /auth/signup` | VALID | {ISO-8601} |
| `AuthApi` | `refreshToken` | `token: String` | `AuthTokenDto` | `POST /auth/refresh` | VALID | {ISO-8601} |
| `MovieApi` | `getMovies` | `page: Int, limit: Int` | `List<MovieDto>` | `GET /movies` | VALID | {ISO-8601} |
| `MovieApi` | `getMovieById` | `id: String` | `MovieDto` | `GET /movies/{id}` | VALID | {ISO-8601} |
| `MovieApi` | `searchMovies` | `query: String, page: Int` | `List<MovieDto>` | `GET /movies/search` | VALID | {ISO-8601} |
| `MoodApi` | `getMoods` | _(none)_ | `List<MoodDto>` | `GET /moods` | VALID | {ISO-8601} |
| `MoodApi` | `getMoviesByMood` | `moodId: String, page: Int` | `List<MovieDto>` | `GET /moods/{id}/movies` | VALID | {ISO-8601} |

### Contract Status Values

| Status | Meaning |
|--------|---------|
| `VALID` | Method signature matches API.md endpoint exactly |
| `STALE` | API.md changed since last verification |
| `DRIFT` | Method exists in code but not in API.md (or vice versa) |
| `NEW` | Detected in API.md but not yet generated |
| `REMOVED` | Was in API.md, now deleted -- code should be cleaned up |

---

## Delta Detection

Compare this registry against `design-spec-layer/features/{feature}/API.md` to find:

### NEW Methods
Methods present in API.md but absent from this registry. Action: generate service method + test.

### MODIFIED Methods
Methods where parameters or return type changed in API.md vs this registry. Action: update DTO, mapper, service method, and re-run contract test.

### REMOVED Methods
Methods listed here but no longer in API.md. Action: deprecate or remove service method, update DI module, clean up tests.

### Detection Algorithm

```
for each feature with API.md:
  1. Parse API.md endpoints -> expected_methods[]
  2. Parse SERVICE_SIGNATURE_REGISTRY -> registered_methods[]
  3. NEW      = expected_methods - registered_methods
  4. REMOVED  = registered_methods - expected_methods
  5. MODIFIED = intersection where signature differs
  6. VALID    = intersection where signature matches
```

---

## Auto-Update Rules

### After `/kmp-client`
1. Parse all generated service interfaces
2. Extract method signatures (name, parameters, return type)
3. Map each method to its API.md endpoint
4. Add/update rows in this registry
5. Set `Contract Status` = `VALID`, `Last Verified` = now

### After `/client test contract`
1. Re-parse API.md for current endpoint definitions
2. Compare against this registry
3. Update `Contract Status` for each method
4. Flag any `STALE`, `DRIFT`, `NEW`, or `REMOVED` entries
5. Update `Last Verified` = now for all `VALID` entries

### After `/client evolve`
1. Apply modifications to service methods
2. Update this registry with new signatures
3. Re-run contract validation
4. Update status accordingly
