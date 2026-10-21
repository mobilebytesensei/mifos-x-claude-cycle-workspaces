# API — Standing Order Detail

Client contract for `standing-order-detail`. This project owns no backend: these are Ktorfit
contracts against the OBP sandbox, not owned schema.

## `api: []` — this screen makes no network call of its own

**OBP has no standing-order detail, pause, resume or delete endpoint at any version.** The
originally specified `GET /standing-orders/{id}`, `POST .../pause`, `POST .../resume` and
`DELETE .../{id}` were all **live-verified 404** and dropped on 2026-06-11.

Everything shown here is re-derived from data the list screen already fetched.

---

## Derived reads

### standing_order_detail_by_series

```
StandingOrdersRepository.detail(bankId, accountId, standingOrderId)
```

Output DTO: `StandingOrderDetail`.

Finds the order by **series id** within the derived/created set — the same `TXN_TYPE=SO` derivation
the list uses — and builds the detail from it.

An unknown id fails to the **error** state ("Standing Order Not Found"), not to empty. This differs
from `direct-debit-detail`, where an unresolvable mandate renders empty; here an id that does not
resolve is treated as a lookup failure.

### standing_order_executions

```
deriveExecutions(transactions, standingOrderId)
```

Output DTO: `List<StandingOrderExecution>`.

Filter: `TXN_TYPE=SO` transactions of that series, **newest first, capped at 5**.

Each `StandingOrderExecution` carries a `transactionId`, which is what makes the history rows
drillable into `transaction-detail`. Without it the executions would be display-only.

The cap is why the card is titled "RECENT EXECUTIONS" rather than presenting itself as a full
history.

---

## Deferred — pause, resume, cancel

`POST .../pause`, `POST .../resume` and `DELETE .../{id}` **do not exist on OBP**.

The screen still shows `sod_pause_resume_button` and `sod_cancel_button`, and they surface
**"coming soon" snackbars**. There is deliberately **no delete dialog** — offering a confirmation
step for an action that cannot be performed would be worse than the snackbar, because it implies the
operation is real and merely needs confirming.

Note the contrast with `direct-debit-detail`, which has no cancel endpoint either but records
cancellation **locally**. Standing orders do not take that route: nothing is written, and the
buttons are honest about being unavailable.

Re-add these only if OBP ships the endpoints.

---

<!--
Regenerated 2026-08-04 by /idea-feature-export --all --force from screens/standing-order-detail/api.yaml.

The previous revision documented four endpoints — GET the standing order, POST pause, POST resume,
and DELETE — with auth notes and response shapes. All four were live-verified 404 and removed from
api.yaml on 2026-06-11; the export was never regenerated, so it went on describing an API surface
that does not exist. api.yaml now declares `api: []` with derived_reads + a deferred block, and this
file reflects that. This is the same drift class found in exports/direct-debit-detail/API.md.
-->
