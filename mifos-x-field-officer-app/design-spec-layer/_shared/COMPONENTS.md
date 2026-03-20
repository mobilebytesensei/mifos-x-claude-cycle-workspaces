# template_meta
# template_version: "2.84.0"
# template_path: "templates/blueprints/workspace-project/design-spec-layer/_shared/COMPONENTS.md"
# last_modified: "2026-03-20"

# Design System - mifos-x-field-officer-app

> **Purpose**: Define reusable UI components and design tokens for consistent implementation.
> **Last Updated**: 2026-03-19
> **Status**: Draft

---

## 1. Color System

### Primary Palette

| Token | Light | Dark | Usage |
|-------|-------|------|-------|
| `primary` | {{PRIMARY_LIGHT}} | {{PRIMARY_DARK}} | Primary actions, buttons |
| `primaryContainer` | {{PRIMARY_CONTAINER_LIGHT}} | {{PRIMARY_CONTAINER_DARK}} | Primary backgrounds |
| `onPrimary` | {{ON_PRIMARY_LIGHT}} | {{ON_PRIMARY_DARK}} | Text on primary |
| `secondary` | {{SECONDARY_LIGHT}} | {{SECONDARY_DARK}} | Secondary actions |
| `tertiary` | {{TERTIARY_LIGHT}} | {{TERTIARY_DARK}} | Accents |

### Background & Surface

| Token | Light | Dark | Usage |
|-------|-------|------|-------|
| `background` | #FFFFFF | #121212 | App background |
| `surface` | #FFFFFF | #1E1E1E | Card backgrounds |
| `surfaceVariant` | #F5F5F5 | #2D2D2D | Elevated surfaces |
| `surfaceContainer` | #FAFAFA | #252525 | Container backgrounds |
| `surfaceContainerHigh` | #F0F0F0 | #333333 | Higher elevation |

### Semantic Colors

| Token | Light | Dark | Usage |
|-------|-------|------|-------|
| `error` | #B3261E | #F2B8B5 | Error states |
| `success` | #1B5E20 | #81C784 | Success states |
| `warning` | #F57C00 | #FFB74D | Warning states |
| `info` | #0288D1 | #4FC3F7 | Information |

### Gradients

| Name | Definition | Usage |
|------|------------|-------|
| `primaryGradient` | `{{GRADIENT_START}} → {{GRADIENT_END}}` | Hero sections, CTAs |
| `cardOverlay` | `transparent → rgba(0,0,0,0.7)` | Image overlays |

---

## 2. Typography Scale

### Font Family

```
Primary: {{FONT_FAMILY}} (or system default)
Fallback: sans-serif
```

### Type Scale

| Style | Weight | Size | Line Height | Letter Spacing | Usage |
|-------|:------:|:----:|:-----------:|:--------------:|-------|
| Display Large | Bold | 57sp | 64sp | -0.25sp | Hero numbers |
| Display Medium | SemiBold | 45sp | 52sp | 0sp | Large headers |
| Headline Large | SemiBold | 32sp | 40sp | 0sp | Screen titles |
| Headline Medium | Medium | 28sp | 36sp | 0sp | Section titles |
| Title Large | SemiBold | 22sp | 28sp | 0sp | Card titles |
| Title Medium | Medium | 16sp | 24sp | 0.15sp | Subtitles |
| Body Large | Regular | 16sp | 24sp | 0.5sp | Primary text |
| Body Medium | Regular | 14sp | 20sp | 0.25sp | Secondary text |
| Label Large | Medium | 14sp | 20sp | 0.1sp | Buttons |
| Label Medium | Medium | 12sp | 16sp | 0.5sp | Tags, chips |
| Label Small | Medium | 11sp | 16sp | 0.5sp | Captions |

---

## 3. Spacing System

### Base Unit: 4dp

| Token | Value | Usage |
|-------|:-----:|-------|
| `spacing.xxs` | 2dp | Tight inline spacing |
| `spacing.xs` | 4dp | Icon-text gaps |
| `spacing.sm` | 8dp | Related element gaps |
| `spacing.md` | 16dp | Standard padding/margin |
| `spacing.lg` | 24dp | Section spacing |
| `spacing.xl` | 32dp | Large section gaps |
| `spacing.xxl` | 48dp | Major section breaks |

### Content Margins

| Context | Value |
|---------|:-----:|
| Screen horizontal | 16dp |
| Card internal | 16dp |
| List item vertical | 12dp |
| Section vertical | 24dp |

---

## 4. Border Radius

| Token | Value | Usage |
|-------|:-----:|-------|
| `radius.none` | 0dp | Sharp corners |
| `radius.xs` | 4dp | Small chips |
| `radius.sm` | 8dp | Buttons, small cards |
| `radius.md` | 12dp | Cards, dialogs |
| `radius.lg` | 16dp | Large cards |
| `radius.xl` | 24dp | Pills, FABs |
| `radius.full` | 9999dp | Circles, avatars |

---

## 5. Elevation & Shadows

| Level | Elevation | Shadow | Usage |
|:-----:|:---------:|--------|-------|
| 0 | 0dp | None | Flat surfaces |
| 1 | 1dp | Subtle | Cards at rest |
| 2 | 3dp | Light | Raised cards |
| 3 | 6dp | Medium | Dialogs |
| 4 | 8dp | Strong | Bottom sheets |
| 5 | 12dp | Maximum | FABs |

---

## 6. Component Library

### 6.1 Buttons

#### Primary Button

```
┌─────────────────────────────────────┐
│           Button Label              │
└─────────────────────────────────────┘
```

| Property | Value |
|----------|-------|
| Height | 48dp |
| Min Width | 88dp |
| Horizontal Padding | 24dp |
| Corner Radius | 24dp (pill) |
| Background | Primary color |
| Text | Label Large, onPrimary |

**States**:
- Default: Primary background
- Pressed: Primary + 12% black overlay
- Disabled: 38% opacity
- Loading: CircularProgress indicator

#### Secondary Button (Outlined)

| Property | Value |
|----------|-------|
| Height | 48dp |
| Border | 1dp, primary color |
| Background | Transparent |
| Text | Label Large, primary |

#### Text Button

| Property | Value |
|----------|-------|
| Height | 40dp |
| Background | Transparent |
| Text | Label Large, primary |

---

### 6.2 Cards

#### Standard Card

```
┌─────────────────────────────────────────────────────┐
│  ┌─────────────────────────────────────────────┐    │
│  │                                             │    │
│  │              Image (optional)               │    │
│  │                                             │    │
│  └─────────────────────────────────────────────┘    │
│                                                     │
│  Title Text                                         │
│  Subtitle or description text goes here             │
│                                                     │
│  [Action 1]              [Action 2]                 │
│                                                     │
└─────────────────────────────────────────────────────┘
```

| Property | Value |
|----------|-------|
| Corner Radius | 12dp |
| Elevation | Level 1 (1dp) |
| Padding | 16dp |
| Background | surfaceContainer |

---

### 6.3 List Items

#### Single Line

```
┌─────────────────────────────────────────────────────┐
│  [Icon]  Primary Text                          [>]  │
└─────────────────────────────────────────────────────┘
```

| Property | Value |
|----------|-------|
| Height | 56dp |
| Horizontal Padding | 16dp |
| Icon Size | 24dp |
| Text | Body Large |

#### Two Line

```
┌─────────────────────────────────────────────────────┐
│  [Icon]  Primary Text                               │
│          Secondary Text                        [>]  │
└─────────────────────────────────────────────────────┘
```

| Property | Value |
|----------|-------|
| Height | 72dp |
| Primary Text | Body Large |
| Secondary Text | Body Medium, onSurfaceVariant |

#### Three Line

```
┌─────────────────────────────────────────────────────┐
│  [Avatar]  Primary Text                             │
│            Secondary Text                           │
│            Tertiary Text                       [>]  │
└─────────────────────────────────────────────────────┘
```

| Property | Value |
|----------|-------|
| Height | 88dp |
| Avatar Size | 40dp |

---

### 6.4 Input Fields

#### Text Field

```
┌─────────────────────────────────────────────────────┐
│  Label                                              │
│  ┌─────────────────────────────────────────────┐    │
│  │ [Icon]  Placeholder text              [X]   │    │
│  └─────────────────────────────────────────────┘    │
│  Helper text or error message                       │
└─────────────────────────────────────────────────────┘
```

| Property | Value |
|----------|-------|
| Height | 56dp |
| Corner Radius | 8dp (top only for filled) |
| Border | 1dp for outlined variant |
| Label | Label Medium |
| Input | Body Large |
| Helper | Label Small |

**States**:
- Default: Outline color
- Focused: Primary, 2dp border
- Error: Error color border + icon
- Disabled: 38% opacity

---

### 6.5 Chips

#### Filter Chip

```
┌───────────────────────┐
│  [Icon] Label    [X]  │
└───────────────────────┘
```

| Property | Value |
|----------|-------|
| Height | 32dp |
| Corner Radius | 8dp |
| Horizontal Padding | 12dp |
| Text | Label Large |

**States**:
- Unselected: Outline, surfaceVariant background
- Selected: Primary tint background

#### Input Chip

```
┌───────────────────────┐
│  [Avatar] Name   [X]  │
└───────────────────────┘
```

| Property | Value |
|----------|-------|
| Height | 32dp |
| Avatar Size | 24dp |
| Corner Radius | 16dp (pill) |

---

### 6.6 Bottom Navigation

```
┌─────────────────────────────────────────────────────┐
│  [Icon]    [Icon]    [Icon]    [Icon]    [Icon]     │
│  Label     Label     Label     Label     Label      │
└─────────────────────────────────────────────────────┘
```

| Property | Value |
|----------|-------|
| Height | 80dp |
| Icon Size | 24dp |
| Label | Label Medium |
| Active | Primary color |
| Inactive | onSurfaceVariant |

---

### 6.7 Top App Bar

#### Standard

```
┌─────────────────────────────────────────────────────┐
│  [<]  Title                              [🔍] [⋮]   │
└─────────────────────────────────────────────────────┘
```

| Property | Value |
|----------|-------|
| Height | 64dp |
| Title | Title Large |
| Icon Size | 24dp |
| Horizontal Padding | 16dp |

#### Large (Collapsing)

```
┌─────────────────────────────────────────────────────┐
│  [<]                                     [🔍] [⋮]   │
│                                                     │
│  Large Title                                        │
└─────────────────────────────────────────────────────┘
```

| Property | Value |
|----------|-------|
| Expanded Height | 152dp |
| Collapsed Height | 64dp |
| Title | Headline Medium |

---

### 6.8 Dialogs

#### Alert Dialog

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│  [Icon]                                             │
│                                                     │
│  Dialog Title                                       │
│                                                     │
│  Dialog body text explaining the action or          │
│  providing information to the user.                 │
│                                                     │
│                        [Cancel]  [Confirm]          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

| Property | Value |
|----------|-------|
| Min Width | 280dp |
| Max Width | 560dp |
| Corner Radius | 28dp |
| Padding | 24dp |
| Title | Headline Small |
| Body | Body Medium |

---

### 6.9 Loading States

#### Skeleton Shimmer Base

```
┌─────────────────────────────────────────────────────┐
│  ████████████████████████████                       │
│  ████████████████                                   │
│  ████████████████████████████████████               │
└─────────────────────────────────────────────────────┘
```

| Property | Value |
|----------|-------|
| Background | surfaceVariant |
| Shimmer | Linear gradient animation |
| Corner Radius | Match content radius |
| Animation | 1.5s duration, infinite |

#### Per-Component Shimmer Specifications

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PER-COMPONENT SHIMMER PATTERNS                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  CARD SHIMMER                                                                │
│  ┌─────────────────────────────────────────────────────────┐                │
│  │  ┌───────────────────────────────────────────────────┐  │                │
│  │  │░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│  │  Image: 200dp  │
│  │  │░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│  │  radius: 12dp  │
│  │  └───────────────────────────────────────────────────┘  │                │
│  │  ████████████████████████████  ← Title: 70% width       │                │
│  │  ████████████████  ← Subtitle: 50% width                │                │
│  │  ████████████████████████  ← Body: 60% width            │                │
│  └─────────────────────────────────────────────────────────┘                │
│                                                                              │
│  LIST ITEM SHIMMER                                                           │
│  ┌─────────────────────────────────────────────────────────┐                │
│  │  [░░░]  ████████████████████████████████         [░░░]  │  Avatar: 40dp  │
│  │         ██████████████████████                          │  circle        │
│  └─────────────────────────────────────────────────────────┘                │
│                                                                              │
│  TEXT BLOCK SHIMMER                                                          │
│  ┌─────────────────────────────────────────────────────────┐                │
│  │  ████████████████████████████████████████████████████   │  Line 1: 100% │
│  │  ████████████████████████████████████████████████       │  Line 2: 95%  │
│  │  ██████████████████████████████████████████████████████ │  Line 3: 100% │
│  │  ████████████████████████████████████████               │  Line 4: 80%  │
│  └─────────────────────────────────────────────────────────┘                │
│                                                                              │
│  AVATAR SHIMMER                                                              │
│  ┌───────────────────────┐                                                  │
│  │  ┌─────┐               │                                                  │
│  │  │░░░░░│  Small: 32dp circle                                             │
│  │  └─────┘               │                                                  │
│  │  ┌───────┐             │                                                  │
│  │  │░░░░░░░│  Medium: 48dp circle                                          │
│  │  └───────┘             │                                                  │
│  │  ┌─────────┐           │                                                  │
│  │  │░░░░░░░░░│  Large: 64dp circle                                         │
│  │  └─────────┘           │                                                  │
│  └───────────────────────┘                                                  │
│                                                                              │
│  IMAGE SHIMMER                                                               │
│  ┌─────────────────────────────────────────────────────────┐                │
│  │  ┌─────────────────────────────────────────────────┐    │                │
│  │  │░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│    │                │
│  │  │░░░░░░░░░░░░░░░[🖼️ Icon]░░░░░░░░░░░░░░░░░░░░░░░░│    │  Center icon  │
│  │  │░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│    │  24dp, 50%    │
│  │  └─────────────────────────────────────────────────┘    │  opacity      │
│  └─────────────────────────────────────────────────────────┘                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### Shimmer Specifications Table

| Component | Shape | Width | Height | Radius | Lines |
|-----------|-------|:-----:|:------:|:------:|:-----:|
| Card Image | Rectangle | 100% | 200dp | 12dp | - |
| Card Title | Rectangle | 70% | 20dp | 4dp | 1 |
| Card Subtitle | Rectangle | 50% | 16dp | 4dp | 1 |
| List Avatar | Circle | 40dp | 40dp | 20dp | - |
| List Primary | Rectangle | 60% | 16dp | 4dp | 1 |
| List Secondary | Rectangle | 40% | 14dp | 4dp | 1 |
| Text Paragraph | Rectangle | 80-100% | 14dp | 4dp | 4 |
| Button | Rectangle | 100% | 48dp | 24dp | - |
| Chip | Rectangle | 80dp | 32dp | 16dp | - |

#### Shimmer Animation Timing

| Property | Value |
|----------|-------|
| Gradient Width | 200% of component |
| Animation Duration | 1.5s |
| Delay Before Showing | 200ms (perceived performance) |
| Gradient Colors | surfaceVariant → surfaceVariant + 20% white → surfaceVariant |
| Direction | Left to Right |

#### Circular Progress

| Property | Value |
|----------|-------|
| Size (default) | 48dp |
| Size (small) | 24dp |
| Stroke Width | 4dp |
| Color | Primary |

---

### 6.10 Empty States

#### Generic Empty State

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│                    [Illustration]                   │
│                                                     │
│              No items found                         │
│                                                     │
│     There are no items to display yet.              │
│     Add your first item to get started.             │
│                                                     │
│              [+ Add Item]                           │
│                                                     │
└─────────────────────────────────────────────────────┘
```

| Property | Value |
|----------|-------|
| Illustration Size | 120dp × 120dp |
| Title | Title Large, centered |
| Description | Body Medium, centered, onSurfaceVariant |
| Action | Primary button |

#### Contextual Empty State Variants

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  CONTEXTUAL EMPTY STATES                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. FIRST USE (Onboarding)                                                   │
│  ┌─────────────────────────────────────────────────────────────┐            │
│  │                                                             │            │
│  │                 [Welcome Illustration]                      │            │
│  │                   (Friendly, inviting)                      │            │
│  │                                                             │            │
│  │                Get Started with {Feature}                   │            │
│  │                                                             │            │
│  │     {Feature} helps you {benefit}. Create your first        │            │
│  │     {item} to see it in action!                             │            │
│  │                                                             │            │
│  │              [+ Create First {Item}]                        │            │
│  │                                                             │            │
│  │              or [See How It Works]  ← optional tutorial     │            │
│  │                                                             │            │
│  └─────────────────────────────────────────────────────────────┘            │
│  Tone: Encouraging, welcoming | Icon: Sparkles, rocket                      │
│                                                                              │
│  2. NO RESULTS (Search/Filter)                                               │
│  ┌─────────────────────────────────────────────────────────────┐            │
│  │                                                             │            │
│  │                   [Search Illustration]                     │            │
│  │                   (Magnifying glass)                        │            │
│  │                                                             │            │
│  │            No results for "{search_query}"                  │            │
│  │                                                             │            │
│  │     Try different keywords or remove some filters.          │            │
│  │                                                             │            │
│  │        [Clear Filters]    [Browse All]                      │            │
│  │                                                             │            │
│  └─────────────────────────────────────────────────────────────┘            │
│  Tone: Helpful, solution-oriented | Icon: Search, filter                    │
│                                                                              │
│  3. ERROR STATE (Failed Load)                                                │
│  ┌─────────────────────────────────────────────────────────────┐            │
│  │                                                             │            │
│  │                    [Error Illustration]                     │            │
│  │                   (Cloud with X, 404)                       │            │
│  │                                                             │            │
│  │              Couldn't Load {Items}                          │            │
│  │                                                             │            │
│  │     Something went wrong. Check your connection             │            │
│  │     and try again.                                          │            │
│  │                                                             │            │
│  │              [Retry]    [Go Back]                           │            │
│  │                                                             │            │
│  └─────────────────────────────────────────────────────────────┘            │
│  Tone: Empathetic, actionable | Icon: Warning, cloud_off                    │
│                                                                              │
│  4. OFFLINE STATE (No Connection)                                            │
│  ┌─────────────────────────────────────────────────────────────┐            │
│  │                                                             │            │
│  │                  [Offline Illustration]                     │            │
│  │                  (Disconnected signal)                      │            │
│  │                                                             │            │
│  │                   You're Offline                            │            │
│  │                                                             │            │
│  │     Connect to the internet to see your {items}.            │            │
│  │                                                             │            │
│  │              [Open Settings]                                │            │
│  │                                                             │            │
│  │     ─────────────────────────────────────                  │            │
│  │     While offline, you can still:                           │            │
│  │     • View cached {items}                                   │            │
│  │     • Create drafts (sync later)                            │            │
│  │                                                             │            │
│  └─────────────────────────────────────────────────────────────┘            │
│  Tone: Informative, reassuring | Icon: wifi_off, cloud_off                  │
│                                                                              │
│  5. PERMISSION REQUIRED                                                      │
│  ┌─────────────────────────────────────────────────────────────┐            │
│  │                                                             │            │
│  │                 [Permission Illustration]                   │            │
│  │                 (Lock, camera, location)                    │            │
│  │                                                             │            │
│  │           {Permission} Access Needed                        │            │
│  │                                                             │            │
│  │     To use this feature, we need access to your             │            │
│  │     {permission}. Your data stays private.                  │            │
│  │                                                             │            │
│  │              [Enable in Settings]                           │            │
│  │                                                             │            │
│  │              [Not Now]                                      │            │
│  │                                                             │            │
│  └─────────────────────────────────────────────────────────────┘            │
│  Tone: Transparent, trustworthy | Icon: lock, shield                        │
│                                                                              │
│  6. COMPLETED / ALL DONE                                                     │
│  ┌─────────────────────────────────────────────────────────────┐            │
│  │                                                             │            │
│  │                  [Success Illustration]                     │            │
│  │                  (Checkmark, celebration)                   │            │
│  │                                                             │            │
│  │                   All Caught Up!                            │            │
│  │                                                             │            │
│  │     You've completed all your {items}. Nice work!           │            │
│  │                                                             │            │
│  │              [Explore More]                                 │            │
│  │                                                             │            │
│  └─────────────────────────────────────────────────────────────┘            │
│  Tone: Celebratory, rewarding | Icon: check_circle, party                   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### Empty State Specifications by Context

| Context | Illustration | Tone | Primary CTA | Secondary CTA |
|---------|--------------|------|-------------|---------------|
| First Use | Welcoming | Encouraging | Create First | Tutorial |
| No Results | Search | Helpful | Clear Filters | Browse All |
| Error | Warning | Empathetic | Retry | Go Back |
| Offline | Disconnected | Reassuring | Settings | View Cached |
| Permission | Lock/Shield | Transparent | Enable | Not Now |
| Completed | Celebration | Rewarding | Explore More | - |

#### Empty State Copy Guidelines

| Element | Rule | Example |
|---------|------|---------|
| Title | Short, specific | "No Transactions Yet" not "Empty" |
| Description | Explain why + what to do | "Add your first account to see transactions here" |
| CTA Label | Action verb + object | "Add Account" not "OK" or "Continue" |
| Tone | Match context | First use = excited, Error = empathetic |

---

### 6.11 Error States

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│                    [Error Icon]                     │
│                                                     │
│              Something went wrong                   │
│                                                     │
│     We couldn't load the content. Please            │
│     check your connection and try again.            │
│                                                     │
│              [Retry]                                │
│                                                     │
└─────────────────────────────────────────────────────┘
```

| Property | Value |
|----------|-------|
| Icon | 48dp, error color |
| Title | Title Large |
| Description | Body Medium |
| Action | Primary or outlined button |

---

## 7. Progressive Disclosure Patterns

> **Principle**: Reveal complexity gradually to reduce cognitive load and guide users through information hierarchy.

### 7.1 Expandable Accordion

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  COLLAPSED STATE                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  [Icon]  Section Title                                        [▼]   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  EXPANDED STATE                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  [Icon]  Section Title                                        [▲]   │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │                                                                     │    │
│  │  Detailed content that was previously hidden is now visible.        │    │
│  │  This can include:                                                  │    │
│  │  • Sub-items                                                        │    │
│  │  • Additional fields                                                │    │
│  │  • Extended information                                             │    │
│  │                                                                     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

| Property | Value |
|----------|-------|
| Header Height | 56dp |
| Chevron Size | 24dp |
| Animation Duration | 200ms |
| Easing | Standard (ease-in-out) |
| Content Padding | 16dp |

**Accordion Behavior**:
- Single expand (exclusive): Only one section open at a time
- Multi expand: Multiple sections can be open simultaneously
- Default: First section expanded, or all collapsed

### 7.2 Show More / Read More

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  TRUNCATED STATE                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                                                                     │    │
│  │  This is a preview of the content. The text is truncated after     │    │
│  │  a certain number of lines to keep the interface clean...          │    │
│  │                                                                     │    │
│  │  [Show more]                                                        │    │
│  │                                                                     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  EXPANDED STATE                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                                                                     │    │
│  │  This is a preview of the content. The text is truncated after     │    │
│  │  a certain number of lines to keep the interface clean. Now        │    │
│  │  that it's expanded, you can see the full content including        │    │
│  │  all the details that were previously hidden from view.            │    │
│  │                                                                     │    │
│  │  [Show less]                                                        │    │
│  │                                                                     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

| Property | Value |
|----------|-------|
| Max Lines (collapsed) | 3 |
| Fade Gradient | 24dp (optional) |
| Link Text | "Show more" / "Show less" |
| Link Color | Primary |
| Animation | Height + fade (250ms) |

### 7.3 Stepwise Reveal (Wizard)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEPWISE FORM DISCLOSURE                                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Progress:  ●────────○────────○────────○                                    │
│            Step 1   Step 2   Step 3   Step 4                                │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                                                                     │    │
│  │  Step 1: Basic Information                                          │    │
│  │                                                                     │    │
│  │  ┌───────────────────────────────────────────────────────────┐     │    │
│  │  │  Name                                                      │     │    │
│  │  └───────────────────────────────────────────────────────────┘     │    │
│  │                                                                     │    │
│  │  ┌───────────────────────────────────────────────────────────┐     │    │
│  │  │  Email                                                     │     │    │
│  │  └───────────────────────────────────────────────────────────┘     │    │
│  │                                                                     │    │
│  │                                              [Continue →]           │    │
│  │                                                                     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  Steps 2-4 are hidden until previous step is completed                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

| Property | Value |
|----------|-------|
| Step Indicator | 8dp circle (active: primary, inactive: outline) |
| Step Connector | 2dp line (complete: primary, incomplete: outline) |
| Step Transition | Slide left (300ms) |
| Validation | Per-step, before allowing proceed |

### 7.4 Contextual Actions (Long Press / Hover)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  CONTEXTUAL ACTIONS REVEAL                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  DEFAULT STATE (Primary actions only)                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  [Image]  Item Title                                          [♡]   │    │
│  │           Subtitle                                                  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  LONG PRESS / HOVER (Secondary actions revealed)                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  [Image]  Item Title                                                │    │
│  │           Subtitle                                                  │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │  [Share]    [Edit]    [Delete]    [More ⋮]                         │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  CONTEXT MENU (overflow)                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  [Image]  Item Title                      ┌───────────────────┐     │    │
│  │           Subtitle                        │ Duplicate         │     │    │
│  │                                           │ Move to folder    │     │    │
│  │                                           │ Add to favorites  │     │    │
│  │                                           │ Report            │     │    │
│  │                                           └───────────────────┘     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

| Trigger | Platform | Duration |
|---------|----------|:--------:|
| Long Press | Mobile | 500ms hold |
| Hover | Desktop | 0ms (immediate) |
| Right Click | Desktop | Immediate |
| Force Touch | iOS | Pressure threshold |

### 7.5 Information Hierarchy (Scanning Pattern)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  F-PATTERN SCANNING HIERARCHY                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  LEVEL 1: SCAN LINE (what user sees first - bold, large)                    │
│  ══════════════════════════════════════════════════════                     │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  $1,234.56                              Primary Value (Display)     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  LEVEL 2: SUPPORTING (what user sees second - medium)                       │
│  ─────────────────────────────────────────────────────                      │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Available Balance                       Label (Title Medium)       │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  LEVEL 3: DETAIL (what user reads if interested - small)                    │
│  · · · · · · · · · · · · · · · · · · · · · · · · · · · · ·                  │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Updated 2 minutes ago                   Meta (Body Small)          │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  LEVEL 4: ON-DEMAND (only if user taps/expands)                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Account: ****4532 | Routing: 123456789  Hidden until tap           │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 7.6 Collapsible Sections (Settings Pattern)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  SETTINGS PROGRESSIVE DISCLOSURE                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Notifications                                              [●]     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│       │                                                                      │
│       │  (When enabled, sub-options appear)                                 │
│       │                                                                      │
│       ├──┌───────────────────────────────────────────────────────────┐      │
│       │  │  Push Notifications                                 [●]   │      │
│       │  └───────────────────────────────────────────────────────────┘      │
│       │                                                                      │
│       ├──┌───────────────────────────────────────────────────────────┐      │
│       │  │  Email Notifications                                [○]   │      │
│       │  └───────────────────────────────────────────────────────────┘      │
│       │                                                                      │
│       └──┌───────────────────────────────────────────────────────────┐      │
│          │  Notification Sound                             [Default ▼]│      │
│          └───────────────────────────────────────────────────────────┘      │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Privacy                                                    [▶]     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│  (Collapsed - tap to expand)                                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Animation for Sub-option Reveal**:
- Duration: 200ms
- Easing: Decelerate
- Effect: Fade + slide down from parent toggle

### Progressive Disclosure Checklist

- [ ] Primary actions always visible
- [ ] Secondary actions accessible within 1 tap/click
- [ ] Tertiary actions in overflow menu
- [ ] Information hierarchy follows scanning patterns
- [ ] Expand/collapse animations are smooth
- [ ] State persists across sessions (where appropriate)
- [ ] Accessibility: Expanded state announced to screen readers

---

## 8. Icons

### Icon Sizes

| Context | Size |
|---------|:----:|
| Navigation | 24dp |
| Action buttons | 24dp |
| List leading | 24dp |
| FAB | 24dp |
| Inline text | 18dp |
| Small indicators | 16dp |

### Icon Colors

| Context | Color |
|---------|-------|
| Primary actions | Primary |
| Secondary actions | onSurfaceVariant |
| Disabled | 38% onSurface |
| Error | Error |

---

## 8. Motion & Animation

### Duration

| Type | Duration | Usage |
|------|:--------:|-------|
| Instant | 0ms | Immediate feedback |
| Fast | 100ms | Micro-interactions |
| Normal | 200ms | Standard transitions |
| Slow | 300ms | Complex animations |
| Emphasis | 400ms | Important transitions |

### Easing

| Type | Curve | Usage |
|------|-------|-------|
| Standard | ease-in-out | Default |
| Decelerate | ease-out | Entering elements |
| Accelerate | ease-in | Exiting elements |
| Spring | spring(0.5, 20, 1) | Playful interactions |

### Common Animations

| Animation | Properties |
|-----------|------------|
| Fade In | Opacity 0→1, 200ms |
| Scale Up | Scale 0.95→1, 150ms |
| Slide Up | TranslateY 100%→0, 300ms |
| Press | Scale 1→0.95→1, 100ms |

---

## 9. Accessibility

### Touch Targets

| Element | Minimum Size |
|---------|:------------:|
| Buttons | 48dp × 48dp |
| List items | 48dp height |
| Icons (tappable) | 48dp × 48dp |

### Color Contrast

| Text Type | Minimum Ratio |
|-----------|:-------------:|
| Normal text | 4.5:1 |
| Large text | 3:1 |
| UI components | 3:1 |

### Screen Reader

- All interactive elements have content descriptions
- Images have alt text
- Form fields have labels
- Error messages are announced

### 9.1 Redundant Coding (Multi-Modal Communication)

> **Principle**: Never rely on a single visual cue. Combine color + icon + text for maximum accessibility.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  REDUNDANT CODING PATTERNS                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PATTERN 1: COLOR + ICON                                                     │
│  ─────────────────────────────────────────────────────────────────────      │
│                                                                              │
│  BAD (Color only):                                                           │
│  ┌───────────────────────────────────────────┐                              │
│  │  Status: ● Active   ● Pending   ● Failed  │  Users with color           │
│  └───────────────────────────────────────────┘  blindness can't tell       │
│                                                                              │
│  GOOD (Color + Icon):                                                        │
│  ┌───────────────────────────────────────────┐                              │
│  │  Status: ✓ Active   ⏳ Pending  ✗ Failed  │  Icon conveys meaning       │
│  └───────────────────────────────────────────┘  without color               │
│                                                                              │
│  PATTERN 2: ICON + TEXT                                                      │
│  ─────────────────────────────────────────────────────────────────────      │
│                                                                              │
│  BAD (Icon only):                                                            │
│  ┌───────────────────────────────────────────┐                              │
│  │  [⬇️]  [📤]  [🗑️]  [⚙️]                    │  Icons can be ambiguous    │
│  └───────────────────────────────────────────┘                              │
│                                                                              │
│  GOOD (Icon + Text):                                                         │
│  ┌───────────────────────────────────────────┐                              │
│  │  [⬇️ Download] [📤 Share] [🗑️ Delete] [⚙️]│  Text clarifies intent     │
│  └───────────────────────────────────────────┘                              │
│                                                                              │
│  PATTERN 3: COLOR + ICON + TEXT (Maximum Clarity)                           │
│  ─────────────────────────────────────────────────────────────────────      │
│                                                                              │
│  ERROR STATE (3 cues):                                                       │
│  ┌───────────────────────────────────────────────────────────────────┐      │
│  │  Email                                                    [✗]     │      │
│  │  ┌─────────────────────────────────────────────────────────┐      │      │
│  │  │  invalid-email                                          │      │      │
│  │  └─────────────────────────────────────────────────────────┘      │      │
│  │  ⚠️ Please enter a valid email address     ← Red text + icon     │      │
│  └───────────────────────────────────────────────────────────────────┘      │
│       ↑ Red border                                                           │
│                                                                              │
│  SUCCESS STATE (3 cues):                                                     │
│  ┌───────────────────────────────────────────────────────────────────┐      │
│  │  Email                                                    [✓]     │      │
│  │  ┌─────────────────────────────────────────────────────────┐      │      │
│  │  │  user@example.com                                       │      │      │
│  │  └─────────────────────────────────────────────────────────┘      │      │
│  │  ✓ Email verified                          ← Green text + icon   │      │
│  └───────────────────────────────────────────────────────────────────┘      │
│       ↑ Green border                                                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### Redundant Coding Requirements

| State | Color | Icon | Text | Required |
|-------|:-----:|:----:|:----:|:--------:|
| Error | Error red | error/warning | Error message | All 3 |
| Success | Success green | check_circle | Success message | All 3 |
| Warning | Warning orange | warning | Warning text | At least 2 |
| Info | Info blue | info | Info text | At least 2 |
| Disabled | Gray (38% opacity) | - | "Unavailable" or similar | At least 2 |

#### Application Examples

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  REAL-WORLD REDUNDANT CODING                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  TRANSACTION STATUS:                                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  ✓ Completed   $50.00   Jan 15   Green badge + checkmark            │    │
│  │  ⏳ Pending     $30.00   Jan 14   Yellow badge + clock               │    │
│  │  ✗ Failed      $20.00   Jan 13   Red badge + X + "Failed" text      │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  BUTTON STATES:                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                                                                     │    │
│  │  [✓ Submit]         Primary, enabled                               │    │
│  │  [⏳ Submitting...]  Loading state with text                        │    │
│  │  [Submit]           Grayed out + cursor: not-allowed               │    │
│  │                                                                     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  FORM FIELD STATES:                                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Password Strength:                                                 │    │
│  │  ─────────────────────────────────────────────────────────────     │    │
│  │  [████░░░░░░] Weak       Red bar + "Weak" text                     │    │
│  │  [████████░░] Good       Yellow bar + "Good" text                  │    │
│  │  [██████████] Strong     Green bar + "Strong" text + ✓             │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  NOTIFICATIONS:                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  ⚠️ Warning: Your session expires in 5 minutes                     │    │
│  │     Yellow background + warning icon + clear text                   │    │
│  │                                                                     │    │
│  │  ✓ Success: Payment completed successfully                          │    │
│  │     Green background + checkmark + confirmation text                │    │
│  │                                                                     │    │
│  │  ✗ Error: Unable to process payment                                │    │
│  │     Red background + X icon + error description + Retry button     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### Redundant Coding Checklist

- [ ] Error states use color + icon + text message
- [ ] Success states use color + icon + confirmation text
- [ ] Status indicators have both color and icon/text
- [ ] Interactive elements have visible focus states
- [ ] Disabled states have visual indicator beyond just color
- [ ] Loading states have both spinner and "Loading..." text
- [ ] Required fields marked with both * and "(Required)" text

---

## 10. Component Checklist

Use this checklist when implementing components:

- [ ] Follows spacing system (4dp base)
- [ ] Uses correct typography style
- [ ] Has all states (default, pressed, disabled, loading, error)
- [ ] Meets accessibility requirements
- [ ] Has dark mode support
- [ ] Has preview composable
- [ ] Documented in this file

---

## Version History

| Date | Change |
|------|--------|
| 2026-03-19 | Initial design system |
