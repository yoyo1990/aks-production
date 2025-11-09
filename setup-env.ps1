# PowerShell script to set up environment and run terraform
# This solves all PATH issues

# Set up PATH with all required tools
$env:PATH += ";C:\Users\shove\AppData\Local\Microsoft\WinGet\Packages\Hashicorp.Terraform_Microsoft.Winget.Source_8wekyb3d8bbwe"
$env:PATH += ";C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin"

Write-Host "🔧 Environment Setup Complete!" -ForegroundColor Green
Write-Host "📁 Current Directory: $(Get-Location)" -ForegroundColor Yellow

# Test that tools are accessible
Write-Host "`n🧪 Testing Tools:" -ForegroundColor Cyan
try {
    $terraformVersion = & terraform version
    Write-Host "✅ Terraform: $($terraformVersion.Split("`n")[0])" -ForegroundColor Green
} catch {
    Write-Host "❌ Terraform not found" -ForegroundColor Red
}

try {
    $azVersion = & az version --output tsv --query '"azure-cli"'
    Write-Host "✅ Azure CLI: $azVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Azure CLI not found" -ForegroundColor Red
}

Write-Host "`n🚀 Ready to run Terraform commands!" -ForegroundColor Green
Write-Host "💰 Remember: 'terraform apply' creates REAL Azure resources and costs money!" -ForegroundColor Yellow