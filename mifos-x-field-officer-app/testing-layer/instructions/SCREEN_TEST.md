# Screen Test Pattern

> Detailed instructions for testing Compose screens in KMP projects

---

## Overview

Screen tests verify:
- UI renders correctly for each state
- User interactions trigger correct actions
- Accessibility (content descriptions, testTags)
- Visual appearance (with screenshots)

---

## Current State of Screen Tests in References

> **Important**: The reference projects have very limited Compose UI tests.
> The only screen test found (`QrImportScreenTest.kt`) tests business logic
> and platform behavior using plain `kotlin.test` assertions -- it does NOT
> use Compose UI test framework (`ComposeTestRule`, `setContent`, etc.).
>
> **Reason**: Compose Multiplatform UI testing in `commonTest` has limited
> KMP support. Android instrumented tests (`androidInstrumentedTest`) work
> but are platform-specific.

### Reference Screen Test Pattern (Logic-Only)

```kotlin
class QrImportScreenTest {
    @Test
    fun givenWebDesktopPlatform_whenRendering_thenScannerOverlaysHidden() {
        val isWebDesktop = WebPlatform.isWebDesktop
        if (isWebDesktop) {
            assertTrue(WebPlatform.isWeb)
        }
    }

    @Test
    fun givenIsProcessingTrue_whenRendering_thenLoadingUIShown() {
        val isProcessing = true
        assertTrue(isProcessing)
    }
}
```

This pattern tests screen BEHAVIOR and FLAGS, not visual rendering.

---

## Recommended Approach

### Option A: Logic-Only Screen Tests (commonTest -- Recommended)

Write screen tests in `commonTest` that verify screen logic without
Compose UI framework. This is cross-platform and matches reference patterns.

**File Location:**
```
feature/${feature}/src/commonTest/kotlin/org/${package}/feature/${feature}/${Feature}ScreenTest.kt
```

```kotlin
class ${Feature}ScreenTest {

    @Test
    fun givenLoadingState_whenRendering_thenShowsLoadingIndicator() {
        val state = ${Feature}State(viewState = ViewState.Loading)
        assertTrue(state.viewState is ViewState.Loading)
    }

    @Test
    fun givenErrorState_whenRendering_thenShowsErrorMessage() {
        val state = ${Feature}State(
            viewState = ViewState.Error("Network error")
        )
        val error = state.viewState as ViewState.Error
        assertEquals("Network error", error.message)
    }

    @Test
    fun givenShowHeaderFalse_whenInNestedContext_thenHeaderHidden() {
        val showHeader = false
        assertFalse(showHeader)
    }
}
```

### Option B: Compose UI Tests (androidInstrumentedTest -- Aspirational)

When Android-specific UI tests are needed, use the Compose test framework.
These only run on Android and require instrumented test infrastructure.

**File Location:**
```
feature/${feature}/src/androidInstrumentedTest/kotlin/org/${package}/feature/${feature}/${Feature}ScreenTest.kt
```

**Dependencies:**
```kotlin
kotlin {
    sourceSets {
        androidInstrumentedTest.dependencies {
            implementation(libs.compose.ui.test.junit4)
            implementation(libs.compose.ui.test.manifest)
        }
    }
}
```

```kotlin
class ${Feature}ScreenTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun loadingState_displaysLoadingIndicator() {
        composeTestRule.setContent {
            ${Feature}Content(
                state = ${Feature}State(uiState = ${Feature}UiState.Loading),
                onAction = {}
            )
        }

        composeTestRule
            .onNodeWithTag(${Feature}TestTags.LOADING)
            .assertIsDisplayed()
    }

    @Test
    fun itemClick_triggersAction() {
        var receivedAction: ${Feature}Action? = null
        val testData = ${Feature}Fixtures.createList(3)

        composeTestRule.setContent {
            ${Feature}Content(
                state = ${Feature}State(
                    uiState = ${Feature}UiState.Success(testData)
                ),
                onAction = { receivedAction = it }
            )
        }

        composeTestRule
            .onNodeWithTag(${Feature}TestTags.item(testData[0].id))
            .performClick()

        assertEquals(
            ${Feature}Action.OnItemClick(testData[0].id),
            receivedAction
        )
    }
}
```

---

## Compose Test API Reference (Android Only)

### Finding Nodes

| Method | Purpose | Example |
|--------|---------|---------|
| `onNodeWithTag(tag)` | Find by testTag | `onNodeWithTag("auth:screen")` |
| `onNodeWithText(text)` | Find by text | `onNodeWithText("Login")` |
| `onNodeWithContentDescription(desc)` | Find by a11y label | `onNodeWithContentDescription("Close")` |
| `onAllNodesWithTag(tag)` | Find all matching | `onAllNodesWithTag("item")` |
| `onRoot()` | Get root node | `onRoot()` |

### Assertions

| Method | Purpose |
|--------|---------|
| `assertIsDisplayed()` | Verify visible |
| `assertDoesNotExist()` | Verify not in tree |
| `assertIsEnabled()` | Verify clickable |
| `assertIsNotEnabled()` | Verify disabled |
| `assertTextEquals(text)` | Verify text content |
| `assertHasClickAction()` | Verify clickable |

### Actions

| Method | Purpose |
|--------|---------|
| `performClick()` | Tap element |
| `performTextInput(text)` | Type text |
| `performTextClearance()` | Clear text field |
| `performScrollTo()` | Scroll to element |
| `performSwipeLeft()` | Swipe gesture |
| `performTouchInput { swipeUp() }` | Custom touch |

---

## Test Categories

### 1. State Rendering Tests

Test each UI state renders correctly.

```kotlin
@Test
fun givenLoadingState_thenProgressIndicatorShown() { ... }

@Test
fun givenSuccessState_thenContentShown() { ... }

@Test
fun givenErrorState_thenErrorViewShown() { ... }

@Test
fun givenEmptyState_thenEmptyViewShown() { ... }
```

### 2. User Interaction Tests

Test all clickable elements trigger correct actions.

```kotlin
@Test
fun givenButton_whenClicked_thenActionTriggered() {
    var action: Action? = null

    composeTestRule.setContent {
        Screen(onAction = { action = it })
    }

    composeTestRule.onNodeWithTag("button").performClick()

    assertEquals(Action.ButtonClicked, action)
}
```

### 3. Form Tests

Test input fields and validation.

```kotlin
@Test
fun givenInput_whenTyping_thenActionEmitted() { ... }

@Test
fun givenInvalidForm_whenRendered_thenSubmitDisabled() { ... }
```

---

## TestTag Best Practices

### Tag Naming

```kotlin
object ${Feature}TestTags {
    const val SCREEN = "${feature}:screen"
    const val LOADING = "${feature}:loading"
    const val ERROR = "${feature}:error"
    const val EMPTY = "${feature}:empty"
    const val LIST = "${feature}:list"
    const val FAB = "${feature}:fab"

    fun item(id: Long) = "${feature}:item:$id"
}
```

---

## Test Coverage Checklist

For each screen, test:

- [ ] State object construction (commonTest)
- [ ] State flag behavior (commonTest)
- [ ] Loading state displays correctly (androidInstrumentedTest)
- [ ] Success state displays content (androidInstrumentedTest)
- [ ] Error state displays message and retry (androidInstrumentedTest)
- [ ] Empty state displays empty message (androidInstrumentedTest)
- [ ] All clickable elements trigger actions (androidInstrumentedTest)
- [ ] Form inputs update state (androidInstrumentedTest)
- [ ] Accessibility labels present (androidInstrumentedTest)

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Putting Compose UI tests in commonTest | Use commonTest for logic-only; androidInstrumentedTest for Compose |
| Not finding node | Check testTag is applied |
| Flaky tests | Use `waitUntil` for async |
| Testing implementation | Test behavior, not structure |
| Missing states | Test all UI states |
