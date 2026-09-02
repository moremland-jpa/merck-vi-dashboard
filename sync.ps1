# Sync latest memory files and push to GitHub
# Usage: .\sync.ps1
# Or with a custom commit message: .\sync.ps1 "Updated after Aug 28 transcript"

param([string]$Message = "Update dashboard data")

$ErrorActionPreference = "Stop"

$memoryDir = "C:\Users\MattOremland\.claude\projects\C--Users-MattOremland-OneDrive---JPA-Health-Sandbox-Merck\memory"
$dataDir = Join-Path $PSScriptRoot "data\memory"

$files = @(
    "congress-ai-status.md",
    "genesis-status.md",
    "mrl-debrief-status.md",
    "asset-reporting-status.md",
    "merck-stakeholders.md",
    "merck-meeting-cadence.md"
)

Write-Host "Copying latest memory files..." -ForegroundColor Cyan
foreach ($f in $files) {
    $src = Join-Path $memoryDir $f
    if (Test-Path $src) {
        Copy-Item $src (Join-Path $dataDir $f) -Force
        Write-Host "  $f" -ForegroundColor Green
    } else {
        Write-Host "  $f (not found, skipped)" -ForegroundColor Yellow
    }
}

Set-Location $PSScriptRoot

$changes = git diff --stat HEAD -- data/memory/
if (-not $changes) {
    Write-Host "`nNo changes detected in memory files. Nothing to push." -ForegroundColor Yellow
    exit 0
}

Write-Host "`nChanges detected:" -ForegroundColor Cyan
git diff --stat HEAD -- data/memory/

git add data/memory/
git commit -m $Message
git push

Write-Host "`nDone! Dashboard will auto-redeploy in ~1 minute." -ForegroundColor Green
