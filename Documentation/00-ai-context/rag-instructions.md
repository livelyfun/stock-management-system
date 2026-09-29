# RAG Instructions — Stock Management System

## Purpose

This directory contains the authoritative project knowledge for the Stock Management System.

AI coding agents must use these documents as project context.

---

## Source of Truth

The documents define:

- Business requirements
- Business rules
- Architecture
- Database design
- Security requirements
- API behavior
- UI requirements
- Workflows
- Testing requirements
- Deployment requirements

---

## Priority

When implementing a feature:

1. Follow explicit business rules.
2. Follow security requirements.
3. Follow database integrity requirements.
4. Follow architecture decisions.
5. Follow API contracts.
6. Follow UI specifications.
7. Follow testing requirements.

---

## Do Not

Do not:

- Invent business rules
- Trust frontend calculations
- Bypass authorization
- Directly modify posted transactions
- Directly modify inventory balances without a transaction
- Delete financial history
- Expose database credentials
- Store secrets in source control
- Ignore database constraints
- Create unrestricted administrative endpoints

---

## Transaction Principle

Business transactions affecting multiple records must be atomic.

---

## Security Principle

The browser is untrusted.

All important validation and authorization must happen server-side.

---

## Inventory Principle

Inventory movement history is authoritative.

Current balances are derived/cached state.

---

## Financial Principle

Customer ledger history is authoritative.

Posted financial transactions must remain auditable.

---

## Change Principle

If implementation requires changing an established architecture decision or business rule:

1. Identify the conflict.
2. Explain the reason for the proposed change.
3. Update the appropriate documentation.
4. Record the decision.
5. Then implement the change.

---

## Ambiguity

If the documents do not define a required business behavior:

Do not silently invent a business rule.

Identify the ambiguity and request clarification or document the proposed decision before implementation.

---

## Coding Agent Behavior

Before implementing a feature:

1. Identify relevant documentation.
2. Retrieve the applicable business rules.
3. Retrieve security requirements.
4. Retrieve database requirements.
5. Check architecture decisions.
6. Implement.
7. Add tests.
8. Verify authorization.
9. Verify transaction integrity.
10. Update documentation if required.

---

## RAG Maintenance

The local knowledge base is maintained from `Documentation/`:

- Run `python rag/ingest.py` (venv at `.rag/venv`) after adding or
  editing documentation to refresh the Qdrant index.
- Ingestion skips unchanged files. Bumping `SCHEMA_VERSION` in
  `rag/config.py` rebuilds the whole collection when the indexing
  format changes.
- Run `python rag/evaluate.py --k 5` (from `rag/`) to verify retrieval
  quality against `rag/golden.json` golden questions. Use it to check
  for regressions after chunking or ranking changes.
- The embedding model is cached under `.rag/model_cache` so it survives
  reboots.
