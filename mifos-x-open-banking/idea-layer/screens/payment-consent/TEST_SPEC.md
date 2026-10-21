# TEST SPEC — Payment Consent (PISP authorisation return)

| Field      | Value                                |
|------------|--------------------------------------|
| Feature    | payment-consent                      |
| Source     | `screens/payment-consent/tests.yaml` |
| Scenarios  | 11                                   |
| Priorities | p0 5 · p1 6                          |
| States     | error 6 · authorised 2 · validating 1 · exchanging 1 · checking 1 |
| Module     | *not yet created* — `status: enriched`, spec ahead of source |

---

## Coverage

Contiguous ids; all five declared states covered. Three of them — `validating`, `exchanging`,
`checking` — were untested until `/idea-sync` closed ST-1 on 2026-08-02; TC-PCON-009/010/011 are
that closure, and they are why this screen now has no untested declared state.

Six of eleven scenarios are error paths. That ratio is right for what this screen is: it does not
render data, it adjudicates a redirect return. Every way that adjudication can fail is a way a
customer's money either moves when it should not, or fails to move with no route back.

---

## Author's coverage notes (carried verbatim from `tests.yaml#coverage_notes`)

**Ordering** — TC-PCON-002 and TC-PCON-004 pin the guard ordering. Validating before exchanging
matters because an authorisation code is single-use with a very short TTL; spending it on a request
that was going to be rejected anyway destroys the PSU's only recovery path.

**Token isolation** — TC-PCON-007 is the guard for the single most damaging mistake available here:
reusing the shipped consent-callback's token persistence would overwrite the AIS session token and
silently conflate a one-payment authorisation with a data-sharing session.

**Terminal vs retryable** — TC-PCON-006 pins that a PSU decline is terminal. Offering Restart after
an explicit decline would nag the PSU to re-approve something they just refused.

---

## The Restart button is the screen's real contract

Four error scenarios differ only in whether "Restart authorisation" appears, and the split is not
about severity — it is about whether restarting could possibly help:

| Scenario | Failure | Restart offered |
|----------|---------|-----------------|
| TC-PCON-002 | state mismatch | **no** (Abandon only) |
| TC-PCON-005 | code expired (400 `invalid_grant`) | yes |
| TC-PCON-006 | PSU declined at the bank (`RJCT`) | **no** |
| TC-PCON-008 | poll deadline elapsed while `AWAU` | yes |

002 withholds it because a mismatched `state` may be an attack, not a mishap. 006 withholds it
because the PSU already answered. The two `yes` rows are both timing failures, where the customer
did nothing wrong and a second attempt is the correct offer.

---

## TC-PCON-001 — Happy path: redirect validates, code exchanges, consent reaches AUTH

**Priority:** p0 · **State:** authorised

- **Given** `PendingAuthStore` holds `consentId 812774903` with state `st1785412953` and nonce `nnc1785412953`
- **When** The redirect arrives with a matching state and a valid code, and the consent poll returns AUTH on the third read
- **Then**
  - `PendingAuthStore.consume()` is called **exactly once**
  - `POST /oauth2/token` sent with `grant_type=authorization_code` and a `private_key_jwt` client assertion
  - `GET /domestic-payment-consents/812774903` polled until `Data.Status == AUTH`
  - `PaymentConsentEvent.Authorised` emitted carrying `consentId` and the payments-scope token
  - The `authorised` state renders

"Exactly once" on `consume()` is the assertion to keep. A second consume returns null and drops
the flow into TC-PCON-004's no-pending-authorisation error — after a successful payment
authorisation.

"On the third read" is deliberate too: the happy path is polled, not immediate, so an
implementation that only handles a first-read AUTH passes nothing here.

---

## TC-PCON-002 — State mismatch rejected before any token exchange

**Priority:** p0 · **State:** error

- **Given** `PendingAuthStore` holds state `st1785412953`
- **When** The redirect arrives with state `st0000000000`
- **Then**
  - Error state renders with the `StateMismatch` message
  - `POST /oauth2/token` is **NEVER** sent — the guard runs before the exchange
  - No Restart authorisation button; only Abandon

---

## TC-PCON-003 — Nonce mismatch in the id_token rejected after exchange

**Priority:** p1 · **State:** error

- **Given** State matches but the returned `id_token` carries a different nonce
- **When** The redirect is handled
- **Then**
  - Error state renders with the `StateMismatch` message
  - The consent status is **NOT** polled

The nonce check necessarily runs *after* the exchange — the `id_token` does not exist until the
token endpoint returns it. So this guard cannot protect the code the way TC-PCON-002 does; what it
protects is everything downstream, which is why the poll must not fire.

---

## TC-PCON-004 — Missing pending authorisation (app restarted mid-flow)

**Priority:** p1 · **State:** error

- **Given** `PendingAuthStore.consume()` returns null because the process was killed during authorisation
- **When** The redirect arrives
- **Then**
  - Error state renders with the `NoPendingAuthorisation` message
  - **No network call of any kind is made**

The app-to-app redirect makes process death a routine event, not an edge case. This is the
receiving half of the invariant login asserts on the way out (TC-LOGIN-005, persist before
redirect).

---

## TC-PCON-005 — Expired authorisation code offers Restart

**Priority:** p0 · **State:** error

- **Given** The code is older than its 30–60s TTL; the token endpoint returns 400 `invalid_grant`
- **When** The code exchange runs
- **Then**
  - Error state renders with the `CodeExpired` message
  - Restart authorisation button visible
  - Tapping it emits `RestartAuthorisation` and returns to send-money

---

## TC-PCON-006 — PSU declined at the bank; RJCT is terminal, not retryable

**Priority:** p0 · **State:** error

- **Given** The consent poll returns `Data.Status RJCT`
- **When** The poll completes
- **Then**
  - Error state renders with the `ConsentRejected` message
  - Restart authorisation button **NOT** visible — the PSU made a deliberate choice
  - Abandon button visible

---

## TC-PCON-007 — The payments-scope token is never written to ConsentSession

**Priority:** p0 · **State:** authorised

- **Given** A successful token exchange returns a payments-scope access token
- **When** The authorisation completes
- **Then**
  - **Zero writes** are made to `ConsentSession`
  - `ConsentSession.isActive()` and `consentId()` unchanged from before the payment
  - The token is carried only on the emitted `Authorised` event

Asserted as *zero writes* rather than "the value is unchanged" — a write-then-restore would pass
the weaker check while leaving a window where the AIS session pointed at a payment consent.

The temptation this guards against is concrete: consent-callback (the AIS screen) already ships
working token persistence, and reusing it here is the obvious shortcut. It would give a
single-payment authorisation the lifetime of a 90-day data-sharing session.

---

## TC-PCON-008 — Poll deadline elapsing while AWAU yields a timeout, not a hang

**Priority:** p1 · **State:** error

- **Given** The consent stays `AWAU` for longer than the 45000 ms deadline
- **When** The poll runs to its deadline
- **Then**
  - Error state renders with the `AuthorisationTimedOut` message
  - Restart authorisation button visible
  - "Check again" remains available during the `checking` state before the deadline

A pending payment authorisation with no deadline is the worst failure available on this screen —
the customer cannot tell whether their money moved.

---

## TC-PCON-009 — Validating state entered on mount, before any network call

**Priority:** p1 · **State:** validating

- **Given** `PendingAuthStore` holds a pending authorisation (state, nonce, `consentId 812774903`); the redirect has arrived and on-mount handling has begun
- **When** The state-nonce guard has not yet completed
- **Then**
  - `authorising_indicator` visible (accessibility label `{strings.payment_consent.progress_label}`)
  - `progress_detail` text visible (`{strings.payment_consent.progress_detail}`)
  - **`POST /oauth2/token` has NOT been called** — the guard must pass before the code is spent
  - `GET /domestic-payment-consents/812774903` has NOT been called
  - `check_again_button` NOT visible — its `state_binding` is `[checking]` only

---

## TC-PCON-010 — Exchanging state held while the token POST is in flight

**Priority:** p1 · **State:** exchanging

- **Given** `PendingAuthStore` validated successfully; `POST /oauth2/token` in progress, no token returned yet
- **When** The code exchange is running
- **Then**
  - `authorising_indicator` remains visible (`{strings.payment_consent.progress_label}`)
  - `progress_detail` text visible (`{strings.payment_consent.progress_detail}`)
  - `check_again_button` NOT visible — `state_binding` is `[checking]`, not `[exchanging]`
  - `GET /domestic-payment-consents/{ConsentId}` has NOT been called — the poll is gated on the `id_token` nonce guard, which runs after the exchange returns

009 and 010 render identically to the customer, and that is intentional: three internal stages
behind one steady progress surface. What separates them is what has been *called*, which is why
both scenarios lead with negative network assertions rather than visual ones.

---

## TC-PCON-011 — Checking state exposes check_again so a late-returning PSU can advance

**Priority:** p1 · **State:** checking

- **Given** State validation passed, token exchange succeeded, and the first automatic `GET /domestic-payment-consents/{ConsentId}` poll returned `AWAU`
- **When** The screen enters `checking` with the automatic poll still running
- **Then**
  - `authorising_indicator` visible (`{strings.payment_consent.progress_label}`)
  - `progress_detail` text visible (`{strings.payment_consent.progress_detail}`)
  - `check_again_button` visible with label `{strings.payment_consent.check_again}`
  - Tapping it triggers a fresh `GET /domestic-payment-consents/{ConsentId}` and keeps the screen in `checking`
  - The button was **NOT** visible during `validating` or `exchanging` — it appears uniquely in this state

The last assertion closes the loop across 009, 010 and 011: the button's absence is asserted twice
and its presence once, so `state_binding: [checking]` is pinned from both directions.

---

_Generated by /idea-feature-test-export | 2026-08-03_
