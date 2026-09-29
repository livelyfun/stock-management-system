# Production Deployment

## Architecture

Internet / Local Network
↓
HTTPS / Reverse Proxy
↓
Web Application
↓
Private PostgreSQL
↓
Backups

Optional:

Redis
Object Storage
Monitoring
Background Workers

---

## Production Principles

### Database

PostgreSQL must not be publicly exposed.

---

### HTTPS

Production traffic must use HTTPS.

---

### Secrets

Use secure environment variables or a secret manager.

Never commit production secrets.

---

### Database Migrations

Production deployment must apply database migrations safely.

Migration history must be tracked.

---

### Monitoring

Production should monitor:

- Application health
- Database health
- Errors
- Resource usage
- Background jobs
- Backup status

---

### Health Checks

Provide appropriate health checks for application and infrastructure.

---

## Deployment Safety

Before deployment:

- Run tests
- Run type checks
- Run linting
- Run security/dependency checks
- Verify migrations
- Verify backups

---

## Rollback

A documented rollback procedure must exist for:

- Application deployment
- Database migration failures
- Configuration errors
