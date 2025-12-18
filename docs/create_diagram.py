#!/usr/bin/env python3
"""
Generate architecture diagrams for Field Content project

Generates:
1. architecture-overview.png - Overall system architecture
2. ansible-runner-detail.png - Ansible runner job detail
3. helm-pattern.png - Helm deployment pattern
4. kustomize-pattern.png - Kustomize deployment pattern
5. ansible-pattern.png - Ansible deployment pattern
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
import os

# Output directory
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

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
    'helm': '#0F1689',           # Helm Blue
    'helm_light': '#E8E9F5',
    'kustomize': '#7B1FA2',      # Kustomize Purple
    'kustomize_light': '#F3E5F5',
    'showroom': '#00796B',       # Teal for Showroom
    'showroom_light': '#E0F2F1',
    'text': '#1A1A1A',
    'white': '#FFFFFF',
    'border': '#666666',
}

def draw_box(ax, x, y, width, height, color, label, fontsize=10, text_color='white'):
    """Draw a rounded rectangle with label"""
    box = FancyBboxPatch((x, y), width, height,
                          boxstyle="round,pad=0.02,rounding_size=0.1",
                          facecolor=color, edgecolor=colors['border'], linewidth=1.5)
    ax.add_patch(box)
    ax.text(x + width/2, y + height/2, label, ha='center', va='center',
            fontsize=fontsize, fontweight='bold', color=text_color, wrap=True)
    return box

def draw_container(ax, x, y, width, height, title, color, title_color=None):
    """Draw a container box with title"""
    container = FancyBboxPatch((x, y), width, height,
                                boxstyle="round,pad=0.02,rounding_size=0.15",
                                facecolor=color, edgecolor=colors['border'], linewidth=2)
    ax.add_patch(container)

    title_height = 0.4
    title_bar = FancyBboxPatch((x, y + height - title_height), width, title_height,
                                boxstyle="round,pad=0.02,rounding_size=0.1",
                                facecolor=title_color or colors['border'], edgecolor='none')
    ax.add_patch(title_bar)
    ax.text(x + width/2, y + height - title_height/2, title,
            ha='center', va='center', fontsize=11, fontweight='bold', color='white')
    return container

def draw_arrow(ax, start, end, color='#666666', style='-|>', connectionstyle='arc3,rad=0'):
    """Draw an arrow between two points"""
    arrow = FancyArrowPatch(start, end,
                            arrowstyle=style,
                            connectionstyle=connectionstyle,
                            mutation_scale=15,
                            color=color, linewidth=2)
    ax.add_patch(arrow)
    return arrow


def create_architecture_overview():
    """Create the main architecture overview diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.set_aspect('equal')
    ax.axis('off')

    # Title
    ax.text(8, 11.5, 'Field Content Architecture', ha='center', va='center',
            fontsize=20, fontweight='bold', color=colors['text'])
    ax.text(8, 11.1, 'Self-Service CI Development Platform for RHDP', ha='center', va='center',
            fontsize=12, color=colors['border'])

    # RHDP Section (Top Left)
    draw_container(ax, 0.3, 8.5, 3.5, 2.2, 'RED HAT DEMO PLATFORM', colors['rhdp_light'], colors['rhdp'])
    draw_box(ax, 0.5, 9.4, 3.1, 0.6, colors['rhdp'], 'User Portal', fontsize=9)
    ax.text(2.05, 8.9, '• Orders "Field Content" CI\n• Provides GitOps repo URL',
            ha='center', va='center', fontsize=8, color=colors['text'])

    # Developer Repo (Top Right)
    draw_container(ax, 12.2, 8.5, 3.5, 2.2, 'DEVELOPER GIT REPO', colors['github_light'], colors['github'])
    draw_box(ax, 12.4, 9.4, 3.1, 0.6, colors['github'], 'GitHub/GitLab', fontsize=9)
    ax.text(13.95, 8.9, '• Helm Chart / Kustomize\n• Ansible Playbooks',
            ha='center', va='center', fontsize=8, color=colors['text'])

    # OpenShift Cluster (Main Center Area)
    draw_container(ax, 0.3, 0.5, 15.4, 7.5, 'OPENSHIFT CLUSTER', colors['k8s_light'], colors['k8s'])

    # ArgoCD Box
    draw_container(ax, 0.6, 5.2, 4.5, 2.3, 'openshift-gitops', colors['argocd_light'], colors['argocd'])
    draw_box(ax, 0.8, 5.8, 4.1, 1.2, colors['argocd'], 'ArgoCD\nApplication Controller', fontsize=9)
    ax.text(2.85, 5.45, 'Syncs & monitors health', ha='center', va='center', fontsize=7, color=colors['text'])

    # Namespace container
    draw_container(ax, 5.5, 0.8, 10, 6.7, 'field-content-demo namespace', colors['white'], colors['border'])

    # Three pattern boxes
    draw_container(ax, 5.8, 4.5, 3, 2.5, 'HELM Pattern', colors['helm_light'], colors['helm'])
    ax.text(7.3, 5.7, 'Values injected\nby ArgoCD', ha='center', va='center', fontsize=8, color=colors['text'])
    draw_box(ax, 6.0, 4.7, 2.6, 0.6, colors['helm'], 'K8s Resources', fontsize=8)

    draw_container(ax, 9.0, 4.5, 3, 2.5, 'KUSTOMIZE Pattern', colors['kustomize_light'], colors['kustomize'])
    ax.text(10.5, 5.7, 'Static manifests\n(no env vars)', ha='center', va='center', fontsize=8, color=colors['text'])
    draw_box(ax, 9.2, 4.7, 2.6, 0.6, colors['kustomize'], 'K8s Resources', fontsize=8)

    draw_container(ax, 12.2, 4.5, 3, 2.5, 'ANSIBLE Pattern', colors['ansible_light'], colors['ansible'])
    ax.text(13.7, 5.7, 'Job runs\nplaybook', ha='center', va='center', fontsize=8, color=colors['text'])
    draw_box(ax, 12.4, 4.7, 2.6, 0.6, colors['ansible'], 'Ansible Job', fontsize=8)

    # Resources created
    draw_container(ax, 5.8, 1.1, 9.4, 3, 'Created Resources', '#F5F5F5', colors['border'])

    # Evenly spaced resource boxes
    resources = ['Deployment', 'Service', 'Route', 'ConfigMap', 'Secret', 'CRDs']
    box_width = 1.3
    total_width = 8.8  # Available width inside container
    spacing = (total_width - (len(resources) * box_width)) / (len(resources) + 1)
    for i, name in enumerate(resources):
        x_pos = 6.0 + spacing + i * (box_width + spacing)
        draw_box(ax, x_pos, 2.8, box_width, 0.5, colors['k8s'], name, fontsize=7)

    # Showroom box (optional deployment that uses data from workloads)
    draw_box(ax, 6.5, 1.5, 4.5, 0.8, colors['showroom'], 'Showroom (optional)\nLab guide using workload data', fontsize=8)
    ax.text(11.2, 1.9, '← Uses data from resources', ha='left', va='center', fontsize=8,
            color=colors['showroom'], fontweight='bold')

    # Arrows
    draw_arrow(ax, (3.8, 9.5), (5.1, 9.5), colors['rhdp'])
    ax.text(4.45, 9.7, 'Creates\nApplication', ha='center', va='bottom', fontsize=7, color=colors['rhdp'])
    draw_arrow(ax, (5.1, 9.5), (5.1, 7.8), colors['rhdp'])

    draw_arrow(ax, (12.2, 9.5), (10.9, 9.5), colors['github'])
    ax.text(11.55, 9.7, 'Git Pull', ha='center', va='bottom', fontsize=7, color=colors['github'])
    draw_arrow(ax, (10.9, 9.5), (10.9, 7.8), colors['github'])

    draw_arrow(ax, (5.0, 6.3), (5.8, 6.3), colors['argocd'])

    # Legend
    legend_y = 0.1
    ax.text(0.5, legend_y, 'Legend:', ha='left', va='center', fontsize=9, fontweight='bold')
    legend_items = [
        (colors['rhdp'], 'RHDP Platform'),
        (colors['argocd'], 'ArgoCD'),
        (colors['k8s'], 'Kubernetes'),
        (colors['ansible'], 'Ansible'),
        (colors['showroom'], 'Showroom'),
    ]
    x_pos = 1.5
    for color, label in legend_items:
        box = FancyBboxPatch((x_pos, legend_y - 0.15), 0.3, 0.3,
                              boxstyle="round,pad=0.02,rounding_size=0.05",
                              facecolor=color, edgecolor='none')
        ax.add_patch(box)
        ax.text(x_pos + 0.4, legend_y, label, ha='left', va='center', fontsize=8)
        x_pos += 2.2

    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, 'architecture-overview.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print(f"Saved: {output_path}")


def create_ansible_runner_detail():
    """Create the Ansible runner detail diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')

    ax.text(7, 9.5, 'Ansible Runner - Detailed Flow', ha='center', va='center',
            fontsize=18, fontweight='bold', color=colors['text'])

    # GitHub box
    github_box = FancyBboxPatch((0.5, 6), 3.5, 2.5, boxstyle="round,pad=0.02,rounding_size=0.2",
                                 facecolor=colors['github_light'], edgecolor=colors['github'], linewidth=2)
    ax.add_patch(github_box)
    ax.text(2.25, 8.2, 'Playbook Repository', ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(2.25, 7.0, '> site.yml\n> roles/\n> ansible.cfg',
             ha='center', va='center', fontsize=10, family='monospace')

    # Ansible Galaxy box
    galaxy_box = FancyBboxPatch((0.5, 2.5), 3.5, 2.5, boxstyle="round,pad=0.02,rounding_size=0.2",
                                 facecolor='#FFEEE6', edgecolor='#CC0000', linewidth=2)
    ax.add_patch(galaxy_box)
    ax.text(2.25, 4.7, 'Ansible Galaxy', ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(2.25, 3.5, '* kubernetes.core\n* community.general',
             ha='center', va='center', fontsize=10, family='monospace')

    # OpenShift cluster
    cluster_box = FancyBboxPatch((5, 1), 8.5, 7.5, boxstyle="round,pad=0.02,rounding_size=0.2",
                                  facecolor=colors['k8s_light'], edgecolor=colors['k8s'], linewidth=2)
    ax.add_patch(cluster_box)
    ax.text(9.25, 8.2, 'OpenShift Cluster', ha='center', va='center', fontsize=12, fontweight='bold', color=colors['k8s'])

    # Job container
    job_box = FancyBboxPatch((5.5, 4), 7.5, 4, boxstyle="round,pad=0.02,rounding_size=0.15",
                              facecolor=colors['ansible_light'], edgecolor=colors['ansible'], linewidth=2)
    ax.add_patch(job_box)
    ax.text(9.25, 7.7, 'Kubernetes Job: ansible-runner', ha='center', va='center', fontsize=11, fontweight='bold')

    container_box = FancyBboxPatch((5.8, 4.3), 6.9, 3.1, boxstyle="round,pad=0.02,rounding_size=0.1",
                                    facecolor='white', edgecolor=colors['border'], linewidth=1)
    ax.add_patch(container_box)
    ax.text(9.25, 7.1, 'Container: UBI8 Python 3.9', ha='center', va='center', fontsize=9, fontweight='bold')

    steps_text = """1. pip install ansible-core, kubernetes...
2. ansible-galaxy collection install
3. git clone playbook repo
4. ansible-playbook site.yml \\
     --extra-vars "cluster_domain=..."
5. Creates K8s resources via API"""
    ax.text(9.25, 5.5, steps_text, ha='center', va='center', fontsize=9, family='monospace')

    # Created resources
    resources_box = FancyBboxPatch((5.5, 1.3), 7.5, 2.2, boxstyle="round,pad=0.02,rounding_size=0.1",
                                    facecolor='#E8F5E9', edgecolor=colors['success'], linewidth=2)
    ax.add_patch(resources_box)
    ax.text(9.25, 3.2, 'Resources Created by Playbook', ha='center', va='center', fontsize=10, fontweight='bold', color=colors['success'])

    resource_items = ['Operator', 'Deployment', 'Service', 'Showroom', 'ConfigMap', 'Route']
    for i, item in enumerate(resource_items):
        x = 6.0 + (i % 3) * 2.3
        y = 2.3 if i < 3 else 1.6
        box = FancyBboxPatch((x, y), 2, 0.5, boxstyle="round,pad=0.02,rounding_size=0.05",
                              facecolor=colors['k8s'], edgecolor='none')
        ax.add_patch(box)
        ax.text(x + 1, y + 0.25, item, ha='center', va='center', fontsize=8, color='white', fontweight='bold')

    # Arrows
    arrow1 = FancyArrowPatch((4, 7.25), (5.8, 6.5), arrowstyle='-|>', mutation_scale=15,
                              color=colors['github'], linewidth=2)
    ax.add_patch(arrow1)
    ax.text(4.5, 7.2, 'git clone', ha='center', va='bottom', fontsize=8, color=colors['github'])

    arrow2 = FancyArrowPatch((4, 3.75), (5.8, 5.0), arrowstyle='-|>', mutation_scale=15,
                              color='#CC0000', linewidth=2)
    ax.add_patch(arrow2)
    ax.text(4.5, 4.0, 'install', ha='center', va='bottom', fontsize=8, color='#CC0000')

    arrow3 = FancyArrowPatch((9.25, 4.0), (9.25, 3.5), arrowstyle='-|>', mutation_scale=15,
                              color=colors['success'], linewidth=2)
    ax.add_patch(arrow3)

    # Environment variables note
    env_text = """Environment Variables:
- CLUSTER_DOMAIN
- CLUSTER_API_URL
- NAMESPACE
- KUBECONFIG"""
    ax.text(0.5, 1.0, env_text, ha='left', va='bottom', fontsize=9,
             family='monospace', color=colors['text'],
             bbox=dict(boxstyle='round', facecolor='#E3F2FD', edgecolor=colors['k8s']))

    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, 'ansible-runner-detail.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print(f"Saved: {output_path}")


def create_helm_pattern():
    """Create the Helm pattern diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')

    ax.text(7, 7.5, 'Helm Deployment Pattern', ha='center', va='center',
            fontsize=18, fontweight='bold', color=colors['helm'])
    ax.text(7, 7.1, 'GitOps deployment with value injection', ha='center', va='center',
            fontsize=11, color=colors['border'])

    # Developer workflow (left)
    draw_container(ax, 0.3, 4, 3.5, 2.5, 'DEVELOPER', colors['github_light'], colors['github'])
    ax.text(2.05, 5.5, '1. Create Helm chart\n2. Define values.yaml\n3. Push to Git',
            ha='center', va='center', fontsize=9, color=colors['text'])

    # Git repo
    draw_box(ax, 0.5, 2.5, 3.1, 1, colors['github'], 'Git Repository\nChart + values.yaml', fontsize=9)

    # ArgoCD
    draw_container(ax, 5, 4, 4, 2.5, 'ARGOCD', colors['argocd_light'], colors['argocd'])
    ax.text(7, 5.5, '• Pulls chart from Git\n• Injects deployer.domain\n• Renders templates',
            ha='center', va='center', fontsize=9, color=colors['text'])

    # OpenShift Cluster
    draw_container(ax, 10, 2.5, 3.5, 4, 'OPENSHIFT', colors['k8s_light'], colors['k8s'])

    resources = ['Subscription', 'Namespace', 'Deployment', 'Service', 'Showroom', 'Userinfo']
    for i, res in enumerate(resources):
        y = 5.7 - (i * 0.55)
        draw_box(ax, 10.3, y, 2.9, 0.45, colors['helm'] if i < 4 else colors['showroom'], res, fontsize=8)

    # Sync waves
    ax.text(10.1, 2.8, 'Sync Waves: 1→2→3→5→6', ha='left', va='center', fontsize=8, color=colors['border'])

    # Arrows
    draw_arrow(ax, (2.05, 4), (2.05, 3.5), colors['github'])
    draw_arrow(ax, (3.8, 3), (5, 5.2), colors['github'])
    ax.text(4.2, 4.3, 'Git Pull', ha='center', va='center', fontsize=8, color=colors['github'])
    draw_arrow(ax, (9, 5.2), (10, 5.2), colors['argocd'])
    ax.text(9.5, 5.4, 'Apply', ha='center', va='center', fontsize=8, color=colors['argocd'])

    # Key benefits box
    benefits_box = FancyBboxPatch((0.3, 0.3), 6, 1.5, boxstyle="round,pad=0.02,rounding_size=0.1",
                                   facecolor='#E8F5E9', edgecolor=colors['success'], linewidth=1)
    ax.add_patch(benefits_box)
    ax.text(3.3, 1.5, 'Key Benefits', ha='center', va='center', fontsize=10, fontweight='bold', color=colors['success'])
    ax.text(3.3, 0.8, '✓ Value injection ({{ .Values.deployer.domain }})\n✓ Conditional resources ({{- if }})\n✓ ~30 second deploy time',
            ha='center', va='center', fontsize=9, color=colors['text'])

    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, 'helm-pattern.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print(f"Saved: {output_path}")


def create_kustomize_pattern():
    """Create the Kustomize pattern diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')

    ax.text(7, 7.5, 'Kustomize Deployment Pattern', ha='center', va='center',
            fontsize=18, fontweight='bold', color=colors['kustomize'])
    ax.text(7, 7.1, 'GitOps deployment with static manifests', ha='center', va='center',
            fontsize=11, color=colors['border'])

    # Developer workflow (left)
    draw_container(ax, 0.3, 4, 3.5, 2.5, 'DEVELOPER', colors['github_light'], colors['github'])
    ax.text(2.05, 5.5, '1. Create YAML manifests\n2. Add kustomization.yaml\n3. Push to Git',
            ha='center', va='center', fontsize=9, color=colors['text'])

    # Git repo
    draw_box(ax, 0.5, 2.5, 3.1, 1, colors['github'], 'Git Repository\nkustomization.yaml', fontsize=9)

    # ArgoCD
    draw_container(ax, 5, 4, 4, 2.5, 'ARGOCD', colors['argocd_light'], colors['argocd'])
    ax.text(7, 5.5, '• Pulls manifests from Git\n• Runs kustomize build\n• Applies common labels',
            ha='center', va='center', fontsize=9, color=colors['text'])

    # OpenShift Cluster
    draw_container(ax, 10, 2.5, 3.5, 4, 'OPENSHIFT', colors['k8s_light'], colors['k8s'])

    resources = ['Subscription', 'Namespace', 'Deployment', 'Service', 'Showroom', 'Userinfo']
    for i, res in enumerate(resources):
        y = 5.7 - (i * 0.55)
        draw_box(ax, 10.3, y, 2.9, 0.45, colors['kustomize'] if i < 4 else colors['showroom'], res, fontsize=8)

    ax.text(10.1, 2.8, 'Sync Waves: 1→2→3→5→6', ha='left', va='center', fontsize=8, color=colors['border'])

    # Arrows
    draw_arrow(ax, (2.05, 4), (2.05, 3.5), colors['github'])
    draw_arrow(ax, (3.8, 3), (5, 5.2), colors['github'])
    ax.text(4.2, 4.3, 'Git Pull', ha='center', va='center', fontsize=8, color=colors['github'])
    draw_arrow(ax, (9, 5.2), (10, 5.2), colors['argocd'])
    ax.text(9.5, 5.4, 'Apply', ha='center', va='center', fontsize=8, color=colors['argocd'])

    # Key benefits box - centered at bottom
    benefits_box = FancyBboxPatch((3.5, 0.3), 7, 1.5, boxstyle="round,pad=0.02,rounding_size=0.1",
                                   facecolor='#E8F5E9', edgecolor=colors['success'], linewidth=1)
    ax.add_patch(benefits_box)
    ax.text(7, 1.5, 'Key Benefits', ha='center', va='center', fontsize=10, fontweight='bold', color=colors['success'])
    ax.text(7, 0.8, '✓ Plain YAML (no templating)\n✓ Easy to read and maintain',
            ha='center', va='center', fontsize=9, color=colors['text'])

    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, 'kustomize-pattern.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print(f"Saved: {output_path}")


def create_ansible_pattern():
    """Create the Ansible pattern diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 9))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.set_aspect('equal')
    ax.axis('off')

    ax.text(7, 8.5, 'Ansible Deployment Pattern', ha='center', va='center',
            fontsize=18, fontweight='bold', color=colors['ansible'])
    ax.text(7, 8.1, 'GitOps deployment with guaranteed ordering via ansible-runner job', ha='center', va='center',
            fontsize=11, color=colors['border'])

    # Developer workflow (left)
    draw_container(ax, 0.3, 5, 3.5, 2.5, 'DEVELOPER', colors['github_light'], colors['github'])
    ax.text(2.05, 6.5, '1. Create Ansible playbooks\n2. Define gitops/values.yaml\n3. Push to Git',
            ha='center', va='center', fontsize=9, color=colors['text'])

    # Git repo with two parts
    draw_box(ax, 0.3, 3.8, 1.6, 0.8, colors['github'], 'gitops/\nHelm chart', fontsize=8)
    draw_box(ax, 2.1, 3.8, 1.6, 0.8, colors['ansible'], 'playbooks/\nAnsible', fontsize=8)

    # ArgoCD
    draw_container(ax, 5, 5, 4, 2.5, 'ARGOCD', colors['argocd_light'], colors['argocd'])
    ax.text(7, 6.5, '• Deploys ansible-runner\n  Helm chart\n• Injects cluster_domain',
            ha='center', va='center', fontsize=9, color=colors['text'])

    # OpenShift Cluster - sized to fit ansible-runner and resources with proper spacing
    draw_container(ax, 10, 2.0, 3.5, 5.5, 'OPENSHIFT', colors['k8s_light'], colors['k8s'])

    # Ansible runner job - positioned inside cluster box with proper margin
    draw_container(ax, 10.2, 5.0, 3.1, 2.0, 'ansible-runner', colors['ansible_light'], colors['ansible'])
    ax.text(11.75, 5.6, '• Clone playbooks\n• Run site.yml\n• Wait for resources',
            ha='center', va='center', fontsize=8, color=colors['text'])

    # Created resources - evenly spaced below the job with no overlap
    resources = ['Operator', 'Deployment', 'Showroom', 'Userinfo']
    start_y = 4.3
    spacing = 0.55
    for i, res in enumerate(resources):
        y = start_y - (i * spacing)
        color = colors['showroom'] if res in ['Showroom', 'Userinfo'] else colors['k8s']
        draw_box(ax, 10.4, y, 2.9, 0.45, color, res, fontsize=8)

    ax.text(11.85, 2.15, 'Sequential with WAIT', ha='center', va='center', fontsize=8, color=colors['success'], fontweight='bold')

    # Arrows
    draw_arrow(ax, (1.1, 5), (1.1, 4.6), colors['github'])
    draw_arrow(ax, (2.9, 5), (2.9, 4.6), colors['ansible'])
    draw_arrow(ax, (3.8, 4.2), (5, 6.2), colors['github'])
    ax.text(4.2, 5.4, 'Git Pull\n(chart)', ha='center', va='center', fontsize=7, color=colors['github'])
    draw_arrow(ax, (9, 6.2), (10.2, 6.2), colors['argocd'])
    ax.text(9.6, 6.4, 'Deploy\nJob', ha='center', va='center', fontsize=7, color=colors['argocd'])

    # Job creates resources - arrow from job to first resource
    draw_arrow(ax, (11.85, 5.0), (11.85, 4.75), colors['success'])

    # Key benefits box - centered at bottom
    benefits_box = FancyBboxPatch((3.5, 0.3), 7, 1.5, boxstyle="round,pad=0.02,rounding_size=0.1",
                                   facecolor='#E8F5E9', edgecolor=colors['success'], linewidth=1)
    ax.add_patch(benefits_box)
    ax.text(7, 1.5, 'Key Benefits', ha='center', va='center', fontsize=10, fontweight='bold', color=colors['success'])
    ax.text(7, 0.85, '✓ Simple to write                    ✓ Conditional logic available\n✓ Guaranteed deployment sequence     ✓ Error handling and retries',
            ha='center', va='center', fontsize=9, color=colors['text'])

    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, 'ansible-pattern.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print(f"Saved: {output_path}")


if __name__ == '__main__':
    print("Generating diagrams...")
    create_architecture_overview()
    create_ansible_runner_detail()
    create_helm_pattern()
    create_kustomize_pattern()
    create_ansible_pattern()
    print("\nDone! Created 5 diagrams in docs/")
