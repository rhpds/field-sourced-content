# OpenShift Virtualization Addon

Installs OpenShift Virtualization (CNV) using the Red Hat operator.

## What Gets Installed

1. `openshift-cnv` namespace
2. OperatorGroup for the namespace
3. Subscription to `kubevirt-hyperconverged` operator
4. HyperConverged CR to deploy the virtualization stack

## Requirements

- OpenShift 4.x cluster
- Nodes with virtualization extensions enabled (for production use)

## Usage

Deploy with ArgoCD pointing to this chart. The operator will install and create the HyperConverged instance automatically.

## Verification

```bash
oc get csv -n openshift-cnv
oc get hyperconverged -n openshift-cnv
```
