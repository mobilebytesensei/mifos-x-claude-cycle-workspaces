# template_meta
# template_version: "2.86.5"
# template_path: "templates/blueprints/workspace-project/PROJECT_TYPES.md"
# last_modified: "2026-03-20"

# Project Types Reference

> **Purpose**: Complete reference for project type taxonomy and configuration options
> **Version**: 2.30.0

---

## Overview

The claude-product-cycle framework supports three primary project types:

```
PROJECT TYPE (What you're building)
├── kmp              # Kotlin Multiplatform App/Library (consumes backend)
├── web              # Web Standalone (consumes backend)
└── backend          # Backend Service (IS the backend)
```

---

## Project Type Taxonomy

### Visual Overview

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                          PROJECT TYPE TAXONOMY                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  ┌─────────────────────────────────────────────────────────────────────────┐ ║
║  │  PROJECT TYPE: kmp (Kotlin Multiplatform)                               │ ║
║  │                                                                          │ ║
║  │  App Code (Kotlin) ──▶ server-layer/ (Schema) ──▶ Backend Provider      │ ║
║  │                                                                          │ ║
║  │  Targets: android, ios, desktop, web-wasm                               │ ║
║  │  Subtypes: kmp-app, kmp-library                                         │ ║
║  └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
║  ┌─────────────────────────────────────────────────────────────────────────┐ ║
║  │  PROJECT TYPE: web (Web Standalone)                                     │ ║
║  │                                                                          │ ║
║  │  Web App (React/Vue) ──▶ JavaScript SDK ──▶ Backend Provider            │ ║
║  │                                                                          │ ║
║  │  Targets: browser, ssr, static                                          │ ║
║  │  Subtypes: web-react, web-vue, web-svelte                               │ ║
║  └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
║  ┌─────────────────────────────────────────────────────────────────────────┐ ║
║  │  PROJECT TYPE: backend (Backend Service)                                │ ║
║  │                                                                          │ ║
║  │  Backend Code (Node/Python) ──▶ Deploys To Provider Platform            │ ║
║  │                                                                          │ ║
║  │  Targets: DERIVED from backend.provider                                 │ ║
║  │  Subtypes: backend-node, backend-python, backend-go, backend-kotlin     │ ║
║  └─────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Project Type Details

### KMP (Kotlin Multiplatform)

| Attribute | Value |
|-----------|-------|
| **project_type** | `kmp` |
| **project_subtype** | `kmp-app` \| `kmp-library` |
| **targets** | `android`, `ios`, `desktop`, `web-wasm` |
| **backend.provider** | Service the app consumes |
| **layers** | design, server, client, feature, platform, testing |

**Use Cases**:
- Mobile apps (Android + iOS)
- Desktop apps (Windows, macOS, Linux)
- Cross-platform libraries
- Apps with shared business logic

**Configuration Example**:
```yaml
project_type: kmp
project_subtype: kmp-app
targets:
  - android
  - ios
  - desktop
backend:
  provider: supabase
  features:
    - database
    - auth
    - storage
stack:
  language: kotlin
  ui: compose
  state: mvi
  di: koin
  http: ktor
```

---

### Web (Web Standalone)

| Attribute | Value |
|-----------|-------|
| **project_type** | `web` |
| **project_subtype** | `web-react` \| `web-vue` \| `web-svelte` |
| **targets** | `browser`, `ssr`, `static` |
| **backend.provider** | Service the app consumes |
| **layers** | design, server, client, feature, testing |

**Use Cases**:
- React/Next.js applications
- Vue/Nuxt applications
- Svelte/SvelteKit applications
- Progressive Web Apps (PWAs)

**Configuration Example**:
```yaml
project_type: web
project_subtype: web-react
targets:
  - browser
  - ssr
backend:
  provider: supabase
  features:
    - database
    - auth
stack:
  language: typescript
  ui: react
  state: zustand
  http: fetch
```

---

### Backend (Backend Service)

| Attribute | Value |
|-----------|-------|
| **project_type** | `backend` |
| **project_subtype** | `backend-node` \| `backend-python` \| `backend-go` \| `backend-kotlin` |
| **targets** | DERIVED from `backend.provider` |
| **backend.provider** | WHERE the code deploys |
| **layers** | design, server (with backend + engine sub-layers), testing |

**Use Cases**:
- API microservices
- Data processing pipelines
- Serverless functions
- Background workers

**Configuration Example**:
```yaml
project_type: backend
project_subtype: backend-node
# NOTE: targets not specified - derived from provider
backend:
  provider: supabase
  # provider determines deployment:
  # supabase → Edge Functions (Deno)
  # firebase → Cloud Functions (Node.js)
  # aws → Lambda (Node/Python/Go)
  # custom → Container/VM
stack:
  language: typescript
  framework: hono
  database: postgresql
```

---

## Backend Providers

### Provider Comparison

| Provider | Database | Auth | Functions | Real-time | Engine |
|----------|:--------:|:----:|:---------:|:---------:|:------:|
| **supabase** | PostgreSQL | Supabase Auth | Edge (Deno) | Yes | Python ETL |
| **firebase** | Firestore | Firebase Auth | Cloud (Node) | Yes | Python ETL |
| **aws** | DynamoDB | Cognito | Lambda | AppSync | Python ETL |
| **custom** | Any | JWT/OAuth | Express/Hono | WebSocket | Python ETL |
| **none** | - | - | - | - | - |

### Provider → Deployment Target

| Provider | Deployment Target | Runtime |
|----------|-------------------|---------|
| `supabase` | Supabase Edge Functions | Deno |
| `firebase` | Cloud Functions | Node.js |
| `aws` | Lambda | Node/Python/Go |
| `custom` | Container/VM | Docker |

---

## Backend Sub-Layers

Every backend provider has two required sub-layers:

```
server-layer/
├── {provider}-backend/     # API Layer (User-Facing)
│   ├── Schema              # Tables, indexes
│   ├── Security            # RLS, rules, IAM
│   ├── Functions           # Serverless compute
│   └── Storage             # File buckets
│
└── {provider}-engine/      # Data Feeder (ETL Pipeline)
    ├── extract/            # Fetch from external APIs
    ├── transform/          # Clean and normalize
    ├── enrich/             # AI augmentation
    └── load/               # Insert into backend
```

### Data Flow

```
External APIs → Engine (ETL) → Backend (Database) → App (KMP/Web)
```

### Sub-Layer by Provider

| Provider | Engine (Data Feeder) | Backend (API Layer) |
|----------|----------------------|---------------------|
| **supabase** | `supabase-engine/` (Python) | `supabase-backend/` (SQL + Deno) |
| **firebase** | `firebase-engine/` (Python) | `firebase-backend/` (Rules + Node) |
| **aws** | `aws-engine/` (Python) | `aws-backend/` (SAM + Lambda) |
| **custom** | `custom-engine/` (Python) | `custom-backend/` (Docker) |

---

## Deployment Targets

### KMP Targets

| Target | Description | Platform |
|--------|-------------|----------|
| `android` | Android smartphones/tablets | Android |
| `ios` | iPhone/iPad | iOS |
| `desktop` | Windows, macOS, Linux | JVM |
| `web-wasm` | Browser via WebAssembly | Browser |

### Web Targets

| Target | Description | Framework |
|--------|-------------|-----------|
| `browser` | Client-side only | React/Vue/Svelte |
| `ssr` | Server-side rendering | Next.js/Nuxt/SvelteKit |
| `static` | Static site generation | Astro/Gatsby |

### Backend Targets

Backend targets are **derived** from the `backend.provider`:

| Provider | Derived Target |
|----------|----------------|
| `supabase` | Supabase Edge Functions |
| `firebase` | Google Cloud Functions |
| `aws` | AWS Lambda |
| `custom` | Docker Container / VM |

---

## Layers by Project Type

| Layer | KMP | Web | Backend | Purpose |
|-------|:---:|:---:|:-------:|---------|
| design-spec-layer | Yes | Yes | Yes | Feature specs, mockups |
| plan-layer | Yes | Yes | Yes | Work planning |
| server-layer | Yes | Yes | Yes (primary) | API documentation |
| client-layer | Yes | Yes | No | Network services, repositories |
| feature-layer | Yes | Yes | No | UI screens, ViewModels |
| infrastructure-layer | Yes | No | No | Build-logic, navigation, DI wiring |
| platform-layer | Yes | No | No | expect/actual declarations |
| testing-layer | Yes | Yes | Yes | Test utilities |

> **Note**: See `LAYER_APPLICABILITY.md` for detailed layer contents and applicability rules.

---

## Stack Configuration

### KMP Stack Options

| Field | Options | Default |
|-------|---------|---------|
| `stack.language` | `kotlin` | `kotlin` |
| `stack.ui` | `compose` | `compose` |
| `stack.state` | `mvi`, `mvvm` | `mvi` |
| `stack.di` | `koin`, `hilt` | `koin` |
| `stack.http` | `ktor` | `ktor` |

### Web Stack Options

| Field | Options | Default |
|-------|---------|---------|
| `stack.language` | `typescript`, `javascript` | `typescript` |
| `stack.ui` | `react`, `vue`, `svelte` | `react` |
| `stack.state` | `redux`, `zustand`, `mobx`, `pinia` | `zustand` |
| `stack.http` | `fetch`, `axios`, `tanstack-query` | `fetch` |

### Backend Stack Options

| Field | Options | Default |
|-------|---------|---------|
| `stack.language` | `typescript`, `python`, `go`, `kotlin` | `typescript` |
| `stack.framework` | `hono`, `express`, `fastapi`, `gin`, `ktor` | `hono` |
| `stack.database` | `postgresql`, `firestore`, `dynamodb` | `postgresql` |

---

## Quick Reference

### Project Type Selection

| I want to build... | Project Type | Subtype |
|-------------------|--------------|---------|
| Android + iOS mobile app | `kmp` | `kmp-app` |
| Shared library for mobile | `kmp` | `kmp-library` |
| React web application | `web` | `web-react` |
| Vue.js web application | `web` | `web-vue` |
| API microservice | `backend` | `backend-node` |
| Data processing service | `backend` | `backend-python` |

### Configuration Cheat Sheet

```yaml
# KMP App with Supabase
project_type: kmp
project_subtype: kmp-app
targets: [android, ios]
backend:
  provider: supabase

# React Web with Firebase
project_type: web
project_subtype: web-react
targets: [browser, ssr]
backend:
  provider: firebase

# Backend Service on AWS
project_type: backend
project_subtype: backend-python
backend:
  provider: aws
```

---

## Related Files

| File | Purpose |
|------|---------|
| `PROJECT.md` | Project configuration template |
| `/project-add` | Add new project command |
| `/project-migration` | Migrate existing projects |
| `E2E_DEVELOPMENT_GUIDE.md` | Full development workflow |
