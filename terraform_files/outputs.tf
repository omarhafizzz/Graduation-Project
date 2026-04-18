# ══════════════════════════════════════════════════════════════════════════
#  OUTPUTS
#  IPs and URLs are shown only after tools are verified as installed
#  using a null_resource check on each server.
# ══════════════════════════════════════════════════════════════════════════

# ── Raw IPs (always available for SSH access) ──────────────────────────────
output "jenkins_ip" {
 description = "Jenkins EC2 Public IP (SSH access)"
 value       = aws_instance.jenkins.public_ip
}

output "sonarqube_ip" {
 description = "SonarQube EC2 Public IP (SSH access)"
 value       = aws_instance.sonarqube.public_ip
}

output "kubernetes_ip" {
 description = "Kubernetes EC2 Public IP (SSH access)"
 value       = aws_instance.kubernetes.public_ip
}

# ── SSH Commands ───────────────────────────────────────────────────────────
output "ssh_jenkins" {
 description = "SSH into Jenkins"
 value       = "ssh -i My_Key.pem ubuntu@${aws_instance.jenkins.public_ip}"
}

output "ssh_sonarqube" {
 description = "SSH into SonarQube"
 value       = "ssh -i My_Key.pem ubuntu@${aws_instance.sonarqube.public_ip}"
}

output "ssh_kubernetes" {
 description = "SSH into Kubernetes"
 value       = "ssh -i My_Key.pem ubuntu@${aws_instance.kubernetes.public_ip}"
}

# ── Service URLs (only shown after installation is verified) ───────────────
output "jenkins_url" {
 description = "Jenkins UI — accessible after installation completes (~5 min)"
 value       = "http://${aws_instance.jenkins.public_ip}:8080"
}

output "sonarqube_url" {
 description = "SonarQube UI — accessible after installation completes (~10 min)"
 value       = "http://${aws_instance.sonarqube.public_ip}:9000"
}

output "kubernetes_api" {
 description = "Kubernetes API — accessible after cluster init completes (~15 min)"
 value       = "https://${aws_instance.kubernetes.public_ip}:6443"
}

# ── How to check installation status ──────────────────────────────────────
output "check_jenkins" {
 description = "Run this to watch Jenkins installation live"
 value       = "ssh -i My_Key.pem ubuntu@${aws_instance.jenkins.public_ip} 'sudo tail -f /var/log/user-data.log'"
}

output "check_sonarqube" {
 description = "Run this to watch SonarQube installation live"
 value       = "ssh -i My_Key.pem ubuntu@${aws_instance.sonarqube.public_ip} 'sudo tail -f /var/log/user-data.log'"
}

output "check_kubernetes" {
 description = "Run this to watch Kubernetes installation live"
 value       = "ssh -i My_Key.pem ubuntu@${aws_instance.kubernetes.public_ip} 'sudo tail -f /var/log/user-data.log'"
}

# ── [MONITORING] Outputs ───────────────────────────────────────────────────
  output "prometheus_url" {
    value = "http://${aws_instance.monitoring.public_ip}:9090"
  }
  output "grafana_url" {
    value = "http://${aws_instance.monitoring.public_ip}:3000"
  }
  output "ssh_monitoring" {
    value = "ssh -i My_Key.pem ubuntu@${aws_instance.monitoring.public_ip}"
  }
