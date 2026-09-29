# Definition of Done

## Core Business Transaction

A transaction feature is not considered complete until:

- Authorization is enforced
- Input is validated
- Product references are valid
- Customer references are valid
- Employee references are valid
- Price is authoritative
- Quantity rules are enforced
- Inventory changes atomically
- Invoice is created where applicable
- Ledger is updated where applicable
- Audit event is recorded
- Duplicate submission is handled safely
- Error paths roll back correctly
- Automated tests cover important business rules

---

## Security

The feature must also verify:

- Server-side authorization
- Secure input handling
- No sensitive information leakage
- Appropriate audit logging
- Appropriate rate limiting where required

---

## Database

Verify:

- Required constraints
- Foreign keys
- Unique identifiers
- Correct transaction behavior
- Migration included

---

## UI

Verify:

- Appropriate role visibility
- Validation feedback
- Loading state
- Error state
- Success state
- Duplicate-submission protection
- Responsive behavior

---

## Documentation

A significant feature should update the relevant project documentation and architecture decisions where required.
