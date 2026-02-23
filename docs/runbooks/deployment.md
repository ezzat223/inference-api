# Deployment Runbook

## Standard Deployment (via CI/CD)

All production deployments go through GitHub Actions. Never deploy directly to production.

```text
PR merged to main → CI tests → Docker image built → Image pushed → ArgoCD syncs to K8s
```

---

## Rollback

```bash
kubectl rollout undo deployment/inference-api -n inference
kubectl rollout status deployment/inference-api -n inference
```

---

## Verifying a Deployment

```bash
# All pods are ready
kubectl get pods -n inference -l app=inference-api

# Health check passes
kubectl exec -n inference deploy/inference-api -- \
  curl -s http://localhost:8000/healthz

# Models are loaded
kubectl exec -n inference deploy/inference-api -- \
  curl -s http://localhost:8000/v1/models | jq '.data[].id'
```

---

## Scaling

See [Scaling Runbook](./scaling.md).
