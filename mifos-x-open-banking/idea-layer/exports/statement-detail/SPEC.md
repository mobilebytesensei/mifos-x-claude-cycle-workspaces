# SPEC — Statement Detail

| Field         | Value                        |
|---------------|------------------------------|
| Feature       | statement-detail             |
| Flavor        | consumer                     |
| Status        | approved                     |
| Quality Score | 95                           |
| ViewModel     | StatementDetailViewModel     |
| Archetype     | detail_screen                |

---

## Overview

One statement period in full: header, balances, fees, interest, the transactions booked within the
period, and a PDF download.

It is the app's only screen requiring **three permissions at once** — `ReadStatementsDetail` for the
record, `ReadTransactions` for the period's transactions, and `ReadStatements` for the file. A
consent can satisfy one and not the others, which is why `ConsentMissingReadStatements` is a named
error type rather than a generic refusal.

The download is tracked as `downloadState` on the state object, separate from `uiState`. The PDF is
a **binary stream, not JSON** — there is no DTO to map; the client hands it to the native
share/save sheet. A failed download therefore surfaces as a snackbar and leaves the statement on
screen, since the content the customer is reading is unaffected.

---

## Screens

| ID               | Name             | ViewModel                | Archetype     |
|------------------|------------------|--------------------------|---------------|
| statement-detail | Statement Detail | StatementDetailViewModel | detail_screen |

---

## Components

| ID                       | Type            | Description                                     |
|--------------------------|-----------------|--------------------------------------------------|
| statement_header_card    | card            | Statement identity                               |
| └ statement_reference    | text            | `{statement.StatementReference}`                 |
| └ statement_period       | text            | Start–end of the period                          |
| └ statement_type         | text            | `{statement.Type}`                               |
| └ statement_created      | text            | Creation timestamp                               |
| balances_header          | section_header  | Balances section                                 |
| balances_list            | list            | `StatementAmount` entries                        |
| └ balance_row            | list_item       | One balance line                                 |
| fees_header              | section_header  | Fees section                                     |
| fees_list                | list            | `StatementFee` entries                           |
| └ fee_row                | list_item       | One fee line                                     |
| interest_header          | section_header  | Interest section                                 |
| interest_list            | list            | `StatementInterest` entries                      |
| └ interest_row           | list_item       | One interest line                                |
| transactions_header      | section_header  | Transactions section                             |
| statement_txns_list      | list            | Transactions booked in the period                |
| └ statement_txn_row      | list_item       | One transaction — opens transaction-detail       |
| empty_txns_state         | empty_state     | No transactions in the period                    |
| download_pdf_button      | button          | `DownloadPdf`                                    |
| download_progress        | progress_linear | `downloadState` in flight                        |
| download_result_snackbar | snackbar        | Download outcome — success or failure            |
| error_state              | error_state     | Load failure — `role: alert`                     |
| └ retry_button           | button          | `RetryLoad`                                      |

`empty_txns_state` sits **inside** a loaded statement — a period with no transactions is still a
valid statement with balances and fees, so the emptiness is scoped to that section.

---

## States

Initial state: `loading`. Four states, matching `StatementDetailUiState` one-for-one.

| State   | Rendering                                                     |
|---------|----------------------------------------------------------------|
| loading | Fetching the statement record                                 |
| content | Header, balances, fees, interest, transactions, download      |
| empty   | Statement resolved with nothing renderable                    |
| error   | `error_state` + retry                                         |

Download progress is **not** a state — it is `downloadState`, so fetching a PDF never replaces the
statement the customer is reading.

---

## State Model

**ViewModel:** `StatementDetailViewModel`.

**State:** `StatementDetailState` — `uiState: StatementDetailUiState`, `downloadState: DownloadState`.

**Screen state:** sealed `StatementDetailUiState` — `Loading`, `Content`, `Empty`, `Error`.

**Error types**

| Type                            | Cause                                          |
|---------------------------------|------------------------------------------------|
| `StatementNotFound`             | Statement id does not resolve                  |
| `ConsentMissingReadStatements`  | Consent lacks the statements scope             |
| `SessionExpired`                | PSU token expired                              |
| `StatementFileNotFound`         | Record exists, **file does not**               |
| `NetworkError`                  | Offline / transport                            |

`StatementFileNotFound` is distinct from `StatementNotFound` on purpose: the statement can be
readable while its PDF is unavailable, and only the download should fail in that case.

**Actions:** `RetryLoad`, `DownloadPdf`.

**Nav callbacks:** `onBack -> popBackStack()` ·
`onNavigateToTransactionDetail(transactionId, accountId) -> TransactionDetailRoute(...)`.

**DI:** `SavedStateHandle`, `StatementDetailRepository`, `StatementFileRepository`,
`StatementFileHandler` — the file path has its own repository and handler because it deals in binary
rather than JSON.

---

## Navigation

| From             | To                 | Trigger                | Type |
|------------------|--------------------|------------------------|------|
| statement-detail | transaction-detail | `statement_txn_row`    | push |
| statement-detail | statements         | `onBack`               | pop  |

---

## API Endpoints

| ID               | Endpoint                                                          | Permission               |
|------------------|-------------------------------------------------------------------|--------------------------|
| statement-detail | `GET /accounts/{AccountId}/statements/{StatementId}`              | `ReadStatementsDetail`   |
| statement-txns   | `GET /accounts/{AccountId}/statements/{StatementId}/transactions` | `ReadTransactions` (+ above) |
| statement-file   | `GET /accounts/{AccountId}/statements/{StatementId}/file`         | `ReadStatements`         |

Three endpoints, three permissions. Full detail: `API.md`.

---

## Design Tokens

Material 3, seed `#266489` ("Open Banking — Trust Blue"), Roboto, with `Roboto Mono` for balance,
fee and interest figures so amounts align across the three lists. Components reference semantic
roles, so both theme modes resolve from `design-system/design-tokens.yaml`; `DESIGN.md` is the
canonical brand spec.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/statement-detail/{ui,api,flow,docs}.yaml. -->
