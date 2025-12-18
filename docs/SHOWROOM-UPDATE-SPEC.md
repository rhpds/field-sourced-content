# Showroom Manifests Update Specification

This document provides a specification for updating the Showroom deployment manifests in the field-content repository. Use this when the upstream Showroom Ansible collection or Helm chart releases new versions with features or fixes that should be incorporated.

## Upstream Sources

### Primary: Ansible Collection

- **Repository**: https://github.com/agnosticd/showroom
- **Collection Name**: `agnosticd.showroom`
- **Role**: `ocp4_workload_showroom`
- **Latest Release**: Check https://github.com/agnosticd/showroom/releases

### Secondary: Helm Chart (used by the Ansible role)

- **Repository**: https://github.com/rhpds/showroom-deployer
- **Helm Chart**: `showroom-single-pod`
- **Chart URL**: https://rhpds.github.io/showroom-deployer
- **Current Version Used**: `^2.0.0`

## Relationship Between Sources

The `agnosticd/showroom` repository contains the Ansible collection with the `ocp4_workload_showroom` role. This role uses the Helm chart from `rhpds/showroom-deployer` to deploy Showroom. Our simplified `deploy-showroom` role is derived from `ocp4_workload_showroom` but removes the `agnosticd.core` dependency.

## Files That Need Updates

### 1. Ansible Role (`examples/ansible/playbooks/roles/deploy-showroom/`)

| File | Purpose |
|------|---------|
| `defaults/main.yml` | Default variables including image versions, chart version, resource limits |
| `tasks/main.yml` | Deployment logic using `kubernetes.core.helm_template` |
| `README.md` | Documentation for the role |

**Update Triggers**:
- New container image versions (showroom-content, terminal, nginx, antora, git-cloner)
- New Helm chart version
- New Helm values structure
- New zero-touch bundle version
- Changes to the upstream `ocp4_workload_showroom` role logic

### 2. Helm Chart (`examples/helm/`)

| File | Purpose |
|------|---------|
| `values.yaml` | Default values including image versions |
| `templates/showroom.yaml` | Static Kubernetes manifests for Showroom |

**Update Triggers**:
- Changes to Showroom pod spec (containers, volumes, ports)
- New init containers or sidecars
- Changes to nginx configuration
- New environment variables

### 3. Kustomize (`examples/kustomize/`)

| File | Purpose |
|------|---------|
| `showroom/showroom.yaml` | Static manifests for Showroom deployment |
| `showroom/namespace.yaml` | Namespace definition |

**Update Triggers**:
- Same as Helm chart above

## Update Procedure

### Step 1: Check Upstream Changes

#### Check Ansible Collection

```bash
# Clone or pull the upstream repository
git clone https://github.com/agnosticd/showroom.git
cd showroom

# Check the role defaults for version changes
cat roles/ocp4_workload_showroom/defaults/main.yml

# Check for task changes
ls -la roles/ocp4_workload_showroom/tasks/
```

Key files to review in the upstream role:
- `roles/ocp4_workload_showroom/defaults/main.yml` - Default variables
- `roles/ocp4_workload_showroom/tasks/deploy_showroom.yaml` - Helm deployment logic
- `roles/ocp4_workload_showroom/tasks/workload.yml` - Main workflow

#### Check Helm Chart

```bash
# Add/update the Helm repo
helm repo add rhpds https://rhpds.github.io/showroom-deployer
helm repo update

# Check available versions
helm search repo rhpds/showroom-single-pod --versions

# Download and inspect the chart
helm pull rhpds/showroom-single-pod --untar
```

### Step 2: Review Changes

#### In the Ansible Collection (`agnosticd/showroom`)

1. **`defaults/main.yml`**: Image versions, chart version, resource defaults
2. **`tasks/deploy_showroom.yaml`**: Helm values structure passed to the chart
3. **`tasks/workload.yml`**: Workflow changes (new steps, changed order)

#### In the Helm Chart (`rhpds/showroom-deployer`)

1. **`Chart.yaml`**: Version number, appVersion
2. **`values.yaml`**: New defaults, image versions, structure changes
3. **`templates/`**: New resources, changed pod specs

### Step 3: Update Ansible Role

#### `defaults/main.yml`

Compare with upstream `roles/ocp4_workload_showroom/defaults/main.yml` and update:

```yaml
# Container images - match upstream versions
showroom_content_image: quay.io/rhpds/showroom-content:vX.X.X
showroom_terminal_image: quay.io/rhpds/openshift-showroom-terminal-ocp:latest

# Helm chart version
showroom_deployer_chart_version: "^X.X.X"

# Zero-touch bundle
showroom_zero_touch_bundle: "https://github.com/rhpds/nookbag/releases/download/nookbag-vX.X.X/nookbag-vX.X.X.zip"
```

#### `tasks/main.yml`

Compare with upstream `roles/ocp4_workload_showroom/tasks/deploy_showroom.yaml` and update the `release_values` block:

```yaml
- name: Render showroom Helm chart
  kubernetes.core.helm_template:
    chart_repo_url: "{{ showroom_chart_package_url }}"
    chart_ref: "{{ showroom_deployer_chart_name }}"
    chart_version: "{{ showroom_deployer_chart_version }}"
    release_values:
      # Update this structure to match upstream deploy_showroom.yaml
      content:
        image: "..."
        # ... other values
```

### Step 4: Update Helm Chart Templates

The `examples/helm/templates/showroom.yaml` contains static manifests. To update:

1. Render the upstream chart with sample values:
   ```bash
   helm template showroom rhpds/showroom-single-pod \
     --set deployer.domain=example.com \
     --set guid=demo \
     --set content.repoUrl=https://github.com/rhpds/showroom_template_default.git \
     --set terminal.setup=true \
     > rendered-upstream.yaml
   ```

2. Compare with current `templates/showroom.yaml`

3. Update the template, preserving:
   - Helm template expressions (`{{ .Values.* }}`)
   - ArgoCD sync-wave annotations
   - Conditional blocks (`{{- if .Values.showroom.enabled }}`)

### Step 5: Update Kustomize Manifests

The `examples/kustomize/showroom/showroom.yaml` contains static YAML. To update:

1. Use the same rendered upstream output from Step 4

2. Replace the manifests in `showroom.yaml`, preserving:
   - Hardcoded namespace (`showroom`)
   - ArgoCD sync-wave annotations
   - Comments indicating where users should update values

### Step 6: Test Updates

Deploy each example type and verify:

1. **Ansible**:
   ```bash
   oc apply -f - <<EOF
   apiVersion: argoproj.io/v1alpha1
   kind: Application
   metadata:
     name: ansible-test
     namespace: openshift-gitops
   spec:
     project: default
     source:
       repoURL: https://github.com/rhpds/field-sourced-content
       path: examples/ansible/gitops
       helm:
         parameters:
           - name: deployer.domain
             value: "apps.YOUR-CLUSTER.example.com"
     destination:
       server: https://kubernetes.default.svc
     syncPolicy:
       automated: {}
   EOF
   ```

2. **Helm**:
   ```bash
   oc apply -f - <<EOF
   apiVersion: argoproj.io/v1alpha1
   kind: Application
   metadata:
     name: helm-test
     namespace: openshift-gitops
   spec:
     project: default
     source:
       repoURL: https://github.com/rhpds/field-sourced-content
       path: examples/helm
       helm:
         parameters:
           - name: deployer.domain
             value: "apps.YOUR-CLUSTER.example.com"
     destination:
       server: https://kubernetes.default.svc
     syncPolicy:
       automated: {}
   EOF
   ```

3. **Kustomize**:
   ```bash
   oc apply -f - <<EOF
   apiVersion: argoproj.io/v1alpha1
   kind: Application
   metadata:
     name: kustomize-test
     namespace: openshift-gitops
   spec:
     project: default
     source:
       repoURL: https://github.com/rhpds/field-sourced-content
       path: examples/kustomize
     destination:
       server: https://kubernetes.default.svc
     syncPolicy:
       automated: {}
   EOF
   ```

### Step 7: Verify Deployment

For each example, confirm:

- [ ] Showroom pod is Running with all containers ready (typically 3/3)
- [ ] Showroom route is accessible and displays the lab guide
- [ ] Terminal is functional (if enabled)
- [ ] No errors in pod logs

## Image Version Reference

Current images used in the manifests:

| Image | Purpose | Registry |
|-------|---------|----------|
| `quay.io/rhpds/showroom-content` | Serves Antora content | quay.io |
| `quay.io/rhpds/openshift-showroom-terminal-ocp` | Terminal container | quay.io |
| `quay.io/rhpds/nginx` | Reverse proxy | quay.io |
| `quay.io/rhpds/antora` | Builds Antora site (init container) | quay.io |
| `quay.io/rhpds/git-cloner` | Clones content repo (init container) | quay.io |

## What NOT to Update

The following features from the upstream role are intentionally NOT supported in our simplified version:

- **Multi-user deployments**: Only single-user mode is supported
- **Wetty terminal**: Only the showroom terminal is supported
- **noVNC**: VNC client deployment is not supported
- **agnosticd.core integration**: User data is passed directly, not via agnosticd plugins (`agnosticd_user_data` lookup, `agnosticd_user_info` module)
- **Passthrough user data**: Not supported

If these features are needed, consider using the full `agnosticd.showroom` collection instead.

## Commit Message Template

When committing updates, use this format:

```
Update Showroom manifests to upstream vX.X.X

- Updated showroom-content image to vX.X.X
- Updated terminal image to vX.X.X
- Updated Helm chart version to vX.X.X
- [List any other changes]

Upstream sources:
- Ansible collection: https://github.com/agnosticd/showroom/releases/tag/vX.X.X
- Helm chart: https://github.com/rhpds/showroom-deployer
```
