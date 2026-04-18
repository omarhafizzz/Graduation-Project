# ⚡ ElectraVision — Smart Grid Monitoring System

<div align="center">

<img width="1900" height="922" alt="Screenshot 2026-04-11 212150" src="https://github.com/user-attachments/assets/9a97a064-693e-4379-b76e-66e6af720620" />
<img width="1908" height="915" alt="Screenshot 2026-04-11 211918" src="https://github.com/user-attachments/assets/4bef6a1c-16a1-4f29-9143-72fe9b1ac73e" />
<img width="1906" height="920" alt="Screenshot 2026-04-11 212015" src="https://github.com/user-attachments/assets/3c64cb3f-f021-436a-918b-36c9b163f103" />
<img width="1900" height="922" alt="Screenshot 2026-04-11 212150" src="https://github.com/user-attachments/assets/0df39bb5-9142-447a-97f7-f3cd14470604" />
<img width="1905" height="916" alt="Screenshot 2026-04-11 212248" src="https://github.com/user-attachments/assets/582a1594-2fea-44df-9e90-523233ca2333" />
<img width="1891" height="917" alt="Screenshot 2026-04-11 212308" src="https://github.com/user-attachments/assets/e73eb9fe-b517-4da4-bfde-07bc3f000ade" />


**A real-time electrical grid monitoring dashboard with a full DevOps CI/CD pipeline on AWS**

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Application](#-application)
- [Infrastructure](#-infrastructure)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Monitoring](#-monitoring)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)

---

## 🔍 Overview

ElectraVision is a graduation project that combines **IoT-style electrical monitoring** with a **complete DevOps pipeline**. It simulates real-time electrical readings (voltage, current, power, frequency, energy, power factor) and displays them on a live dashboard — all deployed automatically to AWS using a Jenkins CI/CD pipeline.

### Key Features

- ⚡ Real-time electrical metrics dashboard
- 📊 Live charts, alerts, and data logs
- 🔄 Automated CI/CD pipeline (Jenkins)
- 🐳 Containerized with Docker
- ☸️ Orchestrated with Kubernetes
- 🔒 Security scanning with Trivy
- 📈 Code quality analysis with SonarQube
- 🏗️ Infrastructure as Code with Terraform
- 📉 Monitoring with Prometheus + Grafana
- 🗄️ Data persistence with AWS RDS MySQL

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  AWS Cloud (eu-central-1)                    │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                  VPC (10.0.0.0/16)                    │  │
│  │                                                        │  │
│  │  Public Subnet (10.0.1.0/24)                          │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐    │  │
│  │  │ Jenkins  │  │SonarQube │  │   Kubernetes     │    │  │
│  │  │t3.medium │  │t3.medium │  │   t3.medium      │    │  │
│  │  │  :8080   │  │  :9000   │  │  single-node     │    │  │
│  │  └──────────┘  └──────────┘  └──────────────────┘    │  │
│  │                                                        │  │
│  │  Private Subnets (10.0.10.0/24 | 10.0.11.0/24)       │  │
│  │  ┌───────────────────────────────────────────────┐    │  │
│  │  │           RDS MySQL (db.t3.micro)              │    │  │
│  │  └───────────────────────────────────────────────┘    │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| **Application** | Python, Flask |
| **Frontend** | HTML, CSS, JavaScript, Chart.js |
| **Containerization** | Docker |
| **Orchestration** | Kubernetes (kubeadm + Calico) |
| **CI/CD** | Jenkins |
| **Code Quality** | SonarQube |
| **Security Scan** | Trivy |
| **Container Registry** | Docker Hub |
| **Infrastructure** | AWS EC2, RDS, VPC |
| **IaC** | Terraform |
| **Monitoring** | Prometheus + Grafana |
| **Database** | MySQL (AWS RDS) |

---

## 📁 Project Structure

```
Graduation-project/
│
├── app.py                  # Flask API server
├── simulator.py            # Electrical data simulator
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container definition
├── Jenkinsfile             # CI/CD pipeline definition
│
├── templates/
│   └── index.html          # Live dashboard
│
├── k8s/
│   ├── deployment.yaml     # Kubernetes deployment
│   └── service.yaml        # Kubernetes service (NodePort)
│
└── terraform_files/
    ├── main.tf             # VPC, EC2, Security Groups
    ├── rds.tf              # RDS MySQL instance
    ├── variables.tf        # Input variables
    ├── outputs.tf          # Output values
    └── scripts/
        ├── jenkins.sh      # Jenkins auto-install
        ├── sonarqube.sh    # SonarQube auto-install
        ├── kubernetes.sh   # K8s cluster auto-setup
        └── monitoring.sh   # Prometheus + Grafana auto-install
```

---

## 💻 Application

### How it works

```
simulator.py  →  POST /data  →  app.py  →  RDS MySQL
                                   ↓
                              GET /data
                                   ↓
                            index.html (dashboard)
```

### Electrical Metrics Monitored

| Metric | Unit | Range |
|--------|------|-------|
| Voltage | V | 210 - 230 V |
| Current | A | 5 - 15 A |
| Power | W | Calculated (V × I × PF) |
| Frequency | Hz | 49.5 - 50.5 Hz |
| Energy | kWh | Accumulated |
| Power Factor | — | 0.80 - 0.99 |

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Dashboard UI |
| `POST` | `/data` | Receive sensor data |
| `GET` | `/data` | Get latest reading |

---

## 🏗️ Infrastructure

Infrastructure is fully managed by **Terraform**.

### EC2 Instances

| Server | Type | Purpose |
|--------|------|---------|
| Jenkins | t3.medium | CI/CD + Docker + Trivy + kubectl |
| SonarQube | t3.medium | Code quality (Docker Compose) |
| Kubernetes | t3.medium | Single-node cluster |
| Monitoring | t3.small | Prometheus + Grafana |

### Deploy Infrastructure

```bash
cd terraform_files/
terraform init
terraform plan
terraform apply -auto-approve
```

### Destroy Infrastructure

```bash
terraform destroy -auto-approve
```

---

## 🔄 CI/CD Pipeline

The Jenkins pipeline runs automatically on every push to `main`.

### Pipeline Stages

```
Clone → SonarQube Analysis → Quality Gate → Build Image
      → Trivy Scan → Push to DockerHub → Remove Image → Deploy to K8s
```

### Stage Details

| Stage | Description |
|-------|-------------|
| **Clone** | Pull latest code from GitHub |
| **SonarQube Analysis** | Scan Python code for bugs & vulnerabilities |
| **Quality Gate** | Fail pipeline if code quality is poor |
| **Build Image** | `docker build` the Flask app |
| **Trivy Scan** | Scan Docker image for CVEs |
| **Push to DockerHub** | Push `omarmo20/electravision:BUILD_NUMBER` |
| **Remove Image** | Clean up local image from Jenkins EC2 |
| **Deploy to K8s** | Rolling update deployment |

---

## 📊 Monitoring

Prometheus scrapes metrics from all servers every 15 seconds.

### Grafana Dashboards

| Dashboard | ID | What it shows |
|-----------|----|---------------|
| Node Exporter | 1860 | CPU, RAM, Disk for all servers |
| Jenkins | 9964 | Build stats, queue, executors |

### Access URLs

```
Prometheus : http://<monitoring-ip>:9090
Grafana    : http://<monitoring-ip>:3000
```

---

## 🚀 Getting Started

### Prerequisites

- AWS Account with CLI configured
- Terraform >= 1.3.0
- Key pair `My_Key` in `eu-central-1`

### Steps

**1. Clone the repo**

```bash
git clone https://github.com/OmarMo20/Graduation-project.git
cd Graduation-project
```

**2. Deploy infrastructure**

```bash
cd terraform_files/
terraform init
terraform apply -auto-approve
```

**3. Setup Jenkins**

- Open `http://<jenkins-ip>:8080`
- Install plugins: `Docker Pipeline`, `SonarQube Scanner`, `Kubernetes CLI`
- Add credentials: `dockerhub-credentials`, `kubeconfig`, `sonarqube-token`
- Configure SonarQube server URL in Jenkins System settings

**4. Run the pipeline**

- Create pipeline pointing to this repo
- Click **Build Now**

**5. Access the app**

```
http://<kubernetes-ip>:30080
```

---


## 👨‍💻 Author

**OUR TEAM** — Graduation Project 2025

---

<div align="center">
Built with ❤️ | ElectraVision v3.0
</div>
