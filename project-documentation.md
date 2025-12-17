# Field Content - Self-Service CI Development Platform

## Project Overview

This project aims to create a way for Red Hat employees to develop their own Catalog Items (CIs) for the Red Hat Demo Platform (RHDP) without needing deep knowledge of the existing Ansible automation infrastructure.

## Current State

### RHDP Platform
- Deploys demo/lab/workshop environments
- Covers many Red Hat products and solutions
- Built by small team using primarily Ansible automation (some GitOps)
- Ansible project that is used is called AgnosticD
  - All Ansible roles and automation can be found in ~/devel/git/agDv2
- Assets published to RHDP portal

### Current CI Structure
- All CIs defined in `~/devel/git/agnosticv` project
- Each CI = bottom level directory containing:
  - `common.yaml` or `common.yml`
  - `dev`, `test`, and/or `prod` files
  - Files contain variable lists used by Ansible for deployment

## Project Goals

### Primary Objectives
1. **Self-Service Development**: Enable company-wide asset development without Ansible expertise
2. **OpenShift Focus**: Initial implementation targets OpenShift-based assets only
3. **GitOps Pattern**: Require automation using GitOps approach:
   - Helm charts
   - Kustomize
   - Plain template lists
4. **Flexibility**: Support both pure GitOps users and those preferring Ansible

### Key Requirements
1. **GitOps First**: Primary deployment pattern via GitOps
2. **Ansible Bridge**: Create GitOps-deployable component that can execute Ansible playbooks
   - Pod-based Ansible execution in OpenShift
   - Allows GitOps deployment while enabling Ansible development
3. **Hybrid Support**: Enable combination of GitOps and Ansible approaches

## Existing Resources

### GitOps Bootstrap Role
- Location: `~/devel/git/agDv2/core_workloads/roles/ocp4_workload_gitops_bootstrap`
- Pattern works well for current use cases
- Can be copied/reused for new project

### Example Workloads
- Location: `~/devel/git/ocp-cluster-addons`
- Good starting point for workload patterns
- Can be pulled into new project

## Task List

### Current Session Tasks
- [x] Create project documentation
- [ ] Gather detailed requirements and clarifications
- [ ] Explore existing GitOps bootstrap role
- [ ] Explore example workloads structure
- [ ] Design project architecture

### Future Tasks (To Be Defined)
- [ ] Implement GitOps bootstrap framework
- [ ] Create Ansible execution pod component
- [ ] Develop CI template structure
- [ ] Create developer documentation
- [ ] Build testing and validation framework

## Requirements Clarification

### Target User Profile
- **Primary**: Developers with some OpenShift knowledge
- **Assumption**: Basic conceptual understanding of GitOps and Ansible
- **Reality**: May not have hands-on development experience with GitOps/Ansible

### Technical Implementation Decisions

#### Ansible Bridge Component
- **Phase 1**: Implement using Kubernetes Job pods
  - Simple, proven pattern
  - Jobs run Ansible playbooks and terminate
  - Example workflow: manifest → manifest → manifest → ansible job → manifest
- **Phase 2**: Consider Operator pattern for advanced lifecycle management

#### Integration Constraints
- **Variable Format**: Maintain compatibility with existing common.yaml/dev/test/prod structure
- **agnosticV Variables**: Minimal variables in existing system
  - Primary: GitOps repository location
  - Metadata: deployment type (helm/kustomize/ansible)
  - Avoid complex configuration in agnosticV
- **Control Location**: Developer manages most configuration from their GitOps repository

## Open Questions

*Additional questions to be identified during exploration*

## Current System Analysis

### GitOps Bootstrap Role Pattern
**Location**: `~/devel/git/agDv2/core_workloads/roles/ocp4_workload_gitops_bootstrap`

**Key Functionality**:
- Creates ArgoCD Application pointing to external GitOps repository
- Supports both Helm and Kustomize deployment patterns
- Health checking: Waits for applications to be healthy/synced
- Data extraction: Retrieves ConfigMaps with `demo.redhat.com/userinfo` label
- Multi-user support: Processes user data back to AgnosticD system

**Configuration Variables**:
- `ocp4_workload_gitops_bootstrap_repo_url`: GitOps repository URL
- `ocp4_workload_gitops_bootstrap_repo_revision`: Git branch/tag
- `ocp4_workload_gitops_bootstrap_repo_path`: Path within repository
- `ocp4_workload_gitops_bootstrap_helm_values`: Helm values (if using Helm)
- Health check and timeout configurations

### Example Addons Structure
**Location**: `~/devel/git/ocp-cluster-addons`

**Pattern Analysis**:
- **Primarily Helm-based**: All examined addons use Helm chart structure
- **Chart structure**: Standard `Chart.yaml`, `templates/`, `values.yaml`
- **Multiple values files**: Support for different environments (e.g., `values-apis.yaml`)
- **Example applications**: Each addon includes example ArgoCD application manifest
- **Advanced patterns**: Some use multiple sources for external value files

**Addon Examples**:
- Red Hat DevSpaces
- Red Hat OpenShift AI (RHOAI)
- Web Terminal
- Data Volumes

## Architecture Decisions

### Adopted Patterns from Current System
1. **ArgoCD Application Bootstrap**: Reuse the proven GitOps bootstrap role pattern
2. **Health Checking**: Implement comprehensive application health validation
3. **Data Flow Back**: Support ConfigMap-based data extraction for user info
4. **Flexible Source Support**: Enable both Helm and Kustomize patterns

### Development Standards

#### Variable Naming Convention
**CRITICAL**: All variables in AgnosticD workload roles MUST follow the `ocp4_workload_` prefix standard.

**Examples**:
- ✅ `ocp4_workload_field_content_gitops_repo_url`
- ✅ `ocp4_workload_field_content_deployment_type`
- ❌ `field_content_gitops_repo_url` (missing prefix)
- ❌ `gitops_repo_url` (missing full prefix)

**Rationale**: This ensures consistency across all AgnosticD workload roles and prevents variable name conflicts between different workloads.

**Files affected**:
- `defaults/main.yml` - All default values
- `tasks/workload.yml` - All variable references
- `templates/*.j2` - All template variables
- `README.md` - Documentation examples

## Proposed Architecture

### System Overview

The new CI will enable developers to create Catalog Items using their own GitOps repositories while integrating seamlessly with the existing RHDP infrastructure.
The new CI will have a blank field where the developer can copy in their github repo URL and we will use that to deploy it.
There will not be a new CI for each field developed asset.

### Core Components

#### 1. Enhanced GitOps Bootstrap Role
**Name**: `ocp4_workload_gitops_field_content`
**Purpose**: Minimal wrapper around existing GitOps bootstrap functionality

**agnosticV Variables (Minimal)**:
```yaml
# In agnosticV common.yaml
ocp4_workload_field_content_gitops_repo_url: "https://github.com/developer/my-demo-ci"
ocp4_workload_field_content_gitops_repo_revision: "main"
ocp4_workload_field_content_gitops_repo_path: ""
ocp4_workload_field_content_deployment_type: "helm"  # helm|kustomize|ansible|hybrid
```

**Functionality**:
- Inherits all existing `ocp4_workload_gitops_bootstrap` capabilities
- Minimal configuration required in agnosticV
- Developer controls all specifics from their GitOps repository

#### 2. Ansible Execution Pod Component
**Name**: `ansible-runner-job`
**Purpose**: Execute Ansible playbooks from within GitOps workflow

**Features**:
- Kubernetes Job template deployable via GitOps
- Configurable Ansible playbook source (Git repository, ConfigMap, etc.)
- Support for Ansible Galaxy requirements
- ConfigMap output for data flow back to AgnosticD
- Sync wave configuration for ordered execution

**Example Integration**:
```yaml
# GitOps workflow example:
# Wave 0: Namespace, RBAC setup
# Wave 1: Ansible Job (runs infrastructure playbooks)
# Wave 2: Application deployments (depend on Ansible output)
```

#### 3. CI Template Structure

**Developer GitOps Repository Layout**:
```
my-demo-ci/
├── README.md
├── application.yaml              # Example ArgoCD application
├── helm/                        # If using Helm
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
├── kustomize/                   # If using Kustomize
│   ├── base/
│   ├── overlays/
│   └── kustomization.yaml
├── ansible/                     # If using Ansible components
│   ├── playbooks/
│   ├── requirements.yml
│   └── job-template.yaml
└── docs/                        # Developer documentation
```

**Integration Points**:
(required)
- **Sync Waves**: Use ArgoCD sync waves for execution order
(optional)
- **ConfigMaps**: Use `demo.redhat.com/userinfo` label for data extraction
- **Health Checks**: Use `demo.redhat.com/application` label for health monitoring

### Workflow Patterns

#### Pattern 1: Pure GitOps (Helm/Kustomize)
```
agnosticV → GitOps Bootstrap → Developer Helm Chart → ConfigMap Output
```

#### Pattern 2: Ansible-First with GitOps Deployment
```
agnosticV → GitOps Bootstrap → Ansible Jobs → Kubernetes Manifests → ConfigMap Output
```

#### Pattern 3: Hybrid (Mixed GitOps and Ansible)
```
agnosticV → GitOps Bootstrap → [K8s Manifests → Ansible Job → K8s Manifests] → ConfigMap Output
```

### Developer Experience

#### Getting Started Flow
1. **Repository Creation**: Developer creates GitOps repository using provided template
2. **Development**: Developer builds their automation using preferred patterns
3. **Testing**: Local testing using provided validation tools
4. **Publishing**: Order from RHDP portal by providing URL to gitops repository to "field assets" CI

#### Supported Automation Types
- **Helm Charts**: Full Helm chart development with custom values
- **Kustomize**: Base + overlay patterns for different environments
- **Raw Manifests**: Direct Kubernetes YAML files
- **Ansible Playbooks**: Infrastructure automation via Job pods
- **Hybrid Approaches**: Combination of above patterns

## Implementation Plan

### Phase 1: Foundation (Weeks 1-2)
1. **Create enhanced GitOps bootstrap role**
   - Copy and modify existing `ocp4_workload_gitops_bootstrap`
   - Add field-content specific variables and defaults
   - Implement minimal agnosticV integration

2. **Develop Ansible runner Job component**
   - Create Kubernetes Job template for Ansible execution
   - Support for Git repository sources
   - ConfigMap output integration
   - Basic error handling and logging

3. **Create developer repository templates**
   - Helm chart template
   - Kustomize template
   - Ansible integration examples
   - Documentation templates

### Phase 2: Integration (Weeks 3-4)
1. **agnosticV Integration**
   - Create first self-service CI example
   - Test integration with existing RHDP pipeline
   - Validate health checking and data flow

2. **Developer tooling**
   - Local validation scripts
   - Testing guidelines
   - Troubleshooting documentation

### Phase 3: Enhancement (Future)
1. **Advanced patterns**
   - Multi-source ArgoCD applications
   - Complex Ansible integration scenarios
   - Performance optimization

2. **Documentation and examples**
   - Complete developer guide
   - Migration examples from existing CIs
   - Best practices documentation

## Implementation Status

### ✅ Completed Components

#### 1. Field Content Workload Role
**Location**: `roles/ocp4_workload_field_content/`
- Enhanced GitOps bootstrap role with field content specific variables
- Support for Helm and Kustomize deployment types
- Automatic cluster information injection
- Health checking and RHDP integration
- Comprehensive documentation

#### 2. Ansible Runner Component
**Location**: `ansible-runner/`
- Single-container architecture (simplified from init+main container design)
- Full Helm chart for configurable deployments
- Support for private Git repositories
- Configurable RBAC permissions
- Integration with field content workload
- Uses `tokenFile` for service account authentication
- Tested with ansible-core 2.15.x and pinned collection versions

#### 3. Developer Examples
**Location**: `examples/`

Each example is self-contained with everything needed to deploy:

**Helm Example** (`examples/helm/`):
- Complete Helm chart with working HTTPD demo application
- Automatic value injection (`deployer.domain`, `deployer.apiUrl`)
- RHDP integration via userinfo ConfigMap
- Sync wave configuration for ordered deployment

**Kustomize Example** (`examples/kustomize/`):
- Pure Kustomize approach for static manifests
- **Limitation**: Environment variable substitution NOT supported
- Route uses auto-generated hostname
- Recommended for static deployments without cluster-specific values

**Ansible Example** (`examples/ansible/`):
- Two-part structure: `gitops/` (infrastructure) + `playbooks/` (automation)
- Complete operator-install role with wait logic
- Shows how to wait for CSV, use variables, create RHDP integration
- Best for complex automation requiring programmatic control

#### 4. Cluster Addons
**Location**: `cluster-addons/`

Reusable Helm charts for common cluster preparation tasks:
- **operator-install/**: Generic OLM operator installer
- **image-prepull/**: DaemonSet to pre-pull container images
- **openshift-virtualization/**: Full CNV stack deployment
- **webterminal/**: Web Terminal operator
- **rhoai/**: Red Hat OpenShift AI

### ✅ Testing Status

All components have been tested on OpenShift 4.20 SNO cluster:

| Component | Status | Notes |
|-----------|--------|-------|
| Operator Install (web-terminal) | ✅ PASSED | OLM Subscription working |
| Image Pre-Pull | ✅ PASSED | DaemonSet deploys to all nodes |
| OpenShift Virtualization | ✅ PASSED | Full CNV stack deployed |
| Helm Template | ✅ PASSED | Value substitution working |
| Kustomize Template | ✅ PASSED | Static manifests, env vars NOT supported |
| Ansible Runner | ✅ PASSED | Playbook execution and ConfigMap creation |

### 🔧 Key Fixes Applied During Testing

1. **Ansible Runner**:
   - Simplified to single-container architecture
   - Fixed kubeconfig to use `tokenFile` instead of shell expansion
   - Added `ansible-core` to requirements
   - Pinned collections: `kubernetes.core:==3.2.0`, `community.general:==9.5.0`
   - Changed `stdout_callback` from `yaml` to `default`

2. **Kustomize Template**:
   - Removed unsupported `replacements.options` and `metadata` fields
   - Removed `$(CLUSTER_DOMAIN)` patterns (not supported)
   - Documented limitations clearly

### 📋 Next Steps

1. **E2E Testing**: Run fresh end-to-end tests on a new cluster
2. **Integration Validation**: Verify integration with existing RHDP infrastructure
3. **Cluster Addon Creation Guide**: Create AsciiDoc documentation (TODO)
4. **Developer Onboarding**: Create user guides

---

*Last Updated: 2025-12-16*