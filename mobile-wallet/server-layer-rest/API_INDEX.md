# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mobile-wallet/server-layer-rest/API_INDEX.md"
# last_modified: "2026-03-20"

# API Index - O(1) Lookup

**Project:** mobile-wallet
**Backend:** {{BACKEND_TYPE}}
**Base URL:** {{BASE_URL}}
**API Version:** v1
**Last Updated:** 2026-03-19
**Auto-Generated:** {{AUTO_GENERATED}}

---

## Quick Reference

<!-- AUTO_POPULATE_START: QUICK_REFERENCE -->
| Feature | Endpoints | Doc File | Status |
|---------|:---------:|----------|:------:|
| authentication | 4 | [endpoints/authentication.md](endpoints/authentication.md) | ✅ Documented |
| users | 5 | [endpoints/users.md](endpoints/users.md) | ✅ Documented |
<!-- Populated by /project-add Step A7.4 -->
<!-- AUTO_POPULATE_END -->

---

## Endpoint Summary

### Authentication

| Method | Endpoint | Description |
|:------:|----------|-------------|
| POST | /api/v1/auth/login | User login |
| POST | /api/v1/auth/signup | User registration |
| POST | /api/v1/auth/refresh | Refresh access token |
| POST | /api/v1/auth/logout | User logout |

### Users

| Method | Endpoint | Description |
|:------:|----------|-------------|
| GET | /api/v1/users | List users |
| GET | /api/v1/users/:id | Get user by ID |
| POST | /api/v1/users | Create user |
| PUT | /api/v1/users/:id | Update user |
| DELETE | /api/v1/users/:id | Delete user |

---

## By HTTP Method

<!-- AUTO_POPULATE_START: HTTP_METHODS -->

### GET Endpoints

| Endpoint | Feature | Description |
|----------|---------|-------------|
| /api/v1/users | users | List users |
| /api/v1/users/:id | users | Get user by ID |

### POST Endpoints

| Endpoint | Feature | Description |
|----------|---------|-------------|
| /api/v1/auth/login | authentication | User login |
| /api/v1/auth/signup | authentication | User registration |
| /api/v1/auth/refresh | authentication | Refresh token |
| /api/v1/auth/logout | authentication | User logout |
| /api/v1/users | users | Create user |

### PUT Endpoints

| Endpoint | Feature | Description |
|----------|---------|-------------|
| /api/v1/users/:id | users | Update user |

### DELETE Endpoints

| Endpoint | Feature | Description |
|----------|---------|-------------|
| /api/v1/users/:id | users | Delete user |

<!-- Populated by /project-add Step A7.4 -->
<!-- AUTO_POPULATE_END -->

---

## Status Legend

| Status | Meaning |
|:------:|---------|
| Documented | Endpoint fully documented |
| Partial | Some fields missing |
| Pending | Not yet documented |
| Deprecated | Will be removed |

---

## Commands

```bash
/server check       # Verify all design layer APIs are documented
/server status      # Show documentation coverage
```
