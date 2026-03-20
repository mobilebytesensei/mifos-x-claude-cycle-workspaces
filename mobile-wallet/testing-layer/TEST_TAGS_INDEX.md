# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mobile-wallet/testing-layer/TEST_TAGS_INDEX.md"
# last_modified: "2026-03-20"

# Test Tags Index - mobile-wallet

> Test tags for UI testing

---

## Test Tag Convention

```kotlin
object FeatureTestTags {
    const val SCREEN = "feature:screen"
    const val BUTTON_SUBMIT = "feature:button:submit"
    const val INPUT_AMOUNT = "feature:input:amount"
}
```

---

## Discovered Test Tags

| Module | Test Tags File | Status |
|--------|----------------|:------:|
| home | HomeTestTags | ⬜ |
| auth | AuthTestTags | ⬜ |
| accounts | AccountsTestTags | ⬜ |
| payments | PaymentsTestTags | ⬜ |
| transfers | TransfersTestTags | ⬜ |

---

## Usage in Tests

```kotlin
@Test
fun homeScreen_showsBalance() {
    composeRule
        .onNodeWithTag(HomeTestTags.BALANCE_TEXT)
        .assertIsDisplayed()
}
```

---

## Quick Actions

```bash
# Generate test tags for feature
/gen-tests [feature] --tags

# Check test tag coverage
/gap-analysis testing
```
