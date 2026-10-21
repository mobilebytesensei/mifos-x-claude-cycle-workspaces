# TEST SPEC — Payment Status

| Field      | Value                               |
|------------|-------------------------------------|
| Feature    | payment-status                      |
| Source     | `screens/payment-status/tests.yaml` |
| Scenarios  | 9                                   |
| Priorities | p0 3 · p1 5 · p2 1                  |
| States     | content 7 · error 1 · loading 1     |
| Module     | *not yet created* — `status: enriched`, spec ahead of source |

---

## Coverage

Contiguous ids; all three declared states covered. TC-PSTAT-009 closed the `loading` gap on
2026-08-02 as part of ST-1 — before it, the state was declared and untested.

Seven of nine scenarios sit in `content`, which looks lopsided until you see what they cover: this
screen has one layout and **five dispositions**, and almost every scenario is about mapping an
OBIE status onto the right one.

---

## Author's coverage notes (carried verbatim from `tests.yaml#coverage_notes`)

**Truthfulness** — TC-PSTAT-002 and TC-PSTAT-003 are the guard for this screen's whole reason to
exist. A successful submit returns `AcceptedSettlementInProcess`, so the tempting simplification —
treat any `Accepted*` prefix as success — would tell a PSU their money had moved when it had not.
These two tests make that regression fail loudly.

**Polling hygiene** — TC-PSTAT-004 and TC-PSTAT-005 pin that polling is bounded by disposition, not
by a timer. Polling a terminal status is how a client earns a 429 for no information gain.

**Fail open** — TC-PSTAT-006 encodes the deliberate choice to treat an unknown status as
still-working. Guessing success on an unmapped code is the worst available failure mode.

---

## The disposition map, as the scenarios pin it

| OBIE status | disposition | chip | refresh | in-progress note |
|---|---|---|---|---|
| `AcceptedSettlementInProcess` | `in_progress` | progress | — | visible |
| `AcceptedSettlementCompleted` | `terminal_success` | success | **hidden** | hidden |
| `Rejected` | `terminal_failure` | — | **hidden** | — |
| `AcceptedTechnicalValidation` (unmapped) | `in_progress` | neither success nor failure | — | — |

The two hidden refresh buttons are the same rule stated twice: a terminal status cannot change, so
offering a refresh invites the customer to keep checking something that will never move.

---

## TC-PSTAT-001 — Payment resource loads and renders the echoed Initiation

**Priority:** p0 · **State:** content

- **Given** `GET /domestic-payments/PMT-812774903-01` returns `AcceptedSettlementInProcess`
- **When** Screen mounts with `paymentId=PMT-812774903-01`
- **Then**
  - Amount renders as £850.00
  - Payee renders as Jameson Lettings
  - Reference renders as RENT-FLAT12
  - Funding account renders from `Data.Initiation.DebtorAccount`
  - Submitted-at renders from `Data.CreationDateTime`

Everything here comes from the **echoed** `Initiation` block on the payment resource, not from the
local form the customer filled in. That is the point: the screen shows what the bank recorded, so
a divergence between what was submitted and what was accepted is visible rather than masked by
local state.

---

## TC-PSTAT-002 — An in-progress payment is NEVER described as sent or complete

**Priority:** p0 · **State:** content

- **Given** Status is `AcceptedSettlementInProcess`
- **When** The content state renders
- **Then**
  - `disposition` is `in_progress`
  - Status chip uses the **progress** variant, not the success variant
  - In-progress note visible, explaining the money has not moved yet
  - **No visible string asserts the payment is sent, complete, or successful**

The last assertion is unusually broad — it constrains all copy on the screen, not one component —
and deliberately so. There are many ways to imply success (a tick, "Done", "£850.00 sent") and
only the blanket form catches them.

---

## TC-PSTAT-003 — Only a settled status renders as terminal success

**Priority:** p0 · **State:** content

- **Given** Status is `AcceptedSettlementCompleted`
- **When** The content state renders
- **Then**
  - `disposition` is `terminal_success`
  - Status chip uses the success variant
  - In-progress note **NOT** visible
  - Refresh button **NOT** visible — a terminal status cannot change

---

## TC-PSTAT-004 — Polling stops the moment a terminal disposition arrives

**Priority:** p1 · **State:** content

- **Given** The read sequence is in-process, in-process, settled
- **When** The auto-poll runs
- **Then**
  - **Exactly three reads** are made
  - **Zero** further reads occur after the settled response

---

## TC-PSTAT-005 — Polling never starts when the first read is already terminal

**Priority:** p1 · **State:** content

- **Given** The first read returns `AcceptedSettlementCompleted`
- **When** Screen mounts
- **Then**
  - **Exactly one read** is made
  - No poll timer is started

Paired with 004, this pins that the poll is gated on disposition *before* it starts, not merely
cancelled after the first tick. "No timer started" and "no second read" are different
implementations, and only one of them survives a backgrounded app.

---

## TC-PSTAT-006 — An unrecognised status fails open to in_progress

**Priority:** p1 · **State:** content

- **Given** Status is `AcceptedTechnicalValidation`, outside the mapped vocabulary
- **When** The content state renders
- **Then**
  - `disposition` is `in_progress`
  - Polling continues
  - The status is **NOT** rendered as either success or failure

OBIE's status vocabulary is larger than any client maps, and it grows. The failure this prevents
is not a crash — it is a screen confidently reporting an outcome it did not understand.

---

## TC-PSTAT-007 — A rejected payment offers a fresh payment, not a retry

**Priority:** p1 · **State:** content

- **Given** Status is `Rejected`
- **When** The content state renders
- **Then**
  - `disposition` is `terminal_failure`
  - New payment button visible, routes to send-money with a **cleared** form
  - Refresh button **NOT** visible
  - **No affordance resubmits against the rejected consent**

The distinction between "new payment" and "retry" is the whole scenario. A rejected domestic
payment consent is spent — resubmitting against it fails — so the only honest offer is a fresh
instruction. The cleared form is part of that: a pre-filled form is a retry wearing a new label.

---

## TC-PSTAT-008 — A not-found payment is terminal and gets no Retry

**Priority:** p2 · **State:** error

- **Given** The read returns 400 `U011` "Resource cannot be found"
- **When** Screen mounts with an unknown `paymentId`
- **Then**
  - Error state renders with the `PaymentNotFound` message
  - Retry button **NOT** visible — the resource does not exist, so retrying cannot help

Note OBIE returns this as a **400**, not a 404, which is why the code (`U011`) rather than the
status class is what the mapping keys on.

---

## TC-PSTAT-009 — Circular loading indicator while the initial read is in flight

**Priority:** p1 · **State:** loading

- **Given** `GET /domestic-payments/{DomesticPaymentId}` has not yet responded
- **When** Screen mounts with `paymentId=PMT-812774903-01` and the read is in flight
- **Then**
  - Circular progress indicator visible
  - Its accessibility label matches `{strings.payment_status.loading_label}`
  - Status chip **NOT** visible — no content has arrived yet
  - Payment summary card **NOT** visible
  - Error state **NOT** visible

The hidden status chip is the assertion that matters. A chip rendered before its status arrives
has to default to something, and every default on this screen is a claim about the customer's
money.

---

_Generated by /idea-feature-test-export | 2026-08-03_
