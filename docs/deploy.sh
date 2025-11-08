#!/usr/bin/env bash
set -euo pipefail

# Example deploy script (bash)
# 1) Run from project root after setting Azure subscription and authenticating
# 2) Edit infra/variables.tf to set a unique acr_name

# Terraform provision
cd infra
terraform init
terraform apply -auto-approve

# capture outputs
ACR=$(terraform output -raw acr_login_server)
KUBE_RAW=$(terraform output -raw kube_admin_config_raw)
cd ..

# write kubeconfig (optional)
echo "$KUBE_RAW" > /tmp/kubeconfig_aks
export KUBECONFIG=/tmp/kubeconfig_aks

# Build & push images
docker build -t ${ACR}/service-a:latest ./app-a
docker build -t ${ACR}/service-b:latest ./app-b

docker push ${ACR}/service-a:latest
docker push ${ACR}/service-b:latest

# Apply k8s manifests
kubectl apply -f k8s/

echo "Deployment complete. Get ingress address: kubectl get ingress services-ingress"
