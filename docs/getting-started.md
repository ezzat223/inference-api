# Getting Started

This guide gets you from zero to running the API locally in under 10 minutes.

---

## Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Git access to `ezzat223/inference-api`

---

## 1. Clone the Repo

```bash
git clone https://github.com/ezzat223/inference-api.git
cd inference-api
```

## 2. Set Up a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## 3. Run Locally

```bash
docker compose up
```

The API will be available at `http://localhost:8000`.

## 4. Test the API

```bash
# Health check
curl http://localhost:8000/healthz

# List available models
curl http://localhost:8000/v1/models

# Send a completion request
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3-8b-ft-v2",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## 5. View Interactive API Docs

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## 6. Run Tests

```bash
pytest
```

---

## Common Issues

!!! warning "Model registry unreachable"
    If you see `Registry unreachable, falling back to static catalogue` in logs — that is expected in local dev.
    The service falls back to a built-in list of models automatically.

!!! tip "Hot reload in development"
    `docker compose up` mounts `./src` into the container, so code changes are reflected immediately without rebuilding.
