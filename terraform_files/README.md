# ElectraVision – Terraform Infrastructure

## Structure
```
terraform/
├── main.tf               # VPC, subnets, SGs, EC2 instances
├── variables.tf          # All variables
├── outputs.tf            # Public IPs and URLs
└── scripts/
    ├── jenkins.sh        # Jenkins + Docker + Trivy + kubectl
    ├── sonarqube.sh      # SonarQube + PostgreSQL
    ├── kubernetes.sh     # Single-node K8s cluster (kubeadm + Calico)
    └── monitoring.sh     # Prometheus + Node Exporter + Grafana
```

## Prerequisites
- Terraform >= 1.3.0 installed
- AWS CLI configured (`aws configure`)
- Key pair `My_Key` exists in `eu-central-1`

## Usage

```bash
# 1. Initialize
terraform init

# 2. Preview what will be created
terraform plan

# 3. Deploy (takes ~5 min)
terraform apply -auto-approve

# 4. Destroy everything when done
terraform destroy -auto-approve
```

## Access URLs (shown after apply)
| Service     | URL                          | Default Credentials     |
|-------------|------------------------------|-------------------------|
| Jenkins     | http://<ip>:8080             | See initial password below |
| SonarQube   | http://<ip>:9000             | admin / admin           |
| Prometheus  | http://<ip>:9090             | —                       |
| Grafana     | http://<ip>:3000             | admin / admin           |
| K8s API     | https://<ip>:6443            | —                       |

## Get Jenkins Initial Password
```bash
ssh -i My_Key.pem ubuntu@<jenkins-ip>
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

## Notes
- All scripts log to `/var/log/user-data.log` on each instance
- Kubernetes is a single-node cluster (master + worker untainted)
- Prometheus is pre-configured with Grafana as default datasource
- Wait ~5 minutes after `apply` for all services to fully start
