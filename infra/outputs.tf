output "acr_login_server" {
  description = "ACR login server (use to tag images)"
  value       = azurerm_container_registry.acr.login_server
}

# Raw admin kubeconfig - be careful with secrets
output "kube_admin_config_raw" {
  description = "Raw admin kubeconfig for the AKS cluster (sensitive)"
  value       = azurerm_kubernetes_cluster.aks.kube_admin_config_raw
  sensitive   = true
}

output "aks_cluster_name" {
  value = azurerm_kubernetes_cluster.aks.name
}
