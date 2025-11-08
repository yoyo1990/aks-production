variable "location" {
  description = "Azure region to deploy into"
  type        = string
  default     = "East US" # change as needed
}

variable "resource_group_name" {
  description = "Name for the resource group"
  type        = string
  default     = "rg-aks-prod"
}

variable "aks_name" {
  description = "Name for the AKS cluster"
  type        = string
  default     = "aks-prod-cluster"
}

variable "node_count" {
  description = "Initial node count for agent pool"
  type        = number
  default     = 2
}

variable "node_size" {
  description = "VM size for nodes"
  type        = string
  default     = "Standard_DS2_v2"
}

variable "acr_sku" {
  description = "ACR SKU"
  type        = string
  default     = "Basic"
}

variable "acr_name" {
  description = "ACR name (must be globally unique)"
  type        = string
  default     = "myacrprod" # change before apply
}
