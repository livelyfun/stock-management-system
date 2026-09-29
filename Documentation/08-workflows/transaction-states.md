# Transaction State Models

## Delivery

DRAFT
↓
CONFIRMED
↓
POSTED

Optional controlled path:

POSTED
↓
VOIDED / REVERSED

---

## General Principle

A posted transaction is considered final.

It cannot be freely edited.

Corrections use controlled reversal or adjustment workflows.

---

## Why

This protects:

- Financial history
- Inventory history
- Auditability
- Accountability

---

## State Transition Rules

State transitions must:

- Be explicitly defined
- Be authorized
- Be validated server-side
- Create audit events where sensitive
- Preserve history
