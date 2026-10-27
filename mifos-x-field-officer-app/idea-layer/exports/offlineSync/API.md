<!--
generated_by: /idea-feature-export
generated_at: 2026-10-27
feature_id: offlineSync
sources:
  - screens/offlineSync/api.yaml
  - screens/offlineSync/data-flow.yaml
  - dtos/BatchRequest.yaml
  - dtos/BatchResponse.yaml
-->

# API — Offline sync

The SCREEN reads only local state. These calls are made by the background job (`OfflineSyncWorker`) and
the record picker, over the existing authenticated Ktor client. Every download read is the SAME call — and
goes through the SAME store with the SAME key — that the record's own screen makes. All paths probed live
on the gateway 2026-10-27 (fieldofficer @ apis.mifos.community, tenant mifos-bank-1).

## Picker (3)

| id | Method · path | Permission |
|---|---|---|
| list_centres | `GET centers?officeId&staffId` | READ_CENTER |
| list_groups | `GET groups?officeId&staffId` | READ_GROUP |
| list_clients | `GET clients?officeId&staffId` | READ_CLIENT |

## Download — batched

`POST batches?enclosingTransaction=false`, ≤100 `BatchRequest` rows per call, each answered independently.
**Only these route through the batch API on this gateway:** `loans/{id}?associations=all`,
`loans/{id}?associations=repaymentSchedule`, `datatables/{name}/{appTableId}`. Every other GET answers 501
("Resource … doesn't exist") and is sent as a single call.

## Download — single reads (per record)

| Level | Reads |
|---|---|
| Centre | `centers/{id}?associations=groupMembers,collectionMeetingCalendar` · `centers/{id}/accounts` |
| Group | `groups/{id}?associations=all` (carries clientMembers) · `groups/{id}/accounts` · `groups/{id}/notes` |
| Client | `clients/{id}` · `clients/{id}/accounts` (incl. closed) · `client/{id}/addresses` (**singular** — `clients/…` is 404) · `clients/{id}/identifiers` · `clients/{id}/notes` · `clients/{id}/charges` · `clients/{id}/collaterals` · `clients/{id}/images` (404 = no image, not a failure) · `clients/{id}/documents` + each `…/attachment` |
| Loan | (batched) loan · `loans/{id}/charges` · `loans/{id}/notes` · `rescheduleloans?loanId={id}` · `loans/{id}/documents` · `loans/{id}/transactions/template?command=repayment` (active only) |
| Savings | `savingsaccounts/{id}?associations=transactions,charges` (`=all` is 400) · `savingsaccounts/{id}/transactions/template` (active only) · documents |
| Datatables | `datatables?apptable=m_client\|m_loan\|m_savings_account\|m_group\|m_center` then (batched) each row |
| Once per job | `loanproducts` · `savingsproducts` · `clients/template` · `offices` · `staff?officeId` |

## Errors

A refused read (403 / 404 / 5xx) is recorded on the job with `ServerErrorParser`'s message and the record is
marked `N failed`; it never fails the whole job. All rows of a batch failing surfaces the first as the
job error. Offline → the job waits on its network constraint.

## No writes

Download-only: this feature sends no POST/PUT except the read-only `POST batches`. Offline actions are
drafts, uploaded by Sync & Drafts.
