# Feature Spec: navigation

## Overview

App-level navigation orchestration including splash, authentication routing, and adaptive bottom/rail navigation.

## Screens

### SplashScreen
- **Layout**: App logo centered with loading indicator
- **Navigation**: Auto-navigates to RootNavScreen after delay
- **Requirements**: FR-011

### RootNavScreen (Platform-Specific)
- **Android**: Custom scaffold with system bar handling
- **Non-Android**: Standard scaffold
- **Navigation**: Routes to AuthenticatedNavigation based on auth state
- **ViewModel**: RootNavViewModel (checks auth state, theme, locale)

### AuthenticatedNavbarNavigationScreen
- **ViewModel**: AuthenticatedNavbarNavigationViewModel
- **Layout**:
  - Adaptive scaffold: Bottom bar (phone) / Rail (tablet) / Permanent rail (desktop)
  - Tab items: Home, Profile, Settings
  - Content area with NavHost
- **Components**: KptBottomBar, KptNavigationRail, AdaptiveNavigationSuiteScaffold
- **Requirements**: FR-012, FR-013

## Navigation Architecture

- Type-safe routes via @Serializable data classes
- AppViewModel manages global state (theme, locale, screen capture)
- KoinModules wires all feature modules into navigation graph
