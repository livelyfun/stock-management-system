# Authorization Tests

## Roles

Test each role independently:

- Super Admin
- Admin
- Manager
- Accountant
- Inventory Staff
- Delivery Staff
- Viewer

---

## Test Cases

Verify:

- Viewer cannot create transactions.
- Delivery Staff cannot perform administrative operations.
- Inventory Staff cannot perform unauthorized financial actions.
- Accountant cannot modify restricted inventory operations unless explicitly permitted.
- Low-privilege users cannot access admin endpoints.
- Users cannot access unauthorized customer records.
- Users cannot access unauthorized employee records.

---

## API Security

Attempt restricted operations directly through API requests.

Authorization must remain enforced.

---

## Browser Manipulation

Changing frontend state or request payloads must not bypass authorization.
