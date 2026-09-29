# Delivery API

## Create Draft

POST /api/deliveries

Creates a delivery in DRAFT state.

Must include:

- Customer
- Employee / delivery staff
- Warehouse
- Items

The warehouse identifies where the delivery is fulfilled from. It is
required, because the inventory it will affect is warehouse-scoped.

---

## Confirm

POST /api/deliveries/:id/confirm

Transitions:

DRAFT → CONFIRMED

---

## Post

POST /api/deliveries/:id/post

Transitions:

CONFIRMED → POSTED

Posting must:

- Validate authorization
- Validate customer
- Validate employee
- Validate warehouse
- Validate products
- Validate quantities
- Determine authoritative prices
- Calculate totals
- Create inventory movements against the delivery's warehouse
- Update inventory balances for the delivery's warehouse, enforcing the
  zero floor
- Create invoice where applicable
- Update customer ledger
- Create audit event

All required effects must be atomic.

If posting would cause on-hand for any line to fall below zero in that
warehouse, the delivery is rejected and rolled back. There is no
override.

---

## Void

POST /api/deliveries/:id/void

Only authorized users may void a posted delivery.

Voiding must preserve historical information and use the controlled reversal mechanism.

---

## Get Delivery

GET /api/deliveries/:id

Returns the delivery including its warehouse.

---

## List Deliveries

GET /api/deliveries

Supports:

- Date range
- Customer
- Employee
- Status
- Payment status
- Pagination

### No Warehouse Filter

This endpoint does not support a warehouse filter in the MVP. The
documented filters above are unchanged.

Individual delivery records remain warehouse-identifiable, because the
delivery record carries `warehouse_id`. A warehouse filter is a
filtering requirement, and filtering requirements must not be invented.
