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

variable "enable_port_forward" {
  type    = bool
  default = true
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
    command = "kubectl apply --server-side --force-conflicts -n argo -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml"
  }
}

# Install CloudNativePG Operator via kubectl apply
resource "null_resource" "install_cnpg" {
  triggers = {
    always_run = "${timestamp()}"
  }

  provisioner "local-exec" {
    command = <<-EOT
      kubectl apply --server-side --force-conflicts -f https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/main/releases/cnpg-1.25.0.yaml
      echo "Waiting for CNPG operator to be ready..."
      kubectl wait --for=condition=available --timeout=120s deployment/cnpg-controller-manager -n cnpg-system
    EOT
  }
}

# Install Root Application (App of Apps) via ArgoCD
resource "null_resource" "install_root_app" {
  depends_on = [null_resource.argocd_rbac_admin, null_resource.install_cnpg]

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
        if kubectl get crd applications.argoproj.io applicationsets.argoproj.io >/dev/null 2>&1; then
          echo "CRDs found, waiting for them to be established..."
          kubectl wait --for=condition=established --timeout=60s crd/applications.argoproj.io crd/applicationsets.argoproj.io
          break
        fi
        count=$((count + 1))
        echo "Waiting for CRD registration (attempt $count)..."
        sleep 5
      done
      kubectl apply -n argo -f ../k8s/Argo-CD/application.yaml
      kubectl apply -f ../k8s/ --recursive
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
# Automated Port-Forwarding (Development Only)
resource "null_resource" "port_forwarding" {
  count      = var.enable_port_forward ? 1 : 0
  depends_on = [null_resource.install_root_app]

  triggers = {
    # Run whenever the root app is re-installed or updated
    root_app_trigger = null_resource.install_root_app.id
  }

  provisioner "local-exec" {
    command = <<-EOT
      echo "Waiting for services to be ready before port-forwarding..."
      
      # Wait for deployments to be available
      kubectl wait --for=condition=available --timeout=120s deployment/argocd-server -n argo
      kubectl wait --for=condition=available --timeout=120s deployment/grafana -n rsvp-app
      kubectl wait --for=condition=available --timeout=120s deployment/backend -n rsvp-app
      
      echo "Deployments are available. Starting automated port-forwards..."
      
      # Determine if we are on Windows (check for powershell.exe)
      if command -v powershell.exe >/dev/null 2>&1 || command -v powershell >/dev/null 2>&1; then
          echo "Windows detected. Starting detached background processes..."
          
          # Kill any existing port-forwards
          powershell -Command "Get-Process -Name 'kubectl' -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -match 'port-forward' } | Stop-Process -Force"
          
          # Use Start-Process with -WindowStyle Hidden to truly decouple from Terraform
          powershell -Command "Start-Process kubectl -ArgumentList 'port-forward svc/argocd-server -n argo 8888:443' -WindowStyle Hidden"
          powershell -Command "Start-Process kubectl -ArgumentList 'port-forward svc/grafana -n rsvp-app 3001:80' -WindowStyle Hidden"
          powershell -Command "Start-Process kubectl -ArgumentList 'port-forward svc/backend -n rsvp-app 5000:5000' -WindowStyle Hidden"
      else
          echo "Linux/Other detected. Starting port-forwards in background using nohup..."
          
          # Kill existing ones if pkill is available
          pkill -f "kubectl port-forward" || true
          
          nohup kubectl port-forward svc/argocd-server -n argo 8888:443 >/dev/null 2>&1 &
          nohup kubectl port-forward svc/grafana -n rsvp-app 3001:80 >/dev/null 2>&1 &
          nohup kubectl port-forward svc/backend -n rsvp-app 5000:5000 >/dev/null 2>&1 &
      fi
      
      echo "Port-forwards successfully initiated in the background."
    EOT
  }
}
