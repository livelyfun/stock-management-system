# Entity Relationship Design

## Core Relationships

```mermaid
erDiagram

    USERS ||--o{ AUDIT_LOGS : creates

    CUSTOMERS ||--o{ DELIVERIES : receives
    EMPLOYEES ||--o{ DELIVERIES : handles
    DELIVERIES ||--|{ DELIVERY_ITEMS : contains
    PRODUCTS ||--o{ DELIVERY_ITEMS : sold

    CUSTOMERS ||--o{ RETURNS : makes
    DELIVERIES ||--o{ RETURNS : referenced_by
    RETURNS ||--|{ RETURN_ITEMS : contains
    PRODUCTS ||--o{ RETURN_ITEMS : returned

    CUSTOMERS ||--o{ INVOICES : billed
    INVOICES ||--|{ INVOICE_ITEMS : contains
    PRODUCTS ||--o{ INVOICE_ITEMS : included

    CUSTOMERS ||--o{ PAYMENTS : makes
    PAYMENTS ||--o{ PAYMENT_ALLOCATIONS : allocated_to
    INVOICES ||--o{ PAYMENT_ALLOCATIONS : receives

    PRODUCTS ||--o{ INVENTORY_MOVEMENTS : affects
    WAREHOUSES ||--o{ INVENTORY_MOVEMENTS : records

    PRODUCTS ||--o{ INVENTORY_BALANCES : has
    WAREHOUSES ||--o{ INVENTORY_BALANCES : holds

    PRODUCTS ||--o{ PRODUCT_WAREHOUSE_SETTINGS : configured_by
    WAREHOUSES ||--o{ PRODUCT_WAREHOUSE_SETTINGS : threshold_for

    CUSTOMERS ||--o{ CUSTOMER_LEDGER : owns
    EMPLOYEES ||--o{ EMPLOYEE_LEDGER : owns
```

---

## Inventory Relationships

`INVENTORY_BALANCES` is keyed by `(product_id, warehouse_id)`. A product
has one balance per warehouse, and a warehouse holds one balance per
product.

`PRODUCT_WAREHOUSE_SETTINGS` carries the per-warehouse minimum-stock
threshold and is keyed by the same `(product_id, warehouse_id)` pair. It
is master data and is independent of whether a balance row exists.

---

## Release Status

`WAREHOUSES`, `INVENTORY_MOVEMENTS`, `INVENTORY_BALANCES`, and
`PRODUCT_WAREHOUSE_SETTINGS` are active in the MVP.

Container tracking, and therefore container movement entities, is
deferred.
