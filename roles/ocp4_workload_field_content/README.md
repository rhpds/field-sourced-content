# Field Content Workload

This workload enables self-service deployment of field-developed content using GitOps patterns. It allows developers to create their own automation in a GitOps repository and deploy it through the Red Hat Demo Platform without needing deep knowledge of AgnosticD.

## Overview

The Field Content workload creates an ArgoCD Application pointing to a developer's GitOps repository. The developer controls all aspects of their deployment through their repository, while this role provides minimal orchestration and integration with RHDP infrastructure.

## Supported Deployment Types

- **helm**: Deploy using Helm charts
- **kustomize**: Deploy using Kustomize
- **ansible**: Deploy using Ansible playbooks executed as Kubernetes Jobs
- **hybrid**: Combination of the above approaches

## Required Variables

```yaml
ocp4_workload_field_content_gitops_repo_url: "https://github.com/developer/my-field-content"
```

## Optional Variables

```yaml
ocp4_workload_field_content_gitops_repo_revision: "main"         # Git branch/tag
ocp4_workload_field_content_gitops_repo_path: ""                 # Path within repo
ocp4_workload_field_content_deployment_type: "helm"              # helm|kustomize|ansible|hybrid
ocp4_workload_field_content_helm_values: {}                      # Additional Helm values
```

## Developer Repository Structure

Your GitOps repository should follow these patterns:

### For Helm deployments:
```
my-field-content/
├── Chart.yaml
├── values.yaml
└── templates/
    └── ...
```

### For Kustomize deployments:
```
my-field-content/
├── kustomization.yaml
├── base/
└── overlays/
```

### For Ansible deployments:
```
my-field-content/
├── ansible/
│   ├── playbooks/
│   ├── requirements.yml
│   └── job-template.yaml
└── manifests/
```

## Integration with RHDP

### Data Flow Back to AgnosticD

Create ConfigMaps with the `demo.redhat.com/userinfo` label to pass data back to AgnosticD:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-field-content-info
  labels:
    demo.redhat.com/userinfo: ""
data:
  demo_url: "https://my-demo.apps.cluster.example.com"
  users_json: '{"users": {"user1": {"password": "generated-password"}}}'
```

### Health Checking

Applications with the `demo.redhat.com/application` label will be monitored for health and sync status:

```yaml
metadata:
  labels:
    demo.redhat.com/application: "my-field-content"
```

## Available Deployer Values

The following values are automatically provided to Helm charts and can be used in templates:

```yaml
deployer:
  domain: "apps.cluster-guid.guid.sandbox.opentlc.com"
  apiUrl: "https://api.cluster-guid.guid.sandbox.opentlc.com:6443"
fieldContent:
  deploymentType: "helm"  # The deployment type specified
```
