# Terms and Conditions — Mifos-X Open Banking

**App Name:** Mifos-X Open Banking  
**Package:** org.mifos  
**Developer:** Mifos Initiative / openMF contributors  
**Contact:** legal@mifos.org  
**Effective Date:** 2026-08-06  
**Version:** 2.0.0  
**Standard:** UK Open Banking — OBIE Read/Write API Specification v4.0, FAPI 1.0 Advanced  
**Bank (ASPSP):** HSBC UK — sandbox environment  

---

## 1. Introduction and Agreement

Mifos-X Open Banking ("the App", "Software") is a Kotlin Multiplatform (KMP) open-source consumer banking application providing retail banking self-service from a single codebase on Android, iOS, desktop (macOS, Windows, Linux), and web platforms.

By installing, accessing, or using the App, you ("User", "you") agree to be bound by these Terms and Conditions ("Terms"). If you do not agree, do not install or use the App.

These Terms govern your use of the App software. Separate terms of service from your banking institution govern the financial products and banking services you access through the App.

---

## 2. Description of the Application

### 2.1 Solution

Mifos-X Open Banking is a **UK Open Banking reference client** built to the OBIE Read/Write API Specification v4.0. It acts as an Account Information Service Provider (AISP) and a Payment Initiation Service Provider (PISP) against the HSBC UK Open Banking sandbox. The App provides:

**Account information (AISP):**
- Account overview with balances
- Transaction history
- Beneficiaries, standing orders, direct debits and scheduled payments (read-only)
- Statements, product terms and account holder details
- Consent management — review, revoke and reconfirm your data-sharing consent

**Payment initiation (PISP):** all seven HSBC UK Personal payment types —
- Domestic single, scheduled, and standing order
- International single, scheduled, and standing order
- Domestic Variable Recurring Payments (VRP), including mandate revocation

The App connects exclusively to your bank's Open Banking endpoint. It is a **client application only** — it does not own or operate a database, backend, or financial infrastructure, and it never holds your money.

**Sandbox status:** this deployment connects to HSBC's sandbox, which contains synthetic test data only.

### 2.2 Open-Source License

The App's source code is available at https://github.com/openMF/mifos-x-open-banking under the Mozilla Public License 2.0 (MPL-2.0). Use, modification, and distribution of the source code are governed by that license.

---

## 3. User Eligibility and Accounts

### 3.1 Eligibility

You must be at least 18 years old and legally capable of entering binding agreements to use this App.

### 3.2 Authentication

**The App has no account and no password.** Under UK Open Banking you authenticate directly with your bank, in your bank's own app or website, and the App receives only a scoped access token for the data and actions you approved. You are responsible for:
- Keeping your banking credentials confidential, and never entering them into this App — it will never ask
- Reviewing what a consent grants before approving it at your bank
- Notifying your bank immediately if you suspect unauthorized access
- Logging out of the App when using shared devices

We are not responsible for losses resulting from unauthorized use of your banking credentials.

### 3.3 App Credentials

The App holds its own signing and transport certificates, issued to the deploying organisation under the Open Banking directory. Do not attempt to extract, share, or misuse these credentials.

### 3.4 Regulatory Permissions

AISP and PISP are distinct permissions under the Payment Services Regulations 2017. This deployment operates against a sandbox only; initiating payments for real customers in production requires payment-initiation authorisation that this project does not hold.

---

## 4. Permitted and Prohibited Uses

### 4.1 Permitted Uses

You may use the App to:
- Access your own banking accounts and financial data, under a consent you have granted at your bank
- Initiate payments from your own accounts, of the seven types described in §2.1
- Export or download your own financial data for personal record-keeping

### 4.2 Prohibited Uses

You must not use the App to:
- Access accounts or data belonging to other individuals without explicit authorization
- Attempt to reverse-engineer, decompile, or extract authentication credentials embedded in the App
- Perform automated scraping, bulk data extraction, or API abuse beyond normal single-user operation
- Circumvent security controls, authentication, or rate limits
- Conduct any activity that violates applicable financial regulations (AML, KYC, sanctions screening)
- Upload malicious content or attempt to inject code through the App's interfaces
- Use the App for fraudulent, deceptive, or money-laundering activities

Violation of prohibited uses may result in termination of your access and may be referred to law enforcement.

---

## 5. Financial Services Disclaimer

### 5.1 App is a Client Interface Only

The App is a **front-end interface** to your bank's Open Banking API. It does not:
- Hold, store, or process funds
- Execute payments independently — every payment is executed by your bank, which authenticates you and applies its own checks before doing so
- Provide investment advice, financial planning, or regulated financial advisory services
- Guarantee the accuracy, completeness, or timeliness of account and transaction data displayed

### 5.2 Banking Institution Responsibility

All financial services are provided by your bank. Its separate terms of service, product terms, and regulatory disclosures govern those services. Your bank decides whether to execute any payment the App submits, and may decline it.

### 5.3 Transaction Finality

Payments initiated through the App are submitted to your bank for processing. Once submitted, a payment may be irreversible. Review all details carefully before confirming. We are not liable for erroneous payments initiated by you.

### 5.4 Changing or Cancelling a Recurring Payment

Open Banking does **not** permit this App — or any third-party provider — to amend or cancel a standing order or a future-dated scheduled payment once it is set up. To change or cancel one, use HSBC's own app or online banking. This is a regulatory limitation, not a missing feature.

A **Variable Recurring Payment mandate is different**: you may revoke it from within the App at any time, and no further payments can be taken under it. Once revoked, a mandate cannot be reinstated — you would need to create a new one.

### 5.5 Payment Status

A payment reported as in progress has been accepted for settlement but has not necessarily completed. For standing orders and scheduled payments, the standard provides **no per-execution status at all** — the App can confirm that an instruction is set up, but cannot tell you whether any individual future payment succeeded. Check your transaction history or your bank's own channel to confirm a payment landed.

---

## 6. Data and Privacy

Your use of the App is governed by our Privacy Policy (see `PRIVACY_POLICY.md` and https://mifos.org/privacy-policy). Key data practices:

- Authentication tokens are stored encrypted on-device and cleared on logout
- Financial data is cached locally for offline display and is not transmitted to any server other than your bank's Open Banking endpoint
- Crash and performance telemetry is collected on Android via Firebase Crashlytics and Firebase Performance Monitoring — no financial data is included in these reports
- We do not sell your personal data

---

## 7. Intellectual Property

### 7.1 App Source Code

The App source code is licensed under the Mozilla Public License 2.0 (MPL-2.0). See the full license at https://github.com/openMF/mifos-x-open-banking/blob/dev/LICENSE.

### 7.2 Third-Party Components

The App incorporates third-party open-source libraries including:
- Kotlin Multiplatform / Compose Multiplatform (Apache 2.0 — JetBrains)
- Ktor / Ktorfit (Apache 2.0)
- Koin (Apache 2.0)
- Store5 (Apache 2.0)
- Room KMP (Apache 2.0 — Google)
- Firebase Android SDKs (Apache 2.0 — Google)

A complete license inventory is available in the App's open-source acknowledgements screen.

### 7.3 Mifos Trademarks

"Mifos" and associated logos are trademarks of the Mifos Initiative. Use of these trademarks in derivative works requires prior written permission.

---

## 8. Disclaimers and Limitation of Liability

### 8.1 "As Is" Software

THE APP IS PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.

### 8.2 No Warranty on Financial Data Accuracy

WE DO NOT WARRANT THAT ACCOUNT BALANCES, TRANSACTION HISTORIES, OR OTHER FINANCIAL DATA DISPLAYED IN THE APP ARE ACCURATE, COMPLETE, OR CURRENT AT ALL TIMES. SUCH DATA IS RETRIEVED FROM YOUR BANK'S OPEN BANKING API AND IS SUBJECT TO TRANSMISSION DELAYS, API ERRORS, AND BANKING INSTITUTION PROCESSING TIMES.

### 8.3 Limitation of Liability

TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, IN NO EVENT SHALL THE MIFOS INITIATIVE, OPENMF CONTRIBUTORS, OR AFFILIATED PARTIES BE LIABLE FOR:
- LOSS OF FUNDS ARISING FROM UNAUTHORIZED ACCESS TO YOUR ACCOUNT CREDENTIALS
- ERRONEOUS PAYMENT TRANSACTIONS INITIATED BY YOU
- BUSINESS INTERRUPTION, DATA LOSS, OR LOST PROFITS ARISING FROM USE OF OR INABILITY TO USE THE APP
- INDIRECT, INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES

Where consumer protection law prohibits limitation of liability for certain losses, such limitations shall not apply to the extent prohibited.

---

## 9. Indemnification

You agree to indemnify and hold harmless the Mifos Initiative, openMF contributors, and their directors, employees, and agents from any claims, damages, or expenses arising from:
- Your violation of these Terms
- Your use of the App in a manner not authorized by these Terms
- Your violation of applicable law, including financial regulations
- Infringement of any third-party right by your use of the App

---

## 10. Termination

### 10.1 By You

You may stop using the App at any time by uninstalling it from your device. Uninstalling the App clears the local encrypted database (cached financial data and session tokens).

### 10.2 By Us

We reserve the right to discontinue, suspend, or modify the App at any time, with or without notice. We may release updated versions that supersede prior versions.

---

## 11. Updates and Changes

We may update these Terms from time to time. Material changes will be communicated via an in-app notification and by updating the "Effective Date" above. Continued use of the App after the effective date of revised Terms constitutes acceptance.

---

## 12. Governing Law and Dispute Resolution

These Terms are governed by the laws of the State of Virginia, United States, without regard to conflict of law provisions. Disputes arising from these Terms shall be resolved by binding arbitration administered by the American Arbitration Association under its Commercial Arbitration Rules, except that either party may seek injunctive relief in a court of competent jurisdiction.

If you are located in the European Economic Area, mandatory consumer protection laws of your country of residence may apply in addition to or instead of the above.

---

## 13. Regulatory Compliance

The App is a client interface to your bank's UK Open Banking API, operating under the
Payment Services Regulations 2017. Anti-Money Laundering (AML), Know Your Customer (KYC),
sanctions screening and transaction monitoring rest with your bank, which performs them
before executing any payment the App submits.

Third-party provider status under those regulations — Account Information Service Provider
(AISP) and Payment Initiation Service Provider (PISP) — are distinct FCA permissions. This
deployment operates against a sandbox environment only.

---

## 14. Contact

For questions about these Terms:

**Email:** legal@mifos.org  
**Postal:** Mifos Initiative, c/o Conflux Foundation, 3040 Williams Drive Suite 610, Fairfax VA 22031, USA  

For banking service inquiries, contact your banking institution directly.
