# Backstage Integration Guide

This guide wires this repository to Backstage **Catalog**, **GitHub**, **TechDocs**, and **Kubernetes** using Minikube.

## 1) Catalog entity source of truth

`catalog-info.yaml` is configured with:

- `name: inference-api`
- `type: service`
- `owner: xops-team`
- `lifecycle: production`
- `backstage.io/kubernetes-id: demo-app`
- `backstage.io/kubernetes-namespace: default`
- `github.com/project-slug: ezzat223/inference-api`
- `backstage.io/techdocs-ref: dir:.`

In Backstage UI:

1. Open **Create** > **Register Existing Component**.
2. Provide your repo URL to `catalog-info.yaml`.
3. Open the resulting component entity page.

## 2) GitHub connection

Backstage uses `github.com/project-slug` from `catalog-info.yaml` to connect repository features (PRs, issues, Actions depending on enabled plugins).

If the GitHub card is empty:

- Confirm the repo slug is correct.
- Confirm Backstage backend has a GitHub token/integration configured.

## 3) TechDocs connection

TechDocs is sourced from this repo via `backstage.io/techdocs-ref: dir:.` with navigation in `mkdocs.yml`.

To verify:

1. Open the component in Backstage.
2. Go to the **Docs** tab.
3. Confirm docs render from `docs/`.

## 4) Kubernetes connection (Minikube)

Backstage Kubernetes plugin discovers resources by matching:

- Entity annotation `backstage.io/kubernetes-id`
- Kubernetes label `backstage.io/kubernetes-id`
- Entity namespace annotation `backstage.io/kubernetes-namespace`

Apply demo resources:

```bash
kubectl apply -f k8s/backstage-demo.yaml
```

Verify labels/resources:

```bash
kubectl get deploy,po,svc -n default -l backstage.io/kubernetes-id=demo-app
```

In Backstage UI:

1. Open your component.
2. Go to **Kubernetes** tab.
3. You should see `Deployment`, `Pods`, and `Service` for `demo-app`.

## 5) Typical troubleshooting

If Kubernetes tab is empty:

- Label mismatch between entity annotation and K8s resource labels.
- Namespace mismatch (`default` vs actual namespace).
- Backstage backend RBAC/service-account cannot list resources.
- Wrong cluster context in Backstage backend config.

Quick diagnostics:

```bash
kubectl config current-context
kubectl cluster-info
kubectl get all -n default -l backstage.io/kubernetes-id=demo-app
```
