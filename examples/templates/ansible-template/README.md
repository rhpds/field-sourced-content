# Field Content Ansible Template

This template demonstrates how to create field content using Ansible automation within a GitOps workflow. It combines the flexibility of Ansible with the GitOps deployment pattern by using the Ansible runner component.

## Quick Start

1. **Copy this template** to your own Git repository
2. **Create your Ansible playbooks** in the `ansible/` directory
3. **Update values.yaml** with your playbook repository URL
4. **Test locally** using the ansible-runner
5. **Submit to RHDP** by providing your repository URL

## Template Structure

```
ansible-template/
├── Chart.yaml              # Helm chart metadata
├── values.yaml             # Configuration values
├── charts/                 # Subchart dependencies
│   └── ansible-runner/     # (Copy ansible-runner chart here)
├── templates/
│   ├── namespace.yaml      # Namespace creation
│   └── userinfo.yaml       # RHDP integration
├── ansible/
│   ├── site.yml            # Main Ansible playbook
│   ├── configure-monitoring.yml  # Optional monitoring setup
│   ├── setup-database.yml  # Optional database deployment
│   └── requirements.yml    # Ansible Galaxy requirements
└── README.md               # This file
```

## How It Works

1. **GitOps Deployment**: ArgoCD deploys the Helm chart containing the ansible-runner
2. **Ansible Execution**: The ansible-runner Job clones your playbook repository and executes the specified playbook
3. **Resource Creation**: Your Ansible playbooks create Kubernetes resources
4. **RHDP Integration**: ConfigMaps with proper labels pass data back to RHDP

## Ansible Playbook Development

### Main Playbook (site.yml)

The main playbook receives these variables automatically:
- `cluster_domain`: The cluster's ingress domain
- `cluster_api_url`: The cluster's API URL
- `namespace`: The target namespace for resources
- Custom variables from `values.yaml` under `ansible.extraVars`

### Available Kubernetes Modules

Your playbooks have access to:
- `kubernetes.core.k8s`: Create/manage any Kubernetes resource
- `kubernetes.core.k8s_info`: Query existing resources
- `kubernetes.core.helm`: Deploy Helm charts (if needed)

### Example Playbook Pattern

```yaml
- name: Deploy My Application
  hosts: localhost
  connection: local
  gather_facts: false
  vars:
    app_name: "{{ demo_app_name | default('my-app') }}"
    app_namespace: "{{ namespace }}"

  tasks:
  - name: Create application deployment
    kubernetes.core.k8s:
      state: present
      definition:
        apiVersion: apps/v1
        kind: Deployment
        # ... deployment spec
```

## Configuration

### Repository Setup

Update `values.yaml` to point to your Ansible playbook repository:

```yaml
ansible-runner:
  ansible:
    repository:
      url: "https://github.com/your-username/your-ansible-playbooks"
      branch: "main"
    playbook: "site.yml"
```

### Variable Passing

Pass custom variables to your playbook:

```yaml
ansible-runner:
  ansible:
    extraVars:
      demo_title: "My Custom Demo"
      enable_monitoring: true
      enable_database: true
      custom_config: "value"
```

### RBAC Configuration

Add additional permissions for your playbooks:

```yaml
ansible-runner:
  rbac:
    additionalRules:
    - apiGroups: ["operators.coreos.com"]
      resources: ["subscriptions", "installplans"]
      verbs: ["get", "list", "create", "update", "patch"]
```

## Advanced Patterns

### Multi-Playbook Workflows

Use `import_playbook` to organize complex deployments:

```yaml
# site.yml
- name: Setup Infrastructure
  import_playbook: setup-infrastructure.yml

- name: Deploy Applications
  import_playbook: deploy-applications.yml

- name: Configure Monitoring
  import_playbook: configure-monitoring.yml
  when: enable_monitoring | default(false) | bool
```

### Conditional Deployments

Use Ansible conditionals for optional components:

```yaml
- name: Deploy database
  include_tasks: database-tasks.yml
  when: enable_database | default(false) | bool
```

### External Role Dependencies

Use `requirements.yml` for external roles:

```yaml
roles:
  - name: geerlingguy.postgresql
    version: "3.0.0"
```

### Secret Management

Create secrets in your playbooks:

```yaml
- name: Create application secret
  kubernetes.core.k8s:
    definition:
      apiVersion: v1
      kind: Secret
      metadata:
        name: app-secrets
      type: Opaque
      data:
        api-key: "{{ api_key | b64encode }}"
```

## Integration with RHDP

### User Info ConfigMap

Always create a ConfigMap for RHDP integration:

```yaml
- name: Create user info for RHDP
  kubernetes.core.k8s:
    definition:
      apiVersion: v1
      kind: ConfigMap
      metadata:
        name: demo-userinfo
        labels:
          demo.redhat.com/userinfo: ""  # Required label
      data:
        demo_url: "https://{{ app_name }}.{{ cluster_domain }}/"
        demo_title: "{{ demo_title }}"
        access_instructions: "Your access instructions here"
```

### Health Monitoring

Label your main application resources:

```yaml
metadata:
  labels:
    demo.redhat.com/application: "{{ app_name }}"
```

## Testing

### Local Development

1. **Test playbook syntax**:
   ```bash
   ansible-playbook ansible/site.yml --syntax-check
   ```

2. **Test with sample variables**:
   ```bash
   ansible-playbook ansible/site.yml \
     --extra-vars "cluster_domain=apps.test.com" \
     --extra-vars "namespace=test-namespace" \
     --check
   ```

3. **Test Helm chart**:
   ```bash
   helm template . --values values.yaml
   ```

### Cluster Testing

Deploy to a test cluster using the field content workload with your repository URL.

## Best Practices

1. **Keep playbooks idempotent** - safe to run multiple times
2. **Use proper sync waves** for resource dependencies
3. **Handle errors gracefully** with appropriate error handling
4. **Log important information** for debugging
5. **Create meaningful user info** for RHDP integration
6. **Use resource limits** in deployments
7. **Follow Kubernetes best practices** in your resources

## Troubleshooting

### Common Issues

1. **Permissions**: Check RBAC rules in values.yaml
2. **Variables**: Verify extra vars are properly passed
3. **Dependencies**: Ensure requirements.yml is correct
4. **Syntax**: Validate Ansible syntax before deployment

### Debugging

```bash
# Check ansible job logs
kubectl logs job/ansible-runner-job -n field-content-demo

# Check created resources
kubectl get all -n field-content-demo

# View user info output
kubectl get configmap -l demo.redhat.com/userinfo -o yaml
```

## Examples

The `ansible/` directory contains complete examples showing:
- Basic application deployment
- Database setup
- Monitoring configuration
- Multi-component workflows

## Support

For questions about Ansible-based field content development:
- Ansible documentation: https://docs.ansible.com
- Kubernetes collection docs: https://docs.ansible.com/ansible/latest/collections/kubernetes/core/
- Field Content documentation
- Red Hat Demo Platform guides