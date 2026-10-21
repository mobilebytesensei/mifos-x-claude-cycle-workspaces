# SPEC — Splash Screen

| Field         | Value              |
|---------------|--------------------|
| Feature       | splash             |
| Flavor        | consumer           |
| Status        | approved           |
| Quality Score | 92                 |
| ViewModel     | SplashViewModel    |
| Archetype     | loading            |

---

## Overview

The launch screen: brand mark, app name, tagline and a loading indicator, while `RootNavViewModel`
resolves where the customer belongs.

It is the smallest ViewModel in the app — one state field, no actions, no events, no DI. That is
correct for what it does: splash does not decide anything. Session resolution is the root
navigator's job, and this screen is what renders while that happens.

The single state field is `reducedMotion`, which gates the entry animation. It exists because a
launch animation is exactly the kind of motion that must respect the platform accessibility setting,
and the screen has no other behaviour to model.

---

## Screens

| ID     | Name          | ViewModel       | Archetype |
|--------|---------------|-----------------|-----------|
| splash | Splash Screen | SplashViewModel | loading   |

---

## Components

| ID                       | Type              | Description                          |
|--------------------------|-------------------|---------------------------------------|
| splash_root              | stack             | Centred container                    |
| splash_logo              | image             | Mifos X logo                         |
| splash_app_name          | text              | "Mifos X Open Banking"               |
| splash_tagline           | text              | "Banking for Everyone"               |
| splash_loading_indicator | loading_indicator | `spinner` — session resolution       |

---

## States

Initial state: `loading`. Two states.

| State      | Meaning                                        |
|------------|-------------------------------------------------|
| loading    | Session resolution in progress                 |
| navigating | Destination resolved; transition in flight     |

No error state: a failed session resolution is not shown here — it routes to `login`, which is where
a customer can act on it.

---

## State Model

**ViewModel:** `SplashViewModel` — `SplashUiState`.

| Field           | Type      | Default |
|-----------------|-----------|---------|
| `reducedMotion` | `Boolean` | `false` |

No errors, no events, no actions, no DI. Session state is read by `RootNavViewModel`, not here.

---

## Navigation

Owned by `RootNavViewModel`, not by this screen:

| ID                        | From   | To    | Trigger      | Maps from                                 |
|---------------------------|--------|-------|--------------|-------------------------------------------|
| nav_to_login              | splash | login | auto         | `RootNavState.Auth` (unauthenticated)     |
| nav_to_consumer_home      | splash | home  | auto         | `RootNavState.UserUnlocked`               |
| nav_to_home_authenticated | splash | home  | token_exists | persisted token → `UserUnlocked`          |

Two destinations only. A field-officer branch to `fo-dashboard` was removed on 2026-08-04: no such
screen exists, and the project has been consumer-only single-flavor since 2026-08-02.

---

## API Endpoints

**None.** `api.yaml` declares no operations. Session resolution reads the persisted token from local
storage; no HTTP request is issued from this screen. Full detail: `API.md`.

---

## Design Tokens

Material 3, seed `#266489` ("Open Banking — Trust Blue"), Roboto. The entry animation is gated by
`reducedMotion`, falling back to a static presentation — motion here must declare a
`reduced_motion_fallback` per the design system's motion rules. Components reference semantic roles,
so both theme modes resolve from `design-system/design-tokens.yaml`; `DESIGN.md` is the canonical
brand spec.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/splash/{ui,flow,docs}.yaml. -->
