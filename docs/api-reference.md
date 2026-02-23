# API Reference

The Inference API is fully **OpenAI-compatible**. Any code written against the OpenAI API will work
by simply changing the `base_url`.

---

## Base URLs

| Environment | URL |
| --- | --- |
| Local | `http://localhost:8000` |
| Staging | `http://inference-api.staging.internal` |
| Production | `http://inference-api.internal` |

---

## Endpoints

### `GET /healthz` — Liveness Probe

Returns `200 OK` if the process is alive. Used by Kubernetes liveness probes.

```json
{"status": "ok", "version": "1.0.0"}
```

---

### `GET /readyz` — Readiness Probe

Returns `200 OK` only when the model registry has loaded at least one model.
Returns `503` when no models are available.

---

### `GET /metrics` — Prometheus Metrics

Exposes request count, latency histograms, and error rates in Prometheus format.

---

### `GET /v1/models` — List Models

```json
{
  "object": "list",
  "data": [
    {"id": "llama3-8b-ft-v2", "object": "model", "owned_by": "mlops-team"},
    {"id": "mistral-7b-ft-v1", "object": "model", "owned_by": "mlops-team"},
    {"id": "gpt2-custom-v3",   "object": "model", "owned_by": "mlops-team"}
  ]
}
```

---

### `POST /v1/chat/completions` — Chat Completion

| Field | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `model` | string | ✅ | — | Model ID from `/v1/models` |
| `messages` | array | ✅ | — | Conversation history |
| `max_tokens` | int | ❌ | 512 | Max tokens to generate (cap: 8192) |
| `temperature` | float | ❌ | 0.7 | Sampling temperature (0.0–2.0) |
| `top_p` | float | ❌ | 1.0 | Nucleus sampling (0.0–1.0) |
| `stream` | bool | ❌ | false | Enable SSE streaming |
| `stop` | string/array | ❌ | null | Stop sequences |
| `n` | int | ❌ | 1 | Number of completions (max: 4) |

**Example Request**

```bash
curl http://inference-api.internal/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3-8b-ft-v2",
    "messages": [
      {"role": "system", "content": "You are a helpful MLOps assistant."},
      {"role": "user", "content": "What metrics should I track for my LLM in production?"}
    ],
    "max_tokens": 256,
    "temperature": 0.5
  }'
```

**Example Response**

```json
{
  "id": "chatcmpl-a1b2c3d4e5f6",
  "object": "chat.completion",
  "model": "llama3-8b-ft-v2",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Track latency (p50/p95/p99), token throughput, error rate, cost per request, and output quality scores."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 28,
    "completion_tokens": 42,
    "total_tokens": 70
  }
}
```

---

## Error Codes

| HTTP Code | Meaning |
| --- | --- |
| `422` | Request validation failed (bad parameters) |
| `404` | Model not found in registry |
| `502` | Backend model server error |
| `503` | Service not ready (no models loaded) |
