# Security Testing

## Authentication

Test:

- Brute-force protection
- Session expiry
- Session invalidation
- Password reset security
- Privileged-user MFA

---

## Authorization

Test:

- Staff accessing admin actions
- Viewer attempting writes
- Cross-customer access
- Cross-employee access
- Direct API access to restricted resources
- IDOR/BOLA scenarios

---

## Business Logic

Test:

- Return greater than delivered
- Payment greater than outstanding
- Negative quantities
- Negative prices
- Duplicate transaction numbers
- Insufficient stock
- Concurrent stock updates
- Unauthorized credit adjustments

### Expected Outcomes

The expected results for the inventory cases are fixed, so that a
regression is detectable:

- **Insufficient stock** — the transaction is rejected and the balance
  is unchanged. Negative on-hand stock must not be reachable. There is
  no override permission to test for, because no override exists.
- **Concurrent stock updates** — the final on-hand quantity is never
  negative and stock is never double consumed. The concurrent case is a
  correctness test, not an authorization test.
- **Negative quantities** — rejected, whether submitted directly or
  through an adjustment endpoint.
- **Cross-warehouse access** — a movement must not draw on stock held in
  a warehouse other than the one recorded on the document. Warehouse
  identity is data integrity, and must be enforced independently of
  authorization.

A transaction that fails after the retry limit returns a generic
retryable error, and must not leak the underlying database error.

---

## Application Security

Test:

- SQL injection
- XSS
- CSRF
- IDOR/BOLA
- Mass assignment
- File upload abuse
- Rate-limit bypass
- Security misconfiguration

---

## Dependency Security

Test for:

- Vulnerable dependencies
- Outdated packages
- Known CVEs
- Secret leakage

---

## Production Security

Verify:

- HTTPS
- Secure cookies
- Database not publicly exposed
- Secrets not committed
- Logging enabled
- Backups enabled
