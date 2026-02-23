# Scaling Runbook

## Check HPA Status

```bash
kubectl get hpa -n inference
kubectl describe hpa inference-api -n inference
```

---

## Manual Scale Up (Traffic Spike)

```bash
kubectl scale deployment/inference-api -n inference --replicas=8
kubectl get pods -n inference -l app=inference-api
```

!!! warning "Scale back down after the event"

```bash
    kubectl scale deployment/inference-api -n inference --replicas=2
```

---

## Model Backend Scaling

```bash
kubectl scale deployment/llama3-backend -n inference --replicas=3
kubectl exec -n inference <llama3-pod> -- nvidia-smi
```

---

## Cost Considerations

| Component | Cost driver | Action |
| --- | --- | --- |
| Inference API pods | CPU/Memory | Scale freely, cheap |
| Model backend pods | GPU hours | Scale conservatively |
