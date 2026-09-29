# Return API

## Create Return

POST /api/returns

Must include:

- Customer
- Original delivery
- Warehouse
- Product
- Quantity
- Condition
- Reason

`Warehouse` is the warehouse that receives the returned stock.

If `Warehouse` is omitted, it defaults to the warehouse of the original
delivery. A different warehouse may be sent explicitly.

---

## Validation

Server must verify:

- Delivery exists
- Customer matches
- Warehouse exists
- User is authorized to record a return into that warehouse
- Product belongs to delivery
- Quantity is eligible
- User is authorized

A return must not be rejected for insufficient stock. A return adds
stock, so the zero floor does not apply.

---

## Posting

A posted return must:

- Create return record
- Create return items
- Create an inventory movement with direction `IN` and a positive
  quantity, recorded against the return's warehouse
- Lock and update the balance row for that product in that warehouse
- Apply financial adjustment where applicable
- Update ledger where applicable
- Create audit event

The movement, the balance update, and the ledger adjustment are
committed atomically.

---

## Get Return

GET /api/returns/:id

Returns the return including its warehouse.

---

## List Returns

GET /api/returns

Supports:

- Customer
- Employee
- Product
- Date range
- Pagination
