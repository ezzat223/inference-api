# Scaling Runbook

## Check HPA Status

```bash
kubectl get hpa -n default
kubectl describe hpa inference-api -n default
```

---

## Manual Scale Up (Traffic Spike)

```bash
kubectl scale deployment/inference-api -n default --replicas=8
kubectl get pods -n default -l app=inference-api
```

!!! warning "Scale back down after the event"

```bash
    kubectl scale deployment/inference-api -n default --replicas=2
```

---

## Model Backend Scaling

```bash
kubectl scale deployment/llama3-backend -n default --replicas=3
kubectl exec -n default <llama3-pod> -- nvidia-smi
```

---

## Cost Considerations

| Component | Cost driver | Action |
| --- | --- | --- |
| Inference API pods | CPU/Memory | Scale freely, cheap |
| Model backend pods | GPU hours | Scale conservatively |
