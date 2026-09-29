# System Architecture

## 1. Architecture Style

The initial application architecture is a modular monolith.

The system should be implemented as one deployable application while maintaining clear internal module boundaries.

---

## 2. High-Level Architecture

Browser
↓
HTTPS / Reverse Proxy
↓
Next.js Web Application
↓
Authentication
↓
Authorization
↓
Input Validation
↓
Business Rules
↓
PostgreSQL

Supporting services:

- Redis
- Object Storage
- Background Workers
- Monitoring
- Backups

---

## 3. Browser Security Boundary

The browser must never connect directly to PostgreSQL.

All protected operations must pass through the application server.

---

## 4. Application Layers

Recommended logical layers:

### Presentation

- Web pages
- Forms
- Tables
- Dashboards
- Reports

### API / Server

- Request validation
- Authentication
- Authorization
- Request handling

### Business Layer

- Business rules
- Transaction orchestration
- Financial calculations
- Inventory logic

### Data Layer

- Database queries
- ORM/query builder
- Transactions
- Constraints

### Infrastructure

- Redis
- Object storage
- Backups
- Logging
- Monitoring

---

## 5. Core Modules

- Authentication
- Authorization
- Users
- Customers
- Employees
- Products
- Pricing
- Warehouses
- Inventory
- Deliveries
- Returns
- Invoices
- Payments
- Customer Ledger
- Employee Ledger
- Receipts
- Reports
- Audit
- Settings

---

## 6. Transaction Principle

A business operation that affects multiple business records must be treated as one logical transaction.

Example:

Delivery
→ Inventory
→ Invoice
→ Customer Ledger
→ Audit

must either succeed together or roll back together.
