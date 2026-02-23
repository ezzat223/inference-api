# Configuration

All configuration is injected via environment variables.

---

## Variables Reference

### Application

| Variable | Default | Description |
| --- | --- | --- |
| `APP_ENV` | `development` | Environment name |
| `LOG_LEVEL` | `INFO` | Python log level |
| `ALLOWED_ORIGINS` | `["*"]` | CORS allowed origins |

### Model Registry

| Variable | Default | Description |
| --- | --- | --- |
| `MODEL_REGISTRY_URL` | `http://model-registry:8000` | Base URL of the internal model registry |

### Inference Limits

| Variable | Default | Description |
| --- | --- | --- |
| `MAX_TOKENS_LIMIT` | `8192` | Hard cap on max_tokens |
| `DEFAULT_MAX_TOKENS` | `512` | Default when client doesn't specify |
| `DEFAULT_TEMPERATURE` | `0.7` | Default sampling temperature |
| `REQUEST_TIMEOUT_SECONDS` | `120` | Timeout for backend model requests |

---

## `.env.example`

```bash
APP_ENV=development
LOG_LEVEL=DEBUG
MODEL_REGISTRY_URL=http://localhost:8001
MAX_TOKENS_LIMIT=8192
DEFAULT_MAX_TOKENS=512
REQUEST_TIMEOUT_SECONDS=120
```
