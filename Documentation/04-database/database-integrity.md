# Database Integrity Requirements

Application validation must be supported by database-level constraints.

---

## Required Constraints

Examples:

- Quantity > 0 for normal sales/return lines
- Quantity > 0 for every inventory movement, without exception
- Inventory balance quantity >= 0
- Monetary amounts >= 0 where appropriate
- Unique SKU
- Unique delivery number
- Unique invoice number
- Unique payment/receipt number
- Foreign keys for transaction references
- NOT NULL on required fields
- NOT NULL on `warehouse_id` for warehouse-scoped inventory records
- Controlled status values

### Movement Quantity

Inventory movement quantity is always positive, and the direction of the
movement determines its effect. The `quantity > 0` rule is unconditional
for inventory movements and must not be relaxed per movement type.

### Inventory Balance

`inventory_balances` must be constrained so that its quantity cannot
become negative. Combined with the row-level locking described in the
inventory model, this is the database-level expression of the negative
stock prohibition.

The primary key of `inventory_balances` is:

(product_id, warehouse_id)

---

## Referential Integrity

Transaction references should use foreign keys.

Examples:

Delivery item → Delivery

Delivery item → Product

Delivery → Warehouse

Invoice item → Invoice

Invoice item → Product

Payment allocation → Payment

Payment allocation → Invoice

Inventory movement → Product

Inventory movement → Warehouse

Inventory balance → Product

Inventory balance → Warehouse

Product warehouse setting → Product

Product warehouse setting → Warehouse

---

## Unique Business Numbers

The database must enforce uniqueness for generated business identifiers.

Examples:

- Delivery number
- Invoice number
- Payment number
- Return number
- Receipt number

---

## Defense in Depth

Important business rules should be protected by both:

1. Application validation
2. Database constraints
