# Authentication Requirements

## Login

Users must authenticate using secure credentials.

---

## Password Storage

Passwords must never be stored as plaintext.

Use a strong password hashing algorithm such as Argon2id.

---

## Sessions

Sessions should use secure cookies with appropriate:

- HttpOnly
- Secure
- SameSite

settings.

---

## Session Management

Implement:

- Session expiry
- Session invalidation
- Session rotation where appropriate
- Logout
- Protection against session fixation

---

## Password Reset

Password reset must use:

- Secure random tokens
- Short expiration
- Single-use tokens
- No password disclosure

---

## Login Protection

Protect authentication endpoints against:

- Brute force
- Credential stuffing
- Excessive attempts

Use appropriate rate limiting.

---

## Privileged Accounts

Privileged accounts should support MFA where appropriate.

---

## Audit

Record:

- Login success
- Login failure
- Password reset
- Important authentication events

Never store passwords or authentication secrets in audit logs.
