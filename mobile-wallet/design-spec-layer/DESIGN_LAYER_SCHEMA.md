# template_meta
# template_version: "2.84.0"
# template_path: "templates/blueprints/workspace-project/design-spec-layer/DESIGN_LAYER_SCHEMA.md"
# last_modified: "2026-03-20"

# Design Layer Schema

> Defines the data model and extraction rules for intelligent auto-population between design files.

**Version**: 1.0.0
**Last Updated**: 2025-01-13

---

## Overview

This schema enables Claude to intelligently extract information from upstream files and populate downstream files automatically.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DATA FLOW SCHEMA                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  SPEC.md                                                                     │
│  ├── feature_name ──────────────┬─────────────────────────────────────────▶ │
│  ├── user_stories ──────────────┼──▶ API.md (endpoint generation)           │
│  ├── screens ───────────────────┼──▶ MOCKUP.md (wireframe sections)         │
│  ├── components ────────────────┼──▶ MOCKUP.md (component blocks)           │
│  └── requirements ──────────────┘                                            │
│                                                                              │
│  API.md                                                                      │
│  ├── endpoints ─────────────────────▶ MOCKUP.md (data in wireframes)        │
│  ├── response_dtos ─────────────────▶ MOCKUP.md (content fields)            │
│  └── error_codes ───────────────────▶ MOCKUP.md (error states)              │
│                                                                              │
│  MOCKUP.md                                                                   │
│  ├── wireframes ────────────────────▶ PROMPTS_FIGMA.md                      │
│  ├── components ────────────────────▶ PROMPTS_STITCH.md                     │
│  └── states ────────────────────────▶ Both PROMPTS_*.md                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## File Schemas

### SPEC.md Schema

```yaml
spec_schema:
  metadata:
    feature_name: string          # kebab-case (e.g., "movie-detail")
    feature_title: string         # Display name (e.g., "Movie Detail")
    purpose: string               # One-line description
    user_value: string            # Why users need this
    last_updated: date            # YYYY-MM-DD

  overview:
    summary: string               # 2-3 sentences
    target_users: list[string]    # User personas

  user_stories:
    - id: string                  # US-001
      story: string               # "As a user, I want to..."
      acceptance: list[string]    # Acceptance criteria
      priority: enum[P0, P1, P2]

  screens:
    - name: string                # "MovieDetailScreen"
      description: string         # What this screen shows
      parent: string              # Navigation parent
      components: list[string]    # Components used

  components:
    - name: string                # "MovieCard"
      type: enum[card, list, form, header, nav, button, etc.]
      description: string
      used_in: list[string]       # Screen names

  states:
    - name: enum[success, loading, empty, error]
      description: string
      trigger: string             # What causes this state
      ui_feedback: string         # What user sees

  requirements:
    functional:
      - id: string                # FR-001
        description: string
        related_user_story: string

    non_functional:
      - id: string                # NFR-001
        category: enum[performance, accessibility, security, offline]
        description: string
        metric: string            # Measurable target

  acceptance_criteria:
    - id: string                  # AC-001
      description: string
      testable: boolean
```

### API.md Schema

```yaml
api_schema:
  metadata:
    feature_name: string
    base_url: string
    auth_method: enum[Bearer, Basic, API-Key, None]
    last_updated: date

  endpoints:
    - name: string                # "GetMovieDetail"
      method: enum[GET, POST, PUT, PATCH, DELETE]
      url: string                 # "/api/v1/movies/{id}"
      description: string
      auth_required: boolean

      path_params:
        - name: string
          type: string
          description: string

      query_params:
        - name: string
          type: string
          required: boolean
          description: string

      request_body:
        content_type: string      # "application/json"
        dto_name: string          # "UpdateMovieRequest"
        fields:
          - name: string
            type: string
            required: boolean
            description: string

      responses:
        - status: integer         # 200, 201, 400, etc.
          description: string
          dto_name: string
          fields:
            - name: string
              type: string
              nullable: boolean
              description: string

      errors:
        - status: integer
          code: string            # "movie.not_found"
          message: string
          ui_action: string       # "Show error state"

  dtos:
    request:
      - name: string              # "UpdateMovieRequest"
        fields:
          - name: string
            type: string
            required: boolean
            validation: string    # Optional validation rule

    response:
      - name: string              # "MovieDetailResponse"
        fields:
          - name: string
            type: string
            nullable: boolean
            maps_to: string       # UI field mapping
```

### MOCKUP.md Schema

```yaml
mockup_schema:
  metadata:
    feature_name: string
    target_device: string         # "Mobile (393x852px)"
    design_system: string         # "Material Design 3"
    last_updated: date

  screens:
    - name: string                # "MovieDetailScreen"
      description: string

      states:
        - state: enum[success, loading, empty, error]
          wireframe: string       # ASCII art
          description: string

      components:
        - name: string            # "BackdropHeader"
          position: string        # "top"
          size: string            # "393x240dp"
          wireframe: string       # ASCII block
          content:
            - element: string     # "title"
              data_source: string # "MovieDetailResponse.title"

  navigation:
    - from: string                # "HomeScreen"
      to: string                  # "MovieDetailScreen"
      trigger: string             # "Tap movie card"
      params: list[string]        # ["movieId"]

  interactions:
    - element: string             # "WatchTrailerButton"
      action: string              # "tap"
      result: string              # "Open YouTube"
      api_call: string            # Optional endpoint
```

### PROMPTS_FIGMA.md Schema

```yaml
figma_prompts_schema:
  metadata:
    feature_name: string
    tool: "Figma AI First Draft"
    target: "Mobile (393x852px)"

  screens:
    - name: string
      state: enum[success, loading, empty, error]
      prompt: string              # Natural language description
      layout:
        - section: string         # "Top App Bar"
          description: string     # Natural language
          components: list[string]
      style:
        colors: map[string, string]
        typography: map[string, string]

  components:
    - name: string
      prompt: string              # Component description
      size: string
      content: string

  interactions:
    - element: string
      states: list[string]        # ["default", "hover", "pressed"]
```

### PROMPTS_STITCH.md Schema

```yaml
stitch_prompts_schema:
  metadata:
    feature_name: string
    tool: "Google Stitch AI"
    target: "Mobile portrait (393x852px)"

  design_system:
    colors:
      - name: string              # "Primary"
        value: string             # "#E50914"
        usage: string

    typography:
      - name: string              # "Title Large"
        size: string              # "22sp"
        weight: string            # "600"
        line_height: string

    spacing:
      - name: string              # "md"
        value: string             # "16dp"

    elevation:
      - level: integer
        shadow: string

  screens:
    - name: string
      state: enum[success, loading, empty, error]
      canvas: string              # "393x852px"

      elements:
        - name: string            # "TopAppBar"
          position: string        # "0, 0"
          size: string            # "393x64dp"
          background: string      # "#121212"

          children:
            - name: string        # "BackButton"
              position: string    # "16dp from left"
              size: string        # "40x40dp"
              specs: map[string, string]
```

---

## Extraction Rules

### Rule 1: User Stories → Endpoints

```yaml
extraction_rule:
  name: "user_story_to_endpoint"
  source: "SPEC.md.user_stories"
  target: "API.md.endpoints"

  patterns:
    # View/Read operations
    - match: "view|see|browse|list|search|get|fetch|load|read"
      output:
        method: GET
        url_pattern: "/api/v1/{resource}"

    # Create operations
    - match: "create|add|submit|send|post|upload"
      output:
        method: POST
        url_pattern: "/api/v1/{resource}"

    # Update operations
    - match: "update|edit|modify|change|save"
      output:
        method: PUT
        url_pattern: "/api/v1/{resource}/{id}"

    # Delete operations
    - match: "delete|remove|cancel|clear"
      output:
        method: DELETE
        url_pattern: "/api/v1/{resource}/{id}"

  examples:
    - input: "As a user, I can view movie details"
      output:
        method: GET
        url: "/api/v1/movies/{id}"
        name: "GetMovieDetail"
        response_dto: "MovieDetailResponse"

    - input: "As a user, I can add movies to my watchlist"
      output:
        method: POST
        url: "/api/v1/watchlist"
        name: "AddToWatchlist"
        request_dto: "AddWatchlistRequest"
        response_dto: "WatchlistResponse"
```

### Rule 2: Screens → Wireframe Sections

```yaml
extraction_rule:
  name: "screens_to_wireframes"
  source: "SPEC.md.screens"
  target: "MOCKUP.md.screens"

  template: |
    ## {screen_name} Screen

    ### Success State
    ```
    {wireframe}
    ```

    ### Loading State
    ```
    {shimmer_wireframe}
    ```

    ### Empty State
    ```
    {empty_wireframe}
    ```

    ### Error State
    ```
    {error_wireframe}
    ```

  component_mapping:
    header:
      wireframe: |
        ┌─────────────────────────────────────────┐
        │  ← {title}                          ⋮   │
        └─────────────────────────────────────────┘

    list:
      wireframe: |
        │  ┌─────────────────────────────────┐   │
        │  │ [Item 1]                        │   │
        │  └─────────────────────────────────┘   │
        │  ┌─────────────────────────────────┐   │
        │  │ [Item 2]                        │   │
        │  └─────────────────────────────────┘   │

    card:
      wireframe: |
        │  ┌─────────────────────────────────┐   │
        │  │ [Image]  Title                  │   │
        │  │          Subtitle               │   │
        │  │          [Action Button]        │   │
        │  └─────────────────────────────────┘   │

    empty:
      wireframe: |
        │                                         │
        │           [Illustration]                │
        │                                         │
        │           No items found                │
        │                                         │
        │         [Action Button]                 │
        │                                         │

    error:
      wireframe: |
        │                                         │
        │              ⚠️                         │
        │                                         │
        │       Something went wrong              │
        │                                         │
        │    [Retry]        [Go Back]             │
        │                                         │
```

### Rule 3: API Response → Wireframe Content

```yaml
extraction_rule:
  name: "api_to_wireframe_content"
  source: "API.md.endpoints.responses.fields"
  target: "MOCKUP.md.screens.components.content"

  mapping:
    - api_field: "title"
      ui_element: "Title text"
      position: "prominent"

    - api_field: "description"
      ui_element: "Body text"
      position: "below title"

    - api_field: "imageUrl"
      ui_element: "[Image]"
      position: "leading or top"

    - api_field: "rating"
      ui_element: "★ {value}"
      position: "metadata row"

    - api_field: "items[]"
      ui_element: "List/Grid of cards"
      position: "main content"

  example:
    input:
      endpoint: "GET /movies/{id}"
      response:
        title: string
        overview: string
        posterPath: string
        rating: number
        genres: list[string]

    output:
      wireframe: |
        ┌─────────────────────────────────────────┐
        │  [posterPath]                           │
        │  {title}                                │
        │  ★ {rating} | {genres}                  │
        │                                         │
        │  {overview}                             │
        └─────────────────────────────────────────┘
```

### Rule 4: Wireframe → Natural Language (Figma)

```yaml
extraction_rule:
  name: "wireframe_to_figma_prompt"
  source: "MOCKUP.md.screens.wireframe"
  target: "PROMPTS_FIGMA.md.screens.prompt"

  conversion:
    # ASCII patterns → Natural language
    patterns:
      "← {text}": "Back button with '{text}' title"
      "⋮": "overflow menu (three dots)"
      "[Image]": "image placeholder"
      "[Button]": "button component"
      "★": "star rating icon"
      "┌───┐": "card with rounded corners"
      "│ │": "vertical container"
      "├───┤": "divider line"

    # Layout detection
    layout:
      "top section": "header area, typically 64dp height"
      "scrollable area": "main content, vertically scrollable"
      "bottom section": "bottom navigation or action bar"

    # State descriptions
    states:
      loading: "Replace all content with shimmer effect placeholders"
      empty: "Centered illustration with message and action button"
      error: "Error icon, message, and retry button centered"

  example:
    input: |
      ┌─────────────────────────────────────────┐
      │  ← Movie Detail                      ⋮  │
      ├─────────────────────────────────────────┤
      │  [Backdrop Image]                       │
      │  ┌────┐                                 │
      │  │Post│  Inception                      │
      │  │ er │  2010 | 2h 28m                  │
      │  └────┘  ★ 8.8                          │
      └─────────────────────────────────────────┘

    output: |
      Create a mobile screen (393x852px) for a movie detail page.

      **Layout:**
      - **Top App Bar** (64dp height):
        - Back button (left)
        - Title: "Movie Detail" centered
        - Overflow menu (right)

      - **Backdrop** (240dp height):
        - Full-width movie backdrop image
        - Gradient overlay at bottom

      - **Movie Info Card** (overlapping backdrop):
        - Poster thumbnail (100x150dp) on left
        - Title: "Inception" (headline)
        - Meta: "2010 | 2h 28m"
        - Rating: star icon with "8.8"
```

### Rule 5: Wireframe → Exact Specs (Stitch)

```yaml
extraction_rule:
  name: "wireframe_to_stitch_specs"
  source: "MOCKUP.md.screens.wireframe"
  target: "PROMPTS_STITCH.md.screens.elements"

  measurement_mapping:
    # Standard component sizes
    top_app_bar:
      size: "393x64dp"
      padding: "16dp horizontal"
      back_button: "48x48dp touch target, 24dp icon"
      title: "22sp / 400 weight"

    bottom_nav:
      size: "393x80dp"
      item_count: "3-5 items"
      icon: "24x24dp"
      label: "12sp"

    card:
      width: "361dp (393 - 32dp padding)"
      padding: "16dp internal"
      corner_radius: "12dp"
      elevation: "2dp"

    list_item:
      height: "72dp"
      padding: "16dp horizontal"
      leading_icon: "40x40dp"
      divider: "1dp"

    button:
      filled:
        height: "48dp"
        corner_radius: "24dp (pill)"
        text: "14sp / 500 weight"
      outlined:
        height: "48dp"
        border: "1dp"
        corner_radius: "8dp"

  color_mapping:
    # From design-tokens.json or defaults
    primary: "#E50914"
    surface: "#1E1E1E"
    background: "#121212"
    text_primary: "#FFFFFF"
    text_secondary: "#B3B3B3"
```

---

## Auto-Population Examples

### Complete Flow Example

```yaml
example_flow:
  input:
    user_request: "Create a movie watchlist feature"

  step_1_spec:
    feature_name: "watchlist"
    user_stories:
      - "As a user, I can view my watchlist"
      - "As a user, I can add movies to watchlist"
      - "As a user, I can remove movies from watchlist"
    screens:
      - name: "WatchlistScreen"
        components: ["MovieCard", "EmptyState"]

  step_2_api:
    # Auto-generated from user stories
    endpoints:
      - method: GET
        url: "/api/v1/watchlist"
        response: "WatchlistResponse"
      - method: POST
        url: "/api/v1/watchlist"
        request: "AddWatchlistRequest"
      - method: DELETE
        url: "/api/v1/watchlist/{movieId}"

  step_3_mockup:
    # Auto-generated from screens + API
    screens:
      - name: "WatchlistScreen"
        success: |
          ┌─────────────────────────────────────────┐
          │  ← My Watchlist                     ⋮   │
          ├─────────────────────────────────────────┤
          │  ┌─────────────────────────────────┐   │
          │  │ [Poster]  Movie Title           │   │
          │  │           ★ 8.5 | Action        │   │
          │  │           [Remove]              │   │
          │  └─────────────────────────────────┘   │
          └─────────────────────────────────────────┘
        empty: "No movies in your watchlist"

  step_4_prompts:
    figma: |
      Create a mobile watchlist screen with:
      - Top app bar with back button and title
      - Vertical list of movie cards
      - Each card shows poster, title, rating, remove button

    stitch: |
      WatchlistScreen:
      - Canvas: 393x852px
      - Top App Bar: 393x64dp, #121212
      - Movie Card: 361x140dp, 12dp radius
        - Poster: 80x120dp
        - Title: 16sp / 500 weight
```

---

## Validation Rules

### Pre-Generation Validation

```yaml
validation:
  before_api:
    - check: "SPEC.md exists"
    - check: "SPEC.md has user_stories"
    - check: "SPEC.md has screens"

  before_mockup:
    - check: "SPEC.md exists"
    - check: "API.md exists (for data-driven features)"
    - check: "SPEC.md has components"

  before_prompts:
    - check: "MOCKUP.md exists"
    - check: "MOCKUP.md has wireframes"
    - check: "MOCKUP.md has all states"
```

### Post-Generation Validation

```yaml
validation:
  api_complete:
    - has_endpoints: true
    - has_dtos: true
    - has_error_handling: true

  mockup_complete:
    - has_all_screens: "matches SPEC.screens"
    - has_all_states: [success, loading, empty, error]
    - has_navigation: true

  prompts_complete:
    - has_all_screens: "matches MOCKUP.screens"
    - has_style_guide: true
    - has_component_details: true
```

---

## Related Files

| File | Purpose |
|------|---------|
| `GENERATION_ORDER.md` | Pipeline execution order |
| `design-tokens.json` | Design system values |
| `/design` command | Executes generation |
| `/gap-analysis` | Validates completeness |

