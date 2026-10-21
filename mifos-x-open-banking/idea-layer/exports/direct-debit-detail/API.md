# API — Direct Debit Detail

Client contract for `direct-debit-detail`. This project owns no backend: these are Ktorfit contracts
against the OBP sandbox, not owned schema.

## `api: []` — this screen makes no network call of its own

**OBP has no direct-debit detail endpoint and no direct-debit cancel endpoint, at any version.**
The originally specified `GET /obp/v5.0.0/.../direct-debit/{directDebitId}` and the matching
`DELETE` were **live-verified 404 and dropped** on 2026-06-11, along with some stray Standing-Order
v7.0.0 entries the file had picked up.

Everything this screen shows is re-derived from data another call already fetched, and its one
mutation is local.

---

## Derived reads

### direct_debit_detail_by_id

```
DirectDebitsRepository.listMandates(bankId, accountId)
    .firstOrNull { it.id == mandateId }
```

Output DTO: `DirectDebitMandate`.

Re-derives the account's mandates using the same `TXN_TYPE=DD` derivation the list screen uses, then
locates this one by id. There is no per-mandate fetch to make.

A `mandateId` that no longer resolves — already cancelled or expired before the screen opened —
renders the **empty** state (`event_busy`, "Mandate not available"), not an error. Nothing failed;
the mandate simply is not there any more.

### linked_account_name

```
AccountsRepository.accountDetail(bankId, accountId)
```

Output DTO: `Account`.

Best-effort lookup of the funding account's display name — label, else type, else the literal
`"Account"`. **Resolution is non-blocking**: a failure still renders the mandate with the fallback
name rather than blocking or erroring the screen. This is why `linkedAccountName` is documented with
a fallback rather than as a guaranteed value.

---

## Local mutation

### cancel_direct_debit_local

```
DirectDebitsRepository.cancel(accountId, mandateId)
```

**This never reaches the server.** OBP has no cancel endpoint, so confirming the dialog records the
cancellation **locally** in the Room JSON cache and re-fetches the mandate: it flips to `CANCELLED`
and the next-payment date clears to an em dash.

The local record **persists across restarts**.

Implementers must not read the confirm dialog as a server call. The customer sees the mandate marked
cancelled; the bank does not know. Anything that depends on the mandate actually being cancelled at
the bank — a collection that still lands next month, say — will contradict this screen, and that gap
is a product decision recorded here, not a bug to patch client-side.

---

## Deferred, deliberately

`GET /direct-debit/{id}` and `DELETE /direct-debit/{id}` were in the original design and **do not
exist on OBP**. There is also **no edit affordance**: direct debits are merchant-initiated, so the
consumer surface is view + (local) cancel only.

Re-add a server cancel **only if OBP ships a DELETE endpoint**. Until then, adding one means calling
a URL that 404s.

---

<!--
Regenerated 2026-08-04 by /idea-feature-export --all --force from screens/direct-debit-detail/api.yaml.

The previous revision of this file documented
`GET /obp/v5.0.0/banks/{bankId}/accounts/{accountId}/direct-debit/{directDebitId}` and the matching
DELETE — complete with path parameters, response fields, a sample response and an error-code table.
Both endpoints were live-verified 404 and removed from api.yaml on 2026-06-11; the export was never
regenerated, so it went on instructing implementers to call URLs that do not exist. api.yaml now
declares `api: []` with derived_reads + local_mutations, and this file reflects that.
-->
