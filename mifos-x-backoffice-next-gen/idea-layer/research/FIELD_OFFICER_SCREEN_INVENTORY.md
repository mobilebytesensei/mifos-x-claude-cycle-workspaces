# Field-Officer App — EXHAUSTIVE Screen Inventory (parity checklist)

> Ground truth from a **full source clone** of `openMF/mifos-x-field-officer-app@dev` (not sampled):
> **108 `*Screen.kt` files across 21 feature modules** (+102 ViewModels, 9 core modules). Every row
> is a real screen we must reach for full parity. `→ target` = the mifos-x-backoffice-next-gen
> feature/capability that must model it. Captured 2026-08-01. The evolve drive materializes each
> module to its **full sub-screen set** — our current idea-layer models the module roots + a few
> drill-downs; the sub-screens below are the depth to build.

## Coverage summary (108 screens)

| Module | Screens | → target feature(s) | Depth to build |
|---|---|---|---|
| auth | 1 | fineract-auth-session | modeled |
| passcode | 1 (BiometricsSetup) | cap 18 passcode-lock + cap 19 biometric-setup | build |
| about | 1 | cap 21 about-diagnostics | build |
| search | 1 | m14 | modeled |
| search-record | 1 | FO-5 | build |
| settings | 2 | m17 + network-config | expand (UpdateServerConfig → network-config) |
| center | 5 | m03-groups-centers | **expand to 5** |
| groups | 4 | m03-groups-centers | **expand to 4** |
| **client** | **38** | m02-clients + client-detail-360 + client-list + FO-2/3/4 | **expand to 38 (biggest gap)** |
| **loan** | **21** | m04-loan-portfolio + loan-detail + loan-application-wizard + cap 20 group-loan | **expand to 21** |
| savings | 7 | m05-savings-deposits-shares | **expand to 7** |
| recurringDeposit | 1 | m05 | build |
| collectionSheet | 5 | m06-collections + collection-sheet | **expand to 5** |
| checker-inbox-task | 2 | m15-approvals-makerchecker + checker-inbox | expand to 2 |
| activate | 1 | cross-entity activate | modeled |
| note | 2 | cross-entity note | build |
| document | 2 | cross-entity document | build |
| data-table | 4 | m12-datatables-config + dynamic-template-forms | **expand to 4 (+ data-entry consumer)** |
| report | 3 | m14 + report-runner | expand to 3 |
| offline | 5 | offline-sync-engine + needs-attention-inbox + FO-6 | **expand to 5** |
| path-tracking | 1 | FO-1 | build |

## The complete 108-screen list (by module)

**auth (1)** — LoginScreen
**passcode (1)** — BiometricsSetupScreen
**about (1)** — AboutScreen
**search (1)** — SearchScreen · **search-record (1)** — SearchRecordScreen
**settings (2)** — SettingsScreen · UpdateServerConfigScreen
**activate (1)** — ActivateScreen · **path-tracking (1)** — PathTrackingScreen
**note (2)** — NoteScreen · AddEditNoteScreen
**document (2)** — DocumentListScreen · DocumentDialogScreen

**center (5)** — CenterListScreen · CenterDetailsScreen · CreateNewCenterScreen · GroupListScreen · SyncCentersDialogScreen
**groups (4)** — GroupsListScreen · GroupDetailsScreen · CreateNewGroupScreen · SyncGroupDialogScreen

**client (38)** — ClientListScreen · CreateNewClientScreen · ClientDetailsScreen · ClientProfileScreen · ClientProfileGeneralScreen · ClientProfileDetailsScreen · ClientProfileEditScreen · ClientEditDetailsScreen · ClientAddressScreen · AddAddressScreen · ClientIdentifiersListScreen · ClientIdentitiesAddUpdateScreen · ClientDocumentsScreen · ClientAddDocumentsScreen · DocumentPreviewScreen · ClientSignatureScreen · PinpointClientScreen · SurveyListScreen · SurveyQuestionScreen · SurveySubmitScreen · ClientStaffScreen · ClientTransferScreen · ClientClosureScreen · ClientCollateralScreen · ClientCollateralDetailScreen · ChargesScreen · ClientUpcomingChargesScreen · ClientUpdateDefaultAccountScreen · ClientApplyNewApplicationsScreen · ClientLoanAccountsScreen · SavingsAccountsScreen · ShareAccountsScreen · CreateShareAccountScreen · FixedDepositAccountScreen · CreateFixedDepositAccountScreen · RecurringDepositAccountScreen · SyncClientsDialogScreen

**loan (21)** — LoanDashboardScreen · NewLoanAccountScreen · GroupLoanAccountScreen · LoanAccountScreen · LoanAccountProfileScreen · LoanAccountSummaryScreen · LoanAccountApprovalScreen · LoanDisburseScreen · LoanRejectScreen · LoanRepaymentScreen · LoanRepaymentScheduleScreen · LoanTransactionsScreen · LoanChargeScreen · LoanChargeOffScreen · LoanReschedulesScreen · LoanRescheduleFormScreen · CreateGuarantorScreen · AssignLoanOfficerScreen · AmountTransferScreen · LoanAccountActionScreen · LoanActionPaymentsScreen

**savings (7)** — SavingsAccountScreen · SavingsAccountSummaryScreen · SavingsAccountApprovalScreen · SavingsAccountActivateScreen · SavingsAccountTransactionScreen · SavingsAccountTransactionReceiptScreen
**recurringDeposit (1)** — RecurringAccountScreen

**collectionSheet (5)** — GenerateCollectionSheetScreen · IndividualCollectionSheetScreen · IndividualCollectionSheetDetailsScreen · NewIndividualCollectionSheetScreen · PaymentDetailsScreen

**checker-inbox-task (2)** — CheckerInboxScreen · CheckerInboxTasksScreen
**data-table (4)** — DataTableListScreen · DataTableScreen · DataTableDataScreen · DataTableRowDialogScreen
**report (3)** — ReportScreen · ReportDetailScreen · RunReportScreen
**offline (5)** — OfflineDashboardScreen · SyncClientPayloadsScreen · SyncCenterPayloadsScreen · SyncLoanRepaymentTransactionScreen · SyncSavingsAccountTransactionScreen

## Parity directive
To **achieve all features**, the evolve drive expands each module root into its full sub-screen set
above — decompose `m02-clients` into the 38 client screens, `m04-loan-portfolio` into the 21 loan
screens, `m05` into 7 savings + FD/RD, `m03` into center(5)+groups(4), `m06` into 5 collection-sheet
screens, `offline-sync-engine` into 5 offline screens, `m12`+dynamic-forms into 4 data-table screens,
`m14`+report-runner into 3 report screens. Cross-entity note(2)/document(2) + activate stay shared
modules attachable to client/group/center/loan. Every screen is permission-gated per §4.7 (3-tier).
Source clone: enumerate via `find feature -name '*Screen.kt'` on `openMF/mifos-x-field-officer-app@dev`.
