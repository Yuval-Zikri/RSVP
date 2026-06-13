# 🎉 Event Manager System

![Event Manager Banner](https://img.shields.io/badge/Event-Manager-blueviolet?style=for-the-badge) ![Version](https://img.shields.io/badge/Version-1.0-blue?style=for-the-badge) ![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

A modern, full-stack application for managing events, invitations, and RSVPs. Built with a focus on user experience, localization (Hebrew/English), and seamless email integration.

![DevOps Architecture](RSVP_App%20-Devops%20Architecture.png)

---

## 🚀 Features

### 📅 Event Management
*   **Smart Creation Wizard**: Step-by-step wizard to create events (Wedding, Birthday, Party).
*   **Location Integration**: Built-in Waze & OpenStreetMap search to pinpoint exact event locations.
*   **Custom Themes**: Choose dynamic backgrounds for event pages and emails.

### 💌 Invitation System
*   **Email Automation**: Automatically sends beautiful HTML invitations to guests.
*   **RSVP Tracking**: Guests can confirm attendance directly from the email link.
*   **Live Updates**: Dashboard updates in real-time as guests respond.

### 📊 Dashboard & Analytics
*   **Guest Management**: View, edit, and remove guests.
*   **Statistics**: Track "Attending", "Pending", and "Declined" statuses instantly.
*   **Excel Export**: One-click export of guest lists for printing or vendor use.
*   **Localization**: Full support for **English** (LTR) and **Hebrew** (RTL).

---

## 🛠️ Tech Stack

### Frontend
*   ![React](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB) **React.js** (Vite)
*   **Context API** for State Management
*   **CSS Modules / Variables** for Theming covering Dark/Light modes
*   **Leaflet** for Maps
*   **Axios** for API Communication

### Backend
*   ![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white) **Python Flask**
*   **SQLAlchemy** (ORM) with **PostgreSQL**
*   **Flask-Mail** for SMTP integration
*   **Docker** for containerization

### DevOps & Tools
*   ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) **Docker Compose**
*   **Kubernetes** (Orchestration)
*   **Terraform** (Infrastructure as Code - 1-Click Setup)
*   **ArgoCD** (GitOps Delivery - App-of-Apps Pattern)
*   **CloudNativePG** (High Availability Database Operator)
*   **Chaoskube** (Resilience Testing)
*   **Ngrok** for external tunneling (optional)
*   **Prometheus** for metrics
*   **Grafana** for monitoring dashboards

---

## 📂 Project Structure

The project is organized for scalability and maintainability:

```plaintext
event-manager/
├── 🐳 docker-compose.yaml     # Local Dev orchestration
├── 🐳 docker-compose.ci.yaml  # CI-specific orchestration (Image tags for Push)
├── 📄 Jenkinsfile             # CI/CD Pipeline (Terraform + Docker + GitOps)
├── 📄 Jenkins.Dockerfile      # Custom Jenkins Image with Docker CLI
├── 📂 terraform/              # Infrastructure as Code (IaC)
│   ├── 📄 main.tf             # Cluster Setup (Namespaces, ArgoCD)
│   └── 📄 terraform.tfstate   # State file (Local)
├── 📂 tests/                  # Automated Test Suite
│   ├── 📄 integration_test.py # Backend Integration Tests
│   └── 📄 selenium_test.py    # Frontend UI Tests
├── 📂 k8s/                    # Kubernetes Manifests (HA)
│   ├── 📂 Argo-CD/            # ArgoCD Application Manifests
│   ├── 📂 namespaces/         # Namespace definition
│   ├── 📂 database/           # CloudNativePG Cluster
│   ├── 📂 backend/            # Deployment, Service, HPA
│   ├── 📂 frontend/           # Deployment, Service, HPA
│   ├── 📂 ngrok/              # External Access
│   ├── 📂 chaos/              # Chaoskube Configuration
│   ├── 📂 prometheus/         # Monitoring - Prometheus
│   └── 📂 grafana/            # Monitoring - Grafana Dashboards
├── 📂 backend/
│   ├── 📂 routes/
│   │   ├── 📂 events/         # Event CRUD & Actions
│   │   ├── 📂 invitations/    # Email sending endpoints
│   │   ├── 📂 locations/      # Map & Geocoding endpoints
│   │   └── 📂 rsvp/           # Guest confirmation endpoints
│   ├── 📂 services/
│   │   ├── 📂 email/          # Template gen & Sending logic
│   │   └── 📂 locations/      # Waze/OSM integration
│   ├── 📂 scripts/            # DB Maintenance (wait-for-db, reset)
│   ├── 📄 app.py              # App Factory
│   ├── 📄 config.py           # Central Configuration
│   ├── 📄 extensions.py       # Flask Extensions (DB, Mail)
│   ├── 📄 models.py           # DB Models
│   ├── 📄 requirements.txt    # Python Dependencies
│   ├── 📄 Dockerfile          # Backend Image
│   └── 📄 .env.example        # Environment Variables Template
└── 📂 frontend/
    ├── 📄 package.json        # JS Dependencies
    ├──  vite.config.js      # Build Configuration
    ├── 📄 nginx.conf          # Web Server Config
    ├── 📄 Dockerfile          # Frontend Image
    ├── 📂 src/
    │   ├── 📂 background/     # Static background assets (Images)
    │   ├── 📂 components/     # Reusable UI Components
    │   ├── 📂 pages/          # Route Pages (CreateEvent, Dashboard)
    │   ├── � styles/         # CSS Modules & Themes
    │   ├── 📂 utils/          # Helpers & Translations
    │   ├── 📄 App.jsx         # Main App Component
    │   ├── 📄 main.jsx        # Entry Point
    │   └── 📄 contexts.js     # React Context Definitions
```

---

## ⚡ Quick Start

### Prerequisites
*   [Docker Desktop](https://www.docker.com/products/docker-desktop) installed.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/event-manager.git
    cd event-manager
    ```

2.  **Environment Setup:**
    Create a `.env` file in the `backend/` directory (see `.env.example`).
    ```env
    DATABASE_URL=postgresql://user:password@postgres:5432/events_db
    MAIL_SERVER=smtp.mailtrap.io
    ...
    ```

3.  **Run with Docker:**
    ```bash
    docker-compose up -d --build
    ```

4.  **Access the App:**
    *   Frontend: [http://localhost:3000](http://localhost:3000)
    *   Backend API: [http://localhost:5000](http://localhost:5000)

---

## 🔍 Key Components Usage

### Dashboard
Located at `/dashboard`. Provides a high-level view of all your events. Use the "Export to Excel" button to get a list for your door security or caterer.

### Create Event
Located at `/create-event`. A 4-step wizard:
1.  **Type**: Select event type (Wedding, etc.)
2.  **Details**: Title, Date, Location (Search via Waze API).
3.  **Guests**: Add guests manually or strictly.
4.  **Review**: Finalize and send invites.

---

## 🎨 Design & theming

The application uses a robust CSS variable system defined in `base.css` and `theme.css`.
It supports system-based **standard** and **dark** modes, along with RTL support for Hebrew users.

---

## ☁️ Kubernetes & High Availability

This project is designed to run on a **High Availability (HA)** Kubernetes cluster, ensuring zero downtime even during failures.

### 🏗️ Architecture
*   **Frontend**: Runs **3 replicas** behind a Service (LoadBalancer/NodePort).
*   **Backend**: Runs **3 replicas**, fully stateless.
*   **Database**: Uses **CloudNativePG Operator** to manage a PostgreSQL Cluster with:
    *   1 Primary Instance (Read/Write)
    *   2 Standby Instances (Read/Replication)
    *   Automatic Failover & Self-Healing

### 💥 Chaos Engineering
The system includes **Chaoskube** to continuously test resilience.
*   **What it does**: Randomly kills a pod every **2 minutes**.
*   **Goal**: Prove that the application recovers automatically without user intervention.
*   **Configuration**: Defined in `k8s/chaos/chaoskube.yaml`.

---

## ⚡ Zero-to-Hero: Fresh Start / Recovery Guide
Use this guide if you just ran `minikube delete` or if this is your first time setting up the project.

### 1. Start the Environment
```powershell
minikube start
minikube tunnel  # Keep this terminal open!
```

### 2. Update Jenkins Connection
Since a fresh Minikube cluster has a new internal IP/Certificates, you must update Jenkins:
1.  **Get new Config (Modified for Jenkins)**:
    Run this in PowerShell to generate the portable file for Jenkins (using `host.docker.internal`):
    ```powershell
    $port = (kubectl config view -o jsonpath="{.clusters[?(@.name=='minikube')].cluster.server}" | Split-Path -Leaf).Split(':')[-1]
    kubectl config view --flatten --minify | %{ $_ -replace "https://127.0.0.1:$port", "https://host.docker.internal:$port" -replace 'certificate-authority-data:.*', 'insecure-skip-tls-verify: true' } > kubeconfig_for_jenkins
    ```
2.  **Update Jenkins**: Go to Jenkins -> Credentials -> System -> Global -> Find `kubeconfig` -> Edit -> Upload the output above as a new file.

### 3. Deploy everything (One-Click)
Choose **ONE** of the following:
*   **Via Jenkins (Recommended)**: Simply click **"Build Now"** on your pipeline. It will run Terraform, build images, run tests, and deploy everything via Argo CD.
*   **Via Local Terraform**:
    ```bash
    cd terraform
    terraform init
    terraform apply -auto-approve
    ```

> [!TIP]
> **What's automated?** 
> Everything! Terraform will automatically create host directories (`/project/...`), fix Argo CD permissions, and install the "Root App" which pulls all services recursively. Jenkins will dynamically inject your Ngrok Token and Docker secrets.

---

## ♾️ GitOps & CI/CD Workflow (Method A - Recommended)
This project uses a modern **GitOps** architecture, meaning the state of the Git repository is the single source of truth for the Kubernetes cluster.

### Architecture Overview
1.  **Infrastructure (IaC)**: Managed by **Terraform**. It now bootstraps the entire cluster including Namespaces, **CloudNativePG Operator**, and the **ArgoCD Root Application**.
2.  **Continuous Integration (CI)**: **Jenkins** listens for code changes.
    - Runs **Terraform Apply** to ensure infrastructure/operators are up-to-date.
    - Runs integration/UI tests via Docker Compose.
    - Builds and pushes images to Docker Hub.
3.  **Continuous Deployment (CD)**: **Jenkins** updates the manifests in the `deploy` branch.
4.  **GitOps Sync**: **ArgoCD** (via the App-of-Apps pattern) automatically reconciles the cluster state.

### 🚀 Setup Guide (GitOps)

Follow these steps to deploy the stack using the **GitOps workflow**.

#### 1. Deploy the Infrastructure and Application
This stage installs the "engines" (Argo CD, Database Operator) and creates the namespaces.
Run Terraform from your local machine (or let Jenkins do it):
```bash
cd terraform
terraform init
terraform apply -auto-approve
```
> [!NOTE]
> **No manual `kubectl apply -f k8s/ --recursive` is needed!**
> Terraform now installs Argo CD and the "Root Application", which automatically and recursively deploys everything in the `k8s/` directory.

#### 2. One-Time Configuration (Manual)
Even with automation, you must perform these steps **once** to connect your tools to your specific accounts (GitHub, Docker Hub, etc.).

##### **A. Configure ArgoCD**
1.  **Get Admin Password**:
    ```bash
    (kubectl -n argo get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | 
    ForEach-Object { [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($_)) })
    ```
2.  **Access UI**:
    ```bash
    kubectl port-forward svc/argocd-server -n argo 8888:443
    ```
3.  **Repository Connection**: (Automatic) Jenkins now automatically connects your Git repository to Argo CD using your `git` credentials. No manual steps required.

##### **B. Setup Jenkins Pipeline**
1.  **Access Jenkins**: [http://localhost:8080](http://localhost:8080)
2.  **Create Pipeline**: New Item -> Pipeline -> Definition: "Pipeline script from SCM" -> Git URL.
3.  **Inject Credentials**: 
    Create the following credentials in Jenkins (referenced by `jenkinsfile`):
    *   `docker-hub-credentials` (Username/Password)
    *   `git` (Username / Personal Access Token)
    *   `gmail-auth` & `ngrok-token` (Secret Text)
    *   `kubeconfig` (Secret File - see Troubleshooting)
    
    > [!NOTE]
    > **Automatic Secret Injection**: Sensitive secrets like `ngrok-token` and `regcred` (Docker Hub) are **not stored in Git**. Jenkins automatically injects them into Kubernetes after ArgoCD syncs the manifests, ensuring secrets remain secure and up-to-date.

#### 3. Continuous Automation (Commit & Push)
Once the setup above is done, **everything else is automatic**. Every push to `main` will trigger the full pipeline, infrastructure updates, and GitOps sync.

---

## 🚀 Deployment Guide (Method B - Manual)

Follow these steps to deploy the entire stack manually from scratch on **Minikube** (without Jenkins/ArgoCD).

### 1. Start Minikube & Install Dependencies
```bash
# Start Minikube
minikube start

# Install CloudNativePG Operator (Required for Database Cluster)
kubectl apply --server-side -f https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/main/releases/cnpg-1.25.0.yaml
```

### 2. Build Images into Minikube
Since we use `imagePullPolicy: Never` for local performance, you must build the images directly into the Minikube internal registry:
```bash
# Build Frontend
minikube image build -t event-manager-frontend:latest ./frontend

# Build Backend
minikube image build -t event-manager-backend:latest ./backend

# Pull External Images (helps avoid connection issues later)
minikube image pull ngrok/ngrok:latest
```

### 3. Initialize Environment
```bash
# Create the project structure in Minikube for HostPath volumes
minikube ssh "sudo mkdir -p /project/frontend/src/background"

# Create Namespace
kubectl apply -f k8s/namespaces/
```

### 4. Deploy the Stack
You can now deploy all components using a recursive apply:
```bash
kubectl apply -f k8s/ --recursive
```

### 5. Verify & Access
```bash
# Watch pods until all are "Running"
kubectl get pods -A -w

# Access the Frontend
minikube service frontend -n event-manager

# Access Monitoring Tools
minikube service grafana     # Dashboard: Backend Monitoring (Auto-provisioned)
minikube service prometheus  # Targets: Check backend pods discovery
```

### 💡 Troubleshooting Common Issues

*   **ArgoCD stuck in "Progressing" (ngrok)**:
    This is usually because Minikube's `LoadBalancer` is waiting for an IP. Run:
    ```bash
    minikube tunnel
    ```
*   **Database Cluster degraded / Primary Missing**:
    If the CloudNativePG cluster gets out of sync (e.g., after a node restart), perform a "clean slate" recovery:
    ```bash
    kubectl delete cluster postgres-cluster -n rsvp-app
    kubectl delete pvc -n rsvp-app -l cnpg.io/cluster=postgres-cluster
    # ArgoCD will recreate them correctly starting from Instance 1
    ```
*   **ImagePullBackOff (Connection Refused)**:
    If a pod is stuck pulling an image, try pulling it manually: `minikube image pull <image-name>`.
*   **ContainerCreating (Volume Issues)**:
    If the backend is stuck, ensure the background directory exists inside Minikube:
    ```bash
    minikube ssh "sudo mkdir -p /project/frontend/src/background"
    ```
*   **Generic Reset**:
    If things get messy, you can always start fresh:
    ```bash
    minikube delete
    minikube start
    ```
*   **Connection Refused in Jenkins (Terraform/Kubectl)**:
    If you see `dial tcp: connect: connection refused` pointing to `host.docker.internal`, it usually means Minikube's API port has changed. **You must regenerate and re-upload the kubeconfig credential** as described in the "Kubernetes Access (Runtime Injection)" section whenever Minikube restarts.
*   **ArgoCD ComparisonError (RBAC/Forbidden)**:
    If you see `User ... cannot list resource "validatingadmissionpolicybindings"`, run this patch to fix compatibility with K8s 1.28+:
    ```bash
    kubectl patch clusterrole argocd-application-controller --type='json' -p='[{"op": "add", "path": "/rules/-", "value": {"apiGroups": ["admissionregistration.k8s.io"], "resources": ["validatingadmissionpolicybindings"], "verbs": ["list", "watch"]}}]'
    ```

---

### 📊 Monitoring & Observability

Our Kubernetes setup includes a fully automated monitoring stack designed for high-visibility and proactive health tracking:

*   **Prometheus**: 
    -   **Auto-Discovery**: Uses Kubernetes Service Discovery (RBAC enabled) to automatically find and scrape metrics from all backend replicas.
    -   **Dynamic Scraping**: Configured via a `ConfigMap` to target pods with the `app: backend` label on port `5000`.
*   **Grafana**: 
    -   **Instant Visualization**: Pre-provisioned with a "Backend Monitoring Dashboard".
    -   **Key Metrics**: Tracks real-time **Replica Count** and **Availability Status** (Up/Down) for each pod.
    -   **Automated Setup**: Data sources and dashboards are provisioned automatically on startup using YAML configurations.
*   **Health Awareness**: Integrated with Liveness and Readiness probes to ensure only healthy pods contribute to the metrics and receive traffic.

---

## 🏗️ Jenkins & Docker Integration (Windows Host)

This section explains how to set up a Jenkins environment capable of running Docker commands ("Docker-out-of-Docker"). You can choose between an automated setup using our custom image or a manual step-by-step approach.

### 🌟 Option A: Custom Jenkins Image (Automated & Recommended)
This is the fastest way to get started. We use a custom `Jenkins.Dockerfile` that pre-installs the Docker CLI and Docker Compose V2 plugin.

1.  **Launch the stack:**
    ```bash
    docker-compose -f docker-compose-jenkins.yaml up -d --build
    ```

**Benefits:**
*   **Zero-Config**: Docker and Docker Compose are ready for use immediately.
*   **Optimized Permissions**: Configured to handle the Docker socket (`/var/run/docker.sock`) right out of the box.
*   **Persistence**: Uses the `jenkins_home` volume for data reliability.

---

### 🛠️ Option B: Manual Setup (Step-by-Step)
Use this option if you prefer to configure a standard Jenkins image manually.

#### 1. Run Jenkins Container
To allow Jenkins to communicate with the Docker engine on your Windows host, you must mount the Docker socket and run the container as root.

Run this command in your terminal:

```bash
docker run -d -p 8080:8080 -p 50000:50000 --name jenkins -v /var/run/docker.sock:/var/run/docker.sock -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

### 2. Install Docker in Jenkins Container & Fix Permissions
We need to install the Docker CLI inside the Jenkins container and fix the socket permissions so Jenkins can run Docker commands.

1. Enter the container as root:
   ```bash
   docker exec -it -u root jenkins bash
   ```

2. Update package list:
   ```bash
   apt-get update
   ```

3. Install Docker:
   ```bash
   apt-get install -y docker.io
   ```

4. Fix permissions for the docker socket:
   ```bash
   chmod 666 /var/run/docker.sock
   ```


### 3. Install Docker Compose inside Jenkins
The standard Jenkins image doesn't include the Docker Compose plugin. Install it manually:

```bash
# Inside the Jenkins container (as root)
mkdir -p /usr/local/lib/docker/cli-plugins/
curl -SL https://github.com/docker/compose/releases/download/v2.24.1/docker-compose-linux-x86_64 -o /usr/local/lib/docker/cli-plugins/docker-compose
chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
```

Verify with:
```bash
docker compose version
```

### 4. Configure Credentials
1. Go to **Manage Jenkins** > **Credentials**.
2. Add a new **Username with password** credential.
3. ID: `gmail-auth`
4. Username: Your Gmail address
5. Password: Your Google App Password
6. ID: `ngrok-token`
7. Secret: Your [ngrok Authtoken](https://dashboard.ngrok.com/get-started/your-authtoken).

### 5. Kubernetes Access (Runtime Injection)
To allow Jenkins to deploy to your Minikube cluster, you must provide a "portable" kubeconfig file as a credential.

1.  **Generate Portable Config (One-Liner)**:
    Run this specific command in PowerShell. It flattens the local config, changes the IP to `host.docker.internal`, and disables TLS verification so it works inside the Jenkins container:
    ```powershell
    kubectl config view --flatten --minify | ForEach-Object { $_ -replace '127.0.0.1','host.docker.internal' -replace 'localhost','host.docker.internal' -replace 'certificate-authority-data:.*','insecure-skip-tls-verify: true' } | Out-File -Encoding ASCII kubeconfig_for_jenkins
    ```
    *This creates a file named `kubeconfig_for_jenkins` in your current folder.*

2.  **Upload to Jenkins**:
    *   Go to **Manage Jenkins** > **Credentials** > **Add Credentials**.
    *   **Kind**: `Secret File`.
    *   **File**: Upload the `kubeconfig_for_jenkins` file.
    *   **ID**: `kubeconfig`.
    *   **Description**: `Minikube Config for Jenkins`.

---

## 🧪 Testing

The project includes a comprehensive test suite to ensure stability across the API and the User Interface.

### 🔗 Integration Tests (`tests/integration_test.py`)
Focuses on the backend logic and third-party integrations.
*   **Health Checks**: Verifies all services are responsive.
*   **Email Workflow**: Uses **Mail.tm API** to generate temporary emails and verify that invitations, updates, and reminders are received with the correct content (including background images).
*   **Business Logic**: Tests mixed RSVP responses (Attending/Declining) and ensures the database updates correctly.
*   **API Coverage**: Validates location search and event management endpoints.

### 🎭 UI Tests (`tests/selenium_test.py`)
End-to-End browser automation using **Selenium**.
*   **Event Wizard Flow**: Simulates a complete user journey: selecting event types, filling details (with React-aware date selection), adding guests, and reviewing.
*   **RSVP Flow**: Automatically follows an invitation link, submits an RSVP, and verifies the dashboard reflects the change.
*   **CRUD Operations**: Verifies that editing an event correctly resets RSVP statuses and that deleting an event removes it from the UI.
*   **Advanced Features**: Tests report exporting and responsive layout transitions.

### 🚀 Running the Tests


#### Via Jenkins Pipeline
The `jenkinsfile` is pre-configured to:
1.  Set up a clean environment.
2.  Deploy the full Docker Compose stack.
3.  Inject credentials for SMTP and Ngrok.
4.  Execute both Integration and Selenium test stages.
5.  Report failures with detailed logs (and screenshot captures for Selenium).


