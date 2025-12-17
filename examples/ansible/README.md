# Ansible Example - Web Terminal with Sample Application and Showroom

This example demonstrates a multi-step Ansible deployment that:
1. Installs the Web Terminal operator
2. **Waits** for the operator to be fully ready
3. Creates a demo namespace
4. Deploys a sample httpd application
5. **Waits** for the deployment to be ready
6. Deploys Showroom lab guide
7. Creates RHDP userinfo ConfigMap

## What This Deploys

- **Web Terminal Operator** - Installed via OLM Subscription with wait logic
- **Demo Namespace** - `terminal-demo` namespace for the sample application
- **Sample Application** - A simple httpd deployment with guaranteed readiness
- **Showroom Lab Guide** - Interactive lab instructions with embedded terminal
- **Userinfo ConfigMap** - RHDP integration with access instructions

## Why Ansible?

The key advantage of Ansible over Helm/Kustomize is **guaranteed ordering with wait logic**:

```yaml
# Install the operator
- ansible.builtin.include_role:
    name: operator-install  # Includes wait for CSV to succeed

# Now we can safely create resources that depend on the operator
- name: Wait for deployment to be ready
  kubernetes.core.k8s_info:
    kind: Deployment
    name: hello-world
  until: deployment_info.resources[0].status.readyReplicas >= 1
  retries: 30
  delay: 10

# Deploy Showroom after everything is ready
- ansible.builtin.include_role:
    name: agnosticd.showroom.ocp4_workload_showroom
```

With Helm/Kustomize, sync waves are best-effort. With Ansible, you're guaranteed that:
- The operator is fully installed before continuing
- The deployment is ready before deploying Showroom
- Showroom is ready before creating the userinfo

## Directory Structure

```
ansible/
├── README.md
├── gitops/                     # GitOps config (ArgoCD deploys this)
│   ├── Chart.yaml              # Uses ansible-runner as dependency
│   └── values.yaml             # Configuration
│
└── playbooks/                  # Ansible content (cloned at runtime)
    ├── site.yml                # Main playbook with multi-step workflow
    ├── requirements.yml        # Collections to install (includes showroom)
    └── roles/
        └── operator-install/   # Reusable role for operator installation
            ├── defaults/main.yml
            └── tasks/main.yml
```

## How It Works

```
ArgoCD                Kubernetes Job              Resources
  │                        │                         │
  ├─── deploys ──────────► │                         │
  │                        │                         │
  │                   ansible-playbook               │
  │                        │                         │
  │                        ├── create Subscription ─────► Operator
  │                        │                         │
  │                        │◄── WAIT for CSV ───────────► (ready)
  │                        │                         │
  │                        ├── create Namespace ────────► terminal-demo
  │                        │                         │
  │                        ├── create Deployment ───────► hello-world
  │                        │                         │
  │                        │◄── WAIT for ready ─────────► (running)
  │                        │                         │
  │                        ├── deploy Showroom ─────────► showroom
  │                        │                         │
  │                        │◄── WAIT for ready ─────────► (running)
  │                        │                         │
  │                        ├── create userinfo      │
  │                        │                         │
  │◄─────── healthy ───────┤                         │
```

## Quick Start

1. **Copy this folder** to your Git repository
2. **Update `gitops/values.yaml`** with your repo URL and Showroom content:
   ```yaml
   ansible:
     repository:
       url: "https://github.com/YOUR-USERNAME/YOUR-REPO"
       branch: "main"
     playbook: "site.yml"
     extraVars:
       # UPDATE THIS to your lab guide repository
       showroom_git_repo: "https://github.com/YOUR-ORG/your-showroom-content.git"
   ```
3. **Order** the Field Content CI from RHDP

After deployment:
1. Access the Showroom lab guide at `https://showroom-demo.<cluster-domain>`
2. Follow the lab instructions
3. Use the embedded terminal or click the (>_) icon in the OpenShift console

## Showroom Configuration

Update the Showroom content repository in `gitops/values.yaml`:

```yaml
ansible:
  extraVars:
    # UPDATE THIS to your lab guide repository
    showroom_git_repo: "https://github.com/rhpds/showroom_template_default.git"
    showroom_git_ref: "main"
```

The Ansible playbook uses the `agnosticd.showroom.ocp4_workload_showroom` role which is included in `requirements.yml`.

## Customization

### Change the Demo Application

Edit `gitops/values.yaml`:
```yaml
ansible:
  extraVars:
    app_name: "my-app"
    app_image: "registry.redhat.io/ubi8/nginx-120:latest"
    demo_namespace: "my-demo"
```

### Install a Different Operator

Edit `gitops/values.yaml`:
```yaml
ansible:
  extraVars:
    operator_name: "openshift-pipelines-operator-rh"
    operator_channel: "latest"
```

And update `playbooks/roles/operator-install/defaults/main.yml` accordingly.

## Variables Available

| Variable | Description |
|----------|-------------|
| `cluster_domain` | The cluster's apps domain |
| `cluster_api_url` | Kubernetes API URL |
| `namespace` | Namespace where the job runs |
| `operator_name` | Operator to install |
| `operator_channel` | Operator channel |
| `demo_namespace` | Namespace for demo resources |
| `app_name` | Name of the sample application |
| `showroom_git_repo` | Showroom content repository URL |
| `showroom_git_ref` | Showroom content branch/tag |

## Testing Locally

```bash
cd playbooks

# Install collections
ansible-galaxy collection install -r requirements.yml

# Run the playbook
ansible-playbook site.yml \
  -e "cluster_domain=$(oc get ingresses.config.openshift.io cluster -o jsonpath='{.spec.domain}')" \
  -e "namespace=openshift-operators" \
  -e "operator_name=web-terminal" \
  -e "operator_channel=fast" \
  -e "demo_namespace=terminal-demo" \
  -e "app_name=hello-world" \
  -e "showroom_git_repo=https://github.com/rhpds/showroom_template_default.git"
```

## Comparison with Helm

| Feature | Ansible | Helm |
|---------|---------|------|
| Wait for resources | Yes (guaranteed) | No (best effort) |
| Multi-step workflows | Yes (sequential) | Yes (sync waves) |
| Error handling | Yes | No |
| Templating | Yes (Jinja2) | Yes (Go) |
| Complexity | Higher | Medium |

**Use Ansible when:**
- You need to wait for the operator to be ready before creating CRs
- You need guaranteed ordering (not just best effort)
- You have complex conditional logic based on cluster state

**Use Helm when:**
- Sync waves are sufficient for ordering
- You don't need to wait for resources
- You prefer simpler chart structure

## Comparison with Kustomize

| Feature | Ansible | Kustomize |
|---------|---------|-----------|
| Wait for resources | Yes (guaranteed) | No (best effort) |
| Multi-step workflows | Yes (sequential) | Yes (sync waves) |
| Templating | Yes | No |
| Learning curve | Higher | Lower |
| Complexity | Higher | Low |

**Use Kustomize when:**
- Static manifests with sync waves are sufficient
- You prefer plain YAML
- Simple deployments without wait logic
