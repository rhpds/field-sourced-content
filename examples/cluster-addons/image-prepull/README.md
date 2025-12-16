# Image Pre-Pull Addon

Pre-pulls container images to all worker nodes using a DaemonSet.

## Usage

Specify images to pre-pull in `values.yaml`:

```yaml
images:
  - registry.redhat.io/ubi8/ubi:latest
  - quay.io/my-org/my-app:v1.0
```

## How It Works

Creates a DaemonSet that runs on all worker nodes. Each image is pulled via an init container, then a pause container keeps the pod running.
