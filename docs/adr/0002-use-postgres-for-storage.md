# ADR-0002: Use PostgreSQL for Model Metadata Storage

## Status

Accepted

## Date

2026-03-03

## Context

The inference API needs persistent storage for model metadata, inference
request logs, and experiment tracking. The data is structured and
relational in nature — models have versions, versions have metrics, and
requests are tied to specific model versions. We need a storage solution
that handles concurrent reads efficiently since inference requests arrive
in high volume.

## Decision

We will use PostgreSQL as the primary database for the inference API.

## Alternatives Considered

### SQLite

- ✅ Zero setup, embedded in the application
- ✅ Great for local development and testing
- ❌ No support for concurrent writes — inference workers would block each other
- ❌ Not suitable for multi-instance deployments
- ❌ No connection pooling

### MongoDB

- ✅ Flexible schema — easy to store unstructured model outputs
- ✅ Horizontal scaling via sharding
- ❌ No team experience with MongoDB operations
- ❌ Transactions are more complex than SQL
- ❌ Overkill for our structured, relational data model

### Redis

- ✅ Extremely fast reads — good for caching inference results
- ❌ Not a primary database — data is not durable by default
- ❌ Not designed for complex relational queries
- ✅ Will be used alongside PostgreSQL as a caching layer (see ADR-0003)

### PostgreSQL

- ✅ Battle-tested for high-concurrency workloads
- ✅ Strong ACID guarantees for request logging
- ✅ Native JSON column support for storing model output payloads
- ✅ Team has existing expertise
- ✅ Works seamlessly with SQLAlchemy and Alembic for migrations
- ❌ Requires a running instance (managed via Docker in dev, RDS in prod)

## Consequences

### Positive

- Reliable concurrent read/write handling for high-volume inference traffic
- Schema migrations managed cleanly with Alembic
- Native JSONB columns let us store flexible model outputs without
  sacrificing queryability
- Easy integration with existing Python tooling (SQLAlchemy, asyncpg)

### Negative

- Developers need Docker running locally to spin up a PostgreSQL instance
- Schema migrations must be managed carefully as the API evolves
- Connection pool sizing needs tuning as inference traffic scales

## References

- [PostgreSQL Documentation](https://www.postgresql.org/docs/current/index.html)
- [Alembic Documentation](https://alembic.sqlalchemy.org/en/latest/)
- [asyncpg Documentation](https://magicstack.github.io/asyncpg/current/)