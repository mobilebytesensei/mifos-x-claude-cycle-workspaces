# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mifos-mobile/design-spec-layer/MOCKUP_GENERATION_GUIDE.md"
# last_modified: "2026-03-20"

# Mockup Generation Guide

> Instructions for Claude to generate professional, comprehensive mockups with deep analysis.

**Version**: 1.0.0
**Last Updated**: 2025-01-13

---

## Overview

This guide ensures Claude generates **professional-grade mockups** by performing deep analysis of SPEC.md and API.md, then systematically filling all gaps.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MOCKUP GENERATION WORKFLOW                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  INPUT FILES                    ANALYSIS                    OUTPUT          │
│  ───────────                    ────────                    ──────          │
│                                                                              │
│  ┌──────────┐                                                                │
│  │ SPEC.md  │──┐                                                             │
│  └──────────┘  │    ┌─────────────────────────┐    ┌────────────────────┐   │
│                ├───▶│   DEEP ANALYSIS         │───▶│ MOCKUP.md          │   │
│  ┌──────────┐  │    │   - Extract screens     │    │ (Professional)     │   │
│  │ API.md   │──┘    │   - Map data to UI      │    └────────────────────┘   │
│  └──────────┘       │   - Identify states     │                              │
│                     │   - List interactions   │    ┌────────────────────┐   │
│  ┌──────────┐       │   - Validate coverage   │───▶│ PROMPTS_FIGMA.md   │   │
│  │ design-  │──────▶│                         │    └────────────────────┘   │
│  │ tokens   │       └─────────────────────────┘                              │
│  └──────────┘                                      ┌────────────────────┐   │
│                                                ───▶│ PROMPTS_STITCH.md  │   │
│                                                    └────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Deep Analysis Steps

### Step 1: Extract from SPEC.md

Read SPEC.md and extract:

```yaml
extract_from_spec:
  # Feature basics
  feature_name: "Title from SPEC.md"
  feature_purpose: "One-line description"

  # Screens (CRITICAL - must get all screens)
  screens:
    - name: "Screen name from spec"
      purpose: "What this screen does"
      parent: "Navigation parent"
      entry_points: ["How user reaches this screen"]

  # User stories → UI implications
  user_stories:
    - story: "As a user, I can..."
      ui_implication: "What UI element enables this"
      screen: "Which screen"

  # UI Components mentioned
  components:
    - name: "Component name"
      type: "card/list/form/etc."
      used_in: ["Screen1", "Screen2"]

  # States mentioned
  states:
    - success: "Normal data display"
    - loading: "While fetching"
    - empty: "No data available"
    - error: "API failure"
    - offline: "No connectivity" (if applicable)

  # Interactions defined
  interactions:
    - trigger: "User action"
      result: "What happens"
      screen: "Where"
```

### Step 2: Extract from API.md

Read API.md and map data to UI:

```yaml
extract_from_api:
  # Endpoints → Screens
  endpoints:
    - endpoint: "GET /api/movies"
      maps_to:
        screen: "HomeScreen"
        section: "Movie List"
        loading_state: "Shimmer for cards"
        empty_state: "No movies found"
        error_state: "Failed to load movies"

  # Response fields → UI elements
  data_mapping:
    - field: "response.title"
      ui_element: "Title text"
      position: "Hero section, prominent"

    - field: "response.imageUrl"
      ui_element: "Image"
      position: "Card/Hero"
      fallback: "Placeholder image"

    - field: "response.items[]"
      ui_element: "List/Grid"
      component: "Card component"
      empty_message: "No items to display"

  # Error codes → Error UI
  error_mapping:
    - code: 401
      ui_message: "Please sign in again"
      action: "Sign In button"

    - code: 404
      ui_message: "Content not found"
      action: "Go Back button"

    - code: 500
      ui_message: "Something went wrong"
      action: "Retry button"
```

### Step 3: Generate Component Inventory

For each unique UI pattern, create component:

```yaml
component_inventory:
  # Standard components (always include)
  standard:
    - TopAppBar: "Navigation bar with back/title/actions"
    - BottomNavigation: "Main app navigation"
    - LoadingShimmer: "Placeholder during load"
    - EmptyState: "No content illustration"
    - ErrorState: "Error with retry"

  # Feature-specific components
  feature_specific:
    - from: "SPEC.md components section"
    - derived_from: "API.md response structure"

  # Each component needs:
  component_requirements:
    - wireframe: "ASCII representation"
    - specifications: "Size, padding, colors"
    - states: "Default, pressed, selected, disabled"
    - data_binding: "Which API fields populate it"
    - accessibility: "Screen reader labels"
```

### Step 4: Generate All UI States

**MANDATORY**: Every screen MUST have all states:

```yaml
mandatory_states:
  success:
    description: "Data loaded successfully"
    wireframe: "Full screen with real content"
    annotations: "Section heights, data sources"

  loading:
    description: "Data being fetched"
    wireframe: "Shimmer placeholders matching success layout"
    specifications:
      - shimmer_color: "#E0E0E0 (light) / #2A2A2A (dark)"
      - animation: "1000ms gradient sweep"
      - placeholder_shapes: "Match content dimensions"

  empty:
    description: "No data available"
    wireframe: "Centered illustration + message + CTA"
    requirements:
      - illustration: "200x200dp, related to context"
      - title: "20sp, clear message"
      - subtitle: "14sp, helpful hint"
      - cta: "Action to resolve empty state"

  error:
    description: "Failed to load"
    wireframe: "Centered error icon + message + buttons"
    requirements:
      - icon: "error_outline, 48dp, error color"
      - title: "20sp, 'Something went wrong'"
      - message: "14sp, specific error context"
      - primary_action: "Retry button"
      - secondary_action: "Go Back (optional)"

  offline: # If applicable
    description: "No network connectivity"
    wireframe: "Cached content + offline banner"
    requirements:
      - banner: "Top banner indicating offline"
      - cached_content: "Last loaded data"
      - refresh_hint: "Pull to refresh when online"
```

### Step 5: Map All Interactions

Every touchable element needs interaction mapping:

```yaml
interaction_mapping:
  # Touch interactions
  touch:
    - element: "Every button/card/list item"
      action: "tap/long_press"
      result: "Navigate/Toggle/Submit"
      haptic: "true/false"

  # Gesture interactions
  gestures:
    - pull_refresh: "Main scrollable content"
    - swipe_horizontal: "Carousels, horizontal lists"
    - swipe_to_delete: "Deletable list items"
    - long_press: "Context menus"
    - pinch_zoom: "Images (if applicable)"

  # Navigation flows
  navigation:
    - from: "Current screen"
      trigger: "User action"
      to: "Target screen"
      params: "Data passed"
      transition: "Animation type"
```

### Step 6: Accessibility Audit

Verify accessibility requirements:

```yaml
accessibility_checklist:
  touch_targets:
    - element: "Every interactive element"
      minimum: "48x48dp"
      actual: "Verify meets minimum"

  screen_reader:
    - element: "Every meaningful element"
      label: "Clear description"
      role: "Button/Image/List/etc."

  focus_order:
    - logical: "Top-to-bottom, left-to-right"
    - grouped: "Related elements together"

  contrast:
    - text_primary: "4.5:1 minimum (AA)"
    - text_large: "3:1 minimum (AA)"
    - verify: "Against background color"
```

---

## Completeness Validation

Before finalizing MOCKUP.md, validate:

```yaml
validation_checklist:
  # Screen coverage
  screens:
    - all_spec_screens_present: true
    - all_states_for_each_screen: [success, loading, empty, error]
    - wireframes_match_data_model: true

  # Component coverage
  components:
    - all_unique_components_documented: true
    - each_has_wireframe: true
    - each_has_specifications: true
    - each_has_states: true
    - each_has_data_binding: true

  # Interaction coverage
  interactions:
    - all_buttons_mapped: true
    - all_gestures_defined: true
    - navigation_flow_complete: true
    - haptic_feedback_noted: true

  # Accessibility coverage
  accessibility:
    - touch_targets_verified: true
    - screen_reader_labels: true
    - focus_order_defined: true
    - contrast_checked: true

  # Data coverage
  data:
    - all_api_endpoints_mapped: true
    - all_fields_to_ui_mapping: true
    - error_codes_to_ui: true
    - offline_strategy_defined: true
```

---

## Gap Detection Rules

Claude MUST identify and fill gaps:

### Gap Type 1: Missing Screens

```yaml
detection: "SPEC.md mentions screen not in MOCKUP.md"
action: "Create complete wireframe for screen"
example:
  spec_mentions: "Settings screen for notification preferences"
  mockup_missing: "SettingsScreen wireframe"
  resolution: "Add full SettingsScreen with all states"
```

### Gap Type 2: Missing States

```yaml
detection: "Screen exists but states incomplete"
action: "Generate missing state wireframes"
example:
  screen: "HomeScreen"
  has: [success]
  missing: [loading, empty, error]
  resolution: "Add loading shimmer, empty illustration, error with retry"
```

### Gap Type 3: Unmapped Data

```yaml
detection: "API response field not shown in UI"
action: "Either add to wireframe or document as intentionally hidden"
example:
  api_field: "response.createdAt"
  not_in_ui: true
  resolution:
    option_a: "Add timestamp to card/detail view"
    option_b: "Document: 'createdAt intentionally not displayed'"
```

### Gap Type 4: Missing Interactions

```yaml
detection: "UI element without interaction mapping"
action: "Define interaction for every tappable element"
example:
  element: "Movie card"
  missing: "tap action, navigation target"
  resolution: "Tap → Navigate to MovieDetailScreen with movieId"
```

### Gap Type 5: Accessibility Gaps

```yaml
detection: "Interactive element without screen reader label"
action: "Add content description"
example:
  element: "Star rating icon"
  missing: "Screen reader label"
  resolution: 'contentDescription: "8.5 out of 10 stars"'
```

---

## Output Quality Standards

### Wireframe Quality

```yaml
wireframe_standards:
  # Use consistent ASCII patterns
  patterns:
    top_app_bar: |
      ┌────────────────────────────────────────────────────────┐
      │  [←]  Title                                     [⋮]   │
      └────────────────────────────────────────────────────────┘

    card: |
      ┌────────────────────┐
      │ ████████████████   │
      │ Title              │
      │ Subtitle           │
      └────────────────────┘

    list_item: |
      ┌────────────────────────────────────────────────────────┐
      │  [Icon]  Title                                   [>]   │
      │          Subtitle                                      │
      └────────────────────────────────────────────────────────┘

    button: |
      ┌──────────────────┐
      │  Button Label    │
      └──────────────────┘

    shimmer: |
      ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

  # Annotations
  annotations:
    - position: "Right side of wireframe"
    - format: "← Description (measurement)"
    - example: "← Top App Bar (64dp)"

  # Alignment
  alignment:
    - consistent_width: "60 characters typical"
    - proper_nesting: "Inner elements indented"
    - clear_boundaries: "Use box-drawing characters"
```

### Specification Quality

```yaml
specification_standards:
  # Every component needs
  required_specs:
    - size: "Width x Height in dp"
    - background: "Color code"
    - corner_radius: "In dp"
    - elevation: "Shadow level"
    - padding: "Internal spacing"
    - margin: "External spacing"

  # Every text element needs
  text_specs:
    - font_size: "In sp"
    - font_weight: "400/500/600/700"
    - line_height: "In sp"
    - color: "Hex code"
    - max_lines: "If truncated"

  # Every image needs
  image_specs:
    - size: "Width x Height"
    - corner_radius: "In dp"
    - content_mode: "Fill/Fit/Crop"
    - placeholder: "What to show while loading"
    - fallback: "What to show on error"
```

### Interaction Quality

```yaml
interaction_standards:
  # Complete mapping
  mapping:
    - element: "What is tapped"
    - action: "tap/long_press/swipe"
    - result: "Navigate/Toggle/API call"
    - feedback: "Ripple/Haptic/Sound"
    - parameters: "Data passed"

  # Navigation completeness
  navigation:
    - source: "Current screen"
    - trigger: "User action"
    - destination: "Target screen"
    - transition: "Animation type"
    - back_behavior: "What happens on back"
```

---

## Auto-Generation from API

Claude should automatically generate UI from API structure:

```yaml
api_to_ui_auto_generation:
  # List endpoint → List UI
  list_endpoint:
    api: "GET /items"
    generates:
      - horizontal_list: "If items < 10"
      - vertical_list: "If items > 10"
      - grid: "If items are visual (images)"
      - empty_state: "When items.length == 0"

  # Detail endpoint → Detail UI
  detail_endpoint:
    api: "GET /items/{id}"
    generates:
      - hero_section: "From main image/video"
      - title_block: "From title, subtitle"
      - metadata_row: "From date, rating, etc."
      - description: "From body text"
      - action_buttons: "From available actions"

  # Action endpoint → Button UI
  action_endpoint:
    api: "POST /items/{id}/favorite"
    generates:
      - toggle_button: "Favorite/Unfavorite"
      - loading_state: "While API in progress"
      - success_feedback: "Toast/Animation"
      - error_handling: "Snackbar with retry"

  # Response field → UI element
  field_mapping:
    string: "Text element"
    number: "Formatted text or progress"
    boolean: "Toggle/Checkbox/Icon state"
    url: "Image or link"
    date: "Formatted date text"
    array: "List/Chips/Tags"
    object: "Nested card/section"
```

---

## Example Deep Analysis Output

```yaml
deep_analysis_output:
  feature: "Movie Detail"

  screens_identified:
    - MovieDetailScreen (from SPEC section 2)
    - CastListScreen (from "See All" interaction)
    - SimilarMoviesScreen (from "See All" interaction)

  components_needed:
    - BackdropHeader (hero image with overlay)
    - MovieInfoCard (title, rating, meta)
    - ActionButtonRow (watchlist, watched, share)
    - MoodMatchCard (unique to this app)
    - ProviderChip (streaming services)
    - CastCard (photo, name, character)
    - SimilarMovieCard (poster, title, rating)

  states_required:
    MovieDetailScreen:
      success: "Full detail with all sections"
      loading: "Shimmer for backdrop, info, lists"
      error: "Failed to load movie"
      # No empty state (always has movie data)

  data_mapping:
    - API: "GET /movies/{id}"
      Fields:
        - title → Hero title
        - backdropPath → Backdrop image
        - posterPath → Poster thumbnail
        - rating → Rating badge
        - runtime → Duration text
        - genres → Genre chips
        - overview → Synopsis text
        - cast → Cast list
        - similar → Similar movies list
        - watchProviders → Provider chips

  interactions_count: 15
    - Back navigation
    - Menu options
    - Watch trailer (YouTube)
    - Add to watchlist
    - Mark as watched
    - Share movie
    - Tap provider (open app)
    - Expand synopsis
    - Tap cast member
    - See all cast
    - Tap similar movie
    - See all similar
    - Pull to refresh
    - Scroll content
    - Image zoom

  gaps_found: 0
  completeness: 100%
```

---

## Related Files

| File | Purpose |
|------|---------|
| `GENERATION_ORDER.md` | Overall pipeline |
| `DESIGN_LAYER_SCHEMA.md` | Data schemas |
| `features/mockups/MOCKUP.md` | Template to fill |
| `mockup-tools/design-tokens.json` | Color/typography values |

