# template_meta
# template_version: "2.86.0"
# template_path: "core/blueprints/workspace-project/idea-layer/ARCHITECTURE.md"
# generated_by: "/project-add layer scaffold (from idea-plan.yaml §technical_decisions, §permission_scope, §layers, research/)"

# System Architecture — mifos-x-backoffice-next-gen

> **Version**: 1.0
> **Last Updated**: 2026-07-17
> **Status**: Draft — generated from idea-plan.yaml; refine as the design firms up.
> **Source of truth**: `idea-layer/idea-plan.yaml` (§technical_decisions, §permission_scope, §layers) + `idea-layer/research/`

---

## 1. Overview

MifosX BackOffice is a **single KMP binary** (Compose Multiplatform — Android + iOS + Desktop) that exposes the **entire Apache Fineract API surface** (600 paths / 965 operations, live-verified against the Mifos sandbox) as real, end-to-end features, and shows each user **exactly and only** the features their server-returned permissions allow. The single most important architectural decision is that **a "role" is just a permission bundle** — there is no hardcoded role branching. `POST /v1/authentication` returns a flat `permissions[]` array; a `PermissionEvaluator` resolves a data-driven **Capability Map** that gates every one of the 17 back-office module roots, every screen, and every action. The same binary is a system admin, a teller, an accountant, or a collections field officer depending purely on the login permission array. The whole platform is **offline-first**: reads are cached everywhere (CACHE_FIRST_SWR), writes are queued through a durable outbox, and batch replay guarantees zero duplicate/lost transactions. Backend is Apache Fineract, consumed as-is with **zero server forks**.

---

## 2. Source of Truth & Data Ownership

> The upstream authoritative system is Apache Fineract; the app holds a derived, offline-first cache and a durable write-outbox that is the local system-of-record for un-synced work.

| Data domain | Owner / store | Truth type | Rebuildable? |
|-------------|---------------|------------|--------------|
| All Fineract business entities (clients, loans, savings, GL, products, org, users, …) | Apache Fineract (server) | upstream SoT | yes (re-pull) |
| Cached reads (Room `SourceOfTruth` per entity via Store5) | `core/database` (Room) + `core/store` | derived / cached read model | yes (re-fetch) |
| Queued offline mutations (`framework_submit_drafts` / `DraftEntity`) | `core/database` outbox (Room v11) | system-of-record until replayed | **no** (irreplaceable until synced) |
| Permission set + fingerprint | encrypted local store (Keystore/Keychain-wrapped) | derived from `permissions[]` at login | yes (re-login) |
| Capability Map (`capability-map.json`) | `core/permissions` (data, remote-updatable) | derived / config | yes (re-fetch/rebuild) |

---

## 3. Architecture Style

| Attribute | Choice | Source |
|-----------|--------|--------|
| Pattern | MVI (`BaseViewModel<State,Event,Action>`) | §tech.architecture / §technical_decisions |
| State management | Store5 (`StoreFactory` + Room `SourceOfTruth` + `asScreenStream` CACHE_FIRST_SWR) + `ScreenState` (6 variants) | §technical_decisions.offline_read |
| Dependency injection | Koin | §tech.di |
| Navigation | Permission/capability-registry-driven nav (build-time filter; Material3 Adaptive BottomBar ↔ NavigationRail/drawer) | §technical_decisions.nav_model / adaptive_scaffold |
| Backend provider | none (Apache Fineract consumed as-is; server layer = API contract docs only) | §backend.provider / §layers.server_note |
| Platforms | android, ios (desktop first-class per §technical_decisions.platforms) | §platforms / §technical_decisions.platforms |

---

## 4. Layered Structure

> Enabled layers (from §layers): plan, design-spec, server, client, feature, infrastructure, platform, testing. The runtime source spine follows the openMF/kmp-project-template A–L slot model.

| Layer | Enabled | Responsibility |
|-------|:-------:|----------------|
| plan | ✅ | Roadmap, release phases (P0–P6), gap planning |
| design-spec | ✅ | Screen specs, flows, mockups (Figma design tool) |
| server | ✅ | **Fineract API contract docs** — no server built; backend consumed as-is |
| client | ✅ | Ktorfit APIs + DTOs + repositories (`core/network`, `core/data`) |
| feature | ✅ | Compose UI + MVI ViewModels per module (`feature/{m}`) |
| infrastructure | ✅ | Build config, permission-driven navigation graph, Koin DI wiring |
| platform | ✅ | Android/iOS/Desktop expect-actual (secure storage, biometrics, receipts) |
| testing | ✅ | ViewModel tests, Compose UI tests, capability-matrix golden tests |

```
idea-layer (SoT)
     │
     ▼
server-layer (Fineract API contract docs) ──► client-layer (Ktorfit + DTOs + repos)
                                                     │
                                                     ▼
core/permissions (PermissionEvaluator + CapabilityMap)  ──gates──►  feature-layer (M01–M17 UI + VM)
                                                     │                       │
                                                     ▼                       ▼
                                          infrastructure-layer (nav filter + Koin DI)
                                                     │
                                                     ▼
                                          platform-layer (android / ios / desktop)
```

---

## 5. Component / System Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│  Compose Multiplatform UI  (Android · iOS · Desktop)                   │
│    M01 Dashboard · M02 Clients … M17 Sync/Settings                     │
│    every root/screen/action wrapped in Gated{} (permission-checked)   │
└───────────────┬───────────────────────────────────────┬──────────────┘
                │                                         │
      ┌─────────▼─────────┐                     ┌─────────▼──────────┐
      │ core/permissions  │                     │  MVI ViewModels    │
      │ PermissionSet     │◄── login perms[] ──►│  ScreenState (6)   │
      │ CapabilityMap     │                     └─────────┬──────────┘
      │ PermissionEval.   │                               │
      └───────────────────┘                     ┌─────────▼──────────┐
                                                │ core/store (Store5) │
                                                │ read: CACHE_FIRST   │
                                                │ write: outbox+batch │
                                                └───┬─────────────┬───┘
                                    ┌───────────────▼──┐     ┌────▼─────────────┐
                                    │ core/database    │     │ core/network     │
                                    │ Room SoT + outbox│     │ Ktorfit + DTOs   │
                                    │ (DraftEntity v11)│     │ tenant header    │
                                    └──────────────────┘     └────┬─────────────┘
                                                                  │
                                                     ┌────────────▼────────────┐
                                                     │  Apache Fineract server  │
                                                     │  (consumed as-is)        │
                                                     │  POST /batches keystone  │
                                                     └──────────────────────────┘
```

---

## 6. External Integrations & APIs

> From the Fineract API audit (`research/FINERACT_API_SURFACE.md`). Backend provider is `none` — no self-hosted server; the app is a client of an institution's existing Fineract instance.

| Integration | Provides | Access pattern | Auth |
|-------------|----------|----------------|------|
| Apache Fineract REST API (v1) | 965 operations: clients/KYC, loans, savings/deposits/shares, collections, accounting/GL, products, org, users/roles/permissions, tellers, datatables, scheduler, reports/search/audit, maker-checker, communications | direct + offline-cached (Store5) | basicAuth `base64EncodedAuthenticationKey` after `POST /v1/authentication`; OAuth2/OIDC optional; global `Fineract-Platform-TenantId` header |
| `POST /v1/batches` | Transactional batch replay (`enclosingTransaction`) — the offline-sync keystone | queued via outbox, replayed on reconnect | inherited (basicAuth + tenant) |
| `GET /{entity}/template` + `/v1/datatables` | Field defaults + allowed-value lists → dynamic form schema | cached offline; drives the dynamic-forms engine | inherited |
| Fineract Client KMP SDK (openMF) | Preferred typed client over hand-rolling 965 endpoints; supplement via generated-from-OpenAPI + Ktorfit for gaps | direct | inherited |

---

## 7. Scaling & Performance Considerations

- **CACHE_FIRST_SWR everywhere** — cache emitted instantly; background revalidation only when `FreshnessBands` marks data Stale (`validator.markFresh()` MUST follow every write or TTL never starts).
- **Pagination** — large lists use `Store<PageKey,…>` + `asPagingScreenStream` (`offset = page*pageSize` ≙ Fineract paging); target <1s from cache; no unbounded `LazyColumn`.
- **Durable idempotency** — `idempotency_key` persisted on `DraftEntity` (Room v11) so a crash between save and replay does not mint a new key → zero double-post. (Note: today's template keeps the key in-memory only; the Room-v11 persist migration is a NEW infra piece this project must land.)
- **Per-domain offline policy** — field-ops/transactions are offline-queued + replayed; admin/accounting/config/roles are **online-only + maker-checker** (deferred sync is wrong for GL postings, role changes, product edits). Opt-in per module, never global write-behind.
- **Delta-pull sync** — `Synchronizer.changeListSync` per-entity adapters over `lastModifiedSince`, scoped to the user's office/portfolio; day's ops target <60s on 3G.
- **NFR targets** — cold start <2.5s; sync latency <2h; ≥99.5% crash-free; reversal rate <0.5%.

---

## 8. Key Architecture Decisions

> Each significant decision should be recorded as an ADR under `idea-layer/adr/`.

| ADR | Decision | Status |
|-----|----------|--------|
| (pending) | Permission-driven capability model as the sole UI authorization authority (`core/permissions`) | Proposed |
| (pending) | Offline-first on openMF/kmp-project-template Store5 seam (reads cached, writes outboxed, batch replay) | Proposed |
| (pending) | Per-domain offline policy (transactions queued; admin/accounting online-only + maker-checker) | Proposed |
| (pending) | Dynamic template-driven forms from `GET /{entity}/template` + `/datatables` | Proposed |
| (pending) | Durable idempotency key on `DraftEntity` (Room v11) | Proposed |

---

## 9. Risks & Open Questions

| Risk / question | Impact | Mitigation / owner |
|-----------------|--------|--------------------|
| In-memory idempotency key today → double-post on crash-between-save-and-replay | High (money movement) | Land the Room-v11 durable idempotency migration (NEW infra #3) before P2 money-movement exit |
| Capability Map drift vs server permissions (`403` at runtime) | Medium | 403 drift protocol: refresh permissions, re-resolve map, prune UI, notify once, replay revalidates — never crash |
| 965 operations is a large surface to consume end-to-end | High (scope) | Prefer the openMF Fineract Client KMP SDK; supplement generated-from-OpenAPI; phase delivery P0→P6; contract-test CI vs the live spec |
| Fineract server upgrades change contracts | Medium | P6 Fineract-upgrade regression via contract tests against the live `fineract.json` spec |
| `/v1/self/**` absent from this build's spec (module disabled) | Low | Customer flows, if needed, proxy through the full API under a permission-scoped user |

---

> Regenerate by `/idea-plan` / `/idea-sync` when §technical_decisions or §layers change.
> Hand-edits are preserved — the wizard prompts [Overwrite]/[Merge]/[Keep] before rewriting.
