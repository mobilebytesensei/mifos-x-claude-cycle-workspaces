# Implementation Status: Pocket

> Track implementation progress across all layers

---

## Status Summary

| Layer | Status | Progress |
|-------|:------:|:--------:|
| Design | ✅ Complete | 100% |
| Server (API) | ⏳ Pending | 0% |
| Client (Network) | ⏳ Pending | 0% |
| Feature (UI) | ⏳ Pending | 0% |

**Overall:** 25% (1/4 layers)

---

## Design Layer

| Item | Status | Notes |
|------|:------:|-------|
| User Flow | ✅ | `FLOW-pocket.md` |
| Feature Spec | ✅ | `SPEC.md` |
| API Spec | ✅ | `API.md` |
| Mockups | ⏳ | TBD |

---

## Server Layer (API Integration)

| Endpoint | Status | Notes |
|----------|:------:|-------|
| `GET /self/pockets` | ⏳ | Not implemented |
| `POST linkAccounts` | ⏳ | Not implemented |
| `POST delinkAccounts` | ⏳ | Not implemented |

### Files to Create

- [ ] `ApiEndPoints.kt` - Add POCKETS constant
- [ ] `PocketService.kt` - Ktorfit service interface
- [ ] `PocketAccountsEntity.kt` - Response models
- [ ] `PocketLinkRequest.kt` - Request model

---

## Client Layer (Repository)

| Component | Status | Notes |
|-----------|:------:|-------|
| `PocketRepository` | ⏳ | Interface not created |
| `PocketRepositoryImpl` | ⏳ | Implementation not created |
| Domain models | ⏳ | `Pocket`, `PocketAccount` |

### Files to Create

- [ ] `core/model/.../pocket/Pocket.kt`
- [ ] `core/model/.../pocket/PocketAccount.kt`
- [ ] `core/data/.../PocketRepository.kt`
- [ ] `core/data/.../PocketRepositoryImpl.kt`

---

## Feature Layer (UI)

| Screen | Status | Notes |
|--------|:------:|-------|
| `PocketDashboardScreen` | ⏳ | Main pocket view |
| `ManagePocketScreen` | ⏳ | Link/delink management |
| `LinkAccountsBottomSheet` | ⏳ | Account selection |
| `PocketViewModel` | ⏳ | State management |

### Files to Create

- [ ] `feature/pocket/build.gradle.kts`
- [ ] `PocketNavigation.kt`
- [ ] `PocketRoute.kt`
- [ ] `PocketScreen.kt`
- [ ] `PocketViewModel.kt`
- [ ] `ManagePocketScreen.kt`
- [ ] `ManagePocketViewModel.kt`
- [ ] `components/PocketAccountCard.kt`
- [ ] `components/EmptyPocketView.kt`

---

## Testing Status

| Test Type | Status | Coverage |
|-----------|:------:|:--------:|
| Unit Tests | ⏳ | 0% |
| UI Tests | ⏳ | 0% |
| Integration Tests | ⏳ | 0% |

---

## Blockers

| Blocker | Status | Resolution |
|---------|:------:|------------|
| None | - | - |

## Jira Tickets

| Type | Key | Link | Status |
|------|-----|------|--------|
| Roadmap | MR-16 | [View](https://mifosforge.jira.com/browse/MR-16) | ✅ Created |
| Epic | MW-378 | [View](https://mifosforge.jira.com/browse/MW-378) | ✅ Created |

**Stories:** MW-379 to MW-387 (9 stories with dependencies)

---

## Timeline

| Phase | Target | Actual | Status |
|-------|--------|--------|:------:|
| Design | 2026-03-03 | 2026-03-03 | ✅ |
| Server Layer | TBD | - | ⏳ |
| Client Layer | TBD | - | ⏳ |
| Feature Layer | TBD | - | ⏳ |
| Testing | TBD | - | ⏳ |
| Release | TBD | - | ⏳ |

---

## Commands

```bash
# Implement server layer
/server pocket

# Implement client layer
/client pocket

# Implement feature layer
/feature pocket

# Run tests
/test pocket
```

---

## Related

- **Flow:** `../user-flows/flows/FLOW-pocket.md`
- **Spec:** `SPEC.md`
- **API:** `API.md`
- **PR:** https://github.com/openMF/mobile-wallet/pull/1995
