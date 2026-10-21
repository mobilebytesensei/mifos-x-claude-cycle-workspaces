# API — Statement Detail

Client contracts for `statement-detail`. This project owns no backend: these are Ktorfit contracts
against the HSBC UK/CE sandbox (OBIE Read/Write Standard), not owned schema.
Consumers: `StatementDetailRepository`, `StatementFileRepository`, `StatementFileHandler`.

**Three endpoints requiring three different permissions.** A consent can satisfy one and not the
others, so the screen degrades section by section rather than all-or-nothing.

---

## statement-detail

| | |
|---|---|
| Endpoint | `GET /accounts/{AccountId}/statements/{StatementId}` |
| Permission | **ReadStatementsDetail** |

Returns the single statement record, carrying the `StatementAmount`, `StatementFee` and
`StatementInterest` arrays that populate the three list sections.

The *detail* scope is required for the amounts — the same distinction the `statements` list screen
depends on. `ReadStatements` alone returns the periods without them.

Failure → `StatementNotFound` or `ConsentMissingReadStatements`.

---

## statement-txns

| | |
|---|---|
| Endpoint | `GET /accounts/{AccountId}/statements/{StatementId}/transactions` |
| Permission | **ReadTransactions** — *in addition to* `ReadStatementsDetail` |

Returns the transactions booked within the statement period.

This is the second permission, and it is a genuinely separate grant. A consent can permit statement
records and refuse transaction reads, in which case the header, balances, fees and interest all
render and only the transactions section is unavailable.

An empty result renders `empty_txns_state` **inside** the loaded statement — a period with no
transactions is still a valid statement.

---

## statement-file

| | |
|---|---|
| Endpoint | `GET /accounts/{AccountId}/statements/{StatementId}/file` |
| Permission | **ReadStatements** |
| Produces | `application/pdf` binary stream |

**Not JSON — there is no DTO mapping.** The response is a binary stream handed to the native
share/save sheet via `StatementFileHandler`. That is why the file path has its own repository
(`StatementFileRepository`) rather than going through the JSON client.

Tracked in `downloadState`, separate from `uiState`, so a download never replaces the statement on
screen. Outcome surfaces through `download_result_snackbar`.

`StatementFileNotFound` is a distinct error type from `StatementNotFound`: the record can be
perfectly readable while its PDF is unavailable, and in that case only the download should fail.

Note the sibling behaviour on the `statements` list screen: the HSBC sandbox returns **501 Not
Implemented** for statement files on some account types, modelled there as
`StatementDownloadUnsupportedError` and deliberately never auto-retried. The same refusal is
possible here.

---

## Permission summary

| Endpoint         | Permission             | If absent                                  |
|------------------|------------------------|--------------------------------------------|
| statement-detail | `ReadStatementsDetail` | Screen cannot load — `ConsentMissingReadStatements` |
| statement-txns   | `ReadTransactions`     | Transactions section unavailable; rest renders |
| statement-file   | `ReadStatements`       | Download unavailable; statement still readable |

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/statement-detail/api.yaml. -->
