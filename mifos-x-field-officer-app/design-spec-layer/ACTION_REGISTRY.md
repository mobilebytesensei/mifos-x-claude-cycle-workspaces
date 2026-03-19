# template_meta
# template_version: "2.81.0"
# template_path: "templates/blueprints/workspace-project/design-spec-layer/ACTION_REGISTRY.md"
# last_modified: "2026-03-19"

# Action Registry - O(1) Navigation Event Lookup

**Project:** {PROJECT_NAME}
**Last Updated:** {DATE}
**Total Actions:** {COUNT}

---

## Purpose

This registry tracks ALL navigation events and user actions across features, ensuring:
1. Every action has a valid destination
2. No orphan navigation events
3. Complete E2E flow connectivity

---

## Quick Reference

| Feature | Actions | Connected | Orphan | Status |
|---------|:-------:|:---------:|:------:|:------:|
| home | 7 | 6 | 1 | ⚠️ |
| signin | 2 | 2 | 0 | ✅ |
| moviedetail | 4 | 4 | 0 | ✅ |
| profile | 3 | 2 | 1 | ⚠️ |

---

## Action Types

| Type | Description | Example |
|------|-------------|---------|
| `NAVIGATE` | Navigate to another feature | `NavigateToMovieDetail(id)` |
| `NAVIGATE_BACK` | Return to previous screen | `NavigateBack` |
| `EXTERNAL` | Open external app/URL | `OpenBrowser(url)` |
| `SHEET` | Show bottom sheet | `ShowFilterSheet` |
| `DIALOG` | Show dialog | `ShowConfirmDialog` |
| `SYSTEM` | System action | `ShareContent`, `CopyToClipboard` |

---

## Actions By Feature

### home

| Action | Type | Target Feature | Target Route | Status |
|--------|------|----------------|--------------|:------:|
| `NavigateToMovieDetail` | NAVIGATE | moviedetail | `MovieDetailRoute(movieId)` | ✅ |
| `NavigateToSearch` | NAVIGATE | search | `SearchRoute` | ✅ |
| `NavigateToSeeAll` | NAVIGATE | seeall | `SeeAllRoute(category, title)` | ✅ |
| `NavigateToGenre` | NAVIGATE | genre | `GenreRoute(genreId, name)` | ❌ MISSING |
| `NavigateToProfile` | NAVIGATE | profile | `ProfileRoute` | ✅ |
| `NavigateToMood` | NAVIGATE | mood | `MoodRoute` | ✅ |
| `RefreshContent` | SYSTEM | - | - | ✅ |

**Orphan Actions (require destination):**
- `NavigateToGenre` → Target feature `genre/` does not exist

---

### signin

| Action | Type | Target Feature | Target Route | Status |
|--------|------|----------------|--------------|:------:|
| `NavigateToHome` | NAVIGATE | home | `HomeRoute` | ✅ |
| `NavigateToForgotPassword` | NAVIGATE | forgotpassword | `ForgotPasswordRoute` | ✅ |

---

### moviedetail

| Action | Type | Target Feature | Target Route | Status |
|--------|------|----------------|--------------|:------:|
| `NavigateBack` | NAVIGATE_BACK | - | - | ✅ |
| `NavigateToActor` | NAVIGATE | actor | `ActorRoute(actorId)` | ✅ |
| `ShareMovie` | SYSTEM | - | - | ✅ |
| `AddToWatchlist` | SYSTEM | - | - | ✅ |

---

## Entry Points Registry

Each feature declares how it can be reached.

### Feature Entry Points

| Feature | Route | Required Params | Optional Params | Entry Sources |
|---------|-------|-----------------|-----------------|---------------|
| home | `HomeRoute` | - | - | signin, splash |
| moviedetail | `MovieDetailRoute` | `movieId: Long` | - | home, search, seeall, watchlist |
| search | `SearchRoute` | - | `query: String?` | home, navbar |
| seeall | `SeeAllRoute` | `category: String`, `title: String` | - | home |
| profile | `ProfileRoute` | - | - | home, navbar |

---

## Orphan Actions (Missing Destinations)

Actions that reference features that don't exist:

| Source Feature | Action | Expected Target | Resolution |
|----------------|--------|-----------------|------------|
| home | `NavigateToGenre` | genre | Create `genre/` feature |
| profile | `NavigateToSettings` | settings | Create `settings/` feature |

**Total Orphans:** 2

---

## Missing Entry Points

Features that have no documented entry points:

| Feature | Has Entry Point | Resolution |
|---------|:---------------:|------------|
| splash | ❌ | Add `## Entry Points` to SPEC.md |
| onboarding | ❌ | Add `## Entry Points` to SPEC.md |

---

## Navigation Wiring Status

| Source | Target | Wired in cmp-navigation | Status |
|--------|--------|:-----------------------:|:------:|
| home → moviedetail | `navigateToMovieDetail(id)` | ✅ | ✅ |
| home → search | `navigateToSearch()` | ✅ | ✅ |
| home → seeall | `navigateToSeeAll(category, title)` | ❌ | ⚠️ Needs wiring |
| home → genre | `navigateToGenre(genreId, name)` | ❌ | ❌ Feature missing |

---

## Auto-Update Rules

This registry is automatically updated by:
1. `/gap-implement-project {feature}` - After implementation
2. `/feature {name}` - After feature layer completion
3. `/gap-analysis-project actions` - Full action scan

---

## Keywords

| Keyword | Resolution |
|---------|------------|
| actions | Show this registry |
| navigation | Show wiring status |
| orphan | Show orphan actions |
| entry points | Show entry points |
| wiring | Show navigation wiring |
