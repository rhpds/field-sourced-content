#!/usr/bin/env python3
"""
Generate architecture diagrams for Field Content project
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import matplotlib.lines as mlines
import numpy as np

# Set up the figure with a nice size
fig, ax = plt.subplots(1, 1, figsize=(16, 12))
ax.set_xlim(0, 16)
ax.set_ylim(0, 12)
ax.set_aspect('equal')
ax.axis('off')

# Color scheme - Red Hat inspired
colors = {
    'rhdp': '#EE0000',           # Red Hat Red
    'rhdp_light': '#FFCCCC',
    'argocd': '#E96D3F',         # ArgoCD Orange
    'argocd_light': '#FFE4D9',
    'k8s': '#326CE5',            # Kubernetes Blue
    'k8s_light': '#D6E4FF',
    'ansible': '#1A1918',        # Ansible Black
    'ansible_light': '#E8E8E8',
    'github': '#24292E',         # GitHub Dark
    'github_light': '#F6F8FA',
    'success': '#3E8635',        # Green
    'text': '#1A1A1A',
    'white': '#FFFFFF',
    'border': '#666666',
}

def draw_box(x, y, width, height, color, label, fontsize=10, text_color='white'):
    """Draw a rounded rectangle with label"""
    box = FancyBboxPatch((x, y), width, height,
                          boxstyle="round,pad=0.02,rounding_size=0.1",
                          facecolor=color, edgecolor=colors['border'], linewidth=1.5)
    ax.add_patch(box)
    ax.text(x + width/2, y + height/2, label, ha='center', va='center',
            fontsize=fontsize, fontweight='bold', color=text_color, wrap=True)
    return box

def draw_container(x, y, width, height, title, color, items=None):
    """Draw a container box with title and optional items"""
    # Main container
    container = FancyBboxPatch((x, y), width, height,
                                boxstyle="round,pad=0.02,rounding_size=0.15",
                                facecolor=color, edgecolor=colors['border'], linewidth=2)
    ax.add_patch(container)

    # Title bar
    title_height = 0.4
    title_bar = FancyBboxPatch((x, y + height - title_height), width, title_height,
                                boxstyle="round,pad=0.02,rounding_size=0.1",
                                facecolor=colors['border'], edgecolor='none')
    ax.add_patch(title_bar)
    ax.text(x + width/2, y + height - title_height/2, title,
            ha='center', va='center', fontsize=11, fontweight='bold', color='white')

    return container

def draw_arrow(start, end, color='#666666', style='simple', connectionstyle='arc3,rad=0'):
    """Draw an arrow between two points"""
    arrow = FancyArrowPatch(start, end,
                            arrowstyle='-|>',
                            connectionstyle=connectionstyle,
                            mutation_scale=15,
                            color=color, linewidth=2)
    ax.add_patch(arrow)
    return arrow

# Title
ax.text(8, 11.5, 'Field Content Architecture', ha='center', va='center',
        fontsize=20, fontweight='bold', color=colors['text'])
ax.text(8, 11.1, 'Self-Service CI Development Platform for RHDP', ha='center', va='center',
        fontsize=12, color=colors['border'])

# =====================
# RHDP Section (Top Left)
# =====================
draw_container(0.3, 8.5, 3.5, 2.2, 'RED HAT DEMO PLATFORM', colors['rhdp_light'])
draw_box(0.5, 9.4, 3.1, 0.6, colors['rhdp'], 'User Portal', fontsize=9)
ax.text(2.05, 8.9, '• Orders "Field Content" CI\n• Provides GitOps repo URL',
        ha='center', va='center', fontsize=8, color=colors['text'])

# =====================
# Developer Repo (Top Right)
# =====================
draw_container(12.2, 8.5, 3.5, 2.2, 'DEVELOPER GIT REPO', colors['github_light'])
draw_box(12.4, 9.4, 3.1, 0.6, colors['github'], 'GitHub/GitLab', fontsize=9)
ax.text(13.95, 8.9, '• Helm Chart / Kustomize\n• Ansible Playbooks',
        ha='center', va='center', fontsize=8, color=colors['text'])

# =====================
# OpenShift Cluster (Main Center Area)
# =====================
draw_container(0.3, 0.5, 15.4, 7.5, 'OPENSHIFT CLUSTER', colors['k8s_light'])

# ArgoCD Box
draw_container(0.6, 5.2, 4.5, 2.3, 'openshift-gitops', colors['argocd_light'])
draw_box(0.8, 5.8, 4.1, 1.2, colors['argocd'], 'ArgoCD\nApplication Controller', fontsize=9)
ax.text(2.85, 5.45, 'Syncs & monitors health', ha='center', va='center', fontsize=7, color=colors['text'])

# Namespace container
draw_container(5.5, 0.8, 10, 6.7, 'field-content-demo namespace', colors['white'])

# Three pattern boxes
# Pattern 1: Helm
draw_container(5.8, 4.5, 3, 2.5, 'HELM Pattern', '#E8F5E9')
ax.text(7.3, 5.7, 'Values injected\nby ArgoCD', ha='center', va='center', fontsize=8, color=colors['text'])
draw_box(6.0, 4.7, 2.6, 0.6, colors['success'], 'K8s Resources', fontsize=8)

# Pattern 2: Kustomize
draw_container(9.0, 4.5, 3, 2.5, 'KUSTOMIZE Pattern', '#FFF3E0')
ax.text(10.5, 5.7, 'Static manifests\n(no env vars)', ha='center', va='center', fontsize=8, color=colors['text'])
draw_box(9.2, 4.7, 2.6, 0.6, '#FF9800', 'K8s Resources', fontsize=8)

# Pattern 3: Ansible
draw_container(12.2, 4.5, 3, 2.5, 'ANSIBLE Pattern', colors['ansible_light'])
ax.text(13.7, 5.7, 'Job runs\nplaybook', ha='center', va='center', fontsize=8, color=colors['text'])
draw_box(12.4, 4.7, 2.6, 0.6, colors['ansible'], 'Ansible Job', fontsize=8)

# Resources created
draw_container(5.8, 1.1, 9.4, 3, 'Created Resources', '#F5F5F5')

# Resource boxes
resources = [
    ('Deployment', 1.0), ('Service', 2.5), ('Route', 4.0),
    ('ConfigMap', 5.5), ('Secret', 7.0), ('CRDs', 8.2)
]
for name, offset in resources:
    draw_box(5.9 + offset, 2.8, 1.3, 0.5, colors['k8s'], name, fontsize=7)

# UserInfo ConfigMap (special - highlighted)
draw_box(6.5, 1.5, 4, 0.8, colors['success'], 'ConfigMap (userinfo)\nlabel: demo.redhat.com/userinfo', fontsize=8)
ax.text(12, 1.9, '← Data flows back to RHDP', ha='left', va='center', fontsize=8,
        color=colors['success'], fontweight='bold')

# =====================
# Arrows
# =====================
# RHDP to ArgoCD
draw_arrow((3.8, 9.5), (5.1, 9.5), colors['rhdp'])
ax.text(4.45, 9.7, 'Creates\nApplication', ha='center', va='bottom', fontsize=7, color=colors['rhdp'])

# Arrow down to cluster
draw_arrow((5.1, 9.5), (5.1, 7.8), colors['rhdp'])

# Git repo arrow into cluster
draw_arrow((12.2, 9.5), (10.9, 9.5), colors['github'])
ax.text(11.55, 9.7, 'Git Pull', ha='center', va='bottom', fontsize=7, color=colors['github'])
draw_arrow((10.9, 9.5), (10.9, 7.8), colors['github'])

# ArgoCD to namespaces
draw_arrow((5.0, 6.3), (5.8, 6.3), colors['argocd'])

# Ansible job to external repo (curved arrow)
arrow_ansible = FancyArrowPatch((14.7, 5.0), (14.7, 8.5),
                                arrowstyle='<->',
                                connectionstyle='arc3,rad=-0.3',
                                mutation_scale=12,
                                color=colors['ansible'], linewidth=1.5, linestyle='--')
ax.add_patch(arrow_ansible)
ax.text(15.3, 6.8, 'Clone\nRepo', ha='left', va='center', fontsize=7, color=colors['ansible'])

# =====================
# Legend
# =====================
legend_y = 0.1
ax.text(0.5, legend_y, 'Legend:', ha='left', va='center', fontsize=9, fontweight='bold')

# Legend items
legend_items = [
    (colors['rhdp'], 'RHDP Platform'),
    (colors['argocd'], 'ArgoCD'),
    (colors['k8s'], 'Kubernetes'),
    (colors['ansible'], 'Ansible'),
    (colors['success'], 'RHDP Integration'),
]
x_pos = 1.5
for color, label in legend_items:
    box = FancyBboxPatch((x_pos, legend_y - 0.15), 0.3, 0.3,
                          boxstyle="round,pad=0.02,rounding_size=0.05",
                          facecolor=color, edgecolor='none')
    ax.add_patch(box)
    ax.text(x_pos + 0.4, legend_y, label, ha='left', va='center', fontsize=8)
    x_pos += 2.2

# Save the figure
plt.tight_layout()
plt.savefig('/Users/nstephan/devel/field-content/docs/architecture-overview.png',
            dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
print("Saved: docs/architecture-overview.png")

# =====================
# Second diagram: Ansible Runner Detail
# =====================
fig2, ax2 = plt.subplots(1, 1, figsize=(14, 10))
ax2.set_xlim(0, 14)
ax2.set_ylim(0, 10)
ax2.set_aspect('equal')
ax2.axis('off')

# Title
ax2.text(7, 9.5, 'Ansible Runner - Detailed Flow', ha='center', va='center',
        fontsize=18, fontweight='bold', color=colors['text'])

# Step numbers
def draw_step(x, y, num):
    circle = Circle((x, y), 0.25, facecolor=colors['rhdp'], edgecolor='white', linewidth=2)
    ax2.add_patch(circle)
    ax2.text(x, y, str(num), ha='center', va='center', fontsize=10, fontweight='bold', color='white')

# GitHub box
github_box = FancyBboxPatch((0.5, 6), 3.5, 2.5, boxstyle="round,pad=0.02,rounding_size=0.2",
                             facecolor=colors['github_light'], edgecolor=colors['github'], linewidth=2)
ax2.add_patch(github_box)
ax2.text(2.25, 8.2, 'Playbook Repository', ha='center', va='center', fontsize=11, fontweight='bold')
ax2.text(2.25, 7.0, '> site.yml\n> requirements.yml\n> roles/',
         ha='center', va='center', fontsize=10, family='monospace')

# Ansible Galaxy box
galaxy_box = FancyBboxPatch((0.5, 2.5), 3.5, 2.5, boxstyle="round,pad=0.02,rounding_size=0.2",
                             facecolor='#FFEEE6', edgecolor='#CC0000', linewidth=2)
ax2.add_patch(galaxy_box)
ax2.text(2.25, 4.7, 'Ansible Galaxy', ha='center', va='center', fontsize=11, fontweight='bold')
ax2.text(2.25, 3.5, '* kubernetes.core\n* community.general\n* redhat.openshift',
         ha='center', va='center', fontsize=10, family='monospace')

# OpenShift cluster
cluster_box = FancyBboxPatch((5, 1), 8.5, 7.5, boxstyle="round,pad=0.02,rounding_size=0.2",
                              facecolor=colors['k8s_light'], edgecolor=colors['k8s'], linewidth=2)
ax2.add_patch(cluster_box)
ax2.text(9.25, 8.2, 'OpenShift Cluster', ha='center', va='center', fontsize=12, fontweight='bold', color=colors['k8s'])

# Job container
job_box = FancyBboxPatch((5.5, 4), 7.5, 4, boxstyle="round,pad=0.02,rounding_size=0.15",
                          facecolor=colors['ansible_light'], edgecolor=colors['ansible'], linewidth=2)
ax2.add_patch(job_box)
ax2.text(9.25, 7.7, 'Kubernetes Job: ansible-runner', ha='center', va='center', fontsize=11, fontweight='bold')

# Container inside job
container_box = FancyBboxPatch((5.8, 4.3), 6.9, 3.1, boxstyle="round,pad=0.02,rounding_size=0.1",
                                facecolor='white', edgecolor=colors['border'], linewidth=1)
ax2.add_patch(container_box)
ax2.text(9.25, 7.1, 'Container: UBI8 Python 3.9', ha='center', va='center', fontsize=9, fontweight='bold')

# Steps inside container
steps_text = """1. pip install ansible-core, kubernetes...
2. ansible-galaxy collection install
3. git clone playbook repo
4. ansible-playbook site.yml \\
     --extra-vars "cluster_domain=..."
5. Creates K8s resources via API"""
ax2.text(9.25, 5.5, steps_text, ha='center', va='center', fontsize=9, family='monospace')

# Created resources
resources_box = FancyBboxPatch((5.5, 1.3), 7.5, 2.2, boxstyle="round,pad=0.02,rounding_size=0.1",
                                facecolor='#E8F5E9', edgecolor=colors['success'], linewidth=2)
ax2.add_patch(resources_box)
ax2.text(9.25, 3.2, 'Resources Created by Playbook', ha='center', va='center', fontsize=10, fontweight='bold', color=colors['success'])

resource_items = ['Deployment', 'Service', 'Route', 'ConfigMap', 'Operators', 'CRDs']
for i, item in enumerate(resource_items):
    x = 6.0 + (i % 3) * 2.3
    y = 2.3 if i < 3 else 1.6
    box = FancyBboxPatch((x, y), 2, 0.5, boxstyle="round,pad=0.02,rounding_size=0.05",
                          facecolor=colors['k8s'], edgecolor='none')
    ax2.add_patch(box)
    ax2.text(x + 1, y + 0.25, item, ha='center', va='center', fontsize=8, color='white', fontweight='bold')

# Arrows
# Git clone arrow
arrow1 = FancyArrowPatch((4, 7.25), (5.8, 6.5), arrowstyle='-|>', mutation_scale=15,
                          color=colors['github'], linewidth=2)
ax2.add_patch(arrow1)
ax2.text(4.5, 7.2, 'git clone', ha='center', va='bottom', fontsize=8, color=colors['github'])

# Collection install arrow
arrow2 = FancyArrowPatch((4, 3.75), (5.8, 5.0), arrowstyle='-|>', mutation_scale=15,
                          color='#CC0000', linewidth=2)
ax2.add_patch(arrow2)
ax2.text(4.5, 4.0, 'install', ha='center', va='bottom', fontsize=8, color='#CC0000')

# K8s API arrow
arrow3 = FancyArrowPatch((9.25, 4.0), (9.25, 3.5), arrowstyle='-|>', mutation_scale=15,
                          color=colors['success'], linewidth=2)
ax2.add_patch(arrow3)

# Service Account note
sa_box = FancyBboxPatch((10.5, 0.3), 3, 0.6, boxstyle="round,pad=0.02,rounding_size=0.1",
                         facecolor='#FFF9C4', edgecolor='#F9A825', linewidth=1)
ax2.add_patch(sa_box)
ax2.text(12, 0.6, 'ServiceAccount Token', ha='center', va='center', fontsize=8, fontweight='bold')

# Environment variables note
env_text = """Environment Variables:
- CLUSTER_DOMAIN
- CLUSTER_API_URL
- NAMESPACE
- KUBECONFIG"""
ax2.text(0.5, 1.0, env_text, ha='left', va='bottom', fontsize=9,
         family='monospace', color=colors['text'],
         bbox=dict(boxstyle='round', facecolor='#E3F2FD', edgecolor=colors['k8s']))

plt.tight_layout()
plt.savefig('/Users/nstephan/devel/field-content/docs/ansible-runner-detail.png',
            dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
print("Saved: docs/ansible-runner-detail.png")

print("\nDone! Created two diagrams in docs/")
