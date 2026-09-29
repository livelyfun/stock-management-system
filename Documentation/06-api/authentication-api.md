# Authentication API

## Login

Conceptual endpoint:

POST /api/auth/login

Responsibilities:

- Validate credentials
- Authenticate user
- Create session
- Record login event
- Apply rate limiting

---

## Logout

POST /api/auth/logout

Responsibilities:

- Invalidate session
- Record event where appropriate

---

## Password Reset Request

POST /api/auth/password-reset/request

Responsibilities:

- Accept account identifier
- Generate secure reset token
- Apply rate limiting
- Avoid account enumeration

---

## Password Reset

POST /api/auth/password-reset/confirm

Responsibilities:

- Validate token
- Validate expiration
- Ensure token is single-use
- Set new password
- Invalidate appropriate sessions

---

## Current User

GET /api/auth/me

Returns authenticated user information allowed by the application.

Never return secrets.
