# Field Content Kustomize Template

This template provides a starting point for creating field content using Kustomize. It demonstrates how to structure Kubernetes manifests with proper RHDP integration and environment variable injection.

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
├── route.yaml           # OpenShift route
├── configmap.yaml       # Configuration data
├── userinfo.yaml        # RHDP integration ConfigMap
├── deployment-patch.yaml # Environment-specific patches
└── README.md            # This file
```

## Key Features

### Environment Variable Injection

The field content workload uses the `kustomize-envvar` plugin to inject cluster-specific values:

- `$(CLUSTER_DOMAIN)` - The cluster's ingress domain
- `$(API_URL)` - The cluster's API URL

These are automatically replaced during deployment.

### Sync Waves

Manifests use ArgoCD sync waves for proper deployment order:
- Wave 0: Namespace
- Wave 1: Services and ConfigMaps
- Wave 2: Deployments and Routes
- Wave 3: User info ConfigMap

### RHDP Integration

The `userinfo.yaml` ConfigMap includes the `demo.redhat.com/userinfo` label to pass information back to the RHDP platform.

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

### Environment-Specific Changes

Create overlay directories for different environments:

```
kustomize-template/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   └── ...
└── overlays/
    ├── dev/
    │   ├── kustomization.yaml
    │   └── dev-patch.yaml
    └── prod/
        ├── kustomization.yaml
        └── prod-patch.yaml
```

### Custom Labels and Annotations

Modify the `commonLabels` and `commonAnnotations` in `kustomization.yaml`:

```yaml
commonLabels:
  demo.redhat.com/application: "my-custom-demo"
  app: my-custom-demo
  version: v1.0.0

commonAnnotations:
  description: "My custom field content demo"
```

### Name Prefixes and Suffixes

Use Kustomize transformers to modify resource names:

```yaml
namePrefix: myapp-
nameSuffix: -v1
```

## Testing

### Local Testing

```bash
# Test Kustomize build
kustomize build .

# Test with environment variables
CLUSTER_DOMAIN=apps.example.com API_URL=https://api.example.com:6443 kustomize build .

# Validate manifests
kustomize build . | kubectl apply --dry-run=client -f -
```

### ArgoCD Testing

Create a test ArgoCD application pointing to your repository:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: kustomize-test
spec:
  source:
    repoURL: https://github.com/your-username/your-field-content
    path: .
    plugin:
      name: kustomize-envvar
      env:
        - name: CLUSTER_DOMAIN
          value: "apps.test-cluster.example.com"
        - name: API_URL
          value: "https://api.test-cluster.example.com:6443"
  destination:
    server: https://kubernetes.default.svc
    namespace: field-content-demo
```

## Advanced Patterns

### Using Generators

Add ConfigMap and Secret generators:

```yaml
configMapGenerator:
- name: app-config
  files:
  - config.properties
  - application.yaml

secretGenerator:
- name: app-secrets
  literals:
  - api-key=secret-value
```

### Component Composition

Use Kustomize components for reusable pieces:

```yaml
components:
- github.com/example/common-components/monitoring
- github.com/example/common-components/logging
```

### Strategic Merge Patches

Create targeted patches for specific resources:

```yaml
patchesStrategicMerge:
- deployment-resources.yaml
- service-annotations.yaml
```

## Integration Examples

### With Helm Charts

You can include Helm charts in Kustomize using the Helm generator:

```yaml
helmCharts:
- name: postgresql
  repo: https://charts.bitnami.com/bitnami
  version: 12.1.2
  releaseName: my-database
```

### With External Resources

Reference resources from other repositories:

```yaml
resources:
- github.com/example/base-resources/monitoring?ref=v1.0.0
- https://raw.githubusercontent.com/example/configs/main/common.yaml
```

## Best Practices

1. **Use sync waves** for proper resource ordering
2. **Label all resources** with `demo.redhat.com/application`
3. **Create userinfo ConfigMap** for RHDP integration
4. **Use environment variables** for cluster-specific values
5. **Keep manifests simple** and use patches for variations
6. **Organize with overlays** for different environments
7. **Validate locally** before submitting

## Support

For questions about field content development with Kustomize:
- Field Content documentation
- Red Hat Demo Platform guides
- Kustomize documentation
- OpenShift and Kubernetes documentation