# Reporting API

## Sales

GET /api/reports/sales

Supports:

- Date range
- Customer
- Product
- Employee

---

## Inventory

GET /api/reports/inventory

Supports:

- Product
- Warehouse
- Date range
- Movement type

The warehouse and movement-type filters belong to the reporting
endpoint. They are distinct from `GET /api/deliveries`, which has no
warehouse filter in the MVP.

The movement-type filter reports only the MVP-enabled types, because
deferred types cannot be created in the MVP.

---

## Customer

GET /api/reports/customers

Includes:

- Purchases. **Post-MVP — deferred.**
- Payments
- Outstanding balances

Purchases cannot be created in the MVP, so this line reports no data
until purchasing ships.

---

## Employee

GET /api/reports/employees

Includes:

- Deliveries
- Collections
- Returns
- Outstanding amounts

---

## Credit

GET /api/reports/credit

Includes:

- Outstanding balances
- Due amounts
- Overdue amounts

---

## Export

Exports should eventually support:

- CSV
- Excel
- PDF

Large exports should be processed as background jobs where required.

---

## Security

Reports must enforce authorization.

A user must not be able to access information outside their permitted scope.
