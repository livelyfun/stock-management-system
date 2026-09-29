# Test Plan

## 1. Goals

Testing must verify:

- Functional correctness
- Business-rule correctness
- Authorization
- Transaction integrity
- Inventory consistency
- Financial consistency
- Security
- Concurrency

---

## 2. Test Levels

### Unit Tests

Test individual business rules and services.

### Integration Tests

Test modules interacting with PostgreSQL and other infrastructure.

### API Tests

Test authentication, authorization, validation, and endpoints.

### End-to-End Tests

Test complete business workflows.

### Security Tests

Test common application and business-logic vulnerabilities.

---

## 3. Critical Workflows

Test:

- Create delivery
- Post delivery
- Return delivery item
- Record payment
- Allocate payment
- Customer ledger
- Inventory adjustment
- Transaction reversal
- Role authorization

---

## 4. Failure Testing

Verify rollback when:

- Inventory update fails
- Invoice creation fails
- Ledger update fails
- Audit creation fails where required
- Database error occurs

### Retry Behaviour

Verify that:

- A recognized transient concurrency failure is retried, up to 3
  attempts in total, with backoff of 100 ms then 250 ms
- A business-rule or validation failure, including insufficient stock,
  is rejected immediately and is never retried
- After the final failed attempt, a generic retryable transaction error is
  returned
- The generic error does not expose SQL errors, stack traces, or other
  database internals
- The failure is logged with the request or correlation ID
- A rolled-back transaction leaves no partial movement, balance, or
  audit state

---

## 5. Concurrency Testing

Test multiple simultaneous inventory transactions.

Starting stock = 200, with one user delivering 100 and another
delivering 150 at nearly the same time.

Verify that:

- The final on-hand quantity is never negative
- Stock is never double consumed
- The rejected transaction leaves no partial state
- Row-level locking is obtained before the availability check

---

## 6. Regression Testing

Business rules must have automated regression tests.

Changes must not silently break existing transaction behavior.
