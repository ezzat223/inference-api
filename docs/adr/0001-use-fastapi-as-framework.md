# ADR-0001: Use FastAPI as the API Framework

## Status

Accepted

## Date

2026-03-03

## Context

We need a Python web framework to serve the inference API. The service
needs to handle async requests efficiently, provide automatic OpenAPI
docs, and have strong typing support.

## Decision

We will use FastAPI as the web framework for the inference API.

## Alternatives Considered

### Flask

- ✅ Simple, widely known
- ❌ No native async support
- ❌ No automatic OpenAPI generation

### Django REST Framework

- ✅ Batteries included
- ❌ Too heavyweight for a focused inference API
- ❌ Slower request handling

### FastAPI

- ✅ Native async/await support
- ✅ Automatic OpenAPI/Swagger docs
- ✅ Built-in type validation via Pydantic
- ✅ High performance (Starlette-based)

## Consequences

### Positive

- Fast development with automatic validation
- Free interactive API docs at /docs
- Easy async inference calls

### Negative

- Smaller ecosystem than Flask/Django
- Team needs to learn Pydantic models
