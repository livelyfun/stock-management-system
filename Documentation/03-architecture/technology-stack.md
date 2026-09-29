# Technology Stack

## Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- Responsive UI

---

## Backend

Start with Next.js server/API capabilities.

Architecture style:

Modular Monolith

A dedicated API layer such as NestJS or Fastify may be introduced later if required by scale.

---

## Database

PostgreSQL.

Reasons:

- Strong transaction guarantees
- Referential integrity
- Constraints
- Reporting/query capabilities
- Mature ecosystem

---

## Data Access

Use a typed ORM/query builder.

Candidates:

- Drizzle ORM
- Prisma

The final choice should be recorded as an architecture decision.

---

## Cache / Background Jobs

Redis may be used for:

- Rate limiting
- Temporary cache
- Background job coordination

---

## File Storage

S3-compatible object storage may be used for:

- Generated documents
- Attachments
- Export files

---

## Testing

The implementation should include automated tests covering:

- Business rules
- Authorization
- Security
- Database behavior
- Transaction behavior

---

## Development Principles

- TypeScript
- Database migrations
- Automated tests
- Code quality checks
- Security scanning
- Dependency scanning
