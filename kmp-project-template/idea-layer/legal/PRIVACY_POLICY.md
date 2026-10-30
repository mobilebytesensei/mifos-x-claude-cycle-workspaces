# Privacy Policy — Money Toolkit

**Last updated**: October 30, 2026

## 1. Who we are

Money Toolkit ("the app") is an open-source app published by the Mifos Initiative ("we", "us"). It is also a template other teams fork to build their own apps; a fork that publishes its own app publishes its own privacy policy.

## 2. The short version

- You do not need an account. There is no sign-in.
- Your loans, bills and settings are stored **only on your device**.
- **Usage analytics and crash reports are off** until you switch them on in **Settings → Privacy**, and you can switch them off again at any time.
- To show rates and market data, the app requests **public data** from the services listed in section 5. Those requests do not contain your loans, bills or other personal entries.

## 3. Information stored on your device

| Data | Why | Where |
|---|---|---|
| Loans, bills and reminders you enter | To show, calculate and remind you | On-device database |
| Preferences (theme, language, privacy choices) | To remember your settings | On-device storage |
| Cached rates and market data | So screens work offline | On-device cache |

We cannot see this data. It is removed when you clear the app's data or uninstall it.

## 4. Information sent only if you allow it

Both are **off by default**. Change them in **Settings → Privacy**.

| Setting | What is sent | Service |
|---|---|---|
| Share usage analytics | Which screens and features are used, app version, device type and an app-instance identifier. No advertising identifiers are used, and ad storage is never enabled. | Google Firebase Analytics |
| Send crash reports | Technical details when the app crashes: stack trace, app version, device model and OS version. | Google Firebase Crashlytics |

When you switch crash reports off, reports that have not been sent yet are deleted.

## 5. Services the app connects to

To fetch public data, the app connects to the services below. Like any internet request, each one sees your device's IP address and basic request information; please see each service's own privacy policy.

| Service | Used for | Privacy policy |
|---|---|---|
| Frankfurter (frankfurter.dev) | Currency exchange rates | https://frankfurter.dev |
| CoinGecko | Crypto market prices | https://www.coingecko.com/en/privacy |
| FRED — Federal Reserve Bank of St. Louis | Interest-rate series | https://www.stlouisfed.org/privacy-and-security |
| World Bank Open Data | Country GDP, inflation and unemployment | https://www.worldbank.org/en/about/legal/privacy-notice |
| Supabase | Reading the app's public server configuration | https://supabase.com/privacy |
| Mifos Fineract demo sandbox | Demo data for the banking showcase | https://mifos.org/privacy-policy |
| JSONPlaceholder | Demo data for the offline-edit showcase (no real data is sent) | https://jsonplaceholder.typicode.com |
| Google Firebase (only if you opt in) | Analytics and crash reports — see section 4 | https://policies.google.com/privacy |

**Web version only:** some of these services do not allow direct requests from a web browser, so the web version sends those public-data requests through the CORS relay **corsproxy.io** (https://corsproxy.io). The relay sees the request and your IP address. It is not used by the Android, iOS, macOS or desktop apps.

We do not sell your data, share it with advertisers, or use it to track you across other apps or websites.

## 6. How long data is kept

- **On-device data**: until you delete it, clear the app's data, or uninstall the app.
- **Analytics and crash reports** (only if you opted in): kept by Google under Firebase's standard retention settings.

## 7. Your rights

Under the GDPR and similar laws you can access, correct, delete or restrict your data, object to its processing, and withdraw consent at any time. In the app:

- Withdraw consent: switch analytics or crash reports off in **Settings → Privacy**.
- Delete your entries: remove them in the app, or clear the app's data.

For anything else, including data held by Google for analytics or crash reports, contact us (section 10). You can also complain to your local data-protection authority.

## 8. Security

All connections use HTTPS. Release builds do not log network request or response contents, and credentials and keys are masked in any logs.

## 9. Children

The app is not directed at children under 13, and we do not knowingly collect their information.

## 10. Changes and contact

If this policy changes, we will update the date above and note it in the release notes.

Questions or requests: **team@mifos.org** · Mifos Initiative · https://github.com/openMF/kmp-project-template
