# LLM Inference API

The **LLM Inference API** is the central serving layer for all fine-tuned language models at the company.
It exposes an OpenAI-compatible interface, meaning any client already using the OpenAI Python SDK
can switch to our internal models by changing a single base URL — no other code changes required.

---

## At a Glance

| Property | Value |
| --- | --- |
| **Owner** | MLOps Team |
| **Language** | Python 3.11 / FastAPI |
| **Status** | Production |
| **SLA** | 99.9% uptime / p99 < 300ms |
| **Slack** | `#mlops-inference` |
| **On-Call** | PagerDuty — *MLOps Inference* rotation |

---

## Supported Models

| Model ID | Base Model | Fine-tune Task | Max Tokens | p99 Latency |
| --- | --- | --- | --- | --- |
| `llama3-8b-ft-v2` | Llama 3 8B | Internal Q&A + RAG | 4096 | 120ms |
| `mistral-7b-ft-v1` | Mistral 7B | Code generation | 8192 | 180ms |
| `gpt2-custom-v3` | GPT-2 | Text classification | 2048 | 45ms |

---

## Quick Start

=== "OpenAI SDK (Python)"

```python
    from openai import OpenAI

    client = OpenAI(
        base_url="http://inference-api.internal/v1",
        api_key="not-needed",
    )

    response = client.chat.completions.create(
        model="llama3-8b-ft-v2",
        messages=[{"role": "user", "content": "Summarise this week's model eval results."}],
    )
    print(response.choices[0].message.content)
```

=== "curl"

```bash
    curl http://inference-api.internal/v1/chat/completions \
      -H "Content-Type: application/json" \
      -d '{
        "model": "llama3-8b-ft-v2",
        "messages": [{"role": "user", "content": "Hello"}]
      }'
```

=== "Streaming"

```python
    stream = client.chat.completions.create(
        model="llama3-8b-ft-v2",
        messages=[{"role": "user", "content": "Write a haiku about MLOps."}],
        stream=True,
    )
    for chunk in stream:
        print(chunk.choices[0].delta.content or "", end="")
```

---

## Key Links

| Resource | URL |
| --- | --- |
| GitHub | [ezzat223/inference-api](https://github.com/ezzat223/inference-api) |
| Staging | `http://inference-api.staging.internal` |
| Production | `http://inference-api.internal` |
