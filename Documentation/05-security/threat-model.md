# Security Threat Model

## 1. Broken Authorization

### Risk

A delivery employee accesses another customer's or employee's records by changing an ID in an API request.

### Controls

- Deny-by-default authorization
- Role-based permissions
- Object-level authorization
- Server-side access validation
- Authorization tests

---

## 2. Privilege Escalation

### Risk

A low-privilege user calls an administrative endpoint directly.

### Controls

- Server-side permission middleware
- Explicit permission checks
- Never trust browser-supplied roles
- Test sensitive routes with lower-privilege users

---

## 3. Authentication Attacks

### Risk

Credential guessing, stolen sessions, or password reset abuse.

### Controls

- Argon2id or equivalent strong password hashing
- Secure session cookies
- HttpOnly
- Secure
- Appropriate SameSite policy
- Session expiry
- Session rotation
- Login rate limiting
- Secure password-reset tokens
- MFA for privileged users

---

## 4. SQL Injection

### Risk

Malicious input is interpreted as SQL.

### Controls

- Parameterized queries
- Safe ORM/query builder
- Least-privilege database accounts
- Input validation

---

## 5. XSS

### Risk

User-controlled content becomes executable browser code.

### Controls

- Output encoding
- Safe rendering
- Rich-text validation where allowed
- Content Security Policy where practical

---

## 6. CSRF

### Risk

An authenticated browser is tricked into making an unwanted state-changing request.

### Controls

- Secure cookies
- SameSite policy
- CSRF protection where required
- Origin/Referer validation where appropriate

---

## 7. Financial Manipulation

### Risk

A browser modifies:

- Price
- Quantity
- Total
- Payment status
- Customer ID

before submitting.

### Controls

- Treat browser input as untrusted
- Recalculate totals server-side
- Load authoritative prices from database
- Enforce business rules server-side
- Use atomic database transactions

---

## 8. Inventory Manipulation

### Risk

A user directly changes stock without explanation.

### Controls

- Inventory movement ledger
- Controlled adjustment transactions
- Required adjustment reason
- Audit event
- Restricted inventory permissions

---

## 9. Historical Record Tampering

### Risk

Posted records are silently edited or deleted.

### Controls

- Draft → Confirmed → Posted state model
- Lock posted records
- Reversal/adjustment workflows
- Append-only audit events
- Restricted void operations

---

## 10. Audit Log Tampering

### Risk

Evidence of unauthorized activity is removed.

### Controls

- Restricted audit access
- Append-only semantics
- No direct edit/delete endpoints
- Separate retention/storage for critical audit events where appropriate

---

## 11. Data Loss

### Risk

Database corruption, accidental deletion, infrastructure failure, or ransomware.

### Controls

- Automated encrypted backups
- Off-site backup
- Retention policy
- Point-in-time recovery where available
- Restore testing
- Recovery procedure

---

## 12. Resource Abuse

### Risk

Large reports, exports, searches, or login attempts consume application resources.

### Controls

- Rate limiting
- Pagination
- Query limits
- Maximum export ranges
- Background jobs
- Request timeouts
- Monitoring

---

## 13. Supply Chain Risk

### Risk

Vulnerable or malicious dependency enters the application.

### Controls

- Lockfiles
- Dependency scanning
- Dependency update tooling
- Review new packages
- Minimize unnecessary dependencies
- Regular security updates

---

## 14. Secret Leakage

### Risk

Credentials, API keys, session secrets, or encryption keys enter source control.

### Controls

- Environment secrets
- Secret manager where appropriate
- Never commit secrets
- Secret scanning
- Separate development/production credentials
- Secret rotation
