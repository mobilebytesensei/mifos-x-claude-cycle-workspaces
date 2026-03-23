# template_meta
# template_version: "2.86.5"
# template_path: "workspaces/mifos-x/mifos-x-field-officer-app/testing-layer/TEST_TAGS_INDEX.md"
# last_modified: "2026-03-20"

# Test Tags Index - O(1) Lookup

> **Purpose**: Instant lookup for TestTags objects used in UI testing.

---

## Quick Reference

| # | Feature | TestTags Object | Tags Count | Screen Coverage | Path |
|:-:|---------|-----------------|:----------:|:---------------:|------|
| 1 | {{FEATURE}} | {{FEATURE}}TestTags | {{COUNT}} | {{SCREENS}} | core/testing/.../tags/{{FEATURE}}TestTags.kt |

---

## Category Index

### Core Features
| Feature | TestTags | Path |
|---------|----------|------|

### Account Features
| Feature | TestTags | Path |
|---------|----------|------|

### Transaction Features
| Feature | TestTags | Path |
|---------|----------|------|

---

## Keyword -> TestTags Mapping

```yaml
# Auth
login: AuthTestTags
register: AuthTestTags
authentication: AuthTestTags

# Home
home: HomeTestTags
dashboard: HomeTestTags

# Accounts
accounts: AccountsTestTags
savings: SavingsAccountTestTags
loans: LoanAccountTestTags
```

---

## TestTags Pattern

```kotlin
object FeatureTestTags {
    // Screens
    const val SCREEN = "feature:screen"
    const val CONTENT = "feature:content"

    // Components
    const val LIST = "feature:list"
    const val ITEM = "feature:item"
    const val BUTTON = "feature:button"

    // States
    const val LOADING = "feature:loading"
    const val ERROR = "feature:error"
    const val EMPTY = "feature:empty"
}
```

---

## Usage in Tests

```kotlin
// In Screen
Modifier.testTag(FeatureTestTags.SCREEN)

// In Test
composeTestRule
    .onNodeWithTag(FeatureTestTags.SCREEN)
    .assertIsDisplayed()
```

---

## File Structure

```
core/testing/src/commonMain/kotlin/org/{{package}}/core/testing/
└── tags/
    ├── AuthTestTags.kt
    ├── HomeTestTags.kt
    ├── AccountsTestTags.kt
    └── ...
```

---

## Commands

```bash
/enforce-index test-tags   # Validate this index
/implement [feature]       # Creates TestTags (Phase 5)
/gap-analysis testing      # Check testing layer gaps
```
