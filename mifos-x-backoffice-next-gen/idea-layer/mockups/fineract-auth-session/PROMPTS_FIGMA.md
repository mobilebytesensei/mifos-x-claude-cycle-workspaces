# Fineract Sign In — Figma Design Hand-off Prompts

> Generated from `screens/fineract-auth-session/ui.yaml` by `/idea-feature-mockup`
> Source hash: ui=299bcbd2a718 · Generated: 2026-07-31 · Design system: `design-tokens.yaml`
> Canvas: 393×852dp (Pixel 5), Material 3, **light theme default**, Roboto.

---

## §DS — Design System Variables (map once in Figma)

- **primary** `#0091EA` (Sign in fill) · **on-primary** `#FFFFFF` · **background** `#FCFCFF` · **surface** `#FCFCFF` (login card) · **surface-variant** `#DEE3EB` (field fills)
- **on-surface** `#1A1C1E` (entered values) · **on-surface-variant** `#42474E` (labels, hint) · **outline** `#72777F` · **error** `#BA1A1A` · **error-container** `#FFDAD6` (banner bg) · **on-error-container** `#410002`
- **Type**: headline-small 24/32 w600 (app title) · title-medium 16/24 · label-large 14/20 · body-medium 14/20 · body-small 12/16 (hint)
- **Radius**: field sm 8 · Sign in button 28 · login card lg 16 · **Spacing**: 16dp field gap, 24dp card padding

---

## Screen: Input (login form ready)

Design the **input** state of the Fineract Sign In gate for **mifos-x-backoffice-next-gen**, a clinical Material-3 financial-admin console. Light theme, 393×852dp. No app chrome — this is the pre-auth gate: no bottom nav, no drawer, no FAB.

Center a **branded login card** (bg `surface #FCFCFF`, radius 16, 24dp padding, subtle 1px `outline` border) on a `background #FCFCFF` backdrop. Inside, top-down:
- App title **"Mifos-X Back Office"** in headline-small `on-surface`.
- A one-line `server_hint` in `body-small` `on-surface-variant`: "Sign in against your Fineract server and tenant."
- Four stacked outlined text fields (`surface-variant #DEE3EB` fill, radius 8, 56dp height, label above): **Server URL** (`base_url_field`, prefilled "https://demo.mifos.community", url-format validated), **Tenant** (`tenant_field`, prefilled "default"), **Username** (`username_field`, "mifos"), **Password** (`password_field`, masked "••••••••").
- A full-width **filled primary button "Sign in"** (`sign_in_button`, bg `primary #0091EA`, `on-primary` label, radius 28, 48dp) — **enabled only** when the base-URL is a valid http(s) URL and tenant/username/password are non-empty (disabled/greyed otherwise).

Note: only the derived Basic token is ever stored — never the raw password.

---

## Screen: Restoring (cold-start session read)

Design the **restoring** state. No form — just the branded card outline (or app logo) with a centered circular progress indicator (`primary #0091EA`) and a `body-small` caption "Restoring your session…". This reads the persisted encrypted session with no network; a valid session routes straight onward, absence falls through to Input.

---

## Screen: Authenticating (auth in flight)

Design the **authenticating** state. Same login card as Input but all fields and the Sign in button are **disabled** (reduced opacity 0.38), with a circular progress indicator replacing/overlaying the Sign in button label. Nothing is persisted until success.

---

## Screen: Error (auth failed)

Design the **error** state. Same login card, fields re-enabled with entered values retained (password cleared). Above the fields, an inline **error banner** (`error_banner`): bg `error-container #FFDAD6`, `on-error-container` text, leading `[!]` icon in `error #BA1A1A`, stating the reason in words — "Invalid credentials", "Server unreachable", "No network", or "Password change / 2FA required". Show a **Retry** text/outline button (`retry_button`) alongside Sign in (Retry re-submits after a transient failure; a 401 requires editing the fields first).

---

## Screen: Authenticated (session established)

Transient success state — a brief centered check/spinner before routing to permission-capability-engine (the capability bootstrap). No standalone design needed beyond a success indicator.

---

## Prototype Interactions

- Field edit → re-validate, toggle Sign in enablement.
- Sign in tap → Authenticating → (success) route to permission-capability-engine / (failure) Error.
- Retry tap → re-submit → Authenticating.
- Any 401 elsewhere in the app → routes back to this gate (Input).
