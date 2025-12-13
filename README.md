# 🎉 Event Manager System

![Event Manager Banner](https://img.shields.io/badge/Event-Manager-blueviolet?style=for-the-badge) ![Version](https://img.shields.io/badge/Version-1.0-blue?style=for-the-badge) ![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

A modern, full-stack application for managing events, invitations, and RSVPs. Built with a focus on user experience, localization (Hebrew/English), and seamless email integration.

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
*   **Ngrok** for external tunneling (optional)
*   **Prometheus** for metrics

---

## 📂 Project Structure

The project is organized for scalability and maintainability:

```plaintext
event-manager/
├── 🐳 docker-compose.yaml     # Main orchestration file
├── 📂 k8s/                    # Kubernetes Manifests (HA)
│   ├── 📂 namespaces/         # Namespace definition
│   ├── 📂 database/           # CloudNativePG Cluster
│   ├── 📂 backend/            # Deployment, Service, HPA
│   ├── 📂 frontend/           # Deployment, Service, HPA
│   ├── 📂 ngrok/              # External Access
│   └── 📂 chaos/              # Chaoskube Configuration
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
    ├── � vite.config.js      # Build Configuration
    ├── 📄 nginx.conf          # Web Server Config
    ├── 📄 Dockerfile          # Frontend Image
    ├── �📂 src/
    │   ├── 📂 background/     # Static background assets (Images)
    │   ├── 📂 components/
    │   │   ├── 📂 CreateEvent/ # Step wizard components
    │   │   ├── 📂 Dashboard/   # Stats, Tables, Modals
    │   │   ├── 📂 shared/      # Inputs, Buttons, Modal wrappers
    │   │   ├── 📄 Sidebar.jsx  # Navigation Sidebar
    │   │   ├── 📄 EventPreview.jsx # Live Preview Component
    │   │   └── 📄 ErrorBoundary.jsx # Error Handling
    │   ├── 📂 pages/
    │   │   ├── 📂 CreateEvent/ # Main creation view
    │   │   ├── 📂 Dashboard/
    │   │   │   ├── 📄 Dashboard.jsx      # Main View
    │   │   │   ├── 📄 useDashboard.js    # Logic Hook
    │   │   │   └── 📄 dashboardTranslations.js # Translations
    │   │   └── 📂 RSVP/        # Guest RSVP landing page
    │   ├── 📂 utils/          # Helpers & Translations
    │   ├── 📂 styles/
    │   │   ├── 📂 components/ # Scoped CSS (buttons, cards, forms)
    │   │   ├── 📂 layouts/    # Page layouts (dashboard, sidebar)
    │   │   ├── 📂 themes/     # Dark/Light mode definitions
    │   │   └── 📄 base.css    # Global Reset & Variables
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
# 🎉 Event Manager System

![Event Manager Banner](https://img.shields.io/badge/Event-Manager-blueviolet?style=for-the-badge) ![Version](https://img.shields.io/badge/Version-1.0-blue?style=for-the-badge) ![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

A modern, full-stack application for managing events, invitations, and RSVPs. Built with a focus on user experience, localization (Hebrew/English), and seamless email integration.

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
*   **Ngrok** for external tunneling (optional)
*   **Prometheus** for metrics

---

## 📂 Project Structure

The project is organized for scalability and maintainability:

```plaintext
event-manager/
├── 🐳 docker-compose.yaml     # Main orchestration file
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
    │   ├── 📂 components/
    │   │   ├── 📂 CreateEvent/ # Step wizard components
    │   │   ├── 📂 Dashboard/   # Stats, Tables, Modals
    │   │   ├── 📂 shared/      # Inputs, Buttons, Modal wrappers
    │   │   ├── 📄 Sidebar.jsx  # Navigation Sidebar
    │   │   ├── 📄 EventPreview.jsx # Live Preview Component
    │   │   └── 📄 ErrorBoundary.jsx # Error Handling
    │   ├── 📂 pages/
    │   │   ├── 📂 CreateEvent/ # Main creation view
    │   │   ├── 📂 Dashboard/
    │   │   │   ├── 📄 Dashboard.jsx      # Main View
    │   │   │   ├── 📄 useDashboard.js    # Logic Hook
    │   │   │   └── 📄 dashboardTranslations.js # Translations
    │   │   └── 📂 RSVP/        # Guest RSVP landing page
    │   ├── 📂 utils/          # Helpers & Translations
    │   ├── 📂 styles/
    │   │   ├── 📂 components/ # Scoped CSS (buttons, cards, forms)
    │   │   ├── 📂 layouts/    # Page layouts (dashboard, sidebar)
    │   │   ├── 📂 themes/     # Dark/Light mode definitions
    │   │   └── 📄 base.css    # Global Reset & Variables
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

### 🚀 Deploying to Kubernetes

1.  **Prerequisites**:
    *   Minikube / Kubernetes Cluster
    *   `kubectl` installed

2.  **Deploy Command**:
    ```bash
    # 1. Create Namespace
    kubectl apply -f k8s/namespaces/namespace.yaml

    # 2. Deploy Database (Wait for 3 pods to be Running)
    kubectl apply -f k8s/database/

    # 3. Deploy Application Services
    kubectl apply -f k8s/backend/
    kubectl apply -f k8s/frontend/
    kubectl apply -f k8s/ngrok/

    # 4. Enable Chaos (Optional)
    kubectl apply -f k8s/chaos/
    ```

3.  **Verify Status**:
    ```bash
    kubectl get pods -n event-manager -w
    ```
