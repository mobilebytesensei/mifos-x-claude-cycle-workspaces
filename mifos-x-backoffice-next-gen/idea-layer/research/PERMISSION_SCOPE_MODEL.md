# Permission-Level Scoping Model (audit)

> Verified against `apache/fineract` `develop` source (`AuthenticatedUserData.java`, `AppUser.java`, `CommandWrapper.java`, `PermissionData.java`, `MakercheckersApiResource.java`). ONE binary contains ALL capabilities; every screen, nav entry, button, sync op is resolved through this model. **There are no role `if`s anywhere in app code** — roles exist only server-side as permission bundles.

## A. Permission model

**Login** `POST /v1/authentication` (header `Fineract-Platform-TenantId`) returns:
- `permissions: Collection<String>` — **flat permission codes**, the union of `selected` permissions across the user's enabled roles. **The SOLE runtime authorization input.**
- `roles[]{id,name,description,disabled}` — **display/audit only; never branch on role name** (tenants define arbitrary roles; only codes are stable).
- `officeId/officeName` — **data scope** (server filters rows by office hierarchy), not function scope.
- `staffId/staffDisplayName` — field-officer linkage → "my portfolio/route" (`?staffId=`), orthogonal to permissions.
- `shouldRenewPassword` (true → only password-change reachable), `isTwoFactorAuthenticationRequired` (true → gate behind OTP), `base64EncodedAuthenticationKey` (basic-auth key + silent re-fetch).
- **Critical:** a super user returns `permissions:["ALL_FUNCTIONS"]` — one element. The client can NEVER enumerate effective permissions by expansion; it MUST implement the server's umbrella short-circuits.

**Catalog shape** (`PermissionData{grouping,code,entityName,actionName,selected}`): `GET /permissions`, `?makerCheckerable=true` (badge "requires approval"), `GET /roles/{id}/permissions` (password-less refresh fallback), `PUT` (admin editor). Groupings: `special, authorisation, organisation, portfolio, portfolio_center, transaction_loan, transaction_savings, accounting, report, configuration, datatable, cash_mgmt, loan_reschedule, collection_sheet`.

**Permission-code grammar:**
```
code         := ACTION "_" ENTITY          -- CREATE_CLIENT, DISBURSE_LOAN, DEPOSIT_SAVINGSACCOUNT
checker-code  := code "_CHECKER"           -- CREATE_CLIENT_CHECKER (approve a queued CREATE_CLIENT)
backdate-code := ACTION "INPAST" "_" ENTITY -- REPAYMENTINPAST_LOAN, DISBURSEINPAST_LOAN (enforced!)
report-code   := "READ_" reportName        -- "READ_Active Loans - Summary" (spaces preserved, exact match)
datatable-code:= ACTION "_" datatableName  -- READ_client_kyc_details (case preserved, exact match)
umbrella      := ALL_FUNCTIONS | ALL_FUNCTIONS_READ | CHECKER_SUPER_USER | REPORTING_SUPER_USER | TWOFACTOR_BYPASS
```
**Codes are opaque strings — compose, never decompose** (entity names contain underscores e.g. `DELINQUENCY_BUCKET`; datatable/report codes embed free text). Server composes `taskPermissionName = actionName + "_" + entityName` (`CommandWrapper.java:103`); client does the same + compares whole strings. Case matters at edges. Legacy `*_SUPER_USER` codes (ORGANISATION/PORTFOLIO/USER) are NOT enforced umbrellas — only the 5 above have verified semantics.

**Server evaluation semantics (client must mirror exactly):**
| Check | Grants |
|---|---|
| Read | `ALL_FUNCTIONS` ∨ `ALL_FUNCTIONS_READ` ∨ `READ_{ENTITY}` |
| Command (mutation) | `ALL_FUNCTIONS` ∨ exact `{ACTION}_{ENTITY}` — **`ALL_FUNCTIONS_READ` does NOT apply** |
| Report | `ALL_FUNCTIONS` ∨ `ALL_FUNCTIONS_READ` ∨ `REPORTING_SUPER_USER` ∨ `READ_{reportName}` |
| Datatable read/write | read: +`READ_{dt}`; write: `ALL_FUNCTIONS` ∨ `{ACTION}_{dt}` |
| Checker | `CHECKER_SUPER_USER` ∨ `{ACTION}_{ENTITY}_CHECKER` |
| Backdated loan ops | `ALL_FUNCTIONS` ∨ `{APPROVE,REJECT,WITHDRAW,DISBURSE,REPAYMENT}INPAST_LOAN` |
| Self-read | reading own user record bypasses `READ_USER` |

**Normalize** login → `PermissionSet{codes:HashSet, allFunctions, allRead, checkerSuper, reportingSuper, fingerprint:sha256(sorted(codes))}`. Do NOT lowercase, split, or expand umbrellas. Persist raw list + fingerprint (encrypted) so the offline app evaluates identically to the last online session.

## B. Capability Map (feature → required permission codes)

Conventions: **View** gates screen/nav visibility; **Create/Edit/Delete** gate entry points; **Special** are `?command=` actions (each with implicit `_CHECKER` twin). Permission axis composes with entity lifecycle-state predicates. `ALL_FUNCTIONS` passes all; `ALL_FUNCTIONS_READ` passes View + reports only.

- **Clients** — View `READ_CLIENT` · Create `CREATE_CLIENT` · Edit `UPDATE_CLIENT` · Delete `DELETE_CLIENT`(pending) · Special `ACTIVATE_/REJECT_/WITHDRAW_/CLOSE_/REACTIVATE_/UNDOREJECT_/UNDOWITHDRAWAL_CLIENT`, `ASSIGNSTAFF_/UNASSIGNSTAFF_CLIENT`, transfer `PROPOSETRANSFER_/WITHDRAWTRANSFER_/ACCEPTTRANSFER_/REJECTTRANSFER_/PROPOSEANDACCEPTTRANSFER_CLIENT`. Sub: identifiers `*_CLIENTIDENTIFIER`, documents `*_DOCUMENT`, notes `*_CLIENTNOTE`, charges `*_CLIENTCHARGE` (+`PAY_/WAIVE_/INACTIVATE_`), family `*_FAMILYMEMBERS`, address `*_ADDRESS`.
- **Groups/Centers** — `*_GROUP` (+`ACTIVATE_/CLOSE_/ASSOCIATECLIENTS_/DISASSOCIATECLIENTS_/ASSIGNSTAFF_/TRANSFERCLIENTS_GROUP`), `*_CENTER` (+`ASSOCIATEGROUPS_/DISASSOCIATEGROUPS_`), meetings/calendar `*_MEETING`/`*_CALENDAR` + `SAVEORUPDATEATTENDANCE_MEETING`.
- **Collections (field-officer core)** — generate: `READ_COLLECTIONSHEET`; submit individual `SAVE_COLLECTIONSHEET`; center `SAVECOLLECTIONSHEET_CENTER`; group `SAVECOLLECTIONSHEET_GROUP`; "today's route" `READ_COLLECTIONSHEET ∧ (READ_CENTER ∨ READ_GROUP)` scoped by `staffId`.
- **Loans** — View `READ_LOAN` · Create `CREATE_LOAN` · Edit `UPDATE_LOAN` · Delete `DELETE_LOAN`(pending); approval `APPROVE_/UNDOAPPROVAL_/REJECT_/WITHDRAW_LOAN`; disbursal `DISBURSE_/DISBURSETOSAVINGS_/UNDODISBURSAL_/UNDOLASTDISBURSAL_LOAN`; repayment `REPAYMENT_/ADJUST_/RECOVERYPAYMENT_/CHARGEBACK_/GOODWILLCREDIT_/CREDITBALANCEREFUND_LOAN`; terminal `WAIVEINTERESTPORTION_/WRITEOFF_/CLOSE_/FORECLOSURE_/CHARGEOFF_LOAN`; **backdated** `REPAYMENTINPAST_/DISBURSEINPAST_/APPROVEINPAST_LOAN` (date picker's past range is a capability); charges `*_LOANCHARGE`(+`WAIVE_/PAY_`), guarantors `*_GUARANTOR`, collateral `*_COLLATERAL`, reschedule `*_RESCHEDULELOAN`(+`APPROVE_/REJECT_`), officer `UPDATELOANOFFICER_/BULKREASSIGN_LOAN`.
- **Savings/Deposits/Shares** — `*_SAVINGSACCOUNT` (+`APPROVE_/ACTIVATE_/CLOSE_`); teller `DEPOSIT_/WITHDRAWAL_/UNDOTRANSACTION_/ADJUSTTRANSACTION_/POSTINTEREST_SAVINGSACCOUNT`; holds `HOLDAMOUNT_/RELEASEAMOUNT_/BLOCK_/BLOCKCREDIT_/BLOCKDEBIT_SAVINGSACCOUNT`; charges `*_SAVINGSACCOUNTCHARGE`; FD `*_FIXEDDEPOSITACCOUNT`(+`PREMATURECLOSE_`), RD `*_RECURRINGDEPOSITACCOUNT`(+`DEPOSIT_/WITHDRAWAL_`), shares `*_SHAREACCOUNT`(+`APPLYADDITIONALSHARES_/REDEEMSHARES_`), transfers `*_ACCOUNTTRANSFER`, SI `*_STANDINGINSTRUCTION`.
- **Accounting** — `*_GLACCOUNT`, `*_JOURNALENTRY`(+`REVERSE_`), `*_GLCLOSURE`, `*_ACCOUNTINGRULE`, provisioning `*_PROVISIONINGENTRIES`, `EXECUTE_PERIODICACCRUALACCOUNTING`.
- **Products/Org** — `*_LOANPRODUCT`/`*_SAVINGSPRODUCT`/`*_FIXEDDEPOSITPRODUCT`/`*_SHAREPRODUCT`, `*_CHARGE`, `*_OFFICE`, `*_STAFF`, `*_HOLIDAY`, `*_FUND`, `*_PAYMENTTYPE`.
- **Tellers** — `*_TELLER`, `ALLOCATECASHIER_/ALLOCATECASHTOCASHIER_/SETTLECASHFROMCASHIER_TELLER`.
- **Users/Roles/Permissions** — `*_USER`(own exempt), `*_ROLE`(+`ENABLE_/DISABLE_`), `READ_PERMISSION`, `PERMISSIONS_ROLE`, `UPDATE_PERMISSION`.
- **Datatables/Reports/System** — dynamic `{ACTION}_{tableName}`, `*_DATATABLE`+`REGISTER_/DEREGISTER_`, `READ_{Report Name}`∨`REPORTING_SUPER_USER`, `*_REPORT`, `READ_AUDIT`, checker inbox = `∃_CHECKER ∨ CHECKER_SUPER_USER`, scheduler `READ_/UPDATE_/EXECUTEJOB_SCHEDULER`, config `*_CONFIGURATION`/`*_CODE`/`*_CODEVALUE`, `*_EXTERNALSERVICES`/`*_HOOK`.

## C. Scope-resolution algorithm

- **C0 session gate:** `!authenticated`→error; `2FA required`→OTP (map NOT built); `shouldRenewPassword`→only password-change; else `normalize→persist→emit(PermissionsReady)`.
- **C1 primitives:** `canView(e)=allFunctions∨allRead∨"READ_"+e`; `canDo(a,e)=allFunctions∨(a+"_"+e)` (allRead never grants); `canBackdate(a)=allFunctions∨(a+"INPAST_LOAN")`; `canRunReport(n)=allFunctions∨allRead∨reportingSuper∨"READ_"+n`; `canCheck(a,e)=allFunctions∨checkerSuper∨(a+"_"+e+"_CHECKER")`; `hasAnyChecker=…∨∃code.endsWith("_CHECKER")`.
- **C2 resolve (hide vs disable):** unmapped→`HIDDEN(UNMAPPED)` (**fail closed**); permitted→`VISIBLE(enabled=statePredicate, pendingBadge=makerCheckerable)`; denied→`onDenied: HIDE` (nav roots, Create FABs, destructive) or `DISABLE`+reason (workflow-stage buttons on a visible detail — seeing the stage is operationally meaningful, e.g. "Requires DISBURSE_LOAN — ask your supervisor").
- **C3 domain double-enforcement:** every use case declares `(action,entity)`; `execute()` re-checks `canDo` before dispatch → catches stale-UI races + guards offline replay.
- **C4 403 protocol:** parse body → if NoAuthorization = drift → mark suspect, DON'T retry, `refreshPermissions()`; after refresh, prune UI + toast "your access has changed" OR surface server error verbatim; failed screen stays alive, navigate to nearest visible ancestor. **Never crash, never trust cache over server.**
- **C5 maker-checker:** `queued = commandId≠null ∧ (resourceId==null ∨ rollbackTransaction) ∨ 202` → `PENDING_APPROVAL`, "Submitted for approval" (third state, not error/success), don't optimistically apply. Pre-flight `GET /permissions?makerCheckerable=true` → badge. Checker inbox iff `hasAnyChecker`; per-entry Approve/Reject iff `canCheck(entry.action,entry.entity)`.
- **C6 refresh:** triggers = foreground TTL>15min · every sync · drift-403 · before replay. `POST /authentication` (primary) ∥ `GET /roles/{id}/permissions` union (password-less). If `fingerprint` unchanged→NoChange; else atomic swap → re-resolve map → prune now-hidden backstack → notify once. **replayOfflineQueue:** each op stored WITH `(action,entity)`; if `!canDo`→`BLOCKED_PERMISSION_REVOKED` (surfaced, never silently dropped).

## D. KMP design (`core/permissions` module, commonMain)

- `PermissionSet(codes:Set<String>)` — immutable, `HashSet` exact-case whole-string lookup, umbrella flags, `fingerprint`.
- `CapabilityEntry{id,requires:Requirement(anyOf/allOf tree),onDenied:HIDE|DISABLE,entity?,action?,statePredicateId?}` + `CapabilityMap{version,minAppVersion,entries}` — **DATA not code**, shipped as `capability-map.json` in `commonMain/composeResources`, superseded by signed remote config (monotonic version, checksum). New Fineract deployments (custom datatables/reports/renamed workflows) onboarded by shipping map data, not an app release. Only hardcoded coupling = the permission-code grammar (Fineract's stable public contract).
- `PermissionEvaluator(permissions:StateFlow<PermissionSet>, map:StateFlow<CapabilityMap>, makerCheckerable:StateFlow<Set<String>>)` — the ONLY authority the UI talks to; `resolve(id,entityState?)` + `observe(id):Flow<CapabilityState>`.
- **Compose:** `LocalCapabilities` static composition-local; nav graph FILTERED at build time (`if eval.resolve("clients.root").visible clientsGraph()`); deep-link/notification guard in NavController interceptor → AccessInfoScreen; in-screen `Gated(capability){ enabled -> ... }`. Because `PermissionSet` is a `StateFlow`, C6 refresh recomposes every gated surface + re-filters nav LIVE.
- **Network guard:** Ktor `HttpResponseValidator` 403→`PermissionDriftSuspected`; 202/commandId-without-resourceId→typed `Queued`. **Domain guard:** UseCase base pre-checks `canDo` + stamps requirement on offline-queue entries.
- **Testing (highest-risk unit):** `PermissionSetLawsTest` (umbrella laws, opaque codes, case-exact), `CapabilityMatrixTest` (persona × every entry golden file), `MapCoverageTest` (every nav route + `Gated()` id exists in map — unmapped = build failure), `MonotonicityPropertyTest` (adding permissions only adds capability), `RefreshRaceTest`, `MakerCheckerContractTest`, `Live403ContractTest` (tagged — evaluator prediction ⇔ server status).

## E. Same binary, four+ renders (persona = permission bundle)

- **Collections officer** (`READ_*`, `SAVECOLLECTIONSHEET_*`, `REPAYMENT_LOAN`, `DEPOSIT_SAVINGSACCOUNT`, `SAVEORUPDATEATTENDANCE_MEETING`) → Home = today's `staffId`-scoped route + collection-sheet capture + attendance; client/loan screens read-only (no FABs); no approvals/admin; backdated picker locked (no `REPAYMENTINPAST_LOAN`).
- **Loan officer (maker)** (+`CREATE_CLIENT/DOCUMENT/LOAN`, `UPDATE_LOAN`, `READ_LOANPRODUCT`) → + onboarding wizard, new loan application; loan detail shows Approve/Disburse **visible-but-disabled** ("Requires APPROVE_LOAN"); submissions badge **Pending approval** under tenant maker-checker.
- **Branch supervisor (checker)** (+`APPROVE_/DISBURSE_/WRITEOFF_LOAN`, `*_CHECKER`, `READ_AUDIT`, a report code) → Checker Inbox in nav (self-scoped), approval buttons live, dashboard report tile, Audit tab. Still no Admin.
- **System admin** (`ALL_FUNCTIONS` — one code) → entire surface, umbrella short-circuit, zero enumeration.
- **Auditor** (`ALL_FUNCTIONS_READ`, `READ_AUDIT`) → whole app in glass-case: everything readable, every report runnable, **not one mutating control enabled**.

> Same APK, same nav-graph source, same screens — five permission lists, five apps. **100% data.**
