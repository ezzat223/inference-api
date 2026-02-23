# Troubleshooting Runbook

## Alert: `InferenceHighLatency` (p99 > 500ms)

**Check 1 — New deployment?**

```bash
kubectl rollout history deployment/inference-api -n inference
```

If deployed in last 30 mins, roll back:

```bash
kubectl rollout undo deployment/inference-api -n inference
```

**Check 2 — Backend pod health:**

```bash
kubectl get pods -n inference
kubectl top pods -n inference
kubectl logs -n inference <backend-pod> | grep -i "oom\|memory\|killed"
```

---

## Alert: `InferenceHighErrorRate` (5xx > 1%)

```bash
kubectl logs -n inference deploy/inference-api --tail=100 | grep '"level":"error"'
kubectl get pods -n model-registry
```

---

## Alert: `InferencePodCrashLooping`

```bash
kubectl describe pod -n inference <pod-name>
kubectl logs -n inference <pod-name> --previous
```

| Symptom in logs | Fix |
| --- | --- |
| `ModuleNotFoundError` | Wrong Python version, rebuild image |
| `Connection refused` on startup | Check `MODEL_REGISTRY_URL` env var |
| `OOMKilled` in describe | Increase memory limit in deployment YAML |

---

## Model Returns 404

```bash
curl http://inference-api.internal/v1/models | jq '.data[].id'
python scripts/register_model.py --model-id llama3-8b-ft-v2 --version 2.1
```

---

## Escalation Path

1. Check this runbook (5 min)
2. Check Grafana (5 min)
3. Post in `#mlops-oncall` with summary
4. If unresolved after 20 min → page ML Infra via PagerDuty
