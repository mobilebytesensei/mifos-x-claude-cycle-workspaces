# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mifos-mobile/client-layer/REPOSITORIES_INDEX.md"
# last_modified: "2026-03-20"

# Repositories Index

**Project**: ${PROJECT_NAME}
**Last Updated**: ${DATE}
**Total Repositories**: ${REPOSITORY_COUNT}

---

## Quick Lookup

| Repository | Feature | Package | Path |
|------------|---------|---------|------|
| ${Repository}Repository | ${feature} | repository | [${Repository}Repository.kt](../source/${project}/core/data/.../repository/${Repository}Repository.kt) |

---

## By Feature

### ${feature_1}
- ${Repository1}Repository

### ${feature_2}
- ${Repository2}Repository

---

## Repository Pattern

```kotlin
// Interface in core/domain
interface ${Feature}Repository {
    fun get${Feature}s(): Flow<List<${Feature}>>
    suspend fun get${Feature}(id: Long): ${Feature}
    suspend fun create${Feature}(payload: ${Feature}Payload): ${Feature}
    suspend fun update${Feature}(id: Long, payload: ${Feature}Payload): ${Feature}
    suspend fun delete${Feature}(id: Long)
}

// Implementation in core/data
class ${Feature}RepositoryImpl(
    private val ${feature}Service: ${Feature}Service,
    private val ${feature}Mapper: ${Feature}Mapper
) : ${Feature}Repository {
    // Implementation
}
```

---

## Status

| Status | Count | Repositories |
|--------|-------|--------------|
| Implemented | 0 | - |
| Planned | ${REPOSITORY_COUNT} | All |

---

## How to Add Repository

1. Define interface in `core/domain/repository/`
2. Create implementation in `core/data/repository/`
3. Add mapper in `core/data/mapper/`
4. Register in Koin module
5. Update this index
