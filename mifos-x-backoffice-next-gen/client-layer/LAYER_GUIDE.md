# template_meta
# template_version: "2.86.0"
# template_path: "templates/blueprints/workspace-project/client-layer/LAYER_GUIDE.md"
# last_modified: "2026-03-19"

# Client Layer Guide - mifos-x-backoffice-next-gen

> **Project Type:** {{project_type}}
> Conventions and patterns for network services and data handling.

---

## Purpose

The client layer handles all network communication, data persistence, and repository patterns.

---

## Directory Structure

```
client-layer/
├── LAYER_STATUS.md    # Implementation status
├── FEATURE_MAP.md     # Feature to service mapping
├── SERVICES_INDEX.md  # O(1) service lookup
├── LAYER_GUIDE.md     # This file
├── TESTING_STATUS.md  # Client layer test coverage
├── services/          # Service documentation
└── instructions/      # Project-type specific guides
    └── {kmp|web}/     # Implementation patterns
```

---

## Architecture Pattern

```
┌─────────────────────────────────────────────────────────────┐
│  Feature Layer (ViewModel / Store)                          │
│  └─→ Calls Repository/Service methods                       │
├─────────────────────────────────────────────────────────────┤
│  Repository / Hook (abstracts data sources)                 │
│  └─→ Combines remote and local data                        │
├─────────────────────────────────────────────────────────────┤
│  Service (API)            │  DataStore (local)              │
│  └─→ Network calls        │  └─→ Preferences/Storage        │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Guides

Based on your project type, use these guides:

### For KMP Projects (Kotlin Multiplatform)

See `instructions/kmp/`:
- **KTORFIT.md** - Ktorfit service patterns
- **REPOSITORY.md** - Repository implementations

### For Web Projects (TypeScript/React)

See `instructions/web/`:
- **FETCH_SERVICES.md** - Fetch/Axios service patterns
- **TANSTACK_QUERY.md** - TanStack Query hooks
- **TYPESCRIPT_TYPES.md** - Type definitions and DTOs

---

## Code Locations

### KMP Projects

```
core/
├── network/src/commonMain/kotlin/org/{{package}}/core/network/
│   ├── service/{feature}/   # Services (feature-grouped)
│   │   ├── {Feature}Api.kt
│   │   └── {Feature}Service.kt
│   ├── model/               # Network DTOs (@Serializable)
│   │   └── {Entity}Dto.kt
│   └── di/NetworkModule.kt  # Service DI bindings
│
├── data/src/commonMain/kotlin/org/{{package}}/core/data/
│   ├── repository/          # Repository interfaces
│   │   └── {Feature}Repository.kt
│   ├── repositoryImpl/      # Repository implementations
│   │   └── {Feature}RepositoryImpl.kt
│   └── mapper/              # DTO ↔ Domain mapping
│       └── {Feature}Mapper.kt
│
├── model/src/commonMain/kotlin/org/{{package}}/core/model/
│   └── {Entity}.kt          # Domain models
│
└── datastore/src/commonMain/kotlin/org/{{package}}/core/datastore/
    └── PreferencesDataSource.kt
```

### Web Projects

```
src/
├── services/               # API services
│   └── {feature}Service.ts
├── hooks/                  # TanStack Query hooks
│   └── use{Feature}.ts
├── types/                  # TypeScript types
│   └── {feature}.ts
└── lib/                    # API client configuration
    └── api.ts
```

---

## Naming Conventions

### KMP Projects

| Type | Pattern | Example |
|------|---------|---------|
| Service | `{Feature}Service` | `AuthService` |
| Repository Interface | `{Feature}Repository` | `AuthRepository` |
| Repository Impl | `{Feature}RepositoryImpl` | `AuthRepositoryImpl` |
| Network DTO | `{Entity}Dto` | `UserDto` |
| Domain Model | `{Entity}` | `User` |

### Web Projects

| Type | Pattern | Example |
|------|---------|---------|
| Service | `{feature}Service.ts` | `authService.ts` |
| Query Hook | `use{Feature}` | `useAuth` |
| Mutation Hook | `use{Action}{Feature}` | `useCreateUser` |
| Type File | `{feature}.ts` | `auth.ts` |

---

## Commands

| Command | Purpose |
|---------|---------|
| `/client [feature]` | Generate client layer code |
| `/gap-analysis client` | Check implementation gaps |
| `/enforce-index services` | Validate SERVICES_INDEX |
