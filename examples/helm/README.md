# Helm Example - Web Terminal with Sample Application and Showroom

This example demonstrates a multi-step Helm deployment that:
1. Installs the Web Terminal operator
2. Creates a demo namespace
3. Deploys a sample httpd application
4. Deploys Showroom lab guide
5. Creates RHDP userinfo ConfigMap

![Helm Pattern Diagram](../../docs/helm-pattern.png)

## What This Deploys

- **Web Terminal Operator** - Provides browser-based terminal access directly in the OpenShift console
- **Demo Namespace** - `terminal-demo` namespace for the sample application
- **Sample Application** - A simple httpd deployment you can access via the Web Terminal
- **Showroom Lab Guide** - Interactive lab instructions with embedded terminal (3 containers: nginx, content, terminal)
- **Userinfo ConfigMap** - RHDP integration with access instructions

## Quick Start

1. **Copy this folder** to your own Git repository
2. **Update `values.yaml`** - Set your Showroom content repository:
   ```yaml
   showroom:
     content:
       repoUrl: "https://github.com/YOUR-ORG/your-showroom-content.git"
   ```
3. **Push** to your Git repository
4. **Order** the Field Content CI from RHDP with deployment type `helm`

## File Structure

```
helm/
├── Chart.yaml           # Helm chart metadata
├── values.yaml          # Configuration values
├── README.md            # This file
└── templates/
    ├── subscription.yaml       # OLM Subscription (sync-wave 1)
    ├── namespace.yaml          # Demo namespace (sync-wave 2)
    ├── deployment.yaml         # Sample app deployment (sync-wave 3)
    ├── service.yaml            # Sample app service (sync-wave 3)
    ├── showroom-namespace.yaml # Showroom namespace (sync-wave 5)
    ├── showroom.yaml           # Showroom deployment (sync-wave 5)
    └── userinfo.yaml           # RHDP integration (sync-wave 6)
```

## How It Works

```
ArgoCD deploys resources in sync-wave order:

  Wave 1: Subscription (Web Terminal operator)
     │
     ▼
  Wave 2: Namespace (terminal-demo)
     │
     ▼
  Wave 3: Deployment + Service (hello-world app)
     │
     ▼
  Wave 5: Showroom namespace + deployment
     │
     ▼
  Wave 6: Userinfo ConfigMap
```

After deployment:
1. Access the Showroom lab guide at `https://showroom.<cluster-domain>`
2. Follow the lab instructions
3. Use the embedded terminal or click the (>_) icon in the OpenShift console

## Showroom Configuration

Update the Showroom content repository in `values.yaml`:

```yaml
showroom:
  enabled: true
  namespace: showroom

  # UPDATE THIS to your lab guide repository
  content:
    repoUrl: "https://github.com/rhpds/showroom_template_default.git"
    repoRef: "main"
    antoraPlaybook: "default-site.yml"

  # Terminal in Showroom
  terminal:
    enabled: true
    image: "quay.io/rhpds/openshift-showroom-terminal-ocp:latest"
```

### Disable Showroom

To deploy without Showroom, set:
```yaml
showroom:
  enabled: false
```

## Customization

### Change the Demo Application

Edit `values.yaml`:
```yaml
demo:
  namespace: my-demo
  appName: my-app
  replicas: 2
  image: registry.redhat.io/ubi8/httpd-24:latest
```

### Install a Different Operator

Edit `values.yaml`:
```yaml
operator:
  name: openshift-pipelines-operator-rh
  channel: latest
```

## Testing Locally

```bash
# Validate the chart
helm lint .

# Render templates to preview
helm template my-release . --set deployer.domain=apps.test.example.com

# Install to a test cluster
helm install web-terminal-demo . --namespace openshift-operators
```

## Comparison with Kustomize

| Feature | Helm | Kustomize |
|---------|------|-----------|
| Templating | Yes (`{{ .Values.x }}`) | No |
| Value substitution | Yes | No |
| Conditional resources | Yes (`{{- if }}`) | No |
| Learning curve | Higher | Lower |
| File format | Go templates | Plain YAML |

**Use Helm when:**
- You need different values per environment
- You want parameterized configuration
- You need conditional logic

**Use Kustomize when:**
- Static manifests with no changes needed
- You prefer plain YAML
- Simple deployments

## Comparison with Ansible

| Feature | Helm | Ansible |
|---------|------|---------|
| Wait for resources | No (best effort) | Yes (guaranteed) |
| Multi-step workflows | Yes (sync waves) | Yes (sequential) |
| Error handling | No | Yes |
| Complexity | Medium | Higher |

**Use Ansible when:**
- You need to wait for the operator to be ready before creating CRs
- You need guaranteed ordering (not just best effort)
- You have complex conditional logic based on cluster state
