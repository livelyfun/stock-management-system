# API Contract

## 1. General Principles

All protected API operations must:

1. Authenticate the user.
2. Authorize the requested action.
3. Validate input.
4. Execute business rules.
5. Perform database operations transactionally where required.
6. Record audit events for sensitive actions.

---

## 2. Request Input

All client input is untrusted.

The server must validate:

- Types
- Required fields
- IDs
- Quantities
- Monetary values
- Status transitions
- Business rules

---

## 3. Response Principles

Responses should provide:

- Success/failure status
- Appropriate HTTP status
- Machine-readable error code
- Human-readable message where appropriate

Do not expose internal implementation details.

---

## 4. Error Handling

Do not return:

- SQL errors
- Stack traces
- Database credentials
- Internal secrets
- Sensitive debugging information

to clients.

---

## 5. Transaction Resilience

Concurrency conflicts are transient and safe to replay; business-rule
failures are deterministic and must not be replayed. The retry contract
is therefore explicit.

### Retry Contract

- Maximum 3 attempts in total.
- Backoff between retries of 100 ms, then 250 ms.
- Only recognized transient database concurrency failures are retried,
  such as deadlock or serialization failure.
- Business-rule and validation failures are never retried. This includes
  insufficient stock, which is a business failure and not a transient
  error.
- After the final failed attempt, the API returns a generic retryable
  transaction error.
- The generic error must not identify the database error, as required by
  section 4.

### Diagnosis

A retried-then-failed transaction must be logged server-side with the
request or correlation ID, so the failure can be traced to the specific
request that caused it.

The correlation ID is logged. Whether it is also returned to the client
is not specified, and must not be assumed.

### Transaction Boundaries

Retries replay the whole transaction. Stock validation, the balance
update, and the movement creation therefore remain inside a single
transaction, and must not be split across retries.

---

## 6. Authentication

Protected endpoints require authenticated sessions.

---

## 7. Authorization

Each endpoint must define the required permission.

Example:

POST /api/deliveries

Required:

delivery.create

---

## 8. Idempotency

Financial and inventory-changing operations should support safe duplicate-submission handling.

Where appropriate, use an idempotency key or equivalent server-side mechanism.

---

## 9. Pagination

List endpoints should support pagination.

Avoid returning unlimited records.

---

## 10. Filtering

Filtering should support only explicitly permitted fields.

Do not dynamically expose arbitrary database columns.

---

## 11. Rate Limiting

Apply rate limits to:

- Authentication
- Expensive reports
- Exports
- Sensitive state-changing endpoints
