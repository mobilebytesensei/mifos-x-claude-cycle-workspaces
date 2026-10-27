# Product Idea — mifos-x-field-officer-app

> **Version**: 1.0
> **Last Updated**: 2026-03-22
> **Status**: Active

---

## Vision Statement

Field officer mobile app for Mifos X - A KMP mobile application enabling field officers to manage clients, loans, collections, and centers in the field with offline support.

## Problem

Field officers need a mobile application to manage clients, loans, savings, and collections while working in the field, often with limited or no connectivity.

## Solution

A Kotlin Multiplatform mobile app that provides offline-first client and financial management for Mifos X/Fineract backend.

---

## Target Users

| Persona | Role | Primary Need | Key Workflow |
|---------|------|-------------|-------------|
| Field Officer | Loan officer in rural areas | Manage clients + loans offline | Visit clients → collect data → sync |
| Branch Manager | Office supervisor | Monitor field operations | Review reports → approve loans |

---

## Core Value Propositions

1. Offline-first data collection and management
2. Real-time sync with Fineract backend when connected
3. Complete client/loan/savings lifecycle management

---

## Platform & Technology

| Attribute | Value |
|-----------|-------|
| Platforms | Android, iOS, Desktop |
| Backend | Fineract REST API |
| Project Type | kmp |

---

## Scope Boundaries

### In Scope
- Client management (create, view, edit, activate)
- Loan management (create, approve, disburse, repay)
- Savings and recurring deposits
- Center and group management
- Offline support with sync
- Search and reporting

### Out of Scope
- Fineract server administration
- Accounting module
- Teller operations

---

## Ideas Backlog

| # | Idea | From | Priority | Status | Added |
|:-:|------|------|:--------:|:------:|:-----:|
| 1 | Permission-aware field officer home dashboard — today's collections, work queue, meetings, portfolio, quick actions; every card gated by the user's Fineract permissions (feature `home`; search moves to feature `search`) | Operator, Fineract permission/API audit | P0 | Scaffolded | 2026-10-26 |
| 2 | Offline sync (Settings → Offline sync, separate from Sync & Drafts) — select centres / groups / clients and a background job downloads each one's full downstream tree (closed accounts and document files included); download-only — offline actions are drafts that Sync & Drafts uploads; live dashboard of everything on the device at three levels (Centre / Group / Client) with per-record sync status; Manual or Automatic sync of the chosen records (feature `offlineSync`) | Operator, redesign of 6b66e8a43 feature/offline | P1 | Scaffolded | 2026-10-27 |
| 3 | Profile, opened from the Home avatar — who is signed in (full name, username, Loan officer / Staff, office, roles), what Home shows (my portfolio vs office), the live server session, Change password and Sign out; offline shows the identity saved at sign-in (feature `profile`) | Operator, after the drawer was removed | P1 | Scaffolded | 2026-10-27 |
