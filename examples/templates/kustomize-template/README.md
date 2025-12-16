# Field Content Kustomize Template

This template provides a starting point for creating field content using Kustomize. It's best suited for deploying a collection of Kubernetes manifests that don't require dynamic value substitution.

## When to Use Kustomize vs Helm

| Use Case | Recommended |
|----------|-------------|
| Static manifests with no cluster-specific values | **Kustomize** |
| Need to inject cluster domain, API URL, or other dynamic values | **Helm** |
| Applying patches or overlays to base manifests | **Kustomize** |
| Complex templating with conditionals and loops | **Helm** |

## Limitations

**Environment variable substitution is NOT supported.** Patterns like `$(CLUSTER_DOMAIN)` will not be replaced with actual values. If you need cluster-specific values injected into your manifests, use the Helm template instead.

## Quick Start

1. **Copy this template** to your own Git repository
2. **Customize the manifests** for your application
3. **Modify kustomization.yaml** to add/remove resources
4. **Test locally** using `kustomize build`
5. **Submit to RHDP** by providing your repository URL

## Template Structure

```
kustomize-template/
├── kustomization.yaml    # Main Kustomize configuration
├── namespace.yaml        # Namespace definition
├── deployment.yaml       # Application deployment
├── service.yaml          # Service for the application
├── route.yaml            # OpenShift route
├── configmap.yaml        # Configuration data
├── userinfo.yaml         # RHDP integration ConfigMap
└── README.md             # This file
```

## Key Features

### Sync Waves

Manifests use ArgoCD sync waves for proper deployment order:
- Wave 0: Namespace
- Wave 1: Services and ConfigMaps
- Wave 2: Deployments and Routes
- Wave 3: User info ConfigMap

### RHDP Integration

The `userinfo.yaml` ConfigMap includes the `demo.redhat.com/userinfo` label to pass information back to the RHDP platform.

### Common Labels

All resources are labeled with `demo.redhat.com/application` for health monitoring.

## Customization

### Adding Resources

Add new manifests to the `resources` section in `kustomization.yaml`:

```yaml
resources:
  - namespace.yaml
  - deployment.yaml
  - service.yaml
  - route.yaml
  - configmap.yaml
  - userinfo.yaml
  - my-new-resource.yaml  # Add your resource here
```

### Labels

Use the `labels` transformer to apply common labels:

```yaml
labels:
  - pairs:
      demo.redhat.com/application: my-custom-demo
      app: my-custom-demo
```

### Name Prefixes

Use Kustomize transformers to modify resource names:

```yaml
namePrefix: myapp-
nameSuffix: -v1
```

### Namespace Override

Set a namespace for all resources:

```yaml
namespace: my-demo-namespace
```

## Testing

### Local Testing

```bash
# Test Kustomize build
kustomize build .

# Validate manifests
kustomize build . | kubectl apply --dry-run=client -f -
```

### ArgoCD Testing

Create a test ArgoCD application:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: kustomize-test
  namespace: openshift-gitops
spec:
  project: default
  source:
    repoURL: https://github.com/your-username/your-field-content
    targetRevision: main
    path: .
  destination:
    server: https://kubernetes.default.svc
    namespace: my-demo-namespace
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

## Best Practices

1. **Use sync waves** for proper resource ordering
2. **Label all resources** with `demo.redhat.com/application`
3. **Create userinfo ConfigMap** for RHDP integration
4. **Keep manifests simple** - avoid dynamic values
5. **Validate locally** before submitting
6. **Use hardcoded hostnames** in Routes if needed, or omit the host field to let OpenShift generate one

## Support

For questions about field content development with Kustomize:
- Field Content documentation
- Red Hat Demo Platform guides
- Kustomize documentation: https://kustomize.io/
