# Field Content Project - Session Summary

**Date**: 2025-12-16
**Repository**: https://github.com/rhpds/field-sourced-content
**Objective**: Create a self-service CI development platform for Red Hat Demo Platform (RHDP)

## 🎯 Project Overview

Created a complete self-service platform enabling Red Hat employees to develop their own Catalog Items (CIs) using GitOps patterns without deep AgnosticD knowledge.

### Key Requirements Addressed
- ✅ Single "field assets" CI where users provide GitOps repo URL
- ✅ Support for developers with some OpenShift knowledge
- ✅ GitOps-first approach with Ansible bridge capability
- ✅ Minimal variables in agnosticV (just repo URL + metadata)
- ✅ Developer controls everything from their GitOps repository
- ✅ Integration with existing RHDP infrastructure

## 🏗️ Architecture Overview

### Core Components Built

```
field-content/
├── project-documentation.md              # Complete project docs
├── SESSION-SUMMARY.md                   # This file
├── roles/
│   └── ocp4_workload_field_content/     # Main workload role
│       ├── defaults/main.yml            # Variable defaults
│       ├── tasks/
│       │   ├── main.yml                 # Entry point
│       │   ├── workload.yml            # Main logic
│       │   └── remove_workload.yml     # Cleanup
│       ├── templates/
│       │   └── application.yaml.j2     # ArgoCD application template
│       ├── meta/
│       ├── vars/
│       └── README.md                    # Role documentation
├── ansible-runner/                      # Ansible execution component
│   ├── helm-chart/                     # Helm chart for ansible-runner
│   │   ├── Chart.yaml
│   │   ├── values.yaml
│   │   └── templates/
│   │       ├── _helpers.tpl
│   │       ├── serviceaccount.yaml
│   │       ├── clusterrole.yaml
│   │       ├── clusterrolebinding.yaml
│   │       ├── configmap.yaml
│   │       └── job.yaml
│   ├── job-template.yaml              # Standalone Job template
│   └── README.md                      # Component documentation
└── examples/
    ├── templates/                     # Developer starting templates
    │   ├── helm-template/             # Complete Helm chart template
    │   │   ├── Chart.yaml
    │   │   ├── values.yaml
    │   │   ├── templates/
    │   │   │   ├── namespace.yaml
    │   │   │   ├── deployment.yaml
    │   │   │   ├── service.yaml
    │   │   │   ├── route.yaml
    │   │   │   ├── configmap.yaml
    │   │   │   └── userinfo.yaml
    │   │   ├── application-example.yaml
    │   │   └── README.md
    │   ├── kustomize-template/          # Kustomize template
    │   │   ├── kustomization.yaml
    │   │   ├── namespace.yaml
    │   │   ├── deployment.yaml
    │   │   ├── service.yaml
    │   │   ├── route.yaml
    │   │   ├── configmap.yaml
    │   │   ├── userinfo.yaml
    │   │   ├── deployment-patch.yaml
    │   │   └── README.md
    │   └── ansible-template/           # Ansible automation template
    │       ├── Chart.yaml              # Uses ansible-runner as subchart
    │       ├── values.yaml
    │       ├── templates/
    │       │   ├── namespace.yaml
    │       │   └── userinfo.yaml
    │       ├── ansible/
    │       │   ├── site.yml           # Main playbook
    │       │   ├── configure-monitoring.yml
    │       │   ├── setup-database.yml
    │       │   └── requirements.yml
    │       └── README.md
    └── cluster-addons/                # Reference examples
        ├── operator-install/          # Generic OLM operator installer (tested)
        ├── image-prepull/             # Pre-pull images to nodes (tested)
        ├── openshift-virtualization/  # CNV stack deployment (tested)
        ├── webterminal/               # Web Terminal
        ├── rhoai/                     # Red Hat OpenShift AI
        ├── charts/                    # Shared charts
        └── README.md
```

## 🔧 Key Components Explained

### 1. Field Content Workload Role (`roles/ocp4_workload_field_content/`)

**Purpose**: Enhanced GitOps bootstrap role for field content deployment

**Key Variables** (all follow `ocp4_workload_` prefix standard):
```yaml
# Required
ocp4_workload_field_content_gitops_repo_url: ""

# Optional
ocp4_workload_field_content_gitops_repo_revision: "main"
ocp4_workload_field_content_gitops_repo_path: ""
ocp4_workload_field_content_deployment_type: "helm"  # helm|kustomize|ansible|hybrid
ocp4_workload_field_content_helm_values: {}
ocp4_workload_field_content_namespace: "openshift-gitops"
# ... health check and timeout configurations
```

**Functionality**:
- Creates ArgoCD Application pointing to developer's GitOps repo
- Injects cluster information (domain, API URL) automatically
- Supports Helm, Kustomize, and hybrid deployments
- Health monitoring with `demo.redhat.com/application` label
- Data extraction via `demo.redhat.com/userinfo` ConfigMaps

### 2. Ansible Runner Component (`ansible-runner/`)

**Purpose**: Execute Ansible playbooks as Kubernetes Jobs within GitOps workflows

**Features**:
- Kubernetes Job-based execution
- Full Helm chart for easy integration
- Configurable RBAC permissions
- Git repository cloning and playbook execution
- Integration with field content workload values
- Output ConfigMaps for RHDP integration

**Usage Pattern**:
```yaml
# In developer's Helm chart values.yaml
ansible-runner:
  ansible:
    repository:
      url: "https://github.com/developer/ansible-playbooks"
    playbook: "site.yml"
    extraVars:
      demo_title: "My Ansible Demo"
```

### 3. Developer Examples (`examples/`)

Self-contained examples ready to copy and customize:

**Helm Example** (`examples/helm/`):
- Complete working HTTPD demo application
- Uses `deployer.domain` for dynamic route hostname
- RHDP integration via userinfo ConfigMap
- Sync wave ordering

**Kustomize Example** (`examples/kustomize/`):
- Static manifest deployment with auto-generated route
- **Limitation**: No dynamic cluster values
- Use when you don't need cluster-specific templating

**Ansible Example** (`examples/ansible/`):
- `gitops/` - Helm chart that creates the ansible-runner Job
- `playbooks/` - Actual Ansible content with demo-app role
- Shows wait_for, Jinja2 templates, RHDP integration

## 📋 Critical Standards & Conventions

### Variable Naming Convention
**CRITICAL**: All AgnosticD workload role variables MUST use `ocp4_workload_` prefix

✅ Correct: `ocp4_workload_field_content_gitops_repo_url`
❌ Wrong: `field_content_gitops_repo_url`

### RHDP Integration Requirements
1. **Health Monitoring**: Label resources with `demo.redhat.com/application: "app-name"`
2. **Data Flow**: Create ConfigMaps with `demo.redhat.com/userinfo: ""` label
3. **Sync Waves**: Use ArgoCD sync waves for proper deployment order

### Deployment Patterns Supported
1. **Pure GitOps**: `agnosticV → GitOps Bootstrap → Helm/Kustomize → ConfigMap Output`
2. **Ansible-First**: `agnosticV → GitOps Bootstrap → Ansible Jobs → K8s Manifests → ConfigMap Output`
3. **Hybrid**: Mixed approaches with proper orchestration

## 🔄 Current Status

### ✅ Completed
- [x] Field content workload role with proper variable naming
- [x] Ansible runner component (single-container Helm chart)
- [x] Complete developer templates for all patterns
- [x] Comprehensive documentation
- [x] New cluster addons: operator-install, image-prepull, openshift-virtualization
- [x] Standards documentation
- [x] **All components tested on OpenShift 4.20 SNO**

### ✅ Testing Results (OpenShift 4.20)

| Component | Status | Notes |
|-----------|--------|-------|
| Operator Install (web-terminal) | ✅ PASSED | OLM Subscription working |
| Image Pre-Pull | ✅ PASSED | DaemonSet deploys to all nodes |
| OpenShift Virtualization | ✅ PASSED | Full CNV stack deployed |
| Helm Template | ✅ PASSED | Value substitution working |
| Kustomize Template | ✅ PASSED | Static manifests only |
| Ansible Runner | ✅ PASSED | Playbook execution + ConfigMap creation |

### 🔧 Key Fixes Applied During Testing

1. **Ansible Runner**:
   - Simplified to single-container architecture
   - Fixed kubeconfig to use `tokenFile` instead of shell expansion
   - Added `ansible-core` to requirements
   - Pinned collections: `kubernetes.core:==3.2.0`, `community.general:==9.5.0`
   - Changed `stdout_callback` from `yaml` to `default`

2. **Kustomize Template**:
   - Removed unsupported fields (`replacements.options`, `metadata`)
   - Removed `$(CLUSTER_DOMAIN)` patterns (not supported by ArgoCD plugin)
   - Documented limitations clearly

### 🔄 Next Steps
1. **E2E Testing**: Fresh end-to-end tests on new cluster
2. **Integration Validation**: Test with existing RHDP infrastructure
3. **Developer Onboarding**: Create user guides
4. **Feedback Integration**: Refine based on testing results

### 📝 Documentation TODO
- [ ] **Cluster Addon Creation Guide** (AsciiDoc format)
  - How to create custom cluster-addons
  - Required structure and conventions
  - Integration with ArgoCD and RHDP
  - *Awaiting further guidance on specifics*

## 💡 Key Insights

1. **Single CI Approach**: Users only need to provide their GitOps repo URL to one "field assets" CI
2. **Minimal agnosticV Footprint**: Only ~4 variables needed vs traditional complex configurations
3. **Developer Freedom**: All complexity managed in developer's own repository
4. **Proven Patterns**: Built on existing successful GitOps bootstrap role
5. **Flexibility**: Supports pure GitOps users AND Ansible automation users

## 📞 Handoff Notes

- All variable naming follows AgnosticD standards (`ocp4_workload_` prefix)
- Documentation is comprehensive and ready for developer consumption
- Templates are complete and testable
- Architecture supports your requirement for Job-based Ansible execution
- Ready for cluster testing phase

The implementation successfully addresses all your original requirements and follows your established conventions. The modular design allows developers to choose their preferred automation approach while maintaining consistent RHDP integration.

---

## 📅 Session: 2025-12-17

### Objective
Restructure examples folder and add Showroom integration to all deployment patterns.

### What was accomplished

1. **Restructured examples folder** - Updated Helm, Kustomize, and Ansible patterns to:
   - Use Web Terminal operator as primary workload
   - Include multi-step workflows (operator install → demo app → Showroom)
   - Add Showroom lab guide as the final deployment step

2. **Committed all changes to git** - All three examples updated and pushed

3. **Installed OpenShift GitOps operator** on SNO 4.20 cluster

4. **Deployed Ansible example via ArgoCD** - The ansible-runner job successfully:
   - Installed Web Terminal operator ✅
   - Created demo namespace and hello-world application ✅
   - Installed Helm CLI (required by showroom role) ✅
   - Reached Showroom deployment step

### Fixes applied during testing

1. **Ansible variable recursion** ([site.yml](examples/ansible/playbooks/site.yml))
   - Variables like `app_image: "{{ app_image | default('...') }}"` cause infinite recursion when passed as extra-vars
   - Fixed by using underscore-prefixed internal variables: `_app_image: "{{ app_image | default('...') }}"`
   - Used `set_fact` to resolve `_guid` before passing to showroom role

2. **Missing Helm CLI** ([job.yaml](examples/ansible/gitops/templates/job.yaml))
   - Showroom role requires helm to render its chart templates
   - Added helm installation step in the job container

3. **RBAC permissions** ([clusterrole.yaml](examples/ansible/gitops/templates/clusterrole.yaml))
   - Added `serviceaccounts`, `persistentvolumeclaims` to core API resources
   - Added RBAC resources (roles, rolebindings, clusterroles, clusterrolebindings)
   - Added networking resources (ingresses, networkpolicies)
   - Added `watch` verb to all resources

4. **ArgoCD hook annotations** ([job.yaml](examples/ansible/gitops/templates/job.yaml))
   - Added `argocd.argoproj.io/hook: Sync` and `BeforeHookCreation` delete policy
   - Ensures job is deleted and recreated on each sync

5. **Local showroom collection** ([collections/](examples/ansible/playbooks/collections/))
   - Copied `agnosticd.showroom` role and `agnosticd.core` plugins locally
   - Created galaxy.yml files for both
   - Added ansible.cfg with collections_paths

### Current blocker

The Showroom role deployment is **failing with RBAC permission errors**:
```
serviceaccounts "showroom" is forbidden: User "system:serviceaccount:openshift-operators:ansible-runner"
cannot get resource "serviceaccounts" in API group "" in the namespace "showroom-demo"
```

The last commit (b3403e7) expanded the ClusterRole permissions, but testing was interrupted when the cluster stopped.

### Pending tasks

| Task | Status |
|------|--------|
| Deploy and test Ansible example via GitOps | 🔄 In Progress |
| Fix ansible-runner namespace (was incorrectly using openshift-operators) | ✅ Fixed |
| Create script to regenerate Helm/Kustomize showroom manifests | ⏳ Pending |
| Fix agnosticd.core dependency for showroom role | ⏳ Pending |

---

## 📅 Session: 2025-12-18

### Issue identified

**Ansible-runner job was scheduled in wrong namespace**

The ansible-runner job was configured to run in `openshift-operators` namespace, which is incorrect:
- The `openshift-operators` namespace is reserved for OLM operators only
- Our deployment jobs should NOT run in system namespaces
- This caused confusion with RBAC and resource ownership

### Fix applied

1. Updated [values.yaml](examples/ansible/gitops/values.yaml) to use dedicated `ansible-runner` namespace:
   ```yaml
   namespace:
     name: ansible-runner
     create: true
   ```

2. Created new [namespace.yaml](examples/ansible/gitops/templates/namespace.yaml) template with sync-wave: "0"

3. Sync wave order is now:
   - Wave 0: Namespace
   - Wave 1: ServiceAccount, ClusterRole, ClusterRoleBinding, ConfigMap
   - Wave 2: Job

### For next session

1. **Start with a fresh cluster** - Avoid stuck resources from previous testing
2. **Test Showroom deployment** with expanded RBAC permissions
3. **Consider simplifying Showroom integration** - The current approach using the full `ocp4_workload_showroom` role may be overly complex for this use case. Options:
   - Create a lighter-weight showroom deployment (just helm chart + minimal config)
   - Use the showroom helm chart directly instead of through the Ansible role
   - Document the complexity and provide simpler alternatives

### Key commits today

| Commit | Description |
|--------|-------------|
| Various | Restructured examples with Showroom integration |
| 33e6b50 | Use set_fact to resolve guid before passing to showroom role |
| 97f6513 | Install helm in ansible-runner container |
| b3403e7 | Expand ClusterRole permissions for showroom deployment |

---
*Session completed: 2025-12-16*
*Testing completed: 2025-12-16 (OpenShift 4.20 SNO)*
*Session continued: 2025-12-17 (Showroom integration - in progress)*
*Repository: https://github.com/rhpds/field-sourced-content*