# Customer API

## List Customers

GET /api/customers

Supports:

- Search
- Status
- Customer type
- Pagination

---

## Get Customer

GET /api/customers/:id

Must enforce object-level authorization where required.

---

## Create Customer

POST /api/customers

Requires:

customer.create

Server validates all fields.

---

## Update Customer

PATCH /api/customers/:id

Requires:

customer.update

---

## Deactivate Customer

POST /api/customers/:id/deactivate

Requires appropriate permission.

Do not physically delete historical customer records if doing so would break transaction history.

---

## Customer Ledger

GET /api/customers/:id/ledger

Returns authorized customer financial history.

---

## Customer Balance

GET /api/customers/:id/balance

Returns the current authorized balance.
