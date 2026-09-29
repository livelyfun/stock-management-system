# Audit Logging

## 1. Purpose

Audit logging provides traceability for sensitive security and business operations.

---

## 2. Minimum Events

Record:

- Login success
- Login failure
- Password reset
- User created
- Role changed
- Customer created/updated
- Product created/updated
- Price changed
- Delivery created
- Delivery posted
- Delivery voided
- Return created
- Payment created
- Payment voided
- Stock adjusted
- Credit adjusted
- Settings changed

---

## 3. Audit Record

Suggested fields:

```text
audit_id
actor_user_id
action
entity_type
entity_id
old_value
new_value
ip_address
user_agent
request_id
created_at
```

---

## 4. Correlation With Request Logging

`request_id` carries the request or correlation ID for the operation
that produced the audit record.

A transaction that fails after exhausting its retries is recorded in the
server log with this same identifier, so a failed attempt can be traced
to the request that caused it and to any related audit entries.

The identifier is logged server-side. Whether it is also returned to the
client is not specified.
