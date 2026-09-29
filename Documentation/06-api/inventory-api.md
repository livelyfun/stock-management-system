# Inventory API

## Stock

GET /api/inventory

Supports:

- Product
- Warehouse
- Pagination
- Search

---

## Stock Movements

GET /api/inventory/movements

Supports:

- Product
- Warehouse
- Movement type
- Date range
- Pagination

---

## Stock Adjustment

POST /api/inventory/adjustments

Requires:

inventory.adjust

Must include:

- Product
- Warehouse
- Quantity
- Direction
- Movement type
- Reason

`Quantity` must be a positive value. `Direction` must be either `IN` or
`OUT`.

`Movement type` must be one of the MVP-enabled adjustment movement
types:

- Adjustment
- Damage
- Loss

Must create:

- Inventory movement
- Balance update
- Audit event

inside the appropriate database transaction.

---

## Negative Stock Rejection

An adjustment with direction `OUT` must be rejected if it would cause
the on-hand quantity for that product in that warehouse to fall below
zero.

There is no override parameter and no override permission. A rejected
request must not create a movement, must not change the balance, and
must not leave partial state.

Validation is performed server-side against the locked balance row
inside the transaction, not by the client.

---

## Deferred Movement Types

The controlled movement vocabulary contains the broader target domain,
including Production, Purchase, and Transfer.

Those values must be rejected by this endpoint in the MVP. They are not
usable merely because they exist in the vocabulary.

---

## Important Rule

The API must never expose an unrestricted endpoint that directly modifies inventory balance.
