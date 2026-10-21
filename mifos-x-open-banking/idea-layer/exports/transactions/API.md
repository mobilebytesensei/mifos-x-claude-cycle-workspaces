# API — Transactions

Client contract for `transactions`. This project owns no backend: this is a Ktorfit contract against
the HSBC UK/CE sandbox (OBIE Read/Write Standard), not owned schema.
Consumer: `TransactionsRepository`.

---

## transactions

| | |
|---|---|
| Endpoint | `GET /accounts/{AccountId}/transactions` |
| Permission | `ReadTransactionsDetail` |

Returns **booked and pending** transactions for the account within the optional date range.

Pending entries are included and rendered here with `tx_pending_badge`. That is the difference from
`home`, which slices to five Booked transactions only — a pending amount beside a balance invites
reconciling two numbers that are not meant to agree, whereas a labelled row in a full list is
informative.

---

## Pagination — `Links.Next` cursor

OBIE-standard cursor pagination, not page numbers.

The client stores `Links.Next` from each response as `next_link` state and presents Load More while
it is non-null. `hasNextPage` mirrors that, and `isPaginating` tracks the in-flight append —
separate fields so an append never blanks the list being read.

**A date-range change resets the cursor** and triggers a fresh first page. It cannot do otherwise:
the cursor encodes a position in the previous result set, so reusing it across a different range
would page through the wrong sequence.

---

## What is server-side vs client-side

| Operation           | Where       | Note                                              |
|---------------------|-------------|----------------------------------------------------|
| Date range          | **server**  | Sent as request params; resets pagination         |
| Pagination          | **server**  | `Links.Next` cursor                               |
| Credit/debit filter | **client**  | Applied to the accumulated in-memory list         |
| Text search         | **client**  | Applied to the accumulated in-memory list         |

This split has a consequence worth stating plainly: **filter and search only see what has been
paged in.** A match on an unloaded page will not appear until Load More reaches it. Narrowing by
date range — which *is* server-side — is the reliable way to find something older, and that is why
the date-range chip sits alongside search rather than being buried.

It is also why `empty_transactions` offers Clear Filters: an empty result is more often a
client-side filter over a short loaded window than a genuine absence.

---

## Errors

Failures resolve to `TransactionsUiState.Error`, which renders a status chip, a **consent hint** and
Retry.

The consent hint is there because the most common failure on this screen is a scope problem rather
than a network one: `ReadTransactionsDetail` is a distinct permission, and a consent granted without
it refuses this call identically on every retry. Naming that possibility in the error surface is the
difference between a customer retrying forever and a customer re-consenting.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/transactions/api.yaml. -->
