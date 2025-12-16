# Operator Install Addon

Install any Operator from OperatorHub using OLM Subscription.

## Usage

Configure the operator in `values.yaml`:

```yaml
operator:
  name: web-terminal
  namespace: openshift-operators
  channel: fast
  source: redhat-operators
  sourceNamespace: openshift-marketplace
  installPlanApproval: Automatic
```

## Finding Operator Details

To find available operators and their details:

```bash
oc get packagemanifests -n openshift-marketplace
oc describe packagemanifest <operator-name> -n openshift-marketplace
```
