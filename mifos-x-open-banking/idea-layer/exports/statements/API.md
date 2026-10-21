# API — Statements

Client contracts for `statements`. This project owns no backend: these are Ktorfit contracts
against the HSBC UK/CE sandbox (OBIE Read/Write Standard), not owned schema.
Consumer: `StatementsRepository`.

---

## statements

| | |
|---|---|
| Endpoint | `GET /accounts/{AccountId}/statements` |
| Response DTO | `StatementPeriod` |
| Permission | **ReadStatementsDetail** |

Returns all statement periods for the account.

The permission matters: `ReadStatementsDetail` is what causes each `OBStatement2` record to include
`StatementAmount` — `OpeningBalance` and `ClosingBalance`. The narrower `ReadStatements` scope
returns the periods without those amounts, which would leave the list rows unable to show a
balance. If a consent was granted with only `ReadStatements`, this screen degrades rather than
fails, and the mismatch presents as `ConsentScopeError`.

Mapped to `List<StatementRowUiModel>` for the list; failures resolve to `StatementsUiState.Error`
with `retry_button` → `RetryLoad`.

---

## statement_file

| | |
|---|---|
| Endpoint | `GET /accounts/{AccountId}/statements/{StatementId}/file` |
| Returns | The statement document as PDF or CSV |
| Trigger | `download_statement_button` on a row → `DownloadStatement` |

Per-row, not per-screen: progress and failure are tracked in
`downloadState: Map<String, DownloadState>` keyed by statement id, so several downloads can be in
flight simultaneously and a failure affects only its own row.

**501 Not Implemented — the designed case**

The HSBC sandbox returns 501 for statement files on certain account types. Handling:

- surfaced as the `statements.download.toast_unavailable` toast
- modelled as its own error type, `StatementDownloadUnsupportedError`
- **not retried automatically**

The distinct error type exists so this is treated as a capability the account lacks, rather than a
transient fault. Auto-retrying an unsupported operation would loop against a response that will
never change.

---

## Error types

| Type                                | Cause                                    | Surface                          |
|-------------------------------------|------------------------------------------|----------------------------------|
| `TokenExpiredError`                 | PSU token expired                        | Error state → re-auth path       |
| `ConsentScopeError`                 | Consent lacks ReadStatementsDetail       | Error state — the balances cannot be read |
| `RateLimitedError`                  | Bank throttling                          | Error state, retry               |
| `StatementDownloadUnsupportedError` | 501 on `statement_file`                  | Per-row toast, **no auto-retry** |
| `NetworkError`                      | Offline / transport                      | Error state, retry               |

Only the four list-level types can put the screen in `Error`. The download-unsupported type is
row-scoped by construction — it never blanks a loaded list.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/statements/api.yaml. -->
