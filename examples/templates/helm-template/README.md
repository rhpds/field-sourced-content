# Field Content Helm Template

This is a template for creating field content using Helm charts. It provides a basic structure for deploying applications to OpenShift with proper integration to the Red Hat Demo Platform.

## Quick Start

1. **Copy this template** to your own Git repository
2. **Customize the values.yaml** file with your application details
3. **Modify templates** as needed for your application
4. **Test locally** using ArgoCD or `helm template`
5. **Submit to RHDP** by providing your repository URL

## Template Structure

```
helm-template/
├── Chart.yaml          # Helm chart metadata
├── values.yaml         # Default configuration values
├── templates/
│   ├── namespace.yaml  # Namespace creation
│   ├── deployment.yaml # Application deployment
│   ├── service.yaml    # Service exposure
│   ├── route.yaml      # OpenShift route
│   ├── configmap.yaml  # Configuration data
│   └── userinfo.yaml   # RHDP integration
└── README.md           # This file
```

## Key Features

### Automatic Values Injection
The field content workload automatically provides these values to your Helm chart:

```yaml
deployer:
  domain: "apps.cluster-guid.guid.sandbox.opentlc.com"
  apiUrl: "https://api.cluster-guid.guid.sandbox.opentlc.com:6443"
fieldContent:
  deploymentType: "helm"
```

### Sync Waves
Templates use ArgoCD sync waves for proper deployment order:
- Wave 0: Namespaces and prerequisites
- Wave 1: Services and ConfigMaps
- Wave 2: Deployments and Routes
- Wave 3: User info and post-deployment

### RHDP Integration
The `userinfo.yaml` template creates a ConfigMap with the `demo.redhat.com/userinfo` label that passes data back to the RHDP platform.

## Customization

### Update Application Details
Edit `values.yaml` to customize:
- Application name and version
- Container image and configuration
- Resource requirements
- Networking configuration

### Add New Resources
Create additional templates in the `templates/` directory for:
- Persistent volumes
- Secrets
- Additional services
- Custom resources

### Environment-Specific Values
Create additional values files for different environments:
- `values-dev.yaml`
- `values-prod.yaml`

## Testing

### Local Testing
```bash
# Test template rendering
helm template my-demo . --values values.yaml

# Test with injected values
helm template my-demo . --values values.yaml \
  --set deployer.domain=apps.example.com \
  --set deployer.apiUrl=https://api.example.com:6443
```

### ArgoCD Testing
Create a test ArgoCD application pointing to your repository to validate the deployment.

## Best Practices

1. **Use sync waves** to control deployment order
2. **Label all resources** with `demo.redhat.com/application`
3. **Create userinfo ConfigMap** for RHDP integration
4. **Use deployer values** for cluster-specific configuration
5. **Set resource limits** for all containers
6. **Include health checks** in your deployments

## Support

For questions about field content development, refer to:
- Field Content documentation
- Red Hat Demo Platform guides
- OpenShift and Helm documentation