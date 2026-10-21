# SPEC — Statements

| Field         | Value                 |
|---------------|-----------------------|
| Feature       | statements            |
| Flavor        | consumer              |
| Status        | approved              |
| Quality Score | 97                    |
| ViewModel     | StatementsViewModel   |
| Archetype     | index_list            |

---

## Overview

A list of an account's statement periods, each row offering a document download. It is an
account-scoped index: the `AccountId` arrives via `SavedStateHandle`, and rows open
`statement-detail`.

The download is modelled as **per-row state**, not screen state — `downloadState` is a
`Map<String, DownloadState>` keyed by statement id, so several rows can be downloading, failed or
idle at once without the screen entering a global busy state.

One sandbox behaviour is designed for explicitly: the HSBC sandbox returns **501 Not Implemented**
for statement files on certain account types. That surfaces as a toast and is deliberately **not
retried automatically** — retrying an unsupported operation would loop.

---

## Screens

| ID         | Name       | ViewModel           | Archetype  |
|------------|------------|---------------------|------------|
| statements | Statements | StatementsViewModel | index_list |

**Shell:** top app bar visible, title `{strings.statements.screen_title}`, `back` leading icon.
Bottom navigation visible. No FAB.

---

## Components

| ID                        | Type        | Description                                                    |
|---------------------------|-------------|-----------------------------------------------------------------|
| statements_skeleton       | skeleton    | Loading placeholder mirroring the row layout                    |
| statements_list           | list        | Semantic list of statement periods                              |
| └ statement_row           | list_item   | One statement period — opens `statement-detail`                 |
| &nbsp;&nbsp;└ download_statement_button | icon_button | Per-row download; its state comes from `downloadState[id]` |
| statement_row_divider     | divider     | Row separator                                                   |
| empty_statements          | empty_state | No statements published for this account                        |
| error_state               | error_state | Load failure — `role: alert`, with retry                        |
| └ retry_button            | button      | `{strings.statements.retry.label}` → `RetryLoad`                |

`error_state` is the registry's dedicated error type (assertive `alert` role), not an `empty_state`
styled red — the two are deliberately distinct here.

---

## States

`StatementsUiState` is a sealed class with exactly four members, and the declared state list matches
it one-for-one.

| State   | Rendering                                                    |
|---------|--------------------------------------------------------------|
| loading | `statements_skeleton`                                        |
| content | `statements_list` with `statement_row` per period            |
| empty   | `empty_statements`                                           |
| error   | `error_state` + `retry_button`                               |

Download failures do **not** appear here — they live in `downloadState` per row and surface as
toasts, so a failed download never blanks a loaded list.

---

## State Model

**ViewModel:** `StatementsViewModel`.

**State:** `StatementsState`

| Field           | Type                          | Initial      |
|-----------------|-------------------------------|--------------|
| `uiState`       | `StatementsUiState`           | `Loading`    |
| `downloadState` | `Map<String, DownloadState>`  | `emptyMap()` |

**Screen state:** sealed `StatementsUiState` — `Loading`, `Content`, `Empty`, `Error`.

**Additional state fields:** `statements: List<StatementRowUiModel>`, `downloadState`.

**Actions:** `RetryLoad`, `DownloadStatement`.

**Error types:** `TokenExpiredError`, `ConsentScopeError`, `RateLimitedError`,
`StatementDownloadUnsupportedError`, `NetworkError`.

`StatementDownloadUnsupportedError` is the modelled form of the sandbox 501 — a distinct type
precisely so it can be handled as "this account cannot do this" rather than as a transient failure.

**Nav callbacks:** `onBack -> popBackStack()` ·
`onNavigateToStatementDetail(statementId, accountId) -> StatementDetailRoute(...)`.

**DI:** `SavedStateHandle`, `StatementsRepository`, and the statement-download collaborator.

---

## Navigation

| From       | To               | Trigger                                   | Type |
|------------|------------------|-------------------------------------------|------|
| statements | statement-detail | `statement_row` tap (statementId, accountId) | push |
| statements | (previous)       | `onBack` → `popBackStack()`               | pop  |

Both destinations are passed explicit ids — the detail screen is account-scoped, not resolved from
ambient selection.

---

## API Endpoints

| ID             | Endpoint                                                  | Response DTO      |
|----------------|-----------------------------------------------------------|-------------------|
| statements     | `GET /accounts/{AccountId}/statements`                    | `StatementPeriod` |
| statement_file | `GET /accounts/{AccountId}/statements/{StatementId}/file` | binary (PDF/CSV)  |

`statements` uses the **ReadStatementsDetail** permission so each `OBStatement2` record includes
`StatementAmount` (OpeningBalance, ClosingBalance). Note this is the *detail* scope — the
list-level `ReadStatements` scope would omit those amounts.

Full detail including the 501 handling: `API.md`.

---

## Design Tokens

Material 3, seed `#266489` ("Open Banking — Trust Blue"), Roboto, with `Roboto Mono` for balance
figures so amounts align down the list. Components reference semantic roles, so both theme modes
resolve from `design-system/design-tokens.yaml`; `DESIGN.md` is the canonical brand spec.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/statements/{ui,api,flow,docs}.yaml. -->
