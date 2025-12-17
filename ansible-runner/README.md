# Ansible Runner for Field Content

This component provides a way to execute Ansible playbooks as Kubernetes Jobs within GitOps workflows for field content development. It enables developers who prefer Ansible automation to integrate their playbooks into the GitOps deployment pattern.

## Overview

The Ansible Runner component consists of:
- A Helm chart for configurable deployments
- Integration with the field content workload for automatic cluster information injection

## Architecture

The Ansible Runner uses a single-container architecture that:
1. Installs required Python packages (ansible-core, kubernetes, openshift, etc.)
2. Installs specified Ansible collections
3. Clones your playbook repository from Git
4. Executes the specified playbook with cluster information passed as extra vars
5. Uses the in-cluster service account for Kubernetes API access

## Quick Start

### Using the Helm Chart

1. **Include in your field content repository**:
   ```bash
   # In your GitOps repository
   mkdir charts
   cp -r /path/to/ansible-runner/helm-chart charts/ansible-runner
   ```

2. **Configure your playbook repository**:
   ```yaml
   # values.yaml
   ansible:
     repository:
       url: "https://github.com/your-username/your-ansible-playbooks"
       branch: "main"
     playbook: "site.yml"
   ```

3. **Include in your ArgoCD application**:
   ```yaml
   # templates/ansible-job.yaml
   apiVersion: argoproj.io/v1alpha1
   kind: Application
   metadata:
     name: ansible-automation
     annotations:
       argocd.argoproj.io/sync-wave: "1"
   spec:
     source:
       path: charts/ansible-runner
       helm:
         values: |
           ansible:
             repository:
               url: "{{ .Values.playbookRepo }}"
   ```

## Ansible Playbook Repository Structure

Your Ansible repository should follow this structure:

```
my-ansible-playbooks/
├── site.yml                 # Main playbook
├── requirements.yml         # Ansible Galaxy requirements
├── requirements.txt         # Python requirements (optional)
├── roles/
├── group_vars/
├── host_vars/
└── playbooks/
    ├── setup.yml
    └── configure.yml
```

## Available Variables

The Ansible runner automatically provides these variables to your playbooks:

```yaml
# Cluster information
cluster_domain: "apps.cluster-guid.guid.sandbox.opentlc.com"
cluster_api_url: "https://api.cluster-guid.guid.sandbox.opentlc.com:6443"
namespace: "field-content-demo"

# Additional variables can be specified in values.yaml:
ansible:
  extraVars:
    demo_title: "My Ansible Demo"
    custom_config: "value"
```

## Example Ansible Playbook

```yaml
---
# site.yml
- name: Deploy demo application
  hosts: localhost
  connection: local
  gather_facts: true  # Enable if you need ansible_date_time or other facts
  vars:
    app_name: "ansible-demo"
    app_namespace: "{{ namespace }}"
    app_domain: "{{ cluster_domain }}"

  tasks:
  - name: Create application namespace
    kubernetes.core.k8s:
      name: "{{ app_namespace }}"
      api_version: v1
      kind: Namespace
      state: present

  - name: Deploy application
    kubernetes.core.k8s:
      state: present
      definition:
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: "{{ app_name }}"
          namespace: "{{ app_namespace }}"
        spec:
          replicas: 1
          selector:
            matchLabels:
              app: "{{ app_name }}"
          template:
            metadata:
              labels:
                app: "{{ app_name }}"
            spec:
              containers:
              - name: demo-app
                image: registry.redhat.io/ubi8/httpd-24:latest
                ports:
                - containerPort: 8080

  - name: Create user info ConfigMap
    kubernetes.core.k8s:
      state: present
      definition:
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: "{{ app_name }}-userinfo"
          namespace: "{{ app_namespace }}"
          labels:
            demo.redhat.com/userinfo: ""
        data:
          demo_url: "https://{{ app_name }}.{{ app_domain }}"
          demo_title: "{{ demo_title | default('Ansible Demo') }}"
          ansible_managed: "true"
```

## Configuration Options

### Repository Authentication

For private repositories, create a Kubernetes Secret:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: git-credentials
  namespace: field-content-demo
type: Opaque
data:
  username: base64-encoded-username
  password: base64-encoded-token
```

Then reference it in your values:

```yaml
ansible:
  repository:
    secretName: git-credentials
```

### RBAC Customization

Add additional permissions for your Ansible playbooks:

```yaml
rbac:
  additionalRules:
  - apiGroups: ["operators.coreos.com"]
    resources: ["subscriptions", "installplans"]
    verbs: ["get", "list", "create", "update", "patch"]
  - apiGroups: ["custom.domain.com"]
    resources: ["customresources"]
    verbs: ["*"]
```

### Resource Management

Configure resource limits based on your playbook complexity:

```yaml
resources:
  requests:
    cpu: "500m"
    memory: "512Mi"
  limits:
    cpu: "2000m"
    memory: "2Gi"
```

## Integration with Field Content Workload

The field content workload automatically:
1. Injects cluster domain and API URL values
2. Monitors the job for health and completion
3. Processes any ConfigMaps with `demo.redhat.com/userinfo` label

## Best Practices

1. **Use sync waves** to control execution order
2. **Create output ConfigMaps** with demo information for RHDP
3. **Keep playbooks idempotent** for reliable deployments
4. **Use proper RBAC** - only grant necessary permissions
5. **Handle errors gracefully** in your playbooks
6. **Log important information** for debugging

## Troubleshooting

### Common Issues

1. **Permission Denied**: Check RBAC configuration
2. **Git Clone Fails**: Verify repository URL and credentials
3. **Playbook Fails**: Check logs with `kubectl logs job/ansible-runner-job`
4. **Collection Missing**: Add to `ansible.collections` in values.yaml
5. **Collection Version Incompatibility**: The default UBI8 Python 3.9 image includes ansible-core 2.15.x. Pin collections to compatible versions:
   ```yaml
   collections:
     - kubernetes.core:==3.2.0    # Compatible with ansible-core 2.15.x
     - community.general:==9.5.0  # Compatible with ansible-core 2.15.x
   ```

### Debugging

```bash
# Check job status
kubectl get jobs -n field-content-demo

# View job logs
kubectl logs job/ansible-runner-job -n field-content-demo

# Check created resources
kubectl get all -n field-content-demo

# View output ConfigMap (created by your playbook)
kubectl get configmap -l demo.redhat.com/userinfo -n field-content-demo -o yaml
```

## Tested Configuration

The following configuration has been tested and verified:

```yaml
# values.yaml
ansible:
  requirements:
    - ansible-core
    - ansible-runner
    - kubernetes
    - openshift
    - PyYAML
    - requests
  collections:
    - kubernetes.core:==3.2.0
    - community.general:==9.5.0
image:
  repository: registry.redhat.io/ubi8/python-39
  tag: latest
```

## Examples

See the `examples/ansible/` directory for a complete example of using Ansible automation in field content.