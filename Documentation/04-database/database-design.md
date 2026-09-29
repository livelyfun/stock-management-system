# Database Design

## 1. Database

PostgreSQL is the primary transactional database.

---

## 2. Core Tables

### Authentication

- users
- roles
- permissions
- user_roles

### Employees

- employees

### Customers

- customers
- customer_addresses

### Products

- products
- product_categories
- price_history

### Inventory

- warehouses
- inventory_movements
- inventory_balances
- product_warehouse_settings

`warehouses` is active in the MVP. Multiple warehouses are supported from
the start, with inventory scoped to a warehouse.

`inventory_balances` is keyed by `(product_id, warehouse_id)`.

`product_warehouse_settings` holds the per-warehouse minimum-stock
threshold. It is master data, not a derived balance, so a threshold can
be set before any stock exists for that product and warehouse pair.

### Sales

- deliveries
- delivery_items
- returns
- return_items

`deliveries` carries `warehouse_id`, identifying the warehouse the
delivery is fulfilled from.

### Finance

- invoices
- invoice_items
- payments
- payment_allocations

### Ledgers

- customer_ledger
- employee_ledger

### Other

- receipts
- attachments
- audit_logs

### Deferred

- container_movements

Container tracking is deferred. The `container_movements` table is not
part of the MVP. Reusable container handling remains a long-term
objective, and the table is introduced only when container tracking is
scheduled.

---

## 3. Design Principle

Database design must preserve:

- Referential integrity
- Transaction history
- Auditability
- Unique business identifiers
- Required fields
- Valid status values

---

## 4. Current Balance Tables

Current balance tables may be maintained for performance.

They must remain consistent with transaction history.

They must not become uncontrolled manual fields.

### Balance Tables Versus Master Data

`inventory_balances` is a maintained current-state table. It is not the
authoritative history, and it must not carry manually configured values.

`product_warehouse_settings` is master data and is therefore not a
current balance table. The current balance rule does not apply to it;
it is edited by configuration, not by inventory transactions.

---

## 5. Historical Data

Posted transaction records must preserve the actual values used at posting time.

Examples:

- Unit price
- Quantity
- Customer
- Employee
- Product
- Transaction date
