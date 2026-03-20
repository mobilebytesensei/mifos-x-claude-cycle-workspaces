# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mobile-wallet/feature-layer/LAYER_GUIDE.md"
# last_modified: "2026-03-20"

# Feature Layer Guide - mobile-wallet

> Screen and ViewModel documentation

---

## Layer Purpose

The feature layer documents:
- Screen composables
- ViewModels (state, events, actions)
- Navigation patterns
- UI components

---

## Architecture Pattern

```
┌─────────────────────────────────────────────────────┐
│                     Screen                           │
│              (Compose UI Layer)                      │
├─────────────────────────────────────────────────────┤
│                   ViewModel                          │
│         (State, Events, Actions, Effects)            │
├─────────────────────────────────────────────────────┤
│                   Use Cases                          │
│              (Business Logic)                        │
├─────────────────────────────────────────────────────┤
│                  Repositories                        │
│               (Data Access)                          │
└─────────────────────────────────────────────────────┘
```

---

## Directory Structure

```
feature-layer/
├── MODULES_INDEX.md       # Module registry
├── SCREENS_INDEX.md       # Screen registry
├── LAYER_GUIDE.md         # This file
├── features/              # Per-module documentation
└── instructions/          # Implementation patterns
    ├── VIEWMODEL.md
    ├── COMPOSE.md
    ├── NAVIGATION.md
    └── DI.md
```

---

## Source Locations

| Component | Path |
|-----------|------|
| Features | `source/mobile-wallet/feature/` |
| Navigation | `source/mobile-wallet/cmp-shared/` |

---

## ViewModel Pattern

```kotlin
class FeatureViewModel(
    private val useCase: FeatureUseCase
) : ViewModel() {

    // State
    private val _state = MutableStateFlow(FeatureState())
    val state: StateFlow<FeatureState> = _state.asStateFlow()

    // Events (one-time)
    private val _event = Channel<FeatureEvent>()
    val event = _event.receiveAsFlow()

    // Actions
    fun onAction(action: FeatureAction) {
        when (action) {
            is FeatureAction.Load -> load()
            is FeatureAction.Submit -> submit()
        }
    }
}
```

---

## Commands

| Command | Purpose |
|---------|---------|
| `/feature [module]` | Document feature |
| `/implement [feature]` | Generate implementation |
| `/gap-analysis feature` | Check gaps |
