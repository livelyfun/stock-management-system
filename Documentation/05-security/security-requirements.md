# Security Requirements

## Authentication

The system must provide:

- Secure password hashing
- Secure sessions
- Session expiry
- Session rotation where appropriate
- Password reset protection
- Login rate limiting
- MFA for privileged users where appropriate

---

## Authorization

Authorization must be:

- Server-side
- Deny-by-default
- Role-based
- Object-level where required

---

## Data Protection

Sensitive information must be protected.

Secrets must not be committed to source control.

---

## Database Security

- Use least-privilege database accounts.
- Use parameterized queries.
- Do not expose PostgreSQL directly to the public internet.
- Apply database constraints.

---

## Application Security

Protect against:

- SQL injection
- XSS
- CSRF
- IDOR/BOLA
- Mass assignment
- File upload abuse
- Rate-limit bypass
- Security misconfiguration

---

## Auditability

Sensitive operations must generate audit events.

---

## Infrastructure

Production should use:

- HTTPS
- Secure environment variables
- Database backups
- Monitoring
- Health checks
