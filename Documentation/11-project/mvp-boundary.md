# MVP Boundary

## Authority

This document is authoritative for MVP scope.

Where another document describes a capability that falls outside the MVP,
this document governs. The inventory movement vocabulary is broader than
the MVP-enabled set, and this document records which types are enabled.

---

## Included in MVP

The first usable business release should include:

- Authentication
- Roles
- Customers
- Employees
- Products
- Inventory
- Warehouses
- Deliveries
- Returns
- Invoices
- Payments
- Receipts
- Customer Credit
- Customer Ledger
- Search
- Core Reports
- Audit Logs

---

## Multiple Warehouses

Multiple warehouses are inside the MVP.

Inventory is scoped to a warehouse, the delivery record carries its
warehouse, and the current balance is maintained per product and
warehouse.

The following are explicitly outside the MVP even though multiple
warehouses are inside it:

- Warehouse transfers
- Warehouse-scoped pricing
- Warehouse-scoped authorization

---

## MVP-Enabled Inventory Movement Types

Enabled in the MVP:

- Opening Stock
- Delivery
- Return
- Adjustment
- Damage
- Loss

Deferred, and not usable in the MVP:

- Production
- Purchase
- Transfer

Damage and Loss are recorded through the adjustments mechanism as their
own movement types, so they remain distinguishable in the authoritative
history.

---

## Outside Initial MVP

The following may be implemented later:

- Advanced container tracking
- Route planning
- Messaging
- Payroll
- Purchasing
- Production
- Warehouse transfers
- Tax/accounting expansion
- Customer portal
- Multiple branches
- Advanced vehicle management

---

## Governing Decisions

- ADR-009 — Negative on-hand stock is prohibited
- ADR-010 — Warehouse is a core inventory dimension
- ADR-011 — Movement vocabulary versus MVP-enabled movement types
- ADR-012 — Row-level locking on inventory balances
- ADR-013 — Positive movement quantity with direction
- ADR-014 — Inventory balance key
- ADR-015 — Minimum stock is per-warehouse
- ADR-016 — Transaction retry policy
- ADR-017 — No warehouse filter on the delivery list endpoint
- ADR-018 — Movement sign convention does not apply to the financial ledger

---

## MVP Principle

The MVP must first establish a reliable transaction system.

Advanced features must not compromise:

- Inventory consistency
- Financial correctness
- Security
- Auditability
