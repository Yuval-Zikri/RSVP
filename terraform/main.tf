terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
  }
}

variable "kubeconfig" {
  type    = string
  default = "~/.kube/config"
}

provider "kubernetes" {
  config_path = var.kubeconfig
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
resource "null_resource" "install_argocd" {
  depends_on = [kubernetes_namespace.argo]

  # We force this to run every time to ensure ArgoCD is present even if the cluster was reset.
  # kubectl apply is idempotent, so this is safe.
  triggers = {
    always_run = "${timestamp()}"
  }

  provisioner "local-exec" {
    command = "kubectl apply -n argo -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml"
  }
}

# Install CloudNativePG Operator via kubectl apply
resource "null_resource" "install_cnpg" {
  triggers = {
    always_run = "${timestamp()}"
  }

  provisioner "local-exec" {
    command = "kubectl apply --server-side --force-conflicts -f https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/main/releases/cnpg-1.25.0.yaml"
  }
}

# Install Root Application (App of Apps) via ArgoCD
resource "null_resource" "install_root_app" {
  depends_on = [null_resource.argocd_rbac_admin]

  triggers = {
    always_run = "${timestamp()}"
  }

  provisioner "local-exec" {
    # CRITICAL: We MUST wait for the CRDs to be fully established and the API to recognize them.
    # We use a portable while loop because brace expansion ({1..20}) is not supported in all shells (like /bin/sh).
    command = <<-EOT
      echo "Waiting for ArgoCD CRDs..."
      count=0
      while [ $count -lt 30 ]; do
        if kubectl get crd applications.argoproj.io >/dev/null 2>&1; then
          echo "CRD found, waiting for it to be established..."
          kubectl wait --for=condition=established --timeout=60s crd/applications.argoproj.io
          break
        fi
        count=$((count + 1))
        echo "Waiting for CRD registration (attempt $count)..."
        sleep 5
      done
      kubectl apply -n argo -f ../k8s/Argo-CD/application.yaml
    EOT
  }
}

# Grant Cluster-Admin to ArgoCD Controller (Fixes all RBAC/Comparison Errors)
resource "null_resource" "argocd_rbac_admin" {
  depends_on = [null_resource.install_argocd]

  triggers = {
    always_run = "${timestamp()}"
  }

  provisioner "local-exec" {
    command = "kubectl create clusterrolebinding argocd-application-controller-admin --clusterrole=cluster-admin --serviceaccount=argo:argocd-application-controller --dry-run=client -o yaml | kubectl apply -f -"
  }
}

# Prepare Minikube Host (One-time setup for HostPath volumes)
resource "null_resource" "prepare_minikube_host" {
  triggers = {
    always_run = "${timestamp()}"
  }

  provisioner "local-exec" {
    # Ensure the HostPath directory exists for the background image volume.
    # We use a temporary pod to do this since we don't have 'minikube' CLI in the Jenkins container.
    command = <<-EOT
      echo "Preparing Minikube host directories via temporary pod..."
      kubectl delete pod host-prep --ignore-not-found=true
      kubectl run host-prep --image=busybox --restart=Never --overrides='{"spec": {"containers": [{"name": "host-prep", "image": "busybox", "command": ["sh", "-c", "mkdir -p /host/project/frontend/src/background && chmod 777 /host/project/frontend/src/background"], "volumeMounts": [{"name": "host-root", "mountPath": "/host"}]}], "volumes": [{"name": "host-root", "hostPath": {"path": "/"}}]}}'
      echo "Waiting for host-prep execution..."
      sleep 5
      kubectl delete pod host-prep
    EOT
  }
}
