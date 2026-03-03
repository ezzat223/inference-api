# LLM Inference API

OpenAI-compatible inference service for fine-tuned LLMs.

## Backstage Entity Metadata

This repository is registered in Backstage via `catalog-info.yaml` with:

- `name`: `inference-api`
- `type`: `service`
- `lifecycle`: `production`
- `owner`: `xops-team`
- `backstage.io/kubernetes-id`: `demo-app`
- `backstage.io/kubernetes-namespace`: `default`
- `github.com/project-slug`: `ezzat223/inference-api`
- `backstage.io/techdocs-ref`: `dir:.`

## Local Backstage + Kubernetes Demo

Apply demo resources labeled for Backstage discovery:

```bash
kubectl apply -f k8s/backstage-demo.yaml
kubectl get deploy,po,svc -n default -l backstage.io/kubernetes-id=demo-app
```

Then open the component in Backstage and verify:

- GitHub card (repo linkage)
- Docs tab (TechDocs)
- Kubernetes tab (deployment, pods, service)

## Docs

- Main docs entry: `docs/index.md`
- Integration runbook: `docs/backstage-integration.md`
