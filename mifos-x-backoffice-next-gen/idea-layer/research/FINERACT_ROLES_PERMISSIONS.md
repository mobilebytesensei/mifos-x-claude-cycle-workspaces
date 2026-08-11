# Fineract Roles → Permissions — real data (instance: `mifos-bank-2`)

> Live from `GET /roles` + `GET /roles/{id}/permissions` (selected=true), tenant `mifos-bank-2`, 2026-08-01.
> **15 roles.** Codes are `{ACTION}_{ENTITY}` (+ `_CHECKER` maker-checker twins; `special` = umbrellas).
> This is the real grant-set to model the role-based walkthroughs on. Instance guide: `FINERACT_INSTANCES.md`.

## Role → archetype → grant summary

| id | Role | Perms | Archetype | Signature capability |
|---|---|---|---|---|
| 1 | Super user | 13 | super-user | `ALL_FUNCTIONS` (+ exchange-rate/transfer-fee extras) |
| 2 | Self Service User | 29 | self-service | customer read + own loan/savings apply |
| 3 | SUPERVISOR | 99 | supervisor | client/group/center **activate + reject/withdraw/undo lifecycle** + broad READ |
| 4 | REVISOR DE PRESTAMOS | 459 | loan reviewer/**checker** | near-full portfolio + loan + savings incl. **APPROVE/DISBURSE/WRITEOFF + all _CHECKER** |
| 5 | CAPTURISTA Y REVISOR | 459 | maker+checker | identical grant to REVISOR (full maker + checker) |
| 6 | Oficial KYC | 43 | CSR/onboarding | client activate/close/transfer + READ everything + read users/roles |
| 7 | OFICIAL DE CONTROL | 105 | control/compliance | client reject/withdraw/undo + loan officer reassignment + broad READ |
| 8 | TESORERO | 89 | treasurer | **DISBURSE_LOAN** + disbursal undo + broad READ |
| 9 | CAJERO | 75 | teller/cashier | **DEPOSIT/WITHDRAWAL savings + REPAYMENT_LOAN** + org/datatable READ |
| 10 | CAPTURISTA | 150 | maker (data entry) | full portfolio CREATE/UPDATE (client/loan/savings/deposits) — no transactions |
| 11 | PROMOTOR | 139 | field agent | portfolio CREATE/UPDATE + PAY_CLIENTCHARGE |
| 12 | **OFICIAL DE CAMPO** | 149 | **loan/field officer** | portfolio CREATE/UPDATE (client/loan/savings/guarantor/collateral) — **no APPROVE/DISBURSE** (maker only) |
| 13 | EJECUTIVO | 195 | branch officer | portfolio CREATE/UPDATE + **56 datatable CRUD** + group/center create + FORECLOSURE/CHARGEOFF |
| 14 | OFICIAL PLD | 40 | AML officer | client activate/close/transfer + audit/config/role READ |
| 15 | ANALISTA DE PRESTAMOS | 0 | loan analyst | **empty role — no permissions granted** |

**Reading for the plan:** the maker↔checker split is real and explicit here — `OFICIAL DE CAMPO` (maker, no approve/disburse) vs `REVISOR DE PRESTAMOS`/`CAPTURISTA Y REVISOR` (hold `APPROVE_LOAN`/`DISBURSE_LOAN` + `_CHECKER` twins) vs `TESORERO`/`CAJERO` (money movement). The app's `permission-capability-engine` gates every action on these exact codes.

---

## [1] Super user — 13 permissions
**self_service** (9): `CONVERT_CURRENCY`, `CREATE_EXCHANGE_RATE`, `CREATE_TRANSFER_FEE`, `DELETE_EXCHANGE_RATE`, `DELETE_TRANSFER_FEE`, `READ_EXCHANGE_RATE`, `READ_TRANSFER_FEE`, `UPDATE_EXCHANGE_RATE`, `UPDATE_TRANSFER_FEE`
**portfolio** (3): `FORCE_WITHDRAWAL_SAVINGSACCOUNT`, `FORCE_WITHDRAWAL_SAVINGSACCOUNT_CHECKER`, `SYNC_EXCHANGE_RATE`
**special** (1): `ALL_FUNCTIONS`

## [2] Self Service User — 29 permissions
**portfolio** (14): `CREATE_CLIENTIMAGE`, `CREATE_LOAN`, `CREATE_SAVINGSACCOUNT`, `DELETE_CLIENTIMAGE`, `DELINK_ACCOUNT_FROM_POCKET`, `LINK_ACCOUNT_TO_POCKET`, `READ_CLIENT`, `READ_CLIENTCHARGE`, `READ_CLIENTIMAGE`, `READ_LOAN`, `READ_SAVINGSACCOUNT`, `READ_SAVINGSACCOUNTCHARGE`, `UPDATE_LOAN`, `UPDATE_SAVINGSACCOUNT`
**self_service** (4): `CONVERT_CURRENCY`, `CREATE_EXCHANGE_RATE`, `READ_EXCHANGE_RATE`, `READ_TRANSFER_FEE`
**SSBENEFICIARYTPT** (4): `CREATE_SSBENEFICIARYTPT`, `DELETE_SSBENEFICIARYTPT`, `READ_SSBENEFICIARYTPT`, `UPDATE_SSBENEFICIARYTPT`
**organisation** (3): `READ_LOANPRODUCT`, `READ_OFFICE`, `READ_SAVINGSPRODUCT`
**configuration** (2): `READ_Client Details`, `READ_REPORT`
**transaction_loan** (1): `WITHDRAW_LOAN`
**transaction_savings** (1): `CREATE_ACCOUNTTRANSFER`

## [3] SUPERVISOR — 99 permissions
**portfolio** (45): client/group/center **activate + reject/withdraw/undo lifecycle** + broad READ — `ACTIVATE_CLIENT(+_CHECKER)`, `REACTIVATE_CLIENT(+_CHECKER)`, `REJECT_CLIENT(+_CHECKER)`, `WITHDRAW_CLIENT(+_CHECKER)`, `UNDOREJECT_CLIENT(+_CHECKER)`, `UNDOWITHDRAWAL_CLIENT(+_CHECKER)`, `REJECTTRANSFER_CLIENT(+_CHECKER)`, `WITHDRAWTRANSFER_CLIENT(+_CHECKER)`, `ACTIVATE_GSIMACCOUNT`, `REJECT_GLIMLOAN`, `REJECT_GSIMACCOUNT`, `INACTIVATE_SAVINGSACCOUNTCHARGE(+_CHECKER)`, `DEACTIVATEOVERDUE_LOANCHARGE`, + `READ_*` (ADDRESS, CLIENT, CLIENTCHARGE, CLIENTIDENTIFIER, CLIENTIMAGE, CLIENTNOTE, COLLATERAL, DOCUMENT, FAMILYMEMBERS, FIXEDDEPOSITACCOUNT, FLOATINGRATE, GUARANTOR, LOAN, LOANNOTE, LOANTRANSACTIONNOTE, MEETING, PAYMENTTYPE, PRODUCTMIX, RECURRINGDEPOSITACCOUNT, SAVINGNOTE, SAVINGSACCOUNT, SAVINGSACCOUNTCHARGE, STAFFIMAGE)
**organisation** (23): READ of BUSINESS_DATE, CHARGE, DELINQUENCY_BUCKET/TAGS, EMAIL(+_CAMPAIGN), FIXEDDEPOSITPRODUCT, FUND, HOLIDAY, LOANPRODUCT, OFFICE, OFFICETRANSACTION, RATE(+_CHECKER), RECURRINGDEPOSITPRODUCT, SAVINGSPRODUCT, SMS(+CAMPAIGN), STAFF, TAXCOMPONENT, TAXGROUP, TEMPLATE, WORKINGDAYS
**datatable** (14): READ of the institution's custom tables (CONDICION, CREDITO_INSTITUCIO_FINANCIERA, DATOS_CONTACTO, DATOS_DE_LA_PERSONA_SOLICITANTE, DATOS_DIRECCION, DATOS_RAZON_SOCIAL, DATOS_SUCURSAL, DATOS_UNIDAD_PRODUCTIVA, DOMICILIO_NEGOCIO, DOMICILIO_PARTICULAR, ENTITY_DATATABLE_CHECK, INFORMACION_DEL_NEGOCIO…, INSTITUCION_FINANCIERA, Sample Data Table)
**configuration** (7): `READ_CALENDAR/CODE/CODEVALUE/CONFIGURATION/CURRENCY/DATATABLE/REPORT`
**portfolio_group** (4): `ACTIVATE_GROUP(+_CHECKER)`, `READ_GROUP`, `READ_GROUPNOTE` · **portfolio_center** (3): `ACTIVATE_CENTER(+_CHECKER)`, `READ_CENTER`
**account_transfer** (1): `READ_STANDINGINSTRUCTION` · **loan_reschedule** (1): `READ_RESCHEDULELOAN` · **transaction_client** (1): `READTRANSACTION_CLIENT`

## [4] REVISOR DE PRESTAMOS — 459 permissions  ·  ## [5] CAPTURISTA Y REVISOR — 459 (identical grant)
The two near-full "maker + checker" roles. Breakdown:
**portfolio** (269): full CRUD + lifecycle on client / address / collateral / guarantor / document / familymembers / charts / interestrate / meeting / paymenttype / productmix + accounts (fixed/recurring deposit create/update/delete) + client transfer (PROPOSE/ACCEPT/REJECT/WITHDRAW, +_CHECKER) + GLIM/GSIM (`APPROVE_GLIMLOAN`, `APPROVE_GSIMACCOUNT`, `DISBURSE_GLIMLOAN`, `REPAYMENT_GLIMLOAN`) + `FORECLOSURE_LOAN(+_CHECKER)`, `REAGE_LOAN`, `REAMORTIZE_LOAN`, `SETFRAUD_LOAN`, `SAVEORUPDATEATTENDANCE_MEETING`, `WAIVE_*CHARGE(+_CHECKER)`, `PAY_*CHARGE(+_CHECKER)` (269 codes, ~half `_CHECKER`)
**transaction_savings** (102): full savings/FD/RD lifecycle — `APPROVE/ACTIVATE/REJECT/CLOSE/WITHDRAW`, `DEPOSIT`, `WITHDRAWAL`, `HOLDAMOUNT`/`RELEASEAMOUNT`, `BLOCK`/`UNBLOCK`(+CREDIT/DEBIT), `POSTINTEREST(ASONDATE)`, `CALCULATEINTEREST`, `PREMATURECLOSE` (FD/RD), `CREATE_ACCOUNTTRANSFER`, `REFUNDBYTRANSFER`, `REVERSE/UNDOTRANSACTION` — **each with its `_CHECKER` twin**
**transaction_loan** (61): the full loan-action surface — `APPROVE_LOAN(+_CHECKER)`, `DISBURSE_LOAN(+_CHECKER)`, `DISBURSETOSAVINGS`, `REJECT_LOAN(+_CHECKER)`, `WITHDRAW_LOAN(+_CHECKER)`, `REPAYMENT_LOAN(+_CHECKER)`, `WRITEOFF_LOAN(+_CHECKER)`, `UNDOWRITEOFF`, `CHARGEOFF_LOAN`/`UNDOCHARGEOFF`, `CLOSE_LOAN(+_CHECKER)`, `CLOSEASRESCHEDULED(+_CHECKER)`, `WAIVEINTERESTPORTION(+_CHECKER)`, `DOWNPAYMENT`, `GOODWILLCREDIT`, `INTERESTPAYMENTWAIVER`, `MERCHANTISSUEDREFUND`, `REFUNDBYCASH(+_CHECKER)`, `CREDITBALANCEREFUND`, `RECOVERYPAYMENT`, `CHARGEBACK`, `CHARGEREFUND`, `BULKREASSIGN(+_CHECKER)`, `UPDATELOANOFFICER(+_CHECKER)`, `APPROVALUNDO(+_CHECKER)`, `DISBURSALUNDO`/`DISBURSALLASTUNDO`(+_CHECKER), `BUYDOWNFEE`/`CAPITALIZEDINCOME`/`SALE`/`BUYBACK`/`CONTRACT_TERMINATION` variants
**portfolio_group** (27): full group CRUD + `ASSIGNSTAFF_GROUP`, `ASSOCIATE/DISASSOCIATECLIENTS_GROUP`, `SAVECOLLECTIONSHEET_GROUP`, `TRANSFERCLIENTS_GROUP(+_CHECKER)`, role assign/unassign (+_CHECKER)
> These are the **checker / full-authority** roles: everything a maker can submit, they can also APPROVE/DISBURSE/WRITEOFF and act as `_CHECKER`. (Full per-code list captured in the source dump; the two roles are byte-identical.)

## [6] Oficial KYC — 43 permissions
**portfolio** (23): `ACCEPTTRANSFER_CLIENT(+_CHECKER)`, `ACTIVATE_CLIENT(+_CHECKER)`, `ASSIGNSTAFF_CLIENT`, `CLOSE_CLIENT(+_CHECKER)`, `UPDATE_CLIENT`, `UPDATE_LOAN`, `UPDATE_LOANNOTE`, + `READ_*` (CLIENT, CLIENTCHARGE, CLIENTIDENTIFIER, CLIENTIMAGE, CLIENTNOTE, COLLATERAL, DOCUMENT, FAMILYMEMBERS, FIXEDDEPOSITACCOUNT, FLOATINGRATE, GUARANTOR, LOAN, SAVINGNOTE)
**configuration** (8): `READ_ACCOUNTNUMBERFORMAT/AUDIT/CACHE/CALENDAR/CODE/CONFIGURATION/CURRENCY/HOOK`
**accounting** (4): `READ_ACCOUNTINGRULE/GLACCOUNT/GLCLOSURE/JOURNALENTRY`
**authorisation** (4): `PERMISSIONS_ROLE`, `READ_PASSWORD_PREFERENCES`, `READ_PERMISSION`, `READ_USER`
**account_transfer** (1): `READ_STANDINGINSTRUCTION` · **loan_reschedule** (1): `READ_RESCHEDULELOAN` · **portfolio_center** (1): `READ_CENTER` · **portfolio_group** (1): `READ_GROUP`

## [7] OFICIAL DE CONTROL — 105 permissions
**portfolio** (46): GLIM/GSIM approve/reject/undo (`APPROVE_GLIMLOAN`, `APPROVE_GSIMACCOUNT`, `REJECT_GLIMLOAN`, `REJECT_GSIMACCOUNT`, `UNDOAPPROVAL_GLIMLOAN`, `APPROVALUNDO_GSIMACCOUNT`), client reject/withdraw/undo (+_CHECKER), `CREATE_COLLATERAL/GUARANTOR/LOANCHARGE`, `UPDATE_CLIENT/LOAN`, + broad `READ_*`
**organisation** (23) + **datatable** (14) + **configuration** (7): same READ bundles as SUPERVISOR
**transaction_loan** (7): `APPROVALUNDO_LOAN(+_CHECKER)`, `UPDATELOANOFFICER_LOAN(+_CHECKER)`, `UPDATE_APPROVED_AMOUNT_LOAN`, `WITHDRAW_LOAN(+_CHECKER)`
**portfolio_center** (3): `ACTIVATE_CENTER(+_CHECKER)`, `READ_CENTER` · **portfolio_group** (2): `READ_GROUP/GROUPNOTE` · **account_transfer/loan_reschedule/transaction_client** (1 each): READ + `READTRANSACTION_CLIENT`

## [8] TESORERO (treasurer) — 89 permissions
**portfolio** (31): `CREATE_COLLATERAL/GUARANTOR/LOANCHARGE`, `DISBURSE_GLIMLOAN`, `UNDODISBURSAL_GLIMLOAN`, `UPDATE_CLIENT`, `UPDATE_DISBURSEMENTDETAIL`, `UPDATE_LOAN`, + broad `READ_*`
**organisation** (23) + **datatable** (14) + **configuration** (7): READ bundles
**transaction_loan** (9): the **disbursal** surface — `DISBURSE_LOAN(+_CHECKER)`, `DISBURSETOSAVINGS_LOAN`, `DISBURSEWITHOUTAUTODOWNPAYMENT_LOAN`, `DISBURSALUNDO_LOAN(+_CHECKER)`, `DISBURSALLASTUNDO_LOAN(+_CHECKER)`, `WITHDRAW_LOAN`
**portfolio_group** (2): `READ_GROUP/GROUPNOTE` · **account_transfer/loan_reschedule/portfolio_center** (1 each): READ

## [9] CAJERO (teller/cashier) — 75 permissions
**organisation** (23) + **datatable** (14) + **configuration** (7): READ bundles (products, office, staff, custom tables)
**portfolio** (15): `CREATE_COLLATERAL/GUARANTOR/LOANCHARGE`, `UPDATE_CLIENT`, `UPDATE_LOAN`, + `READ_*` (ADDRESS, CLIENT, CLIENTCHARGE, GUARANTOR, LOAN, PAYMENTTYPE, SAVINGNOTE, SAVINGSACCOUNT, SAVINGSACCOUNTCHARGE, STAFFIMAGE)
**transaction_savings** (7): `DEPOSIT_SAVINGSACCOUNT`, `DEPOSIT_FIXEDDEPOSITACCOUNT`, `DEPOSIT_RECURRINGDEPOSITACCOUNT`, `WITHDRAWAL_SAVINGSACCOUNT`, `WITHDRAWAL_FIXEDDEPOSITACCOUNT`, `WITHDRAWAL_RECURRINGDEPOSITACCOUNT`, `WITHDRAW_FIXEDDEPOSITACCOUNT`
**transaction_loan** (4): `REPAYMENT_LOAN`, `DOWNPAYMENT_LOAN`, `PAY_LOANCHARGE`, `WITHDRAW_LOAN`
**portfolio_group** (2) + account_transfer/loan_reschedule/portfolio_center (1 each): READ
> The **money-movement** role: deposit/withdraw + loan repayment, but **no approve/disburse** and no create-client.

## [10] CAPTURISTA (data-entry maker) — 150 permissions
**portfolio** (150): full CREATE/UPDATE/READ maker surface on client, address, charts, collateral, guarantor, document, familymembers, loan, loancharge, notes, meeting, paymenttype, productmix, savings + fixed/recurring deposit accounts & products, interestratechart, staffimage — with `_CHECKER` twins. **No transaction commands, no approve/disburse** — pure onboarding/origination data entry.

## [11] PROMOTOR (field agent) — 139 permissions
**portfolio** (135): near-identical to CAPTURISTA's CREATE/UPDATE/READ maker surface + `PAY_CLIENTCHARGE`, `RECOVERGUARANTEES_LOAN(+_CHECKER)`, `REAGE/REAMORTIZE_LOAN`
**report** (2): `READ_Active Loans in last installment Summary` (+Pentaho) · **portfolio_center** (1): `READ_CENTER` · **portfolio_group** (1): `READ_GROUP`

## [12] OFICIAL DE CAMPO (loan/field officer) — 149 permissions  ← the plan's field-officer surface
**portfolio** (145): `CREATE_CLIENT(+_CHECKER)`, `CREATE_LOAN(+_CHECKER)`, `CREATE_SAVINGSACCOUNT(+_CHECKER)`, `CREATE_FIXEDDEPOSITACCOUNT`, `CREATE_RECURRINGDEPOSITACCOUNT`, `CREATE_GUARANTOR(+_CHECKER)`, `CREATE_COLLATERAL(+_CHECKER)`, `CREATE_CLIENTIDENTIFIER`, `CREATE_CLIENTNOTE`, `CREATE_DOCUMENT`, `CREATE_MEETING`, `CLOSE_CLIENT(+_CHECKER)`, `REACTIVATE_CLIENT(+_CHECKER)`, `DEPOSIT_GSIMACCOUNT`, `REAGE/REAMORTIZE_LOAN`, `RECOVERGUARANTEES_LOAN(+_CHECKER)`, full `UPDATE_*` on client/loan/savings/collateral/guarantor/deposits, and broad `READ_*`
**report** (2): `READ_Active Loans in last installment Summary` (+Pentaho) · **portfolio_center** (1): `READ_CENTER` · **portfolio_group** (1): `READ_GROUP`
> **Maker only — holds NO `APPROVE_LOAN` / `DISBURSE_LOAN` / `REPAYMENT_LOAN`.** Creates + updates + reads clients, loans, savings, guarantors, collateral; approval & disbursal escalate to REVISOR/TESORERO. This is the exact grant the plan's loan-officer walkthrough assumes (approve/disburse render disabled-with-reason).

## [13] EJECUTIVO (branch officer) — 195 permissions
**portfolio** (98): CREATE/UPDATE/READ on client/loan/savings/deposits + `ATTACH_LOAN_ORIGINATOR`, `FORECLOSURE_LOAN`, `SETFRAUD_LOAN`, `PAY_CLIENTCHARGE`, `DEACTIVATEOVERDUE_LOANCHARGE`
**datatable** (56): **full CRUD** on all custom tables (the only non-super role with datatable write) — CREATE/READ/UPDATE/DELETE across CONDICION, CREDITO_INSTITUCIO_FINANCIERA, DATOS_*, DOMICILIO_*, INSTITUCION_FINANCIERA, etc. + `UPDATE_LIKELIHOOD`
**organisation** (22) + **configuration** (6): READ bundles
**portfolio_group** (6): `CREATE/READ/UPDATE_GROUP(+NOTE)` · **portfolio_center** (3): `CREATE/READ/UPDATE_CENTER`
**account_transfer** (1) + **loan_reschedule** (1): READ · **survey** (1): `REGISTER_SURVEY` · **transaction_loan** (1): `CHARGEOFF_LOAN`

## [14] OFICIAL PLD (AML officer) — 40 permissions
**portfolio** (21): client lifecycle (`ACCEPTTRANSFER(+_CHECKER)`, `ACTIVATE_CLIENT(+_CHECKER)`, `ASSIGNSTAFF_CLIENT`, `CLOSE_CLIENT(+_CHECKER)`, `UPDATE_CLIENT`, `UPDATE_LOANNOTE`) + broad `READ_*`
**configuration** (13): READ of ACCOUNTNUMBERFORMAT, AUDIT, CACHE, CALENDAR, CODE, CODEVALUE, CONFIGURATION, CURRENCY, DATATABLE, EXTERNAL_EVENT_CONFIGURATION, HOOK, REPORT, TWOFACTOR_CONFIGURATION
**authorisation** (4): `READ_PASSWORD_PREFERENCES/PERMISSION/ROLE/USER`
**account_transfer** (1) + **loan_reschedule** (1): READ

## [15] ANALISTA DE PRESTAMOS — 0 permissions
_Empty role — no permissions granted (any user holding only this role can authenticate but see nothing)._
