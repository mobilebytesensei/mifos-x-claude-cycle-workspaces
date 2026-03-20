# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mobile-wallet/design-spec-layer/_shared/PATTERNS.md"
# last_modified: "2026-03-20"

# UI Patterns - mobile-wallet

> Common UI patterns and conventions

---

## Screen Patterns

### List Screen

```kotlin
@Composable
fun ListScreen(
    state: ListState,
    onAction: (ListAction) -> Unit
) {
    Scaffold(
        topBar = { TopAppBar(...) }
    ) { padding ->
        when {
            state.isLoading -> LoadingScreen()
            state.error != null -> ErrorScreen(
                message = state.error,
                onRetry = { onAction(ListAction.Retry) }
            )
            state.items.isEmpty() -> EmptyScreen()
            else -> LazyColumn {
                items(state.items) { item ->
                    ItemRow(item, onClick = { onAction(ListAction.Select(item)) })
                }
            }
        }
    }
}
```

### Form Screen

```kotlin
@Composable
fun FormScreen(
    state: FormState,
    onAction: (FormAction) -> Unit
) {
    Scaffold(
        topBar = { TopAppBar(...) },
        bottomBar = {
            Button(
                onClick = { onAction(FormAction.Submit) },
                enabled = state.isValid
            ) {
                Text("Submit")
            }
        }
    ) { padding ->
        Column(modifier = Modifier.padding(padding)) {
            TextField(
                value = state.field1,
                onValueChange = { onAction(FormAction.UpdateField1(it)) }
            )
            // More fields...
        }
    }
}
```

### Detail Screen

```kotlin
@Composable
fun DetailScreen(
    state: DetailState,
    onAction: (DetailAction) -> Unit
) {
    Scaffold(
        topBar = {
            TopAppBar(
                navigationIcon = { BackButton(onAction(DetailAction.Back)) }
            )
        }
    ) { padding ->
        when {
            state.isLoading -> LoadingScreen()
            state.data != null -> DetailContent(state.data)
        }
    }
}
```

---

## State Patterns

### UI State

```kotlin
data class FeatureState(
    val isLoading: Boolean = false,
    val error: String? = null,
    val data: DataType? = null
)
```

### Actions

```kotlin
sealed interface FeatureAction {
    data object Load : FeatureAction
    data object Retry : FeatureAction
    data class Select(val item: Item) : FeatureAction
}
```

### Events (One-time)

```kotlin
sealed interface FeatureEvent {
    data class Navigate(val route: String) : FeatureEvent
    data class ShowSnackbar(val message: String) : FeatureEvent
}
```

---

## Navigation Patterns

### Bottom Navigation

5 main destinations:
1. Home
2. Accounts
3. Payments
4. History
5. Profile

### Nested Navigation

Each bottom nav destination has its own navigation graph.

### Deep Links

Support for:
- `mifospay://transfer/{accountId}`
- `mifospay://qr/{data}`
