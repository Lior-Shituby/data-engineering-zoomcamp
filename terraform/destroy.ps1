#!/usr/bin/env pwsh
# Safe wrapper for terraform destroy — previews and requires confirmation

Write-Host "`n WARNING: You are about to destroy all Terraform-managed resources.`n" -ForegroundColor Yellow

Write-Host "Previewing what will be destroyed...`n" -ForegroundColor Cyan
terraform plan -destroy

Write-Host "`n This will permanently delete the resources shown above." -ForegroundColor Red
Write-Host "Type 'destroy' to confirm, or anything else to cancel: " -ForegroundColor Red -NoNewline

$input = Read-Host

if ($input -ne "destroy") {
    Write-Host "`nCancelled. Nothing was destroyed." -ForegroundColor Green
    exit 0
}

Write-Host "`nProceeding with destroy...`n" -ForegroundColor Yellow
terraform destroy
