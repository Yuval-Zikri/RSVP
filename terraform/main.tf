terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
  }
}

# Assuming Minikube is running locally and config is in default location
provider "kubernetes" {
  # config_path is omitted to allow dynamic detection via KUBECONFIG env var or default location
}

# Namespace for ArgoCD
resource "kubernetes_namespace" "argo" {
  metadata {
    name = "argo"
  }
}

# Namespace for the RSVP Application
resource "kubernetes_namespace" "rsvp_app" {
  metadata {
    name = "rsvp-app"
  }
}

# Install ArgoCD via kubectl apply
# This is a "wrapper" approach to execute the installation manifest
resource "null_resource" "install_argocd" {
  depends_on = [kubernetes_namespace.argo]

  # This ensures it runs, but we can prevent re-runs by checking existence in a real script.
  # For simplicity, we just run apply, which is idempotent.
  provisioner "local-exec" {
    command = "kubectl apply -n argo -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml"
  }
}
# Install CloudNativePG Operator via kubectl apply
resource "null_resource" "install_cnpg" {
  # This and ArgoCD should ideally both be installed
  # We use server-side apply as recommended by CNPG docs
  provisioner "local-exec" {
    command = "kubectl apply --server-side --force-conflicts -f https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/main/releases/cnpg-1.25.0.yaml"
  }
}
# Install Root Application (App of Apps) via ArgoCD
resource "null_resource" "install_root_app" {
  depends_on = [null_resource.install_argocd]

  provisioner "local-exec" {
    command = "kubectl apply -n argo -f ../k8s/Argo-CD/application.yaml"
  }
}
