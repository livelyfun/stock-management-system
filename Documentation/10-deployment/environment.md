# Environment Configuration

## Environments

At minimum:

- Development
- Production

A staging environment may be introduced later.

---

## Development

Development configuration must not use production secrets.

---

## Production

Production must use:

- Secure secrets
- HTTPS
- Production database
- Production backup configuration
- Production monitoring

---

## Environment Variables

Potential configuration categories:

### Database

DATABASE_URL

### Authentication

AUTH_SECRET

### Redis

REDIS_URL

### Object Storage

Storage credentials/configuration

### Application

Application URL
Environment name

---

## Secret Rules

Never:

- Commit secrets
- Put secrets in frontend code
- Log secrets
- Store secrets in audit logs

---

## Secret Rotation

Secrets must be rotatable without changing source code.
