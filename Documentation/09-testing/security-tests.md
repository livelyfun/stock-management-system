# Security Test Cases

## Authentication

- Brute-force attempts
- Password reset abuse
- Session expiry
- Session invalidation
- Session fixation
- MFA where implemented

---

## Authorization

- IDOR/BOLA
- Privilege escalation
- Cross-customer access
- Cross-employee access
- Unauthorized API calls

---

## Input Security

- SQL injection
- XSS
- CSRF
- Mass assignment
- Malformed input

---

## Resource Abuse

- Large report queries
- Large exports
- Excessive login attempts
- Rate-limit bypass

---

## File Security

Where file uploads are implemented:

- File type validation
- File size limits
- Filename handling
- Malware scanning where appropriate
- Storage isolation
- Unauthorized file access

---

## Dependency Security

Run dependency vulnerability scanning regularly.

---

## Secret Security

Verify:

- No secrets in Git
- No secrets in logs
- No secrets in audit events
- Production secrets separated from development secrets
