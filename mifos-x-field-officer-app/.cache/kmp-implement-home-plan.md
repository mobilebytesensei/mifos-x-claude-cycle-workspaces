# /kmp-implement home — implementation plan (Step 0.1)

Feature: `home` · module `feature/home` (resolved: flat, via pin) · combo `read_dashboard` (FEATURE_LAYER
"Dashboard fan-out shape") · store archetype NETWORK_WITH_CACHE · design tier: Stitch mockups 01-05.

## Reused (no new code)
- SessionRepository.sessionStream — officeId, officeName, permissions, userId, username
- CheckerInboxRepository.checkerTasksStream / rescheduleRequestsStream — work-queue counts
- CollectionSheetRepository.individualCollectionSheetStream — today's collections
- CenterRepository.centersStream + centerWithMeetingStream, GroupRepository.groupsStream — meetings + counts
- FormDraftRepository.observeAll — drafts row (local)
- SearchRecordRepository — recently opened (local)
- ServerConfigRepository — live instance name

## New, bottom-up
1. core/model `dashboard/` — DashboardUser (staff link, firstname), DashboardLoan, PortfolioSummary +
   pure calculators (own-loan filter, per-currency sums, PAR), `User.can(code)` permission predicate.
2. core/network `mifos/dashboard/` — DashboardApi: GET users/{id}, GET businessdate/BUSINESS_DATE,
   GET loans?status=, GET savingsaccounts, GET clients?status=&officeId= (count) + DTOs.
3. core/store `dashboard/` — cachedRead stores per read (@StoreProvider/@CacheKey; offline-first).
4. core/data `dashboard/` — DashboardRepository (@RepositoryBinding) streams, NETWORK_WITH_CACHE.
5. feature/home — HomeViewModel (BaseViewModel; per-card ScreenState slots; permission-gated
   subscription), HomeDashboard (IndependentCardLayout-style independent cards), LoanQueueScreen
   (own loans by status — the one new destination), strings, TestTags, @Preview, UI + VM tests.
6. cmp-navigation — BackboneRegistry.homeBody → HomeDashboard with nav callbacks.

## Not on Home (operator 2026-10-26)
Loan / savings / share / collateral creates — client-owned; start from the client profile.

## Verify
`:feature:home:test`, `:core:model` tests, assembleDebug, install + `am force-stop`, on-device capture
vs Stitch mockups per state, Maestro happy_path.
