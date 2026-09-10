# template_meta
# template_version: "2.86.0"
# template_path: "templates/blueprints/workspace-project/testing-layer/LAYER_GUIDE.md"
# last_modified: "2026-03-19"

# Testing Layer Guide - mifos-products

> **Project Type:** {{project_type}}
> Conventions for testing infrastructure and patterns.

---

## Purpose

The testing layer provides shared testing utilities, fake implementations, fixtures, and test patterns for all feature modules.

---

## Directory Structure

```
testing-layer/
├── LAYER_STATUS.md        # Test coverage status
├── TEST_TAGS_INDEX.md     # O(1) TestTag lookup
├── TEST_PATTERNS.md       # Pattern reference
├── TEST_FIXTURES_INDEX.md # Fixture lookup
├── FAKE_REPOS_INDEX.md    # Fake repo lookup
├── LAYER_GUIDE.md         # This file
├── patterns/              # Detailed patterns
└── instructions/          # Project-type specific guides
    └── {kmp|web}/         # Testing patterns
```

---

## Implementation Guides

Based on your project type, use these guides:

### For KMP Projects (Kotlin Multiplatform)

See `instructions/kmp/`:
- **VIEWMODEL_TEST.md** - ViewModel testing patterns
- **SCREEN_TEST.md** - Compose UI testing
- **FAKE_REPOSITORY.md** - Fake implementation patterns
- **INTEGRATION_TEST.md** - Integration testing

### For Web Projects (TypeScript/React)

See `templates/instructions/testing-layer/web/`:
- **JEST_SETUP.md** - Jest configuration and setup
- **REACT_TESTING_LIBRARY.md** - Component testing patterns
- **E2E_PLAYWRIGHT.md** - End-to-end testing with Playwright

### For Backend Projects (Python/Node.js)

See `templates/instructions/testing-layer/backend/`:
- **API_TEST.md** - REST/GraphQL endpoint testing
- **DATABASE_TEST.md** - Schema, repositories, migrations
- **ASYNC_TEST.md** - Background jobs, events, webhooks
- **INTEGRATION_TEST.md** - Service-to-service testing
- **E2E_TEST.md** - Full request lifecycle testing

---

## Test Types

### KMP Projects

| Type | Location | Framework | Purpose |
|------|----------|-----------|---------|
| Unit | `commonTest` | kotlin-test | ViewModel, Repository |
| Screen | `androidInstrumentedTest` | Compose UI Test | UI behavior |
| Screenshot | `test` (Android) | Roborazzi | Visual regression |
| Integration | `androidTest` | Espresso | End-to-end |

### Web Projects

| Type | Location | Framework | Purpose |
|------|----------|-----------|---------|
| Unit | `__tests__` | Vitest/Jest | Services, utilities |
| Component | `__tests__` | React Testing Library | UI behavior |
| Hook | `__tests__` | @testing-library/react-hooks | Custom hooks |
| E2E | `tests/e2e` | Playwright | Full user flows |

---

### Backend Projects

| Type | Location | Framework | Purpose |
|------|----------|-----------|---------|
| Unit | `tests/unit` | pytest / Jest | Services, validators |
| API | `tests/api` | httpx+pytest / Supertest | Endpoint testing |
| Database | `tests/integration` | pytest / Knex test | Repositories, migrations |
| Async | `tests/integration` | pytest-asyncio / Jest | Jobs, events, webhooks |
| E2E | `tests/e2e` | pytest+Docker / Testcontainers | Full lifecycle |

---

## Code Location

### KMP Projects

```
core/testing/src/
├── commonMain/kotlin/org/{{package}}/core/testing/
│   ├── di/TestModule.kt           # Koin test module
│   ├── fake/                       # Fake implementations
│   │   ├── FakeAuthRepository.kt
│   │   └── Fake{Feature}Repository.kt
│   ├── fixture/                    # Test data factories
│   │   ├── UserFixture.kt
│   │   └── {Entity}Fixture.kt
│   ├── tags/                       # TestTag objects
│   │   ├── AuthTestTags.kt
│   │   └── {Feature}TestTags.kt
│   └── util/
│       ├── FlowTestExtensions.kt
│       └── TestCoroutineExtensions.kt
├── androidMain/kotlin/...
│   └── ComposeTestHelpers.kt
└── iosMain/kotlin/...
    └── IosTestUtils.kt
```

### Web Projects

```
src/
├── __tests__/              # Unit/component tests
│   ├── components/
│   │   └── {Feature}Card.test.tsx
│   ├── hooks/
│   │   └── use{Feature}.test.ts
│   └── services/
│       └── {feature}Service.test.ts
├── mocks/                  # MSW handlers
│   ├── handlers.ts
│   ├── server.ts
│   └── fixtures/
│       └── {feature}Fixtures.ts
└── tests/
    └── e2e/                # Playwright tests
        ├── pages/
        │   └── {Feature}Page.ts
        └── {feature}.spec.ts
```

### Backend Projects

```
tests/                          # Python (pytest)
├── conftest.py                 # Shared fixtures
├── unit/
│   ├── test_validators.py
│   └── test_transformers.py
├── integration/
│   ├── test_user_service.py
│   └── test_order_repository.py
├── api/
│   ├── test_auth_routes.py
│   └── test_resource_routes.py
└── e2e/
    └── test_checkout_flow.py

__tests__/                      # Node.js (Jest)
├── setup.ts
├── unit/
├── integration/
├── api/
└── e2e/
```

---

## Testing Patterns

### Test Naming Convention

Both project types use `given_when_then` naming:

```
givenInitialState_whenViewModelCreated_thenStateHasDefaults
givenSuccessResponse_whenDataLoaded_thenStateIsSuccess
```

### Fixture Pattern

Create reusable test data factories:

**KMP:**
```kotlin
object UserFixture {
    fun create(id: Long = 1, name: String = "Test User") = User(id, name)
    fun createList(count: Int = 3) = (1..count).map { create(id = it.toLong()) }
}
```

**Web:**
```typescript
export const createUser = (overrides?: Partial<User>): User => ({
  id: '1',
  name: 'Test User',
  email: 'test@example.com',
  ...overrides,
});
```

---

## Commands

| Command | Purpose |
|---------|---------|
| `/gap-analysis testing` | Check test coverage |
| `/implement [feature]` | Phase 5 creates test stubs |
| `/test [feature]` | Run feature tests |
