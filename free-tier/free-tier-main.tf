# Azure Free Tier AKS Setup - Uses free/cheap resources
# This configuration is designed to stay within Azure Free Tier limits

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Resource Group (FREE)
resource "azurerm_resource_group" "rg_free" {
  name     = "rg-aks-free-tier"
  location = "East US"  # Free tier available region
  
  tags = {
    Environment = "FreeTier"
    Project     = "BitcoinApp"
    CreatedBy   = "Terraform"
    CostCenter  = "Free"
  }
}

# Container Registry - Basic SKU (CHEAP - ~$5/month)
resource "azurerm_container_registry" "acr_free" {
  name                = "acrfreetier${random_string.unique.result}"
  resource_group_name = azurerm_resource_group.rg_free.name
  location           = azurerm_resource_group.rg_free.location
  sku                = "Basic"  # Cheapest option
  admin_enabled      = true

  tags = {
    Environment = "FreeTier"
    CostEstimate = "~$5/month"
  }
}

# Random string for unique names
resource "random_string" "unique" {
  length  = 4
  upper   = false
  special = false
}

# AKS Cluster - Free Tier (Control plane is FREE!)
resource "azurerm_kubernetes_cluster" "aks_free" {
  name                = "aks-free-cluster"
  location            = azurerm_resource_group.rg_free.location
  resource_group_name = azurerm_resource_group.rg_free.name
  dns_prefix          = "aks-free-${random_string.unique.result}"
  
  # FREE control plane!
  sku_tier = "Free"  

  default_node_pool {
    name       = "agentpool"
    node_count = 1  # Start with just 1 node to save costs
    vm_size    = "standard_g1"  # Available VM size from the error list
    
    # Enable autoscaling to save costs when not in use
    enable_auto_scaling = true
    min_count          = 1
    max_count          = 2  # Don't go crazy with scaling
    
    os_disk_size_gb = 30  # Smaller disk to save money
    os_disk_type    = "Managed"
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin    = "kubenet"  # Simpler, cheaper networking
    load_balancer_sku = "standard"
  }
  
  # Disable unnecessary features to save costs
  role_based_access_control_enabled = true
  
  tags = {
    Environment = "FreeTier"
    CostEstimate = "Control plane: FREE, Nodes: ~$30/month"
  }
}

# Role assignment for ACR (FREE)
resource "azurerm_role_assignment" "acr_pull_free" {
  principal_id                     = azurerm_kubernetes_cluster.aks_free.kubelet_identity[0].object_id
  role_definition_name             = "AcrPull"
  scope                           = azurerm_container_registry.acr_free.id
  skip_service_principal_aad_check = true
}

# Outputs
output "resource_group_name" {
  value = azurerm_resource_group.rg_free.name
}

output "acr_login_server" {
  value = azurerm_container_registry.acr_free.login_server
}

output "aks_cluster_name" {
  value = azurerm_kubernetes_cluster.aks_free.name
}

output "cost_estimate" {
  value = "Monthly cost: ACR Basic ~$5 + 1x Standard_B2s node ~$30 = ~$35/month total"
}

output "kube_config_raw" {
  value     = azurerm_kubernetes_cluster.aks_free.kube_config_raw
  sensitive = true
}