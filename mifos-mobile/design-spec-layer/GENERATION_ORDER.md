# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mifos-mobile/design-spec-layer/GENERATION_ORDER.md"
# last_modified: "2026-03-20"

# Design Layer Generation Order

> Defines the intelligent generation sequence for design-spec-layer files.
> Each file builds upon previous files, enabling auto-population of content.

**Version**: 1.0.0
**Last Updated**: 2025-01-13

---

## Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         GENERATION PIPELINE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   USER REQUEST                                                               │
│        │                                                                     │
│        ▼                                                                     │
│   ┌─────────┐    ┌─────────┐    ┌──────────┐    ┌─────────────┐             │
│   │ SPEC.md │───▶│ API.md  │───▶│MOCKUP.md │───▶│ PROMPTS_*.md│             │
│   └─────────┘    └─────────┘    └──────────┘    └─────────────┘             │
│        │              │              │                 │                     │
│        └──────────────┴──────────────┴─────────────────┘                     │
│                              │                                               │
│                              ▼                                               │
│                    ┌────────────────┐                                        │
│                    │   STATUS.md    │                                        │
│                    └────────────────┘                                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Generation Phases

### Phase 1: SPEC.md (Foundation)

**Priority**: P0 - Must exist before any other file
**Input**: User request, feature idea, product requirements
**Command**: `/design [feature]`

#### What SPEC.md Defines:
```yaml
extracts:
  feature_name: "Title of the feature"
  feature_description: "One-line description"
  user_stories: "List of user stories"
  screens: "List of screen names"
  components: "UI components needed"
  states: "UI states (success, loading, empty, error)"
  requirements_functional: "What the feature does"
  requirements_nonfunctional: "Performance, accessibility"
  acceptance_criteria: "Definition of done"
```

#### Auto-Population Rules:
```yaml
# SPEC.md populates these fields in other files:
feeds:
  API.md:
    - feature_name → ${FEATURE_NAME}
    - requirements_functional → endpoint definitions
    - user_stories → API use cases

  MOCKUP.md:
    - screens → screen sections
    - components → component wireframes
    - states → state variations

  STATUS.md:
    - feature_name → ${FEATURE_NAME}
    - screens → implementation checklist
```

---

### Phase 2: API.md (Data Contract)

**Priority**: P0 - Required for data-driven features
**Input**: SPEC.md requirements
**Command**: Auto-generated after SPEC.md or `/design [feature] --api`

#### What API.md Defines:
```yaml
extracts:
  base_url: "API base URL"
  auth_method: "Authentication type"
  endpoints: "List of endpoints with method, URL, purpose"
  request_dtos: "Request data structures"
  response_dtos: "Response data structures"
  error_codes: "Error handling definitions"
```

#### Auto-Population Rules:
```yaml
# Extract from SPEC.md:
from_spec:
  - user_story: "As a user, I can view my profile"
    generates:
      endpoint: "GET /api/v1/profile"
      response_dto: "ProfileResponse"

  - user_story: "As a user, I can update my settings"
    generates:
      endpoint: "PUT /api/v1/settings"
      request_dto: "UpdateSettingsRequest"
      response_dto: "SettingsResponse"

# API.md populates:
feeds:
  MOCKUP.md:
    - response_dtos → data fields in wireframes
    - endpoints → loading/error state triggers

  client-layer:
    - endpoints → Service.kt methods
    - request_dtos → Request data classes
    - response_dtos → Response data classes
```

---

### Phase 3: MOCKUP.md (UI Structure)

**Priority**: P1 - Visual representation
**Input**: SPEC.md screens + API.md data
**Command**: Auto-generated or `/design [feature] --mockup`

#### What MOCKUP.md Defines:
```yaml
extracts:
  screen_layouts: "ASCII wireframes for each screen"
  component_hierarchy: "Parent-child relationships"
  navigation_flow: "Screen transitions"
  state_variations: "Success, loading, empty, error states"
  interaction_points: "Buttons, inputs, gestures"
```

#### Auto-Population Rules:
```yaml
# Extract from SPEC.md + API.md:
from_spec:
  - screen: "Home"
    components: ["Header", "MovieList", "BottomNav"]

from_api:
  - endpoint: "GET /api/movies"
    populates:
      - MovieList items
      - Loading state
      - Empty state message
      - Error state message

# MOCKUP.md populates:
feeds:
  PROMPTS_FIGMA.md:
    - screen_layouts → natural language descriptions
    - components → component prompts
    - states → state-specific prompts

  PROMPTS_STITCH.md:
    - screen_layouts → exact measurements
    - components → MD3 specifications

  feature-layer:
    - screens → Screen.kt composables
    - components → Component.kt files
```

---

### Phase 4: AI Prompts (Parallel Generation)

#### 4a. PROMPTS_FIGMA.md

**Priority**: P2 - Design tooling
**Input**: MOCKUP.md structure
**Command**: Auto-generated or `/mockup [feature] --figma`

```yaml
extracts:
  screen_prompts: "Natural language for each screen"
  component_prompts: "Component descriptions"
  style_guidelines: "Colors, typography, spacing"

# Auto-population from MOCKUP.md:
from_mockup:
  - ascii_wireframe → descriptive prompt
  - component_list → component section
  - state: "loading" → shimmer description
  - state: "empty" → empty state prompt
  - state: "error" → error state prompt
```

#### 4b. PROMPTS_STITCH.md

**Priority**: P2 - Design tooling
**Input**: MOCKUP.md + design-tokens.json
**Command**: Auto-generated or `/mockup [feature] --stitch`

```yaml
extracts:
  exact_measurements: "dp values for all elements"
  color_codes: "Hex values from design tokens"
  typography_specs: "Font sizes, weights, line heights"
  spacing_grid: "8dp base grid values"

# Auto-population:
from_mockup:
  - component → exact size in dp
  - layout → position coordinates

from_design_tokens:
  - colors → hex values
  - typography → sp values
  - spacing → dp values
```

---

### Phase 5: Tracking Files

#### 5a. FIGMA_LINKS.md

**Priority**: P3 - Organization
**Input**: Generated Figma files (manual entry)
**Command**: Created empty, populated manually

```yaml
structure:
  - main_files: "Links to Figma files"
  - screen_links: "Frame-specific links"
  - version_history: "Design iterations"
```

#### 5b. STATUS.md

**Priority**: P1 - Progress tracking
**Input**: All design files
**Command**: Auto-updated by `/gap-analysis`

```yaml
# Auto-population from all files:
tracks:
  spec_status: "SPEC.md completeness"
  api_status: "API.md completeness"
  mockup_status: "MOCKUP.md completeness"
  figma_status: "Figma file status"
  implementation_status: "Code implementation %"

# Updated by:
  - /design → marks design files complete
  - /gap-analysis → updates percentages
  - /implement → marks implementation progress
```

---

## Intelligent Extraction Rules

### From SPEC.md to API.md

```yaml
extraction_patterns:
  # User stories → Endpoints
  - pattern: "As a user, I can {action} {resource}"
    generates:
      GET: "view, see, browse, list, search"
      POST: "create, add, submit, send"
      PUT: "update, edit, modify, change"
      DELETE: "delete, remove, cancel"

  # Example:
  - input: "As a user, I can view my watchlist"
    output:
      method: GET
      url: "/api/v1/watchlist"
      response: "WatchlistResponse"

  # Requirements → DTOs
  - pattern: "Display {field1}, {field2}, {field3}"
    generates:
      dto_fields: [field1, field2, field3]
```

### From SPEC.md to MOCKUP.md

```yaml
extraction_patterns:
  # Screens → Wireframe sections
  - pattern: "Screen: {name}"
    generates:
      section: "## {name} Screen"
      states: [Success, Loading, Empty, Error]

  # Components → ASCII blocks
  - pattern: "Component: {name} - {description}"
    generates:
      wireframe_block: |
        ┌─────────────────┐
        │ {name}          │
        │ {description}   │
        └─────────────────┘
```

### From API.md to MOCKUP.md

```yaml
extraction_patterns:
  # Response fields → Display elements
  - pattern: "response.{field}: {type}"
    generates:
      text_element: "{field} label + value"

  # List responses → List components
  - pattern: "response.items: List<{Type}>"
    generates:
      list_component: "Scrollable list of {Type} cards"
      empty_state: "No {Type}s found"
```

### From MOCKUP.md to PROMPTS

```yaml
extraction_patterns:
  # ASCII → Natural language (FIGMA)
  - input: |
      ┌─────────────────────────┐
      │ ← Title              ⋮ │
      ├─────────────────────────┤
      │ [Movie Poster]  Title   │
      │                 Rating  │
      └─────────────────────────┘
    output_figma: |
      Create a mobile screen with:
      - Top app bar with back button, title, and menu
      - Movie card with poster image on left
      - Title and rating on right

  # ASCII → Exact specs (STITCH)
  - input: "┌─────────────────────────┐" (width indicator)
    output_stitch: |
      - Size: 393x64dp
      - Background: Primary (#6200EE)
      - Padding: 16dp horizontal
```

---

## Generation Commands

### Full Feature Design

```bash
# Generate all design files in order
/design [feature]

# Execution order:
# 1. Create/update SPEC.md
# 2. Generate API.md from SPEC
# 3. Generate MOCKUP.md from SPEC + API
# 4. Generate PROMPTS_FIGMA.md from MOCKUP
# 5. Generate PROMPTS_STITCH.md from MOCKUP + tokens
# 6. Create FIGMA_LINKS.md (empty template)
# 7. Update STATUS.md
```

### Incremental Generation

```bash
# Generate specific file
/design [feature] --spec      # Only SPEC.md
/design [feature] --api       # Only API.md (requires SPEC)
/design [feature] --mockup    # Only MOCKUP.md (requires SPEC + API)
/design [feature] --prompts   # Only PROMPTS_*.md (requires MOCKUP)

# Gap filling
/gap-implement [feature] design   # Fill missing design files
```

### Regeneration

```bash
# Regenerate downstream files after SPEC change
/design [feature] --refresh

# This will:
# 1. Read updated SPEC.md
# 2. Regenerate API.md sections affected by changes
# 3. Update MOCKUP.md with new screens/components
# 4. Regenerate PROMPTS_*.md
# 5. Update STATUS.md
```

---

## File Dependencies Graph

```
                    ┌─────────────────┐
                    │  User Request   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    SPEC.md      │ ◄── Foundation
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
     ┌─────────────┐  ┌───────────┐  ┌───────────┐
     │   API.md    │  │ STATUS.md │  │ MOCKUP.md │
     └──────┬──────┘  └───────────┘  └─────┬─────┘
            │                              │
            │         ┌────────────────────┤
            │         │                    │
            ▼         ▼                    ▼
     ┌─────────────────────┐    ┌──────────────────┐
     │  client-layer/      │    │ PROMPTS_FIGMA.md │
     │  - Service.kt       │    └──────────────────┘
     │  - Repository.kt    │    ┌──────────────────┐
     │  - DTOs.kt          │    │ PROMPTS_STITCH.md│
     └─────────────────────┘    └────────┬─────────┘
                                         │
                                         ▼
                                ┌──────────────────┐
                                │  Figma Files     │
                                └────────┬─────────┘
                                         │
                                         ▼
                                ┌──────────────────┐
                                │ FIGMA_LINKS.md   │
                                └──────────────────┘
```

---

## Validation Rules

### Before Generation

```yaml
phase_1_spec:
  required: user_request
  validates:
    - feature_name: "Must be kebab-case"
    - user_stories: "At least 1 story"
    - screens: "At least 1 screen"

phase_2_api:
  required: SPEC.md
  validates:
    - spec_has_requirements: true
    - spec_has_user_stories: true

phase_3_mockup:
  required: [SPEC.md, API.md]
  validates:
    - spec_has_screens: true
    - api_has_endpoints: true

phase_4_prompts:
  required: MOCKUP.md
  validates:
    - mockup_has_wireframes: true
    - mockup_has_states: true
```

### After Generation

```yaml
completeness_check:
  SPEC.md:
    - has_overview: true
    - has_user_stories: true
    - has_screens: true
    - has_requirements: true

  API.md:
    - has_endpoints: true
    - has_dtos: true
    - has_error_handling: true

  MOCKUP.md:
    - has_all_screens: "matches SPEC.screens"
    - has_all_states: [success, loading, empty, error]
    - has_navigation: true
```

---

## Related Files

| File | Purpose |
|------|---------|
| `/design` command | Executes generation pipeline |
| `/gap-analysis` | Identifies missing files |
| `/gap-implement` | Fills gaps automatically |
| `design-tokens.json` | Provides color/typography values |
| `FEATURES_INDEX.md` | Lists all features |

