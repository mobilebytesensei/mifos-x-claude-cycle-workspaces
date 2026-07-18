# template_meta
# template_version: "2.86.0"
# template_path: "templates/blueprints/workspace-project/feature-layer/LAYER_GUIDE.md"
# last_modified: "2026-03-19"

# Feature Layer Guide - mifos-x-backoffice-next-gen

> **Project Type:** {{project_type}}
> Conventions and patterns for UI implementation.

---

## Purpose

The feature layer contains all UI screens, components, state management, and navigation logic.

---

## Directory Structure

```
feature-layer/
├── LAYER_STATUS.md       # Implementation status
├── MODULES_INDEX.md      # O(1) module lookup
├── SCREENS_INDEX.md      # O(1) screen lookup
├── LAYER_GUIDE.md        # This file
├── TESTING_STATUS.md     # Feature test coverage
├── features/             # Feature tracking
└── instructions/         # Project-type specific guides
    └── {kmp|web}/        # Implementation patterns
```

---

## Implementation Guides

Based on your project type, use these guides:

### For KMP Projects (Kotlin Multiplatform)

See `instructions/kmp/`:
- **COMPOSE.md** - Compose Multiplatform patterns
- **VIEWMODEL.md** - ViewModel and MVI patterns
- **DI.md** - Koin dependency injection
- **NAVIGATION.md** - Navigation patterns

### For Web Projects (TypeScript/React)

See `instructions/web/`:
- **REACT_COMPONENTS.md** - React component patterns
- **ZUSTAND_STORES.md** - Zustand state management
- **NEXTJS_ROUTING.md** - Next.js App Router patterns
- **FORM_VALIDATION.md** - React Hook Form + Zod

---

## Code Locations

### KMP Projects

```
feature/
└── {name}/src/commonMain/kotlin/org/{{package}}/feature/{name}/
    ├── {Name}Screen.kt        # Composable UI
    ├── {Name}ViewModel.kt     # State management
    ├── {Name}UiState.kt       # UI state sealed class
    ├── {Name}Action.kt        # User actions (optional)
    ├── navigation/
    │   └── {Name}Navigation.kt
    └── di/
        └── {Name}Module.kt
```

### Web Projects

```
src/
├── app/                    # Next.js App Router pages
│   └── {feature}/
│       ├── page.tsx        # Page component
│       ├── loading.tsx     # Loading state
│       └── error.tsx       # Error boundary
├── components/             # React components
│   └── {feature}/
│       ├── {Feature}Card.tsx
│       ├── {Feature}List.tsx
│       └── {Feature}Form.tsx
└── stores/                 # Zustand stores
    └── {feature}Store.ts
```

---

## Module Structure

### KMP Projects

Each feature module follows this pattern:

```
feature/{name}/
├── build.gradle.kts
└── src/
    ├── commonMain/kotlin/...
    │   ├── {Name}Screen.kt
    │   ├── {Name}ViewModel.kt
    │   ├── {Name}UiState.kt
    │   ├── navigation/
    │   └── di/
    ├── commonTest/kotlin/...
    │   └── {Name}ViewModelTest.kt
    └── androidInstrumentedTest/kotlin/...
        └── {Name}ScreenTest.kt
```

### Web Projects

Each feature follows this structure:

```
src/components/{feature}/
├── {Feature}Card.tsx          # Presentational component
├── {Feature}List.tsx          # List container
├── {Feature}Form.tsx          # Form component
├── {Feature}Container.tsx     # Container with logic
└── __tests__/
    ├── {Feature}Card.test.tsx
    └── {Feature}Form.test.tsx
```

---

## State Management

### KMP: MVI Pattern

```
State (data class) ←→ ViewModel ←→ Screen
                    ↓
              Events (one-shot)
              Actions (user input)
```

### Web: Zustand + TanStack Query

```
Server State (TanStack) ←→ Component ←→ Client State (Zustand)
                        ↓
                  Mutations/Queries
```

---

## Commands

| Command | Purpose |
|---------|---------|
| `/feature [name]` | Generate feature module |
| `/implement [feature]` | Full implementation |
| `/gap-analysis feature` | Check implementation gaps |
| `/enforce-index modules` | Validate MODULES_INDEX |
| `/enforce-index screens` | Validate SCREENS_INDEX |
