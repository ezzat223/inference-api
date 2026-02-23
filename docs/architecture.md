# Architecture

## System Overview

```yaml
┌─────────────────────────────────────────────────────┐
│                      Clients                         │
│        (Python SDK / curl / Internal Services)       │
└──────────────────────┬──────────────────────────────┘
                       │  HTTP  (OpenAI-compatible)
                       ▼
┌─────────────────────────────────────────────────────┐
│              Inference API (this service)            │
│                                                      │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │ FastAPI App │─▶│  Inference   │─▶│   Model    │  │
│  │ +Middleware │  │  Service     │  │  Registry  │  │
│  └─────────────┘  └──────────────┘  └────────────┘  │
│                          │                           │
└──────────────────────────┼───────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
   ┌────────────┐  ┌─────────────┐  ┌────────────┐
   │ Llama 3 8B │  │ Mistral 7B  │  │ GPT-2      │
   │ Backend    │  │ Backend     │  │ Backend    │
   └────────────┘  └─────────────┘  └────────────┘
```

---

## Component Responsibilities

### Inference API

- **Request routing** — resolves model name → backend URL via the model registry
- **Schema validation** — enforces OpenAI-compatible request/response schemas via Pydantic
- **Streaming** — proxies SSE chunks from backends to clients
- **Observability** — emits structured logs and Prometheus metrics for every request
- **Resilience** — falls back to a static model catalogue if the registry is down

### Model Registry

A separate internal service that stores model metadata: name, version, backend URL, hardware requirements, and owner.

### Model Backends

Each fine-tuned model runs on a dedicated backend pod (vLLM or Text Generation Inference).

---

## Request Lifecycle

```text
1. Client sends POST /v1/chat/completions
2. LoggingMiddleware assigns request_id and starts timer
3. Pydantic validates the request body (returns 422 on failure)
4. InferenceService looks up backend_url from registry cache
5. Request is forwarded to the backend over HTTP
6. Response is validated and returned to client
7. Prometheus metrics are updated automatically
```

---

## Technology Choices

| Decision | Choice | Reason |
| --- | --- | --- |
| Web framework | FastAPI | Native async, auto OpenAPI docs, Pydantic integration |
| HTTP client | httpx | Async-native, streaming support |
| Schema validation | Pydantic v2 | Speed, OpenAI schema compatibility |
| Metrics | prometheus-fastapi-instrumentator | Zero-config Prometheus metrics |
| Container base | python:3.11-slim | Minimal attack surface |
