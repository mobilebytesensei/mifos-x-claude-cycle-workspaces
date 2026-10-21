# Privacy Policy — Mifos-X Open Banking

**App Name:** Mifos-X Open Banking  
**Package:** org.mifos  
**Developer:** Mifos Initiative / openMF contributors  
**Contact:** privacy@mifos.org  
**Effective Date:** 2026-08-06  
**Version:** 2.0.0  
**Standard:** UK Open Banking — OBIE Read/Write API Specification v4.0, FAPI 1.0 Advanced  
**Bank (ASPSP):** HSBC UK — sandbox environment  

---

## 1. Introduction

Mifos-X Open Banking ("the App", "we", "us", "our") is a Kotlin Multiplatform consumer banking application available on Android, iOS, desktop, and web. It is a **UK Open Banking reference client** built to the OBIE (Open Banking Implementation Entity) Read/Write API Specification v4.0, operating as an Account Information Service Provider (AISP) and Payment Initiation Service Provider (PISP) against the **HSBC UK Open Banking sandbox**.

We are committed to protecting your personal data and financial privacy. This Privacy Policy explains what data we collect, how we use it, who we share it with, and what rights you have.

This policy applies to all platforms on which the App is available: Android, iOS (iPhone and iPad), desktop (macOS, Windows, Linux), and web browser.

**The App never sees or handles your banking password.** Under UK Open Banking you authenticate directly with your bank, in your bank's own app or website. The App receives only a scoped access token, and only for the data and actions you explicitly approve.

---

## 2. Controller Identity

Two parties act as controllers, for different data:

- **Your bank (the ASPSP)** is the controller for your account, balance, transaction and payment data. It holds that data, authenticates you, and decides what a consent grants. For this deployment that is **HSBC UK**. Consult HSBC's own privacy notice for how it processes your data.
- **The App operator (the TPP)** is the controller for the consent records, session tokens and device telemetry described in §3. For this reference deployment that is the **Mifos Initiative / openMF contributors**, contactable at privacy@mifos.org.

The App is open-source software. If you are using a deployment operated by another organisation, that organisation is the TPP-side controller — consult their privacy notice.

**Sandbox status:** this deployment connects to HSBC's *sandbox* environment, which contains synthetic test data only. No real customer accounts are reachable through it.

---

## 3. Data We Collect and Why

### 3.1 Financial and Account Information

Every item below is read **only** if the corresponding OBIE permission is in the account-access consent you approved at your bank. Revoking the consent stops all of it immediately.

| Data Type | Source (OBIE v4.0 AIS) | OBIE Permission | Purpose |
|---|---|---|---|
| Account identifiers and details | `GET /aisp/accounts`, `/accounts/{id}` | `ReadAccountsBasic`, `ReadAccountsDetail` | Display account list and detail |
| Account balances | `GET /aisp/accounts/{id}/balances` | `ReadBalances` | Home dashboard, account detail |
| Transaction history | `GET /aisp/accounts/{id}/transactions` | `ReadTransactionsBasic/Detail/Credits/Debits` | Transaction list, spending snapshot |
| Beneficiaries (saved payees) | `GET /aisp/accounts/{id}/beneficiaries` | `ReadBeneficiariesBasic`, `ReadBeneficiariesDetail` | Choosing a payee when paying |
| Standing orders | `GET /aisp/accounts/{id}/standing-orders` | `ReadStandingOrdersBasic`, `ReadStandingOrdersDetail` | Standing orders screen |
| Scheduled payments | `GET /aisp/accounts/{id}/scheduled-payments` | `ReadScheduledPaymentsBasic`, `ReadScheduledPaymentsDetail` | Scheduled payments screen |
| Direct debits | `GET /aisp/accounts/{id}/direct-debits` | `ReadDirectDebits` | Direct debits screen |
| Statements | `GET /aisp/accounts/{id}/statements` | `ReadStatementsBasic`, `ReadStatementsDetail` | Statements list and detail |
| Product terms | `GET /aisp/accounts/{id}/product` | `ReadProducts` | Product screen |
| Account holder details | `GET /aisp/accounts/{id}/party` | `ReadParty` | Account holder screen |
| Card number (unmasked) | `transactions` records | `ReadPAN` | Only where a transaction is card-funded |

**Retention:** Financial data is displayed in-session and may be cached locally in an encrypted on-device database for offline viewing. The App transmits your financial data to no server other than your bank's Open Banking endpoint.

### 3.2 Payment Initiation Data

When you initiate a payment, the App sends the payment instruction you composed to your bank. It does not retain the instruction beyond what is needed to track its status.

| Data Type | Destination (OBIE v4.0 PIS) | Purpose |
|---|---|---|
| Payment instruction — debtor account, creditor account and name, amount, currency, and where applicable execution date, recurrence or VRP control parameters | `POST /pisp/{family}-consents` and `POST /pisp/{family}` | Staging and submitting the payment you asked for |
| Payment and consent identifiers | Held on-device | Tracking the payment to settlement via the status endpoints |
| VRP mandate records, including revocation | Held on-device | Once a mandate is revoked its consent is permanently unreadable, so the App keeps its own record |

The App initiates **consumer** payments only — you paying a person, or moving money between your own accounts. It never sends merchant or e-commerce context, and never sends merchant category codes, merchant customer identifiers or delivery addresses.

### 3.3 Authentication Credentials

**The App has no password field and never receives your banking credentials.** Authentication uses the FAPI 1.0 Advanced profile: you are redirected to your bank, authenticate there, and the App receives only a token.

| Data Type | How Stored | Purpose |
|---|---|---|
| TPP signing and transport keys | Encrypted secrets store — never in source code | Mutual TLS and request signing between the App and your bank |
| Access token (scoped to the consent) | Encrypted on-device store; cleared on logout or revocation | Making the API requests you approved |
| Refresh token | Encrypted on-device store; cleared on logout or revocation | Renewing access without re-authenticating |
| Consent identifiers | Encrypted on-device store | Showing you what is shared, and letting you revoke it |

Payment-scope tokens are held only for the life of a single payment and are never written into the account-data session.

### 3.4 Personal Identifiers

| Data Type | Source | Purpose |
|---|---|---|
| Account holder name, email, mobile, address | `GET /aisp/accounts/{id}/party` (`ReadParty` only) | Account holder screen |

The App accesses only your own account data. It does not collect or process third-party customer records, and it has no user profile of its own — there is no App account, no username and no password.

### 3.4 Device Identifiers and Technical Data

| Data Type | Source | Purpose |
|---|---|---|
| Device crash data (stack traces, device model, OS version, App version) | Firebase Crashlytics SDK (Android only) | Crash reporting and bug fixing |
| App performance metrics (cold-start time, frame rates, network latency) | Firebase Performance Monitoring SDK (Android only) | Performance monitoring |
| Installation UUID (Firebase installation ID) | Firebase SDK (Android only) | Aggregating crash + performance telemetry |

Firebase Crashlytics and Firebase Performance Monitoring are **Android-only** features. These SDKs do not operate on iOS, desktop, or web builds of this App.

### 3.5 Local Storage

The App uses Room KMP (SQLite) encrypted local database for:
- Caching account and transaction data for offline display
- Storing user preferences (theme, language)
- Storing encrypted session token

Local database data does not leave your device except as part of normal Open Banking API interactions with your bank.

---

## 4. Third-Party Services

The App integrates with the following third-party services:

### 4.1 Your bank's UK Open Banking API (HSBC UK)

- **Provider:** HSBC UK, acting as the ASPSP (Account Servicing Payment Service Provider)
- **Purpose:** All banking data access and payment initiation — accounts, balances, transactions, beneficiaries, standing orders, scheduled payments, direct debits, statements, and the seven payment types
- **Data shared:** The scoped access token, your API queries, and any payment instruction you compose
- **Privacy policy:** https://www.hsbc.co.uk/privacy-notice/
- **Data transfer:** All API calls are made over mutual TLS (mTLS, TLS 1.2+) to HSBC's Open Banking endpoint. Payment writes additionally carry a detached JWS signature so the bank can verify the instruction came from this App unaltered.
- **Standard:** OBIE Read/Write API Specification v4.0, FAPI 1.0 Advanced security profile
- **Regulatory basis:** UK Open Banking under the Payment Services Regulations 2017 / PSD2. Your bank is required to provide this access once you consent, and to stop it the moment you revoke.

### 4.2 Firebase Crashlytics (Android only)

- **Provider:** Google LLC
- **Purpose:** Crash reporting — automatic capture of unhandled exceptions and fatal errors
- **Data shared:** Crash stack traces, device model, Android OS version, App version, Firebase installation UUID
- **No PII in crash reports:** We do not log usernames, account numbers, or financial data to Crashlytics. Crash reports contain only technical diagnostics.
- **Privacy policy:** https://policies.google.com/privacy
- **Google Data Processing Terms:** https://business.safety.google/adsprocessorterms/

### 4.3 Firebase Performance Monitoring (Android only)

- **Provider:** Google LLC
- **Purpose:** App performance metrics — cold start time, screen rendering, network request latency
- **Data shared:** Anonymous performance traces, network request URLs (no request bodies or auth tokens), device class
- **No PII in performance traces:** Network URLs logged by Performance Monitoring are stripped of auth tokens and query parameters containing user data.
- **Privacy policy:** https://policies.google.com/privacy

---

## 5. Legal Basis for Processing (GDPR)

If you are located in the European Economic Area (EEA), United Kingdom, or Switzerland, we process your personal data under the following legal bases:

| Processing Activity | Legal Basis |
|---|---|
| Accessing account and transaction data | **Explicit consent** (Art. 6(1)(a) GDPR), given at your bank under the Payment Services Regulations 2017. This is the account-access consent you approve on HSBC's own site, and you can withdraw it at any time. |
| Initiating a payment you have composed | **Contract performance** (Art. 6(1)(b) GDPR) — carrying out the payment you asked for |
| Token and consent-record handling | **Contract performance** (Art. 6(1)(b) GDPR) |
| Firebase Crashlytics crash telemetry | **Legitimate interests** (Art. 6(1)(f) GDPR) — maintaining app stability and security |
| Firebase Performance telemetry | **Legitimate interests** (Art. 6(1)(f) GDPR) — app quality improvement |
| Local preference data | **Contract performance** / **Legitimate interests** |

Account information access under Open Banking rests on **explicit consent**, not on contract performance. That is why it is revocable at any moment and why the App shows you a consent dashboard.

---

## 6. Data Retention

| Data Category | Retention |
|---|---|
| Access token | Deleted on logout or on consent revocation |
| Refresh token | Deleted on logout or on consent revocation |
| Account-access consent | Expires per the consent's own expiry, and in any case requires reconfirmation every 90 days under UK Open Banking rules |
| Cached financial data | Cleared on logout or revocation; maximum 30 days inactive |
| Payment and consent identifiers | Retained while the payment is trackable, then cleared |
| VRP mandate records | Retained until the mandate is revoked, then kept as a revocation record only |
| Firebase crash reports | 90 days in Firebase Console (Google's retention policy) |
| Firebase performance traces | 90 days in Firebase Console |

---

## 7. Data Transfers

Financial data is transmitted to and from your bank's UK Open Banking endpoint, operated by HSBC UK within the United Kingdom.

Firebase services (Crashlytics and Performance Monitoring) are provided by Google LLC, a US-based company. Google participates in the EU-US Data Privacy Framework. Data processing agreements are in place per GDPR Article 28.

---

## 8. Security

We implement the following technical safeguards:

- All network communications use **mutual TLS (mTLS)**, TLS 1.2 or higher, with a client certificate issued to this App
- Authentication follows the **FAPI 1.0 Advanced** security profile: signed request object, PKCE S256, and `private_key_jwt` client authentication
- Every payment write carries a **detached JWS signature** (PS256), so your bank can verify the instruction reached it unaltered
- Every payment write carries an **idempotency key**, so a retry after a network failure cannot create a second payment
- Tokens are stored in an encrypted on-device store (Android Keystore / iOS Secure Enclave / platform-equivalent) and cleared on logout or revocation
- **The App has no password field.** You authenticate at your bank, so there is no banking credential for this App to log, store, leak or lose
- Payment-scope tokens are never written into the account-data session
- Firebase SDKs are configured to exclude sensitive fields from crash reports

---

## 9. Your Rights

### GDPR Rights (EEA / UK / Switzerland)

You have the following rights regarding your personal data:

- **Right of Access (Art. 15):** You may request a copy of the personal data we hold about you.
- **Right to Rectification (Art. 16):** You may request correction of inaccurate personal data.
- **Right to Erasure / "Right to be Forgotten" (Art. 17):** You may request deletion of your personal data where we no longer have a lawful basis to retain it.
- **Right to Restriction of Processing (Art. 18):** You may request that we restrict how we process your data in certain circumstances.
- **Right to Data Portability (Art. 20):** You may request your data in a machine-readable format.
- **Right to Object (Art. 21):** You may object to processing based on legitimate interests.
- **Right to Withdraw Consent:** Where processing is based on consent, you may withdraw it at any time.
- **Right to Lodge a Complaint:** You have the right to lodge a complaint with your national data protection authority (e.g., ICO in the UK, BfDI in Germany).

### Your Open Banking rights

These sit alongside your GDPR rights and are specific to UK Open Banking:

- **Revoke at any time.** You may withdraw an account-access consent from the App's consent dashboard, or directly in your bank's app. Access stops immediately; no further data is read.
- **90-day reconfirmation.** UK rules require you to reconfirm an account-access consent every 90 days. If you do not, access lapses automatically.
- **Revoke a VRP mandate at any time.** A Variable Recurring Payment mandate can be cancelled from the App or from your bank, and no further payments can be taken under it.
- **Standing orders and scheduled payments must be changed at your bank.** Open Banking does not permit this App to amend or cancel them — please use HSBC's own app or online banking.
- **You are never asked for your banking password.** If any app or website claiming to be an Open Banking provider asks for it, that is not how the standard works.

### CCPA Rights (California Residents)

If you are a California resident, you have the following rights under the California Consumer Privacy Act:

- **Right to Know:** You may request disclosure of the categories and specific pieces of personal information we have collected about you.
- **Right to Delete:** You may request deletion of personal information we have collected, subject to exceptions.
- **Right to Opt-Out of Sale:** We do **not** sell your personal information to third parties.
- **Right to Non-Discrimination:** You will not receive discriminatory treatment for exercising your CCPA rights.

To exercise any of these rights, contact: **privacy@mifos.org**

Response time: 30 days for GDPR requests; 45 days for CCPA requests.

---

## 10. Children's Privacy

This App is a banking application intended for adults (18+) and authorized banking professionals. We do not knowingly collect personal data from individuals under 18. If you believe a minor's data has been collected, contact privacy@mifos.org immediately.

---

## 11. Changes to This Policy

We will notify you of material changes to this policy via an in-app notification and by updating the "Effective Date" above. Continued use of the App after the effective date constitutes acceptance of the revised policy.

---

## 12. Contact

For privacy inquiries, data subject rights requests, or to report a data protection concern:

**Email:** privacy@mifos.org  
**Postal:** Mifos Initiative, c/o Conflux Foundation, 3040 Williams Drive Suite 610, Fairfax VA 22031, USA  
**Response time:** 30 days  

For EU/UK data protection inquiries, you may also contact the deploying financial institution's Data Protection Officer if applicable.
