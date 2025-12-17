# OCP Cluster Addons

Collection of addons for the OpenShift Container Platform.

These addons are designed to be installed on an existing OpenShift cluster with ArgoCD.

## Available Addons

| Addon | Description |
|-------|-------------|
| `image-prepull` | Pre-pull container images to all worker nodes |
| `operator-install` | Install any Operator from OperatorHub |
| `openshift-virtualization` | Install OpenShift Virtualization (CNV) |
| `rhoai` | Install Red Hat OpenShift AI |
| `webterminal` | Install Web Terminal operator |

## What is an Addon?

An addon is similar to an OCP4 workload in AgnosticD. Think of it as a library of software that enables developers to enhance their OpenShift cluster with additional features.

## Red Hat Demo Platform

These addons are designed to help developers of the demo platform create their own environments based on OpenShift.

We aim to make it easy for developers to get started with GitOps and ArgoCD for deploying their applications, prioritizing this approach over using Ansible with AgnosticD.

However, this is not the place to find or add your specific demo or lab environment configurations. This is meant for reusable addons that can be utilized by multiple demo environments.

## How to Use

Simply create a new ArgoCD application in your OpenShift cluster and point it to this repository and the desired addon path.

Inside each addon, you'll find a README with usage instructions.

## The charts folder

The `charts` folder is a designated folder containing Helm charts that are published to GitHub's package registry using GitHub Actions.
